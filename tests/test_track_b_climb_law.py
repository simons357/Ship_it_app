"""Climb law from the field: t=0 packets do not produce c=8."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_law import C_SAVE, run  # noqa: E402


class TrackBClimbLawTests(unittest.TestCase):
    def test_t0_not_saving_visc_down(self):
        tmp = Path(tempfile.mkdtemp()) / "climb_law_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B12_barycenter"]["verdict"], "pass")
        self.assertEqual(by["B12a_c_from_rhs"]["verdict"], "pass")
        self.assertEqual(by["B12b_t0_not_saving"]["verdict"], "fail")
        self.assertEqual(by["B12c_visc_pulls_down"]["verdict"], "fail")
        self.assertEqual(by["B12d_evolved_cascade_open"]["verdict"], "open")
        self.assertEqual(by["B12e_law_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLess(by["B12b_t0_not_saving"]["viscous_max"], C_SAVE)
        self.assertLess(by["B12b_t0_not_saving"]["euler_max"], C_SAVE)
        self.assertTrue(all(c < 0.0 for c in by["B12c_visc_pulls_down"]["viscous"]))

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-CLIMB-LAW.md").is_file())


if __name__ == "__main__":
    unittest.main()
