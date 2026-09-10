#!/usr/bin/env python3
"""
P1 low-pass Biot-Savart thinness.

Classical NS. No Q1. No K(t). Not WRITE (6).
The estimate sits on {ω : |k| ≤ K}. NSE membership
is not this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from track_b_lemmas import curl, make_grid, project, rec  # noqa: E402


def _energy_hat(uh, vh, wh) -> float:
    return float(np.sum(np.abs(uh) ** 2 + np.abs(vh) ** 2 + np.abs(wh) ** 2))


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
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    e_u = _energy_hat(uh, vh, wh)
    e_w = _energy_hat(oxh, oyh, ozh)
    if e_u <= 0.0:
        raise RuntimeError("empty band")
    ratio = e_w / e_u
    k_used = kabs[(np.abs(uh) + np.abs(vh) + np.abs(wh)) > 0]
    return {
        "n": n,
        "kmin": float(kmin),
        "kmax": float(kmax),
        "seed": seed,
        "modes": int(np.sum(band)),
        "k_min_used": float(np.min(k_used)) if k_used.size else 0.0,
        "k_max_used": float(np.max(k_used)) if k_used.size else 0.0,
        "ratio_w_over_u": ratio,
        "bound_kmax2": float(kmax * kmax),
        "bound_kmin2": float(kmin * kmin) if kmin > 0 else 0.0,
    }


def sweep(n: int = 32, seed: int = 7) -> dict:
    low = [_band_field(n, 0.0, k, seed + i) for i, k in enumerate((2.0, 3.0, 4.0))]
    high = [_band_field(n, 8.0, 12.0, seed + 20 + i) for i in range(3)]
    return {
        "meta": {
            "slot": "B",
            "write": "H1 P1 low-pass Biot-Savart",
            "tuning_the_pde": False,
            "h1_proved": False,
            "lemma_p1_sits": True,
            "nse_class": "open",
            "n": n,
        },
        "lowpass": low,
        "highpass": high,
    }


def lemmas(payload: dict) -> list[dict]:
    low = payload["lowpass"]
    high = payload["highpass"]
    low_ok = all(r["ratio_w_over_u"] <= r["bound_kmax2"] * (1.0 + 1e-9) for r in low)
    # High-pass must sit above kmin^2 and beat the low-pass K=3 bound
    # at rho = 1/3, i.e. rho^2 ∫|ω|^2 / ∫|u|^2 = ratio / 9.
    high_floor = all(r["ratio_w_over_u"] >= r["bound_kmin2"] * 0.99 for r in high)
    rho = 1.0 / 3.0
    high_breaks = all((rho * rho) * r["ratio_w_over_u"] > 4.0 for r in high)
    low_held = all((rho * rho) * r["ratio_w_over_u"] <= 1.0 + 1e-9 for r in low if r["kmax"] <= 3.0)
    return [
        rec(
            "H1p1_lowpass_sits",
            "∫|ω|² ≤ K² ∫|u|² on |k|≤K, from Biot-Savart / Plancherel",
            "pass" if low_ok and low_held else "fail",
            "The estimate sits on the stated class. Not a Gaussian number.",
            ratios=[r["ratio_w_over_u"] for r in low],
            bounds=[r["bound_kmax2"] for r in low],
        ),
        rec(
            "H1p1_highpass_needed",
            "high-pass at the same ρ breaks the O(1) thinness claim",
            "pass" if high_floor and high_breaks else "fail",
            "The class is necessary. NSE membership is the hole.",
            ratios=[r["ratio_w_over_u"] for r in high],
            rho=rho,
            high_thinness=[(rho * rho) * r["ratio_w_over_u"] for r in high],
        ),
        rec(
            "H1p1_is_h1",
            "Lemma P1 is WRITE (6) / H1",
            "fail",
            "Frequency localization of ω is not A_bad versus dissipation. Not H1.",
        ),
        rec(
            "H1p1_nse_class",
            "NSE puts Bad vorticity in the low-pass class",
            "open",
            "No candidate. Do not cash P1 as (6).",
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
