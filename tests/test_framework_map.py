"""Framework map: endpoint first; maps only; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "FRAMEWORK-MAP.md"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"
TINY = ROOT / "docs" / "TINY.txt"


class FrameworkMapTests(unittest.TestCase):
    def test_page_is_a_map_not_a_close(self):
        text = PAGE.read_text()
        flat = " ".join(text.split())
        self.assertIn("endpoint first", text.lower())
        self.assertIn("A new metaphor is not an estimate", text)
        self.assertIn("Ordinary Navier–Stokes is not solved", flat)
        self.assertIn("\\mathcal R_\\star", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("A_{\\mathrm{bad}}", text)
        self.assertIn("Never say die", text)
        self.assertIn("grow", text.lower())
        self.assertIn("9B", text)
        self.assertIn("Do **not** implement", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("coherence viscosity", text)

    def test_verdicts_are_named(self):
        text = PAGE.read_text()
        for mark in ("MAP", "RENAME", "STOP", "DEAD"):
            self.assertIn(mark, text)
        self.assertIn("Selection on bad pairs", text)
        self.assertIn("WRITE (6)", text)
        self.assertIn("55/56", text)
        self.assertIn("occupation", text.lower())
        self.assertIn("withdrawn", text.lower())

    def test_pointers_sit(self):
        self.assertIn("FRAMEWORK-MAP.md", SHEET.read_text())
        self.assertIn("FRAMEWORK-MAP.md", TINY.read_text())

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
