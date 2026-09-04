"""Stretching budget: aligned cap pays; a short run does not empty it."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_stretch import HIGH, WMEAN_GAP, run  # noqa: E402


class TrackBStretchTests(unittest.TestCase):
    def test_budget_aligned_run_does_not_empty(self):
        tmp = Path(tempfile.mkdtemp()) / "stretch_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B15_stretch_budget"]["verdict"], "pass")
        self.assertEqual(by["B15a_cf_weights_budget"]["verdict"], "pass")
        self.assertEqual(by["B15b_majority_from_aligned"]["verdict"], "pass")
        self.assertEqual(by["B15c_run_not_depleted"]["verdict"], "fail")
        self.assertEqual(by["B15d_run_keeps_aligned_budget"]["verdict"], "fail")
        self.assertEqual(by["B15e_budget_not_X_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B15f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        for g in by["B15a_cf_weights_budget"]["gaps"]:
            self.assertGreater(g, WMEAN_GAP)
        for f in by["B15b_majority_from_aligned"]["frac_pos_hi"]:
            self.assertGreater(f, 0.5)
        for m in by["B15c_run_not_depleted"]["median_end"]:
            self.assertGreater(m, 0.25)
        for f in by["B15d_run_keeps_aligned_budget"]["visc_frac_hi_end"]:
            self.assertGreater(f, 0.5)
        self.assertEqual(HIGH, 0.8)
        self.assertIn("B16e", payload["next_da_move"])
        self.assertIn("B15e", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-STRETCH.md").is_file())


if __name__ == "__main__":
    unittest.main()
