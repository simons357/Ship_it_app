"""Honesty locks for the 24 Sep 2026 Gate 1-7 recovery seated on the close plan."""

from __future__ import annotations

import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "NS-CLOSE-PLAN.md"
GATES = ROOT / "docs" / "NS-CLOSE-PLAN-GATES.md"
LOCK = ROOT / "data" / "ns_close_plan" / "gates_recovered_2026-09-24.json"


class TestNsClosePlanGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = PLAN.read_text(encoding="utf-8")
        cls.gates = GATES.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))

    def test_sources_present(self) -> None:
        self.assertTrue(PLAN.is_file(), f"missing {PLAN}")
        self.assertTrue(GATES.is_file(), f"missing {GATES}")
        self.assertTrue(LOCK.is_file(), f"missing {LOCK}")

    def test_close_plan_points_at_recovery(self) -> None:
        self.assertIn("NS-CLOSE-PLAN-GATES.md", self.plan)
        self.assertIn("REOPEN = recompute", self.plan)
        self.assertIn("not a reopen", self.plan.lower())

    def test_ns_not_solved(self) -> None:
        for text in (self.plan, self.gates):
            self.assertIn("NS not solved", text)
            self.assertNotIn("Clay Millennium solved", text)
            self.assertNotIn("Statement B is closed", text)

    def test_reopen_rule(self) -> None:
        self.assertTrue(self.lock["superseded"])
        self.assertFalse(self.lock["overwrites_current_board"])
        self.assertEqual(self.lock["rule"], "REOPEN = recompute")
        self.assertIn("REOPEN = recompute", self.gates)
        self.assertIn("superseded", self.gates.lower())

    def test_gate_statuses(self) -> None:
        expected = {
            "1": "CLAIMED",
            "2": "CLOSED",
            "3": "CLOSED",
            "4": "PARTIAL",
            "5": "CLAIMED",
            "6": "NOT YET STARTED",
            "7": "NOT YET STARTED",
        }
        for number, status in expected.items():
            self.assertEqual(self.lock["gates"][number]["status"], status)
        self.assertFalse(self.lock["gates"]["5"]["independently_reproducible"])
        self.assertFalse(self.lock["gates"]["4"]["global"])

    def test_missing_pieces_stay_missing(self) -> None:
        missing_phrases = (
            "screenshot-truncated",
            "full six-permutation identity",
            "exact definitions of u, m, d",
            "definition of ++ / +++",
            "numerical protocol",
            "formula for L",
            "formula for A",
            "Gate-7 definition of T_c",
        )
        blob = json.dumps(self.lock)
        for phrase in missing_phrases:
            self.assertIn(phrase, blob)
        self.assertGreaterEqual(self.gates.lower().count("missing"), 12)

    def test_do_not_splice_later_definitions(self) -> None:
        self.assertTrue(self.lock["gates"]["7"]["do_not_splice_later_program_quantities"])
        self.assertIn("spliced", self.gates.lower())
        self.assertIn("Do **not** splice later", self.plan)

    def test_d_plus_sign_convention(self) -> None:
        compact = re.sub(r"\s+", "", self.gates)
        self.assertIn("4C_0C_2-C_1^2", compact)
        self.assertIn("C_1^2-4C_0C_2", compact)
        self.assertIn("was **not**", self.gates)
        self.assertEqual(self.lock["gates"]["5"]["preserved"]["D_plus_is_not"], "C1^2 - 4 C0 C2")
        self.assertEqual(self.lock["gates"]["5"]["preserved"]["D_plus"], "4 C0 C2 - C1^2")

    def test_quadratic_vertex_identity(self) -> None:
        # P0(z) = C0 + C1 z + C2 z^2, z* = -C1/(2 C2)
        # P0(z*) = (4 C0 C2 - C1^2) / (4 C2) = D+ / (4 C2)
        samples = (
            (3.0, -4.0, 1.0),
            (2.0, -5.0, 2.0),
            (1.25, -3.5, 0.5),
        )
        for c0, c1, c2 in samples:
            d_plus = 4.0 * c0 * c2 - c1 * c1
            z_star = -c1 / (2.0 * c2)
            p_star = c0 + c1 * z_star + c2 * z_star * z_star
            self.assertAlmostEqual(p_star, d_plus / (4.0 * c2))
            self.assertAlmostEqual(d_plus, - (c1 * c1 - 4.0 * c0 * c2))

    def test_triangle_delta_is_16_area_squared(self) -> None:
        # Sides 3, 4, 5: area 6, so 16 area^2 = 576.
        r, t, s = 3.0, 4.0, 5.0
        delta = 2.0 * (r * r * t * t + t * t * s * s + s * s * r * r) - (
            r**4 + t**4 + s**4
        )
        self.assertAlmostEqual(delta, 16.0 * 6.0 * 6.0)
        self.assertIn("2(r^2t^2+t^2s^2+s^2r^2)", self.gates.replace(" ", "").replace("\\", ""))

    def test_lengths_not_squared_lengths(self) -> None:
        self.assertEqual(self.lock["gates"]["3"]["r_s_t_are"], "lengths")
        self.assertIn("They are **lengths**, not squared", self.gates)

    def test_c2_complete_c0_c1_truncated(self) -> None:
        preserved = self.lock["gates"]["5"]["preserved"]
        self.assertEqual(
            preserved["C2_complete"],
            "16 m^2 + 2 m u + 18 m - 4 u^2 - 10 u - 2",
        )
        self.assertEqual(preserved["C0_C1"], "screenshot-truncated")
        self.assertIn("16m^2+2mu+18m-4u^2-10u-2", re.sub(r"\s+", "", self.gates))
        self.assertIn("truncated", self.gates.lower())

    def test_what_is_left_is_three_items(self) -> None:
        self.assertEqual(len(self.lock["what_is_left"]), 3)
        left = " ".join(self.lock["what_is_left"]).lower()
        self.assertIn("gate 5", left)
        self.assertIn("gate 6", left)
        self.assertIn("gate 7", left)
        self.assertIn("Finish Gate 5", self.plan)
        self.assertIn("NOT YET STARTED", self.plan)


if __name__ == "__main__":
    unittest.main()
