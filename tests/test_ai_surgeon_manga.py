#!/usr/bin/env python3
"""Gift manga follows the writer's story, Japanese leads, wholesome ending."""

from __future__ import annotations

import socket
import threading
import unittest
from contextlib import closing
from http.client import HTTPConnection
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANGA = ROOT / "ai_surgeon" / "manga"


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class TestMangaGift(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = (MANGA / "index.html").read_text(encoding="utf-8")
        cls.readmes = (MANGA / "README.md").read_text(encoding="utf-8")

    def test_files_and_art(self):
        self.assertTrue((MANGA / "index.html").is_file())
        self.assertTrue((MANGA / "README.md").is_file())
        for name in (
            "manga_cover_kuroto.png",
            "manga_ch01_sky.png",
            "manga_ch03_oracle.png",
            "manga_ch05_ants.png",
            "manga_ch12_residue.png",
        ):
            path = MANGA / "art" / name
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 50_000, name)

    def test_japanese_leads_and_same_spine(self):
        h = self.html
        self.assertIn("奥村 淳", h)
        self.assertIn("ソロモン先生", h)
        self.assertIn("霧花", h)
        self.assertIn("キラナ", h)
        self.assertIn("海斗", h)
        self.assertIn("花", h)
        self.assertIn("1023", h)
        self.assertIn("There is no Warrior", h)
        self.assertIn("Just the Surgeon", h)
        self.assertIn("LADY OF THE LAKE", h)
        self.assertIn("It all comes back to you", h)
        self.assertIn("I followed her through the mist of Avalon", h)

    def test_wholesome_gift_ending(self):
        h = self.html.lower()
        self.assertIn("for my daughter and my son", h)
        self.assertIn("residue of love", h)
        self.assertIn("残り香は、愛だった", self.html)
        self.assertIn("good conquers evil", h)
        self.assertIn("look first", h)
        self.assertNotIn("whiskey", h)
        self.assertNotIn("nude", h)

    def test_maps_original_beats(self):
        r = self.readmes
        self.assertIn("01 空の上", r)
        self.assertIn("12 愛の残り香", r)
        self.assertIn("Warrior-Surgeon.extracted.txt", r)

    def test_not_dumped_into_playable_cases(self):
        proto = (ROOT / "ai_surgeon" / "ai-surgeon-prototype.html").read_text(
            encoding="utf-8", errors="replace"
        )
        trauma = (ROOT / "ai_surgeon" / "ai-surgeon-module02-trauma.html").read_text(
            encoding="utf-8", errors="replace"
        )
        self.assertNotIn("奥村", proto)
        self.assertNotIn("キラナ", trauma)


class TestMangaServe(unittest.TestCase):
    def test_loopback_serves_manga(self):
        from ai_surgeon.serve import SurgeonHandler
        from http.server import ThreadingHTTPServer

        port = _free_port()
        httpd = ThreadingHTTPServer(("127.0.0.1", port), SurgeonHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            conn = HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("GET", "/manga/")
            res = conn.getresponse()
            body = res.read().decode("utf-8", errors="replace")
            self.assertEqual(res.status, 200)
            self.assertIn("黒塔と湖", body)
            conn.request("GET", "/manga/art/manga_cover_kuroto.png")
            res = conn.getresponse()
            png = res.read()
            self.assertEqual(res.status, 200)
            self.assertGreater(len(png), 50_000)
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
