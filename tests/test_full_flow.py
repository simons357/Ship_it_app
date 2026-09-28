#!/usr/bin/env python3
"""Sprint 01 full-flow identities: k+p+q=0, conjugation, charge.

Not a close. NS is not solved. v2 not run. DA-NS-2 open.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.channel_coefficient import HETEROCHIRAL_SIGMA, PARALLELOGRAM, is_heterochiral
from ns_attacks.full_flow import (
    PARALLELOGRAM_SUM0,
    SEED_SUM0,
    canonical_24_payload_sum0,
    channel_transfers,
    energy_fit_g,
    full_flow_report,
    g_Delta_sigma,
)
from ns_attacks.helical import add, wrap_pi

PI = math.pi
PI6 = PI / 6.0
FIVE_PI6 = 5.0 * PI / 6.0


def _near_abs(theta: float, target: float, places: int = 8) -> bool:
    return abs(abs(wrap_pi(theta)) - target) < 10 ** (-places)


class TestSum0Representatives(unittest.TestCase):
    def test_seed_is_sprint01_section_4_3(self):
        name, k, p, q = SEED_SUM0
        self.assertEqual(name, "seed")
        self.assertEqual(k, (1, 0, 0))
        self.assertEqual(p, (0, 1, 1))
        self.assertEqual(q, (-1, -1, -1))
        self.assertEqual(add(add(k, p), q), (0, 0, 0))

    def test_parallelogram_sum0_is_negated_output(self):
        self.assertEqual(len(PARALLELOGRAM_SUM0), 4)
        for (name0, k, p, q), (name, p_old, q_old, k_out) in zip(PARALLELOGRAM_SUM0, PARALLELOGRAM):
            self.assertEqual(name0, name)
            self.assertEqual(p, p_old)
            self.assertEqual(q, q_old)
            self.assertEqual(k, tuple(-x for x in k_out))
            self.assertEqual(add(add(k, p), q), (0, 0, 0))


class TestFullFlowAlgebra(unittest.TestCase):
    def test_full_flow_report_passes(self):
        report = full_flow_report()
        self.assertTrue(report["passed"], report["maxima"])
        self.assertEqual(report["n_certified"], 5 * 6)
        self.assertTrue(report["conjugation_essential"])
        self.assertTrue(report["DA_NS_2_open"])
        self.assertTrue(report["v2_not_run"])
        self.assertGreater(report["max_Theta_no_conj_err_live"], 1e-3)
        for key, val in report["maxima"].items():
            self.assertLess(val, 1e-10, key)

    def test_U_is_unimodular_not_identically_one(self):
        report = full_flow_report()
        live = [row for row in report["rows"] if not row["vandermonde_zero"]]
        self.assertGreaterEqual(len(live), 20)
        for row in live:
            self.assertAlmostEqual(row["U_abs"], 1.0, places=12)
        t1 = [row for row in live if row["delta"] == "T1"]
        t2 = [row for row in live if row["delta"] == "T2"]
        t3 = [row for row in live if row["delta"] == "T3"]
        t4 = [row for row in live if row["delta"] == "T4"]
        seed = [row for row in live if row["delta"] == "seed"]
        self.assertTrue(t1 and t2 and t3 and t4 and seed)
        for row in t1:
            self.assertAlmostEqual(row["U_arg"], 0.0, places=10)
        for row in t2:
            self.assertAlmostEqual(abs(row["U_arg"]), PI, places=10)
        for row in t3:
            self.assertAlmostEqual(abs(row["U_arg"]), PI / 2.0, places=10)
        for row in t4 + seed:
            self.assertTrue(
                _near_abs(row["U_arg"], PI6) or _near_abs(row["U_arg"], FIVE_PI6),
                row["U_arg"],
            )
        self.assertTrue(report["U_frame"]["do_not_treat_U_as_1"])

    def test_energy_fit_uses_conjugation(self):
        _, k, p, q = SEED_SUM0
        sigma = (1, 1, -1)
        g = energy_fit_g(k, p, q, sigma)
        amps = (0.3 + 0.4j, 0.5 - 0.2j, -0.1 + 0.7j)
        ch = channel_transfers(k, p, q, sigma, *amps)
        a, b, c = ch["a"], ch["b"], ch["c"]
        Theta = ch["T"][k] / (b - c)
        self.assertAlmostEqual((g * ch["aaa"].conjugate()).real, Theta, places=12)
        self.assertGreater(abs((g * ch["aaa"]).real - Theta), 1e-3)


class TestCanonical24Sum0(unittest.TestCase):
    def test_payload_count_convention_and_U(self):
        payload = canonical_24_payload_sum0()
        self.assertEqual(payload["n_channels"], 24)
        self.assertEqual(payload["convention"], "k+p+q=0")
        self.assertEqual(len(payload["channels"]), 24)
        self.assertTrue(payload["DA_NS_2_open"])
        self.assertTrue(payload["v2_not_run"])
        ids = [ch["gamma"]["delta_id"] for ch in payload["channels"]]
        self.assertEqual(ids.count("T1"), 6)
        self.assertEqual(ids.count("T2"), 6)
        self.assertEqual(ids.count("T3"), 6)
        self.assertEqual(ids.count("T4"), 6)
        live_u = 0
        for ch in payload["channels"]:
            k, p, q = ch["gamma"]["k"], ch["gamma"]["p"], ch["gamma"]["q"]
            self.assertEqual(add(add(tuple(k), tuple(p)), tuple(q)), (0, 0, 0))
            self.assertTrue(is_heterochiral(ch["gamma"]["sigma_kpq"]))
            self.assertGreater(abs(ch["g_Delta_sigma"]["abs"]), 1e-12)
            if ch["vandermonde_zero"]:
                self.assertNotIn("U", ch)
                continue
            self.assertAlmostEqual(ch["U"]["abs"], 1.0, places=12)
            live_u += 1
        self.assertEqual(live_u, 20)  # T1/T2 odd-k are Vandermonde zeros

    def test_heterochiral_sigma_are_the_six(self):
        self.assertEqual(len(HETEROCHIRAL_SIGMA), 6)
        G0 = g_Delta_sigma(*SEED_SUM0[1:], (1, 1, -1))
        self.assertGreater(abs(G0), 1e-12)


if __name__ == "__main__":
    unittest.main()
