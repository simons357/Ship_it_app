"""v1.2 freeze table: attached, new preregistration, feasible under 2 GiB."""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "docs" / "GATE-D" / "GATE-D-V1.2-FREEZE.json"
TEXT = ROOT / "docs" / "GATE-D" / "GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md"
COPIES = (
    ROOT / "packets" / "GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md",
    ROOT / "packets" / "gate_d" / "GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md",
)
GIB = 2 * 1024**3


class GateDV12PreregistrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.freeze = json.loads(FREEZE.read_text())
        self.text = TEXT.read_text()

    def test_file_is_attached_in_gate_d_and_packets(self) -> None:
        self.assertTrue(TEXT.is_file())
        self.assertTrue(FREEZE.is_file())
        for path in COPIES:
            self.assertTrue(path.is_file(), path)
            self.assertEqual(path.read_text(), self.text)

    def test_new_preregistration_not_an_amendment(self) -> None:
        self.assertEqual(self.freeze["id"], "GATE-D-V1.2")
        self.assertFalse(self.freeze["amends_v1_1"])
        self.assertFalse(self.freeze["reuses_v1_1_runs"])
        self.assertFalse(self.freeze["approved"])
        self.assertFalse(self.freeze["ns_solved"])
        self.assertFalse(self.freeze["cutoff_independent_budget"])

    def test_physical_cutoff_fixed_independent_of_n(self) -> None:
        cut = self.freeze["physical_cutoff"]
        self.assertEqual(cut["kappa_star"], 8)
        self.assertTrue(cut["independent_of_n"])
        self.assertFalse(cut["chosen_from_v1_1_tail_gate_s_0_75"])
        self.assertTrue(cut["relative_high_fraction_forbidden"])
        boxes = {(b["N"], b["K"], b["L_exact"]) for b in cut["boxes"]}
        self.assertEqual(boxes, {(8, 4, "2*pi"), (16, 8, "4*pi")})
        for box in cut["boxes"]:
            L = box["L"]
            self.assertAlmostEqual(box["N"], cut["kappa_star"] * L / (2 * math.pi), places=12)
            self.assertAlmostEqual(box["K"], box["N"] / 2, places=12)

    def test_cutoff_fits_both_proposed_grids(self) -> None:
        for n in self.freeze["memory"]["grids_allowed_pending_rss"]:
            for box in self.freeze["physical_cutoff"]["boxes"]:
                self.assertLess(box["N"], n / 3)

    def test_two_gib_ceiling_and_excluded_grids(self) -> None:
        mem = self.freeze["memory"]
        self.assertEqual(mem["ceiling_bytes"], GIB)
        self.assertEqual(mem["grids_allowed_pending_rss"], [64, 96])
        self.assertEqual(mem["grids_excluded"], [128, 160, 192])
        self.assertFalse(mem["preflight_is_peak_rss_certificate"])
        for n in mem["grids_allowed_pending_rss"]:
            self.assertLessEqual(576 * n**3, GIB)
        for n in mem["grids_excluded"]:
            # Historical Heavy scale: n=128 is already over 2 GiB once overhead is counted.
            self.assertGreaterEqual(mem["scaled_estimate_GB"][str(n)], 2.0)

    def test_text_states_the_live_v1_1_conflicts(self) -> None:
        for phrase in (
            "new preregistration, not an amendment",
            "2 GiB",
            r"s\approx 0.75",
            "does **not** re-score",
            "n=128,160,192",
            "standard base at 128",
            "escalated set at 160 and 192",
        ):
            self.assertIn(phrase, self.text)


if __name__ == "__main__":
    unittest.main()
