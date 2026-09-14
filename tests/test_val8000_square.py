#!/usr/bin/env python3
"""VAL8000 always-visible square dock in the Domain Architect view."""

from __future__ import annotations

import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from time import sleep

from domain_architect.app import DomainArchitectHandler

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "domain_architect" / "static"
DOCK = STATIC / "val8000"
LIVE_PY = ROOT / "domain_architect"

BANNED = (
    "HAL 9000",
    "HAL9000",
    "I'm sorry Dave",
    "I'm sorry, Dave",
    "pod bay",
    "Clay",
    "NAV-42",
    "Fluid-Q",
    "Chat Vault",
    "2.2 Hz",
    "val8000-mouth-teeth",
    "ns solved",
    "RH proved",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSquareLivesInTheDaView(unittest.TestCase):
    def test_index_docks_the_square_beside_the_shell(self) -> None:
        html = _read(STATIC / "index.html")
        self.assertIn('id="val8000-dock"', html)
        self.assertIn('class="val8000-square"', html)
        self.assertIn("val8000-mouth-line.png", html)
        self.assertIn("Help with unanswered", html)
        self.assertIn("Ask the Desk", html)
        self.assertIn("/val8000/val8000-dock.css", html)
        self.assertIn("/val8000/val8000-dock.js", html)
        self.assertLess(html.index('class="shell"'), html.index('id="val8000-dock"'))
        self.assertNotIn("val8000-mouth-teeth", html)
        self.assertNotIn("HAL 9000", html)
        self.assertIn("straight mouth line", html)

    def test_face_assets_are_the_idle_line_and_the_smile(self) -> None:
        line = DOCK / "val8000-mouth-line.png"
        smile = DOCK / "val8000-mouth-smile.png"
        self.assertTrue(line.is_file())
        self.assertTrue(smile.is_file())
        self.assertGreater(line.stat().st_size, 20_000)
        self.assertGreater(smile.stat().st_size, 20_000)
        self.assertNotEqual(line.read_bytes(), smile.read_bytes())
        self.assertFalse((DOCK / "val8000-mouth-teeth.png").exists())

    def test_css_keeps_a_square_in_the_layout(self) -> None:
        css = _read(DOCK / "val8000-dock.css")
        self.assertIn(".val8000-dock", css)
        self.assertIn("7.2rem", css)
        self.assertIn("position: sticky", css)
        self.assertNotIn("display: none", css.split(".val8000-square")[1][:400])


class TestUnansweredHelp(unittest.TestCase):
    def test_js_helps_blank_fields_without_inventing_theorems(self) -> None:
        js = _read(DOCK / "val8000-dock.js")
        self.assertIn("helpUnanswered", js)
        self.assertIn("Help with unanswered", _read(STATIC / "index.html"))
        self.assertIn("decExpr", js)
        self.assertIn("trLeft", js)
        self.assertIn("syTarget", js)
        self.assertIn("cyExciseK", js)
        self.assertIn("val8000-ask", js)
        self.assertIn("DA-VC-01 stays FAIL", js)
        self.assertIn("TRANSFORMABLE without a real T", js)
        self.assertIn("Unaugmented leftover stays OPEN", js)
        self.assertIn("I do not invent theorems", js)
        self.assertIn("setMouth", js)
        self.assertIn("val8000-mouth-smile.png", js)
        self.assertIn("val8000-mouth-line.png", js)
        self.assertNotIn("val8000-mouth-teeth", js)
        for phrase in BANNED:
            self.assertNotIn(phrase, js, phrase)

    def test_live_python_still_does_not_name_him(self) -> None:
        for path in LIVE_PY.rglob("*.py"):
            blob = path.read_text(encoding="utf-8")
            self.assertNotIn("VAL8000", blob)
            self.assertNotIn("val8000", blob)


class TestDockIsServed(unittest.TestCase):
    def test_local_app_serves_the_square_and_the_line_png(self) -> None:
        port = 0
        server = ThreadingHTTPServer(("127.0.0.1", port), DomainArchitectHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        sleep(0.15)
        port = server.server_address[1]
        try:
            conn = HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("GET", "/")
            home = conn.getresponse()
            body = home.read().decode("utf-8")
            self.assertEqual(home.status, 200)
            self.assertIn("val8000-dock", body)
            self.assertIn("Help with unanswered", body)
            conn.request("GET", "/val8000/val8000-mouth-line.png")
            png = conn.getresponse()
            data = png.read()
            self.assertEqual(png.status, 200)
            self.assertEqual(png.getheader("Content-Type"), "image/png")
            self.assertGreater(len(data), 20_000)
            conn.request("GET", "/val8000/val8000-dock.js")
            js = conn.getresponse()
            self.assertEqual(js.status, 200)
            self.assertIn("helpUnanswered", js.read().decode("utf-8"))
            conn.close()
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
