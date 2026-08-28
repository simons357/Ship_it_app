#!/usr/bin/env python3
"""Tests: shape–texture ontology and library indexer."""

from __future__ import annotations

import json
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

from domain_architect.cli import main as cli_main
from domain_architect.library_index import (
    MANIFEST_PATH,
    inventory_summary,
    load_manifest,
    scan_library,
)
from domain_architect.shape_texture import (
    ShapeMatchVerdict,
    extract_shape,
    extract_texture,
    finger_glossary,
    navigate_millennium,
    shape_match,
    texture_translate,
)


class TestShapeExtraction(unittest.TestCase):
    def test_extract_shape_ns_book(self):
        shape = extract_shape("NS-B")
        self.assertIn("P", shape.fingers)
        self.assertIn("H", shape.fingers)
        self.assertIn("admissibility", shape.role_topology)

    def test_extract_shape_expression(self):
        shape = extract_shape("partial_t omega = nu Delta omega")
        self.assertTrue(shape.role_topology or shape.fingers)

    def test_extract_texture_snd_c(self):
        tex = extract_texture("SND-C")
        self.assertIn(tex.notation, ("SND_shell_flux", "generic", "NS_PDE", "Clay_packaging"))
        self.assertEqual(tex.book_id, "SND-C")

    def test_finger_glossary(self):
        gloss = finger_glossary()
        self.assertIn("P", gloss)


class TestShapeMatch(unittest.TestCase):
    def test_snd_c_boot_m_compatible(self):
        match = shape_match("SND-C", "BOOT-M")
        self.assertIn(
            match.verdict,
            (ShapeMatchVerdict.COMPATIBLE, ShapeMatchVerdict.SAME_SHAPE_DIFFERENT_TEXTURE),
        )

    def test_sfe_ns_incompatible(self):
        match = shape_match("SFE", "NS-B")
        self.assertEqual(match.verdict, ShapeMatchVerdict.INCOMPATIBLE)

    def test_jx_vs_lambda_texture_mismatch(self):
        jx = "inf_t J(t)/X(t) >= c_* > 0"
        bypass = (
            "inf lambda_min(tilde_H_N)/lambda_max(tilde_H_N) > -1/2"
        )
        match = shape_match(jx, bypass)
        self.assertIn(
            match.verdict,
            (
                ShapeMatchVerdict.SAME_SHAPE_DIFFERENT_TEXTURE,
                ShapeMatchVerdict.COMPATIBLE,
                ShapeMatchVerdict.INCOMPATIBLE,
            ),
        )
        trans = texture_translate(jx, bypass)
        self.assertTrue(trans.hypothesis_only)
        self.assertTrue(trans.candidate_rewrites)


class TestLibraryIndex(unittest.TestCase):
    def test_scan_library_produces_objects(self):
        manifest = scan_library(write_manifest=True)
        self.assertGreater(manifest["object_count"], 10)
        self.assertIn("NS", manifest.get("millennium_coverage", {}))

    def test_manifest_file_written(self):
        scan_library(write_manifest=True)
        self.assertTrue(MANIFEST_PATH.exists())
        data = json.loads(MANIFEST_PATH.read_text())
        self.assertIn("objects", data)

    def test_inventory_summary(self):
        manifest = load_manifest()
        summary = inventory_summary(manifest)
        self.assertIn("KEEP", summary)
        self.assertIn("objects", summary)


class TestNavigate(unittest.TestCase):
    def test_navigate_ns(self):
        manifest = load_manifest()
        nav = navigate_millennium("NS", manifest=manifest.get("objects"))
        self.assertEqual(nav.millennium_id, "NS")
        self.assertIn("navigates", nav.statement.lower())

    def test_navigate_rh(self):
        manifest = load_manifest()
        nav = navigate_millennium("RH", manifest=manifest.get("objects"))
        self.assertEqual(nav.millennium_id, "RH")


class TestCliShapeTexture(unittest.TestCase):
    def test_cli_shape(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--shape", "NS-B"])
        self.assertEqual(code, 0)
        self.assertIn("Shape:", buf.getvalue())

    def test_cli_texture(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--texture", "SND-C"])
        self.assertEqual(code, 0)
        self.assertIn("Texture:", buf.getvalue())

    def test_cli_shape_compare(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--shape-compare", "SND-C", "BOOT-M"])
        self.assertEqual(code, 0)
        self.assertIn("Shape compare:", buf.getvalue())

    def test_cli_library_scan(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--library-scan"])
        self.assertEqual(code, 0)
        self.assertIn("Library", buf.getvalue())

    def test_cli_navigate_ns_json(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--navigate", "NS", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["millennium_id"], "NS")


if __name__ == "__main__":
    unittest.main()
