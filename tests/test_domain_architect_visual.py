#!/usr/bin/env python3
"""Human see-desk: pictures first, not a proof."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.visual import (
    DEFAULT_STATE,
    follow,
    load_focus,
    render_html,
    svg_cylinder,
    svg_gap,
    write_see,
)


ROOT = Path(__file__).resolve().parents[1]


class TestSeeDesk(unittest.TestCase):
    def test_html_is_pictures_not_a_proof(self):
        html = render_html()
        self.assertIn("Not a proof", html)
        self.assertIn("Not CosmoEvolution", html)
        self.assertIn("Now looking at", html)
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
        self.assertIn("Visual appendage", proc.stdout)

    def test_tube_json_updates_see_state(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--tube", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["hardy_probe"]["holds"])
        state = json.loads((ROOT / DEFAULT_STATE).read_text(encoding="utf-8"))
        self.assertEqual(state["action"], "tube")
        self.assertEqual(state["appendage"], "SEE")
        self.assertTrue(state["not_a_proof"])
        html = (ROOT / "docs" / "domain-architect" / "see.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("Live math: tube estimate", html)

    def test_proceed_does_not_move_the_picture(self):
        follow("gap", "B")
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--proceed", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(load_focus()["action"], "gap")

    def test_follow_rewrites_the_banner(self):
        state = follow("overlay", "B")
        self.assertEqual(state["action"], "overlay")
        html = render_html(state)
        self.assertIn("Live math: overlay of done pieces", html)
        self.assertIn("Visual appendage of the think tank", html)


if __name__ == "__main__":
    unittest.main()
