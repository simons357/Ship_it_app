#!/usr/bin/env python3
"""
Geometry on CONC packets: Ring Lipschitz is real; depletion is not.

Classical NS. No Q1. No ε. Strain identity on E_c.
CONC does not force small cos α_3. IF |cos α_3| is small,
stretching is smaller. That is Constantin–Fefferman as a
conditional, not as an all-data close.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from track_b_lemmas import curl, ifft, rec, three_shell_field

_CACHE: list[dict] | None = None


def packet_geometry(n: int = 32, jstar: int = 3, seed: int = 1, n_pts: int = 240) -> dict:
    rng = np.random.default_rng(seed)
    uh, vh, wh, kx, ky, kz, _ = three_shell_field(n, jstar, rng)
    ox, oy, oz, _, _, _ = curl(uh, vh, wh, kx, ky, kz)
    d = [[ifft(1j * k * h) for k in (kx, ky, kz)] for h in (uh, vh, wh)]
    s00, s11, s22 = d[0][0], d[1][1], d[2][2]
    s01 = 0.5 * (d[0][1] + d[1][0])
    s02 = 0.5 * (d[0][2] + d[2][0])
    s12 = 0.5 * (d[1][2] + d[2][1])
    mag2 = ox * ox + oy * oy + oz * oz
    mag = np.sqrt(mag2)
    rms = float(np.sqrt(np.mean(mag2)))
    ec = mag >= 0.5 * rms
    pts = np.argwhere(ec)
    pick = rng.choice(len(pts), min(n_pts, len(pts)), replace=False)
    ident_errs: list[float] = []
    cos3 = []
    ratio = []
    for p in pts[pick]:
        i, j, k = (int(p[0]), int(p[1]), int(p[2]))
        mat = np.array(
            [
                [s00[i, j, k], s01[i, j, k], s02[i, j, k]],
                [s01[i, j, k], s11[i, j, k], s12[i, j, k]],
                [s02[i, j, k], s12[i, j, k], s22[i, j, k]],
            ]
        )
        wts, vecs = np.linalg.eigh(mat)
        xi = np.array([ox[i, j, k], oy[i, j, k], oz[i, j, k]])
        nrm = np.linalg.norm(xi)
        if nrm < 1e-14:
            continue
        xi = xi / nrm
        coss = np.array([float(np.dot(xi, vecs[:, a])) for a in range(3)])
        frame = float(np.dot(wts, coss * coss))
        direct = float(xi @ mat @ xi)
        ident_errs.append(abs(frame - direct) / (abs(direct) + 1e-30))
        c3 = abs(coss[2])
        lam = max(abs(float(wts[0])), abs(float(wts[2]))) + 1e-30
        r = abs(direct) / lam
        cos3.append(c3)
        ratio.append(r)
    cos3_a = np.array(cos3)
    ratio_a = np.array(ratio)
    low = ratio_a[cos3_a < 0.25]
    high = ratio_a[cos3_a > 0.8]
    return {
        "seed": seed,
        "ident_rel": float(np.max(ident_errs)) if ident_errs else 1.0,
        "median_cos3": float(np.median(cos3_a)) if len(cos3_a) else 1.0,
        "mean_cos3": float(np.mean(cos3_a)) if len(cos3_a) else 1.0,
        "frac_cos3_lt_0.25": float(np.mean(cos3_a < 0.25)) if len(cos3_a) else 0.0,
        "n_pts": int(len(cos3_a)),
        "ratio_low": float(np.mean(low)) if len(low) else 0.0,
        "ratio_high": float(np.mean(high)) if len(high) else 0.0,
        "n_low": int(len(low)),
        "n_high": int(len(high)),
    }


def samples(trials: int = 6) -> list[dict]:
    global _CACHE
    if _CACHE is None:
        _CACHE = [packet_geometry(seed=s) for s in range(1, trials + 1)]
    return _CACHE


def lemma_strain_identity() -> dict:
    rows = samples()
    ok = all(r["ident_rel"] < 1e-8 for r in rows)
    return rec(
        "B14_strain_identity",
        "ω·Sω = |ω|² ∑ λ_i cos² α_i on E_c",
        "pass" if ok else "fail",
        "Algebra in the strain eigenframe. Geometry starts here. Not depletion.",
        ident_rels=[r["ident_rel"] for r in rows],
    )


def lemma_conc_not_depleted() -> dict:
    rows = samples()
    med = float(np.median([r["median_cos3"] for r in rows]))
    depleted = med <= 0.25
    return rec(
        "B14a_conc_not_depleted",
        "3-CONC packets have median |cos α_3| ≤ 0.25 on E_c",
        "fail" if not depleted else "open",
        "Median |cos α_3| sits near 1/2: random on the sphere, not depleted. CONC is a spectrum, not an alignment.",
        median_cos3=med,
        means=[r["mean_cos3"] for r in rows],
        frac_lt_025=[r["frac_cos3_lt_0.25"] for r in rows],
    )


def lemma_ring_not_alignment() -> dict:
    return rec(
        "B14b_ring_not_alignment",
        "Ring Lipschitz of ξ on E_c forces cos α_3 → 0",
        "fail",
        "B3 bounds |∇ξ|. Direction slowly varying is not direction aligned. Biot–Savart slogan stays forbidden.",
    )


def lemma_cf_conditional() -> dict:
    rows = samples()
    usable = [r for r in rows if r["n_low"] >= 20 and r["n_high"] >= 20]
    ok = bool(usable) and all(r["ratio_low"] < r["ratio_high"] for r in usable)
    return rec(
        "B14c_cf_conditional",
        "on E_c, samples with |cos α_3|<0.25 stretch less than |cos α_3|>0.8, relative to |λ|_max",
        "pass" if ok else "fail",
        "Constantin–Fefferman as a conditional. IF less aligned with extension, stretching is smaller. Not all-data.",
        ratio_low=[r["ratio_low"] for r in usable],
        ratio_high=[r["ratio_high"] for r in usable],
        mean_ratio_low=float(np.mean([r["ratio_low"] for r in usable])) if usable else 0.0,
        mean_ratio_high=float(np.mean([r["ratio_high"] for r in usable])) if usable else 0.0,
    )


def lemma_geometry_not_close() -> dict:
    return rec(
        "B14d_geometry_not_X_a_priori",
        "packet geometry closes a bound for classical X",
        "fail",
        "Lipschitz direction plus a conditional on alignment is not continuation. Median |cos α_3| ~ 1/2. An if is not a bound (B25).",
    )


def lemma_geo_not_a_retune() -> dict:
    return rec(
        "B14e_not_a_pde_retune",
        "reading strain alignment is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. Geometry is a knob on the estimate: a number you can miss.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_strain_identity(),
        lemma_conc_not_depleted(),
        lemma_ring_not_alignment(),
        lemma_cf_conditional(),
        lemma_geometry_not_close(),
        lemma_geo_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "geometry on CONC packets",
            "tuning_the_pde": False,
            "tesla": "exacting, not a jerk. Alignment is a number. If you cannot miss it, it is a paragraph.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent leftover is B17e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_geometry.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Geometry. Ring Lipschitz is real. Depletion is not all-data.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
