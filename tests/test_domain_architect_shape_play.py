#!/usr/bin/env python3
"""Fill the other side of a shape and measure. Play is not a lemma."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.shape_play import play_cylinder, play_strain, shape_play


ROOT = Path(__file__).resolve().parents[1]


class TestStrainFill(unittest.TestCase):
    def test_third_eigenvalue_is_forced(self):
        row = play_strain(1.0, 0.4)
        self.assertTrue(row["sum_is_zero"])
        self.assertEqual(row["status"], "identity")
        self.assertAlmostEqual(row["filled"]["λ3"], -1.4)
        self.assertEqual(row["clip_still_open"], "CLIP-B3b-ALIGN")


class TestCylinderPlay(unittest.TestCase):
    def test_even_reflect_fills_outer_and_young_measures(self):
        cyl = play_cylinder()
        self.assertTrue(cyl["not_a_lemma"])
        even = next(c for c in cyl["completions"] if c["id"] == "even_reflect")
        self.assertTrue(even["extra_E"])
        self.assertTrue(even["outer_vanishes"])
        self.assertTrue(even["young_holds"])
        self.assertIn("CLIP-T3-WELD", even["does_not_buy"])

    def test_refuse_leaves_the_cut(self):
        cyl = play_cylinder()
        refuse = next(c for c in cyl["completions"] if c["id"] == "refuse")
        self.assertFalse(refuse["extra_E"])
        self.assertFalse(refuse["young_holds"])

    def test_radial_play_does_not_buy_t3b(self):
        report = shape_play()
        self.assertTrue(report["gap"]["even_reflect_buys_T3a"])
        self.assertFalse(report["gap"]["even_reflect_buys_T3b"])
        self.assertIn("CLIP-T3-WELD", report["gap"]["still_missing"])
        self.assertEqual(report["three_shell"]["status"], "cannot_fill")


class TestShapePlayCli(unittest.TestCase):
    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--shape-play", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["not_a_regularity_proof"])
        self.assertTrue(payload["cylinder"]["not_a_lemma"])
        self.assertTrue(payload["strain"]["sum_is_zero"])


if __name__ == "__main__":
    unittest.main()
