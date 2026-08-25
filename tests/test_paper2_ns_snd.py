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
CHAIN = NS_SND / "NS_UNAUGMENTED_PROOF_CHAIN.md"
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
        self.assertIn("NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md", readme)
        self.assertIn("zenodo-20272545", readme)
        self.assertIn("Lemma 6.1 OPEN", readme)
        self.assertIn("NS_UNAUGMENTED_PROOF_CHAIN.md", readme)


class TestClassicalUnaugmentedChainFile(unittest.TestCase):
    def test_chain_file_exists_and_is_open_not_claimed(self):
        self.assertTrue(CHAIN.is_file(), CHAIN)
        text = CHAIN.read_text(encoding="utf-8")
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("OPEN", text)
        self.assertIn("Ring Lemma", text)
        self.assertIn("NS-6", text)
        self.assertIn("June FIXED PDF compile", text)
        self.assertIn("Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex", text)
        self.assertIn("H_N[a]", text)
        self.assertIn("Q6", text)
        faces = FACES.read_text(encoding="utf-8")
        self.assertIn("NS_UNAUGMENTED_PROOF_CHAIN.md", faces)
        self.assertIn("Ring Lemma is PROVED", faces)
        self.assertTrue("7–8" in faces or "7-8" in faces)


class TestPaper2ImpliesFacesAreNotTheJunePdf(unittest.TestCase):
    IMPLIES_MAC = NS_SND / "Paper2_NS_Regularity_SND.pdf"
    IMPLIES_MAC_SHA256 = (
        "9e53d6640cc3808696afbcbec8f78c08de860b4816680ff43cdc816ce5c60cb0"
    )
    ZENODO = NS_SND / "zenodo-20272545" / "Paper2_NS_Regularity_SND.pdf"
    ZENODO_SHA256 = (
        "87610856449007e7bdca3b87d82683e463b299484b3906a0dda27a18bec416a3"
    )
    AUDIT = NS_SND / "NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md"

    def test_three_pdfs_are_distinct_bytes(self):
        mac = self.IMPLIES_MAC.read_bytes()
        zen = self.ZENODO.read_bytes()
        june = PDF.read_bytes()
        self.assertEqual(hashlib.sha256(mac).hexdigest(), self.IMPLIES_MAC_SHA256)
        self.assertEqual(hashlib.sha256(zen).hexdigest(), self.ZENODO_SHA256)
        self.assertEqual(hashlib.sha256(june).hexdigest(), PDF_SHA256)
        self.assertNotEqual(mac, zen)
        self.assertNotEqual(mac, june)
        self.assertNotEqual(zen, june)

    def test_audit_names_the_kink_and_withdrawn_doi(self):
        audit = self.AUDIT.read_text(encoding="utf-8")
        self.assertIn("10.5281/zenodo.20272545", audit)
        self.assertIn("Lemma 6.1", audit)
        self.assertIn("OPEN", audit)
        self.assertIn("T2", audit)
        self.assertIn("not an unconditional proof", audit.lower())
        faces = FACES.read_text(encoding="utf-8")
        self.assertIn("Claim withdrawn", faces)
        self.assertIn("Lemma 6.1 OPEN", faces)
        self.assertIn("Paper2_NS_Regularity_SND_FIXED.tex", faces)
        self.assertIn("not received", faces.lower())
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file(),
            "June FIXED TeX was not attached; do not invent it",
        )


class TestJune14ClaySubmitDidNotArrive(unittest.TestCase):
    """Mac ClaySubmit was selected but never uploaded. Do not invent it."""

    CLAY_SUBMIT = "2f30e8c4f_NS_ClaySubmit_Jonathan_Simons_2026-06-14.tex"

    def test_claysubmit_is_absent_and_not_a_fixed_or_clay_solution(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn(self.CLAY_SUBMIT, faces)
        self.assertIn("June 14 Clay-submit", faces)
        self.assertIn("not received", faces.lower())
        self.assertIn("**Not** FIXED", faces)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("a compile of the fixed pdf", faces.lower())
        self.assertIn("Clay solution", faces)
        self.assertIn(self.CLAY_SUBMIT, readme)
        self.assertIn("NOT CLAIMED", readme)
        invented = [
            NS_SND / self.CLAY_SUBMIT,
            NS_SND / "historical" / self.CLAY_SUBMIT,
            ROOT / "docs" / "archive" / self.CLAY_SUBMIT,
            ROOT / "docs" / "papers" / "ns-snd" / "historical" / self.CLAY_SUBMIT,
        ]
        for path in invented:
            self.assertFalse(path.is_file(), f"do not invent {path}")
        tex = PAPER.read_text(encoding="utf-8")
        self.assertNotIn("ClaySubmit", tex)
        self.assertNotIn("2f30e8c4f", tex)


class TestFinalPolishedIsADistinctFace(unittest.TestCase):
    """Mac 'NS Regularity Final Polished.tex' is not FIXED and not August."""

    POLISHED = NS_SND / "NS_Regularity_Final_Polished.tex"
    POLISHED_SHA256 = (
        "b9249af37f3624548d7bee69f26fc2fc0d93c22e744c54cd110810725cd80817"
    )
    AUGUST_SHA256 = (
        "1ff7a211c00d660c30365e5913727f0129cfc5cd76f1f40ed9a47f468c746cc3"
    )

    def test_hash_lock_and_not_a_june_or_august_compile(self):
        self.assertTrue(self.POLISHED.is_file(), self.POLISHED)
        raw = self.POLISHED.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.POLISHED_SHA256)
        self.assertEqual(raw.count(b"\n"), 825)
        august = PAPER.read_bytes()
        self.assertEqual(hashlib.sha256(august).hexdigest(), self.AUGUST_SHA256)
        self.assertNotEqual(raw, august)
        self.assertNotEqual(self.POLISHED.resolve(), PAPER.resolve())
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file(),
            "do not invent June FIXED TeX from this filename",
        )
        tex = raw.decode("utf-8")
        self.assertIn(
            "Global Regularity of the Three-Dimensional Incompressible", tex
        )
        self.assertIn("Self-Adaptive Spectral Damping", tex)
        self.assertIn(r"\date{2026}", tex)
        self.assertIn(r"\documentclass[12pt]{amsart}", tex)
        self.assertNotIn("Corrected June 2026", tex)
        self.assertNotIn("Conditional Regularity Criterion", tex)
        self.assertNotIn("Goldbach", tex)
        self.assertNotIn("GNC", tex)
        self.assertNotIn("Lemma 6.1", tex)
        self.assertIn("Conditional global regularity of classical NS", tex)
        self.assertIn(r"\begin{openproblem}[The Spectral Non-Dispersal Condition]", tex)
        self.assertIn(r"\Qsix", tex)
        self.assertIn(r"\lH", tex)
        self.assertIn(r"\R^3", tex)
        self.assertNotIn(r"\mathbb T^3", tex)

    def test_faces_and_readme_mark_it_not_closed(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("NS_Regularity_Final_Polished.tex", faces)
        self.assertIn("NS_Regularity_Final_Polished.tex", readme)
        self.assertIn("Self-Adaptive Spectral Damping", faces)
        self.assertIn("do not use as closed", faces.lower())
        self.assertIn("do not use as closed", readme.lower())
        self.assertIn("825", faces)
        self.assertIn("b9249af37f", faces)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("NOT CLAIMED", readme)
        self.assertIn("not a compile pair", faces.lower())
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
