"""Phase network: factorization, heterochiral bridge, phase twins."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.galerkin import Field, flux_stats, moments  # noqa: E402
from ns_attacks.phase_network import (  # noqa: E402
    SEED_K,
    SEED_P,
    SEED_Q,
    SEED_SIGMA,
    C_multiplier,
    channel_record,
    network_sum,
)
from ns_attacks.symmetry_2d3c import locked_seed  # noqa: E402


def _single_channel(ak, ap, aq, sigma=SEED_SIGMA) -> Field:
    return Field().from_amplitudes(
        {
            (SEED_K, sigma[0]): ak,
            (SEED_P, sigma[1]): ap,
            (SEED_Q, sigma[2]): aq,
        },
        reality=True,
    )


class HelicalPhaseNetworkTests(unittest.TestCase):
    def test_seed_triad_closes(self):
        self.assertEqual(
            (SEED_K[0] + SEED_P[0] + SEED_Q[0], SEED_K[1] + SEED_P[1] + SEED_Q[1], SEED_K[2] + SEED_P[2] + SEED_Q[2]),
            (0, 0, 0),
        )

    def test_eight_signed_channels_on_one_triad(self):
        f = _single_channel(1.0, 0.4 + 0.3j, -0.7 + 0.2j)
        modes = f.modes()
        rec = network_sum(f, modes)
        self.assertEqual(rec["n_signed"], 8.0)
        self.assertLess(rec["recon_err"], 1e-12)
        self.assertLess(rec["max_factor_resid"], 1e-12)

    def test_heterochiral_bridge(self):
        f = _single_channel(1.0, 1.2 - 0.5j, -0.7 + 0.2j)
        Lam = moments(f)["Lambda"]
        rec = channel_record(f, SEED_K, SEED_P, SEED_Q, SEED_SIGMA, Lam)
        self.assertLess(rec["het_resid"], 1e-12)
        self.assertAlmostEqual(rec["T_c"], rec["R_lambda"] * rec["Q_abs"], places=10)

    def test_homochiral_absolute_helicity_cancels(self):
        f = _single_channel(1.0, 1.2 - 0.5j, -0.7 + 0.2j, sigma=(1, 1, 1))
        Lam = moments(f)["Lambda"]
        rec = channel_record(f, SEED_K, SEED_P, SEED_Q, (1, 1, 1), Lam)
        self.assertLess(abs(rec["Q_abs"]), 1e-12)
        self.assertNotAlmostEqual(rec["T_c"], 0.0, places=6)

    def test_phase_twin_flips_sign(self):
        f = _single_channel(1.0, 0.8, 0.5 + 0.4j)
        twin = _single_channel(1.0, 0.8, -(0.5 + 0.4j))
        modes = f.modes()
        a = flux_stats(f, modes)
        b = flux_stats(twin, modes)
        for key in ("X", "Y", "Z", "Lambda", "D_s"):
            self.assertAlmostEqual(a[key], b[key], places=10, msg=key)
        self.assertAlmostEqual(a["T_c"], -b["T_c"], places=10)
        self.assertGreater(abs(a["T_c"]), 1e-8)

    def test_locked_seed_alignment_and_reconstruction(self):
        f = locked_seed()
        rec = network_sum(f, f.modes())
        self.assertEqual(rec["n_signed"], 8.0)
        self.assertLess(rec["recon_err"], 1e-12)
        from ns_attacks.symmetry_2d3c import all_raw_W_imaginary_parts

        im = all_raw_W_imaginary_parts(f, f.modes())
        self.assertTrue(im)
        self.assertLess(max(im), 1e-12)

    def test_C_vanishes_when_two_signed_radii_equal(self):
        a, b, c, Lam = 2.0, 2.0, -3.0, 1.0
        self.assertAlmostEqual(C_multiplier(a, b, c, Lam), 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
