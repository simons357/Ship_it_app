#!/usr/bin/env python3
"""Gate D full-trajectory FFT Galerkin — six-box Signed-Gate, no top-M.

Memory-frugal rfft path for the ball |k| <= cut_mul*H. Preserves the
signed-scalene diagnostic (exact T_sc on modes above a numerical-zero floor).
No energy-ranking top-M prune. No Gaussian substitute.

Score: B_I / R_I with boundary term (b-a)*d(a) when d(a)>0.
Numerical evidence only. No theorem stamp. Not (17).
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import numpy as np
from scipy import fft as sp_fft

from verify_signed_gate import packet
from gate_d_adversarial_run import build_packet_arrays, choose_nu, normalize_E
from gate_d_adversarial_run import transfer_scalene

# Threaded FFTs (N=512 rfft is the step bottleneck).
_FFT_WORKERS = max(1, int(os.environ.get("GATE_D_FFT_WORKERS", "4")))


def next_fft_n(k_max: int) -> int:
    need = 2 * k_max + 1
    n = 1
    while n < need:
        n *= 2
    return n


def freq_1d(N: int):
    kx = np.fft.fftfreq(N, d=1.0 / N).astype(np.float32)
    ky = np.fft.fftfreq(N, d=1.0 / N).astype(np.float32)
    kz = np.fft.rfftfreq(N, d=1.0 / N).astype(np.float32)
    return kx, ky, kz


def k2_grid(kx, ky, kz):
    return (
        kx[:, None, None] ** 2 + ky[None, :, None] ** 2 + kz[None, None, :] ** 2
    ).astype(np.float32)


def embed_packet_rfft(k, u, N, k_max2):
    """Hermitian embed via full complex grid → real field → rfft."""
    uc = np.zeros((N, N, N, 3), dtype=np.complex64)
    for i in range(k.shape[0]):
        kx, ky, kz = int(k[i, 0]), int(k[i, 1]), int(k[i, 2])
        a = kx * kx + ky * ky + kz * kz
        if a == 0 or a > k_max2:
            continue
        uc[kx % N, ky % N, kz % N] = u[i].astype(np.complex64)
    phys = np.empty((N, N, N, 3), dtype=np.float32)
    with sp_fft.set_workers(_FFT_WORKERS):
        for c in range(3):
            phys[..., c] = (
                sp_fft.ifftn(uc[..., c], axes=(0, 1, 2)).real * (N**3)
            ).astype(np.float32)
    del uc
    uh = np.empty((N, N, N // 2 + 1, 3), dtype=np.complex64)
    with sp_fft.set_workers(_FFT_WORKERS):
        for c in range(3):
            uh[..., c] = (
                sp_fft.rfftn(phys[..., c], axes=(0, 1, 2)).astype(np.complex64) / (N**3)
            )
    del phys
    return uh


def project_ball(uh, K2, k_max2):
    ball = K2 <= float(k_max2)
    out = np.empty_like(uh)
    for c in range(3):
        out[..., c] = np.where(ball, uh[..., c], np.complex64(0))
    out[0, 0, 0] = 0
    return out


def leray_inplace(fx, fy, fz, kx, ky, kz, K2):
    inv = np.zeros_like(K2)
    mask = K2 > 0
    inv[mask] = 1.0 / K2[mask]
    kdot = (
        kx[:, None, None] * fx + ky[None, :, None] * fy + kz[None, None, :] * fz
    ) * inv
    fx -= kx[:, None, None] * kdot
    fy -= ky[None, :, None] * kdot
    fz -= kz[None, None, :] * kdot
    fx[0, 0, 0] = 0
    fy[0, 0, 0] = 0
    fz[0, 0, 0] = 0
    return fx, fy, fz


def rhs_fft(uh, nu, kx, ky, kz, K2, k_max2, N):
    """Memory-frugal ∂t û = -ν|k|²û - P[(u·∇)u].

    ``uh`` stores Fourier coefficients û in the sum-convention
    (phys = ∑ û e^{ik·x}). NumPy irfftn(uh) returns phys/N³, so restore
    the factor N³ on every physical field.
    """
    axes = (0, 1, 2)
    n3 = float(N**3)
    u_phys = np.empty((N, N, N, 3), dtype=np.float32)
    with sp_fft.set_workers(_FFT_WORKERS):
        for c in range(3):
            u_phys[..., c] = (
                sp_fft.irfftn(uh[..., c], s=(N, N, N), axes=axes).astype(np.float32)
                * n3
            )

        adv = np.zeros_like(u_phys)
        for c in range(3):
            tmp = (
                sp_fft.irfftn(
                    (1j * kx[:, None, None] * uh[..., c]).astype(np.complex64),
                    s=(N, N, N),
                    axes=axes,
                ).real.astype(np.float32)
                * n3
            )
            adv[..., c] += u_phys[..., 0] * tmp
            tmp = (
                sp_fft.irfftn(
                    (1j * ky[None, :, None] * uh[..., c]).astype(np.complex64),
                    s=(N, N, N),
                    axes=axes,
                ).real.astype(np.float32)
                * n3
            )
            adv[..., c] += u_phys[..., 1] * tmp
            tmp = (
                sp_fft.irfftn(
                    (1j * kz[None, None, :] * uh[..., c]).astype(np.complex64),
                    s=(N, N, N),
                    axes=axes,
                ).real.astype(np.float32)
                * n3
            )
            adv[..., c] += u_phys[..., 2] * tmp
        del u_phys, tmp

        fx = sp_fft.rfftn(adv[..., 0], axes=axes).astype(np.complex64) / n3
        fy = sp_fft.rfftn(adv[..., 1], axes=axes).astype(np.complex64) / n3
        fz = sp_fft.rfftn(adv[..., 2], axes=axes).astype(np.complex64) / n3
    del adv
    fx, fy, fz = leray_inplace(fx, fy, fz, kx, ky, kz, K2)

    damp = (nu * K2).astype(np.float32)
    ball = K2 <= float(k_max2)
    out = np.empty_like(uh)
    for c, fcomp in enumerate((fx, fy, fz)):
        out[..., c] = np.where(ball, -fcomp - damp * uh[..., c], np.complex64(0))
    out[0, 0, 0] = 0
    return out


def moments_grid(uh, K2, k_high2):
    mag2 = np.sum(np.abs(uh) ** 2, axis=3).astype(np.float64)
    mult = np.ones_like(mag2)
    mult[:, :, 1:] = 2.0
    E = float(np.sum(mult * mag2))
    X = float(np.sum(mult * K2 * mag2))
    Y = float(np.sum(mult * (K2.astype(np.float64) ** 2) * mag2))
    high = K2 >= float(k_high2)
    X_H = float(np.sum(mult * K2 * mag2 * high))
    Y_H = float(np.sum(mult * (K2.astype(np.float64) ** 2) * mag2 * high))
    amp = np.sqrt(np.maximum(mag2, 0.0))
    U = float(np.sum(mult * amp))
    W = float(np.sum(mult * K2 * amp))
    return E, X, Y, X_H, Y_H, U, W


def sparse_from_grid(uh, kx, ky, kz, K2, k_max2, floor_mag2):
    mag2 = np.sum(np.abs(uh) ** 2, axis=3)
    sel = (K2 <= float(k_max2)) & (K2 > 0) & (mag2 >= floor_mag2)
    ix, iy, iz = np.where(sel)
    if ix.size == 0:
        return (
            np.zeros((0, 3), dtype=np.int32),
            np.zeros((0, 3), dtype=np.complex128),
        )
    ks = []
    us = []
    for a, b, c in zip(ix.tolist(), iy.tolist(), iz.tolist()):
        kx_i = int(round(float(kx[a])))
        ky_i = int(round(float(ky[b])))
        kz_i = int(round(float(kz[c])))
        v = uh[a, b, c].astype(np.complex128)
        ks.append((kx_i, ky_i, kz_i))
        us.append(v)
        if kz_i > 0:
            ks.append((-kx_i, -ky_i, -kz_i))
            us.append(np.conj(v))
    return np.asarray(ks, dtype=np.int32), np.asarray(us, dtype=np.complex128)


def measure_episode(
    n,
    nu,
    *,
    cut_mul=4,
    t_max_factor=2500.0,
    dt_factor=2.0,
    floor_rel=1e-18,
    max_steps=None,
    smoke=False,
):
    meta = packet(n)
    H = int(meta["H"])
    k_high2 = H * H
    k_max = cut_mul * H
    k_max2 = k_max * k_max
    N = next_fft_n(k_max)

    k, u = build_packet_arrays(n)
    u = normalize_E(u, 1.0)

    t_wall = time.time()
    print(f"  embedding packet on N={N} (cut={cut_mul}H={k_max}) ...", flush=True)
    uh = embed_packet_rfft(k, u, N, k_max2)
    kx, ky, kz = freq_1d(N)
    K2 = k2_grid(kx, ky, kz)
    uh = project_ball(uh, K2, k_max2)

    E0, X0, Y0, X_H0, Y_H0, U0, W0 = moments_grid(uh, K2, k_high2)
    uh *= np.float32(np.sqrt(1.0 / max(E0, 1e-300)))
    E0, X0, Y0, X_H0, Y_H0, U0, W0 = moments_grid(uh, K2, k_high2)

    floor_mag2 = floor_rel
    ks, us = sparse_from_grid(uh, kx, ky, kz, K2, k_max2, floor_mag2)
    T0, n_act = transfer_scalene(ks, us, float(k_high2))
    T_expected = float(meta["T_scalene"]) / (float(meta["E"]) ** 1.5)
    D0 = T0 - nu * Y_H0 / 4.0
    d0 = D0 / max(X_H0, 1e-300)

    f0 = rhs_fft(uh, nu, kx, ky, kz, K2, k_max2, N)
    # float32 RHS: use a larger probe than 1e-8 so D' is not lost to roundoff
    eps = 1e-5
    uh_eps = project_ball(uh + np.float32(eps) * f0, K2, k_max2)
    _, _, _, _, YHe, _, _ = moments_grid(uh_eps, K2, k_high2)
    ks_e, us_e = sparse_from_grid(uh_eps, kx, ky, kz, K2, k_max2, floor_mag2)
    Te, _ = transfer_scalene(ks_e, us_e, float(k_high2))
    Dp = ((Te - nu * YHe / 4.0) - D0) / eps

    _, Xeps, Yeps, _, _, _, _ = moments_grid(uh_eps, K2, k_high2)
    Xp = (Xeps - X0) / eps
    identity_residual = Xp - (-2 * nu * Y0 + 2 * T0)
    del uh_eps, f0

    tau_nl = float(H ** (-2.5))
    dt = dt_factor * tau_nl
    t_max = (5.0 if smoke else t_max_factor) * tau_nl
    if max_steps is None:
        max_steps = 8 if smoke else 10**9

    times = [0.0]
    Ds = [float(D0)]
    Xs = [float(X_H0)]
    UWs = [float(U0 * W0)]
    Ts = [float(T0)]

    t = 0.0
    episode_start = 0.0 if D0 > 0 else None
    episode_end = None
    B_trap = R_UW_acc = R_X_acc = 0.0
    steps = 0
    status_detail = "RUNNING"
    extract_max = int(ks.shape[0])

    print(
        f"  t0: extract={ks.shape[0]} D={D0:.6e} d={d0:.6e} Dp={Dp:.6e} "
        f"T_err={(T0 - T_expected) / abs(T_expected):.3e} "
        f"X'_res={identity_residual:.3e} E={E0:.6f}",
        flush=True,
    )

    while t < t_max and steps < max_steps:
        f1 = rhs_fft(uh, nu, kx, ky, kz, K2, k_max2, N)
        mid = project_ball(uh + np.float32(0.5 * dt) * f1, K2, k_max2)
        del f1
        f2 = rhs_fft(mid, nu, kx, ky, kz, K2, k_max2, N)
        del mid
        uh = project_ball(uh + np.float32(dt) * f2, K2, k_max2)
        del f2
        t += dt
        steps += 1

        E, X, Y, X_H, Y_H, U, W = moments_grid(uh, K2, k_high2)
        ks, us = sparse_from_grid(uh, kx, ky, kz, K2, k_max2, floor_mag2)
        extract_max = max(extract_max, int(ks.shape[0]))
        Tsc, _ = transfer_scalene(ks, us, float(k_high2))
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
                B_trap = 0.5 * (D / max(X_H, 1e-300)) * (t - episode_start)
                uw_c = UWs[-2] + frac * (UWs[-1] - UWs[-2])
                R_UW_acc = 0.5 * (uw_c + UWs[-1]) * (t - episode_start)
                x_c = Xs[-2] + frac * (Xs[-1] - Xs[-2])
                R_X_acc = 0.5 * (x_c + Xs[-1]) * (t - episode_start)
        else:
            Xp_, Xc = max(Xs[-2], 1e-300), max(Xs[-1], 1e-300)
            B_trap += 0.5 * (Ds[-2] / Xp_ + Ds[-1] / Xc) * dt
            R_UW_acc += 0.5 * (UWs[-2] + UWs[-1]) * dt
            R_X_acc += 0.5 * (Xs[-2] + Xs[-1]) * dt
            if Ds[-2] > 0.0 >= D:
                frac = Ds[-2] / (Ds[-2] - D)
                episode_end = times[-2] + frac * dt
                B_trap -= 0.5 * (Ds[-2] / Xp_ + Ds[-1] / Xc) * dt
                R_UW_acc -= 0.5 * (UWs[-2] + UWs[-1]) * dt
                R_X_acc -= 0.5 * (Xs[-2] + Xs[-1]) * dt
                seg = episode_end - times[-2]
                x_end = Xs[-2] + frac * (Xs[-1] - Xs[-2])
                uw_end = UWs[-2] + frac * (UWs[-1] - UWs[-2])
                B_trap += 0.5 * (Ds[-2] / Xp_) * seg
                R_UW_acc += 0.5 * (UWs[-2] + uw_end) * seg
                R_X_acc += 0.5 * (Xs[-2] + x_end) * seg
                status_detail = "COMPLETE_FIRST_EPISODE"
                break

        if steps <= 5 or steps % 10 == 0:
            print(
                f"  step={steps} t/tau={t / tau_nl:.2f} D={D:.4e} T={Tsc:.4e} "
                f"B_trap={B_trap:.4e} extract={ks.shape[0]} E={E:.5f}",
                flush=True,
            )

    if episode_start is not None and episode_end is None:
        episode_end = t
        if status_detail == "RUNNING":
            status_detail = "TRUNCATED_POSITIVE_EPISODE"
    if episode_start is None and status_detail == "RUNNING":
        status_detail = "NO_POSITIVE_EPISODE_IN_WINDOW"
    if smoke and status_detail == "RUNNING":
        status_detail = "SMOKE_OK"

    I_len = (
        None
        if episode_start is None or episode_end is None
        else float(episode_end - episode_start)
    )
    boundary = 0.0
    if (
        episode_start is not None
        and episode_end is not None
        and d0 > 0
        and abs(episode_start) < 1e-30
    ):
        boundary = float(I_len) * float(d0)
    B_IH = None if episode_start is None else float(B_trap + boundary)
    R_UW = None if episode_start is None else float(R_UW_acc)
    B_over_R = (
        None if B_IH is None or R_UW is None or R_UW == 0.0 else float(B_IH / R_UW)
    )

    return {
        "n": n,
        "H": H,
        "nu": nu,
        "E": float(E0),
        "fft_N": N,
        "k_high": H,
        "k_max": k_max,
        "cut_mul": cut_mul,
        "method": "fft_Galerkin_rfft_complex64_rk2_no_topM",
        "topM": False,
        "floor_rel": floor_rel,
        "extract_modes_max": extract_max,
        "T_sc_E1": float(T0),
        "T_sc_E1_expected_from_verifier": float(T_expected),
        "T_sc_rel_err_vs_verifier": float((T0 - T_expected) / abs(T_expected)),
        "energy_identity_Xprime_residual": float(identity_residual),
        "X_H(0)": float(X_H0),
        "Y_H(0)": float(Y_H0),
        "D_H(0)": float(D0),
        "d(0)": float(d0),
        "D_H_prime(0)": float(Dp),
        "episode_start": episode_start,
        "episode_end": episode_end,
        "I_H_length": I_len,
        "H^{5/2}|I_H|_duration_diagnostic_only": (
            None if I_len is None else float((H**2.5) * I_len)
        ),
        "B_trap_integral": None if episode_start is None else float(B_trap),
        "boundary_term_(b-a)d(a)": boundary,
        "B_IH": B_IH,
        "resource_UW_integral": R_UW,
        "resource_X_integral_DIAGNOSTIC_ruled_out": (
            None if episode_start is None else float(R_X_acc)
        ),
        "B_over_R": B_over_R,
        "steps": steps,
        "dt": dt,
        "tau_nl_H^{-5/2}": tau_nl,
        "wall_seconds": time.time() - t_wall,
        "status": "NUMERICAL_EVIDENCE_ONLY",
        "status_detail": status_detail,
        "full_trajectory_complete": status_detail == "COMPLETE_FIRST_EPISODE",
        "theorem_stamp": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[1])
    ap.add_argument("--nu", type=float, default=None)
    ap.add_argument("--cut-mul", type=int, default=4)
    ap.add_argument("--t-max-factor", type=float, default=2500.0)
    ap.add_argument("--dt-factor", type=float, default=2.0)
    ap.add_argument("--floor-rel", type=float, default=1e-18)
    ap.add_argument("--max-steps", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("GATE-D-FULL-TRAJECTORY-FFT.json"),
    )
    args = ap.parse_args()

    runs = []
    for n in args.n:
        nu = args.nu if args.nu is not None else choose_nu(n)
        print(
            f"=== Gate D FFT full-trajectory n={n} H={63 * n} nu={nu:.6e} "
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
            max_steps=args.max_steps,
            smoke=args.smoke,
        )
        keys = [
            "n",
            "H",
            "fft_N",
            "method",
            "topM",
            "D_H(0)",
            "d(0)",
            "D_H_prime(0)",
            "T_sc_rel_err_vs_verifier",
            "energy_identity_Xprime_residual",
            "B_IH",
            "boundary_term_(b-a)d(a)",
            "B_over_R",
            "status_detail",
            "full_trajectory_complete",
            "extract_modes_max",
            "wall_seconds",
            "theorem_stamp",
        ]
        print(json.dumps({k: rec.get(k) for k in keys}, indent=2), flush=True)
        runs.append(rec)

    payload = {
        "title": "Gate D full-trajectory FFT solver — numerical evidence",
        "adversary": "Signed-Gate-B-Sharp-Band-Exponent-2026-10-07 six-box",
        "theorem_stamp": False,
        "gaussian_substituted": False,
        "topM": False,
        "scoring": "B_IH / R_UW with boundary term (b-a)d(a)",
        "review": "GATE-D-REVIEW-2026-10-09",
        "runs": runs,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
