"""Honesty locks for the three unfinished measurements."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from three_unfinished_measurements import (  # noqa: E402
    loop_certified_upper,
    t0_odd_check,
)

PACKET = ROOT / "packets" / "THREE-UNFINISHED-MEASUREMENTS-2026-09-25.md"
LOCK = ROOT / "data" / "three_unfinished_measurements_2026-09-25.json"
RESULT = ROOT / "results" / "three_unfinished_measurements.json"


class TestThreeUnfinished(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.result = json.loads(RESULT.read_text(encoding="utf-8"))

    def test_open_locks(self) -> None:
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["da_ns_2"], "OPEN")
        self.assertEqual(self.lock["missing_17"], "OPEN")
        self.assertEqual(self.lock["sept20_IC"], "MISSING")
        self.assertFalse(self.lock["sept20_S1_reproduced"])
        self.assertEqual(self.lock["eta_DA"], "NOT_EVALUATED")
        self.assertEqual(self.lock["alpha_c_chi"], "UNSTAMPED")
        self.assertIn("MISSING", self.page)
        self.assertIn("NS not solved", self.page)
        self.assertIn("NOT EVALUATED", self.page)

    def test_does_not_claim_sept20_match(self) -> None:
        self.assertFalse(self.result["sixteen_positive_part"]["evolved_odd_A9_N2_20"]["is_sept20_datum"])
        reported = self.result["sept20_S1_reported_not_reproduced"]
        measured = self.result["sixteen_positive_part"]["evolved_odd_A9_N2_20"]["S"]
        self.assertTrue(all(abs(measured - x) > 1e-4 for x in reported))

    def test_positive_part_is_live(self) -> None:
        t0 = t0_odd_check()
        self.assertTrue(t0["locks"]["T_match"])
        self.assertTrue(t0["locks"]["X_match"])
        self.assertTrue(t0["locks"]["Y_match"])
        self.assertTrue(t0["locks"]["positive_part_live"])
        self.assertTrue(self.result["sixteen_positive_part"]["evolved_odd_A9_N2_20"]["ever_positive_part"])
        self.assertGreater(self.result["sixteen_positive_part"]["evolved_odd_A9_N2_20"]["S"], 0.0)

    def test_loop_certificate(self) -> None:
        loop = loop_certified_upper()
        self.assertAlmostEqual(loop["Gamma_cyc"], 0.8717, places=3)
        self.assertFalse(loop["is_general_L_N_M_N_U_N"])
        self.assertEqual(loop["scale_decay_prize"], "OPEN")
        self.assertFalse(loop["is_ns_defect"])
        self.assertFalse(self.lock["loop"]["is_ns_defect"])

    def test_skeleton_stays_large_Q_collapses(self) -> None:
        q0 = self.lock["Q_actual_t0"]
        q1 = self.lock["Q_actual_t1"]
        s1 = self.lock["skeleton_t1"]
        self.assertGreater(q0, 1.0)
        self.assertLess(q1, 0.01)
        self.assertGreater(s1, 10.0)
        self.assertGreater(s1 / q1, 100.0)

    def test_does_not_ship_other_gates(self) -> None:
        self.assertFalse((ROOT / "packets" / "DA-GATE-NARROW-DANGER-2026-09-24.md").exists())
        self.assertFalse((ROOT / "packets" / "FOURIER-TRIANGLES-AUDIT-2026-09-20.md").exists())


if __name__ == "__main__":
    unittest.main()
