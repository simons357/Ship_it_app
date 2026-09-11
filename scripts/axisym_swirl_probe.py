#!/usr/bin/env python3
"""
Measure T_{j<-j}/Z_j on compact axisymmetric-with-swirl fields.

Class: unaugmented axisymmetric-with-swirl NS.
The continuum field is a compact swirl (and optional meridional)
blob on R^3, sampled on the torus with support inside a ball
of radius R < π so the periodic images do not overlap.

The scored object is the Leray projection of the Fourier
interpolant, 2/3-dealiased, so the pairing check is the same
diagnostic as axisym_shell.py. That interpolant is not the
continuum field. Rotation residual says how much SO(2) survived.

Remainder T_{j<-j} is not bounded. [ρ] is not claimed.
If pairing_rel >= 1e-15, the identity is not closed.
Do not quote the sign of Lambda'.
Occupancy is not scored here. α is printed separately.
NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from axisym_shell import (  # noqa: E402
    PAIRING_TOL,
    energy,
    from_physical,
    physical,
    score_field,
)
from estimate_audit import classify_paragraph  # noqa: E402
from track_b_lemmas import rec  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "AXISYM-SWIRL-PROBE.md"
ESTIMATE = ROOT / "docs" / "AXISYM-SHELL.md"


def cinf_ball(q2: np.ndarray, r2: float) -> np.ndarray:
    out = np.zeros_like(q2)
    mask = q2 < r2
    out[mask] = np.exp(-1.0 / (r2 - q2[mask]))
    return out


def coords(n: int):
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    Xc = X - math.pi
    Yc = Y - math.pi
    Zc = Z - math.pi
    r2 = Xc * Xc + Yc * Yc
    q2 = r2 + Zc * Zc
    return Xc, Yc, Zc, r2, q2


def bump_and_derivs(q2: np.ndarray, r_ball: float):
    r2 = r_ball * r_ball
    s = r2 - q2
    b = cinf_ball(q2, r2)
    # dB/dq2 = -B / s^2 on the support
    db = np.zeros_like(q2)
    mask = q2 < r2
    db[mask] = -b[mask] / (s[mask] ** 2)
    return b, db


def compact_swirl(n: int, r_ball: float = 2.4, kz: float = 1.0) -> np.ndarray:
    """u = B(q) (1 + sin(kz Z)) (-Y, X, 0). Smooth on the axis. div-free."""
    Xc, Yc, Zc, _r2, q2 = coords(n)
    b, _db = bump_and_derivs(q2, r_ball)
    amp = b * (1.0 + np.sin(kz * Zc))
    u = np.stack([-Yc * amp, Xc * amp, np.zeros_like(amp)], axis=0)
    return u


def compact_swirl_meridional(
    n: int,
    r_ball: float = 2.4,
    kz: float = 1.0,
    meridional: float = 1.0,
) -> np.ndarray:
    """Swirl plus a Stokes-stream meridional field from χ = r² B."""
    Xc, Yc, Zc, r2, q2 = coords(n)
    b, db = bump_and_derivs(q2, r_ball)
    wave = 1.0 + np.sin(kz * Zc)
    amp = b * wave
    u = np.stack([-Yc * amp, Xc * amp, np.zeros_like(amp)], axis=0)
    # χ = r² B; u^r = (1/r) ∂_z χ, u^z = -(1/r) ∂_r χ
    m = float(meridional)
    u[0] = u[0] + m * 2.0 * Xc * Zc * db * wave
    u[1] = u[1] + m * 2.0 * Yc * Zc * db * wave
    u[2] = u[2] - m * (2.0 * b + 2.0 * r2 * db) * wave
    return u


def normalize_energy(uh: np.ndarray) -> np.ndarray:
    e = energy(uh)
    if e <= 0:
        return uh
    return uh / math.sqrt(e)


def rotate_z90_about_axis(u: np.ndarray) -> np.ndarray:
    """90° about the grid axis x=y=π. dest(i,j) reads (j, (n-i) mod n)."""
    n = u.shape[1]
    tmp = np.transpose(u, (0, 2, 1, 3))
    src = tmp[:, (n - np.arange(n)) % n, :, :]
    out = np.empty_like(src)
    out[0] = -src[1]
    out[1] = src[0]
    out[2] = src[2]
    return out


def rotation_residual(uh: np.ndarray) -> float:
    u = physical(uh)
    rot = rotate_z90_about_axis(u)
    num = float(np.mean((u - rot) ** 2))
    den = float(np.mean(u**2)) + 1e-30
    return math.sqrt(num / den)


def summarize(scored: dict, rot: float, kind: str, r_ball: float, kz: float) -> dict:
    pairing_closed = bool(scored["pairing_closed"])
    return {
        "name": scored["name"],
        "kind": kind,
        "n": scored["n"],
        "r_ball": r_ball,
        "kz": kz,
        "E": scored["E"],
        "pairing_rel": scored["pairing_rel"],
        "pairing_closed": pairing_closed,
        "identity_closed": pairing_closed,
        "lambda_prime_sign_quoted": False,
        "sum_T_rel": scored["sum_T_rel"],
        "max_split_err": scored["max_split_err"],
        "max_abs_rho_E": scored["max_abs_rho_E"],
        "max_abs_rho_Z": scored["max_abs_rho_Z"],
        "rho_E": scored["rho_E"],
        "rho_Z": scored["rho_Z"],
        "alignment": scored["alignment"],
        "rotation_residual": rot,
        "occupancy_scored": False,
    }


def build_and_score(
    n: int,
    kind: str,
    r_ball: float,
    kz: float,
    meridional: float = 1.0,
) -> dict:
    if kind == "pure_swirl":
        u = compact_swirl(n, r_ball=r_ball, kz=kz)
    elif kind == "swirl_meridional":
        u = compact_swirl_meridional(n, r_ball=r_ball, kz=kz, meridional=meridional)
    else:
        raise ValueError(kind)
    uh = normalize_energy(from_physical(u))
    scored = score_field(uh, kind)
    rot = rotation_residual(uh)
    row = summarize(scored, rot, kind, r_ball, kz)
    row["meridional"] = 0.0 if kind == "pure_swirl" else float(meridional)
    return row


def lemmas(rows: list[dict], page_ok: bool) -> list[dict]:
    pairing_ok = all(r["pairing_closed"] for r in rows)
    split_ok = all(r["max_split_err"] < 1e-12 for r in rows)
    rot_ok = all(r["rotation_residual"] < 1e-12 for r in rows)
    return [
        rec(
            "ASW_class_field",
            "scored fields are compact axisymmetric-with-swirl samples",
            "pass" if rot_ok else "fail",
            "Continuum swirl on a ball R<π. Scored object is the dealiased interpolant.",
        ),
        rec(
            "ASW_pairing",
            "energy pairing residual < 10^{-15} relative",
            "pass" if pairing_ok else "fail",
            "If this fails, the identity is not closed. Sign of Lambda' is not quoted either way.",
        ),
        rec(
            "ASW_split",
            "Door 1 split residual is at roundoff",
            "pass" if split_ok else "fail",
            "T_j = T_IR + T_loc + T_UV on the interpolant.",
        ),
        rec(
            "ASW_rho_printed",
            "ρ_j = T_{j<-j}/Z_j is printed on the swirl samples",
            "pass",
            "A printed ratio. Not [ρ] for the class. A number may come out large.",
        ),
        rec(
            "ASW_alpha_separate",
            "alignment α is printed and is not occupancy",
            "pass",
            "Door 3 criterion. Occupancy not scored. Not a bound.",
        ),
        rec(
            "ASW_remainder",
            "T_{j<-j} is bounded for axisymmetric-with-swirl NS",
            "fail",
            "Named remainder. These samples do not close it.",
        ),
        rec(
            "ASW_rho_class",
            "[ρ] holds for the class",
            "fail",
            "Not measured for every field in the class.",
        ),
        rec(
            "ASW_page_clean",
            "probe page has no discard-list object",
            "pass" if page_ok else "fail",
            "Filter: estimate_audit.classify_paragraph.",
        ),
        rec(
            "ASW_ns_solved",
            "swirl probe solves NS",
            "fail",
            "Class and ρ_j stay in the sentence.",
        ),
    ]


def run(
    n: int = 32,
    r_ball: float = 2.4,
    kz: float = 1.0,
    out: Path | None = None,
) -> dict:
    fields = [
        build_and_score(n, "pure_swirl", r_ball, kz),
        build_and_score(n, "swirl_meridional", r_ball, kz, meridional=1.0),
        build_and_score(n, "swirl_meridional", r_ball, kz, meridional=3.0),
    ]
    fields[1]["name"] = "swirl_meridional_m1"
    fields[2]["name"] = "swirl_meridional_m3"
    page_text = PAGE.read_text() if PAGE.exists() else ""
    page_cls = classify_paragraph(page_text) if page_text else {
        "discard_hits": [],
        "allowed_in_estimate": True,
    }
    page_ok = page_cls["allowed_in_estimate"]
    if page_text:
        page_ok = page_ok and "not a close" in page_text.lower()
    rows = lemmas(fields, page_ok)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for item in rows:
        counts[item["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "axisymmetric swirl probe of T_{j<-j}",
            "class": "axisymmetric with swirl",
            "manifold": "compact blob on R^3, sampled on T^3 with R<π",
            "remainder": "T_{j<-j}",
            "tuning_the_pde": False,
            "lemma_star_open": True,
            "h1_started": False,
            "estimate_open": True,
            "kill": False,
            "lambda_prime_sign_quoted": False,
            "occupancy_scored": False,
            "n": n,
            "r_ball": r_ball,
            "kz": kz,
            "pairing_tol": PAIRING_TOL,
        },
        "fields": fields,
        "page_filter": page_cls,
        "lemmas": rows,
        "counts": counts,
        "domain_verdict": "open",
        "claim": (
            "Axisymmetric-with-swirl unaugmented NS; Z_j shell budget; "
            "remainder T_{j<-j}; compact-swirl interpolants measured; "
            "[ρ] not assumed as a class fact."
        ),
    }
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=32)
    p.add_argument("--r-ball", type=float, default=2.4)
    p.add_argument("--kz", type=float, default=1.0)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    print(json.dumps(run(n=args.n, r_ball=args.r_ball, kz=args.kz, out=args.out), indent=2))


if __name__ == "__main__":
    main()
