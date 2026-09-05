"""DA done: emit is not classical NS finished."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_attempt import is_attempt_ask  # noqa: E402
from da_done import CLAIMS, ROWS, is_done_ask, run  # noqa: E402
from da_proof import is_proof_ask  # noqa: E402


class DaDoneTests(unittest.TestCase):
    def test_split_a_done_b_open(self):
        tmp = Path(tempfile.mkdtemp()) / "da_done_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["E1"]["verdict"], "pass")
        self.assertEqual(by["E2"]["verdict"], "pass")
        self.assertEqual(by["E3"]["verdict"], "fail")
        self.assertEqual(by["E4"]["verdict"], "fail")
        self.assertEqual(by["E5"]["verdict"], "fail")
        self.assertEqual(by["E6"]["verdict"], "open")
        rows = {r["id"]: r for r in ROWS}
        self.assertTrue(rows["A_this_pde"]["done"])
        self.assertFalse(rows["A_uniform"]["done"])
        self.assertFalse(rows["B"]["done"])
        self.assertTrue(rows["emit"]["done"])
        self.assertFalse(rows["A_is_B"]["done"])
        self.assertTrue(payload["meta"]["a_this_pde_done"])
        self.assertTrue(payload["meta"]["b_not_done"])
        self.assertTrue(payload["meta"]["emit_is_not_qed"])
        ask = "is that right for Navi Stokes"
        self.assertTrue(is_done_ask(ask))
        self.assertFalse(is_proof_ask(ask))
        self.assertFalse(is_attempt_ask(ask))
        self.assertTrue(is_done_ask("is Navier-Stokes done"))
        self.assertTrue(is_done_ask("can DA finish it"))
        self.assertTrue(is_done_ask("looks like it is done"))
        self.assertFalse(is_done_ask(""))
        self.assertFalse(is_done_ask("Track B please write"))
        self.assertTrue(is_proof_ask("Track B please write"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-DONE.md").is_file())


if __name__ == "__main__":
    unittest.main()
