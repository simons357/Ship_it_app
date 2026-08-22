#!/usr/bin/env python3
"""HB loop: map → reconstruct → compare."""

from __future__ import annotations

import unittest

from domain_architect.audit import audit_expression
from domain_architect.cli import main as cli_main
from domain_architect.hb_loop import check_reconstruction, compare_reports


class TestReconstruction(unittest.TestCase):
    def test_ns_inventory_reconstructs(self):
        report = audit_expression(
            "partial_t omega = (omega * nabla) u + nu Delta omega"
        )
        self.assertIsNotNone(report.reconstruction)
        self.assertTrue(report.reconstruction["passed"])
        self.assertEqual(report.hb_map["domain_book"], "NS-B")
        self.assertIn("reconstruct", " ".join(report.notes).lower())

    def test_gravity_representation_reconstructs(self):
        report = audit_expression("nabla^2 Phi = 4 pi G rho")
        recon = check_reconstruction(report)
        self.assertTrue(recon.passed)
        self.assertEqual(recon.kind, "representation_recovery")


class TestCompare(unittest.TestCase):
    def test_ns_vs_gravity_side_by_side(self):
        left = audit_expression(
            "partial_t omega = (omega * nabla) u + nu Delta omega"
        )
        right = audit_expression("nabla^2 Phi = 4 pi G rho")
        cmp = compare_reports(left, right)
        self.assertEqual(cmp.left.domain_book, "NS-B")
        self.assertEqual(cmp.right.domain_book, "gravity-poisson")
        self.assertTrue(
            any("different domain books" in w.lower() for w in cmp.why_not_working)
        )
        narrative = cmp.narrative().lower()
        self.assertIn("shared roles", narrative)
        self.assertIn("new physics", narrative)

    def test_cli_compare(self):
        code = cli_main(
            [
                "--compare",
                "partial_t omega = nu Delta omega",
                "nabla^2 Phi = 4 pi G rho",
            ]
        )
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
