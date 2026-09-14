#!/usr/bin/env python3
"""Navier–Stokes learning pack: exists, pictures, no HB import, no solve claim."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs" / "learn" / "navier-stokes"
FIGURES = PACK / "figures"
LIVE = ROOT / "domain_architect"

LESSONS = (
    PACK / "README.md",
    PACK / "01-the-news.md",
    PACK / "02-why-these-equations.md",
    PACK / "03-pictures.md",
)

PICTURES = (
    "laminar_vs_turbulent.png",
    "laminar_vs_turbulent_plot.png",
    "control_volume.png",
    "control_volume_plot.png",
    "vortex.png",
    "vortex_plot.png",
    "energy_cascade.png",
    "energy_spectrum_plot.png",
)

ARTIFACT_IMGS = (
    "/opt/cursor/artifacts/ns_laminar_vs_turbulent.png",
    "/opt/cursor/artifacts/ns_laminar_vs_turbulent_plot.png",
    "/opt/cursor/artifacts/ns_control_volume.png",
    "/opt/cursor/artifacts/ns_control_volume_plot.png",
    "/opt/cursor/artifacts/ns_vortex.png",
    "/opt/cursor/artifacts/ns_vortex_plot.png",
    "/opt/cursor/artifacts/ns_energy_cascade.png",
    "/opt/cursor/artifacts/ns_energy_spectrum_plot.png",
)

HB_IMPORT = (
    "HB_Math_Physics_Dossier",
    "Harmonic Blueprint",
    "Simons Field Equation",
    "canonical sfe",
    "UHF",
    "DHFA",
    "NAV-42",
)

SOLVE_CLAIMS = (
    "we solved",
    "this pack proves",
    "navier–stokes is solved",
    "navier-stokes is solved",
    "da-vc-01 is pass",
    "da-vc-01 pass",
    "t_{j\\leftarrow j} is closed",
    "leftover is closed",
)


def pack_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in LESSONS)


class TestNsLearningPackExists(unittest.TestCase):
    def test_index_and_lessons_exist(self):
        self.assertTrue((ROOT / "docs" / "learn" / "README.md").is_file())
        for path in LESSONS:
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 400, path)

    def test_figure_script_exists(self):
        script = PACK / "scripts" / "make_figures.py"
        self.assertTrue(script.is_file(), script)


class TestNsLearningPackPictures(unittest.TestCase):
    def test_pictures_exist_and_are_png(self):
        for name in PICTURES:
            path = FIGURES / name
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 8_000, path)
            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n", name)

    def test_lessons_embed_absolute_artifact_images(self):
        text = pack_text()
        self.assertIn("<img src=", text)
        for src in ARTIFACT_IMGS:
            self.assertIn(f'src="{src}"', text, src)
            self.assertIn("alt=", text)


class TestNsLearningPackHonesty(unittest.TestCase):
    def test_does_not_import_hb_dossier(self):
        text = pack_text()
        lower = text.lower()
        for needle in HB_IMPORT:
            self.assertNotIn(needle.lower(), lower, needle)
        self.assertNotIn("docs/archive/sfe-hb", text)

    def test_does_not_claim_a_solve(self):
        text = pack_text().lower().replace("–", "-")
        for needle in SOLVE_CLAIMS:
            self.assertNotIn(needle, text, needle)
        self.assertNotIn("clay is not claimed", text)
        self.assertNotIn("clay is not claimed", pack_text())

    def test_keeps_repo_split(self):
        text = pack_text()
        self.assertIn("DECOMPOSE", text)
        self.assertIn("CROSS-DOMAIN TRANSLATE", text)
        self.assertIn("SYNTHESIZE", text)
        self.assertIn("DA-VC-01", text)
        self.assertRegex(text, r"not PASS")
        self.assertIn(r"T_{j\leftarrow j}", text)
        self.assertIn("OPEN", text)
        self.assertRegex(text, r"Paper2 SND")
        self.assertRegex(text, r"conditional")
        self.assertIn(r"\Phi = u_\theta/r", text)
        self.assertRegex(text, r"not.*Domain Architect")

    def test_news_is_september_2026_and_sourced(self):
        news = (PACK / "01-the-news.md").read_text(encoding="utf-8")
        self.assertIn("8 September 2026", news)
        self.assertIn("https://openai.com/index/navier-stokes-solution/", news)
        self.assertIn("terrytao.wordpress.com", news)
        self.assertIn("smooth force", news.lower())
        self.assertIn("IPO", news)
        self.assertIn("pace", news.lower())

    def test_why_bother_is_continuum_law_not_waste(self):
        why = (PACK / "02-why-these-equations.md").read_text(encoding="utf-8")
        self.assertIn("continuum law", why.lower())
        self.assertIn("not a waste", why.lower())
        self.assertIn("nonlinear", why.lower())
        self.assertIn("chatbot headline", why.lower())
        self.assertIn(r"\partial_t u", why)

    def test_live_domain_architect_py_untouched_by_nav42(self):
        hits = []
        for path in LIVE.rglob("*.py"):
            body = path.read_text(encoding="utf-8")
            if "NAV-42" in body or "NAV42" in body:
                hits.append(path)
        self.assertEqual(hits, [])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
