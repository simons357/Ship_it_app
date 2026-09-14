#!/usr/bin/env python3
"""Kept NS model: DA accepts the fluids book; Clay NS not claimed."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.ns_model import ns_components, run_ns_model
from domain_architect.schema import CANONICAL_SFE_STATUS, NS_CLAY_STATUS, RH_STATUS


ROOT = Path(__file__).resolve().parents[1]


class TestNSModel(unittest.TestCase):
    def test_kept_algebra_barrier_open_clay_not_claimed(self):
        report = run_ns_model()
        self.assertEqual(report.instance_name, "kept-ns-swirl")
        self.assertGreater(report.component_count, 5)
        self.assertEqual(report.core_role_count, 5)
        self.assertGreater(report.extension_count, 5)
        self.assertEqual(report.ns_clay_status, NS_CLAY_STATUS)
        self.assertEqual(report.ns_clay_status, "not claimed")
        self.assertEqual(report.rh_status, RH_STATUS)
        self.assertEqual(report.canonical_sfe_status, CANONICAL_SFE_STATUS)

        ids = {c.component_id for c in report.components}
        self.assertIn("NS-keep", ids)
        self.assertIn("NS-barrier", ids)
        self.assertIn("NS-Phi-FRA", ids)
        self.assertIn("NS-park", ids)

        keep = next(c for c in report.components if c.component_id == "NS-keep")
        self.assertTrue(keep.independently_specified)
        self.assertIn("KEEP", keep.verdict)
        self.assertIn("algebra", keep.verdict.lower())

        barrier = next(c for c in report.components if c.component_id == "NS-barrier")
        self.assertFalse(barrier.independently_specified)
        self.assertIn("OPEN", barrier.verdict)
        self.assertIn("u^r/r", barrier.occupant)

        fra_phi = next(c for c in report.components if c.component_id == "NS-Phi-FRA")
        self.assertFalse(fra_phi.independently_specified)
        self.assertIn("Do not write Φ_FRA := Φ_swirl", fra_phi.verdict)

        h_role = next(c for c in report.components if c.component_id == "NS-H")
        self.assertIn("not as a Hilbert–Pólya Hamiltonian", h_role.da_action)

        self.assertIn("NS-H002", report.registry_ids)
        filled = " ".join(report.filled)
        self.assertIn("KEEP swirl identity", filled)
        gaps = " ".join(report.open_gaps)
        self.assertIn("u^r/r", gaps)

        text = report.narrative().lower()
        self.assertIn("fluids book", text)
        self.assertIn("load-bearing gap", text)
        self.assertNotIn("proves the riemann hypothesis", text)
        self.assertNotIn("proves clay", text)
        self.assertNotIn("ns is solved", text)
        self.assertIn("not claimed", text)
        self.assertIn("cannot call this clay ns closed", text)

    def test_swirl_phi_is_not_fra_phi(self):
        roles = {c.component_id: c for c in ns_components()}
        self.assertEqual(roles["NS-Phi-FRA"].role, "Φ")
        swirl = next(c for c in ns_components() if "Φ_swirl" in c.occupant)
        self.assertNotEqual(swirl.component_id, "NS-Phi-FRA")
        self.assertNotEqual(swirl.role, "Φ")

    def test_cli_ns_model(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--ns-model"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("kept NS model", proc.stdout)
        self.assertIn("KEEP identity", proc.stdout)
        self.assertIn("Clay NS status: not claimed", proc.stdout)
        self.assertIn("Riemann hypothesis status: not claimed", proc.stdout)
        self.assertIn("Φ_swirl", proc.stdout)
        self.assertIn("u^r/r", proc.stdout)
        self.assertIn("NS-H002", proc.stdout)
        self.assertIn("fluids book", proc.stdout)
        self.assertNotIn("proves the riemann hypothesis", proc.stdout.lower())
        self.assertNotIn("proves clay", proc.stdout.lower())
        self.assertIn("cannot call this clay ns closed", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
