"""★ reason: map of identities. Not a theorem."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "LEMMA-STAR-REASON.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"


class LemmaStarReasonTests(unittest.TestCase):
    def test_page_is_a_map_not_a_theorem(self):
        text = PAGE.read_text()
        flat = " ".join(text.split())
        self.assertIn("quantity is", text)
        self.assertIn("\\mathcal R_\\star", text)
        self.assertIn("T_c", text)
        self.assertIn("\\mathcal D_s", text)
        self.assertIn("HH→L", text)
        self.assertIn("It is not a proof", flat)
        self.assertIn("occupancy", text.lower())
        self.assertIn("16s", text)
        self.assertIn("Lemma★ OPEN", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_pointers_and_filter(self):
        self.assertIn("LEMMA-STAR-REASON.md", TAPE.read_text())
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
