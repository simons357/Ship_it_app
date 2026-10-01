"""Fail-fast tests for the STTP normal-form diagnostic.

Not a closure theorem. Centered drift remains OPEN. NS is not solved.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.sttp_normal_form import (  # noqa: E402
    CUBELET,
    IDENTITY_TOL,
    C_lambda,
    C_lambda_polarization,
    R4,
    comparable_triad_filter_vacuous,
    cubelet_frequency_lengths,
    cubelet_max_length_ratio,
    dphi_dlam,
    euler_identity_error,
    exhibit_c_field,
    lambda_dot,
    moments,
    moving_lambda_term,
    phi_lambda,
    random_cubelet_field,
    run_diagnostic,
    scale_field,
)


class CubeletTriadTests(unittest.TestCase):
    def test_lengths_lie_between_1_and_sqrt3(self):
        lengths = cubelet_frequency_lengths()
        self.assertAlmostEqual(lengths[0], 1.0)
        self.assertAlmostEqual(lengths[-1], math.sqrt(3.0))
        self.assertEqual(len(CUBELET), 26)

    def test_ratio_2_filter_is_vacuous(self):
        self.assertLess(cubelet_max_length_ratio(), 2.0)
        self.assertTrue(comparable_triad_filter_vacuous())


class FixedLambdaIdentityTests(unittest.TestCase):
    def test_closed_form_matches_polarization(self):
        rng = np.random.default_rng(3)
        errors = []
        for _ in range(12):
            field = random_cubelet_field(rng)
            lam = moments(field)["Lambda"]
            closed = C_lambda(field, lam)
            pol = C_lambda_polarization(field, lam)
            errors.append(abs(closed - pol))
            self.assertLess(euler_identity_error(field, lam), 1e-12)
        self.assertLess(max(errors), IDENTITY_TOL)

    def test_identity_fails_fast_when_threshold_breaks(self):
        with self.assertRaises(AssertionError) as ctx:
            from ns_attacks.sttp_normal_form import DiagnosticReport, _assert_report

            bad = DiagnosticReport(
                identity_max_abs_error=1e-3,
                identity_pass=False,
                r4_positive=10,
                r4_negative=10,
                r4_nonfinite=0,
                n_random=20,
                C_lambda_amp_slope=3.0,
                R4_amp_slope=4.0,
                scaling_pass=True,
                exhibit_c_moving_term=0.01,
                exhibit_c_lambda_dot=0.01,
                exhibit_c_dphi_dlam=1.0,
                cubelet_min_length=1.0,
                cubelet_max_length=math.sqrt(3.0),
                cubelet_max_ratio=math.sqrt(3.0),
                comparable_triad_filter_vacuous=True,
                centered_drift_closed=False,
                ns_solved=False,
                moving_lambda_included=True,
                fail_fast=True,
            )
            _assert_report(bad)
        self.assertIn("fixed-λ identity failed", str(ctx.exception))


class RemainderAndScalingTests(unittest.TestCase):
    def test_amplitude_degrees(self):
        shape = exhibit_c_field()
        amps = (0.5, 1.0, 2.0)
        from ns_attacks.sttp_normal_form import loglog_slope

        c_vals = []
        r_vals = []
        for a in amps:
            f = scale_field(shape, a)
            lam = moments(f)["Lambda"]
            c_vals.append(C_lambda(f, lam))
            r_vals.append(R4(f, lam))
        self.assertAlmostEqual(loglog_slope(amps, c_vals), 3.0, places=6)
        self.assertAlmostEqual(loglog_slope(amps, r_vals), 4.0, places=6)

    def test_r4_is_nonzero_and_recorded_on_random_cubelets(self):
        rng = np.random.default_rng(11)
        pos = neg = 0
        vals = []
        for _ in range(40):
            field = random_cubelet_field(rng)
            rem = R4(field, moments(field)["Lambda"])
            vals.append(rem)
            if rem > 0:
                pos += 1
            elif rem < 0:
                neg += 1
        self.assertGreater(pos + neg, 0)
        self.assertTrue(all(np.isfinite(vals)))
        # This declared resolvent primitive has been positive on every
        # cubelet sample so far. That is a sample, not a positivity theorem,
        # and it is not ChatGPT's sign-indefinite remainder.


class MovingLambdaTests(unittest.TestCase):
    def test_exhibit_c_term_is_computed_and_nonzero(self):
        field = exhibit_c_field()
        lam = moments(field)["Lambda"]
        term = moving_lambda_term(field, lam)
        self.assertTrue(np.isfinite(term))
        self.assertGreater(abs(term), 1e-18)
        self.assertAlmostEqual(term, lambda_dot(field) * dphi_dlam(field, lam))

    def test_omitting_the_term_is_a_failure(self):
        from ns_attacks.sttp_normal_form import DiagnosticReport, _assert_report

        with self.assertRaises(AssertionError) as ctx:
            _assert_report(
                DiagnosticReport(
                    identity_max_abs_error=1e-14,
                    identity_pass=True,
                    r4_positive=10,
                    r4_negative=10,
                    r4_nonfinite=0,
                    n_random=20,
                    C_lambda_amp_slope=3.0,
                    R4_amp_slope=4.0,
                    scaling_pass=True,
                    exhibit_c_moving_term=0.0,
                    exhibit_c_lambda_dot=0.01,
                    exhibit_c_dphi_dlam=0.0,
                    cubelet_min_length=1.0,
                    cubelet_max_length=math.sqrt(3.0),
                    cubelet_max_ratio=math.sqrt(3.0),
                    comparable_triad_filter_vacuous=True,
                    centered_drift_closed=False,
                    ns_solved=False,
                    moving_lambda_included=True,
                    fail_fast=True,
                )
            )
        self.assertIn("moving-λ term vanished", str(ctx.exception))


class HonestyLockTests(unittest.TestCase):
    def test_diagnostic_does_not_close_centered_drift(self):
        report = run_diagnostic(seed=5, n_random=40, fail_fast=True)
        self.assertFalse(report.centered_drift_closed)
        self.assertFalse(report.ns_solved)
        self.assertTrue(report.moving_lambda_included)
        self.assertTrue(report.identity_pass)
        self.assertTrue(report.scaling_pass)
        self.assertTrue(report.comparable_triad_filter_vacuous)

    def test_phi_is_real_on_real_fields(self):
        field = exhibit_c_field()
        value = phi_lambda(field, moments(field)["Lambda"])
        self.assertIsInstance(value, float)
        self.assertTrue(np.isfinite(value))


if __name__ == "__main__":
    unittest.main()
