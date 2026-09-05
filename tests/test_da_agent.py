"""DA tick: agent-shaped process; not a closer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_agent import CLAIMS, run  # noqa: E402


class DaAgentTests(unittest.TestCase):
    def test_agent_is_process_not_a_close(self):
        tmp = Path(tempfile.mkdtemp()) / "da_agent_test.json"
        payload = run(out=tmp, fetch=False)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["G1"]["verdict"], "pass")
        self.assertEqual(by["G2"]["verdict"], "pass")
        self.assertEqual(by["G3"]["verdict"], "fail")
        self.assertEqual(by["G4"]["verdict"], "fail")
        self.assertEqual(by["G5"]["verdict"], "fail")
        self.assertEqual(by["G6"]["verdict"], "fail")
        self.assertEqual(by["G7"]["verdict"], "pass")
        self.assertEqual(by["G8"]["verdict"], "fail")
        self.assertEqual(by["G9"]["verdict"], "fail")
        self.assertEqual(by["G10"]["verdict"], "open")
        self.assertEqual(by["G11"]["verdict"], "pass")
        self.assertTrue(payload["meta"]["agent_shaped"])
        self.assertTrue(payload["meta"]["not_a_closer"])
        self.assertTrue(payload["meta"]["does_not_replace_checker"])
        self.assertTrue(payload["meta"]["latest_data_belongs"])
        self.assertIn("Barker", payload["tick"]["seated_living"])
        self.assertIn("Robinson", payload["tick"]["seated_living"])
        self.assertIn("GWOSC_GWTC", payload["tick"]["feed_sources"])
        self.assertFalse(payload["tick"]["fetched"])
        self.assertIn("stale", payload["tick"]["freshness"])
        self.assertFalse(payload["tick"]["freshness"]["network"])
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-AGENT.md").is_file())


if __name__ == "__main__":
    unittest.main()
