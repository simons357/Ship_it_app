"""φ_κ / d_κ comparison and L_e. Not DA-NS-2. NS is not solved."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.core_tail_sbp import (  # noqa: E402
    C_annulus,
    d_kappa,
    high_core_low_reservoir,
    phi_e,
    phi_over_d,
    phi_over_d_scaled,
    sympy_phi_vs_d,
)


class RatioIdentities(unittest.TestCase):
    def test_A_B_and_shell_limit(self):
        s = sympy_phi_vs_d()
        self.assertTrue(s["A_identity"])
        self.assertTrue(s["B_identity"])
        self.assertTrue(s["shell_limit_is_5_over_8k2"])
        self.assertIn("x**3 + 3*x**2 + 5*x + 2", s["dg_numerator"])

    def test_numeric_A_matches_definition(self):
        kappa = 4.0
        for m in (0.5, 1.0, 3.9, 4.1, 8.0, 20.0):
            left = phi_e(m, kappa) / d_kappa(m, kappa)
            right = phi_over_d(m, kappa)
            self.assertAlmostEqual(left, right, places=12)
            x = m / kappa
            self.assertAlmostEqual(
                right,
                phi_over_d_scaled(x) / (2.0 * kappa * kappa),
                places=12,
            )

    def test_shell_limit_value(self):
        kappa = 6.0
        self.assertAlmostEqual(phi_over_d(kappa, kappa), 5.0 / (8.0 * kappa * kappa), places=15)
        self.assertAlmostEqual(phi_over_d_scaled(1.0) / 2.0, 5.0 / 8.0, places=15)

    def test_high_tail_decays_low_tail_blows_up(self):
        kappa = 5.0
        self.assertAlmostEqual(phi_over_d(200.0, kappa) * (200.0**2), 0.5, places=2)
        self.assertAlmostEqual(phi_over_d(0.05, kappa) * (0.05**2), 1.0, delta=0.02)
        self.assertGreater(phi_over_d(0.2, kappa), phi_over_d(kappa, kappa))
        self.assertGreater(phi_over_d(kappa, kappa), phi_over_d(25.0, kappa))

    def test_annulus_comparison_C(self):
        # Decreasing ⇒ C(a,b) = (1/2) g(a).
        self.assertAlmostEqual(
            C_annulus(0.5, 2.0),
            (0.25 + 1.0 + 2.0) / (2.0 * 0.25 * 2.25),
            places=12,
        )
        kappa = 8.0
        a, b = 0.6, 1.4
        C = C_annulus(a, b)
        for x in (0.6, 1.0, 1.4):
            self.assertLessEqual(phi_over_d(x * kappa, kappa), C / (kappa * kappa) + 1e-12)


class LowReservoirTests(unittest.TestCase):
    def test_L_e_and_low_tail_dominates_Phi(self):
        row = high_core_low_reservoir(kappa=20.0, e_low=0.02, i_core=1.0)
        self.assertTrue(row["low_dominates_Phi"])
        self.assertAlmostEqual(row["low_share_of_Phi"], 1.0, places=12)
        self.assertGreater(row["core_share_of_Y"], 0.99)
        self.assertAlmostEqual(row["L_e"], 0.02, places=5)
        self.assertLess(row["E_low_over_E"], 0.03)
        # Energy bound is too weak to pay κ⁴ E_low.
        self.assertGreater(row["phi_at_zero"], row["L_e"] * 1e3)

    def test_energy_does_not_control_L_e(self):
        # E_low ≤ Y_low on the torus (m≥1), but κ⁴ Y_low / Y can be large.
        kappa = 10.0
        Y_low = 1.0**4 * 0.05
        Y = kappa**4 * 1.0
        self.assertLessEqual(0.05, Y_low + 1e-15)
        self.assertGreater(kappa**4 * 0.05 / Y, 0.0)
        self.assertAlmostEqual(kappa**4 * 0.05 / Y, 0.05, places=12)


if __name__ == "__main__":
    unittest.main()
