"""Phase cancellation probe — fast targeted numerics.

1) Random independent triads → receiver shell (optimistic cancellation).
2) Shared-mode coherent search on a small overlapping family
   (shells {5,8,9,10,25} — jet blocks + (9,25) anchor), measuring
   |sum T_σ| / sum |T_σ|.

Not a proof. numpy only.
"""
from __future__ import annotations

from itertools import combinations
from math import isqrt, sqrt
from pathlib import Path
import json
import numpy as np


def radius(k):
    return int(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


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
    kx, ky, kz = (float(t) for t in k)
    if abs(kx) + abs(ky) < 1e-15:
        a = np.array([1.0, 0.0, 0.0])
    else:
        a = np.array([-ky, kx, 0.0])
    e1 = a / np.linalg.norm(a)
    e2 = np.cross(np.array([kx, ky, kz]), e1)
    e2 /= np.linalg.norm(e2)
    return e1, e2


def enumerate_shapes(shells, allowed):
    shapes = []
    for a, b, c in combinations(sorted(allowed), 3):
        sa, sb, sc = sqrt(a), sqrt(b), sqrt(c)
        if not (
            abs(sa - sb) <= sc <= sa + sb
            and abs(sa - sc) <= sb <= sa + sc
            and abs(sb - sc) <= sa <= sb + sc
        ):
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


def build_modes(shells, active):
    modes, seen = [], set()
    for a in active:
        for p in shells[a]:
            mp = (-p[0], -p[1], -p[2])
            key = tuple(sorted((p, mp)))
            if key in seen:
                continue
            seen.add(key)
            modes.append(p)
    return modes


def make_field(modes, phases, amps, pols):
    u = {}
    for p, ph, amp, pol in zip(modes, phases, amps, pols):
        mp = (-p[0], -p[1], -p[2])
        uk = 1j * amp * np.exp(1j * ph) * pol
        u[p] = (complex(uk[0]), complex(uk[1]), complex(uk[2]))
        if mp != p:
            u[mp] = (uk[0].conjugate(), uk[1].conjugate(), uk[2].conjugate())
    return u


def T_abc(u, shells, a, b, c):
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
            Ip += (q[0] * up[0] + q[1] * up[1] + q[2] * up[2]) * (
                uq[0] * ur[0] + uq[1] * ur[1] + uq[2] * ur[2]
            )
            Iq += (r[0] * uq[0] + r[1] * uq[1] + r[2] * uq[2]) * (
                ur[0] * up[0] + ur[1] * up[1] + ur[2] * up[2]
            )
            Ir += (p[0] * ur[0] + p[1] * ur[1] + p[2] * ur[2]) * (
                up[0] * uq[0] + up[1] * uq[1] + up[2] * uq[2]
            )
    return (c - b) * Ip.imag + (a - c) * Iq.imag + (b - a) * Ir.imag


def family_score(phases, modes, amps, pols, shells, shapes):
    u = make_field(modes, phases, amps, pols)
    ts = np.array([T_abc(u, shells, a, b, c) for a, b, c in shapes], float)
    abs_sum = float(np.sum(np.abs(ts)))
    signed = float(np.sum(ts))
    ratio = abs(signed) / abs_sum if abs_sum > 1e-30 else 0.0
    return signed, abs_sum, ratio, ts


def random_receiver_experiment(n_triads, rng, rmax=20, receiver=13):
    shells = {r: lattice_shell(r) for r in range(1, rmax + 1) if lattice_shell(r)}
    shell_of = {p: a for a, pts in shells.items() for p in pts}
    donors = []
    for p, a in shell_of.items():
        if a == receiver:
            continue
        for r in shells[receiver]:
            q = (r[0] - p[0], r[1] - p[1], r[2] - p[2])
            b = radius(q)
            if b == a or b == receiver or q not in shell_of:
                continue
            donors.append((p, q, r, b))
    abs_sum = signed_sum = 0.0
    for _ in range(n_triads):
        p, q, r, b = donors[int(rng.integers(0, len(donors)))]
        pols = []
        for k in (p, q, r):
            e1, e2 = orthonormal_perp(k)
            th = float(rng.uniform(0, 2 * np.pi))
            pols.append(np.cos(th) * e1 + np.sin(th) * e2)
        amps = rng.uniform(0.5, 1.5, size=3)
        ph = rng.uniform(0, 2 * np.pi, size=3)
        up = 1j * amps[0] * np.exp(1j * ph[0]) * pols[0]
        uq = 1j * amps[1] * np.exp(1j * ph[1]) * pols[1]
        ur = 1j * amps[2] * np.exp(1j * ph[2]) * pols[2]
        mono = np.dot(np.array(q, float), up) * np.dot(uq, ur)
        w = receiver - b
        abs_sum += abs(mono) * abs(w)
        signed_sum += mono.imag * w
    return {
        "n_triads": n_triads,
        "receiver_shell": receiver,
        "donor_pool_size": len(donors),
        "sum_abs": abs_sum,
        "sum_signed": signed_sum,
        "cancellation_ratio": abs(signed_sum) / abs_sum if abs_sum else None,
    }


def coherent_search(shells, shapes, rng, n_restarts=10, n_passes=4, grid=10):
    active = sorted({s for sh in shapes for s in sh})
    modes = build_modes(shells, active)
    n = len(modes)
    amps = np.array([1.0 / sqrt(max(len(shells[radius(p)]), 1)) for p in modes])
    pols = []
    for p in modes:
        e1, e2 = orthonormal_perp(p)
        th = float(rng.uniform(0, 2 * np.pi))
        pols.append(np.cos(th) * e1 + np.sin(th) * e2)

    best = {"ratio": -1.0}
    for restart in range(n_restarts):
        phases = rng.uniform(0, 2 * np.pi, size=n)
        signed, abs_sum, ratio, ts = family_score(
            phases, modes, amps, pols, shells, shapes
        )
        for _ in range(n_passes):
            improved = False
            for i in rng.permutation(n):
                best_abs_s, best_ph = abs(signed), phases[i]
                best_pack = (signed, abs_sum, ratio, ts)
                for trial in np.linspace(0, 2 * np.pi, grid, endpoint=False):
                    phases[i] = trial
                    s2, a2, r2, t2 = family_score(
                        phases, modes, amps, pols, shells, shapes
                    )
                    if abs(s2) > best_abs_s + 1e-14:
                        best_abs_s, best_ph = abs(s2), trial
                        best_pack = (s2, a2, r2, t2)
                        improved = True
                phases[i] = best_ph
                signed, abs_sum, ratio, ts = best_pack
            if not improved:
                break
        if ratio > best["ratio"]:
            best = {
                "ratio": ratio,
                "sum_signed": signed,
                "sum_abs": abs_sum,
                "restart": int(restart),
                "n_modes": n,
                "n_shapes": len(shapes),
                "max_abs_shape": float(np.max(np.abs(ts))) if len(ts) else 0.0,
            }

    rand_ratios = []
    for _ in range(40):
        phases = rng.uniform(0, 2 * np.pi, size=n)
        _, _, r, _ = family_score(phases, modes, amps, pols, shells, shapes)
        rand_ratios.append(r)

    return {
        "worst_case_coherent": best,
        "random_phase_baseline": {
            "ratio_mean": float(np.mean(rand_ratios)),
            "ratio_max": float(np.max(rand_ratios)),
            "ratio_median": float(np.median(rand_ratios)),
            "n_samples": len(rand_ratios),
        },
        "active_shells": active,
        "shapes": shapes,
    }


def main():
    rng = np.random.default_rng(20261006)

    # §2 optimistic experiment
    random_recv = random_receiver_experiment(500, rng, rmax=18, receiver=13)

    # Shared-mode family: compact shells including jet + (9,25)
    allowed = [5, 8, 9, 10, 25]
    shells = {r: lattice_shell(r) for r in allowed}
    shapes = enumerate_shapes(shells, allowed)
    coherent = coherent_search(shells, shapes, rng)

    # Shell-phase toy on synthetic 32 channels (shared phase per shell label 0..S-1)
    # Models: T_σ = cos(φ_{a}+φ_{b}+φ_{c}) for 32 random triples on S shells with overlap
    S, n_shapes = 12, 32
    # build triples with controlled overlap (each shell in ~ multiplicity 4 style)
    triples = []
    shells_ids = list(range(S))
    # repeat combinations to get 32 with reuse
    combos = list(combinations(shells_ids, 3))
    rng.shuffle(combos)
    while len(triples) < n_shapes:
        for c in combos:
            triples.append(c)
            if len(triples) >= n_shapes:
                break

    def shell_phase_ratio(phases):
        ts = np.array([np.cos(phases[a] + phases[b] + phases[c]) for a, b, c in triples])
        abs_sum = float(np.sum(np.abs(ts)))
        signed = float(np.sum(ts))
        return abs(signed) / abs_sum if abs_sum else 0.0, signed, abs_sum

    toy_best = 0.0
    for _ in range(30):
        ph = rng.uniform(0, 2 * np.pi, size=S)
        for _pass in range(8):
            for i in range(S):
                best_r, best_ph = shell_phase_ratio(ph)[0], ph[i]
                for trial in np.linspace(0, 2 * np.pi, 16, endpoint=False):
                    ph[i] = trial
                    r = shell_phase_ratio(ph)[0]
                    if r > best_r:
                        best_r, best_ph = r, trial
                ph[i] = best_ph
        toy_best = max(toy_best, shell_phase_ratio(ph)[0])
    toy_rand = [shell_phase_ratio(rng.uniform(0, 2 * np.pi, size=S))[0] for _ in range(100)]

    out = {
        "terminology": "shell = exact |k|^2; not physical",
        "author_random_triad_reference": {
            "n_triads": 500,
            "sum_abs_approx": 3468,
            "sum_signed_approx": -4.3,
            "cancellation_ratio_approx": 0.0012,
        },
        "random_receiver_experiment": random_recv,
        "shared_mode_family_compact": {
            "note": (
                "Exact 32-list awaits ZIP; compact mode-level family on "
                "{5,8,9,10,25} including jet blocks and (9,25) anchor shells"
            ),
            **coherent,
        },
        "shell_phase_toy_32": {
            "note": (
                "Synthetic 32 triples on 12 shell labels with shared shell "
                "phases — models overlap constraint without full lattice"
            ),
            "n_shapes": n_shapes,
            "n_shell_labels": S,
            "worst_case_ratio": toy_best,
            "random_ratio_mean": float(np.mean(toy_rand)),
            "random_ratio_max": float(np.max(toy_rand)),
        },
        "reading": {
            "single_triad": "no worst-case phase gain",
            "random_independent": "strong cancellation (optimistic)",
            "shared_mode": (
                "compare worst_case_coherent.ratio to random baseline; "
                "if O(1), shared phases destroy the 0.0012 regime"
            ),
            "next": "signed multi-shape lemma guided by measured coherent ratio",
        },
        "status": "NUMERICAL exploration; not a proof of (17)",
    }
    path = Path(__file__).with_name("PHASE-CANCELLATION-PROBE.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
