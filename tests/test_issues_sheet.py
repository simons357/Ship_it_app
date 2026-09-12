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

    def test_four_jobs_are_named(self):
        text = PAGE.read_text()
        self.assertIn("H1 = WRITE (6)", text)
        self.assertIn("Lemma★", text)
        self.assertIn("Axisymmetric remainder", text)
        self.assertIn("RH WRITE (6)", text)
        self.assertIn("55/56", text)

    def test_help_report_points_at_the_sheet(self):
        text = HELP.read_text()
        self.assertIn("ISSUES-SHEET.md", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
