"""All-radii geometric counting: Euclidean ≤2, circle counterexample."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.all_radii_counting import (  # noqa: E402
    circle_counterexample,
    common_closer_planes,
    lattice_common_closers,
    lin_indep,
    parallel_distinct_shell_degeneracy,
    report,
    two_planes_sphere,
)


class TestTwoPlanesSphere(unittest.TestCase):
    def test_at_most_two_when_independent(self):
        out = two_planes_sphere((1.0, 0.0, 0.0), 0.0, (0.0, 1.0, 0.0), 0.0, 1.0)
        self.assertTrue(out["independent_normals"])
        self.assertLessEqual(out["n_real"], 2)
        self.assertEqual(out["n_real"], 2)
        for x in out["solutions"]:
            self.assertAlmostEqual(x[0], 0.0, places=9)
            self.assertAlmostEqual(x[1], 0.0, places=9)
            self.assertAlmostEqual(x[2] ** 2, 1.0, places=9)

    def test_parallel_normals_are_degenerate(self):
        out = two_planes_sphere((1.0, 0.0, 0.0), 1.0, (2.0, 0.0, 0.0), 2.0, 4.0)
        self.assertFalse(out["independent_normals"])
        self.assertEqual(out["degeneracy"], "parallel_planes")

    def test_solutions_satisfy_the_system(self):
        n1, c1 = (1.0, 1.0, 0.0), 1.0
        n2, c2 = (0.0, 1.0, 1.0), 0.5
        r2 = 4.0
        out = two_planes_sphere(n1, c1, n2, c2, r2)
        self.assertGreater(out["n_real"], 0)
        for x in out["solutions"]:
            self.assertAlmostEqual(n1[0] * x[0] + n1[1] * x[1] + n1[2] * x[2], c1, places=8)
            self.assertAlmostEqual(n2[0] * x[0] + n2[1] * x[1] + n2[2] * x[2], c2, places=8)
            self.assertAlmostEqual(x[0] ** 2 + x[1] ** 2 + x[2] ** 2, r2, places=8)


class TestDistinctShellHypothesis(unittest.TestCase):
    def test_parallel_distinct_shells(self):
        d = parallel_distinct_shell_degeneracy()
        self.assertTrue(d["distinct_shells"])
        self.assertFalse(d["linearly_independent"])
        self.assertFalse(d["independent_normals"])

    def test_independent_vectors_on_distinct_shells(self):
        p, q = (1, 0, 0), (0, 2, 0)
        self.assertTrue(lin_indep(p, q))
        self.assertNotEqual(p[0] ** 2 + p[1] ** 2 + p[2] ** 2, q[0] ** 2 + q[1] ** 2 + q[2] ** 2)
        geo = common_closer_planes(p, q, rho=5.0, gamma=6.0, delta=9.0)
        self.assertTrue(geo["independent_normals"])
        self.assertLessEqual(geo["n_real"], 2)


class TestCircleCounterexample(unittest.TestCase):
    def test_one_input_two_shell_exceeds_two(self):
        c = circle_counterexample()
        self.assertEqual(c["n_lattice"], 4)
        self.assertTrue(c["exceeds_two"])
        expected = {(2, 0, -1), (-2, 0, -1), (0, 2, -1), (0, -2, -1)}
        self.assertEqual(set(c["partners"]), expected)

    def test_partners_close_the_triad(self):
        p = (0, 0, 2)
        for q in circle_counterexample()["partners"]:
            self.assertEqual(q[0] ** 2 + q[1] ** 2 + q[2] ** 2, 5)
            s = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            self.assertEqual(s[0] ** 2 + s[1] ** 2 + s[2] ** 2, 5)


class TestTwoInputLattice(unittest.TestCase):
    def test_independent_pair_at_most_two(self):
        p, q = (1, 0, 0), (0, 1, 0)
        pts = lattice_common_closers(p, q, rho=2, gamma=3, delta=3, box=4)
        self.assertLessEqual(len(pts), 2)
        geo = common_closer_planes(p, q, 2.0, 3.0, 3.0)
        self.assertLessEqual(geo["n_real"], 2)


class TestReportVerdicts(unittest.TestCase):
    def test_report_does_not_promote_trilinear_from_counting(self):
        payload = report()
        v = payload["verdicts"]
        self.assertTrue(v["euclidean_two_planes_sphere_le_2"])
        self.assertFalse(v["distinct_shell_implies_independent_normals"])
        self.assertFalse(v["one_input_two_shell_multiplicity_le_2"])
        self.assertTrue(v["two_input_common_closer_le_2_when_independent"])
        self.assertFalse(v["counting_implies_trilinear_norm_bound"])
        self.assertFalse(payload["ns_solved"])
        self.assertFalse(payload["theorem_17_proved"])
        self.assertLessEqual(payload["lemma_two_planes_sphere"]["max_n_real"], 2)


if __name__ == "__main__":
    unittest.main()
