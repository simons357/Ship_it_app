"""Geometry on CONC packets: identity holds; depletion is not all-data."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_geometry import run  # noqa: E402


class TrackBGeometryTests(unittest.TestCase):
    def test_identity_not_depletion_cf_conditional(self):
        tmp = Path(tempfile.mkdtemp()) / "geometry_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B14_strain_identity"]["verdict"], "pass")
        self.assertEqual(by["B14a_conc_not_depleted"]["verdict"], "fail")
        self.assertEqual(by["B14b_ring_not_alignment"]["verdict"], "fail")
        self.assertEqual(by["B14c_cf_conditional"]["verdict"], "pass")
        self.assertEqual(by["B14d_geometry_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(by["B14e_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        for rel in by["B14_strain_identity"]["ident_rels"]:
            self.assertLess(rel, 1e-8)
        self.assertGreater(by["B14a_conc_not_depleted"]["median_cos3"], 0.25)
        self.assertLess(
            by["B14c_cf_conditional"]["mean_ratio_low"],
            by["B14c_cf_conditional"]["mean_ratio_high"],
        )
        self.assertIn("B5b", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-GEOMETRY.md").is_file())


if __name__ == "__main__":
    unittest.main()
