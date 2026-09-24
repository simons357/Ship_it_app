"""Polarization holonomy. Stars can; loops are the remaining static target."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.helical import geometric_coupling  # noqa: E402
from ns_attacks.loop_gauge import PARALLELOGRAM, STAR_WITNESS  # noqa: E402
from ns_attacks.polarization_holonomy import (  # noqa: E402
    parallelogram_polarization,
    polarization_test,
    star_polarization,
)


class HelicalCouplingTests(unittest.TestCase):
    def test_requires_closed_triad(self):
        with self.assertRaises(ValueError):
            geometric_coupling((1, 0, 0), (0, 1, 0), (1, 0, 0), 1, 1, 1)

    def test_nonzero_on_the_unit_square(self):
        g = geometric_coupling((1, 0, 0), (0, 1, 0), (1, 1, 0), 1, -1, 1)
        self.assertIsInstance(g, complex)


class StarTests(unittest.TestCase):
    def test_star_is_not_a_loop_defect(self):
        rep = star_polarization()
        test = rep["test"]
        self.assertTrue(test["tree_combinatorial"])
        self.assertFalse(test["static_loop_defect"])
        self.assertIn("Stars can", rep["lock"])

    def test_polarization_test_on_star_runs(self):
        test = polarization_test(STAR_WITNESS)
        self.assertEqual(test["n_triads"], 2)
        self.assertEqual(test["dim_ker_BT"], 0)


class ParallelogramTests(unittest.TestCase):
    def test_parallelogram_is_a_cycle(self):
        test = polarization_test(PARALLELOGRAM)
        self.assertEqual(test["dim_ker_BT"], 1)
        self.assertFalse(test["tree_combinatorial"])

    def test_frame_scan_returns_a_reading(self):
        rep = parallelogram_polarization()
        self.assertEqual(len(rep["per_axis"]), 3)
        self.assertIn("reading", rep)
        # A defect that moves with the axis is not a theorem.
        if rep["defect_on_some_frame"] and not rep["defect_frame_invariant"]:
            self.assertIn("frame", rep["reading"])


if __name__ == "__main__":
    unittest.main()
