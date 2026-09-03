#!/usr/bin/env python3
"""Inner think tank consult: insight is not a weld."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.think_tank import consult, format_consult
from domain_architect.scan import scan_report


ROOT = Path(__file__).resolve().parents[1]


class TestConsult(unittest.TestCase):
    def test_experts_on_scan_do_not_fill(self):
        data = consult("scan")
        names = {row["name"] for row in data["notes"]}
        self.assertIn("Jean Leray", names)
        self.assertIn("Beale–Kato–Majda", names)
        self.assertIn("Caffarelli–Kohn–Nirenberg", names)
        self.assertIn("Jacques Hadamard", names)
        self.assertIn("Richard Hamming", names)
        self.assertEqual(data["fills_found"], 0)
        self.assertTrue(all(n["fills_gap"] == "no" for n in data["notes"]))
        text = format_consult(data).lower()
        self.assertNotIn("clay", text)
        self.assertNotIn("millennium", text)
        self.assertIn("insight is not a weld", text)

    def test_method_consult_is_general(self):
        data = consult("method")
        names = {row["name"] for row in data["notes"]}
        self.assertIn("Hermann Weyl", names)
        self.assertNotIn("Jean Leray", names)
        self.assertEqual(data["fills_found"], 0)
        tank = scan_report("B")["think_tank"]
        self.assertEqual(tank["fills_found"], 0)
        self.assertGreaterEqual(len(tank["notes"]), 8)

    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--consult", "scan", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["appendage"], "THINK")
        self.assertEqual(payload["fills_found"], 0)


if __name__ == "__main__":
    unittest.main()
