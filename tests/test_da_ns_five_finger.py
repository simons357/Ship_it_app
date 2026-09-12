"""B-hand five-finger map: speculated whole; MAP, not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_ns_five_finger import classify_bhand_claim, run  # noqa: E402
from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "DA-NS-FIVE-FINGER.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"
TINY = ROOT / "docs" / "TINY.txt"
NEED = ROOT / "docs" / "NEED-STAR-HH-L-DUAL.md"
COSMO = ROOT / "docs" / "DA-FINGERS.md"


class DaNsFiveFingerTests(unittest.TestCase):
    def test_page_names_the_whole_and_refuses_a_close(self):
        text = PAGE.read_text()
        self.assertIn("quantity", text.lower())
        self.assertIn("spindle", text)
        self.assertIn("after the spindle", text)
        self.assertIn("Fire state", text)
        self.assertIn("Realized state", text)
        self.assertIn("Future state", text)
        self.assertIn("Need★", text)
        self.assertIn("MISSING", text)
        self.assertIn("H2", text)
        self.assertIn("H3", text)
        self.assertIn("REPAIR", text)
        self.assertIn("Soft X silent", text)
        self.assertIn("MAP", text)
        self.assertIn("unaugmented", text.lower())
        self.assertIn("DA-FINGERS.md", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("hygiene", text.lower())

    def test_machine_fills_blanks_and_refuses_close(self):
        summary = run()
        self.assertEqual(summary["hand"], "B-hand")
        self.assertEqual(summary["verdict"], "MAP")
        self.assertIs(summary["accepted_as_close"], False)
        self.assertIs(summary["ns_solved"], False)
        self.assertEqual(summary["lemma_star"], "OPEN")
        self.assertEqual(summary["need_star"], "SIGNED_DUAL_MISSING")
        self.assertIs(summary["h1_theorem"], False)
        self.assertEqual(summary["soft_x"], "silent")
        self.assertIs(summary["three_writings_welded"], False)
        self.assertIs(summary["k_in_pde"], False)
        self.assertEqual(summary["cosmo_fingers_as_ns"], "NO")
        self.assertEqual(len(summary["fingers"]), 5)
        self.assertEqual(summary["fingers"][1]["name"], "spindle")
        self.assertEqual(summary["fingers"][2]["name"], "after the spindle")
        self.assertEqual(len(summary["after_the_spindle"]), 6)
        self.assertEqual(summary["after_the_spindle"][2]["status"], "REPAIR")
        self.assertIn("fire", summary["states"])
        self.assertIn("realized", summary["states"])
        self.assertIn("future", summary["states"])
        self.assertGreaterEqual(len(summary["da_filled"]), 4)
        self.assertGreaterEqual(len(summary["da_cannot_fill"]), 6)
        self.assertEqual(summary["issues_rows_moved"], [])
        self.assertEqual(summary["catalog_b_open"], 1)
        self.assertTrue(summary["allowed_in_estimate"])
        self.assertEqual(summary["discard_hits"], [])

    def test_fake_close_is_refused(self):
        claim = classify_bhand_claim("Five fingers close NS. Need★ is proved.")
        self.assertFalse(claim["accepted_as_close"])
        self.assertGreaterEqual(len(claim["refuse_hits"]), 1)
        self.assertEqual(claim["verdict"], "MAP")
        self.assertEqual(claim["need_star"], "MISSING")

        cosmo = classify_bhand_claim("Cosmo five fingers as NS. Soft X closes.")
        self.assertFalse(cosmo["accepted_as_close"])
        self.assertGreaterEqual(len(cosmo["refuse_hits"]), 1)

    def test_pointers_and_filter(self):
        self.assertIn("DA-NS-FIVE-FINGER.md", TAPE.read_text())
        self.assertIn("DA-NS-FIVE-FINGER.md", SHEET.read_text())
        self.assertIn("DA-NS-FIVE-FINGER.md", TINY.read_text())
        need = NEED.read_text()
        self.assertIn("DA-NS-FIVE-FINGER.md", need)
        self.assertIn("Cosmo", need)
        self.assertTrue(COSMO.is_file())
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
