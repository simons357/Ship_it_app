"""Unit checks for Route N shellwise floor probe."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[1]
_PROBE = _REPO / "scripts" / "route_n_shell_floor_probe.py"
_spec = importlib.util.spec_from_file_location("route_n_shell_floor_probe", _PROBE)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
probe_one = _mod.probe_one
shell_index_sets = _mod.shell_index_sets


class TestRouteNShellFloor(unittest.TestCase):
    def test_shell_partition_covers_1_to_M(self) -> None:
        M = 40
        shells = shell_index_sets(M)
        idxs = sorted(i for _, block in shells for i in block)
        self.assertEqual(idxs, list(range(M)))
        # n=1 → j=0; n in [2,3] → j=1; [4,7] → j=2
        by_j = dict(shells)
        self.assertEqual(by_j[0], [0])
        self.assertEqual(by_j[1], [1, 2])
        self.assertEqual(by_j[2], [3, 4, 5, 6])

    def test_convexity_toy_equal_blocks(self) -> None:
        # Elementary sanity: λ_min of convex combo ≥ weighted sum of λ_mins
        B0 = np.diag([1.0, -0.2])
        B1 = np.diag([0.5, -0.3])
        a0, a1 = 0.4, 0.6
        combo = a0 * B0 + a1 * B1
        lhs = float(np.linalg.eigvalsh(combo)[0])
        rhs = a0 * float(np.linalg.eigvalsh(B0)[0]) + a1 * float(
            np.linalg.eigvalsh(B1)[0]
        )
        self.assertGreaterEqual(lhs + 1e-12, rhs)
        self.assertGreaterEqual(rhs, min(-0.2, -0.3) - 1e-12)

    def test_shellwise_clears_half_while_full_q_fails(self) -> None:
        # Through M=64: full Q̃ can sit below −1/2 while shell mins clear it.
        r = probe_one(64)
        self.assertLess(r["q_full"], -0.5)
        self.assertGreater(r["q_min_shell"], -0.5)
        self.assertGreater(r["h_min_shell"], -0.5)
        self.assertTrue(r["q_shell_clear_half"])
        self.assertTrue(r["h_shell_clear_half"])

    def test_worst_shell_stable_near_j1(self) -> None:
        r = probe_one(128)
        worst = min(r["q_shells"], key=lambda t: t[2])
        # Probe historically pins worst Q̃ shell near j=1 (indices {2,3})
        self.assertEqual(worst[0], 1)
        self.assertGreater(worst[2], -0.5)
        self.assertLess(worst[2], -0.2)


if __name__ == "__main__":
    unittest.main()
