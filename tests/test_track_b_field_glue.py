"""Field glue: j*=2 model grows; NS packet falls; α_c is not the cubic."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_field_glue import ALPHA_RATIO_MAX, run  # noqa: E402


class TrackBFieldGlueTests(unittest.TestCase):
    def test_model_grows_packet_falls(self):
        tmp = Path(tempfile.mkdtemp()) / "field_glue_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B19_field_rates"]["verdict"], "pass")
        self.assertEqual(by["B19a_sign_mismatch"]["verdict"], "fail")
        self.assertEqual(by["B19b_not_the_blowup"]["verdict"], "fail")
        self.assertEqual(by["B19c_alpha_not_the_cubic"]["verdict"], "fail")
        self.assertEqual(by["B19d_gamma_not_visc"]["verdict"], "fail")
        self.assertEqual(by["B19e_field_glue_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(by["B19f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(by["B19a_sign_mismatch"]["sign_match"])
        self.assertGreater(by["B19a_sign_mismatch"]["Xdot_model"], 0.0)
        self.assertLess(by["B19a_sign_mismatch"]["Xdot_ns"], 0.0)
        self.assertGreater(by["B19b_not_the_blowup"]["dX_model"], 0.0)
        self.assertLess(by["B19b_not_the_blowup"]["dX_ns"], 0.0)
        for name in ("packet", "blob"):
            self.assertLess(by["B19c_alpha_not_the_cubic"]["alpha_ratio"][name], ALPHA_RATIO_MAX)
        self.assertGreater(by["B19d_gamma_not_visc"]["visc_ratio"], 2.0)
        self.assertIn("B11e", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-FIELD-GLUE.md").is_file())


if __name__ == "__main__":
    unittest.main()
