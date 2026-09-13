"""Cosmic GRAFITTI Issue 00: night-wall magazine, not the Universal Geometry reprint."""

from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAG = ROOT / "apps" / "cosmic-grafitti" / "index.html"
CUT = ROOT / "docs" / "COSMIC-GRAFITTI-ISSUE-00.md"
ART = ROOT / "apps" / "cosmic-grafitti" / "art"


class TestCosmicGrafittiIssue00(unittest.TestCase):
    def test_issue_files_present(self) -> None:
        for name in ("cover.png", "swirl.png", "tube.png", "wall.png", "primes.png", "ringdown.png"):
            self.assertTrue((ART / name).is_file(), f"missing art/{name}")
        self.assertTrue(MAG.is_file())
        self.assertTrue(CUT.is_file())

    def test_brand_and_honesty(self) -> None:
        html = MAG.read_text(encoding="utf-8")
        self.assertIn("COSMIC GRAFITTI", html)
        self.assertIn("Issue 00", html)
        self.assertIn("Night Wall", html)
        self.assertIn("NS NOT SOLVED", html)
        self.assertIn("NS not solved", html)
        self.assertIn("∂<sub>z</sub>(Γ<sup>2</sup>)", html)
        self.assertIn("∂<sub>z</sub>(Φ<sup>2</sup>)", html)
        self.assertIn("Clay Statement B is not claimed", html)
        self.assertIn("WRITE (6)", html)
        self.assertIn("href=\"#feature\"", html)
        self.assertIn("href=\"#tube\"", html)
        self.assertIn("id=\"prev\"", html)
        self.assertNotIn("NS is solved", html)
        self.assertNotIn("Clay is closed", html)
        self.assertNotIn("Tikkun", html)
        self.assertNotIn("Axis of Evil", html)
        self.assertNotIn("Planck confirms", html)

    def test_cut_is_the_leftover_not_the_lattice(self) -> None:
        cut = CUT.read_text(encoding="utf-8")
        self.assertIn("WRITE (6)", cut)
        self.assertIn("Not a proof", cut)
        self.assertIn("Universal Geometry", cut)
        self.assertIn("not the may 2026", cut.lower())
        self.assertNotIn("Tikkun", cut)
        self.assertNotIn("Saturn hexagon", cut)


if __name__ == "__main__":
    unittest.main()
