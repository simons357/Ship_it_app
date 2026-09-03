#!/usr/bin/env python3
"""Stop at the wall; the missing piece sits between it and the next candidate."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.gap import format_gap, gap_chain, gap_report, locate_gap
from domain_architect.ns_chain import ns_chain
from domain_architect.ns_tube import tube_estimate


ROOT = Path(__file__).resolve().parents[1]


class TestLocateGap(unittest.TestCase):
    def test_fails_before_open_are_not_the_wall(self):
        steps = [
            {"step": "A", "status": "pass", "clip_id": "—", "inequality": "ok"},
            {"step": "B", "status": "fail", "clip_id": "CLIP-FAKE", "clip": "fake"},
            {"step": "C", "status": "pass", "clip_id": "—", "inequality": "ok"},
            {"step": "D", "status": "open", "clip_id": "CLIP-GAP", "remainder": "weld"},
            {"step": "E", "status": "pass", "clip_id": "—", "inequality": "later identity"},
        ]
        report = locate_gap(steps, book="B", chain="test").to_dict()
        self.assertTrue(report["stopped"])
        self.assertEqual(report["wall"]["step"], "D")
        self.assertEqual([s["step"] for s in report["walked"]], ["A", "C"])
        self.assertEqual(report["refused_before_wall"][0]["step"], "B")
        after = [c["step"] for c in report["candidates_after"]]
        self.assertIn("E", after)
        self.assertNotIn("E", [s["step"] for s in report["walked"]])

    def test_missing_piece_sits_between_last_walked_and_need(self):
        report = gap_report("B")
        self.assertTrue(report["stopped"])
        self.assertEqual(report["wall"]["step"], "T3b")
        self.assertEqual(report["missing"]["gap_id"], "GAP-T3")
        self.assertEqual(report["missing"]["between"], ["T3a", "T5"])
        clips = {c["clip_id"] for c in report["missing"]["clips"]}
        self.assertIn("CLIP-T3-WELD", clips)
        self.assertIn("CLIP-T3-OUTER", clips)
        outer = next(c for c in report["missing"]["clips"] if c["clip_id"] == "CLIP-T3-OUTER")
        self.assertIn("outer", outer["what"].lower())
        by = {c["step"]: c for c in report["candidates_after"]}
        self.assertEqual(by["T5"]["relation"], "needs_gap")
        self.assertEqual(by["T4"]["relation"], "parallel")
        self.assertFalse(by["spread Bony T"]["in_chain"])
        self.assertIn("Φ-cancel", {b["step"] for b in report["refused_bypasses"]})
        text = format_gap(report)
        self.assertIn("STOP", text)
        self.assertIn("MISSING PIECE", text)
        self.assertIn("CANDIDATES AFTER", text)
        self.assertIn("not walked", text.lower())


class TestChainGap(unittest.TestCase):
    def test_b5_after_b4b_is_a_candidate_not_a_walk(self):
        report = gap_chain()
        self.assertEqual(report["wall"]["step"], "B4b")
        walked = {s["step"] for s in report["walked"]}
        self.assertIn("B4", walked)
        self.assertNotIn("B5", walked)
        by = {c["step"]: c for c in report["candidates_after"]}
        self.assertEqual(by["B5"]["relation"], "parallel")
        self.assertEqual(by["B5b"]["relation"], "needs_gap")
        self.assertEqual(by["B6"]["relation"], "refused")

    def test_chain_json_still_has_later_steps(self):
        payload = ns_chain()
        self.assertEqual(payload["gap"]["wall"]["step"], "B4b")
        self.assertEqual(payload["counts"]["pass"], 5)
        names = [s["step"] for s in payload["steps"]]
        self.assertIn("B5", names)


class TestTubeGap(unittest.TestCase):
    def test_tube_payload_stops_at_t3b(self):
        payload = tube_estimate()
        self.assertEqual(payload["gap"]["wall"]["step"], "T3b")
        self.assertEqual(payload["gap"]["missing"]["between"], ["T3a", "T5"])


class TestGapCli(unittest.TestCase):
    def test_cli_tube_default(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--gap", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["stopped"])
        self.assertEqual(payload["wall"]["step"], "T3b")
        self.assertEqual(payload["missing"]["gap_id"], "GAP-T3")

    def test_cli_chain(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--gap", "CHAIN"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("WALL  B4b", proc.stdout)
        self.assertIn("MISSING PIECE", proc.stdout)
        self.assertIn("B5", proc.stdout)


if __name__ == "__main__":
    unittest.main()
