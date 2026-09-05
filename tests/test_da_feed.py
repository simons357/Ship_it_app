"""Live feed: public test results stay in slot; glue refused."""

from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_feed import CLAIMS, SOURCES, fetch_source, freshness, run  # noqa: E402
from da_machine import classify_claim  # noqa: E402


class DaFeedTests(unittest.TestCase):
    def test_feed_is_process_not_a_close(self):
        tmp = Path(tempfile.mkdtemp()) / "da_feed_test.json"
        payload = run(out=tmp, fetch=False)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["F1"]["verdict"], "pass")
        self.assertEqual(by["F2"]["verdict"], "fail")
        self.assertEqual(by["F3"]["verdict"], "fail")
        self.assertEqual(by["F4"]["verdict"], "fail")
        self.assertEqual(by["F5"]["verdict"], "fail")
        self.assertEqual(by["F6"]["verdict"], "fail")
        self.assertEqual(by["F7"]["verdict"], "fail")
        self.assertEqual(by["F8"]["verdict"], "pass")
        self.assertEqual(by["F9"]["verdict"], "pass")
        self.assertEqual(by["F10"]["verdict"], "pass")
        self.assertEqual(by["F11"]["verdict"], "fail")
        self.assertTrue(payload["meta"]["ongoing"])
        self.assertTrue(payload["meta"]["must_stay_current"])
        self.assertTrue(payload["meta"]["does_not_write_X"])
        self.assertTrue(payload["meta"]["does_not_write_F"])
        self.assertTrue(payload["meta"]["fetch_miss_is_open"])
        self.assertFalse(payload["meta"]["fetched"])
        self.assertIsNone(payload["meta"]["fetched_at"])
        self.assertEqual(payload["counts"]["scanned"], 0)
        self.assertTrue(payload["freshness"]["stale"])
        self.assertFalse(payload["freshness"]["network"])
        self.assertTrue((ROOT / "docs" / "DA-FEED.md").is_file())

    def test_sources_include_ligo_and_accelerators(self):
        names = {s["name"] for s in SOURCES}
        self.assertIn("GWOSC_GWTC", names)
        self.assertIn("INSPIRE_LHC", names)
        self.assertIn("arXiv_hep_ex", names)
        self.assertIn("arXiv_math_AP", names)
        self.assertIn("PDG", names)
        slots = {s["name"]: s["slot"] for s in SOURCES}
        self.assertEqual(slots["GWOSC_GWTC"], "U")
        self.assertEqual(slots["INSPIRE_LHC"], "U")
        self.assertEqual(slots["arXiv_math_AP"], "B")
        self.assertEqual(len(SOURCES), len({s["id"] for s in SOURCES}))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))

    def test_fetch_source_returns_structure(self):
        src = next(s for s in SOURCES if s["name"] == "PDG")
        hit = fetch_source(src, timeout=2.0)
        self.assertIn("ok", hit)
        self.assertIn("items", hit)
        self.assertTrue(isinstance(hit["items"], list))

    def test_classify_roster_and_feed_land_in_u(self):
        r = classify_claim("living genius roster on the desk")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")
        r2 = classify_claim("scan the live feed for latest LIGO test results")
        self.assertEqual(r2["domain"], "U")
        self.assertEqual(r2["verdict"], "open")
        r3 = classify_claim("particle accelerator latest results on the feed")
        self.assertEqual(r3["domain"], "U")
        self.assertEqual(r3["verdict"], "open")
        r4 = classify_claim("DA feed freshness on status; stale DA is weaker")
        self.assertEqual(r4["domain"], "U")
        self.assertEqual(r4["verdict"], "open")
        r5 = classify_claim("must stay current with last scan age")
        self.assertEqual(r5["domain"], "U")
        self.assertEqual(r5["verdict"], "open")

    def test_freshness_is_local_and_stale_after_a_day(self):
        missing = Path(tempfile.mkdtemp()) / "no_such_feed.json"
        miss = freshness(path=missing)
        self.assertTrue(miss["stale"])
        self.assertEqual(miss["reason"], "missing")
        self.assertFalse(miss["network"])
        self.assertIsNone(miss["age_hours"])

        tmp = Path(tempfile.mkdtemp()) / "da_feed_fresh.json"
        clock = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)
        fresh_at = (clock - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        tmp.write_text(
            '{"meta": {"fetched_at": "%s"}, "scan": []}' % fresh_at
        )
        hit = freshness(path=tmp, now=clock)
        self.assertFalse(hit["stale"])
        self.assertEqual(hit["reason"], "fresh")
        self.assertFalse(hit["network"])
        self.assertAlmostEqual(hit["age_hours"], 2.0, places=2)

        old_at = (clock - timedelta(hours=25)).strftime("%Y-%m-%dT%H:%M:%SZ")
        tmp.write_text(
            '{"meta": {"fetched_at": "%s"}, "scan": []}' % old_at
        )
        old = freshness(path=tmp, now=clock)
        self.assertTrue(old["stale"])
        self.assertEqual(old["reason"], "older_than_24h")
        self.assertFalse(old["network"])
        self.assertAlmostEqual(old["age_hours"], 25.0, places=2)


if __name__ == "__main__":
    unittest.main()
