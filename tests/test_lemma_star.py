#!/usr/bin/env python3
"""Tests: Lemma★ / DA-NS-1 — hypothesis status, PRODUCT-BLOCK, refuse proved."""

from __future__ import annotations

import json
import unittest
from io import StringIO
from unittest import mock

from domain_architect.cli import main as cli_main
from domain_architect.gap_closure import diagnose_gap
from domain_architect.lemma_star import (
    EXPR_LEMMA_STAR,
    analyze_lemma_star,
    compare_lemma_star_shapes,
    express_lemma_star_as_proved,
    insert_product_block_candidate,
    product_block_incompleteness,
    recognize_lemma_star,
    refuse_proved_lemma_star,
    screen_lemma_star,
)
from domain_architect.theory_splicer import express, get_book, load_millennium_registry, screen


class TestLemmaStarRecognition(unittest.TestCase):
    def test_recognize_canonical(self):
        self.assertTrue(recognize_lemma_star(EXPR_LEMMA_STAR))

    def test_recognize_label_variants(self):
        self.assertTrue(recognize_lemma_star("Lemma★ energy budget"))
        self.assertTrue(recognize_lemma_star("DA-NS-1 spectral drift"))
        self.assertTrue(recognize_lemma_star("lemma-star closing estimate"))

    def test_recognize_unicode(self):
        self.assertTrue(
            recognize_lemma_star(
                "T_c ≤ θν(Z − ΛY) + C_0 ν^{-1} ||u||_2^2 X Λ"
            )
        )


class TestAnalyzeHypothesis(unittest.TestCase):
    def test_status_hypothesis(self):
        report = analyze_lemma_star()
        self.assertEqual(report.status, "HYPOTHESIS")
        self.assertEqual(report.blocker, "PRODUCT-BLOCK")
        self.assertEqual(report.clay_implication, "CONDITIONAL")
        self.assertEqual(report.clay_weld, "WITHHELD")
        self.assertEqual(report.ordinary_3d_product, "INSUFFICIENT")

    def test_quantities_present(self):
        report = analyze_lemma_star()
        for key in ("T_c", "Lambda", "X", "Y", "Z", "E", "nu", "theta", "C_0", "C_geom", "D_s"):
            self.assertIn(key, report.quantities)
        self.assertIn("A(A-Lambda)", report.quantities["T_c"])
        self.assertIn("M - Lambda", report.quantities["T_c"])

    def test_attack_routes_ranked(self):
        report = analyze_lemma_star()
        self.assertGreaterEqual(len(report.attack_routes), 4)
        self.assertEqual(report.attack_routes[0]["id"], "TC-STRUCTURE-HH-L")
        self.assertEqual(report.attack_routes[1]["id"], "SND-SHELL-CONDITIONAL")

    def test_five_lane_status_synced(self):
        report = analyze_lemma_star()
        self.assertFalse(report.ns_solved)
        self.assertEqual(report.analytic_gap, "HH→L")
        self.assertEqual(report.five_lane["pr"], 48)
        self.assertEqual(report.five_lane["lanes"]["K0_absorption"], "DEAD")
        self.assertIn("NOT_PROVED", report.five_lane["lanes"]["lemma_star_numeric_kill"])
        self.assertEqual(report.five_lane["lanes"]["bony_hh_to_l"], "GAP_LIVE")
        self.assertFalse(report.five_lane["lemma_star_proved"])


class TestProductBlock(unittest.TestCase):
    def test_product_block_flagged(self):
        block = product_block_incompleteness()
        self.assertEqual(block["break_id"], "PRODUCT-BLOCK")
        self.assertEqual(block["status"], "OPEN")
        self.assertIn("INSUFFICIENT", block["ordinary_3d"])
        self.assertIn("PRODUCT-BLOCK", block["headline"])
        self.assertEqual(block["analytic_gap"], "HH→L")
        self.assertFalse(block["ns_solved"])

    def test_gap_closure_finds_product_block(self):
        gap = diagnose_gap(EXPR_LEMMA_STAR)
        ids = [f.break_id for f in gap.findings]
        self.assertIn("PRODUCT-BLOCK", ids)
        self.assertEqual(gap.domain_book_hint, "DA-NS-1")

    def test_insert_product_block_candidate(self):
        result = insert_product_block_candidate()
        self.assertTrue(result.success)
        self.assertEqual(result.operation, "INSERT")


class TestRefuseProved(unittest.TestCase):
    def test_refuse_proved_claim(self):
        result = refuse_proved_lemma_star(
            "Lemma★ proved; closes Clay Statement B"
        )
        self.assertTrue(result["refused"])
        self.assertFalse(result["ok"])
        self.assertIn("PRODUCT-BLOCK", " ".join(result["refusal_reasons"]))

    def test_refuse_almost_proved(self):
        result = refuse_proved_lemma_star(
            "Lemma★ is almost proved; numeric survival greening"
        )
        self.assertTrue(result["refused"])
        joined = " ".join(result["refusal_reasons"]).lower()
        self.assertTrue(
            "almost" in joined or "numeric" in joined or "hh" in joined
        )
        self.assertFalse(result["ns_solved"])

    def test_refuse_ns_solved(self):
        result = refuse_proved_lemma_star("Navier-Stokes solved via Lemma★")
        self.assertTrue(result["refused"])

    def test_refuse_kab_equals_full_star(self):
        result = refuse_proved_lemma_star(
            "K_{alpha,beta} equals the full Lemma★"
        )
        self.assertTrue(result["refused"])
        joined = " ".join(result["refusal_reasons"])
        self.assertIn("K_", joined)
        self.assertIn("restricted", joined.lower())

    def test_express_da_ns_1_refuses_green(self):
        result = express("DA-NS-1")
        self.assertFalse(result.success)
        self.assertTrue(result.bullshit_destroyed)
        self.assertIn("PRODUCT-BLOCK", " ".join(result.bullshit_flags))

    def test_express_lemma_star_alias(self):
        result = express("LEMMA-STAR")
        self.assertFalse(result.success)

    def test_express_as_proved_bundle(self):
        bundle = express_lemma_star_as_proved()
        self.assertTrue(bundle["refused_proved"])


class TestRegistryBooks(unittest.TestCase):
    def test_da_ns_1_book_loads(self):
        book = get_book("DA-NS-1")
        self.assertEqual(book.status, "HYPOTHESIS")
        self.assertTrue(any(c.claim_id == "LEMMA-STAR" for c in book.claims))

    def test_lemma_star_alias(self):
        book = get_book("LEMMA-STAR")
        self.assertEqual(book.book_id, "DA-NS-1")

    def test_product_block_book(self):
        book = get_book("PRODUCT-BLOCK")
        self.assertEqual(book.status, "OPEN")
        claim = book.claim_by_id("PRODUCT-BLOCK")
        self.assertIsNotNone(claim)
        self.assertEqual(claim.status, "OPEN")

    def test_ns_welds_include_withheld_clay(self):
        report = screen("NS")
        withheld = [w for w in report.welds if w.get("screen_verdict") == "WITHHELD"]
        self.assertTrue(
            any("LEMMASTAR" in w["weld_id"].replace("-", "") for w in withheld)
            or any(w["weld_id"] == "W-NS-LEMMASTAR-CLAY" for w in withheld)
        )

    def test_screen_lemma_star(self):
        rep = screen_lemma_star()
        self.assertGreaterEqual(rep["withheld_count"], 1)
        self.assertGreaterEqual(len(rep["lemma_welds"]), 3)
        self.assertIn("HYPOTHESIS", rep["statement"])

    def test_millennium_registry_has_books(self):
        reg = load_millennium_registry()
        books = {b["book_id"] for b in reg["problems"]["NS"]["books"]}
        self.assertIn("DA-NS-1", books)
        self.assertIn("PRODUCT-BLOCK", books)


class TestShapeCompare(unittest.TestCase):
    def test_shape_compare_vs_snd_and_nsb(self):
        shapes = compare_lemma_star_shapes()
        self.assertIn("vs_SND-C", shapes)
        self.assertIn("vs_NS-B", shapes)
        # Should not crash; verdict is some ShapeMatchVerdict value
        self.assertIn("verdict", shapes["vs_SND-C"])


class TestCLI(unittest.TestCase):
    def test_cli_lemma_star(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--lemma-star"])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("HYPOTHESIS", out)
        self.assertIn("PRODUCT-BLOCK", out)
        self.assertTrue("HH" in out or "hh" in out.lower())
        self.assertIn("NOT SOLVED", out)

    def test_cli_navigate_da_ns_1(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--navigate", "DA-NS-1"])
        self.assertEqual(code, 0)
        self.assertIn("DA-NS-1", buf.getvalue())

    def test_cli_splice_screen_lemma_star(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--splice-screen", "LEMMA-STAR"])
        self.assertEqual(code, 0)
        self.assertIn("LEMMA-STAR", buf.getvalue())

    def test_cli_lemma_star_proved_exits_2(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(
                ["--lemma-star", "Lemma★ proved closes Clay Statement B"]
            )
        self.assertEqual(code, 2)

    def test_cli_almost_proved_exits_2(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--lemma-star", "Lemma★ almost proved"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
