"""Centered master-ledger identities. Not DA-NS-2. NS is not solved."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.centered_ledger import (  # noqa: E402
    W_K,
    W_K_modal,
    circle_tangent,
    f_weight,
    kperp2,
    moments,
    moving_center,
    report,
    reset_dW,
    two_shell_gap,
    two_shell_zeros,
)


class CenteredLedgerTests(unittest.TestCase):
    def test_two_shell_factorization(self):
        alpha, beta, lam = 5.0, 2.0, 3.0
        left = f_weight(beta, lam) - f_weight(alpha, lam)
        right = two_shell_gap(alpha, beta, lam)
        self.assertAlmostEqual(left, right, places=12)
        self.assertAlmostEqual(left, (beta - alpha) * (alpha + beta - lam), places=12)

    def test_two_shell_structural_zeros(self):
        z = two_shell_zeros(5.0, 3.0)
        self.assertAlmostEqual(z["gap"], 0.0, places=12)
        self.assertAlmostEqual(z["flat_kperp2"], 0.0, places=12)
        self.assertAlmostEqual(z["centered"], 0.0, places=12)

    def test_kperp_and_flat(self):
        self.assertAlmostEqual(kperp2(6.0, 4.0), 4.0 * (1.0 - 4.0 / 24.0), places=12)
        self.assertAlmostEqual(kperp2(1.0, 4.0), 0.0, places=12)
        self.assertGreater(kperp2(5.0, 2.0), 0.0)

    def test_unequal_length_defect(self):
        a, b, c, lam = 5.0, 3.0, 2.0, 3.0
        left = (
            f_weight(a, lam) - f_weight(c, lam),
            f_weight(b, lam) - f_weight(c, lam),
        )
        right = (
            (a - c) * (a + c - lam),
            (b - c) * (b + c - lam),
        )
        self.assertAlmostEqual(left[0], right[0], places=12)
        self.assertAlmostEqual(left[1], right[1], places=12)
        self.assertNotAlmostEqual(left[0], left[1], places=12)

    def test_Ds_is_exact_variance(self):
        eigs = [1.0, 2.0, 5.0]
        mass = [0.4, 0.3, 0.2]
        m = moments(eigs, mass)
        self.assertAlmostEqual(m["D_s"], m["D_s_var"], places=12)
        self.assertGreater(m["D_s"], 0.0)
        self.assertAlmostEqual(m["Lambda"], m["Y"] / m["X"], places=12)

    def test_WK_identity_and_reset_jump(self):
        eigs = [1.0, 2.0, 5.0]
        mass = [0.4, 0.3, 0.2]
        m = moments(eigs, mass)
        self.assertAlmostEqual(
            W_K(m["D_s"], m["X"], m["Lambda"], m["Lambda"]),
            m["D_s"],
            places=12,
        )
        k_old, k_new = 1.0, 4.0
        jump = reset_dW(m["X"], m["Lambda"], k_old, k_new)
        expanded = m["X"] * (k_old - k_new) * (2.0 * m["Lambda"] - k_old - k_new)
        self.assertAlmostEqual(jump, expanded, places=12)
        from_modal = W_K_modal(eigs, mass, k_new) - W_K_modal(eigs, mass, k_old)
        self.assertAlmostEqual(jump, from_modal, places=12)
        self.assertAlmostEqual(
            W_K_modal(eigs, mass, k_old),
            W_K(m["D_s"], m["X"], m["Lambda"], k_old),
            places=12,
        )

    def test_circle_tangent_identity(self):
        khat = (0.0, 0.0, 1.0)
        rho = (1.0, 0.0, 0.0)
        x = (0.2, 0.3, 0.0)
        y = (-0.1, 0.4, 0.0)
        out = circle_tangent(rho, khat, x, y)
        for i in range(3):
            self.assertAlmostEqual(out["w"][i], out["w_from_sigma"][i], places=12)
        # tangent to the equal-input circle: w · k̂ = 0 and w · ρ = 0
        self.assertAlmostEqual(
            out["w"][0] * khat[0] + out["w"][1] * khat[1] + out["w"][2] * khat[2],
            0.0,
            places=12,
        )
        self.assertAlmostEqual(
            out["w"][0] * rho[0] + out["w"][1] * rho[1] + out["w"][2] * rho[2],
            0.0,
            places=12,
        )

    def test_moving_center_compression(self):
        # Two-channel toy: Q cancels, A differs, residual is −(Λ−λ_e)S
        Rdev = [1.0, -0.5]
        A = [2.0, 3.0]
        Q = [1.0, -1.0]
        Lambda, lam_e = 4.0, 2.0
        out = moving_center(Rdev, A, Q, Lambda, lam_e)
        self.assertAlmostEqual(out["Q_Gamma"], 0.0, places=12)
        self.assertAlmostEqual(out["S_Gamma"], 2.0 * 1.0 + 3.0 * (-1.0), places=12)
        self.assertAlmostEqual(out["rho_mov"], -(Lambda - lam_e) * out["S_Gamma"], places=12)
        self.assertNotAlmostEqual(out["rho_rad"], 0.0, places=12)
        self.assertNotAlmostEqual(out["rho_mov"], 0.0, places=12)

    def test_report_locks(self):
        r = report()
        self.assertTrue(r["locks"]["not_a_close"])
        self.assertTrue(r["locks"]["not_DA_NS_2"])
        self.assertAlmostEqual(r["two_shell"]["f_diff"], r["two_shell"]["factored"], places=12)
        self.assertAlmostEqual(r["W_K"]["from_def"], r["W_K"]["D_s"], places=12)
        self.assertAlmostEqual(r["W_K"]["reset"], r["W_K"]["reset_expand"], places=12)


if __name__ == "__main__":
    unittest.main()
