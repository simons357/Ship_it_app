"""Smith form, torus reachability, TREE/LOOP cycle rank."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.integer_snf import (  # noqa: E402
    integer_rank,
    matmul,
    smith_invariants,
    smith_normal_form,
    transpose,
)
from ns_attacks.min_cycle import PARALLELOGRAM_M, PARALLELOGRAM_TREE  # noqa: E402
from ns_attacks.torus_p2 import (  # noqa: E402
    apply_MT,
    assemble_from_phases,
    cycle_rank,
    is_tree,
    left_kernel_primitive,
    snf_certificate,
    torus_reachability,
    tree_to_loop_control,
)


class SmithFormTests(unittest.TestCase):
    def test_identity(self):
        I = [[1, 0], [0, 1]]
        U, S, V = smith_normal_form(I)
        self.assertEqual(S, I)
        self.assertEqual(matmul(matmul(U, I), V), S)

    def test_diagonal_invariants(self):
        A = [[2, 0], [0, 4]]
        inv = smith_invariants(A)
        self.assertEqual(inv, [2, 4])

    def test_rank_deficient(self):
        A = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
        self.assertEqual(integer_rank(A), 2)

    def test_reconstructs_nonsquare(self):
        A = [[1, 2, 3], [4, 5, 6]]
        cert = snf_certificate(A)
        self.assertTrue(cert["reconstructs"])
        self.assertFalse(cert["novelty"])


class TorusReachabilityTests(unittest.TestCase):
    def test_tree_every_target_is_reachable(self):
        M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertTrue(is_tree(M))
        self.assertEqual(cycle_rank(M), 0)
        cert = torus_reachability(M, [0.4, -1.2, 2.0])
        self.assertTrue(cert["reachable"])
        self.assertEqual(cert["ker_Z_MT"], [])

    def test_image_point_is_reachable(self):
        M = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]]
        theta = [0.3, -0.2, 1.1]
        b = assemble_from_phases(M, theta)
        cert = torus_reachability(M, b)
        self.assertTrue(cert["reachable"])
        self.assertEqual(cert["r_cyc"], 1)

    def test_kernel_obstruction(self):
        M = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]]
        ker = left_kernel_primitive(M)
        self.assertEqual(len(ker), 1)
        c = ker[0]
        self.assertEqual(apply_MT(M, c), [0, 0, 0])
        # Pairing  π  is not 0 mod 2π.
        b = [math.pi * float(v) for v in c]
        cert = torus_reachability(M, b)
        self.assertFalse(cert["reachable"])
        self.assertAlmostEqual(abs(cert["conditions"][0]["cTb_mod_2pi"]), math.pi, places=10)

    def test_statement_is_standard_not_gate_c(self):
        M = [[1, 0], [0, 1]]
        cert = torus_reachability(M, [0.0, 0.0])
        self.assertIn("Not a Gate-C theorem", cert["statement"])
        self.assertIn("Pontryagin", cert["statement"])


class TreeToLoopTests(unittest.TestCase):
    def test_algebraic_control(self):
        M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        ctrl = tree_to_loop_control(M, [1, 1, 0])
        self.assertEqual(ctrl["r_cyc_before"], 0)
        self.assertEqual(ctrl["r_cyc_after"], 1)
        self.assertEqual(ctrl["transition"], "0 → 1")
        self.assertEqual(len(ctrl["primitive_c"]), 4)
        self.assertTrue(ctrl["not_a_picture"])
        self.assertEqual(apply_MT(ctrl["M_loop"], ctrl["primitive_c"]), [0, 0, 0])

    def test_rejects_existing_loop(self):
        M = [[1, 0], [1, 0]]
        with self.assertRaises(ValueError):
            tree_to_loop_control(M, [1, 0])

    def test_parallelogram_rows_are_a_tree_then_a_loop(self):
        self.assertTrue(is_tree(PARALLELOGRAM_TREE))
        self.assertEqual(cycle_rank(PARALLELOGRAM_M), 1)
        ctrl = tree_to_loop_control(PARALLELOGRAM_TREE, [1, -1, 1])
        self.assertEqual(ctrl["primitive_c"] in ([1, -1, 1, -1], [-1, 1, -1, 1]), True)


class KernelExactnessTests(unittest.TestCase):
    def test_left_kernel_annihilates(self):
        M = [[2, 4, 6], [3, 9, 6], [5, 13, 12]]
        for c in left_kernel_primitive(M):
            self.assertEqual(apply_MT(M, c), [0, 0, 0])


if __name__ == "__main__":
    unittest.main()
