#!/usr/bin/env python3
"""Energy as a visual object: Bernstein fills; outside does not fill the tube."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.energy_play import (
    energy_play,
    play_bernstein,
    play_energy_tank,
    play_guess_inside_from_outside,
    play_shared_tail,
)


ROOT = Path(__file__).resolve().parents[1]


class TestBernsteinFill(unittest.TestCase):
    def test_shell_energy_fills_enstrophy(self):
        row = play_bernstein()
        self.assertEqual(row["status"], "identity")
        self.assertFalse(row["not_a_lemma"])
        self.assertTrue(row["warped"])
        self.assertGreater(row["peak_enstrophy_shell"], row["peak_energy_shell"])


class TestGuessFromOutside(unittest.TestCase):
    def test_even_blob_fills_and_tube_blob_does_not(self):
        blob = play_guess_inside_from_outside()
        self.assertTrue(blob["not_a_lemma"])
        self.assertTrue(blob["even_guess_works"])
        self.assertTrue(blob["tube_guess_fails"])
        self.assertGreater(blob["error_when_tube_concentrated"], blob["error_when_even"])


class TestCannotFill(unittest.TestCase):
    def test_shared_tail_two_cores(self):
        tail = play_shared_tail()
        self.assertTrue(tail["same_tail"])
        self.assertFalse(tail["same_peak"])
        self.assertEqual(tail["clip_id"], "CLIP-B2-OCCUPATION")

    def test_tank_does_not_bound_x(self):
        tank = play_energy_tank()
        self.assertTrue(tank["X_unbounded"])
        self.assertEqual(tank["clip_id"], "CLIP-B6-SPIKE")


class TestEnergyPlayCli(unittest.TestCase):
    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--energy-play", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["identity"]["warped"])
        self.assertFalse(payload["gap"]["outside_fills_tube"])
        self.assertFalse(payload["gap"]["energy_fills_X_infty"])
        self.assertTrue(payload["play"]["tube_guess_fails"])


if __name__ == "__main__":
    unittest.main()
