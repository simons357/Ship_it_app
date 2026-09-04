"""Finer box as an a priori: a bigger FFT is not continuation."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_law import C_SAVE  # noqa: E402
from track_b_finer import run  # noqa: E402
from track_b_longer import ABOVE_MAX, T_ROOM  # noqa: E402


class TrackBFinerTests(unittest.TestCase):
    def test_finer_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "finer_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B33_finer_readable"]["verdict"], "pass")
        self.assertEqual(by["B33a_finer_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B33b_fft_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B33c_n64_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B33d_finer_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B33e_dns_finer_leftover"]["verdict"], "fail")
        self.assertEqual(by["B33f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(payload["meta"]["spawned_n64"])
        self.assertGreater(by["B33_finer_readable"]["T"], T_ROOM)
        self.assertLess(by["B33_finer_readable"]["c_inc_max"], C_SAVE)
        self.assertLess(by["B33_finer_readable"]["window_T"], by["B33_finer_readable"]["t_room"])
        for name in ("packet", "blob"):
            self.assertLess(by["B33_finer_readable"]["aboveT"][name], ABOVE_MAX)
        self.assertIn("Regularity stays open", payload["next_da_move"])
        self.assertIn("B34e", payload["next_da_move"])
        self.assertIn("B23e", payload["next_da_move"])
        self.assertIn("B22e", payload["next_da_move"])
        self.assertIn("B21e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-FINER.md").is_file())


if __name__ == "__main__":
    unittest.main()
