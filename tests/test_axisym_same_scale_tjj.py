#!/usr/bin/env python3
"""Same-scale T_{j←j} attack diagnostics. No class close. NS not solved."""

from __future__ import annotations

import unittest
from pathlib import Path

from domain_architect.axisym_same_scale_tjj import (
    DEFINITION,
    avenue_axisym_cancellation,
    avenue_conditional_theta,
    avenue_depletion_to_A,
    avenue_numeric_kill_search,
    conditional_theta_bound,
    energy_z,
    enumerate_hh_to_l_triads,
    enumerate_near_scale_feeders,
    enumerate_same_scale_triads,
    geometric_factor_theta,
    maximize_same_scale_ratio,
    random_div_free_amp,
    run_same_scale_attack_battery,
    shell_modes,
    triad_signed_transfer,
)
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ESTIMATE = ROOT / "docs" / "papers" / "swirl" / "AXISYMMETRIC-SHELL-ESTIMATE.md"
AUDIT = ROOT / "docs" / "domain-architect" / "AXISYMMETRIC-SHELL-AUDIT.md"


class TestDefinition(unittest.TestCase):
    def test_definition_separates_same_scale_from_cross(self):
        self.assertIn("T_{j←j}", DEFINITION["same_scale_block"])
        self.assertIn("HH→L", DEFINITION["cross_scale_block"])
        self.assertTrue(DEFINITION["not_lemma_star"])
        self.assertIn("does_not_kill", DEFINITION["axisym_swirl_kill_or_reduce"])


class TestFourierDisk(unittest.TestCase):
    def test_axisym_slice_has_ky_zero(self):
        modes = shell_modes(2.0, 4.0, disk="axisym_swirl_slice")
        self.assertTrue(modes)
        self.assertTrue(all(k[1] == 0 for k in modes))

    def test_div_free_amp(self):
        rng = np.random.default_rng(0)
        k = (3, 0, 4)
        u = random_div_free_amp(k, rng, disk="axisym_swirl_slice")
        self.assertLess(abs(np.dot(np.array(k, dtype=float), u)), 1e-12)

    def test_signed_transfer_is_real_float(self):
        rng = np.random.default_rng(1)
        p, q = (2, 0, 2), (1, 0, -1)
        k = (3, 0, 1)
        up = random_div_free_amp(p, rng, disk="axisym_swirl_slice")
        uq = random_div_free_amp(q, rng, disk="axisym_swirl_slice")
        uk = random_div_free_amp(k, rng, disk="axisym_swirl_slice")
        t = triad_signed_transfer(up, uq, uk, q)
        self.assertIsInstance(t, float)

    def test_same_scale_and_hh_enumeration_disjoint_roles(self):
        high = shell_modes(3.0, 4.5, disk="axisym_swirl_slice")
        low = shell_modes(0.5, 1.5, disk="axisym_swirl_slice")
        same = enumerate_same_scale_triads(high)
        hh = enumerate_hh_to_l_triads(high, low)
        # HH→L targets live in low shell; same-scale targets in high
        for _p, _q, k in same:
            self.assertIn(k, set(high))
        for _p, _q, k in hh:
            self.assertIn(k, set(low))

    def test_maximize_reports_nonzero_near_scale(self):
        run = maximize_same_scale_ratio(
            disk="axisym_swirl_slice", n_trials=40, seed=11
        )
        self.assertGreater(run["n_shell_modes"], 0)
        self.assertGreater(run["n_neighbor_modes"], run["n_shell_modes"])
        self.assertTrue(run["energy_sharp_b0_identity_holds"])
        self.assertLess(run["max_|T_internal_b0|"], 1e-8)
        self.assertGreater(run["best"]["max_|T_near|/Z^{3/2}"], 1e-8)
        self.assertFalse(run["uses_edot_zdot_lambda"])
        self.assertFalse(run["claimed_bound"])

    def test_sharp_b0_energy_identity_is_not_depletion(self):
        """Sharp b=0 energy internal ≡0 is triad pairing, not depletion."""
        run = maximize_same_scale_ratio(
            disk="axisym_swirl_slice",
            n_trials=20,
            seed=5,
        )
        self.assertTrue(run["energy_sharp_b0_identity_holds"])
        self.assertIn("triad pairing", run["hygiene_shell_only_would_telescope"].lower())
        self.assertIn("b≥1", run["hygiene_shell_only_would_telescope"])


class TestAvenues(unittest.TestCase):
    def test_depletion_kills_occupancy_and_recycling(self):
        a2 = avenue_depletion_to_A()
        self.assertEqual(a2["status"], "PARTIAL")
        statuses = {c["status"] for c in a2["killed"]}
        self.assertEqual(statuses, {"KILLED"})
        self.assertFalse(a2["implies_A_for_class"])
        self.assertEqual(a2["open_candidate"]["status"], "OPEN")

    def test_conditional_theta_template(self):
        ok = conditional_theta_bound(theta=0.3, z=2.0, d_proxy=4.0, c_young=1.0)
        self.assertEqual(ok["status"], "conditional_template")
        self.assertFalse(ok["claimed"])
        self.assertFalse(ok["is_condition_A"])
        self.assertAlmostEqual(ok["rhs"], 0.3 * 1.0 * 2.0 * 2.0)
        bad = conditional_theta_bound(theta=1.5, z=1.0, d_proxy=1.0)
        self.assertEqual(bad["status"], "refused")

    def test_cancellation_avenue_partial(self):
        a1 = avenue_axisym_cancellation()
        self.assertEqual(a1["status"], "PARTIAL")
        self.assertIsNone(a1["bound_obtained"])
        self.assertEqual(a1["absolute_value_Young"], "REFUSED for this avenue")

    def test_numeric_kills_axisym_forces_zero(self):
        a4 = avenue_numeric_kill_search()
        self.assertIn("KILLED", a4["killed_claim"])
        self.assertIn("KILLED", a4["killed_artifact"])
        self.assertFalse(a4["claimed"])
        self.assertGreater(
            a4["axisym_disk"]["best"]["max_|T_near|/Z^{3/2}"], 1e-8
        )
        self.assertTrue(a4["axisym_disk"]["energy_sharp_b0_identity_holds"])

    def test_conditional_avenue(self):
        a3 = avenue_conditional_theta()
        self.assertEqual(a3["status"], "PARTIAL")
        self.assertFalse(a3["seats_A"])
        self.assertIsNone(a3["class_bound"])

    def test_battery_honesty(self):
        bat = run_same_scale_attack_battery()
        self.assertFalse(bat["honesty"]["NS_solved"])
        self.assertEqual(bat["honesty"]["clay"], "NOT CLAIMED")
        self.assertFalse(bat["honesty"]["lemma_star_smuggled"])
        self.assertFalse(bat["honesty"]["uses_edot_zdot_lambda_to_bound_Tjj"])
        self.assertEqual(bat["honesty"]["principal_unresolved"], "T_{j←j}")
        self.assertIn("OPEN", bat["summary"]["overall"])


class TestDocuments(unittest.TestCase):
    def test_estimate_has_same_scale_attack_section(self):
        text = ESTIMATE.read_text(encoding="utf-8")
        self.assertIn("Same-scale transfer attack", text)
        self.assertIn("NS not solved", text)
        self.assertNotIn("depletion established", text.lower())
        # Must not smuggle Lemma★ as transfer control
        attack = (
            text.split("## Same-scale transfer attack")[1]
            if "## Same-scale transfer attack" in text
            else ""
        )
        self.assertIn("OPEN", attack)
        self.assertIn("PARTIAL", attack)
        self.assertIn("KILLED", attack)

    def test_audit_keep_mentions_same_scale_attack(self):
        text = AUDIT.read_text(encoding="utf-8")
        self.assertIn("same-scale", text.lower())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
