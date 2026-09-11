#!/usr/bin/env python3
"""Tests: DA refuses unconditional Clay / SND-U and points at the weld."""

from __future__ import annotations

import json
import unittest
from io import StringIO
from unittest import mock

from domain_architect.audit import audit_expression
from domain_architect.cli import main as cli_main
from domain_architect.gap_closure import (
    CLOSURE_CATALOG,
    EXPR_CLAY_GLUE,
    EXPR_NS_B,
    EXPR_SND_C,
    EXPR_SND_U,
    diagnose_gap,
    ranked_top_closures,
    snd_c_vs_snd_u_compare,
)
from domain_architect.registry import EquationRegistry
from domain_architect.schema import ConflictRelation


class TestGapClosureDiagnosis(unittest.TestCase):
    def test_refuses_clay_glue_with_x_le_m(self):
        gap = diagnose_gap(EXPR_CLAY_GLUE)
        self.assertTrue(gap.refuses_unconditional_clay)
        ids = {f.break_id for f in gap.findings}
        self.assertIn("TH-H1", ids)
        text = gap.narrative()
        self.assertIn("Broken weld:", text)
        self.assertIn("Suggested closure:", text)

    def test_refuses_standalone_snd_u(self):
        gap = diagnose_gap(EXPR_SND_U)
        self.assertTrue(gap.refuses_unconditional_clay)
        self.assertTrue(any(f.severity == "refuse" for f in gap.findings))
        line = gap.findings[0].narrative_line()
        self.assertTrue(line.startswith("Broken weld:"))
        self.assertIn("Suggested closure:", line)

    def test_snd_c_alone_is_warn_not_clay_cheer(self):
        gap = diagnose_gap(EXPR_SND_C)
        # Conditional book alone should not green Clay.
        self.assertFalse(gap.refuses_unconditional_clay)
        self.assertEqual(gap.domain_book_hint, "SND-C")

    def test_classical_ns_not_refused(self):
        gap = diagnose_gap(EXPR_NS_B)
        self.assertFalse(gap.refuses_unconditional_clay)
        self.assertEqual(gap.domain_book_hint, "NS-B")

    def test_q1_clay_refused(self):
        gap = diagnose_gap(
            "Q1 hyperdissipative epsilon->0; Clay Statement B resolved via SND"
        )
        self.assertTrue(gap.refuses_unconditional_clay)
        ids = {f.break_id for f in gap.findings}
        self.assertIn("TH-H7-Q1", ids)

    def test_ranked_closures_include_structural_and_analytic(self):
        top = ranked_top_closures(5)
        self.assertEqual(len(top), 5)
        kinds = {m.kind for m in top}
        self.assertIn("structural", kinds)
        self.assertIn("analytic", kinds)
        self.assertEqual(top[0].break_id, "TH-H1")
        analytic = [m for m in top if m.kind == "analytic"]
        self.assertGreaterEqual(len(analytic), 2)

    def test_catalog_headlines_are_closure_shaped(self):
        for m in CLOSURE_CATALOG:
            h = m.headline()
            self.assertIn("Broken at", h)
            self.assertIn("close by", h)
            self.assertNotIn("remains open", h.lower())


class TestSndDualCompare(unittest.TestCase):
    def test_snd_c_vs_u_incompatible(self):
        dual = snd_c_vs_snd_u_compare()
        self.assertEqual(dual["relation"], ConflictRelation.INCOMPATIBLE.value)
        self.assertIn("Broken weld:", dual["narrative"])
        self.assertTrue(dual["right"]["refuses_unconditional_clay"])
        self.assertIn("Split theorems", dual["suggested_closure"])
        self.assertIn("X≤M", dual["why_incompatible"])


class TestInferBookExpressionFirst(unittest.TestCase):
    def test_snd_c_not_flipped_by_snd_u_notes(self):
        from domain_architect.audit import audit_expression
        from domain_architect.gap_closure import EXPR_SND_C
        from domain_architect.hb_loop import build_hb_map, compare_reports

        left = audit_expression(EXPR_NS_B)
        right = audit_expression(EXPR_SND_C)
        cmp = compare_reports(left, right)
        self.assertEqual(cmp.right.domain_book, "SND-C")
        self.assertNotEqual(cmp.right.domain_book, "SND-U")


class TestRegistryConflicts(unittest.TestCase):
    def test_snd_c_clay_incompatible_in_registry(self):
        reg = EquationRegistry.load_default()
        pairs = {
            (c.left_id, c.right_id, c.relation)
            for c in reg.conflicts
        }
        self.assertIn(
            ("SND-C001", "CLAY-B001", ConflictRelation.INCOMPATIBLE.value),
            pairs,
        )
        self.assertIn(
            ("SND-C001", "SND-U001", ConflictRelation.INCOMPATIBLE.value),
            pairs,
        )
        clay = reg.equations["CLAY-B001"]
        self.assertEqual(clay.audit_disposition, "RETIRE")
        snd_u = reg.equations["SND-U001"]
        self.assertEqual(snd_u.audit_disposition, "RETIRE")


class TestAuditAttach(unittest.TestCase):
    def test_audit_attaches_gap_closure_on_glue_claim(self):
        report = audit_expression(EXPR_CLAY_GLUE)
        self.assertIsNotNone(report.gap_closure)
        self.assertTrue(report.gap_closure["refuses_unconditional_clay"])
        blob = " ".join(report.warnings + report.notes).lower()
        self.assertIn("refuse", blob)
        self.assertIn("broken weld", blob)
        # incompleteness candidates include weld closures
        kinds = {c["kind"] for c in report.incompleteness["candidates"]}
        self.assertIn("gap_closure_weld", kinds)


class TestCliGapClosure(unittest.TestCase):
    def test_cli_gap_closure_exit_2_on_refuse(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--gap-closure", EXPR_CLAY_GLUE])
        self.assertEqual(code, 2)
        out = buf.getvalue()
        self.assertIn("Broken weld:", out)
        self.assertIn("Suggested closure:", out)

    def test_cli_gap_closure_exit_0_on_ns(self):
        code = cli_main(["--gap-closure", EXPR_NS_B])
        self.assertEqual(code, 0)

    def test_cli_snd_dual(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--snd-dual"])
        self.assertEqual(code, 0)
        self.assertIn("INCOMPATIBLE", buf.getvalue())

    def test_cli_list_closures(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--list-closures", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(len(payload["closures"]), 5)


class TestSndClaimsIntegration(unittest.TestCase):
    def test_anatomizer_refuses_clay_resolved(self):
        from domain_architect.snd_claims import anatomize_claim

        audit = anatomize_claim("Clay Statement B resolved via Theorem H")
        self.assertTrue(audit.refused)
        self.assertIsNone(audit.allowed_routing)

    def test_cli_snd_claim(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(
                ["--snd-claim", "Clay Statement B resolved via unconditional SND"]
            )
        self.assertEqual(code, 2)
        self.assertIn("REFUSE", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
