#!/usr/bin/env python3
"""Tests: SND tweet equations route honestly through Domain Architect."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock
from io import StringIO

from domain_architect.audit import audit_expression
from domain_architect.cli import main as cli_main
from domain_architect.gap_closure import diagnose_gap
from domain_architect.registry import EquationRegistry
from domain_architect.snd_claims import anatomize_claim

TWEET_CENTER = (
    "inf_{t>=0} lambda_min(tilde_H_N[u(t)]) / "
    "lambda_max(tilde_H_N[u(t)]) > -1/2"
)
TWEET_SND = "inf_t J(t)/X(t) >= c_* > 0"
TWEET_THM_D = "Clay Statement B <=> [SND]"
TWEET_MAIN = "Main result: global regularity on T^3 — no finite-time blowup (proved)"
TWEET_BYPASS = "Bypass Lemma: tilde_H_N norm bound with 5× safety margin on T^3"


class TestSndTweetRegistry(unittest.TestCase):
    def test_tweet_equations_loaded_from_sidecar(self):
        reg = EquationRegistry.load_default()
        self.assertIn("SND-TWEET-CENTER001", reg.equations)
        self.assertIn("SND-TWEET-THM-D001", reg.equations)
        center = reg.equations["SND-TWEET-CENTER001"]
        self.assertIn("lambda_min", center.original_expression)

    def test_tweet_inventory_file_exists(self):
        path = Path("data/domain_architect/snd_tweet_equations.json")
        self.assertTrue(path.exists())
        payload = json.loads(path.read_text())
        self.assertEqual(payload["source"]["tweet_id"], "2072045366430601408")


class TestSndTweetRouting(unittest.TestCase):
    def test_center_routes_to_snd_bypass_book(self):
        from domain_architect.hb_loop import build_hb_map

        report = audit_expression(TWEET_CENTER)
        hb = build_hb_map(report)
        self.assertEqual(hb.domain_book, "SND-BYPASS")

    def test_snd_jx_routes_to_snd_hyp(self):
        from domain_architect.hb_loop import build_hb_map

        report = audit_expression(TWEET_SND)
        hb = build_hb_map(report)
        self.assertEqual(hb.domain_book, "SND-HYP")

    def test_bypass_gap_closure_book_hint(self):
        gap = diagnose_gap(TWEET_BYPASS)
        self.assertEqual(gap.domain_book_hint, "SND-BYPASS")


class TestSndTweetGapRefusal(unittest.TestCase):
    def test_thm_d_refuses_clay_equiv(self):
        gap = diagnose_gap(TWEET_THM_D)
        self.assertTrue(gap.refuses_unconditional_clay)
        ids = {f.break_id for f in gap.findings}
        self.assertIn("TH-H2", ids)

    def test_main_result_refuses_unconditional_clay(self):
        gap = diagnose_gap(TWEET_MAIN)
        self.assertTrue(gap.refuses_unconditional_clay)

    def test_thm_d_anatomizer_refuses(self):
        audit = anatomize_claim(TWEET_THM_D)
        self.assertTrue(audit.refused)

    def test_cli_gap_thm_d_exit_2(self):
        buf = StringIO()
        with mock.patch("sys.stdout", buf):
            code = cli_main(["--gap-closure", TWEET_THM_D])
        self.assertEqual(code, 2)
        self.assertIn("Broken weld:", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
