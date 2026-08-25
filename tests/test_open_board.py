#!/usr/bin/env python3
"""Honest OPEN board: withdrawn/rejected/missing are not infinite OPEN math."""

from __future__ import annotations

import json
import unittest

from domain_architect.app import handle_api
from domain_architect.open_board import cycle_open_board, open_board
from domain_architect.pipeline import run_named_cycle
from domain_architect.schema import CorrespondenceKind, ValidationGate
from domain_architect.synthesize import (
    inverse_design_architecture,
    is_recognized_setpoint,
)


class TestA13FailClosed(unittest.TestCase):
    def test_setpoints_still_get_a_controller(self):
        self.assertTrue(is_recognized_setpoint("x=1"))
        self.assertTrue(is_recognized_setpoint("x★ = 1"))
        self.assertTrue(is_recognized_setpoint("x → 1.0"))
        cand = inverse_design_architecture("x=1", ["|u|<=1"])
        self.assertEqual(cand.name, "inverse_design[second_order_linear]")
        self.assertTrue(any("control u" in c for c in cand.components))

    def test_profit_and_ns_are_refused(self):
        profit = inverse_design_architecture("maximize profit", ["tax law"])
        self.assertEqual(profit.name, "inverse_design[refused]")
        self.assertFalse(any("control u" in c for c in profit.components))
        ns = inverse_design_architecture(
            "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl",
            ["classical NS"],
        )
        self.assertEqual(ns.name, "inverse_design[refused]")
        joined = ns.hypothesis.lower()
        self.assertIn("strain", joined)
        self.assertIn("not claimed", joined)
        self.assertIn("fail-closed", joined)


class TestOpenBoard(unittest.TestCase):
    def test_counts_and_still_open_are_short(self):
        payload = open_board()
        self.assertEqual(payload["protocol"], "open-board")
        self.assertTrue(payload["a13_fail_closed"])
        self.assertGreaterEqual(payload["counts"]["CLOSED_WITHDRAWN"], 3)
        self.assertGreaterEqual(payload["counts"]["CLOSED_REJECTED"], 2)
        self.assertEqual(payload["counts"]["STILL_OPEN"], 3)
        self.assertEqual(payload["counts"]["CONDITIONAL"], 3)
        self.assertEqual(payload["counts"].get("CLOSED_IDENTITY"), 2)
        self.assertEqual(payload["counts"].get("DA_ENGINEERING"), 1)
        still_ids = [row["id"] for row in payload["still_open"]]
        self.assertEqual(
            still_ids,
            ["gap1-step-f", "route-j", "ns-open"],
        )
        cond_ids = [row["id"] for row in payload["conditional"]]
        self.assertEqual(cond_ids, ["swirl-strain", "ring-snd", "paper2-simplex"])
        self.assertFalse(payload["leftover_split"]["reconstruction_closed"])
        self.assertEqual(payload["leftover_split"]["honest_close"], "CONDITIONAL")
        self.assertTrue(
            all(p["status"] == "CONDITIONAL" for p in payload["leftover_split"]["pieces"])
        )
        self.assertIsNotNone(payload["localized_repair"]["graft"])
        self.assertIn("lemma 6.1", payload["localized_repair"]["graft"].lower())
        self.assertEqual(payload["translate_snd_vs_h"]["mapping"], {})
        self.assertEqual(payload["kind"], CorrespondenceKind.ANALOGY.value)
        blob = json.dumps(payload).lower()
        self.assertIn("withdrawn", blob)
        self.assertIn("do not treat a13 refuse as a da-vc-01 pass", blob)
        self.assertIn("not claimed", blob)

    def test_cycle_and_api(self):
        report = cycle_open_board()
        self.assertEqual(report.mode, "open-board")
        self.assertEqual(report.validation_gate, ValidationGate.MATHEMATICAL)
        self.assertEqual(report.translation.mapping, {})
        named = run_named_cycle("open-board")
        self.assertEqual(named.mode, "open-board")
        status, body, _ = handle_api("/api/open-board", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertTrue(payload["a13_fail_closed"])
        status, body, _ = handle_api("/api/cycle", {"name": "open-board"})
        self.assertEqual(status, 200)
        cycle = json.loads(body)
        self.assertEqual(cycle["mode"], "open-board")
        self.assertIn("open_board_honest_close", json.dumps(cycle))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
