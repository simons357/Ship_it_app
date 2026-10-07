#!/usr/bin/env python3
"""All-shape charge-count kill probe (desk step 1).

Convention (locked by matching independent desk table):
  - Fix high shell squared radius c.
  - Enumerate lattice triads q + p + k = 0 with |q|² = c and 1 ≤ |p|² ≤ c.
  - Record unordered shape (a, b, c) with a = min(|p|², |k|²), b = max(...).
  - Drop collinear / zero-transfer shapes: (x − y − z)² = 4yz for some
    permutation of the three legs.

Desk reference (independent Oct 7 recompute):
  c=25 → 266; c=50 → 1254; c=101 → 5185; c=401 → 58550.

This is a *count* probe. Weighted sum with audit ρ needs the ZIP formula
for per-shape constants — face values ρ, ρ′ alone are not enough.
Not a proof. Not criterion (17). NS not solved.
"""

from __future__ import annotations

import json
import time
from math import isqrt
from pathlib import Path

# 32-package thirds (anchors (5,25) and active (9,25))
PKG_5 = {8, 10, 14, 18, 20, 22, 24, 26, 30, 34, 36, 38, 40, 42, 46, 50, 52}
PKG_9 = {6, 10, 12, 14, 16, 24, 30, 34, 38, 44, 52, 54, 56, 58, 62}
PKG_SHAPES = {(5, b, 25) for b in PKG_5} | {(9, b, 25) for b in PKG_9}

DESK = {25: 266, 50: 1254, 101: 5185, 401: 58550}

OUT = Path(__file__).resolve().parents[2] / "results" / "shared_budget"
OUT.mkdir(parents=True, exist_ok=True)


def shell_pts(r2: int) -> list[tuple[int, int, int]]:
    R = isqrt(r2)
    pts: list[tuple[int, int, int]] = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            z2 = r2 - x * x - y * y
            if z2 < 0:
                continue
            z = isqrt(z2)
            if z * z == z2:
                pts.append((x, y, z))
                if z:
                    pts.append((x, y, -z))
    return pts


def ball_pts(pmax: int) -> list[tuple[int, int, int, int]]:
    """Lattice points with 1 ≤ |p|² ≤ pmax, as (x,y,z,r2)."""
    P = isqrt(pmax)
    pts: list[tuple[int, int, int, int]] = []
    for x in range(-P, P + 1):
        for y in range(-P, P + 1):
            for z in range(-P, P + 1):
                r2 = x * x + y * y + z * z
                if 1 <= r2 <= pmax:
                    pts.append((x, y, z, r2))
    return pts


def is_collinear(a: int, b: int, c: int) -> bool:
    for x, y, z in ((a, b, c), (b, a, c), (c, a, b)):
        if (x - y - z) ** 2 == 4 * y * z:
            return True
    return False


def shapes_charging_shell(c: int, pmax: int | None = None) -> set[tuple[int, int, int]]:
    if pmax is None:
        pmax = c
    sc = shell_pts(c)
    ps = ball_pts(pmax)
    shapes: set[tuple[int, int, int]] = set()
    for qx, qy, qz in sc:
        for px, py, pz, pr in ps:
            kx, ky, kz = -(qx + px), -(qy + py), -(qz + pz)
            kr = kx * kx + ky * ky + kz * kz
            if kr == 0:
                continue
            a, b = sorted((pr, kr))
            if is_collinear(a, b, c):
                continue
            shapes.add((a, b, c))
    return shapes


def package_coverage(c: int, shapes: set[tuple[int, int, int]]) -> int:
    """How many of the 32 package shapes charge shell c under this convention."""
    if c == 25:
        n = 0
        for anc, b, hi in PKG_SHAPES:
            key = (min(anc, b), max(anc, b), hi)
            if key in shapes:
                n += 1
        return n
    # For other shells: package thirds that equal c (desk: 50→1, 101→0, 401→0)
    return sum(1 for _anc, b, _hi in PKG_SHAPES if b == c)


def main() -> None:
    plan = [25, 50, 101, 401]
    rows = []
    all_match = True
    for c in plan:
        t0 = time.time()
        print(f"counting shell {c} ...", flush=True)
        shapes = shapes_charging_shell(c)
        elapsed = time.time() - t0
        n = len(shapes)
        desk = DESK[c]
        match = n == desk
        all_match = all_match and match
        covered = package_coverage(c, shapes)
        growth = n / (c * c) if c else None
        row = {
            "shell_c": c,
            "n_shapes_charging": n,
            "desk_reference_count": desk,
            "matches_desk": match,
            "n_package_covered": covered,
            "growth_n_over_c2": growth,
            "elapsed_sec": round(elapsed, 3),
            "sample_hits": sorted(shapes)[:12],
        }
        rows.append(row)
        print(
            f"  -> {n} (desk {desk}, match={match}, pkg={covered}, "
            f"n/c²={growth:.4f}, {elapsed:.2f}s)",
            flush=True,
        )

    payload = {
        "status": "COUNT_PROBE_PASS" if all_match else "COUNT_PROBE_MISMATCH",
        "purpose": "kill-test step 1 — all-shape charge counts vs desk table",
        "convention": {
            "high_shell": "fixed c = |q|²",
            "p_range": "1 ≤ |p|² ≤ c",
            "shape_id": "unordered (a,b,c) with a≤b",
            "exclude": "collinear / zero-transfer legs",
        },
        "growth_observation": (
            "n ≈ 0.4 c² (desk reading). High-pass gain only c^{-1/2}. "
            "All-shape rule needs average per-shape constant faster than ~c^{-3/2}."
        ),
        "weighted_rho_sum": (
            "NOT RUN — needs audit per-shape ρ formula from "
            "Shared-Budget-17-Family-Audit-and-9-25-Extension.zip. "
            "Face values ρ≈0.6318550824, ρ′≈0.8253067330 alone do not define "
            "the all-shape weighted sum."
        ),
        "expectation": (
            "Weighted sum expected to fail; if so, stop extending families — "
            "route closed as a standalone argument toward (17)."
        ),
        "charging_convention_for_32_package": (
            "Zero-pruned multiplicity 4 at R=216 holds if only third shell b "
            "and the 25-shell are charged (low anchors bounded by √E₀). "
            "If low anchors 5n² and 9n² are also charged, R=3600 picks up a "
            "fifth charge (9·20²) and coefficient → 2ρ+3ρ′≈3.7396."
        ),
        "rows": rows,
        "all_desk_counts_match": all_match,
        "ns_regularity": "open",
        "criterion_17": "open",
    }
    out = OUT / "all_shape_charge_count_kill.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in (
        "status", "all_desk_counts_match", "weighted_rho_sum", "expectation"
    )}, indent=2))
    print(f"wrote {out}")
    if not all_match:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
