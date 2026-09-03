#!/usr/bin/env python3
"""Scan leftover holes against rudimentary pieces. A match is not a weld."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.scan import format_scan, scan_report
from domain_architect.visual import DEFAULT_STATE


ROOT = Path(__file__).resolve().parents[1]


class TestScanAnatomy(unittest.TestCase):
    def test_identified_not_smooth(self):
        data = scan_report("B")
        self.assertTrue(data["not_a_proof"])
        self.assertTrue(data["anatomy"]["identified"])
        self.assertFalse(data["anatomy"]["smooth"])
        self.assertFalse(data["focus"]["any_fill"])
        self.assertIn("NS-B", data["anatomy"]["views"])
        self.assertIn("J/X", data["anatomy"]["views"])
        self.assertGreaterEqual(data["anatomy"]["view_count"], 3)
        self.assertGreater(data["counts"]["pieces"], 20)

    def test_t3a_looks_like_fit_does_not_fill(self):
        named = {row["piece"]: row for row in scan_report("B")["focus"]["named_matches"]}
        self.assertEqual(named["L9-YOUNG"]["verdict"], "LOOKS_LIKE_FIT")
        self.assertEqual(named["L9-YOUNG"]["fills"], "no")
        self.assertEqual(named["Q6"]["verdict"], "WRONG_OBJECT")
        self.assertEqual(named["VIZ"]["verdict"], "WRONG_OBJECT")

    def test_inventory_does_not_fill_a_b_hole(self):
        matches = scan_report("GAP-T3")["focus"]["inventory_matches"]
        inv = [row for row in matches if row["kind"] == "inventory"]
        self.assertTrue(inv)
        self.assertTrue(all(row["fills"] == "no" for row in inv))
        gravity = next(row for row in inv if row["piece"] == "GRV-H001")
        self.assertEqual(gravity["verdict"], "WRONG_OBJECT")

    def test_format_has_no_forbidden_words(self):
        text = format_scan().lower()
        self.assertNotIn("clay", text)
        self.assertNotIn("millennium", text)
        self.assertIn("looks_like_fit", text)
        self.assertIn("anatomy", text)
        self.assertIn("leray", text)


class TestScanCli(unittest.TestCase):
    def test_cli_json_updates_see_state(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--scan", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["anatomy"]["smooth"])
        state = json.loads((ROOT / DEFAULT_STATE).read_text(encoding="utf-8"))
        self.assertEqual(state["action"], "scan")


if __name__ == "__main__":
    unittest.main()
