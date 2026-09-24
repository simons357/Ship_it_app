"""Honesty locks for the 24 Sep static-frontier sign-realizability gate."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_gate_static_frontier import (  # noqa: E402
    L1_N,
    OUTCOMES,
    R2_N,
    SEED_REQUIRED,
    classify_outcome,
    finite_gap_remainder_check,
    lock_payload,
    seed_is_canonical,
)

PACKET = ROOT / "packets" / "DA-GATE-STATIC-FRONTIER-2026-09-24.md"
LOCK = ROOT / "data" / "da_gate_static_frontier_2026-09-24.json"


class TestDaGateStaticFrontier(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.payload = lock_payload()

    def test_sources_and_open_locks(self) -> None:
        self.assertTrue(PACKET.is_file())
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["da_ns_2"], "OPEN")
        self.assertTrue(self.lock["sbp_gate_unaltered"])
        self.assertTrue(self.lock["no_more_potentials"])
        self.assertTrue(self.lock["rho_N_pm_is_not_ledger_rho_Gamma"])
        self.assertFalse(self.lock["I_3_seated_here"])
        self.assertFalse(self.lock["predicted_R2_order_invented_here"])
        self.assertIn("NS not solved", self.page)
        self.assertIn("Do not alter", self.page)

    def test_does_not_ship_the_sbp_gate(self) -> None:
        self.assertFalse(
            (ROOT / "packets" / "DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md").exists()
        )
        self.assertFalse((ROOT / "scripts" / "da_gate_rms_sbp.py").exists())

    def test_frontiers_frozen(self) -> None:
        self.assertEqual(
            self.lock["frontiers"]["static"], "arithmetic sign realizability"
        )
        self.assertEqual(
            self.lock["frontiers"]["dynamic"], "dangerous-state persistence"
        )
        self.assertIn("STATIC FRONTIER", self.page)
        self.assertIn("DYNAMIC FRONTIER", self.page)
        self.assertIn("No more potentials", self.page)

    def test_L1_and_R2_definitions(self) -> None:
        delta = (1.0, 0.0)
        t0 = (2.0, 3.0)
        lam = 4.0
        t_c = 8.25
        self.assertAlmostEqual(L1_N(lam, delta, t0), 8.0, places=12)
        self.assertAlmostEqual(R2_N(t_c, lam, delta, t0), 0.25, places=12)
        self.assertIn("L_{1,N}", self.page)
        self.assertIn("R_{2,N}", self.page)

    def test_silent_T0_substitution_is_flagged(self) -> None:
        check = finite_gap_remainder_check(
            t_c_n=1.0,
            lambda_n=3.0,
            delta_n=(0.1, 0.2),
            t0_n=(1.0, -1.0),
            neighboring_t_m=(1.0, -1.0),
        )
        self.assertTrue(check["silent_T0_substitution"])
        self.assertTrue(check["forbidden_if_used_as_finite_gap_T"])
        distinct = finite_gap_remainder_check(
            t_c_n=1.0,
            lambda_n=3.0,
            delta_n=(0.1, 0.2),
            t0_n=(1.0, -1.0),
            neighboring_t_m=(1.1, -0.8),
        )
        self.assertFalse(distinct["silent_T0_substitution"])
        self.assertIn("FORBIDDEN", self.page)
        self.assertIn("finite-gap identity", self.lock["forbidden"][0])

    def test_four_outcomes_locked(self) -> None:
        self.assertEqual(tuple(self.lock["outcomes"].keys()), OUTCOMES)
        both = classify_outcome(
            has_neighbor=True,
            family="heterochiral",
            signs=("PLUS", "MINUS"),
            rho_abs_min=0.4,
            c=0.1,
        )
        self.assertEqual(both["outcome"], "BOTH_SIGNS")
        self.assertTrue(both["stop_static_closure"])
        self.assertTrue(both["save_adversarial_seed"])
        zero = classify_outcome(
            has_neighbor=True, family="homochiral", signs=("ZERO",)
        )
        self.assertTrue(zero["does_not_rescue_NSE"])
        one = classify_outcome(
            has_neighbor=True, family="heterochiral", signs=("PLUS",)
        )
        self.assertEqual(one["I_3_bridge"], "prospective; not seated here")
        none = classify_outcome(has_neighbor=False, family="")
        self.assertTrue(none["own_category"])
        self.assertIn("Arithmetic rigidity is not sign depletion", self.page)

    def test_adversarial_seed_schema(self) -> None:
        self.assertEqual(self.lock["adversarial_seed"]["required"], list(SEED_REQUIRED))
        thin = {"delta": [0.1], "T^{(0)}": [1.0]}
        self.assertFalse(seed_is_canonical(thin))
        full = {
            "integer_wavevectors": [(1, 0, 0), (0, 1, 1), (-1, -1, -1)],
            "helicity_labels": ["+", "-", "+"],
            "polarizations": [[1.0, 0.0, 0.0]],
            "amplitudes": [0.2, 0.2, 0.2],
        }
        self.assertTrue(seed_is_canonical(full))
        self.assertIn("not merely", self.page)

    def test_payload_matches_lock(self) -> None:
        self.assertEqual(self.payload["frontiers"], self.lock["frontiers"])
        self.assertFalse(self.payload["ns_solved"])
        self.assertEqual(self.payload["sign_realizability_search"], "OPEN")


if __name__ == "__main__":
    unittest.main()
