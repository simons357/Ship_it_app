"""Desk write-up: corpus method, all benches listed."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_desk import CORPUS_RULES, PAIRS, run  # noqa: E402


class DaDeskTests(unittest.TestCase):
    def test_corpus_method_not_toe_and_benches_listed(self):
        tmp = Path(tempfile.mkdtemp()) / "da_desk_test.json"
        payload = run(out=tmp)
        by = {r["id"]: r for r in payload["corpus_rules"]}
        self.assertEqual(by["K1"]["verdict"], "pass")
        self.assertEqual(by["K2"]["verdict"], "pass")
        self.assertEqual(by["K3"]["verdict"], "pass")
        self.assertEqual(by["K4"]["verdict"], "fail")
        self.assertEqual(by["K5"]["verdict"], "fail")
        self.assertEqual(by["K6"]["verdict"], "fail")
        self.assertEqual(by["K7"]["verdict"], "fail")
        pairs = {r["id"]: r for r in payload["pairs"]}
        self.assertEqual(pairs["Y2"]["verdict"], "pass")
        self.assertEqual(pairs["Y6"]["verdict"], "fail")
        self.assertEqual(pairs["Y7"]["verdict"], "fail")
        names = {m["name"] for m in payload["dream_team"]}
        self.assertIn("Leray", names)
        self.assertIn("Einstein", names)
        review = {m["name"] for m in payload["program_review"]}
        self.assertIn("Feynman", review)
        self.assertIn("Tesla", review)
        now = {m["name"] for m in payload["now_bench"]}
        self.assertIn("LVK collaboration", now)
        self.assertTrue(payload["meta"]["program_review"])
        self.assertTrue(payload["meta"]["anti_bullshit_device"])
        self.assertEqual(payload["purpose"]["as_process"], "pass")
        self.assertEqual(payload["purpose"]["as_unifier"], "fail")
        self.assertEqual(payload["meta"]["writeup"], "docs/DA-DESK.md")
        self.assertGreaterEqual(payload["vocab_n"], 20)
        self.assertEqual(len(CORPUS_RULES), len({r["id"] for r in CORPUS_RULES}))
        self.assertEqual(len(PAIRS), len({r["id"] for r in PAIRS}))
        self.assertTrue(payload["agent_shaped"])
        self.assertIn("Tao", payload["living_roster"])
        self.assertIn("Robinson", payload["living_roster"])
        self.assertIn("Pavlovic", payload["living_roster"])
        self.assertIn("Rusin", payload["living_roster"])
        self.assertIn("Germain", payload["living_roster"])
        self.assertIn("Cao", payload["living_roster"])
        self.assertIn("Hieber", payload["living_roster"])
        self.assertIn("Bedrossian", payload["living_roster"])
        self.assertIn("Kelliher", payload["living_roster"])
        self.assertIn("Silvestre", payload["living_roster"])
        self.assertIn("Schonbek", payload["living_roster"])
        self.assertIn("Ponce", payload["living_roster"])
        self.assertIn("Iftimie", payload["living_roster"])
        self.assertIn("Fursikov", payload["living_roster"])
        self.assertIn("Maremonti", payload["living_roster"])
        self.assertIn("Korobkov", payload["living_roster"])
        self.assertIn("Hishida", payload["living_roster"])
        self.assertIn("Mucha", payload["living_roster"])
        self.assertIn("Paicu", payload["living_roster"])
        self.assertIn("Gibbon", payload["living_roster"])
        self.assertIn("Ambrosio", payload["living_roster"])
        self.assertIn("Enciso", payload["living_roster"])
        self.assertIn("GWOSC_GWTC", payload["feed_sources"])
        self.assertIn("stale", payload["feed_freshness"])
        self.assertFalse(payload["feed_freshness"]["network"])
        self.assertTrue((ROOT / "docs" / "DA-DESK.md").is_file())
        self.assertTrue((ROOT / "docs" / "DA-PAPER.md").is_file())
        self.assertTrue((ROOT / "docs" / "DA-THINK-TANK.md").is_file())


if __name__ == "__main__":
    unittest.main()
