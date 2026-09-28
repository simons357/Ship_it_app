"""Direct T_c versus the undecomposed helical sum. Not DA-NS-2."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier import cube_modes  # noqa: E402
from ns_attacks.galerkin import random_cube  # noqa: E402
from ns_attacks.phase_network import network_sum  # noqa: E402


class FullHelicalFlowTests(unittest.TestCase):
    def test_radius_one_176_channels(self):
        rng = np.random.default_rng(0)
        f = random_cube(1, rng)
        modes = cube_modes(1)
        rec = network_sum(f, modes)
        self.assertEqual(rec["n_signed"], 176.0)
        self.assertEqual(rec["n_triads"], 22.0)
        self.assertLess(rec["recon_err"], 1e-12)
        self.assertLess(abs(rec["energy_pairing"]), 1e-12)

    def test_radius_two_4272_channels(self):
        rng = np.random.default_rng(0)
        f = random_cube(2, rng)
        modes = cube_modes(2)
        rec = network_sum(f, modes)
        self.assertEqual(rec["n_signed"], 4272.0)
        self.assertLess(rec["recon_err"], 1e-10)
        self.assertLess(rec["max_factor_resid"], 1e-10)

    def test_second_seed_still_reconstructs(self):
        rng = np.random.default_rng(7)
        f = random_cube(1, rng)
        rec = network_sum(f, cube_modes(1))
        self.assertLess(rec["recon_err"], 1e-12)


if __name__ == "__main__":
    unittest.main()
