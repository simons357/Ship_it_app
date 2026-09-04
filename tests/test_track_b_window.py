"""Climb sketch as an a priori: a short window is not the sitting."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_sketch import J_ROOM  # noqa: E402
from track_b_window import run  # noqa: E402


class TrackBWindowTests(unittest.TestCase):
    def test_sketch_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "window_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B32_window_readable"]["verdict"], "pass")
        self.assertEqual(by["B32a_window_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B32b_short_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B32c_growing_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B32d_window_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B32e_finer_leftover"]["verdict"], "open")
        self.assertEqual(by["B32f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLess(by["B32_window_readable"]["jT"], J_ROOM)
        self.assertLess(by["B32_window_readable"]["T"], by["B32_window_readable"]["t_room"])
        self.assertGreater(by["B32_window_readable"]["dX_ode"], 0.0)
        self.assertLess(by["B32_window_readable"]["dX_ns"], 0.0)
        self.assertFalse(by["B32_window_readable"]["sign_match"])
        self.assertGreater(by["B32c_growing_not_ns"]["dj_ode"], 0.0)
        self.assertLess(by["B32c_growing_not_ns"]["dj_ns"], 0.0)
        self.assertIn("B22e", payload["next_da_move"])
        self.assertIn("B21e", payload["next_da_move"])
        self.assertIn("B20e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-WINDOW.md").is_file())


if __name__ == "__main__":
    unittest.main()
