"""Stretching budget as an a priori: a share is not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_payers import HIGH, WMEAN_GAP, run  # noqa: E402


class TrackBPayersTests(unittest.TestCase):
    def test_budget_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "payers_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B26_payers_readable"]["verdict"], "pass")
        self.assertEqual(by["B26a_share_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B26b_emptying_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B26c_share_not_a_class"]["verdict"], "fail")
        self.assertEqual(by["B26d_aligned_budget_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B26e_enstrophy_leftover"]["verdict"], "open")
        self.assertEqual(by["B26f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        for g in by["B26_payers_readable"]["gaps"]:
            self.assertGreater(g, WMEAN_GAP)
        for f in by["B26_payers_readable"]["frac_pos_hi"]:
            self.assertGreater(f, 0.5)
        for f in by["B26b_emptying_not_continuation"]["visc_frac_hi_end"]:
            self.assertGreater(f, 0.5)
        for m in by["B26b_emptying_not_continuation"]["median_end"]:
            self.assertGreater(m, 0.25)
        self.assertEqual(HIGH, 0.8)
        self.assertIn("B16e", payload["next_da_move"])
        self.assertIn("B15e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-PAYERS.md").is_file())


if __name__ == "__main__":
    unittest.main()
