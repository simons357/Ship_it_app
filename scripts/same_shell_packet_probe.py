#!/usr/bin/env python3
"""Same-shell packet probe: two fixed-gap lattice spheres, not an AP.

Counts integer points on |k|^2 = n and |k|^2 = n+d, then unordered
additive closures k+p+r = 0 of mixed type (n, n, n+d).

This is a combinatorial check of the natural whole-sphere ensemble.
It does not prove a uniform triadic bound and does not solve Navier–Stokes.

D_s here is the two-mass spectral remainder (XZ - Y^2)/X for equal L^2
mass on the two shells, with Stokes eigenvalues λ = n and μ = n+d.
That uses the gap d, not an AP width. For fixed d it scales as O(n).

R_star from the 10 Sep 2026 note is recorded as user-reported numerics
in the companion markdown. This script does not invent that ratio.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
Vec = Tuple[int, int, int]


def lattice_sphere(n: int) -> Set[Vec]:
    """Integer points k in Z^3 with |k|^2 = n."""
    if n < 0:
        return set()
    r = int(math.isqrt(n)) + 2
    pts: Set[Vec] = set()
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            z2 = n - x * x - y * y
            if z2 < 0:
                continue
            z = int(math.isqrt(z2))
            if z * z == z2:
                pts.add((x, y, z))
                if z:
                    pts.add((x, y, -z))
    return pts


def nrm2(k: Vec) -> int:
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def mixed_gap_closures(
    shell_n: Iterable[Vec], shell_np: Iterable[Vec], n: int, d: int
) -> List[FrozenSet[Vec]]:
    """Unique {k,p,r} with k+p+r=0 and shells (n, n, n+d)."""
    packet = set(shell_n) | set(shell_np)
    pts = list(packet)
    found: List[FrozenSet[Vec]] = []
    seen: Set[FrozenSet[Vec]] = set()
    target = (n, n, n + d)
    for i, k in enumerate(pts):
        for p in pts[i + 1 :]:
            r = (-k[0] - p[0], -k[1] - p[1], -k[2] - p[2])
            if r not in packet:
                continue
            key = frozenset((k, p, r))
            if len(key) < 3 or key in seen:
                continue
            shells = tuple(sorted(nrm2(v) for v in key))
            if shells != target:
                continue
            seen.add(key)
            found.append(key)
    return found


def two_shell_Ds(n: int, d: int, mass_n: float = 1.0, mass_np: float = 1.0) -> Dict[str, float]:
    """Equal-mass (default) two-point remainder D_s = (XZ - Y^2)/X.

    X = λ a + μ b, Y = λ² a + μ² b, Z = λ³ a + μ³ b with λ=n, μ=n+d.
    Then XZ - Y² = a b λ μ d², so D_s = a b λ μ d² / X.
    For a=b and d fixed this is Θ(n).
    """
    lam = float(n)
    mu = float(n + d)
    a, b = float(mass_n), float(mass_np)
    x = lam * a + mu * b
    y = lam * lam * a + mu * mu * b
    z = lam**3 * a + mu**3 * b
    xz_y2 = a * b * lam * mu * (d**2)
    ds = xz_y2 / x if x else 0.0
    return {
        "lambda": lam,
        "mu": mu,
        "gap_d": float(d),
        "X": x,
        "Y": y,
        "Z": z,
        "Lambda": y / x if x else 0.0,
        "D_s": ds,
        "D_s_over_n": ds / lam if lam else 0.0,
        "identity_XZ_minus_Y2": xz_y2,
    }


def probe_pair(n: int, d: int) -> Dict[str, object]:
    a = lattice_sphere(n)
    b = lattice_sphere(n + d)
    m = len(a) + len(b)
    closures = mixed_gap_closures(a, b, n, d)
    c = len(closures)
    spectral = two_shell_Ds(n, d) if a and b else None
    return {
        "n": n,
        "d": d,
        "r3_n": len(a),
        "r3_n_plus_d": len(b),
        "m_keys": m,
        "mixed_closures_n_n_np": c,
        "closures_over_m": (c / m) if m else 0.0,
        "closures_over_m2": (c / (m * m)) if m else 0.0,
        "sqrt_m": math.sqrt(m) if m else 0.0,
        "spectral_two_mass": spectral,
        "ensemble": "full_lattice_spheres",
        "not_an_AP": True,
    }


DEFAULT_PAIRS: Sequence[Tuple[int, int]] = (
    (9, 1),
    (13, 1),
    (17, 1),
    (25, 1),
    (41, 1),
    (49, 1),
    (89, 1),
    (9, 2),
    (17, 2),
    (25, 2),
    (41, 2),
    (49, 2),
    (89, 2),
    (9, 3),
    (17, 3),
    (25, 3),
    (41, 3),
    (49, 3),
    (89, 3),
)


def run_table(pairs: Sequence[Tuple[int, int]] = DEFAULT_PAIRS) -> Dict[str, object]:
    rows = [probe_pair(n, d) for n, d in pairs]
    d1 = [r for r in rows if r["d"] == 1]
    closures = [int(r["mixed_closures_n_n_np"]) for r in d1]
    ms = [int(r["m_keys"]) for r in d1]
    return {
        "construction": (
            "Full Z^3 spheres |k|^2=n and |k|^2=n+d; m=#keys grows with n; "
            "D_s from the two-shell gap, not an AP width; closures are "
            "k+p+r=0 of type (n,n,n+d)."
        ),
        "sot": "docs/ns-recovery/SOT.md",
        "locked": "2026-09-10",
        "status": {
            "heuristic_O_m2_aligned_closures": "false_on_natural_same_shell_ensemble",
            "uniform_triadic_bound": "open",
            "navier_stokes": "not_solved",
            "packet_kill_still_requires": (
                "a designed two-shell subset with Theta(m^2) closures and locked phases, "
                "with R_star tracking m"
            ),
        },
        "rows": rows,
        "d1_closure_range": {"min": min(closures), "max": max(closures)} if closures else {},
        "d1_closures_scale_like_m_not_m2": all(
            (c / (m * m) < 0.05) for c, m in zip(closures, ms) if m >= 50
        ),
        "user_reported_R_star_not_computed_here": {
            "n=9_d=1": 0.11,
            "n=89_d=1_144_plus_120_keys_288_closures": 0.031,
            "note": "Recorded from the 10 Sep 2026 note. Formula not in this repo.",
        },
    }


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json-out",
        type=Path,
        default=ROOT / "results" / "same_shell_packet.json",
    )
    args = parser.parse_args(argv)
    table = run_table()
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(table, indent=2) + "\n")
    print(f"wrote {args.json_out}")
    for row in table["rows"]:
        if row["d"] != 1 and row["mixed_closures_n_n_np"] == 0:
            extra = "  (no mixed landings)"
        else:
            extra = ""
        print(
            f"n={row['n']:3d} d={row['d']}  keys={row['r3_n']}+{row['r3_n_plus_d']}  "
            f"m={row['m_keys']:3d}  closures={row['mixed_closures_n_n_np']:3d}  "
            f"c/m={row['closures_over_m']:.3f}  c/m^2={row['closures_over_m2']:.5f}"
            f"{extra}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
