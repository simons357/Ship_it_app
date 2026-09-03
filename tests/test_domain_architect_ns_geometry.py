#!/usr/bin/env python3
"""Geometric analysis of Track B is architecture, not a close."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.ns_geometry import ns_geometry


ROOT = Path(__file__).resolve().parents[1]


class TestNsGeometry(unittest.TestCase):
    def test_not_a_proof(self):
        report = ns_geometry()
        self.assertTrue(report["not_a_regularity_proof"])
        self.assertTrue(any("I_tube" in x for x in report["open_geometrically"]))
        self.assertIn("AXIS-TUBE", {o["id"] for o in report["objects"]})

    def test_b3b_alignment_stays_a_remainder(self):
        steps = {s["step"]: s for s in ns_geometry()["steps"]}
        self.assertEqual(steps["B3"]["remainder_id"], "CLIP-B3b-ALIGN")
        self.assertEqual(steps["B4b"]["proved"], "nothing yet (open)")

    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--geometry", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertIn("physical", payload["diagrams"])
        self.assertIn("I_off", payload["split"])


if __name__ == "__main__":
    unittest.main()
