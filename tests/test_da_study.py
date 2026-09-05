"""DA study: questions pointed at DA; emit is not a solver pass."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_done import is_done_ask  # noqa: E402
from da_proof import is_proof_ask  # noqa: E402
from da_q import is_q_ask  # noqa: E402
from da_study import ASKS, CLAIMS, is_study_ask, run  # noqa: E402


class DaStudyTests(unittest.TestCase):
    def test_exam_split_write_from_finish(self):
        tmp = Path(tempfile.mkdtemp()) / "da_study_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["S1"]["verdict"], "pass")
        self.assertEqual(by["S2"]["verdict"], "pass")
        self.assertEqual(by["S3"]["verdict"], "pass")
        self.assertEqual(by["S4"]["verdict"], "fail")
        self.assertEqual(by["S5"]["verdict"], "fail")
        self.assertEqual(by["S6"]["verdict"], "open")
        asks = {a["id"]: a for a in ASKS}
        self.assertTrue(asks["B_write"]["can_write"])
        self.assertFalse(asks["B_write"]["can_finish"])
        self.assertTrue(asks["A_write"]["can_finish"])
        self.assertFalse(asks["RH_write"]["can_finish"])
        self.assertFalse(asks["Q7"]["can_finish"])
        self.assertTrue(payload["meta"]["questions_are_the_exam"])
        self.assertTrue(payload["meta"]["da_is_not_a_solver"])
        ask = (
            "These questions are all directed at da to see if he can do it or not."
        )
        self.assertTrue(is_study_ask(ask))
        self.assertFalse(is_proof_ask(ask))
        self.assertFalse(is_q_ask(ask))
        self.assertTrue(is_study_ask("can DA do it"))
        self.assertFalse(is_study_ask(""))
        self.assertFalse(is_study_ask("Track B please write"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-STUDY.md").is_file())


if __name__ == "__main__":
    unittest.main()
