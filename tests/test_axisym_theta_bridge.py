#!/usr/bin/env python3
"""θ lab diagnostics: not a bridge to (A); not WRITE (6). NS not solved."""

from __future__ import annotations

import unittest
from pathlib import Path

from domain_architect.axisym_theta_bridge import (
    HONESTY,
    natural_theta_proxy_probe,
    numeric_bridge_probe,
    run_theta_bridge_battery,
    scaling_obstruction,
)


ROOT = Path(__file__).resolve().parents[1]
ESTIMATE = ROOT / "docs" / "papers" / "swirl" / "AXISYMMETRIC-SHELL-ESTIMATE.md"
BRIEF = ROOT / "docs" / "domain-architect" / "DA-CLASS-HUNT-BRIEF.md"
DECISIONS = ROOT / "docs" / "domain-architect" / "DECISIONS.md"
FACES = ROOT / "docs" / "papers" / "swirl" / "FACES.md"
SND_SIX = ROOT / "docs" / "domain-architect" / "SND-AND-SIX.md"


class TestHonesty(unittest.TestCase):
    def test_locks(self):
        self.assertFalse(HONESTY["NS_solved"])
        self.assertEqual(HONESTY["clay"], "NOT CLAIMED")
        self.assertEqual(HONESTY["DA_VC_01"], "FAIL")
        self.assertFalse(HONESTY["uses_edot_zdot_lambda_to_bound_Tjj"])
        self.assertFalse(HONESTY["A_seated"])
        self.assertFalse(HONESTY["bridges_to_A"])
        self.assertFalse(HONESTY["supplies_WRITE_6_H1"])
        self.assertFalse(HONESTY["D_is_palinstrophy"])
        self.assertFalse(HONESTY["theta_class_proves_NSE_invariance"])
        self.assertFalse(HONESTY["conditional_theta_bound_proves_cutoff_uniform_C"])
        self.assertFalse(HONESTY["spectral_shift_is_lemma_star"])
        self.assertFalse(HONESTY["energy_b0_identity_is_depletion"])
        self.assertIn("wrong_quantities", HONESTY["three_unresolved_parts"][0])
        self.assertIn("enstrophy_transfer", HONESTY["missing_mathematics"][0])
        self.assertIn("bad-pair", HONESTY["WRITE_6_status"])


class TestScalingObstruction(unittest.TestCase):
    def test_kill_direct_is_O_nu(self):
        s = scaling_obstruction(lambda_shell=1.0, z_shell=1.0)
        self.assertEqual(s["status"], "KILL")
        self.assertEqual(s["status_as_bridge"], "PARTIAL/KILL")
        self.assertFalse(s["A_seated"])
        self.assertFalse(s["bridges_to_A"])
        self.assertFalse(s["supplies_WRITE_6_H1"])
        self.assertFalse(s["quantity_mismatch"]["D_is_palinstrophy"])
        self.assertEqual(s["route_1_direct_absorption"]["theta_star_scaling"], "O(ν)")
        self.assertEqual(
            s["route_2_young_palinstrophy_weights"]["theta_star_for_nu_uniform_R"],
            "O(√ν)",
        )
        row = next(r for r in s["nu_table"] if abs(r["nu"] - 1e-4) < 1e-15)
        self.assertLess(row["theta_star_needed_direct_R0"], 1e-3)
        self.assertLess(row["theta_star_needed_young_nu_uniform_R"], 0.05)
        self.assertIn("ė_j", s["does_not_use"])

    def test_coeff_scales_with_nu(self):
        s = scaling_obstruction()
        direct = [r["theta_star_needed_direct_R0"] for r in s["nu_table"]]
        for a, b in zip(direct, direct[1:]):
            self.assertGreater(a, b)


class TestNumericBridge(unittest.TestCase):
    def test_mixed_disks_kill_support(self):
        n = numeric_bridge_probe(n_trials=60, seed=11)
        self.assertIn(n["status"], ("KILL", "PARTIAL"))
        self.assertGreater(n["n_records"], 10)
        self.assertGreater(n["theta_stats"]["mean"], 1e-3)
        frac = n["fraction_trials_eps_implied_lt_1"].get("nu=0.0001", 1.0)
        self.assertLess(frac, 0.5)
        self.assertFalse(n["A_seated"])
        self.assertFalse(n["uses_edot_zdot_lambda"])


class TestNaturalProxy(unittest.TestCase):
    def test_natural_proxy_kill(self):
        p = natural_theta_proxy_probe(n_trials=50, seed=12)
        self.assertEqual(p["status"], "KILL")
        self.assertFalse(p["theta_unrestricted"]["stays_small_on_nonempty_mixed_class"])
        self.assertFalse(p["E_mer/E"]["stays_small_on_nonempty_mixed_class"])
        self.assertGreater(p["E_mer/E"]["mean"], 0.05)


class TestBattery(unittest.TestCase):
    def test_overall_kill(self):
        bat = run_theta_bridge_battery(n_trials=50, seed=13)
        self.assertEqual(bat["overall_status"], "KILL")
        self.assertEqual(bat["status_as_bridge"], "PARTIAL/KILL")
        self.assertEqual(bat["analytic_scaling"]["status"], "KILL")
        self.assertFalse(bat["locks"]["A_seated"])
        self.assertFalse(bat["locks"]["bridges_to_A"])
        self.assertFalse(bat["locks"]["supplies_WRITE_6_H1"])
        self.assertFalse(bat["locks"]["D_is_palinstrophy"])
        self.assertEqual(bat["locks"]["DA_VC_01"], "FAIL")
        self.assertIn("PARTIAL/KILL", bat["dead_end_writeup"]["bridge_status"])
        self.assertIn("not palinstrophy", bat["dead_end_writeup"]["obstruction"])
        self.assertIn("OPEN", bat["dead_end_writeup"]["WRITE_6_H1"])


class TestDocsSynced(unittest.TestCase):
    def test_estimate_has_honesty_lock(self):
        text = ESTIMATE.read_text(encoding="utf-8")
        self.assertIn("What this is not", text)
        self.assertIn("not** palinstrophy", text)
        self.assertIn("conditional laboratory material", text)
        self.assertIn("bad-pair cylinder", text)
        self.assertIn("WRITE (6)", text)
        self.assertIn("axisym_theta_bridge", text)
        self.assertNotIn("θ → palinstrophy bridge: KILL", text.split("## 12.")[0])

    def test_brief_and_decisions_updated(self):
        brief = BRIEF.read_text(encoding="utf-8")
        decisions = DECISIONS.read_text(encoding="utf-8")
        faces = FACES.read_text(encoding="utf-8")
        snd = SND_SIX.read_text(encoding="utf-8")
        self.assertIn("What this is not", brief)
        self.assertIn("not** palinstrophy", brief)
        self.assertIn("WRITE (6)", brief)
        self.assertIn("θ lab honesty lock", decisions)
        self.assertIn("bad-pair cylinder", decisions)
        self.assertIn("θ lab honesty lock", faces)
        self.assertIn("bad-pair cylinder estimate", snd)
        self.assertIn("still needed", snd)


if __name__ == "__main__":
    unittest.main()
