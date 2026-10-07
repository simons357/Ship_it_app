"""Analytic lower-bound sequence for Gate A load L_z = A(z).

Sequence: z_n = 2 n².
Subnet shapes from lattice vectors
  u=(k,0,ℓ), v=(n-k,n,-ℓ), w=(-n,-n,0)
with (k,ℓ) in a fixed positive-measure rectangle in the (θ,φ)=(k/n,ℓ/n) plane.

One-term bound: L*_n ≥ (κ/n) · #{distinct a=k²+ℓ² in the rectangle}.
Distinct sums of two squares in a Θ(n)×Θ(n) rectangle are
≍ n²/√(log n) (Landau–Ramanujan type), hence L*_n → ∞.

Not (17). Supports Gate A Outcome B.
"""
from __future__ import annotations

from collections import defaultdict
from math import sqrt, log
from pathlib import Path
import json


def delta(a, b, c) -> float:
    s = (c - a - b) / 2.0
    return a * b - s * s


def collinear(a, b, c) -> bool:
    return (b - a - c) ** 2 == 4 * a * c


def C_abc(a, b, c) -> float:
    d = delta(a, b, c)
    if d <= 0:
        return 0.0
    return sqrt(3 * d) * (
        abs(c - b) / sqrt(a) + abs(c - a) / sqrt(b) + abs(b - a) / sqrt(c)
    )


def subnet_stats(n: int) -> dict:
    c = 2 * n * n
    k_lo = int(0.3 * n)
    k_hi = int(0.7 * n)
    ell_hi = int(0.4 * n)
    by_a: dict[int, list[float]] = defaultdict(list)
    pairs = 0
    min_t_over_n = None
    for k in range(k_lo, k_hi + 1):
        for ell in range(0, ell_hi + 1):
            a = k * k + ell * ell
            b = n * n + (n - k) * (n - k) + ell * ell
            if not (a < b < c):
                continue
            if collinear(a, b, c) or delta(a, b, c) <= 0:
                continue
            t = C_abc(a, b, c) / b  # C/b
            by_a[a].append(t)
            pairs += 1
            tn = t / n
            min_t_over_n = tn if min_t_over_n is None else min(min_t_over_n, tn)

    # L*_n ≥ ∑_a (1/(2c)) max_b (C/b)
    A_lb = sum((1.0 / (2 * c)) * max(ts) for ts in by_a.values())
    A_full = sum(
        (1.0 / (2 * c)) * sqrt(sum(t * t for t in ts)) for ts in by_a.values()
    )
    n_a = len(by_a)
    return {
        "n": n,
        "z_n": c,
        "distinct_a": n_a,
        "pairs": pairs,
        "min_C_over_b_n": min_t_over_n,
        "A_lb_max_term": A_lb,
        "A_subnet_full_rho": A_full,
        "A_lb_over_n": A_lb / n,
        "distinct_a_over_n2": n_a / (n * n),
        "R_lb": A_lb / sqrt(c),
        # heuristic Landau–Ramanujan scale
        "n_over_sqrt_log": n / sqrt(log(n)) if n > 2 else None,
    }


def main():
    rows = [subnet_stats(n) for n in (20, 40, 80, 160, 320)]
    # Uniform κ from min over computed rows
    kappa = min(r["min_C_over_b_n"] for r in rows)
    payload = {
        "definition": {
            "L_z": "A(z)=∑_a ρ_a(z) under Convention F2",
            "z_n": "2 n²",
            "subnet": "u=(k,0,ℓ), v=(n-k,n,-ℓ), w=(-n,-n,0)",
            "rectangle": "k/n ∈ [0.3,0.7], ℓ/n ∈ [0,0.4]",
        },
        "analytic_spine": {
            "one_term": "L*_n ≥ (κ/n) · #{distinct a=k²+ℓ²}",
            "kappa_lower_from_rerun": kappa,
            "number_theory_input": (
                "#{distinct sums of two squares in a Θ(n)×Θ(n) rectangle} "
                "≍ n²/√(log n) (Landau–Ramanujan type)"
            ),
            "conclusion": "L*_n → ∞ along z_n=2n², hence L_{z_n}→∞",
        },
        "rows": rows,
        "gate_A": {
            "status": "CLOSED — Outcome B",
            "kill": "L_{z_n}→∞ along z_n=2n² (see docs/GATE-A-KILL-CERTIFICATE-2026-10-07.md)",
            "number_theory": "r_2(m)≪_ε m^ε ⇒ N_n ≫ n^{2-2ε} ⇒ L*_n ≫ n^{1-2ε}",
        },
        "status": "Gate A analytic kill support — Outcome B; not (17)",
    }
    path = Path(__file__).with_name("ANALYTIC-LOAD-LOWER-BOUND.json")
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
