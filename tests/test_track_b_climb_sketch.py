"""Climb sketch: c=8 has not reached the viscous room on the NS window."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_law import C_SAVE  # noqa: E402
from track_b_climb_sketch import J_ROOM, run  # noqa: E402


class TrackBClimbSketchTests(unittest.TestCase):
    def test_sketch_not_the_ns_window(self):
        tmp = Path(tempfile.mkdtemp()) / "climb_sketch_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B21_window_rates"]["verdict"], "pass")
        self.assertEqual(by["B21a_not_the_room"]["verdict"], "fail")
        self.assertEqual(by["B21b_not_the_sitting"]["verdict"], "fail")
        self.assertEqual(by["B21c_delta_j_not_prescribed"]["verdict"], "fail")
        self.assertEqual(by["B21d_sketch_did_not_save"]["verdict"], "fail")
        self.assertEqual(by["B21e_sketch_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(by["B21f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLess(by["B21a_not_the_room"]["jT"], J_ROOM)
        self.assertLess(by["B21a_not_the_room"]["T"], by["B21a_not_the_room"]["t_room"])
        self.assertGreater(by["B21b_not_the_sitting"]["dX_ode"], 0.0)
        self.assertLess(by["B21b_not_the_sitting"]["dX_ns"], 0.0)
        self.assertFalse(by["B21b_not_the_sitting"]["sign_match"])
        self.assertGreater(by["B21c_delta_j_not_prescribed"]["dj_ode"], 0.0)
        self.assertLess(by["B21c_delta_j_not_prescribed"]["dj_ns"], 0.0)
        self.assertLess(by["B21c_delta_j_not_prescribed"]["c_mean_ns"], C_SAVE)
        self.assertGreater(by["B21d_sketch_did_not_save"]["Xdot0"], 0.0)
        self.assertIn("B13f", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-CLIMB-SKETCH.md").is_file())


if __name__ == "__main__":
    unittest.main()
