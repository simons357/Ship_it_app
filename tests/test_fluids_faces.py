"""Swirl WITH/WITHOUT cancel and unaugmented NS live in Domain Architect, not ChatVault."""

from __future__ import annotations

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
from domain_architect.ns_unaugmented import (
    NS_OPERATOR,
    T3_POSTER_RELATIVE,
    face as ns_face,
    looks_like_ns_t3_archive,
    looks_like_ns_unaugmented,
    t3_archive_face,
)
from domain_architect.registry import EquationRegistry
from domain_architect.schema import ConflictRelation
from domain_architect.site_server import SiteHandler
from domain_architect.swirl import (
    SWIRL_WITH_OPERATOR,
    SWIRL_WITHOUT_OPERATOR,
    SWIRL_WITH_PDF_NAME,
    SWIRL_WITHOUT_PDF_NAME,
    compare_faces,
    looks_like_swirl_compare,
    looks_like_swirl_with_cancel,
    looks_like_swirl_without_cancel,
    with_cancel_face,
    without_cancel_face,
)
from domain_architect.track_b_mobius import LOCKED_OPERATOR
from domain_architect.universe import looks_like_universe_inquiry

_REPO = Path(__file__).resolve().parents[1]
_FACES = _REPO / "domain_architect" / "static" / "faces"
_WITH_PDF = _FACES / SWIRL_WITH_PDF_NAME
_WITHOUT_PDF = _FACES / SWIRL_WITHOUT_PDF_NAME
_NS_PDF = _FACES / "ns_unaugmented_classical.pdf"
_T3_POSTER = _REPO / "domain_architect" / "static" / T3_POSTER_RELATIVE
_HOME = _REPO / "domain_architect" / "static" / "index.html"
_JS = _REPO / "domain_architect" / "static" / "da-home.js"
_SW = _REPO / "domain_architect" / "static" / "da-sw.js"

_COMPARE = "axisymmetric Navier-Stokes with swirl: with vs without cancellation"
_T3_PACK = (
    "Global Regularity of the Navier-Stokes Equations on T3. "
    "Clay Statement B. No blowup on T3. doi:10.5281/zenodo.20405526"
)


class SwirlLooksLike(unittest.TestCase):
    def test_with_and_without_are_distinct(self) -> None:
        self.assertTrue(looks_like_swirl_with_cancel(SWIRL_WITH_OPERATOR))
        self.assertTrue(looks_like_swirl_with_cancel("01_phi_renormalization.pdf"))
        self.assertTrue(looks_like_swirl_with_cancel("zenodo.22050974 phi-renormalization"))
        self.assertFalse(looks_like_swirl_without_cancel(SWIRL_WITH_OPERATOR))

        self.assertTrue(looks_like_swirl_without_cancel(SWIRL_WITHOUT_OPERATOR))
        self.assertTrue(looks_like_swirl_without_cancel("swirl without cancellation"))
        self.assertTrue(looks_like_swirl_without_cancel("axisymmetric with swirl 1/r^4 axis term"))
        self.assertFalse(looks_like_swirl_with_cancel(SWIRL_WITHOUT_OPERATOR))
        self.assertFalse(looks_like_swirl_with_cancel("swirl without cancel"))

        self.assertTrue(looks_like_swirl_compare(_COMPARE))
        self.assertFalse(looks_like_swirl_with_cancel(_COMPARE))
        self.assertFalse(looks_like_swirl_without_cancel(_COMPARE))

        self.assertFalse(looks_like_swirl_with_cancel(LOCKED_OPERATOR))
        self.assertFalse(looks_like_swirl_without_cancel(NS_OPERATOR))
        self.assertFalse(looks_like_universe_inquiry(SWIRL_WITH_OPERATOR))
        self.assertFalse(looks_like_universe_inquiry("swirl without cancel"))


class SwirlFaces(unittest.TestCase):
    def test_both_pdfs_load_and_do_not_claim_clay(self) -> None:
        self.assertTrue(_WITH_PDF.is_file(), f"missing {_WITH_PDF}")
        self.assertTrue(_WITH_PDF.read_bytes().startswith(b"%PDF"))
        self.assertGreater(_WITH_PDF.stat().st_size, 10_000)
        self.assertTrue(_WITHOUT_PDF.is_file(), f"missing {_WITHOUT_PDF}")
        self.assertTrue(_WITHOUT_PDF.read_bytes().startswith(b"%PDF"))
        self.assertGreater(_WITHOUT_PDF.stat().st_size, 5_000)

        with_face = with_cancel_face()
        without_face = without_cancel_face()
        self.assertEqual(with_face["engine"], "domain_architect")
        self.assertEqual(without_face["not_engine"], "chatvault")
        self.assertNotEqual(with_face["operator"], without_face["operator"])
        self.assertEqual(with_face["cancellation"], "with")
        self.assertEqual(without_face["cancellation"], "without")
        self.assertFalse(with_face["clay_ns_claimed"])
        self.assertFalse(without_face["clay_ns_claimed"])
        self.assertFalse(with_face["rh_claimed"])
        self.assertTrue(with_face["pdf_present"])
        self.assertTrue(without_face["pdf_present"])
        self.assertEqual(with_face["pdf_url"], "/faces/" + SWIRL_WITH_PDF_NAME)
        self.assertIn("22050974", with_face["doi_live"])

        cmp = compare_faces()
        self.assertEqual(cmp["with_cancel"]["operator"], with_face["operator"])
        self.assertEqual(cmp["without_cancel"]["operator"], without_face["operator"])
        self.assertFalse(cmp["clay_ns_claimed"])
        blob = json.dumps(cmp).lower()
        self.assertNotIn("clay ns is proved", blob)
        self.assertIn("danchin-2007", {c["id"] for c in without_face["citations"]})
        self.assertIn("ladyzhenskaya-prodi-serrin", {c["id"] for c in with_face["citations"]})
        self.assertFalse(cmp["gaps_filled"])
        self.assertFalse(any(gap["filled"] for gap in cmp["gaps"]))


class SwirlInquiry(unittest.TestCase):
    def test_inquiry_distinguishes_and_refuses_drain(self) -> None:
        with_pay = inquire(SWIRL_WITH_OPERATOR, drain=True)
        without_pay = inquire(SWIRL_WITHOUT_OPERATOR, drain=True)
        cmp_pay = inquire(_COMPARE, drain=True)

        self.assertIn("swirl_with_cancel", with_pay)
        self.assertNotIn("swirl_without_cancel", with_pay)
        self.assertIn("swirl_comparison", with_pay)
        self.assertEqual(with_pay["swirl_with_cancel"]["cancellation"], "with")

        self.assertIn("swirl_without_cancel", without_pay)
        self.assertNotIn("swirl_with_cancel", without_pay)
        self.assertEqual(without_pay["swirl_without_cancel"]["cancellation"], "without")

        self.assertIn("swirl_with_cancel", cmp_pay)
        self.assertIn("swirl_without_cancel", cmp_pay)
        self.assertNotEqual(
            with_pay["swirl_with_cancel"]["operator"],
            without_pay["swirl_without_cancel"]["operator"],
        )

        for payload in (with_pay, without_pay, cmp_pay):
            self.assertEqual(payload["lane"], "inquiry")
            self.assertIsNone(payload["drain"])
            self.assertFalse(payload["chatvault"])
            self.assertIn("Not filed into ChatVault", payload["drain_refused"])
            self.assertFalse(payload.get("swirl_comparison", {}).get("clay_ns_claimed", False))
            notes = " ".join(payload["audit"]["notes"]).lower()
            self.assertNotIn("clay ns is claimed", notes)

        self.assertIn("WITH cancel", " ".join(with_pay["audit"]["notes"]))
        self.assertIn("WITHOUT cancel", " ".join(without_pay["audit"]["notes"]))
        self.assertNotIn("ns_unaugmented", with_pay)
        self.assertNotIn("ns_unaugmented", without_pay)
        self.assertIn("Danchin", " ".join(without_pay["audit"]["notes"]))
        self.assertIn("Ladyzhenskaya–Prodi–Serrin", " ".join(with_pay["audit"]["notes"]))


class UnaugmentedNS(unittest.TestCase):
    def test_face_is_open_not_clay(self) -> None:
        self.assertTrue(_NS_PDF.is_file(), f"missing {_NS_PDF}")
        self.assertTrue(_NS_PDF.read_bytes().startswith(b"%PDF"))
        self.assertTrue(_T3_POSTER.is_file())
        self.assertEqual(_T3_POSTER.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

        self.assertTrue(looks_like_ns_unaugmented(NS_OPERATOR))
        self.assertTrue(looks_like_ns_unaugmented("classical unaugmented 3D Navier-Stokes"))
        self.assertTrue(looks_like_ns_t3_archive(_T3_PACK))
        self.assertFalse(looks_like_ns_unaugmented(SWIRL_WITH_OPERATOR))
        self.assertFalse(looks_like_ns_unaugmented(SWIRL_WITHOUT_OPERATOR))
        self.assertFalse(looks_like_universe_inquiry(NS_OPERATOR))

        face = ns_face()
        self.assertEqual(face["status"], "open_not_proved")
        self.assertFalse(face["clay_ns_claimed"])
        self.assertFalse(face["rh_claimed"])
        self.assertFalse(face["chatvault"])
        self.assertTrue(face["pdf_present"])
        blob = json.dumps(face).lower()
        self.assertNotIn('"clay_ns_claimed": true', blob)

        archive = t3_archive_face()
        self.assertEqual(archive["status"], "superseded_prize_packaging")
        self.assertEqual(archive["use_instead"], "/faces/ns_unaugmented_classical.pdf")
        self.assertFalse(archive["clay_ns_claimed"])

    def test_inquiry_opens_equation_and_refuses_drain(self) -> None:
        payload = inquire(NS_OPERATOR, drain=True)
        self.assertIn("ns_unaugmented", payload)
        self.assertEqual(payload["ns_unaugmented"]["status"], "open_not_proved")
        self.assertIsNone(payload["drain"])
        self.assertFalse(payload["chatvault"])
        self.assertIn("Not filed into ChatVault", payload["drain_refused"])
        notes = " ".join(payload["audit"]["notes"])
        self.assertIn("OPEN", notes)
        self.assertNotIn("Clay Statement B is claimed", notes)

        packed = inquire(_T3_PACK, drain=True)
        self.assertIn("ns_unaugmented", packed)
        self.assertIn("ns_t3_archive", packed)
        self.assertEqual(packed["ns_t3_archive"]["status"], "superseded_prize_packaging")
        self.assertEqual(packed["ns_unaugmented"]["status"], "open_not_proved")
        self.assertIsNone(packed["drain"])
        self.assertNotIn("swirl_with_cancel", payload)
        self.assertNotIn("swirl_without_cancel", payload)


class FluidsHomepage(unittest.TestCase):
    def test_desktop_pack_is_on_the_inquiry_page(self) -> None:
        html = _HOME.read_text(encoding="utf-8")
        self.assertIn("da-swirl-card", html)
        self.assertIn("da-ns-card", html)
        self.assertIn("/faces/01_phi_renormalization.pdf", html)
        self.assertIn("/faces/swirl_without_cancel.pdf", html)
        self.assertIn("/faces/ns_unaugmented_classical.pdf", html)
        self.assertIn("does not file into chatvault", html.lower())
        self.assertIn("tweet_inverse_gcd_route_c.png", html)
        js = _JS.read_text(encoding="utf-8")
        self.assertIn("/api/swirl-with-cancel", js)
        self.assertIn("/api/swirl-without-cancel", js)
        self.assertIn("/api/ns-unaugmented", js)
        self.assertIn("runInquiry(false)", js)
        self.assertIn("/faces/", _SW.read_text(encoding="utf-8"))


class FluidsRegistry(unittest.TestCase):
    def test_ns_and_swirl_rows(self) -> None:
        registry = EquationRegistry.load_default()
        self.assertEqual(registry.equations["NS-PHI001"].audit_disposition, "RETAIN")
        self.assertEqual(registry.equations["NS-B001"].audit_disposition, "RETAIN")
        self.assertEqual(registry.equations["NS-T3001"].audit_disposition, "RETIRE")
        self.assertIn("OPEN", registry.equations["NS-B001"].notes)
        self.assertIn("Not ChatVault", registry.equations["NS-PHI000"].notes)
        pairs = {frozenset({c.left_id, c.right_id}): c for c in registry.conflicts}
        self.assertEqual(
            pairs[frozenset({"NS-PHI000", "NS-PHI001"})].relation,
            ConflictRelation.INCOMPATIBLE.value,
        )
        self.assertEqual(
            pairs[frozenset({"NS-B001", "NS-A001"})].relation,
            ConflictRelation.INCOMPATIBLE.value,
        )


class FluidsCli(unittest.TestCase):
    def test_flags_and_drain_refuse(self) -> None:
        for flag, key in (
            ("--swirl-with-cancel", "cancellation"),
            ("--swirl-without-cancel", "cancellation"),
            ("--ns-unaugmented", "status"),
        ):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main([flag, "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(buf.getvalue())
            self.assertFalse(payload["clay_ns_claimed"])
            self.assertFalse(payload["chatvault"])
            self.assertIn(key, payload)

        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(["--drain-chatvault", SWIRL_WITH_OPERATOR, "--json"])
        self.assertEqual(rc, 0)
        self.assertIn("Not filed into ChatVault", err.getvalue())
        self.assertNotEqual(json.loads(out.getvalue()).get("format"), "chatvault-export")


class FluidsHttp(unittest.TestCase):
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

    def test_pdfs_apis_and_inquiry(self) -> None:
        for path in (
            "/faces/01_phi_renormalization.pdf",
            "/faces/swirl_without_cancel.pdf",
            "/faces/ns_unaugmented_classical.pdf",
        ):
            with urllib.request.urlopen(f"{self.origin}{path}") as res:
                self.assertEqual(res.status, 200)
                self.assertIn("pdf", res.headers.get("Content-Type", ""))
                self.assertTrue(res.read().startswith(b"%PDF"))

        with urllib.request.urlopen(f"{self.origin}/api/swirl-with-cancel") as res:
            with_meta = json.loads(res.read().decode("utf-8"))
        with urllib.request.urlopen(f"{self.origin}/api/swirl-without-cancel") as res:
            without_meta = json.loads(res.read().decode("utf-8"))
        self.assertNotEqual(with_meta["operator"], without_meta["operator"])
        self.assertFalse(with_meta["clay_ns_claimed"])

        req = urllib.request.Request(
            f"{self.origin}/api/inquiry",
            data=json.dumps({"inquiry": _COMPARE, "drain": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as res:
            inq = json.loads(res.read().decode("utf-8"))
        self.assertIsNone(inq["drain"])
        self.assertIn("swirl_comparison", inq)
        self.assertIn("Not filed into ChatVault", inq["drain_refused"])

        ns_req = urllib.request.Request(
            f"{self.origin}/api/inquiry",
            data=json.dumps({"inquiry": NS_OPERATOR, "drain": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(ns_req) as res:
            ns_inq = json.loads(res.read().decode("utf-8"))
        self.assertEqual(ns_inq["ns_unaugmented"]["status"], "open_not_proved")
        self.assertIsNone(ns_inq["drain"])


if __name__ == "__main__":
    unittest.main()
