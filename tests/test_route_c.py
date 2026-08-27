"""Route C lives in Domain Architect inquiry, not ChatVault."""

from __future__ import annotations

import io
import json
import threading
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from http.server import ThreadingHTTPServer
from pathlib import Path

from domain_architect.audit import audit_expression
from domain_architect.chatvault_bridge import inquire
from domain_architect.cli import main
from domain_architect.registry import EquationRegistry
from domain_architect.route_c import (
    JUNE_OPERATOR,
    JUNE_POSTER_RELATIVE,
    ROUTE_C_OPERATOR,
    ROUTE_C_PDF_FILENAME,
    ROUTE_C_PDF_RELATIVE,
    looks_like_route_c_operator,
    looks_like_superseded_june_route_c,
    route_c_face,
    superseded_june_face,
)
from domain_architect.schema import ConflictRelation
from domain_architect.site_server import SiteHandler
from domain_architect.track_b_mobius import LOCKED_OPERATOR, quarantined_operator_hit

_REPO = Path(__file__).resolve().parents[1]
_PDF = _REPO / "domain_architect" / "static" / "faces" / ROUTE_C_PDF_FILENAME
_POSTER = _REPO / "domain_architect" / "static" / JUNE_POSTER_RELATIVE
_JUNE = (
    "Route C architecture locked. Q_N(i,j) = 1/gcd(i,j). "
    "RH iff lambda_min(Q_N)/log N -> -1/(2pi). doi:10.5281/zenodo.20518388"
)
_HOME = _REPO / "domain_architect" / "static" / "index.html"
_SW = _REPO / "domain_architect" / "static" / "da-sw.js"


class RouteCLooksLike(unittest.TestCase):
    def test_tex_operator_and_aliases(self) -> None:
        self.assertTrue(
            looks_like_route_c_operator(r"Q_N[i,j] = 1/(\gcd(i,j)\sqrt{ij})")
        )
        self.assertTrue(looks_like_route_c_operator(ROUTE_C_OPERATOR))
        self.assertTrue(looks_like_route_c_operator("05_route_c_conditional.pdf"))
        self.assertTrue(looks_like_route_c_operator("Route C conditional RH face"))
        self.assertFalse(looks_like_route_c_operator(LOCKED_OPERATOR))
        self.assertFalse(looks_like_route_c_operator("Q_N[i,j] = 1/gcd(i,j)"))
        self.assertFalse(looks_like_route_c_operator(_JUNE))
        self.assertTrue(looks_like_superseded_june_route_c(_JUNE))
        self.assertTrue(looks_like_superseded_june_route_c("RH_Riemann_final.tex"))
        self.assertFalse(looks_like_superseded_june_route_c(ROUTE_C_OPERATOR))
        self.assertFalse(looks_like_superseded_june_route_c("Route C conditional RH face"))


class RouteCFace(unittest.TestCase):
    def test_face_is_exploratory_not_proof(self) -> None:
        face = route_c_face()
        self.assertEqual(face["engine"], "domain_architect")
        self.assertEqual(face["not_engine"], "chatvault")
        self.assertEqual(face["status"], "exploratory_conditional")
        self.assertFalse(face["claims_rh"])
        self.assertFalse(face["rh_claimed"])
        self.assertFalse(face["chatvault"])
        gaps = " ".join(face["gaps_open"])
        self.assertIn("Gap A", gaps)
        self.assertIn("Gap B", gaps)
        self.assertNotEqual(face["operator"], LOCKED_OPERATOR)
        self.assertTrue(face["pdf_present"])
        self.assertEqual(face["pdf_relative"], ROUTE_C_PDF_RELATIVE)
        self.assertEqual(face["pdf_url"], "/faces/" + ROUTE_C_PDF_FILENAME)
        self.assertIn("zenodo.20518388", face["supersedes"])


class RouteCPdfOnDisk(unittest.TestCase):
    def test_pdf_is_real_pdf_in_da_static(self) -> None:
        self.assertTrue(_PDF.is_file(), f"missing {_PDF}")
        self.assertTrue(_PDF.read_bytes().startswith(b"%PDF"))
        self.assertGreater(_PDF.stat().st_size, 10_000)

    def test_june_poster_is_archived_not_live(self) -> None:
        self.assertTrue(_POSTER.is_file(), f"missing {_POSTER}")
        self.assertTrue(_POSTER.read_bytes()[:3] == b"\xff\xd8\xff")
        face = superseded_june_face()
        self.assertEqual(face["status"], "superseded")
        self.assertEqual(face["operator"], JUNE_OPERATOR)
        self.assertTrue(face["poster_present"])
        self.assertFalse(face["rh_claimed"])
        self.assertEqual(face["use_instead"], "/faces/" + ROUTE_C_PDF_FILENAME)


class RouteCNotQuarantinedAsTrackB(unittest.TestCase):
    def test_route_c_operator_is_not_track_b_quarantine(self) -> None:
        self.assertIsNone(quarantined_operator_hit(ROUTE_C_OPERATOR))
        self.assertIsNone(quarantined_operator_hit(r"1/(\gcd\sqrt{ij})"))
        self.assertEqual(
            quarantined_operator_hit("Q_N[i,j] = 1/gcd(i,j)"),
            "raw inverse-GCD 1/gcd is not RH Track B",
        )


class RouteCAudit(unittest.TestCase):
    def test_audit_opens_route_c_book_without_chatvault(self) -> None:
        report = audit_expression(ROUTE_C_OPERATOR)
        notes = " ".join(report.notes)
        extra = " ".join(report.extra_structures)
        self.assertIn("Route C", notes)
        self.assertIn("ChatVault", notes)
        self.assertIn("Gaps A and B remain open", notes)
        self.assertIn("RH is not claimed", notes)
        self.assertIn("Route C exploratory face", extra)
        self.assertNotIn("Mertens-bridge", notes)
        self.assertFalse(any("QUARANTINE" in item.upper() for item in report.notes))
        self.assertNotIn("unified theory", notes.lower())


class RouteCJunePosterSuperseded(unittest.TestCase):
    def test_audit_marks_june_poster_superseded(self) -> None:
        report = audit_expression(_JUNE)
        notes = " ".join(report.notes)
        extra = " ".join(report.extra_structures)
        self.assertIn("SUPERSEDED", notes)
        self.assertIn("RH_Riemann_final.tex", notes)
        self.assertIn("05_route_c_conditional.pdf", notes)
        self.assertIn("not claimed", notes.lower())
        self.assertIn("June 2026 Route C poster SUPERSEDED", extra)
        self.assertNotIn("Route C operator locked: " + ROUTE_C_OPERATOR, notes)

    def test_inquire_refuses_drain_and_does_not_open_live_face(self) -> None:
        payload = inquire(_JUNE, drain=True)
        self.assertIsNone(payload["drain"])
        self.assertFalse(payload["chatvault"])
        self.assertEqual(payload["route_c_superseded"]["status"], "superseded")
        self.assertNotIn("route_c", payload)


class RouteCDoesNotDrain(unittest.TestCase):
    def test_inquire_refuses_chatvault_drain(self) -> None:
        payload = inquire(ROUTE_C_OPERATOR, drain=True)
        self.assertEqual(payload["lane"], "inquiry")
        self.assertIsNone(payload["drain"])
        self.assertFalse(payload["chatvault"])
        self.assertIn("Not filed into ChatVault", payload["drain_refused"])
        self.assertEqual(payload["route_c"]["pdf_url"], "/faces/" + ROUTE_C_PDF_FILENAME)
        self.assertFalse(payload["route_c"]["rh_claimed"])


class RouteCHomepage(unittest.TestCase):
    def test_inquiry_card_loads_route_c_without_filing(self) -> None:
        html = _HOME.read_text(encoding="utf-8")
        self.assertIn("da-load-route-c", html)
        self.assertIn("da-route-c-card", html)
        self.assertIn("/faces/05_route_c_conditional.pdf", html)
        self.assertIn("superseded", html.lower())
        self.assertIn("june_2026_rh_poster.jpg", html)
        self.assertIn("does not file into ChatVault", html)
        sw = _SW.read_text(encoding="utf-8")
        self.assertIn("/faces/", sw)
        js = (_REPO / "domain_architect" / "static" / "da-home.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("da-load-route-c", js)
        self.assertIn("runInquiry(false)", js)


class RouteCRegistry(unittest.TestCase):
    def test_arith_rc001_conflicts_with_track_b(self) -> None:
        registry = EquationRegistry.load_default()
        self.assertIn("ARITH-RC001", registry.equations)
        rec = registry.equations["ARITH-RC001"]
        self.assertEqual(rec.original_expression, ROUTE_C_OPERATOR)
        self.assertIn("Not ChatVault", rec.notes)
        self.assertEqual(registry.equations["ARITH-RC000"].audit_disposition, "RETIRE")
        pairs = {
            frozenset({c.left_id, c.right_id}): c for c in registry.conflicts
        }
        pair = pairs[frozenset({"ARITH-TB001", "ARITH-RC001"})]
        self.assertEqual(pair.relation, ConflictRelation.INCOMPATIBLE.value)
        june_pair = pairs[frozenset({"ARITH-RC000", "ARITH-RC001"})]
        self.assertEqual(june_pair.relation, ConflictRelation.INCOMPATIBLE.value)


class RouteCCli(unittest.TestCase):
    def test_route_c_flag_json(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--route-c", "--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["operator"], ROUTE_C_OPERATOR)
        self.assertFalse(payload["rh_claimed"])
        self.assertFalse(payload["chatvault"])
        self.assertTrue(payload["pdf_present"])
        notes = " ".join(payload["audit"]["notes"])
        self.assertIn("Route C", notes)

    def test_drain_flag_refuses_route_c(self) -> None:
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(["--drain-chatvault", ROUTE_C_OPERATOR, "--json"])
        self.assertEqual(rc, 0)
        self.assertIn("Not filed into ChatVault", err.getvalue())
        payload = json.loads(out.getvalue())
        self.assertNotEqual(payload.get("format"), "chatvault-export")
        self.assertIn("Route C", " ".join(payload["notes"]))


class RouteCHttp(unittest.TestCase):
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

    def test_pdf_and_api_and_inquiry_without_drain(self) -> None:
        with urllib.request.urlopen(f"{self.origin}/api/route-c") as res:
            meta = json.loads(res.read().decode("utf-8"))
        self.assertEqual(meta["not_engine"], "chatvault")
        self.assertTrue(meta["pdf_present"])
        self.assertFalse(meta["rh_claimed"])

        with urllib.request.urlopen(
            f"{self.origin}/api/route-c-superseded"
        ) as res:
            old = json.loads(res.read().decode("utf-8"))
        self.assertEqual(old["status"], "superseded")
        self.assertFalse(old["rh_claimed"])

        with urllib.request.urlopen(
            f"{self.origin}/{JUNE_POSTER_RELATIVE}"
        ) as img:
            self.assertEqual(img.status, 200)
            self.assertIn("jpeg", img.headers.get("Content-Type", ""))
            self.assertTrue(img.read()[:3] == b"\xff\xd8\xff")

        with urllib.request.urlopen(
            f"{self.origin}/faces/{ROUTE_C_PDF_FILENAME}"
        ) as pdf_res:
            self.assertEqual(pdf_res.status, 200)
            self.assertIn("pdf", pdf_res.headers.get("Content-Type", ""))
            body = pdf_res.read()
        self.assertTrue(body.startswith(b"%PDF"))
        self.assertGreater(len(body), 10_000)

        req = urllib.request.Request(
            f"{self.origin}/api/inquiry",
            data=json.dumps({"inquiry": ROUTE_C_OPERATOR, "drain": True}).encode(
                "utf-8"
            ),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as res:
            inq = json.loads(res.read().decode("utf-8"))
        self.assertEqual(inq["ok"], True)
        self.assertEqual(inq["lane"], "inquiry")
        self.assertIsNone(inq["drain"])
        self.assertIn("Route C", " ".join(inq["audit"]["notes"]))
        self.assertIn("Not filed into ChatVault", inq["drain_refused"])


if __name__ == "__main__":
    unittest.main()
