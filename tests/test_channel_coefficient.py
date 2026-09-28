#!/usr/bin/env python3
"""Coefficient identity and canonical γ=(Δ,σ) 24-channel catalog."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.channel_coefficient import (
    A_coeff,
    HETEROCHIRAL_SIGMA,
    PARALLELOGRAM,
    PARALLELOGRAM_CYCLE,
    PROBE_TRIADS,
    arg_delta_ordered_minus_cross,
    canonical_24_payload,
    certify_one,
    channel_radii,
    identity_report,
    is_heterochiral,
    kernels,
    odd_leg,
    signed_radii,
)
from ns_attacks.helical import AXES, add, wrap_pi


class TestHeterochiralOntology(unittest.TestCase):
    def test_six_heterochiral_sigma_not_cyclic_outputs(self):
        self.assertEqual(len(HETEROCHIRAL_SIGMA), 6)
        self.assertEqual(len(set(HETEROCHIRAL_SIGMA)), 6)
        odds = [odd_leg(s) for s in HETEROCHIRAL_SIGMA]
        self.assertEqual(odds.count("k"), 2)
        self.assertEqual(odds.count("p"), 2)
        self.assertEqual(odds.count("q"), 2)
        for s in HETEROCHIRAL_SIGMA:
            self.assertTrue(is_heterochiral(s))
            self.assertEqual(abs(sum(s)), 1)  # two + one −, or two − one +

    def test_homochiral_rejected(self):
        self.assertFalse(is_heterochiral((1, 1, 1)))
        self.assertFalse(is_heterochiral((-1, -1, -1)))
        with self.assertRaises(ValueError):
            odd_leg((1, 1, 1))

    def test_overall_sign_pairs(self):
        pairs = [
            ((1, 1, -1), (-1, -1, 1)),
            ((1, -1, 1), (-1, 1, -1)),
            ((-1, 1, 1), (1, -1, -1)),
        ]
        for a, b in pairs:
            self.assertEqual(tuple(-x for x in a), b)
            self.assertEqual(odd_leg(a), odd_leg(b))


class TestCoefficientIdentity(unittest.TestCase):
    def test_identity_report_passes(self):
        report = identity_report()
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["n_certified"], (4 + 5) * 6)
        self.assertLess(report["max_phase_err"], 1e-10)
        self.assertLess(report["max_axis_spread_of_mu"], 1e-10)

    def test_gW_is_k_leg_fold_not_channel(self):
        # Isosceles |p|=|q|, odd-k: g_W = 0 while G_cross and g_ordered live.
        p, q, k = (1, 0, 0), (0, 1, 0), (1, 1, 0)
        sigma = (-1, 1, 1)  # odd k
        self.assertEqual(odd_leg(sigma), "k")
        kn = kernels(p, q, k, sigma)
        a, b, c = signed_radii(p, q, k, sigma)
        self.assertAlmostEqual(b - c, 0.0, places=12)
        self.assertLess(abs(kn["g_W"]), 1e-12)
        self.assertGreater(abs(kn["g_cross"]), 1e-8)
        self.assertGreater(abs(kn["g_ordered"]), 1e-8)

    def test_phase_offset_is_minus_sp_pi_over_2(self):
        p, q, k = (3, 1, 1), (-1, 2, 2), (2, 3, 3)
        for sigma in HETEROCHIRAL_SIGMA:
            kn = kernels(p, q, k, sigma)
            sp = sigma[1]
            d = wrap_pi(
                math.atan2(kn["g_ordered"].imag, kn["g_ordered"].real)
                - math.atan2(kn["g_cross"].imag, kn["g_cross"].real)
            )
            self.assertAlmostEqual(d, arg_delta_ordered_minus_cross(sp), places=10)

    def test_axis_invariance_of_ratio(self):
        p, q, k = (2, -1, 0), (0, 2, 1), (2, 1, 1)
        for sigma in HETEROCHIRAL_SIGMA:
            cert = certify_one(p, q, k, sigma, AXES)
            self.assertLess(cert["axis_spread"], 1e-12)

    def test_probe_triads_close(self):
        for p, q, k in PROBE_TRIADS:
            self.assertEqual(add(p, q), k)


class TestCanonical24(unittest.TestCase):
    def test_payload_count_and_A(self):
        payload = canonical_24_payload()
        self.assertEqual(payload["n_channels"], 24)
        self.assertEqual(len(payload["channels"]), 24)
        self.assertEqual(payload["n_geometric_delta"], 4)
        self.assertEqual(payload["n_heterochiral_sigma"], 6)
        self.assertEqual(payload["cycle_sum"], 0)
        self.assertTrue(payload["v2_not_run"])
        ids = [ch["gamma"]["delta_id"] for ch in payload["channels"]]
        self.assertEqual(ids.count("T1"), 6)
        self.assertEqual(ids.count("T2"), 6)
        self.assertEqual(ids.count("T3"), 6)
        self.assertEqual(ids.count("T4"), 6)
        for ch in payload["channels"]:
            i, j, o = ch["radii"]["i"], ch["radii"]["j"], ch["radii"]["o"]
            self.assertAlmostEqual(ch["A_gamma"], A_coeff(i, j, o), places=12)
            self.assertGreater(abs(ch["g_Delta_sigma"]["abs"]), 1e-12)
            p, q, k = ch["gamma"]["p"], ch["gamma"]["q"], ch["gamma"]["k"]
            self.assertEqual(add(tuple(p), tuple(q)), tuple(k))

    def test_parallelogram_cycle_sums_to_zero(self):
        self.assertEqual(sum(PARALLELOGRAM_CYCLE), 0)
        self.assertEqual(len(PARALLELOGRAM), 4)

    def test_A_matches_phase_to_charge_prefactor(self):
        # A = (i+o)(j+o)/(2o) on T1, odd q: i=|p|=1, j=|k|=√2, o=1
        p, q, k = PARALLELOGRAM[0][1:]
        sigma = (1, 1, -1)
        rad = channel_radii(p, q, k, sigma)
        self.assertEqual(rad["odd"], "q")
        self.assertAlmostEqual(rad["o"], 1.0, places=12)
        self.assertAlmostEqual(A_coeff(rad["i"], rad["j"], rad["o"]), (1 + math.sqrt(2)), places=12)


if __name__ == "__main__":
    unittest.main()
