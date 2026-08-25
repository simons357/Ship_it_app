#!/usr/bin/env python3
"""The live Domain Architect path must not revive SFE or HB."""

from __future__ import annotations

import ast
import hashlib
import unittest
from pathlib import Path

from domain_architect.app import handle_api
from domain_architect.audit import audit_expression
from domain_architect.compatibility import Transformation
from domain_architect.decompose import decompose
from domain_architect.realization import realize_second_order
from domain_architect.translate import mechanical_electrical_translation


LIVE_FORBIDDEN = (
    "canonical sfe",
    "simons field equation",
    "unified harmonic framework",
    "harmonic blueprint",
    "uhf",
    "dhfa",
)

LIVE_ROOT = Path(__file__).resolve().parents[1] / "domain_architect"
ARCHIVE_QSTACK = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "archive"
    / "qstack"
    / "qstack_regularity_paper.pdf"
)
QSTACK_SHA256 = (
    "3ea9a93ac39d35e773f550c12b6f1e643f6fd65247ccf9b094d108789e7f96e8"
)


class TestLivePathDropsSfeHb(unittest.TestCase):
    def test_oscillator_report_is_domain_architect(self):
        report = audit_expression("m*xdd + c*xd + k*x = f")
        narrative = report.narrative().lower()
        self.assertIn("decompose", narrative)
        for phrase in LIVE_FORBIDDEN:
            self.assertNotIn(phrase, narrative)

    def test_schema_does_not_export_sfe_status(self):
        import domain_architect.schema as schema

        self.assertFalse(hasattr(schema, "CANONICAL_SFE_STATUS"))
        self.assertTrue(hasattr(schema, "PRIMARY_OPERATIONS"))

    def test_core_modules_do_not_import_historical(self):
        root = Path(__file__).resolve().parents[1] / "domain_architect"
        banned = {"historical"}
        live = [
            "decompose.py",
            "translate.py",
            "synthesize.py",
            "compatibility.py",
            "cycle.py",
            "realization.py",
            "audit.py",
            "classify.py",
            "leftover_repair.py",
            "lab_cases.py",
            "localized_repair.py",
        ]
        for name in live:
            tree = ast.parse((root / name).read_text(encoding="utf-8"))
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[-1])
            self.assertFalse(
                imported & banned,
                f"{name} imports historical archive modules: {imported & banned}",
            )


class TestExecutableTransformation(unittest.TestCase):
    def test_apply_remaps_coefficients(self):
        t = Transformation(name="firestone", mapping={"m": "L", "c": "R", "k": "1/C"})
        out = t.apply({"m": 2.0, "c": 0.4, "k": 3.0})
        self.assertEqual(out["L"], 2.0)
        self.assertEqual(out["R"], 0.4)
        self.assertTrue(t.applied)
        self.assertFalse(t.is_identity())

    def test_mechanical_electrical_is_transformable_not_equivalent(self):
        record = mechanical_electrical_translation()
        self.assertEqual(record.kind.value, "mathematical_correspondence")
        self.assertTrue(all(c.transformation and c.transformation.applied for c in record.compatibility))
        kinds = {c.kind.value for c in record.compatibility}
        self.assertNotIn("structure_preserving_equivalence", kinds)


class TestRealization(unittest.TestCase):
    def test_free_response_decays(self):
        real = realize_second_order(omega=2.0, zeta=0.25, t_final=6.0)
        self.assertLess(abs(real.y[-1]), abs(real.y[0]))
        self.assertIn("standard", real.method.lower())


class TestDesktopApi(unittest.TestCase):
    def test_status_and_decompose(self):
        status, body, _ctype = handle_api("/api/status", {})
        self.assertEqual(status, 200)
        payload = __import__("json").loads(body)
        self.assertIn("DECOMPOSE", payload["operations"])
        self.assertIn("archived", payload["historical_note"].lower())

        status, body, _ctype = handle_api("/api/decompose", {"expression": "m*xdd + c*xd + k*x = f"})
        self.assertEqual(status, 200)
        report = __import__("json").loads(body)
        text = report["narrative"].lower()
        self.assertIn("domain architect", text)
        self.assertNotIn("canonical sfe", text)

    def test_archive_is_opt_in(self):
        status, body, _ctype = handle_api("/api/archive", {})
        self.assertEqual(status, 200)
        payload = __import__("json").loads(body)
        ids = [eq["equation_id"] for eq in payload["equations"]]
        self.assertIn("SFE-H001", ids)


class TestQstackRegularityPdfStaysArchived(unittest.TestCase):
    def test_pdf_is_in_archive_not_in_live_package(self):
        self.assertTrue(ARCHIVE_QSTACK.is_file(), ARCHIVE_QSTACK)
        raw = ARCHIVE_QSTACK.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), QSTACK_SHA256)
        self.assertEqual(len(raw), 191238)
        self.assertFalse((LIVE_ROOT / "qstack.py").is_file())
        self.assertFalse((LIVE_ROOT / "qnav.py").is_file())
        note = ARCHIVE_QSTACK.parent.joinpath("README.md").read_text(encoding="utf-8")
        self.assertIn("archive only", note.lower())
        self.assertIn("Not Clay", note)
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("import into `domain_architect/`", note)
        archive_index = (
            Path(__file__).resolve().parents[1] / "docs" / "archive" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("qstack/", archive_index)
        self.assertIn("not live DA", archive_index)
        self.assertNotIn("qstack_regularity", " ".join(p.name for p in LIVE_ROOT.iterdir()))


class TestNoPaddedParameterLevel(unittest.TestCase):
    def test_mechanism_is_not_wrapped_in_dummy_parameter(self):
        dec = decompose("m*xdd + c*xd + k*x = f")
        levels = {n.level for n in dec.tree.walk()}
        self.assertIn("MECHANISM", levels)
        self.assertNotIn("PARAMETER", levels)


if __name__ == "__main__":
    unittest.main()
