#!/usr/bin/env python3
"""Acceptance tests A–H from the August 2026 scientific rectification."""

from __future__ import annotations

import unittest

import numpy as np

from domain_architect.audit import audit_expression
from domain_architect.checks import classify_permission
from domain_architect.gravity import solve_periodic_poisson
from domain_architect.identifiability import analyze_product_abx
from domain_architect.index_audit import audit_canonical_index
from domain_architect.recovery import classify_recovery
from domain_architect.registry import EquationRegistry
from domain_architect.schema import (
    CANONICAL_SFE_STATUS,
    ConflictRelation,
    EvidenceLevel,
    RecoveryKind,
)
from domain_architect.selectors import run_selector_lab


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


class TestDDegeneratePrimeIndexing(unittest.TestCase):
    def test_degenerate_spectrum_warns_basis_dependence(self):
        eigenvalues = np.array([1.0, 1.0, 4.0, 9.0])
        audit = audit_canonical_index(
            eigenvalues,
            selector_acts_on="individual_basis_vectors",
        )
        self.assertTrue(audit.degenerate)
        self.assertTrue(audit.basis_dependent)
        self.assertFalse(audit.valid_for_physical_prime_test)
        joined = " ".join(audit.warnings).lower()
        self.assertIn("basis", joined)
        self.assertIn("prime", joined)


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
        self.assertNotIn("derivation from a canonical sfe", narrative.replace("not derivation", ""))
        self.assertIn("not derivation from a canonical sfe", narrative)
        rec = classify_recovery(
            known_equation_rewritten=True,
            independent_broader_model=False,
            target_theory="Newtonian Poisson gravity",
        )
        self.assertEqual(rec.kind, RecoveryKind.REPRESENTATION_RECOVERY)


class TestGHistoricalConflict(unittest.TestCase):
    def test_incompatible_sfe_candidates_are_preserved(self):
        registry = EquationRegistry.load_default()
        self.assertIn("SFE-H001", registry.equations)
        self.assertIn("SFE-H002", registry.equations)
        status = registry.refuse_hybrid("SFE-H001", "SFE-H002")
        self.assertEqual(status, "preserved_both_flagged_conflict")
        pairs = {
            frozenset({c.left_id, c.right_id}): c
            for c in registry.conflicts
        }
        self.assertIn(frozenset({"SFE-H001", "SFE-H002"}), pairs)
        self.assertEqual(
            pairs[frozenset({"SFE-H001", "SFE-H002"})].relation,
            ConflictRelation.INCOMPATIBLE.value,
        )
        e1 = registry.equations["SFE-H001"].original_expression
        e2 = registry.equations["SFE-H002"].original_expression
        self.assertNotEqual(e1, e2)
        hybrid = " ".join([e1, e2])
        self.assertNotIn(hybrid, [eq.original_expression for eq in registry.equations.values()])
        self.assertEqual(registry.canonical_sfe_status(), CANONICAL_SFE_STATUS)


class TestHPrimeComparisonNegative(unittest.TestCase):
    def test_negative_prime_result_is_stored_and_reported(self):
        n = 32
        field = np.zeros(n)
        # Energy on composite / non-prime indices so a prime mask is a poor encoding.
        field[[0, 1, 4, 6, 8, 9, 10, 12]] = 1.0
        lab = run_selector_lab(field, budget=4, random_seeds=(1, 2, 3), include_optimized=True)
        self.assertTrue(lab.negative)
        self.assertIn("worse than the tested random controls", lab.conclusion.lower())
        self.assertNotIn("prime structure is fundamental", lab.conclusion.lower())
        registry = EquationRegistry()
        rec = registry.record_null(
            kind="prime selector failed",
            statement=lab.conclusion,
            evidence=str(lab.metrics),
            source="acceptance Test H",
        )
        self.assertEqual(registry.prominent_nulls()[0].null_id, rec.null_id)
        self.assertIn("worse", registry.prominent_nulls()[0].statement.lower())


class TestLanguageAndScope(unittest.TestCase):
    def test_canonical_sfe_unresolved_on_every_report(self):
        report = audit_expression("Hψ")
        self.assertEqual(report.canonical_sfe_status, CANONICAL_SFE_STATUS)
        self.assertIn("unresolved", report.narrative().lower())

    def test_role_confidence_does_not_imply_physics(self):
        report = audit_expression("∇²Φ = 4π G ρ")
        self.assertEqual(report.confidence.physical_validation_status, "benchmark_representation")
        narrative = report.narrative().lower()
        self.assertIn("does not imply physical validity", narrative)


if __name__ == "__main__":
    unittest.main()
