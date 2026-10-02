"""L3 budget gates. (L3-1) classical. (L3-5) not proved. NS not solved."""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.l3_budget_gates import (  # noqa: E402
    bernstein_H12,
    gn_ratio_fourier,
    holder_exponents,
    report,
    serrin_endpoint_p,
    young_rep_split,
)


class HolderSerrinTests(unittest.TestCase):
    def test_holder_l2_from_l3_l6(self):
        h = holder_exponents()
        self.assertTrue(h["ok"])
        self.assertEqual(h["sum"], Fraction(1, 2))

    def test_serrin_q3_has_no_finite_p(self):
        self.assertIsNone(serrin_endpoint_p(3))
        self.assertIsNone(serrin_endpoint_p(2))

    def test_serrin_subcritical_exponents(self):
        # 2/p + 3/q = 1
        self.assertEqual(serrin_endpoint_p(4), 8)  # 2/8 + 3/4 = 1
        self.assertEqual(serrin_endpoint_p(6), 4)  # 2/4 + 3/6 = 1
        self.assertEqual(serrin_endpoint_p(9), 3)  # 2/3 + 3/9 = 1


class InterpolationTests(unittest.TestCase):
    def test_young_rep_from_audit(self):
        self.assertTrue(young_rep_split(Fraction(52), Fraction(532), Fraction(3, 2)))
        self.assertTrue(young_rep_split(Fraction(4), Fraction(9), Fraction(1)))

    def test_bernstein_high_pass(self):
        out = bernstein_H12([4, 9], [Fraction(1, 2), Fraction(1, 3)], K=1)
        self.assertTrue(out["ok"])
        self.assertGreater(out["Xh"], 0)
        # K=3 drops the |k|=2 shell
        dropped = bernstein_H12([4, 9], [Fraction(1, 2), Fraction(1, 3)], K=2)
        self.assertEqual(dropped["min_r"], 3)
        self.assertTrue(dropped["ok"])

    def test_gn_cs_proxy_le_1(self):
        ratio = gn_ratio_fourier(
            [1, 4, 9],
            [Fraction(1), Fraction(1, 2), Fraction(1, 4)],
        )
        self.assertLessEqual(ratio, 1)
        # equality on a single shell
        eq = gn_ratio_fourier([4], [Fraction(3)])
        self.assertEqual(eq, 1)


class LockTests(unittest.TestCase):
    def test_report_locks(self):
        r = report()
        self.assertTrue(r["holder"]["ok"])
        self.assertIsNone(r["serrin"]["q3_finite_p"])
        self.assertTrue(r["serrin"]["q4_is_8"])
        self.assertTrue(r["bernstein"]["ok"])
        self.assertTrue(r["gn_cs_le_1"])
        self.assertTrue(r["young_ok"])
        self.assertTrue(r["l3_5"]["serrin_q3_finite_p"])
        self.assertTrue(r["l3_5"]["l3_5_carries_Lambda"])
        self.assertTrue(r["l3_5"]["equivalent_to_17"])
        self.assertTrue(r["locks"]["not_a_close"])
        self.assertTrue(r["locks"]["l3_1_classical"])
        self.assertFalse(r["locks"]["l3_5_proved"])
        self.assertFalse(r["locks"]["theorem_17_proved"])
        self.assertTrue(r["locks"]["not_beyond_ESS"])
        self.assertTrue(r["locks"]["no_novelty"])
        self.assertTrue(r["locks"]["lemma_A_unaltered"])
        self.assertTrue(r["locks"]["sign_gate_unaltered"])


if __name__ == "__main__":
    unittest.main()
