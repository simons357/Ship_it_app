#!/usr/bin/env python3
"""Incompleteness, drill-down, and dual-SFE compare tests."""

from __future__ import annotations

import unittest

from domain_architect.audit import audit_expression
from domain_architect.cli import main as cli_main
from domain_architect.decompose import decompose_report
from domain_architect.incompleteness import analyze_incompleteness, sketch_from_roles
from domain_architect.schema import CANONICAL_SFE_STATUS
from domain_architect.sfe_compare import compare_sfe_pair, list_sfe_candidates


class TestIncompleteness(unittest.TestCase):
    def test_thin_ns_flags_missing_advection(self):
        report = audit_expression("partial_t omega = nu Delta omega")
        self.assertIsNotNone(report.incompleteness)
        inc = report.incompleteness
        self.assertEqual(inc["domain_book"], "NS-B")
        self.assertIn("advection_or_stretch_term", inc["missing_terms"])
        kinds = {c["kind"] for c in inc["candidates"]}
        self.assertIn("missing_term", kinds)
        joined = " ".join(c["honesty_note"] for c in inc["candidates"]).lower()
        self.assertIn("clay", joined)

    def test_full_ns_role_complete(self):
        report = audit_expression(
            "partial_t omega = (omega * nabla) u + nu Delta omega"
        )
        # Roles complete; may still soft-flag explicit incompressibility.
        self.assertFalse(report.incompleteness["missing_roles"])
        self.assertTrue(report.incompleteness["present_roles"])

    def test_roles_to_sketch(self):
        inc = sketch_from_roles(
            [
                "admissibility",
                "interaction",
                "state",
                "scale_response",
                "realized_output",
                "environment",
            ],
            book="NS-B",
        )
        self.assertTrue(inc.is_complete)
        self.assertIn("ν", inc.equation_sketch or inc.candidates[0].proposal)
        self.assertEqual(inc.canonical_sfe_status, CANONICAL_SFE_STATUS)

    def test_cli_incompleteness_json(self):
        code = cli_main(
            ["--incompleteness-json", "partial_t omega = nu Delta omega"]
        )
        self.assertEqual(code, 0)


class TestDecompose(unittest.TestCase):
    def test_ns_drilldown_recompose(self):
        report = audit_expression(
            "partial_t omega = (omega * nabla) u + nu Delta omega"
        )
        self.assertIsNotNone(report.decomposition)
        dec = report.decomposition
        self.assertEqual(dec["domain_book"], "NS-B")
        self.assertTrue(dec["all_recompose_ok"])
        self.assertGreaterEqual(dec["depth"], 3)
        self.assertGreater(dec["terminal_count"], 5)
        # Stop reasons exist on leaves
        root = dec["root"]
        stops = []

        def walk(n):
            if n.get("kind") == "terminal":
                stops.append(n.get("stop_reason"))
            for c in n.get("children") or []:
                walk(c)

        walk(root)
        self.assertTrue(any(stops))
        self.assertTrue(
            any(
                s in stops
                for s in (
                    "standard_operator",
                    "measurable_scalar",
                    "measurable_field",
                    "defined_operator",
                )
            )
        )

    def test_gravity_drilldown(self):
        report = audit_expression("nabla^2 Phi = 4 pi G rho")
        dec = decompose_report(report)
        self.assertEqual(dec.domain_book, "gravity-poisson")
        self.assertTrue(dec.all_recompose_ok)
        narrative = dec.narrative().lower()
        self.assertIn("drill-down", narrative)
        self.assertIn("not a pde solve", narrative)

    def test_cli_decompose_json(self):
        code = cli_main(["--decompose-json", "nabla^2 Phi = 4 pi G rho"])
        self.assertEqual(code, 0)


class TestSFEDual(unittest.TestCase):
    def test_list_sfe(self):
        items = list_sfe_candidates()
        ids = {i["equation_id"] for i in items}
        self.assertIn("SFE-H001", ids)
        self.assertIn("SFE-H002", ids)

    def test_put_sfe_in_twice_distinct(self):
        dual = compare_sfe_pair("SFE-H001", "SFE-H002", include_audits=False)
        self.assertEqual(dual.canonical_sfe_status, CANONICAL_SFE_STATUS)
        self.assertFalse(dual.same_expression)
        self.assertEqual(dual.registry_relation, "INCOMPATIBLE")
        text = dual.narrative().lower()
        self.assertIn("unresolved", text)
        self.assertIn("hybrid", text)
        self.assertNotIn("canonical sfe is", text)

    def test_same_sfe_twice(self):
        dual = compare_sfe_pair("SFE-H001", "SFE-H001", include_audits=False)
        self.assertTrue(dual.same_expression)
        self.assertEqual(dual.registry_relation, "IDENTICAL")
        self.assertEqual(dual.canonical_sfe_status, CANONICAL_SFE_STATUS)

    def test_cli_sfe_compare(self):
        code = cli_main(["--sfe-compare", "SFE-H001", "SFE-H002"])
        self.assertEqual(code, 0)

    def test_cli_list_sfe(self):
        code = cli_main(["--list-sfe"])
        self.assertEqual(code, 0)


class TestNoForbiddenClaims(unittest.TestCase):
    def test_audit_notes_stay_honest(self):
        report = audit_expression(
            "partial_t omega = (omega * nabla) u + nu Delta omega"
        )
        blob = report.narrative().lower()
        # Negated disclaimers are OK; positive forbidden claims are not.
        self.assertIn("not a theory of everything", blob)
        self.assertNotIn("proves regularity", blob)
        self.assertNotIn("canonical sfe is resolved", blob)
        self.assertIn("unresolved", blob)


if __name__ == "__main__":
    unittest.main()
