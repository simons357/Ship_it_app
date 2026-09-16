#!/usr/bin/env python3
"""Class hunt diagnostics for Door-1 / (A). No class close. NS not solved."""

from __future__ import annotations

import unittest
from pathlib import Path

from domain_architect.axisym_class_hunt import (
    HONESTY,
    class_alignment_theta,
    class_finite_fourier_disk,
    class_odd_odd_even,
    class_pure_swirl,
    class_small_data,
    class_sparse_no_near_triads,
    class_spectral_gap,
    run_class_hunt_battery,
)


ROOT = Path(__file__).resolve().parents[1]
ESTIMATE = ROOT / "docs" / "papers" / "swirl" / "AXISYMMETRIC-SHELL-ESTIMATE.md"
AUDIT = ROOT / "docs" / "domain-architect" / "AXISYMMETRIC-SHELL-AUDIT.md"
DECISIONS = ROOT / "docs" / "domain-architect" / "DECISIONS.md"
FACES = ROOT / "docs" / "papers" / "swirl" / "FACES.md"


class TestHonesty(unittest.TestCase):
    def test_honesty_lock(self):
        self.assertFalse(HONESTY["NS_solved"])
        self.assertEqual(HONESTY["clay"], "NOT CLAIMED")
        self.assertFalse(HONESTY["lemma_star_smuggled"])
        self.assertFalse(HONESTY["uses_edot_zdot_lambda_to_bound_Tjj"])
        self.assertEqual(HONESTY["principal_unresolved"], "T_{j←j}")


class TestPureSwirl(unittest.TestCase):
    def test_instantaneous_zero_evolutionary_kill(self):
        r = class_pure_swirl(n_trials=20, seed=3)
        self.assertEqual(r["verdict_instantaneous"], "KEEP")
        self.assertEqual(r["verdict_evolutionary"], "KILL")
        self.assertLess(r["numeric"]["max_|T_near|"], 1e-10)
        self.assertTrue(r["A_seats"])
        self.assertFalse(r["millennium_relevant"])
        self.assertFalse(r["uses_edot_zdot_lambda"])


class TestFiniteDisk(unittest.TestCase):
    def test_labeled_not_kmax_infinity(self):
        r = class_finite_fourier_disk(n_trials=10, seed=4)
        self.assertEqual(r["verdict_door1_chain"], "KEEP-CONDITIONAL")
        self.assertIn("NOT scaling", r["label"])
        self.assertFalse(r["millennium_relevant"])
        self.assertTrue(r["A_seats"])


class TestSmallData(unittest.TestCase):
    def test_conditional_not_large_data(self):
        r = class_small_data()
        self.assertEqual(r["verdict_door1_chain"], "KEEP-CONDITIONAL")
        self.assertFalse(r["millennium_relevant"])
        self.assertIn("smallness", r["control_kind"])


class TestOOE(unittest.TestCase):
    def test_kills_general_seat(self):
        r = class_odd_odd_even(n_trials=30, seed=5)
        self.assertEqual(r["verdict_door1_chain"], "KILL")
        self.assertFalse(r["A_seats"])
        self.assertTrue(r["numeric"]["general_seat_killed"])
        self.assertGreater(
            r["numeric"]["live_parity_kx_even_kz_even"]["max_|T_near|/Z^{3/2}"],
            1e-8,
        )
        self.assertEqual(
            r["numeric"]["empty_triad_parity_kx_odd_kz_even"]["n_near_triads"],
            0,
        )


class TestSpectralGap(unittest.TestCase):
    def test_gap_kills_energy_near_scale(self):
        r = class_spectral_gap(n_trials=15, seed=6)
        self.assertEqual(r["verdict_door1_chain"], "KEEP-CONDITIONAL")
        self.assertEqual(r["verdict_evolutionary"], "KILL")
        self.assertTrue(r["numeric"]["energy_gap_identity_holds"])
        self.assertFalse(r["A_seats"])  # enstrophy (A) not seated


class TestThetaClass(unittest.TestCase):
    def test_template_not_A(self):
        r = class_alignment_theta(theta_star=0.05, n_trials=40, seed=7)
        self.assertEqual(r["verdict_door1_chain"], "KEEP-CONDITIONAL")
        self.assertFalse(r["A_seats"])
        self.assertTrue(r["Tjj_controlled"])
        self.assertFalse(r["numeric"]["template"]["is_condition_A"])


class TestSparse(unittest.TestCase):
    def test_empty_feeders(self):
        r = class_sparse_no_near_triads()
        self.assertEqual(r["verdict_door1_chain"], "KEEP-CONDITIONAL")
        self.assertEqual(r["verdict_evolutionary"], "KILL")
        self.assertEqual(r["numeric"]["n_near_triads"], 0)
        self.assertTrue(r["Tjj_controlled"])


class TestBattery(unittest.TestCase):
    def test_battery_overall_open(self):
        bat = run_class_hunt_battery()
        self.assertFalse(bat["honesty"]["NS_solved"])
        self.assertIn("No Millennium-scaling", bat["overall"])
        ids = {row["class_id"] for row in bat["summary_table"]}
        self.assertIn("pure_swirl", ids)
        self.assertIn("enforced_alignment_theta", ids)
        self.assertIn("odd_odd_even_reflection", ids)
        ooe = bat["classes"]["odd_odd_even_reflection"]
        self.assertEqual(ooe["verdict_door1_chain"], "KILL")
        # No survivor claims millennium relevance
        for row in bat["summary_table"]:
            self.assertFalse(row["millennium_relevant"])
        self.assertTrue(bat["still_missing_for_full_proof"])


class TestDocuments(unittest.TestCase):
    def test_estimate_has_class_hunt(self):
        text = ESTIMATE.read_text(encoding="utf-8")
        self.assertIn("## Class hunt", text)
        self.assertIn("KEEP", text)
        self.assertIn("KILL", text)
        self.assertIn("enforced_alignment_theta", text)
        self.assertIn("NS not solved", text)
        hunt = text.split("## Class hunt", 1)[1].split("## 11.", 1)[0]
        self.assertIn("NOT CLAIMED", hunt)
        self.assertIn("not seated", hunt.lower())
        self.assertNotIn("Clay is solved", hunt)
        # §12 still refuses the slogan (curly quotes in the refuse list).
        self.assertTrue(
            ("“Clay is solved”" in text) or ('"Clay is solved"' in text)
        )

    def test_audit_decisions_faces_mention_class_hunt(self):
        audit = AUDIT.read_text(encoding="utf-8")
        decisions = DECISIONS.read_text(encoding="utf-8")
        faces = FACES.read_text(encoding="utf-8")
        self.assertIn("class hunt", audit.lower())
        self.assertIn("class hunt", decisions.lower())
        self.assertIn("class hunt", faces.lower())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
