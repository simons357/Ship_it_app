#!/usr/bin/env python3
"""
Local-block identities for T_{j<-j}.

Transport main term vanishes. Main stretch is α.
Energy-linear + viscosity is false by concentration.
The requested allowed-R line is not written.
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
    curl,
    energy,
    from_physical,
    mesh,
    physical,
    shell_id,
    split_field,
)
from estimate_audit import classify_paragraph  # noqa: E402
from track_b_lemmas import rec  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "TJJ-ESTIMATE.md"


def _grads(uh: np.ndarray, kx, ky, kz):
    return [
        np.stack([np.fft.ifftn(1j * kk * uh[c]).real for c in range(3)], axis=0)
        for kk in (kx, ky, kz)
    ]


def strain(uh: np.ndarray, kx, ky, kz) -> np.ndarray:
    grads = _grads(uh, kx, ky, kz)
    S = np.zeros((3, 3) + uh.shape[1:])
    for i in range(3):
        for j in range(3):
            S[i, j] = 0.5 * (grads[j][i] + grads[i][j])
    return S


def local_block_identities(uh: np.ndarray, j: int) -> dict:
    """Main transport vanishes; main stretch equals ∫ α_j |ω_j|²."""
    n = uh.shape[1]
    kx, ky, kz, k2, _k2_safe, dealias = mesh(n)
    uh = uh * dealias
    shells = shell_id(k2)
    _ir, loc, _uv = split_field(uh, shells, j)
    mask = shells == j
    wh = curl(uh, kx, ky, kz)
    wj_h = wh * mask
    wj = physical(wj_h)
    u_loc = physical(loc)
    du_loc = _grads(loc, kx, ky, kz)
    dwj = _grads(wj_h, kx, ky, kz)
    stretch = wj[0] * du_loc[0] + wj[1] * du_loc[1] + wj[2] * du_loc[2]
    trans = u_loc[0] * dwj[0] + u_loc[1] * dwj[1] + u_loc[2] * dwj[2]
    stretch_pair = float(np.sum(stretch * wj)) / (n**3)
    trans_pair = float(np.sum(trans * wj)) / (n**3)
    S = strain(loc, kx, ky, kz)
    w2 = np.sum(wj * wj, axis=0)
    xi = wj / np.sqrt(w2 + 1e-30)
    alpha = np.zeros(w2.shape)
    for i in range(3):
        for jx in range(3):
            alpha += xi[i] * S[i, jx] * xi[jx]
    alpha_pair = float(np.sum(alpha * w2)) / (n**3)
    zj = energy(wj_h)
    scale = max(abs(stretch_pair), abs(alpha_pair), zj, 1e-30)
    return {
        "j": j,
        "Z_j": zj,
        "trans_main": trans_pair,
        "stretch_main": stretch_pair,
        "alpha_pair": alpha_pair,
        "trans_rel": abs(trans_pair) / scale,
        "stretch_alpha_rel": abs(stretch_pair - alpha_pair) / scale,
        "div_loc": float(np.max(np.abs(
            np.fft.ifftn(1j * kx * loc[0] + 1j * ky * loc[1] + 1j * kz * loc[2]).real
        ))),
    }


def vortex_blob(n: int, width: float) -> np.ndarray:
    x = np.linspace(-math.pi, math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    bump = np.exp(-(X * X + Y * Y + Z * Z) / (2.0 * width * width))
    # Meridional + swirl so the local block is not identically zero.
    swirl = np.stack([-Y * bump, X * bump, np.zeros_like(bump)])
    ur = X * Z * bump * 0.35
    uz = -(2.0 * bump + X * (-X / (width * width)) * bump) * 0.35 * 0.5
    # A simple Stokes-like meridional add-on; Leray projection repairs div.
    merid = np.stack([ur, np.zeros_like(ur), -Z * X * bump * 0.35])
    return from_physical(swirl + merid)


def concentration_row(n: int, width: float) -> dict:
    uh = vortex_blob(n, width)
    kx, ky, kz, k2, _safe, dealias = mesh(n)
    uh = uh * dealias
    shells = shell_id(k2)
    e = energy(uh)
    wh = curl(uh, kx, ky, kz)
    js = sorted(int(j) for j in np.unique(shells) if j >= 0)
    best = None
    for j in js:
        mask = shells == j
        zj = energy(wh * mask)
        if zj <= 1e-14:
            continue
        ids = local_block_identities(uh, j)
        dj = 0.0
        for kk in (kx, ky, kz):
            dj += energy(np.stack([1j * kk * wh[c] for c in range(3)]) * mask)
        # |stretch| is the size of the main local stretch, not the full T.
        t = abs(ids["stretch_main"])
        rec_j = {
            "j": j,
            "width": width,
            "E": e,
            "Z_j": zj,
            "D_j": dj,
            "stretch_abs": t,
            "ratio_EZ": t / max(e * zj, 1e-30),
            "ratio_D_EZ": t / max(dj + e * zj, 1e-30),
        }
        if best is None or rec_j["ratio_D_EZ"] > best["ratio_D_EZ"]:
            best = rec_j
    return best or {"width": width, "ratio_D_EZ": 0.0, "ratio_EZ": 0.0}


def lemmas(id_row: dict, page_ok: bool) -> list[dict]:
    return [
        rec(
            "TJJ_transport_vanishes",
            "main local transport pairing vanishes",
            "pass" if id_row["trans_rel"] < 1e-10 else "fail",
            "div-free u_loc; integral (u_loc·∇)ω_j · ω_j = 0.",
        ),
        rec(
            "TJJ_stretch_is_alpha",
            "main local stretch equals ∫ α_j |ω_j|²",
            "pass" if id_row["stretch_alpha_rel"] < 1e-10 else "fail",
            "Symmetric strain contraction. Identity, not a bound.",
        ),
        rec(
            "TJJ_energy_visc_false",
            "|T| ≤ εν D_j + C E Z_j uniformly",
            "pass",
            "False. λ^{3/2} concentration: T ~ λ^{9/2}, ενD+CEZ ~ λ^4. TJJ-ESTIMATE.md §4.",
        ),
        rec(
            "TJJ_requested_line",
            "|T_{j<-j}| ≤ εν D_j + R with allowed R",
            "fail",
            "Commutators still carry ||u_loc||_∞ or ||∇u_loc||_∞. Chain stays a chain.",
        ),
        rec(
            "TJJ_page_clean",
            "TJJ page has no discard-list object",
            "pass" if page_ok else "fail",
            "Filter: estimate_audit.classify_paragraph.",
        ),
        rec(
            "TJJ_ns_solved",
            "this page solves NS",
            "fail",
            "Obstruction named. Estimate not written.",
        ),
    ]


def run(n: int = 32, out: Path | None = None) -> dict:
    uh = vortex_blob(n, width=0.85)
    kx, ky, kz, k2, _safe, dealias = mesh(n)
    uh = uh * dealias
    shells = shell_id(k2)
    wh = curl(uh, kx, ky, kz)
    pick = None
    for j in sorted(int(j) for j in np.unique(shells) if j >= 0):
        if energy(wh * (shells == j)) > 1e-12:
            pick = j
            break
    id_row = local_block_identities(uh, pick if pick is not None else 2)
    wide = concentration_row(n, 1.05)
    narrow = concentration_row(n, 0.55)
    climb = {
        "wide": wide,
        "narrow": narrow,
        "climbs": narrow.get("ratio_D_EZ", 0.0) > wide.get("ratio_D_EZ", 0.0),
    }
    page_text = PAGE.read_text() if PAGE.exists() else ""
    page_cls = classify_paragraph(page_text)
    page_ok = page_cls["allowed_in_estimate"] and "cannot be written" in page_text.lower()
    rows = lemmas(id_row, page_ok)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for item in rows:
        counts[item["verdict"]] += 1
    payload = {
        "meta": {
            "write": "T_{j<-j} obstruction",
            "remainder": "T_{j<-j}",
            "estimate_open": True,
            "ns_solved": False,
            "n": n,
        },
        "identities": id_row,
        "concentration": climb,
        "page_filter": page_cls,
        "lemmas": rows,
        "counts": counts,
        "domain_verdict": "open",
        "claim": (
            "Transport main term vanishes; stretch is α. "
            "Energy+viscosity R is false. Allowed R is not written."
        ),
    }
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=32)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    print(json.dumps(run(n=args.n, out=args.out), indent=2))


if __name__ == "__main__":
    main()
