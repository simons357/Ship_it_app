#!/usr/bin/env python3
"""Official Domain Architect mark: chrome A + rainbow triskelion."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from domain_architect.app import handle_api
from domain_architect.brand import (
    PRESETS,
    MarkParams,
    apply_mark_files,
    apply_mark_from_params,
    apply_svg_document,
    icon_params,
    preset_svg,
    render_mark_svg,
    write_factory_marks,
)


class TestMarkParams(unittest.TestCase):
    def test_unknown_keys_are_ignored(self):
        params = MarkParams.from_dict({"hue": 40, "evil": 1, "size": 512})
        self.assertEqual(params.hue, 40.0)
        self.assertEqual(params.size, 512)
        self.assertFalse(hasattr(params, "evil"))

    def test_bool_coercion(self):
        params = MarkParams.from_dict({"show_wordmark": "false", "show_frame": 1})
        self.assertFalse(params.show_wordmark)
        self.assertTrue(params.show_frame)


class TestRender(unittest.TestCase):
    def test_presets_render_svg(self):
        for name in ("gold", "silver", "icon"):
            svg = preset_svg(name)
            self.assertIn("<svg", svg)
            self.assertIn("Domain Architect", svg)
            self.assertIn("triskelion", svg.lower())
            self.assertNotIn("#2EC4D6", svg)

    def test_gold_lockup_has_wordmark(self):
        svg = preset_svg("gold")
        self.assertIn(">DOMAIN</text>", svg)
        self.assertIn(">ARCHITECT</text>", svg)
        self.assertIn("DECOMPOSE", svg)
        self.assertIn("#e6c35a", svg)

    def test_icon_has_no_type(self):
        svg = preset_svg("icon")
        self.assertNotIn(">DOMAIN</text>", svg)
        self.assertNotIn(">ARCHITECT</text>", svg)

    def test_gold_and_silver_differ(self):
        self.assertNotEqual(preset_svg("gold"), preset_svg("silver"))

    def test_icon_params_strip_type(self):
        icon = icon_params(PRESETS["gold"])
        self.assertFalse(icon.show_wordmark)
        self.assertFalse(icon.show_tagline)
        self.assertGreaterEqual(icon.a_scale, 0.48)


class TestApply(unittest.TestCase):
    def test_apply_writes_icon_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            written = apply_mark_files(preset_svg("icon"), root)
            self.assertGreaterEqual(len(written), 3)
            for path in written:
                text = Path(path).read_text(encoding="utf-8")
                self.assertIn("<svg", text)
                self.assertNotIn("#2EC4D6", text)

    def test_apply_from_params_writes_lockup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = apply_mark_from_params(PRESETS["gold"].to_dict(), root)
            self.assertTrue(any(p.endswith("favicon.svg") for p in result["written"]))
            lockup = (root / "assets" / "brand" / "domain-architect-official.svg").read_text(
                encoding="utf-8"
            )
            self.assertIn(">DOMAIN</text>", lockup)
            icon = (root / "assets" / "domain-architect.svg").read_text(encoding="utf-8")
            self.assertNotIn(">DOMAIN</text>", icon)

    def test_script_svg_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                apply_mark_files('<svg><script>alert(1)</script></svg>', tmp)

    def test_apply_svg_document(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#0A0D11"/></svg>'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            written = apply_svg_document(svg, root)
            self.assertTrue(any(p.endswith("favicon.svg") for p in written))
            official = root / "assets" / "brand" / "domain-architect-official.svg"
            self.assertEqual(official.read_text(encoding="utf-8"), svg)

    def test_write_factory_marks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brand = root / "assets" / "brand"
            brand.mkdir(parents=True)
            (brand / "domain-architect.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><path fill="#2EC4D6"/></svg>\n',
                encoding="utf-8",
            )
            paths = write_factory_marks(root)
            self.assertTrue(Path(paths["icon"]).exists())
            self.assertTrue((brand / "exploratory-spine.svg").exists())
            self.assertIn("#2EC4D6", (brand / "exploratory-spine.svg").read_text(encoding="utf-8"))
            self.assertIn("DOMAIN", Path(paths["gold"]).read_text(encoding="utf-8"))
            self.assertNotIn("DOMAIN", Path(paths["icon"]).read_text(encoding="utf-8"))


class TestLambdaLab(unittest.TestCase):
    def test_lab_file_is_the_construction_tool(self):
        path = Path(__file__).resolve().parents[1] / "domain_architect" / "static" / "lambda-lab.html"
        text = path.read_text(encoding="utf-8")
        self.assertIn("Lambda Lab", text)
        self.assertIn("watch the 40", text)
        self.assertIn("Triskele", text)
        self.assertIn("Use as app icon", text)
        self.assertIn("/api/brand/apply", text)
        self.assertIn('data-v="gold"', text)
        self.assertIn('data-v="silver"', text)
        self.assertIn("function lambdaPaths", text)


class TestBrandApi(unittest.TestCase):
    def test_presets_endpoint(self):
        status, body, ctype = handle_api("/api/brand/presets", {})
        self.assertEqual(status, 200)
        self.assertIn("json", ctype)
        payload = json.loads(body)
        self.assertIn("gold", payload)
        self.assertIn("silver", payload)
        self.assertIn("icon", payload)
        self.assertEqual(payload["gold"]["domain_metal"], "#e6c35a")
        self.assertEqual(payload["silver"]["domain_metal"], "#e8e8e8")

    def test_render_endpoint_gold(self):
        status, body, ctype = handle_api("/api/brand/render", {"preset": "gold"})
        self.assertEqual(status, 200)
        self.assertIn("svg", ctype)
        text = body.decode("utf-8")
        self.assertIn("<svg", text)
        self.assertIn("DOMAIN", text)

    def test_render_endpoint_custom_hue(self):
        status, body, _ctype = handle_api("/api/brand/render", {"hue": 200, "show_wordmark": False})
        self.assertEqual(status, 200)
        text = body.decode("utf-8")
        self.assertNotIn(">DOMAIN</text>", text)


class TestLiveIcon(unittest.TestCase):
    def test_checked_in_icon_is_chrome_a(self):
        root = Path(__file__).resolve().parents[1]
        live = (root / "assets" / "domain-architect.svg").read_text(encoding="utf-8")
        self.assertIn("Domain Architect", live)
        self.assertNotIn("#2EC4D6", live)
        self.assertIn("open chrome a", live.lower())


if __name__ == "__main__":
    unittest.main()
