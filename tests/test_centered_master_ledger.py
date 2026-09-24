"""Honesty locks and boxed identities for the 24 Sep 2026 centered ledger."""

from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "CENTERED-MASTER-LEDGER.md"
LOCK = ROOT / "data" / "centered_master_ledger_2026-09-24.json"


class TestCenteredMasterLedger(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = LEDGER.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))

    def test_sources_present(self) -> None:
        self.assertTrue(LEDGER.is_file())
        self.assertTrue(LOCK.is_file())

    def test_ns_not_solved(self) -> None:
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["clay_statement_b"], "OPEN")
        self.assertEqual(self.lock["da_ns_2"], "OPEN")
        self.assertIn("NS not solved", self.page)
        self.assertIn("DA-NS-2 stays **OPEN**", self.page)
        self.assertNotIn("Clay Millennium solved", self.page)

    def test_buckets(self) -> None:
        self.assertEqual(self.lock["buckets"]["OPEN"], [2, 8, 16])
        self.assertEqual(self.lock["items"]["2"]["bucket"], "OPEN")
        self.assertTrue(self.lock["items"]["2"]["is_the_actual_close"])
        self.assertEqual(self.lock["items"]["7"]["bucket"], "KILLED")
        self.assertEqual(self.lock["items"]["12"]["bucket"], "KILLED")
        self.assertEqual(self.lock["items"]["10"]["orientation_only_payment"], "KILLED")

    def test_static_sag_and_loops(self) -> None:
        self.assertEqual(self.lock["items"]["7"]["Gamma_star"], 1)
        self.assertFalse(self.lock["items"]["7"]["mode_reuse_creates_depletion"])
        self.assertFalse(self.lock["items"]["8"]["loops_automatically_force_phase_frustration"])
        self.assertFalse(self.lock["items"]["8"]["certified_upper_bound"])
        self.assertFalse(self.lock["items"]["8"]["Gamma_cyc_le_0.7_is_enough"])
        self.assertIn("lower bounds only", self.lock["items"]["8"]["heavy_loop_trend"])
        self.assertIn("loops do not automatically force phase frustration", self.page)

    def test_section_17_stays_truncated(self) -> None:
        self.assertEqual(self.lock["section_17"], "TRUNCATED")
        self.assertTrue(self.lock["do_not_complete_truncated_formulas"])
        self.assertFalse(self.lock["items"]["17"]["increment_completed"])
        self.assertIn("TRUNCATED", self.page)
        self.assertIn("completed here", self.page.lower())
        self.assertIn("cut mid-formula", self.page.lower())

    def test_two_shell_identity(self) -> None:
        """T_{c,△} = [f(β)-f(α)] τ_k = (β-α)(α+β-Λ) τ_k when τ_p+τ_q+τ_k=0."""

        def f(x: float, lam: float) -> float:
            return x * (x - lam)

        samples = (
            (4.0, 8.0, 5.0, 1.0, -0.4, -0.6),
            (1.0, 3.0, 2.0, 0.5, 0.25, -0.75),
            (9.0, 4.0, 6.5, -2.0, 0.5, 1.5),
        )
        for alpha, beta, lam, tau_p, tau_q, tau_k in samples:
            self.assertAlmostEqual(tau_p + tau_q + tau_k, 0.0, places=12)
            left = f(alpha, lam) * tau_p + f(alpha, lam) * tau_q + f(beta, lam) * tau_k
            mid = (f(beta, lam) - f(alpha, lam)) * tau_k
            right = (beta - alpha) * (alpha + beta - lam) * tau_k
            self.assertAlmostEqual(left, mid, places=12)
            self.assertAlmostEqual(mid, right, places=12)

    def test_flat_and_centered_zeros(self) -> None:
        def pref(alpha: float, beta: float, lam: float, tau_k: float) -> float:
            return (beta - alpha) * (alpha + beta - lam) * tau_k

        def struct(alpha: float, beta: float, lam: float, s: float) -> float:
            return pref(alpha, beta, lam, 1.0) * (beta * (1.0 - beta / (4.0 * alpha))) ** 0.5 * s

        self.assertEqual(pref(3.0, 3.0, 5.0, 2.0), 0.0)
        self.assertEqual(pref(2.0, 5.0, 7.0, 2.0), 0.0)
        self.assertAlmostEqual(struct(2.0, 8.0, 1.0, 2.0), 0.0, places=12)

    def test_k_perp_geometry(self) -> None:
        def k_perp_sq(alpha: float, beta: float) -> float:
            return beta * (1.0 - beta / (4.0 * alpha))

        self.assertAlmostEqual(k_perp_sq(4.0, 8.0), 4.0, places=12)
        self.assertAlmostEqual(k_perp_sq(1.0, 4.0), 0.0, places=12)

    def test_frozen_variance_identity_sits(self) -> None:
        """W_K = D_s + X(Λ-K)^2 is boxed and complete. ΔW is not filled."""
        x, y, z = 4.0, 10.0, 30.0
        lam = y / x
        d_s = z - lam * y
        for k in (0.0, lam, 4.0, -1.0):
            w_k = d_s + x * (lam - k) ** 2
            self.assertGreaterEqual(w_k, 0.0)
            self.assertAlmostEqual(w_k, z - lam * y + x * (lam - k) ** 2, places=12)
        self.assertIn("W_K=\\mathcal D_s+X(\\Lambda-K)^2", self.page)

    def test_phase_twin_magnitudes(self) -> None:
        u = self.lock["items"]["10"]["T_c_u"]
        twin = self.lock["items"]["10"]["T_c_twin"]
        self.assertAlmostEqual(twin, -u, places=11)
        self.assertAlmostEqual(abs(u), 0.79707557316, places=11)


if __name__ == "__main__":
    unittest.main()
