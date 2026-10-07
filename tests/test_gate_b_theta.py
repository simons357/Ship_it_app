"""Gate B / Dish #3 locks.

Cauchy–Schwarz on ∑ f_x² = E. Gate A stays
UNRESOLVED / DIAGNOSTIC ONLY. Not (17).
"""

from __future__ import annotations

import sys
import unittest
from math import sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ns_attacks.gate_b_theta import (  # noqa: E402
    dish3_bound_factor,
    family_rho_vector,
    report,
    rho_l1_l2,
    subnet_l1_l2,
    theta_hat,
)


class TestGateBTheta(unittest.TestCase):
    def test_cs_norm_comparison(self) -> None:
        agg = rho_l1_l2({1: 0.5, 2: 1.5, 3: 2.0})
        self.assertTrue(agg["S_le_L"])
        self.assertTrue(agg["L_le_sqrtM_S"])
        self.assertAlmostEqual(agg["L"], 4.0)
        self.assertAlmostEqual(agg["S"], sqrt(0.25 + 2.25 + 4.0))
        self.assertEqual(agg["M"], 3)

    def test_empty_family(self) -> None:
        agg = rho_l1_l2({})
        self.assertEqual(agg["M"], 0)
        self.assertEqual(agg["L"], 0.0)
        self.assertEqual(agg["S"], 0.0)
        self.assertTrue(agg["L_le_sqrtM_S"])

    def test_c25_rho_vector(self) -> None:
        fam = family_rho_vector()
        self.assertAlmostEqual(fam["rhos"][5], 0.6318550824, places=8)
        self.assertAlmostEqual(fam["rhos"][9], 0.8253067330, places=8)
        self.assertAlmostEqual(fam["rhos"][13], 1.0833160571, places=8)
        self.assertTrue(fam["S_le_L"])
        self.assertTrue(fam["L_le_sqrtM_S"])
        self.assertAlmostEqual(fam["L"], 2.5404778725, places=8)
        self.assertAlmostEqual(fam["S"], 1.501117, places=5)

    def test_subnet_L_grows_S_stays_O1(self) -> None:
        r20 = subnet_l1_l2(20)
        r80 = subnet_l1_l2(80)
        self.assertEqual(r20["c"], 800)
        self.assertEqual(r80["c"], 12800)
        self.assertGreater(r80["L"], 1.5 * r20["L"])
        self.assertLess(r80["S"], 0.5)
        self.assertLess(abs(r80["S"] - r20["S"]), 0.05)
        self.assertAlmostEqual(r20["L"], r20["A_subnet_full_rho"], places=12)
        self.assertTrue(r20["S_le_L"])
        self.assertTrue(r80["L_le_sqrtM_S"])

    def test_theta_hat_near_zero_on_sample(self) -> None:
        r20 = subnet_l1_l2(20)
        r40 = subnet_l1_l2(40)
        th = theta_hat(r20, r40)
        self.assertLess(abs(th), 0.1)

    def test_dish3_factor(self) -> None:
        out = dish3_bound_factor(0.276)
        self.assertAlmostEqual(out["prefactor"], 0.552)
        self.assertEqual(out["form"], "2 S sqrt(E) Y")
        self.assertEqual(out["theta_if_S_bounded"], 0.0)

    def test_report_locks(self) -> None:
        payload = report()
        locks = payload["locks"]
        self.assertEqual(locks["gate_A"], "UNRESOLVED / DIAGNOSTIC ONLY")
        self.assertTrue(locks["gate_A_not_open"])
        self.assertTrue(locks["gate_A_not_failed"])
        self.assertTrue(locks["gate_A_not_dead"])
        self.assertTrue(locks["gate_B_active"])
        self.assertFalse(locks["theta_proved"])
        self.assertFalse(locks["theorem_17_proved"])
        self.assertTrue(locks["C_majorant_is_upper_bound"])
        self.assertTrue(locks["general_c_allocation_not_sot"])
        self.assertTrue(locks["no_infinite_divergent_cost"])
        self.assertTrue(locks["not_a_close"])
        self.assertTrue(payload["subnet_diagnostic"]["L_grows"])
        self.assertTrue(payload["subnet_diagnostic"]["S_stays_O1"])
        self.assertLess(abs(payload["subnet_diagnostic"]["mean_theta_hat"]), 0.05)

    def test_program_status_language(self) -> None:
        theta = (ROOT / "docs" / "GATE-B-THETA.md").read_text(encoding="utf-8")
        self.assertIn("UNRESOLVED / DIAGNOSTIC ONLY", theta)
        self.assertIn("Dish #3", theta)
        self.assertNotIn("CLOSED — Outcome B", theta)

        prog = (ROOT / "docs" / "PROGRAM-GATES-A-D.md").read_text(encoding="utf-8")
        self.assertIn("UNRESOLVED / DIAGNOSTIC ONLY", prog)
        self.assertNotIn("Gate A closed (Outcome B)", prog)

        dated = (ROOT / "docs" / "PROGRAM-GATES-A-D-2026-10-07.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("UNRESOLVED / DIAGNOSTIC ONLY", dated)
        self.assertNotIn("CLOSED — Outcome B", dated)


if __name__ == "__main__":
    unittest.main()
