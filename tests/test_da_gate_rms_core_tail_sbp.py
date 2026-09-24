"""Honesty locks and sympy identities for the 24 Sep RMS/SBP gate."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_gate_rms_sbp import (  # noqa: E402
    CONVENTION,
    measure_phi_over_y,
    phi_e,
    prove_all,
    prove_R_core,
    prove_phi_e,
    prove_sbp_coefficients,
)

PACKET = ROOT / "packets" / "DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md"
LOCK = ROOT / "data" / "da_gate_rms_core_tail_sbp_2026-09-24.json"


class TestDaGateRmsSbp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.proofs = prove_all()

    def test_sources_and_open_locks(self) -> None:
        self.assertTrue(PACKET.is_file())
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["da_ns_2"], "OPEN")
        self.assertEqual(self.lock["tail_estimate"], "OPEN")
        self.assertEqual(self.lock["convention"], CONVENTION)
        self.assertTrue(self.lock["do_not_mix_with_live_Lambda"])
        self.assertIn("NS not solved", self.page)
        self.assertIn("FORBIDDEN", self.page)
        self.assertFalse(self.lock["n64_n96_in_tree"])

    def test_do_not_mix_conventions(self) -> None:
        self.assertEqual(CONVENTION, "FROZEN_EPOCH")
        self.assertIn("frozen epoch", self.page.lower())
        self.assertIn("Do not mix", self.page)
        self.assertTrue(self.proofs["do_not_mix_with_live_Lambda"])

    def test_phi_e_identities(self) -> None:
        p = prove_phi_e()
        for key in (
            "square_prefactor",
            "quadratic_disc_negative",
            "equals_expanded",
            "vanishes_at_shell",
            "first_derivative_at_shell",
            "phi_at_zero",
            "constant_shift_is_kappa4",
        ):
            self.assertTrue(p[key], key)
        self.assertEqual(p["leading_m4_coeff"], "1/2")
        self.assertAlmostEqual(phi_e(0.0, 1.5), 1.5**4, places=12)
        self.assertAlmostEqual(phi_e(1.5, 1.5), 0.0, places=12)

    def test_sbp_coefficient_identity(self) -> None:
        s = prove_sbp_coefficients()
        self.assertTrue(s["coefficient_identity"])
        self.assertEqual(s["convention"], "FROZEN_EPOCH")

    def test_R_core_gradient(self) -> None:
        r = prove_R_core()
        self.assertTrue(r["R_at_core_is_2kappa3"])
        self.assertTrue(r["A_at_core_is_2kappa"])
        self.assertTrue(r["dR_dLambda_at_core"])
        self.assertTrue(r["grad_i"])
        self.assertTrue(r["grad_j"])
        self.assertTrue(r["grad_o"])

    def test_signed_sum_stays_forbidden(self) -> None:
        self.assertIn("replace a signed sum by a sum of absolute values", self.lock["forbidden"])
        self.assertIn("sum of absolute values", self.page)

    def test_charge_and_het_moments_recorded(self) -> None:
        self.assertIn("Q_a = (1/2) (d/dt)_NL ||u||_{Hdot^{1/2}}^2", self.lock["proved"])
        self.assertEqual(self.proofs["M_het"], "sum A H Q")
        self.assertEqual(self.proofs["N_het"], "sum A Q")
        self.assertIn("cross-radius helicity primitive", self.lock["unconfirmed"][0])

    def test_phi_over_y_split_sums(self) -> None:
        modes = {
            (1, 0, 0): 1.0,
            (2, 0, 0): 0.1,
            (0, 0, 1): 0.4,
        }
        m = measure_phi_over_y(modes, kappa_e=1.0, r_core=0.2)
        parts = m["core_over_Y"] + m["low_tail_over_Y"] + m["high_tail_over_Y"]
        self.assertAlmostEqual(parts, m["Phi_e_over_Y"], places=12)
        self.assertGreater(m["kappa4_E_over_Y"], 0.0)

    def test_n16_phi_over_y_table_is_high_tail(self) -> None:
        table = ROOT / "results" / "da_gate_rms_phi_e_over_y.json"
        self.assertTrue(table.is_file())
        payload = json.loads(table.read_text(encoding="utf-8"))
        self.assertFalse(payload["ns_solved"])
        self.assertEqual(payload["da_ns_2"], "OPEN")
        self.assertEqual(payload["tail_estimate"], "OPEN")
        first, last = payload["rows"][0], payload["rows"][-1]
        self.assertAlmostEqual(first["t"], 0.0)
        self.assertAlmostEqual(first["Phi_e_over_Y"], 0.0, places=12)
        self.assertAlmostEqual(first["D_s"], 0.0, places=12)
        self.assertAlmostEqual(last["t"], 4.5)
        self.assertGreater(last["Phi_e_over_Y"], 0.3)
        self.assertAlmostEqual(last["high_tail_over_Y"], last["Phi_e_over_Y"], places=12)
        self.assertAlmostEqual(last["core_over_Y"], 0.0, places=12)
        self.assertAlmostEqual(last["low_tail_over_Y"], 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
