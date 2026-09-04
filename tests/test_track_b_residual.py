"""Residual tool: holes of R are readable; not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_residual import run  # noqa: E402


class TrackBResidualTests(unittest.TestCase):
    def test_holes_readable_not_a_bound(self):
        tmp = Path(tempfile.mkdtemp()) / "residual_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B37_residual_readable"]["verdict"], "pass")
        self.assertEqual(by["B37a_residual_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B37b_residual_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B37c_residual_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B37d_residual_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B37e_residual_not_regularity"]["verdict"], "fail")
        self.assertEqual(by["B37f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(by["B38_miller_readable"]["verdict"], "pass")
        self.assertEqual(by["B38a_miller_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B38b_miller_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B38c_miller_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B38d_miller_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B38e_miller_not_regularity"]["verdict"], "fail")
        self.assertEqual(by["B38f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(by["B39_empty_rename"]["verdict"], "pass")
        self.assertEqual(by["B39a_empty_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B39b_empty_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B39c_empty_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B39d_empty_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B39e_empty_not_regularity"]["verdict"], "fail")
        self.assertEqual(by["B39f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(by["B40_blanks_readable"]["verdict"], "pass")
        self.assertEqual(by["B40a_blanks_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B40b_blanks_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B40c_blanks_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B40d_blanks_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B40e_blanks_not_regularity"]["verdict"], "fail")
        self.assertEqual(by["B40f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(payload["meta"]["spawned_n64"])
        self.assertEqual(by["B37_residual_readable"]["n"], 32)
        self.assertGreater(by["B37_residual_readable"]["hole1_mean"], 0.5)
        self.assertLess(by["B37_residual_readable"]["pd_max"], 0.05)
        self.assertLess(by["B37_residual_readable"]["xdot_max"], 0.0)
        self.assertGreater(by["B38_miller_readable"]["gap_mean"], 0.10)
        self.assertLess(by["B38_miller_readable"]["e2_mean"], by["B38_miller_readable"]["hole2_mean"])
        self.assertIn("holes", payload["next_da_move"])
        self.assertIn("Miller", payload["next_da_move"])
        self.assertIn("Sit down", payload["next_da_move"])
        self.assertLess(by["B39_empty_rename"]["ident_max"], 1e-10)
        self.assertLess(by["B39_empty_rename"]["gap_mean"], 0.05)
        self.assertTrue(by["B40_blanks_readable"]["a1_off"])
        self.assertTrue(by["B40_blanks_readable"]["a2_live"])
        self.assertGreater(by["B40_blanks_readable"]["l2p_inf_mean"], 0.0)
        self.assertIn("A1", payload["next_da_move"])
        self.assertIn("Regularity stays open", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-RESIDUAL.md").is_file())


if __name__ == "__main__":
    unittest.main()
