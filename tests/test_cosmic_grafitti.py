"""Cosmic GRAFITTI issue 01 is the swirl leftover magazine, not the lattice essay."""

from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAG = ROOT / "apps" / "cosmic-grafitti" / "index.html"
CUT = ROOT / "docs" / "SWIRL-MAGAZINE.md"
FACE = ROOT / "docs" / "COSMIC-GRAFITTI-MAGAZINE.md"
FOUND = ROOT / "docs" / "ns-review" / "archives" / "COSMIC-GRAFITTI-FOUND.md"


class TestCosmicGrafitti(unittest.TestCase):
    def test_issue_files_present(self) -> None:
        for path in (MAG, CUT, FACE, FOUND):
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_magazine_is_the_swirl_leftover(self) -> None:
        html = MAG.read_text(encoding="utf-8")
        self.assertIn("COSMIC GRAFITTI", html)
        self.assertIn("WRITE (6)", html)
        self.assertIn("Constantin", html)
        self.assertIn("Beirão", html)
        self.assertIn("NS not solved", html)
        self.assertIn("wrong wall", html.lower())
        self.assertNotIn("Tikkun", html)
        self.assertNotIn("Axis of Evil", html)
        self.assertNotIn("Planck 2018", html)

    def test_print_cut_is_swirl_magazine(self) -> None:
        cut = CUT.read_text(encoding="utf-8")
        self.assertIn("WRITE (6)", cut)
        self.assertIn("Not a proof", cut)
        self.assertIn("Hölder", cut)

    def test_found_note_rejects_lattice_as_issue(self) -> None:
        found = FOUND.read_text(encoding="utf-8")
        self.assertIn("Wrong one", found)
        self.assertIn("SWIRL-MAGAZINE.md", found)


if __name__ == "__main__":
    unittest.main()
