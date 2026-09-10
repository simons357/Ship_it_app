#!/usr/bin/env python3
"""Tests: Attack 9B K_{α,β} + 9C fixed-gap + 9D Θ(m²) naming locks."""

from __future__ import annotations

import unittest

from domain_architect.kab_quantity import (
    ATTACK_3_PRECISION,
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
        self.assertFalse(out["is_HH_to_L_direction"])  # β>α

    def test_HH_to_L_direction_flag(self):
        out = kab_rayleigh(8.0, 4.0, pi_beta_B_ww_norm_sq=1.0, w_norm_sq=1.0)
        self.assertTrue(out["is_HH_to_L_direction"])  # β<α

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


class TestAttack9PrecisionLocks(unittest.TestCase):
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
        self.assertEqual(inv["attack_9c"]["verdict"], "NEGATIVE_FOR_KILL")
        self.assertEqual(inv["attack_9c"]["id"], "ATTACK-9C-FIXED-GAP-SPHERES")
        self.assertFalse(inv["attack_9c"]["pr48_sweep_script"])
        self.assertFalse(inv["attack_9c"]["pr48_sweep_data"])
        self.assertEqual(
            inv["attack_9d"]["verdict"], "REMAINING_PACKET_FALSIFIER"
        )
        self.assertEqual(inv["attack_9d"]["closures"], "Theta(m^2)")
        self.assertEqual(inv["jonathan_action"], "none")
        self.assertEqual(inv["remaining_falsifier"], "ATTACK-9D-THETA-M2-CLOSURE")
        self.assertEqual(inv["canonical_quotient"], "ratio_R_star_shape")
        self.assertEqual(inv["legacy_quotient_do_not_compare"], "ratio_star")
        self.assertFalse(inv["attack_3_precision"]["strictly_HH_to_L"])
        self.assertFalse(ATTACK_9B_STATUS["runtime_max_is_HH_to_L"])
        self.assertEqual(ATTACK_9B_STATUS["runtime_max_pair"], (4, 8))
        self.assertIn("K_{alpha,beta}", inv["K_alpha_beta"])
        self.assertIn("K_{alpha,beta}", KAB_FORMULA)
        self.assertEqual(ATTACK_9A_STATUS["verdict"], "NEGATIVE_FOR_KILL")
        self.assertEqual(
            ATTACK_9_FIXED_GAP_STATUS["R_star"]["values"], (0.11, 0.031)
        )
        self.assertFalse(ATTACK_9_FIXED_GAP_STATUS["R_star"]["tracks_m_half"])
        self.assertIs(ATTACK_9_FIXED_GAP_STATUS, ATTACK_9C_STATUS)
        self.assertEqual(ATTACK_9D_STATUS["closures"], "Theta(m^2)")
        self.assertFalse(ATTACK_3_PRECISION["restricts_output_to_low"])

    def test_refuse_same_shell_ensemble_kills_star(self):
        r = refuse_same_shell_ensemble_kills_star(
            "same-shell ensemble kills ★"
        )
        self.assertTrue(r["refused"])
        self.assertEqual(r["kill_lane"]["status"], "LIVE")
        self.assertFalse(r["fixed_gap"]["killed_lemma_star"])
        self.assertEqual(r["attack_9c"]["verdict"], "NEGATIVE_FOR_KILL")
        self.assertEqual(
            r["attack_9d"]["verdict"], "REMAINING_PACKET_FALSIFIER"
        )

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
        closed = refuse_kill_lane_closed("AP packet closed kill lane")
        self.assertTrue(closed["refused"])
        self.assertTrue(closed["attack_9a_negative_for_kill"])
        self.assertTrue(closed["fixed_gap_negative_for_kill"])
        self.assertEqual(
            closed["remaining_falsifier"], "ATTACK-9D-THETA-M2-CLOSURE"
        )


if __name__ == "__main__":
    unittest.main()
