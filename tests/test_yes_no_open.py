"""Yes / no / open tape: the flip does not move the lock."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"


class YesNoOpenTests(unittest.TestCase):
    def test_page_is_the_tape(self):
        text = PAGE.read_text()
        flat = " ".join(text.split())
        self.assertIn("This page is the lock", text)
        self.assertIn("That happened. It is bad for you", flat)
        self.assertIn("YES = sits as stated", text)
        self.assertIn("NO = dead, withdrawn, or a false close", text)
        self.assertIn("OPEN = named leftover", text)
        self.assertIn("A write is not a theorem", text)
        self.assertIn("this page wins", text)
        self.assertIn("Ordinary Navier–Stokes is not solved", text)
        self.assertIn("\\mathcal G", text)
        self.assertIn("\\mathcal R_\\star", text)
        self.assertIn("55/56", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("H1 is a theorem", text)

    def test_designed_9d_stays_no_and_h1_write_is_not_the_move(self):
        text = PAGE.read_text()
        self.assertIn("designed 9d", text.lower())
        self.assertIn("grow", text.lower())
        self.assertIn("The write in", text)
        self.assertIn("H1-WRITE.md", text)
        self.assertIn("withdrawn", text.lower())

    def test_pointers_and_filter(self):
        self.assertIn("YES-NO-OPEN.md", TINY.read_text())
        self.assertIn("YES-NO-OPEN.md", SHEET.read_text())
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
