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
JUNE19 = RING / "RingLemma_Simons_June19_2026.tex"
PDF = RING / "02_ring_lemma_snd_conditional.pdf"
README = RING / "README.md"
FACES = RING / "FACES.md"
FRAGMENT = RING / "KAPPA-SND-CF-BKM-FRAGMENT.md"
LEFTOVER = ROOT / "docs" / "domain-architect" / "LEFTOVER-REPAIR.md"

TEX_SHA256 = "4602065ef68a6eb8402e2c99d708d7be888c4b959122ff8ba4dafbc073440157"
JUNE19_SHA256 = "a73d949f51a122ada93d6341926990991f7fd04e6cd5146a79b27d3d4ca99961"
PDF_SHA256 = "0304f039406c7a95868b326b62f6c9ed4ea6b8c8386dc86ebd088a1a2ab114a3"

PASTE_LABELS = (
    r"lem:triad_bound_formal",
    r"eq:triad_bound_result",
    r"prop:CF_integrability",
    r"thm:CF93_theorem",
)


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
        self.assertIn("not a clay claim", faces.lower())
        self.assertIn("not the june fixed pdf", faces.lower())
        self.assertIn("KAPPA-SND-CF-BKM-FRAGMENT.md", faces)
        self.assertIn("RingLemma_Simons_June19_2026.tex", faces)
        self.assertIn("a73d949f", faces)
        self.assertIn(r"\kappa_j", faces)
        self.assertIn(r"E_{\min}", faces)
        self.assertIn("CONDITIONAL", faces)
        self.assertIn("DA-VC-01", faces)
        self.assertIn("FAIL", faces)
        self.assertIn("naming collision", faces)
        self.assertIn("TRANSFORMABLE", faces)
        self.assertIn("c8a03f315_RingLemma_Simons_June19_2026.tex", readme)
        self.assertIn("KAPPA-SND-CF-BKM-FRAGMENT.md", readme)
        self.assertIn("NOT CLAIMED", readme)
        self.assertIn("HTTP **302**", faces)
        self.assertIn("then **200**", faces)
        self.assertIn("untrusted alias", faces.lower())
        self.assertIn("not overwritten", faces.lower())
        self.assertIn("a73d949f51a122", faces)
        lookup = (ROOT / "docs" / "packets" / "OLD-PAPERS-LOOK-UP.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("c8a03f315_RingLemma_Simons_June19_2026.tex", lookup)
        self.assertIn("a73d949f", lookup)
        self.assertIn("filed", lookup.lower())
        self.assertNotIn(
            "still not in this VM** under that pack name",
            lookup,
        )
        self.assertIn("OVERLEAF-VS-PACK-AUDIT-2026-08-15.md", faces)
        self.assertIn("OVERLEAF-VS-PACK-AUDIT-2026-08-15.md", readme)
        self.assertIn("CLAY_FINAL", faces)
        self.assertIn("a73d949f", faces)
        self.assertIn("kappa", faces.lower())


class TestPastedKappaSndIsNotRingLemmaFinal(unittest.TestCase):
    def test_unique_labels_absent_from_filed_ring_and_paper2_tex(self):
        sources = [
            TEX.read_text(encoding="utf-8"),
            JUNE19.read_text(encoding="utf-8"),
            PDF.read_bytes().decode("latin-1"),
        ]
        for name in (
            "Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex",
            "Simons_NS_Paper2_DRAFT_original.tex",
            "NS_Regularity_Final_Polished.tex",
        ):
            sources.append((NS_SND / name).read_text(encoding="utf-8"))
        blob = "\n".join(sources)
        for label in PASTE_LABELS:
            self.assertNotIn(label, blob)
        self.assertNotIn(r"E_{\min}", TEX.read_text(encoding="utf-8"))
        self.assertNotIn(r"E_{\min}", JUNE19.read_text(encoding="utf-8"))
        self.assertNotIn(r"\kappa_j", TEX.read_text(encoding="utf-8"))
        self.assertNotIn("Borromean Triadic Transfer Bound", blob)

    def test_april_and_june19_thm_main_is_augmented_not_clay(self):
        april = TEX.read_text(encoding="utf-8")
        june = JUNE19.read_text(encoding="utf-8")
        self.assertIn("Global Regularity, Augmented NS", april)
        self.assertIn("Global Regularity, Augmented System", june)
        self.assertIn(r"\textcolor{open}{\textbf{Open}}", april)
        self.assertIn(r"\textcolor{open}{\textbf{Open}}", june)
        self.assertIn(r"\textcolor{notclaimed}{\textbf{Not claimed}}", april)
        self.assertIn(r"\textcolor{notclaimed}{\textbf{Not claimed}}", june)
        self.assertIn("does \\textbf{not} claim unconditional regularity", april)
        self.assertIn("does \\textbf{not} claim unconditional regularity", june)

    def test_fragment_note_is_conditional_not_complete_tex(self):
        note = FRAGMENT.read_text(encoding="utf-8")
        self.assertTrue(FRAGMENT.is_file(), FRAGMENT)
        self.assertIn("CONDITIONAL", note)
        self.assertIn("NOT CLAIMED", note)
        self.assertIn("DA-VC-01", note)
        self.assertIn("FAIL", note)
        self.assertIn("lem:triad_bound_formal", note)
        self.assertIn("eq:triad_bound_result", note)
        self.assertIn("prop:CF_integrability", note)
        self.assertIn("thm:CF93_theorem", note)
        self.assertIn(r"E_{\min}", note)
        self.assertIn("not automatically", note.lower())
        self.assertIn(r"\inf J/X\ge c_*", note)
        self.assertIn("naming collision", note)
        self.assertIn("Do not invent a preamble", note)
        self.assertIn("domain_architect/", note)
        self.assertIn("TRANSFORMABLE", note)
        self.assertNotIn(r"\documentclass", note)

    def test_kappa_snd_is_not_jx_and_not_imported_to_da(self):
        faces = FACES.read_text(encoding="utf-8")
        leftover = LEFTOVER.read_text(encoding="utf-8")
        self.assertIn(r"\kappa_j(t)=E_j/E\le\kappa^*<1", faces)
        self.assertIn(r"\inf_t J(t)/X(t)\ge c_*>0", faces)
        self.assertIn("non-concentration", faces)
        self.assertIn("enstrophy", faces)
        self.assertIn(r"H_N[a]", faces)
        self.assertIn(r"E_{\min}:=\inf E_{j^*(t)}>0", faces)
        self.assertIn("as if it were free", faces)
        self.assertIn(r"\kappa_j=E_j/E\le\kappa^*<1", leftover)
        self.assertIn("TRANSFORMABLE", leftover)
        self.assertIn(r"\inf_t J(t)/X(t)\ge c_*>0", leftover)


class TestJune19PackIsFiledAugmentedNotThePaste(unittest.TestCase):
    ALIAS = "c8a03f315_RingLemma_Simons_June19_2026.tex"

    def test_hash_size_and_date(self):
        raw = JUNE19.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), JUNE19_SHA256)
        self.assertEqual(len(raw), 44368)
        self.assertEqual(raw.count(b"\n"), 887)
        tex = raw.decode("utf-8")
        self.assertIn(r"\date{June 19, 2026", tex)
        self.assertIn("Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal", tex)
        self.assertIn(r"\textup{(SND1)}", tex)
        self.assertIn(r"\rho(t) = J(t)/X(t)", tex)
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(), TEX_SHA256)
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(), PDF_SHA256)

    def test_not_an_alias_of_april_final_and_not_kappa_snd(self):
        june = JUNE19.read_text(encoding="utf-8")
        april = TEX.read_text(encoding="utf-8")
        self.assertNotEqual(JUNE19.read_bytes(), TEX.read_bytes())
        self.assertIn(r"\date{April 2026", april)
        self.assertNotIn(r"\date{June 19, 2026", april)
        self.assertIn("prop:zeta-spread", june)
        self.assertNotIn("prop:zeta-spread", april)
        self.assertNotIn(r"\kappa_j", june)
        self.assertNotIn(r"E_{\min}", june)
        self.assertNotIn(r"H_N[a]", june)
        self.assertNotIn("Paper2_NS_Regularity_SND_FIXED", june)
        self.assertNotIn("Statement B", june)
        self.assertIn(r"\textcolor{open}{\textbf{Open}}", june)
        self.assertIn(r"\textcolor{notclaimed}{\textbf{Not claimed}}", june)
        self.assertFalse(
            (RING / self.ALIAS).is_file(),
            "do not re-file the Base44 hash-prefix name as a second copy",
        )
        self.assertFalse((NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file())

    def test_pdf_bytes_unchanged(self):
        pdf = PDF.read_bytes()
        self.assertEqual(hashlib.sha256(pdf).hexdigest(), PDF_SHA256)
        self.assertEqual(len(pdf), 241673)
        self.assertNotEqual(pdf, JUNE19.read_bytes())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
