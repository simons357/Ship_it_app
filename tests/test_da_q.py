"""DA Q: GCD paper, floors, Q6, Q7 not seated."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_done import is_done_ask  # noqa: E402
from da_hunt import is_look_ask  # noqa: E402
from da_proof import is_proof_ask  # noqa: E402
from da_q import CLAIMS, FLOOR_LINES, NAMES, PAPER, is_q_ask, run  # noqa: E402


class DaQTests(unittest.TestCase):
    def test_q6_paper_q7_absent(self):
        tmp = Path(tempfile.mkdtemp()) / "da_q_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["Q1"]["verdict"], "pass")
        self.assertEqual(by["Q2"]["verdict"], "pass")
        self.assertEqual(by["Q3"]["verdict"], "fail")
        self.assertEqual(by["Q5"]["verdict"], "fail")
        self.assertEqual(by["Q6c"]["verdict"], "fail")
        self.assertEqual(by["Q7c"]["verdict"], "fail")
        self.assertEqual(by["Q8"]["verdict"], "fail")
        self.assertEqual(by["Q9"]["verdict"], "open")
        self.assertTrue(payload["meta"]["q7_not_seated"])
        self.assertTrue(payload["meta"]["full_floor_false"])
        self.assertEqual(PAPER["slot"], "Q")
        self.assertTrue(any(r["id"] == "Theorem P" for r in PAPER["sits"]))
        self.assertTrue(any(n["id"] == "Q7" for n in NAMES))
        ask = (
            "Look at my best gcd paper as well. "
            "And can it find the electoral floor? "
            "What about q6. Where does q7 fit in"
        )
        self.assertTrue(is_q_ask(ask))
        self.assertFalse(is_done_ask(ask))
        self.assertFalse(is_proof_ask(ask))
        self.assertFalse(is_look_ask(ask))
        self.assertTrue(is_q_ask("look at my best gcd paper"))
        self.assertTrue(is_q_ask("what about Q6"))
        self.assertTrue(is_q_ask("where does Q7 fit"))
        self.assertTrue(is_q_ask("can it find the electoral floor"))
        self.assertTrue(is_q_ask("Q6. Spectral floor"))
        self.assertEqual(
            [L["status"] for L in FLOOR_LINES],
            ["have"] * 5 + ["write", "follows", "open"],
        )
        self.assertEqual(payload["lines"][4]["status"], "have")
        self.assertEqual(payload["lines"][5]["status"], "write")
        self.assertTrue((ROOT / "docs" / "Q6-FLOOR-CHAIN.md").is_file())
        self.assertFalse(is_q_ask("use my best paper and write RH please"))
        self.assertTrue(is_proof_ask("use my best paper and write RH please"))
        self.assertFalse(is_q_ask("is that right for Navi Stokes"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-Q.md").is_file())


if __name__ == "__main__":
    unittest.main()
