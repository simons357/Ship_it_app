"""Monday packet: pile closes; leftovers stay open."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "MONDAY-PACKET.md"


class MondayPacketTests(unittest.TestCase):
    def test_page_is_extract_not_close(self):
        text = PAGE.read_text()
        flat = " ".join(text.split())
        self.assertIn("This is the extract. It is not a close.", text)
        self.assertIn("Ordinary Navier–Stokes is not solved", flat)
        self.assertIn("THEOREM-A-Q1.pdf", text)
        self.assertIn("SWIRL-PAPER.pdf", text)
        self.assertIn("ISSUES-SHEET.md", text)
        self.assertIn("22045478", text)
        self.assertIn("Correction and extract", text)
        self.assertIn("withdrawn", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("coherence viscosity", text)
        self.assertNotIn("cursor.com/agents", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
