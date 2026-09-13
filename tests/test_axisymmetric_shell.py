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
    MIXED_SPLIT_SAMPLES,
    REFUSED_YOUNG,
    THREE_D_FACTS,
    TWO_D_FACTS,
    axisymmetric_shell_estimate,
    claim_tripwire_hits,
    closed_triad_rewrite,
    contains_discard_claim,
    cycle_axisymmetric_shell,
    format_shell_diagnostic,
    pairing_closed,
    pairing_residual,
    shell_diagnostic,
    swirl_split_residual,
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
            self.assertNotIn(
                phrase,
                text.split("What this note refuses")[0]
                if "What this note refuses" in text
                else text,
            )
        self.assertIn("NOT COMPUTED", text)
        self.assertIn("no DNS", text)
        identity_and_measure = (
            text.split("What this note refuses")[0]
            if "What this note refuses" in text
            else text
        )
        self.assertEqual(claim_tripwire_hits(identity_and_measure), [])
        self.assertNotIn("we close", identity_and_measure.lower())
        self.assertNotIn("small leftover", identity_and_measure.lower())
        self.assertNotIn("T_{j\\leftarrow j} is O(", identity_and_measure)
        self.assertIn("REFUSED", text)
        self.assertIn("not dns", text.lower())
        self.assertIn("T^{\\mathrm{mm}}", text)
        self.assertIn("spectral-shift identity", text.lower())
        self.assertIn("not an absorption criterion", text.lower())
        self.assertIn("k_{\\max}", text.lower())
        self.assertIn("candidate routes", text.lower())
        self.assertNotIn("depletion established", text.lower())
        self.assertIn("energy \\(z_j=", text.lower())
        self.assertIn("enstrophy", text.lower())

    def test_estimate_writes_exact_pairing(self):
        text = ESTIMATE.read_text(encoding="utf-8")
        self.assertIn("P_j(u\\cdot\\nabla u)", text)
        self.assertIn("T_{j\\leftarrow \\ell m}", text)
        self.assertIn("locality width", text.lower())
        self.assertIn("The one term that can grow the quantity", text)


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
        self.assertEqual(payload["remainder"], "T_{j←j}")
        self.assertEqual(payload["da_vc_01"], "FAIL")
        self.assertTrue(contains_discard_claim("Clay is solved"))
        self.assertFalse(contains_discard_claim(payload["first_sentence"]))
        self.assertEqual(claim_tripwire_hits(payload["first_sentence"]), [])
        self.assertEqual(
            claim_tripwire_hits(json.dumps(payload["identity"])),
            [],
        )

    def test_closed_pairing_without_time_series_does_not_quote_lambda(self):
        payload = axisymmetric_shell_estimate()
        self.assertTrue(payload["pairing"]["closed"])
        self.assertLessEqual(payload["pairing"]["residual"], 1e-16)
        self.assertFalse(payload["bookkeeping"]["time_series_closed"])
        self.assertIsNone(payload["bookkeeping"]["value"])
        self.assertFalse(payload["bookkeeping"]["sign_quoted"])

    def test_two_d_ratio_is_not_a_three_d_close(self):
        payload = axisymmetric_shell_estimate()
        three = payload["measured_facts"]["3d"]
        self.assertNotIn("adversary_|Tc|/Ds", three)
        self.assertNotEqual(three.get("random_phase_ratio"), 0.017)
        self.assertFalse(payload["measured_facts"]["2d"]["imported_to_3d"])
        self.assertFalse(three["occupancy_imported_to_cfm"])

    def test_identity_residual_gate_and_open_leftover(self):
        diag = shell_diagnostic()
        self.assertTrue(diag["pairing"]["closed_triad_closed"])
        self.assertLessEqual(diag["pairing"]["closed_triad_residual"], 1e-16)
        self.assertFalse(diag["pairing"]["broken_triad_closed"])
        self.assertGreater(diag["pairing"]["broken_triad_residual"], 1e-16)
        self.assertEqual(diag["tjj_over_zj"]["status"], "NOT COMPUTED")
        self.assertEqual(diag["remainder_status"], "OPEN")
        self.assertEqual(diag["lambda_prime_sign"], "NOT QUOTED")
        self.assertEqual(diag["clay"], "NOT CLAIMED")
        self.assertEqual(diag["da_vc_01"], "FAIL")
        printed = format_shell_diagnostic(diag)
        self.assertIn("NOT COMPUTED", printed)
        self.assertIn("2-D recorded", printed)
        self.assertIn("0.017", printed)
        self.assertIn("3-D recorded", printed)
        self.assertIn("NOT QUOTED", printed)
        self.assertIn("OPEN", printed)
        self.assertNotIn("Clay is solved", printed)
        self.assertEqual(claim_tripwire_hits(printed), [])
        self.assertIn("NOT COMPUTED", " ".join(audit_expression(SHELL_REMAINDER_LAB).warnings))

    def test_refused_young_is_not_a_close(self):
        self.assertEqual(REFUSED_YOUNG["status"], "REFUSED")
        payload = axisymmetric_shell_estimate()
        self.assertEqual(payload["refused_young"]["status"], "REFUSED")
        self.assertEqual(payload["status"], "OPEN")
        self.assertEqual(payload["tjj_over_zj"]["status"], "NOT COMPUTED")
        printed = format_shell_diagnostic()
        self.assertIn("REFUSED", printed)
        self.assertNotIn("requested local Young is seated", printed.lower())

    def test_tjj_chain_facts_are_labeled(self):
        payload = axisymmetric_shell_estimate()
        samples = payload["measured_facts"]["compact_swirl_samples"]
        self.assertEqual(samples["kind"], "named compact samples, not DNS, not a class bound")
        self.assertFalse(samples["imported_from_2d"])
        self.assertFalse(samples["imported_to_3d_cfm"])
        self.assertAlmostEqual(samples["mixed_m1_n32_max_|Tjj/Xj|"], 0.00112)
        self.assertLess(samples["pure_swirl_n32_max_|Tjj/Xj|"], 1e-18)
        split = payload["measured_facts"]["mixed_split_samples"]
        self.assertTrue(split["T_mm_is_the_bulk"])
        self.assertFalse(split["centrifugal_only_leftover"])
        self.assertIn("n=24", split["class"])
        exact = swirl_split_residual(8.0, -1.0, 0.5, 7.5)
        self.assertLessEqual(exact, 1e-16)
        rounded = MIXED_SPLIT_SAMPLES["shells"][0]
        self.assertGreater(
            swirl_split_residual(
                rounded["T_mm"], rounded["T_ss"], rounded["T_cross"], rounded["Tjj"]
            ),
            1.0,
        )
        printed = format_shell_diagnostic()
        self.assertIn("not DNS", printed)
        self.assertIn("T_mm is the bulk", printed)

    def test_standing_language_refuses_false_closes(self):
        payload = axisymmetric_shell_estimate()
        standing = payload["standing_language"]
        self.assertFalse(standing["identity_is_lemma_star"])
        self.assertFalse(standing["rho_j_lt_nu_is_energy_absorption"])
        self.assertFalse(standing["occupancy_alpha_is_depletion"])
        self.assertEqual(standing["principal_unresolved"], "T_{j←j}")
        self.assertEqual(standing["routes_A_B_C"], "candidate routes, not theorems")
        self.assertFalse(payload["closed_triad"]["is_lemma_star"])
        self.assertFalse(payload["closed_triad"]["controls_nonlinear_transfer"])
        self.assertFalse(payload["shells_labeled"]["glued"])
        self.assertIn("LP projector", payload["shells_labeled"]["energy"])
        self.assertIn("palinstrophy", payload["shells_labeled"]["palinstrophy"])
        self.assertFalse(payload["measured_facts"]["3d"]["occupancy_alpha_is_depletion"])
        self.assertFalse(payload["measured_facts"]["compact_swirl_samples"]["kmax_to_infinity"])
        self.assertFalse(payload["measured_facts"]["compact_swirl_samples"]["generic_data"])
        self.assertEqual(payload["status"], "OPEN")
        printed = format_shell_diagnostic()
        self.assertIn("not Lemma-star", printed)
        self.assertIn("not energy-budget absorption", printed)
        self.assertIn("does not establish depletion", printed)
        self.assertIn("candidate routes, not theorems", printed)
        self.assertNotIn("depletion established", printed.lower())
        self.assertTrue(contains_discard_claim("depletion established"))
        self.assertFalse(contains_discard_claim(printed))


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
        self.assertEqual(report.prediction["tjj_over_zj"]["status"], "NOT COMPUTED")
        self.assertEqual(report.prediction["da_vc_01"], "FAIL")
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
