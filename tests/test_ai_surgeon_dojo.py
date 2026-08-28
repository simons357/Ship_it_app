#!/usr/bin/env python3
"""Storyboard JSON feeds the cartoon dojo; Godot skeleton exists; Unreal is import notes."""

from __future__ import annotations

import json
import socket
import threading
import unittest
from contextlib import closing
from http.client import HTTPConnection
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENG = ROOT / "ai_surgeon" / "engine"
SURGEON = ROOT / "ai_surgeon"


class TestStoryboard(unittest.TestCase):
    def test_twelve_chapters_and_dojo_skills(self):
        board = json.loads((ENG / "storyboard.json").read_text(encoding="utf-8"))
        self.assertEqual(board["title"], "黒塔と湖")
        self.assertEqual(board["style"]["look"], "speed-racer-cel")
        self.assertEqual(len(board["chapters"]), 12)
        self.assertEqual(board["engines"]["budget_team"], "godot4")
        self.assertEqual(board["engines"]["later_studio"], "unreal5")
        self.assertEqual(board["engines"]["play_now"], "web-dojo")
        ids = [c["id"] for c in board["chapters"]]
        self.assertEqual(ids[0], "ch01")
        self.assertEqual(ids[-1], "ch12")
        skills = board["dojo"]["skills"]
        kinds = {s["id"]: s["kind"] for s in skills}
        self.assertEqual(list(kinds), ["leopard", "tai_chi", "surroundings", "spar"])
        self.assertEqual(kinds["leopard"], "hold")
        self.assertEqual(kinds["tai_chi"], "slow_sequence")
        self.assertEqual(kinds["surroundings"], "choose")
        self.assertEqual(kinds["spar"], "spar")
        self.assertIn("broom", board["dojo"]["weapons_from_the_room"])
        self.assertNotIn("katana_mall", board["dojo"]["weapons_from_the_room"])
        self.assertEqual(board["dojo"]["skills"][2]["options"], ["broom", "ribbon", "sand", "empty"])
        self.assertIn("There is no Warrior", board["moral"]["solomon"])
        self.assertTrue(board["respect"]["not_slurs"])
        self.assertTrue(board["respect"]["not_a_medical_device"])
        self.assertIn("David Carradine", board["respect"]["not_ip"])
        self.assertIn("F-35", board["respect"]["modernity"])
        self.assertIn("frame-diff", board["respect"]["camera"])
        self.assertIn("Not a medical device", board["dojo"]["disclaimer"])
        self.assertIn("David Carradine IP", board["dojo"]["not"])

    def test_godot_copy_matches_the_one_contract(self):
        src = json.loads((ENG / "storyboard.json").read_text(encoding="utf-8"))
        copy = json.loads((ENG / "godot" / "data" / "storyboard.json").read_text(encoding="utf-8"))
        self.assertEqual(src, copy)

    def test_godot_and_unreal_are_not_fake_unreal_projects(self):
        self.assertTrue((ENG / "godot" / "project.godot").is_file())
        self.assertTrue((ENG / "godot" / "scripts" / "Dojo.gd").is_file())
        self.assertTrue((ENG / "godot" / "data" / "storyboard.json").is_file())
        unreal = (ENG / "unreal" / "README.md").read_text(encoding="utf-8")
        self.assertIn("DataTable", unreal)
        self.assertIn("not a fake", unreal.lower())
        self.assertFalse(list(ENG.joinpath("unreal").glob("*.uproject")))
        gd = (ENG / "godot" / "scripts" / "Dojo.gd").read_text(encoding="utf-8")
        self.assertIn("func _draw", gd)
        self.assertIn("leopard", gd)
        self.assertIn("tai_chi", gd)
        self.assertIn("surroundings", gd)
        self.assertIn("spar", gd)
        self.assertIn("storyboard.json", gd)
        self.assertIn("Do not rebuild the 12 chapters", gd)


class TestDojoPage(unittest.TestCase):
    def test_html_and_art(self):
        html = (SURGEON / "dojo.html").read_text(encoding="utf-8")
        js = (SURGEON / "dojo.js").read_text(encoding="utf-8")
        self.assertIn("dojo.js", html)
        self.assertIn("engine/storyboard.json", html)
        self.assertIn("leopard", html.lower())
        self.assertIn("tai chi", html.lower())
        self.assertIn("broom", html.lower())
        self.assertIn("ribbon", html.lower())
        self.assertIn("f-35", html.lower())
        self.assertIn("frame-diff", html.lower())
        self.assertIn("not pose ai", html.lower())
        self.assertIn("not a medical device", html.lower())
        self.assertIn("not david carradine", html.lower())
        self.assertIn("not pt", html.lower())
        self.assertNotIn("tensorflow", js.lower())
        self.assertNotIn("mediapipe", js.lower())
        self.assertNotIn("pose-landmarker", js.lower())
        self.assertIn("drawJun", js)
        self.assertIn("drawPartner", js)
        self.assertIn("bowedIn", js)
        self.assertIn("prop-", js)
        self.assertIn("KurotoDojo", js)
        self.assertIn("sampleCam", js)
        art = SURGEON / "art" / "dojo_speed_racer_style.png"
        self.assertTrue(art.is_file())
        self.assertGreater(art.stat().st_size, 20_000)

    def test_hub_links_dojo_without_lore_dump(self):
        hub = (SURGEON / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="dojo.html"', hub)
        self.assertIn("Cartoon dojo", hub)
        self.assertIn("黒塔と湖", hub)
        self.assertNotIn("Black Tower", hub)
        self.assertNotIn("F-22", hub)
        self.assertNotIn("John Occam", hub)
        self.assertNotIn("Kyranna", hub)

    def test_loopback(self):
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
            conn.request("GET", "/dojo.html")
            res = conn.getresponse()
            body = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("DOJO", body)
            conn.request("GET", "/dojo.js")
            res = conn.getresponse()
            js = res.read().decode("utf-8")
            self.assertEqual(res.status, 200)
            self.assertIn("drawJun", js)
            conn.request("GET", "/engine/storyboard.json")
            res = conn.getresponse()
            board = json.loads(res.read().decode("utf-8"))
            self.assertEqual(res.status, 200)
            self.assertEqual(len(board["chapters"]), 12)
            conn.request("GET", "/engine/godot/project.godot")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertIn(b"Kuroto Dojo", res.read())
            conn.request("GET", "/art/dojo_speed_racer_style.png")
            res = conn.getresponse()
            self.assertEqual(res.status, 200)
            self.assertGreater(len(res.read()), 20_000)
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
