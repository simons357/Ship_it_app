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
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"


class Pr24ClosureReviewTests(unittest.TestCase):
    def test_pages_do_not_close_ns(self):
        for path in (PAGE, BOUND):
            text = path.read_text()
            self.assertIn("not solved", text.lower())
            self.assertNotIn("NS is solved", text)
            self.assertNotIn("Clay is solved", text)
            self.assertNotIn("almost proved", text.lower())
            self.assertNotIn("hygiene", text.lower())
        bound = BOUND.read_text()
        flat = " ".join(bound.split())
        self.assertIn("CLAIMED", bound)
        self.assertIn(
            "CLAIMED: written derivation available; internal checks passed; independent specialist review pending. Numerical sweeps provide consistency checks only.",
            flat,
        )
        self.assertIn("single input shell", bound)
        self.assertIn("No as a regularity close", bound)
        self.assertIn("Soft X silent", bound)
        self.assertIn("three-shear", bound)
        self.assertIn("K=2/3", bound.replace(" ", ""))
        self.assertIn("normalized torus", bound)
        self.assertIn("does not perform the shell-count experiments", flat)
        self.assertNotIn("sweep shows nothing near", bound)
        self.assertIn("weighted incidence", bound)
        self.assertIn("complex-polarization identity", flat)
        self.assertIn("Hermitian", bound)
        self.assertIn("0<\\beta\\le4\\alpha", bound.replace(" ", ""))
        self.assertIn("g'(x)", bound.replace(" ", ""))
        self.assertIn("8/3", bound)

    def test_family_kills_the_box_on_the_live_evaluator(self):
        payload = run()
        self.assertIs(payload["ns_solved"], False)
        self.assertIs(payload["accepted_as_ns_close"], False)
        self.assertEqual(payload["unrestricted_lemma_star"], "KILLED_BY_EXPLICIT_FAMILY")
        self.assertFalse(payload["need_star_repairs_unrestricted"])
        self.assertEqual(payload["soft_x"], "silent")
        self.assertTrue(payload["family"]["all_ok"])
        self.assertTrue(payload["seed"]["ok"])
        self.assertGreater(payload["family"]["rows"][-1]["R_star"], payload["family"]["rows"][0]["R_star"])
        self.assertTrue(payload["exact_shell"]["ok"])
        self.assertFalse(payload["exact_shell"]["performs_shell_count_experiments"])
        self.assertTrue(payload["exact_shell"]["three_shear"]["ok"])
        self.assertAlmostEqual(payload["exact_shell"]["three_shear"]["K"], 2.0 / 3.0, places=12)
        self.assertTrue(payload["exact_shell"]["k_form"]["ok"])
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
