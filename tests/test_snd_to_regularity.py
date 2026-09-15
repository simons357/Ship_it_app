"""SND to regularity: shell vs drift; circular inputs named; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "SND-TO-REGULARITY.md"
PLAIN = ROOT / "docs" / "SND-H-PLAIN.md"
PLAN = ROOT / "docs" / "UNAUGMENTED-R4-VORTICITY-PLAN.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
REPAIR = ROOT / "docs" / "DA-REPAIR.md"


class SndToRegularityTests(unittest.TestCase):
    def test_page_answers_the_three_questions(self):
        text = PAGE.read_text()
        flat = " ".join(text.replace("*", "").split()).lower()
        self.assertIn("What the shell condition controls", text)
        self.assertIn("What frequency drift is still needed", text)
        self.assertIn("Does the proof assume the desired", text)
        self.assertIn("instantaneous partition", text)
        self.assertIn("j_*", text)
        self.assertIn("Lambda", text.replace("\\", ""))
        self.assertIn("Pi_{j_*}", text.replace("\\", ""))
        self.assertIn("X\\ge\\delta_*/4", text)
        self.assertIn("not an upper bound", flat)
        self.assertIn("T2 Lemma 2", text)
        self.assertIn("H^{2.3}", text)
        self.assertIn("Theorem F", text)
        self.assertIn("4^{N-1}", text)
        self.assertIn("Theorem E", text)
        self.assertIn("already-smooth", text)
        self.assertIn("B11d", text)
        self.assertIn("B12e", text)
        self.assertIn("B10b", text)
        self.assertIn("B7c", text)
        self.assertIn("B1b", text)
        self.assertIn("drift law", text)
        self.assertIn("MISSING", text)
        self.assertIn("OPEN", text)
        self.assertIn("does not imply regularity", flat)
        self.assertIn("No more", text)
        self.assertIn("K", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", flat)
        self.assertNotIn("hygiene", flat)

    def test_honest_skeleton_needs_three_conjuncts(self):
        text = PAGE.read_text()
        self.assertIn("SND-C in SPREAD", text)
        self.assertIn("Ring in 3-CONC", text)
        self.assertIn("uniform in", text)
        self.assertIn("Low Bony", text)
        self.assertIn("SIMPLEX", text)
        self.assertIn("PARK", text)
        self.assertIn("Closing SND-C does not close ordinary NS", text)

    def test_pointers_and_filter(self):
        for path in (PLAIN, PLAN, TAPE, SHEET, TINY, LATEST, REPAIR):
            self.assertIn("SND-TO-REGULARITY.md", path.read_text(), msg=path.name)
        self.assertIn("Closing SND does not close ordinary NS", PLAIN.read_text())
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
