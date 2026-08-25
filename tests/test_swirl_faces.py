#!/usr/bin/env python3
"""Book B swirl faces. Older April/June files are not a compile of 22 August."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SWIRL = ROOT / "docs" / "papers" / "swirl"
NS_SND = ROOT / "docs" / "papers" / "ns-snd"
AUG22 = SWIRL / "Simons_PhiRenorm_Swirl_2026-08-22.tex"
FACES = SWIRL / "FACES.md"
README = SWIRL / "README.md"

AUG22_SHA256 = (
    "eec7aa57b32ac4d87378b6029fa8e0ea68f8cb9c4925c73a06b7841283a89c35"
)
JUNE30_PDF_SHA256 = (
    "2ca8744763cd61bd5ef7c624074ec6b840251f27869801fd735a46c434c35b7a"
)
COMPLETE_SHA256 = (
    "3190b8bd45bc1086eecac022cdef35fa3f4652946dd9d10ffe84d0f24738a41d"
)
FINAL_V2_SHA256 = (
    "96de5f7c2cae2ae3fb0c64cfbaba797f7a611735280f5881a8dfc32ec989dd01"
)
MAY_PDF_SHA256 = (
    "477a857f8ab4e066d1ef2be7e05786a4dd101cd31b325ab484e4f0ddef11f6cd"
)
MAY_TEX_SHA256 = (
    "01c47ff4ab9013ff92c616fbd2e973f083c583226d84c31d6aded3b478a330cb"
)


class TestControllingSwirlFaceIs22August(unittest.TestCase):
    def test_august_tex_hash_is_frozen(self):
        self.assertTrue(AUG22.is_file(), AUG22)
        raw = AUG22.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), AUG22_SHA256)
        self.assertEqual(len(raw), 37042)
        tex = raw.decode("utf-8")
        self.assertIn(r"\date{22 August 2026}", tex)
        self.assertIn("five-dimensional energy", tex)
        self.assertIn(r"\Ph:=\frac{\ut}{r}", tex)


class TestOlderSwirlFacesAreNotACompileOf22August(unittest.TestCase):
    JUNE30 = SWIRL / "Simons_PhiRenorm_Swirl_2026-06-30.pdf"
    COMPLETE = SWIRL / "NS_PhiRenorm_complete.tex"
    FINAL_V2 = SWIRL / "PhiRenorm_FINAL_v2.tex"
    MAY_PDF = SWIRL / "zenodo-may" / "PhiRenorm_TrackB.pdf"
    MAY_TEX = SWIRL / "zenodo-may" / "Simons_PhiRenorm_Axisymmetric.tex"

    def test_hash_locks_and_distinct_bytes(self):
        june = self.JUNE30.read_bytes()
        complete = self.COMPLETE.read_bytes()
        final = self.FINAL_V2.read_bytes()
        may_pdf = self.MAY_PDF.read_bytes()
        may_tex = self.MAY_TEX.read_bytes()
        aug = AUG22.read_bytes()
        self.assertEqual(hashlib.sha256(june).hexdigest(), JUNE30_PDF_SHA256)
        self.assertEqual(hashlib.sha256(complete).hexdigest(), COMPLETE_SHA256)
        self.assertEqual(hashlib.sha256(final).hexdigest(), FINAL_V2_SHA256)
        self.assertEqual(hashlib.sha256(may_pdf).hexdigest(), MAY_PDF_SHA256)
        self.assertEqual(hashlib.sha256(may_tex).hexdigest(), MAY_TEX_SHA256)
        self.assertEqual(len(june), 416268)
        self.assertEqual(len(complete), 39950)
        self.assertEqual(len(final), 29703)
        blobs = (june, complete, final, may_pdf, may_tex, aug)
        for i, left in enumerate(blobs):
            for right in blobs[i + 1 :]:
                self.assertNotEqual(left, right)

    def test_complete_tex_is_april_conditional_reduction(self):
        tex = self.COMPLETE.read_text(encoding="utf-8")
        self.assertIn("April 2026", tex)
        self.assertIn("Conditional Reduction of Global Regularity", tex)
        self.assertIn(r"\Phi = u^\theta/r", tex)
        self.assertNotIn("22 August 2026", tex)
        self.assertNotIn("five-dimensional energy", tex)
        self.assertEqual(tex.count("\n"), 999)

    def test_final_v2_is_june_track_b_and_not_claimed(self):
        # Uploaded suffix was .tex_2; file has a byte-corrupted tabular.
        raw = self.FINAL_V2.read_bytes()
        tex = raw.decode("latin-1")
        self.assertIn("June 2026", tex)
        self.assertIn("Preprint (Track B)", tex)
        self.assertIn("Not claimed", tex)
        self.assertIn("global regularity (no augmentation)", tex)
        self.assertIn(r"\Phi = \frac{\Gamma}{r^2} = \frac{u_\theta}{r}", tex)
        self.assertNotIn("22 August 2026", tex)
        self.assertEqual(raw.count(b"\n"), 249)

    def test_faces_and_readme_split_the_book(self):
        faces = FACES.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("not a compile of 22 august", faces.lower())
        self.assertIn("Simons_PhiRenorm_Swirl_2026-06-30.pdf", faces)
        self.assertIn("NS_PhiRenorm_complete.tex", faces)
        self.assertIn("PhiRenorm_FINAL_v2.tex", faces)
        self.assertIn("NOT CLAIMED", faces)
        self.assertIn("eec7aa57b32a", faces)
        self.assertIn("2ca8744763cd", faces)
        self.assertIn("not a compile of 22 august", readme.lower())
        self.assertIn("NOT CLAIMED", readme)
        self.assertIn(r"u_\theta/r", readme)
        self.assertNotIn("Paper2_NS_Regularity_SND_FIXED.tex", "".join(
            p.name for p in NS_SND.iterdir() if p.is_file()
        ))
        self.assertFalse(
            (NS_SND / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
