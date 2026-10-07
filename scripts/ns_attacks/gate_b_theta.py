#!/usr/bin/env python3
"""Gate B / Dish #3: global energy sharing and remaining frequency loss θ.

One Cauchy–Schwarz on ∑ f_x² = E. Gate A stays UNRESOLVED / DIAGNOSTIC ONLY.
Not (17). NS is not solved.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from math import log, sqrt

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.analytic_load_lower_bound import C_abc, subnet_stats
from ns_attacks.rho_formula_and_growth_probe import (
    B5,
    B13_PACKAGE,
    B9_ACTIVE,
    rho_anchor,
)


def rho_l1_l2(rhos: dict[int, float]) -> dict:
    vals = list(rhos.values())
    L = sum(vals)
    S2 = sum(r * r for r in vals)
    S = sqrt(S2)
    M = len(vals)
    return {
        "M": M,
        "L": L,
        "S": S,
        "S_le_L": S <= L + 1e-15,
        "L_le_sqrtM_S": L <= (sqrt(M) * S) + 1e-12 if M else True,
    }


def family_rho_vector() -> dict:
    rhos = {
        5: rho_anchor(5, B5, 25),
        9: rho_anchor(9, B9_ACTIVE, 25),
        13: rho_anchor(13, B13_PACKAGE, 25),
    }
    agg = rho_l1_l2(rhos)
    return {"rhos": rhos, **agg}


def subnet_l1_l2(n: int) -> dict:
    """ℓ¹ load L vs ℓ² assembly S on the z_n=2n² diagnostic subnet."""
    c = 2 * n * n
    # Rebuild per-anchor ρ from the same rectangle as analytic_load_lower_bound.
    from ns_attacks.analytic_load_lower_bound import collinear, delta

    k_lo = int(0.3 * n)
    k_hi = int(0.7 * n)
    ell_hi = int(0.4 * n)
    by_a: dict[int, list[float]] = defaultdict(list)
    for k in range(k_lo, k_hi + 1):
        for ell in range(0, ell_hi + 1):
            a = k * k + ell * ell
            b = n * n + (n - k) * (n - k) + ell * ell
            if not (a < b < c):
                continue
            if collinear(a, b, c) or delta(a, b, c) <= 0:
                continue
            t = C_abc(a, b, c) / b
            by_a[a].append(t)
    rhos = {
        a: (1.0 / (2 * c)) * sqrt(sum(t * t for t in ts)) for a, ts in by_a.items()
    }
    agg = rho_l1_l2(rhos)
    spine = subnet_stats(n)
    return {
        "n": n,
        "c": c,
        "Lambda_proxy": c,
        **agg,
        "A_subnet_full_rho": spine["A_subnet_full_rho"],
        "distinct_a": spine["distinct_a"],
    }


def theta_hat(row0: dict, row1: dict) -> float:
    """Effective power of c in S ~ c^θ. Λ ~ c on this diagnostic."""
    s0, s1 = row0["S"], row1["S"]
    c0, c1 = row0["c"], row1["c"]
    if s0 <= 0 or s1 <= 0:
        return float("nan")
    return log(s1 / s0) / log(c1 / c0)


def dish3_bound_factor(S: float) -> dict:
    """T_sc⁺ ≤ 2 S √E Y under Y-charge f_b ≤ √Y/b, f_c ≤ √Y/c, plus the C-majorant."""
    return {
        "prefactor": 2.0 * S,
        "form": "2 S sqrt(E) Y",
        "theta_if_S_bounded": 0.0,
    }


def report() -> dict:
    fam = family_rho_vector()
    ns = (20, 40, 80, 160)
    rows = [subnet_l1_l2(n) for n in ns]
    thetas = [
        {"from_n": rows[i]["n"], "to_n": rows[i + 1]["n"], "theta_hat": theta_hat(rows[i], rows[i + 1])}
        for i in range(len(rows) - 1)
    ]
    S_vals = [r["S"] for r in rows]
    L_vals = [r["L"] for r in rows]
    return {
        "families_c25": {
            "rhos": fam["rhos"],
            "L": fam["L"],
            "S": fam["S"],
            "M": fam["M"],
        },
        "subnet_diagnostic": {
            "rows": rows,
            "theta_hats": thetas,
            "L_grows": L_vals[-1] > L_vals[0] * 1.5,
            "S_stays_O1": max(S_vals) < 2.0 * min(S_vals) + 0.5,
            "mean_theta_hat": sum(t["theta_hat"] for t in thetas) / len(thetas),
        },
        "dish3": dish3_bound_factor(rows[-1]["S"]),
        "locks": {
            "gate_A": "UNRESOLVED / DIAGNOSTIC ONLY",
            "gate_A_not_open": True,
            "gate_A_not_failed": True,
            "gate_A_not_dead": True,
            "gate_B_active": True,
            "theta_proved": False,
            "theorem_17_proved": False,
            "not_a_close": True,
            "C_majorant_is_upper_bound": True,
            "general_c_allocation_not_sot": True,
            "no_infinite_divergent_cost": True,
            "no_novelty": True,
        },
    }


def main(argv=None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    payload = report()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
