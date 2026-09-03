#!/usr/bin/env python3
"""
Unifier-program exercise (not a physics claim).

Domain Architect is not a unifier. This script only asks: if success is a
defined scalar R, which of 16 reconstructed coordinates actually move R?

The DA Cosmos 16-list is not in this repository. Coordinates below are
reconstructed from the public SFE one-liner plus the four-force scales any
unification score has to hit. Re-run when the Cosmos list is supplied.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


# Observed dimensionless anchors (PDG-style, order-of-magnitude).
# Used only as the external target of R, not as a derived prediction.
OBS = {
    "log_alpha_em": math.log(1.0 / 127.9),
    "log_alpha_s": math.log(0.1180),
    "sin2_theta_w": 0.23122,
    "log_hierarchy": math.log(1.2209e19 / 246.22),  # M_Pl / v
    "log_qcd_ratio": math.log(0.217 / 246.22),  # Λ_QCD / v
    "log_cc_ratio": math.log((2.3e-3) / (246.22 * 1e9)),  # ρ_Λ^{1/4} (GeV) / v
    "log_weak_ratio": math.log(80.377 / 246.22),  # m_W / v
}

# 15 inputs. Index 16 is R, the realization / success output.
INPUTS = [
    "A_mean",
    "f_mean",
    "phi_scale",
    "delta_spread",
    "p_cut",
    "S_coh",
    "grad_coh",
    "kappa_att",
    "log_alpha_em",
    "log_alpha_s",
    "sin2_theta_w",
    "log_hierarchy",
    "log_qcd_ratio",
    "log_cc_ratio",
    "log_weak_ratio",
]


def realization(row: dict[str, float]) -> tuple[float, float, float, float]:
    """
    Success definition.

    A unifier program with state x succeeds at tolerance ε when a single
    map reproduces the four interaction scales and the two leftover
    hierarchies (Planck, vacuum energy) with χ²_ext ≤ ε², and the internal
    coherence bookkeeping is not disordered (χ²_int small).

    R = exp(-½ χ²_ext) · exp(-½ χ²_int) ∈ (0, 1].

    This is a score on a reconstructed vector. It is not a derivation of
    the Standard Model or of SFE.
    """
    chi_ext = 0.0
    for key, target in OBS.items():
        chi_ext += (row[key] - target) ** 2

    # Internal HB-language bookkeeping: low entropy, low phase disorder,
    # moderate attractor, gradient not exploding.
    chi_int = (
        (row["S_coh"] - 0.0) ** 2
        + (row["delta_spread"] - 0.0) ** 2
        + (row["grad_coh"] - 0.2) ** 2
        + (row["kappa_att"] - 0.5) ** 2
        + (row["A_mean"] - 1.0) ** 2 * 0.25
        + (row["f_mean"] - 1.0) ** 2 * 0.25
        + (row["phi_scale"] - 1.0) ** 2 * 0.25
        + ((row["p_cut"] - 8.0) / 8.0) ** 2 * 0.25
    )
    r_ext = math.exp(-0.5 * chi_ext)
    r_int = math.exp(-0.5 * chi_int)
    r = r_ext * r_int
    return r, chi_ext, chi_int, r_ext


def sample_rows(n: int, rng: np.random.Generator) -> list[dict[str, float]]:
    rows = []
    for _ in range(n):
        row = {
            "A_mean": float(rng.uniform(0.2, 2.0)),
            "f_mean": float(rng.uniform(0.2, 2.0)),
            "phi_scale": float(rng.uniform(0.2, 2.0)),
            "delta_spread": float(rng.uniform(0.0, 1.5)),
            "p_cut": float(rng.uniform(2.0, 16.0)),
            "S_coh": float(rng.uniform(0.0, 2.0)),
            "grad_coh": float(rng.uniform(0.0, 1.5)),
            "kappa_att": float(rng.uniform(0.0, 1.5)),
            "log_alpha_em": float(OBS["log_alpha_em"] + rng.normal(0.0, 0.15)),
            "log_alpha_s": float(OBS["log_alpha_s"] + rng.normal(0.0, 0.15)),
            "sin2_theta_w": float(OBS["sin2_theta_w"] + rng.normal(0.0, 0.03)),
            "log_hierarchy": float(OBS["log_hierarchy"] + rng.normal(0.0, 1.5)),
            "log_qcd_ratio": float(OBS["log_qcd_ratio"] + rng.normal(0.0, 0.4)),
            "log_cc_ratio": float(OBS["log_cc_ratio"] + rng.normal(0.0, 2.0)),
            "log_weak_ratio": float(OBS["log_weak_ratio"] + rng.normal(0.0, 0.15)),
        }
        r, chi_ext, chi_int, r_ext = realization(row)
        row["R"] = r
        row["chi_ext"] = chi_ext
        row["chi_int"] = chi_int
        row["R_ext"] = r_ext
        rows.append(row)
    return rows


def corr_with_r(rows: list[dict[str, float]]) -> dict[str, float]:
    r = np.array([row["R"] for row in rows])
    out = {}
    for name in INPUTS:
        x = np.array([row[name] for row in rows])
        if np.std(x) < 1e-18 or np.std(r) < 1e-18:
            out[name] = 0.0
        else:
            out[name] = float(np.corrcoef(x, r)[0, 1])
    return out


def permutation_importance(rows: list[dict[str, float]], rng: np.random.Generator) -> dict[str, float]:
    """Mean |ΔR| when one coordinate is shuffled (normalized to a fraction)."""
    r0 = np.array([row["R"] for row in rows])
    imp = {}
    for name in INPUTS:
        shuffled = [dict(row) for row in rows]
        vals = np.array([row[name] for row in shuffled])
        rng.shuffle(vals)
        r1 = []
        for row, val in zip(shuffled, vals):
            row[name] = float(val)
            r1.append(realization(row)[0])
        imp[name] = float(np.mean(np.abs(np.array(r1) - r0)))
    s = sum(imp.values()) or 1.0
    return {k: v / s for k, v in imp.items()}


def observed_row() -> dict[str, float]:
    row = {
        "A_mean": 1.0,
        "f_mean": 1.0,
        "phi_scale": 1.0,
        "delta_spread": 0.0,
        "p_cut": 8.0,
        "S_coh": 0.0,
        "grad_coh": 0.2,
        "kappa_att": 0.5,
        **OBS,
    }
    r, chi_ext, chi_int, r_ext = realization(row)
    row["R"] = r
    row["chi_ext"] = chi_ext
    row["chi_int"] = chi_int
    row["R_ext"] = r_ext
    return row


def main() -> int:
    p = argparse.ArgumentParser(description="Unifier-program sensitivity exercise")
    p.add_argument("--n", type=int, default=4000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--out", type=Path, default=Path("results/unifier_exercise.json"))
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    rows = sample_rows(args.n, rng)
    corr = corr_with_r(rows)
    imp = permutation_importance(rows, rng)
    ranked = sorted(imp.items(), key=lambda kv: kv[1], reverse=True)
    target = observed_row()

    payload = {
        "meta": {
            "exercise": True,
            "not_a_unifier": True,
            "cosmos_list_found": True,
            "this_score_is_not_the_cosmo_16": True,
            "note": (
                "Official Cosmo 16 is docs/COSMO-SIXTEEN.md. This score still uses "
                "the reconstructed 15-input vector. R is the 16th coordinate here; "
                "Cosmo's 16th is sum m_nu. Do not glue the catalogs."
            ),
            "n": args.n,
            "seed": args.seed,
        },
        "success_definition": {
            "R": "exp(-1/2 χ²_ext) * exp(-1/2 χ²_int)",
            "chi_ext": "sum of squared log-residuals of the four-force / hierarchy anchors",
            "chi_int": "SFE-knob distance to a quiet coherence state",
            "unifier_at_eps": "χ²_ext ≤ ε² with one map for all four interactions",
        },
        "inputs": INPUTS,
        "observed_anchors": OBS,
        "target_state": target,
        "importance": {k: v for k, v in ranked},
        "corr_with_R": corr,
        "top_drivers": [name for name, _ in ranked[:5]],
        "works_as_unifier": False,
        "works_as_exercise": True,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))

    print("reconstructed inputs:", ", ".join(INPUTS))
    print(f"target R (quiet + observed anchors) = {target['R']:.6f}  χ²_ext={target['chi_ext']:.3e}")
    print("permutation importance (fraction of R-sensitivity):")
    for name, val in ranked:
        print(f"  {name:16s}  {val:7.3f}   corr={corr[name]:+.3f}")
    print(f"wrote {args.out}")
    print("not a unifier. exercise only. cosmos 16-list not found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
