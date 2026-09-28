"""Gate 83B-2b curvature. Polarization line on the 13/10 cube.

NS not solved. 71E packets and locked gates are not altered.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_83b2b_curvature as gate  # noqa: E402
import sympy as sp


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md",
    "packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md",
    "packets/DA-GATE-83-RADICAL-TRAPPING-2026-09-27.md",
    "packets/DA-GATE-83-MINOR-FACTOR-2026-09-27.md",
)


class TestGate83B2bCurvature(unittest.TestCase):
    def test_exact_lattice_is_cocircular_and_volumetric(self):
        lat = gate.exact_lattice_identities()
        self.assertTrue(lat["cocircular"])
        self.assertEqual(lat["delta"], "-6/25")
        self.assertTrue(lat["delta_nonzero"])
        self.assertEqual(lat["lam"], "-12/5")
        self.assertEqual(lat["r"], ["-1/2", "6/5", "6/5"])
        self.assertEqual(lat["b"], ["1/2", "1/10"])
        for key in ("000", "100", "010", "001", "111"):
            self.assertEqual(lat["radii_squared"][key], "169/100")

    def test_raw_F_is_affine_in_each_zi(self):
        aff = gate.affinity_in_each_zi()
        self.assertTrue(aff["D2F_e_zi_e_zi_identically_zero"])
        self.assertEqual(aff["max_degree_in_zi"], [1] * 8)

    def test_witness_line_has_rank_7_and_live_pairs(self):
        payload = gate.run()
        self.assertFalse(payload["ns_solved"])
        self.assertTrue(payload["da_ns_2_open"])
        self.assertFalse(payload["unrestricted_star_restored"])
        self.assertEqual(payload["global_rank8_trap"], "FALSIFIED")
        self.assertEqual(payload["question_83_34"], "OPEN")
        wit = payload["witness"]
        self.assertTrue(wit["activity"]["live"])
        self.assertEqual(wit["activity"]["dead_pairs"], 0)
        self.assertEqual(wit["activity"]["n_pairs"], 16)
        self.assertEqual(wit["rank_9x8"], 7)
        self.assertTrue(wit["z4_column_vanishes"])
        self.assertFalse(wit["z7_column_vanishes"])
        self.assertTrue(wit["line_is_exact_coherent"])
        self.assertLess(wit["max_abs_raw"], 1e-10)
        self.assertLess(abs(wit["ell_dot_d2"]), 1e-10)
        self.assertTrue(payload["all_checks_ok"])
        self.assertEqual(payload["boxed_obstruction"], r"\ell^T D^2F[v,v] = 0")

    def test_pages_do_not_claim_ns_or_close_83_34(self):
        proof = (ROOT / "docs" / "ns-recovery" / "GATE-83B2B-CURVATURE.md").read_text()
        card = (ROOT / "packets" / "DA-GATE-83B2B-CURVATURE-2026-09-28.md").read_text()
        self.assertTrue(proof.startswith("# Gate 83B-2b"))
        self.assertTrue(
            r"\ell^T\mathrm{D}^2F[v,v]=0" in proof or r"\ell^T D^2F[v,v]=0" in card
        )
        self.assertIn("NOT YET ESTABLISHED", proof)
        self.assertIn("83.34", proof)
        self.assertNotIn("NS is solved", proof)
        self.assertNotIn("NS is solved", card)
        for rel in LOCKED:
            text = (ROOT / rel).read_text()
            self.assertNotIn("83B-2b", text)
            self.assertNotIn("NS is solved", text)
        out = ROOT / "results" / "da_gate_83b2b_curvature.json"
        if not out.exists():
            gate.main()
        data = json.loads(out.read_text())
        self.assertFalse(data["ns_solved"])
        self.assertEqual(data["question_83_34"], "OPEN")
        self.assertEqual(data["witness"]["rank_9x8"], 7)

    def test_delta_is_exactly_minus_six_twenty_fifths(self):
        self.assertEqual(sp.simplify(gate.DELTA_EXACT), -sp.Rational(6, 25))


if __name__ == "__main__":
    unittest.main()
