"""Alignment as an a priori: geometry is a number, not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_align import run  # noqa: E402


class TrackBAlignTests(unittest.TestCase):
    def test_alignment_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "align_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B25_align_readable"]["verdict"], "pass")
        self.assertEqual(by["B25a_depletion_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B25b_frame_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B25c_median_not_a_class"]["verdict"], "fail")
        self.assertEqual(by["B25d_cf_not_bkm"]["verdict"], "fail")
        self.assertEqual(by["B25e_budget_leftover"]["verdict"], "open")
        self.assertEqual(by["B25f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertGreater(by["B25_align_readable"]["median_cos3"], 0.25)
        self.assertLess(
            by["B25_align_readable"]["mean_ratio_low"],
            by["B25_align_readable"]["mean_ratio_high"],
        )
        self.assertIn("B15e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-ALIGN.md").is_file())


if __name__ == "__main__":
    unittest.main()
