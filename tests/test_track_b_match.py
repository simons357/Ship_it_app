"""Field glue as an a priori: a wrong-sign sketch is not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_field_glue import ALPHA_RATIO_MAX  # noqa: E402
from track_b_match import run  # noqa: E402


class TrackBMatchTests(unittest.TestCase):
    def test_glue_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "match_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B30_match_readable"]["verdict"], "pass")
        self.assertEqual(by["B30a_match_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B30b_shrink_alpha_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B30c_wrong_sign_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B30d_match_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B30e_climb_leftover"]["verdict"], "fail")
        self.assertEqual(by["B30f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(by["B30_match_readable"]["sign_match"])
        self.assertGreater(by["B30_match_readable"]["Xdot_model"], 0.0)
        self.assertLess(by["B30_match_readable"]["Xdot_ns"], 0.0)
        self.assertGreater(by["B30_match_readable"]["dX_model"], 0.0)
        self.assertLess(by["B30_match_readable"]["dX_ns"], 0.0)
        for name in ("packet", "blob"):
            self.assertLess(by["B30b_shrink_alpha_not_continuation"]["alpha_ratio"][name], ALPHA_RATIO_MAX)
        self.assertIn("B21e", payload["next_da_move"])
        self.assertIn("B20e", payload["next_da_move"])
        self.assertIn("B19e", payload["next_da_move"])
        self.assertIn("B18e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-MATCH.md").is_file())


if __name__ == "__main__":
    unittest.main()
