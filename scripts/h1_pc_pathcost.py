#!/usr/bin/env python3
"""
PC path-cost of one Bad pair.

Classical NS leftover class. No Q1. No K(t). Not WRITE (6).
The 1-D bound sits. Gap / thin tube show it is not H1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from track_b_lemmas import rec  # noqa: E402


def _unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n <= 0.0:
        raise RuntimeError("zero vector")
    return v / n


def geodesic(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))


def sin_phi(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(np.cross(a, b)))


def sphere_sample(n: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    gaps = []
    for _ in range(n):
        a = _unit(rng.normal(size=3))
        b = _unit(rng.normal(size=3))
        phi = geodesic(a, b)
        s = sin_phi(a, b)
        gaps.append(phi - s)
    return {
        "n": n,
        "min_phi_minus_sin": float(np.min(gaps)),
        "all_geodesic": bool(np.min(gaps) >= -1e-12),
    }


def rotating_segment(alpha: float, rho: float, steps: int = 400) -> dict:
    # ξ(z) = (cos(α z/ρ), sin(α z/ρ), 0), z ∈ [0, ρ]
    z = np.linspace(0.0, rho, steps)
    ang = alpha * z / rho
    xi = np.stack((np.cos(ang), np.sin(ang), np.zeros_like(ang)), axis=1)
    dxi = np.diff(xi, axis=0)
    chord = float(np.sum(np.linalg.norm(dxi, axis=1)))
    # |∂z ξ| = α/ρ exactly, so ∫|∇ξ| ds = α. Chords underestimate the arc.
    path = float(alpha)
    phi = geodesic(xi[0], xi[-1])
    s = sin_phi(xi[0], xi[-1])
    grad = alpha / rho
    return {
        "alpha": float(alpha),
        "rho": float(rho),
        "phi": phi,
        "sin_phi": s,
        "path_cost": path,
        "chord_sum": chord,
        "grad_along": float(grad),
        "path_ge_phi": path + 1e-12 >= phi,
        "phi_ge_sin": phi + 1e-12 >= s,
    }


def gap_two_blobs(rho: float, blob_r: float) -> dict:
    # {|ω|≥Λ} = B(0,r) ∪ B(ρ e_1, r) with ρ > 2r: disconnected.
    connected = rho <= 2.0 * blob_r
    return {
        "rho": float(rho),
        "blob_r": float(blob_r),
        "high_set_connected": bool(connected),
        "path_exists_in_high_set": bool(connected),
    }


def thin_tube_fold(alpha: float, rho: float, eps: float) -> dict:
    # Rotation in a tube of radius ε about the segment.
    # Path along the axis still costs α.
    # Volume model: |∇ξ| ~ α/ρ on volume π ε² ρ.
    path = float(alpha)
    vol = float(np.pi * (eps**2) * rho * (alpha / rho) ** 2)
    fold_target = float(rho * rho)
    return {
        "alpha": float(alpha),
        "rho": float(rho),
        "eps": float(eps),
        "path_cost": path,
        "volume_grad2": vol,
        "fold_target_rho2": fold_target,
        "volume_lt_fold": vol < 0.25 * fold_target,
    }


def sweep(seed: int = 7) -> dict:
    sphere = sphere_sample(400, seed)
    c_star = 0.25
    rho = 0.04
    alpha = 0.8  # |sin α| ≈ 0.717 > C_* √ρ ≈ 0.05
    rot = rotating_segment(alpha, rho)
    bad = rot["sin_phi"] > c_star * np.sqrt(rho)
    rot["c_star"] = c_star
    rot["bad_cut"] = bool(bad)
    rot["path_gt_cstar_root"] = bool(rot["path_cost"] > c_star * np.sqrt(rho))
    gap = gap_two_blobs(rho=1.0, blob_r=0.2)
    tube = thin_tube_fold(alpha=0.8, rho=0.5, eps=0.02)
    return {
        "meta": {
            "slot": "B",
            "write": "H1 PC path-cost of one Bad pair",
            "tuning_the_pde": False,
            "h1_proved": False,
            "lemma_pc_sits": True,
            "lemma_pc_is_h1": False,
        },
        "sphere": sphere,
        "rotating": rot,
        "gap": gap,
        "thin_tube": tube,
    }


def lemmas(payload: dict) -> list[dict]:
    sph = payload["sphere"]
    rot = payload["rotating"]
    gap = payload["gap"]
    tube = payload["thin_tube"]
    return [
        rec(
            "H1pc_geodesic_sits",
            "φ ≥ |sin φ| on S²",
            "pass" if sph["all_geodesic"] else "fail",
            "Sphere geometry. No NSE.",
            min_gap=sph["min_phi_minus_sin"],
        ),
        rec(
            "H1pc_path_sits",
            "rotating field: ∫_γ |∇ξ| ≥ φ ≥ |sin φ|",
            "pass" if rot["path_ge_phi"] and rot["phi_ge_sin"] else "fail",
            "Chain rule on one C¹ path. Not a volume integral.",
            path_cost=rot["path_cost"],
            phi=rot["phi"],
        ),
        rec(
            "H1pc_bad_cut",
            "Bad cut ⇒ path-cost > C_* ρ^{1/2} on that field",
            "pass" if rot["bad_cut"] and rot["path_gt_cstar_root"] else "fail",
            "Uses the WRITE (6) angular cut. Still one curve.",
            c_star=rot["c_star"],
            rho=rot["rho"],
        ),
        rec(
            "H1pc_gap",
            "two blobs: no path in {|ω|≥Λ}",
            "pass" if (not gap["path_exists_in_high_set"]) else "fail",
            "Lemma PC does not apply. The pair can still be Bad.",
            rho=gap["rho"],
            blob_r=gap["blob_r"],
        ),
        rec(
            "H1pc_not_fold",
            "thin tube keeps path-cost and drops volume below ρ²",
            "pass" if tube["volume_lt_fold"] and tube["path_cost"] > 0.5 else "fail",
            "1-D bound is not ∫_{B_{2ρ}} |∇ω|² ≳ Λ² ρ². Not shape 2.",
            volume_grad2=tube["volume_grad2"],
            fold_target=tube["fold_target_rho2"],
        ),
        rec(
            "H1pc_is_h1",
            "Lemma PC is WRITE (6) / H1",
            "fail",
            "A segment lower bound is not A_bad versus dissipation. Not H1.",
        ),
    ]


def run(seed: int = 7, out: Path | None = None) -> dict:
    payload = sweep(seed=seed)
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
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    payload = run(seed=args.seed, out=args.out)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
