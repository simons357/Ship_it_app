"""Gate 83D hinge lock. No new witness. NS not solved."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md",
    "packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md",
    "packets/DA-GATE-83-RADICAL-TRAPPING-2026-09-27.md",
    "packets/DA-GATE-83-MINOR-FACTOR-2026-09-27.md",
    "packets/DA-GATE-83B2B-CURVATURE-2026-09-28.md",
)


class TestGate83DHinge(unittest.TestCase):
    def test_pages_lock_the_hinge_and_forbid_a_new_witness(self):
        proof = (ROOT / "docs" / "ns-recovery" / "GATE-83D-HINGE.md").read_text()
        card = (ROOT / "packets" / "DA-GATE-83D-HINGE-2026-09-28.md").read_text()
        self.assertTrue(proof.startswith("# Gate 83D"))
        self.assertIn("No new witness", proof)
        self.assertIn("83.40", proof)
        self.assertIn("83.41", proof)
        self.assertIn("83.42", proof)
        self.assertIn("rank drop", proof)
        self.assertIn("every cube", proof)
        self.assertIn("NOT YET ESTABLISHED", proof)
        self.assertIn("83.34", proof)
        self.assertNotIn("NS is solved", proof)
        self.assertNotIn("NS is solved", card)
        self.assertFalse((ROOT / "scripts" / "da_gate_83d_hinge.py").exists())
        self.assertTrue(
            (ROOT / "docs" / "ns-recovery" / "GATE-83B2B-CURVATURE.md").exists()
        )
        self.assertIn("PROVED / REPORTED", proof)
        self.assertIn("R_{111}-R_{000}", proof)
        self.assertIn("sqrt113_spec", proof)

    def test_hinge_does_not_rewrite_locked_packets(self):
        for rel in LOCKED:
            text = (ROOT / rel).read_text()
            self.assertNotIn("83D", text)
            self.assertNotIn("NS is solved", text)

    def test_card_points_at_the_existing_witness_page(self):
        card = (ROOT / "packets" / "DA-GATE-83D-HINGE-2026-09-28.md").read_text()
        self.assertIn("GATE-83B2B-CURVATURE.md", card)
        self.assertIn("83.40", card)
        self.assertIn("OPEN", card)

    def test_fifth_radius_identity_and_sqrt113_spec(self):
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        import da_gate_83d_sqrt113_spec as spec  # noqa: E402

        payload = spec.run()
        self.assertTrue(payload["fifth_radius_identity"]["holds_identically"])
        self.assertEqual(payload["fifth_radius_identity"]["residual"], "0")
        cube = payload["sqrt113_cube"]
        self.assertTrue(cube["five_radii_equal"])
        self.assertTrue(cube["G_zero"])
        self.assertEqual(cube["delta"], "-6/25")
        self.assertEqual(cube["free_node_on_I_act"], "seated z4 = p100")
        self.assertFalse(payload["ns_solved"])
        self.assertEqual(payload["heavy_83D"]["status"], "PROVED_REPORTED")
        self.assertTrue(payload["all_checks_ok"])
        spec.main()
        data = json.loads(
            (ROOT / "results" / "da_gate_83d_sqrt113_spec.json").read_text()
        )
        self.assertTrue(data["all_checks_ok"])
        card = (ROOT / "packets" / "DA-GATE-83D-SQRT113-SPEC-2026-09-28.md").read_text()
        self.assertIn("113", card)
        self.assertNotIn("NS is solved", card)


if __name__ == "__main__":
    unittest.main()
