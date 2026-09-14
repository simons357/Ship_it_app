#!/usr/bin/env python3
"""Hilbert–Pólya program: role map, circular fills, GUE ≠ identity."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.audit import audit_expression
from domain_architect.hilbert_polya import (
    CIRCULAR_ASSIGNMENT_WARNING,
    GUE_NOT_IDENTITY_WARNING,
    RH_STATUS,
    audit_candidate,
    default_program_audit,
    gue_is_not_riemann_spectrum,
    hamiltonian_is_independent,
    is_circular_fill,
    looks_like_hilbert_polya,
    program_pieces,
    weyl_law_screen,
)
from domain_architect.registry import EquationRegistry
from domain_architect.schema import (
    CANONICAL_SFE_STATUS,
    EvidenceLevel,
    HILBERT_POLYA_STATUS,
    SCOPE_PROHIBITIONS,
)


ROOT = Path(__file__).resolve().parents[1]


class TestCircularFill(unittest.TestCase):
    def test_target_identity_is_circular_and_incomplete(self):
        audit = audit_candidate("target-identity")
        self.assertTrue(audit.circular)
        self.assertFalse(audit.complete)
        self.assertEqual(audit.rh_status, RH_STATUS)
        self.assertIn("not claimed", audit.rh_status)
        self.assertFalse(audit.complete)
        self.assertIn("HP-S0", audit.missing_piece_ids)
        self.assertIn("HP-S5", audit.missing_piece_ids)
        joined = " ".join(audit.warnings)
        self.assertIn("does not specify", joined.lower())
        self.assertIn(CIRCULAR_ASSIGNMENT_WARNING[:40], joined)

    def test_diagonal_zeros_is_circular(self):
        self.assertTrue(
            is_circular_fill(hamiltonian="H = diag(γ_n) on ℓ²")
        )
        audit = audit_candidate("diagonal-zeros")
        self.assertTrue(audit.circular)
        self.assertFalse(hamiltonian_is_independent(audit.core_roles[1].target_occupant))
        h_role = next(r for r in audit.core_roles if r.role == "H")
        self.assertFalse(h_role.independent_of_zeros)

    def test_blank_instance_is_not_a_quantum_system(self):
        audit = audit_candidate("unspecified")
        self.assertFalse(audit.complete)
        self.assertFalse(audit.circular)
        self.assertIn("HP-S0", audit.missing_piece_ids)
        self.assertEqual(audit.hilbert_polya_status, HILBERT_POLYA_STATUS)


class TestBerryKeatingIsIndependentButIncomplete(unittest.TestCase):
    def test_xp_is_independent_and_still_missing_identity(self):
        self.assertTrue(hamiltonian_is_independent("H = xp"))
        audit = audit_candidate("berry-keating")
        self.assertFalse(audit.circular)
        h_role = next(r for r in audit.core_roles if r.role == "H")
        self.assertTrue(h_role.independent_of_zeros)
        self.assertIn("HP-S1", audit.missing_piece_ids)
        self.assertIn("HP-S5", audit.missing_piece_ids)
        self.assertFalse(audit.complete)
        self.assertEqual(audit.rh_status, "not claimed")
        self.assertIn("cutoff", " ".join(audit.notes).lower())


class TestCandidatesStayDistinct(unittest.TestCase):
    def test_berry_keating_not_merged_with_connes(self):
        bk = audit_candidate("berry-keating")
        connes = audit_candidate("connes")
        self.assertNotEqual(bk.core_roles[1].target_occupant, connes.core_roles[1].target_occupant)
        self.assertNotIn("adelic", bk.core_roles[1].target_occupant.lower())
        connes_text = " ".join(
            connes.notes + [r.target_occupant for r in connes.core_roles]
        ).lower()
        self.assertIn("absorption", connes_text)

    def test_weil_is_theorem_not_hamiltonian(self):
        audit = audit_candidate("weil-explicit")
        self.assertFalse(audit.complete)
        self.assertFalse(audit.circular)
        t1 = next(p for p in audit.pieces if p["piece_id"] == "HP-T1")
        self.assertEqual(t1["status"], "theorem")
        self.assertIn("HP-S0", audit.missing_piece_ids)


class TestGueIsNotIdentity(unittest.TestCase):
    def test_random_gue_is_not_the_gamma_sequence(self):
        lab = gue_is_not_riemann_spectrum(seed=0, n=24)
        self.assertFalse(lab["is_riemann_spectrum"])
        self.assertGreater(lab["affine_residual_to_first_gammas"], 0.01)
        self.assertIn("not the zeta operator", lab["conclusion"].lower())

    def test_weyl_screen_rejects_oscillator_not_xp_leading_term(self):
        screen = weyl_law_screen()
        self.assertTrue(screen["oscillator_rejected"])
        self.assertTrue(screen["xp_classical_leading_term_compatible"])
        self.assertLess(screen["spacing_ratio_high_over_low_riemann"], 0.5)
        self.assertGreater(screen["spacing_ratio_high_over_low_oscillator"], 0.99)

    def test_montgomery_candidate_flags_universality(self):
        audit = audit_candidate("montgomery-gue")
        self.assertIsNotNone(audit.gue_laboratory)
        self.assertFalse(audit.gue_laboratory["is_riemann_spectrum"])
        self.assertIn(GUE_NOT_IDENTITY_WARNING, audit.warnings)
        self.assertEqual(
            audit.highest_evidence_level,
            int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY),
        )
        self.assertIn("HP-S5", audit.missing_piece_ids)


class TestPiecesAreIndependentlySpecified(unittest.TestCase):
    def test_expected_piece_ids_exist(self):
        ids = [p.piece_id for p in program_pieces()]
        for needed in (
            "HP-U1",
            "HP-S0",
            "HP-S1",
            "HP-S5",
            "HP-T1",
            "HP-G1",
            "HP-F1",
        ):
            self.assertIn(needed, ids)
        s0 = next(p for p in program_pieces() if p.piece_id == "HP-S0")
        self.assertTrue(s0.independently_tackleable)
        s5 = next(p for p in program_pieces() if p.piece_id == "HP-S5")
        self.assertFalse(s5.independently_tackleable)
        self.assertIn("HP-S1", s5.blocked_on)

    def test_lambda_subtype_is_eigenvalue(self):
        audit = default_program_audit()
        lam = next(r for r in audit.core_roles if r.role == "λ")
        self.assertEqual(lam.scale_subtype, "eigenvalue")
        self.assertEqual(len(audit.core_roles), 5)


class TestExpressionRouting(unittest.TestCase):
    def test_xp_and_riemann_are_routed(self):
        self.assertTrue(looks_like_hilbert_polya("H = xp"))
        self.assertTrue(looks_like_hilbert_polya("Hilbert-Pólya Hamiltonian"))
        report = audit_expression("H = xp")
        narrative = report.narrative().lower()
        self.assertIn("hilbert", narrative)
        self.assertIn("not a construction of h", " ".join(report.warnings).lower())
        self.assertIn("not claimed", " ".join(report.notes).lower())
        self.assertEqual(report.canonical_sfe_status, CANONICAL_SFE_STATUS)
        self.assertLessEqual(
            int(report.highest_evidence_level),
            int(EvidenceLevel.COHERENT_CLASSIFICATION),
        )

    def test_does_not_claim_to_prove_rh(self):
        audit = default_program_audit()
        text = audit.narrative().lower()
        self.assertNotIn("proves the riemann hypothesis", text)
        self.assertIn("not claimed", text)
        self.assertTrue(
            any("filled five-role map proves the riemann" in p.lower() for p in SCOPE_PROHIBITIONS)
        )


class TestRegistryRecords(unittest.TestCase):
    def test_hp_equations_and_nulls_ship(self):
        registry = EquationRegistry.load_default()
        for eq_id in (
            "HP-H001",
            "HP-H002",
            "HP-H003",
            "HP-H004",
            "HP-H005",
            "HP-H006",
            "HP-H007",
            "HP-H008",
            "HP-H009",
            "HP-H010",
        ):
            self.assertIn(eq_id, registry.equations)
        self.assertEqual(registry.equations["HP-H002"].audit_disposition, "RETAIN")
        self.assertEqual(registry.equations["HP-H007"].audit_disposition, "RETIRE")
        self.assertEqual(registry.equations["HP-H003"].audit_disposition, "UNRESOLVED")
        null_ids = {n.null_id for n in registry.nulls}
        self.assertIn("NULL-HP-CIRCULAR", null_ids)
        self.assertIn("NULL-HP-GUE", null_ids)
        self.assertIn("NULL-HP-OSCILLATOR", null_ids)
        pairs = {(c.left_id, c.right_id, c.relation) for c in registry.conflicts}
        self.assertIn(("HP-H003", "HP-H004", "INCOMPATIBLE"), pairs)
        self.assertIn(("HP-H007", "HP-H001", "INCOMPATIBLE"), pairs)
        self.assertIn(("HP-H008", "HP-H003", "COMPATIBLE_DISTINCT"), pairs)

    def test_cli_default_program(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--hilbert-polya"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Circular assignment: True", proc.stdout)
        self.assertIn("Riemann hypothesis status: not claimed", proc.stdout)
        self.assertIn("Canonical SFE status: unresolved", proc.stdout)
        self.assertNotIn("proves the riemann hypothesis", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
