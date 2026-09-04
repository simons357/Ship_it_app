"""Climbing CONC: slow dies, fast sits; NS does not hand us c."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb import run  # noqa: E402


class TrackBClimbTests(unittest.TestCase):
    def test_slow_blows_fast_sits_law_open(self):
        tmp = Path(tempfile.mkdtemp()) / "climb_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B11_climb_bookkeeping"]["verdict"], "pass")
        self.assertEqual(by["B11a_bounded_j_bounds_X"]["verdict"], "pass")
        self.assertEqual(by["B11b_slow_climb_blows"]["verdict"], "fail")
        self.assertEqual(by["B11c_fast_climb_sits"]["verdict"], "pass")
        self.assertEqual(by["B11d_ns_climb_law_open"]["verdict"], "open")
        self.assertEqual(by["B11e_climb_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertTrue(by["B11b_slow_climb_blows"]["run"]["blew"])
        self.assertFalse(by["B11c_fast_climb_sits"]["run"]["blew"])
        self.assertGreaterEqual(by["B11c_fast_climb_sits"]["run"]["j_final"], 5.0)

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-CLIMB.md").is_file())


if __name__ == "__main__":
    unittest.main()
