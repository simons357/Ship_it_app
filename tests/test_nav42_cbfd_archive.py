"""NAV-42 / CBFD April 2026 Grok dump is archive Track A/B/C, not Domain Architect."""

from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive" / "nav-42-cbfd-2026-04"
DA_PY = ROOT / "domain_architect"
BH_TOY = ARCHIVE / "sfe_black_hole_simulator_paste.py"
BH_RECEIPT = ARCHIVE / "SFE_BLACK_HOLE_SIMULATOR.RECEIPT.md"
E8_RECEIPT = ARCHIVE / "GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md"


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
        self.assertIn("chat paste arrived", text.lower())
        self.assertIn("does not depend on", text.lower())
        self.assertIn("SFE_BLACK_HOLE_SIMULATOR.RECEIPT.md", text)
        self.assertIn("GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md", text)
        self.assertIn("Chat Vault", text)
        self.assertIn("2.2 Hz", text)
        self.assertIn("Goldbach-closed", text)
        self.assertIn("REJECTED", text)

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
        self.assertIn("sfe_field", index)
        self.assertIn("SFE_BLACK_HOLE_SIMULATOR.RECEIPT.md", index)
        self.assertIn("GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md", index)
        self.assertIn("2.2 Hz paint", index)
        self.assertIn("Chat Vault", index)

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
        self.assertIn("sfe_black_hole_simulator_paste.py", ns)
        self.assertIn("sfe_black_hole_simulator_paste.py", ring)
        collapsed_ring = " ".join(ring.lower().replace("*", " ").split())
        self.assertIn("not ring snd", collapsed_ring)
        swirl = (ROOT / "docs" / "papers" / "swirl" / "FACES.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("sfe_black_hole_simulator_paste.py", swirl)
        self.assertIn(r"\Phi=u_\theta/r", swirl)
        self.assertIn("GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md", ns)
        self.assertIn("GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md", ring)
        self.assertIn("GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md", swirl)
        self.assertIn("spectral floor", ns)
        self.assertIn("spectral floor", ring)
        self.assertIn("spectral floor", swirl)

    def test_queued_track_c_receipts_exist_outside_live_da(self) -> None:
        archive = ARCHIVE
        self.assertTrue((archive / "Alignment_Functionals_Strong_Draft.MISSING.md").is_file())
        self.assertTrue((archive / "qc_qr_toys.py").is_file())
        self.assertTrue((archive / "Q-OS-FLUID-Q.RECEIPT.md").is_file())
        qos = (archive / "Q-OS-FLUID-Q.RECEIPT.md").read_text(encoding="utf-8")
        self.assertIn("not received", qos.lower())
        self.assertIn("11524", qos)
        self.assertIn("cylinder-wake", qos)
        self.assertIn("rejected", qos.lower())
        self.assertIn("NOT CLAIMED", qos)
        self.assertIn("Not Track A", qos)
        self.assertTrue((archive / "sfe_black_hole_simulator_paste.py").is_file())
        self.assertTrue((archive / "SFE_BLACK_HOLE_SIMULATOR.RECEIPT.md").is_file())
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
        self.assertIn("11524", lookup)
        self.assertIn("SFE Black Hole Simulator", lookup)
        self.assertIn("chat paste **arrived**", lookup)
        self.assertIn("SFE_BLACK_HOLE_SIMULATOR.RECEIPT.md", lookup)
        self.assertTrue((archive / "GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md").is_file())
        self.assertIn("GROK-E8-NAV42-SUPERSTRUCTURE.RECEIPT.md", lookup)
        self.assertIn("GAP1_RECONCILIATION_HANDOFF.md", lookup)
        self.assertIn("5c2f4994ea44", lookup)
        self.assertIn("Goldbach-closed **REJECTED**", lookup)
        self.assertIn("2.2 Hz paint", lookup)
        self.assertIn("Chat Vault", lookup)

    def test_live_domain_architect_python_has_no_nav42_toys(self) -> None:
        forbidden = (
            "qc_coherence",
            "qr_resonance",
            "Fluid-Q",
            "Fluid_Q",
            "NAV-42",
            "NAV_42",
            "Q Operating System",
            "sfe_field",
            "Black Hole Simulator",
            "Coherence Collapse",
            "Chat Vault",
            "2.2 Hz",
            "resonant paint",
            "Super E8",
            "Leech",
        )
        hits: list[str] = []
        for path in DA_PY.glob("*.py"):
            body = path.read_text(encoding="utf-8")
            for token in forbidden:
                if token in body:
                    hits.append(f"{path.name}:{token}")
        self.assertEqual(hits, [], msg="live DA must not import Track C toys")

    def test_sfe_black_hole_paste_arrived_as_track_c_disk_mask(self) -> None:
        receipt = BH_RECEIPT.read_text(encoding="utf-8")
        self.assertIn("chat paste", receipt.lower())
        self.assertIn("arrived", receipt.lower())
        self.assertIn("NOT CLAIMED", receipt)
        self.assertIn("Not Domain Architect", receipt)
        self.assertIn("does not depend", receipt.lower())
        self.assertIn("disk", receipt.lower())
        collapsed = " ".join(receipt.lower().replace("*", " ").split())
        self.assertIn("not gr", collapsed)
        self.assertIn("not swirl", collapsed)
        self.assertIn("not track a", collapsed)
        self.assertIn("not live da", collapsed.replace("domain architect", "da"))
        toy = BH_TOY.read_text(encoding="utf-8")
        self.assertIn("Historical toy only", toy)
        self.assertIn("does not depend on x or y", toy)
        self.assertIn("primes is None", toy)
        self.assertNotIn("primes=[2,3,5,7]", toy)
        self.assertIn(
            "Phi += A * np.sin(2 * np.pi * f_p * t / phi_mod + delta)",
            toy,
        )
        self.assertIn("Gamma = np.abs(Phi) / (r + 1e-5)", toy)
        self.assertIn("if __name__ ==", toy)
        html = (DA_PY / "static" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Black Hole Simulator", html)
        self.assertNotIn("sfe_field", html)
        self.assertNotIn("Equation Explorer", html)
        os.environ.setdefault("MPLBACKEND", "Agg")
        spec = importlib.util.spec_from_file_location("sfe_bh_archive_toy", BH_TOY)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        import numpy as np

        x = np.linspace(-10.0, 10.0, 81)
        y = np.linspace(-10.0, 10.0, 81)
        X, Y = np.meshgrid(x, y)
        flat = np.zeros_like(X)
        for p in (2, 3, 5, 7):
            flat = flat + np.sin(2 * np.pi * p * 0.1)
        field = mod.sfe_field(X, Y, 0.1, epsilon=0.5)
        r = np.sqrt(X**2 + Y**2)
        expected = np.where(np.abs(flat) / (r + 1e-5) >= 0.5, 0.0, flat)
        np.testing.assert_allclose(field, expected, rtol=0, atol=1e-12)
        self.assertTrue(np.allclose(field[r > 8], flat[r > 8]))
        self.assertTrue(np.allclose(field[r < 0.2], 0.0))
        zero = mod.sfe_field(X, Y, 0.0)
        np.testing.assert_allclose(zero, 0.0, atol=1e-12)

    def test_e8_nav42_superstructure_is_track_c_rejected(self) -> None:
        self.assertTrue(E8_RECEIPT.is_file(), E8_RECEIPT)
        receipt = E8_RECEIPT.read_text(encoding="utf-8")
        self.assertIn("Track C", receipt)
        self.assertIn("NOT CLAIMED", receipt)
        self.assertIn("**Not** Domain Architect", receipt)
        collapsed = " ".join(receipt.lower().replace("*", " ").split())
        self.assertIn("rejected as product strategy", collapsed)
        self.assertIn("chat vault", collapsed)
        self.assertIn("2.2 hz", collapsed)
        self.assertIn("not a lab formula", collapsed)
        self.assertIn("goldbach", collapsed)
        self.assertIn("rejected", collapsed)
        self.assertIn("not measured", collapsed)
        self.assertIn("15–25%", receipt)
        self.assertIn("personal overlay was withdrawn from public stacking", collapsed)
        self.assertIn("not filed", collapsed)
        self.assertIn("5c2f4994ea44", receipt)
        self.assertIn("NOT identical", receipt)
        self.assertIn("NOT a theorem", receipt)
        self.assertIn("OPEN", receipt)
        self.assertIn("0.04706", receipt)
        self.assertIn(r"\Phi=u_\theta/r", receipt)
        self.assertIn("HN = D^((-1)/2)*Qtilde*D^((-1)/2)", receipt)
        self.assertIn("inf J/X", receipt)
        self.assertIn("do not dump the sixteen", collapsed)
        self.assertIn("do not add chat vault", collapsed)
        self.assertFalse((DA_PY / "chat_vault.py").is_file())
        self.assertFalse((DA_PY / "resonant_paint.py").is_file())
        self.assertFalse((DA_PY / "e8_visualizer.py").is_file())
        self.assertFalse((DA_PY / "nav42.py").is_file())
        html = (DA_PY / "static" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Chat Vault", html)
        self.assertNotIn("2.2 Hz", html)
        self.assertNotIn("resonant paint", html)
        self.assertNotIn("E8 visualizer", html)
        self.assertNotIn("Equation Explorer", html)
        self.assertNotIn("Goldbach closed", receipt)
        self.assertNotIn("DA-VC-01 PASS", receipt)


if __name__ == "__main__":
    unittest.main()
