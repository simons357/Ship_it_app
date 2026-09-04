"""Enstrophy balance: fluids look at the net, not the share."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_balance import CANCEL_MAX, IDENT_MAX, PD_MAX, PPD_MAX, run  # noqa: E402


class TrackBBalanceTests(unittest.TestCase):
    def test_identity_cancel_not_bkm(self):
        tmp = Path(tempfile.mkdtemp()) / "balance_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B16_enstrophy_identity"]["verdict"], "pass")
        self.assertEqual(by["B16a_visc_owns_net"]["verdict"], "pass")
        self.assertEqual(by["B16b_plus_not_net_cubic"]["verdict"], "fail")
        self.assertEqual(by["B16c_l2_is_not_bkm"]["verdict"], "fail")
        self.assertEqual(by["B16d_not_all_conc"]["verdict"], "fail")
        self.assertEqual(by["B16e_balance_not_X_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B16f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLess(by["B16_enstrophy_identity"]["rel"], IDENT_MAX)
        for r in by["B16a_visc_owns_net"]["P_over_D"]:
            self.assertLess(abs(r), PD_MAX)
        for c in by["B16b_plus_not_net_cubic"]["cancel"]:
            self.assertLess(c, CANCEL_MAX)
        for p in by["B16b_plus_not_net_cubic"]["Pplus_over_D"]:
            self.assertLess(p, PPD_MAX)
        self.assertIn("B17e", payload["next_da_move"])
        self.assertIn("B16e", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-BALANCE.md").is_file())


if __name__ == "__main__":
    unittest.main()
