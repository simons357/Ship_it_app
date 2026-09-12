#!/usr/bin/env python3
"""HH-channel push + Cauchy-sufficient route block (analytic support).

Proves / verifies (not PRODUCT-BLOCK):
  K. HH mass control for θ>1: X_H ≤ D_s / ((θ-1)^2 Λ^2)
  L. Face-family witness: Q = ||A^{1/2}B||_2^2/(E Y) grows ~ c K^2
     while R_★ = 0 on the same fields — Cauchy-sufficient close is
     strategically blocked (cancellations mandatory). Q→∞ is recorded as
     a conjecture with monotone growth through K≤K_max, not a theorem.
  M. Sanity: true same-shell HH→L lattice triples are sparse; when present,
     sampled R_★ stays small (no kill).

Honesty: does NOT prove sup R_★ < ∞. Does NOT claim Clay / NS.
Numerics ≠ proof. Policy: docs/ns-review/RESEARCH-POLICY.md
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
    shell_wavevectors,
    T_c_direct,
    D_s_moment_form,
    D_s_direct_form,
)
from uniform_rstar_attack import (  # noqa: E402
    T_c_lambda_channels,
    two_shell_field,
)
from uniform_rstar_identities import Ahalf_B_norm2  # noqa: E402

ARTIFACT_DIR = Path("/opt/cursor/artifacts/uniform-rstar-hh-push")


def Q_B(field: Field) -> float:
    E, X, Y, Z, Lam = moments(field)
    if E * Y <= 0:
        return float("nan")
    return Ahalf_B_norm2(field) / (E * Y)


def safe_R_star(field: Field) -> dict:
    E, X, Y, Z, Lam = moments(field)
    Ds_m = D_s_moment_form(X, Y, Z)
    Ds_d = D_s_direct_form(field, Lam)
    Tc = T_c_direct(field, Lam)
    if Ds_m <= 1e-28 and Ds_d <= 1e-28:
        return {
            "R_star": None,
            "vacuous": abs(Tc) < 1e-14,
            "T_c": Tc,
            "D_s": 0.0,
            "Lambda": Lam,
            "E": E,
            "Y": Y,
        }
    rec = R_star(field, verify=True)
    return {
        "R_star": None if rec["R_star"] == float("inf") else float(rec["R_star"]),
        "vacuous": bool(rec.get("vacuous_single_shell")),
        "T_c": float(rec["T_c"]),
        "D_s": float(rec["D_s"]),
        "Lambda": float(rec["Lambda"]),
        "E": float(rec["E"]),
        "Y": float(rec["Y"]),
    }


def X_high(field: Field, Lambda: float, theta: float) -> float:
    total = 0.0
    for k, vk in field.modes.items():
        if lam(k) >= theta * Lambda:
            total += lam(k) * float(np.vdot(vk, vk).real)
    return total


def check_lemma_K_hh_mass(
    field: Field, theta: float = 2.0, tol: float = 1e-9
) -> dict:
    """Lemma K: for θ>1, X_H ≤ D_s / ((θ-1)^2 Λ^2)."""
    if theta <= 1.0:
        raise ValueError("Lemma K requires θ>1")
    E, X, Y, Z, Lam = moments(field)
    Ds = Z - (Y * Y) / X if X > 0 else 0.0
    XH = X_high(field, Lam, theta)
    bound = Ds / (((theta - 1.0) ** 2) * (Lam ** 2)) if Lam > 0 else 0.0
    return {
        "theta": theta,
        "Lambda": Lam,
        "D_s": Ds,
        "X_H": XH,
        "bound": bound,
        "ok": bool(XH <= bound + tol),
        "ratio_XH_over_bound": (XH / bound) if bound > 0 else None,
    }


def face_field(K: int, pol: str = "e2") -> Field:
    """Deterministic face support {k_1=K, |k_2|,|k_3|≤K} \\ {0}, pol → e_2."""
    f = Field()
    if pol == "e2":
        w0 = np.array([0.0, 1.0, 0.0], dtype=complex)
    elif pol == "e3":
        w0 = np.array([0.0, 0.0, 1.0], dtype=complex)
    else:
        w0 = np.array([0.0, 1.0, 1.0], dtype=complex)
    for a in range(-K, K + 1):
        for b in range(-K, K + 1):
            k = (K, a, b)
            if (a < 0) or (a == 0 and b < 0) or (a == 0 and b == 0):
                continue
            f.set_mode(k, project_perp(k, w0))
    return f.normalize(1.0)


def face_family_probe(K_max: int = 12) -> dict:
    """Lemma L witness: Q_B grows on face fields; R_★ stays 0."""
    rows = []
    for K in range(2, K_max + 1):
        f = face_field(K)
        qb = Q_B(f)
        rs = safe_R_star(f)
        rows.append(
            {
                "K": K,
                "n_modes_canonical": len(f.modes) // 2,
                "Q_B": qb,
                "Q_B_over_K": qb / K,
                "Q_B_over_K2": qb / (K * K),
                "R_star": rs["R_star"],
                "T_c": rs["T_c"],
                "D_s": rs["D_s"],
                "Y": rs["Y"],
            }
        )
    qbs = [r["Q_B"] for r in rows]
    monotone = all(qbs[i] < qbs[i + 1] for i in range(len(qbs) - 1))
    # Strategic block: Q already exceeds sparse-mode O(1) folklore ceiling
    # while T_c vanishes (cancellations mandatory for R_★).
    block = bool(qbs[-1] > 1.0 and all(abs(r["T_c"]) < 1e-12 for r in rows))
    return {
        "rows": rows,
        "monotone_Q_through_Kmax": monotone,
        "K_max": K_max,
        "Q_at_Kmax": qbs[-1] if qbs else None,
        "Q_over_K2_at_Kmax": rows[-1]["Q_B_over_K2"] if rows else None,
        "cauchy_sufficient_strategically_blocked": block,
        "Q_unbounded_status": "CONJECTURE_growth_~c_K2_not_theorem",
        "note": (
            "Face fields give large Q with T_c=0=R_★. "
            "Closes nothing on PRODUCT-BLOCK; kills relying on O(1) Q alone."
        ),
    }


def find_hh_to_low_triples(alpha: int, beta: int, max_pairs: int = 40) -> list:
    ks_a = shell_wavevectors(alpha, canonical_only=False)
    ks_b = shell_wavevectors(beta, canonical_only=False)
    set_b = set(ks_b)
    triples = []
    for k in ks_a:
        for p in ks_b:
            q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
            if q in set_b:
                triples.append((k, p, q))
                if len(triples) >= max_pairs:
                    return triples
    return triples


def hh_to_low_sanity(rng: np.random.Generator) -> dict:
    """Lemma M: sparse true HH→L triples; sampled R_★ small."""
    pair_counts = {}
    best = {"R_star": 0.0}
    for alpha, beta in [(1, 5), (1, 13), (2, 10), (2, 50), (5, 25)]:
        triples = find_hh_to_low_triples(alpha, beta, max_pairs=30)
        pair_counts[f"{alpha}_{beta}"] = len(triples)
        for (k, p, q) in triples[:8]:
            for amp_h in (0.05, 0.2, 0.8):
                f = Field()
                f.set_mode(k, project_perp(k, np.array([1.0, 0.2, -0.1], complex)))
                f.set_mode(
                    p,
                    amp_h
                    * project_perp(p, rng.normal(size=3) + 1j * rng.normal(size=3)),
                )
                f.set_mode(
                    q,
                    amp_h
                    * project_perp(q, rng.normal(size=3) + 1j * rng.normal(size=3)),
                )
                f = f.normalize(1.0)
                E, X, Y, Z, Lam = moments(f)
                if not (lam(p) >= Lam - 1e-12 and lam(q) >= Lam - 1e-12):
                    continue
                rs = safe_R_star(f)
                if rs["R_star"] is None:
                    continue
                ch = T_c_lambda_channels(f, theta=1.0)
                if rs["R_star"] > best["R_star"]:
                    best = {
                        "R_star": rs["R_star"],
                        "alpha": alpha,
                        "beta": beta,
                        "T_c_HH": ch["T_c_HH"],
                        "T_c_HL": ch["T_c_HL"],
                        "Q_B": Q_B(f),
                    }
    return {
        "triple_counts": pair_counts,
        "best_true_HH_sample": best,
        "kill_triggered": bool(best["R_star"] > 1e3),
        "note": "Sparse lattice HH→L; no R_★ divergence in samples.",
    }


def run(seed: int = 20260912, K_max: int = 10) -> dict:
    rng = np.random.default_rng(seed)
    lemma_K_rows = []
    for _ in range(25):
        f = two_shell_field(
            1, 8, rng, amp2=float(rng.uniform(0.1, 2.0)), per_shell=3
        )
        for theta in (1.5, 2.0, 3.0):
            lemma_K_rows.append(check_lemma_K_hh_mass(f, theta=theta))
    face = face_family_probe(K_max=K_max)
    hh_l = hh_to_low_sanity(rng)

    summary = {
        "attack": "uniform_rstar_hh_push",
        "seed": seed,
        "lemma_K_hh_mass_all_ok": all(r["ok"] for r in lemma_K_rows),
        "lemma_K_n": len(lemma_K_rows),
        "lemma_L_face": {
            "monotone_Q": face["monotone_Q_through_Kmax"],
            "Q_at_Kmax": face["Q_at_Kmax"],
            "Q_over_K2_at_Kmax": face["Q_over_K2_at_Kmax"],
            "cauchy_sufficient_strategically_blocked": face[
                "cauchy_sufficient_strategically_blocked"
            ],
            "Q_unbounded_status": face["Q_unbounded_status"],
        },
        "lemma_M_hh_to_low": {
            "triple_counts": hh_l["triple_counts"],
            "best_R_star": hh_l["best_true_HH_sample"].get("R_star"),
            "kill_triggered": hh_l["kill_triggered"],
        },
        "status": {
            "PRODUCT_BLOCK": "OPEN",
            "uniform_R_star": "OPEN",
            "Lemma_star": "HYPOTHESIS",
            "Clay_Statement_B": "NOT_SOLVED",
            "HH_bound": "OPEN",
            "HL_LL_geometric": "OPEN",
            "cauchy_sufficient_sup_Q_finite": "STRATEGICALLY_BLOCKED_conjecture_unbounded",
            "R_star_kill_lane": "LIVE_no_family_found",
            "numerics_are_proof": False,
            "publisher_X_gate": "CLOSED_until_real_proof",
        },
        "progress_doc": "docs/ns-review/UNIFORM-RSTAR-PROGRESS.md",
        "note": (
            "HH mass lemma K proved. Face family blocks Cauchy-only close. "
            "Geometric HH / PRODUCT-BLOCK still OPEN. No Clay claim."
        ),
    }
    return {
        "summary": summary,
        "lemma_K_rows": lemma_K_rows,
        "face_family": face,
        "hh_to_low": hh_l,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=20260912)
    ap.add_argument("--K-max", type=int, default=10)
    ap.add_argument("--out-dir", type=str, default=str(ARTIFACT_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = run(seed=args.seed, K_max=args.K_max)
    s = payload["summary"]

    (out_dir / "uniform_rstar_hh_push.json").write_text(
        json.dumps(payload, indent=2, default=str)
    )

    L = s["lemma_L_face"]
    M = s["lemma_M_hh_to_low"]
    lines = [
        "uniform_rstar_hh_push — HH mass + Cauchy-route block",
        s["note"],
        f"K hh_mass_ok={s['lemma_K_hh_mass_all_ok']} (n={s['lemma_K_n']})",
        f"L face: monotone_Q={L['monotone_Q']} Q(Kmax)={L['Q_at_Kmax']!r} "
        f"Q/K^2={L['Q_over_K2_at_Kmax']!r} "
        f"cauchy_blocked={L['cauchy_sufficient_strategically_blocked']} "
        f"Q_status={L['Q_unbounded_status']}",
        f"M HH→L: best_R*={M['best_R_star']!r} kill={M['kill_triggered']} "
        f"triples={M['triple_counts']}",
        f"status PRODUCT-BLOCK={s['status']['PRODUCT_BLOCK']} "
        f"HH={s['status']['HH_bound']} "
        f"Cauchy_sup_Q={s['status']['cauchy_sufficient_sup_Q_finite']} "
        f"Clay={s['status']['Clay_Statement_B']} "
        f"publisher_gate={s['status']['publisher_X_gate']}",
    ]
    text = "\n".join(lines) + "\n"
    (out_dir / "uniform_rstar_hh_push.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
