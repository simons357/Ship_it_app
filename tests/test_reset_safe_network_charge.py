"""Reset-safe net-charge lemma: charge-only form is false."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.reset_safe import charge_covariance, second_witness  # noqa: E402


class ResetSafeNetworkChargeTests(unittest.TestCase):
    def test_first_witness_zero_charge_positive_drift(self):
        s = charge_covariance()
        self.assertEqual(s["sum1"], 0.0)
        self.assertEqual(s["sum2"], 0.0)
        self.assertEqual(s["rank_three"], 1.0)
        self.assertAlmostEqual(s["Q_a_Gamma"], 0.0, places=12)
        self.assertGreater(s["T_c_het_Gamma"], 0.0)
        self.assertAlmostEqual(s["T_c_het_Gamma"], s["rho"], places=10)
        # Without ρ the inequality [T]_+ ≤ 2κ³ [Q]_+ is false.
        two_k3 = s["two_kappa_cubed"]
        self.assertGreater(s["T_c_het_Gamma"], two_k3 * max(s["Q_a_Gamma"], 0.0) + 1e-12)

    def test_second_witness_negative_charge_negative_multiplier(self):
        w = second_witness()
        self.assertLess(w["Q_a_Gamma"], 0.0)
        self.assertLess(w["R_1"], 0.0)
        self.assertAlmostEqual(w["R_1"], w["R_2"], places=8)
        self.assertGreater(w["T_c_het_Gamma"], 0.0)
        # Common multiplier times net charge is positive, so T = R Q would be
        # positive even with Q<0 and R<0; covariance is still required on
        # the first witness where Q_Γ = 0.
        self.assertGreater(w["R_1"] * w["Q_a_Gamma"], 0.0)

    def test_split_T_equals_two_k3_Q_plus_rho(self):
        s = charge_covariance()
        recon = s["two_kappa_cubed"] * s["Q_a_Gamma"] + s["rho"]
        self.assertAlmostEqual(recon, s["T_c_het_Gamma"], places=10)


if __name__ == "__main__":
    unittest.main()
