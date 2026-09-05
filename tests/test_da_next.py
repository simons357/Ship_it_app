"""DA next: now-what spoke; not a closer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_next import CLAIMS, is_lost_ask, translate, run  # noqa: E402


class DaNextTests(unittest.TestCase):
    def test_next_is_spoke_not_a_close(self):
        tmp = Path(tempfile.mkdtemp()) / "da_next_test.json"
        payload = run(out=tmp, ask="what do we do from here", fetch=False)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["W1"]["verdict"], "pass")
        self.assertEqual(by["W2"]["verdict"], "pass")
        self.assertEqual(by["W3"]["verdict"], "pass")
        self.assertEqual(by["W4"]["verdict"], "fail")
        self.assertEqual(by["W5"]["verdict"], "fail")
        self.assertEqual(by["W6"]["verdict"], "fail")
        self.assertEqual(by["W7"]["verdict"], "fail")
        self.assertEqual(by["W8"]["verdict"], "fail")
        self.assertEqual(by["W9"]["verdict"], "open")
        self.assertEqual(by["W10"]["verdict"], "pass")
        self.assertTrue(payload["meta"]["not_a_closer"])
        self.assertTrue(payload["meta"]["target_is_not_F"])
        self.assertTrue(payload["wall"]["not_F"])
        self.assertIn("X", payload["wall"]["target_B"])
        self.assertEqual(payload["translate"]["slot"], "B")
        self.assertEqual(payload["translate"]["chair"], "Tao")
        self.assertIn("GWOSC_GWTC", payload["rim"]["feed_sources"])
        self.assertFalse(payload["rim"]["fetched"])
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-NEXT.md").is_file())
        self.assertIn("nowwhat", payload["nowwhat"])
        self.assertTrue(any(s["name"] == "nowwhat" for s in payload["spokes"]))
        self.assertTrue(any(s["name"] == "hunt" for s in payload["spokes"]))
        self.assertTrue(any(s["name"] == "look" for s in payload["spokes"]))
        self.assertTrue(any(s["name"] == "from" for s in payload["spokes"]))
        self.assertTrue(any(s["name"] == "proof" for s in payload["spokes"]))
        self.assertTrue(any(s["name"] == "repair" for s in payload["spokes"]))
        self.assertFalse(is_lost_ask("what do we do from here"))

    def test_translate_splits_F_from_X(self):
        hit = translate("is the target F or the realization variable")
        self.assertEqual(hit["slot"], "U")
        self.assertIn("not F", hit["english"])
        ligo = translate("do we need the latest LIGO data")
        self.assertEqual(ligo["slot"], "U")
        a1 = translate("is the wall Fefferman alignment")
        self.assertEqual(a1["slot"], "B")
        self.assertEqual(a1["chair"], "Fefferman")


if __name__ == "__main__":
    unittest.main()
