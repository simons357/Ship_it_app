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

    def test_eight_to_twelve_slogan_is_not_a_setpoint(self):
        cand = inverse_design_architecture(
            "8-12% net turbulent skin-friction drag reduction",
            ["aircraft cruise"],
        )
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
        self.assertIn("locally-resonant-film", catalog_ids)
        shs = next(m for m in payload["catalog"] if m["id"] == "superhydrophobic-slip")
        self.assertFalse(shs["selected"])
        self.assertFalse(shs["field_ready"])
        resonant = next(m for m in payload["catalog"] if m["id"] == "locally-resonant-film")
        self.assertFalse(resonant["selected"])
        self.assertFalse(resonant["field_ready"])
        self.assertIsNone(resonant["literature_cf_reduction"])
        riblet = next(m for m in payload["stack"] if m["id"] == "sawtooth-riblets")
        self.assertEqual(riblet["geometry"]["s_plus"], [12, 16])
        self.assertEqual(riblet["geometry"]["h_plus"], [8, 12])
        self.assertEqual(payload["operating_regime"]["mach"], [0.75, 0.85])
        self.assertEqual(payload["operating_regime"]["altitude_ft"], [30000, 40000])
        self.assertEqual(payload["operating_regime"]["re_tau_panel"], [1000, 5000])
        self.assertIn("submarine hull", payload["operating_regime"]["secondary"])
        overlay = payload["licensing_overlay"]
        self.assertTrue(overlay["da_does_not_file"])
        self.assertEqual(overlay["claimed_first_cycle_lab"]["da_status"], "refused")
        kept = {p["id"]: p["kept"] for p in overlay["pieces"]}
        self.assertTrue(kept["cruise-regime"])
        self.assertTrue(kept["riblet-geometry"])
        self.assertFalse(kept["resonant-film"])
        self.assertFalse(kept["first-cycle-9-14-lab"])
        self.assertFalse(kept["provisional-patent"])
        self.assertIn("partial", overlay["da_verdict"])
        self.assertAlmostEqual(payload["commercial_band"]["low"], 0.08)
        self.assertAlmostEqual(payload["commercial_band"]["high"], 0.12)
        self.assertTrue(payload["commercial_band"]["inside_selected_envelope"])
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
        self.assertNotIn("2.2 hz", blob)
        self.assertNotIn("resonant paint", blob)

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

    def test_cli_prints_desired_and_analog_not_hardware_certificate(self):
        import io
        from contextlib import redirect_stdout

        from domain_architect.cli import main

        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["cycle", "available-turbulence"])
        self.assertEqual(code, 0)
        text = buf.getvalue()
        self.assertIn("desired x → 0.85", text)
        self.assertIn("analog relative reduction=0.150", text)
        self.assertIn("hardware_realized=False", text)
        self.assertIn("envelope_contains_15%=True", text)
        self.assertIn("literature ranges are not added", text.lower())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
