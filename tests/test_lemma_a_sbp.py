"""Lemma A and sharp L3. Not DA-NS-2. NS is not solved."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.core_tail_sbp import d_kappa, phi_e, phi_over_d  # noqa: E402
from ns_attacks.lemma_a_sbp import (  # noqa: E402
    C_kappa,
    numeric_L1_L3,
    sympy_frozen_equals_W,
    sympy_lemma_A,
)
from ns_attacks.narrow_het_residual import moments  # noqa: E402


class LemmaATests(unittest.TestCase):
    def test_C_kappa_formula_and_bound(self):
        s = sympy_lemma_A()
        self.assertTrue(s["lemma_A"])
        self.assertTrue(s["C_le_1"])
        self.assertTrue(s["C_equals_ratio_at_gap"])
        self.assertEqual(s["lim_inf_C"], "1")
        self.assertTrue(s["one_minus_C_positive"])
        for kappa in (0.5, 1.0, 2.0, 7.0, 50.0):
            C = C_kappa(kappa)
            self.assertLessEqual(C, 1.0)
            self.assertAlmostEqual(C, phi_over_d(1.0, kappa), places=12)
            self.assertAlmostEqual(
                1.0 - C,
                (kappa + 0.5) / (kappa + 1.0) ** 2,
                places=12,
            )

    def test_pointwise_phi_le_d_on_torus(self):
        for kappa in (1.0, 3.0, 11.0):
            for m in (1.0, 1.3, 2.0, kappa, 2.5 * kappa, 40.0):
                self.assertLessEqual(phi_e(m, kappa), d_kappa(m, kappa) + 1e-12)

    def test_shell_and_infinity_are_strictly_inside(self):
        self.assertAlmostEqual(phi_over_d(6.0, 6.0), 5.0 / (8.0 * 36.0), places=12)
        self.assertLess(phi_over_d(6.0, 6.0), C_kappa(6.0))
        self.assertLess(phi_over_d(200.0, 6.0), 1e-3)


class FrozenWTests(unittest.TestCase):
    def test_cross_term_is_barycenter(self):
        s = sympy_frozen_equals_W()
        self.assertTrue(s["cross_is_2_times_barycenter_factor"])
        self.assertIn("W_{λ_e}", s["identity"])

    def test_D_frozen_equals_W_and_L3(self):
        for seed in range(6):
            row = numeric_L1_L3(seed=seed)
            self.assertTrue(row["L1"])
            self.assertTrue(row["frozen_eq_W"])
            self.assertTrue(row["L3_sharp"])
            self.assertLessEqual(row["Phi_over_Y"], row["Ds_over_Y"] + row["zeta2"] + 1e-10)

    def test_moments_kill_the_cross_term(self):
        eigs = [1.0, 4.0, 9.0, 25.0]
        mass = [0.5, 0.2, 0.2, 0.1]
        m = moments(eigs, mass)
        cross = sum(a * (a - m["Lambda"]) * w for a, w in zip(eigs, mass))
        self.assertAlmostEqual(cross, 0.0, places=12)
        self.assertAlmostEqual(m["Y"] - m["Lambda"] * m["X"], 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
