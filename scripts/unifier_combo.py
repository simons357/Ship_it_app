#!/usr/bin/env python3
"""
Combinatorial search for which reconstructed knobs lock realization R.

Not a unifier. Domain Architect does not supply the missing map F.
This only answers: if we do not know how many coordinates are involved,
which smallest subsets lock R when they sit at the target and the rest
are left random.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from unifier_exercise import INPUTS, OBS, observed_row  # noqa: E402


TARGET = observed_row()
EXT = list(OBS.keys())
INT_W = {
    "S_coh": (0.0, 1.0),
    "delta_spread": (0.0, 1.0),
    "grad_coh": (0.2, 1.0),
    "kappa_att": (0.5, 1.0),
    "A_mean": (1.0, 0.25),
    "f_mean": (1.0, 0.25),
    "phi_scale": (1.0, 0.25),
    "p_cut": (8.0, 0.25 / 64.0),  # ((p-8)/8)^2 * 0.25 = (p-8)^2 * 0.25/64
}


def sample_matrix(n: int, rng: np.random.Generator) -> np.ndarray:
    x = np.zeros((n, len(INPUTS)))
    x[:, 0] = rng.uniform(0.2, 2.0, n)  # A_mean
    x[:, 1] = rng.uniform(0.2, 2.0, n)  # f_mean
    x[:, 2] = rng.uniform(0.2, 2.0, n)  # phi_scale
    x[:, 3] = rng.uniform(0.0, 1.5, n)  # delta_spread
    x[:, 4] = rng.uniform(2.0, 16.0, n)  # p_cut
    x[:, 5] = rng.uniform(0.0, 2.0, n)  # S_coh
    x[:, 6] = rng.uniform(0.0, 1.5, n)  # grad_coh
    x[:, 7] = rng.uniform(0.0, 1.5, n)  # kappa_att
    x[:, 8] = OBS["log_alpha_em"] + rng.normal(0.0, 0.15, n)
    x[:, 9] = OBS["log_alpha_s"] + rng.normal(0.0, 0.15, n)
    x[:, 10] = OBS["sin2_theta_w"] + rng.normal(0.0, 0.03, n)
    x[:, 11] = OBS["log_hierarchy"] + rng.normal(0.0, 1.5, n)
    x[:, 12] = OBS["log_qcd_ratio"] + rng.normal(0.0, 0.4, n)
    x[:, 13] = OBS["log_cc_ratio"] + rng.normal(0.0, 2.0, n)
    x[:, 14] = OBS["log_weak_ratio"] + rng.normal(0.0, 0.15, n)
    return x


def r_batch(x: np.ndarray) -> np.ndarray:
    idx = {name: i for i, name in enumerate(INPUTS)}
    chi_ext = np.zeros(x.shape[0])
    for name in EXT:
        chi_ext = chi_ext + (x[:, idx[name]] - OBS[name]) ** 2
    chi_int = (
        (x[:, idx["S_coh"]] - 0.0) ** 2
        + (x[:, idx["delta_spread"]] - 0.0) ** 2
        + (x[:, idx["grad_coh"]] - 0.2) ** 2
        + (x[:, idx["kappa_att"]] - 0.5) ** 2
        + 0.25 * (x[:, idx["A_mean"]] - 1.0) ** 2
        + 0.25 * (x[:, idx["f_mean"]] - 1.0) ** 2
        + 0.25 * (x[:, idx["phi_scale"]] - 1.0) ** 2
        + 0.25 * ((x[:, idx["p_cut"]] - 8.0) / 8.0) ** 2
    )
    return np.exp(-0.5 * chi_ext) * np.exp(-0.5 * chi_int)


def lock_score(base: np.ndarray, names: tuple[str, ...]) -> float:
    x = base.copy()
    idx = {name: i for i, name in enumerate(INPUTS)}
    for name in names:
        x[:, idx[name]] = TARGET[name]
    return float(np.mean(r_batch(x)))


def main() -> int:
    p = argparse.ArgumentParser(description="Subset search for knobs that lock R")
    p.add_argument("--n", type=int, default=256)
    p.add_argument("--kmax", type=int, default=5)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--out", type=Path, default=Path("results/unifier_combo.json"))
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    base = sample_matrix(args.n, rng)
    baseline = float(np.mean(r_batch(base)))

    best_by_k = []
    hits_half = []
    hits_80 = []
    for k in range(1, args.kmax + 1):
        best_name = None
        best_val = -1.0
        for combo in itertools.combinations(INPUTS, k):
            val = lock_score(base, combo)
            rec = {"k": k, "set": list(combo), "lock_R": val}
            if val > best_val:
                best_val = val
                best_name = rec
            if val >= 0.5:
                hits_half.append(rec)
            if val >= 0.8:
                hits_80.append(rec)
        best_by_k.append(best_name)
        print(f"k={k}  best lock_R={best_val:.4f}  set={best_name['set']}")

    # greedy forward, for a check past kmax
    greedy = []
    chosen: list[str] = []
    for _ in range(min(8, len(INPUTS))):
        leftover = [n for n in INPUTS if n not in chosen]
        pick, pick_val = None, -1.0
        for name in leftover:
            val = lock_score(base, tuple(chosen + [name]))
            if val > pick_val:
                pick, pick_val = name, val
        chosen.append(pick)
        greedy.append({"k": len(chosen), "set": list(chosen), "lock_R": pick_val})

    # variables that appear in every best set of size k>=2
    core = set(best_by_k[-1]["set"]) if best_by_k else set()
    for rec in best_by_k[1:]:
        core &= set(rec["set"])

    payload = {
        "meta": {
            "exercise": True,
            "not_a_unifier": True,
            "note": (
                "lock_R = E[R | named coords at target, others random]. "
                "DA does not compute F. This is subset search on the score."
            ),
            "n": args.n,
            "kmax": args.kmax,
            "baseline_R_all_random": baseline,
        },
        "best_by_k": best_by_k,
        "greedy_forward": greedy,
        "n_sets_lock_ge_0.5": len(hits_half),
        "n_sets_lock_ge_0.8": len(hits_80),
        "smallest_half": min(hits_half, key=lambda r: (r["k"], -r["lock_R"]), default=None),
        "smallest_80": min(hits_80, key=lambda r: (r["k"], -r["lock_R"]), default=None),
        "core_in_best_sets_k_ge_2": sorted(core),
        "candidates": {
            "must_lock_external": ["log_cc_ratio", "log_hierarchy"],
            "must_lock_internal": ["S_coh", "delta_spread"],
            "weak_on_this_score": [
                "A_mean",
                "f_mean",
                "phi_scale",
                "p_cut",
                "log_alpha_em",
                "log_alpha_s",
                "sin2_theta_w",
                "log_weak_ratio",
            ],
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))
    print(f"baseline all-random R={baseline:.4f}")
    print("core in best sets k>=2:", sorted(core))
    print(f"sets with lock_R>=0.5: {len(hits_half)}; >=0.8: {len(hits_80)}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
