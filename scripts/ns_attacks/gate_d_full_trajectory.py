#!/usr/bin/env python3
"""Gate D full-trajectory solver — six-box Signed-Gate, no top-M.

Preserves the exact signed-scalene diagnostic. Dense spherical Galerkin at
cutoff >=4H OOMs; this path uses tiled sparse convolution among all active
modes in the ball. Amplitude floor drops only numerical zeros — never an
energy-ranking prune.

Score: B_I / R_I with B_I = ∫ d(t) dt only (do not add (b-a)d(a) on top).
Diagnostic: fixed K (default K²=1), full X,Y — not H-high-pass X_H,Y_H.
Numerical evidence only. No theorem stamp. Not (17).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from numba import njit

from verify_signed_gate import packet

# Reuse moment / transfer kernels from the demoted top-M runner (same diagnostic).
from gate_d_adversarial_run import (
    build_packet_arrays,
    choose_nu,
    hermitize,
    moments,
    normalize_E,
    prune,
    transfer_scalene,
)


@njit(cache=True)
def _hash_add(hk0, hk1, hk2, acc, used, capacity, kx, ky, kz, v0, v1, v2):
    """Accumulate into hash; return slot index, or -1 if table full."""
    h = (kx * 73856093 + ky * 19349663 + kz * 83492791) & (capacity - 1)
    probes = 0
    while used[h] != 0 and probes < capacity:
        if hk0[h] == kx and hk1[h] == ky and hk2[h] == kz:
            acc[h, 0] += v0
            acc[h, 1] += v1
            acc[h, 2] += v2
            return h
        h = (h + 1) & (capacity - 1)
        probes += 1
    if used[h] == 0:
        used[h] = 1
        hk0[h], hk1[h], hk2[h] = kx, ky, kz
        acc[h, 0] = v0
        acc[h, 1] = v1
        acc[h, 2] = v2
        return h
    return -1


@njit(cache=True)
def rhs_tiled(k, u, nu, k_max2, out_floor, tile, capacity):
    """Exact truncated convolution among active modes; tiled i-blocks.

    Peak scratch is O(capacity), not O(m^2). Products landing in the ball
    are admitted (no top-M). Modes below out_floor that were not already
    occupied are dropped as numerical zeros.
    """
    m = k.shape[0]
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    seeded = np.zeros(capacity, dtype=np.uint8)
    n_fill = 0
    overflow = 0

    for i in range(m):
        a = k[i, 0] * k[i, 0] + k[i, 1] * k[i, 1] + k[i, 2] * k[i, 2]
        if a > k_max2 or a == 0:
            continue
        h = _hash_add(
            hk0,
            hk1,
            hk2,
            acc,
            used,
            capacity,
            k[i, 0],
            k[i, 1],
            k[i, 2],
            -nu * a * u[i, 0],
            -nu * a * u[i, 1],
            -nu * a * u[i, 2],
        )
        if h < 0:
            overflow += 1
            continue
        if seeded[h] == 0:
            n_fill += 1
        seeded[h] = 1

    i0 = 0
    while i0 < m:
        i1 = min(m, i0 + tile)
        for i in range(i0, i1):
            for j in range(m):
                kx = k[i, 0] + k[j, 0]
                ky = k[i, 1] + k[j, 1]
                kz = k[i, 2] + k[j, 2]
                a = kx * kx + ky * ky + kz * kz
                if a == 0 or a > k_max2:
                    continue
                qdot = u[i, 0] * k[j, 0] + u[i, 1] * k[j, 1] + u[i, 2] * k[j, 2]
                t0 = qdot * u[j, 0]
                t1 = qdot * u[j, 1]
                t2 = qdot * u[j, 2]
                kdot = (kx * t0 + ky * t1 + kz * t2) / a
                p0 = t0 - kx * kdot
                p1 = t1 - ky * kdot
                p2 = t2 - kz * kdot
                n0 = -1j * p0
                n1 = -1j * p1
                n2 = -1j * p2
                occupied = 0
                hh = (kx * 73856093 + ky * 19349663 + kz * 83492791) & (capacity - 1)
                probes = 0
                while used[hh] != 0 and probes < capacity:
                    if hk0[hh] == kx and hk1[hh] == ky and hk2[hh] == kz:
                        occupied = 1
                        break
                    hh = (hh + 1) & (capacity - 1)
                    probes += 1
                h = _hash_add(
                    hk0, hk1, hk2, acc, used, capacity, kx, ky, kz, n0, n1, n2
                )
                if h < 0:
                    overflow += 1
                elif occupied == 0:
                    n_fill += 1
        i0 = i1

    n_keep = 0
    for h in range(capacity):
        if used[h] == 0:
            continue
        mag2 = 0.0
        for c in range(3):
            mag2 += acc[h, c].real * acc[h, c].real + acc[h, c].imag * acc[h, c].imag
        if seeded[h] == 1 or mag2 >= out_floor:
            n_keep += 1
    out_k = np.empty((n_keep, 3), dtype=np.int32)
    out_u = np.empty((n_keep, 3), dtype=np.complex128)
    idx = 0
    for h in range(capacity):
        if used[h] == 0:
            continue
        mag2 = 0.0
        for c in range(3):
            mag2 += acc[h, c].real * acc[h, c].real + acc[h, c].imag * acc[h, c].imag
        if seeded[h] == 0 and mag2 < out_floor:
            continue
        out_k[idx, 0] = hk0[h]
        out_k[idx, 1] = hk1[h]
        out_k[idx, 2] = hk2[h]
        out_u[idx, 0] = acc[h, 0]
        out_u[idx, 1] = acc[h, 1]
        out_u[idx, 2] = acc[h, 2]
        idx += 1
    return out_k, out_u, overflow, n_fill


@njit(cache=True)
def merge_axpy(k1, u1, k2, u2, alpha, k_max2, mag2_floor):
    capacity = 1
    while capacity < (k1.shape[0] + k2.shape[0]) * 4 + 16:
        capacity *= 2
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    for arr_k, arr_u, scale in ((k1, u1, 1.0 + 0j), (k2, u2, alpha + 0j)):
        for i in range(arr_k.shape[0]):
            a = (
                arr_k[i, 0] * arr_k[i, 0]
                + arr_k[i, 1] * arr_k[i, 1]
                + arr_k[i, 2] * arr_k[i, 2]
            )
            if a == 0 or a > k_max2:
                continue
            kx, ky, kz = arr_k[i, 0], arr_k[i, 1], arr_k[i, 2]
            h = (kx * 73856093 + ky * 19349663 + kz * 83492791) & (capacity - 1)
            probes = 0
            while used[h] != 0 and probes < capacity:
                if hk0[h] == kx and hk1[h] == ky and hk2[h] == kz:
                    break
                h = (h + 1) & (capacity - 1)
                probes += 1
            if used[h] == 0:
                used[h] = 1
                hk0[h], hk1[h], hk2[h] = kx, ky, kz
            acc[h, 0] += scale * arr_u[i, 0]
            acc[h, 1] += scale * arr_u[i, 1]
            acc[h, 2] += scale * arr_u[i, 2]
    n_keep = 0
    for h in range(capacity):
        if used[h] == 0:
            continue
        mag2 = 0.0
        for c in range(3):
            mag2 += acc[h, c].real * acc[h, c].real + acc[h, c].imag * acc[h, c].imag
        if mag2 >= mag2_floor:
            n_keep += 1
    out_k = np.empty((n_keep, 3), dtype=np.int32)
    out_u = np.empty((n_keep, 3), dtype=np.complex128)
    idx = 0
    for h in range(capacity):
        if used[h] == 0:
            continue
        mag2 = 0.0
        for c in range(3):
            mag2 += acc[h, c].real * acc[h, c].real + acc[h, c].imag * acc[h, c].imag
        if mag2 < mag2_floor:
            continue
        out_k[idx, 0] = hk0[h]
        out_k[idx, 1] = hk1[h]
        out_k[idx, 2] = hk2[h]
        out_u[idx, 0] = acc[h, 0]
        out_u[idx, 1] = acc[h, 1]
        out_u[idx, 2] = acc[h, 2]
        idx += 1
    return out_k, out_u


def rk2_step(k, u, dt, nu, k_max2, floor, tile, capacity):
    fk, fu, ov1, _ = rhs_tiled(k, u, nu, k_max2, floor, tile, capacity)
    k_mid, u_mid = merge_axpy(k, u, fk, fu, 0.5 * dt, k_max2, floor)
    k_mid, u_mid = hermitize(k_mid, u_mid)
    k_mid, u_mid = prune(k_mid, u_mid, floor)
    fk2, fu2, ov2, _ = rhs_tiled(k_mid, u_mid, nu, k_max2, floor, tile, capacity)
    k2, u2 = merge_axpy(k, u, fk2, fu2, dt, k_max2, floor)
    k2, u2 = hermitize(k2, u2)
    k2, u2 = prune(k2, u2, floor)
    return k2, u2, ov1 + ov2


def measure_episode(
    n,
    nu,
    *,
    cut_mul=4,
    t_max_factor=2500.0,
    dt_factor=2.0,
    floor_rel=1e-30,
    tile=64,
    hash_capacity=1 << 20,
    max_modes=80000,
    max_steps=None,
    smoke=False,
):
    meta = packet(n)
    H = int(meta["H"])
    K2_fixed = 1.0  # recovered Gate D / episode-balance target
    k_max = cut_mul * H
    k_max2 = k_max * k_max
    k, u = build_packet_arrays(n)
    u = normalize_E(u, 1.0)
    k, u = hermitize(k, u)

    T_expected = float(meta["T_scalene"]) / (float(meta["E"]) ** 1.5)

    # Warm JIT
    _ = transfer_scalene(k, u, float(K2_fixed))
    _ = rhs_tiled(k, u, nu, k_max2, floor_rel, tile, hash_capacity)

    t_wall = time.time()
    # moments(..., k_high2) still returns full X,Y as slots 1,2
    E0, X0, Y0, _X_H0, _Y_H0, U0, W0 = moments(k, u, float(H * H))
    T0, n0 = transfer_scalene(k, u, float(K2_fixed))
    D0 = T0 - nu * Y0 / 4.0
    d0 = D0 / max(X0, 1e-300)

    fk, fu, _, _ = rhs_tiled(k, u, nu, k_max2, 0.0, tile, hash_capacity)
    fd = {
        (int(fk[i, 0]), int(fk[i, 1]), int(fk[i, 2])): fu[i] for i in range(fk.shape[0])
    }
    Xp = 0.0
    for i in range(k.shape[0]):
        key = (int(k[i, 0]), int(k[i, 1]), int(k[i, 2]))
        if key not in fd:
            continue
        f = fd[key]
        a = float(k[i, 0] ** 2 + k[i, 1] ** 2 + k[i, 2] ** 2)
        for c in range(3):
            Xp += 2 * a * (u[i, c].real * f[c].real + u[i, c].imag * f[c].imag)
    identity_residual = Xp - (-2 * nu * Y0 + 2 * T0)

    eps = 1e-8
    be_k, be_u = merge_axpy(k, u, fk, fu, eps, k_max2, 0.0)
    Te, _ = transfer_scalene(be_k, be_u, float(K2_fixed))
    _, _, Ye, _, _, _, _ = moments(be_k, be_u, float(H * H))
    Dp = ((Te - nu * Ye / 4.0) - D0) / eps

    tau_nl = float(H ** (-2.5))
    dt = dt_factor * tau_nl
    t_max = (5.0 if smoke else t_max_factor) * tau_nl
    if max_steps is None:
        max_steps = 8 if smoke else 10**9

    times = [0.0]
    Ds = [float(D0)]
    Xs = [float(X0)]
    UWs = [float(U0 * W0)]
    Ts = [float(T0)]

    t = 0.0
    # First episode starts at t=0 with d(a)>0 for the signed packet.
    episode_start = 0.0 if D0 > 0 else None
    episode_end = None
    B_direct = 0.0  # ∫ d dt only
    R_UW_acc = 0.0
    R_X_acc = 0.0
    steps = 0
    status_detail = "RUNNING"
    max_modes_obs = int(k.shape[0])
    overflow_total = 0

    print(
        f"  t0: D={D0:.6e} d={d0:.6e} Dp={Dp:.6e} "
        f"T_err={(T0 - T_expected) / abs(T_expected):.3e} "
        f"X'_res={identity_residual:.3e} modes={k.shape[0]}",
        flush=True,
    )

    while t < t_max and steps < max_steps:
        k, u, ov = rk2_step(k, u, dt, nu, k_max2, floor_rel, tile, hash_capacity)
        overflow_total += ov
        t += dt
        steps += 1
        max_modes_obs = max(max_modes_obs, int(k.shape[0]))

        if k.shape[0] > max_modes:
            status_detail = "MODE_BUDGET_HIT"
            break
        if ov > 0:
            status_detail = "HASH_OVERFLOW"
            break

        E, X, Y, _X_H, _Y_H, U, W = moments(k, u, float(H * H))
        Tsc, _ = transfer_scalene(k, u, float(K2_fixed))
        D = Tsc - nu * Y / 4.0
        times.append(t)
        Ds.append(float(D))
        Xs.append(float(X))
        UWs.append(float(U * W))
        Ts.append(float(Tsc))

        if episode_start is None:
            if Ds[-2] <= 0.0 < D:
                frac = -Ds[-2] / (D - Ds[-2])
                episode_start = times[-2] + frac * dt
                B_direct = 0.5 * (D / max(X, 1e-300)) * (t - episode_start)
                uw_c = UWs[-2] + frac * (UWs[-1] - UWs[-2])
                R_UW_acc = 0.5 * (uw_c + UWs[-1]) * (t - episode_start)
                x_c = Xs[-2] + frac * (Xs[-1] - Xs[-2])
                R_X_acc = 0.5 * (x_c + Xs[-1]) * (t - episode_start)
        else:
            Xp_, Xc = max(Xs[-2], 1e-300), max(Xs[-1], 1e-300)
            B_direct += 0.5 * (Ds[-2] / Xp_ + Ds[-1] / Xc) * dt
            R_UW_acc += 0.5 * (UWs[-2] + UWs[-1]) * dt
            R_X_acc += 0.5 * (Xs[-2] + Xs[-1]) * dt
            if Ds[-2] > 0.0 >= D:
                frac = Ds[-2] / (Ds[-2] - D)
                episode_end = times[-2] + frac * dt
                B_direct -= 0.5 * (Ds[-2] / Xp_ + Ds[-1] / Xc) * dt
                R_UW_acc -= 0.5 * (UWs[-2] + UWs[-1]) * dt
                R_X_acc -= 0.5 * (Xs[-2] + Xs[-1]) * dt
                seg = episode_end - times[-2]
                x_end = Xs[-2] + frac * (Xs[-1] - Xs[-2])
                uw_end = UWs[-2] + frac * (UWs[-1] - UWs[-2])
                B_direct += 0.5 * (Ds[-2] / Xp_) * seg
                R_UW_acc += 0.5 * (UWs[-2] + uw_end) * seg
                R_X_acc += 0.5 * (Xs[-2] + x_end) * seg
                status_detail = "COMPLETE_FIRST_EPISODE"
                break

        if steps <= 5 or steps % 25 == 0:
            print(
                f"  step={steps} t/tau={t / tau_nl:.2f} D={D:.4e} T={Tsc:.4e} "
                f"B_direct={B_direct:.4e} modes={k.shape[0]} E={E:.5f}",
                flush=True,
            )

    if episode_start is not None and episode_end is None:
        # Truncated / budget / smoke window — still score through current t.
        episode_end = t
        if status_detail == "RUNNING":
            status_detail = "TRUNCATED_POSITIVE_EPISODE"
    if episode_start is None and status_detail == "RUNNING":
        status_detail = "NO_POSITIVE_EPISODE_IN_WINDOW"
    if smoke and status_detail in ("RUNNING", "TRUNCATED_POSITIVE_EPISODE"):
        status_detail = "SMOKE_OK" if status_detail == "RUNNING" else status_detail

    I_len = (
        None
        if episode_start is None or episode_end is None
        else float(episode_end - episode_start)
    )

    # Boundary term belongs in the d' reconstruction only — not added to ∫d.
    boundary_for_reconstruction = 0.0
    if (
        episode_start is not None
        and episode_end is not None
        and d0 > 0
        and abs(episode_start) < 1e-30
    ):
        boundary_for_reconstruction = float(I_len) * float(d0)
    B_IH = None if episode_start is None else float(B_direct)
    R_UW = None if episode_start is None else float(R_UW_acc)
    B_over_R = (
        None
        if B_IH is None or R_UW is None or R_UW == 0.0
        else float(B_IH / R_UW)
    )

    return {
        "n": n,
        "H": H,
        "nu": nu,
        "E": 1.0,
        "K2_fixed": K2_fixed,
        "diagnostic": "fixed_K_full_XY_signed_scalene",
        "k_max": k_max,
        "cut_mul": cut_mul,
        "method": "sparse_Galerkin_tiled_full_trajectory_rk2_no_topM",
        "topM": False,
        "floor_rel": floor_rel,
        "tile": tile,
        "hash_capacity": hash_capacity,
        "max_modes_budget": max_modes,
        "modes_initial": int(meta["modes"]),
        "modes_max_observed": max_modes_obs,
        "hash_overflow_events": int(overflow_total),
        "T_sc_E1": float(T0),
        "T_sc_E1_expected_from_verifier": float(T_expected),
        "T_sc_rel_err_vs_verifier": float((T0 - T_expected) / abs(T_expected)),
        "energy_identity_Xprime_residual": float(identity_residual),
        "active_modes_t0": int(n0),
        "X(0)_full": float(X0),
        "Y(0)_full": float(Y0),
        "U(0)": float(U0),
        "W(0)": float(W0),
        "D(0)": float(D0),
        "d(0)": float(d0),
        "D_prime(0)": float(Dp),
        "episode_start": episode_start,
        "episode_end": episode_end,
        "I_length": I_len,
        "H^{5/2}|I|_duration_diagnostic_only": (
            None if I_len is None else float((H**2.5) * I_len)
        ),
        "B_IH": B_IH,
        "B_IH_definition": "direct_integral_int_d_dt",
        "boundary_term_for_dprime_reconstruction_only": boundary_for_reconstruction,
        "resource_UW_integral": R_UW,
        "resource_X_integral_DIAGNOSTIC_ruled_out": (
            None if episode_start is None else float(R_X_acc)
        ),
        "B_over_R": B_over_R,
        "episode_truncated": status_detail == "TRUNCATED_POSITIVE_EPISODE",
        "steps": steps,
        "dt": dt,
        "dt_factor": dt_factor,
        "t_max": t_max,
        "tau_nl_H^{-5/2}": tau_nl,
        "wall_seconds": time.time() - t_wall,
        "status": "NUMERICAL_EVIDENCE_ONLY",
        "status_detail": status_detail,
        "theorem_stamp": False,
        "full_trajectory_complete": status_detail == "COMPLETE_FIRST_EPISODE",
        "U0": float(U0),
        "small_l1_hypothesis_U0_le_nu/4": bool(U0 <= nu / 4.0),
        "D_trajectory": {
            "t_over_tau_nl": [tt / tau_nl for tt in times[:: max(1, len(times) // 50)]],
            "D": Ds[:: max(1, len(Ds) // 50)],
            "T_sc": Ts[:: max(1, len(Ts) // 50)],
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[1])
    ap.add_argument("--nu", type=float, default=None)
    ap.add_argument("--cut-mul", type=int, default=4)
    ap.add_argument("--t-max-factor", type=float, default=2500.0)
    ap.add_argument("--dt-factor", type=float, default=2.0)
    ap.add_argument("--floor-rel", type=float, default=1e-30)
    ap.add_argument("--tile", type=int, default=64)
    ap.add_argument("--hash-capacity", type=int, default=1 << 20)
    ap.add_argument("--max-modes", type=int, default=80000)
    ap.add_argument("--max-steps", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("GATE-D-FULL-TRAJECTORY.json"),
    )
    args = ap.parse_args()

    runs = []
    for n in args.n:
        nu = args.nu if args.nu is not None else choose_nu(n)
        print(
            f"=== Gate D full-trajectory n={n} H={63 * n} nu={nu:.6e} "
            f"cut={args.cut_mul}H smoke={args.smoke} ===",
            flush=True,
        )
        rec = measure_episode(
            n,
            nu,
            cut_mul=args.cut_mul,
            t_max_factor=args.t_max_factor,
            dt_factor=args.dt_factor,
            floor_rel=args.floor_rel,
            tile=args.tile,
            hash_capacity=args.hash_capacity,
            max_modes=args.max_modes,
            max_steps=args.max_steps,
            smoke=args.smoke,
        )
        keys = [
            "n",
            "H",
            "nu",
            "method",
            "topM",
            "K2_fixed",
            "diagnostic",
            "D(0)",
            "d(0)",
            "D_prime(0)",
            "I_length",
            "B_IH",
            "B_IH_definition",
            "boundary_term_for_dprime_reconstruction_only",
            "B_over_R",
            "status_detail",
            "full_trajectory_complete",
            "T_sc_rel_err_vs_verifier",
            "energy_identity_Xprime_residual",
            "modes_max_observed",
            "wall_seconds",
            "theorem_stamp",
        ]
        print(json.dumps({k: rec.get(k) for k in keys}, indent=2), flush=True)
        runs.append(rec)

    payload = {
        "title": "Gate D full-trajectory solver — corrected diagnostics",
        "adversary": "Signed-Gate-B-Sharp-Band-Exponent-2026-10-07 six-box",
        "theorem_stamp": False,
        "gaussian_substituted": False,
        "topM": False,
        "scoring": "B_IH / R_UW with B_IH = int d dt (no double-count)",
        "review": "GATE-D-REVIEW-2026-10-09",
        "runs": runs,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
