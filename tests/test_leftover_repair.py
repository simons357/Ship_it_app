#!/usr/bin/env python3
"""Usable Ring SND and Q6 H_N sit side by side. Leftovers stay un-glued."""

from __future__ import annotations

import json
import unittest

from domain_architect.app import handle_api
from domain_architect.audit import audit_expression
from domain_architect.lab_cases import (
    NS_LEFTOVERS,
    Q6_HN_LAB,
    RING_SND_LAB,
    SIMPLEX_LEFTOVER_LAB,
    SWIRL_LEFTOVER_LAB,
)
from domain_architect.leftover_repair import cycle_leftover_repair, leftover_repair
from domain_architect.parser import NodeKind, parse_expression, tokenize
from domain_architect.pipeline import run_named_cycle
from domain_architect.schema import CorrespondenceKind, ValidationGate
from domain_architect.synthesize import inverse_design_architecture
from domain_architect.translate import snd_vs_h_translation, translate_expressions


class TestParserLabStrings(unittest.TestCase):
    def test_qtilde_and_cstar_stay_atomic(self):
        self.assertEqual(tokenize("Qtilde"), ["Qtilde"])
        self.assertEqual(tokenize("cstar"), ["cstar"])
        self.assertEqual(tokenize("HN"), ["HN"])
        self.assertEqual(tokenize("urad"), ["urad"])

    def test_snd_inequality_parses(self):
        parsed = parse_expression(RING_SND_LAB)
        self.assertTrue(parsed.ok)
        self.assertEqual(parsed.tree.kind, NodeKind.EQUALITY)
        self.assertEqual(parsed.tree.name, ">=")
        self.assertEqual(parsed.tokens, ["J", "/", "X", ">=", "cstar"])

    def test_hn_power_is_not_divide_by_two(self):
        parsed = parse_expression(Q6_HN_LAB)
        self.assertTrue(parsed.ok)
        pows = [n for n in parsed.tree.walk() if n.kind == NodeKind.POW]
        self.assertGreaterEqual(len(pows), 2)
        self.assertIn("Qtilde", parsed.tokens)
        self.assertNotIn("tilde", parsed.tokens)


class TestDecomposeUsableEquations(unittest.TestCase):
    def test_ring_snd_is_unclassified_with_book_warning(self):
        report = audit_expression(RING_SND_LAB).to_dict()
        self.assertEqual(report["pattern"], "unclassified")
        self.assertEqual(report["highest_evidence_level"], 0)
        joined = " ".join(report["warnings"])
        self.assertIn("Ring-book SND", joined)
        self.assertIn("not Paper2", joined)
        self.assertIn("not GNC", joined)
        self.assertNotIn("TRANSFORMABLE", joined)

    def test_q6_hn_is_unclassified_with_definition_warning(self):
        report = audit_expression(Q6_HN_LAB).to_dict()
        self.assertEqual(report["pattern"], "unclassified")
        joined = " ".join(report["warnings"])
        self.assertIn("Q6 definition", joined)
        self.assertIn("not FRA coupling", joined)
        self.assertIn("withdrawn", joined)
        self.assertIn("degree matrix", joined)

    def test_swirl_and_simplex_leftovers_are_named(self):
        swirl = " ".join(audit_expression(SWIRL_LEFTOVER_LAB).to_dict()["warnings"])
        simplex = " ".join(audit_expression(SIMPLEX_LEFTOVER_LAB).to_dict()["warnings"])
        self.assertIn("swirl leftover", swirl)
        self.assertIn("Paper2 leftover", simplex)


class TestSndVsHSideBySide(unittest.TestCase):
    def test_translate_refuses_letter_map(self):
        record = snd_vs_h_translation()
        self.assertEqual(record.kind, CorrespondenceKind.ANALOGY)
        self.assertEqual(record.mapping, {})
        self.assertIn("no_checked_structure_map", record.broken)
        self.assertIn("different_books", record.broken)
        self.assertLess(record.confidence, 0.5)
        joined = " ".join(record.notes)
        self.assertIn("does not glue", joined.lower())
        self.assertNotIn("TRANSFORMABLE", joined)
        self.assertNotEqual(record.mapping.get("J"), "HN")

    def test_api_translate_with_both_fields_is_not_mechanical(self):
        status, body, _ = handle_api(
            "/api/translate",
            {"left": RING_SND_LAB, "right": Q6_HN_LAB},
        )
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["kind"], "analogy")
        self.assertEqual(payload["mapping"], {})
        self.assertNotIn("m", payload["mapping"])

    def test_leftover_pair_also_refuses_map(self):
        record = translate_expressions(SWIRL_LEFTOVER_LAB, RING_SND_LAB)
        self.assertEqual(record.mapping, {})
        self.assertEqual(record.kind, CorrespondenceKind.ANALOGY)


class TestLeftoverRepairProtocol(unittest.TestCase):
    def test_three_open_pieces_and_conditional_put_back(self):
        payload = leftover_repair()
        self.assertEqual(payload["protocol"], "leftover-split")
        self.assertEqual(len(payload["pieces"]), 3)
        self.assertEqual(len(NS_LEFTOVERS), 3)
        ids = [p["id"] for p in payload["pieces"]]
        self.assertEqual(ids, ["swirl-strain", "ring-snd", "paper2-simplex"])
        self.assertTrue(all(p["status"] == "OPEN" for p in payload["pieces"]))
        self.assertFalse(payload["reconstruction"]["closed"])
        self.assertEqual(payload["kind"], "analogy")
        re_embed = payload["re_embed"]
        self.assertEqual(len(re_embed), 3)
        self.assertTrue(all(row["status"] == "OPEN" for row in re_embed))
        paper2 = next(row for row in re_embed if row["id"] == "paper2-simplex")
        self.assertIn("Lemma 6.1", paper2["put_back"])
        self.assertIn("T2 Closed", paper2["put_back"])
        joined = " ".join(payload["refused"]).lower()
        self.assertIn("pd", joined)
        self.assertIn("clay", joined)

    def test_cycle_does_not_emit_pd_loop(self):
        report = cycle_leftover_repair()
        self.assertEqual(report.validation_gate, ValidationGate.MATHEMATICAL)
        self.assertEqual(report.candidate.name, "leftover_split_conditional")
        blob = json.dumps(report.to_dict()).lower()
        self.assertNotIn("control u = k", blob)
        self.assertIn("leftover-split", blob)
        self.assertIn("open", blob)
        self.assertEqual(report.translation.kind, CorrespondenceKind.ANALOGY)
        self.assertEqual(report.translation.mapping, {})
        self.assertFalse(
            any(
                getattr(c, "verdict", None)
                and c.verdict.value == "TRANSFORMABLE"
                for c in report.translation.compatibility
            )
        )

    def test_named_cycle_alias(self):
        report = run_named_cycle("leftover-repair")
        self.assertEqual(report.mode, "leftover-repair")
        self.assertIsNotNone(report.prediction)
        self.assertEqual(report.prediction["protocol"], "leftover-split")

    def test_api_leftover_repair(self):
        status, body, _ = handle_api("/api/leftover-repair", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(len(payload["pieces"]), 3)
        self.assertEqual(payload["snd_vs_h"]["translation"]["mapping"], {})

    def test_inverse_design_of_ns_is_still_the_a13_hole(self):
        """Leftover repair must not silently 'fix' A13 by rewriting inverse design."""
        cand = inverse_design_architecture(
            "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl",
            ["classical NS"],
        )
        self.assertTrue(any("control u" in c for c in cand.components))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
