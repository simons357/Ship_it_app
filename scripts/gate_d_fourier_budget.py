#!/usr/bin/env python3
"""Gate D: accelerated Fourier solver, dynamical-budget measurements.

Classical unforced Navier–Stokes on T³. Integrating-factor RK4 treats
viscosity exactly so the nonlinear term can take a larger step than
the explicit viscous RK4 in the S1–S3 core.

This file measures regeneration, turnover, and danger episodes. It does
not establish a cutoff-independent budget. Not (17). NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_solver_core import (  # noqa: E402
    VOL_T3,
    _convective_hat,
    energy,
    enstrophy,
    fft,
    grad_components,
    ifft,
    inner,
    make_grid,
    max_div,
    project,
    project_state,
    taylor_green,
)


def nonlinear_hat(u, v, w, kx, ky, kz, k2_safe, dealias):
    du, _, _, _ = grad_components(u, v, w, kx, ky, kz)
    cuh, cvh, cwh = _convective_hat(u, v, w, du, kx, ky, kz, k2_safe, dealias)
    # rhs nonlinear in Fourier space: -P(u·∇u)
    return -cuh, -cvh, -cwh, du


def ifrk4_step(uh, vh, wh, dt, kx, ky, kz, k2, k2_safe, dealias, nu):
    """Integrating-factor RK4: L = −ν|k|² exact, N = −P(u·∇u)."""
    decay_full = np.exp(-nu * k2 * dt)
    decay_half = np.exp(-nu * k2 * (0.5 * dt))

    def n_from_hat(u_h, v_h, w_h):
        u, v, w = ifft(u_h), ifft(v_h), ifft(w_h)
        nuh, nvh, nwh, du = nonlinear_hat(u, v, w, kx, ky, kz, k2_safe, dealias)
        return nuh, nvh, nwh, du

    n1u, n1v, n1w, _ = n_from_hat(uh, vh, wh)
    u2 = decay_half * (uh + 0.5 * dt * n1u)
    v2 = decay_half * (vh + 0.5 * dt * n1v)
    w2 = decay_half * (wh + 0.5 * dt * n1w)
    n2u, n2v, n2w, _ = n_from_hat(u2, v2, w2)
    u3 = decay_half * uh + 0.5 * dt * n2u
    v3 = decay_half * vh + 0.5 * dt * n2v
    w3 = decay_half * wh + 0.5 * dt * n2w
    n3u, n3v, n3w, _ = n_from_hat(u3, v3, w3)
    u4 = decay_full * uh + dt * decay_half * n3u
    v4 = decay_full * vh + dt * decay_half * n3v
    w4 = decay_full * wh + dt * decay_half * n3w
    n4u, n4v, n4w, du = n_from_hat(u4, v4, w4)
    uh_n = decay_full * uh + (dt / 6.0) * (
        decay_full * n1u + 2.0 * decay_half * n2u + 2.0 * decay_half * n3u + n4u
    )
    vh_n = decay_full * vh + (dt / 6.0) * (
        decay_full * n1v + 2.0 * decay_half * n2v + 2.0 * decay_half * n3v + n4v
    )
    wh_n = decay_full * wh + (dt / 6.0) * (
        decay_full * n1w + 2.0 * decay_half * n2w + 2.0 * decay_half * n3w + n4w
    )
    uh_n, vh_n, wh_n = project(uh_n, vh_n, wh_n, kx, ky, kz, k2_safe)
    return uh_n, vh_n, wh_n, du


def shell_energy(uh, vh, wh, k2, n: int) -> dict[int, float]:
    amp2 = np.abs(uh) ** 2 + np.abs(vh) ** 2 + np.abs(wh) ** 2
    shells: dict[int, float] = {}
    k2i = np.rint(k2).astype(int)
    scale = 0.5 * VOL_T3 / (n**6)
    for val in np.unique(k2i):
        iv = int(val)
        if iv == 0:
            continue
        shells[iv] = float(np.sum(amp2[k2i == iv])) * scale
    return shells


def local_extrema(series: list[float], *, min_rel: float = 1e-8) -> dict:
    """Count interior local maxima / minima; regeneration = min then later max."""
    peaks = []
    troughs = []
    for i in range(1, len(series) - 1):
        if series[i] >= series[i - 1] and series[i] > series[i + 1]:
            peaks.append(i)
        if series[i] <= series[i - 1] and series[i] < series[i + 1]:
            troughs.append(i)
    regen = 0
    for t in troughs:
        if any(p > t and series[p] > series[t] + min_rel for p in peaks):
            regen += 1
    gaps = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
    return {
        "n_peaks": len(peaks),
        "n_troughs": len(troughs),
        "regeneration_events": regen,
        "turnover_gaps_steps": gaps,
        "mean_turnover_steps": float(np.mean(gaps)) if gaps else None,
    }


def broadband_ic(n: int, seed: int, k_peak: float = 3.0):
    """Deterministic divergence-free broadband field (unforced)."""
    rng = np.random.default_rng(seed)
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    shape = kx.shape
    spec = np.exp(-0.5 * (np.sqrt(k2) / k_peak) ** 2)
    spec[0, 0, 0] = 0.0
    uh = spec * (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    vh = spec * (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    wh = spec * (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    uh, vh, wh = project(uh, vh, wh, kx, ky, kz, k2_safe)
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    return u, v, w


def run_budget(
    n: int,
    nu: float,
    t_end: float,
    dt: float,
    *,
    seed: int = 0,
    ic: str = "broadband",
    high_shell_frac: float = 0.5,
    danger_ratio: float = 1.0,
) -> dict:
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    if ic == "taylor_green":
        u, v, w = taylor_green(n)
    else:
        u, v, w = broadband_ic(n, seed=seed)
    u, v, w = project_state(u, v, w, kx, ky, kz, k2_safe)
    uh, vh, wh = fft(u), fft(v), fft(w)
    kmax = float(np.max(np.sqrt(k2)))
    high_cut = (high_shell_frac * kmax) ** 2

    steps = max(1, int(round(t_end / dt)))
    dt = t_end / steps
    times = []
    energies = []
    enstrophies = []
    high_series = []
    danger_flags = []
    transfer_series = []
    visc_series = []
    e0 = energy(u, v, w)

    for s in range(steps + 1):
        t = s * dt
        u, v, w = ifft(uh), ifft(vh), ifft(wh)
        e = energy(u, v, w)
        x = enstrophy(u, v, w, kx, ky, kz)
        nuh, nvh, nwh, du = nonlinear_hat(u, v, w, kx, ky, kz, k2_safe, dealias)
        transfer = float(inner(u, v, w, ifft(nuh), ifft(nvh), ifft(nwh)))
        visc = nu * float(
            np.mean(sum(du[i][j] ** 2 for i in range(3) for j in range(3)))
        ) * VOL_T3
        shells = shell_energy(uh, vh, wh, k2, n)
        high = sum(val for rad, val in shells.items() if rad >= high_cut)
        danger = visc > 0 and abs(transfer) > danger_ratio * visc and s > 0
        times.append(t)
        energies.append(e)
        enstrophies.append(x)
        high_series.append(high)
        danger_flags.append(bool(danger))
        transfer_series.append(transfer)
        visc_series.append(visc)
        if s == steps:
            break
        uh, vh, wh, _ = ifrk4_step(
            uh, vh, wh, dt, kx, ky, kz, k2, k2_safe, dealias, nu
        )

    high_ext = local_extrema(high_series)
    ens_ext = local_extrema(enstrophies)
    danger_episodes = 0
    in_ep = False
    for flag in danger_flags:
        if flag and not in_ep:
            danger_episodes += 1
            in_ep = True
        elif not flag:
            in_ep = False

    return {
        "n": n,
        "nu": nu,
        "t_end": t_end,
        "dt": dt,
        "ic": ic,
        "seed": seed,
        "energy0": e0,
        "energy_end": energies[-1],
        "enstrophy0": enstrophies[0],
        "enstrophy_end": enstrophies[-1],
        "max_div_end": max_div(ifft(uh), ifft(vh), ifft(wh), kx, ky, kz),
        "high_shell": high_ext,
        "enstrophy_extrema": ens_ext,
        "danger_episodes": danger_episodes,
        "danger_ratio": danger_ratio,
        "n_steps": steps,
        "energy_decayed": energies[-1] < energies[0],
        "cutoff_independent_budget": False,
        "ns_solved": False,
        "classical_ns_open": True,
        "series": {
            "t": times,
            "energy": energies,
            "enstrophy": enstrophies,
            "high_shell_energy": high_series,
            "transfer": transfer_series,
            "viscous": visc_series,
            "danger": danger_flags,
        },
    }


def cutoff_compare(payload_a: dict, payload_b: dict) -> dict:
    """Diagnostic only: episode counts vs grid. Not a budget theorem."""
    return {
        "n_pair": [payload_a["n"], payload_b["n"]],
        "danger_episodes": [payload_a["danger_episodes"], payload_b["danger_episodes"]],
        "high_regeneration": [
            payload_a["high_shell"]["regeneration_events"],
            payload_b["high_shell"]["regeneration_events"],
        ],
        "energy_end_ratio": payload_b["energy_end"] / payload_a["energy_end"]
        if payload_a["energy_end"]
        else None,
        "same_episode_count": payload_a["danger_episodes"] == payload_b["danger_episodes"],
        "cutoff_independent_budget": False,
        "note": (
            "Matching finite-grid episode counts is not a cutoff-independent "
            "dynamical budget."
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Gate D Fourier dynamical-budget probe")
    p.add_argument("--n", type=int, nargs="+", default=[8, 12])
    p.add_argument("--nu", type=float, default=0.05)
    p.add_argument("--t", type=float, default=0.2)
    p.add_argument("--dt", type=float, default=0.02)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--ic", choices=("broadband", "taylor_green"), default="broadband")
    p.add_argument("--out", type=Path, default=Path("results/gate_d_fourier_budget.json"))
    args = p.parse_args()

    runs = [
        run_budget(n, args.nu, args.t, args.dt, seed=args.seed, ic=args.ic)
        for n in args.n
    ]
    # Drop long series from the on-disk summary except endpoints.
    slim = []
    for r in runs:
        s = dict(r)
        series = s.pop("series")
        s["series_endpoints"] = {
            "t0": series["t"][0],
            "t1": series["t"][-1],
            "energy0": series["energy"][0],
            "energy1": series["energy"][-1],
            "enstrophy0": series["enstrophy"][0],
            "enstrophy1": series["enstrophy"][-1],
        }
        slim.append(s)
    compare = cutoff_compare(runs[0], runs[-1]) if len(runs) >= 2 else None
    payload = {
        "meta": {
            "gate": "D",
            "solver": "integrating_factor_rk4",
            "equation": "classical unforced Navier-Stokes on T^3",
            "note": (
                "Regeneration / turnover / danger-episode measurements. "
                "Not a cutoff-independent budget. Not (17). NS not solved."
            ),
        },
        "runs": slim,
        "cutoff_compare": compare,
        "ns_solved": False,
        "cutoff_independent_budget": False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))
    print(
        f"{'n':>6} {'E0':>10} {'ET':>10} {'X0':>10} {'XT':>10} "
        f"{'regen':>8} {'danger':>8} {'div':>10}"
    )
    for r in runs:
        print(
            f"{r['n']:6d} {r['energy0']:10.4f} {r['energy_end']:10.4f} "
            f"{r['enstrophy0']:10.4f} {r['enstrophy_end']:10.4f} "
            f"{r['high_shell']['regeneration_events']:8d} "
            f"{r['danger_episodes']:8d} {r['max_div_end']:10.2e}"
        )
    if compare:
        print("cutoff compare:", json.dumps(compare))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
