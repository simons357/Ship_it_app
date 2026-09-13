"""PR-24 closure review: family kills unrestricted ★; NS not solved."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from verify_pr24_closure_review import run  # noqa: E402

PAGE = ROOT / "docs" / "LEMMA-STAR-GROWING-LAYER.md"
BOUND = ROOT / "docs" / "ATTACK-9D-FULL-SUPPORT-BOUND.md"
MATH_BOUND = ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_9D_FULL_SUPPORT_BOUND.md"
MATH_KILL = ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_GROWING_LAYER_COUNTEREXAMPLE.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"


class Pr24ClosureReviewTests(unittest.TestCase):
    def test_pages_do_not_close_ns(self):
        for path in (PAGE, BOUND, MATH_BOUND, MATH_KILL):
            text = path.read_text()
            self.assertIn("not solved", text.lower())
            self.assertNotIn("NS is solved", text)
            self.assertNotIn("Clay is solved", text)
            self.assertNotIn("almost proved", text.lower())
            self.assertNotIn("hygiene", text.lower())
        self.assertGreater(len(MATH_BOUND.read_text()), 800)
        self.assertGreater(len(MATH_KILL.read_text()), 800)
        self.assertIn("16/9", MATH_BOUND.read_text())
        self.assertIn("Geometry on one input shell", MATH_BOUND.read_text())
        self.assertIn("8/3", MATH_BOUND.read_text())
        self.assertIn("Hermitian", MATH_BOUND.read_text())
        self.assertIn("Constraint set", MATH_BOUND.read_text())
        self.assertIn("internal check", MATH_BOUND.read_text())
        self.assertIn("165888", MATH_KILL.read_text())

    def test_family_kills_the_box_on_the_live_evaluator(self):
        payload = run()
        self.assertIs(payload["ns_solved"], False)
        self.assertIs(payload["accepted_as_ns_close"], False)
        self.assertEqual(payload["unrestricted_lemma_star"], "KILLED_BY_EXPLICIT_FAMILY")
        self.assertFalse(payload["need_star_repairs_unrestricted"])
        self.assertEqual(payload["soft_x"], "silent")
        self.assertTrue(payload["family"]["all_ok"])
        self.assertGreater(payload["family"]["rows"][-1]["R_star"], payload["family"]["rows"][0]["R_star"])
        self.assertLess(payload["exact_shell"]["max_K_on_samples"], 16.0 / 9.0)
        self.assertTrue(payload["exact_shell"]["all_K_under_bound"])
        self.assertFalse(payload["stokes_moments_overwritten"])

    def test_tape_and_sheet_record_the_kill(self):
        tape = TAPE.read_text()
        sheet = SHEET.read_text()
        statement = (ROOT / "docs" / "LEMMA-STAR-STATEMENT.md").read_text()
        self.assertIn("LEMMA-STAR-GROWING-LAYER.md", tape)
        self.assertIn("LEMMA-STAR-GROWING-LAYER.md", sheet)
        self.assertIn("KILLED", tape)
        self.assertIn("replacement", sheet.lower())
        self.assertIn("Killed by", statement)
        self.assertIn("Replacement energy-budget closure", statement)


if __name__ == "__main__":
    unittest.main()
