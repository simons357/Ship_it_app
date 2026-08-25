#!/usr/bin/env python3
"""Q6 arithmetic stays in gcd/. MAGNUM hash-prefix is an alias of the archived mix TeX."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GCD = ROOT / "docs" / "papers" / "gcd"
ARCHIVE = ROOT / "docs" / "archive" / "gcd-spectral-attractor-2026-05"
LIVE_ROOT = ROOT / "domain_architect"
NS_SND = ROOT / "docs" / "papers" / "ns-snd"

Q6_PDF = GCD / "04_q6_inverse_gcd.pdf"
Q6_SHA256 = "a239112289a1a150d7a7a2212ec7f3649382b81542b49d5d2300f8611df3d6b1"
MIX_TEX = ARCHIVE / "Simons_GCD_Spectral_Attractor_Unified.tex"
MIX_SHA256 = "f41194c76cf422a227d6b7489d4a6c95bf7f717404213e6a02a29239a14aeec5"
MIX_MD5 = "4668827389bbf4d893957bb253a34a98"
HN_LAB = "HN = D^((-1)/2)*Qtilde*D^((-1)/2)"
MAGNUM_NAME = "GCD_SPECTRAL_ATTRACTOR_MAGNUM.tex"
HASH_PREFIX = "224b718b3_GCD_SPECTRAL_ATTRACTOR_MAGNUM"
HASH_PREFIX_F246 = "f246f9e41_GCD_SPECTRAL_ATTRACTOR_MAGNUM"


class TestQ6PdfIsCurrentArithmeticFace(unittest.TestCase):
    def test_hash_title_and_usable_h(self):
        self.assertTrue(Q6_PDF.is_file(), Q6_PDF)
        raw = Q6_PDF.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), Q6_SHA256)
        self.assertEqual(len(raw), 238962)
        readme = (GCD / "README.md").read_text(encoding="utf-8")
        faces = (GCD / "FACES.md").read_text(encoding="utf-8")
        for text in (readme, faces):
            self.assertIn(HN_LAB, text)
            self.assertIn("a239112289a1", text)
            self.assertIn("Inverse-GCD Operator", text)
            self.assertIn("August 2026", text)
            self.assertIn("Do not overwrite", text)
            self.assertIn(r"\lambda_{\min}>-1/2", text)
            self.assertIn("Goldbach", text)
            self.assertIn("H_N[a]", text)
            self.assertIn("Paper2", text)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("NOT CLAIMED", readme)


class TestMagnumHashPrefixIsMixAlias(unittest.TestCase):
    def test_no_second_magnum_tex_copy(self):
        invented = [
            GCD / MAGNUM_NAME,
            ARCHIVE / MAGNUM_NAME,
            ARCHIVE / f"{HASH_PREFIX}.tex",
            ARCHIVE / f"{HASH_PREFIX_F246}.tex",
            ROOT / "docs" / "archive" / MAGNUM_NAME,
            NS_SND / MAGNUM_NAME,
            LIVE_ROOT / MAGNUM_NAME,
        ]
        for path in invented:
            self.assertFalse(path.is_file(), f"do not re-file {path}")
        named = list((ROOT / "docs").rglob("GCD_SPECTRAL_ATTRACTOR_MAGNUM.tex"))
        self.assertEqual(named, [])
        self.assertFalse((ARCHIVE / "GCD_SPECTRAL_ATTRACTOR_MAGNUM.MISSING.md").is_file())

    def test_alias_receipt_locks_the_fetch(self):
        receipt = ARCHIVE / "GCD_SPECTRAL_ATTRACTOR_MAGNUM.ALIAS.md"
        self.assertTrue(receipt.is_file(), receipt)
        text = receipt.read_text(encoding="utf-8")
        self.assertIn("alias", text.lower())
        self.assertIn("not re-filed", text.lower())
        self.assertIn(HASH_PREFIX, text)
        self.assertIn(HASH_PREFIX_F246, text)
        self.assertIn("HTTP **302**", text)
        self.assertIn("**200**", text)
        self.assertIn("**403**", text)
        self.assertIn("37 366", text)
        self.assertIn("f41194c76cf4", text)
        self.assertIn("a239112289a1", text)
        self.assertIn("May 25, 2026", text)
        self.assertIn("The GCD Spectral Attractor", text)
        self.assertIn(HN_LAB, text)
        self.assertIn("import into `domain_architect/`", text)
        self.assertIn("Do not invent", text)
        self.assertIn("Overleaf audit", text)
        self.assertIn("July 23", text)
        self.assertIn("7de9444d", text)
        self.assertNotIn("DA-VC-01 PASS", text)


class TestMayMixTexStaysArchivedAndIsNotQ6(unittest.TestCase):
    def test_hash_title_date_and_mix(self):
        self.assertTrue(MIX_TEX.is_file(), MIX_TEX)
        raw = MIX_TEX.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), MIX_SHA256)
        self.assertEqual(hashlib.md5(raw).hexdigest(), MIX_MD5)
        self.assertEqual(len(raw), 37366)
        self.assertEqual(raw.count(b"\n"), 1089)
        tex = raw.decode("utf-8")
        self.assertIn(r"\textbf{The GCD Spectral Attractor}", tex)
        self.assertIn(r"\date{May 25, 2026}", tex)
        self.assertIn("Navier--Stokes Regularity", tex)
        self.assertIn("Riemann Hypothesis", tex)
        self.assertIn("Simons Field Equation", tex)
        self.assertIn("Goldbach", tex)
        self.assertIn("Clay Millennium", tex)
        self.assertNotIn(r"\date{August 2026}", tex)
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(), Q6_SHA256)
        self.assertNotEqual(raw, Q6_PDF.read_bytes())

    def test_readme_banners_keep_books_split(self):
        note = (ARCHIVE / "README.md").read_text(encoding="utf-8")
        faces = (GCD / "FACES.md").read_text(encoding="utf-8")
        readme = (GCD / "README.md").read_text(encoding="utf-8")
        index = (ROOT / "docs" / "archive" / "README.md").read_text(encoding="utf-8")
        lookup = (ROOT / "docs" / "packets" / "OLD-PAPERS-LOOK-UP.md").read_text(
            encoding="utf-8"
        )
        for text in (note, faces, readme, index, lookup):
            self.assertIn(HASH_PREFIX, text)
            self.assertIn(HASH_PREFIX_F246, text)
            self.assertIn("GCD_SPECTRAL_ATTRACTOR_MAGNUM", text)
            self.assertIn("alias", text.lower())
            self.assertIn("not re-filed", text.lower())
        for text in (note, faces, readme):
            self.assertIn("archive only", text.lower())
            self.assertIn("f41194c76cf4", text)
            self.assertIn("a239112289a1", text)
            self.assertIn("20405599", text)
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("May 25, 2026", note)
        self.assertIn("gcd-spectral-attractor-2026-05/", index)
        self.assertIn("not live DA", index)
        self.assertIn("Do not invent TeX", note)
        self.assertIn("import into `domain_architect/`", note)
        self.assertIn("NOT CLAIMED", note)
        self.assertIn("OVERLEAF-VS-PACK-AUDIT-2026-08-15.md", faces)
        self.assertIn("OVERLEAF-VS-PACK-AUDIT-2026-08-15.md", readme)
        self.assertIn("pack-only", faces.lower())
        self.assertIn("PAPER_A", faces)
        self.assertNotIn("DA-VC-01 PASS", note)
        self.assertNotIn("DA-VC-01 PASS", readme)
        self.assertFalse((LIVE_ROOT / "gcd_spectral_attractor.py").is_file())
        self.assertFalse((GCD / MIX_TEX.name).is_file())
        self.assertFalse((NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file())
        self.assertNotIn(MAGNUM_NAME, [p.name for p in GCD.iterdir() if p.is_file()])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
