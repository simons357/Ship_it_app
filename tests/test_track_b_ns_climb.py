"""NS climb law: blob and B18 paths do not produce c=8; offset is not a climb."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_law import C_SAVE  # noqa: E402
from track_b_ns_climb import OFFSET_MIN, run  # noqa: E402


class TrackBNsClimbTests(unittest.TestCase):
    def test_field_does_not_force_saving_c(self):
        tmp = Path(tempfile.mkdtemp()) / "ns_climb_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B20_field_c"]["verdict"], "pass")
        self.assertEqual(by["B20a_blob_t0_not_saving"]["verdict"], "fail")
        self.assertEqual(by["B20b_paths_not_saving"]["verdict"], "fail")
        self.assertEqual(by["B20c_blob_visc_not_ladder"]["verdict"], "fail")
        self.assertEqual(by["B20d_offset_not_climb"]["verdict"], "fail")
        self.assertEqual(by["B20e_ns_climb_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(by["B20f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLess(by["B20a_blob_t0_not_saving"]["t0_visc_c"], 0.0)
        self.assertLess(by["B20a_blob_t0_not_saving"]["t0_visc_c"], C_SAVE)
        self.assertLess(by["B20a_blob_t0_not_saving"]["t0_euler_c"], C_SAVE)
        for name in ("packet", "blob"):
            self.assertLess(by["B20b_paths_not_saving"]["c_mean_visc"][name], 0.0)
            self.assertLess(by["B20b_paths_not_saving"]["c_mean_visc"][name], C_SAVE)
            self.assertLess(by["B20b_paths_not_saving"]["c_mean_euler"][name], C_SAVE)
        self.assertLess(
            by["B20c_blob_visc_not_ladder"]["jbarT"],
            by["B20c_blob_visc_not_ladder"]["jbar0"],
        )
        self.assertGreaterEqual(by["B20d_offset_not_climb"]["offset"], OFFSET_MIN)
        self.assertLess(by["B20d_offset_not_climb"]["c_mean_visc"], 0.0)
        self.assertIn("B13f", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-NS-CLIMB.md").is_file())


if __name__ == "__main__":
    unittest.main()
