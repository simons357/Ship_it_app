#!/usr/bin/env python3
"""Chronogate chrome, hub stills, citations bible, and the empty field-demo slot."""

from __future__ import annotations

import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

from ai_surgeon.serve import SurgeonHandler

ROOT = Path(__file__).resolve().parents[1]
SURGEON = ROOT / "ai_surgeon"
HUB = SURGEON / "index.html"
CREDITS = SURGEON / "credits.html"
ART = SURGEON / "art"
CITES = SURGEON / "docs" / "bible" / "AI-Surgeon-Final-With-Citations.txt"

HUB_ART = (
    "surgery-verse.png",
    "hardware-ladder.png",
    "anesthesia-the-pen.png",
    "identify-before-you-cut.png",
    "biomechanical-ai-key.webp",
    "cg-reticle-logo.png",
    "chronogate-wordmark.png",
)


class TestHubArtOnDisk(unittest.TestCase):
    def test_seven_drop_stills_exist(self):
        for name in HUB_ART:
            path = ART / name
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 20_000, name)

    def test_manifest_lists_the_same_seven(self):
        data = json.loads((ART / "HUB-ART.json").read_text(encoding="utf-8"))
        files = [p["file"].split("/", 1)[-1] for p in data["pieces"]]
        self.assertEqual(files, list(HUB_ART))
        self.assertEqual(data["video"]["status"], "missing")
        self.assertEqual(data["studio"], "Chronogate")
        self.assertIn("Not a medical device", data["note"])


class TestBrandLock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hub = HUB.read_text(encoding="utf-8")
        cls.credits = CREDITS.read_text(encoding="utf-8")

    def test_cg_logo_is_chrome_ai_surgeon_is_the_game(self):
        self.assertIn("art/cg-reticle-logo.png", self.hub)
        self.assertIn("brandmark cg", self.hub)
        self.assertIn("<h1>AI Surgeon</h1>", self.hub)
        self.assertIn("art/cg-reticle-logo.png", self.credits)

    def test_chronogate_lock_on_hub_and_credits(self):
        for body in (self.hub, self.credits):
            self.assertIn("Chronogate", body)
            self.assertIn("The Field Journal", body)
            self.assertIn("Prime Field Technologies", body)
            self.assertIn("CHRONOGATE", body.upper())

    def test_gallery_and_identify_and_verse_and_ladder(self):
        for path in (
            "art/surgery-verse.png",
            "art/hardware-ladder.png",
            "art/anesthesia-the-pen.png",
            "art/identify-before-you-cut.png",
            "art/biomechanical-ai-key.webp",
            "art/chronogate-wordmark.png",
        ):
            self.assertIn(path, self.hub)

    def test_demo_slot_is_labeled_and_does_not_invent_footage(self):
        self.assertIn('id="field-demo-slot"', self.hub)
        self.assertIn("8098483949091603692 2.MP4", self.hub)
        self.assertIn("Footage is not invented", self.hub)
        self.assertNotIn('<video', self.hub.lower())
        mp4s = list(ART.glob("*.mp4")) + list(ART.glob("*.MP4")) + list(ART.glob("*.webm"))
        self.assertEqual(mp4s, [])

    def test_not_a_cleared_device_and_not_foreign_products(self):
        h = self.hub.lower()
        self.assertIn("not a medical device", h)
        self.assertIn("not a cleared medical device", h)
        self.assertIn("not chatvault", h)
        self.assertIn("not rh", h)

    def test_credits_page_exists(self):
        self.assertTrue(CREDITS.is_file())
        self.assertIn('href="credits.html"', self.hub)
        self.assertIn("Not a cleared medical device", self.credits)


class TestCitationsBibleAndSystems(unittest.TestCase):
    def test_citations_bible_is_the_1e55_drop(self):
        self.assertTrue(CITES.is_file())
        body = CITES.read_text(encoding="utf-8", errors="replace")
        self.assertIn("11. References & Citations", body)
        self.assertIn("Market Research Future (2024)", body)
        self.assertIn("Harvard Medical School (2023)", body)

    def test_systems_runtime_still_has_the_shared_engine(self):
        js = (SURGEON / "ai-surgeon-systems.js").read_text(encoding="utf-8")
        self.assertIn("AISS.RETENTION = 'derived-band-only'", js)
        self.assertIn("AISS.Humor", js)
        self.assertIn("AISS.Handover", js)
        self.assertGreater(js.count("\n"), 1000)


class TestBrandServed(unittest.TestCase):
    def test_loopback_serves_webp_logo_credits_and_cites(self):
        import socket
        from contextlib import closing

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.bind(("127.0.0.1", 0))
            port = int(sock.getsockname()[1])
        httpd = ThreadingHTTPServer(("127.0.0.1", port), SurgeonHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            conn = HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("GET", "/art/cg-reticle-logo.png")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertEqual(res.getheader("Content-Type"), "image/png")
            self.assertGreater(len(res.read()), 20_000)

            conn.request("GET", "/art/biomechanical-ai-key.webp")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertEqual(res.getheader("Content-Type"), "image/webp")
            self.assertGreater(len(res.read()), 20_000)

            conn.request("GET", "/credits.html")
            res = conn.getresponse()
            body = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("CHRONOGATE", body)

            conn.request("GET", "/docs/bible/AI-Surgeon-Final-With-Citations.txt")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertIn(b"References & Citations", res.read())
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
