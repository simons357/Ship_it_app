"""Live feed: public test results stay in slot; glue refused."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_feed import CLAIMS, SOURCES, fetch_source, run  # noqa: E402
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
        self.assertTrue(payload["meta"]["ongoing"])
        self.assertTrue(payload["meta"]["does_not_write_X"])
        self.assertTrue(payload["meta"]["does_not_write_F"])
        self.assertTrue(payload["meta"]["fetch_miss_is_open"])
        self.assertEqual(payload["counts"]["scanned"], 0)
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


if __name__ == "__main__":
    unittest.main()
