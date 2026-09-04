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

    def test_cross_term_factorization(self):
        # (1/√p - 1/√q)(1/√r - 1/√s) for distinct primes
        for p, q, r, s in [(3, 5, 7, 11), (2, 3, 5, 7), (5, 13, 11, 17)]:
            cross = (
                1 / (p * r) ** 0.5
                - 1 / (p * s) ** 0.5
                - 1 / (q * r) ** 0.5
                + 1 / (q * s) ** 0.5
            )
            fact = (p**-0.5 - q**-0.5) * (r**-0.5 - s**-0.5)
            self.assertAlmostEqual(cross, fact, places=12)
            if p < q and r < s:
                self.assertGreater(cross, 0.0)

    def test_multirep_bridge_star(self):
        def primes_upto(n: int) -> set[int]:
            s = [True] * (n + 1)
            s[0] = s[1] = False
            for i in range(2, int(n**0.5) + 1):
                if s[i]:
                    s[i * i :: i] = [False] * len(s[i * i :: i])
            return {i for i, b in enumerate(s) if b}

        N = 80
        Qt = mat_tilde(N)
        P = primes_upto(N)
        for k in range(4, N + 1, 2):
            v = np.zeros(N)
            for p in range(2, (k + 1) // 2):
                q = k - p
                if p in P and q in P and q <= N:
                    v[p - 1] += 1.0
                    v[q - 1] -= 1.0
            nrm2 = float(v @ v)
            if nrm2 < 1e-12:
                continue
            R = float(v @ Qt @ v) / nrm2
            self.assertGreater(R, -0.5, msg=f"k={k} R={R}")

    def test_tilde_Q_floor_fails(self):
        self.assertLess(float(np.linalg.eigvalsh(mat_tilde(20))[0]), -0.5)

    def test_route_c_mobius_lemma_a_false_at_gcd2(self):
        # 1/gcd = sum mu phi/d^2 fails at gcd=2: LHS 1/2, RHS 3/4
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
            r, x, p = n, n, 2
            while p * p <= x:
                if x % p == 0:
                    while x % p == 0:
                        x //= p
                    r -= r // p
                p += 1
            if x > 1:
                r -= r // x
            return r

        rhs = sum(mu(d) * phi(d) / (d * d) for d in (1, 2))
        self.assertAlmostEqual(rhs, 0.75)
        self.assertNotAlmostEqual(rhs, 0.5)

    def test_positive_gcd_zero_diag_kill(self):
        N = 5
        Q = np.array([[gcd(i, j) / (i * j) ** 0.5 for j in range(1, N + 1)] for i in range(1, N + 1)])
        Qh = Q.copy()
        np.fill_diagonal(Qh, 0.0)
        self.assertLess(float(np.linalg.eigvalsh(Qh)[0]), -0.5)

    def test_uniform_pair_floor(self):
        # R > -1/sqrt(pq) >= -1/sqrt(6)
        bound = -1 / 6**0.5
        for p, q in [(2, 3), (3, 5), (5, 7), (11, 13)]:
            R = 0.5 * (1 / p**2 + 1 / q**2) - 1 / (p * q) ** 0.5
            self.assertGreater(R, -1 / (p * q) ** 0.5 - 1e-12)
            self.assertGreater(R, bound - 1e-12)


if __name__ == "__main__":
    unittest.main()
