#!/usr/bin/env python3
"""Tube Hardy probe, Young wall-trace, and live I_tube chain."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.ns_tube import (
    hardy_wall_probe,
    tube_estimate,
    wall_trace_probe,
)


ROOT = Path(__file__).resolve().parents[1]


class TestHardyWall(unittest.TestCase):
    def test_probe_holds(self):
        probe = hardy_wall_probe()
        self.assertTrue(probe["holds"])
        self.assertLessEqual(probe["worst_lhs_over_rhs"], 1.05)
        self.assertEqual(probe["verdict"], "pass")


class TestWallTrace(unittest.TestCase):
    def test_young_from_outside_holds_when_outer_vanishes(self):
        probe = wall_trace_probe()
        self.assertTrue(probe["holds"])
        self.assertEqual(probe["verdict"], "pass")
        self.assertLessEqual(probe["worst_lhs_over_rhs"], 1.05)
        self.assertIn("T^3", probe["torus_obstruction"])


class TestTubeEstimate(unittest.TestCase):
    def test_domination_stays_open(self):
        report = tube_estimate()
        self.assertTrue(report["not_a_regularity_proof"])
        by = {s["step"]: s for s in report["steps"]}
        self.assertEqual(by["T2"]["status"], "pass")
        self.assertEqual(by["T3a"]["status"], "pass")
        self.assertEqual(by["T3b"]["status"], "open")
        self.assertEqual(by["T5"]["status"], "open")
        self.assertEqual(by["T7"]["status"], "open")
        self.assertIn("1/r^4", report["keep"])
        self.assertEqual(by["T3b"]["clip_id"], "CLIP-T3-WELD")
        self.assertEqual(report["monomial_mismatch"]["verdict"], "open")
        self.assertEqual(report["swirl_vs_angular"]["verdict"], "open")

    def test_cli(self):
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
        self.assertTrue(payload["wall_trace_probe"]["holds"])
        self.assertEqual(payload["wall_trace_probe"]["verdict"], "pass")


if __name__ == "__main__":
    unittest.main()
