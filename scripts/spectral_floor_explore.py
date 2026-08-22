#!/usr/bin/env python3
"""
Restricted / renormalized spectral-floor checks for inverse-GCD matrices.

This does not restore the withdrawn claim λ_min > -1/2 on the full space.
It records which restricted Rayleigh statements still sit above -1/2, and
whether the known counterexample modes are concentrated.

Matrices (1-based indices i,j = 1..N):
  Q(i,j)      = 1/gcd(i,j)
  Qtilde(i,j) = 1/(gcd(i,j) sqrt(i j))
  H           = D^{-1/2} Qtilde D^{-1/2},  D_ii = row-sum of Qtilde
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


def gcd_matrix(n: int) -> np.ndarray:
    g = np.zeros((n, n), dtype=np.int64)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            g[i - 1, j - 1] = math.gcd(i, j)
    return g


def raw_q(n: int) -> np.ndarray:
    return 1.0 / gcd_matrix(n).astype(float)


def qtilde(n: int) -> np.ndarray:
    idx = np.arange(1, n + 1, dtype=float)
    return raw_q(n) / np.sqrt(np.outer(idx, idx))


def h_matrix(qt: np.ndarray) -> np.ndarray:
    d = qt.sum(axis=1)
    d = np.maximum(d, 1e-18)
    s = 1.0 / np.sqrt(d)
    return (s[:, None]) * qt * (s[None, :])


def primes_upto(n: int) -> list[int]:
    if n < 2:
        return []
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = False
    return [int(i) for i in range(2, n + 1) if sieve[i]]


def lambda_min(a: np.ndarray) -> tuple[float, np.ndarray]:
    evals, evecs = np.linalg.eigh(a)
    return float(evals[0]), evecs[:, 0]


def rayleigh(a: np.ndarray, v: np.ndarray) -> float:
    nrm = float(np.dot(v, v))
    if nrm <= 0.0:
        return float("nan")
    return float(v @ a @ v / nrm)


def ipr(v: np.ndarray) -> float:
    nrm = float(np.dot(v, v))
    if nrm <= 0.0:
        return float("nan")
    u = v / math.sqrt(nrm)
    return float(np.sum(u**4))


def support_mass(v: np.ndarray, frac: float = 0.9) -> int:
    """Smallest number of coordinates carrying `frac` of l2 mass."""
    w = np.abs(v) ** 2
    s = float(w.sum())
    if s <= 0.0:
        return 0
    order = np.sort(w)[::-1]
    c = np.cumsum(order)
    return int(np.searchsorted(c, frac * s) + 1)


def principal(a: np.ndarray, idx: list[int]) -> np.ndarray:
    if not idx:
        return np.zeros((0, 0))
    ii = np.array(idx, dtype=int)
    return a[np.ix_(ii, ii)]


def mean_zero_min(a: np.ndarray) -> float:
    n = a.shape[0]
    p = np.eye(n) - np.ones((n, n)) / n
    b = p @ a @ p
    evals = np.linalg.eigvalsh(b)
    # One eigenvalue is numerically 0 (all-ones kernel). Take the smallest
    # among those that are not that kernel mode.
    evals = np.sort(evals)
    return float(evals[0] if abs(evals[0]) > 1e-10 else evals[1])


def bridge_star_values(n: int) -> list[float]:
    ps = primes_upto(n)
    out = []
    for i, p in enumerate(ps):
        for q in ps[i + 1 :]:
            r = 0.5 * (1.0 / p**2 + 1.0 / q**2) - 1.0 / math.sqrt(p * q)
            out.append(r)
    return out


def multi_rep_min(qt: np.ndarray, n: int) -> tuple[float, int | None]:
    prime_set = set(primes_upto(n))
    best = float("inf")
    best_k = None
    for k in range(4, n + 1, 2):
        reps = [p for p in prime_set if p <= k / 2 and (k - p) in prime_set]
        if len(reps) < 1:
            continue
        v = np.zeros(n)
        for p in reps:
            v[p - 1] += 1.0
            v[k - p - 1] -= 1.0
        if np.dot(v, v) <= 0.0:
            continue
        r = rayleigh(qt, v)
        if r < best:
            best = r
            best_k = k
    if best_k is None:
        return float("nan"), None
    return float(best), best_k


def random_spread_min(a: np.ndarray, trials: int, rng: np.random.Generator) -> float:
    """Monte Carlo lower envelope of Rayleigh on delocalized Gaussian vectors."""
    n = a.shape[0]
    best = float("inf")
    for _ in range(trials):
        v = rng.standard_normal(n)
        v -= v.mean()
        r = rayleigh(a, v)
        if r < best:
            best = r
    return float(best)


def clipped_minimizer_rayleigh(a: np.ndarray, v: np.ndarray, cap: float) -> float:
    """Rayleigh of the λ_min mode after clipping ||v||_∞ / ||v||_2 ≤ cap."""
    nrm = math.sqrt(float(np.dot(v, v)))
    if nrm <= 0.0:
        return float("nan")
    u = v / nrm
    u = np.clip(u, -cap, cap)
    return rayleigh(a, u)


@dataclass
class Row:
    n: int
    q_min: float
    qt_min: float
    h_min: float
    q_min_over_log: float
    qt_min_over_log: float
    h_min_over_log: float
    qt_ipr: float
    qt_support90: int
    qt_prime_min: float
    qt_composite_min: float
    qt_mean_zero_min: float
    bridge_star_min: float
    multi_rep_min: float
    multi_rep_k: int | None
    qt_spread_mc: float
    qt_clipped_min: float


def analyze(n: int, rng: np.random.Generator, mc: int) -> Row:
    q = raw_q(n)
    qt = qtilde(n)
    h = h_matrix(qt)
    qmin, _ = lambda_min(q)
    qtmin, qtvec = lambda_min(qt)
    hmin, _ = lambda_min(h)
    logn = math.log(n)

    ps = primes_upto(n)
    prime_idx = [p - 1 for p in ps]
    comp_idx = [i for i in range(n) if (i + 1) not in set(ps)]
    qt_p = principal(qt, prime_idx)
    qt_c = principal(qt, comp_idx)
    pmin = float(np.linalg.eigvalsh(qt_p)[0]) if qt_p.size else float("nan")
    cmin = float(np.linalg.eigvalsh(qt_c)[0]) if qt_c.size else float("nan")

    bs = bridge_star_values(n)
    mr, mrk = multi_rep_min(qt, n)

    return Row(
        n=n,
        q_min=qmin,
        qt_min=qtmin,
        h_min=hmin,
        q_min_over_log=qmin / logn,
        qt_min_over_log=qtmin / logn,
        h_min_over_log=hmin / logn,
        qt_ipr=ipr(qtvec),
        qt_support90=support_mass(qtvec, 0.9),
        qt_prime_min=pmin,
        qt_composite_min=cmin,
        qt_mean_zero_min=mean_zero_min(qt),
        bridge_star_min=min(bs) if bs else float("nan"),
        multi_rep_min=mr,
        multi_rep_k=mrk,
        qt_spread_mc=random_spread_min(qt, mc, rng),
        qt_clipped_min=clipped_minimizer_rayleigh(qt, qtvec, cap=2.0 / math.sqrt(n)),
    )


def prime_subspace_min(n: int) -> float:
    """λ_min of Q̃ restricted to prime indices. Algebra: ≥ -1/4."""
    qt = qtilde(n)
    idx = [p - 1 for p in primes_upto(n)]
    block = principal(qt, idx)
    if block.size == 0:
        return float("nan")
    return float(np.linalg.eigvalsh(block)[0])


def certificates() -> dict:
    q10, _ = lambda_min(raw_q(10))
    qt20, _ = lambda_min(qtilde(20))
    return {
        "q10_min": q10,
        "q10_below_half": q10 < -0.5,
        "qt20_min": qt20,
        "qt20_below_half": qt20 < -0.5,
        "bridge_star_23": 0.5 * (1 / 4 + 1 / 9) - 1 / math.sqrt(6),
        "prime_subspace_80": prime_subspace_min(80),
        "prime_subspace_ge_minus_quarter": prime_subspace_min(80) >= -0.25 - 1e-12,
        "h4_min": lambda_min(h_matrix(qtilde(4)))[0],
        "h_floor_minus_one": lambda_min(h_matrix(qtilde(4)))[0] >= -1.0,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Restricted inverse-GCD spectral-floor scan")
    p.add_argument("--nmax", type=int, default=80)
    p.add_argument("--mc", type=int, default=400)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--out", type=Path, default=Path("results/spectral_floor_explore.json"))
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    ns = [10, 20, 30, 40, 60]
    ns = [n for n in ns if n <= args.nmax]
    if args.nmax not in ns:
        ns.append(args.nmax)

    rows = [asdict(analyze(n, rng, args.mc)) for n in ns]
    cert = certificates()

    def above_half(key: str) -> bool:
        vals = [r[key] for r in rows if isinstance(r[key], (int, float)) and math.isfinite(r[key])]
        return bool(vals) and min(vals) > -0.5

    payload = {
        "meta": {
            "note": (
                "Full-spectrum λ_min > -1/2 is false. This scan asks which "
                "restricted / renormalized statements still sit above -1/2."
            ),
            "nmax": args.nmax,
            "mc": args.mc,
        },
        "certificates": cert,
        "rows": rows,
        "live_restricted": {
            "bridge_star_pairs": above_half("bridge_star_min"),
            "multi_rep": above_half("multi_rep_min"),
            "prime_principal_qt": above_half("qt_prime_min"),
            "composite_principal_qt": above_half("qt_composite_min"),
            "mean_zero_qt": above_half("qt_mean_zero_min"),
            "spread_mc_qt": above_half("qt_spread_mc"),
            "clipped_minimizer_qt": above_half("qt_clipped_min"),
            "full_qt": above_half("qt_min"),
            "full_h": above_half("h_min"),
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))

    print(
        f"{'N':>4} {'Qmin':>9} {'Qtmin':>9} {'Hmin':>9} {'Qt/log':>8} "
        f"{'IPR':>6} {'s90':>4} {'prime':>9} {'comp':>9} {'mz':>9} "
        f"{'B*':>8} {'mrep':>8} {'spread':>8} {'clip':>8}"
    )
    for r in rows:
        print(
            f"{r['n']:4d} {r['q_min']:9.4f} {r['qt_min']:9.4f} {r['h_min']:9.4f} "
            f"{r['qt_min_over_log']:8.4f} {r['qt_ipr']:6.3f} {r['qt_support90']:4d} "
            f"{r['qt_prime_min']:9.4f} {r['qt_composite_min']:9.4f} {r['qt_mean_zero_min']:9.4f} "
            f"{r['bridge_star_min']:8.4f} {r['multi_rep_min']:8.4f} "
            f"{r['qt_spread_mc']:8.4f} {r['qt_clipped_min']:8.4f}"
        )
    print("certificates", json.dumps(cert, indent=2))
    print("live_restricted", json.dumps(payload["live_restricted"], indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
