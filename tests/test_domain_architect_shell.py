#!/usr/bin/env python3
"""Inside plus outer shell: silhouette may already be identified."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.shell import format_shell, shell_report
from domain_architect.visual import DEFAULT_STATE


ROOT = Path(__file__).resolve().parents[1]


class TestShell(unittest.TestCase):
    def test_identity_shell_is_a_giveaway(self):
        data = shell_report("B")
        self.assertTrue(data["giveaway"]["dead_giveaway"])
        self.assertTrue(data["intended_move"])
        self.assertFalse(data["giveaway"]["smooth"])
        self.assertIn("NS-B", data["giveaway"]["catalog"])
        self.assertIn("J/X", data["giveaway"]["catalog"])
        self.assertEqual(data["play_shell"]["status"], "play")
        self.assertEqual(data["play_shell"]["clip_id"], "CLIP-T3-OUTER")
        self.assertFalse(data["play_shell"]["match"]["already_identified"])
        text = format_shell(data).lower()
        self.assertNotIn("clay", text)
        self.assertIn("dead giveaway", text)
        self.assertIn("this is the move", text)

    def test_q_shell_is_not_fluids(self):
        data = shell_report("Q")
        self.assertTrue(data["giveaway"]["dead_giveaway"])
        self.assertIn("Q6", data["giveaway"]["catalog"])
        self.assertTrue(data["play_shell"]["trap"])

    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--shell", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["giveaway"]["dead_giveaway"])
        state = json.loads((ROOT / DEFAULT_STATE).read_text(encoding="utf-8"))
        self.assertEqual(state["action"], "shell")


if __name__ == "__main__":
    unittest.main()
