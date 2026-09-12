"""One-page issues sheet: leftovers named; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "ISSUES-SHEET.md"
HELP = ROOT / "docs" / "HELP-OFF-DESK.md"


class IssuesSheetTests(unittest.TestCase):
    def test_page_is_the_send_sheet(self):
        text = PAGE.read_text()
        flat = " ".join(text.split())
        self.assertIn("One page. Send this.", text)
        self.assertIn("Ordinary Navier–Stokes is not solved", flat)
        self.assertIn("A_{\\mathrm{bad}}", text)
        self.assertIn("\\mathcal R_\\star", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("HELP-OFF-DESK.md", text)
        self.assertIn("occupation", text.lower())
        self.assertIn("withdrawn", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("coherence viscosity", text)

    def test_every_open_row_is_named(self):
        text = PAGE.read_text()
        for mark in (
            "H1 = WRITE (6)",
            "H2 from energy",
            "H3",
            "Lemma★",
            "Hyp-Lat★",
            "Axisymmetric remainder",
            "RH WRITE (6)",
            "Uniform",
            "Goldbach",
            "Yang–Mills",
            "BSD",
            "Hodge",
            "P vs NP",
            "55/56",
            "9D",
        ):
            self.assertIn(mark, text)

    def test_help_report_points_at_the_sheet(self):
        text = HELP.read_text()
        self.assertIn("ISSUES-SHEET.md", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
