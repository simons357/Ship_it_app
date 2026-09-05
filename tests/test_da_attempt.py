"""DA attempt: best A and RH; dream team looks; vote is not a close."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_attempt import CLAIMS, JOBS, is_attempt_ask, parse_job, parse_jobs, run  # noqa: E402
from da_proof import is_proof_ask  # noqa: E402
from da_repair import is_repair_ask  # noqa: E402


class DaAttemptTests(unittest.TestCase):
    def test_takes_best_and_refuses_a_vote(self):
        tmp = Path(tempfile.mkdtemp()) / "da_attempt_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["D1"]["verdict"], "pass")
        self.assertEqual(by["D2"]["verdict"], "pass")
        self.assertEqual(by["D3"]["verdict"], "pass")
        self.assertEqual(by["D4"]["verdict"], "fail")
        self.assertEqual(by["D5"]["verdict"], "fail")
        self.assertEqual(by["D6"]["verdict"], "pass")
        self.assertEqual(by["D7"]["verdict"], "fail")
        self.assertEqual(by["D8"]["verdict"], "fail")
        self.assertEqual(by["D9"]["verdict"], "open")
        self.assertEqual(by["D10"]["verdict"], "open")
        self.assertEqual(by["D11"]["verdict"], "pass")
        self.assertEqual(by["D12"]["verdict"], "fail")
        self.assertEqual(by["D13"]["verdict"], "fail")
        self.assertEqual(by["D14"]["verdict"], "fail")
        self.assertEqual(by["D15"]["verdict"], "open")
        self.assertEqual(by["D16"]["verdict"], "open")
        self.assertTrue(payload["meta"]["takes_mine"])
        self.assertTrue(payload["meta"]["uses_dream_team"])
        self.assertTrue(payload["meta"]["uses_einstein_tesla"])
        self.assertTrue(payload["meta"]["vote_is_not_a_close"])
        self.assertTrue(payload["meta"]["a_this_pde_complete"])
        self.assertTrue(payload["meta"]["rh_write_not_complete"])
        self.assertTrue(payload["meta"]["q_is_not_rh"])
        self.assertTrue(payload["meta"]["snd_is_not_x"])
        self.assertEqual(payload["picked"], [])
        self.assertEqual([j["id"] for j in payload["jobs"]], ["A", "B", "RH", "SND", "H"])
        self.assertTrue(JOBS["B"].get("do"))
        self.assertEqual(parse_job(ask="UN augmented"), "B")
        self.assertEqual(parse_job(ask="unaugmented"), "B")
        self.assertTrue(is_attempt_ask("UN augmented"))
        self.assertEqual(parse_job(ask="close NS in augmented"), "A")
        a = JOBS["A"]
        rh = JOBS["RH"]
        snd = JOBS["SND"]
        h = JOBS["H"]
        self.assertEqual(len(a["team"]), 6)
        self.assertEqual(len(rh["team"]), 6)
        self.assertIn("Einstein", [c["who"] for c in snd["team"]])
        self.assertIn("Tesla", [c["who"] for c in snd["team"]])
        self.assertIn("Einstein", [c["who"] for c in h["team"]])
        self.assertIn("Tesla", [c["who"] for c in h["team"]])
        self.assertTrue(any("SND-C" in line for line in snd["need_to_close"]))
        self.assertTrue(any("two H" in line for line in h["need_to_close"]))
        self.assertTrue(all(c["sits"] for c in a["team"]))
        self.assertIn("Ladyzhenskaya", [c["who"] for c in a["team"]])
        self.assertIn("Hardy", [c["who"] for c in rh["team"]])
        self.assertTrue(any(p["id"] == "A_theorem" and p["verdict"] == "pass" for p in a["progress"]))
        self.assertTrue(any(p["id"] == "A_uniform_H1" and p["verdict"] == "open" for p in a["progress"]))
        self.assertTrue(any(p["id"] == "RH6" and p["verdict"] == "open" for p in rh["progress"]))
        self.assertTrue(any(p["id"] == "Q_is_RH" and p["verdict"] == "fail" for p in rh["progress"]))
        self.assertTrue(is_attempt_ask("analyze my augmented"))
        self.assertTrue(is_attempt_ask("dream team look at my RH"))
        self.assertTrue(is_attempt_ask("complete the chain"))
        self.assertTrue(is_attempt_ask("Q1 with renormalization"))
        self.assertTrue(is_attempt_ask("what do I need to close SND"))
        self.assertTrue(is_attempt_ask("Einstein and Tesla figure out H"))
        self.assertTrue(is_attempt_ask("now what close NS in augmented please"))
        self.assertEqual(parse_job(ask="close NS in augmented"), "A")
        self.assertTrue(JOBS["A"].get("do"))
        self.assertFalse(is_attempt_ask(""))
        self.assertFalse(is_attempt_ask("now what"))
        self.assertFalse(is_attempt_ask("RH proof chain please"))
        self.assertTrue(is_proof_ask("RH proof chain please"))
        self.assertTrue(is_repair_ask("what's wrong with the augmented one"))
        self.assertFalse(is_attempt_ask("what's wrong with the augmented one"))
        self.assertEqual(parse_job(ask="analyze my augmented"), "A")
        self.assertEqual(parse_job(ask="dream team look at my RH"), "RH")
        self.assertEqual(parse_jobs(ask="analyze my A and RH"), ["A", "RH"])
        self.assertEqual(parse_jobs(ask="Einstein and Tesla figure it out"), ["SND", "H"])
        self.assertEqual(parse_job(ask="close H"), "H")
        self.assertEqual(parse_job(job="SND"), "SND")
        self.assertEqual(parse_job(job="RH"), "RH")
        only = run(out=Path(tempfile.mkdtemp()) / "da_attempt_rh.json", job="RH")
        self.assertEqual(only["picked"], ["RH"])
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-ATTEMPT.md").is_file())


if __name__ == "__main__":
    unittest.main()
