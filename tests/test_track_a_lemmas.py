"""Track A lemma catalog: this PDE only; eps->0 open; A=>B fail."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_machine import classify_claim, run_checker  # noqa: E402
from track_a_lemmas import run  # noqa: E402


class TrackALemmasTests(unittest.TestCase):
    def test_theorem_a_pass_eps_gap_open_export_fails(self):
        tmp = Path(tempfile.mkdtemp()) / "track_a_test.json"
        payload = run(out=tmp)
        by = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(by["A1_energy"]["verdict"], "pass")
        self.assertEqual(by["A2_galerkin"]["verdict"], "pass")
        self.assertEqual(by["A3_weak_limit"]["verdict"], "pass")
        self.assertEqual(by["A4_unique_H1"]["verdict"], "pass")
        self.assertEqual(by["A5_smooth"]["verdict"], "pass")
        self.assertEqual(by["A_theorem"]["verdict"], "pass")
        self.assertEqual(by["A_E1_residual"]["verdict"], "pass")
        self.assertEqual(by["A_E2_q1_positive"]["verdict"], "pass")
        self.assertEqual(by["A_E3_enstrophy_finite"]["verdict"], "pass")
        self.assertEqual(by["A_E4_eps_dependence"]["verdict"], "pass")
        self.assertEqual(by["A_E5_div"]["verdict"], "pass")
        self.assertEqual(by["A6_q1_leaves"]["verdict"], "pass")
        self.assertEqual(by["A7_box_uniform"]["verdict"], "fail")
        self.assertEqual(by["A8_box_is_nogo"]["verdict"], "fail")
        self.assertEqual(by["A9_q1_vanishes_writes_H1"]["verdict"], "fail")
        self.assertEqual(by["A_uniform_H1"]["verdict"], "open")
        self.assertEqual(by["A_implies_B"]["verdict"], "fail")
        self.assertEqual(by["A_phi_estimate"]["verdict"], "fail")
        self.assertEqual(by["A_export_olga"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["theorem_A"], "pass")
        self.assertEqual(payload["meta"]["eps_to_0"], "open")
        self.assertEqual(payload["meta"]["implies_B"], "fail")
        self.assertEqual(payload["counts"]["open"], 1)
        self.assertTrue((ROOT / "docs" / "TRACK-A-LEMMAS.md").is_file())

    def test_classify_and_check_a(self):
        r = classify_claim("Q1 augmented energy identity")
        self.assertEqual(r["domain"], "A")
        result = run_checker("A")
        self.assertEqual(result["verdict"], "pass")


if __name__ == "__main__":
    unittest.main()
