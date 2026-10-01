"""Unified unaugmented NS status: enough for a score, not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "UNAUG-NS-UNIFIED.md"
STATUS = ROOT / "docs" / "NS-STATUS.md"
PLAN = ROOT / "docs" / "MASTER-PLAN.md"
AUDIT = ROOT / "docs" / "REPORT-AUDIT.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"


class UnaugNsUnifiedTests(unittest.TestCase):
    def test_page_scores_and_does_not_close(self):
        text = PAGE.read_text()
        flat = " ".join(text.replace("*", "").split()).lower()
        self.assertIn("Enough information?", text)
        self.assertIn("Yes to score", text)
        self.assertIn("No to close", text)
        self.assertIn("withdrawn", text.lower())
        self.assertIn("KILLED", text)
        self.assertIn("CLAIMED", text)
        self.assertIn("Route A", text)
        self.assertIn("Route B", text)
        self.assertIn("instrument", text.lower())
        self.assertIn("frequency-drift", flat)
        self.assertIn("Do not write", text)
        self.assertIn("SURVIVES", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", flat)
        self.assertNotIn("hygiene", flat)
        self.assertNotIn("Exact-shell 9D — claimed", text)
        self.assertNotIn("9D bound CLAIMED", text)

    def test_pointers_and_filter(self):
        for path in (STATUS, PLAN, AUDIT, TAPE, TINY, LATEST, SHEET):
            self.assertIn("UNAUG-NS-UNIFIED.md", path.read_text(), msg=path.name)
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
