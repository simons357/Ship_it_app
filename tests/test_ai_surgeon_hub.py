#!/usr/bin/env python3
"""Hub copy follows the locked docs: playable cases stay playable; stubs stay stubs."""

from __future__ import annotations

import socket
import threading
import unittest
from contextlib import closing
from http.client import HTTPConnection
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "ai_surgeon" / "index.html"


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class TestHubCopy(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = HUB.read_text(encoding="utf-8")

    def test_identify_before_you_cut_and_phases(self):
        h = self.html.lower()
        self.assertIn("identify before you cut", h)
        self.assertIn("twist to choose, touch to commit", h)
        self.assertIn("study one", h)
        self.assertIn("see one", h)
        self.assertIn("do one", h)
        self.assertIn("teach one", h)
        self.assertIn("touch", h)
        self.assertIn("twist", h)

    def test_two_seats_one_case_not_a_metaverse(self):
        h = self.html.lower()
        self.assertIn("two seats of the same case", h)
        self.assertIn("surgeon", h)
        self.assertIn("anaesthesia", h)
        self.assertIn("scrub", h)

    def test_hardware_ladder(self):
        h = self.html.lower()
        self.assertIn("phone first", h)
        self.assertIn("tablet", h)
        self.assertIn("mat", h)
        self.assertIn("vr", h)

    def test_scoring_coherence_death_rules(self):
        h = self.html.lower()
        self.assertIn("10 points a card", h)
        self.assertIn("25 points a step", h)
        self.assertIn("40 points a step", h)
        self.assertIn("coherence", h)
        self.assertIn("disabled in entry", h)
        self.assertIn("enabled from trauma", h)
        self.assertIn("losing the patient", h)

    def test_playable_modules_still_linked(self):
        self.assertIn('href="ai-surgeon-prototype.html"', self.html)
        self.assertIn('href="ai-surgeon-module02-trauma.html"', self.html)
        self.assertIn("Open Appendectomy", self.html)
        self.assertIn("Tube Thoracostomy", self.html)
        self.assertIn("Playable", self.html)
        self.assertIn('href="phone.html"', self.html)
        self.assertIn("docs/WARRIOR-SURGEON.md", self.html)
        self.assertIn('href="pen.html"', self.html)
        self.assertIn("docs/THE-PEN.md", self.html)
        self.assertIn('href="manga/"', self.html)
        self.assertIn("For a daughter and a son", self.html)
        self.assertIn('href="dojo.html"', self.html)
        self.assertIn("Cartoon dojo", self.html)
        self.assertTrue((ROOT / "ai_surgeon" / "phone.html").is_file())
        self.assertTrue((ROOT / "ai_surgeon" / "ai-surgeon-prototype.html").is_file())
        self.assertTrue((ROOT / "ai_surgeon" / "ai-surgeon-module02-trauma.html").is_file())

    def test_warrior_surgeon_aligns_without_lore_dump(self):
        h = self.html
        self.assertIn("Look at the rib you are crossing before you cut", h)
        self.assertIn("Anaesthesia is a seat on this clock", h)
        self.assertNotIn("John Occam", h)
        self.assertNotIn("F-22", h)
        self.assertNotIn("Kyranna", h)
        self.assertNotIn("Black Tower", h)

    def test_honest_stubs_for_unbuilt(self):
        h = self.html
        for name in (
            "I&amp;D of a Finger",
            "Laparoscopic Cholecystectomy",
            "Inguinal Hernia",
            "Bowel Anastomosis",
            "Cricothyroidotomy",
            "Damage Control Laparotomy",
            "Cardiac — CABG",
            "Neurosurgery — Craniotomy",
            "Blame Anesthesia",
        ):
            self.assertIn(name, h)
        self.assertGreater(h.count("Pitch · not playable"), 6)
        # Stubs are not fake playable links.
        self.assertNotIn("href=\"ai-surgeon-module13", h)

    def test_non_claims_and_no_fake_store(self):
        h = self.html.lower()
        self.assertIn("not a medical device", h)
        self.assertIn("not a clinical reference", h)
        self.assertNotIn("stripe", h)
        self.assertIn("no checkout", h)
        self.assertNotIn("add to cart", h)

    def test_cite_strip_and_credit(self):
        self.assertIn("id=\"about-cites\"", self.html)
        self.assertIn("Harvard Medical School (2023)", self.html)
        self.assertIn("docs/CITATIONS.md", self.html)
        self.assertIn("Jonathan Simons, CRNA", self.html)
        self.assertIn("who the plans say pay", self.html.lower())

    def test_does_not_claim_chatvault_or_da(self):
        h = self.html.lower()
        self.assertIn("not chatvault", h)
        self.assertIn("not on domain architect", h)


class TestHubServe(unittest.TestCase):
    def test_loopback_serves_hub_and_bible(self):
        from ai_surgeon.serve import SurgeonHandler
        from http.server import ThreadingHTTPServer

        port = _free_port()
        httpd = ThreadingHTTPServer(("127.0.0.1", port), SurgeonHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            conn = HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("GET", "/")
            res = conn.getresponse()
            body = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("Identify before you cut", body)
            conn.request("GET", "/docs/CITATIONS.md")
            res = conn.getresponse()
            cites = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("Market Research Future (2024)", cites)
            conn.request("GET", "/docs/bible/AI-Surgeon-Final-With-Citations.txt")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


class TestPlayableHtmlUntouchedAsGames(unittest.TestCase):
    """Copy work is on the hub. The two playable cases must still exist as modules."""

    def test_appendectomy_and_trauma_files(self):
        proto = ROOT / "ai_surgeon" / "ai-surgeon-prototype.html"
        trauma = ROOT / "ai_surgeon" / "ai-surgeon-module02-trauma.html"
        self.assertTrue(proto.is_file())
        self.assertTrue(trauma.is_file())
        p = proto.read_text(encoding="utf-8", errors="replace")
        t = trauma.read_text(encoding="utf-8", errors="replace")
        self.assertIn("McBurney", p)
        self.assertIn("thoracostomy", t.lower())


if __name__ == "__main__":
    unittest.main()
