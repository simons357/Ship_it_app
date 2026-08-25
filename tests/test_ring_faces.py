#!/usr/bin/env python3
"""Ring book faces. RingLemma_Final.tex is not a compile of the 21 Aug PDF."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RING = ROOT / "docs" / "papers" / "ring"
NS_SND = ROOT / "docs" / "papers" / "ns-snd"
TEX = RING / "RingLemma_Final.tex"
PDF = RING / "02_ring_lemma_snd_conditional.pdf"
README = RING / "README.md"
FACES = RING / "FACES.md"

TEX_SHA256 = "4602065ef68a6eb8402e2c99d708d7be888c4b959122ff8ba4dafbc073440157"
PDF_SHA256 = "0304f039406c7a95868b326b62f6c9ed4ea6b8c8386dc86ebd088a1a2ab114a3"


class TestRingLemmaFinalIsOlderStandaloneSource(unittest.TestCase):
    def test_tex_hash_is_frozen(self):
        self.assertTrue(TEX.is_file(), TEX)
        raw = TEX.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), TEX_SHA256)
        self.assertEqual(len(raw), 21216)
        self.assertEqual(raw.count(b"\n"), 448)

    def test_title_date_and_open_snd(self):
        tex = TEX.read_text(encoding="utf-8")
        self.assertIn("Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal", tex)
        self.assertIn(r"\date{April 2026", tex)
        self.assertIn("Preprint", tex)
        self.assertIn(r"\textup{(SND1)}", tex)
        self.assertIn(r"\rho = J(t)/X(t)", tex)
        self.assertIn("Dynamical [SND] preservation for \\emph{classical} NS", tex)
        self.assertIn(r"\textcolor{open}{\textbf{Open}}", tex)
        self.assertIn("Unconditional classical 3D NS regularity", tex)
        self.assertIn(r"\textcolor{notclaimed}{\textbf{Not claimed}}", tex)
        self.assertIn("does \\textbf{not} claim unconditional regularity", tex)
        self.assertIn("SND Attack Problem", tex)

    def test_not_clay_not_fixed_not_paper2(self):
        tex = TEX.read_text(encoding="utf-8")
        self.assertIn("Clay Millennium Prize rests on this question", tex)
        self.assertNotIn("Statement B", tex)
        self.assertNotIn("Paper2_NS_Regularity_SND_FIXED", tex)
        self.assertNotIn(r"H_N[a]", tex)
        self.assertNotIn(r"\|a-\mu\|", tex)
        self.assertFalse((NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file())
        self.assertNotEqual(TEX.name, "Paper2_NS_Regularity_SND_FIXED.tex")


class TestAugustPdfIsNotACompileOfRingLemmaFinal(unittest.TestCase):
    def test_pdf_hash_is_frozen_and_distinct(self):
        self.assertTrue(PDF.is_file(), PDF)
        pdf = PDF.read_bytes()
        tex = TEX.read_bytes()
        self.assertEqual(hashlib.sha256(pdf).hexdigest(), PDF_SHA256)
        self.assertEqual(len(pdf), 241673)
        self.assertNotEqual(pdf, tex)
        self.assertNotEqual(hashlib.sha256(pdf).hexdigest(), TEX_SHA256)

    def test_pdf_title_and_usable_snd_differ_from_april_tex(self):
        faces = FACES.read_text(encoding="utf-8")
        tex = TEX.read_text(encoding="utf-8")
        self.assertIn(
            "A Ring Lemma for Band-Limited Vorticity Direction",
            faces,
        )
        self.assertIn("Corrected preprint — August 2026", faces)
        self.assertIn("2026-08-20", faces)
        self.assertIn("Borromean Triads", tex)
        self.assertNotIn("Borromean Triads", faces.split("April / June-era TeX")[0])
        self.assertNotIn("Corrected preprint — August 2026", tex)
        self.assertNotIn(r"\date{August 2026", tex)


class TestRingReadmeAndFacesSplitTheBook(unittest.TestCase):
    def test_faces_and_readme_keep_usable_snd(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("not a compile of 21 august", faces.lower())
        self.assertIn("RingLemma_Final.tex", faces)
        self.assertIn("492e0654f_RingLemma_Final.tex", faces)
        self.assertIn("4602065ef68a", faces)
        self.assertIn("0304f039406c", faces)
        self.assertIn("June 20-ish", faces)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("Do not overwrite", faces)
        self.assertIn(r"\inf J(t)/X(t)\ge c_*>0", faces)
        self.assertIn("operator-norm", faces)
        self.assertIn("not a compile of the 21 aug", readme.lower())
        self.assertIn("RingLemma_Final.tex", readme)
        self.assertIn(r"\inf J(t)/X(t)\ge c_*>0", readme)
        self.assertIn("open", readme.lower())
        self.assertIn("No Clay claim", readme)
        self.assertIn("Do not overwrite", readme)
        self.assertIn("not paper2", readme.lower())
        self.assertNotIn("Paper2_NS_Regularity_SND_FIXED.tex", "".join(
            p.name for p in RING.iterdir() if p.is_file()
        ))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
