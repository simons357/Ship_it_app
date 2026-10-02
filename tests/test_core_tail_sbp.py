"""Core / tail SBP identities. Not DA-NS-2. NS is not solved."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.core_tail_sbp import (  # noqa: E402
    R_linear_bound_sample,
    phi_e,
    phi_e_poly,
    phi_over_Y_split,
    random_energy_conserving_sbp,
    report,
    sympy_R_core,
    sympy_modal_sbp,
    sympy_phi_factorization,
    sympy_waleffe_m_flux,
    tail_holds_Ds,
)


class PhiAndRTests(unittest.TestCase):
    def test_phi_factorization_and_jet(self):
        s = sympy_phi_factorization()
        self.assertTrue(s["factor_equals_expanded"])
        self.assertEqual(s["phi_at_shell"], "0")
        self.assertEqual(s["dphi_at_shell"], "0")
        self.assertEqual(s["phi_at_zero"], "kappa**4")
        for kappa in (1.0, 2.5, 7.0):
            self.assertAlmostEqual(phi_e(0.0, kappa), kappa**4, places=12)
            self.assertAlmostEqual(phi_e(kappa, kappa), 0.0, places=12)
            self.assertAlmostEqual(phi_e(kappa, kappa), phi_e_poly(kappa, kappa), places=12)
            self.assertAlmostEqual(phi_e(4.2, kappa), phi_e_poly(4.2, kappa), places=10)
            self.assertGreaterEqual(phi_e(0.3, kappa), 0.0)
            self.assertGreaterEqual(phi_e(11.0, kappa), 0.0)

    def test_R_gradient_at_core(self):
        s = sympy_R_core()
        self.assertTrue(s["grad_is_5k2_5k2_0"])
        self.assertTrue(s["dR_dLambda_is_minus_2k"])
        self.assertTrue(s["frozen_shift_is_minus_2k_dLambda"])
        self.assertEqual(s["R_on_shell"], "2*kappa**3")

    def test_live_vs_frozen_are_labeled(self):
        r = report()
        self.assertTrue(r["conventions"]["frozen_epoch_only"])
        self.assertTrue(r["conventions"]["live_kappa_does_not_telescope"])
        self.assertTrue(r["conventions"]["frozen_core_picks_up_2k_dLambda"])
        self.assertTrue(r["conventions"]["do_not_mix"])


class SBPTests(unittest.TestCase):
    def test_modal_weight_is_minus_kappa4(self):
        s = sympy_modal_sbp()
        self.assertTrue(s["is_minus_kappa4"])

    def test_random_transfers_satisfy_SBP(self):
        for seed in range(8):
            row = random_energy_conserving_sbp(n=15, seed=seed)
            self.assertLess(row["abs_err"], 1e-10)

    def test_waleffe_m_flux(self):
        s = sympy_waleffe_m_flux()
        self.assertEqual(s["homo_flux"], "0")
        self.assertTrue(s["het_is_4g_o_i_minus_j"])
        self.assertTrue(s["Qa_is_half_Hdot_half_flux"])

    def test_linear_R_bound_and_frozen_extra(self):
        row = R_linear_bound_sample()
        self.assertTrue(row["within_linear_plus_quad"])
        self.assertGreater(row["abs_dR"], 0.0)
        # Linear piece is 5κ³ Lr; the excess is the O((Lr)²) remainder.
        self.assertLess(row["abs_dR"] - row["five_k3_Lr"], 0.3)
        self.assertAlmostEqual(row["frozen_core_dR"], row["two_k_dLambda"], places=10)

    def test_tail_can_hold_Ds(self):
        t = tail_holds_Ds()
        self.assertLess(t["tail_X_share"], 0.05)
        self.assertLess(t["tail_Y_share"], 0.15)
        self.assertGreater(t["tail_Ds_share"], 0.8)
        self.assertGreater(t["core_X_share"], 0.9)

    def test_Phi_Y_splitter_and_no_TG_claim(self):
        split = phi_over_Y_split(
            [0.5, 3.0, 8.0],
            [0.4, 0.5, 0.02],
            kappa=3.0,
            core_halfwidth=0.4,
        )
        self.assertGreater(split["Phi_over_Y"], 0.0)
        self.assertAlmostEqual(split["phi_at_zero"], split["kappa4"], places=12)
        shares = (
            split["low_share_of_Phi"]
            + split["core_share_of_Phi"]
            + split["high_share_of_Phi"]
        )
        self.assertAlmostEqual(shares, 1.0, places=12)
        self.assertTrue(report()["locks"]["no_TG_in_this_checkout"])
        self.assertTrue(report()["locks"]["moves_tail_does_not_remove_it"])


if __name__ == "__main__":
    unittest.main()
