"""Tube budget as an a priori: packet budget is not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_tube import run  # noqa: E402


class TrackBTubeTests(unittest.TestCase):
    def test_tube_budget_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "tube_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B24_tube_readable"]["verdict"], "pass")
        self.assertEqual(by["B24a_angular_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B24b_b4c_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B24c_rd_not_bounded"]["verdict"], "fail")
        self.assertEqual(by["B24d_not_revive_hardy_or_phi"]["verdict"], "fail")
        self.assertEqual(by["B24e_geometry_leftover"]["verdict"], "fail")
        self.assertEqual(by["B24f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertGreater(min(by["B24_tube_readable"]["R_ang"]), 1.0)
        self.assertLess(max(by["B24_tube_readable"]["R_D"]), 1.0)
        self.assertIn("B15e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-TUBE.md").is_file())


if __name__ == "__main__":
    unittest.main()
