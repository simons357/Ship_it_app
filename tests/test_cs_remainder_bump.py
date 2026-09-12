"""ABC_λ evaluator. Finite climb ≠ falsifier. Not a plate."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.cs_remainder_bump import localized_abc, probe_hat  # noqa: E402

JSON = ROOT / "results" / "cs_remainder_bump" / "cs_remainder.json"
CORE = ROOT / "results" / "cs_remainder_bump" / "exact_core_check.json"
PHONE = ROOT / "docs" / "CS-REMAINDER.md"
SCORE = ROOT / "docs" / "ns-recovery" / "CS-REMAINDER-VS-DA-REJECT.md"


class CsRemainderTests(unittest.TestCase):
    def test_phone_and_json(self):
        self.assertTrue(PHONE.is_file())
        text = PHONE.read_text()
        self.assertIn("still OPEN", text)
        self.assertIn("NS not solved", text)
        self.assertIn("evaluator, not a proof", text)
        self.assertIn("not a falsifier", text)
        self.assertIn("H1", text)
        self.assertIn("Untested", text)
        self.assertNotIn("Stop patching", text)
        self.assertNotIn("Target A is false", text)
        self.assertNotIn("falsifier-of-record", text)
        data = json.loads(JSON.read_text())
        self.assertIs(data["ns_solved"], False)
        abc = [r for r in data["rows"] if r["family"] == "local_abc"]
        self.assertGreaterEqual(len(abc), 6)
        Rs = [r["R_star_signed"] for r in abc]
        self.assertAlmostEqual(Rs[-1], 0.327, places=2)
        self.assertLess(max(Rs), 1.0)

    def test_exact_core_four_jobs(self):
        self.assertTrue(CORE.is_file())
        data = json.loads(CORE.read_text())
        self.assertIs(data["ns_solved"], False)
        self.assertEqual(data.get("lemma_star"), "OPEN")
        self.assertIs(data.get("falsifier"), False)
        self.assertIs(data["H1_tested_on_ABC_lambda"], False)
        self.assertTrue(data["same_field_matches"])
        self.assertTrue(data["dilation_invariant"])
        lams = [r["lambda"] for r in data["rows"]]
        self.assertEqual(lams, [2, 3, 4])
        self.assertLess(data["same_field"]["R_rel"], 1e-9)
        self.assertIn("Not a falsifier", data["verdict"])
        text = PHONE.read_text()
        self.assertIn("λ=2, 3, 4 only", text)
        self.assertIn("never ran λ=8 or 16", text)

    def test_score_refuses_stamp(self):
        self.assertTrue(SCORE.is_file())
        text = SCORE.read_text()
        self.assertIn("Refuse", text)
        self.assertIn("ABC_λ did not kill ★", text)
        self.assertIn("0.327", text)
        self.assertIn("Do not stop patching", text)
        self.assertIn("Q-stack", text)

    def test_live_lambda_2_to_3(self):
        a = probe_hat(*localized_abc(32, width=2.0, k0=2))
        b = probe_hat(*localized_abc(48, width=3.0, k0=3))
        self.assertGreater(a["cs_ratio"], 2.0)
        self.assertGreater(b["cs_ratio"], a["cs_ratio"] * 1.4)
        self.assertGreater(b["R_star_signed"], a["R_star_signed"] * 2.0)
        self.assertLess(a["T_c"], 0.0)
        self.assertEqual(a["R_star"], 0.0)


if __name__ == "__main__":
    unittest.main()
