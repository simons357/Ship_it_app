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


class TestStoryboard(unittest.TestCase):
    def test_twelve_chapters_and_dojo_skills(self):
        board = json.loads((ENG / "storyboard.json").read_text(encoding="utf-8"))
        self.assertEqual(board["title"], "黒塔と湖")
        self.assertEqual(board["style"]["look"], "speed-racer-cel")
        self.assertEqual(len(board["chapters"]), 12)
        self.assertEqual(board["engines"]["budget_team"], "godot4")
        self.assertEqual(board["engines"]["later_studio"], "unreal5")
        ids = [c["id"] for c in board["chapters"]]
        self.assertEqual(ids[0], "ch01")
        self.assertEqual(ids[-1], "ch12")
        skills = board["dojo"]["skills"]
        kinds = {s["id"]: s["kind"] for s in skills}
        self.assertEqual(kinds["leopard"], "hold")
        self.assertEqual(kinds["tai_chi"], "slow_sequence")
        self.assertIn("broom", board["dojo"]["weapons_from_the_room"])
        self.assertNotIn("katana_mall", board["dojo"]["weapons_from_the_room"])
        self.assertIn("There is no Warrior", board["moral"]["solomon"])

    def test_godot_and_unreal_are_not_fake_unreal_projects(self):
        self.assertTrue((ENG / "godot" / "project.godot").is_file())
        self.assertTrue((ENG / "godot" / "scripts" / "Dojo.gd").is_file())
        self.assertTrue((ENG / "godot" / "data" / "storyboard.json").is_file())
        unreal = (ENG / "unreal" / "README.md").read_text(encoding="utf-8")
        self.assertIn("DataTable", unreal)
        self.assertIn("not a fake", unreal.lower())
        self.assertFalse(list(ENG.joinpath("unreal").glob("*.uproject")))


class TestDojoPage(unittest.TestCase):
    def test_html_and_art(self):
        html = (ROOT / "ai_surgeon" / "dojo.html").read_text(encoding="utf-8")
        self.assertIn("dojo.js", html)
        self.assertIn("engine/storyboard.json", html)
        self.assertIn("leopard", html.lower())
        self.assertIn("tai chi", html.lower())
        art = ROOT / "ai_surgeon" / "art" / "dojo_speed_racer_style.png"
        self.assertTrue(art.is_file())
        self.assertGreater(art.stat().st_size, 20_000)

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
            conn.request("GET", "/engine/storyboard.json")
            res = conn.getresponse()
            board = json.loads(res.read().decode("utf-8"))
            self.assertEqual(res.status, 200)
            self.assertEqual(len(board["chapters"]), 12)
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
