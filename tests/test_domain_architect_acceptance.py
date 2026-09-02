#!/usr/bin/env python3
"""Kept mathematical hygiene tests from the 2026 rectification.

Historical SFE / prime-selector tests live in test_historical_archive.py.
"""

from __future__ import annotations

import unittest

import numpy as np

from domain_architect.audit import audit_expression
from domain_architect.checks import classify_permission
from domain_architect.gravity import solve_periodic_poisson
from domain_architect.identifiability import analyze_product_abx
from domain_architect.recovery import classify_recovery
from domain_architect.schema import (
    EvidenceLevel,
    RecoveryKind,
)


class TestASymbolAmbiguity(unittest.TestCase):
    def test_h_psi_is_not_a_hamiltonian(self):
        report = audit_expression("Hψ")
        roles = [
            (a["symbol"], a["candidate_role"], a.get("subtype"))
            for a in report.role_assignments
        ]
        for symbol, role, subtype in roles:
            self.assertNotEqual(role.lower(), "hamiltonian")
            self.assertNotEqual((subtype or "").lower(), "hamiltonian")
            if symbol == "H":
                self.assertIn(role, {"unresolved_left_factor", "unresolved"})
        joined = " ".join(report.warnings).lower()
        self.assertTrue(
            "not automatically a hamiltonian" in joined
            or "does not declare h a hamiltonian" in joined
        )


class TestBProjector(unittest.TestCase):
    def test_non_idempotent_operator_is_not_a_projector(self):
        p = np.array([[1.0, 0.2], [0.0, 0.5]])
        check = classify_permission(p)
        self.assertFalse(check.is_projector)
        self.assertNotIn("projector", check.label)
        self.assertIn("not a mathematical projector", check.details.lower())


class TestCPoissonZeroMode(unittest.TestCase):
    def test_nonzero_mean_rejected_before_k_squared(self):
        x = np.linspace(0.0, 2.0 * np.pi, 64, endpoint=False)
        rho = 1.0 + 0.3 * np.cos(x)
        result = solve_periodic_poisson(rho, mean_policy="reject")
        self.assertFalse(result.compatibility.compatible)
        self.assertFalse(result.divided_by_k_squared)
        self.assertIsNone(result.potential)
        self.assertIn("1/k", result.compatibility.message.lower())
        self.assertGreater(abs(result.compatibility.source_mean), 1e-6)

    def test_zero_mean_source_solves(self):
        x = np.linspace(0.0, 2.0 * np.pi, 64, endpoint=False)
        rho = np.cos(x)
        result = solve_periodic_poisson(rho, G=1.0, mean_policy="reject")
        self.assertTrue(result.compatibility.compatible)
        self.assertTrue(result.divided_by_k_squared)
        self.assertIsNotNone(result.potential)
        # ∇²Φ = 4πGρ  ⇒  Φ ≈ -4πG cos(x) because ∇² cos(x) = -cos(x)
        expected = -4.0 * np.pi * rho
        self.assertLess(
            np.linalg.norm(result.potential - expected) / np.linalg.norm(expected),
            1e-6,
        )


class TestEParameterRedundancy(unittest.TestCase):
    def test_abx_not_separately_identifiable(self):
        report = analyze_product_abx(np.array([1.0, 2.0, 3.0]))
        self.assertFalse(report.locally_full_rank)
        self.assertTrue(report.product_ambiguities)
        self.assertIn("not separately identifiable", report.product_ambiguities[0])
        self.assertNotEqual(report.statement.lower(), "the parameters are identifiable.")
        audited = audit_expression("y=abx")
        self.assertIsNotNone(audited.identifiability)
        self.assertIn(
            "not separately identifiable",
            " ".join(audited.identifiability["product_ambiguities"]),
        )


class TestFRepresentationVersusDerivation(unittest.TestCase):
    def test_poisson_map_is_representation_not_derivation(self):
        report = audit_expression("∇²Φ = 4π G ρ")
        narrative = report.narrative().lower()
        self.assertEqual(report.recovery_kind, RecoveryKind.REPRESENTATION_RECOVERY.value)
        self.assertLessEqual(
            int(report.highest_evidence_level),
            int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY),
        )
        self.assertIn("represent", narrative)
        self.assertNotIn("derives newtonian gravity", narrative)
        self.assertIn("not derivation", narrative)
        self.assertNotIn("canonical sfe", narrative)
        rec = classify_recovery(
            known_equation_rewritten=True,
            independent_broader_model=False,
            target_theory="Newtonian Poisson gravity",
        )
        self.assertEqual(rec.kind, RecoveryKind.REPRESENTATION_RECOVERY)


class TestLanguageAndScope(unittest.TestCase):
    def test_live_reports_do_not_revive_sfe(self):
        report = audit_expression("Hψ")
        narrative = report.narrative().lower()
        self.assertIn("decompose", narrative)
        self.assertNotIn("canonical sfe status: unresolved", narrative)

    def test_role_confidence_does_not_imply_physics(self):
        report = audit_expression("∇²Φ = 4π G ρ")
        self.assertEqual(report.confidence.physical_validation_status, "benchmark_representation")
        narrative = report.narrative().lower()
        self.assertIn("does not imply physical validity", narrative)


if __name__ == "__main__":
    unittest.main()
