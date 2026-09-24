"""SAG eyes on the two-triad witness. Not DA-NS-2."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.sag_two_triad_witness import (  # noqa: E402
    L_family,
    charge_covariance,
    geometry,
    sag_eyes,
)


class TwoTriadWitnessTests(unittest.TestCase):
    def test_closes_and_is_rank_three(self):
        g = geometry()
        self.assertTrue(g["closes"])
        self.assertEqual(g["det_kpr"], -1)
        self.assertTrue(g["rank_three"])
        self.assertTrue(g["shared_output_after_sign_flip"])

    def test_scalene_not_equal_input(self):
        g = geometry()
        self.assertFalse(g["equal_input_circle"])
        self.assertAlmostEqual(g["lengths"]["p"], math.sqrt(2.0), places=12)
        self.assertAlmostEqual(g["lengths"]["q"], math.sqrt(3.0), places=12)
        self.assertAlmostEqual(g["lengths"]["r"], 1.0, places=12)
        self.assertAlmostEqual(g["lengths"]["s"], math.sqrt(2.0), places=12)

    def test_charge_cancels_Tc_does_not(self):
        c = charge_covariance()
        self.assertAlmostEqual(c["Lambda"], 2.0, places=12)
        self.assertAlmostEqual(c["Q_a_Gamma"], 0.0, places=12)
        self.assertAlmostEqual(c["T_c_1"], c["R_1"] * c["Q_a_1"], places=10)
        self.assertAlmostEqual(c["T_c_2"], c["R_2"] * c["Q_a_2"], places=10)
        self.assertAlmostEqual(c["T_c_het_Gamma"], c["T_from_RQ"], places=10)
        self.assertAlmostEqual(c["T_c_het_Gamma"], c["boxed"], places=10)
        self.assertGreater(c["T_c_het_Gamma"], 0.0)
        self.assertFalse(c["R_1_equals_R_2"])

    def test_static_shared_output_does_not_rescue(self):
        s = sag_eyes()
        self.assertTrue(s["shared_output"])
        self.assertTrue(s["Q_cancel"])
        self.assertTrue(s["Tc_het_positive"])
        self.assertFalse(s["static_shared_output_forces_Tc_cancel"])
        self.assertIn("KILLED", s["verdict"])

    def test_L_family_stays_rank_three(self):
        for L in (2, 7, 55):
            row = L_family(L)
            self.assertEqual(row["sum_1"], (0, 0, 0))
            self.assertEqual(row["sum_2"], (0, 0, 0))
            self.assertEqual(row["det"], L * L * (2 * L + 1))
            self.assertTrue(row["rank_three"])
            self.assertFalse(row["equal_input"])


if __name__ == "__main__":
    unittest.main()
