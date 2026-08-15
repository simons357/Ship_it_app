"""Smoke tests for Bridge* / H_N panel checks."""
from __future__ import annotations

import unittest
from math import gcd

import numpy as np


def mat_tilde(N: int) -> np.ndarray:
    A = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / (gcd(i, j) * (i * j) ** 0.5)
            A[i - 1, j - 1] = A[j - 1, i - 1] = v
    return A


def H_matrix(N: int) -> np.ndarray:
    Qt = mat_tilde(N)
    d = Qt.sum(axis=1)
    inv = 1.0 / np.sqrt(d)
    return (inv[:, None] * Qt) * inv[None, :]


class TestBridgeStarAndHN(unittest.TestCase):
    def test_section_21_identity_false(self):
        # June 5 claimed 1/n = Σ μ(d)φ(d)/d² — false at n=2
        def mu(n):
            if n == 1:
                return 1
            x, c, p = n, 0, 2
            while p * p <= x:
                if x % p == 0:
                    x //= p
                    c += 1
                    if x % p == 0:
                        return 0
                p += 1
            if x > 1:
                c += 1
            return -1 if c % 2 else 1

        def phi(n):
            r, x = n, n
            p = 2
            while p * p <= x:
                if x % p == 0:
                    while x % p == 0:
                        x //= p
                    r -= r // p
                p += 1
            if x > 1:
                r -= r // x
            return r

        s = sum(mu(d) * phi(d) / (d * d) for d in (1, 2))
        self.assertNotAlmostEqual(s, 0.5)

    def test_single_pair_bridge_star(self):
        for p, q in [(2, 3), (3, 5), (3, 7), (5, 11), (11, 19)]:
            R = 0.5 * (1 / p**2 + 1 / q**2) - 1 / (p * q) ** 0.5
            self.assertGreater(R, -0.5)

    def test_raw_Q_floor_fails(self):
        N = 20
        A = np.empty((N, N))
        for i in range(1, N + 1):
            for j in range(i, N + 1):
                v = 1.0 / gcd(i, j)
                A[i - 1, j - 1] = A[j - 1, i - 1] = v
        self.assertLess(float(np.linalg.eigvalsh(A)[0]), -0.5)

    def test_H_N_not_universal_minus_3_14(self):
        mn = float(np.linalg.eigvalsh(H_matrix(4))[0])
        self.assertLess(mn, -3.0 / 14.0)
        self.assertGreater(mn, -0.5)

    def test_H_N_lambda_max_one(self):
        for N in (10, 50):
            mx = float(np.linalg.eigvalsh(H_matrix(N))[-1])
            self.assertAlmostEqual(mx, 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
