"""Hypothesized NS regularity realization and honest-mistake note stay in DA."""

from __future__ import annotations

import io
import json
import tempfile
import threading
import unittest
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from http.server import ThreadingHTTPServer
from pathlib import Path

from domain_architect.audit import audit_expression
from domain_architect.chatvault_bridge import inquire
from domain_architect.cli import main
from domain_architect.honest_mistake import (
    HONEST_MISTAKE_PARAGRAPH,
    HONEST_MISTAKE_PROMPT,
    LIVE_CITES,
    face as honest_face,
    looks_like_honest_mistake,
)
from domain_architect.ns_regularity_realization import (
    ALLOWED_CLASSES,
    CLASS_DOES_NOT_FOLLOW,
    CLASS_INDEPENDENT,
    CLASS_OBSTRUCTION,
    CLASS_OPEN,
    REALIZATION_PROMPT,
    experiment,
    insight_markdown,
    looks_like_ns_regularity_realization,
    write_outputs,
)
from domain_architect.ns_unaugmented import looks_like_ns_unaugmented
from domain_architect.site_server import SiteHandler
from domain_architect.universe import looks_like_universe_inquiry

_REPO = Path(__file__).resolve().parents[1]
_HOME = _REPO / "domain_architect" / "static" / "index.html"
_JS = _REPO / "domain_architect" / "static" / "da-home.js"
_DOCS = _REPO / "docs" / "domain-architect"
_JSON = _DOCS / "ns_regularity_realization.json"
_NOTE = _DOCS / "NS-REGULARITY-REALIZATION.md"
_HONEST_DOC = _DOCS / "HONEST-MISTAKE.md"

_EXPECTED = {
    "swirl_with_cancel": CLASS_INDEPENDENT,
    "swirl_without_cancel": CLASS_OPEN,
    "unaugmented_classical_ns": CLASS_OPEN,
    "snd": CLASS_DOES_NOT_FOLLOW,
    "ring_lemma": CLASS_DOES_NOT_FOLLOW,
    "gnc_goldbach": CLASS_DOES_NOT_FOLLOW,
    "bridge": CLASS_DOES_NOT_FOLLOW,
    "inverse_gcd_floor": CLASS_DOES_NOT_FOLLOW,
    "route_c": CLASS_OPEN,
    "track_b_mobius": CLASS_OBSTRUCTION,
    "sfe_universe": CLASS_OPEN,
    "q1_vs_classical": CLASS_INDEPENDENT,
}


class HonestMistakeCopy(unittest.TestCase):
    def test_paragraph_is_the_locked_note(self) -> None:
        self.assertTrue(looks_like_honest_mistake(HONEST_MISTAKE_PROMPT))
        self.assertTrue(looks_like_honest_mistake("honest mistake June 2026 treated"))
        self.assertFalse(looks_like_honest_mistake("∇²Φ = 4π G ρ"))
        self.assertFalse(looks_like_universe_inquiry(HONEST_MISTAKE_PROMPT))

        payload = honest_face()
        self.assertEqual(payload["paragraph"], HONEST_MISTAKE_PARAGRAPH)
        self.assertFalse(payload["proof"])
        self.assertFalse(payload["endorsed"])
        self.assertFalse(payload["rh_claimed"])
        self.assertFalse(payload["clay_ns_claimed"])
        self.assertFalse(payload["chatvault"])
        self.assertFalse(payload["titles_restamped"])
        self.assertIn("10.5281/zenodo.22050963", payload["paragraph"])
        self.assertIn("10.5281/zenodo.22050978", payload["paragraph"])
        self.assertIn("[Claim withdrawn]", payload["paragraph"])
        self.assertIn("titles were restored 26 Aug 2026", payload["paragraph"])
        blob = json.dumps(payload).lower()
        self.assertNotIn("tombstoned", blob)
        self.assertNotIn("crime tape", blob)
        self.assertNotIn("files were fake", payload["paragraph"].lower())
        self.assertNotIn("files were fake", " ".join(payload["notes"]).lower())
        for doi in LIVE_CITES:
            self.assertIn(doi, payload["live_cites"])

        html = _HOME.read_text(encoding="utf-8")
        self.assertIn("da-honest-mistake", html)
        self.assertIn("da-inquire-honest-mistake", html)
        self.assertIn(HONEST_MISTAKE_PARAGRAPH[:80], html.replace("\n", " "))
        self.assertIn("10.5281/zenodo.22050978", html)
        doc = _HONEST_DOC.read_text(encoding="utf-8")
        self.assertIn("That packaging does not hold", doc)
        self.assertNotIn("files were fake", doc.lower())
        self.assertNotIn("crime tape", doc.lower())


class RealizationClassifier(unittest.TestCase):
    def test_looks_like_is_not_the_open_ns_face(self) -> None:
        self.assertTrue(looks_like_ns_regularity_realization(REALIZATION_PROMPT))
        self.assertTrue(
            looks_like_ns_regularity_realization(
                "hypothesized realization of unconditional closed NS"
            )
        )
        self.assertFalse(looks_like_ns_unaugmented(REALIZATION_PROMPT))
        self.assertFalse(looks_like_universe_inquiry(REALIZATION_PROMPT))
        self.assertFalse(looks_like_ns_regularity_realization("∇²Φ = 4π G ρ"))
        self.assertFalse(
            looks_like_ns_regularity_realization(
                "classical unaugmented 3D Navier-Stokes OPEN"
            )
        )

    def test_classifies_every_finger_and_does_not_endorse(self) -> None:
        payload = experiment()
        self.assertFalse(payload["endorsed"])
        self.assertFalse(payload["theorem"])
        self.assertFalse(payload["proof"])
        self.assertFalse(payload["rh_claimed"])
        self.assertFalse(payload["clay_ns_claimed"])
        self.assertFalse(payload["chatvault"])
        self.assertEqual(payload["closed_fingers"], 0)
        self.assertEqual(payload["engine"], "domain_architect")
        ids = [row["id"] for row in payload["fingers"]]
        self.assertEqual(ids, list(_EXPECTED))
        self.assertEqual(payload["classifications"], _EXPECTED)
        for row in payload["fingers"]:
            self.assertIn(row["classification"], ALLOWED_CLASSES)
            self.assertFalse(row["closed_by_this_experiment"])
        self.assertEqual(payload["classifications"]["track_b_mobius"], CLASS_OBSTRUCTION)
        self.assertEqual(payload["classifications"]["swirl_with_cancel"], CLASS_INDEPENDENT)
        self.assertEqual(payload["classifications"]["q1_vs_classical"], CLASS_INDEPENDENT)
        blob = json.dumps(payload).lower()
        self.assertNotIn("clay ns is proved", blob)
        self.assertNotIn("rh is proved", blob)
        self.assertNotIn('"endorsed": true', blob)

        insight = insight_markdown(payload)
        self.assertIn("Q1 ≠ classical", insight)
        self.assertIn("Mertens bridge", insight)
        self.assertIn("1/(gcd√ij)", insight)
        self.assertIn("Beale–Kato–Majda", insight)
        self.assertIn("Keep fingers separate", insight)


class RealizationInquiry(unittest.TestCase):
    def test_audit_and_drain_refuse(self) -> None:
        report = audit_expression(REALIZATION_PROMPT)
        extra = " ".join(report.extra_structures)
        notes = " ".join(report.notes)
        self.assertIn("hypothesized NS regularity realization", extra)
        self.assertIn("not a theorem DA endorses", extra)
        self.assertIn("HYPOTHESIZED", notes)
        self.assertIn("track_b_mobius=obstruction", notes)
        self.assertNotIn("Universe / SFE picture", extra)
        self.assertEqual(report.canonical_sfe_status, "unresolved")

        payload = inquire(REALIZATION_PROMPT, drain=True)
        self.assertEqual(payload["lane"], "inquiry")
        self.assertIsNone(payload["drain"])
        self.assertFalse(payload["chatvault"])
        self.assertIn("Not filed into ChatVault", payload["drain_refused"])
        self.assertFalse(payload["ns_regularity_realization"]["endorsed"])
        self.assertEqual(
            payload["ns_regularity_realization"]["classifications"], _EXPECTED
        )
        self.assertNotIn("ns_unaugmented", payload)

        honest = inquire(HONEST_MISTAKE_PROMPT, drain=True)
        self.assertIsNone(honest["drain"])
        self.assertEqual(honest["honest_mistake"]["paragraph"], HONEST_MISTAKE_PARAGRAPH)
        self.assertIn("Not filed into ChatVault", honest["drain_refused"])


class RealizationCliAndDocs(unittest.TestCase):
    def test_cli_json_and_docs_match(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--ns-regularity-realization", "--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["classifications"], _EXPECTED)
        self.assertFalse(payload["endorsed"])
        self.assertIn("written", payload)

        self.assertTrue(_JSON.is_file())
        on_disk = json.loads(_JSON.read_text(encoding="utf-8"))
        self.assertEqual(on_disk["classifications"], _EXPECTED)
        self.assertFalse(on_disk["clay_ns_claimed"])
        self.assertTrue(_NOTE.is_file())
        note = _NOTE.read_text(encoding="utf-8")
        self.assertIn("`obstruction`", note)
        self.assertIn("next attempt", note.lower())

        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(["--drain-chatvault", REALIZATION_PROMPT, "--json"])
        self.assertEqual(rc, 0)
        self.assertIn("Not filed into ChatVault", err.getvalue())
        drained = json.loads(out.getvalue())
        self.assertNotEqual(drained.get("format"), "chatvault-export")

        honest_buf = io.StringIO()
        with redirect_stdout(honest_buf):
            rc = main(["--honest-mistake", "--json"])
        self.assertEqual(rc, 0)
        honest = json.loads(honest_buf.getvalue())
        self.assertEqual(honest["paragraph"], HONEST_MISTAKE_PARAGRAPH)

    def test_write_outputs_to_temp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            arts = Path(tmp) / "arts"
            written = write_outputs(docs_dir=docs, artifacts_dir=arts)
            self.assertTrue(written["docs_json"].is_file())
            self.assertTrue(written["artifacts_json"].is_file())
            data = json.loads(written["docs_json"].read_text(encoding="utf-8"))
            self.assertEqual(data["classifications"]["snd"], CLASS_DOES_NOT_FOLLOW)


class RealizationHomepage(unittest.TestCase):
    def test_desk_has_note_and_realization(self) -> None:
        html = _HOME.read_text(encoding="utf-8")
        js = _JS.read_text(encoding="utf-8")
        self.assertIn("da-honest-mistake", html)
        self.assertIn("da-ns-realization-card", html)
        self.assertIn("da-run-ns-realization", html)
        self.assertIn("da-inquire-honest-mistake", js)
        self.assertIn("/api/ns-regularity-realization", js)
        self.assertIn("/api/honest-mistake", js)
        self.assertIn("Hypothesized. Not endorsed. Not a proof.", html)
        self.assertNotIn("crime tape", html.lower())
        self.assertNotIn("files were fake", html.lower())


class RealizationHttp(unittest.TestCase):
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
        with urllib.request.urlopen(f"{self.origin}/api/ns-regularity-realization") as res:
            meta = json.loads(res.read().decode("utf-8"))
        self.assertFalse(meta["endorsed"])
        self.assertEqual(meta["classifications"], _EXPECTED)

        with urllib.request.urlopen(f"{self.origin}/api/honest-mistake") as res:
            note = json.loads(res.read().decode("utf-8"))
        self.assertEqual(note["paragraph"], HONEST_MISTAKE_PARAGRAPH)

        req = urllib.request.Request(
            f"{self.origin}/api/inquiry",
            data=json.dumps({"inquiry": REALIZATION_PROMPT, "drain": True}).encode(
                "utf-8"
            ),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as res:
            inq = json.loads(res.read().decode("utf-8"))
        self.assertEqual(inq["ok"], True)
        self.assertIsNone(inq["drain"])
        self.assertIn("Not filed into ChatVault", inq["drain_refused"])
        self.assertFalse(inq["ns_regularity_realization"]["clay_ns_claimed"])

        with urllib.request.urlopen(f"{self.origin}/") as home:
            html = home.read().decode("utf-8")
        self.assertIn("da-honest-mistake", html)
        self.assertIn("da-ns-realization-card", html)


if __name__ == "__main__":
    unittest.main()
