"""Public-facing Zenodo restore pack: clean titles, page-1 honesty, page-2 errata."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from pypdf import PdfReader

_REPO = Path(__file__).resolve().parents[1]
_PACK = _REPO / "docs" / "zenodo-public-record"
_GEN = _PACK / "generate_public_record.py"
_TITLES = _PACK / "titles.json"
_OUT = _PACK / "out"

_PAGE1_FORBIDDEN = ("Claim withdrawn", "[Superseded")
_PAUSE = "I am pausing this research line"


def _page_text(path: Path, index: int) -> str:
    reader = PdfReader(str(path))
    return reader.pages[index].extract_text() or ""


def _meta_title(path: Path) -> str:
    reader = PdfReader(str(path))
    meta = reader.metadata or {}
    return str(meta.title or "")


class TestZenodoPublicRecord(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(_GEN)])
        cls.titles = json.loads(_TITLES.read_text(encoding="utf-8"))
        cls.status = _OUT / "status_note_public_facing.pdf"

    def test_generator_wrote_status_note(self) -> None:
        self.assertTrue(self.status.is_file())
        self.assertGreater(self.status.stat().st_size, 1000)

    def test_titles_json_restore_titles_have_no_withdrawn_prefix(self) -> None:
        for rec in self.titles["restore"]:
            title = rec["restore_title"]
            lowered = title.lower()
            self.assertFalse(
                lowered.startswith("[claim withdrawn"),
                msg=title,
            )
            self.assertFalse(lowered.startswith("[superseded"), msg=title)
            self.assertNotIn("withdrawn", lowered)
            self.assertNotIn("superseded", lowered)
        status_title = self.titles["status_note"]["restore_title"]
        self.assertNotIn("withdrawn", status_title.lower())
        self.assertNotIn("What Stands and What Is Withdrawn", status_title)
        for rec in self.titles.get("optional_rename", []):
            self.assertNotIn("withdrawn", rec["restore_title"].lower())

    def test_status_note_page1_clean_page2_errata(self) -> None:
        page1 = _page_text(self.status, 0)
        page2 = _page_text(self.status, 1)
        for blob in _PAGE1_FORBIDDEN:
            self.assertNotIn(blob, page1)
        self.assertNotIn(_PAUSE, page1)
        self.assertNotIn(_PAUSE, page2)
        self.assertIn("errata", page2.lower())
        self.assertIn("walked back", page1.lower())
        self.assertIn("live", page1.lower())
        self.assertGreaterEqual(len(PdfReader(str(self.status)).pages), 2)
        meta = _meta_title(self.status)
        self.assertNotIn("Withdrawn", meta)
        self.assertEqual(
            meta,
            "August 2026 status note: live stack and walked-back prize language",
        )

    def test_wrapped_and_notice_pdfs_page1_clean(self) -> None:
        for rec in self.titles["restore"]:
            pdf = _OUT / rec["upload_pdf"]
            self.assertTrue(pdf.is_file(), msg=str(pdf))
            page1 = _page_text(pdf, 0)
            page2 = _page_text(pdf, 1)
            for blob in _PAGE1_FORBIDDEN:
                self.assertNotIn(blob, page1, msg=f"{pdf} page1 has {blob!r}")
            self.assertNotIn(_PAUSE, page1)
            self.assertIn("errata", page2.lower())
            self.assertEqual(_meta_title(pdf), rec["restore_title"])
            reader = PdfReader(str(pdf))
            if rec["kind"] == "wrap":
                self.assertGreaterEqual(len(reader.pages), 3)
            else:
                self.assertEqual(len(reader.pages), 2)

    def test_optional_reader_notices_exist_and_page1_clean(self) -> None:
        for rec in self.titles["live_clean"]:
            rel = rec.get("optional_upload_pdf")
            if not rel:
                continue
            pdf = _OUT / rel
            self.assertTrue(pdf.is_file(), msg=str(pdf))
            page1 = _page_text(pdf, 0)
            for blob in _PAGE1_FORBIDDEN:
                self.assertNotIn(blob, page1)
            self.assertIn("OPTIONAL", page1)

    def test_unicode_titles_render(self) -> None:
        pdf = _OUT / "20552400_public_facing.pdf"
        page1 = _page_text(pdf, 0)
        self.assertTrue(
            "SND" in page1 and "GNC" in page1 and "Bridge" in page1,
            msg=page1[:400],
        )
        # DejaVu should keep the identity glyph; fall back to the letters.
        self.assertIn("Universal Non-Concentration Principle", page1)

    def test_exact_restore_map(self) -> None:
        by_id = {rec["id"]: rec["restore_title"] for rec in self.titles["restore"]}
        self.assertEqual(
            by_id[20405526],
            "Global Regularity of the Navier-Stokes Equations on T3: Spectral Non-Dispersal, the Ring Lemma, Phi-Renormalization, and the Shell-Conditioned Commutator Estimate",
        )
        self.assertEqual(
            by_id[20552682],
            "The Prime Lattice as a Prototype for the BSD Hamiltonian: Rank as Spectral Multiplicity and the Zeta-Function Case of the Birch and Swinnerton-Dyer Conjecture",
        )
        self.assertEqual(
            by_id[20272545],
            "Spectral Non-Concentration Implies Global Regularity for 3D Navier–Stokes on T³",
        )
        self.assertEqual(
            by_id[20405599],
            "The GCD Spectral Attractor: A Unified Structural Framework for Navier-Stokes, the Riemann Hypothesis, and the Simons Field Equation",
        )
        self.assertEqual(
            by_id[20271457],
            "The Ramanujan–Möbius Identity and Prime Lattice Spectral Theory: GCD Operators, Spectral Floors, and the Arithmetic Casimir Constant",
        )
        self.assertIn(20272622, by_id)
        self.assertIn(20405585, by_id)
        self.assertIn(20269536, by_id)
        self.assertEqual(
            self.titles["optional_rename"][0]["restore_title"],
            "The Inverse-GCD Operator Q_N: Definitions and a Restricted Rayleigh Bound",
        )


if __name__ == "__main__":
    unittest.main()
