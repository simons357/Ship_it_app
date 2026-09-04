"""Coherent CONC: signed-strain blob nets; working-box cubic is not live."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_coherent import (  # noqa: E402
    CANCEL_MIN,
    IDENT_MAX,
    PD_MAX,
    SIGMA_MIN,
    TUBE_CANCEL_MAX,
    run,
)


class TrackBCoherentTests(unittest.TestCase):
    def test_blob_nets_tube_cancels_visc_owns(self):
        tmp = Path(tempfile.mkdtemp()) / "coherent_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B17_coherent_field"]["verdict"], "pass")
        self.assertEqual(by["B17a_net_is_plus"]["verdict"], "pass")
        self.assertEqual(by["B17b_cubic_not_live"]["verdict"], "fail")
        self.assertEqual(by["B17c_tube_still_cancels"]["verdict"], "fail")
        self.assertEqual(by["B17d_blob_is_not_bkm"]["verdict"], "fail")
        self.assertEqual(by["B17e_coherent_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(by["B17f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLess(by["B17_coherent_field"]["rel"], IDENT_MAX)
        self.assertGreaterEqual(by["B17_coherent_field"]["sigma"], SIGMA_MIN)
        self.assertGreaterEqual(by["B17a_net_is_plus"]["cancel"], CANCEL_MIN)
        self.assertLess(abs(by["B17b_cubic_not_live"]["P_over_D"]), PD_MAX)
        self.assertLess(by["B17b_cubic_not_live"]["Xdot"], 0.0)
        self.assertLess(by["B17c_tube_still_cancels"]["cancel"], TUBE_CANCEL_MAX)
        self.assertIn("B9d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-COHERENT.md").is_file())


if __name__ == "__main__":
    unittest.main()
