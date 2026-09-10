"""Localized ABC climbs R★. CS remainder is false. Not a plate."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.cs_remainder_bump import localized_abc, probe_hat  # noqa: E402

JSON = ROOT / "results" / "cs_remainder_bump" / "cs_remainder.json"
PHONE = ROOT / "docs" / "CS-REMAINDER.md"


class CsRemainderTests(unittest.TestCase):
    def test_phone_and_json(self):
        self.assertTrue(PHONE.is_file())
        text = PHONE.read_text()
        self.assertIn("Target A is false", text)
        self.assertIn("NS not solved", text)
        self.assertIn("ABC", text)
        data = json.loads(JSON.read_text())
        self.assertIs(data["ns_solved"], False)
        self.assertTrue(data["climbs_cs"])
        self.assertTrue(data["climbs_R_star"])
        abc = [r for r in data["rows"] if r["family"] == "local_abc"]
        self.assertGreaterEqual(len(abc), 6)
        Rs = [r["R_star_signed"] for r in abc]
        self.assertLess(Rs[0], 0.01)
        self.assertGreater(Rs[-1], 0.3)
        self.assertGreater(Rs[-1] / Rs[0], 40.0)

    def test_live_lambda_2_to_3(self):
        a = probe_hat(*localized_abc(32, width=2.0, k0=2))
        b = probe_hat(*localized_abc(48, width=3.0, k0=3))
        self.assertGreater(a["cs_ratio"], 2.0)
        self.assertGreater(b["cs_ratio"], a["cs_ratio"] * 1.4)
        self.assertGreater(b["R_star_signed"], a["R_star_signed"] * 2.0)
        self.assertLess(a["T_c"], 0.0)


if __name__ == "__main__":
    unittest.main()
