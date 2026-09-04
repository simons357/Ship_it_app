"""Longer n=32 path: T past the B11c room time; still no c=8."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_law import C_SAVE  # noqa: E402
from track_b_longer import ABOVE_MAX, T_ROOM, run  # noqa: E402


class TrackBLongerTests(unittest.TestCase):
    def test_longer_past_room_not_saving(self):
        tmp = Path(tempfile.mkdtemp()) / "longer_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B22_longer_readable"]["verdict"], "pass")
        self.assertEqual(by["B22a_longer_not_saving"]["verdict"], "fail")
        self.assertEqual(by["B22b_longer_not_ladder"]["verdict"], "fail")
        self.assertEqual(by["B22c_longer_no_high_fill"]["verdict"], "fail")
        self.assertEqual(by["B22d_longer_clock_did_not_save"]["verdict"], "fail")
        self.assertEqual(by["B22e_finer_open"]["verdict"], "open")
        self.assertEqual(by["B22f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertGreater(by["B22_longer_readable"]["T"], T_ROOM)
        self.assertLess(by["B22a_longer_not_saving"]["c_inc_max"], C_SAVE)
        for name in ("packet", "blob"):
            self.assertLess(by["B22a_longer_not_saving"]["c_mean"][name], 0.0)
            self.assertLess(
                by["B22b_longer_not_ladder"]["jbarT"][name],
                by["B22b_longer_not_ladder"]["jbar0"][name],
            )
            self.assertLess(by["B22c_longer_no_high_fill"]["aboveT"][name], ABOVE_MAX)
            self.assertEqual(by["B22d_longer_clock_did_not_save"]["switches"][name], 0)
            self.assertTrue(by["B22d_longer_clock_did_not_save"]["X_fell"][name])
        self.assertLess(by["B22a_longer_not_saving"]["c_mean"]["euler"], C_SAVE)
        self.assertIn("B13f", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-LONGER.md").is_file())


if __name__ == "__main__":
    unittest.main()
