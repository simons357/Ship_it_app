"""Gravity-quantum coupling inventory smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_gq import PAIRS, run  # noqa: E402


class DaGqTests(unittest.TestCase):
    def test_each_pair_separate_and_einstein_passes(self):
        tmp = Path(tempfile.mkdtemp()) / "da_gq_test.json"
        payload = run(out=tmp)
        self.assertEqual(len(payload["pairs"]), len(PAIRS))
        self.assertGreaterEqual(len(payload["pairs"]), 6)
        by_name = {p["name"]: p for p in payload["pairs"]}
        self.assertEqual(by_name["Einstein"]["verdict"], "pass")
        self.assertEqual(by_name["equivalence"]["verdict"], "pass")
        self.assertEqual(by_name["vacuum_to_gravity"]["verdict"], "fail")
        self.assertEqual(by_name["gauge3_to_G"]["verdict"], "fail")
        self.assertEqual(payload["leftovers"], ["vacuum_to_gravity", "hierarchy"])
        self.assertTrue(payload["meta"]["do_not_glue_to_gauge3"])


if __name__ == "__main__":
    unittest.main()
