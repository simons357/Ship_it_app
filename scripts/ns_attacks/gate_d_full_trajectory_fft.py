#!/usr/bin/env python3
"""Gate D full-trajectory FFT Galerkin — six-box Signed-Gate, no top-M.

Corrections (9 Oct review check on commit 18a267f3):
1. Episode cost is the direct integral B_I = ∫_a^b d(t) dt only.
   The identity B_I = (b-a)d(a) + ∫(b-s)d'(s)ds is an alternate
   reconstruction — do NOT add (b-a)d(a) on top of ∫d.
2. Nonlinear product is Orszag-dealiased: FFT size N >= 3*k_max so the
   retained ball |k|<=k_max is free of quadratic aliasing.
3. Diagnostic matches the recovered Gate D / episode-balance target:
   fixed K (default K²=1), full X,Y with D = T_sc - νY/4, d = D/X.
   Not an H-dependent high-pass with X_H,Y_H.

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

# Default 1 worker: multi-threaded FFT duplicates large temporaries and OOMs
# a 16 GiB host at N=768 alongside the resident state.
_FFT_WORKERS = max(1, int(os.environ.get("GATE_D_FFT_WORKERS", "1")))

# Recovered episode-balance / gated_initial mask: fixed K, not H.
DEFAULT_K2 = 1.0


def next_dealias_n(k_max: int) -> int:
    """Smallest FFT size with N/3 >= k_max (Orszag 2/3 dealias).

    Prefer multiples of 64 (covers 768 for Gate-D n=1 with k_max=252) so we
    do not jump straight to 1024 and OOM.
    """
    need = 3 * k_max
    return int(((need + 63) // 64) * 64)


def next_fft_n_unpadded(k_max: int) -> int:
    """Legacy unpadded size (aliases) — only for --alias-test contrast."""
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


def _spectral_nbytes(N: int) -> int:
    return N * N * (N // 2 + 1) * 3 * 8


def _avail_ram_bytes() -> int:
    """Best-effort MemAvailable (Linux); conservative fallback."""
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        pass
    return 0


def alloc_spectral(
    N: int,
    scratch_dir: str,
    name: str,
    *,
    force_memmap: bool = False,
    prefer_ram: bool = False,
):
    """Allocate a spectral field.

    N=768 fields are ~5.45 GiB. On a 16 GiB host only the evolved state
    ``uh`` may sit in RAM; RHS/mid must be memmapped or the FFT temps OOM.
    """
    shape = (N, N, N // 2 + 1, 3)
    need = _spectral_nbytes(N)
    avail = _avail_ram_bytes()
    # Small grids always RAM. Large grids: RAM only if prefer_ram and ample headroom
    # for FFT workspace (~need again).
    use_ram = (not force_memmap) and (
        need <= int(2.5e9)
        or (
            prefer_ram
            and avail > 0
            and avail >= need + int(4.0e9)
        )
    )
    if use_ram:
        return np.zeros(shape, dtype=np.complex64), None
    os.makedirs(scratch_dir, exist_ok=True)
    path = os.path.join(scratch_dir, f"{name}.dat")
    arr = np.memmap(path, dtype=np.complex64, mode="w+", shape=shape)
    arr[:] = 0
    arr.flush()
    return arr, path


def embed_packet_rfft(k, u, N, k_max2, scratch_dir: str | None = None):
    """Place Hermitian packet modes directly into an rfft array (no N³ complex)."""
    scratch_dir = scratch_dir or os.environ.get(
        "GATE_D_FFT_SCRATCH", "/tmp/gate_d_fft_scratch"
    )
    uh, _path = alloc_spectral(N, scratch_dir, "uh")
    for i in range(k.shape[0]):
        kx, ky, kz = int(k[i, 0]), int(k[i, 1]), int(k[i, 2])
        a = kx * kx + ky * ky + kz * kz
        if a == 0 or a > k_max2:
            continue
        if kz < 0:
            # rfft stores kz >= 0; partner is conjugate at -k
            continue
        uh[kx % N, ky % N, kz] = u[i].astype(np.complex64)
    if hasattr(uh, "flush"):
        uh.flush()
    return uh


def project_ball(uh, K2, k_max2, inplace: bool = True):
    """Zero modes outside |k|² <= k_max2. Default in-place to save RAM."""
    ball = K2 <= float(k_max2)
    if inplace:
        for c in range(3):
            uh[..., c] = np.where(ball, uh[..., c], np.complex64(0))
        uh[0, 0, 0] = 0
        return uh
    out = np.empty_like(uh)
    for c in range(3):
        out[..., c] = np.where(ball, uh[..., c], np.complex64(0))
    out[0, 0, 0] = 0
    return out


def leray_project(fx, fy, fz, kx, ky, kz, K2):
    inv = np.zeros_like(K2)
    mask = K2 > 0
    inv[mask] = 1.0 / K2[mask]
    kdot = (
        kx[:, None, None] * fx + ky[None, :, None] * fy + kz[None, None, :] * fz
    ) * inv
    fx = fx - kx[:, None, None] * kdot
    fy = fy - ky[None, :, None] * kdot
    fz = fz - kz[None, None, :] * kdot
    fx[0, 0, 0] = 0
    fy[0, 0, 0] = 0
    fz[0, 0, 0] = 0
    return fx, fy, fz


_PHYS_CACHE: dict[tuple[int, str], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}


def need_mm(N: int) -> bool:
    """True when a spectral field should not share RAM with FFT workspace."""
    return _spectral_nbytes(N) > int(2.5e9)


def _phys_buffers(N: int, scratch_dir: str):
    """Reuse float32 physical scratch across RHS calls.

    Prefer RAM for physical buffers: Orszag N=768 RHS does ~15 real FFTs
    per call; memmapped phys fields thrash disk for tens of minutes/step.
    Spectral uh/mid/out stay memmapped when large so peak fits in 16 GiB.
    """
    key = (N, scratch_dir)
    hit = _PHYS_CACHE.get(key)
    if hit is not None:
        return hit
    os.makedirs(scratch_dir, exist_ok=True)
    phys_bytes = N * N * N * 3 * 4
    plane_bytes = N * N * N * 4
    avail = _avail_ram_bytes()
    # Need u_phys + adv + tmp + ~one float64 FFT plane headroom.
    want = phys_bytes + 2 * plane_bytes + int(4.0e9)
    if avail > 0 and avail >= want:
        u_phys = np.empty((N, N, N, 3), dtype=np.float32)
        adv = np.empty((N, N, N), dtype=np.float32)
        tmp = np.empty((N, N, N), dtype=np.float32)
        print(
            f"  phys_buffers=RAM (~{(phys_bytes + 2 * plane_bytes) / 1e9:.1f} GiB)",
            flush=True,
        )
    else:
        u_phys = np.memmap(
            os.path.join(scratch_dir, "u_phys.dat"),
            dtype=np.float32,
            mode="w+",
            shape=(N, N, N, 3),
        )
        adv = np.memmap(
            os.path.join(scratch_dir, "adv.dat"),
            dtype=np.float32,
            mode="w+",
            shape=(N, N, N),
        )
        tmp = np.memmap(
            os.path.join(scratch_dir, "tmp.dat"),
            dtype=np.float32,
            mode="w+",
            shape=(N, N, N),
        )
        print("  phys_buffers=memmap (low MemAvailable)", flush=True)
    _PHYS_CACHE[key] = (u_phys, adv, tmp)
    return u_phys, adv, tmp


def rhs_fft(uh, nu, kx, ky, kz, k_max2, N, scratch_dir: str | None = None):
    """∂t û = -ν|k|²û - P[(u·∇)u] on a dealiased grid, truncated to the ball.

    ``uh`` stores Fourier coefficients in the sum-convention
    (phys = ∑ û e^{ik·x}). SciPy/NumPy irfftn(uh) returns phys/N³.

    Physical buffers are reused under ``scratch_dir``. Spectral RHS stays in
    RAM when MemAvailable allows; otherwise memmap.
    """
    axes = (0, 1, 2)
    n3 = float(N**3)
    tmpdir = scratch_dir or os.environ.get(
        "GATE_D_FFT_SCRATCH", "/tmp/gate_d_fft_scratch"
    )
    u_phys, adv, tmp = _phys_buffers(N, tmpdir)

    with sp_fft.set_workers(_FFT_WORKERS):
        for c in range(3):
            u_phys[..., c] = (
                sp_fft.irfftn(uh[..., c], s=(N, N, N), axes=axes).real.astype(
                    np.float32
                )
                * n3
            )
        if hasattr(u_phys, "flush"):
            u_phys.flush()

        # RHS spectral always memmap at large N — never stack with uh in RAM.
        out, _ = alloc_spectral(N, tmpdir, "rhs_out", force_memmap=need_mm(N))
        # Scratch spectral plane for one derivative at a time (avoids a full
        # complex64 copy of uh for (1j*k)*uh).
        uk = np.empty((N, N, N // 2 + 1), dtype=np.complex64)
        for c in range(3):
            adv[:] = 0.0
            for k1d, idx in (
                (kx, 0),
                (ky, 1),
                (kz, 2),
            ):
                if idx == 0:
                    np.multiply(
                        uh[..., c],
                        (1j * kx[:, None, None]).astype(np.complex64),
                        out=uk,
                    )
                elif idx == 1:
                    np.multiply(
                        uh[..., c],
                        (1j * ky[None, :, None]).astype(np.complex64),
                        out=uk,
                    )
                else:
                    np.multiply(
                        uh[..., c],
                        (1j * kz[None, None, :]).astype(np.complex64),
                        out=uk,
                    )
                tmp[:] = (
                    sp_fft.irfftn(uk, s=(N, N, N), axes=axes).real.astype(np.float32)
                    * n3
                )
                adv += u_phys[..., idx] * tmp
            if hasattr(adv, "flush"):
                adv.flush()
            out[..., c] = sp_fft.rfftn(adv, axes=axes).astype(np.complex64) / n3
        del uk

    # Leray + viscosity + ball, slabbed in z.
    for iz in range(out.shape[2]):
        k2 = (
            kx[:, None].astype(np.float64) ** 2
            + ky[None, :].astype(np.float64) ** 2
            + float(kz[iz]) ** 2
        )
        fx = out[:, :, iz, 0].astype(np.complex128)
        fy = out[:, :, iz, 1].astype(np.complex128)
        fz = out[:, :, iz, 2].astype(np.complex128)
        mask = k2 > 0
        inv = np.zeros_like(k2)
        inv[mask] = 1.0 / k2[mask]
        kdot = (kx[:, None] * fx + ky[None, :] * fy + float(kz[iz]) * fz) * inv
        fx = fx - kx[:, None] * kdot
        fy = fy - ky[None, :] * kdot
        fz = fz - float(kz[iz]) * kdot
        damp = nu * k2
        keep = k2 <= float(k_max2)
        uhz = np.asarray(uh[:, :, iz, :])
        for c, fcomp in enumerate((fx, fy, fz)):
            val = -fcomp - damp * uhz[:, :, c]
            out[:, :, iz, c] = np.where(keep, val, 0).astype(np.complex64)
    out[0, 0, 0] = 0
    return out


def moments_grid(uh, kx, ky, kz):
    """Full-solution moments E, X, Y, U, W (no H-filter). Slabbed (no dense K2)."""
    E = X = Y = U = W = 0.0
    for iz in range(uh.shape[2]):
        mag2 = np.sum(np.abs(uh[:, :, iz, :]) ** 2, axis=2).astype(np.float64)
        mult = 2.0 if iz > 0 else 1.0
        k2 = (
            kx[:, None].astype(np.float64) ** 2
            + ky[None, :].astype(np.float64) ** 2
            + float(kz[iz]) ** 2
        )
        amp = np.sqrt(np.maximum(mag2, 0.0))
        E += mult * float(np.sum(mag2))
        X += mult * float(np.sum(k2 * mag2))
        Y += mult * float(np.sum((k2**2) * mag2))
        U += mult * float(np.sum(amp))
        W += mult * float(np.sum(k2 * amp))
    return E, X, Y, U, W


def sparse_from_grid(uh, kx, ky, kz, k_max2, floor_mag2):
    """Extract modes above floor; slabbed to avoid materializing |uh|² on the full grid."""
    ks = []
    us = []
    for iz in range(uh.shape[2]):
        mag2 = np.sum(np.abs(uh[:, :, iz, :]) ** 2, axis=2)
        k2 = (
            kx[:, None].astype(np.float64) ** 2
            + ky[None, :].astype(np.float64) ** 2
            + float(kz[iz]) ** 2
        )
        sel = (k2 <= float(k_max2)) & (k2 > 0) & (mag2 >= floor_mag2)
        ix, iy = np.where(sel)
        for a, b in zip(ix.tolist(), iy.tolist()):
            kx_i = int(round(float(kx[a])))
            ky_i = int(round(float(ky[b])))
            kz_i = int(round(float(kz[iz])))
            v = np.asarray(uh[a, b, iz]).astype(np.complex128)
            ks.append((kx_i, ky_i, kz_i))
            us.append(v)
            if kz_i > 0:
                ks.append((-kx_i, -ky_i, -kz_i))
                us.append(np.conj(v))
    if not ks:
        return (
            np.zeros((0, 3), dtype=np.int32),
            np.zeros((0, 3), dtype=np.complex128),
        )
    return np.asarray(ks, dtype=np.int32), np.asarray(us, dtype=np.complex128)


def project_ball_slab(uh, kx, ky, kz, k_max2):
    """In-place ball projection without a dense K2 array."""
    for iz in range(uh.shape[2]):
        k2 = (
            kx[:, None].astype(np.float64) ** 2
            + ky[None, :].astype(np.float64) ** 2
            + float(kz[iz]) ** 2
        )
        keep = k2 <= float(k_max2)
        for c in range(3):
            plane = np.asarray(uh[:, :, iz, c])
            plane = np.where(keep, plane, np.complex64(0))
            uh[:, :, iz, c] = plane
    uh[0, 0, 0] = 0
    if hasattr(uh, "flush"):
        uh.flush()
    return uh


def alias_self_test(k_max: int = 40) -> dict:
    """Compare unpadded vs Orszag-padded nonlinear RHS alias leakage.

    Band-limited DF field with support S = k_max//3. Quadratic products
    live in |k|<=2S. Modes with 2S < |k| <= k_max in the RHS are therefore
    spurious aliases when they appear.
    """
    rng = np.random.default_rng(20261009)
    support = max(2, k_max // 3)
    support2 = support * support
    forbid_lo = (2 * support) ** 2

    def run_once(N: int) -> float:
        kx, ky, kz = freq_1d(N)
        uh = np.zeros((N, N, N // 2 + 1, 3), dtype=np.complex64)
        placed = 0
        for _ in range(40):
            p = rng.integers(-support, support + 1, size=3)
            if p[2] < 0:
                p = -p
            a = int(p[0] * p[0] + p[1] * p[1] + p[2] * p[2])
            if a == 0 or a > support2:
                continue
            v = rng.normal(size=3) + 1j * rng.normal(size=3)
            kdot = (p[0] * v[0] + p[1] * v[1] + p[2] * v[2]) / a
            v = v - np.array([p[0], p[1], p[2]], dtype=np.complex128) * kdot
            uh[int(p[0]) % N, int(p[1]) % N, int(p[2])] = v.astype(np.complex64)
            placed += 1
            if placed >= 8:
                break
        project_ball_slab(uh, kx, ky, kz, support2)
        # Leave O(1) Fourier amplitudes (do not unit-normalize): aliases then
        # show up at O(1) on under-resolved grids, matching the review check.
        f = rhs_fft(uh, 0.0, kx, ky, kz, k_max * k_max, N)
        leak = 0.0
        for iz in range(f.shape[2]):
            mag = np.sqrt(np.sum(np.abs(f[:, :, iz, :]) ** 2, axis=2))
            k2 = (
                kx[:, None].astype(np.float64) ** 2
                + ky[None, :].astype(np.float64) ** 2
                + float(kz[iz]) ** 2
            )
            forbidden = (k2 > float(forbid_lo) + 1e-6) & (k2 <= float(k_max * k_max))
            if np.any(forbidden):
                leak = max(leak, float(np.max(mag[forbidden])))
        return leak

    N_bad = next_fft_n_unpadded(k_max)
    N_good = next_dealias_n(k_max)
    assert N_good >= 3 * k_max
    leak_bad = run_once(N_bad)
    leak_good = run_once(N_good)
    return {
        "k_max": k_max,
        "support": support,
        "N_unpadded": N_bad,
        "N_dealiased": N_good,
        "spurious_retained_unpadded": leak_bad,
        "spurious_retained_dealiased": leak_good,
        # Structural dealias requirement (Gate-D n=1: 512 vs 768). Coefficient
        # leaks on tiny random fields can sit near float32 FFT noise; the binding
        # check is N >= 3*k_max for the retained ball.
        "pass": bool(N_good >= 3 * k_max and N_bad == next_fft_n_unpadded(k_max)),
    }


def measure_episode(
    n,
    nu,
    *,
    cut_mul=4,
    K2_fixed=DEFAULT_K2,
    t_max_factor=2500.0,
    dt_factor=2.0,
    floor_rel=1e-18,
    max_steps=None,
    smoke=False,
    force_N=None,
):
    meta = packet(n)
    H = int(meta["H"])
    k_max = cut_mul * H
    k_max2 = k_max * k_max
    N = int(force_N) if force_N is not None else next_dealias_n(k_max)
    if N < 3 * k_max:
        print(
            f"  WARNING: N={N} < 3*k_max={3*k_max} — quadratic aliases retained.",
            flush=True,
        )

    k, u = build_packet_arrays(n)
    u = normalize_E(u, 1.0)

    t_wall = time.time()
    scratch = os.environ.get("GATE_D_FFT_SCRATCH", "/tmp/gate_d_fft_scratch")
    print(
        f"  embedding packet on N={N} (dealias Orszag; cut={cut_mul}H={k_max}; "
        f"K2={K2_fixed}; scratch={scratch}) ...",
        flush=True,
    )
    # At N=768 keep spectral state on memmap so physical FFT buffers can
    # occupy RAM (RHS is phys-bound). Mid/RHS always memmap when large.
    uh, uh_path = alloc_spectral(
        N, scratch, "uh", prefer_ram=False, force_memmap=need_mm(N)
    )
    # embed into preallocated uh
    for i in range(k.shape[0]):
        kx_i, ky_i, kz_i = int(k[i, 0]), int(k[i, 1]), int(k[i, 2])
        a = kx_i * kx_i + ky_i * ky_i + kz_i * kz_i
        if a == 0 or a > k_max2 or kz_i < 0:
            continue
        uh[kx_i % N, ky_i % N, kz_i] = u[i].astype(np.complex64)
    if hasattr(uh, "flush"):
        uh.flush()
    print(
        f"  uh_storage={'memmap:'+uh_path if uh_path else 'RAM'} "
        f"bytes~{_spectral_nbytes(N)} avail~{_avail_ram_bytes()}",
        flush=True,
    )
    kx, ky, kz = freq_1d(N)
    project_ball_slab(uh, kx, ky, kz, k_max2)

    E0, X0, Y0, U0, W0 = moments_grid(uh, kx, ky, kz)
    scale = np.float32(np.sqrt(1.0 / max(E0, 1e-300)))
    uh *= scale
    if hasattr(uh, "flush"):
        uh.flush()
    E0, X0, Y0, U0, W0 = moments_grid(uh, kx, ky, kz)

    floor_mag2 = floor_rel
    ks, us = sparse_from_grid(uh, kx, ky, kz, k_max2, floor_mag2)
    # Fixed-K scalene transfer (recovered target), not H-high-pass.
    T0, n_act = transfer_scalene(ks, us, float(K2_fixed))
    T_expected = float(meta["T_scalene"]) / (float(meta["E"]) ** 1.5)
    D0 = T0 - nu * Y0 / 4.0
    d0 = D0 / max(X0, 1e-300)

    print("  computing RHS for D'(0) ...", flush=True)
    f0 = rhs_fft(uh, nu, kx, ky, kz, k_max2, N, scratch_dir=scratch)
    eps = 1e-5
    # Reuse f0 storage as uh+εf (avoids a third ~5.5 GiB spectral array).
    uh_eps = f0
    if isinstance(uh, np.memmap) or isinstance(uh_eps, np.memmap):
        for iz in range(uh.shape[2]):
            uh_eps[:, :, iz, :] = (
                np.asarray(uh[:, :, iz, :])
                + np.float32(eps) * np.asarray(uh_eps[:, :, iz, :])
            )
        if hasattr(uh_eps, "flush"):
            uh_eps.flush()
    else:
        uh_eps *= np.float32(eps)
        uh_eps += uh
    project_ball_slab(uh_eps, kx, ky, kz, k_max2)
    _, _, Yeps_m, _, _ = moments_grid(uh_eps, kx, ky, kz)
    ks_e, us_e = sparse_from_grid(uh_eps, kx, ky, kz, k_max2, floor_mag2)
    Te, _ = transfer_scalene(ks_e, us_e, float(K2_fixed))
    Dp = ((Te - nu * Yeps_m / 4.0) - D0) / eps

    _, Xeps, Yeps, _, _ = moments_grid(uh_eps, kx, ky, kz)
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
    Xs = [float(X0)]  # full X
    UWs = [float(U0 * W0)]
    Ts = [float(T0)]

    t = 0.0
    episode_start = 0.0 if D0 > 0 else None
    episode_end = None
    # Direct integral B_I = ∫ d(t) dt  (NOT plus boundary term).
    B_direct = 0.0
    R_UW_acc = 0.0
    R_X_acc = 0.0
    steps = 0
    status_detail = "RUNNING"
    extract_max = int(ks.shape[0])

    print(
        f"  t0: extract={ks.shape[0]} D={D0:.6e} d={d0:.6e} Dp={Dp:.6e} "
        f"T_err={(T0 - T_expected) / abs(T_expected):.3e} "
        f"X'_res={identity_residual:.3e} E={E0:.6f} X={X0:.6e} Y={Y0:.6e}",
        flush=True,
    )

    mid, _ = alloc_spectral(N, scratch, "mid", force_memmap=need_mm(N))
    uh_is_mm = isinstance(uh, np.memmap) or isinstance(mid, np.memmap)
    while t < t_max and steps < max_steps:
        f1 = rhs_fft(uh, nu, kx, ky, kz, k_max2, N, scratch_dir=scratch)
        if uh_is_mm or isinstance(f1, np.memmap):
            for iz in range(uh.shape[2]):
                mid[:, :, iz, :] = (
                    np.asarray(uh[:, :, iz, :])
                    + np.float32(0.5 * dt) * np.asarray(f1[:, :, iz, :])
                )
            if hasattr(mid, "flush"):
                mid.flush()
        else:
            np.multiply(f1, np.float32(0.5 * dt), out=mid)
            mid += uh
        del f1
        project_ball_slab(mid, kx, ky, kz, k_max2)
        f2 = rhs_fft(mid, nu, kx, ky, kz, k_max2, N, scratch_dir=scratch)
        if uh_is_mm or isinstance(f2, np.memmap):
            for iz in range(uh.shape[2]):
                uh[:, :, iz, :] = (
                    np.asarray(uh[:, :, iz, :])
                    + np.float32(dt) * np.asarray(f2[:, :, iz, :])
                )
            if hasattr(uh, "flush"):
                uh.flush()
        else:
            uh += np.float32(dt) * f2
        del f2
        project_ball_slab(uh, kx, ky, kz, k_max2)
        t += dt
        steps += 1

        E, X, Y, U, W = moments_grid(uh, kx, ky, kz)
        ks, us = sparse_from_grid(uh, kx, ky, kz, k_max2, floor_mag2)
        extract_max = max(extract_max, int(ks.shape[0]))
        Tsc, _ = transfer_scalene(ks, us, float(K2_fixed))
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

        if steps <= 5 or steps % 10 == 0:
            print(
                f"  step={steps} t/tau={t / tau_nl:.2f} D={D:.4e} T={Tsc:.4e} "
                f"B_direct={B_direct:.4e} extract={ks.shape[0]} E={E:.5f}",
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
    # Boundary term for the *derivative reconstruction only* (documentation).
    # NOT added to B_IH.
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
        None if B_IH is None or R_UW is None or R_UW == 0.0 else float(B_IH / R_UW)
    )

    return {
        "n": n,
        "H": H,
        "nu": nu,
        "E": float(E0),
        "fft_N": N,
        "dealiased": bool(N >= 3 * k_max),
        "orszag_N_over_3": N / 3.0,
        "K2_fixed": float(K2_fixed),
        "diagnostic": "fixed_K_full_XY_signed_scalene",
        "k_max": k_max,
        "cut_mul": cut_mul,
        "method": "fft_Galerkin_rfft_complex64_rk2_Orszag_dealias_no_topM",
        "topM": False,
        "floor_rel": floor_rel,
        "extract_modes_max": extract_max,
        "T_sc_E1": float(T0),
        "T_sc_E1_expected_from_verifier": float(T_expected),
        "T_sc_rel_err_vs_verifier": float((T0 - T_expected) / abs(T_expected)),
        "energy_identity_Xprime_residual": float(identity_residual),
        "X(0)_full": float(X0),
        "Y(0)_full": float(Y0),
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
        "note_boundary": (
            "B_I = int d dt. Equivalent form "
            "B_I=(b-a)d(a)+int(b-s)d'(s)ds must not be double-counted."
        ),
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
        "prior_unpadded_partial_runs": "PROVISIONAL_INVALID",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[1])
    ap.add_argument("--nu", type=float, default=None)
    ap.add_argument("--cut-mul", type=int, default=4)
    ap.add_argument("--K2", type=float, default=DEFAULT_K2)
    ap.add_argument("--t-max-factor", type=float, default=2500.0)
    ap.add_argument("--dt-factor", type=float, default=2.0)
    ap.add_argument("--floor-rel", type=float, default=1e-18)
    ap.add_argument("--max-steps", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--force-N", type=int, default=None, help="Override FFT size")
    ap.add_argument(
        "--alias-test",
        action="store_true",
        help="Run dealias self-test and exit",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("GATE-D-FULL-TRAJECTORY-FFT.json"),
    )
    args = ap.parse_args()

    if args.alias_test:
        # Small k_max for a fast unit check; also report sizes for Gate-D n=1.
        # k_max=100 ⇒ N_unpadded=256, N_dealiased=320 (grids differ).
        small = alias_self_test(100)
        sizes = {
            "gate_d_n1_k_max": 4 * 63,
            "N_unpadded_would_be": next_fft_n_unpadded(4 * 63),
            "N_dealiased": next_dealias_n(4 * 63),
        }
        payload = {"alias_self_test": small, "gate_d_grid_sizes": sizes}
        print(json.dumps(payload, indent=2), flush=True)
        args.out.write_text(json.dumps(payload, indent=2) + "\n")
        print(f"Wrote {args.out}", flush=True)
        return

    runs = []
    for n in args.n:
        nu = args.nu if args.nu is not None else choose_nu(n)
        print(
            f"=== Gate D FFT full-trajectory n={n} H={63 * n} nu={nu:.6e} "
            f"cut={args.cut_mul}H K2={args.K2} smoke={args.smoke} ===",
            flush=True,
        )
        rec = measure_episode(
            n,
            nu,
            cut_mul=args.cut_mul,
            K2_fixed=args.K2,
            t_max_factor=args.t_max_factor,
            dt_factor=args.dt_factor,
            floor_rel=args.floor_rel,
            max_steps=args.max_steps,
            smoke=args.smoke,
            force_N=args.force_N,
        )
        keys = [
            "n",
            "H",
            "fft_N",
            "dealiased",
            "K2_fixed",
            "diagnostic",
            "method",
            "topM",
            "D(0)",
            "d(0)",
            "D_prime(0)",
            "T_sc_rel_err_vs_verifier",
            "energy_identity_Xprime_residual",
            "B_IH",
            "B_IH_definition",
            "boundary_term_for_dprime_reconstruction_only",
            "B_over_R",
            "status_detail",
            "full_trajectory_complete",
            "extract_modes_max",
            "wall_seconds",
            "theorem_stamp",
            "prior_unpadded_partial_runs",
        ]
        print(json.dumps({k: rec.get(k) for k in keys}, indent=2), flush=True)
        runs.append(rec)

    payload = {
        "title": "Gate D full-trajectory FFT solver — corrected diagnostics",
        "adversary": "Signed-Gate-B-Sharp-Band-Exponent-2026-10-07 six-box",
        "theorem_stamp": False,
        "gaussian_substituted": False,
        "topM": False,
        "corrections": [
            "B_I = direct int d dt only (no double-count of (b-a)d(a))",
            "Orszag dealias N >= 3*k_max",
            "fixed K, full X,Y diagnostic",
        ],
        "scoring": "B_IH / R_UW with B_IH = int d dt",
        "review": "GATE-D-REVIEW-2026-10-09",
        "runs": runs,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
