"""DA proof: write the NS chain; emit is not QED."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_attempt import is_attempt_ask  # noqa: E402
from da_brute import is_brute_ask  # noqa: E402
from da_hunt import is_look_ask  # noqa: E402
from da_picture import is_picture_ask  # noqa: E402
from da_proof import CLAIMS, LINES, PROBLEMS, is_proof_ask, parse_problem, run  # noqa: E402


class DaProofTests(unittest.TestCase):
    def test_writes_the_chain(self):
        tmp = Path(tempfile.mkdtemp()) / "da_proof_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["C1"]["verdict"], "pass")
        self.assertEqual(by["C2"]["verdict"], "pass")
        self.assertEqual(by["C3"]["verdict"], "fail")
        self.assertEqual(by["C4"]["verdict"], "fail")
        self.assertEqual(by["C5"]["verdict"], "fail")
        self.assertEqual(by["C6"]["verdict"], "open")
        self.assertEqual(by["C7"]["verdict"], "fail")
        self.assertEqual(by["C8"]["verdict"], "open")
        self.assertTrue(payload["meta"]["nothing_wrong_with_asking"])
        self.assertTrue(payload["meta"]["q_is_not_rh"])
        self.assertEqual(payload["problem"], "NS")
        self.assertEqual(payload["counts"]["write"], 1)
        self.assertEqual([L["status"] for L in LINES], ["have"] * 5 + ["write"] + ["follows"] * 3)
        self.assertTrue(is_proof_ask("write me the proof chain for Navier-Stokes"))
        self.assertTrue(is_proof_ask("Xavier Stokes"))
        self.assertTrue(is_proof_ask("proof chain"))
        self.assertTrue(is_proof_ask("Track B please write"))
        self.assertEqual(parse_problem(ask="Track B please write"), "NS")
        self.assertFalse(is_look_ask("Track B please write"))
        self.assertFalse(is_brute_ask("Track B please write"))
        self.assertFalse(is_picture_ask("Track B please write"))
        self.assertFalse(is_attempt_ask("Track B please write"))
        self.assertTrue(is_proof_ask("RH proof chain please"))
        self.assertTrue(is_proof_ask("RH"))
        self.assertFalse(is_proof_ask(""))
        self.assertFalse(is_proof_ask("now what"))
        self.assertEqual(parse_problem(ask="RH proof chain please"), "RH")
        self.assertEqual(parse_problem(ask="Xavier Stokes"), "NS")
        rh = run(out=Path(tempfile.mkdtemp()) / "da_proof_rh.json", problem="RH")
        self.assertEqual(rh["problem"], "RH")
        self.assertIn("1/2", rh["theorem"]["aimed"])
        self.assertTrue(any("inverse-GCD" in line for line in rh["object"]["window"]))
        self.assertEqual(set(PROBLEMS), {"NS", "RH"})
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-PROOF.md").is_file())
        self.assertTrue((ROOT / "docs" / "NS-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "RH-PROOF-CHAIN.md").is_file())


if __name__ == "__main__":
    unittest.main()
