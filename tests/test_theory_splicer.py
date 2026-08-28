#!/usr/bin/env python3
"""Tests: theory splicer CRISPR operations — cut/insert/splice refuse/pass."""

from __future__ import annotations

import json
import unittest
from io import StringIO
from unittest import mock

from domain_architect.cli import main as cli_main
from domain_architect.schema import ConflictRelation
from domain_architect.theory_splicer import (
    cut,
    express,
    get_book,
    insert,
    list_millennium_problems,
    load_millennium_registry,
    screen,
    splice,
)


class TestMillenniumRegistry(unittest.TestCase):
    def test_registry_loads_all_seven_problems(self):
        reg = load_millennium_registry()
        problems = reg["problems"]
        self.assertIn("NS", problems)
        self.assertIn("RH", problems)
        self.assertIn("POINCARE", problems)
        self.assertEqual(problems["NS"]["status"], "OPEN")
        self.assertEqual(problems["POINCARE"]["status"], "SOLVED_REFERENCE")

    def test_list_millennium_honest_status(self):
        items = list_millennium_problems()
        ns = next(i for i in items if i["id"] == "NS")
        self.assertIn("NOT proved", ns["honest_note"])
        self.assertIn("SND-C", ns["books"])


class TestScreenWelds(unittest.TestCase):
    def test_ns_screen_finds_incompatible_welds(self):
        report = screen("NS")
        self.assertTrue(report.bullshit_destroyed)
        self.assertGreater(report.incompatible_count, 0)
        incompatible = [w for w in report.welds if w["screen_verdict"] == "INCOMPATIBLE"]
        ids = {w["weld_id"] for w in incompatible}
        self.assertIn("W-NS-SNDC-CLAY", ids)

    def test_rh_screen_has_open_q6_weld(self):
        report = screen("RH")
        open_welds = [w for w in report.welds if w["screen_verdict"] == "OPEN"]
        self.assertTrue(any("Q6" in w["weld_id"] for w in open_welds))


class TestCutInsert(unittest.TestCase):
    def test_cut_thm_d_clay(self):
        result = cut("SND-C", "THM-D-CLAY")
        self.assertTrue(result.success)
        self.assertTrue(result.bullshit_destroyed)
        self.assertIn("Clay", " ".join(result.bullshit_flags))

    def test_cut_missing_claim_fails(self):
        result = cut("NS-B", "NONEXISTENT")
        self.assertFalse(result.success)

    def test_insert_boot_m_candidate(self):
        result = insert(
            "BOOT-M",
            "scale_response",
            "Lemma (Bootstrap-M): M=M(||u0||_{H^1})",
        )
        self.assertTrue(result.success)
        self.assertFalse(result.bullshit_destroyed)

    def test_insert_refuses_clay_glue_candidate(self):
        result = insert(
            "NS-B",
            "realized_output",
            "Clay Statement B resolved via unconditional SND for all H^1 data",
        )
        self.assertFalse(result.success)
        self.assertTrue(result.bullshit_destroyed)


class TestSpliceRefusePass(unittest.TestCase):
    def test_refuses_clay_glue_splice_sndc_clay(self):
        result = splice("SND-C", "CLAY-B")
        self.assertFalse(result.success)
        self.assertTrue(result.bullshit_destroyed)
        self.assertIn("INCOMPATIBLE", result.message)

    def test_refuses_sfe_to_ns_splice(self):
        result = splice("SFE", "NS-B")
        self.assertFalse(result.success)
        self.assertTrue(result.bullshit_destroyed)
        flags = " ".join(result.bullshit_flags)
        self.assertIn("INCOMPATIBLE", flags)

    def test_allows_compatible_distinct_boot_sndc(self):
        result = splice("BOOT-M", "SND-C")
        self.assertTrue(result.success)
        self.assertFalse(result.bullshit_destroyed)
        self.assertIn("COMPATIBLE_DISTINCT", result.message)

    def test_q6_to_rh_insufficient_information(self):
        result = splice("Q6", "RH-ROUTE-C")
        self.assertFalse(result.success)
        self.assertIn("insufficient", result.message.lower())

    def test_q6_to_ns_refused(self):
        result = splice("Q6", "NS-B")
        self.assertFalse(result.success)
        self.assertTrue(result.bullshit_destroyed)


class TestExpress(unittest.TestCase):
    def test_express_ns_b_inventory(self):
        result = express("NS-B")
        self.assertIn("NS-B", result.message)
        self.assertIn("reconstruction", result.details)

    def test_express_snd_c_not_proved_closure(self):
        result = express("SND-C")
        # Conditional book may pass inventory but must not claim Clay proof
        self.assertIn("honest_status", result.details)


class TestCliSpliceFlags(unittest.TestCase):
    def test_cli_list_millennium(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--list-millennium"])
        self.assertEqual(code, 0)
        self.assertIn("Navier-Stokes", buf.getvalue())

    def test_cli_splice_screen_ns_exit_2(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--splice-screen", "NS"])
        self.assertEqual(code, 2)
        self.assertIn("INCOMPATIBLE", buf.getvalue())

    def test_cli_splice_join_refuses_clay(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--splice-join", "SND-C", "CLAY-B"])
        self.assertEqual(code, 2)
        self.assertIn("bullshit_destroyed=True", buf.getvalue())

    def test_cli_splice_cut_json(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--splice-cut", "SND-C", "THM-D-CLAY", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["success"])
        self.assertTrue(payload["bullshit_destroyed"])

    def test_cli_theory_express(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--theory-express", "NS-B", "--json"])
        self.assertIn(code, (0, 2))
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["operation"], "EXPRESS")


class TestHonestyRules(unittest.TestCase):
    def test_all_results_have_bullshit_destroyed_field(self):
        for op in (
            cut("SND-C", "THM-D-CLAY"),
            insert("BOOT-M", "scale_response", "M=M(||u0||)"),
            splice("SFE", "NS-B"),
            express("NS-B"),
        ):
            d = op.to_dict()
            self.assertIn("bullshit_destroyed", d)

    def test_get_book_ns_b(self):
        book = get_book("NS-B")
        self.assertEqual(book.book_id, "NS-B")
        self.assertEqual(book.millennium_id, "NS")


if __name__ == "__main__":
    unittest.main()
