"""Statement page quotes the lock. Not a reconstruction."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "LEMMA-STAR-STATEMENT.md"
CANON = ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_CANONICAL.md"


class LemmaStarStatementTests(unittest.TestCase):
    def test_quotes_boxed_claim_and_stays_open(self):
        text = PAGE.read_text()
        self.assertIn("**OPEN. Not a proof. NS not solved.**", text)
        self.assertIn("C_{\\mathrm{geom}}", text)
        self.assertIn("\\sup_v\\mathcal R_\\star<\\infty", text)
        self.assertIn("not a reconstruction", text.lower())
        self.assertIn("★ \\(\\Rightarrow\\) global", text)
        self.assertIn("That is not the same sentence as", text)
        self.assertIn("H1 / WRITE (6)", text)
        self.assertIn("LEMMA_STAR_CANONICAL.md", text)

    def test_canonical_still_open(self):
        text = CANON.read_text()
        self.assertIn("**OPEN.**", text)
        self.assertIn("NS not solved", text)
        self.assertIn("Do not write", text)
        self.assertIn("no converse", text.lower())


if __name__ == "__main__":
    unittest.main()
