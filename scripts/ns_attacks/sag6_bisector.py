#!/usr/bin/env python3
"""SAG-6C/D — bisector-plane stack of equal-input circles.

Not a T_c bound. NS is not solved.

p = k/2 + r, q = k/2 − r, r · k = 0, |p| = |q|.
Circles C_{α,k} partition the bisector lattice (r ↔ −r once).
W_{α,k} is the signed vector of the whole circle, not occupancy.

ρ_k(N) = ||∑ G W|| / ∑ |G| ||W||.
G^{T_c} = β(β−Λ) is independent of α and factors out.
Do not impose random phase. Solve the extremal problem.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.sag6_lattice_circle import (
    Mode,
    mode_norm2,
    perp_basis,
    radial_inplane,
    sigma_from_u,
    vec,
)

Record = dict


def half_integer_ok(k: Mode) -> bool:
    return all(c % 2 == 0 for c in k)


def enumerate_bisector(k: Mode, r_max: int) -> List[Record]:
    """Every unordered {r, −r} in the integer bisector plane, |r| ≤ r_max.

    Keeps α, r, −r, p, q, transverse direction, triangle-plane normal,
    and the circle id |r|^2. Occupancy is not the object.
    """
    if not half_integer_ok(k):
        raise ValueError("k must be even so k/2 is an integer lattice point")
    kh = vec(k)
    kn = float(np.linalg.norm(kh))
    half = (k[0] // 2, k[1] // 2, k[2] // 2)
    beta = mode_norm2(k)
    seen = set()
    rows: List[Record] = []
    lim = int(r_max)
    for x in range(-lim, lim + 1):
        for y in range(-lim, lim + 1):
            for z in range(-lim, lim + 1):
                r = (x, y, z)
                if r == (0, 0, 0):
                    continue
                if x * k[0] + y * k[1] + z * k[2] != 0:
                    continue
                rn2 = x * x + y * y + z * z
                if rn2 > r_max * r_max:
                    continue
                key = min(r, (-x, -y, -z))
                if key in seen:
                    continue
                seen.add(key)
                p = (half[0] + x, half[1] + y, half[2] + z)
                q = (half[0] - x, half[1] - y, half[2] - z)
                alpha = mode_norm2(p)
                rr = vec(r)
                rhat = rr / np.linalg.norm(rr)
                # transverse: P_{p^⊥} k / |k_⊥|, equals direction of k_⊥(p)
                kperp = kh - ((kh @ vec(p)) / float(mode_norm2(p))) * vec(p)
                knrm = np.linalg.norm(kperp)
                kperp_hat = kperp / knrm if knrm > 1e-15 else rhat
                normal = np.cross(vec(p), vec(q))
                nn = np.linalg.norm(normal)
                rows.append(
                    {
                        "alpha": alpha,
                        "r2": rn2,
                        "r": r,
                        "minus_r": (-x, -y, -z),
                        "p": p,
                        "q": q,
                        "beta": beta,
                        "rhat": (float(rhat[0]), float(rhat[1]), float(rhat[2])),
                        "kperp_hat": (
                            float(kperp_hat[0]),
                            float(kperp_hat[1]),
                            float(kperp_hat[2]),
                        ),
                        "triangle_normal": (
                            float(normal[0] / nn) if nn > 1e-15 else (0.0, 0.0, 0.0)
                        ),
                        "circle_id": rn2,
                    }
                )
    rows.sort(key=lambda row: (row["circle_id"], row["r"]))
    return rows


def incidences(rows: List[Record]) -> dict:
    """Mode-sharing across circles. Occupancy is recorded, not used as a bound."""
    mode_to_circles: Dict[Mode, List[int]] = defaultdict(list)
    for row in rows:
        for m in (row["p"], row["q"]):
            cid = int(row["circle_id"])
            if cid not in mode_to_circles[m]:
                mode_to_circles[m].append(cid)
    shared = {str(m): cids for m, cids in mode_to_circles.items() if len(cids) > 1}
    circles = defaultdict(list)
    for row in rows:
        circles[int(row["circle_id"])].append(row)
    return {
        "n_triangles": len(rows),
        "n_circles": len(circles),
        "n_input_modes": len(mode_to_circles),
        "n_cross_circle_input_modes": len(shared),
        "shared_input_modes": shared,
        "circle_sizes": {str(cid): len(items) for cid, items in sorted(circles.items())},
    }


def circle_points(k: Mode, rows: List[Record], circle_id: int) -> List[Mode]:
    pts = []
    for row in rows:
        if int(row["circle_id"]) != circle_id:
            continue
        pts.append(row["p"])
        pts.append(row["q"])
    return sorted(set(pts))


def hemisphere_with_axis(k: Mode, pts: List[Mode], e1: np.ndarray) -> Dict[Mode, np.ndarray]:
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(vec(k) / np.linalg.norm(vec(k)), e1)
    e2 = e2 / np.linalg.norm(e2)
    out = {}
    for p in pts:
        r = radial_inplane(k, p)
        out[p] = e1.copy() if float(r @ e1) >= 0.0 else e2.copy()
    return out


def circle_W(
    k: Mode, pts: List[Mode], e1: np.ndarray, flip: bool = False
) -> np.ndarray:
    if flip:
        e1 = -e1
    field = hemisphere_with_axis(k, pts, e1)
    return sigma_from_u(k, field)


def align_signs(vectors: List[np.ndarray], axis: np.ndarray) -> List[np.ndarray]:
    """Independent circle sign flips: put every W into the half-plane of axis."""
    out = []
    for w in vectors:
        if np.real(np.vdot(axis, w)) < 0.0:
            out.append(-w)
        else:
            out.append(w)
    return out


def rho_from_vectors(vectors: List[np.ndarray]) -> dict:
    if not vectors:
        return {"rho": float("nan"), "num": 0.0, "den": 0.0, "n_circles": 0}
    stacked = np.sum(vectors, axis=0)
    num = float(np.linalg.norm(stacked))
    den = float(sum(np.linalg.norm(w) for w in vectors))
    return {
        "rho": num / den if den > 0 else float("nan"),
        "num": num,
        "den": den,
        "n_circles": len(vectors),
    }


def stack_rho(k: Mode, r_max: int) -> dict:
    rows = enumerate_bisector(k, r_max)
    inc = incidences(rows)
    e1, e2 = perp_basis(k)
    # One global axis for the hemisphere construction on every circle.
    ids = sorted({int(row["circle_id"]) for row in rows})
    raw = []
    for cid in ids:
        pts = circle_points(k, rows, cid)
        if len(pts) < 2:
            continue
        raw.append(circle_W(k, pts, e1, flip=False))
    # 6D adversary: flip each circle independently (legal iff inputs disjoint).
    aligned = align_signs(raw, e2)
    # Contrast: no sign flips, same hemisphere on every circle.
    unaligned = rho_from_vectors(raw)
    adv = rho_from_vectors(aligned)
    # Independent-circle envelope is the denominator. Occupancy unused.
    return {
        "k": k,
        "r_max": r_max,
        "alpha_max": max((row["alpha"] for row in rows), default=0),
        "incidences": inc,
        "rho_common_axis": unaligned,
        "rho_adversary": adv,
        "mode_disjoint": inc["n_cross_circle_input_modes"] == 0,
        "G_Tc_factors_out": True,
    }


def scan(k: Mode, radii: List[int]) -> dict:
    rows = []
    for r_max in radii:
        rows.append(stack_rho(k, r_max))
    rhos = [row["rho_adversary"]["rho"] for row in rows]
    # 6D: does ρ stay away from 0 as the stack grows?
    stays = all(math.isfinite(x) and x >= 0.5 for x in rhos)
    return {
        "k": k,
        "radii": radii,
        "rows": rows,
        "rho_adversary_list": rhos,
        "verdict_6D": "COHERENT FAMILY — ρ_k(N) ↛ 0" if stays else "NEEDS MORE",
        "note": (
            "Equal-input circles into one k are input-mode-disjoint. "
            "Sign of each W_{α,k} is therefore free. Half-plane alignment "
            "is a legal globally compatible DF field. Random phase is not imposed."
        ),
    }


def report() -> dict:
    scans = [
        scan((0, 0, 2), [2, 4, 6, 8, 10, 12]),
        scan((0, 0, 4), [2, 4, 6, 8]),
        scan((2, 2, 0), [2, 4, 6, 8]),
    ]
    return {
        "tag": "SAG-6 bisector stack. Occupancy is not the remainder.",
        "SAG_6A": "bisector plane = ⊔_α C_{α,k} EXACT",
        "SAG_6B": "single-circle arithmetic sparse; not the half-power source",
        "SAG_6C": "inter-circle compatible alignment; inputs disjoint on one k",
        "SAG_6D": "adversary: half-plane sign alignment of W_{α,k}",
        "G_Tc": "β(β−Λ) independent of α; ρ with G=1 is the T_c ratio",
        "scans": scans,
        "locks": {
            "no_abs_envelope": True,
            "no_occupancy_bound": True,
            "no_random_phase_postulate": True,
            "not_a_close": True,
        },
    }


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()] if x.ndim else _py(x.item())
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-records", type=int, default=0, help="r_max for raw tape")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.dump_records:
        rec = enumerate_bisector((0, 0, 2), args.dump_records)
        print(json.dumps(_py({"n": len(rec), "records": rec, "incidences": incidences(rec)}), indent=2))
        return 0
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
