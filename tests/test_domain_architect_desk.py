#!/usr/bin/env python3
"""Computing-bench desk: layers, splices, and proceed map."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.desk import (
    COSMOEVOLUTION_URL,
    compare_shape,
    format_proceed,
    proceed_report,
    refuse_splice,
)
from domain_architect.registry import EquationRegistry
from domain_architect.schema import CANONICAL_SFE_STATUS


ROOT = Path(__file__).resolve().parents[1]


class TestProceedMap(unittest.TestCase):
    def test_sfe_unresolved_and_cosmo_is_viz(self):
        report = proceed_report()
        self.assertEqual(report["canonical_sfe_status"], CANONICAL_SFE_STATUS)
        self.assertEqual(report["cosmoevolution"]["role"], "visualization only")
        self.assertIn("VIZ ONLY", report["cosmoevolution"]["banner"])
        self.assertEqual(report["cosmoevolution"]["url"], COSMOEVOLUTION_URL)
        self.assertIn("compiler", report["where_we_go"].lower())
        text = format_proceed(report)
        self.assertIn("ChatVault", text)
        self.assertIn("shape first", text.lower())
        self.assertIn("think tank", text.lower())
        self.assertIn("weyl", text.lower())
        self.assertIn("visual appendage", text.lower())
        self.assertNotIn("unified theory", text.lower())
        arms = {a["id"] for a in report["appendages"]}
        self.assertEqual(arms, {"THINK", "SEE"})
        self.assertEqual(report["cosmoevolution"]["role"], "visualization only")

    def test_books_stay_unglued(self):
        ids = {book["id"] for book in proceed_report()["books"]}
        self.assertEqual(ids, {"A", "B", "Q", "U"})


class TestRefuseSplice(unittest.TestCase):
    def test_cosmo_cannot_write_navier_stokes(self):
        d = refuse_splice("COSMO", "B")
        self.assertFalse(d.allowed)
        self.assertEqual(d.opcode, "REFUSED")

    def test_chatvault_cannot_certify_rh(self):
        d = refuse_splice("ChatVault", "RH")
        self.assertFalse(d.allowed)
        self.assertEqual(d.source, "SEARCH")

    def test_a_does_not_imply_b(self):
        d = refuse_splice("A", "B")
        self.assertFalse(d.allowed)
        self.assertIn("different pde", d.reason.lower())

    def test_q_does_not_imply_rh(self):
        d = refuse_splice("Q", "RH")
        self.assertFalse(d.allowed)

    def test_same_book_is_noop(self):
        d = refuse_splice("B", "B")
        self.assertTrue(d.allowed)
        self.assertEqual(d.opcode, "NOOP")

    def test_see_cannot_write_navier_stokes(self):
        d = refuse_splice("SEE", "B")
        self.assertFalse(d.allowed)
        self.assertEqual(d.opcode, "REFUSED")
        self.assertIn("cannot write", d.reason.lower())

    def test_see_is_not_cosmo(self):
        d = refuse_splice("SEE", "VIZ")
        self.assertFalse(d.allowed)
        self.assertEqual(d.opcode, "REFUSED")


class TestShapeFirst(unittest.TestCase):
    def test_pde_and_jx_are_same_shape_different_texture(self):
        c = compare_shape("NS-B", "J/X")
        self.assertEqual(c.verdict, "SAME_SHAPE_DIFFERENT_TEXTURE")
        self.assertFalse(c.allowed_weld)
        self.assertIn("not a theorem", c.reason.lower())

    def test_jx_and_lambda_min_are_incompatible_shapes(self):
        c = compare_shape("J/X", "LAMBDA-MIN")
        self.assertEqual(c.verdict, "INCOMPATIBLE_SHAPE")
        self.assertEqual(c.left_book, "B")
        self.assertEqual(c.right_book, "Q")

    def test_cosmo_is_not_the_da_shape(self):
        c = compare_shape("VIZ", "DA")
        self.assertEqual(c.verdict, "INCOMPATIBLE_SHAPE")

    def test_see_is_not_cosmo_shape(self):
        c = compare_shape("SEE", "VIZ")
        self.assertEqual(c.verdict, "INCOMPATIBLE_SHAPE")
        self.assertEqual(c.left_book, "SEE")
        self.assertEqual(c.right_book, "VIZ")


class TestRegistryRecords(unittest.TestCase):
    def test_viz_and_search_are_registered(self):
        registry = EquationRegistry.load_default()
        self.assertIn("VIZ-H001", registry.equations)
        self.assertIn("SYS-H001", registry.equations)
        self.assertEqual(registry.equations["VIZ-H001"].audit_disposition, "RETIRE")
        self.assertEqual(registry.equations["SYS-H001"].audit_disposition, "RETAIN")
        null_ids = {n.null_id for n in registry.nulls}
        self.assertIn("NULL-COSMO-UNIFIER", null_ids)
        self.assertIn("NULL-CHATVAULT-ORACLE", null_ids)
        pairs = {frozenset({c.left_id, c.right_id}) for c in registry.conflicts}
        self.assertIn(frozenset({"VIZ-H001", "FRA-H002"}), pairs)


class TestCli(unittest.TestCase):
    def test_proceed_exit_zero(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--proceed", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["canonical_sfe_status"], "unresolved")

    def test_refuse_splice_cli(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--refuse-splice", "VIZ", "Q"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("REFUSED", proc.stdout)

    def test_shape_compare_cli(self):
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "domain_architect",
                "--shape-compare",
                "J/X",
                "LAMBDA-MIN",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("INCOMPATIBLE_SHAPE", proc.stdout)


if __name__ == "__main__":
    unittest.main()
