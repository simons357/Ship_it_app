"""NAV-42 / CBFD April 2026 Grok dump is archive Track A/B/C, not Domain Architect."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive" / "nav-42-cbfd-2026-04"
DA_PY = ROOT / "domain_architect"


class TestNav42CbfdArchive(unittest.TestCase):
    def test_track_a_exists_and_rejects_false_multiplier(self) -> None:
        text = (ARCHIVE / "TRACK-A.md").read_text(encoding="utf-8")
        self.assertIn("A_3", text)
        self.assertIn("eigenbasis", text.lower())
        self.assertIn("false in general", text.lower())
        self.assertIn("Clay NOT CLAIMED", text)
        self.assertIn("**Not** Domain Architect", text)
        self.assertIn("**Not** Paper2 SND", text)
        self.assertIn("A_{\\omega S}", text)
        self.assertIn("D_\\xi", text)
        self.assertIn("H_{NS}", text)

    def test_track_a_does_not_claim_production_dominated_by_a3(self) -> None:
        text = (ARCHIVE / "TRACK-A.md").read_text(encoding="utf-8")
        self.assertIn("not a multiplier that dominates", text.lower())
        self.assertIn("intermediate-eigenvector", text.lower())

    def test_track_bc_segregates_speculative_layers(self) -> None:
        text = (ARCHIVE / "TRACK-BC.md").read_text(encoding="utf-8")
        self.assertIn("Anti-twisting", text)
        self.assertIn("Helicity", text)
        self.assertIn("Q Operating System", text)
        self.assertIn("qc_coherence", text)
        self.assertIn("Forbidden", text)
        self.assertIn("cylinder-wake", text)

    def test_readme_points_at_tracks(self) -> None:
        text = (ARCHIVE / "README.md").read_text(encoding="utf-8")
        self.assertIn("TRACK-A.md", text)
        self.assertIn("TRACK-BC.md", text)
        self.assertIn("do **not** dump", text.lower())
        bc = (ARCHIVE / "TRACK-BC.md").read_text(encoding="utf-8")
        self.assertIn("do not dump", bc.lower())
        index = (ROOT / "docs" / "archive" / "README.md").read_text(encoding="utf-8")
        self.assertIn("nav-42-cbfd-2026-04/", index)
        self.assertIn("not live DA", index)
        self.assertIn("qc_coherence", index)

    def test_faces_keep_a3_off_paper2_and_ring(self) -> None:
        ns = (ROOT / "docs" / "papers" / "ns-snd" / "FACES.md").read_text(
            encoding="utf-8"
        )
        ring = (ROOT / "docs" / "papers" / "ring" / "FACES.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("nav-42-cbfd-2026-04", ns)
        self.assertIn("A_3", ns)
        collapsed_ns = " ".join(ns.lower().replace("*", " ").split())
        self.assertIn("not paper2 operator snd", collapsed_ns)
        self.assertIn("nav-42-cbfd-2026-04", ring)
        self.assertIn("Patent Pending", ring)
        self.assertIn("branding", ring.lower())
        self.assertIn(r"A_3", ring)

    def test_queued_track_c_receipts_exist_outside_live_da(self) -> None:
        archive = ARCHIVE
        self.assertTrue((archive / "Alignment_Functionals_Strong_Draft.MISSING.md").is_file())
        self.assertTrue((archive / "qc_qr_toys.py").is_file())
        self.assertTrue((archive / "Q-OS-FLUID-Q.RECEIPT.md").is_file())
        self.assertTrue((archive / "sfe_black_hole_simulator_paste.py").is_file())
        missing = (archive / "Alignment_Functionals_Strong_Draft.MISSING.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("not received", missing.lower())
        self.assertIn("NOT CLAIMED", missing)
        collapsed = " ".join(missing.lower().replace("*", " ").split())
        self.assertIn("not an attachment", collapsed)
        self.assertIn("403", missing)
        self.assertIn("Stanley", missing)
        self.assertIn("7de9444d", missing)
        toys = (archive / "qc_qr_toys.py").read_text(encoding="utf-8")
        self.assertIn("archive only", toys.lower())
        self.assertIn("qc_coherence", toys)
        self.assertIn("qr_resonance", toys)
        self.assertIn("Forbidden in live domain_architect", toys)
        self.assertIn("unused", toys.lower())
        self.assertIn("entropy", toys)
        self.assertIn("correlate", toys)
        self.assertNotIn("from scipy.stats import entropy", toys)
        self.assertIn("[0.8, 0.1, 0.05, 0.05]", toys)
        self.assertIn("L1-uniform", toys)
        self.assertFalse((DA_PY / "qc_qr_toys.py").is_file())
        self.assertFalse((DA_PY / "sfe_black_hole_simulator_paste.py").is_file())
        lookup = (ROOT / "docs" / "packets" / "OLD-PAPERS-LOOK-UP.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("nav-42-cbfd-2026-04", lookup)
        self.assertIn("Alignment Functionals", lookup)
        self.assertIn("qc_coherence", lookup)

    def test_live_domain_architect_python_has_no_nav42_toys(self) -> None:
        forbidden = (
            "qc_coherence",
            "qr_resonance",
            "Fluid-Q",
            "Fluid_Q",
            "NAV-42",
            "NAV_42",
            "Q Operating System",
        )
        hits: list[str] = []
        for path in DA_PY.glob("*.py"):
            body = path.read_text(encoding="utf-8")
            for token in forbidden:
                if token in body:
                    hits.append(f"{path.name}:{token}")
        self.assertEqual(hits, [], msg="live DA must not import Track C toys")


if __name__ == "__main__":
    unittest.main()
