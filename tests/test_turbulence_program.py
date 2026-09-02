#!/usr/bin/env python3
"""Turbulence-reduction program: four applications, ships ACTIVE, rest QUEUED."""

from __future__ import annotations

import json
import unittest
from io import StringIO
from contextlib import redirect_stdout

from domain_architect.app import handle_api
from domain_architect.pipeline import run_named_cycle
from domain_architect.schema import CorrespondenceKind, ValidationGate
from domain_architect.synthesize import inverse_design_architecture
from domain_architect.turbulence_program import (
    APPLICATION_ORDER,
    cycle_turbulence_reduction,
    turbulence_reduction_program,
)


class TestSloganStillRefuses(unittest.TestCase):
    def test_decrease_turbulence_is_not_the_program_setpoint(self):
        cand = inverse_design_architecture("decrease turbulence", ["|u|<=6"])
        self.assertEqual(cand.name, "inverse_design[refused]")
        self.assertFalse(any("control u" in c for c in cand.components))


class TestTurbulenceReductionProgram(unittest.TestCase):
    def test_four_applications_ships_active_rest_queued(self):
        payload = turbulence_reduction_program()
        self.assertEqual(payload["protocol"], "turbulence-reduction")
        self.assertEqual(payload["project"], "turbulence-reduction")
        self.assertEqual(payload["application_order"], list(APPLICATION_ORDER))
        self.assertEqual(
            payload["application_order"],
            ["ships", "aircraft", "submarines", "hypersonic"],
        )
        self.assertEqual(payload["active"], ["ships"])
        self.assertEqual(payload["queued"], ["aircraft", "submarines", "hypersonic"])
        self.assertEqual(payload["kind"], CorrespondenceKind.ANALOGY.value)
        self.assertEqual(payload["validation_gate"], ValidationGate.MATHEMATICAL.value)

        apps = payload["applications"]
        self.assertEqual([row["id"] for row in apps], list(APPLICATION_ORDER))

        ships = payload["by_id"]["ships"]
        self.assertEqual(ships["status"], "ACTIVE")
        self.assertEqual(ships["customer"], "Maersk-class liner and similar")
        self.assertEqual(ships["cycle"], "available-turbulence")
        self.assertTrue(ships["contains_8pct"])
        self.assertFalse(ships["contains_12pct"])
        self.assertFalse(ships["envelope_awarded"])
        self.assertIn("Maersk", ships["operating_regime"])

        for slot in ("aircraft", "submarines", "hypersonic"):
            row = payload["by_id"][slot]
            self.assertEqual(row["status"], "QUEUED")
            self.assertFalse(row["envelope_awarded"])
            self.assertEqual(row["stack_selected"], [])
            self.assertIsNone(row["cycle"])
            self.assertNotIn("contains_8pct", row)
            self.assertNotIn("product_stack", row)

        aircraft = payload["by_id"]["aircraft"]
        self.assertIn("drones / UAV", aircraft["includes"])

        hypersonic = payload["by_id"]["hypersonic"]
        self.assertTrue(hypersonic["not_a_weapon_design"])
        self.assertTrue(hypersonic["public_literature_only"])
        self.assertIn("plasma", hypersonic["operating_regime"])

        board = payload["board"]["text"]
        self.assertIn("TURBULENCE REDUCTION PROGRAM", board)
        self.assertIn("QUEUED", board)
        self.assertIn("ships", board)
        self.assertIn("aircraft", board)
        self.assertIn("submarines", board)
        self.assertIn("hypersonic", board)
        self.assertIn("drones", board)
        self.assertNotIn("  missiles  ", board)
        self.assertIn("12% contained=False", board)

        blob = json.dumps(payload).lower()
        self.assertIn("not claimed", blob)
        self.assertIn("clay", blob)
        self.assertIn("maersk", blob)
        self.assertNotIn("nav-42", blob)
        self.assertNotIn("qc_coherence", blob)
        self.assertNotIn("fluid-q", blob)
        self.assertNotIn("2.2 hz", blob)
        self.assertNotIn("resonant paint", blob)
        self.assertNotIn("chat vault", blob)

    def test_cycle_named_api_and_aliases(self):
        report = cycle_turbulence_reduction()
        self.assertEqual(report.mode, "turbulence-reduction")
        self.assertEqual(report.validation_gate, ValidationGate.MATHEMATICAL)
        self.assertEqual(report.candidate.name, "turbulence_reduction_program")
        self.assertFalse(any("control u" in c for c in report.candidate.components))

        named = run_named_cycle("turbulence-reduction")
        self.assertEqual(named.mode, "turbulence-reduction")
        alias = run_named_cycle("tr-program")
        self.assertEqual(alias.mode, "turbulence-reduction")
        apps = run_named_cycle("tr-applications")
        self.assertEqual(apps.mode, "turbulence-reduction")

        status, body, _ = handle_api("/api/turbulence-reduction", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["protocol"], "turbulence-reduction")
        self.assertEqual(payload["active"], ["ships"])

        status, body, _ = handle_api("/api/cycle", {"name": "turbulence-reduction"})
        self.assertEqual(status, 200)
        cycle = json.loads(body)
        self.assertEqual(cycle["mode"], "turbulence-reduction")
        prediction = cycle["prediction"]
        self.assertEqual(prediction["queued"], ["aircraft", "submarines", "hypersonic"])

    def test_cli_prints_program_board(self):
        from domain_architect.cli import main

        buf = StringIO()
        with redirect_stdout(buf):
            code = main(["cycle", "turbulence-reduction"])
        self.assertEqual(code, 0)
        text = buf.getvalue()
        self.assertIn("TURBULENCE REDUCTION PROGRAM", text)
        self.assertIn("QUEUED", text)
        self.assertIn("ships", text)
        self.assertIn("aircraft", text)
        self.assertIn("submarines", text)
        self.assertIn("hypersonic", text)
        self.assertIn("drones", text)
        self.assertIn("12% contained=False", text)
        self.assertNotIn("NAV-42", text)
        self.assertNotIn("2.2 Hz", text)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
