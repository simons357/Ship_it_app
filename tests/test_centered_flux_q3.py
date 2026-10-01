#!/usr/bin/env python3
"""Independent checks of the 1 Oct 2026 centered-flux / q=3 note.

Exact Q[i] convolution. No claim that Lemma★ or NS is closed.
"""

from __future__ import annotations

import pathlib
import sys
import unittest
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.centered_flux_q3 import (  # noqa: E402
    NEAR_SHELL_EPSILONS,
    C,
    Ds_double_sum,
    Ds_two_shell,
    Ds_variance_sum,
    I,
    Lambda_prime_from_XY,
    Lambda_prime_rhs,
    am_gm_remainder,
    amplitude_scaling_kill,
    closed_Ds_near_shell,
    closed_Tc_near_shell,
    flux_moments,
    grad_L3,
    moments,
    near_shell_triad,
    probe_near_shell,
    scale_field,
    shell_energies,
)


class TestExactFluxAlgebra(unittest.TestCase):
    def setUp(self) -> None:
        self.field = near_shell_triad(Fraction(1, 8))
        self.flux = flux_moments(self.field)

    def test_energy_cancellation_is_exactly_zero(self) -> None:
        self.assertEqual(self.flux["sum_Tk"], Fraction(0))

    def test_boundary_term_vanishes(self) -> None:
        self.assertEqual(self.flux["boundary_Lambda_sum_Tk"], Fraction(0))

    def test_N_equals_centered_rewrite(self) -> None:
        self.assertEqual(self.flux["N"], self.flux["N_centered"])

    def test_Tc_three_writings_agree(self) -> None:
        self.assertEqual(self.flux["Tc"], self.flux["Tc_direct"])
        self.assertEqual(self.flux["Tc"], self.flux["Tc_from_quad"])

    def test_Ds_equivalent_forms(self) -> None:
        Ds = self.flux["Ds"]
        self.assertEqual(Ds_variance_sum(self.field), Ds)
        self.assertEqual(Ds_double_sum(self.field), Ds)
        shells = shell_energies(self.field)
        self.assertEqual(len(shells), 2)
        (alpha, e_a), (beta, e_b) = list(shells.items())
        self.assertEqual(Ds_two_shell(Fraction(alpha), Fraction(beta), e_a, e_b), Ds)

    def test_barycenter_recovered_from_energy_moments(self) -> None:
        nu = Fraction(3, 10)
        lhs = Lambda_prime_rhs(self.flux["Tc"], self.flux["Ds"], self.flux["X"], nu)
        rhs = Lambda_prime_from_XY(
            self.flux["N"],
            self.flux["M"],
            self.flux["X"],
            self.flux["Y"],
            self.flux["Z"],
            nu,
        )
        self.assertEqual(lhs, rhs)

    def test_zero_potential_supplies_no_Tc_bound(self) -> None:
        # Σ T_k = 0 is exact and independent of how large T_c is.
        self.assertEqual(self.flux["sum_Tk"], 0)
        self.assertNotEqual(self.flux["Tc"], 0)


class TestNearShellObstruction(unittest.TestCase):
    def test_five_exact_epsilons(self) -> None:
        self.assertEqual(len(NEAR_SHELL_EPSILONS), 5)
        rows = [probe_near_shell(eps, n_grid=24) for eps in NEAR_SHELL_EPSILONS]
        ratios = [abs(Fraction(r.abs_Tc_over_Ds)) for r in rows]
        for prev, nxt in zip(ratios, ratios[1:]):
            self.assertLess(prev, nxt)
        # Leading orders: T_c / ε stays O(1) and nonzero; D_s / ε² stays O(1).
        for r, eps in zip(rows, NEAR_SHELL_EPSILONS):
            self.assertEqual(Fraction(r.Ds), closed_Ds_near_shell(eps))
            self.assertNotEqual(Fraction(r.Tc), 0)
            self.assertGreater(abs(Fraction(r.Tc_over_eps)), 1)
            self.assertGreater(Fraction(r.Ds_over_eps2), 100)

    def test_closed_Ds_formula(self) -> None:
        eps = Fraction(1, 4)
        field = near_shell_triad(eps)
        self.assertEqual(moments(field)["Ds"], Fraction(256) * eps * eps / (1 + eps * eps))

    def test_closed_Tc_formula(self) -> None:
        for eps in NEAR_SHELL_EPSILONS:
            flux = flux_moments(near_shell_triad(eps))
            self.assertEqual(flux["Tc"], closed_Tc_near_shell(eps))
            self.assertEqual(flux["Ds"], closed_Ds_near_shell(eps))
            self.assertEqual(abs(flux["Tc"]) / flux["Ds"], (2 + eps * eps) / (4 * eps))

    def test_linear_viscosity_bound_impossible(self) -> None:
        # A constant that works at the largest ε already fails at the smallest.
        nu = Fraction(1)
        large = flux_moments(near_shell_triad(NEAR_SHELL_EPSILONS[0]))
        small = flux_moments(near_shell_triad(NEAR_SHELL_EPSILONS[-1]))
        C = abs(large["Tc"]) / (nu * large["Ds"])
        self.assertGreater(abs(small["Tc"]), C * nu * small["Ds"])

    def test_sqrt_Ds_ratio_stays_bounded_on_family(self) -> None:
        values = []
        for eps in NEAR_SHELL_EPSILONS:
            flux = flux_moments(near_shell_triad(eps))
            values.append(abs(float(flux["Tc"])) / float(flux["Ds"]) ** 0.5)
        # Same leading order: values stay in a tight band, unlike T_c / D_s.
        self.assertLess(max(values) / min(values), 2.0)


class TestStatedQ3Target(unittest.TestCase):
    def test_amplitude_kills_universal_constant(self) -> None:
        rows = amplitude_scaling_kill(eps=Fraction(1, 8), amps=(1, 2, 4))
        rho = [r["rho_q3"] for r in rows]
        self.assertGreater(rho[1], 1.8 * rho[0])
        self.assertGreater(rho[2], 1.8 * rho[1])
        for r in rows:
            self.assertAlmostEqual(r["rho_q3_over_amp"], rows[0]["rho_q3_over_amp"], places=5)

    def test_homogeneous_repair_is_amplitude_invariant(self) -> None:
        base = near_shell_triad(Fraction(1, 8))
        rhos = []
        for amp in (1, 2, 4):
            field = scale_field(base, amp)
            flux = flux_moments(field)
            g3 = grad_L3(field, n_grid=24)
            rho_Y = abs(float(flux["Tc"])) / (
                g3 * float(flux["Y"]) ** 0.5 * float(flux["Ds"]) ** 0.5
            )
            rhos.append(rho_Y)
        self.assertAlmostEqual(rhos[0], rhos[1], places=5)
        self.assertAlmostEqual(rhos[1], rhos[2], places=5)

    def test_am_gm_algebra_only(self) -> None:
        rem = am_gm_remainder(C=2.0, grad_L3_norm=3.0, nu=0.5)
        self.assertAlmostEqual(rem, (4.0 * 9.0) / 2.0)
        # The implication needs the hypothesis. Hypothesis is not a theorem.
        self.assertGreater(rem, 0)

    def test_honesty_lock(self) -> None:
        note = (ROOT / "docs" / "ns-review" / "CENTERED-FLUX-Q3-2026-10-01.md").read_text()
        self.assertIn("NOT proved", note)
        self.assertIn("NS NOT solved", note)
        self.assertIn("KILLED", note)
        self.assertNotIn("Clay is closed", note)
        script = (ROOT / "scripts" / "ns_attacks" / "centered_flux_q3.py").read_text()
        self.assertIn("ns_solved", script)
        self.assertIn("False", script)


class TestComplexRational(unittest.TestCase):
    def test_i_squared(self) -> None:
        self.assertEqual((I * I).re, Fraction(-1))
        self.assertEqual((I * I).im, Fraction(0))

    def test_division(self) -> None:
        z = C(2, 1) / C(1, 1)
        self.assertEqual(z.re, Fraction(3, 2))
        self.assertEqual(z.im, Fraction(-1, 2))


if __name__ == "__main__":
    unittest.main()
