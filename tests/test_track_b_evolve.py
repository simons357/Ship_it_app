"""Short CONC evolution: field runs; no saving climb on n=32."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_evolve import C_SAVE, run  # noqa: E402


class TrackBEvolveTests(unittest.TestCase):
    def test_short_run_no_saving_climb(self):
        tmp = Path(tempfile.mkdtemp()) / "evolve_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B13_short_run"]["verdict"], "pass")
        self.assertEqual(by["B13a_no_saving_climb"]["verdict"], "fail")
        self.assertEqual(by["B13b_no_high_fill"]["verdict"], "fail")
        self.assertEqual(by["B13c_stays_conc"]["verdict"], "pass")
        self.assertEqual(by["B13d_visc_still_down"]["verdict"], "fail")
        self.assertEqual(by["B13e_finer_longer_open"]["verdict"], "open")
        self.assertEqual(by["B13f_evolve_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(payload["meta"]["stopped_at_t0"])
        self.assertLess(by["B13a_no_saving_climb"]["visc_c"], C_SAVE)
        self.assertLess(by["B13a_no_saving_climb"]["euler_c"], C_SAVE)
        self.assertGreaterEqual(by["B13c_stays_conc"]["sigma_end"], 0.5)
        self.assertGreater(
            by["B13d_visc_still_down"]["jbar0"],
            by["B13d_visc_still_down"]["jbarT"],
        )

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-EVOLVE.md").is_file())


if __name__ == "__main__":
    unittest.main()
