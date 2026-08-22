#!/usr/bin/env python3
"""Auto role assignment + tuning export checks."""

from __future__ import annotations

import json
import unittest
from io import StringIO
from unittest import mock

from domain_architect.audit import audit_expression
from domain_architect.cli import main as cli_main
from domain_architect.tuning_export import build_tuning_export


class TestAutoTuningExport(unittest.TestCase):
    def test_gravity_auto_and_controls(self):
        report = audit_expression("nabla^2 Phi = 4 pi G rho")
        self.assertIsNotNone(report.tuning_export)
        self.assertTrue(report.tuning_export["auto_assigned"])
        names = {c["name"] for c in report.tuning_export["controls"]}
        self.assertIn("P", names)
        self.assertTrue(
            any("rho" in n.lower() or n == "rho / S" for n in names)
        )
        narrative = report.narrative().lower()
        self.assertIn("auto tuning export", narrative)
        self.assertIn("bridge", narrative)

    def test_ns_auto_viscosity_control(self):
        report = audit_expression(
            "partial_t omega = (omega * nabla) u + nu Delta omega"
        )
        te = build_tuning_export(report)
        self.assertTrue(te.auto_assigned)
        self.assertEqual(te.domain_book, "NS-B")
        free = {c.name for c in te.controls if c.status == "free"}
        self.assertIn("nu", free)
        self.assertTrue(
            any("Leray" in f or "div-free" in f for f in te.fixed_structure)
        )

    def test_generic_refuses_name_only(self):
        report = audit_expression("H psi")
        te = build_tuning_export(report)
        self.assertFalse(te.auto_assigned)
        self.assertEqual(te.domain_book, "generic")

    def test_cli_tuning_json(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(
                ["--tuning-json", "nabla^2 Phi = 4 pi G rho"]
            )
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["auto_assigned"])
        self.assertEqual(payload["domain_book"], "gravity-poisson")


if __name__ == "__main__":
    unittest.main()
