#!/usr/bin/env python3
"""
P1-loc cutoff Biot-Savart / energy.

Classical NS. No Q1. No K(t). Not WRITE (6).
The cutoff inequality sits. Dropping ∇u does not.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from track_b_lemmas import curl, ifft, make_grid, project, rec  # noqa: E402

C_ENERGY = 1.5 * np.pi**2  # 3π²/2
C_GRAD = 4.0


def _per_dist(x: np.ndarray, c: float) -> np.ndarray:
    d = np.abs(x - c)
    return np.minimum(d, 2.0 * np.pi - d)


def cosine_cutoff(n: int, rho: float):
    x = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r = np.sqrt(
        _per_dist(X, np.pi) ** 2 + _per_dist(Y, np.pi) ** 2 + _per_dist(Z, np.pi) ** 2
    )
    eta = np.zeros_like(r)
    inner = r <= rho
    outer = r >= 2.0 * rho
    mid = ~inner & ~outer
    t = (r[mid] - rho) / rho
    eta[inner] = 1.0
    eta[mid] = 0.5 * (1.0 + np.cos(np.pi * t))
    dndr = np.zeros_like(r)
    dndr[mid] = -0.5 * (np.pi / rho) * np.sin(np.pi * t)
    # unit radial in periodic metric
    rx = np.where(r > 0, (X - np.pi) - 2.0 * np.pi * np.round((X - np.pi) / (2.0 * np.pi)), 0.0)
    ry = np.where(r > 0, (Y - np.pi) - 2.0 * np.pi * np.round((Y - np.pi) / (2.0 * np.pi)), 0.0)
    rz = np.where(r > 0, (Z - np.pi) - 2.0 * np.pi * np.round((Z - np.pi) / (2.0 * np.pi)), 0.0)
    inv = np.zeros_like(r)
    np.divide(1.0, r, out=inv, where=r > 0)
    gx, gy, gz = dndr * rx * inv, dndr * ry * inv, dndr * rz * inv
    return eta, r, (gx, gy, gz)


def _band_field(n: int, kmin: float, kmax: float, seed: int):
    rng = np.random.default_rng(seed)
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    shape = (n, n, n)
    uh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    vh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    wh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    kabs = np.sqrt(np.maximum(k2, 0.0))
    band = (kabs > kmin) & (kabs <= kmax) & dealias
    uh, vh, wh = uh * band, vh * band, wh * band
    uh, vh, wh = project(uh, vh, wh, kx, ky, kz, k2_safe)
    return uh, vh, wh, kx, ky, kz


def _grad_sq(uh, vh, wh, kx, ky, kz) -> np.ndarray:
    acc = np.zeros_like(ifft(uh))
    for comp in (uh, vh, wh):
        for kk in (kx, ky, kz):
            acc = acc + ifft(1j * kk * comp) ** 2
    return acc


def _measure(field: np.ndarray, n: int) -> float:
    return float(np.mean(field) * (2.0 * np.pi) ** 3)


def one_field(n: int, rho: float, kmin: float, kmax: float, seed: int) -> dict:
    uh, vh, wh, kx, ky, kz = _band_field(n, kmin, kmax, seed)
    ox, oy, oz, _, _, _ = curl(uh, vh, wh, kx, ky, kz)
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    eta, r, _ = cosine_cutoff(n, rho)
    w2 = ox * ox + oy * oy + oz * oz
    u2 = u * u + v * v + w * w
    g2 = _grad_sq(uh, vh, wh, kx, ky, kz)
    ball = r <= rho
    big = r <= 2.0 * rho
    left = _measure(w2 * ball, n)
    right_g = _measure(g2 * big, n)
    right_u = _measure(u2 * big, n)
    right = C_GRAD * right_g + C_ENERGY * (rho**-2) * right_u
    thin = (rho * rho) * left / max(right_u, 1e-30)
    return {
        "n": n,
        "rho": float(rho),
        "kmin": float(kmin),
        "kmax": float(kmax),
        "seed": seed,
        "left": left,
        "right": right,
        "right_grad": right_g,
        "right_u": right_u,
        "held": left <= right * (1.0 + 1e-6),
        "thinness_drop_gradu": thin,
    }


def sweep(n: int = 32, seed: int = 7) -> dict:
    rho = 0.9
    mixed = [
        one_field(n, rho, 0.0, 4.0, seed + i) for i in range(3)
    ]
    high = [
        one_field(n, rho, 8.0, 12.0, seed + 20 + i) for i in range(3)
    ]
    return {
        "meta": {
            "slot": "B",
            "write": "H1 P1-loc cutoff Biot-Savart / energy",
            "tuning_the_pde": False,
            "h1_proved": False,
            "lemma_p1loc_sits": True,
            "drop_gradu": False,
            "nse_class": "open",
            "n": n,
            "rho": rho,
            "C_grad": C_GRAD,
            "C_energy": C_ENERGY,
        },
        "mixed": mixed,
        "highpass": high,
    }


def lemmas(payload: dict) -> list[dict]:
    mixed = payload["mixed"]
    high = payload["highpass"]
    held = all(r["held"] for r in mixed + high)
    # Drop ∇u: high-pass thinness should exceed a generous O(1)
    drops = all(r["thinness_drop_gradu"] > 4.0 for r in high)
    return [
        rec(
            "H1p1loc_cutoff_sits",
            "∫_{Bρ}|ω|² ≤ 4∫_{B_{2ρ}}|∇u|² + C ρ^{-2} ∫_{B_{2ρ}}|u|²",
            "pass" if held else "fail",
            "Cutoff product rule. ∇u stays. Not a frequency class.",
            left=[r["left"] for r in mixed],
            right=[r["right"] for r in mixed],
        ),
        rec(
            "H1p1loc_drop_gradu",
            "ρ² ∫_{Bρ}|ω|² ≲ ∫_{B_{2ρ}}|u|² after the cutoff",
            "fail" if drops else "open",
            "High-pass at the same ρ breaks the O(1) drop. Class still needed.",
            thinness=[r["thinness_drop_gradu"] for r in high],
        ),
        rec(
            "H1p1loc_is_h1",
            "Lemma P1-loc is WRITE (6) / H1",
            "fail",
            "A localized energy identity is not A_bad versus dissipation.",
        ),
        rec(
            "H1p1loc_nse_class",
            "NSE puts Bad on a class that drops ∇u",
            "open",
            "No candidate. Do not invent a drop. Do not cash as (6).",
        ),
    ]


def run(n: int = 32, seed: int = 7, out: Path | None = None) -> dict:
    payload = sweep(n=n, seed=seed)
    rows = lemmas(payload)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in rows:
        counts[row["verdict"]] += 1
    payload["lemmas"] = rows
    payload["counts"] = counts
    payload["domain_verdict"] = "open"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=32)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    payload = run(n=args.n, seed=args.seed, out=args.out)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
