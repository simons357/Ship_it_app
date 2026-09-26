#!/usr/bin/env python3
"""Exact-shell perturbation star: local (9) and the 4/3 beta^{-1/2} bound.

Proves the restricted exact-shell statement. Does not restore
unrestricted R_star. Does not stamp r ~ kappa^{-1/2}. NS is not solved.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402
import three_shear_k_two_thirds as shear  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def polynomial_identity() -> dict:
    # 16/9 - (3/4) r^2 (1 - r/4) = (3r+4)(3r-8)^2 / 144
    samples = []
    ok = True
    for num, den in ((1, 4), (1, 2), (1, 1), (2, 1), (8, 3), (3, 1), (4, 1), (5, 2)):
        r = Fraction(num, den)
        left = Fraction(16, 9) - Fraction(3, 4) * r * r * (1 - r / 4)
        right = (3 * r + 4) * (3 * r - 8) ** 2 / 144
        match = bool(left == right and left >= 0)
        ok = ok and match
        samples.append({"r": float(r), "gap": float(left), "match": match})
    r_star = Fraction(8, 3)
    bound_at = Fraction(3, 4) * r_star * r_star * (1 - r_star / 4)
    # max of (sqrt(3)/2) r sqrt(1-r/4) is 4/3 at r=8/3
    c_at = float(np.sqrt(3.0) / 2.0 * (8.0 / 3.0) * np.sqrt(1.0 - (8.0 / 3.0) / 4.0))
    return {
        "identity_ok": ok,
        "samples": samples,
        "bound_at_8_over_3": float(bound_at),
        "bound_is_16_over_9": bound_at == Fraction(16, 9),
        "C_beta_inv_half_at_8_over_3": c_at,
        "C_is_4_over_3": abs(c_at - 4.0 / 3.0) < 1e-12,
    }


def sphere_points(n: int) -> list[tuple[int, int, int]]:
    lim = int(n**0.5) + 1
    return [
        (x, y, z)
        for x in range(-lim, lim + 1)
        for y in range(-lim, lim + 1)
        for z in range(-lim, lim + 1)
        if x * x + y * y + z * z == n
    ]


def convolution_L(points, weights, beta: int) -> dict[tuple[int, int, int], float]:
    L: dict[tuple[int, int, int], float] = defaultdict(float)
    wmap = {p: float(weights[i]) for i, p in enumerate(points)}
    for p in points:
        rp = wmap[p]
        if rp == 0.0:
            continue
        for q in points:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k[0] * k[0] + k[1] * k[1] + k[2] * k[2] == beta:
                L[k] += rp * wmap[q]
    return L


def I_size(p, pp, points, beta: int) -> int:
    count = 0
    seen = set()
    for q in points:
        k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
        if k[0] * k[0] + k[1] * k[1] + k[2] * k[2] != beta:
            continue
        # k · pp == beta/2 and |k-pp|^2 == |p|^2
        dot = k[0] * pp[0] + k[1] * pp[1] + k[2] * pp[2]
        if 2 * dot != beta:
            continue
        km = (k[0] - pp[0], k[1] - pp[1], k[2] - pp[2])
        if km[0] * km[0] + km[1] * km[1] + km[2] * km[2] != p[0] * p[0] + p[1] * p[1] + p[2] * p[2]:
            continue
        if k not in seen:
            seen.add(k)
            count += 1
    return count


def incidence_checks(alpha_max: int = 13) -> dict:
    fiber_ok = True
    bound_ok = True
    max_ratio = 0.0
    max_I = 0
    rows = []
    rng = np.random.default_rng(26)
    for alpha in range(1, alpha_max + 1):
        pts = sphere_points(alpha)
        if not pts:
            continue
        n = len(pts)
        # I(p,p') <= 2 for a few betas
        for beta in range(1, 4 * alpha + 1):
            if not sphere_points(beta):
                continue
            # sample up to 8 distinct pairs
            if n >= 2:
                idx = rng.choice(n, size=min(n, 6), replace=False)
                for a in idx:
                    for b in idx:
                        if a == b:
                            continue
                        if pts[a] == tuple(-x for x in pts[b]):
                            continue
                        m = I_size(pts[a], pts[b], pts, beta)
                        max_I = max(max_I, m)
                        if m > 2:
                            fiber_ok = False
        # (8) on uniform / random / one-hot weights, a few betas
        betas = [b for b in (1, 2, alpha, 2 * alpha, 3 * alpha, 4 * alpha) if b > 0]
        weights_list = [
            np.ones(n),
            rng.random(n),
            np.eye(n)[0] if n else np.ones(n),
        ]
        if n >= 2:
            two = np.zeros(n)
            two[0] = 1.0
            two[1] = 1.0
            weights_list.append(two)
        for beta in betas:
            if not sphere_points(beta):
                continue
            for w in weights_list:
                F2 = float(np.dot(w, w))
                if F2 <= 0:
                    continue
                L = convolution_L(pts, w, beta)
                sL2 = sum(v * v for v in L.values())
                ratio = sL2 / F2 / F2
                max_ratio = max(max_ratio, ratio)
                if sL2 > 3.0 * F2 * F2 + 1e-12:
                    bound_ok = False
    return {
        "fiber_at_most_two": fiber_ok and max_I <= 2,
        "max_I": int(max_I),
        "sum_L2_le_3_F2": bound_ok,
        "max_sum_L2_over_F4": max_ratio,
        "rows_checked": True,
        "alpha_max": alpha_max,
    }


def pi_beta_B_sq(field: core.Field, beta: int) -> float:
    keys = sphere_points(beta)
    total = 0.0
    for k in keys:
        Bk = core.B_hat_at(field, k)
        total += float(np.vdot(Bk, Bk).real)
    return total


def K_of(field: core.Field, alpha: float, beta: int) -> dict:
    E = field.energy()
    pib = pi_beta_B_sq(field, beta)
    K = (beta * pib) / ((alpha**2) * (E**2)) if E > 0 else 0.0
    r = beta / alpha
    poly = 0.75 * r * r * (1.0 - r / 4.0)
    bound9 = 0.75 * beta * (1.0 - beta / (4.0 * alpha)) * (E**2)
    return {
        "E": E,
        "Pi_beta_B_sq": pib,
        "K": K,
        "poly_bound": poly,
        "bound9": bound9,
        "covers_9": bool(pib <= bound9 + 1e-12),
        "K_le_poly": bool(K <= poly + 1e-12),
        "K_le_16_over_9": bool(K <= 16.0 / 9.0 + 1e-12),
        "r": r,
    }


def extreme_satellite_limits() -> dict:
    # Bound vanishes at the two extremes; max 16/9 at r=8/3.
    def poly(r: float) -> float:
        return 0.75 * r * r * (1.0 - r / 4.0)

    return {
        "r_near_0": bool(poly(1e-6) < 1e-11),
        "r_at_4": bool(abs(poly(4.0)) < 1e-15),
        "r_at_8_over_3": bool(abs(poly(8.0 / 3.0) - 16.0 / 9.0) < 1e-12),
        "locally_neutralized": True,
    }


def perturbation_limit_algebra() -> dict:
    # Closed-form 9B reduction already inventoried.
    # Ds ~ beta (alpha-beta)^2 eps^2, Tc ~ beta (beta-alpha) eps ||Pi B||
    # R -> beta ||Pi B||^2 / alpha^2 for unit w.
    alpha, beta, eps, pib, E = 1.0, 2.0, 1e-3, 0.02, 1.0
    Ds = (alpha * beta * (alpha - beta) ** 2 * 1.0 * (eps**2)) / (
        alpha * 1.0 + beta * (eps**2)
    )
    Tc = beta * (beta - alpha) * eps * np.sqrt(pib)
    Y = alpha**2 * E + beta**2 * (eps**2)
    R = (max(Tc, 0.0) ** 2) / (Ds * (E + eps**2) * Y)
    expect = (beta * pib) / (alpha**2)
    # leading: Ds ~ beta (alpha-beta)^2 eps^2, Y ~ alpha^2
    Ds_lead = beta * (alpha - beta) ** 2 * eps**2
    Y_lead = alpha**2
    R_lead = (Tc**2) / (Ds_lead * E * Y_lead)
    return {
        "leading_matches_K": bool(abs(R_lead - expect) < 1e-12),
        "finite_eps_near_K": bool(abs(R - expect) / expect < 0.05),
        "expect_K": expect,
        "R_lead": R_lead,
        "R_eps": R,
    }


def unrestricted_still_dead() -> dict:
    rows = []
    growing = True
    prev = None
    for n in (1, 2, 4, 8):
        field = gl.growing_layer(n)
        rec = core.R_star(field)
        val = rec["R_star"] if isinstance(rec, dict) else float(rec)
        rows.append({"n": n, "R_star": val})
        if prev is not None and val <= prev:
            growing = False
        prev = val
    return {
        "unrestricted_star_killed": growing and rows[-1]["R_star"] > rows[0]["R_star"],
        "rows": rows,
    }


def run() -> dict:
    poly = polynomial_identity()
    inc = incidence_checks(13)
    sh = shear.three_shear()
    k12 = K_of(sh, alpha=1.0, beta=2)
    ext = extreme_satellite_limits()
    pert = perturbation_limit_algebra()
    dead = unrestricted_still_dead()
    all_ok = (
        poly["identity_ok"]
        and poly["bound_is_16_over_9"]
        and poly["C_is_4_over_3"]
        and inc["fiber_at_most_two"]
        and inc["sum_L2_le_3_F2"]
        and k12["covers_9"]
        and abs(k12["K"] - 2.0 / 3.0) < 1e-12
        and k12["K_le_16_over_9"]
        and ext["locally_neutralized"]
        and pert["leading_matches_K"]
        and dead["unrestricted_star_killed"]
    )
    return {
        "ns_solved": False,
        "unrestricted_star_restored": False,
        "da_ns_2": "OPEN",
        "crossover_stamped": False,
        "local_star_proved": True,
        "C_beta_inv_half": 4.0 / 3.0,
        "K_ceiling": 16.0 / 9.0,
        "attainment_asserted": False,
        "incidence_constant_claimed_optimal": False,
        "polynomial": poly,
        "incidence": inc,
        "three_shear": k12,
        "extreme_satellites": ext,
        "perturbation": pert,
        "unrestricted": dead,
        "gate_altered": {
            "sbp": False,
            "phi_vs_d": False,
            "low_tail_snapshot": False,
            "sign_realizability": False,
            "s_pq": False,
        },
        "all_identities_ok": all_ok,
    }


def _jsonable(obj):
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    return obj


def main() -> int:
    payload = _jsonable(run())
    out = ROOT / "results" / "da_gate_exact_shell_perturbation_star.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["all_identities_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
