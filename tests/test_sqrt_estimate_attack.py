#!/usr/bin/env python3
"""Exact identities and small-case board for the unproved square-root candidate.

A passing suite certifies the tested Fourier identities and the certified
||∇u||_3 bookkeeping.  It does not prove the uniform estimate.
"""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.exact_fourier import (  # noqa: E402
    Field,
    GQ,
    I,
    ONE,
    cascade,
    certified_grad_l3,
    integer_perp,
    lam,
    moments,
    project_perp,
    shell_energy,
    two_shell_D_s,
    verify_identities,
    vdot_k,
    gq_vec,
)
from ns_attacks.sqrt_estimate_attack import (  # noqa: E402
    coherent_affine_packet,
    dense_coordinated_packet,
    main as attack_main,
    near_shell_obstruction_rows,
    near_shell_several_triads,
    run_board,
    separated_varied_amplitudes,
)


def _single_pair(k, amp=Fraction(1)) -> Field:
    f = Field()
    n = integer_perp(k)
    f.set_mode(k, gq_vec((amp * n[0], amp * n[1], amp * n[2])))
    return f


class TestGaussianRational(unittest.TestCase):
    def test_mul_div_roundtrip(self):
        z = GQ(Fraction(2, 3), Fraction(-5, 7))
        w = z * I
        self.assertEqual(w / I, z)
        self.assertEqual(z.conj().conj(), z)
        self.assertEqual((z * z.conj()).im, 0)
        self.assertEqual((z * z.conj()).re, z.abs2())


class TestLinearIdentities(unittest.TestCase):
    def test_single_shell_D_s_zero_and_T_c_zero(self):
        f = _single_pair((1, 2, 0))
        f.check_invariants()
        mom = moments(f)
        cas = cascade(f, mom.Lambda)
        self.assertEqual(mom.D_s, 0)
        self.assertEqual(mom.Ds_variance, 0)
        self.assertEqual(mom.Ds_pairwise, 0)
        self.assertEqual(cas.T_c, 0)
        self.assertEqual(cas.sum_T, 0)
        self.assertTrue(verify_identities(f).ok)

    def test_two_shell_closed_form(self):
        f = near_shell_several_triads(Fraction(1, 4))
        mom = moments(f)
        e5 = shell_energy(f, 5)
        e10 = shell_energy(f, 10)
        self.assertEqual(e5 + e10, mom.E)
        self.assertEqual(two_shell_D_s(5, 10, e5, e10), mom.D_s)
        self.assertEqual(mom.Ds_moment, mom.Ds_variance)
        self.assertEqual(mom.Ds_moment, mom.Ds_pairwise)

    def test_divergence_free_and_reality(self):
        f = dense_coordinated_packet(1)
        f.check_invariants()
        for k, vk in f.modes.items():
            self.assertEqual(vdot_k(k, vk).abs2(), 0)
            self.assertGreater(lam(k), 0)


class TestCascadeIdentities(unittest.TestCase):
    def test_T_c_equals_M_minus_Lambda_N(self):
        for builder in (
            lambda: near_shell_several_triads(Fraction(1, 2)),
            lambda: separated_varied_amplitudes(Fraction(1, 4)),
            lambda: dense_coordinated_packet(1),
            lambda: coherent_affine_packet(2, Fraction(1, 2)),
        ):
            f = builder()
            report = verify_identities(f)
            self.assertTrue(report.ok, report.failures)
            mom = moments(f)
            cas = cascade(f, mom.Lambda)
            self.assertEqual(cas.T_c, cas.T_c_from_MN)
            self.assertEqual(cas.sum_T, 0)

    def test_grad_spectrum_zero_mode_is_X(self):
        f = separated_varied_amplitudes(Fraction(4))
        mom = moments(f)
        cas = cascade(f, mom.Lambda)
        cert = certified_grad_l3(f, mom, cas)
        self.assertEqual(cert.c0_minus_X, 0)
        self.assertGreaterEqual(cert.L4_fourth, 0)

    def test_Q_lb_does_not_exceed_Q_ub(self):
        f = near_shell_several_triads(Fraction(1))
        cert = certified_grad_l3(f)
        self.assertFalse(cert.vacuous)
        self.assertLessEqual(cert.Q_lb_sixth, cert.Q_ub_sq ** 3)

    def test_amplitude_invariance_of_certified_Q(self):
        f = near_shell_several_triads(Fraction(1, 2))
        g = f.scale(3)
        cf = certified_grad_l3(f)
        cg = certified_grad_l3(g)
        self.assertEqual(cf.Q_ub_sq, cg.Q_ub_sq)
        self.assertEqual(cf.Q_lb_sixth, cg.Q_lb_sixth)
        self.assertEqual(cascade(g, moments(g).Lambda).T_c, 27 * cascade(f, moments(f).Lambda).T_c)

    def test_Leray_stays_in_Q_i(self):
        w = project_perp((2, 1, 0), gq_vec((1, 1, 1)))
        self.assertEqual(vdot_k((2, 1, 0), w).abs2(), 0)
        # λ=5, so components live in Q
        for comp in w:
            self.assertIsInstance(comp.re, Fraction)
            self.assertIsInstance(comp.im, Fraction)


class TestNearShellObstruction(unittest.TestCase):
    def test_square_root_is_motivated_not_proved(self):
        rows = near_shell_obstruction_rows()
        ratios = []
        linear = []
        for row, report, extra in rows:
            self.assertTrue(report.ok, report.failures)
            self.assertEqual(extra["two_shell_D_s_check"], row.D_s)
            if extra["T_c_sq_over_D_s"] is None:
                continue
            ratios.append(Fraction(extra["T_c_sq_over_D_s"]))
            linear.append(Fraction(extra["T_c_sq_over_D_s_sq"]))
        self.assertGreaterEqual(len(ratios), 3)
        # T_c^2 / D_s stays within a fixed factor of the coarsest sample.
        # T_c^2 / D_s^2 grows as the satellite shrinks (linear-in-D_s dies).
        self.assertLess(max(ratios) / min(ratios), Fraction(1000))
        self.assertGreater(linear[-1], linear[0])
        self.assertGreater(linear[-1] / linear[0], Fraction(10))


class TestFamiliesAndScript(unittest.TestCase):
    def test_all_three_priority_families_verify(self):
        fields = [
            near_shell_several_triads(Fraction(1, 8), phase=I),
            separated_varied_amplitudes(Fraction(1, 16)),
            dense_coordinated_packet(1),
            coherent_affine_packet(3, Fraction(1, 2)),
        ]
        for f in fields:
            report = verify_identities(f)
            self.assertTrue(report.ok, report.failures)
            self.assertGreater(f.energy(), 0)

    def test_board_and_cli_verify_identities_only(self):
        payload = run_board()
        self.assertTrue(payload["identities_verified"], payload["identity_failures"])
        self.assertEqual(payload["status"], "UNPROVED CANDIDATE")
        self.assertEqual(payload["uniform_inequality"], "SEPARATE PROOF OBLIGATION")
        self.assertEqual(payload["time_budget"], "SEPARATE PROOF OBLIGATION")
        families = {rec["family"] for rec in payload["cases"]}
        self.assertIn("near_shell_triads", families)
        self.assertIn("separated_amplitudes", families)
        self.assertIn("dense_box_packet", families)
        self.assertIn("dense_affine_packet", families)
        self.assertEqual(attack_main([]), 0)


if __name__ == "__main__":
    unittest.main()
