"""Five-lane export: PR 48 found, Origin codebase URL not found."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "docs" / "five-lane-export" / "INDEX.md"
SHAPE = ROOT / "docs" / "five-lane-export" / "LEMMA_STAR_SHAPE_FORM.md"
CANON = ROOT / "docs" / "five-lane-export" / "LEMMA_STAR_CANONICAL.md"
PROOF = ROOT / "docs" / "five-lane-export" / "PROOF_LemmaStar_STATUS.md"


class FiveLaneExportTests(unittest.TestCase):
    def test_pr48_and_defs_present(self):
        text = IDX.read_text()
        self.assertIn("https://github.com/simons357/Ship_it_app/pull/48", text)
        self.assertIn("cursor/ns-five-lane-lemma-star-1390", text)
        self.assertIn("**not found**", text)
        self.assertIn("\\Lambda &= Y/X", text)
        self.assertIn("T_c=M-\\Lambda N", text)
        self.assertIn("HH→L", text)
        self.assertIn("DEAD BY SCALING", text)
        self.assertNotIn("NS is solved", text)

    def test_shape_form_copied(self):
        text = SHAPE.read_text()
        self.assertIn("NS is NOT solved", text)
        self.assertIn("\\mathcal{D}_s", text)
        self.assertIn("\\mathcal{R}_\\star", text)
        self.assertTrue(SHAPE.exists())

    def test_canonical_and_proof_lock(self):
        self.assertTrue(CANON.exists())
        self.assertIn("LEMMA_STAR_CANONICAL.md", CANON.read_text())
        proof = PROOF.read_text()
        self.assertIn("DEAD BY SCALING", proof)
        self.assertIn("One direction only", proof)
        self.assertIn("NS is NOT solved", proof)


if __name__ == "__main__":
    unittest.main()
