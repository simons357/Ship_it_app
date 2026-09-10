#!/usr/bin/env python3
"""Tests: Attack 9B K_{α,β} stub — ε-cancel narrative, same-shell D_s=0."""

from __future__ import annotations

import unittest

from domain_architect.kab_quantity import (
    ATTACK_9A_STATUS,
    KAB_FORMULA,
    kab_inventory,
    kab_rayleigh,
    limiting_closing_quotient,
    refuse_ap_packet_closed_kill_lane,
    same_shell_D_s_zero,
)
from domain_architect.lemma_star import (
    FIVE_LANE_STATUS,
    refuse_proved_lemma_star,
)
from domain_architect.rstar_quantities import refuse_kill_lane_closed


class TestKabRayleigh(unittest.TestCase):
    def test_rayleigh_formula(self):
        # β ‖ΠB‖² / (α² ‖w‖⁴) = 4*9/(1²*2²) = 9
        out = kab_rayleigh(1.0, 4.0, pi_beta_B_ww_norm_sq=9.0, w_norm_sq=2.0)
        self.assertTrue(out["ok"])
        self.assertFalse(out["is_supremum"])
        self.assertAlmostEqual(out["rayleigh"], 9.0)

    def test_rejects_zero_norm(self):
        with self.assertRaises(ValueError):
            kab_rayleigh(1.0, 2.0, 1.0, 0.0)


class TestSameShellDsZero(unittest.TestCase):
    def test_pure_shell_wavevectors(self):
        energies = {
            (1, 0, 0): 1.0,
            (-1, 0, 0): 1.0,
            (0, 1, 0): 0.5,
            (0, -1, 0): 0.5,
        }
        out = same_shell_D_s_zero(energies)
        self.assertTrue(out["ok"])
        self.assertAlmostEqual(out["D_s"], 0.0)

    def test_two_shell_not_zero(self):
        out = same_shell_D_s_zero({1.0: 1.0, 4.0: 0.25})
        self.assertFalse(out["ok"])
        self.assertGreater(out["D_s"], 0.0)


class TestEpsCancelNarrative(unittest.TestCase):
    def test_ds_over_eps2_approaches_limit(self):
        out = limiting_closing_quotient(
            alpha=1.0,
            beta=4.0,
            e_alpha=2.0,
            z_norm_sq=1.0,
            pi_beta_B_ww_norm_sq=3.0,
            epsilons=(1e-1, 1e-2, 1e-3, 1e-4),
        )
        self.assertTrue(out["ok"])
        self.assertTrue(out["eps_cancel_narrative"])
        ray = kab_rayleigh(1.0, 4.0, 3.0, 2.0)["rayleigh"]
        self.assertAlmostEqual(out["rayleigh"], ray)
        self.assertLess(out["relative_error_smallest_eps"], 1e-6)


class TestAttack9ARefusal(unittest.TestCase):
    def test_refuse_ap_packet_closed_kill_lane(self):
        r = refuse_ap_packet_closed_kill_lane(
            "AP packet closed kill lane after Attack 9A"
        )
        self.assertTrue(r["refused"])
        self.assertEqual(r["kill_lane"]["status"], "LIVE")
        self.assertFalse(r["attack_9a"]["killed_lemma_star"])

    def test_inventory_lock(self):
        inv = kab_inventory()
        self.assertFalse(inv["ns_solved"])
        self.assertFalse(inv["sfe"])
        self.assertEqual(inv["attack_9a"]["verdict"], "NEGATIVE_FOR_KILL")
        self.assertEqual(inv["jonathan_action"], "none")
        self.assertIn("K_{alpha,beta}", inv["K_alpha_beta"])
        self.assertIn("K_{alpha,beta}", KAB_FORMULA)
        self.assertEqual(ATTACK_9A_STATUS["verdict"], "NEGATIVE_FOR_KILL")

    def test_lemma_star_refuses_ap_packet_claim(self):
        result = refuse_proved_lemma_star(
            "AP packet closed kill lane; Lemma★ almost proved"
        )
        self.assertTrue(result["refused"])

    def test_kill_lane_still_live_in_five_lane(self):
        self.assertEqual(FIVE_LANE_STATUS["lanes"]["kill_lane"], "LIVE")
        self.assertEqual(
            FIVE_LANE_STATUS["lanes"]["attack_9a"], "NEGATIVE_FOR_KILL"
        )
        self.assertEqual(
            FIVE_LANE_STATUS["attack_9a"]["verdict"], "NEGATIVE_FOR_KILL"
        )
        closed = refuse_kill_lane_closed("AP packet closed kill lane")
        self.assertTrue(closed["refused"])
        self.assertTrue(closed["attack_9a_negative_for_kill"])


if __name__ == "__main__":
    unittest.main()
