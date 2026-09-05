"""DA repair: take A / SND / H; name the fault; do not export A."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_repair import CLAIMS, JOBS, is_repair_ask, parse_job, parse_jobs, run  # noqa: E402


class DaRepairTests(unittest.TestCase):
    def test_takes_mine_and_names_the_write(self):
        tmp = Path(tempfile.mkdtemp()) / "da_repair_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["R1"]["verdict"], "pass")
        self.assertEqual(by["R2"]["verdict"], "pass")
        self.assertEqual(by["R3"]["verdict"], "fail")
        self.assertEqual(by["R4"]["verdict"], "fail")
        self.assertEqual(by["R5"]["verdict"], "fail")
        self.assertEqual(by["R6"]["verdict"], "fail")
        self.assertEqual(by["R7"]["verdict"], "open")
        self.assertEqual(by["R8"]["verdict"], "open")
        self.assertEqual(by["R9"]["verdict"], "open")
        self.assertTrue(payload["meta"]["takes_mine"])
        self.assertTrue(payload["meta"]["a_is_closed_for_this_pde"])
        self.assertTrue(payload["meta"]["a_is_not_b"])
        self.assertEqual(payload["picked"], [])
        self.assertEqual([j["id"] for j in payload["jobs"]], ["A", "SND", "H"])
        self.assertEqual(set(JOBS), {"A", "SND", "H"})
        self.assertIn("A_uniform_H1", JOBS["A"]["fault"])
        self.assertIn("not a repair", JOBS["A"]["do_not"].lower() + " " + by["R3"]["why"].lower())
        self.assertIn("CONC", JOBS["SND"]["repair"])
        self.assertIn("SPREAD", JOBS["SND"]["repair"])
        self.assertIn("-1/4", JOBS["H"]["repair"])
        self.assertNotIn("A=>B", JOBS["A"]["repair"])
        self.assertTrue(is_repair_ask("what's wrong with the augmented one"))
        self.assertTrue(is_repair_ask("how to fix SND"))
        self.assertTrue(is_repair_ask("repair H"))
        self.assertTrue(is_repair_ask("da repair"))
        self.assertTrue(is_repair_ask("fix a"))
        self.assertFalse(is_repair_ask(""))
        self.assertFalse(is_repair_ask("now what"))
        self.assertFalse(is_repair_ask("from my work"))
        self.assertEqual(parse_job(ask="what's wrong with the augmented one"), "A")
        self.assertEqual(parse_job(ask="fix SND"), "SND")
        self.assertEqual(parse_job(ask="repair H"), "H")
        self.assertEqual(parse_job(job="A"), "A")
        self.assertEqual(parse_jobs(ask="fix SND and H"), ["SND", "H"])
        self.assertEqual(parse_jobs(ask="repair A"), ["A"])
        a_only = run(out=Path(tempfile.mkdtemp()) / "da_repair_a.json", job="A")
        self.assertEqual(a_only["picked"], ["A"])
        self.assertEqual([j["id"] for j in a_only["jobs"]], ["A"])
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-REPAIR.md").is_file())


if __name__ == "__main__":
    unittest.main()
