"""Swirl WITH vs WITHOUT cancel: named citations, unfilled gaps, not Clay."""

from __future__ import annotations

import hashlib
import io
import json
import threading
import unittest
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from http.server import ThreadingHTTPServer
from pathlib import Path

from domain_architect.audit import audit_expression
from domain_architect.chatvault_bridge import inquire
from domain_architect.cli import main
from domain_architect.site_server import SiteHandler
from domain_architect.swirl import (
    CITATION_CHEN_FANG_ZHANG,
    CITATION_DANCHIN,
    CITATION_LPS,
    GAP_WITH_TO_CLASSICAL,
    GAP_WITHOUT_TO_WITH,
    LIVE_WITH_PDF_SHA256,
    SWIRL_WITH_OPERATOR,
    SWIRL_WITHOUT_OPERATOR,
    SWIRL_WITH_PDF_NAME,
    SWIRL_WITHOUT_PDF_NAME,
    compare_faces,
    looks_like_swirl_compare,
    looks_like_swirl_with_cancel,
    looks_like_swirl_without_cancel,
    with_cancel_face,
    with_cancel_pdf_path,
    without_cancel_face,
    without_cancel_pdf_path,
)
from domain_architect.universe import live_desk, looks_like_universe_inquiry

_REPO = Path(__file__).resolve().parents[1]
_HOME = _REPO / "domain_architect" / "static" / "index.html"
_COMPARE = "axisymmetric Navier-Stokes with swirl: with vs without cancellation"


def _pdf_text(path: Path) -> str:
    try:
        import pymupdf
    except ImportError:  # pragma: no cover
        import fitz as pymupdf  # type: ignore

    doc = pymupdf.open(path)
    try:
        return "".join(page.get_text() for page in doc)
    finally:
        doc.close()


class SwirlRouting(unittest.TestCase):
    def test_with_without_and_compare_are_distinct(self) -> None:
        self.assertTrue(looks_like_swirl_with_cancel(SWIRL_WITH_OPERATOR))
        self.assertTrue(looks_like_swirl_with_cancel("Phi-renormalization 22050974"))
        self.assertFalse(looks_like_swirl_without_cancel(SWIRL_WITH_OPERATOR))

        self.assertTrue(looks_like_swirl_without_cancel(SWIRL_WITHOUT_OPERATOR))
        self.assertTrue(looks_like_swirl_without_cancel("swirl without cancel"))
        self.assertFalse(looks_like_swirl_with_cancel("swirl without cancel"))

        self.assertTrue(looks_like_swirl_compare(_COMPARE))
        self.assertFalse(looks_like_swirl_with_cancel(_COMPARE))
        self.assertFalse(looks_like_swirl_without_cancel(_COMPARE))
        self.assertFalse(looks_like_universe_inquiry(SWIRL_WITH_OPERATOR))
        self.assertFalse(looks_like_universe_inquiry(SWIRL_WITHOUT_OPERATOR))


class SwirlCitationsAndGaps(unittest.TestCase):
    def test_danchin_is_named_and_does_not_fill_without_to_with(self) -> None:
        self.assertEqual(CITATION_DANCHIN["name"], "R. Danchin")
        self.assertFalse(CITATION_DANCHIN["fills_gap"])
        self.assertFalse(GAP_WITHOUT_TO_WITH["filled"])
        self.assertEqual(GAP_WITHOUT_TO_WITH["id"], "GAP-SWIRL-AXIS")
        self.assertIn("Chen–Fang–Zhang", GAP_WITHOUT_TO_WITH["next_attempt"]["lemma"])
        self.assertNotIn("Goldbach", GAP_WITHOUT_TO_WITH["next_attempt"]["lemma"])
        self.assertNotIn("Riemann", GAP_WITHOUT_TO_WITH["next_attempt"]["lemma"])

        without = without_cancel_face()
        names = [c["name"] for c in without["citations"]]
        self.assertIn("R. Danchin", names)
        self.assertTrue(any(not c["fills_gap"] for c in without["citations"]))
        notes = " ".join(without["notes"])
        self.assertIn("Danchin", notes)
        self.assertIn("UNFILLED", notes)
        self.assertIn("GAP-SWIRL-AXIS", notes)
        self.assertFalse(without["clay_ns_claimed"])
        self.assertFalse(without["rh_claimed"])
        self.assertEqual(without["not_engine"], "chatvault")

    def test_lps_is_named_and_does_not_close_classical_ns(self) -> None:
        self.assertFalse(CITATION_LPS["fills_gap"])
        self.assertFalse(GAP_WITH_TO_CLASSICAL["filled"])
        self.assertEqual(GAP_WITH_TO_CLASSICAL["id"], "GAP-Q1-CLASSICAL")
        self.assertIn("C(ε)", GAP_WITH_TO_CLASSICAL["next_attempt"]["lemma"])
        self.assertNotIn("Goldbach", GAP_WITH_TO_CLASSICAL["next_attempt"]["lemma"])

        with_face = with_cancel_face()
        names = [c["name"] for c in with_face["citations"]]
        self.assertTrue(any("Ladyzhenskaya–Prodi–Serrin" in name for name in names))
        notes = " ".join(with_face["notes"])
        self.assertIn("UNFILLED", notes)
        self.assertIn("GAP-Q1-CLASSICAL", notes)
        self.assertIn("Q1-augmented", notes)
        self.assertFalse(with_face["clay_ns_claimed"])
        self.assertEqual(with_face["pdf_sha256"], LIVE_WITH_PDF_SHA256)
        self.assertTrue(with_face["pdf_matches_live_zenodo"])

        cmp = compare_faces()
        self.assertFalse(cmp["gaps_filled"])
        gap_ids = {g["id"] for g in cmp["gaps"]}
        self.assertEqual(gap_ids, {"GAP-SWIRL-AXIS", "GAP-Q1-CLASSICAL"})
        self.assertFalse(any(g["filled"] for g in cmp["gaps"]))
        blob = json.dumps(cmp).lower()
        self.assertIn("danchin", blob)
        self.assertNotIn("clay ns is proved", blob)
        self.assertIn(CITATION_CHEN_FANG_ZHANG["name"].split(",")[0].lower(), blob)

    def test_live_with_pdf_is_byte_identical_and_without_cites_danchin(self) -> None:
        with_pdf = with_cancel_pdf_path()
        without_pdf = without_cancel_pdf_path()
        self.assertTrue(with_pdf.is_file())
        self.assertTrue(without_pdf.is_file())
        self.assertTrue(with_pdf.read_bytes().startswith(b"%PDF"))
        self.assertTrue(without_pdf.read_bytes().startswith(b"%PDF"))
        digest = hashlib.sha256(with_pdf.read_bytes()).hexdigest()
        self.assertEqual(digest, LIVE_WITH_PDF_SHA256)

        without_text = _pdf_text(without_pdf)
        self.assertIn("Danchin", without_text)
        self.assertIn("1/r", without_text)
        self.assertIn("22050974", without_text)
        self.assertNotIn("Clay Statement B is proved", without_text)
        self.assertNotIn("[Claim withdrawn]", without_text)


class SwirlInquiryBothPaths(unittest.TestCase):
    def test_both_paths_run_and_refuse_chatvault_drain(self) -> None:
        with_pay = inquire(SWIRL_WITH_OPERATOR, drain=True)
        without_pay = inquire(SWIRL_WITHOUT_OPERATOR, drain=True)
        cmp_pay = inquire(_COMPARE, drain=True)

        self.assertEqual(with_pay["swirl_with_cancel"]["cancellation"], "with")
        self.assertEqual(without_pay["swirl_without_cancel"]["cancellation"], "without")
        self.assertNotEqual(
            with_pay["swirl_with_cancel"]["operator"],
            without_pay["swirl_without_cancel"]["operator"],
        )
        self.assertIn("GAP-Q1-CLASSICAL", " ".join(with_pay["audit"]["notes"]))
        self.assertIn("Danchin", " ".join(without_pay["audit"]["notes"]))
        self.assertIn("GAP-SWIRL-AXIS", " ".join(without_pay["audit"]["notes"]))
        self.assertIn("UNFILLED", " ".join(cmp_pay["audit"]["notes"]))
        self.assertFalse(cmp_pay["swirl_comparison"]["gaps_filled"])

        for payload in (with_pay, without_pay, cmp_pay):
            self.assertEqual(payload["lane"], "inquiry")
            self.assertIsNone(payload["drain"])
            self.assertFalse(payload["chatvault"])
            self.assertIn("Not filed into ChatVault", payload["drain_refused"])
            self.assertFalse(payload.get("swirl_comparison", {}).get("clay_ns_claimed", True))

        with_report = audit_expression(SWIRL_WITH_OPERATOR)
        without_report = audit_expression(SWIRL_WITHOUT_OPERATOR)
        self.assertIn("swirl WITH", " ".join(with_report.extra_structures))
        self.assertIn("swirl WITHOUT", " ".join(without_report.extra_structures))
        self.assertLess(
            with_report.narrative().find("Swirl / NS book"),
            with_report.narrative().find("Abstract syntax tree"),
        )


class SwirlDesktopAndCli(unittest.TestCase):
    def test_homepage_has_both_paths(self) -> None:
        html = _HOME.read_text(encoding="utf-8")
        self.assertIn("da-swirl-card", html)
        self.assertIn("da-inquire-swirl-with", html)
        self.assertIn("da-inquire-swirl-without", html)
        self.assertIn("da-inquire-swirl-compare", html)
        self.assertIn("/faces/" + SWIRL_WITH_PDF_NAME, html)
        self.assertIn("/faces/" + SWIRL_WITHOUT_PDF_NAME, html)
        self.assertIn("Danchin", html)
        self.assertIn("does not file into chatvault", html.lower())

    def test_cli_compare_json_keeps_gaps_unfilled(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--swirl-compare", "--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertFalse(payload["gaps_filled"])
        self.assertFalse(payload["clay_ns_claimed"])
        self.assertIn("danchin", json.dumps(payload).lower())

        err = io.StringIO()
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(["--drain-chatvault", SWIRL_WITHOUT_OPERATOR, "--json"])
        self.assertEqual(rc, 0)
        self.assertIn("Not filed into ChatVault", err.getvalue())
        self.assertNotEqual(json.loads(out.getvalue()).get("format"), "chatvault-export")

    def test_universe_desk_still_four_live_dois(self) -> None:
        dois = {item["doi"] for item in live_desk()}
        self.assertEqual(
            dois,
            {
                "10.5281/zenodo.22050963",
                "10.5281/zenodo.22050974",
                "10.5281/zenodo.22050976",
                "10.5281/zenodo.22050962",
            },
        )


class SwirlHttp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), SiteHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_both_inquiry_paths_over_http(self) -> None:
        for path in (
            f"/faces/{SWIRL_WITH_PDF_NAME}",
            f"/faces/{SWIRL_WITHOUT_PDF_NAME}",
        ):
            with urllib.request.urlopen(f"{self.origin}{path}") as res:
                self.assertEqual(res.status, 200)
                self.assertTrue(res.read().startswith(b"%PDF"))

        with urllib.request.urlopen(f"{self.origin}/api/swirl-compare") as res:
            cmp = json.loads(res.read().decode("utf-8"))
        self.assertFalse(cmp["gaps_filled"])
        self.assertEqual(cmp["with_cancel"]["cancellation"], "with")
        self.assertEqual(cmp["without_cancel"]["cancellation"], "without")

        for inquiry in (SWIRL_WITH_OPERATOR, SWIRL_WITHOUT_OPERATOR, _COMPARE):
            req = urllib.request.Request(
                f"{self.origin}/api/inquiry",
                data=json.dumps({"inquiry": inquiry, "drain": True}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req) as res:
                payload = json.loads(res.read().decode("utf-8"))
            self.assertIsNone(payload["drain"])
            self.assertIn("Not filed into ChatVault", payload["drain_refused"])
            notes = " ".join(payload["audit"]["notes"])
            self.assertIn("UNFILLED", notes)


if __name__ == "__main__":
    unittest.main()
