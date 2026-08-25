"""Kernel facts for the SFE black-hole matplotlib toy.

Not a physics test. Checks the honest description: Phi is independent
of (x, y); the only spatial structure is a disk mask.
"""

from __future__ import annotations

import ast
import importlib.util
import unittest
from pathlib import Path

import numpy as np

ARCHIVE = Path(__file__).resolve().parents[1] / "docs" / "archive" / "sfe-black-hole-sim"
HEADLESS = ARCHIVE / "sfe_field_headless.py"
PASTE = ARCHIVE / "sfe_field_paste.py"


def _load_headless():
    spec = importlib.util.spec_from_file_location("sfe_field_headless", HEADLESS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestSfeBlackHoleToy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_headless()

    def test_phi_independent_of_xy(self):
        x = np.linspace(-10, 10, 40)
        y = np.linspace(-10, 10, 40)
        X, Y = np.meshgrid(x, y)
        t = 1.3
        masked = self.mod.sfe_field(X, Y, t)
        unique = np.unique(np.round(masked, 12))
        self.assertLessEqual(unique.size, 2)
        self.assertIn(0.0, unique)

    def test_disk_mask_zeros_inside(self):
        epsilon = 0.5
        t = 0.7
        phi = self.mod.phi_scalar(t)
        X, Y = np.meshgrid(np.linspace(-10, 10, 80), np.linspace(-10, 10, 80))
        r = np.sqrt(X**2 + Y**2)
        out = self.mod.sfe_field(X, Y, t, epsilon=epsilon)
        inside = r + 1e-5 <= abs(phi) / epsilon
        if np.any(inside):
            self.assertTrue(np.allclose(out[inside], 0.0))
        outside = r + 1e-5 > abs(phi) / epsilon
        if np.any(outside) and abs(phi) > 1e-12:
            self.assertTrue(np.allclose(out[outside], phi))

    def test_paste_keeps_title_and_gamma(self):
        text = PASTE.read_text(encoding="utf-8")
        self.assertIn("SFE Black Hole Simulator: Coherence Collapse", text)
        self.assertIn("sfe_field", text)
        self.assertIn("Gamma", text)
        self.assertIn("r + 1e-5", text)
        self.assertIn("plt.show()", text)
        self.assertNotIn("chatvault", text.lower())

    def test_headless_has_no_show(self):
        tree = ast.parse(HEADLESS.read_text(encoding="utf-8"))
        calls = [
            n.func.attr
            for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
        ]
        self.assertNotIn("show", calls)

    def test_render_frame_shape(self):
        frame = self.mod.render_frame(0.0, n=32)
        self.assertEqual(frame.shape, (32, 32))


if __name__ == "__main__":
    unittest.main()
