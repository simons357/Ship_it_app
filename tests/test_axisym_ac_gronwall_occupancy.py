#!/usr/bin/env python3
"""(A)–(C) / occupancy / conditional Gronwall diagnostics. No class close."""

from __future__ import annotations

import unittest

from domain_architect.axisym_ac_tests import (
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    condition_a_gate,
    condition_a_on_recorded_samples,
    condition_b_occupancy_alignment,
    condition_c_axisymmetric_restriction,
    conditional_gronwall_under_A,
    occupancy_implication_table,
    run_ac_occupancy_battery,
)


class TestRoutesABC(unittest.TestCase):
    def test_route_statements_are_filed_not_empty(self):
        self.assertIn("P_j", ROUTE_A)
        self.assertIn("depletion", ROUTE_B.lower())
        self.assertIn("axisymmetry", ROUTE_C.lower())

    def test_condition_a_toy_gate(self):
        ok = condition_a_gate(0.01, 1.0, 0.03, 0.5, 0.0)
        self.assertTrue(ok["holds_on_supplied_numbers"])
        self.assertEqual(ok["class_verdict"], "inconclusive")
        self.assertFalse(ok["is_energy_budget_absorption"])
        bad = condition_a_gate(1.0, 1.0, 0.03, 0.5, 0.0)
        self.assertFalse(bad["holds_on_supplied_numbers"])

    def test_condition_a_recorded_hygiene_fail(self):
        rec = condition_a_on_recorded_samples()
        self.assertEqual(rec["class_verdict"], "inconclusive")
        self.assertEqual(rec["diagnostic_verdict"], "fail_hygiene")

    def test_condition_b_fails_depletion(self):
        b = condition_b_occupancy_alignment()
        self.assertEqual(b["class_verdict"], "fail")
        self.assertFalse(b["establishes_depletion"])
        self.assertFalse(b["establishes_A"])
        self.assertAlmostEqual(b["depletion_factor_1_minus_|alpha|"], 0.5)

    def test_condition_c_pure_swirl_only(self):
        c = condition_c_axisymmetric_restriction()
        self.assertTrue(c["pure_swirl_near_zero"])
        self.assertFalse(c["closes_generic_3d"])
        self.assertEqual(c["class_verdict"], "inconclusive")

    def test_occupancy_does_not_imply_depletion(self):
        occ = occupancy_implication_table()
        self.assertFalse(occ["establishes_depletion"])
        self.assertIn("condition (A)", occ["does_not_imply"][1])

    def test_conditional_gronwall_nu_power_one(self):
        gr = conditional_gronwall_under_A(
            eps=0.5,
            nu=0.03,
            c_shell=1.0,
            j=2,
            z0=1.0,
            r_integrable_bound=0.1,
            t=1.0,
        )
        self.assertEqual(gr["status"], "conditional_template")
        self.assertFalse(gr["claimed"])
        self.assertEqual(gr["nu_power_in_alpha"], 1)
        self.assertTrue(gr["refuses_nu_squared_rate"])
        # alpha = 2*0.03*0.5*1*16 = 0.48
        self.assertAlmostEqual(gr["alpha"], 0.48)
        refused = conditional_gronwall_under_A(
            eps=1.0,
            nu=0.03,
            c_shell=1.0,
            j=2,
            z0=1.0,
            r_integrable_bound=0.1,
            t=1.0,
        )
        self.assertEqual(refused["status"], "refused")

    def test_battery_honesty(self):
        bat = run_ac_occupancy_battery()
        self.assertFalse(bat["honesty"]["NS_solved"])
        self.assertEqual(bat["honesty"]["clay"], "NOT CLAIMED")
        self.assertEqual(bat["honesty"]["principal_unresolved"], "T_{j←j}")
        self.assertFalse(bat["honesty"]["routes_are_theorems"])
        self.assertIn("inconclusive", bat["summary"]["A"])
        self.assertIn("fail", bat["summary"]["B"])


class TestEstimateDocumentsABC(unittest.TestCase):
    def test_estimate_files_abc_and_gronwall(self):
        from pathlib import Path

        text = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "swirl"
            / "AXISYMMETRIC-SHELL-ESTIMATE.md"
        ).read_text(encoding="utf-8")
        self.assertIn("enstrophy–palinstrophy bound", text)
        self.assertIn("depletion implying (A)", text)
        self.assertIn("restriction of the data", text)
        self.assertIn("Conditional Gronwall under (A)", text)
        self.assertIn("one** power of", text)
        self.assertIn("NS not solved", text)
        self.assertNotIn("depletion established", text.lower())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
