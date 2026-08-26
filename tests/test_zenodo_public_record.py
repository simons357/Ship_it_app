"""Public-facing Zenodo restore pack: clean titles, page-1 footnote, page-2 errata."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from pypdf import PdfReader

_REPO = Path(__file__).resolve().parents[1]
_PACK = _REPO / "docs" / "zenodo-public-record"
_GEN = _PACK / "generate_public_record.py"
_API = _PACK / "api_restore_titles.py"
_TITLES = _PACK / "titles.json"
_OUT = _PACK / "out"

_PAGE1_FORBIDDEN = ("Claim withdrawn", "[Superseded", "WITHDRAWN")
_PAUSE = "I am pausing this research line"
_FOOTNOTE_NEEDLES = (
    "prize-claim language walked back",
    "page 2 of this file",
    "10.5281/zenodo.22050978",
)


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

    def test_status_note_page1_footnote_page2_errata(self) -> None:
        page1 = _page_text(self.status, 0)
        page2 = _page_text(self.status, 1)
        for blob in _PAGE1_FORBIDDEN:
            self.assertNotIn(blob, page1)
        self.assertNotIn(_PAUSE, page1)
        self.assertNotIn(_PAUSE, page2)
        self.assertIn("errata", page2.lower())
        self.assertIn("live", page1.lower())
        for needle in _FOOTNOTE_NEEDLES:
            self.assertIn(needle, page1, msg=f"missing footnote text {needle!r}")
        self.assertIn("10.5281/zenodo.22050976", page1)
        self.assertNotIn("Why the August 2026 action happened", page1)
        self.assertIn("Why the August 2026 action happened", page2)
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
                self.assertNotIn(blob, page2, msg=f"{pdf} page2 has {blob!r}")
            self.assertNotIn(_PAUSE, page1)
            self.assertIn("errata", page2.lower())
            for needle in _FOOTNOTE_NEEDLES:
                self.assertIn(
                    needle,
                    page1,
                    msg=f"{pdf} page1 missing footnote {needle!r}",
                )
            self.assertNotIn("Why the August 2026 action happened", page1)
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
            self.assertIn("prize-claim language walked back", page1)
            self.assertIn("10.5281/zenodo.22050978", page1)

    def test_unicode_titles_render(self) -> None:
        pdf = _OUT / "20552400_public_facing.pdf"
        page1 = _page_text(pdf, 0)
        self.assertTrue(
            "SND" in page1 and "GNC" in page1 and "Bridge" in page1,
            msg=page1[:400],
        )
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
        self.assertEqual(
            by_id[20183673],
            "Diffuse Cascade in 3D Navier–Stokes: Time-Resolved Evidence for Triad Equidistribution",
        )
        self.assertEqual(
            by_id[20184148],
            "The Montgomery–Dyson Coincidence Resolved by the Q6 Prime Lattice Operator",
        )
        self.assertEqual(
            by_id[20271879],
            "Spectral Properties of GCD Operators and Ramanujan Quadratic Forms",
        )
        self.assertIn(20272622, by_id)
        self.assertIn(20405585, by_id)
        self.assertIn(20269536, by_id)
        self.assertNotIn(20269738, by_id)
        self.assertNotIn(19842061, by_id)
        self.assertEqual(
            self.titles["optional_rename"][0]["restore_title"],
            "The Inverse-GCD Operator Q_N: Definitions and a Restricted Rayleigh Bound",
        )

    def test_live_clean_includes_ring_q6_and_may18_gcd(self) -> None:
        live = {row["id"]: row for row in self.titles["live_clean"]}
        self.assertEqual(
            live[22050976]["title"],
            "A Ring Lemma for Band-Limited Vorticity Direction and a Conditional Spectral Non-Dispersal Criterion",
        )
        self.assertEqual(
            live[20269738]["title"],
            "Spectral Properties of the GCD Operator and the Ramanujan–Möbius Identity",
        )
        self.assertEqual(
            live[22050962]["doi"],
            "10.5281/zenodo.22050962",
        )
        self.assertEqual(self.titles["fact_check"]["unrelated_ids"][0]["id"], 19842061)

    def test_paste_sheet_is_not_a_click_edit_checklist(self) -> None:
        paste = (_OUT / "PASTE_TITLES.md").read_text(encoding="utf-8")
        self.assertIn("api_restore_titles.py --apply", paste)
        self.assertNotIn("Click **Edit**", paste)
        jobs = (_OUT / "RESTORE_JOBS.md").read_text(encoding="utf-8")
        self.assertIn("api_restore_titles.py --apply", jobs)
        self.assertIn("20183673", jobs)
        self.assertIn("20184148", jobs)

    def test_api_restore_dry_run_and_apply_without_token(self) -> None:
        env = {k: v for k, v in os.environ.items() if not k.startswith("ZENODO")}
        dry = subprocess.run(
            [sys.executable, str(_API)],
            cwd=_REPO,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(dry.returncode, 0, msg=dry.stderr)
        self.assertIn("20183673", dry.stdout)
        self.assertIn("22050978", dry.stdout)
        self.assertIn("--apply", dry.stdout)
        applied = subprocess.run(
            [sys.executable, str(_API), "--apply"],
            cwd=_REPO,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(applied.returncode, 2, msg=applied.stdout)
        err = applied.stderr.lower()
        self.assertIn("personal access token", err)
        self.assertIn("deposit:write", err)
        self.assertNotIn("password", applied.stdout.lower())


if __name__ == "__main__":
    unittest.main()
