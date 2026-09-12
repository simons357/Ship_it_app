"""Off-desk help report: leftovers named; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "HELP-OFF-DESK.md"


class HelpOffDeskTests(unittest.TestCase):
    def test_page_is_a_handoff(self):
        text = PAGE.read_text()
        flat = " ".join(text.split())
        self.assertIn("Not a close", text)
        self.assertIn("Ordinary Navier–Stokes is not solved", flat)
        self.assertIn("A_{\\mathrm{bad}}", text)
        self.assertIn("\\mathcal R_\\star", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("Job 1", text)
        self.assertIn("Job 2", text)
        self.assertIn("Job 3", text)
        self.assertIn("Job 4", text)
        self.assertIn("occupation decay", text.lower())
        self.assertIn("withdrawn", text.lower())
        self.assertIn("good-set", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("coherence viscosity", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
