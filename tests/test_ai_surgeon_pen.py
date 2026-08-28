#!/usr/bin/env python3
"""The Pen: one stylus, two modes, mapped gestures — not a toy tray."""

from __future__ import annotations

import socket
import threading
import unittest
from contextlib import closing
from http.client import HTTPConnection
from pathlib import Path

from ai_surgeon.screens_engine import (
    curriculum_can_do_one,
    curriculum_can_see_one,
    pen_action,
    pen_gates,
    pen_matches,
    pen_normalize,
    pen_resolve,
    pen_score,
)

ROOT = Path(__file__).resolve().parents[1]
SURGEON = ROOT / "ai_surgeon"


class TestPenSpec(unittest.TestCase):
    def test_spec_is_theirs_not_arthurian(self):
        spec = (SURGEON / "docs" / "THE-PEN.md").read_text(encoding="utf-8")
        low = spec.lower()
        self.assertIn("one object in the hand", low)
        self.assertIn("twist", low)
        self.assertIn("click the top", low)
        self.assertIn("squeeze", low)
        self.assertIn("see one", low)
        self.assertIn("do one", low)
        self.assertIn("exploration", low)
        self.assertIn("curriculum", low)
        self.assertIn("coherence", low)
        self.assertIn("vision", low)
        self.assertIn("not a medical device", low)
        self.assertIn("language", low)
        self.assertIn("kelly", low)
        self.assertIn("not harrison", low)
        self.assertNotIn("excalibur", low)
        self.assertNotIn("avalon", low)

    def test_theirs_points_at_the_pen(self):
        theirs = (SURGEON / "docs" / "THEIRS-medical-big-picture.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("THE-PEN.md", theirs)
        self.assertIn("pen.html", theirs)


class TestPenRules(unittest.TestCase):
    def test_aliases_map_onto_existing_actions(self):
        self.assertTrue(pen_matches("click", "swipe"))
        self.assertTrue(pen_matches("click", "tap"))
        self.assertTrue(pen_matches("squeeze", "pinch"))
        self.assertTrue(pen_matches("squeeze", "spread"))
        self.assertTrue(pen_matches("squeeze", "hold"))
        self.assertFalse(pen_matches("click", "hold"))
        self.assertEqual(pen_resolve("squeeze", "pinch"), "pinch")
        self.assertEqual(pen_normalize("swipe"), "click")
        self.assertEqual(pen_action("click", "knife"), "incise")
        self.assertEqual(pen_action("squeeze", "clamp"), "clamp")
        self.assertEqual(pen_action("squeeze", "retract"), "retract")
        self.assertEqual(pen_action("squeeze", "ligate"), "ligate")
        self.assertEqual(pen_action("twist"), "choose")

    def test_exploration_zero_penalty_curriculum_counts(self):
        self.assertEqual(pen_score("exploration", -8), 0)
        self.assertEqual(pen_score("exploration", 25), 25)
        self.assertEqual(pen_score("curriculum", -8), -8)
        self.assertEqual(pen_score("curriculum", 25), 25)

    def test_curriculum_gates_lab_then_see_then_do(self):
        self.assertFalse(curriculum_can_see_one(False))
        self.assertTrue(curriculum_can_see_one(True))
        self.assertFalse(curriculum_can_do_one(True, False))
        self.assertTrue(curriculum_can_do_one(True, True))
        explore = pen_gates("exploration", False, False)
        self.assertTrue(explore["can_do_one"])
        self.assertEqual(explore["penalty"], 0)
        self.assertFalse(explore["clock"])
        curr = pen_gates("curriculum", False, False)
        self.assertFalse(curr["can_do_one"])
        self.assertEqual(curr["penalty"], 1)
        self.assertTrue(curr["clock"])


class TestPenHubAndScreen(unittest.TestCase):
    def test_hub_card_and_toggle_copy(self):
        hub = (SURGEON / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="the-pen"', hub)
        self.assertIn('id="pen-card"', hub)
        self.assertIn('href="pen.html"', hub)
        self.assertIn("docs/THE-PEN.md", hub)
        self.assertIn("Exploration", hub)
        self.assertIn("Curriculum", hub)
        self.assertIn("zero penalty", hub.lower())
        self.assertIn("must study in the Lab", hub)
        self.assertIn("cannot make a phone stylus feel like a Kelly", hub)
        self.assertIn("twist to choose, touch to commit", hub.lower())
        self.assertNotIn("John Occam", hub)
        self.assertNotIn("Excalibur", hub)

    def test_pen_html_has_mode_gates_vision_honest(self):
        html = (SURGEON / "pen.html").read_text(encoding="utf-8")
        self.assertIn("ai-surgeon-systems.js", html)
        self.assertIn('id="btn-explore"', html)
        self.assertIn('id="btn-curr"', html)
        self.assertIn('id="gate-lab"', html)
        self.assertIn('id="gate-see"', html)
        self.assertIn('id="gate-do"', html)
        self.assertIn('data-pen="twist"', html)
        self.assertIn('data-pen="click"', html)
        self.assertIn('data-pen="squeeze"', html)
        self.assertIn("not a cleared tracker", html.lower())
        self.assertIn("not a medical device", html.lower())
        self.assertIn("stills/10-twist-stylus.png", html)
        self.assertNotIn("Avalon", html)

    def test_systems_and_prototypes_wire_pen_without_dropping_cases(self):
        systems = (SURGEON / "ai-surgeon-systems.js").read_text(encoding="utf-8")
        self.assertIn("AISS.Mode", systems)
        self.assertIn("exploration", systems)
        self.assertIn("curriculum", systems)
        self.assertIn("AISS.Pen", systems)
        self.assertIn("AISS.Vision", systems)
        self.assertIn("CLEARED: false", systems)
        self.assertIn("not cleared", systems.lower())
        proto = (SURGEON / "ai-surgeon-prototype.html").read_text(encoding="utf-8")
        trauma = (SURGEON / "ai-surgeon-module02-trauma.html").read_text(encoding="utf-8")
        for body in (proto, trauma):
            self.assertIn('id="penpad"', body)
            self.assertIn("AISS.Pen.resolve", body)
            self.assertIn("AISS.Mode.score", body)
        self.assertIn("McBurney", proto)
        self.assertIn("thoracostomy", trauma.lower())
        self.assertNotIn("Lady of the Lake", proto)
        self.assertNotIn("Avalon", systems)


class TestPenServed(unittest.TestCase):
    def test_loopback_serves_pen_and_spec(self):
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
            conn.request("GET", "/pen.html")
            res = conn.getresponse()
            body = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("The Pen", body)
            self.assertIn("Exploration", body)
            conn.request("GET", "/docs/THE-PEN.md")
            res = conn.getresponse()
            spec = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("min-movement", spec.lower())
            conn.request("GET", "/")
            res = conn.getresponse()
            hub = res.read().decode("utf-8", errors="replace")
            self.assertIn("pen.html", hub)
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
