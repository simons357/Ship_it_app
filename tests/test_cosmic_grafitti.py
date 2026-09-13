"""Cosmic GRAFITTI reprints the found 10 Sep swirl leftover cut."""

from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAG = ROOT / "apps" / "cosmic-grafitti" / "index.html"
CUT = ROOT / "docs" / "SWIRL-MAGAZINE.md"
PAPER = ROOT / "docs" / "SWIRL-PAPER.md"
DEPOSIT = ROOT / "docs" / "SWIRL-DEPOSIT.md"
FACE = ROOT / "docs" / "COSMIC-GRAFITTI-ISSUE-00.md"
FOUND = ROOT / "docs" / "ns-review" / "archives" / "COSMIC-GRAFITTI-FOUND.md"


class TestCosmicGrafittiFound(unittest.TestCase):
    def test_found_files_present(self) -> None:
        for path in (MAG, CUT, PAPER, DEPOSIT, FACE, FOUND):
            self.assertTrue(path.is_file(), f"missing {path}")
        for name in ("cover.png", "swirl.png", "tube.png", "wall.png"):
            self.assertTrue((ROOT / "apps" / "cosmic-grafitti" / "art" / name).is_file())

    def test_html_is_the_leftover_not_the_lattice(self) -> None:
        html = MAG.read_text(encoding="utf-8")
        self.assertIn("COSMIC GRAFITTI", html)
        self.assertIn("WRITE (6)", html)
        self.assertIn("Swirl, alignment, and what Navier–Stokes still owes", html)
        self.assertIn("Hölder 1/2", html)
        self.assertIn("NS NOT SOLVED", html)
        self.assertIn("A / B", html)
        self.assertIn("C / D", html)
        self.assertIn("href=\"#write6\"", html)
        self.assertIn("href=\"#found\"", html)
        self.assertNotIn("Tikkun", html)
        self.assertNotIn("Axis of Evil", html)
        self.assertNotIn("Planck confirms", html)
        self.assertNotIn("NS is solved", html)

    def test_print_cut_is_jonathan_10_sep(self) -> None:
        cut = CUT.read_text(encoding="utf-8")
        self.assertIn("Swirl, alignment, and what Navier–Stokes still owes", cut)
        self.assertIn("WRITE (6)", cut)
        self.assertIn("10 September 2026", cut)
        self.assertIn("Not a proof", cut)
        self.assertIn("Jonathan Robert Simons", cut)


if __name__ == "__main__":
    unittest.main()
