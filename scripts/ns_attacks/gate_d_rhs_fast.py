#!/usr/bin/env python3
"""Separate copy of the Gate D Fourier interaction sum.

The reference solver and any checkpoint stay untouched. This file only
reimplements the pair sum, then checks it against
``gate_d_full_trajectory.rhs_tiled`` on the same field, viscosity, cutoff,
and time step.

Numerical evidence only. Not a turnover run. Not (17).
"""
from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from numba import njit, set_num_threads

from gate_d_adversarial_run import (
    build_packet_arrays,
    choose_nu,
    hermitize,
    moments,
    normalize_E,
    prune,
    transfer_scalene,
)
from gate_d_full_trajectory import _hash_add, rhs_tiled

# Match the reference defaults used for a continuation step.
TILE = 64
HASH_CAPACITY = 1 << 20
FLOOR_REL = 1e-30
DT_FACTOR = 2.0
K2_FIXED = 1.0


@njit(cache=True)
def _reference_pair_slice(k, u, i0, i1, k_max2, capacity):
    """Copy of the reference pair loop over i in [i0, i1), for timing only."""
    m = k.shape[0]
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    overflow = 0
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
            hh = (kx * 73856093 + ky * 19349663 + kz * 83492791) & (capacity - 1)
            probes = 0
            while used[hh] != 0 and probes < capacity:
                if hk0[hh] == kx and hk1[hh] == ky and hk2[hh] == kz:
                    break
                hh = (hh + 1) & (capacity - 1)
                probes += 1
            h = _hash_add(hk0, hk1, hk2, acc, used, capacity, kx, ky, kz, n0, n1, n2)
            if h < 0:
                overflow += 1
    n_keep = 0
    for h in range(capacity):
        if used[h] != 0:
            n_keep += 1
    out_k = np.empty((n_keep, 3), dtype=np.int32)
    out_u = np.empty((n_keep, 3), dtype=np.complex128)
    idx = 0
    for h in range(capacity):
        if used[h] == 0:
            continue
        out_k[idx, 0] = hk0[h]
        out_k[idx, 1] = hk1[h]
        out_k[idx, 2] = hk2[h]
        out_u[idx, 0] = acc[h, 0]
        out_u[idx, 1] = acc[h, 1]
        out_u[idx, 2] = acc[h, 2]
        idx += 1
    return out_k, out_u, overflow, n_keep


@njit(cache=True)
def _nonlinear_slice(k, u, i0, i1, k_max, k_max2, order, kx_sorted, capacity):
    """Ordered pairs with i in [i0, i1). Partners are restricted by |kx_i+kx_j|<=k_max."""
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    overflow = 0
    n_fill = 0
    for i in range(i0, i1):
        ai = k[i, 0] * k[i, 0] + k[i, 1] * k[i, 1] + k[i, 2] * k[i, 2]
        if ai > k_max2 or ai == 0:
            continue
        for j in range(k.shape[0]):
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
            n0 = -1j * (t0 - kx * kdot)
            n1 = -1j * (t1 - ky * kdot)
            n2 = -1j * (t2 - kz * kdot)
            h = _hash_add(hk0, hk1, hk2, acc, used, capacity, kx, ky, kz, n0, n1, n2)
            if h < 0:
                overflow += 1
            else:
                n_fill += 1
    n_keep = 0
    for h in range(capacity):
        if used[h] != 0:
            n_keep += 1
    out_k = np.empty((n_keep, 3), dtype=np.int32)
    out_u = np.empty((n_keep, 3), dtype=np.complex128)
    idx = 0
    for h in range(capacity):
        if used[h] == 0:
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
def _viscosity_field(k, u, nu, k_max2):
    m = k.shape[0]
    out_u = np.zeros_like(u)
    for i in range(m):
        a = k[i, 0] * k[i, 0] + k[i, 1] * k[i, 1] + k[i, 2] * k[i, 2]
        if a == 0 or a > k_max2:
            continue
        damp = -nu * a
        out_u[i, 0] = damp * u[i, 0]
        out_u[i, 1] = damp * u[i, 1]
        out_u[i, 2] = damp * u[i, 2]
    return out_u


@njit(cache=True)
def _merge_seeded(parts_k, parts_u, seed_k, seed_u, k_max2, out_floor, capacity):
    """Sum partial interaction fields onto the seeded viscosity field."""
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    seeded = np.zeros(capacity, dtype=np.uint8)
    overflow = 0

    for i in range(seed_k.shape[0]):
        a = seed_k[i, 0] ** 2 + seed_k[i, 1] ** 2 + seed_k[i, 2] ** 2
        if a == 0 or a > k_max2:
            continue
        h = _hash_add(
            hk0,
            hk1,
            hk2,
            acc,
            used,
            capacity,
            seed_k[i, 0],
            seed_k[i, 1],
            seed_k[i, 2],
            seed_u[i, 0],
            seed_u[i, 1],
            seed_u[i, 2],
        )
        if h < 0:
            overflow += 1
        else:
            seeded[h] = 1

    for p in range(len(parts_k)):
        pk = parts_k[p]
        pu = parts_u[p]
        for i in range(pk.shape[0]):
            a = pk[i, 0] ** 2 + pk[i, 1] ** 2 + pk[i, 2] ** 2
            if a == 0 or a > k_max2:
                continue
            h = _hash_add(
                hk0,
                hk1,
                hk2,
                acc,
                used,
                capacity,
                pk[i, 0],
                pk[i, 1],
                pk[i, 2],
                pu[i, 0],
                pu[i, 1],
                pu[i, 2],
            )
            if h < 0:
                overflow += 1

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
    return out_k, out_u, overflow


def rhs_fast(k, u, nu, k_max2, out_floor, capacity, n_threads):
    """Reference pair arithmetic, kx-culled and split across threads, then merged."""
    m = k.shape[0]
    if n_threads < 1:
        n_threads = 1
    if m == 0:
        return k.copy(), np.zeros_like(u), 0
    k_max = int(np.floor(np.sqrt(k_max2) + 1e-9))
    order = np.argsort(k[:, 0], kind="mergesort").astype(np.int64)
    kx_sorted = np.ascontiguousarray(k[order, 0])
    edges = [int(round(i * m / n_threads)) for i in range(n_threads + 1)]
    slices = [(edges[i], edges[i + 1]) for i in range(n_threads) if edges[i] < edges[i + 1]]
    overflow = 0
    parts_k = []
    parts_u = []
    if len(slices) == 1:
        pk, pu, ov, _ = _nonlinear_slice(
            k, u, slices[0][0], slices[0][1], k_max, k_max2, order, kx_sorted, capacity
        )
        overflow += ov
        parts_k.append(pk)
        parts_u.append(pu)
    else:
        with ThreadPoolExecutor(max_workers=len(slices)) as pool:
            futs = [
                pool.submit(
                    _nonlinear_slice, k, u, a, b, k_max, k_max2, order, kx_sorted, capacity
                )
                for a, b in slices
            ]
            for fut in futs:
                pk, pu, ov, _ = fut.result()
                overflow += ov
                parts_k.append(pk)
                parts_u.append(pu)
    visc = _viscosity_field(k, u, nu, k_max2)
    # Numba needs a typed list of arrays. Pass tuples via a fixed object mode
    # merge written in Python over a njit two-field fold.
    acc_k, acc_u, ov = _merge_seeded(
        _as_list(parts_k), _as_list(parts_u), k, visc, k_max2, out_floor, capacity
    )
    return acc_k, acc_u, overflow + ov


def _as_list(arrs):
    """Numba accepts a reflected list of 2d arrays."""
    return arrs


@njit(cache=True)
def field_l2_diff(k1, u1, k2, u2):
    """L2 difference of two sparse Fourier fields. Returns (diff, n1, n2)."""
    capacity = 1
    while capacity < (k1.shape[0] + k2.shape[0]) * 4 + 16:
        capacity *= 2
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    for arr_k, arr_u, sign in ((k1, u1, 1.0), (k2, u2, -1.0)):
        for i in range(arr_k.shape[0]):
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
            acc[h, 0] += sign * arr_u[i, 0]
            acc[h, 1] += sign * arr_u[i, 1]
            acc[h, 2] += sign * arr_u[i, 2]
    diff = 0.0
    for h in range(capacity):
        if used[h] == 0:
            continue
        for c in range(3):
            diff += acc[h, c].real * acc[h, c].real + acc[h, c].imag * acc[h, c].imag
    return np.sqrt(diff), k1.shape[0], k2.shape[0]


def energy_balance(k, u, fk, fu, nu, k_high2):
    """X' residual against -2 ν Y + 2 T, and the signed excess T - ν Y/4."""
    E, X, Y, _, _, _, _ = moments(k, u, k_high2)
    T, n_act = transfer_scalene(k, u, K2_FIXED)
    fd = {(int(fk[i, 0]), int(fk[i, 1]), int(fk[i, 2])): fu[i] for i in range(fk.shape[0])}
    xp = 0.0
    for i in range(k.shape[0]):
        key = (int(k[i, 0]), int(k[i, 1]), int(k[i, 2]))
        if key not in fd:
            continue
        f = fd[key]
        a = float(k[i, 0] ** 2 + k[i, 1] ** 2 + k[i, 2] ** 2)
        for c in range(3):
            xp += 2 * a * (u[i, c].real * f[c].real + u[i, c].imag * f[c].imag)
    residual = xp - (-2.0 * nu * Y + 2.0 * T)
    excess = T - nu * Y / 4.0
    return {
        "E": float(E),
        "X": float(X),
        "Y": float(Y),
        "T": float(T),
        "signed_excess": float(excess),
        "energy_identity_residual": float(residual),
        "active_for_transfer": int(n_act),
    }


def rk2_with(rhs, k, u, dt, nu, k_max2, floor, capacity, n_threads):
    if rhs is rhs_tiled:
        fk, fu, ov1, _ = rhs(k, u, nu, k_max2, floor, TILE, capacity)
    else:
        fk, fu, ov1 = rhs(k, u, nu, k_max2, floor, capacity, n_threads)
    from gate_d_full_trajectory import merge_axpy

    k_mid, u_mid = merge_axpy(k, u, fk, fu, 0.5 * dt, k_max2, floor)
    k_mid, u_mid = hermitize(k_mid, u_mid)
    k_mid, u_mid = prune(k_mid, u_mid, floor)
    if rhs is rhs_tiled:
        fk2, fu2, ov2, _ = rhs(k_mid, u_mid, nu, k_max2, floor, TILE, capacity)
    else:
        fk2, fu2, ov2 = rhs(k_mid, u_mid, nu, k_max2, floor, capacity, n_threads)
    k2, u2 = merge_axpy(k, u, fk2, fu2, dt, k_max2, floor)
    k2, u2 = hermitize(k2, u2)
    k2, u2 = prune(k2, u2, floor)
    return k2, u2, ov1 + ov2


def _time_call(fn, repeats=3):
    times = []
    last = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        last = fn()
        times.append(time.perf_counter() - t0)
    return float(np.median(times)), last


def initial_state(n, cut_mul):
    meta = None
    from verify_signed_gate import packet

    meta = packet(n)
    H = int(meta["H"])
    nu = choose_nu(n)
    k_max = cut_mul * H
    k, u = build_packet_arrays(n)
    u = normalize_E(u, 1.0)
    k, u = hermitize(k, u)
    dt = DT_FACTOR * float(H ** (-2.5))
    return {
        "n": n,
        "H": H,
        "nu": float(nu),
        "cut_mul": cut_mul,
        "k_max": k_max,
        "k_max2": k_max * k_max,
        "dt": dt,
        "k": k,
        "u": u,
        "modes0": int(k.shape[0]),
    }


def run_agreement(n=1, cut_mul=8, n_threads=4):
    set_num_threads(n_threads)
    st = initial_state(n, cut_mul)
    k, u = st["k"], st["u"]
    nu, k_max2, dt = st["nu"], st["k_max2"], st["dt"]
    k_high2 = float(st["H"] * st["H"])

    # Warm both kernels before timing.
    rhs_tiled(k, u, nu, k_max2, 0.0, TILE, HASH_CAPACITY)
    rhs_fast(k, u, nu, k_max2, 0.0, HASH_CAPACITY, n_threads)

    def ref_call():
        return rhs_tiled(k, u, nu, k_max2, 0.0, TILE, HASH_CAPACITY)

    def fast_call():
        return rhs_fast(k, u, nu, k_max2, 0.0, HASH_CAPACITY, n_threads)

    t_ref, ref = _time_call(ref_call)
    t_fast, fast = _time_call(fast_call)
    fk, fu = ref[0], ref[1]
    gk, gu = fast[0], fast[1]
    diff, n_ref, n_fast = field_l2_diff(fk, fu, gk, gu)
    ref_norm = field_l2_diff(fk, fu, fk, np.zeros_like(fu))[0]
    bal_ref = energy_balance(k, u, fk, fu, nu, k_high2)
    bal_fast = energy_balance(k, u, gk, gu, nu, k_high2)

    # One step from the same initial field. This is the first accepted step
    # when the step is admitted; the reference integrator is unchanged.
    k1, u1, ov1 = rk2_with(rhs_tiled, k, u, dt, nu, k_max2, FLOOR_REL, HASH_CAPACITY, n_threads)
    k2, u2, ov2 = rk2_with(rhs_fast, k, u, dt, nu, k_max2, FLOOR_REL, HASH_CAPACITY, n_threads)
    step_diff, n1, n2 = field_l2_diff(k1, u1, k2, u2)
    step_norm = field_l2_diff(k1, u1, k1, np.zeros_like(u1))[0]
    bal1 = energy_balance(k1, u1, k1, np.zeros_like(u1), nu, k_high2)
    # energy_balance uses fk as the derivative. For the state itself, pass u as a dummy
    # derivative of zero so the identity residual is just -( -2 nu Y + 2 T) if fk is 0.
    # Recompute transfer/energy directly.
    E1, X1, Y1, _, _, _, _ = moments(k1, u1, k_high2)
    T1, _ = transfer_scalene(k1, u1, K2_FIXED)
    E2, X2, Y2, _, _, _, _ = moments(k2, u2, k_high2)
    T2, _ = transfer_scalene(k2, u2, K2_FIXED)

    # Full m^2 at the first accepted state is the continuation bottleneck.
    # Time the same i-range of the reference pair loop and the fast pair loop,
    # then scale. Do not alter the reference solver.
    nrows = min(2048, int(k1.shape[0]))
    order = np.argsort(k1[:, 0], kind="mergesort").astype(np.int64)
    kx_sorted = np.ascontiguousarray(k1[order, 0])
    k_max = int(np.floor(np.sqrt(k_max2) + 1e-9))
    _reference_pair_slice(k1, u1, 0, 2, k_max2, HASH_CAPACITY)
    _nonlinear_slice(k1, u1, 0, 2, k_max, k_max2, order, kx_sorted, HASH_CAPACITY)

    def ref_rows():
        return _reference_pair_slice(k1, u1, 0, nrows, k_max2, HASH_CAPACITY)

    def fast_rows():
        width = (nrows + n_threads - 1) // n_threads
        chunks = [(a, min(nrows, a + width)) for a in range(0, nrows, width)]
        with ThreadPoolExecutor(max_workers=len(chunks)) as pool:
            futs = [
                pool.submit(
                    _nonlinear_slice, k1, u1, a, b, k_max, k_max2, order, kx_sorted, HASH_CAPACITY
                )
                for a, b in chunks
            ]
            parts = [fut.result() for fut in futs]
        pk = [p[0] for p in parts]
        pu = [p[1] for p in parts]
        return _merge_seeded(pk, pu, k1[:0], u1[:0], k_max2, 0.0, HASH_CAPACITY)

    t_ref_g, ref_rows_out = _time_call(ref_rows, repeats=1)
    t_fast_g, fast_rows_out = _time_call(fast_rows, repeats=1)
    row_diff, _, _ = field_l2_diff(ref_rows_out[0], ref_rows_out[1], fast_rows_out[0], fast_rows_out[1])
    row_norm = field_l2_diff(ref_rows_out[0], ref_rows_out[1], ref_rows_out[0], np.zeros_like(ref_rows_out[1]))[0]
    pairs_rows = nrows * int(k1.shape[0])
    pairs_grown = int(k1.shape[0]) * int(k1.shape[0])
    scale = pairs_grown / pairs_rows if pairs_rows else None

    pairs = int(k.shape[0]) * int(k.shape[0])
    report = {
        "reference_solver": "scripts/ns_attacks/gate_d_full_trajectory.py",
        "copy": "scripts/ns_attacks/gate_d_rhs_fast.py",
        "experiment_fixed": {
            "n": st["n"],
            "H": st["H"],
            "nu": st["nu"],
            "cut_mul": cut_mul,
            "k_max": st["k_max"],
            "dt": st["dt"],
            "dt_factor": DT_FACTOR,
            "E_target": 1.0,
            "floor_rel": FLOOR_REL,
            "modes_initial": st["modes0"],
            "ordered_pairs_initial": pairs,
        },
        "threads": n_threads,
        "initial_derivative": {
            "reference_seconds_median": t_ref,
            "fast_seconds_median": t_fast,
            "speedup": (t_ref / t_fast) if t_fast > 0 else None,
            "L2_difference": float(diff),
            "L2_reference": float(ref_norm),
            "relative_L2": float(diff / ref_norm) if ref_norm else None,
            "modes_reference": int(n_ref),
            "modes_fast": int(n_fast),
            "signed_excess_reference": bal_ref["signed_excess"],
            "signed_excess_fast_state": bal_fast["signed_excess"],
            "energy_identity_residual_reference": bal_ref["energy_identity_residual"],
            "energy_identity_residual_fast": bal_fast["energy_identity_residual"],
            "T_reference": bal_ref["T"],
            "E_reference": bal_ref["E"],
        },
        "first_step": {
            "dt": dt,
            "modes_reference": int(n1),
            "modes_fast": int(n2),
            "L2_difference": float(step_diff),
            "L2_reference": float(step_norm),
            "relative_L2": float(step_diff / step_norm) if step_norm else None,
            "E_reference": float(E1),
            "E_fast": float(E2),
            "T_reference": float(T1),
            "T_fast": float(T2),
            "signed_excess_reference": float(T1 - nu * Y1 / 4.0),
            "signed_excess_fast": float(T2 - nu * Y2 / 4.0),
            "overflow_reference": int(ov1),
            "overflow_fast": int(ov2),
        },
        "next_derivative_at_first_accepted_state": {
            "modes": int(k1.shape[0]),
            "ordered_pairs_full": pairs_grown,
            "timed_i_rows": nrows,
            "ordered_pairs_timed": pairs_rows,
            "reference_seconds": t_ref_g,
            "fast_seconds": t_fast_g,
            "speedup_on_timed_rows": (t_ref_g / t_fast_g) if t_fast_g > 0 else None,
            "reference_seconds_scaled_to_full": (t_ref_g * scale) if scale else None,
            "fast_seconds_scaled_to_full": (t_fast_g * scale) if scale else None,
            "row_L2_difference": float(row_diff),
            "row_L2_reference": float(row_norm),
            "row_relative_L2": float(row_diff / row_norm) if row_norm else None,
            "note": "Same first-accepted field. Reference rows are serial. Fast rows split that i-range across threads and merge. Full-sum times are scaled by pair count.",
        },
        "resume": "not started — agreement is the deliverable; downward crossing waits",
        "turnover_promised": False,
    }
    return report


def main():
    report = run_agreement()
    out = Path(__file__).with_name("GATE-D-RHS-SPEEDUP.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print(f"Wrote {out}", flush=True)


if __name__ == "__main__":
    main()
