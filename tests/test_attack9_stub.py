#!/usr/bin/env python3
"""Tests: Attack 9 packet/fan stub + honesty controls."""

from __future__ import annotations

import unittest
from io import StringIO
from unittest import mock

from scripts.attack9_packet_fan_stub import CONTROLS, DECISION_RULE, attack9_protocol, main


class TestAttack9Stub(unittest.TestCase):
    def test_protocol_bundle(self):
        rep = attack9_protocol()
        self.assertIn("Attack 9", rep["name"])
        self.assertEqual(rep["kill_lane"]["status"], "LIVE")
        self.assertTrue(rep["kill_lane"]["falsification"] == "LIVE")
        self.assertTrue(rep["kill_lane"]["proof"] == "LIVE")
        self.assertFalse(rep["ns_solved"])
        self.assertFalse(rep["sfe"])
        self.assertFalse(rep["decision_rule"]["proves_lemma_star"])
        self.assertTrue(rep["invariances_check"]["ok"])
        self.assertTrue(rep["refuse_kill_lane_closed"]["refused"])
        self.assertTrue(rep["refuse_legacy_comparison"]["refused"])
        self.assertGreaterEqual(len(CONTROLS), 6)
        self.assertIn("m^gamma", DECISION_RULE["fit"])

    def test_refuse_star_claim(self):
        rep = attack9_protocol(claim_star_from_samples=True)
        self.assertTrue(rep["refused"])
        self.assertTrue(rep["refuse_star_from_samples"]["refused"])
        self.assertIn("NOT SOLVED", rep["message"] + " " + rep["refuse_star_from_samples"]["message"])

    def test_cli_ok(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = main([])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("LIVE", out)
        self.assertIn("gamma", out.lower() + "γ")
        self.assertIn("NS solved: False", out)

    def test_cli_claim_star_exits_2(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = main(["--claim-star"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
