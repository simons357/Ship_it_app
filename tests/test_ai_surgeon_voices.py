#!/usr/bin/env python3
"""Two voices stay split: THEIRS = medical big picture; Harrison's = Lady of the Lake."""

from __future__ import annotations

import hashlib
import socket
import threading
import unittest
from contextlib import closing
from http.client import HTTPConnection
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURGEON = ROOT / "ai_surgeon"
DOCS = SURGEON / "docs"
BLOB = DOCS / "warrior-surgeon"
THEIRS = DOCS / "THEIRS-medical-big-picture.md"
HARRISONS = DOCS / "HARRISONS-arthurian-lady-of-the-lake.md"
LOCK = DOCS / "VOICE-LOCK.md"
HUB = SURGEON / "index.html"
CREDITS = SURGEON / "credits.html"

IDENTICAL_MD5 = "08bca7fbdf5ed9f27da7bdf13e80ddc3"
UPLOADS = Path("/home/ubuntu/.cursor/projects/workspace/uploads")


def _flat(text: str) -> str:
    return (
        text.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .lower()
    )


class TestBlobWasOneFileThenSplit(unittest.TestCase):
    def test_both_uploads_match_the_stored_docx(self):
        stored = (BLOB / "Warrior_Surgeon.docx").read_bytes()
        self.assertEqual(hashlib.md5(stored).hexdigest(), IDENTICAL_MD5)
        for name in ("Warrior_Surgeon__a2aa.docx", "Warrior_Surgeon__2_e010.docx"):
            upload = UPLOADS / name
            if upload.is_file():
                self.assertEqual(hashlib.md5(upload.read_bytes()).hexdigest(), IDENTICAL_MD5)

    def test_extract_and_manifest_name_the_identical_blob(self):
        extract = (BLOB / "Warrior-Surgeon.extracted.txt").read_text(encoding="utf-8")
        manifest = (BLOB / "MANIFEST.txt").read_text(encoding="utf-8")
        self.assertIn("priestess of Avalon", extract)
        self.assertIn("There is no Warrior. Just the Surgeon.", extract)
        self.assertIn(IDENTICAL_MD5, manifest)
        self.assertIn("IDENTICAL", manifest)


class TestVoiceSplit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.theirs = THEIRS.read_text(encoding="utf-8")
        cls.harrisons = HARRISONS.read_text(encoding="utf-8")
        cls.lock = LOCK.read_text(encoding="utf-8")

    def test_files_are_labeled(self):
        t, h, lock = _flat(self.theirs), _flat(self.harrisons), _flat(self.lock)
        self.assertIn("theirs — medical big picture", t)
        self.assertIn("this is the user's voice", t)
        self.assertIn("harrison's — arthurian lady of the lake", h)
        self.assertIn("this is harrison's voice", h)
        self.assertIn("theirs", lock)
        self.assertIn("harrison", lock)

    def test_theirs_is_the_playable_medical_product(self):
        t = _flat(self.theirs)
        for needle in (
            "identify before you cut",
            "physiology",
            "trauma",
            "anaesthesia",
            "coherence",
            "death-enabled",
            "playable product",
            "ai-surgeon-prototype.html",
            "ai-surgeon-module02-trauma.html",
        ):
            self.assertIn(needle, t)
        self.assertIn("there is no warrior. just the surgeon.", t)
        self.assertIn("unless he's dying, fix him.", t)

    def test_harrisons_is_lady_of_the_lake_not_an_or_reskin(self):
        h = _flat(self.harrisons)
        self.assertIn("priestess of avalon", h)
        self.assertIn("lady of the lake", h)
        self.assertIn("welcome to avalon.", h)
        self.assertIn("consciousness is liquid.", h)
        self.assertIn("gives the sword", h)
        self.assertIn("not a fantasy reskin of the or", h)
        self.assertIn("i followed her through the mist of avalon", h)
        self.assertNotIn("mcburney", h)
        self.assertNotIn("tube thoracostomy", h)

    def test_does_not_invent_harrison_quotations(self):
        cites = (DOCS / "CITATIONS.md").read_text(encoding="utf-8")
        for body in (self.harrisons, self.lock, cites):
            low = _flat(body)
            self.assertIn("do not invent", low)
            self.assertNotIn("21st edition", low)
            self.assertNotIn("21st ed", low)
            self.assertNotIn("doi.org", low)
            self.assertNotRegex(body, r"Harrison.s Principles of Internal Medicine,\s+p\.\s*\d+")

    def test_blob_never_named_harrison_or_excalibur(self):
        extract = (BLOB / "Warrior-Surgeon.extracted.txt").read_text(encoding="utf-8")
        self.assertNotIn("Harrison", extract)
        self.assertNotIn("Excalibur", extract)
        self.assertIn("never says", _flat(self.harrisons))


class TestHubAndCreditsCarryBothBeats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hub = HUB.read_text(encoding="utf-8")
        cls.credits = CREDITS.read_text(encoding="utf-8")

    def test_one_medical_line_and_one_lake_line(self):
        for body in (self.hub, self.credits):
            self.assertIn('id="two-voices"', body)
            self.assertIn('id="medical-big-picture"', body)
            self.assertIn('id="harrisons-lake"', body)
            self.assertIn("what the playable product is", body.lower())
            self.assertIn("gives the sword from the water", body.lower())
            self.assertIn("not a fantasy reskin of the OR", body)

    def test_chronogate_cyan_gold_stays_lake_is_atmosphere(self):
        self.assertIn("art/cg-reticle-logo.png", self.hub)
        self.assertIn("--cyan:#3fd0e8", self.hub)
        self.assertIn("--gold:#d4af37", self.hub)
        self.assertIn("radial-gradient", self.hub)
        self.assertIn("atmosphere", self.hub.lower())
        self.assertIn("Chronogate", self.credits)
        self.assertIn("art/cg-reticle-logo.png", self.credits)

    def test_not_foreign_products_or_a_device(self):
        h = self.hub.lower()
        self.assertIn("not a medical device", h)
        self.assertIn("not chatvault", h)
        self.assertIn("not rh", h)


class TestSiblingsNotClobbered(unittest.TestCase):
    def test_playable_cases_and_systems_still_there(self):
        proto = (SURGEON / "ai-surgeon-prototype.html").read_text(encoding="utf-8")
        trauma = (SURGEON / "ai-surgeon-module02-trauma.html").read_text(encoding="utf-8")
        systems = (SURGEON / "ai-surgeon-systems.js").read_text(encoding="utf-8")
        self.assertIn("McBurney", proto)
        self.assertIn("thoracostomy", trauma.lower())
        self.assertIn("AISS", systems)
        self.assertGreater(systems.count("\n"), 1000)
        self.assertNotIn("Lady of the Lake", proto)
        self.assertNotIn("Lady of the Lake", trauma)
        self.assertNotIn("Avalon", systems)


class TestVoicesServed(unittest.TestCase):
    def test_loopback_serves_voice_docs_and_docx(self):
        from http.server import ThreadingHTTPServer

        from ai_surgeon.serve import SurgeonHandler

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.bind(("127.0.0.1", 0))
            port = int(sock.getsockname()[1])
        httpd = ThreadingHTTPServer(("127.0.0.1", port), SurgeonHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            conn = HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("GET", "/")
            res = conn.getresponse()
            hub = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("medical-big-picture", hub)
            self.assertIn("harrisons-lake", hub)

            conn.request("GET", "/docs/THEIRS-medical-big-picture.md")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertIn(b"medical big picture", res.read().lower())

            conn.request("GET", "/docs/HARRISONS-arthurian-lady-of-the-lake.md")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertIn(b"priestess of Avalon", res.read())

            conn.request("GET", "/docs/warrior-surgeon/Warrior_Surgeon.docx")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertIn("officedocument.wordprocessingml", res.getheader("Content-Type") or "")
            self.assertGreater(len(res.read()), 10_000)
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
