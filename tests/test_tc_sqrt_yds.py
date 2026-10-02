"""Attack |T_c| ≤ C ||∇u||_3 √(Y D_s). ★ NOT proved. NS NOT solved."""

from __future__ import annotations

import math
import pathlib
import unittest
from fractions import Fraction

from scripts.ns_attacks.tc_sqrt_yds import (
    ahalf_B_sq,
    closed_Ds_near_shell,
    closed_Tc_growing_layer,
    closed_Tc_near_shell,
    field_to_uhat,
    flux_moments,
    growing_layer,
    localized_curl_bump,
    near_shell_triad,
    ratios_from_exact,
    ratios_from_uhat,
    run_attack,
    scale_field,
    spectral_flux,
)


ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "ns-review" / "TC-SQRT-YDS-2026-10-01.md"


class TestNearShellLocks(unittest.TestCase):
    def test_closed_forms(self) -> None:
        for eps in (Fraction(1, 2), Fraction(1, 8), Fraction(1, 32)):
            flux = flux_moments(near_shell_triad(eps))
            self.assertEqual(flux["Tc"], closed_Tc_near_shell(eps))
            self.assertEqual(flux["Ds"], closed_Ds_near_shell(eps))

    def test_linear_absorption_blows(self) -> None:
        ratios = []
        for eps in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)):
            flux = flux_moments(near_shell_triad(eps))
            ratio = abs(flux["Tc"]) / flux["Ds"]
            self.assertEqual(ratio, (2 + eps * eps) / (4 * eps))
            ratios.append(ratio)
        self.assertTrue(all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1)))

    def test_sqrt_Ds_order_tends_to_eight(self) -> None:
        eps = Fraction(1, 32)
        flux = flux_moments(near_shell_triad(eps))
        val = abs(float(flux["Tc"])) / math.sqrt(float(flux["Ds"]))
        self.assertAlmostEqual(val, 8.0, places=2)

    def test_pairing_cs(self) -> None:
        field = near_shell_triad(Fraction(1, 8))
        flux = flux_moments(field)
        rhs = math.sqrt(float(ahalf_B_sq(field)) * float(flux["Ds"]))
        self.assertGreaterEqual(rhs + 1e-12, abs(float(flux["Tc"])))


class TestAmplitudeHomogeneity(unittest.TestCase):
    def test_q3_without_Y_grows_like_amp(self) -> None:
        base = near_shell_triad(Fraction(1, 8))
        rhos = []
        rhoY = []
        for a in (1, 2, 4):
            row = ratios_from_exact(scale_field(base, a), n_grid=16)
            q3 = abs(float(Fraction(row["Tc"]))) / (
                row["grad_L3"] * math.sqrt(float(Fraction(row["Ds"])))
            )
            rhos.append(q3)
            rhoY.append(row["rho_Y"])
        self.assertAlmostEqual(rhos[1] / rhos[0], 2.0, places=6)
        self.assertAlmostEqual(rhos[2] / rhos[0], 4.0, places=6)
        self.assertAlmostEqual(rhoY[0], rhoY[1], places=8)
        self.assertAlmostEqual(rhoY[1], rhoY[2], places=8)


class TestGrowingLayer(unittest.TestCase):
    def test_energy_and_tc_lock(self) -> None:
        for n in (1, 2, 3):
            field = growing_layer(n)
            flux = flux_moments(field)
            self.assertEqual(flux["E"], Fraction(4 * (2 * n + 1)))
            self.assertEqual(flux["Tc"], closed_Tc_growing_layer(n))
            self.assertGreater(flux["Ds"], 0)

    def test_rho_Y_does_not_grow(self) -> None:
        rows = [ratios_from_exact(growing_layer(n), n_grid=8 * n) for n in (1, 2, 3)]
        rhos = [r["rho_Y"] for r in rows]
        self.assertLess(rhos[-1], rhos[0])
        # Unrestricted ★ still grows on this family.
        self.assertGreater(rows[-1]["rho_star"], rows[0]["rho_star"])


class TestLocalizedBump(unittest.TestCase):
    def test_rho_Y_plateau_and_g32_ell_half(self) -> None:
        ells = (0.65, 0.48, 0.36)
        rows = []
        for ell in ells:
            rows.append((ell, ratios_from_uhat(localized_curl_bump(ell, n_grid=32))))
        rhoY = [r["rho_Y"] for _, r in rows]
        collapse = [r["rho_g32"] * math.sqrt(ell) for ell, r in rows]
        g32 = [r["rho_g32"] for _, r in rows]
        self.assertLess(max(rhoY) / min(rhoY), 1.15)
        self.assertTrue(all(g32[i] < g32[i + 1] for i in range(len(g32) - 1)))
        self.assertLess(max(collapse) / min(collapse), 1.15)
        self.assertLess(max(rhoY), 0.25)


class TestSpectralConsistency(unittest.TestCase):
    def test_spectral_matches_exact_triad(self) -> None:
        field = near_shell_triad(Fraction(1, 8))
        exact = flux_moments(field)
        spec = spectral_flux(field_to_uhat(field, 24))
        self.assertAlmostEqual(spec["Tc"], float(exact["Tc"]), places=8)
        self.assertAlmostEqual(spec["Ds"], float(exact["Ds"]), places=8)


class TestAttackReport(unittest.TestCase):
    def test_note_exists(self) -> None:
        self.assertTrue(NOTE.is_file())
        text = NOTE.read_text(encoding="utf-8")
        self.assertIn("NOT proved", text)
        self.assertIn("NOT solved", text)
        self.assertIn(r"\sqrt{YD_s}", text)

    def test_run_attack_honesty(self) -> None:
        summary = run_attack(n_grid_sparse=16, n_grid_bump=32)
        self.assertFalse(summary["ns_solved"])
        self.assertFalse(summary["lemma_star_proved"])
        self.assertEqual(summary["kill_lane"], "LIVE")
        self.assertTrue(summary["pairing_identity_holds"])
        self.assertTrue(summary["spectral_matches_exact_on_triad"])
        self.assertEqual(summary["inherited_kills"]["T_c_le_C_nu_Ds"], "KILLED_by_near_shell")
        self.assertEqual(
            summary["inherited_kills"]["T_c_le_C_gradL3_sqrt_Ds"],
            "KILLED_by_amplitude",
        )
        self.assertEqual(summary["candidate_status"], "OPEN")
        self.assertIn("localized_bump", summary["alternate_status"])
        self.assertLess(summary["max_rho_Y"]["near_shell"], 0.3)
        self.assertGreater(summary["max_rho_Y"]["near_shell"], 0.15)


if __name__ == "__main__":
    unittest.main()
