#!/usr/bin/env python3
"""Overlay only done transposable pieces; refine holes; do not silent-merge."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.overlay import overlay_report


ROOT = Path(__file__).resolve().parents[1]


class TestOverlay(unittest.TestCase):
    def test_composite_is_architecture_not_regularity(self):
        data = overlay_report()
        self.assertTrue(data["not_a_regularity_proof"])
        self.assertFalse(data["composite"]["is_complete"])
        self.assertFalse(data["composite"]["is_regularity"])
        stacked_ids = {layer["id"] for layer in data["stacked"]}
        self.assertIn("L1-TORUS", stacked_ids)
        self.assertIn("L7-HARDY", stacked_ids)
        self.assertIn("L3-BERNSTEIN", stacked_ids)
        self.assertNotIn("L10-WELD", stacked_ids)
        self.assertNotIn("L11-ITUBE", stacked_ids)
        self.assertNotIn("L13-PHI", stacked_ids)

    def test_t3a_done_but_not_transposable(self):
        data = overlay_report()
        held = {layer["id"]: layer for layer in data["done_not_stacked"]}
        self.assertIn("L9-YOUNG", held)
        self.assertEqual(held["L9-YOUNG"]["clip_id"], "CLIP-T3-OUTER")
        waiting = {layer["id"] for layer in data["waiting"]}
        self.assertIn("L10-WELD", waiting)
        self.assertIn("L11-ITUBE", waiting)

    def test_holes_include_live_weld(self):
        data = overlay_report()
        clips = {h["clip_id"] for h in data["holes"]}
        self.assertIn("CLIP-T3-WELD", clips)
        self.assertIn("CLIP-B4b-ITUBE", clips)
        self.assertIn("CLIP-B6-SPIKE", clips)
        self.assertEqual(data["refine"]["first_hole"], "GAP-T3")

    def test_phi_never_stacked(self):
        data = overlay_report()
        self.assertEqual(data["refused"][0]["id"], "L13-PHI")


class TestOverlayCli(unittest.TestCase):
    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--overlay", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertGreaterEqual(payload["composite"]["counts"]["stacked"], 8)
        self.assertFalse(payload["composite"]["is_complete"])
        self.assertIn("GAP-T3", payload["refine"]["first_hole"])


if __name__ == "__main__":
    unittest.main()
