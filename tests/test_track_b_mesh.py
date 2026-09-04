"""Finer DNS as an a priori: a finer mesh is not continuation."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_climb_law import C_SAVE  # noqa: E402
from track_b_longer import T_ROOM  # noqa: E402
from track_b_mesh import run  # noqa: E402


class TrackBMeshTests(unittest.TestCase):
    def test_finer_dns_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "mesh_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B34_mesh_readable"]["verdict"], "pass")
        self.assertEqual(by["B34a_mesh_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B34b_mesh_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B34c_finer_dns_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B34d_mesh_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B34e_regularity_leftover"]["verdict"], "fail")
        self.assertEqual(by["B34f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(payload["meta"]["spawned_n64"])
        self.assertGreater(by["B34_mesh_readable"]["T_long"], T_ROOM)
        self.assertLess(by["B34_mesh_readable"]["c_inc_max"], C_SAVE)
        self.assertIn("B23e", payload["next_da_move"])
        self.assertIn("B22e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])
        self.assertIn("B34e", payload["next_da_move"])
        self.assertIn("Regularity stays open", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-MESH.md").is_file())


if __name__ == "__main__":
    unittest.main()
