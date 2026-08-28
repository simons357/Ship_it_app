"""AI Surgeon hub, shared systems, and trauma loops — not ChatVault, not DA."""

from __future__ import annotations

import re
import subprocess
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from ai_surgeon import DEFAULT_PORT, ROOT
from ai_surgeon.serve import SurgeonHandler, public_path

_REPO = Path(__file__).resolve().parents[1]


def _get(origin: str, path: str) -> tuple[int, str, bytes]:
    with urllib.request.urlopen(origin + path) as res:
        return res.status, res.headers.get_content_type(), res.read()


class PublicPath(unittest.TestCase):
    def test_prefix_and_index(self) -> None:
        self.assertEqual(public_path("/"), "index.html")
        self.assertEqual(public_path("/ai-surgeon/"), "index.html")
        self.assertEqual(public_path("/ai-surgeon/ai-surgeon-systems.js"), "ai-surgeon-systems.js")
        self.assertEqual(public_path("/art/hero-surgical-table.jpg"), "art/hero-surgical-table.jpg")


class Layout(unittest.TestCase):
    def test_ingested_files_and_art_are_wired(self) -> None:
        self.assertTrue((ROOT / "index.html").is_file())
        self.assertTrue((ROOT / "ai-surgeon-prototype.html").is_file())
        self.assertTrue((ROOT / "ai-surgeon-module02-trauma.html").is_file())
        self.assertTrue((ROOT / "ai-surgeon-systems.js").is_file())
        self.assertTrue((ROOT / "trauma_physiology.js").is_file())
        self.assertTrue((ROOT / "docs" / "AI-Surgeon-Storyboard.pdf").is_file())
        self.assertTrue((ROOT / "docs" / "AI-Surgeon-Systems-and-Progression.md").is_file())
        hero = ROOT / "art" / "hero-surgical-table.jpg"
        key = ROOT / "art" / "key-art-x.jpg"
        self.assertGreater(hero.stat().st_size, 50_000)
        self.assertGreater(key.stat().st_size, 50_000)
        self.assertTrue((ROOT / "vendor" / "three.min.js").is_file())

    def test_hub_uses_art_and_playable_links(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("art/hero-surgical-table.jpg", html)
        self.assertIn("art/key-art-x.jpg", html)
        self.assertIn('href="ai-surgeon-prototype.html"', html)
        self.assertIn('href="ai-surgeon-module02-trauma.html"', html)
        self.assertNotIn("OS for your AI", html)
        self.assertNotIn("Navier", html)

    def test_loading_screens_use_the_two_stills(self) -> None:
        proto = (ROOT / "ai-surgeon-prototype.html").read_text(encoding="utf-8")
        trauma = (ROOT / "ai-surgeon-module02-trauma.html").read_text(encoding="utf-8")
        self.assertIn('url("art/hero-surgical-table.jpg")', proto)
        self.assertIn('src="art/key-art-x.jpg"', proto)
        self.assertIn('url("art/key-art-x.jpg")', trauma)
        self.assertIn('src="art/hero-surgical-table.jpg"', trauma)

    def test_modules_load_local_systems_not_cdn(self) -> None:
        proto = (ROOT / "ai-surgeon-prototype.html").read_text(encoding="utf-8")
        trauma = (ROOT / "ai-surgeon-module02-trauma.html").read_text(encoding="utf-8")
        self.assertIn('src="ai-surgeon-systems.js"', proto)
        self.assertIn('src="vendor/three.min.js"', proto)
        self.assertIn('src="ai-surgeon-systems.js"', trauma)
        self.assertIn('src="trauma_physiology.js"', trauma)
        self.assertIn('src="vendor/three.min.js"', trauma)
        self.assertNotIn("cdnjs.cloudflare.com", proto)
        self.assertNotIn("cdnjs.cloudflare.com", trauma)
        self.assertIn("Hand it over", proto)
        self.assertIn("Hand it over", trauma)
        self.assertIn("TraumaPhys.step", trauma)

    def test_module_beats_match_the_uploads(self) -> None:
        proto = (ROOT / "ai-surgeon-prototype.html").read_text(encoding="utf-8")
        trauma = (ROOT / "ai-surgeon-module02-trauma.html").read_text(encoding="utf-8")
        proto_steps = re.findall(r"\{ id:'(\w+)'", proto.split("const STEPS =")[1].split("const BRIEF")[0])
        trauma_steps = re.findall(r"\{ id:'(\w+)'", trauma.split("const STEPS =")[1].split("const TRAY")[0])
        self.assertEqual(len(proto_steps), 11)
        self.assertEqual(len(trauma_steps), 10)
        self.assertEqual(trauma_steps[0], "needle")
        self.assertEqual(trauma_steps[-1], "confirm")
        self.assertIn("Study one", (ROOT / "index.html").read_text(encoding="utf-8"))


class ServeHttp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), SurgeonHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_hub_and_prefixed_path(self) -> None:
        status, ctype, body = _get(self.origin, "/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", ctype)
        html = body.decode("utf-8")
        self.assertIn("AI Surgeon", html)
        self.assertIn("Open Appendectomy", html)
        self.assertIn("Tube Thoracostomy", html)
        status2, _, body2 = _get(self.origin, "/ai-surgeon/")
        self.assertEqual(status2, 200)
        self.assertEqual(body, body2)

    def test_systems_js_and_physiology_load(self) -> None:
        status, ctype, body = _get(self.origin, "/ai-surgeon-systems.js")
        self.assertEqual(status, 200)
        self.assertIn("javascript", ctype)
        text = body.decode("utf-8")
        self.assertIn("AISS.Handover", text)
        self.assertIn("derived-band-only", text)
        _, _, phys = _get(self.origin, "/trauma_physiology.js")
        self.assertIn("TraumaPhys", phys.decode("utf-8"))

    def test_art_and_storyboard(self) -> None:
        st, ctype, data = _get(self.origin, "/art/hero-surgical-table.jpg")
        self.assertEqual(st, 200)
        self.assertEqual(ctype, "image/jpeg")
        self.assertGreater(len(data), 50_000)
        st, ctype, data = _get(self.origin, "/art/key-art-x.jpg")
        self.assertEqual(st, 200)
        self.assertGreater(len(data), 50_000)
        st, ctype, data = _get(self.origin, "/docs/AI-Surgeon-Storyboard.pdf")
        self.assertEqual(st, 200)
        self.assertEqual(ctype, "application/pdf")
        self.assertTrue(data.startswith(b"%PDF"))

    def test_playable_html_and_three(self) -> None:
        for path in (
            "/ai-surgeon-prototype.html",
            "/ai-surgeon-module02-trauma.html",
            "/ai-surgeon/ai-surgeon-module02-trauma.html",
        ):
            st, _, body = _get(self.origin, path)
            self.assertEqual(st, 200, path)
            self.assertGreater(len(body), 10_000)
        st, ctype, body = _get(self.origin, "/vendor/three.min.js")
        self.assertEqual(st, 200)
        self.assertIn(b"THREE", body)

    def test_default_port_is_not_da(self) -> None:
        self.assertEqual(DEFAULT_PORT, 8770)
        self.assertNotEqual(DEFAULT_PORT, 8765)


class NodePlaytest(unittest.TestCase):
    def test_systems_and_trauma_loops(self) -> None:
        result = subprocess.run(
            ["node", "--test", "tests/systems.test.mjs", "tests/trauma_loop.test.mjs"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            self.fail(result.stdout + "\n" + result.stderr)


if __name__ == "__main__":
    unittest.main()
