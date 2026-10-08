#!/usr/bin/env python3
"""Gate D adversarial run: six-box Signed-Gate packet, full Galerkin.

Numerical evidence only. No theorem stamp.
Adversary: verify_signed_gate.packet — imaginary-coefficient six-box.
Do not substitute a Gaussian or real-coefficient Gate-B construction.

Method
------
Sparse spectral Galerkin on the ball |k|^2 <= (4H)^2. The nonlinear term is
the exact truncated convolution over the retained modes (full interactions
among retained degrees of freedom; not a triad-only model). After each Euler
step the largest M modes by |û|^2 are kept (default M=2500) so the active set
stays tractable over the long first episode. Energy-identity checks at t=0
confirm X' = -2νY + 2T_sc on the signed packet.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from numba import njit

from verify_signed_gate import box, packet, polarization


def choose_nu(n: int, safety: float = 0.25) -> float:
    """ν = safety * 4 * (T/(sqrt(E) Y)) so D(0)=T-νY/4 > 0 at E=1."""
    raw = packet(n)
    E = float(raw["E"])
    Y = float(raw["Y"])
    T = float(raw["T_scalene"])
    return float(safety * 4.0 * T / (np.sqrt(E) * Y))


def build_packet_arrays(n: int):
    L = 64 * n
    P = box((L, 0, 0), n)
    Q = box((0, 3 * L, 0), n)
    R = box((L, 3 * L, 0), 2 * n)
    ks, us, seen = [], [], set()
    for modes, j in ((P, 1), (Q, 2), (R, 2)):
        for k in modes:
            for kk, sign in ((k, 1), ((-k[0], -k[1], -k[2]), -1)):
                if kk in seen:
                    continue
                seen.add(kk)
                v = polarization(k, j)
                if sign < 0:
                    v = (-v[0], -v[1], -v[2])
                ks.append(kk)
                us.append([1j * v[0], 1j * v[1], 1j * v[2]])
    return np.asarray(ks, dtype=np.int32), np.asarray(us, dtype=np.complex128)


def normalize_E(u, E_target=1.0):
    E = np.sum(np.abs(u) ** 2).real
    return u * np.sqrt(E_target / E)


@njit(cache=True)
def moments(k, u, k_high2):
    E = X = Y = X_H = Y_H = U = W = 0.0
    for i in range(k.shape[0]):
        a = float(k[i, 0] * k[i, 0] + k[i, 1] * k[i, 1] + k[i, 2] * k[i, 2])
        mag2 = 0.0
        for c in range(3):
            mag2 += u[i, c].real * u[i, c].real + u[i, c].imag * u[i, c].imag
        amp = np.sqrt(mag2)
        E += mag2
        X += a * mag2
        Y += a * a * mag2
        U += amp
        W += a * amp
        if a >= k_high2:
            X_H += a * mag2
            Y_H += a * a * mag2
    return E, X, Y, X_H, Y_H, U, W


@njit(cache=True)
def transfer_scalene(k, u, k_high2):
    m = k.shape[0]
    w = np.empty((m, 3), dtype=np.float64)
    rad = np.empty(m, dtype=np.float64)
    active = np.empty(m, dtype=np.int64)
    n_act = 0
    for i in range(m):
        ai = float(k[i, 0] * k[i, 0] + k[i, 1] * k[i, 1] + k[i, 2] * k[i, 2])
        rad[i] = ai
        if ai < k_high2 or ai == 0.0:
            continue
        for c in range(3):
            w[i, c] = u[i, c].imag
        active[n_act] = i
        n_act += 1
    if n_act == 0:
        return 0.0, 0
    capacity = 1
    while capacity < n_act * 4:
        capacity *= 2
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    vals = np.empty(capacity, dtype=np.int32)
    used = np.zeros(capacity, dtype=np.uint8)
    for ii in range(n_act):
        i = active[ii]
        h = (k[i, 0] * 73856093 + k[i, 1] * 19349663 + k[i, 2] * 83492791) & (
            capacity - 1
        )
        while used[h] != 0:
            h = (h + 1) & (capacity - 1)
        used[h] = 1
        hk0[h] = k[i, 0]
        hk1[h] = k[i, 1]
        hk2[h] = k[i, 2]
        vals[h] = i
    T = 0.0
    for ii in range(n_act):
        i = active[ii]
        ai = rad[i]
        for jj in range(n_act):
            j = active[jj]
            bj = rad[j]
            kx = k[i, 0] + k[j, 0]
            ky = k[i, 1] + k[j, 1]
            kz = k[i, 2] + k[j, 2]
            h = (kx * 73856093 + ky * 19349663 + kz * 83492791) & (capacity - 1)
            recv = -1
            probes = 0
            while used[h] != 0 and probes < capacity:
                if hk0[h] == kx and hk1[h] == ky and hk2[h] == kz:
                    recv = vals[h]
                    break
                h = (h + 1) & (capacity - 1)
                probes += 1
            if recv < 0:
                continue
            c = rad[recv]
            if ai == bj or ai == c or bj == c:
                continue
            qdot = k[j, 0] * w[i, 0] + k[j, 1] * w[i, 1] + k[j, 2] * w[i, 2]
            wqwk = w[j, 0] * w[recv, 0] + w[j, 1] * w[recv, 1] + w[j, 2] * w[recv, 2]
            T += c * qdot * wqwk
    return T, n_act


@njit(cache=True)
def prune(k, u, mag2_floor):
    m = k.shape[0]
    keep = np.zeros(m, dtype=np.uint8)
    n_keep = 0
    for i in range(m):
        mag2 = 0.0
        for c in range(3):
            mag2 += u[i, c].real * u[i, c].real + u[i, c].imag * u[i, c].imag
        if mag2 >= mag2_floor:
            keep[i] = 1
            n_keep += 1
    out_k = np.empty((n_keep, 3), dtype=np.int32)
    out_u = np.empty((n_keep, 3), dtype=np.complex128)
    j = 0
    for i in range(m):
        if keep[i] == 0:
            continue
        out_k[j, 0] = k[i, 0]
        out_k[j, 1] = k[i, 1]
        out_k[j, 2] = k[i, 2]
        out_u[j, 0] = u[i, 0]
        out_u[j, 1] = u[i, 1]
        out_u[j, 2] = u[i, 2]
        j += 1
    return out_k, out_u


@njit(cache=True)
def hermitize(k, u):
    m = k.shape[0]
    capacity = 1
    while capacity < m * 4 + 8:
        capacity *= 2
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    n_fill = 0
    for i in range(m):
        for side in range(2):
            if side == 0:
                kx, ky, kz = k[i, 0], k[i, 1], k[i, 2]
                v0, v1, v2 = u[i, 0], u[i, 1], u[i, 2]
            else:
                kx, ky, kz = -k[i, 0], -k[i, 1], -k[i, 2]
                v0, v1, v2 = np.conj(u[i, 0]), np.conj(u[i, 1]), np.conj(u[i, 2])
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
                n_fill += 1
            acc[h, 0] += 0.5 * v0
            acc[h, 1] += 0.5 * v1
            acc[h, 2] += 0.5 * v2
    out_k = np.empty((n_fill, 3), dtype=np.int32)
    out_u = np.empty((n_fill, 3), dtype=np.complex128)
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
    return out_k[:idx], out_u[:idx]


@njit(cache=True)
def rhs_sparse(k, u, nu, k_max2, out_floor):
    m = k.shape[0]
    capacity = 1
    target = min(m * m + m + 16, 120000)
    while capacity < target:
        capacity *= 2
    hk0 = np.empty(capacity, dtype=np.int32)
    hk1 = np.empty(capacity, dtype=np.int32)
    hk2 = np.empty(capacity, dtype=np.int32)
    acc = np.zeros((capacity, 3), dtype=np.complex128)
    used = np.zeros(capacity, dtype=np.uint8)
    seeded = np.zeros(capacity, dtype=np.uint8)
    n_fill = 0

    for i in range(m):
        a = k[i, 0] * k[i, 0] + k[i, 1] * k[i, 1] + k[i, 2] * k[i, 2]
        if a > k_max2 or a == 0:
            continue
        h = (k[i, 0] * 73856093 + k[i, 1] * 19349663 + k[i, 2] * 83492791) & (
            capacity - 1
        )
        while used[h] != 0:
            if hk0[h] == k[i, 0] and hk1[h] == k[i, 1] and hk2[h] == k[i, 2]:
                break
            h = (h + 1) & (capacity - 1)
        if used[h] == 0:
            used[h] = 1
            seeded[h] = 1
            hk0[h], hk1[h], hk2[h] = k[i, 0], k[i, 1], k[i, 2]
            n_fill += 1
        else:
            seeded[h] = 1
        acc[h, 0] += -nu * a * u[i, 0]
        acc[h, 1] += -nu * a * u[i, 1]
        acc[h, 2] += -nu * a * u[i, 2]

    for i in range(m):
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
            # ∂t û = -ν|k|^2 û - i P[(û_p·q)û_q]  (torus convention; X'=-2νY+2T)
            n0 = -1j * p0
            n1 = -1j * p1
            n2 = -1j * p2
            h = (kx * 73856093 + ky * 19349663 + kz * 83492791) & (capacity - 1)
            probes = 0
            while used[h] != 0 and probes < capacity:
                if hk0[h] == kx and hk1[h] == ky and hk2[h] == kz:
                    break
                h = (h + 1) & (capacity - 1)
                probes += 1
            if used[h] == 0:
                if n_fill >= capacity // 2:
                    continue
                used[h] = 1
                hk0[h], hk1[h], hk2[h] = kx, ky, kz
                n_fill += 1
            acc[h, 0] += n0
            acc[h, 1] += n1
            acc[h, 2] += n2

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
    return out_k, out_u


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


def keep_top_modes(k, u, M):
    if k.shape[0] <= M:
        return k, u
    mag2 = np.sum(np.abs(u) ** 2, axis=1).real
    idx = np.argsort(mag2)[-M:]
    return k[idx].copy(), u[idx].copy()


def euler_step(k, u, dt, nu, k_max2, floor, Mcap):
    fk, fu = rhs_sparse(k, u, nu, k_max2, floor)
    k2, u2 = merge_axpy(k, u, fk, fu, dt, k_max2, floor)
    k2, u2 = hermitize(k2, u2)
    k2, u2 = prune(k2, u2, floor)
    k2, u2 = keep_top_modes(k2, u2, Mcap)
    k2, u2 = hermitize(k2, u2)
    return k2, u2


def measure_episode(
    n,
    nu,
    t_max_factor=2500.0,
    dt_factor=2.0,
    floor_rel=1e-16,
    Mcap=2500,
):
    meta = packet(n)
    H = int(meta["H"])
    k_high2 = H * H
    k_max2 = (4 * H) * (4 * H)
    k, u = build_packet_arrays(n)
    u = normalize_E(u, 1.0)
    k, u = hermitize(k, u)

    T_expected = float(meta["T_scalene"]) / (float(meta["E"]) ** 1.5)

    _ = transfer_scalene(k, u, float(k_high2))
    _ = rhs_sparse(k, u, nu, k_max2, floor_rel)

    t_wall = time.time()
    E0, X0, Y0, X_H0, Y_H0, U0, W0 = moments(k, u, float(k_high2))
    T0, n0 = transfer_scalene(k, u, float(k_high2))
    D0 = T0 - nu * Y_H0 / 4.0

    # Energy identity check: X' ?= -2νY + 2T
    fk, fu = rhs_sparse(k, u, nu, k_max2, 0.0)
    fd = {(int(fk[i, 0]), int(fk[i, 1]), int(fk[i, 2])): fu[i] for i in range(fk.shape[0])}
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
    Te, _ = transfer_scalene(be_k, be_u, float(k_high2))
    _, _, _, _, YHe, _, _ = moments(be_k, be_u, float(k_high2))
    Dp = ((Te - nu * YHe / 4.0) - D0) / eps

    tau_nl = float(H ** (-2.5))
    dt = dt_factor * tau_nl
    t_max = t_max_factor * tau_nl

    times = [0.0]
    Ds = [float(D0)]
    Xs = [float(X_H0)]
    UWs = [float(U0 * W0)]
    Ts = [float(T0)]

    t = 0.0
    episode_start = 0.0 if D0 > 0 else None
    episode_end = None
    B_acc = R_UW_acc = R_X_acc = 0.0
    steps = 0
    status_detail = "RUNNING"
    max_modes = int(k.shape[0])

    print(
        f"  t0: D={D0:.6e} Dp={Dp:.6e} T_err={(T0-T_expected)/abs(T_expected):.3e} "
        f"X'_res={identity_residual:.3e} modes={k.shape[0]}",
        flush=True,
    )

    while t < t_max:
        k, u = euler_step(k, u, dt, nu, k_max2, floor_rel, Mcap)
        t += dt
        steps += 1
        max_modes = max(max_modes, int(k.shape[0]))

        E, X, Y, X_H, Y_H, U, W = moments(k, u, float(k_high2))
        Tsc, n_act = transfer_scalene(k, u, float(k_high2))
        D = Tsc - nu * Y_H / 4.0
        times.append(t)
        Ds.append(float(D))
        Xs.append(float(X_H))
        UWs.append(float(U * W))
        Ts.append(float(Tsc))

        if episode_start is None:
            if Ds[-2] <= 0.0 < D:
                frac = -Ds[-2] / (D - Ds[-2])
                episode_start = times[-2] + frac * dt
                B_acc = 0.5 * (D / max(X_H, 1e-300)) * (t - episode_start)
                uw_c = UWs[-2] + frac * (UWs[-1] - UWs[-2])
                R_UW_acc = 0.5 * (uw_c + UWs[-1]) * (t - episode_start)
                x_c = Xs[-2] + frac * (Xs[-1] - Xs[-2])
                R_X_acc = 0.5 * (x_c + Xs[-1]) * (t - episode_start)
        else:
            Xp, Xc = max(Xs[-2], 1e-300), max(Xs[-1], 1e-300)
            B_acc += 0.5 * (Ds[-2] / Xp + Ds[-1] / Xc) * dt
            R_UW_acc += 0.5 * (UWs[-2] + UWs[-1]) * dt
            R_X_acc += 0.5 * (Xs[-2] + Xs[-1]) * dt
            if Ds[-2] > 0.0 >= D:
                frac = Ds[-2] / (Ds[-2] - D)
                episode_end = times[-2] + frac * dt
                B_acc -= 0.5 * (Ds[-2] / Xp + Ds[-1] / Xc) * dt
                R_UW_acc -= 0.5 * (UWs[-2] + UWs[-1]) * dt
                R_X_acc -= 0.5 * (Xs[-2] + Xs[-1]) * dt
                seg = episode_end - times[-2]
                x_end = Xs[-2] + frac * (Xs[-1] - Xs[-2])
                uw_end = UWs[-2] + frac * (UWs[-1] - UWs[-2])
                B_acc += 0.5 * (Ds[-2] / Xp) * seg
                R_UW_acc += 0.5 * (UWs[-2] + uw_end) * seg
                R_X_acc += 0.5 * (Xs[-2] + x_end) * seg
                status_detail = "COMPLETE_FIRST_EPISODE"
                break

        if steps <= 5 or steps % 50 == 0:
            print(
                f"  step={steps} t/tau={t/tau_nl:.2f} D={D:.4e} T={Tsc:.4e} "
                f"B={B_acc:.4e} modes={k.shape[0]} E={E:.5f}",
                flush=True,
            )

    if episode_start is not None and episode_end is None and status_detail == "RUNNING":
        episode_end = t
        status_detail = "TRUNCATED_POSITIVE_EPISODE"
    if episode_start is None and status_detail == "RUNNING":
        status_detail = "NO_POSITIVE_EPISODE_IN_WINDOW"

    I_len = (
        None
        if episode_start is None or episode_end is None
        else float(episode_end - episode_start)
    )

    # Single-n reading against the three-way score (family needs multiple H)
    reading = None
    if status_detail == "COMPLETE_FIRST_EPISODE":
        if abs(B_acc) < 1e-2:
            reading = "B_small_at_this_H — need H-family to test B->0"
        elif R_UW_acc >= 0.1:
            reading = "B_finite_with_large_UW_resource_spend — not the dangerous o(1)-resource case"
        else:
            reading = "CHECK: B_O(1)_with_small_UW — potential Gate D damage"

    return {
        "n": n,
        "H": H,
        "nu": nu,
        "E": 1.0,
        "k_high": H,
        "k_max": 4 * H,
        "method": "sparse_Galerkin_ball_4H_euler_topM",
        "Mcap": Mcap,
        "floor_rel": floor_rel,
        "modes_initial": int(meta["modes"]),
        "modes_max_observed": max_modes,
        "T_sc_E1": float(T0),
        "T_sc_E1_expected_from_verifier": float(T_expected),
        "T_sc_rel_err_vs_verifier": float((T0 - T_expected) / abs(T_expected)),
        "energy_identity_Xprime_residual": float(identity_residual),
        "active_high_modes_t0": int(n0),
        "X_H(0)": float(X_H0),
        "Y_H(0)": float(Y_H0),
        "U(0)": float(U0),
        "W(0)": float(W0),
        "D_H(0)": float(D0),
        "D_H_prime(0)": float(Dp),
        "episode_start": episode_start,
        "episode_end": episode_end,
        "I_H_length": I_len,
        "H^{5/2}|I_H|": None if I_len is None else float((H**2.5) * I_len),
        "B_IH": None if episode_start is None else float(B_acc),
        "resource_UW_integral": None if episode_start is None else float(R_UW_acc),
        "resource_X_integral_DIAGNOSTIC_ruled_out": None
        if episode_start is None
        else float(R_X_acc),
        "B_over_resource_UW": (
            None
            if episode_start is None or R_UW_acc == 0
            else float(B_acc / R_UW_acc)
        ),
        "episode_truncated": status_detail == "TRUNCATED_POSITIVE_EPISODE",
        "steps": steps,
        "dt": dt,
        "dt_factor": dt_factor,
        "t_max": t_max,
        "tau_nl_H^{-5/2}": tau_nl,
        "wall_seconds": time.time() - t_wall,
        "status": "NUMERICAL_EVIDENCE_ONLY",
        "status_detail": status_detail,
        "single_n_reading": reading,
        "theorem_stamp": False,
        "U0": float(U0),
        "small_l1_hypothesis_U0_le_nu/4": bool(U0 <= nu / 4.0),
        "prototype_UW_integral_ceiling": (
            float((U0**2) / (2.0 * (nu - U0))) if U0 < nu else None
        ),
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
    ap.add_argument("--t-max-factor", type=float, default=2500.0)
    ap.add_argument("--dt-factor", type=float, default=2.0)
    ap.add_argument("--floor-rel", type=float, default=1e-16)
    ap.add_argument("--Mcap", type=int, default=2500)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("GATE-D-ADVERSARIAL-RUN.json"),
    )
    args = ap.parse_args()

    runs = []
    for n in args.n:
        nu = args.nu if args.nu is not None else choose_nu(n)
        print(f"=== Gate D run n={n} H={63*n} nu={nu:.6e} ===", flush=True)
        rec = measure_episode(
            n,
            nu,
            t_max_factor=args.t_max_factor,
            dt_factor=args.dt_factor,
            floor_rel=args.floor_rel,
            Mcap=args.Mcap,
        )
        keys = [
            "n", "H", "nu", "D_H(0)", "D_H_prime(0)", "I_H_length",
            "H^{5/2}|I_H|", "B_IH", "resource_UW_integral",
            "resource_X_integral_DIAGNOSTIC_ruled_out", "B_over_resource_UW",
            "status_detail", "single_n_reading", "T_sc_rel_err_vs_verifier",
            "energy_identity_Xprime_residual", "modes_max_observed",
            "wall_seconds", "theorem_stamp",
        ]
        print(json.dumps({k: rec.get(k) for k in keys}, indent=2), flush=True)
        runs.append(rec)

    payload = {
        "title": "Gate D adversarial run — numerical evidence",
        "adversary": "Signed-Gate-B-Sharp-Band-Exponent-2026-10-07 six-box",
        "theorem_stamp": False,
        "gaussian_substituted": False,
        "scoring_note": (
            "Family score (B->0 / O(1)+O(1) resource / dangerous O(1)+o(1) resource) "
            "requires multiple H=63n. Single-n readings are diagnostics only."
        ),
        "runs": runs,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
