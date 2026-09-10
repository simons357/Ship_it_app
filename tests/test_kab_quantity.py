#!/usr/bin/env python3
"""Tests: Attack 9B K_{α,β} stub — ε-cancel narrative, SoT 9A–9D naming."""

from __future__ import annotations

import unittest

from domain_architect.kab_quantity import (
    ATTACK_9A_STATUS,
    ATTACK_9B_STATUS,
    ATTACK_9C_STATUS,
    ATTACK_9D_STATUS,
    ATTACK_9_FIXED_GAP_STATUS,
    KAB_FORMULA,
    kab_inventory,
    kab_rayleigh,
    limiting_closing_quotient,
    refuse_ap_packet_closed_kill_lane,
    refuse_nine_b_killed_star,
    refuse_same_shell_ensemble_kills_star,
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


class TestAttack9SoTNaming(unittest.TestCase):
    def test_refuse_ap_packet_closed_kill_lane(self):
        r = refuse_ap_packet_closed_kill_lane(
            "AP packet closed kill lane after Attack 9A"
        )
        self.assertTrue(r["refused"])
        self.assertEqual(r["kill_lane"]["status"], "LIVE")
        self.assertFalse(r["attack_9a"]["killed_lemma_star"])

    def test_refuse_nine_b_killed_star(self):
        r = refuse_nine_b_killed_star("9B killed ★")
        self.assertTrue(r["refused"])
        self.assertFalse(r["attack_9b"]["killed_lemma_star"])
        self.assertAlmostEqual(r["runtime"]["max_K_approx"], 0.641, places=3)
        self.assertEqual(r["runtime"]["at_alpha_beta"], (4, 8))
        self.assertEqual(r["kill_lane"]["status"], "LIVE")

    def test_inventory_lock(self):
        inv = kab_inventory()
        self.assertFalse(inv["ns_solved"])
        self.assertFalse(inv["sfe"])
        self.assertEqual(inv["attack_9a"]["verdict"], "NEGATIVE_FOR_KILL")
        self.assertEqual(inv["attack_9c"]["verdict"], "NEGATIVE_FOR_KILL")
        self.assertEqual(
            inv["attack_9_fixed_gap"]["verdict"], "NEGATIVE_FOR_KILL"
        )
        self.assertIs(ATTACK_9_FIXED_GAP_STATUS, ATTACK_9C_STATUS)
        self.assertEqual(
            inv["attack_9d"]["verdict"], "REMAINING_PACKET_FALSIFIER"
        )
        self.assertEqual(inv["jonathan_action"], "none")
        self.assertEqual(inv["remaining_falsifier"], "ATTACK-9D-THETA-M2-CLOSURE")
        self.assertIn("K_{alpha,beta}", inv["K_alpha_beta"])
        self.assertIn("K_{alpha,beta}", KAB_FORMULA)
        self.assertEqual(ATTACK_9A_STATUS["verdict"], "NEGATIVE_FOR_KILL")
        self.assertEqual(
            ATTACK_9C_STATUS["R_star"]["values"], (0.11, 0.031)
        )
        self.assertFalse(ATTACK_9C_STATUS["R_star"]["tracks_m_half"])
        self.assertEqual(ATTACK_9D_STATUS["closures"], "Theta(m^2)")
        self.assertEqual(
            ATTACK_9B_STATUS["verdict"], "FINITE_SAMPLE_NOT_KILL_LANE_LIVE"
        )
        self.assertAlmostEqual(
            ATTACK_9B_STATUS["runtime"]["max_K"], 0.6410131735094131
        )
        self.assertEqual(inv["naming_sot"]["9C"].startswith("Fixed-gap"), True)
        self.assertIn("Θ(m²)", inv["naming_sot"]["9D"])

    def test_refuse_same_shell_ensemble_kills_star(self):
        r = refuse_same_shell_ensemble_kills_star(
            "same-shell ensemble kills ★"
        )
        self.assertTrue(r["refused"])
        self.assertEqual(r["kill_lane"]["status"], "LIVE")
        self.assertFalse(r["fixed_gap"]["killed_lemma_star"])
        self.assertEqual(
            r["attack_9d"]["verdict"], "REMAINING_PACKET_FALSIFIER"
        )
        self.assertEqual(r["attack_9c"]["id"], "ATTACK-9C-FIXED-GAP-SPHERES")

    def test_lemma_star_refuses_ap_packet_claim(self):
        result = refuse_proved_lemma_star(
            "AP packet closed kill lane; Lemma★ almost proved"
        )
        self.assertTrue(result["refused"])

    def test_lemma_star_refuses_same_shell_kill(self):
        result = refuse_proved_lemma_star(
            "Natural same-shell ensemble kills Lemma★"
        )
        self.assertTrue(result["refused"])

    def test_kill_lane_still_live_in_five_lane(self):
        self.assertEqual(FIVE_LANE_STATUS["lanes"]["kill_lane"], "LIVE")
        self.assertEqual(
            FIVE_LANE_STATUS["lanes"]["attack_9a"], "NEGATIVE_FOR_KILL"
        )
        self.assertEqual(
            FIVE_LANE_STATUS["lanes"]["attack_9_fixed_gap"],
            "NEGATIVE_FOR_KILL_NATURAL_SAME_SHELL",
        )
        self.assertEqual(
            FIVE_LANE_STATUS["lanes"]["attack_9c"],
            "NEGATIVE_FOR_KILL_NATURAL_SAME_SHELL",
        )
        self.assertEqual(
            FIVE_LANE_STATUS["lanes"]["attack_9d"],
            "REMAINING_THETA_M2_CLOSURE_FALSIFIER",
        )
        self.assertEqual(
            FIVE_LANE_STATUS["attack_9a"]["verdict"], "NEGATIVE_FOR_KILL"
        )
        closed = refuse_kill_lane_closed("AP packet closed kill lane")
        self.assertTrue(closed["refused"])
        self.assertTrue(closed["attack_9a_negative_for_kill"])
        self.assertTrue(closed["fixed_gap_negative_for_kill"])
        self.assertEqual(
            closed["remaining_falsifier"], "ATTACK-9D-THETA-M2-CLOSURE"
        )


if __name__ == "__main__":
    unittest.main()
