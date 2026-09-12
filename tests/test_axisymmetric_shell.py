#!/usr/bin/env python3
"""Axisymmetric-with-swirl shell estimate: remainder Tjj stays OPEN."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from domain_architect.app import handle_api
from domain_architect.audit import audit_expression
from domain_architect.axisymmetric_shell import (
    DISCARD_CLAIM_PHRASES,
    THREE_D_FACTS,
    TWO_D_FACTS,
    axisymmetric_shell_estimate,
    closed_triad_rewrite,
    contains_discard_claim,
    cycle_axisymmetric_shell,
    pairing_closed,
    pairing_residual,
)
from domain_architect.lab_cases import SHELL_REMAINDER_LAB, SWIRL_LEFTOVER_LAB
from domain_architect.pipeline import run_named_cycle
from domain_architect.schema import CorrespondenceKind, ValidationGate
from domain_architect.translate import translate_expressions


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "domain-architect" / "AXISYMMETRIC-SHELL-AUDIT.md"
ESTIMATE = ROOT / "docs" / "papers" / "swirl" / "AXISYMMETRIC-SHELL-ESTIMATE.md"


class TestAuditDocuments(unittest.TestCase):
    def test_filter_opens_with_class_quantity_remainder(self):
        text = AUDIT.read_text(encoding="utf-8")
        self.assertIn("Class / quantity / remainder / assumed", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("KEEP", text)
        self.assertIn("DISCARD", text)
        self.assertIn("PARK", text)
        self.assertIn("must not be used in the estimate", text)
        self.assertIn("2026-09-12", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("“Clay is solved,”", text)
        self.assertIn("DISCARD", text)

    def test_estimate_first_sentence_and_gap(self):
        text = ESTIMATE.read_text(encoding="utf-8")
        first = text.splitlines()
        joined = "\n".join(first[:20])
        self.assertIn("unaugmented axisymmetric", joined.lower())
        self.assertIn("Z_j", joined)
        self.assertIn("T_{j\\leftarrow j}", joined)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("2-D", text)
        self.assertIn("3-D", text)
        self.assertIn("do not import 2-d", text.lower())
        self.assertIn("not claimed", text.lower())
        self.assertNotIn("unconditional 3-d regularity is claimed", text.lower())
        for phrase in (
            "E8 cathedral",
            "GCD spectral attractor",
            "Base 44 / gematria",
            "Q6-Kabbalah",
            "Lightning Flash",
        ):
            self.assertNotIn(phrase, text.split("## 7.")[0] if "## 7." in text else text)


class TestPairingAndFacts(unittest.TestCase):
    def test_closed_pairing_residual_is_machine_epsilon(self):
        self.assertLessEqual(pairing_residual(0.25, -0.10, -0.15), 1e-16)
        self.assertTrue(pairing_closed(0.25, -0.10, -0.15))
        self.assertFalse(pairing_closed(0.25, -0.10, 0.0))

    def test_open_pairing_refuses_lambda_sign(self):
        payload = axisymmetric_shell_estimate(jp=1.0, jq=1.0, jr=1.0)
        self.assertFalse(payload["pairing"]["closed"])
        self.assertIsNone(payload["bookkeeping"]["value"])
        self.assertFalse(payload["bookkeeping"]["sign_quoted"])

    def test_closed_triad_rewrite_and_lattice_shift(self):
        tau = closed_triad_rewrite(3.0, 1.0, 0.0, 0.25, -0.10)
        self.assertAlmostEqual(tau, (3.0 - 0.0) * 0.25 + (1.0 - 0.0) * (-0.10))

    def test_facts_are_labeled_by_dimension(self):
        self.assertEqual(TWO_D_FACTS["class"], "2-D")
        self.assertFalse(TWO_D_FACTS["imported_to_3d"])
        self.assertEqual(THREE_D_FACTS["class"], "3-D")
        self.assertFalse(THREE_D_FACTS["occupancy_imported_to_cfm"])
        payload = axisymmetric_shell_estimate()
        self.assertEqual(payload["measured_facts"]["2d"]["class"], "2-D")
        self.assertEqual(payload["measured_facts"]["3d"]["class"], "3-D")
        self.assertFalse(payload["measured_facts"]["2d"]["imported_to_3d"])

    def test_discard_phrases_are_not_claimed_closes(self):
        payload = axisymmetric_shell_estimate()
        blob = json.dumps(payload).lower()
        self.assertNotIn("clay is solved", blob)
        self.assertNotIn("tao certification", blob)
        self.assertEqual(payload["clay"], "NOT CLAIMED")
        self.assertEqual(payload["unconditional_3d_regularity"], "NOT CLAIMED")
        self.assertEqual(payload["status"], "OPEN")
        self.assertTrue(contains_discard_claim("Clay is solved"))
        self.assertFalse(contains_discard_claim(payload["first_sentence"]))


class TestDecomposeAndGlue(unittest.TestCase):
    def test_lab_string_warns_open_remainder(self):
        report = audit_expression(SHELL_REMAINDER_LAB).to_dict()
        self.assertEqual(report["pattern"], "unclassified")
        joined = " ".join(report["warnings"])
        self.assertIn("T_{j←j}", joined)
        self.assertIn("OPEN", joined)
        self.assertIn("NOT CLAIMED", joined)
        self.assertNotIn("TRANSFORMABLE", joined)

    def test_strain_vs_shell_refuses_map(self):
        record = translate_expressions(SWIRL_LEFTOVER_LAB, SHELL_REMAINDER_LAB)
        self.assertEqual(record.kind, CorrespondenceKind.ANALOGY)
        self.assertEqual(record.mapping, {})
        self.assertIn("no_checked_structure_map", record.broken)


class TestCycleAndApi(unittest.TestCase):
    def test_cycle_stays_open(self):
        report = cycle_axisymmetric_shell()
        self.assertEqual(report.mode, "axisymmetric-shell")
        self.assertEqual(report.validation_gate, ValidationGate.MATHEMATICAL)
        self.assertEqual(report.candidate.name, "axisymmetric_shell_open")
        self.assertEqual(report.prediction["status"], "OPEN")
        self.assertEqual(report.prediction["clay"], "NOT CLAIMED")
        self.assertEqual(report.prediction["remainder"], "T_{j←j}")
        blob = json.dumps(report.to_dict()).lower()
        self.assertNotIn("control u = k", blob)
        self.assertNotIn("clay is solved", blob)

    def test_named_cycle_and_api(self):
        named = run_named_cycle("axisymmetric-shell")
        self.assertEqual(named.mode, "axisymmetric-shell")
        alias = run_named_cycle("tjj")
        self.assertEqual(alias.prediction["remainder"], "T_{j←j}")
        status, body, _ = handle_api("/api/axisymmetric-shell", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["protocol"], "axisymmetric-shell")
        self.assertEqual(payload["status"], "OPEN")
        status, body, _ = handle_api("/api/cycle", {"name": "axisymmetric-shell"})
        self.assertEqual(status, 200)
        cycle = json.loads(body)
        self.assertEqual(cycle["mode"], "axisymmetric-shell")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
