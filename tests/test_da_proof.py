"""DA proof: write the NS chain; emit is not QED."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_proof import CLAIMS, LINES, is_proof_ask, run  # noqa: E402


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
        self.assertTrue(payload["meta"]["nothing_wrong_with_asking"])
        self.assertEqual(payload["counts"]["write"], 1)
        self.assertEqual([L["status"] for L in LINES], ["have"] * 5 + ["write"] + ["follows"] * 3)
        self.assertTrue(is_proof_ask("write me the proof chain for Navier-Stokes"))
        self.assertTrue(is_proof_ask("Xavier Stokes"))
        self.assertTrue(is_proof_ask("proof chain"))
        self.assertFalse(is_proof_ask(""))
        self.assertFalse(is_proof_ask("now what"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-PROOF.md").is_file())
        self.assertTrue((ROOT / "docs" / "NS-PROOF-CHAIN.md").is_file())


if __name__ == "__main__":
    unittest.main()
