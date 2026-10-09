#!/usr/bin/env python3
"""Fourier–Galerkin Navier–Stokes core on T³ = [0, 2π]³.

Approved solver core plus three small edits:

  S1. Instantaneous power balance replaces the integrated trapezoidal
      residual that printed a misleading 3–5e-4 on the Q1 run.
  S2. Diagnostics are taken on the accepted, re-projected state, not
      the RK predictor field.
  S3. Dissipation uses the actual inner product ⟨u, rhs_term⟩, not the
      analytic ||∇u||_{β+2}^{β+2} proxy (that proxy is what produced
      the 3–5e-4 number under dealiasing).

Track A / Q1 is optional. Classical unaugmented NS is the default
measurement target. This file does not speak to whether smooth
solutions stay smooth. Classical NS stays open.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

VOL_T3 = (2.0 * math.pi) ** 3


def k_1d(n: int) -> np.ndarray:
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


def taylor_green(n: int, amp: float = 1.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    u = amp * np.sin(X) * np.cos(Y) * np.cos(Z)
    v = -amp * np.cos(X) * np.sin(Y) * np.cos(Z)
    w = np.zeros_like(u)
    return u, v, w


def inner(u, v, w, a, b, c) -> float:
    """⟨U, A⟩ = ∫ U·A on T³."""
    return float(np.mean(u * a + v * b + w * c)) * VOL_T3


def l2sq(u, v, w) -> float:
    return inner(u, v, w, u, v, w)


def energy(u, v, w) -> float:
    return 0.5 * l2sq(u, v, w)


def grad_components(u, v, w, kx, ky, kz):
    uh, vh, wh = fft(u), fft(v), fft(w)
    du = [
        [ifft(1j * kx * uh), ifft(1j * ky * uh), ifft(1j * kz * uh)],
        [ifft(1j * kx * vh), ifft(1j * ky * vh), ifft(1j * kz * vh)],
        [ifft(1j * kx * wh), ifft(1j * ky * wh), ifft(1j * kz * wh)],
    ]
    return du, uh, vh, wh


def grad_l2sq(du) -> float:
    s = 0.0
    for i in range(3):
        for j in range(3):
            s += float(np.mean(du[i][j] ** 2))
    return s * VOL_T3


def enstrophy(u, v, w, kx, ky, kz) -> float:
    uh, vh, wh = fft(u), fft(v), fft(w)
    wx = ifft(1j * ky * wh - 1j * kz * vh)
    wy = ifft(1j * kz * uh - 1j * kx * wh)
    wz = ifft(1j * kx * vh - 1j * ky * uh)
    return 0.5 * l2sq(wx, wy, wz)


def max_div(u, v, w, kx, ky, kz) -> float:
    uh, vh, wh = fft(u), fft(v), fft(w)
    div = ifft(1j * kx * uh + 1j * ky * vh + 1j * kz * wh)
    return float(np.max(np.abs(div)))


def _convective_hat(u, v, w, du, kx, ky, kz, k2_safe, dealias):
    ux, uy, uz = du[0]
    vx, vy, vz = du[1]
    wx, wy, wz = du[2]
    conv_u = u * ux + v * uy + w * uz
    conv_v = u * vx + v * vy + w * vz
    conv_w = u * wx + v * wy + w * wz
    cuh, cvh, cwh = fft(conv_u), fft(conv_v), fft(conv_w)
    cuh = cuh * dealias
    cvh = cvh * dealias
    cwh = cwh * dealias
    return project(cuh, cvh, cwh, kx, ky, kz, k2_safe)


def _q1_hat(du, kx, ky, kz, k2_safe, dealias, beta: float):
    g2 = np.zeros_like(du[0][0])
    for i in range(3):
        for j in range(3):
            g2 = g2 + du[i][j] ** 2
    factor = np.maximum(g2, 0.0) ** (0.5 * beta)
    qh = []
    for i in range(3):
        shx = fft(factor * du[i][0])
        shy = fft(factor * du[i][1])
        shz = fft(factor * du[i][2])
        qh.append((1j * kx * shx + 1j * ky * shy + 1j * kz * shz) * dealias)
    return project(qh[0], qh[1], qh[2], kx, ky, kz, k2_safe)


def rhs_terms(u, v, w, kx, ky, kz, k2, k2_safe, dealias, nu, eps=0.0, alpha=1.0, beta=0.5):
    """Split RHS. Each term is already projected and dealias-masked."""
    du, uh, vh, wh = grad_components(u, v, w, kx, ky, kz)
    cuh, cvh, cwh = _convective_hat(u, v, w, du, kx, ky, kz, k2_safe, dealias)
    visc = -nu * k2
    vu, vv, vw = visc * uh, visc * vh, visc * wh
    if eps > 0.0:
        quh, qvh, qwh = _q1_hat(du, kx, ky, kz, k2_safe, dealias, beta)
        gain = eps**alpha
        quh, qvh, qwh = gain * quh, gain * qvh, gain * qwh
    else:
        quh = qvh = qwh = np.zeros_like(uh)
    uh_t = -cuh + vu + quh
    vh_t = -cvh + vv + qvh
    wh_t = -cwh + vw + qwh
    uh_t, vh_t, wh_t = project(uh_t, vh_t, wh_t, kx, ky, kz, k2_safe)
    return {
        "du": du,
        "conv": (ifft(-cuh), ifft(-cvh), ifft(-cwh)),
        "visc": (ifft(vu), ifft(vv), ifft(vw)),
        "q1": (ifft(quh), ifft(qvh), ifft(qwh)),
        "full": (ifft(uh_t), ifft(vh_t), ifft(wh_t)),
    }


def rhs(u, v, w, **kw):
    terms = rhs_terms(u, v, w, **kw)
    ut, vt, wt = terms["full"]
    return ut, vt, wt, terms["du"]


def project_state(u, v, w, kx, ky, kz, k2_safe):
    uh, vh, wh = project(fft(u), fft(v), fft(w), kx, ky, kz, k2_safe)
    return ifft(uh), ifft(vh), ifft(wh)


def rk4_step(u, v, w, dt, **kw):
    """Classical RK4. Accepted state is re-projected (S2)."""
    k1u, k1v, k1w, _ = rhs(u, v, w, **kw)
    u2, v2, w2 = u + 0.5 * dt * k1u, v + 0.5 * dt * k1v, w + 0.5 * dt * k1w
    k2u, k2v, k2w, _ = rhs(u2, v2, w2, **kw)
    u3, v3, w3 = u + 0.5 * dt * k2u, v + 0.5 * dt * k2v, w + 0.5 * dt * k2w
    k3u, k3v, k3w, _ = rhs(u3, v3, w3, **kw)
    u4, v4, w4 = u + dt * k3u, v + dt * k3v, w + dt * k3w
    k4u, k4v, k4w, _ = rhs(u4, v4, w4, **kw)
    u_n = u + (dt / 6.0) * (k1u + 2.0 * k2u + 2.0 * k3u + k4u)
    v_n = v + (dt / 6.0) * (k1v + 2.0 * k2v + 2.0 * k3v + k4v)
    w_n = w + (dt / 6.0) * (k1w + 2.0 * k2w + 2.0 * k3w + k4w)
    return project_state(u_n, v_n, w_n, kw["kx"], kw["ky"], kw["kz"], kw["k2_safe"])


def instantaneous_energy_check(u, v, w, **kw) -> dict:
    """S1 + S3: power balance from the actual RHS inner products.

    The retired check integrated a trapezoidal residual of the analytic
    ||∇u||_{β+2}^{β+2} proxy. That printed 3–5e-4 on the Q1 Taylor–Green
    run and was not a conservation defect.
    """
    terms = rhs_terms(u, v, w, **kw)
    ut, vt, wt = terms["full"]
    power = inner(u, v, w, ut, vt, wt)
    visc_ip = -inner(u, v, w, *terms["visc"])
    q1_ip = -inner(u, v, w, *terms["q1"])
    conv_ip = -inner(u, v, w, *terms["conv"])
    proxy_visc = kw["nu"] * grad_l2sq(terms["du"])
    residual = abs(power + visc_ip + q1_ip)
    scale = max(abs(visc_ip), abs(power), 1e-30)
    return {
        "power": power,
        "viscous_inner": visc_ip,
        "q1_inner": q1_ip,
        "convective_inner": conv_ip,
        "viscous_proxy": proxy_visc,
        "residual": residual,
        "relative_residual": residual / scale,
        "energy": energy(u, v, w),
        "grad_l2sq": grad_l2sq(terms["du"]),
    }


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
    relative_residual: float
    retired_integrated_residual: float
    enstrophy0: float
    enstrophy_t: float
    max_div: float
    energy_check: str = "instantaneous_inner_product"


def run_once(
    n: int,
    nu: float,
    eps: float,
    alpha: float,
    beta: float,
    t_end: float,
    dt: float,
) -> RunResult:
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
        eps=eps,
        alpha=alpha,
        beta=beta,
    )
    e0 = energy(u, v, w)
    x0 = enstrophy(u, v, w, kx, ky, kz)
    check0 = instantaneous_energy_check(u, v, w, **kw)
    visc_int = 0.0
    q1_int = 0.0
    visc_prev = check0["viscous_inner"]
    q1_prev = check0["q1_inner"]
    steps = max(1, int(round(t_end / dt)))
    dt = t_end / steps
    for _ in range(steps):
        u, v, w = rk4_step(u, v, w, dt, **kw)
        # S2: accepted-state diagnostics, not the predictor field.
        check = instantaneous_energy_check(u, v, w, **kw)
        visc_int += 0.5 * (visc_prev + check["viscous_inner"]) * dt
        q1_int += 0.5 * (q1_prev + check["q1_inner"]) * dt
        visc_prev, q1_prev = check["viscous_inner"], check["q1_inner"]

    e_t = energy(u, v, w)
    retired = abs(e_t + visc_int + q1_int - e0)
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
        residual=check["residual"],
        relative_residual=check["relative_residual"],
        retired_integrated_residual=retired,
        enstrophy0=x0,
        enstrophy_t=enstrophy(u, v, w, kx, ky, kz),
        max_div=max_div(u, v, w, kx, ky, kz),
    )


def main() -> int:
    p = argparse.ArgumentParser(description="NS solver-core energy check (S1–S3)")
    p.add_argument("--n", type=int, default=16)
    p.add_argument("--nu", type=float, default=0.02)
    p.add_argument("--alpha", type=float, default=1.0)
    p.add_argument("--beta", type=float, default=0.5)
    p.add_argument("--t", type=float, default=0.4)
    p.add_argument("--dt", type=float, default=0.01)
    p.add_argument("--eps", type=float, nargs="+", default=[0.0, 0.05, 0.2])
    p.add_argument("--out", type=Path, default=Path("results/ns_solver_core.json"))
    args = p.parse_args()

    rows = []
    print(
        f"{'eps':>8} {'E0':>10} {'ET':>10} {'visc':>10} {'Q1':>10} "
        f"{'inst':>10} {'rel':>10} {'retired':>10} {'div':>10}"
    )
    for eps in args.eps:
        r = run_once(args.n, args.nu, eps, args.alpha, args.beta, args.t, args.dt)
        rows.append(asdict(r))
        print(
            f"{r.eps:8.3f} {r.energy0:10.4f} {r.energy_t:10.4f} {r.diss_visc:10.4f} "
            f"{r.diss_q1:10.4f} {r.residual:10.3e} {r.relative_residual:10.3e} "
            f"{r.retired_integrated_residual:10.3e} {r.max_div:10.2e}"
        )

    payload = {
        "meta": {
            "track": "solver-core",
            "note": (
                "Instantaneous inner-product energy check. "
                "Not a proof that smooth solutions stay smooth. "
                "Classical NS stays open."
            ),
            "fixes": [
                "S1_instantaneous_power_balance",
                "S2_accepted_state_diagnostics",
                "S3_inner_product_dissipation",
            ],
            "n": args.n,
            "nu": args.nu,
            "alpha": args.alpha,
            "beta": args.beta,
            "t": args.t,
            "dt": args.dt,
        },
        "runs": rows,
        "ns_solved": False,
        "classical_ns_open": True,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
