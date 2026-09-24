#!/usr/bin/env python3
"""S measurement: unique three-wave transfer vs viscous amount.

The per-triangle kernel is labeling-invariant: all 6 permutations of a
distinct triad {k, p, q} with k+p+q=0 return the same value (checked
to ~13 decimals). The first measurement pass added each triangle once
for each labeling, so it counted every one 6 times.

Coherence is a ratio, so the 6× factor cancelled. S compares the
transfer to a viscous amount that was not multiplied by 6, so S was
inflated. Count each unordered triangle once.

Always print the numbers behind a zero S. A thresholded zero is not a
reason to hide transfer, viscous, or coherence.

Per-field β tables from the first (6×) run stay inconclusive until
this re-run. Classical NS stays open. This file produces measured
evidence, not a regularity proof.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np

from ns_solver_core import (
    VOL_T3,
    energy,
    enstrophy,
    instantaneous_energy_check,
    k_1d,
    make_grid,
    project_state,
    rk4_step,
    taylor_green,
)

PERM_COUNT = 6


def mode_coeff(uh: np.ndarray) -> np.ndarray:
    """Physical Fourier coefficient: u = Σ û_k e^{ik·x}."""
    return uh / float(uh.shape[0] * uh.shape[1] * uh.shape[2])


def wavevectors(n: int, dealias: bool = True):
    k = k_1d(n).astype(int)
    pts = []
    cutoff = n / 3 if dealias else n / 2
    for i, kx in enumerate(k):
        for j, ky in enumerate(k):
            for m, kz in enumerate(k):
                if kx == 0 and ky == 0 and kz == 0:
                    continue
                if dealias and (abs(kx) >= cutoff or abs(ky) >= cutoff or abs(kz) >= cutoff):
                    continue
                pts.append(((int(kx), int(ky), int(kz)), (i, j, m)))
    return pts


def _index_map(n: int):
    k = k_1d(n).astype(int)
    loc = {}
    for i, kx in enumerate(k):
        loc[int(kx)] = i
    return loc


def i3(p, q, k, vp, vq, vk) -> float:
    """I₃(p, q; k) = Im[(q·v_p)(v_q · conj(v_k))], p+q=k."""
    qf = np.asarray(q, dtype=float)
    return float(np.imag(np.dot(qf, vp) * np.dot(vq, np.conj(vk))))


def invariant_interaction(k, p, q, vk, vp, vq) -> float:
    """Labeling-invariant three-wave interaction for k+p+q=0.

    Φ(k,p,q) = I₃(p,q;-k) + I₃(q,k;-p) + I₃(k,p;-q).
    On a real divergence-free field this is the same number for every
    permutation of (k,p,q).
    """
    mk = tuple(-x for x in k)
    mp = tuple(-x for x in p)
    mq = tuple(-x for x in q)
    return i3(p, q, mk, vp, vq, vk) + i3(q, k, mp, vq, vk, vp) + i3(k, p, mq, vk, vp, vq)


def triangle_key(k, p, q):
    return tuple(sorted((tuple(k), tuple(p), tuple(q))))


def _velocity_at(uh, vh, wh, loc, k):
    i, j, m = loc[k[0]], loc[k[1]], loc[k[2]]
    return np.array([uh[i, j, m], vh[i, j, m], wh[i, j, m]], dtype=complex)


def collect_modes(u, v, w, dealias: bool = True, rel_floor: float = 1e-10):
    n = u.shape[0]
    uh = mode_coeff(np.fft.fftn(u))
    vh = mode_coeff(np.fft.fftn(v))
    wh = mode_coeff(np.fft.fftn(w))
    loc = _index_map(n)
    raw = {}
    peak = 0.0
    for k, _idx in wavevectors(n, dealias=dealias):
        vk = _velocity_at(uh, vh, wh, loc, k)
        nrm = float(np.linalg.norm(vk))
        raw[k] = (vk, nrm)
        if nrm > peak:
            peak = nrm
    floor = rel_floor * max(peak, 1e-30)
    modes = {k: vk for k, (vk, nrm) in raw.items() if nrm > floor}
    return modes, uh, vh, wh, loc


def measure_field(u, v, w, nu: float, dealias: bool = True, overcount: bool = False) -> dict:
    """Transfer, viscous amount, coherence, and S on one snapshot.

    overcount=True reproduces the first-run 6× bookkeeping (do not use
    for a reported S). Default counts each unordered triangle once.
    """
    modes, _uh, _vh, _wh, _loc = collect_modes(u, v, w, dealias=dealias)
    keys = list(modes.keys())
    keyset = set(keys)
    seen = set()
    transfer = 0.0
    abs_transfer = 0.0
    n_counted = 0
    per_shell = {}

    for k in keys:
        for p in keys:
            q = (-k[0] - p[0], -k[1] - p[1], -k[2] - p[2])
            if q not in keyset:
                continue
            if q == (0, 0, 0) or len({k, p, q}) < 3:
                continue
            tkey = triangle_key(k, p, q)
            if (not overcount) and tkey in seen:
                continue
            phi = invariant_interaction(k, p, q, modes[k], modes[p], modes[q])
            # Physical energy-rate scaling: Φ is built from û = FFT/N³.
            # ∫ involves vol, matching the solver inner product.
            phi *= VOL_T3
            transfer += phi
            abs_transfer += abs(phi)
            n_counted += 1
            seen.add(tkey)
            shells = tuple(
                sorted(
                    (
                        k[0] ** 2 + k[1] ** 2 + k[2] ** 2,
                        p[0] ** 2 + p[1] ** 2 + p[2] ** 2,
                        q[0] ** 2 + q[1] ** 2 + q[2] ** 2,
                    )
                )
            )
            bucket = per_shell.setdefault(
                str(shells),
                {"transfer": 0.0, "abs_transfer": 0.0, "triangles": 0},
            )
            bucket["transfer"] += phi
            bucket["abs_transfer"] += abs(phi)
            bucket["triangles"] += 1
    n_unique = len(seen)

    kx, ky, kz, _k2, _k2_safe, _dealias = make_grid(u.shape[0])
    check = instantaneous_energy_check(
        u,
        v,
        w,
        kx=kx,
        ky=ky,
        kz=kz,
        k2=_k2,
        k2_safe=_k2_safe,
        dealias=_dealias,
        nu=nu,
        eps=0.0,
        alpha=1.0,
        beta=0.5,
    )
    viscous = check["viscous_inner"]
    coherence = abs(transfer) / abs_transfer if abs_transfer > 0.0 else 0.0
    # S is zero when unique |transfer| does not beat viscous. Always
    # keep the underlying numbers (M2).
    s_zero = abs_transfer < viscous
    s_value = 0.0 if s_zero else abs_transfer / viscous
    return {
        "transfer": transfer,
        "abs_transfer": abs_transfer,
        "viscous": viscous,
        "coherence": coherence,
        "S": s_value,
        "S_is_zero": s_zero,
        "n_unique_triangles": n_unique,
        "n_counted": n_counted,
        "overcount": overcount,
        "count_factor": (n_counted / n_unique) if n_unique else 0.0,
        "energy": energy(u, v, w),
        "enstrophy": enstrophy(u, v, w, kx, ky, kz),
        "power_residual": check["residual"],
        "per_shell": per_shell,
        "numbers_behind_zero": {
            "abs_transfer": abs_transfer,
            "viscous": viscous,
            "coherence": coherence,
            "abs_transfer_over_viscous": (abs_transfer / viscous) if viscous else None,
        },
    }


def permutation_invariance_check(k, p, q, vk, vp, vq, tol: float = 5e-13) -> dict:
    """Φ is the same for all 6 labelings. Numerical lock ~13 decimals."""
    vecs = {"k": (k, vk), "p": (p, vp), "q": (q, vq)}
    values = []
    for order in itertools.permutations(("k", "p", "q")):
        a, b, c = (vecs[name] for name in order)
        values.append(invariant_interaction(a[0], b[0], c[0], a[1], b[1], c[1]))
    spread = float(max(values) - min(values))
    return {
        "values": values,
        "spread": spread,
        "ok": spread <= tol * max(1.0, max(abs(x) for x in values)),
        "perm_count": len(values),
    }


def format_measurement(m: dict, label: str = "") -> str:
    """Always print the numbers behind a zero S."""
    head = f"S={m['S']:.6g}" if not m["S_is_zero"] else "S=0"
    return (
        f"{label}{head}  transfer={m['transfer']:.10g}  "
        f"|transfer|={m['abs_transfer']:.10g}  viscous={m['viscous']:.10g}  "
        f"coherence={m['coherence']:.10g}  "
        f"|T|/visc={m['numbers_behind_zero']['abs_transfer_over_viscous']!s}  "
        f"triangles={m['n_unique_triangles']}  counted={m['n_counted']}"
    )


def evolve_taylor_green(n: int, nu: float, t_end: float, dt: float):
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    u, v, w = taylor_green(n)
    u, v, w = project_state(u, v, w, kx, ky, kz, k2_safe)
    kw = dict(
        kx=kx,
        ky=ky,
        kz=kz,
        k2=k2,
        k2_safe=k2_safe,
        dealias=dealias,
        nu=nu,
        eps=0.0,
        alpha=1.0,
        beta=0.5,
    )
    steps = max(1, int(round(t_end / dt)))
    dt = t_end / steps
    snapshots = [(0.0, u.copy(), v.copy(), w.copy())]
    t = 0.0
    for _ in range(steps):
        u, v, w = rk4_step(u, v, w, dt, **kw)
        t += dt
        snapshots.append((t, u.copy(), v.copy(), w.copy()))
    return snapshots, kw


def peak_table(n: int, nu: float, t_end: float, dt: float, stride: int = 1) -> dict:
    snapshots, _kw = evolve_taylor_green(n, nu, t_end, dt)
    rows = []
    peak = None
    for i, (t, u, v, w) in enumerate(snapshots):
        if i % stride != 0 and i != 0 and i != len(snapshots) - 1:
            continue
        m = measure_field(u, v, w, nu=nu)
        row = {
            "t": t,
            "energy": m["energy"],
            "enstrophy": m["enstrophy"],
            "transfer": m["transfer"],
            "abs_transfer": m["abs_transfer"],
            "viscous": m["viscous"],
            "coherence": m["coherence"],
            "S": m["S"],
            "S_is_zero": m["S_is_zero"],
            "n_unique_triangles": m["n_unique_triangles"],
            "numbers_behind_zero": m["numbers_behind_zero"],
        }
        rows.append(row)
        print(format_measurement(m, label=f"t={t:.4f}  "), flush=True)
        if peak is None or row["abs_transfer"] > peak["abs_transfer"]:
            peak = row

    # Six-count comparison at the peak snapshot (evidence, not a second S).
    peak_t = peak["t"]
    peak_snap = min(snapshots, key=lambda s: abs(s[0] - peak_t))
    unique = measure_field(peak_snap[1], peak_snap[2], peak_snap[3], nu=nu, overcount=False)
    sixfold = measure_field(peak_snap[1], peak_snap[2], peak_snap[3], nu=nu, overcount=True)
    return {
        "meta": {
            "field": "Taylor-Green",
            "n": n,
            "nu": nu,
            "t_end": t_end,
            "dt": dt,
            "count": "unique_unordered_triangle",
            "note": (
                "S=0 when |transfer| < viscous. Numbers behind every zero "
                "are printed. First-run per-field β tables stay inconclusive "
                "until this unique-count re-run. Classical NS stays open."
            ),
        },
        "rows": rows,
        "peak": peak,
        "peak_count_check": {
            "unique_abs_transfer": unique["abs_transfer"],
            "sixfold_abs_transfer": sixfold["abs_transfer"],
            "ratio": (
                sixfold["abs_transfer"] / unique["abs_transfer"]
                if unique["abs_transfer"]
                else None
            ),
            "unique_viscous": unique["viscous"],
            "expected_count_factor": float(PERM_COUNT),
        },
        "beta_tables": {
            "status": "re-run_with_unique_count",
            "first_run": "inconclusive",
            "per_shell_at_peak": unique["per_shell"],
        },
        "ns_solved": False,
        "classical_ns_open": True,
        "loop_defect": {
            "status": "inconclusive",
            "note": (
                "Loop family shows a trend on lower bounds only. "
                "A guaranteed upper bound is required before calling "
                "anything a defect."
            ),
        },
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Unique-count S measurement")
    p.add_argument("--n", type=int, default=16)
    p.add_argument("--nu", type=float, default=0.02)
    p.add_argument("--t", type=float, default=5.0)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--stride", type=int, default=1)
    p.add_argument("--out", type=Path, default=Path("results/s_measurement_peak_tables.json"))
    args = p.parse_args()

    table = peak_table(args.n, args.nu, args.t, args.dt, stride=args.stride)
    peak = table["peak"]
    print(
        "PEAK  "
        + format_measurement(
            {
                **peak,
                "transfer": peak["transfer"],
                "n_counted": peak["n_unique_triangles"],
            },
            label="",
        ),
        flush=True,
    )
    print(
        "count check: unique={:.6g}  6-fold={:.6g}  ratio={}".format(
            table["peak_count_check"]["unique_abs_transfer"],
            table["peak_count_check"]["sixfold_abs_transfer"],
            table["peak_count_check"]["ratio"],
        ),
        flush=True,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(table, indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
