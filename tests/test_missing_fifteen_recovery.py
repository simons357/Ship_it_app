#!/usr/bin/env python3
"""Drive Missing Fifteen + Base44 Grok recovery: identities, not substitutes."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKETS = ROOT / "docs" / "packets"
NS_SND = ROOT / "docs" / "papers" / "ns-snd"
RING = ROOT / "docs" / "papers" / "ring"
ARCHIVE_SFE = ROOT / "docs" / "archive" / "sfe-hb"
ARCHIVE_GCD = ROOT / "docs" / "archive" / "gcd-spectral-attractor-2026-05"
LIVE_ROOT = ROOT / "domain_architect"

MISSING = PACKETS / "MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md"
BASE44 = PACKETS / "BASE44-RECOVERY-REPORT-FOR-GROK-2026-08-25.md"
LOOKUP = PACKETS / "OLD-PAPERS-LOOK-UP.md"
FACES_NS = NS_SND / "FACES.md"
FACES_RING = RING / "FACES.md"
README_NS = NS_SND / "README.md"

UNIFICATION = ARCHIVE_SFE / "SPECTRAL_UNIFICATION_PAPER.tex"
UNIFICATION_SHA256 = (
    "4ea7ccd72dc60d773e603aee0328a10ad254376c465d1ee1ddee849d35f2291c"
)
MIX = ARCHIVE_GCD / "Simons_GCD_Spectral_Attractor_Unified.tex"
MIX_SHA256 = "f41194c76cf422a227d6b7489d4a6c95bf7f717404213e6a02a29239a14aeec5"
Q6_SHA256 = "a239112289a1a150d7a7a2212ec7f3649382b81542b49d5d2300f8611df3d6b1"
FIXED_PDF = NS_SND / "Paper2_NS_Regularity_SND_FIXED.pdf"
FIXED_PDF_SHA256 = (
    "7de9444d18054fc8f49a52c3fd7ed2f086a7c7d7d6d1e95bad350c378535c41b"
)
REPAIRED = NS_SND / "Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex"
RING_FINAL = RING / "RingLemma_Final.tex"
RING_FINAL_SHA256 = (
    "4602065ef68a6eb8402e2c99d708d7be888c4b959122ff8ba4dafbc073440157"
)
RING_JUNE19 = RING / "RingLemma_Simons_June19_2026.tex"
RING_JUNE19_SHA256 = (
    "a73d949f51a122ada93d6341926990991f7fd04e6cd5146a79b27d3d4ca99961"
)


class TestRecoveryPacketsExist(unittest.TestCase):
    def test_packets_lock_instructions_and_rejects(self):
        self.assertTrue(MISSING.is_file(), MISSING)
        self.assertTrue(BASE44.is_file(), BASE44)
        missing = MISSING.read_text(encoding="utf-8")
        base44 = BASE44.read_text(encoding="utf-8")
        lookup = LOOKUP.read_text(encoding="utf-8")
        faces = FACES_NS.read_text(encoding="utf-8")
        for text in (missing, base44, lookup, faces):
            self.assertIn("NOT CLAIMED", text)
            self.assertIn("Stop Paper 2 reconstruction", text)
            self.assertNotIn("DA-VC-01 PASS", text)
        self.assertIn("REJECT", missing)
        self.assertIn("Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex", missing)
        self.assertIn("RingLemma_Final.tex", missing)
        self.assertIn("c8a03f315_RingLemma_Simons_June19_2026.tex", missing)
        self.assertIn("74ecca4e5", missing)
        self.assertIn("CURRENT_CLAIM_LEDGER.md", missing)
        self.assertIn("does it have J?", missing)
        self.assertIn("ChatVault", missing)
        self.assertIn("not a product rewrite", missing.lower())
        self.assertIn("Route J", base44)
        self.assertIn("Triple Lock", base44)
        self.assertIn("separate", base44.lower())
        self.assertIn("conditional structural-exclusion framework", base44)
        self.assertIn("A Spectral Coherence Criterion", base44)
        self.assertIn("April 23", base44)
        self.assertIn("7de9444d", base44)
        self.assertIn("f246f9e41_GCD_SPECTRAL_ATTRACTOR_MAGNUM", base44)
        self.assertIn("index miss", base44)
        self.assertIn("ChatVaultEntry", base44)
        self.assertIn("/app/SPECTRAL_UNIFICATION_PAPER.tex", base44)
        self.assertIn("/app/GOLD/SPECTRAL_UNIFICATION_PAPER.tex", base44)
        self.assertIn("/app/ARCHIVE/math_drafts/GCD_SPECTRAL_ATTRACTOR_MAGNUM.tex", base44)
        self.assertIn("CLAIM_LEDGER.md", base44)
        self.assertIn("once recovered", base44)
        self.assertIn("Do **not** blend", base44)
        self.assertIn("BASE44-RECOVERY-REPORT-FOR-GROK-2026-08-25.md", lookup)
        self.assertIn("MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md", lookup)


class TestRecoveredShasAlreadyInGit(unittest.TestCase):
    def test_unification_matches_base44_report(self):
        raw = UNIFICATION.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), UNIFICATION_SHA256)
        self.assertEqual(len(raw), 10586)
        tex = raw.decode("utf-8")
        self.assertIn("One Operator, Three Millennia", tex)
        self.assertIn("June 10, 2026", tex)
        self.assertIn("Status: Proved", tex)
        note = (ARCHIVE_SFE / "SPECTRAL_UNIFICATION_PAPER.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("rejected", note.lower())
        self.assertIn("/app/SPECTRAL_UNIFICATION_PAPER.tex", note)
        self.assertIn("/app/GOLD/", note)
        self.assertFalse((LIVE_ROOT / "SPECTRAL_UNIFICATION_PAPER.tex").is_file())

    def test_magnum_matches_chatvault_verified_url_not_q6(self):
        raw = MIX.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), MIX_SHA256)
        self.assertNotEqual(MIX_SHA256, Q6_SHA256)
        self.assertFalse(
            (ARCHIVE_GCD / "GCD_SPECTRAL_ATTRACTOR_MAGNUM.tex").is_file()
        )
        alias = (ARCHIVE_GCD / "GCD_SPECTRAL_ATTRACTOR_MAGNUM.ALIAS.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("f246f9e41_", alias)
        self.assertIn("224b718b3_", alias)
        self.assertIn("index miss", alias)
        self.assertIn("ChatVaultEntry", alias)
        self.assertIn("/app/ARCHIVE/math_drafts/GCD_SPECTRAL_ATTRACTOR_MAGNUM.tex", alias)
        self.assertIn("a239112289a1", alias)


class TestJuneFixedTexStillMissingStopReconstruction(unittest.TestCase):
    def test_tex_absent_pdf_kept_repaired_excluded(self):
        self.assertFalse((NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file())
        pdf = FIXED_PDF.read_bytes()
        self.assertEqual(hashlib.sha256(pdf).hexdigest(), FIXED_PDF_SHA256)
        self.assertEqual(len(pdf), 309576)
        self.assertTrue(REPAIRED.is_file())
        self.assertNotEqual(
            hashlib.sha256(REPAIRED.read_bytes()).hexdigest(),
            FIXED_PDF_SHA256,
        )
        faces = FACES_NS.read_text(encoding="utf-8")
        readme = README_NS.read_text(encoding="utf-8")
        base44 = BASE44.read_text(encoding="utf-8")
        for text in (faces, readme, base44):
            self.assertIn("Stop Paper 2 reconstruction", text)
            self.assertIn("7de9444d", text)
        self.assertIn("REJECT as identity", faces)
        self.assertIn("April 23", base44)
        self.assertIn("Dominant-Shell", base44)
        collapsed_base44 = " ".join(base44.lower().replace("*", " ").split())
        self.assertIn("not the april 23", collapsed_base44)
        named = list((ROOT / "docs").rglob("Paper2_NS_Regularity_SND_FIXED.tex"))
        self.assertEqual(named, [])


class TestRingJune19IsNotFinal(unittest.TestCase):
    def test_drive_high_substitute_rejected(self):
        final = RING_FINAL.read_bytes()
        june19 = RING_JUNE19.read_bytes()
        self.assertEqual(hashlib.sha256(final).hexdigest(), RING_FINAL_SHA256)
        self.assertEqual(hashlib.sha256(june19).hexdigest(), RING_JUNE19_SHA256)
        self.assertEqual(len(final), 21216)
        self.assertEqual(len(june19), 44368)
        self.assertNotEqual(final, june19)
        faces = FACES_RING.read_text(encoding="utf-8")
        missing = MISSING.read_text(encoding="utf-8")
        self.assertIn("REJECT as identity", faces)
        self.assertIn("REJECT", missing)
        self.assertIn("a73d949f51a122", missing)
        self.assertIn("4602065ef68a", missing)


class TestStillMissingExactNames(unittest.TestCase):
    def test_requested_absentees_are_absent(self):
        absent = [
            NS_SND / "SND_GNC_BRIDGE_EXTRACTED.txt",
            ROOT / "docs" / "papers" / "swirl" / "SYNTHESIS-AXISYMMETRIC-SND-BRIDGE.md",
            NS_SND / "03_t2_shell_flux_gronwall.tex",
            NS_SND / "CURRENT_CLAIM_LEDGER.md",
            ROOT / "docs" / "archive" / "anesthesia-claim-governance"
            / "CURRENT_CLAIM_LEDGER_JULY23_FULL.md",
            NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex",
            ROOT / "docs" / "papers" / "anesthesia" / "PAPER1_REBUILT_Coherence_Index.md",
        ]
        for path in absent:
            self.assertFalse(path.is_file(), path)
        missing = MISSING.read_text(encoding="utf-8")
        for name in (
            "SND_GNC_BRIDGE_EXTRACTED.txt",
            "SYNTHESIS-AXISYMMETRIC-SND-BRIDGE.md",
            "03_t2_shell_flux_gronwall.tex",
            "CURRENT_CLAIM_LEDGER.md",
            "CURRENT_CLAIM_LEDGER_JULY23_FULL.md",
            "Paper2_NS_Regularity_SND_FIXED.tex",
            "PAPER1_REBUILT_Coherence_Index.md",
        ):
            self.assertIn(name, missing)
        self.assertIn("Do **not** glue swirl leftover", missing)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
