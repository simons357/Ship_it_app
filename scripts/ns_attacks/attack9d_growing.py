#!/usr/bin/env python3
"""Attack 9D — remaining packet falsifier.

Growing input and output supports. Full complex (elliptical)
polarizations. Frequency factors kept.

Target: ||Π_β B(w,w)||_2 ≤ C (α/√β) ||w||_2^2
     iff  sup K_{α,β} < ∞.

Fixed-output Θ(m²) is excluded (K≤16s). Freiman-AP is dead.
Do not redo finite 9B (K≈0.641, linear pol).

Bounded samples are not a proof. A diverging family would
kill ★. NS is not solved. Lemma★ OPEN.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    _orthonormal_pol_basis,
    normalize_field,
    shells_up_to,
)
from ns_attacks.attack9b_output_counting import cs_rows  # noqa: E402
from ns_attacks.stokes_moments import Field, ModeKey, enforce_reality  # noqa: E402


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def full_complex_pol(k: ModeKey, psi: float, phi1: float, phi2: float) -> np.ndarray:
    """Unit elliptical polarization in k^⊥. Three real angles.

    Linear polarization is the slice phi1 = phi2 (up to the global phase
    already in pol_from_angles). This is the extra 9D degree of freedom.
    """
    e1, e2 = _orthonormal_pol_basis(k)
    v = np.cos(psi) * np.exp(1j * phi1) * e1 + np.sin(psi) * np.exp(1j * phi2) * e2
    return v.astype(np.complex128)


def build_full_complex_field(
    modes: Sequence[ModeKey],
    amps: Sequence[float],
    psis: Sequence[float],
    phi1s: Sequence[float],
    phi2s: Sequence[float],
) -> Field:
    field: Field = {}
    for k, a, psi, p1, p2 in zip(modes, amps, psis, phi1s, phi2s):
        if a <= 0:
            continue
        field[k] = a * full_complex_pol(k, float(psi), float(p1), float(p2))
    return enforce_reality(field)


def random_full_complex_params(n: int, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    return {
        "amps": rng.uniform(0.2, 1.5, size=n),
        "psis": rng.uniform(0.0, 0.5 * np.pi, size=n),
        "phi1s": rng.uniform(0.0, 2 * np.pi, size=n),
        "phi2s": rng.uniform(0.0, 2 * np.pi, size=n),
    }


def linear_slice_params(n: int, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    """Linear polarization: φ1=φ2, ψ = θ in the real plane."""
    thetas = rng.uniform(0.0, 2 * np.pi, size=n)
    phis = rng.uniform(0.0, 2 * np.pi, size=n)
    # Map real-plane angle into [0, π/2] mix + sign into phases.
    psis = np.mod(thetas, 0.5 * np.pi)
    return {
        "amps": rng.uniform(0.2, 1.5, size=n),
        "psis": psis,
        "phi1s": phis,
        "phi2s": phis.copy(),
    }


def field_from_full_params(modes: Sequence[ModeKey], params: Dict[str, np.ndarray]) -> Field:
    return normalize_field(
        build_full_complex_field(
            modes, params["amps"], params["psis"], params["phi1s"], params["phi2s"]
        )
    )


def optimize_full_complex(
    modes: Sequence[ModeKey],
    beta: float,
    rng: np.random.Generator,
    n_trials: int,
    n_refine: int,
) -> Dict:
    n = len(modes)
    best = {"K": -1.0, "rec": None, "params": None}
    if n < 2:
        return {"K": float("nan"), "has_params": False}
    alphas = {k[0] * k[0] + k[1] * k[1] + k[2] * k[2] for k in modes}
    alpha = float(next(iter(alphas))) if len(alphas) == 1 else float("nan")
    for _ in range(n_trials):
        params = random_full_complex_params(n, rng)
        w = field_from_full_params(modes, params)
        rec = cs_rows(w, float(beta))
        if rec["K"] > best["K"]:
            best = {"K": rec["K"], "rec": rec, "params": {k: v.copy() for k, v in params.items()}}
    if best["params"] is not None:
        params = {k: v.copy() for k, v in best["params"].items()}
        for _ in range(n_refine):
            trial = {k: v.copy() for k, v in params.items()}
            trial["psis"] = np.clip(trial["psis"] + rng.normal(0, 0.25, size=n), 0.0, 0.5 * np.pi)
            trial["phi1s"] = trial["phi1s"] + rng.normal(0, 0.4, size=n)
            trial["phi2s"] = trial["phi2s"] + rng.normal(0, 0.4, size=n)
            trial["amps"] = np.clip(trial["amps"] * rng.uniform(0.7, 1.35, size=n), 0.05, 5.0)
            w = field_from_full_params(modes, trial)
            rec = cs_rows(w, float(beta))
            if rec["K"] > best["K"]:
                best = {"K": rec["K"], "rec": rec, "params": {k: v.copy() for k, v in trial.items()}}
                params = trial
    out = dict(best["rec"] or {})
    out["opt_K"] = float(best["K"])
    out["has_params"] = best["params"] is not None
    out["alpha"] = alpha
    out["beta"] = float(beta)
    out["n_pos"] = n
    return out


def linear_control_K(modes: Sequence[ModeKey], beta: float, rng: np.random.Generator) -> float:
    """One linear-pol field, same modes. Control, not the 9B 0.641 redo."""
    n = len(modes)
    thetas = rng.uniform(0, 2 * np.pi, size=n)
    phis = rng.uniform(0, 2 * np.pi, size=n)
    amps = rng.uniform(0.2, 1.5, size=n)
    from ns_attacks.attack9b_exact_shell_K import build_exact_shell_field

    w = normalize_field(build_exact_shell_field(modes, amps, thetas, phis))
    return float(cs_rows(w, float(beta))["K"])


def run(
    seed: int = 1390,
    n_random: int = 8,
    n_opt_trials: int = 20,
    n_opt_refine: int = 10,
) -> Dict:
    rng = np.random.default_rng(seed)
    shells = shells_up_to(12)
    shells_ext = shells_up_to(16)
    wanted = [(4, 8), (5, 10), (9, 18), (8, 16), (13, 26), (5, 2), (9, 8)]
    m_list = (2, 4, 8, 16)
    rows = []
    for alpha, beta in wanted:
        pos = shells.get(alpha, [])
        if len(pos) < 2 or beta not in shells_ext:
            continue
        targets = [m for m in m_list if 2 <= m <= len(pos)]
        if len(pos) not in targets:
            targets.append(len(pos))
        for m in targets:
            modes = list(pos[:m])
            print(f"  9D α={alpha} β={beta} m_pos={len(modes)}", flush=True)
            for t in range(n_random):
                params = random_full_complex_params(len(modes), rng)
                w = field_from_full_params(modes, params)
                rec = cs_rows(w, float(beta))
                rec["construction"] = "full_complex_random"
                rec["trial"] = t
                rec["n_pos"] = len(modes)
                rec["keep_|k|"] = True
                rec["target_ratio"] = rec.get("correct_target_ratio")
                rows.append(rec)
            if n_opt_trials > 0:
                opt = optimize_full_complex(
                    modes, float(beta), rng, n_trials=n_opt_trials, n_refine=n_opt_refine
                )
                opt["construction"] = "full_complex_optimized"
                opt["keep_|k|"] = True
                opt["target_ratio"] = opt.get("correct_target_ratio")
                opt["linear_control_K"] = linear_control_K(modes, float(beta), rng)
                rows.append(opt)

    def _max(key):
        vals = [r[key] for r in rows if r.get(key) is not None and math.isfinite(r.get(key, float("nan")))]
        return max(vals) if vals else None

    n_fail_16s = sum(1 for r in rows if not r.get("K_le_16s", True))
    n_fail_cs = sum(1 for r in rows if not r.get("cs_ok", True))
    n_fail_pairs = sum(1 for r in rows if not r.get("pairs_le_m", True))
    worst = max(rows, key=lambda r: r.get("K") or -1.0) if rows else {}
    # Wrong packaging: drop |k| / write ||ΠB|| ≤ C α ||w||²  ⇒  K ≲ β.
    wrong = [
        (r.get("PiB_L2") or 0.0) / max(r.get("alpha") or 1.0, 1e-30)
        for r in rows
        if r.get("PiB_L2") is not None
    ]
    return {
        "attack": "9D-growing-full-complex",
        "seed": seed,
        "target": "||Π_β B||_2 ≤ C (α/√β) ||w||_2^2  iff  sup K < ∞",
        "frequency_factors": "kept",
        "polarization": "full complex / elliptical (3 angles per mode)",
        "excluded": "fixed-output Θ(m²); Freiman-AP",
        "do_not_redo": "finite 9B K≈0.641 linear-pol",
        "n_fields": len(rows),
        "max_K": _max("K"),
        "max_sqrt_K": _max("sqrt_K"),
        "max_s": _max("s"),
        "max_m": _max("m"),
        "max_target_ratio": _max("correct_target_ratio"),
        "n_fail_K_le_16s": n_fail_16s,
        "n_fail_cs": n_fail_cs,
        "n_fail_pairs_le_m": n_fail_pairs,
        "worst": {
            "K": worst.get("K"),
            "s": worst.get("s"),
            "m": worst.get("m"),
            "alpha": worst.get("alpha"),
            "beta": worst.get("beta"),
            "construction": worst.get("construction"),
            "sqrt_K": worst.get("sqrt_K"),
        },
        "wrong_packaging_max_PiB_over_alpha": max(wrong) if wrong else None,
        "verdict": (
            "9D_SAMPLES_FINITE_NOT_PROOF_kill_lane_LIVE"
            if n_fail_16s == 0 and n_fail_pairs == 0
            else "INEQUALITY_FAIL_check_implementation"
        ),
        "ns_solved": False,
        "lemma_star": "OPEN",
        "kill_lane": "LIVE",
        "star_reason": "NOT written",
        "rows": rows,
        "note": (
            "Bounded max K is not C0 and is not a kill. "
            "A family with K→∞ would kill ★. "
            "The ★ reason (signed stretching vs spectral spread) is not written. "
            "Do not merge Attack 12 R_★ ∼ β/α with √K. NS not solved."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument("--n-random", type=int, default=8)
    ap.add_argument("--opt-trials", type=int, default=20)
    ap.add_argument("--opt-refine", type=int, default=10)
    args = ap.parse_args()
    print("Attack 9D — growing supports, full complex pol, |k| kept", flush=True)
    print("Kill lane LIVE. ★ OPEN. NS not solved.", flush=True)
    summary = run(
        seed=args.seed,
        n_random=args.n_random,
        n_opt_trials=args.opt_trials,
        n_opt_refine=args.opt_refine,
    )
    slim = {k: v for k, v in summary.items() if k != "rows"}
    print(json.dumps(_py(slim), indent=2), flush=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(_py(summary), indent=2))
        print(f"wrote {args.out}", flush=True)
    return 0 if summary["verdict"].startswith("9D_SAMPLES") else 1


if __name__ == "__main__":
    raise SystemExit(main())
