#!/usr/bin/env python3
"""Dilation-invariant structure probes for uniform R_★ (analytic support).

Proves-by-algebra / verifies (not PRODUCT-BLOCK):
  G. Lattice-dilation scaling ledger: R_★ and ||A^{1/2}B||_2^2/(E Y) invariant
  H. Two-shell channel dichotomy (θ=1): shell α always L, β always H
  I. Naive Λ-power HL/LL bookkeeping is NOT dilation-invariant (route kill)
  J. Signed Stokes weights: only child-on-high can feed (T_c)_+ on two-shell

Honesty: does NOT prove sup R_★ < ∞. Numerics ≠ proof.
Policy: docs/ns-review/RESEARCH-POLICY.md
Progress: docs/ns-review/UNIFORM-RSTAR-PROGRESS.md
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ns_lemma_star_core import (  # noqa: E402
    Field,
    R_star,
    lam,
    moments,
    project_perp,
)
from uniform_rstar_attack import (  # noqa: E402
    T_c_lambda_channels,
    near_shell_field,
    triad_packet_field,
    two_shell_field,
)
from uniform_rstar_identities import Ahalf_B_norm2  # noqa: E402

ARTIFACT_DIR = Path("/opt/cursor/artifacts/uniform-rstar-dilation")


def dilate_field(field: Field, n: int) -> Field:
    """Lattice dilation k ↦ n k with coefficients transported along rays.

    For n ∈ ℕ_{≥1}: v'_{n k} = v_k (same complex amplitude). This is the
    Fourier-side dilation used in Lemma D / Lemma G. Requires that n·k
    collisions do not occur for distinct support rays (true when support
    is already a set of lattice points closed under ± and n· is injective
    on that set — always for n≥1 on Z^3 without zero).
    """
    if n < 1 or int(n) != n:
        raise ValueError("dilation factor n must be a positive integer")
    n = int(n)
    out = Field()
    # Write +k only; set_mode also writes -k.
    seen = set()
    for k, vk in field.modes.items():
        if k in seen:
            continue
        nk = tuple(n * int(x) for x in k)
        # Avoid double-writing conjugates: prefer the representative with
        # first nonzero coordinate positive, else lexicographic.
        first_nz = next((c for c in k if c != 0), 0)
        if first_nz < 0:
            continue
        seen.add(k)
        seen.add(tuple(-x for x in k))
        out.set_mode(nk, vk)
    return out


def scaling_ledger(field: Field, n: int) -> dict:
    """Compare moments / R_★ / Cauchy upper bound before and after dilation."""
    f_n = dilate_field(field, n)
    E0, X0, Y0, Z0, Lam0 = moments(field)
    En, Xn, Yn, Zn, Lamn = moments(f_n)
    Ds0 = Z0 - (Y0 * Y0) / X0 if X0 > 0 else 0.0
    Dsn = Zn - (Yn * Yn) / Xn if Xn > 0 else 0.0
    rec0 = R_star(field, verify=True)
    recn = R_star(f_n, verify=True)
    AhB0 = Ahalf_B_norm2(field)
    AhBn = Ahalf_B_norm2(f_n)
    Q0 = AhB0 / (E0 * Y0) if E0 * Y0 > 0 else None
    Qn = AhBn / (En * Yn) if En * Yn > 0 else None

    def rel(a, b):
        return abs(a - b) / max(abs(a), abs(b), 1e-300)

    return {
        "n": n,
        "E_ratio": En / E0 if E0 else None,
        "X_ratio_over_n2": (Xn / X0) / (n * n) if X0 else None,
        "Y_ratio_over_n4": (Yn / Y0) / (n**4) if Y0 else None,
        "Z_ratio_over_n6": (Zn / Z0) / (n**6) if Z0 else None,
        "Lambda_ratio_over_n2": (Lamn / Lam0) / (n * n) if Lam0 else None,
        "D_s_ratio_over_n6": (Dsn / Ds0) / (n**6) if Ds0 > 1e-14 else None,
        "R_star_0": None if rec0["R_star"] == float("inf") else float(rec0["R_star"]),
        "R_star_n": None if recn["R_star"] == float("inf") else float(recn["R_star"]),
        "R_star_rel_err": (
            None
            if rec0["R_star"] == float("inf") or recn["R_star"] == float("inf")
            else rel(float(rec0["R_star"]), float(recn["R_star"]))
        ),
        "Q_AhalfB_over_EY_0": Q0,
        "Q_AhalfB_over_EY_n": Qn,
        "Q_rel_err": None if Q0 is None or Qn is None else rel(Q0, Qn),
        "T_c_0": float(rec0["T_c"]),
        "T_c_n": float(recn["T_c"]),
        "ok_R_star_invariant": bool(
            rec0.get("vacuous_single_shell")
            or (
                rec0["R_star"] != float("inf")
                and recn["R_star"] != float("inf")
                and rel(float(rec0["R_star"]), float(recn["R_star"])) < 1e-8
            )
            or (abs(float(rec0["T_c"])) < 1e-12 and abs(float(recn["T_c"])) < 1e-12)
        ),
        "ok_Q_invariant": bool(Q0 is not None and Qn is not None and rel(Q0, Qn) < 1e-8),
        "ok_moment_powers": bool(
            E0 > 0
            and rel(En, E0) < 1e-10
            and rel(Xn, (n * n) * X0) < 1e-10
            and rel(Yn, (n**4) * Y0) < 1e-10
            and rel(Zn, (n**6) * Z0) < 1e-10
            and rel(Lamn, (n * n) * Lam0) < 1e-10
        ),
    }


def two_shell_dichotomy(n1: int, n2: int, rng: np.random.Generator, theta: float = 1.0) -> dict:
    """Lemma H check: on exact two-shell α<β with θ=1, α is L and β is H."""
    if n1 == n2:
        raise ValueError("need distinct shells")
    alpha, beta = (n1, n2) if n1 < n2 else (n2, n1)
    f = two_shell_field(alpha, beta, rng, amp2=float(rng.uniform(0.3, 2.0)), per_shell=4)
    E, X, Y, Z, Lam = moments(f)
    # Algebra: Λ ∈ (α, β) whenever both shell energies > 0.
    assert alpha < Lam < beta or abs(Lam - alpha) < 1e-12 or abs(Lam - beta) < 1e-12
    shells = {}
    for k in f.modes:
        lk = int(round(lam(k)))
        shells.setdefault(lk, []).append(k)
    alpha_high = all(lam(k) >= theta * Lam for k in shells.get(alpha, []))
    beta_high = all(lam(k) >= theta * Lam for k in shells.get(beta, []))
    # With θ=1 and both energies positive, α < Λ < β ⇒ α all Low, β all High.
    both_positive = True  # two_shell_field puts energy on both
    expected = (not alpha_high) and beta_high and both_positive and (alpha < Lam < beta)
    ch = T_c_lambda_channels(f, theta=theta)
    # Signed Stokes weights for children on each shell.
    w_alpha = alpha * (alpha - Lam)
    w_beta = beta * (beta - Lam)
    return {
        "alpha": alpha,
        "beta": beta,
        "Lambda": Lam,
        "alpha_lt_Lambda_lt_beta": bool(alpha < Lam < beta),
        "alpha_all_high": bool(alpha_high),
        "beta_all_high": bool(beta_high),
        "dichotomy_ok": bool(expected),
        "weight_alpha": w_alpha,  # < 0 when α < Λ
        "weight_beta": w_beta,  # > 0 when β > Λ
        "only_high_child_feeds_Tc_plus": bool(w_alpha < 0 < w_beta),
        "T_c_HH": ch["T_c_HH"],
        "T_c_HL": ch["T_c_HL"],
        "T_c_LL": ch["T_c_LL"],
        "channel_sum_err": ch["channel_sum_err"],
    }


def naive_lambda_power_not_invariant(rng: np.random.Generator) -> dict:
    """Lemma I sanity: a toy HL/LL residual with unmatched Λ powers moves under dilation.

    Model the *elementary* leftover after absorbing low-mode mass via
        D_s ≥ c Λ² X_L
    as a dimensionless but Λ-dependent proxy
        ρ(v) = (Λ^{1/2} X) / Y
    (one of many equivalent wrong leftovers). Under k↦n k:
        Λ→n²Λ, X→n²X, Y→n⁴Y ⇒ ρ → ρ / n.
    So ρ is NOT dilation-invariant, while R_★ is. Any close that needs a
    uniform bound on ρ (or similar unmatched powers) is not geometry-only.
    """
    f0 = None
    for _ in range(30):
        cand = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=0.8)
        rec = R_star(cand, verify=True)
        if not rec.get("vacuous_single_shell") and rec["R_star"] != float("inf"):
            f0 = cand
            break
    if f0 is None:
        return {"ok": False, "error": "no_seed"}

    def rho(field: Field) -> float:
        E, X, Y, Z, Lam = moments(field)
        return (math.sqrt(Lam) * X) / Y if Y > 0 else float("nan")

    rows = []
    for n in (1, 2, 3, 4):
        f = f0 if n == 1 else dilate_field(f0, n)
        rec = R_star(f, verify=True)
        rows.append(
            {
                "n": n,
                "rho": rho(f),
                "R_star": float(rec["R_star"]),
                "rho_times_n": rho(f) * n,
            }
        )
    rhos = [r["rho"] for r in rows]
    rs = [r["R_star"] for r in rows]
    rho_spread = (max(rhos) - min(rhos)) / max(max(rhos), 1e-300)
    rs_spread = (max(rs) - min(rs)) / max(max(rs), 1e-300)
    # rho should track ~1/n; R_★ flat.
    return {
        "rows": rows,
        "rho_rel_spread": rho_spread,
        "R_star_rel_spread": rs_spread,
        "rho_not_invariant": bool(rho_spread > 0.5),
        "R_star_invariant": bool(rs_spread < 1e-8),
        "ok": bool(rho_spread > 0.5 and rs_spread < 1e-8),
        "note": (
            "Elementary unmatched Λ-power residual ρ=Λ^{1/2} X/Y scales as 1/n "
            "under lattice dilation; R_★ stays flat. This kills filing HL/LL as "
            "classical via that residual, not PRODUCT-BLOCK itself."
        ),
    }


def signed_weight_structure(rng: np.random.Generator) -> dict:
    """Lemma J: on two-shell α<β, Stokes weight on α is negative, on β positive."""
    rows = []
    for alpha, beta in ((1, 2), (2, 5), (5, 13)):
        for _ in range(3):
            d = two_shell_dichotomy(alpha, beta, rng, theta=1.0)
            rows.append(d)
    return {
        "rows": rows,
        "all_dichotomy_ok": all(r["dichotomy_ok"] for r in rows),
        "all_signed_weights_ok": all(r["only_high_child_feeds_Tc_plus"] for r in rows),
        "max_channel_sum_err": max(r["channel_sum_err"] for r in rows),
        "ok": all(r["dichotomy_ok"] and r["only_high_child_feeds_Tc_plus"] for r in rows),
    }


def run(seed: int = 20260912) -> dict:
    rng = np.random.default_rng(seed)
    # Build a nontrivial seed with T_c ≠ 0 when possible.
    seed_field = None
    for _ in range(40):
        cand = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=float(rng.uniform(0.4, 1.2)))
        rec = R_star(cand, verify=True)
        if (
            not rec.get("vacuous_single_shell")
            and rec["R_star"] != float("inf")
            and abs(float(rec["T_c"])) > 1e-12
        ):
            seed_field = cand
            break
    if seed_field is None:
        seed_field = two_shell_field(1, 2, rng, amp2=1.0, per_shell=4)

    ledger_rows = [scaling_ledger(seed_field, n) for n in (2, 3, 4)]
    # Also check near-shell packet dilation.
    near = near_shell_field(5, 8, 0.2, rng)
    ledger_rows.append(scaling_ledger(near, 2))

    naive = naive_lambda_power_not_invariant(rng)
    signed = signed_weight_structure(rng)

    summary = {
        "attack": "uniform_rstar_dilation_push",
        "seed": seed,
        "lemma_G_dilation_ledger_ok": all(
            r["ok_moment_powers"] and r["ok_R_star_invariant"] and r["ok_Q_invariant"]
            for r in ledger_rows
        ),
        "lemma_H_I_J_two_shell_signed_ok": signed["ok"],
        "lemma_I_naive_lambda_route_killed": naive["ok"],
        "max_R_star_rel_err": max(
            (r["R_star_rel_err"] for r in ledger_rows if r["R_star_rel_err"] is not None),
            default=None,
        ),
        "max_Q_rel_err": max(
            (r["Q_rel_err"] for r in ledger_rows if r["Q_rel_err"] is not None),
            default=None,
        ),
        "status": {
            "PRODUCT_BLOCK": "OPEN",
            "uniform_R_star": "OPEN",
            "Lemma_star": "HYPOTHESIS",
            "Clay_Statement_B": "NOT_SOLVED",
            "HL_LL_classical_route": "KILLED_unmatched_Lambda_powers",
            "HL_LL_geometric_bound": "OPEN",
            "HH_bound": "OPEN",
            "dilation_invariant_close": "OPEN",
            "numerics_are_proof": False,
        },
        "progress_doc": "docs/ns-review/UNIFORM-RSTAR-PROGRESS.md",
        "note": (
            "Dilation ledger + two-shell dichotomy + naive-Λ route kill. "
            "Does not prove PRODUCT-BLOCK. HH and geometric HL/LL still open."
        ),
    }
    return {
        "summary": summary,
        "ledger_rows": ledger_rows,
        "naive_lambda_route": naive,
        "signed_two_shell": signed,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=20260912)
    ap.add_argument("--out-dir", type=str, default=str(ARTIFACT_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = run(seed=args.seed)
    s = payload["summary"]
    (out_dir / "uniform_rstar_dilation.json").write_text(
        json.dumps(payload, indent=2, default=str)
    )
    lines = [
        "uniform_rstar_dilation — analytic support push",
        s["note"],
        f"G dilation_ok={s['lemma_G_dilation_ledger_ok']}  "
        f"H/J two_shell_ok={s['lemma_H_I_J_two_shell_signed_ok']}  "
        f"I naive_Lambda_killed={s['lemma_I_naive_lambda_route_killed']}",
        f"max_R*_rel_err={s['max_R_star_rel_err']!r}  max_Q_rel_err={s['max_Q_rel_err']!r}",
        f"status PRODUCT-BLOCK={s['status']['PRODUCT_BLOCK']}  "
        f"HL/LL_geom={s['status']['HL_LL_geometric_bound']}  "
        f"HH={s['status']['HH_bound']}  "
        f"Clay={s['status']['Clay_Statement_B']}",
    ]
    text = "\n".join(lines) + "\n"
    (out_dir / "uniform_rstar_dilation.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
