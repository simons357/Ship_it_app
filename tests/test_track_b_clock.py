"""Field occupation as an a priori: a clock that stays CONC is not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_clock import run  # noqa: E402
from track_b_field_occ import CONC_FRAC_MIN  # noqa: E402


class TrackBClockTests(unittest.TestCase):
    def test_occupation_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "clock_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B29_clock_readable"]["verdict"], "pass")
        self.assertEqual(by["B29a_stay_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B29b_full_occ_not_short"]["verdict"], "fail")
        self.assertEqual(by["B29c_occ_not_live_cubic"]["verdict"], "fail")
        self.assertEqual(by["B29d_clock_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B29e_glue_leftover"]["verdict"], "open")
        self.assertEqual(by["B29f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        for name in ("packet", "blob"):
            self.assertGreaterEqual(by["B29_clock_readable"]["tau_frac"][name], CONC_FRAC_MIN)
            self.assertEqual(by["B29_clock_readable"]["switches"][name], 0)
            self.assertTrue(by["B29_clock_readable"]["X_fell"][name])
            self.assertEqual(by["B29c_occ_not_live_cubic"]["live_samples"][name], 0)
        self.assertIn("B19e", payload["next_da_move"])
        self.assertIn("B18e", payload["next_da_move"])
        self.assertIn("B17e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-CLOCK.md").is_file())


if __name__ == "__main__":
    unittest.main()
