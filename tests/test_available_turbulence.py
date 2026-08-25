#!/usr/bin/env python3
"""Available-tech stack: riblets + suction, 15% desired. Not a tank certificate."""

from __future__ import annotations

import json
import unittest

from domain_architect.app import handle_api
from domain_architect.available_turbulence import (
    available_turbulence_system,
    cycle_available_turbulence,
)
from domain_architect.catalog import default_catalog
from domain_architect.pipeline import run_named_cycle
from domain_architect.schema import CorrespondenceKind, FunctionalRole, ValidationGate
from domain_architect.synthesize import inverse_design_architecture


class TestSloganStillRefuses(unittest.TestCase):
    def test_decrease_turbulence_is_not_a_setpoint(self):
        cand = inverse_design_architecture("decrease turbulence", ["|u|<=6"])
        self.assertEqual(cand.name, "inverse_design[refused]")
        self.assertFalse(any("control u" in c for c in cand.components))


class TestCatalogHasSuction(unittest.TestCase):
    def test_discrete_suction_is_a_forcing_mechanism(self):
        by_id = {m.mechanism_id: m for m in default_catalog()}
        self.assertIn("discrete_suction", by_id)
        self.assertIn("riblet_geometry", by_id)
        suction = by_id["discrete_suction"]
        self.assertEqual(suction.signature.role, FunctionalRole.FORCING)
        self.assertEqual(suction.operator, "v_wall = −v_suction")


class TestAvailableTurbulenceStack(unittest.TestCase):
    def test_desired_fifteen_percent_and_envelope_not_added(self):
        payload = available_turbulence_system()
        self.assertEqual(payload["protocol"], "available-turbulence")
        self.assertEqual(payload["realized_or_desired"], "desired")
        self.assertEqual(payload["desired"]["as_setpoint"], "x → 0.85")
        self.assertAlmostEqual(payload["desired"]["value"], 0.85)
        self.assertAlmostEqual(payload["target_cut"], 0.15)
        self.assertAlmostEqual(payload["industry_standard"]["x"], 1.0)
        selected_ids = [m["id"] for m in payload["stack"]]
        self.assertEqual(selected_ids, ["sawtooth-riblets", "discrete-suction"])
        catalog_ids = [m["id"] for m in payload["catalog"]]
        self.assertIn("superhydrophobic-slip", catalog_ids)
        shs = next(m for m in payload["catalog"] if m["id"] == "superhydrophobic-slip")
        self.assertFalse(shs["selected"])
        self.assertFalse(shs["field_ready"])
        self.assertFalse(payload["percentages_were_added"])
        self.assertGreaterEqual(payload["selected_high"], 0.15)
        self.assertTrue(payload["envelope_can_contain_target"])
        self.assertGreater(payload["sum_of_highs_not_used"], payload["selected_high"])
        self.assertEqual(payload["kind"], CorrespondenceKind.ANALOGY.value)
        self.assertNotIn("TRANSFORMABLE", payload["kind"].upper())
        self.assertFalse(payload["states"]["hardware_realized"]["value"])
        self.assertEqual(
            payload["states"]["hardware_realized"]["gate"],
            "empirical[unverified]",
        )
        self.assertTrue(payload["states"]["analog_realized"]["value"])
        self.assertAlmostEqual(payload["analog"]["treated_x"], 0.85, places=3)
        self.assertGreater(payload["analog"]["relative_reduction"], 0.12)
        self.assertLess(payload["analog"]["relative_reduction"], 0.18)
        self.assertEqual(payload["candidate"]["name"], "available_turbulence_stack")
        joined = " ".join(payload["candidate"]["components"])
        self.assertIn("riblet_geometry", joined)
        self.assertIn("discrete_suction", joined)
        self.assertIn("no adding literature percentages", " ".join(payload["refused"]))
        blob = json.dumps(payload).lower()
        self.assertIn("not claimed", blob)
        self.assertIn("clay", blob)
        self.assertNotIn("nav-42", blob)
        self.assertNotIn("qc_coherence", blob)
        self.assertNotIn("fluid-q", blob)

    def test_cycle_uses_recognized_setpoint_and_api(self):
        report = cycle_available_turbulence()
        self.assertEqual(report.mode, "available-turbulence")
        self.assertEqual(report.target, "x → 0.85")
        self.assertEqual(report.validation_gate, ValidationGate.COMPUTATIONAL)
        self.assertEqual(report.candidate.name, "available_turbulence_stack")
        self.assertTrue(any("control u" in c for c in report.candidate.components))
        named = run_named_cycle("available-turbulence")
        self.assertEqual(named.mode, "available-turbulence")
        alias = run_named_cycle("turbulence-system")
        self.assertEqual(alias.mode, "available-turbulence")
        status, body, _ = handle_api("/api/available-turbulence", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["realized_or_desired"], "desired")
        self.assertTrue(payload["envelope_can_contain_target"])
        status, body, _ = handle_api("/api/cycle", {"name": "available-turbulence"})
        self.assertEqual(status, 200)
        cycle = json.loads(body)
        self.assertEqual(cycle["mode"], "available-turbulence")
        blob = json.dumps(cycle).lower()
        self.assertIn("not claimed", blob)
        self.assertNotIn("nav-42", blob)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
