#!/usr/bin/env python3
"""Q6 → Mertens transfer stays OPEN. Not a Clay close."""

from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GCD = ROOT / "docs" / "papers" / "gcd"
LIVE_ROOT = ROOT / "domain_architect"
MOD = GCD / "q6_mertens_bridge.py"
NOTE = GCD / "Q6_MERTENS_TRANSFER.md"


def _load():
    spec = importlib.util.spec_from_file_location("q6_mertens_bridge", MOD)
    if spec is None or spec.loader is None:
        raise ImportError(MOD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BRIDGE = _load()


class TestQ6MertensBridgeStaysOpen(unittest.TestCase):
    def test_operators_are_not_the_same_matrix(self):
        self.assertAlmostEqual(BRIDGE.frobenius_diff(30), 9.05, places=2)
        a = BRIDGE.operator_a(10)
        b = BRIDGE.operator_b(10)
        self.assertFalse(np_allclose(a, b))
        self.assertEqual(a[0, 0], 1.0)
        self.assertNotEqual(a[0, 0], BRIDGE.mertens(10))

    def test_unsigned_trial_cannot_match_negative_target_on_locked_operator(self):
        n = 30
        a = BRIDGE.operator_a(n)
        v = BRIDGE.trial_one_over_sqrt(n)
        r = BRIDGE.rayleigh(a, v)
        target = BRIDGE.MINUS_ONE_OVER_TWO_PI * math.log(n)
        self.assertGreater(r, 0.0)
        self.assertGreater(r, abs(target))
        self.assertLess(BRIDGE.lambda_min(a), 0.0)
        self.assertLessEqual(BRIDGE.lambda_min(a), r)

    def test_written_step_f_sum_has_the_wrong_sign(self):
        for n in (20, 50, 100):
            u = BRIDGE.gap1_written_squarefree_sum(n)
            target = BRIDGE.MINUS_ONE_OVER_TWO_PI * math.log(n)
            self.assertGreater(u, 0.0)
            self.assertGreater(u, abs(target))

    def test_august_pdf_certificate_lambda_min_eQ20(self):
        lam = BRIDGE.lambda_min(BRIDGE.operator_a(20))
        self.assertLess(lam, -0.5)
        self.assertAlmostEqual(lam, -0.505, places=3)

    def test_mobius_trial_is_not_the_ground_state(self):
        n = 50
        a = BRIDGE.operator_a(n)
        evals, evecs = _eigh(a)
        v = evecs[:, 0]
        if v[0] < 0:
            v = -v
        mu_v = BRIDGE.trial_mu_over_sqrt(n)
        mu_v = mu_v / (mu_v @ mu_v) ** 0.5
        corr = abs(float(v @ mu_v))
        self.assertLess(corr, 0.2)
        self.assertGreater(abs(float(evals[0]) - BRIDGE.rayleigh(a, mu_v)), 0.4)

    def test_note_keeps_the_bridge_open(self):
        text = NOTE.read_text(encoding="utf-8")
        self.assertIn("still OPEN", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("Littlewood", text)
        self.assertIn("Cardinal", text)
        self.assertIn("Step F", text)
        self.assertIn("wrong sign", text)
        self.assertIn("9.054", text)
        self.assertIn("HN = D^((-1)/2)*Qtilde*D^((-1)/2)", text)
        self.assertIn("import into `domain_architect/`", text)
        self.assertNotIn("DA-VC-01 PASS", text)
        self.assertNotIn("RH follows", text.lower())
        self.assertFalse((LIVE_ROOT / "q6_mertens_bridge.py").is_file())
        self.assertFalse((LIVE_ROOT / "Q6_MERTENS_TRANSFER.md").is_file())

    def test_readme_and_faces_point_at_the_open_transfer(self):
        readme = (GCD / "README.md").read_text(encoding="utf-8")
        faces = (GCD / "FACES.md").read_text(encoding="utf-8")
        for text in (readme, faces):
            self.assertIn("Q6_MERTENS_TRANSFER.md", text)
            self.assertIn("still OPEN", text)
            self.assertIn("NOT CLAIMED", text)


def np_allclose(a, b) -> bool:
    import numpy as np

    return bool(np.allclose(a, b))


def _eigh(matrix):
    import numpy as np

    return np.linalg.eigh(matrix)


if __name__ == "__main__":
    unittest.main()
