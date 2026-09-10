#!/usr/bin/env python3
"""Tests: Lemma★ / DA-NS-1 — shape statement, R_★, refuse proved / numerics."""

from __future__ import annotations

import unittest
from io import StringIO
from unittest import mock

from domain_architect.cli import main as cli_main
from domain_architect.gap_closure import diagnose_gap
from domain_architect.lemma_star import (
    EXPR_LEMMA_STAR,
    EXPR_R_STAR,
    EXPR_SHAPE_FORM,
    R_STAR_KILL_RULES,
    SHAPE_FORM_STATUS,
    analyze_lemma_star,
    compare_lemma_star_shapes,
    express_lemma_star_as_proved,
    insert_product_block_candidate,
    load_lemma_star_inventory,
    product_block_incompleteness,
    recognize_lemma_star,
    recognize_shape_form,
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

    def test_recognize_shape_form_and_r_star(self):
        self.assertTrue(recognize_lemma_star(EXPR_SHAPE_FORM))
        self.assertTrue(recognize_lemma_star(EXPR_R_STAR))
        self.assertTrue(recognize_shape_form("shape statement via R_star"))
        self.assertTrue(recognize_shape_form("u=av size optimization"))


class TestAnalyzeHypothesis(unittest.TestCase):
    def test_status_hypothesis(self):
        report = analyze_lemma_star()
        self.assertEqual(report.status, "HYPOTHESIS")
        self.assertEqual(report.blocker, "PRODUCT-BLOCK")
        self.assertEqual(report.clay_implication, "CONDITIONAL")
        self.assertEqual(report.clay_weld, "WITHHELD")
        self.assertEqual(report.ordinary_3d_product, "INSUFFICIENT")

    def test_shape_statement_lock_in(self):
        report = analyze_lemma_star()
        self.assertTrue(report.shape_statement)
        self.assertTrue(report.viscosity_cancelled)
        self.assertEqual(report.expression_shape_form, EXPR_SHAPE_FORM)
        self.assertEqual(report.expression_r_star, EXPR_R_STAR)
        self.assertIn("SHAPE STATEMENT", report.narrative())
        self.assertFalse(report.ns_solved)
        self.assertEqual(report.shape_form["decisive_form"], "R-STAR / SHAPE-FORM")
        self.assertTrue(SHAPE_FORM_STATUS["viscosity_cancelled"])

    def test_r_star_kill_rules_printed(self):
        report = analyze_lemma_star()
        self.assertEqual(len(report.kill_rules), len(R_STAR_KILL_RULES))
        narr = report.narrative()
        self.assertIn("R_★", narr)
        self.assertIn("DEAD", narr)
        self.assertIn("D_s=0", narr)
        self.assertIn("evidence only", narr.lower())

    def test_quantities_present(self):
        report = analyze_lemma_star()
        for key in (
            "T_c",
            "D_s",
            "R_star",
            "Lambda",
            "X",
            "Y",
            "Z",
            "E",
            "nu",
            "theta",
            "C_0",
        ):
            self.assertIn(key, report.quantities)

    def test_attack_routes_ranked(self):
        report = analyze_lemma_star()
        self.assertGreaterEqual(len(report.attack_routes), 8)
        self.assertEqual(report.attack_routes[0]["id"], "TC-STRUCTURE-HH-L")
        self.assertEqual(report.attack_routes[1]["id"], "SND-SHELL-CONDITIONAL")
        self.assertEqual(report.attack_routes[3]["id"], "NEGATIVE-KILL-R-STAR")
        self.assertEqual(report.attack_routes[4]["id"], "ATTACK-9A-AP-PACKET")
        self.assertEqual(
            report.attack_routes[4]["verdict"], "NEGATIVE_FOR_KILL"
        )
        self.assertEqual(
            report.attack_routes[5]["id"], "ATTACK-9C-FIXED-GAP-SPHERES"
        )
        self.assertEqual(
            report.attack_routes[5]["verdict"], "NEGATIVE_FOR_KILL"
        )
        self.assertEqual(
            report.attack_routes[6]["id"], "ATTACK-9B-EXACT-SHELL-CLOSING"
        )
        self.assertIn("K_{alpha,beta}", report.attack_routes[6]["quantity"])
        self.assertEqual(
            report.attack_routes[7]["id"], "ATTACK-9D-THETA-M2-CLOSURE"
        )
        self.assertEqual(
            report.attack_routes[7]["verdict"], "REMAINING_PACKET_FALSIFIER"
        )

    def test_five_lane_status_synced(self):
        report = analyze_lemma_star()
        self.assertFalse(report.ns_solved)
        self.assertEqual(report.analytic_gap, "HH→L")
        self.assertEqual(report.five_lane["pr"], 48)
        self.assertEqual(report.five_lane["lanes"]["K0_absorption"], "DEAD")
        self.assertEqual(
            report.five_lane["lanes"]["D_s_zero_kill"], "ALIGNED_WITH_K0_DEAD"
        )
        self.assertEqual(report.five_lane["lanes"]["kill_lane"], "LIVE")
        self.assertEqual(report.kill_lane["status"], "LIVE")
        self.assertFalse(report.kill_lane["closed"])
        self.assertIn(
            "NOT_PROVED", report.five_lane["lanes"]["lemma_star_numeric_kill"]
        )
        self.assertIn(
            "UNIFORM", report.five_lane["lanes"]["numeric_bound_vs_uniform"]
        )
        self.assertEqual(report.five_lane["lanes"]["bony_hh_to_l"], "GAP_LIVE")
        self.assertFalse(report.five_lane["lemma_star_proved"])
        self.assertIn("LIVE", report.five_lane["cross_link"])
        self.assertTrue(report.rstar_invariances["ok"])


class TestProductBlock(unittest.TestCase):
    def test_product_block_flagged(self):
        block = product_block_incompleteness()
        self.assertEqual(block["break_id"], "PRODUCT-BLOCK")
        self.assertEqual(block["status"], "OPEN")
        self.assertIn("INSUFFICIENT", block["ordinary_3d"])
        self.assertIn("PRODUCT-BLOCK", block["headline"])
        self.assertEqual(block["analytic_gap"], "HH→L")
        self.assertIn("R_★", block["equivalent_gap"])
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

    def test_refuse_numerics_prove_star(self):
        result = refuse_proved_lemma_star(
            "Numerics prove Lemma★; finite samples green R_star"
        )
        self.assertTrue(result["refused"])
        joined = " ".join(result["refusal_reasons"]).lower()
        self.assertTrue(
            "numeric" in joined
            or "uniform" in joined
            or "evidence" in joined
            or "hypothesis" in joined
        )

    def test_refuse_greening_from_finite_samples(self):
        result = refuse_proved_lemma_star(
            "Finite samples prove Lemma★ shape form; "
            "R_star bounded on samples proves star"
        )
        self.assertTrue(result["refused"])
        self.assertFalse(result["ns_solved"])
        self.assertTrue(result["shape_statement"])

    def test_refuse_ns_solved(self):
        result = refuse_proved_lemma_star("Navier-Stokes solved via Lemma★")
        self.assertTrue(result["refused"])

    def test_refuse_kill_lane_closed(self):
        result = refuse_proved_lemma_star(
            "Lemma★: the kill lane is closed after numeric search"
        )
        self.assertTrue(result["refused"])
        joined = " ".join(result["refusal_reasons"]).lower()
        self.assertTrue(
            "kill lane" in joined or "live" in joined or "closed" in joined
        )
        self.assertEqual(result["kill_lane"]["status"], "LIVE")
        self.assertFalse(result["ns_solved"])

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
        self.assertTrue(bundle["refused_numerics_prove"])


class TestRegistryBooks(unittest.TestCase):
    def test_da_ns_1_book_loads(self):
        book = get_book("DA-NS-1")
        self.assertEqual(book.status, "HYPOTHESIS")
        self.assertTrue(any(c.claim_id == "LEMMA-STAR" for c in book.claims))
        self.assertTrue(any(c.claim_id == "R-STAR" for c in book.claims))
        self.assertTrue(any(c.claim_id == "SHAPE-FORM" for c in book.claims))

    def test_lemma_star_alias(self):
        book = get_book("LEMMA-STAR")
        self.assertEqual(book.book_id, "DA-NS-1")

    def test_product_block_book(self):
        book = get_book("PRODUCT-BLOCK")
        self.assertEqual(book.status, "OPEN")
        claim = book.claim_by_id("PRODUCT-BLOCK")
        self.assertIsNotNone(claim)
        self.assertEqual(claim.status, "OPEN")
        self.assertIn("R_star", claim.expression)

    def test_ns_welds_include_withheld_clay(self):
        report = screen("NS")
        withheld = [
            w for w in report.welds if w.get("screen_verdict") == "WITHHELD"
        ]
        self.assertTrue(
            any(
                "LEMMASTAR" in w["weld_id"].replace("-", "") for w in withheld
            )
            or any(w["weld_id"] == "W-NS-LEMMASTAR-CLAY" for w in withheld)
        )

    def test_rstar_weld_present(self):
        report = screen("NS")
        self.assertTrue(
            any(w["weld_id"] == "W-NS-RSTAR-LEMMASTAR" for w in report.welds)
        )

    def test_screen_lemma_star(self):
        rep = screen_lemma_star()
        self.assertGreaterEqual(rep["withheld_count"], 1)
        self.assertGreaterEqual(len(rep["lemma_welds"]), 3)
        self.assertIn("HYPOTHESIS", rep["statement"])
        self.assertIn("R-STAR", rep["claim_ids"])

    def test_millennium_registry_has_books(self):
        reg = load_millennium_registry()
        books = {b["book_id"] for b in reg["problems"]["NS"]["books"]}
        self.assertIn("DA-NS-1", books)
        self.assertIn("PRODUCT-BLOCK", books)

    def test_inventory_has_r_star_and_shape_form(self):
        inv = load_lemma_star_inventory()
        ids = {c["claim_id"] for c in inv["claims"]}
        self.assertIn("R-STAR", ids)
        self.assertIn("SHAPE-FORM", ids)
        self.assertIn("LEMMA-STAR", ids)
        self.assertIn("KILL-LANE", ids)
        self.assertIn("ATTACK-8", ids)
        self.assertIn("ATTACK-9A", ids)
        self.assertIn("ATTACK-9-FIXED-GAP", ids)
        self.assertIn("ATTACK-9B", ids)
        self.assertIn("ATTACK-9C", ids)
        self.assertIn("ATTACK-9D", ids)
        self.assertTrue(any("numerics" in r for r in inv["refused_routings"]))
        self.assertTrue(any("kill lane" in r for r in inv["refused_routings"]))
        self.assertEqual(inv["kill_lane"]["status"], "LIVE")


class TestShapeCompare(unittest.TestCase):
    def test_shape_compare_vs_snd_and_nsb(self):
        shapes = compare_lemma_star_shapes()
        self.assertIn("vs_SND-C", shapes)
        self.assertIn("vs_NS-B", shapes)
        self.assertIn("verdict", shapes["vs_SND-C"])
        self.assertIn("shape_form_lock_in", shapes)


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
        self.assertTrue(
            "SHAPE" in out
            or "shape" in out.lower()
            or "R_★" in out
            or "R_star" in out
        )

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

    def test_cli_numerics_prove_exits_2(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(
                ["--lemma-star", "Numerics prove Lemma★ from finite samples"]
            )
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
