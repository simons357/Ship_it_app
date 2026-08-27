"""Universe / SFE picture stays unresolved in Domain Architect inquiry."""

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
from domain_architect.route_c import ROUTE_C_OPERATOR
from domain_architect.schema import CANONICAL_SFE_STATUS
from domain_architect.site_server import SiteHandler
from domain_architect.track_b_mobius import LOCKED_OPERATOR
from domain_architect.universe import (
    DOI_PHI,
    DOI_Q6,
    DOI_RING,
    DOI_ROUTE_C,
    UNIVERSE_PROMPT,
    face,
    looks_like_universe_inquiry,
    universe_notes,
)

_REPO = Path(__file__).resolve().parents[1]
_HOME = _REPO / "domain_architect" / "static" / "index.html"
_JS = _REPO / "domain_architect" / "static" / "da-home.js"
_PROGRAM = _REPO / "docs" / "domain-architect" / "UNIVERSE-PROGRAM.md"
_README = _REPO / "docs" / "domain-architect" / "README.md"

_FORBIDDEN_PUBLIC = (
    "withdrawn",
    "tombstoned",
    "ai withdrew",
)


class UniverseLooksLike(unittest.TestCase):
    def test_picture_questions_match_and_other_books_do_not(self) -> None:
        self.assertTrue(looks_like_universe_inquiry(UNIVERSE_PROMPT))
        self.assertTrue(looks_like_universe_inquiry("what is the universe"))
        self.assertTrue(looks_like_universe_inquiry("canonical SFE"))
        self.assertTrue(looks_like_universe_inquiry("theory of everything"))
        self.assertTrue(looks_like_universe_inquiry("TOE"))
        self.assertTrue(looks_like_universe_inquiry("one Hamiltonian, three prizes"))
        self.assertTrue(looks_like_universe_inquiry("SFE-PUB as the field"))
        self.assertFalse(looks_like_universe_inquiry("∇²Φ = 4π G ρ"))
        self.assertFalse(looks_like_universe_inquiry(ROUTE_C_OPERATOR))
        self.assertFalse(looks_like_universe_inquiry(LOCKED_OPERATOR))
        self.assertFalse(looks_like_universe_inquiry("Q1-augmented swirl without cancel"))
        self.assertFalse(looks_like_universe_inquiry("classical unaugmented Navier-Stokes on T3"))
        self.assertFalse(looks_like_universe_inquiry("Phi-renormalization for axisymmetric swirl"))
        self.assertFalse(looks_like_universe_inquiry("Navier-Stokes on T3"))
        self.assertFalse(looks_like_universe_inquiry("x = y"))


class UniverseFace(unittest.TestCase):
    def test_face_is_unresolved_not_a_proof(self) -> None:
        payload = face()
        self.assertEqual(payload["engine"], "domain_architect")
        self.assertEqual(payload["not_engine"], "chatvault")
        self.assertEqual(payload["status"], "unresolved")
        self.assertTrue(payload["exploratory"])
        self.assertFalse(payload["proof"])
        self.assertFalse(payload["rh_claimed"])
        self.assertFalse(payload["ns_claimed"])
        self.assertFalse(payload["claims_toe"])
        self.assertFalse(payload["chatvault"])
        self.assertEqual(payload["canonical_sfe_status"], CANONICAL_SFE_STATUS)
        dois = {item["doi"] for item in payload["live_desk"]}
        self.assertEqual(dois, {DOI_ROUTE_C, DOI_PHI, DOI_RING, DOI_Q6})
        blob = json.dumps(payload).lower()
        for phrase in _FORBIDDEN_PUBLIC:
            self.assertNotIn(phrase, blob)
        self.assertNotIn("unified theory", " ".join(universe_notes()).lower())


class UniverseAudit(unittest.TestCase):
    def test_inquiry_returns_unresolved_exploratory_not_a_proof(self) -> None:
        report = audit_expression(UNIVERSE_PROMPT)
        notes = " ".join(report.notes)
        extra = " ".join(report.extra_structures)
        narrative = report.narrative().lower()
        self.assertEqual(report.canonical_sfe_status, "unresolved")
        self.assertIn("unresolved", notes.lower())
        self.assertIn("exploratory", notes.lower())
        self.assertIn("not a proof", notes.lower())
        self.assertIn(DOI_ROUTE_C, notes)
        self.assertIn(DOI_PHI, notes)
        self.assertIn("Universe / SFE picture", extra)
        self.assertIn("not a proof", narrative)
        self.assertLess(narrative.find("program status"), narrative.find("abstract syntax tree"))
        self.assertNotIn("withdrawn", notes.lower())
        self.assertNotIn("tombstoned", notes.lower())
        self.assertNotIn("proves the riemann", narrative)
        self.assertNotIn("clay statement", narrative)

    def test_poisson_is_not_a_universe_claim(self) -> None:
        report = audit_expression("∇²Φ = 4π G ρ")
        extra = " ".join(report.extra_structures)
        self.assertNotIn("Universe / SFE picture", extra)
        self.assertEqual(report.canonical_sfe_status, "unresolved")


class UniverseDoesNotDrain(unittest.TestCase):
    def test_inquire_stays_on_da_and_refuses_chatvault(self) -> None:
        payload = inquire(UNIVERSE_PROMPT, drain=True)
        self.assertEqual(payload["lane"], "inquiry")
        self.assertIsNone(payload["drain"])
        self.assertFalse(payload["chatvault"])
        self.assertIn("Not filed into ChatVault", payload["drain_refused"])
        self.assertEqual(payload["universe"]["status"], "unresolved")
        self.assertFalse(payload["universe"]["proof"])
        notes = " ".join(payload["audit"]["notes"])
        self.assertIn("unresolved", notes.lower())
        self.assertNotIn("PROVED", json.dumps(payload))


class UniverseHomepage(unittest.TestCase):
    def test_hero_is_a_live_desk_not_a_retraction(self) -> None:
        html = _HOME.read_text(encoding="utf-8")
        lowered = html.lower()
        for phrase in _FORBIDDEN_PUBLIC:
            self.assertNotIn(phrase, lowered)
        self.assertIn(
            "Domain Architect is inquiry. Paste an equation; see roles, collisions, and what remains open.",
            html,
        )
        self.assertIn("ChatVault is search. Same origin, not the same engine.", html)
        self.assertIn("10.5281/zenodo.22050963", html)
        self.assertIn("10.5281/zenodo.22050974", html)
        self.assertIn("10.5281/zenodo.22050976", html)
        self.assertIn("10.5281/zenodo.22050962", html)
        self.assertIn("Q1-augmented swirl; not Clay", html)
        self.assertIn(
            "The universe / SFE / unified picture is unresolved.",
            html,
        )
        self.assertIn("There is no theory of everything, and no “one Hamiltonian, three prizes.”", html)
        self.assertIn("June 2026 posters remain on the desk as a dated archive.", html)
        self.assertIn("da-universe-card", html)
        self.assertIn("da-inquire-universe", html)
        self.assertIn("does not file into ChatVault", html)
        self.assertIn("da-load-route-c", html)
        self.assertIn("/faces/05_route_c_conditional.pdf", html)
        js = _JS.read_text(encoding="utf-8")
        self.assertIn("da-inquire-universe", js)
        self.assertIn("/api/universe", js)
        self.assertIn("runInquiry(false)", js)

    def test_program_note_is_linked_and_calm(self) -> None:
        readme = _README.read_text(encoding="utf-8")
        program = _PROGRAM.read_text(encoding="utf-8")
        self.assertIn("UNIVERSE-PROGRAM.md", readme)
        self.assertIn("What is live", program)
        self.assertIn("What is open", program)
        self.assertIn("What Domain Architect is for", program)
        self.assertIn("What is not claimed", program)
        lowered = program.lower()
        for phrase in _FORBIDDEN_PUBLIC:
            self.assertNotIn(phrase, lowered)
        self.assertIn(DOI_ROUTE_C, program)
        self.assertIn("dated archive", program.lower())


class UniverseCli(unittest.TestCase):
    def test_universe_flag_json(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--universe", "--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "unresolved")
        self.assertFalse(payload["proof"])
        self.assertFalse(payload["chatvault"])
        notes = " ".join(payload["audit"]["notes"])
        self.assertIn("unresolved", notes.lower())

    def test_drain_flag_refuses_universe(self) -> None:
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(["--drain-chatvault", UNIVERSE_PROMPT, "--json"])
        self.assertEqual(rc, 0)
        self.assertIn("Not filed into ChatVault", err.getvalue())
        payload = json.loads(out.getvalue())
        self.assertNotEqual(payload.get("format"), "chatvault-export")
        self.assertIn("unresolved", " ".join(payload["notes"]).lower())


class UniverseHttp(unittest.TestCase):
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

    def test_api_and_inquiry_without_drain(self) -> None:
        with urllib.request.urlopen(f"{self.origin}/api/universe") as res:
            meta = json.loads(res.read().decode("utf-8"))
        self.assertEqual(meta["status"], "unresolved")
        self.assertFalse(meta["proof"])
        self.assertEqual(meta["not_engine"], "chatvault")

        req = urllib.request.Request(
            f"{self.origin}/api/inquiry",
            data=json.dumps({"inquiry": UNIVERSE_PROMPT, "drain": True}).encode(
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
        self.assertIn("unresolved", " ".join(inq["audit"]["notes"]).lower())
        self.assertIn("Not filed into ChatVault", inq["drain_refused"])

        with urllib.request.urlopen(f"{self.origin}/") as home:
            html = home.read().decode("utf-8")
        self.assertIn("da-program", html)
        self.assertIn("da-universe-card", html)
        self.assertNotIn("tombstoned", html.lower())


if __name__ == "__main__":
    unittest.main()
