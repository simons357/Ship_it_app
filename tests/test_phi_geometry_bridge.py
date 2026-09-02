#!/usr/bin/env python3
"""Swirl Phi is algebra in one PDE. Cosmic identifications stay analogy."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from domain_architect.audit import audit_expression
from domain_architect.schema import CorrespondenceKind
from domain_architect.translate import translate_expressions

SWIRL = Path(__file__).resolve().parents[1] / "docs" / "papers" / "swirl"
IDENTITY = "(1/r^4)*dz(Gamma^2) = dz(Phi^2)"


class TestPhiGeometryBridgeFiles(unittest.TestCase):
    def test_essay_and_da_reading_exist(self):
        essay = (SWIRL / "PHI_GEOMETRY_BRIDGE.md").read_text(encoding="utf-8")
        reading = (SWIRL / "DA-ON-PHI-GEOMETRY.md").read_text(encoding="utf-8")
        self.assertIn("Phi-Renormalization as Universal Geometry", essay)
        self.assertIn("not physical equivalence", reading)
        self.assertIn("refused", reading.lower())

    def test_older_swirl_faces_are_not_the_22_aug_compile(self):
        faces = (SWIRL / "FACES.md").read_text(encoding="utf-8")
        self.assertIn("not a compile of 22 august", faces.lower())
        controlling = SWIRL / "Simons_PhiRenorm_Swirl_2026-08-22.tex"
        digest = hashlib.sha256(controlling.read_bytes()).hexdigest()
        self.assertEqual(
            digest,
            "eec7aa57b32ac4d87378b6029fa8e0ea68f8cb9c4925c73a06b7841283a89c35",
        )
        june = SWIRL / "Simons_PhiRenorm_Swirl_2026-06-30.pdf"
        self.assertNotEqual(june.read_bytes(), controlling.read_bytes())


class TestSwirlIdentityIsNotGravityOrCosmos(unittest.TestCase):
    def test_decompose_does_not_make_phi_gravity(self):
        payload = audit_expression(IDENTITY).to_dict()
        self.assertEqual(payload["pattern"], "unclassified")
        self.assertEqual(payload["highest_evidence_level"], 0)
        warnings = " ".join(payload["warnings"])
        self.assertIn("gravitational potential", warnings)
        self.assertIsNone(payload["poisson_compatibility"])
        self.assertIsNone(payload["recovery_kind"])

    def test_translate_to_cmb_language_is_analogy_not_identity(self):
        record = translate_expressions(
            IDENTITY,
            "C_ell = quadrupole suppressed at ell = 2",
        )
        self.assertEqual(record.kind, CorrespondenceKind.ANALOGY)
        self.assertLess(record.confidence, 0.5)
        self.assertIn("no_checked_structure_map", record.broken)

    def test_translate_definition_is_not_structure_map(self):
        record = translate_expressions(IDENTITY, "Phi = Gamma / r^2")
        self.assertEqual(record.kind, CorrespondenceKind.ANALOGY)
        self.assertIn("no_checked_structure_map", record.broken)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
