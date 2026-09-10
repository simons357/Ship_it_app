"""H1 locator: named leftover, not a paper hunt."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "WHERE-H1.md"


class WhereH1Tests(unittest.TestCase):
    def test_names_the_leftover_and_stays_open(self):
        text = PAGE.read_text()
        self.assertIn("**OPEN. Not a theorem. NS is not solved.**", text)
        self.assertIn("H1 = WRITE (6) = Lemma I on the ball", text)
        self.assertIn("Near-Bad", text)
        self.assertIn("not h1", text.lower())
        self.assertIn("LOOKUP-H1.md", text)
        self.assertIn("H1-OBJECT.md", text)
        self.assertIn("not under another name", text.lower())
        self.assertIn("Do not start H1 from ABC", text)
        self.assertIn("P1-lowpass", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("H1 is proved", text)

    def test_does_not_glue_star_or_matrix(self):
        text = PAGE.read_text()
        self.assertIn("Lemma★", text)
        self.assertIn("Different integral", text)
        self.assertIn("H_N", text)
        self.assertIn("Do not glue", text)


if __name__ == "__main__":
    unittest.main()
