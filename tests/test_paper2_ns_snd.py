#!/usr/bin/env python3
"""Paper2 SND/GNC is a separate book. Do not glue it to swirl or DA."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS_SND = ROOT / "docs" / "papers" / "ns-snd"
SWIRL = ROOT / "docs" / "papers" / "swirl"
PAPER = NS_SND / "Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex"
PDF = NS_SND / "Paper2_NS_Regularity_SND_FIXED.pdf"
README = NS_SND / "README.md"
FACES = NS_SND / "FACES.md"
PDF_SHA256 = "7de9444d18054fc8f49a52c3fd7ed2f086a7c7d7d6d1e95bad350c378535c41b"


def collapsed(text: str) -> str:
    return " ".join(text.split())


class TestPaper2IsItsOwnBook(unittest.TestCase):
    def test_repaired_tex_and_readme_exist(self):
        self.assertTrue(PAPER.is_file(), PAPER)
        self.assertTrue(README.is_file(), README)
        tex = collapsed(PAPER.read_text(encoding="utf-8"))
        readme = README.read_text(encoding="utf-8")
        self.assertIn("Spectral Non-Concentration", tex)
        self.assertIn(r"\mathbb T^3", tex)
        self.assertIn("not claim unconditional global regularity", tex)
        self.assertIn("separate book", readme)
        self.assertIn("the axisymmetric swirl paper", readme.lower())
        self.assertIn("not a compile", readme.lower())

    def test_june_pdf_is_not_a_compile_of_august_tex(self):
        self.assertTrue(PDF.is_file(), PDF)
        self.assertTrue(FACES.is_file(), FACES)
        digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
        self.assertEqual(digest, PDF_SHA256)
        self.assertGreater(PDF.stat().st_size, 100_000)
        faces = FACES.read_text(encoding="utf-8")
        self.assertIn("not a compile pair", faces.lower())
        self.assertIn("Corrected June 2026", faces)
        self.assertIn("1 August 2026", faces)
        self.assertIn("GNC / false gcd", faces)
        self.assertIn("Absent", faces)
        tex = PAPER.read_text(encoding="utf-8")
        self.assertIn("Goldbach", tex)

    def test_open_and_withdrawn_status_is_in_the_source(self):
        tex = collapsed(PAPER.read_text(encoding="utf-8"))
        self.assertIn("SND Simplex Stability — Open", tex)
        self.assertIn("T2 -- Closed Gronwall Proof", tex)
        self.assertIn("is withdrawn", tex)
        self.assertIn("no Goldbach theorem is claimed", tex)
        self.assertIn(r"gcd(2k-i,2k-j)=\gcd(i,j)", tex)
        self.assertIn("NUMERICAL / UNDER AUDIT", tex)
        self.assertIn("Classical 3D NS global regularity", tex)
        self.assertIn("Not claimed", tex)

    def test_paper2_is_not_the_swirl_identity_paper(self):
        tex = PAPER.read_text(encoding="utf-8")
        swirl = (SWIRL / "Simons_PhiRenorm_Swirl_2026-08-22.tex").read_text(
            encoding="utf-8"
        )
        self.assertIn(r"\Ph:=\frac{\ut}{r}", swirl)
        self.assertNotIn(r"\ut", tex)
        self.assertNotIn("Shahmurov", tex)
        self.assertNotIn("Harmonic Blueprint", tex)
        self.assertNotIn("QStack", tex)
        flat = collapsed(tex)
        self.assertIn("not claim unconditional global regularity", flat)
        self.assertIn(
            "not an unconditional solution of classical three-dimensional",
            flat,
        )

    def test_readme_forbids_glue(self):
        readme = README.read_text(encoding="utf-8")
        self.assertIn("FRA coupling", readme)
        self.assertIn("SND ≡ GNC ≡ Bridge", readme)
        self.assertIn(r"u_\theta/r", readme)
        self.assertIn("Do not identify them", readme)
        self.assertIn("nonlinear shell fluxes", readme)
        self.assertIn("Paper2_NS_Regularity_SND_FIXED.pdf", readme)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
