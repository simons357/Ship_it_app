#!/usr/bin/env python3
"""DA-VC-01 fixtures: unaugmented swirl is not a PD plant and not gravity."""

from __future__ import annotations

import unittest
from pathlib import Path

from domain_architect.audit import audit_expression
from domain_architect.schema import CorrespondenceKind
from domain_architect.synthesize import inverse_design_architecture
from domain_architect.translate import translate_expressions

CHALLENGE = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "domain-architect"
    / "DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md"
)
IDENTITY = "(1/r^4)*dz(Gamma^2) = dz(Phi^2)"
INTENSIVE = (
    "dt F + ur*dr F + uz*dz F + 2*(ur/r)*F = "
    "nu*(drr F + (3/r)*dr F + dzz F)"
)


class TestChallenge01Document(unittest.TestCase):
    def test_challenge_file_states_fail_and_open(self):
        text = CHALLENGE.read_text(encoding="utf-8")
        self.assertIn("DA-VC-01", text)
        self.assertIn("Unaugmented", text)
        self.assertIn("FAIL", text)
        self.assertIn("OPEN", text)
        self.assertIn("no hyperviscosity", text)


class TestChallenge01LiveLab(unittest.TestCase):
    def test_identity_is_not_poisson_or_gravity(self):
        payload = audit_expression(IDENTITY).to_dict()
        self.assertEqual(payload["pattern"], "unclassified")
        self.assertIsNone(payload["poisson_compatibility"])
        self.assertIn("gravitational potential", " ".join(payload["warnings"]))

    def test_intensive_field_is_not_oscillator(self):
        payload = audit_expression(INTENSIVE).to_dict()
        self.assertNotEqual(payload["pattern"], "second_order_linear")
        self.assertEqual(payload["pattern"], "unclassified")

    def test_cmb_translate_stays_analogy(self):
        record = translate_expressions(
            IDENTITY,
            "C_ell = quadrupole suppressed at ell = 2",
        )
        self.assertEqual(record.kind, CorrespondenceKind.ANALOGY)
        self.assertIn("no_checked_structure_map", record.broken)

    def test_s1_fail_closes_without_pd_loop(self):
        """A13: inverse design of unaugmented NS must not emit a PD plant.

        DA-VC-01 overall stays FAIL until A5 (declared T) also lands.
        NS-open stays OPEN. Do not treat A13 refuse as a DA-VC-01 pass.
        """
        cand = inverse_design_architecture(
            "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl",
            ["classical NS", "no hyperviscosity", "no (A,W)"],
        )
        self.assertEqual(cand.name, "inverse_design[refused]")
        self.assertIn("will not emit", cand.hypothesis)
        self.assertFalse(
            any("control u" in c for c in cand.components),
            cand.components,
        )
        joined = " ".join(cand.components + [cand.hypothesis] + cand.notes).lower()
        self.assertIn("strain", joined)
        self.assertIn("not claimed", joined)
        self.assertNotIn("clay is claimed", joined)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
