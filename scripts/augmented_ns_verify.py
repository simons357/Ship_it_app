#!/usr/bin/env python3
"""
Fourier-Galerkin check of the Q1-augmented NS energy law on T^3.

Track A verification only. Not a proof of the unaugmented system.

  d/dt (1/2 ||u||^2) + nu ||grad u||^2 + eps^alpha ||grad u||_{L^{beta+2}}^{beta+2} = 0
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


def k_1d(n: int) -> np.ndarray:
    """Integer Fourier modes on T^3 = [0, 2π]^3."""
    return np.fft.fftfreq(n) * n


def make_grid(n: int):
    k = k_1d(n)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k2_safe = k2.copy()
    k2_safe[0, 0, 0] = 1.0
    dealias = (np.abs(kx) < n / 3) & (np.abs(ky) < n / 3) & (np.abs(kz) < n / 3)
    return kx, ky, kz, k2, k2_safe, dealias


def fft(u: np.ndarray) -> np.ndarray:
    return np.fft.fftn(u)


def ifft(uh: np.ndarray) -> np.ndarray:
    return np.fft.ifftn(uh).real


def project(uh, vh, wh, kx, ky, kz, k2_safe):
    div = kx * uh + ky * vh + kz * wh
    uh = uh - kx * div / k2_safe
    vh = vh - ky * div / k2_safe
    wh = wh - kz * div / k2_safe
    uh[0, 0, 0] = 0.0
    vh[0, 0, 0] = 0.0
    wh[0, 0, 0] = 0.0
    return uh, vh, wh


def taylor_green(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    u = np.sin(X) * np.cos(Y) * np.cos(Z)
    v = -np.cos(X) * np.sin(Y) * np.cos(Z)
    w = np.zeros_like(u)
    return u, v, w


def grad_components(u, v, w, kx, ky, kz):
    uh, vh, wh = fft(u), fft(v), fft(w)
    du = [
        [ifft(1j * kx * uh), ifft(1j * ky * uh), ifft(1j * kz * uh)],
        [ifft(1j * kx * vh), ifft(1j * ky * vh), ifft(1j * kz * vh)],
        [ifft(1j * kx * wh), ifft(1j * ky * wh), ifft(1j * kz * wh)],
    ]
    return du, uh, vh, wh


def l2sq(u, v, w) -> float:
    vol = (2.0 * math.pi) ** 3
    return float(np.mean(u * u + v * v + w * w)) * vol


def grad_l2sq(du) -> float:
    vol = (2.0 * math.pi) ** 3
    s = 0.0
    for i in range(3):
        for j in range(3):
            s += float(np.mean(du[i][j] ** 2))
    return s * vol


def grad_lp(du, p: float) -> float:
    vol = (2.0 * math.pi) ** 3
    g2 = np.zeros_like(du[0][0])
    for i in range(3):
        for j in range(3):
            g2 = g2 + du[i][j] ** 2
    g = np.sqrt(np.maximum(g2, 0.0))
    return float(np.mean(g**p)) * vol


def enstrophy(u, v, w, kx, ky, kz) -> float:
    uh, vh, wh = fft(u), fft(v), fft(w)
    wx = ifft(1j * ky * wh - 1j * kz * vh)
    wy = ifft(1j * kz * uh - 1j * kx * wh)
    wz = ifft(1j * kx * vh - 1j * ky * uh)
    return 0.5 * l2sq(wx, wy, wz)


def rhs(u, v, w, kx, ky, kz, k2, k2_safe, dealias, nu, eps, alpha, beta):
    du, uh, vh, wh = grad_components(u, v, w, kx, ky, kz)

    # convective: -P((u·∇)u)
    ux, uy, uz = du[0]
    vx, vy, vz = du[1]
    wx, wy, wz = du[2]
    conv_u = u * ux + v * uy + w * uz
    conv_v = u * vx + v * vy + w * vz
    conv_w = u * wx + v * wy + w * wz
    cuh, cvh, cwh = fft(conv_u), fft(conv_v), fft(conv_w)
    cuh *= dealias
    cvh *= dealias
    cwh *= dealias
    cuh, cvh, cwh = project(cuh, cvh, cwh, kx, ky, kz, k2_safe)

    # viscous
    visc = -nu * k2

    # Q1: P div(|∇u|^β ∇u)
    g2 = ux * ux + uy * uy + uz * uz + vx * vx + vy * vy + vz * vz + wx * wx + wy * wy + wz * wz
    factor = np.maximum(g2, 0.0) ** (0.5 * beta)
    sigma = [[factor * du[i][j] for j in range(3)] for i in range(3)]
    # divergence of each row
    qh = []
    for i in range(3):
        shx, shy, shz = fft(sigma[i][0]), fft(sigma[i][1]), fft(sigma[i][2])
        qh.append((1j * kx * shx + 1j * ky * shy + 1j * kz * shz) * dealias)
    quh, qvh, qwh = project(qh[0], qh[1], qh[2], kx, ky, kz, k2_safe)

    gain = eps**alpha if eps > 0.0 else 0.0
    uh_t = -cuh + visc * uh + gain * quh
    vh_t = -cvh + visc * vh + gain * qvh
    wh_t = -cwh + visc * wh + gain * qwh
    uh_t, vh_t, wh_t = project(uh_t, vh_t, wh_t, kx, ky, kz, k2_safe)
    return ifft(uh_t), ifft(vh_t), ifft(wh_t), du


def rk2_step(u, v, w, dt, **kw):
    ku, kv, kwv, _ = rhs(u, v, w, **kw)
    u1, v1, w1 = u + dt * ku, v + dt * kv, w + dt * kwv
    k2u, k2v, k2w, du = rhs(u1, v1, w1, **kw)
    u_n = u + 0.5 * dt * (ku + k2u)
    v_n = v + 0.5 * dt * (kv + k2v)
    w_n = w + 0.5 * dt * (kwv + k2w)
    # re-project
    kx, ky, kz, _, k2_safe, _ = (
        kw["kx"],
        kw["ky"],
        kw["kz"],
        kw["k2"],
        kw["k2_safe"],
        kw["dealias"],
    )
    uh, vh, wh = project(fft(u_n), fft(v_n), fft(w_n), kx, ky, kz, k2_safe)
    return ifft(uh), ifft(vh), ifft(wh), du


@dataclass
class RunResult:
    eps: float
    nu: float
    beta: float
    alpha: float
    n: int
    t: float
    energy0: float
    energy_t: float
    diss_visc: float
    diss_q1: float
    residual: float
    enstrophy0: float
    enstrophy_t: float
    max_div: float


def run_once(n: int, nu: float, eps: float, alpha: float, beta: float, t_end: float, dt: float) -> RunResult:
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    u, v, w = taylor_green(n)
    uh, vh, wh = project(fft(u), fft(v), fft(w), kx, ky, kz, k2_safe)
    u, v, w = ifft(uh), ifft(vh), ifft(wh)

    kw = dict(
        kx=kx, ky=ky, kz=kz, k2=k2, k2_safe=k2_safe, dealias=dealias, nu=nu, eps=eps, alpha=alpha, beta=beta
    )
    du, _, _, _ = grad_components(u, v, w, kx, ky, kz)
    e0 = 0.5 * l2sq(u, v, w)
    x0 = enstrophy(u, v, w, kx, ky, kz)
    visc_prev = nu * grad_l2sq(du)
    q1_prev = (eps**alpha) * grad_lp(du, beta + 2.0) if eps > 0.0 else 0.0
    visc_int = 0.0
    q1_int = 0.0
    steps = max(1, int(round(t_end / dt)))
    dt = t_end / steps
    for _ in range(steps):
        u, v, w, du = rk2_step(u, v, w, dt, **kw)
        visc_now = nu * grad_l2sq(du)
        q1_now = (eps**alpha) * grad_lp(du, beta + 2.0) if eps > 0.0 else 0.0
        visc_int += 0.5 * (visc_prev + visc_now) * dt
        q1_int += 0.5 * (q1_prev + q1_now) * dt
        visc_prev, q1_prev = visc_now, q1_now

    e_t = 0.5 * l2sq(u, v, w)
    residual = abs(e_t + visc_int + q1_int - e0)
    # max div
    uh, vh, wh = fft(u), fft(v), fft(w)
    div = ifft(1j * kx * uh + 1j * ky * vh + 1j * kz * wh)
    return RunResult(
        eps=eps,
        nu=nu,
        beta=beta,
        alpha=alpha,
        n=n,
        t=t_end,
        energy0=e0,
        energy_t=e_t,
        diss_visc=visc_int,
        diss_q1=q1_int,
        residual=residual,
        enstrophy0=x0,
        enstrophy_t=enstrophy(u, v, w, kx, ky, kz),
        max_div=float(np.max(np.abs(div))),
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Track A Q1-augmented NS energy/enstrophy check")
    p.add_argument("--n", type=int, default=16)
    p.add_argument("--nu", type=float, default=0.02)
    p.add_argument("--alpha", type=float, default=1.0)
    p.add_argument("--beta", type=float, default=0.5)
    p.add_argument("--t", type=float, default=0.5)
    p.add_argument("--dt", type=float, default=0.01)
    p.add_argument("--eps", type=float, nargs="+", default=[0.0, 0.05, 0.2])
    p.add_argument("--out", type=Path, default=Path("results/augmented_ns_verify.json"))
    args = p.parse_args()

    rows = []
    print(f"{'eps':>8} {'E0':>10} {'ET':>10} {'visc':>10} {'Q1':>10} {'resid':>10} {'X0':>10} {'XT':>10} {'div':>10}")
    for eps in args.eps:
        r = run_once(args.n, args.nu, eps, args.alpha, args.beta, args.t, args.dt)
        rows.append(asdict(r))
        print(
            f"{r.eps:8.3f} {r.energy0:10.4f} {r.energy_t:10.4f} {r.diss_visc:10.4f} "
            f"{r.diss_q1:10.4f} {r.residual:10.3e} {r.enstrophy0:10.4f} {r.enstrophy_t:10.4f} {r.max_div:10.2e}"
        )

    payload = {
        "meta": {
            "track": "A-augmented",
            "note": "Energy-law consistency for Q1. Not a proof of the classical system.",
            "n": args.n,
            "nu": args.nu,
            "alpha": args.alpha,
            "beta": args.beta,
            "t": args.t,
            "dt": args.dt,
        },
        "runs": rows,
        "checks": {
            "E1_energy_residual": max(r["residual"] for r in rows),
            "E2_q1_positive_when_eps": all(r["diss_q1"] > 0.0 for r in rows if r["eps"] > 0.0),
            "E3_enstrophy_finite": all(math.isfinite(r["enstrophy_t"]) and r["enstrophy_t"] > 0.0 for r in rows),
            "E4_xt_grows_as_eps_falls": all(
                later["enstrophy_t"] >= earlier["enstrophy_t"] - 1e-9
                for earlier, later in zip(
                    sorted(rows, key=lambda r: r["eps"], reverse=True),
                    sorted(rows, key=lambda r: r["eps"], reverse=True)[1:],
                )
            )
            if len(rows) >= 2
            else True,
            "E5_max_div": max(r["max_div"] for r in rows),
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
