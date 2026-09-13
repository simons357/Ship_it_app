"""Cosmic GRAFITTI issue 01: recovered essay + honesty lock on the wall."""

from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAG = ROOT / "apps" / "cosmic-grafitti" / "index.html"
CUT = ROOT / "docs" / "COSMIC-GRAFITTI-MAGAZINE.md"
ESSAY = ROOT / "docs" / "papers" / "swirl" / "PHI_GEOMETRY_BRIDGE.md"
DA = ROOT / "docs" / "papers" / "swirl" / "DA-ON-PHI-GEOMETRY.md"
FOUND = ROOT / "docs" / "ns-review" / "archives" / "COSMIC-GRAFITTI-FOUND.md"


class TestCosmicGrafitti(unittest.TestCase):
    def test_issue_files_present(self) -> None:
        for path in (MAG, CUT, ESSAY, DA, FOUND):
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_magazine_brand_and_honesty(self) -> None:
        html = MAG.read_text(encoding="utf-8")
        self.assertIn("COSMIC GRAFITTI", html)
        self.assertIn("NS not solved", html)
        self.assertIn("Park", html)
        self.assertIn("Keep", html)
        self.assertIn("∂<sub>z</sub>(Γ<sup>2</sup>)", html)
        self.assertIn("∂<sub>z</sub>(Φ<sup>2</sup>)", html)
        self.assertIn("Clay Statement B", html)
        self.assertNotIn("NS is solved", html)
        self.assertNotIn("Clay is closed", html)

    def test_recovered_essay_is_the_may_wall(self) -> None:
        essay = ESSAY.read_text(encoding="utf-8")
        self.assertIn("The Phi-Renormalization as Universal Geometry", essay)
        self.assertIn("Cosmic Star Lattice", essay)
        self.assertIn("May 2026", essay)
        self.assertIn("Saturn", essay)
        self.assertIn("Tikkun", essay)
        self.assertIn(r"\frac{1}{r^4}\partial_z(\Gamma^2) = \partial_z(\Phi^2)", essay)

    def test_da_reading_refuses_equivalence(self) -> None:
        da = DA.read_text(encoding="utf-8")
        self.assertIn("functional correspondence is a", da)
        self.assertIn("analogy at most", da)
        self.assertIn("**open**", da)

    def test_cut_names_keep_and_park(self) -> None:
        cut = CUT.read_text(encoding="utf-8")
        self.assertIn("KEEP", cut)
        self.assertIn("PARK", cut)
        self.assertIn("Not a proof", cut)


if __name__ == "__main__":
    unittest.main()
