#!/usr/bin/env python3
"""Human see-desk: pictures first, not a proof."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.visual import render_html, svg_cylinder, svg_gap, write_see


ROOT = Path(__file__).resolve().parents[1]


class TestSeeDesk(unittest.TestCase):
    def test_html_is_pictures_not_a_proof(self):
        html = render_html()
        self.assertIn("Not a proof", html)
        self.assertIn("Not CosmoEvolution", html)
        self.assertIn("GAP-T3", html)
        self.assertIn("CLIP-T3-WELD", html)
        self.assertIn("<svg", html)
        self.assertNotIn("unified theory", html.lower())

    def test_cylinder_svg_has_a_wall(self):
        svg = svg_cylinder()
        self.assertIn("tube", svg)
        self.assertIn("wall r=δ", svg)

    def test_gap_svg_stops(self):
        svg = svg_gap()
        self.assertIn("STOP", svg)
        self.assertIn("T5", svg)

    def test_write_see(self):
        dest = write_see(ROOT / "docs" / "domain-architect" / "see.html")
        self.assertTrue(dest.exists())
        self.assertTrue(dest.with_name("see-overlay.svg").exists())


class TestSeeCli(unittest.TestCase):
    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--see", "B"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Wrote", proc.stdout)
        self.assertIn("see.html", proc.stdout)


if __name__ == "__main__":
    unittest.main()
