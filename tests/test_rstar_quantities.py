#!/usr/bin/env python3
"""Tests: exact Fourier / R_★ quantities (Lemma★ shape form)."""

from __future__ import annotations

import unittest

from domain_architect.rstar_quantities import (
    DOC_PATH,
    HARD_RULES,
    R_star,
    T_c_from_signed_triads,
    TriadContribution,
    D_s_moment,
    D_s_pairwise,
    D_s_variance,
    exact_formula_inventory,
    lambda_prime,
    shape_form_holds,
    spectral_moments,
    two_shell_D_s,
    verify_two_shell_vs_sum,
)


class TestSpectralMoments(unittest.TestCase):
    def test_single_shell_D_s_zero(self):
        m = spectral_moments({1.0: 2.0, 1: 0.0})  # one live shell λ=1
        # only λ=1 with energy 2
        m = spectral_moments({1: 2.0})
        self.assertAlmostEqual(m.energy_l2, 2.0)
        self.assertAlmostEqual(m.X, 2.0)
        self.assertAlmostEqual(m.Y, 2.0)
        self.assertAlmostEqual(m.Z, 2.0)
        self.assertAlmostEqual(m.Lambda, 1.0)
        self.assertAlmostEqual(m.D_s_form1, 0.0)
        self.assertAlmostEqual(m.D_s_form2, 0.0)
        self.assertAlmostEqual(m.D_s_form3, 0.0)
        self.assertTrue(m.forms_agree())

    def test_three_forms_agree_two_shell(self):
        energies = {1.0: 3.0, 4.0: 1.0}
        m = spectral_moments(energies)
        self.assertTrue(m.forms_agree())
        self.assertAlmostEqual(m.D_s_form1, m.D_s_form2)
        self.assertAlmostEqual(m.D_s_form1, m.D_s_form3)
        self.assertGreater(m.D_s, 0.0)
        self.assertAlmostEqual(D_s_moment(energies), m.D_s_form1)
        self.assertAlmostEqual(D_s_variance(energies), m.D_s_form2)
        self.assertAlmostEqual(D_s_pairwise(energies), m.D_s_form3)

    def test_wavevector_keys(self):
        # |k|^2: (1,0,0)->1, (0,2,0)->4
        energies = {(1, 0, 0): 1.0, (-1, 0, 0): 1.0, (0, 2, 0): 0.5}
        m = spectral_moments(energies)
        self.assertAlmostEqual(m.energy_l2, 2.5)
        self.assertAlmostEqual(m.X, 1.0 * 1.0 + 1.0 * 1.0 + 4.0 * 0.5)
        self.assertTrue(m.forms_agree())

    def test_Lambda_equals_Y_over_X(self):
        m = spectral_moments({2.0: 1.0, 5.0: 2.0})
        self.assertAlmostEqual(m.Lambda, m.Y / m.X)


class TestTwoShell(unittest.TestCase):
    def test_closed_form_matches_sum(self):
        alpha, beta = 1.0, 9.0
        ea, eb = 2.0, 0.5
        closed = two_shell_D_s(alpha, beta, ea, eb)
        expected = (alpha * beta * (alpha - beta) ** 2 * ea * eb) / (
            alpha * ea + beta * eb
        )
        self.assertAlmostEqual(closed, expected)
        v = verify_two_shell_vs_sum(alpha, beta, ea, eb)
        self.assertTrue(v["ok"])
        self.assertAlmostEqual(v["two_shell_closed"], v["D_s_form1"])

    def test_degenerate_same_shell(self):
        self.assertAlmostEqual(two_shell_D_s(3.0, 3.0, 1.0, 2.0), 0.0)


class TestTcSigned(unittest.TestCase):
    def test_never_abs_raw_pieces(self):
        # signed pieces that would cancel under abs wrongly
        pieces = [1.5, -1.0, -0.25]
        res = T_c_from_signed_triads(pieces, Lambda=2.0)
        self.assertAlmostEqual(res.T_c, 0.25)
        self.assertTrue(res.complete)
        self.assertFalse(res.used_restricted_channel)

    def test_from_mode_contributions(self):
        # two modes λ=1, λ=4; Λ = Y/X with equal |v|^2=1 → X=5, Y=17, Λ=17/5
        lambdas = {"lo": 1.0, "hi": 4.0}
        X = 1.0 * 1.0 + 4.0 * 1.0
        Y = 1.0 + 16.0
        Lam = Y / X
        contribs = [
            TriadContribution(p="a", q="b", k="lo", value=0.5),
            TriadContribution(p="c", q="d", k="hi", value=-0.2),
        ]
        res = T_c_from_signed_triads(
            contribs, lambdas=lambdas, X=X, Y=Y
        )
        # T_lo=0.5, T_hi=-0.2
        # N = 1*0.5 + 4*(-0.2) = 0.5 - 0.8 = -0.3
        # M = 1*0.5 + 16*(-0.2) = 0.5 - 3.2 = -2.7
        # T_c = M - Λ N
        N = -0.3
        M = -2.7
        expected = M - Lam * N
        self.assertAlmostEqual(res.N, N)
        self.assertAlmostEqual(res.M, M)
        self.assertAlmostEqual(res.T_c, expected)
        self.assertTrue(res.complete)

    def test_hh_to_l_restricted_refused(self):
        bad = [
            TriadContribution(p=1, q=2, k=3, value=1.0, channel="HH->L"),
        ]
        with self.assertRaises(ValueError):
            T_c_from_signed_triads(bad, Lambda=1.0)
        diag = T_c_from_signed_triads(bad, Lambda=1.0, allow_restricted=True)
        self.assertTrue(diag.used_restricted_channel)
        self.assertFalse(diag.complete)


class TestRStar(unittest.TestCase):
    def test_quotient_with_T_c_plus(self):
        # T_c negative → R_★ = 0
        out = R_star(T_c=-2.0, D_s=1.0, energy_l2=2.0, Y=3.0)
        self.assertTrue(out["ok"])
        self.assertAlmostEqual(out["R_star"], 0.0)
        self.assertAlmostEqual(out["T_c_plus"], 0.0)

        out2 = R_star(T_c=3.0, D_s=1.0, energy_l2=2.0, Y=3.0)
        self.assertAlmostEqual(out2["R_star"], 9.0 / 6.0)
        self.assertFalse(out2["uniform_bound"])
        self.assertFalse(out2["ns_solved"])

    def test_D_s_zero_T_c_positive_dead(self):
        out = R_star(T_c=1.0, D_s=0.0, energy_l2=1.0, Y=1.0)
        self.assertIn("DEAD", out["kill"] or "")

    def test_pure_single_shell_not_kill(self):
        out = R_star(T_c=0.0, D_s=0.0, energy_l2=1.0, Y=1.0)
        self.assertIn("NOT_KILL", out["kill"] or "")

    def test_incomplete_T_c_refused(self):
        out = R_star(T_c=1.0, D_s=1.0, energy_l2=1.0, Y=1.0, complete_T_c=False)
        self.assertIsNone(out["R_star"])
        self.assertFalse(out["ok"])
        self.assertIn("REFUSE", out["reason"])


class TestSignCheckAndInventory(unittest.TestCase):
    def test_lambda_prime(self):
        # Λ' = (2/X)(T_c - ν D_s)
        val = lambda_prime(T_c=4.0, nu=0.5, D_s=2.0, X=2.0)
        self.assertAlmostEqual(val, (2.0 / 2.0) * (4.0 - 0.5 * 2.0))

    def test_shape_form_holds_evidence_only(self):
        chk = shape_form_holds(T_c=1.0, D_s=1.0, energy_l2=1.0, Y=1.0, theta=1.0, C_0=1.0)
        self.assertTrue(chk["holds"])
        self.assertTrue(chk["evidence_only"])
        self.assertFalse(chk["proof"])
        self.assertFalse(chk["ns_solved"])

    def test_inventory_lock_in(self):
        inv = exact_formula_inventory()
        self.assertEqual(inv["doc"], DOC_PATH)
        self.assertTrue(inv["shape_statement"])
        self.assertFalse(inv["ns_solved"])
        self.assertFalse(inv["sfe"])
        self.assertIn("Z - Lambda*Y", inv["D_s_forms"][0])
        self.assertIn("SIGNED", inv["nonlinear"]["T_k"])
        for rule in HARD_RULES:
            self.assertIn(rule, inv["hard_rules"])


class TestLemmaStarSoTPointer(unittest.TestCase):
    def test_inventory_points_at_full_shape_sot(self):
        inv = exact_formula_inventory()
        self.assertEqual(inv["doc"], "docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md")
        self.assertTrue(inv["full_lemma"])
        self.assertFalse(inv["K_alpha_beta_is_full_star"])
        self.assertIn("-<B(v,v), A(A-Lambda)v>", inv["nonlinear"]["T_c"])
        self.assertIn("K_{α,β}", " ".join(inv["hard_rules"]))

    def test_lemma_star_quantities_match_sot_tc(self):
        from domain_architect.lemma_star import analyze_lemma_star

        report = analyze_lemma_star()
        self.assertIn("A(A-Lambda)", report.quantities["T_c"])
        self.assertFalse(report.ns_solved)
        joined = " ".join(report.notes)
        self.assertIn("K_", joined)
        self.assertIn("restricted", joined.lower())


if __name__ == "__main__":
    unittest.main()
