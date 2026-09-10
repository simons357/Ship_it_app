"""Explore-boundedness score stays a score. Not a close."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "LEMMA-STAR-EXPLORE.md"


class LemmaStarExploreTests(unittest.TestCase):
    def test_stays_open_and_refuses_glue(self):
        text = PAGE.read_text()
        self.assertIn("**★ OPEN. NS not solved.", text)
        self.assertIn("Do not start H1.", text)
        self.assertIn("Do not glue Q-stack.", text)
        self.assertIn("Two-shell \\(D_s\\).** Sits:", text)
        self.assertIn("Do not mix those groups", text)
        self.assertIn("continuum / Bloch scaling", text)
        self.assertIn("0.327", text)
        self.assertIn("0.610", text)
        self.assertIn("0.641", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("falsifier-of-record", text)


if __name__ == "__main__":
    unittest.main()
