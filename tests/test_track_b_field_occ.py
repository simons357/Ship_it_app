"""Field occupation: clock on a path; CONC the whole interval; cubic not live in time."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_field_occ import CONC_FRAC_MIN, PD_MAX, run  # noqa: E402


class TrackBFieldOccTests(unittest.TestCase):
    def test_clock_stays_conc_cubic_not_live(self):
        tmp = Path(tempfile.mkdtemp()) / "field_occ_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B18_field_clock"]["verdict"], "pass")
        self.assertEqual(by["B18a_paths_stay_conc"]["verdict"], "pass")
        self.assertEqual(by["B18b_clock_did_not_save"]["verdict"], "fail")
        self.assertEqual(by["B18c_conc_not_short"]["verdict"], "fail")
        self.assertEqual(by["B18d_cubic_not_live_time"]["verdict"], "fail")
        self.assertEqual(by["B18e_field_occ_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(by["B18f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        for name in ("packet", "blob"):
            self.assertGreaterEqual(by["B18a_paths_stay_conc"]["tau_frac"][name], CONC_FRAC_MIN)
            self.assertEqual(by["B18b_clock_did_not_save"]["switches"][name], 0)
            self.assertEqual(by["B18d_cubic_not_live_time"]["live_samples"][name], 0)
            self.assertTrue(by["B18b_clock_did_not_save"]["X_fell"][name])
            for p in by["B18d_cubic_not_live_time"]["P_over_D"][name]:
                self.assertLess(abs(p), PD_MAX)
        self.assertIn("B11d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-FIELD-OCC.md").is_file())


if __name__ == "__main__":
    unittest.main()
