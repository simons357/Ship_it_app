#!/usr/bin/env python3
"""Breakdown children: split parent pieces, run parseable ones, path guides."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.breakdown_children import (
    breakdown_children,
    path_guides,
    run_breakdown_children,
    runnable_children,
)
from domain_architect.schema import RH_STATUS


ROOT = Path(__file__).resolve().parents[1]


class TestBreakdownChildren(unittest.TestCase):
    def test_children_split_parents_and_guide_the_path(self):
        kids = breakdown_children()
        ids = {c.child_id for c in kids}
        self.assertIn("HP-S0.a", ids)
        self.assertIn("HP-S0.c", ids)
        self.assertIn("HP-S3.b", ids)
        self.assertIn("GB-1", ids)
        self.assertIn("GB-4", ids)
        self.assertIn("NS-Φ.1", ids)
        self.assertIn("NS-F.1", ids)
        self.assertGreater(len(kids), len({c.parent_id for c in kids}))
        self.assertTrue(runnable_children())
        guides = " ".join(path_guides()).lower()
        self.assertIn("cannot", guides)
        self.assertIn("oscillator", guides)
        self.assertIn("glue", guides)
        text = run_breakdown_children().lower()
        self.assertIn("path guidance", text)
        self.assertIn(RH_STATUS, run_breakdown_children())
        self.assertNotIn("proves the riemann hypothesis", text)

    def test_cli_breakdown_children(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--breakdown-children"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Path guidance", proc.stdout)
        self.assertIn("HP-S0.c", proc.stdout)
        self.assertIn("GB-1", proc.stdout)
        self.assertIn("laplacian(G) = -delta", proc.stdout)
        self.assertIn("NS-Φ.2", proc.stdout)
        self.assertNotIn("proves the riemann hypothesis", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
