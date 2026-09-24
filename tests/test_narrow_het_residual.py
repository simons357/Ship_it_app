"""Narrow heterochiral residual. Not DA-NS-2. NS is not solved."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.narrow_het_residual import (  # noqa: E402
    A_coeff,
    H_ijo,
    L_channels,
    R_of,
    crossover_audit,
    evaluate_network,
    het_channels_from_triads,
    geometric_triads,
    lattice_modes,
    moments,
    relative_width,
    spanning_tree_channels,
    two_triad_channels,
    vandermonde,
)


class CrossoverAuditTests(unittest.TestCase):
    def test_Ds_over_Y_is_Lambda_r2(self):
        m = moments([1.0, 4.0, 9.0], [0.5, 0.3, 0.2])
        r = relative_width(m["D_s"], m["Lambda"], m["Y"])
        self.assertAlmostEqual(m["D_s"] / m["Y"], m["Lambda"] * r * r, places=12)
        self.assertAlmostEqual(m["D_s"], m["D_s_var"], places=12)

    def test_crossover_equivalence(self):
        """r ≳ κ^{-1/2}  ⇔  D_s/Y ≳ κ. Exact, torus units."""
        for r, kappa in ((0.2, 4.0), (0.5, 4.0), (0.8, 4.0), (0.05, 100.0)):
            ds_over_y = (kappa**2) * r * r
            self.assertEqual(r >= kappa ** -0.5, ds_over_y >= kappa)

    def test_two_point_family_r_is_relative_lambda_width(self):
        audit = crossover_audit()
        for row in audit["two_point_family"]:
            self.assertAlmostEqual(row["r"], row["eps"], places=12)
            self.assertAlmostEqual(row["Ds_over_Y"], row["Lambda_r2"], places=12)
            self.assertEqual(row["broad_by_r"], row["broad_by_visc"])
        self.assertFalse(audit["two_point_family"][1]["broad_by_r"])  # r=0.25, κ=4
        self.assertTrue(audit["two_point_family"][2]["broad_by_r"])  # r=0.80, κ=4

    def test_R_equals_two_kappa_cubed_on_shell(self):
        for kappa in (1.0, 2.0, 5.0, 11.0):
            self.assertAlmostEqual(
                R_of(kappa, kappa, kappa, kappa**2),
                2.0 * kappa**3,
                places=10,
            )
            self.assertAlmostEqual(A_coeff(kappa, kappa, kappa), 2.0 * kappa, places=12)
            self.assertAlmostEqual(H_ijo(kappa, kappa, kappa), 2.0 * kappa**2, places=12)

    def test_dR_dLambda_is_minus_A(self):
        i, j, o, lam = 3.0, 4.0, 2.0, 7.0
        dlam = 1e-6
        deriv = (R_of(i, j, o, lam + dlam) - R_of(i, j, o, lam - dlam)) / (2.0 * dlam)
        self.assertAlmostEqual(deriv, -A_coeff(i, j, o), places=8)

    def test_R_gap_is_linear_in_relative_width(self):
        audit = crossover_audit()
        self.assertAlmostEqual(audit["R_minus_2k3"]["R0"], 250.0, places=10)
        scales = [abs(s["dR_over_kappa3_r"]) for s in audit["R_minus_2k3"]["samples"]]
        self.assertGreater(min(scales), 1.0)
        self.assertLess(max(scales), 20.0)

    def test_vandermonde_is_cubic_in_r(self):
        audit = crossover_audit()
        ratios = [row["V_over_kappa3_r3"] for row in audit["vandermonde"]]
        self.assertAlmostEqual(ratios[0], ratios[1], places=12)
        self.assertAlmostEqual(ratios[1], ratios[2], places=12)
        x, y, z = 5.2, 4.8, 4.7
        self.assertAlmostEqual(vandermonde(x, y, z), (x - y) * (y - z) * (z - x), places=12)

    def test_convention_flags(self):
        c = crossover_audit()["conventions"]
        self.assertTrue(c["r_dimensionless"])
        self.assertTrue(c["kappa_inv_sqrt_is_torus_unit"])
        self.assertTrue(c["box_rescaling_changes_the_number"])


class PrimitiveTests(unittest.TestCase):
    def test_two_triad_tree_solves_and_does_not_share(self):
        net = evaluate_network("two_triad_tree", two_triad_channels())
        self.assertEqual(net["n_channels"], 2)
        self.assertEqual(net["n_modes"], 5)
        self.assertTrue(net["A"]["compatible"])
        self.assertTrue(net["ones"]["compatible"])
        self.assertEqual(net["A"]["n_left_null"], 0)
        self.assertLess(net["A"]["cond"], 3.0)
        self.assertFalse(net["A_is_constant"])
        self.assertFalse(net["share_same_w_for_both_targets"])
        self.assertTrue(net["both_in_range"])

    def test_L_family_trees_stay_conditioned(self):
        norms = []
        for L in (2, 7, 16, 55):
            net = evaluate_network(f"L{L}", L_channels(L))
            self.assertTrue(net["A"]["compatible"], msg=L)
            self.assertLess(net["A"]["cond"], 2.0)
            norms.append(net["A"]["min_norm_w"])
        # ||w|| stays O(1) as the L-family scales.
        self.assertGreater(min(norms), 1.0)
        self.assertLess(max(norms), 2.0)

    def test_lattice_loop_has_holonomy_obstruction(self):
        ch = het_channels_from_triads(geometric_triads(lattice_modes(10)))
        net = evaluate_network("lat10", ch)
        self.assertGreater(net["n_channels"], 1000)
        self.assertGreater(net["A"]["n_left_null"], 100)
        self.assertFalse(net["A"]["compatible"])
        self.assertFalse(net["ones"]["compatible"])
        self.assertGreater(net["A"]["worst_holonomy_rel"], 0.9)
        self.assertFalse(net["isotropic_A"]["compatible"])

    def test_lattice_tree_modal_solves_isotropic_does_not(self):
        ch = het_channels_from_triads(geometric_triads(lattice_modes(10)))
        tree = spanning_tree_channels(ch)
        net = evaluate_network("tree10", tree)
        self.assertTrue(net["A"]["compatible"])
        self.assertEqual(net["A"]["n_left_null"], 0)
        self.assertFalse(net["isotropic_A"]["compatible"])
        self.assertGreater(net["isotropic_A"]["worst_holonomy_rel"], 0.5)
        # Lattice tree is solvable but not uniformly well-conditioned.
        self.assertGreater(net["A"]["cond"], 10.0)


if __name__ == "__main__":
    unittest.main()
