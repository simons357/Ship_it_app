#!/usr/bin/env python3
"""Exact-core printout of localized ABC on λ=2,4,8,16.

Boxed write-up (LEMMA_STAR_CANONICAL / standalone evaluator):

    R★ = (T_c)_+² / (D_s E Y)

T_c(-v) = -T_c(v). If T_c<0, boxed R★=0 and the table column is
boxed R★(-v) = T_c²/(D_s E Y). Same object. Not an ABC-only variant.

Standalone evaluator: scripts/ns_lemma_star_core.py
This is an evaluator, not a proof. NS not solved. Not a plate.
H1 is a different integral and is not run here.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ns_lemma_star_core as star  # noqa: E402
from ns_attacks.cs_remainder_bump import (  # noqa: E402
    _wave_numbers,
    localized_abc,
    probe_hat,
)
from ns_attacks.stokes_moments import probe  # noqa: E402

OUT = ROOT / "results" / "cs_remainder_bump"

# Same grids as the FFT local_abc table: n = max(48, 16λ).
LAMBDAS = (2, 4, 8, 16)
CORE_RSTAR_MODE_CAP = 2500


def grid_for(lam: int) -> int:
    n = max(48, 16 * int(lam))
    return n + (n % 2)


def hat_to_field(vx, vy, vz, energy_keep: float = 0.9999) -> star.Field:
    """Export FFT hats into the standalone Field, keeping energy_keep of E."""
    n = vx.shape[0]
    k1d = _wave_numbers(n)
    amp2 = (np.abs(vx) ** 2 + np.abs(vy) ** 2 + np.abs(vz) ** 2).real
    E = float(amp2.sum())
    order = np.argsort(amp2.ravel())[::-1]
    f = star.Field()
    seen = set()
    kept = 0.0
    for idx in order:
        e = float(amp2.ravel()[idx])
        if e <= 0.0:
            break
        i, j, l = np.unravel_index(int(idx), amp2.shape)
        k = (int(k1d[i]), int(k1d[j]), int(k1d[l]))
        if k == (0, 0, 0) or k in seen:
            kept += e
            if kept >= energy_keep * E:
                break
            continue
        w = np.array([vx[i, j, l], vy[i, j, l], vz[i, j, l]], dtype=complex)
        f.set_mode(k, w)
        seen.add(k)
        seen.add((-k[0], -k[1], -k[2]))
        kept += e
        if kept >= energy_keep * E:
            break
    return f.normalize(1.0)


def boxed_from_tc(Tc: float, Ds: float, E: float, Y: float) -> dict:
    """Write-up R★ and the sign-flipped column used when T_c<0."""
    if Ds <= 1e-14 or E <= 0.0 or Y <= 0.0:
        return {"R_star_box": 0.0, "R_star_flip": 0.0}
    tc_plus = max(Tc, 0.0)
    return {
        "R_star_box": (tc_plus ** 2) / (Ds * E * Y),
        "R_star_flip": (Tc ** 2) / (Ds * E * Y),
    }


def embed_probe(field: star.Field) -> dict:
    """FFT B on a grid with n > 2 kmax: exact triad for this finite support."""
    kmax = max(max(abs(x) for x in k) for k in field.modes)
    n = 2 * (2 * kmax + 4)
    if n % 2:
        n += 1
    n = min(n, 256)
    hx = np.zeros((n, n, n), dtype=np.complex128)
    hy = np.zeros_like(hx)
    hz = np.zeros_like(hx)
    for k, v in field.modes.items():
        if max(abs(x) for x in k) >= n // 2:
            continue
        idx = (k[0] % n, k[1] % n, k[2] % n)
        hx[idx] += v[0]
        hy[idx] += v[1]
        hz[idx] += v[2]
    return probe_hat(hx, hy, hz)


def check_one(lam: int) -> dict:
    n = grid_for(lam)
    vx, vy, vz = localized_abc(n, width=float(lam), k0=lam)
    fft = probe_hat(vx, vy, vz)
    fft_box = boxed_from_tc(fft["T_c"], fft["Ds"], fft["E"], fft["Y"])

    keep = 0.9999 if lam <= 4 else 0.999
    core_f = hat_to_field(vx, vy, vz, energy_keep=keep)
    mom = star.moments(core_f)
    E, X, Y, Z, Lambda = mom
    Ds = star.D_s_direct_form(core_f, Lambda)

    core_R = None
    core_Tc = None
    used = "embed_fft"
    if len(core_f.modes) <= CORE_RSTAR_MODE_CAP:
        rec = star.R_star(core_f, verify=True)
        core_R = rec["R_star"]
        core_Tc = rec["T_c"]
        used = "standalone_R_star"
        Ds = rec["D_s"]
        E, Y = rec["E"], rec["Y"]
    emb = embed_probe(core_f)
    if core_Tc is None:
        core_Tc = emb["T_c"]
        Ds = float(Ds)
    core_box = boxed_from_tc(core_Tc, Ds, E, Y)

    return {
        "lambda": lam,
        "n_grid": n,
        "n_modes": len(core_f.modes),
        "energy_keep": keep,
        "evaluator": used,
        "normalization": "R_star = (T_c)_+^2 / (D_s E Y)  [write-up / standalone]",
        "fft_Tc": fft["T_c"],
        "fft_Ds": fft["Ds"],
        "fft_E": fft["E"],
        "fft_Y": fft["Y"],
        "fft_R_star_box": fft_box["R_star_box"],
        "fft_R_star_flip": fft_box["R_star_flip"],
        "core_Tc": core_Tc,
        "core_Ds": Ds,
        "core_E": E,
        "core_Y": Y,
        "core_R_star_box": core_R if core_R is not None else core_box["R_star_box"],
        "core_R_star_flip": core_box["R_star_flip"],
        "embed_Tc": emb["T_c"],
        "embed_R_star_flip": boxed_from_tc(emb["T_c"], emb["Ds"], emb["E"], emb["Y"])[
            "R_star_flip"
        ],
        "fft_cs": fft["cs_ratio"],
        "same_norm_as_writeup": True,
        "H1_tested": False,
    }


def _probe_formula_lock() -> dict:
    """Standalone R★ matches stokes_moments.probe on a three-mode field."""
    from ns_attacks.stokes_moments import enforce_reality, make_divfree_amp

    field = {}
    field[(1, 0, 0)] = make_divfree_amp((1, 0, 0), (0.0, 1.0, 0.3))
    field[(0, 1, 0)] = 0.4 * make_divfree_amp((0, 1, 0), (1.0, 0.0, 0.2))
    field[(1, 1, 0)] = 0.25 * make_divfree_amp((1, 1, 0), (0.2, 0.5, 1.0))
    field = enforce_reality(field)
    f = star.from_mode_dict(field)
    pr = probe(field)
    rec = star.R_star(f, verify=True)
    R_probe = (max(pr.Tc, 0.0) ** 2) / (pr.Ds * pr.E * pr.Y) if pr.Ds > 0 else 0.0
    R_flip_probe = (pr.Tc ** 2) / (pr.Ds * pr.E * pr.Y) if pr.Ds > 0 else 0.0
    return {
        "probe_Tc": pr.Tc,
        "core_Tc": rec["T_c"],
        "probe_Ds": pr.Ds,
        "core_Ds": rec["D_s"],
        "probe_R_box": R_probe,
        "core_R_box": rec["R_star"],
        "probe_R_flip": R_flip_probe,
        "Tc_err": abs(pr.Tc - rec["T_c"]),
        "Ds_err": abs(pr.Ds - rec["D_s"]),
        "R_box_err": abs(R_probe - rec["R_star"]),
    }


def dilation_invariance(lam: int = 2) -> dict:
    n = grid_for(lam)
    vx, vy, vz = localized_abc(n, width=float(lam), k0=lam)
    f = hat_to_field(vx, vy, vz, energy_keep=0.999)
    if len(f.modes) <= CORE_RSTAR_MODE_CAP:
        r1 = star.R_star(f, verify=True)["R_star"]
        r2 = star.R_star(star.dilate(f, 2), verify=True)["R_star"]
    else:
        a = boxed_from_tc(*[embed_probe(f)[k] for k in ("T_c", "Ds", "E", "Y")])
        b = boxed_from_tc(
            *[embed_probe(star.dilate(f, 2))[k] for k in ("T_c", "Ds", "E", "Y")]
        )
        r1, r2 = a["R_star_flip"], b["R_star_flip"]
    return {
        "R_base": r1,
        "R_dilated": r2,
        "rel": abs(r1 - r2) / max(abs(r1), 1e-30),
        "n_modes": len(f.modes),
    }


def same_field_fft_vs_exact(lam: int = 2) -> dict:
    n = grid_for(lam)
    vx, vy, vz = localized_abc(n, width=float(lam), k0=lam)
    f = hat_to_field(vx, vy, vz, energy_keep=0.999)
    emb = embed_probe(f)
    if len(f.modes) <= CORE_RSTAR_MODE_CAP:
        rec = star.R_star(f, verify=True)
        exact_Tc, exact_R = rec["T_c"], rec["R_star"]
        exact_flip = boxed_from_tc(rec["T_c"], rec["D_s"], rec["E"], rec["Y"])[
            "R_star_flip"
        ]
    else:
        exact_Tc, exact_R = emb["T_c"], emb["R_star"]
        exact_flip = boxed_from_tc(emb["T_c"], emb["Ds"], emb["E"], emb["Y"])[
            "R_star_flip"
        ]
    return {
        "n_modes": len(f.modes),
        "exact_Tc": exact_Tc,
        "fft_Tc": emb["T_c"],
        "exact_R_box": exact_R,
        "fft_R_box": emb["R_star"],
        "exact_R_flip": exact_flip,
        "fft_R_flip": boxed_from_tc(emb["T_c"], emb["Ds"], emb["E"], emb["Y"])[
            "R_star_flip"
        ],
        "Tc_rel": abs(exact_Tc - emb["T_c"]) / max(abs(exact_Tc), 1e-30),
        "R_rel": abs(exact_flip - boxed_from_tc(emb["T_c"], emb["Ds"], emb["E"], emb["Y"])["R_star_flip"])
        / max(abs(exact_flip), 1e-30),
    }


def main():
    lock = _probe_formula_lock()
    print("formula_lock", json.dumps(lock), flush=True)
    if lock["Tc_err"] > 1e-8 or lock["Ds_err"] > 1e-8 or lock["R_box_err"] > 1e-8:
        raise RuntimeError(f"standalone R★ disagrees with probe: {lock}")

    rows = []
    for lam in LAMBDAS:
        print(f"checking λ={lam} n={grid_for(lam)}", flush=True)
        rec = check_one(lam)
        rows.append(rec)
        print(json.dumps(rec, indent=2), flush=True)

    inv = dilation_invariance()
    print("dilation", json.dumps(inv), flush=True)
    same = same_field_fft_vs_exact()
    print("same_field", json.dumps(same), flush=True)

    flips = [r["core_R_star_flip"] for r in rows]
    fft_flips = [r["fft_R_star_flip"] for r in rows]
    climb = bool(len(flips) >= 3 and flips[-1] > 4.0 * max(flips[0], 1e-12))
    fft_climb = bool(len(fft_flips) >= 3 and fft_flips[-1] > 4.0 * max(fft_flips[0], 1e-12))
    exponents = []
    for i in range(1, len(rows)):
        a, b = rows[i - 1], rows[i]
        ratio = b["lambda"] / a["lambda"]
        if a["core_R_star_flip"] > 0:
            exponents.append(
                math.log(b["core_R_star_flip"] / a["core_R_star_flip"]) / math.log(ratio)
            )
    same_ok = same["R_rel"] < 1e-6 and same["Tc_rel"] < 1e-6
    dil_ok = inv["rel"] < 1e-12
    payload = {
        "ns_solved": False,
        "lemma_star": "OPEN",
        "H1_tested_on_ABC_lambda": False,
        "normalization": "R_star = (T_c)_+^2 / (D_s E Y) from scripts/ns_lemma_star_core.py",
        "formula_lock": lock,
        "rows": rows,
        "dilation": inv,
        "same_field": same,
        "same_field_matches": bool(same_ok),
        "dilation_invariant": bool(dil_ok),
        "core_R_climbs": bool(climb),
        "fft_R_climbs": bool(fft_climb),
        "core_R_flip": flips,
        "fft_R_flip": fft_flips,
        "log_log_exponents": exponents,
        "verdict": (
            "Exact objects still climb on λ=2,4,8,16 under the write-up R★. "
            "Falsifier-of-record for this field + Target A / CS / ★-as-closer. "
            "Stop patching Lemma★. Evaluator ≠ proof. NS not solved. H1 untested."
            if same_ok and climb
            else (
                "FFT climb on this family; exact-core climb not locked. "
                "Do not restamp. NS not solved. H1 untested."
                if fft_climb and not climb
                else "Exact-core printout did not confirm a λ³ climb. NS not solved."
            )
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "exact_core_check.json").write_text(json.dumps(payload, indent=2))
    print("verdict", payload["verdict"])


if __name__ == "__main__":
    main()
