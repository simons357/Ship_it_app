"""NS climb as an a priori: a field that did not make c=8 is not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_law import C_SAVE  # noqa: E402
from track_b_ns_climb import OFFSET_MIN  # noqa: E402
from track_b_saving import run  # noqa: E402


class TrackBSavingTests(unittest.TestCase):
    def test_climb_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "saving_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B31_saving_readable"]["verdict"], "pass")
        self.assertEqual(by["B31a_field_c_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B31b_offset_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B31c_ladder_not_a_class"]["verdict"], "fail")
        self.assertEqual(by["B31d_c_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B31e_sketch_leftover"]["verdict"], "open")
        self.assertEqual(by["B31f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLess(by["B31_saving_readable"]["t0_visc_c"], C_SAVE)
        self.assertLess(by["B31_saving_readable"]["t0_euler_c"], C_SAVE)
        for name in ("packet", "blob"):
            self.assertLess(by["B31_saving_readable"]["c_mean_visc"][name], C_SAVE)
            self.assertLess(by["B31_saving_readable"]["c_mean_euler"][name], C_SAVE)
        self.assertGreaterEqual(by["B31b_offset_not_continuation"]["offset"], OFFSET_MIN)
        self.assertLess(by["B31b_offset_not_continuation"]["c_mean_visc"], 0.0)
        self.assertLess(by["B31c_ladder_not_a_class"]["jbarT"], by["B31c_ladder_not_a_class"]["jbar0"])
        self.assertIn("B21e", payload["next_da_move"])
        self.assertIn("B20e", payload["next_da_move"])
        self.assertIn("B19e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-SAVING.md").is_file())


if __name__ == "__main__":
    unittest.main()
