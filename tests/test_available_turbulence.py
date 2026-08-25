#!/usr/bin/env python3
"""Available-tech stack: riblets + suction, 15% desired. Not a tank certificate."""

from __future__ import annotations

import json
import unittest

from domain_architect.app import handle_api
from domain_architect.available_turbulence import (
    available_turbulence_system,
    cycle_available_turbulence,
    is_desired_intensity_setpoint,
    maybe_available_stack,
    riblet_spacing_m,
    shear_velocity,
    wants_available_hardware,
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


class TestRibletWallUnits(unittest.TestCase):
    def test_spacing_scales_as_nu_over_utau(self):
        u_tau = shear_velocity(10.0, 0.002)
        self.assertAlmostEqual(u_tau, 10.0 * (0.001 ** 0.5), places=9)
        s = riblet_spacing_m(s_plus=16.0, nu=1.2e-6, u_tau=u_tau)
        self.assertAlmostEqual(s, 16.0 * 1.2e-6 / u_tau, places=12)
        self.assertGreater(s, 4e-5)
        self.assertLess(s, 8e-5)


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
        self.assertEqual(riblet["geometry"]["s_plus"], [15, 17])
        self.assertAlmostEqual(riblet["geometry"]["h_over_s"], 0.5)
        self.assertEqual(payload["operating_regime"]["primary"], "large cargo / container ship hull")
        self.assertEqual(payload["operating_regime"]["aircraft_cruise"]["mach"], [0.75, 0.85])
        self.assertEqual(
            payload["operating_regime"]["aircraft_cruise"]["altitude_ft"],
            [30000, 40000],
        )
        self.assertEqual(payload["operating_regime"]["re_tau_panel"], [1000, 5000])
        self.assertIn("aircraft cruise", payload["operating_regime"]["secondary"])
        ship = payload["ship_package"]
        self.assertEqual(ship["primary_market"], "large cargo / container ships")
        self.assertEqual(ship["realized_or_desired"], "desired")
        self.assertTrue(ship["cf_reduction_target"]["contains_8pct"])
        self.assertFalse(ship["cf_reduction_target"]["contains_12pct"])
        self.assertTrue(ship["da_does_not_file"])
        self.assertEqual(ship["validation_gate"], "empirical[unverified]")
        hull_ids = [row["id"] for row in ship["not_selected_for_hull"]]
        self.assertIn("discrete-suction", hull_ids)
        self.assertIn("locally-resonant-film", hull_ids)
        s_um = ship["stations"][0]["s_um_band"]
        self.assertGreater(s_um[0], 30.0)
        self.assertLess(s_um[1], 120.0)
        overlay = payload["licensing_overlay"]
        self.assertTrue(overlay["da_does_not_file"])
        self.assertEqual(overlay["claimed_first_cycle_lab"]["da_status"], "refused")
        kept = {p["id"]: p["kept"] for p in overlay["pieces"]}
        self.assertTrue(kept["ship-regime"])
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
        board = payload["board"]["text"]
        self.assertIn("SHIP PRODUCT (MAERSK-CLASS)", board)
        self.assertIn("contains_12%=False", board)
        self.assertIn("SELECTED", board)
        self.assertIn("sawtooth-riblets", board)
        self.assertIn("discrete-suction", board)
        self.assertIn("NOT SELECTED", board)
        self.assertIn("locally-resonant-film", board)
        self.assertIn("refused", board)
        self.assertIn("first-cycle-9-14-lab", board)
        self.assertIn("provisional-patent", board)
        self.assertIn("kept", board)
        self.assertIn("riblet-geometry", board)
        self.assertIn("NOT CLAIMED", board.upper())
        self.assertEqual(payload["board"]["selected"], ["sawtooth-riblets", "discrete-suction"])
        self.assertIn("resonant-film", payload["board"]["refused_overlay"])
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
        self.assertIn("AVAILABLE-TECH TURBULENCE STACK", text)
        self.assertIn("SHIP PRODUCT (MAERSK-CLASS)", text)
        self.assertIn("contains_12%=False", text)
        self.assertIn("GROK HYBRID SKETCH", text)
        self.assertIn("refused", text)
        self.assertIn("first-cycle-9-14-lab", text)


class TestSynthesizeHardwarePath(unittest.TestCase):
    def test_hardware_language_selects_the_stack(self):
        self.assertTrue(is_desired_intensity_setpoint("x → 0.85"))
        self.assertTrue(is_desired_intensity_setpoint("x=0.85"))
        self.assertFalse(is_desired_intensity_setpoint("x=1"))
        self.assertFalse(is_desired_intensity_setpoint("decrease turbulence"))
        self.assertTrue(wants_available_hardware(["hardware already available"]))
        self.assertFalse(wants_available_hardware(["|u| ≤ 6", "manufacturable"]))
        stacked = maybe_available_stack(
            "x → 0.85",
            ["|u| ≤ 6", "hardware already available"],
        )
        self.assertIsNotNone(stacked)
        self.assertEqual(stacked["name"], "available_turbulence_stack")
        self.assertEqual(stacked["protocol"], "available-turbulence")
        self.assertEqual(stacked["realized_or_desired"], "desired")
        self.assertIn("riblet_geometry", " ".join(stacked["components"]))
        self.assertIn("AVAILABLE-TECH TURBULENCE STACK", stacked["board"]["text"])
        analog = maybe_available_stack("x → 0.85", ["|u| ≤ 6"])
        self.assertIsNone(analog)
        hijack = maybe_available_stack("x=1", ["hardware already available"])
        self.assertIsNone(hijack)
        slogan = maybe_available_stack(
            "decrease turbulence",
            ["hardware already available"],
        )
        self.assertIsNone(slogan)
        cand = inverse_design_architecture("x → 0.85", ["|u| ≤ 6"])
        self.assertEqual(cand.name, "inverse_design[second_order_linear]")

    def test_synthesize_api_and_cli_use_the_stack_path(self):
        import io
        from contextlib import redirect_stdout

        from domain_architect.cli import main

        status, body, _ = handle_api(
            "/api/synthesize",
            {
                "target": "x → 0.85",
                "constraints": ["|u| ≤ 6", "hardware already available"],
            },
        )
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["name"], "available_turbulence_stack")
        self.assertIn("AVAILABLE-TECH TURBULENCE STACK", payload["board"]["text"])
        status, body, _ = handle_api(
            "/api/synthesize",
            {"target": "x → 0.85", "constraints": ["|u| ≤ 6"]},
        )
        self.assertEqual(status, 200)
        analog = json.loads(body)
        self.assertEqual(analog["name"], "inverse_design[second_order_linear]")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(
                [
                    "synthesize",
                    "--target",
                    "x → 0.85",
                    "--constraint",
                    "|u| ≤ 6",
                    "--constraint",
                    "hardware already available",
                ]
            )
        self.assertEqual(code, 0)
        text = buf.getvalue()
        self.assertIn("available_turbulence_stack", text)
        self.assertIn("AVAILABLE-TECH TURBULENCE STACK", text)
        self.assertIn("riblet_geometry", text)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
