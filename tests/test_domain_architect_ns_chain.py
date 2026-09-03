#!/usr/bin/env python3
"""Track B chain: each lemma as a shape delta."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.ns_chain import ns_chain


ROOT = Path(__file__).resolve().parents[1]


class TestNsChain(unittest.TestCase):
    def test_domain_stays_open(self):
        report = ns_chain()
        self.assertTrue(report["not_a_regularity_proof"])
        self.assertEqual(report["domain_verdict"], "open")
        self.assertIn("no closed bound", report["skeleton"]["Phi"].lower())

    def test_passes_do_not_fill_phi(self):
        report = ns_chain()
        by_id = {s["step"]: s for s in report["steps"]}
        for sid in ("B1", "B2", "B3", "B5"):
            self.assertEqual(by_id[sid]["verdict"], "pass")
            self.assertTrue(by_id[sid]["shape_delta"].startswith("none"))
        self.assertEqual(by_id["B-reg"]["verdict"], "open")
        self.assertEqual(by_id["B4b"]["verdict"], "open")
        self.assertEqual(by_id["B6"]["verdict"], "fail")
        self.assertTrue(by_id["B6"]["clip_id"].startswith("CLIP-"))

    def test_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--chain", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["counts"]["pass"], 5)
        self.assertEqual(payload["counts"]["fail"], 4)
        self.assertEqual(payload["counts"]["open"], 3)


if __name__ == "__main__":
    unittest.main()
