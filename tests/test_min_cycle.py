"""MIN-CYCLE gate and NA-2B relabel."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.min_cycle import (  # noqa: E402
    CANONICAL_TREE,
    PARALLELOGRAM_M,
    algebraic_tree_to_loop,
    min_cycle_acceptance,
    parallelogram_tree_to_loop,
)
from ns_attacks.na2b_assembly import exact_assembly, na2b_unit_report  # noqa: E402
from ns_attacks.torus_p2 import cycle_rank, is_tree  # noqa: E402


class MinCycleGateTests(unittest.TestCase):
    def test_acceptance_record(self):
        acc = min_cycle_acceptance()
        self.assertEqual(acc["gate"], "MIN-CYCLE")
        self.assertTrue(acc["accepted_on_this_gate"])
        self.assertEqual(acc["scale_rate_defect"], "OPEN")
        self.assertFalse(acc["ns_solved"])
        self.assertTrue(acc["finite_size_does_not_imply_scale_decay"])
        self.assertTrue(acc["rho_less_than_one_is_not_a_rate"])
        self.assertIn("0.15 is a threshold/convention", acc["threshold_015"])
        self.assertIn("Gate-C novelty", acc["not_accepted"][3])
        self.assertTrue(acc["algebraic_control_accepted"])
        self.assertTrue(acc["prediction_measurement_pass"])
        self.assertTrue(acc["na2b_pass"])

    def test_tree_shorthand_is_cycle_rank(self):
        self.assertTrue(is_tree(CANONICAL_TREE))
        self.assertEqual(cycle_rank(CANONICAL_TREE), 0)
        self.assertEqual(cycle_rank(PARALLELOGRAM_M), 1)

    def test_parallelogram_control_is_algebraic(self):
        ctrl = parallelogram_tree_to_loop()
        self.assertEqual(ctrl["transition"], "0 → 1")
        self.assertIn(ctrl["primitive_c"], ([1, -1, 1, -1], [-1, 1, -1, 1]))
        self.assertTrue(ctrl["not_a_picture"])

    def test_algebraic_control_not_a_drawing(self):
        alg = algebraic_tree_to_loop()
        self.assertTrue(alg["accepted"])
        self.assertTrue(alg["control"]["not_a_picture"])


class NA2BTests(unittest.TestCase):
    def test_relabel_is_unit_test_not_optimizer(self):
        M = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]]
        rep = na2b_unit_report(M, [0.1, 0.2, -0.3])
        self.assertEqual(rep["label"], "NA-2B")
        self.assertEqual(rep["role"], "exact cancellation/assembly unit test")
        self.assertTrue(rep["not_optimizer_evidence"])
        self.assertTrue(rep["not_scale_rate"])
        self.assertTrue(rep["pass"])

    def test_assembly_of_image_point(self):
        M = [[1, 0], [0, 1], [1, 1]]
        out = exact_assembly(M, [0.4, -0.5])
        self.assertTrue(out["pass"])
        self.assertTrue(out["not_optimizer_evidence"])


if __name__ == "__main__":
    unittest.main()
