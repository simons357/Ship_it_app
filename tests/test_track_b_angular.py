"""Angular 1/r² vs I_tube: extra piece loses on packets; full D still budgets."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_angular import run  # noqa: E402


class TrackBAngularTests(unittest.TestCase):
    def test_angular_loses_full_D_wins(self):
        tmp = Path(tempfile.mkdtemp()) / "angular_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B5b_tube_vs_viscosity"]["verdict"], "fail")
        self.assertEqual(by["B5c_angular_climbs"]["verdict"], "pass")
        self.assertEqual(by["B5d_killer_not_angular_kill"]["verdict"], "fail")
        self.assertEqual(by["B5e_not_a_phi_cancel"]["verdict"], "fail")
        self.assertEqual(by["B5f_angular_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(by["B5g_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        angs = by["B5b_tube_vs_viscosity"]["R_ang"]
        ds = by["B5b_tube_vs_viscosity"]["R_D"]
        self.assertGreater(min(angs), 1.0)
        self.assertGreater(angs[-1], 2.0 * angs[0])
        self.assertLess(ds[-1], ds[0])
        self.assertTrue(by["B5d_killer_not_angular_kill"]["falls"])
        self.assertIn("B16d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-ANGULAR.md").is_file())


if __name__ == "__main__":
    unittest.main()
