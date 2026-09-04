"""Enstrophy balance as an a priori: a decaying net is not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_balance import CANCEL_MAX, PD_MAX  # noqa: E402
from track_b_net import run  # noqa: E402


class TrackBNetTests(unittest.TestCase):
    def test_balance_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "net_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B27_net_readable"]["verdict"], "pass")
        self.assertEqual(by["B27a_visc_ensemble_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B27b_cancel_not_all_data"]["verdict"], "fail")
        self.assertEqual(by["B27c_decay_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B27d_net_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B27e_coherent_leftover"]["verdict"], "open")
        self.assertEqual(by["B27f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        for r in by["B27_net_readable"]["P_over_D"]:
            self.assertLess(abs(r), PD_MAX)
        for c in by["B27_net_readable"]["cancel"]:
            self.assertLess(c, CANCEL_MAX)
        for xd in by["B27_net_readable"]["Xdot"]:
            self.assertLess(xd, 0.0)
        self.assertIn("B17e", payload["next_da_move"])
        self.assertIn("B16e", payload["next_da_move"])
        self.assertIn("B15e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-NET.md").is_file())


if __name__ == "__main__":
    unittest.main()
