"""Numerical stress test of SCHEME B target (B1): |T_sc| /?≤ C X√Y.

Builds synthetic divergence-free Fourier fields on exact shells,
assembles scalene signed transfer T_sc via (7), and records the ratio
|T_sc|/(X√Y). Not a proof. Standard library only.
"""
from __future__ import annotations

from itertools import combinations
from math import isqrt, sqrt
from pathlib import Path
import json
import random


def radius(k):
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def lattice_shell(r2: int):
    R = isqrt(r2) + 1
    return [
        (x, y, z)
        for x in range(-R, R + 1)
        for y in range(-R, R + 1)
        for z in range(-R, R + 1)
        if x * x + y * y + z * z == r2
    ]


def orthonormal_perp(k):
    """Two real orthonormal vectors ⊥ k (for building div-free modes)."""
    kx, ky, kz = k
    # pick a vector not parallel to k
    if abs(kx) + abs(ky) < 1e-15:
        a = (1.0, 0.0, 0.0)
    else:
        a = (-ky, kx, 0.0)
    na = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
    e1 = (a[0] / na, a[1] / na, a[2] / na)
    # e2 = k × e1
    e2 = (
        ky * e1[2] - kz * e1[1],
        kz * e1[0] - kx * e1[2],
        kx * e1[1] - ky * e1[0],
    )
    n2 = sqrt(e2[0] * e2[0] + e2[1] * e2[1] + e2[2] * e2[2])
    e2 = (e2[0] / n2, e2[1] / n2, e2[2] / n2)
    return e1, e2


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def scalene_shapes(shells, rmax):
    shapes = []
    for a, b, c in combinations(range(1, rmax + 1), 3):
        if a not in shells or b not in shells or c not in shells:
            continue
        sa, sb, sc = sqrt(a), sqrt(b), sqrt(c)
        if not (abs(sa - sb) <= sc <= sa + sb):
            continue
        if not (abs(sa - sc) <= sb <= sa + sc):
            continue
        if not (abs(sb - sc) <= sa <= sb + sc):
            continue
        for p in shells[a]:
            for q in shells[b]:
                r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
                if radius(r) == c:
                    shapes.append((a, b, c))
                    break
            else:
                continue
            break
    return shapes


def build_field(shells, active, rng, amp_law):
    """Map mode -> complex coeff as 3-vector; enforce u_{-k}=conj u_k, k·u=0.

    Real representation: store real+imag parts via two perp polarizations.
    We use purely imaginary Hermitian subspace (real-odd velocity): u_k = i v_k
    with v_k real, v_{-k}=-v_k (so u_{-k}=conj u_k).
    """
    u = {}  # k -> (ux,uy,uz) as complex triples stored as real imag-only: i*v
    for a in active:
        pts = shells[a]
        # process pairs ± together
        seen = set()
        for p in pts:
            if p in seen:
                continue
            mp = (-p[0], -p[1], -p[2])
            seen.add(p)
            seen.add(mp)
            e1, e2 = orthonormal_perp(p)
            # amplitude scale
            amp = amp_law(a, rng)
            th = rng.random() * 2 * 3.141592653589793
            # real vector v_p in plane ⊥ p
            vx = amp * (cos := __import__("math").cos(th)) * e1[0] + amp * (
                sin := __import__("math").sin(th)
            ) * e2[0]
            vy = amp * cos * e1[1] + amp * sin * e2[1]
            vz = amp * cos * e1[2] + amp * sin * e2[2]
            # optional second random mix
            th2 = rng.random() * 2 * 3.141592653589793
            amp2 = amp * (0.3 + 0.7 * rng.random())
            vx += amp2 * __import__("math").cos(th2) * e2[0]
            vy += amp2 * __import__("math").cos(th2) * e2[1]
            vz += amp2 * __import__("math").cos(th2) * e2[2]
            v = (vx, vy, vz)
            # u_p = i v, u_{-p} = -i v = conj(i v) if v real... wait
            # u_{-p} should be conj(u_p). If u_p = i v with v real, conj = -i v,
            # so u_{-p} = -i v, hence v_{-p} for u=i v_{-p} gives v_{-p}=-v.
            u[p] = (1j * v[0], 1j * v[1], 1j * v[2])
            if mp != p:
                u[mp] = (-1j * v[0], -1j * v[1], -1j * v[2])
    return u


def moments(u):
    E = X = Y = 0.0
    for k, uk in u.items():
        a = radius(k)
        ek = abs(uk[0]) ** 2 + abs(uk[1]) ** 2 + abs(uk[2]) ** 2
        E += ek
        X += a * ek
        Y += (a * a) * ek
    return E, X, Y


def T_abc(u, shells, a, b, c):
    """Signed block transfer (7) with I_p, I_q, I_r."""
    Ip = Iq = Ir = 0.0
    for p in shells[a]:
        up = u.get(p)
        if up is None:
            continue
        for q in shells[b]:
            uq = u.get(q)
            if uq is None:
                continue
            r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
            if radius(r) != c:
                continue
            ur = u.get(r)
            if ur is None:
                continue
            # Im[(q·u_p)(u_q·u_r)]
            q_dot_up = q[0] * up[0] + q[1] * up[1] + q[2] * up[2]
            uq_dot_ur = uq[0] * ur[0] + uq[1] * ur[1] + uq[2] * ur[2]
            mono = q_dot_up * uq_dot_ur
            Ip += mono.imag
            # cyclic I_q: Im[(r·u_q)(u_r·u_p)]
            r_dot_uq = r[0] * uq[0] + r[1] * uq[1] + r[2] * uq[2]
            ur_dot_up = ur[0] * up[0] + ur[1] * up[1] + ur[2] * up[2]
            Iq += (r_dot_uq * ur_dot_up).imag
            # I_r: Im[(p·u_r)(u_p·u_q)]
            p_dot_ur = p[0] * ur[0] + p[1] * ur[1] + p[2] * ur[2]
            up_dot_uq = up[0] * uq[0] + up[1] * uq[1] + up[2] * uq[2]
            Ir += (p_dot_ur * up_dot_uq).imag
    return (c - b) * Ip + (a - c) * Iq + (b - a) * Ir


def T_sc(u, shells, shapes):
    return sum(T_abc(u, shells, a, b, c) for a, b, c in shapes)


def run_trials(rmax=12, n_trials=24, seed=20261006):
    shells = {r: lattice_shell(r) for r in range(1, rmax + 1)}
    # drop empty (none) 
    shapes = scalene_shapes(shells, rmax)
    rng = random.Random(seed)
    results = []

    def amp_flat(a, rng):
        return rng.uniform(0.2, 1.0) / sqrt(len(shells[a]))

    def amp_decay(a, rng):
        return rng.uniform(0.2, 1.0) / (a * sqrt(len(shells[a])))

    def amp_high(a, rng):
        # emphasize higher shells
        return rng.uniform(0.2, 1.0) * sqrt(a) / sqrt(len(shells[a]))

    laws = [("flat", amp_flat), ("decay_1_a", amp_decay), ("emphasize_high", amp_high)]
    active_sets = [
        ("all", list(range(1, rmax + 1))),
        ("S4_plus", [5, 8, 10, 13, 14, 17, 18, 20, 25][: min(9, rmax)]),
        ("no_low", list(range(3, rmax + 1))),
    ]
    # filter active shells that exist and ≤ rmax
    active_sets = [
        (name, [a for a in acts if 1 <= a <= rmax and shells[a]])
        for name, acts in active_sets
    ]

    ratios = []
    for law_name, law in laws:
        for act_name, active in active_sets:
            for t in range(n_trials):
                u = build_field(shells, active, rng, law)
                E, X, Y = moments(u)
                if X <= 1e-15 or Y <= 1e-15:
                    continue
                # only shapes fully inside active shells
                sh = [s for s in shapes if s[0] in active and s[1] in active and s[2] in active]
                tsc = T_sc(u, shells, sh)
                denom = X * sqrt(Y)
                ratio = abs(tsc) / denom
                ratios.append(ratio)
                results.append(
                    {
                        "law": law_name,
                        "active": act_name,
                        "trial": t,
                        "E": E,
                        "X": X,
                        "Y": Y,
                        "T_sc": tsc,
                        "abs_T_sc_over_X_sqrtY": ratio,
                        "n_shapes_used": len(sh),
                    }
                )

    ratios_sorted = sorted(ratios)
    summary = {
        "rmax": rmax,
        "n_shapes_total": len(shapes),
        "n_samples": len(ratios),
        "ratio_max": max(ratios) if ratios else None,
        "ratio_p95": ratios_sorted[int(0.95 * (len(ratios_sorted) - 1))] if ratios else None,
        "ratio_median": ratios_sorted[len(ratios_sorted) // 2] if ratios else None,
        "ratio_mean": sum(ratios) / len(ratios) if ratios else None,
        "rep_constant_in_11": sqrt(3) / 2,
        "reading": (
            "If ratio_max stays O(1) across laws/supports, (B1) is numerically "
            "plausible with C_star on the order of a few units (compare √3/2≈0.866 "
            "for repeated radius). If ratio grows with rmax, (B1) needs weights "
            "beyond X√Y or is false."
        ),
    }
    return summary, results


def main():
    s12, _ = run_trials(rmax=12, n_trials=16)
    s16, samples = run_trials(rmax=16, n_trials=12)
    out = {
        "target": "|T_sc| ≤ C_star X √Y  (SCHEME B / B1)",
        "terminology": "shell = exact |k|^2; not physical",
        "runs": [s12, s16],
        "growth_ratio_max_12_to_16": (
            None
            if not s12["ratio_max"] or not s16["ratio_max"]
            else s16["ratio_max"] / s12["ratio_max"]
        ),
        "sample_peak": max(samples, key=lambda d: d["abs_T_sc_over_X_sqrtY"]) if samples else None,
        "status": "NUMERICAL probe of (B1); not a proof of (17)",
    }
    path = Path(__file__).with_name("SCHEME-B-B1-RATIO-PROBE.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
