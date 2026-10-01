#!/usr/bin/env python3
"""Exact identities and transfer-rule refusals for the Möbius–GCD matrix."""

from __future__ import annotations

import unittest

import numpy as np

from arith_qn.experiment import SIX_OVER_PI_SQUARED, q6_record, survey_row
from arith_qn.identity import (
    BRIDGE_COMPLETE,
    CANCELLATION_STATUS,
    degree_matrix,
    dirichlet_g_table,
    inverse_gcd_matrix,
    mertens,
    mobius_table,
    q_matrix,
    q6_explicit,
    trace_identity,
)
from arith_qn.spectral import (
    assess_transfer,
    congruence_eigenvalues,
    group_spectral_weights,
    spectral_decomposition,
)


class TestMobiusAndMertens(unittest.TestCase):
    def test_known_mobius_values(self):
        mu = mobius_table(30)
        self.assertEqual(mu[1], 1)
        self.assertEqual(mu[2], -1)
        self.assertEqual(mu[3], -1)
        self.assertEqual(mu[4], 0)
        self.assertEqual(mu[5], -1)
        self.assertEqual(mu[6], 1)
        self.assertEqual(mu[12], 0)
        self.assertEqual(mu[30], -1)

    def test_mertens_from_definition(self):
        mu = mobius_table(20)
        for n in range(1, 21):
            self.assertEqual(mertens(n, mu), int(mu[1 : n + 1].sum()))

    def test_mertens_six_is_minus_one(self):
        self.assertEqual(mertens(6), -1)

    def test_dirichlet_g_on_squares(self):
        g = dirichlet_g_table(4)
        self.assertAlmostEqual(g[1], 1.0)
        self.assertAlmostEqual(g[2], -1.5)
        self.assertAlmostEqual(g[4], 0.5)


class TestTraceIdentity(unittest.TestCase):
    def test_diagonal_is_mu_over_n(self):
        mu = mobius_table(32)
        q = q_matrix(32, mu)
        for n in range(1, 33):
            self.assertAlmostEqual(q[n - 1, n - 1], mu[n] / n)

    def test_trace_equals_mertens_through_80(self):
        mu = mobius_table(80)
        for n in range(1, 81):
            rec = trace_identity(n, mu)
            self.assertEqual(rec.mertens, mertens(n, mu))
            self.assertLess(rec.residual, 1e-10)
            self.assertLess(rec.divisor_residual, 1e-8)

    def test_q_is_symmetric_and_not_inverse_gcd(self):
        q = q_matrix(10)
        tilde = inverse_gcd_matrix(10)
        self.assertTrue(np.allclose(q, q.T))
        self.assertFalse(np.allclose(q, tilde))
        self.assertAlmostEqual(q[0, 0], 1.0)
        self.assertAlmostEqual(tilde[0, 0], 1.0)
        self.assertAlmostEqual(q[1, 1], -0.5)
        self.assertAlmostEqual(tilde[1, 1], 0.5)


class TestQ6(unittest.TestCase):
    def test_explicit_q6_entries(self):
        q = q6_explicit()
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, -0.5, 1.0, -0.5, 1.0, -0.5],
                [1.0, 1.0, -1.0 / 3.0, 1.0, 1.0, -1.0 / 3.0],
                [1.0, -0.5, 1.0, 0.0, 1.0, -0.5],
                [1.0, 1.0, 1.0, 1.0, -0.2, 1.0],
                [1.0, -0.5, -1.0 / 3.0, -0.5, 1.0, 1.0 / 6.0],
            ]
        )
        self.assertTrue(np.allclose(q, expected))

    def test_q6_trace_and_record(self):
        rec = trace_identity(6)
        self.assertEqual(rec.mertens, -1)
        self.assertLess(rec.residual, 1e-12)
        payload = q6_record()
        self.assertEqual(payload["mertens"], -1)
        self.assertAlmostEqual(payload["weight_sum"], 21.0, places=8)


class TestSpectralIdentity(unittest.TestCase):
    def test_weighted_sum_matches_mertens(self):
        mu = mobius_table(48)
        for n in (1, 2, 6, 10, 16, 24, 32, 48):
            decomp = spectral_decomposition(n, mu)
            self.assertLess(decomp.residual, 1e-8)
            self.assertAlmostEqual(decomp.weight_sum, n * (n + 1) / 2.0, places=6)
            self.assertGreaterEqual(decomp.weight_min, 1.0 - 1e-8)
            self.assertLessEqual(decomp.weight_max, n + 1e-8)

    def test_orthonormal_eigenbasis(self):
        decomp = spectral_decomposition(20)
        gram = decomp.eigenvectors.T @ decomp.eigenvectors
        self.assertTrue(np.allclose(gram, np.eye(20), atol=1e-10))
        reconstructed = (
            decomp.eigenvectors * decomp.eigenvalues
        ) @ decomp.eigenvectors.T
        self.assertTrue(np.allclose(reconstructed, q_matrix(20), atol=1e-10))

    def test_projector_weights_reproduce_mertens(self):
        decomp = spectral_decomposition(24)
        clusters = group_spectral_weights(decomp)
        total = sum(c.contribution for c in clusters)
        self.assertAlmostEqual(total, decomp.mertens, places=8)
        self.assertAlmostEqual(
            sum(c.projector_weight for c in clusters),
            decomp.weight_sum_target,
            places=6,
        )

    def test_congruence_trace_is_mertens(self):
        for n in (6, 12, 30):
            alpha = congruence_eigenvalues(n)
            self.assertAlmostEqual(float(np.sum(alpha)), mertens(n), places=8)

    def test_degree_matrix_is_index_diagonal(self):
        d = degree_matrix(5)
        self.assertTrue(np.array_equal(np.diag(d), np.arange(1, 6)))


class TestCrudeBoundAndTransferRule(unittest.TestCase):
    def test_op_norm_at_least_sqrt_n(self):
        # First column of Q_N is all ones, so ||Q_N e_1|| = √N.
        for n in (6, 16, 36):
            decomp = spectral_decomposition(n)
            self.assertGreaterEqual(decomp.op_norm, np.sqrt(n) - 1e-8)
            self.assertGreaterEqual(decomp.crude_bound, np.sqrt(n) * n * (n + 1) / 2.0 - 1e-6)
            self.assertGreater(decomp.crude_bound, abs(decomp.mertens))

    def test_crude_bound_is_weaker_than_trivial_mertens(self):
        row = survey_row(32)
        self.assertGreater(row.crude_bound, 32)  # trivial |M| ≤ N
        self.assertGreater(row.crude_over_abs_m, 10.0)

    def test_op_norm_tracks_coprime_density(self):
        row = survey_row(96)
        self.assertAlmostEqual(row.op_norm_over_n, SIX_OVER_PI_SQUARED, delta=0.03)
        self.assertGreater(row.leading_weight, 10.0)

    def test_bridge_stays_open(self):
        self.assertFalse(BRIDGE_COMPLETE)
        self.assertEqual(CANCELLATION_STATUS, "OPEN")
        closed = assess_transfer(identity_residual_ok=True, independent_qn_bound=False)
        self.assertTrue(closed.identity_proved)
        self.assertFalse(closed.useful_transfer)
        self.assertFalse(closed.bridge_complete)
        self.assertEqual(closed.cancellation_status, "OPEN")

    def test_even_an_independent_bound_flag_does_not_claim_rh(self):
        # The module constant BRIDGE_COMPLETE is hard-false. A later
        # independent Q_N estimate would still need a separate proof.
        maybe = assess_transfer(identity_residual_ok=True, independent_qn_bound=True)
        self.assertTrue(maybe.useful_transfer)
        self.assertFalse(maybe.bridge_complete)


if __name__ == "__main__":
    unittest.main()
