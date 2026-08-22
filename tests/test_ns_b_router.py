#!/usr/bin/env python3
"""Classical NS-B five-finger router acceptance checks."""

from __future__ import annotations

import unittest

from domain_architect.audit import audit_expression
from domain_architect.navier_stokes import (
    DOMAIN_ID,
    detect_classical_ns,
)
from domain_architect.parser import parse_expression
from domain_architect.registry import EquationRegistry
from domain_architect.schema import EvidenceLevel


class TestNSBDetection(unittest.TestCase):
    def test_vorticity_form_detected(self):
        expr = "partial_t omega + (u * nabla) omega = (omega * nabla) u + nu Delta omega"
        parsed = parse_expression(expr)
        det = detect_classical_ns(expr, parsed)
        self.assertTrue(det.matched)
        self.assertEqual(det.form, "vorticity")

    def test_velocity_form_detected(self):
        expr = "partial_t u + (u * nabla) u = - nabla p + nu Delta u"
        parsed = parse_expression(expr)
        det = detect_classical_ns(expr, parsed)
        self.assertTrue(det.matched)
        self.assertEqual(det.form, "velocity")

    def test_augmented_track_a_not_ns_b(self):
        expr = "partial_t omega = nu Delta omega + epsilon |nabla u|^2"
        det = detect_classical_ns(expr, parse_expression(expr))
        self.assertFalse(det.matched)


class TestNSBAuditRouting(unittest.TestCase):
    def test_auto_routes_and_assigns_five_fingers(self):
        expr = "partial_t omega = (omega * nabla) u + nu Delta omega"
        report = audit_expression(expr)
        roles = {a["candidate_role"] for a in report.role_assignments}
        self.assertIn("admissibility", roles)
        self.assertIn("interaction", roles)
        self.assertIn("state", roles)
        self.assertIn("scale_response", roles)
        self.assertIn("realized_output", roles)
        self.assertIn("environment", roles)
        joined = " ".join(report.notes + report.warnings).lower()
        self.assertIn("ns-b", joined)
        self.assertIn("millennium", joined)
        self.assertEqual(
            report.highest_evidence_level,
            EvidenceLevel.COHERENT_CLASSIFICATION,
        )
        self.assertNotIn("sfe derivation", joined)
        # No gravity-style known-limit recovery for classical NS routing.
        self.assertIsNone(report.recovery_kind)

    def test_velocity_cli_style_tokens(self):
        expr = "partialt u = -nablap + nu Deltau"
        report = audit_expression(expr)
        joined = " ".join(report.notes + report.warnings)
        self.assertIn(DOMAIN_ID, joined)
        symbols = {a["symbol"] for a in report.role_assignments}
        self.assertTrue({"u", "nu", "p"} & symbols)

    def test_registry_contains_ns_b(self):
        reg = EquationRegistry.load_default()
        ids = set(reg.equations.keys())
        self.assertIn("NS-B001", ids)
        self.assertIn("NS-B002", ids)


class TestNSBDoesNotStealGravity(unittest.TestCase):
    def test_poisson_still_gravity(self):
        report = audit_expression("nabla^2 Phi = 4 pi G rho")
        joined = " ".join(report.notes + [report.recovery_statement or ""]).lower()
        self.assertIn("poisson", joined)
        self.assertNotIn("ns-b", " ".join(report.warnings).lower())


if __name__ == "__main__":
    unittest.main()
