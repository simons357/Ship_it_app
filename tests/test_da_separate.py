"""Isolated-candidate run smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_separate import run  # noqa: E402


class DaSeparateTests(unittest.TestCase):
    def test_three_decks_all_alone(self):
        tmp = Path(tempfile.mkdtemp()) / "da_separate_test.json"
        payload = run(n=40, seed=1, out=tmp)
        self.assertEqual(payload["counts"]["GQ"], 8)
        self.assertEqual(payload["counts"]["SIX"], 16)
        self.assertEqual(payload["counts"]["COSMO"], 16)
        self.assertTrue(all(r["alone"] for r in payload["GQ"]))
        self.assertTrue(all(r["alone"] for r in payload["PUB"]))
        self.assertTrue(all(r["alone"] for r in payload["SIX"]))
        self.assertTrue(all(r["alone"] for r in payload["COSMO"]))
        self.assertFalse(any(r["glued"] for r in payload["PUB"]))
        self.assertTrue(all(r["produce_alone"] == "fail" for r in payload["COSMO"]))
        gq = {r["name"]: r["verdict"] for r in payload["GQ"]}
        self.assertEqual(gq["Einstein"], "pass")
        self.assertEqual(gq["vacuum_to_gravity"], "fail")
        six = {r["name"]: r for r in payload["SIX"]}
        self.assertEqual(six["R"]["verdict"], "fail")
        self.assertGreater(six["log_cc_ratio"]["delta_lock_R"], 0.02)


if __name__ == "__main__":
    unittest.main()
