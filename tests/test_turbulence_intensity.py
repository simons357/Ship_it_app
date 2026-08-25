#!/usr/bin/env python3
"""Lumped intensity vs no-actuation control. Not 3D NS. Not a coating."""

from __future__ import annotations

import json
import unittest

from domain_architect.app import handle_api
from domain_architect.pipeline import run_named_cycle
from domain_architect.schema import ValidationGate
from domain_architect.synthesize import inverse_design_architecture
from domain_architect.turbulence_intensity import (
    cycle_turbulence_intensity,
    turbulence_intensity_lab,
)


class TestSloganStillRefuses(unittest.TestCase):
    def test_decrease_turbulence_is_not_a_setpoint(self):
        cand = inverse_design_architecture("decrease turbulence", ["|u|<=6"])
        self.assertEqual(cand.name, "inverse_design[refused]")
        self.assertFalse(any("control u" in c for c in cand.components))


class TestIntensityVersusControl(unittest.TestCase):
    def test_treated_is_below_no_actuation_arm(self):
        payload = turbulence_intensity_lab()
        self.assertEqual(payload["protocol"], "turbulence-intensity")
        self.assertEqual(payload["desired"]["as_setpoint"], "x → 0.85")
        self.assertAlmostEqual(payload["desired"]["value"], 0.85)
        self.assertAlmostEqual(payload["desired"]["below_industry_fraction"], 0.15)
        self.assertAlmostEqual(payload["industry_standard"]["x"], 1.0)
        self.assertGreater(payload["control_arm"]["terminal_x"], 0.95)
        self.assertAlmostEqual(payload["treated_arm"]["terminal_x"], 0.85, places=3)
        self.assertLess(
            payload["treated_arm"]["terminal_x"],
            0.9 * payload["control_arm"]["terminal_x"],
        )
        self.assertGreater(payload["relative_reduction"], 0.12)
        self.assertLess(payload["relative_reduction"], 0.18)
        self.assertTrue(payload["reduced_vs_control"])
        self.assertTrue(payload["treated_arm"]["settled"])
        self.assertLessEqual(payload["treated_arm"]["max_control"], 6.0 + 1e-9)
        self.assertEqual(payload["control_arm"]["max_control"], 0.0)
        self.assertIn("no 3D Navier–Stokes", " ".join(payload["refused"]))
        self.assertNotIn("TRANSFORMABLE", payload["kind"].upper())

    def test_cycle_uses_recognized_setpoint_and_api(self):
        report = cycle_turbulence_intensity()
        self.assertEqual(report.mode, "turbulence-intensity")
        self.assertEqual(report.validation_gate, ValidationGate.COMPUTATIONAL)
        self.assertEqual(report.candidate.name, "inverse_design[second_order_linear]")
        self.assertTrue(any("control u" in c for c in report.candidate.components))
        named = run_named_cycle("turbulence-intensity")
        self.assertEqual(named.mode, "turbulence-intensity")
        alias = run_named_cycle("intensity")
        self.assertEqual(alias.mode, "turbulence-intensity")
        status, body, _ = handle_api("/api/turbulence-intensity", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertTrue(payload["reduced_vs_control"])
        status, body, _ = handle_api("/api/cycle", {"name": "turbulence-intensity"})
        self.assertEqual(status, 200)
        cycle = json.loads(body)
        self.assertEqual(cycle["mode"], "turbulence-intensity")
        blob = json.dumps(cycle).lower()
        self.assertIn("not claimed", blob)
        self.assertIn("clay", blob)
        self.assertNotIn("nav-42", blob)
        self.assertNotIn("qc_coherence", blob)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
