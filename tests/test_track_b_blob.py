"""Signed-strain blob as an a priori: one-sided is not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_blob import run  # noqa: E402
from track_b_coherent import CANCEL_MIN, PD_MAX, SIGMA_MIN  # noqa: E402


class TrackBBlobTests(unittest.TestCase):
    def test_blob_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "blob_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B28_blob_readable"]["verdict"], "pass")
        self.assertEqual(by["B28a_onesided_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B28b_sign_not_a_class"]["verdict"], "fail")
        self.assertEqual(by["B28c_peaked_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B28d_nu_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B28e_occupation_leftover"]["verdict"], "fail")
        self.assertEqual(by["B28f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertGreaterEqual(by["B28_blob_readable"]["sigma"], SIGMA_MIN)
        self.assertGreaterEqual(by["B28_blob_readable"]["cancel"], CANCEL_MIN)
        self.assertLess(abs(by["B28_blob_readable"]["P_over_D"]), PD_MAX)
        self.assertLess(by["B28_blob_readable"]["Xdot"], 0.0)
        self.assertIn("B21e", payload["next_da_move"])
        self.assertIn("B20e", payload["next_da_move"])
        self.assertIn("B19e", payload["next_da_move"])
        self.assertIn("B18e", payload["next_da_move"])
        self.assertIn("B17e", payload["next_da_move"])
        self.assertIn("B16e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-BLOB.md").is_file())


if __name__ == "__main__":
    unittest.main()
