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


def classify_paper2_tex_title_page(tex: str) -> str:
    """Identify a Paper2 TeX face from title + date, never from an untrusted filename."""
    june_title = "Conditional Regularity Criterion" in tex
    june_date = "Corrected June 2026" in tex
    implies = "Implies Global Regularity" in tex
    may18 = r"\date{May 18, 2026}" in tex
    august = "Conditional Global-Regularity Framework" in tex
    april_coherence = (
        "A Spectral Coherence Criterion" in tex
        or "Dominant-Shell Damping" in tex
    )
    if june_title and june_date:
        return "june_fixed_source"
    if august:
        return "august_repaired"
    if april_coherence:
        return "april_spectral_coherence"
    if implies and may18:
        return "may18_implies_draft"
    return "unknown"


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
        self.assertIn("zenodo-20269536", readme)
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

    def test_zenodo_20272545_sha_is_not_june_fixed_7de9444d(self):
        zen = self.ZENODO.read_bytes()
        june = PDF.read_bytes()
        zen_sha = hashlib.sha256(zen).hexdigest()
        june_sha = hashlib.sha256(june).hexdigest()
        self.assertEqual(zen_sha, self.ZENODO_SHA256)
        self.assertEqual(self.ZENODO_SHA256[:8], "87610856")
        self.assertEqual(june_sha, PDF_SHA256)
        self.assertEqual(
            PDF_SHA256,
            "7de9444d18054fc8f49a52c3fd7ed2f086a7c7d7d6d1e95bad350c378535c41b",
        )
        self.assertNotEqual(zen_sha, PDF_SHA256)
        self.assertNotEqual(zen, june)
        self.assertEqual(len(zen), 360856)
        self.assertEqual(len(june), 309576)

    def test_faces_mark_zenodo_20272545_not_june_fixed(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        note = (NS_SND / "zenodo-20272545" / "README.md").read_text(encoding="utf-8")
        for text in (faces, readme, note):
            self.assertIn("20272545", text)
            self.assertIn("Claim withdrawn", text)
            self.assertIn("87610856", text)
            self.assertIn("NOT the June FIXED PDF", text)
            self.assertIn("7de9444d", text)
        self.assertIn("Implies Global Regularity", faces)
        self.assertIn("20269536", faces)
        self.assertIn("distinct", faces.lower())
        self.assertIn("NOT CLAIMED", faces)
        self.assertNotIn("DA-VC-01 PASS", faces)
        self.assertNotIn("DA-VC-01 PASS", readme)
        self.assertNotIn("DA-VC-01 PASS", note)


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


class TestV7ArXivDocxIsADistinctFace(unittest.TestCase):
    """Word v7 export is another Q6/lambda_H face. Not FIXED. Not Clay."""

    DOCX = NS_SND / "NS_Regularity_v7_ArXiv.docx"
    TXT = NS_SND / "NS_Regularity_v7_ArXiv.txt"
    DOCX_SHA256 = (
        "ca055da6db23aa58ed04747c2e9ea505ada3d373054f74ac3dd8d841c796046e"
    )
    TXT_SHA256 = (
        "4488187effbfd6b1ab31abe59d639765d259f9d8bbf510674f71daa58e858d0c"
    )

    def test_hash_lock_distinct_from_polished_and_august(self):
        self.assertTrue(self.DOCX.is_file(), self.DOCX)
        self.assertTrue(self.TXT.is_file(), self.TXT)
        docx = self.DOCX.read_bytes()
        txt = self.TXT.read_bytes()
        self.assertEqual(hashlib.sha256(docx).hexdigest(), self.DOCX_SHA256)
        self.assertEqual(hashlib.sha256(txt).hexdigest(), self.TXT_SHA256)
        self.assertEqual(len(docx), 34637)
        polished = (NS_SND / "NS_Regularity_Final_Polished.tex").read_bytes()
        august = PAPER.read_bytes()
        self.assertNotEqual(docx, polished)
        self.assertNotEqual(docx, august)
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file(),
            "do not invent June FIXED TeX from the v7 Word filename",
        )
        extract = txt.decode("utf-8")
        self.assertIn("Self-Adaptive Spectral Damping", extract)
        self.assertIn("Open Problem (The Spectral Non-Dispersal Condition)", extract)
        self.assertIn("[SND]", extract)
        self.assertIn("Open — precisely stated", extract)
        self.assertNotIn("Goldbach", extract)
        self.assertNotIn("GNC", extract)
        self.assertNotIn("Lemma 6.1", extract)
        self.assertNotIn("Corrected June 2026", extract)

    def test_faces_mark_v7_not_fixed_not_clay(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("NS_Regularity_v7_ArXiv.docx", faces)
        self.assertIn("NS_Regularity_v7_ArXiv.txt", faces)
        self.assertIn("ca055da6db23", faces)
        self.assertIn("READOUT_v7_Millennium_Publisher_Match.md", faces)
        self.assertIn("not on disk", faces.lower())
        self.assertIn("NS_Regularity_v7_ArXiv.docx", readme)
        self.assertIn("NOT CLAIMED", readme)
        self.assertIn("do not use as closed", faces.lower())
        self.assertFalse(
            (ROOT / "READOUT_v7_Millennium_Publisher_Match.md").is_file()
        )
        self.assertFalse(
            (NS_SND / "READOUT_v7_Millennium_Publisher_Match.md").is_file()
        )


class TestShellStressIsNumericalNotTheorem(unittest.TestCase):
    XLSX = NS_SND / "shell-stress" / "Simons_NS_Shell_Stress_Test.xlsx"
    NOTE = NS_SND / "shell-stress" / "README.md"
    XLSX_SHA256 = (
        "ddba329536ee6bf6148c495813347725b7658b2bd33a0d4f47685543f980f3d7"
    )

    def test_hash_lock_and_readme_forbids_theorem_claim(self):
        self.assertTrue(self.XLSX.is_file(), self.XLSX)
        self.assertTrue(self.NOTE.is_file(), self.NOTE)
        raw = self.XLSX.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.XLSX_SHA256)
        self.assertEqual(len(raw), 287973)
        note = self.NOTE.read_text(encoding="utf-8")
        self.assertIn("not a theorem", note.lower())
        self.assertIn("route j", note.lower())
        self.assertIn("all-", note.lower())
        self.assertIn("not clay", note.lower())
        self.assertIn("24", note)
        self.assertIn("not an axisymmetric-swirl", note.lower())
        faces = FACES.read_text(encoding="utf-8")
        self.assertIn("Simons_NS_Shell_Stress_Test.xlsx", faces)
        self.assertIn("Route J", faces)
        self.assertIn("ddba329536ee", faces)
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )


class TestDraftOriginalIsHistoricalImpliesFace(unittest.TestCase):
    """May 18 submission draft. Not FIXED. Not August controlling face. Not Clay."""

    DRAFT = NS_SND / "Simons_NS_Paper2_DRAFT_original.tex"
    DRAFT_SHA256 = (
        "f51ed5c05ec3886603a69de942b890dc76c73b3860fe089a056b4665ab8cc4cb"
    )
    AUGUST_SHA256 = (
        "1ff7a211c00d660c30365e5913727f0129cfc5cd76f1f40ed9a47f468c746cc3"
    )
    POLISHED_SHA256 = (
        "b9249af37f3624548d7bee69f26fc2fc0d93c22e744c54cd110810725cd80817"
    )

    def test_hash_lock_and_not_june_or_august_or_polished(self):
        self.assertTrue(self.DRAFT.is_file(), self.DRAFT)
        raw = self.DRAFT.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.DRAFT_SHA256)
        self.assertEqual(len(raw), 26998)
        self.assertEqual(raw.count(b"\n"), 664)
        august = PAPER.read_bytes()
        polished = (NS_SND / "NS_Regularity_Final_Polished.tex").read_bytes()
        self.assertEqual(hashlib.sha256(august).hexdigest(), self.AUGUST_SHA256)
        self.assertEqual(hashlib.sha256(polished).hexdigest(), self.POLISHED_SHA256)
        self.assertNotEqual(raw, august)
        self.assertNotEqual(raw, polished)
        self.assertNotEqual(self.DRAFT.resolve(), PAPER.resolve())
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file(),
            "do not invent June FIXED TeX from this draft filename",
        )
        tex = raw.decode("utf-8")
        self.assertIn("PAPER 2 — SUBMISSION DRAFT", tex)
        self.assertIn("Implies Global Regularity", tex)
        self.assertIn(r"\date{May 18, 2026}", tex)
        self.assertIn(r"\mathbb T^3", tex)
        self.assertIn("SND Simplex Stability — Open", tex)
        self.assertIn("T2 — Closed Gronwall Proof", tex)
        self.assertIn("T2 — Closed (conditional on SND)", tex)
        self.assertIn("Open", tex)
        self.assertNotIn("Corrected June 2026", tex)
        self.assertNotIn("Conditional Regularity Criterion", tex)
        self.assertNotIn("Conditional Global-Regularity Framework", tex)
        self.assertNotIn("Goldbach", tex)
        self.assertNotIn("GNC", tex)
        self.assertNotIn("QStack", tex)
        self.assertNotIn("ClaySubmit", tex)
        self.assertNotIn("Self-Adaptive Spectral Damping", tex)

    def test_faces_mark_draft_not_fixed_not_august_not_clay(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("Simons_NS_Paper2_DRAFT_original.tex", faces)
        self.assertIn("Simons_NS_Paper2_DRAFT_original.tex", readme)
        self.assertIn("f51ed5c05ec3", faces)
        self.assertIn("664", faces)
        self.assertIn("Draft", faces)
        self.assertIn("august controlling", faces.lower())
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("NOT CLAIMED", readme)
        self.assertIn("do not use as closed", faces.lower())
        self.assertIn("7–8", faces)
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )


class TestAprilSpectralCoherenceFilenameIsMay18ImpliesAlias(unittest.TestCase):
    """Desktop/Base44 April Spectral Coherence DRAFT is the May 18 implies TeX.

    Filename claimed April Q6 / *A Spectral Coherence Criterion*. Bytes are
    Simons_NS_Paper2_DRAFT_original.tex. Not FIXED. Not August. Not Clay.
    """

    DRAFT = NS_SND / "Simons_NS_Paper2_DRAFT_original.tex"
    DRAFT_SHA256 = (
        "f51ed5c05ec3886603a69de942b890dc76c73b3860fe089a056b4665ab8cc4cb"
    )
    AUGUST_SHA256 = (
        "1ff7a211c00d660c30365e5913727f0129cfc5cd76f1f40ed9a47f468c746cc3"
    )
    POLISHED_SHA256 = (
        "b9249af37f3624548d7bee69f26fc2fc0d93c22e744c54cd110810725cd80817"
    )
    ALIAS = "5dfeb6b64_Paper2_April_Spectral_Coherence_DRAFT.tex"
    DOWNLOADS_DRAFT = "675001cd1_Simons_NS_Paper2_DRAFT.tex"

    def test_alias_is_not_refiled_and_not_fixed_or_august(self):
        raw = self.DRAFT.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.DRAFT_SHA256)
        self.assertEqual(len(raw), 26998)
        self.assertEqual(raw.count(b"\n"), 664)
        june = PDF.read_bytes()
        august = PAPER.read_bytes()
        polished = (NS_SND / "NS_Regularity_Final_Polished.tex").read_bytes()
        self.assertEqual(hashlib.sha256(june).hexdigest(), PDF_SHA256)
        self.assertEqual(hashlib.sha256(august).hexdigest(), self.AUGUST_SHA256)
        self.assertEqual(hashlib.sha256(polished).hexdigest(), self.POLISHED_SHA256)
        self.assertEqual(PDF_SHA256, (
            "7de9444d18054fc8f49a52c3fd7ed2f086a7c7d7d6d1e95bad350c378535c41b"
        ))
        self.assertNotEqual(raw, june)
        self.assertNotEqual(raw, august)
        self.assertNotEqual(raw, polished)
        self.assertNotEqual(self.DRAFT_SHA256, PDF_SHA256)
        self.assertNotEqual(self.DRAFT_SHA256, self.AUGUST_SHA256)
        self.assertNotEqual(self.DRAFT_SHA256, self.POLISHED_SHA256)
        tex = raw.decode("utf-8")
        self.assertIn("Implies Global Regularity", tex)
        self.assertIn(r"\date{May 18, 2026}", tex)
        self.assertNotIn("A Spectral Coherence Criterion", tex)
        self.assertNotIn("Dominant-Shell Damping", tex)
        self.assertNotIn("Corrected June 2026", tex)
        self.assertNotIn("Conditional Regularity Criterion", tex)
        self.assertNotIn("Conditional Global-Regularity Framework", tex)
        self.assertNotIn("Goldbach", tex)
        self.assertNotIn("GNC", tex)
        self.assertFalse(
            (NS_SND / "Paper2_April_Spectral_Coherence_DRAFT.tex").is_file(),
            "duplicate of May 18 draft; do not re-file under the Desktop name",
        )
        self.assertFalse(
            (NS_SND / self.ALIAS).is_file(),
            "do not re-file the Base44 hash-prefix name as a second copy",
        )
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file(),
            "do not invent June FIXED TeX from the April Spectral filename",
        )
        self.assertFalse(
            (NS_SND / self.DOWNLOADS_DRAFT).is_file(),
            "do not invent the still-absent Downloads draft from a line count",
        )

    def test_faces_record_alias_and_reject_expected_april_q6_family(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("April Spectral Coherence DRAFT", faces)
        self.assertIn("April Spectral Coherence DRAFT", readme)
        self.assertIn("5dfeb6b64", faces)
        self.assertIn("5dfeb6b64", readme)
        self.assertIn(self.ALIAS, faces)
        self.assertIn("f51ed5c05ec3", faces)
        self.assertIn("f51ed5c05ec3", readme)
        self.assertIn("664", faces)
        self.assertIn("May 18, 2026", faces)
        self.assertIn("Implies Global Regularity", faces)
        self.assertIn("not re-filed", faces.lower())
        self.assertIn("not that family", faces.lower())
        self.assertIn("A Spectral Coherence Criterion", faces)
        self.assertIn("Dominant-Shell", faces)
        self.assertIn("**Not** FIXED", faces)
        self.assertIn("**Not** August", faces)
        self.assertIn("**Not** Clay", faces)
        self.assertIn("Final Polished", faces)
        self.assertIn("b9249af37f", faces)
        self.assertIn("a compile of june pdf", faces.lower())
        self.assertIn("7de9444d", faces)
        self.assertIn("7de9444d", readme)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("do not use as closed", faces.lower())
        self.assertIn("Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex", faces)
        self.assertIn("675001cd1_Simons_NS_Paper2_DRAFT.tex", faces)
        self.assertIn("still absent", faces.lower())
        self.assertIn("base44.app", faces)
        self.assertIn("69b28657b0df374441f0302e", faces)
        self.assertIn("HTTP **302**", faces)
        self.assertIn("HTTP **200**", faces)
        self.assertIn("untrusted alias", faces.lower())
        self.assertIn("HTTP **302**", readme)
        self.assertIn("HTTP **200**", readme)
        self.assertIn("untrusted", readme.lower())

    def test_title_page_is_may18_implies_not_june_fixed_unless_fixed_source(self):
        """This alias is not FIXED PDF 7de9444d unless the title page actually is FIXED TeX."""
        raw = self.DRAFT.read_bytes()
        tex = raw.decode("utf-8")
        identity = classify_paper2_tex_title_page(tex)
        fixed_tex = NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex"
        if identity == "june_fixed_source":
            self.assertTrue(fixed_tex.is_file(), "June title page must be filed as FIXED TeX")
            self.assertEqual(hashlib.sha256(fixed_tex.read_bytes()).hexdigest(), self.DRAFT_SHA256)
            self.assertIn("Conditional Regularity Criterion", tex)
            self.assertIn("Corrected June 2026", tex)
            return
        self.assertEqual(identity, "may18_implies_draft")
        self.assertNotEqual(identity, "june_fixed_source")
        self.assertNotEqual(identity, "april_spectral_coherence")
        self.assertNotEqual(identity, "august_repaired")
        self.assertFalse(fixed_tex.is_file(), "do not invent FIXED TeX from this alias")
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(), PDF_SHA256)
        self.assertEqual(hashlib.sha256(PDF.read_bytes()).hexdigest(), PDF_SHA256)
        self.assertIn("Implies Global Regularity", tex)
        self.assertIn(r"\date{May 18, 2026}", tex)
        self.assertNotIn("Conditional Regularity Criterion", tex)
        self.assertNotIn("Corrected June 2026", tex)
        self.assertIn("T2 — Closed Gronwall Proof", tex)
        self.assertNotIn("QStack", tex)


class TestZenodo20269536IsMay18ImpliesAlias(unittest.TestCase):
    """Zenodo 10.5281/zenodo.20269536 is the May 18 implies TeX, not FIXED.

    Record title is *[Superseded] …Criteria…*. File bytes match
    Simons_NS_Paper2_DRAFT_original.tex (SHA f51ed5c05ec3…). Not a new face.
    Not June FIXED 7de9444d…. Not 20272545. Not Ring. Not swirl.
    """

    DRAFT = NS_SND / "Simons_NS_Paper2_DRAFT_original.tex"
    DRAFT_SHA256 = (
        "f51ed5c05ec3886603a69de942b890dc76c73b3860fe089a056b4665ab8cc4cb"
    )
    AUGUST_SHA256 = (
        "1ff7a211c00d660c30365e5913727f0129cfc5cd76f1f40ed9a47f468c746cc3"
    )
    ZENODO_IMPLIES_PDF = NS_SND / "zenodo-20272545" / "Paper2_NS_Regularity_SND.pdf"
    ZENODO_IMPLIES_SHA256 = (
        "87610856449007e7bdca3b87d82683e463b299484b3906a0dda27a18bec416a3"
    )
    RING_PDF = ROOT / "docs" / "papers" / "ring" / "02_ring_lemma_snd_conditional.pdf"
    RING_PDF_SHA256 = (
        "0304f039406c7a95868b326b62f6c9ed4ea6b8c8386dc86ebd088a1a2ab114a3"
    )
    RING_TEX = ROOT / "docs" / "papers" / "ring" / "RingLemma_Final.tex"
    RING_TEX_SHA256 = (
        "4602065ef68a6eb8402e2c99d708d7be888c4b959122ff8ba4dafbc073440157"
    )
    NOTE = NS_SND / "zenodo-20269536" / "README.md"
    DOI = "10.5281/zenodo.20269536"

    def test_sha_is_may18_draft_and_not_fixed_unless_bytes_match(self):
        raw = self.DRAFT.read_bytes()
        june = PDF.read_bytes()
        draft_sha = hashlib.sha256(raw).hexdigest()
        june_sha = hashlib.sha256(june).hexdigest()
        self.assertEqual(draft_sha, self.DRAFT_SHA256)
        self.assertEqual(june_sha, PDF_SHA256)
        self.assertEqual(
            PDF_SHA256,
            "7de9444d18054fc8f49a52c3fd7ed2f086a7c7d7d6d1e95bad350c378535c41b",
        )
        self.assertEqual(len(raw), 26998)
        self.assertEqual(raw.count(b"\n"), 664)
        self.assertNotEqual(raw, june)
        self.assertNotEqual(draft_sha, PDF_SHA256)
        zen_pdf = self.ZENODO_IMPLIES_PDF.read_bytes()
        self.assertEqual(
            hashlib.sha256(zen_pdf).hexdigest(), self.ZENODO_IMPLIES_SHA256
        )
        self.assertNotEqual(raw, zen_pdf)
        self.assertNotEqual(draft_sha, self.ZENODO_IMPLIES_SHA256)
        august = PAPER.read_bytes()
        self.assertEqual(hashlib.sha256(august).hexdigest(), self.AUGUST_SHA256)
        self.assertNotEqual(raw, august)
        ring_pdf = self.RING_PDF.read_bytes()
        ring_tex = self.RING_TEX.read_bytes()
        self.assertEqual(hashlib.sha256(ring_pdf).hexdigest(), self.RING_PDF_SHA256)
        self.assertEqual(hashlib.sha256(ring_tex).hexdigest(), self.RING_TEX_SHA256)
        self.assertNotEqual(draft_sha, self.RING_PDF_SHA256)
        self.assertNotEqual(draft_sha, self.RING_TEX_SHA256)
        tex = raw.decode("utf-8")
        self.assertIn("Implies Global Regularity", tex)
        self.assertIn(r"\date{May 18, 2026}", tex)
        self.assertNotIn("Corrected June 2026", tex)
        self.assertNotIn("Conditional Regularity Criterion", tex)
        self.assertNotIn("A Spectral Coherence Criterion", tex)

    def test_doi_is_alias_not_a_second_copy(self):
        self.assertTrue(self.NOTE.is_file(), self.NOTE)
        note = self.NOTE.read_text(encoding="utf-8")
        self.assertIn(self.DOI, note)
        self.assertIn("f51ed5c05ec3", note)
        self.assertIn("7de9444d", note)
        self.assertIn("87610856", note)
        self.assertIn("Superseded", note)
        self.assertIn("Criteria", note)
        self.assertIn("2026-05-18", note)
        self.assertIn("simons, jonathan", note)
        self.assertIn("Simons_NS_Paper2_DRAFT.tex", note)
        self.assertIn("22045474", note)
        self.assertIn("19842060", note)
        self.assertIn("do not re-file", note.lower())
        extras = [
            p
            for p in (NS_SND / "zenodo-20269536").iterdir()
            if p.name != "README.md"
        ]
        self.assertEqual(extras, [], f"do not duplicate the TeX under {extras}")
        self.assertFalse((NS_SND / "Simons_NS_Paper2_DRAFT.tex").is_file())
        self.assertFalse(
            (NS_SND / "zenodo-20269536" / "Simons_NS_Paper2_DRAFT.tex").is_file()
        )
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )

    def test_faces_record_doi_and_reject_fixed_ring_swirl(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        ring_faces = (ROOT / "docs" / "papers" / "ring" / "FACES.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(self.DOI, faces)
        self.assertIn(self.DOI, readme)
        self.assertIn("zenodo-20269536", faces)
        self.assertIn("zenodo-20269536", readme)
        self.assertIn("2026-05-18", faces)
        self.assertIn("2026-08-21", faces)
        self.assertIn("simons, jonathan", faces)
        self.assertIn("Superseded - see errata", faces)
        self.assertIn("Spectral Non-Concentration Criteria", faces)
        self.assertIn("f51ed5c05ec3", faces)
        self.assertIn("7de9444d", faces)
        self.assertIn("87610856", faces)
        self.assertIn("0304f039", faces)
        self.assertIn("4602065ef68a", faces)
        self.assertIn("this DOI is not an alias of FIXED", faces)
        self.assertIn("**Not** swirl", faces)
        self.assertIn("22045474", faces)
        self.assertIn("19842060", faces)
        self.assertIn("do not remap", faces.lower())
        self.assertIn("do not revive those maps", faces.lower())
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("do not use as closed", faces.lower())
        self.assertIn("not re-filed", faces.lower())
        self.assertIn(self.DOI, ring_faces)
        self.assertIn("not this Ring book", ring_faces)
        self.assertIn("Paper2", ring_faces)


class TestCleanPdfIsNotPaper2OrFixed(unittest.TestCase):
    """April 2026 Phi-renorm CLEAN ReportLab. Not Paper2. Not FIXED. Not Clay."""

    CLEAN = NS_SND / "00a14f6d9_NS_Simons_2026_CLEAN.pdf"
    CLEAN_SHA256 = (
        "8b4cff04c308b77e9ec5837f5a27c1c82fefadf141465f67fc0e4c4236caf4d4"
    )
    AUDIT = NS_SND / "NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md"
    AUDIT_SHA256 = (
        "53ef73976701da0b6c767c4280b9fcae1ccc71ebb6f06e299681d6ef2e276462"
    )

    def test_hash_lock_distinct_from_three_paper2_pdfs(self):
        self.assertTrue(self.CLEAN.is_file(), self.CLEAN)
        raw = self.CLEAN.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.CLEAN_SHA256)
        self.assertEqual(len(raw), 19393)
        mac = (NS_SND / "Paper2_NS_Regularity_SND.pdf").read_bytes()
        zen = (NS_SND / "zenodo-20272545" / "Paper2_NS_Regularity_SND.pdf").read_bytes()
        june = PDF.read_bytes()
        self.assertEqual(hashlib.sha256(june).hexdigest(), PDF_SHA256)
        self.assertNotEqual(raw, mac)
        self.assertNotEqual(raw, zen)
        self.assertNotEqual(raw, june)
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file(),
            "CLEAN is not the June FIXED TeX and must not invent it",
        )
        try:
            from pypdf import PdfReader
        except ImportError:
            self.skipTest("pypdf not installed")
        reader = PdfReader(str(self.CLEAN))
        self.assertEqual(len(reader.pages), 8)
        meta_title = str(reader.metadata.title) if reader.metadata else ""
        self.assertIn("anonymous", meta_title.lower())
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        self.assertIn("Phi-Renormalization", text)
        self.assertIn("April 2026", text)
        self.assertIn("Axisymmetric", text)
        self.assertNotIn("Conditional Regularity Criterion", text)
        self.assertNotIn("Corrected June 2026", text)

    def test_faces_and_audit_duplicate_note(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        audit = self.AUDIT.read_bytes()
        self.assertEqual(hashlib.sha256(audit).hexdigest(), self.AUDIT_SHA256)
        self.assertIn("00a14f6d9_NS_Simons_2026_CLEAN.pdf", faces)
        self.assertIn("00a14f6d9_NS_Simons_2026_CLEAN.pdf", readme)
        self.assertIn("8b4cff04c308", faces)
        self.assertIn("Phi-Renormalization", faces)
        self.assertIn("a Paper2 SND face", faces)
        self.assertIn("duplicate", faces.lower())
        self.assertIn("53ef73976701", faces)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("**Not** Clay", faces)
        self.assertIn("QStack is **not** in live DA", faces)
        self.assertNotIn("DA-VC-01 PASS", faces)
        self.assertNotIn("DA-VC-01 PASS", readme)
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )
        self.assertFalse(
            (NS_SND / "NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026_aad8.md").is_file(),
            "do not file a second copy of the identical Aug 1 audit",
        )


class TestSnd2UploadsAreMacAliasesNotFixed(unittest.TestCase):
    """Paper2_NS_Regularity_SND_2 / Base44 hashes are aliases. Classify by SHA.

    FIXED only if SHA-256 is 7de9444d… (title *Conditional Regularity Criterion*).
    These SND_2 uploads are Mac SND 2 (9e53d664…, *Implies*, May 18, 2026).
    """

    MAC = NS_SND / "Paper2_NS_Regularity_SND.pdf"
    MAC_SHA256 = (
        "9e53d6640cc3808696afbcbec8f78c08de860b4816680ff43cdc816ce5c60cb0"
    )
    ZENODO_SHA256 = (
        "87610856449007e7bdca3b87d82683e463b299484b3906a0dda27a18bec416a3"
    )
    CLEAN_SHA256 = (
        "8b4cff04c308b77e9ec5837f5a27c1c82fefadf141465f67fc0e4c4236caf4d4"
    )
    DRAFT_TEX_SHA256 = (
        "f51ed5c05ec3886603a69de942b890dc76c73b3860fe089a056b4665ab8cc4cb"
    )
    ALIAS_NAMES = (
        "Paper2_NS_Regularity_SND_2_963e.pdf",
        "Paper2_NS_Regularity_SND_2_7a79.pdf",
    )
    UPLOAD_DIRS = (
        Path("/home/ubuntu/.cursor/projects/workspace/uploads"),
        ROOT / "uploads",
    )

    def _classify(self, digest: str) -> str:
        if digest == PDF_SHA256:
            return "FIXED"
        if digest == self.MAC_SHA256:
            return "MAC_SND2"
        if digest == self.ZENODO_SHA256:
            return "ZENODO_20272545"
        if digest == self.CLEAN_SHA256:
            return "CLEAN_SWIRL"
        if digest == self.DRAFT_TEX_SHA256:
            return "ZENODO_20269536_TEX"
        return "UNKNOWN"

    def test_filed_mac_snd2_is_not_fixed_unless_sha_matches(self):
        raw = self.MAC.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        self.assertEqual(digest, self.MAC_SHA256)
        self.assertEqual(len(raw), 561297)
        self.assertEqual(self._classify(digest), "MAC_SND2")
        self.assertNotEqual(digest, PDF_SHA256)
        self.assertNotEqual(self._classify(digest), "FIXED")
        self.assertNotEqual(digest, self.ZENODO_SHA256)
        self.assertNotEqual(digest, self.CLEAN_SHA256)
        self.assertNotEqual(digest, self.DRAFT_TEX_SHA256)
        june = PDF.read_bytes()
        self.assertEqual(hashlib.sha256(june).hexdigest(), PDF_SHA256)
        self.assertEqual(PDF_SHA256, (
            "7de9444d18054fc8f49a52c3fd7ed2f086a7c7d7d6d1e95bad350c378535c41b"
        ))
        self.assertNotEqual(raw, june)
        try:
            from pypdf import PdfReader
        except ImportError:
            self.skipTest("pypdf not installed")
        mac_text = PdfReader(str(self.MAC)).pages[0].extract_text() or ""
        june_text = PdfReader(str(PDF)).pages[0].extract_text() or ""
        self.assertIn("IMPLIES GLOBAL", mac_text.upper())
        self.assertIn("May 18, 2026", mac_text)
        self.assertNotIn("Conditional Regularity Criterion", mac_text)
        self.assertNotIn("Corrected June 2026", mac_text)
        self.assertIn("Conditional Regularity Criterion", june_text)
        self.assertIn("Corrected June 2026", june_text)
        self.assertNotIn("IMPLIES GLOBAL", june_text.upper())

    def test_snd2_filename_aliases_are_not_refiled(self):
        extras = sorted(
            p.name
            for p in NS_SND.glob("Paper2_NS_Regularity_SND_2*.pdf")
        )
        self.assertEqual(extras, [], f"do not re-file SND_2 aliases: {extras}")
        for name in self.ALIAS_NAMES:
            self.assertFalse(
                (NS_SND / name).is_file(),
                f"do not re-file {name}; it is a Mac SND 2 alias",
            )
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )

    def test_uploads_hash_to_mac_snd2_not_fixed_when_present(self):
        seen = []
        for directory in self.UPLOAD_DIRS:
            if not directory.is_dir():
                continue
            for name in self.ALIAS_NAMES:
                path = directory / name
                if not path.is_file():
                    continue
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                seen.append((str(path), digest))
                label = self._classify(digest)
                if digest == PDF_SHA256:
                    self.assertEqual(label, "FIXED")
                else:
                    self.assertNotEqual(label, "FIXED")
                    self.assertEqual(digest, self.MAC_SHA256)
                    self.assertEqual(label, "MAC_SND2")
                    self.assertNotEqual(digest, PDF_SHA256)
                    self.assertNotEqual(digest, self.ZENODO_SHA256)
        if not seen:
            self.skipTest("SND_2 uploads not present in this environment")

    def test_faces_record_snd2_aliases_not_fixed(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        hay = faces.lower()
        self.assertIn("9e53d664", faces)
        self.assertIn("9e53d664", readme)
        self.assertIn("SND_2", faces)
        self.assertIn("963e", faces)
        self.assertIn("7a79", faces)
        self.assertIn("Paper2_NS_Regularity_SND_2_963e.pdf", faces)
        self.assertIn("Paper2_NS_Regularity_SND_2_7a79.pdf", faces)
        self.assertIn("aliases", hay)
        self.assertIn("not re-filed", hay)
        self.assertIn("Implies Global Regularity", faces)
        self.assertIn("May 18, 2026", faces)
        self.assertIn("7de9444d", faces)
        self.assertIn("87610856", faces)
        self.assertIn("f51ed5c05ec3", faces)
        self.assertIn("**Not** FIXED", faces)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("DA-VC-01 **FAIL**", faces)
        self.assertIn("Letters collide", faces)
        self.assertIn("Dominant-Shell", faces)
        self.assertIn("Q6-augmented", faces)
        self.assertIn("SND_2_963e", readme)
        self.assertIn("7de9444d", readme)
        self.assertIn("not re-filed", readme.lower())
        self.assertNotIn("DA-VC-01 PASS", faces)
        self.assertNotIn("DA-VC-01 PASS", readme)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
