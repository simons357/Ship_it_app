"""Hyp-ST★ incidence package: conditional continuum win, lattice transfer MISSING."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md"


class HypSTIncidenceTests(unittest.TestCase):
    def test_conditional_win_not_a_theorem(self):
        text = DOC.read_text()
        self.assertIn("**Win (CONDITIONAL).**", text)
        self.assertIn("C(S)=O(m^{4/3})", text)
        self.assertIn("\\Theta(m^2)", text)
        self.assertIn("**Not a theorem. ★ is not", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Lemma★ is proved", text)

    def test_lattice_transfer_missing(self):
        text = DOC.read_text()
        for tag in ("X1", "X2", "X3", "X4", "X6"):
            self.assertIn(tag, text)
        self.assertGreaterEqual(text.count("**MISSING**"), 5)
        self.assertIn("Hyp-Lat★", text)
        self.assertIn("SSZ", text)
        self.assertIn("rich circles", text)
        self.assertIn("Slice uniformity", text)
        self.assertIn("continuum", text)
        self.assertIn("lattice", text.lower())

    def test_not_h1_and_ap_already_scored(self):
        text = DOC.read_text()
        self.assertIn("Do not glue this to H1", text)
        self.assertIn("AP already scored", text)
        self.assertIn("| This is H1 | **fail** |", text)


if __name__ == "__main__":
    unittest.main()
