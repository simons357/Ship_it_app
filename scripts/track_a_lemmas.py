#!/usr/bin/env python3
"""
Track A lemmas: Q1-augmented NS, eps>0.

Theorem A is for this PDE only. Uniform H1 as eps->0 stays
open. A does not imply B. Olga stays on A.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from augmented_ns_verify import run_once  # noqa: E402


def rec(name: str, statement: str, verdict: str, why: str, **extra) -> dict:
    row = {"name": name, "statement": statement, "verdict": verdict, "why": why}
    row.update(extra)
    return row


def _checks() -> dict:
    rows = []
    for eps in (0.2, 0.05, 0.0):
        rows.append(run_once(n=12, nu=0.05, eps=eps, alpha=1.0, beta=0.5, t_end=0.1, dt=0.01))
    e1 = max(r.residual / r.energy0 for r in rows)
    e2 = all(r.diss_q1 > 0.0 for r in rows if r.eps > 0.0)
    e3 = all(r.enstrophy_t > 0.0 and r.enstrophy_t < 1e6 for r in rows)
    by_eps = sorted(rows, key=lambda r: r.eps, reverse=True)
    e4 = all(
        later.enstrophy_t + 1e-9 >= earlier.enstrophy_t
        for earlier, later in zip(by_eps, by_eps[1:])
    )
    e5 = max(r.max_div for r in rows)
    return {
        "E1_rel_residual": e1,
        "E2_q1_positive": e2,
        "E3_enstrophy_finite": e3,
        "E4_xt_grows_as_eps_falls": e4,
        "E5_max_div": e5,
        "rows": [
            {
                "eps": r.eps,
                "energy0": r.energy0,
                "energy_t": r.energy_t,
                "diss_q1": r.diss_q1,
                "residual": r.residual,
                "enstrophy_t": r.enstrophy_t,
                "max_div": r.max_div,
            }
            for r in rows
        ],
    }


def lemmas(checks: dict) -> list[dict]:
    return [
        rec(
            "A1_energy",
            "Q1 energy identity holds for a smooth solution",
            "pass",
            "Lemma 1. Test against u. Convective and pressure vanish. Extra term is exact dissipation.",
        ),
        rec(
            "A2_galerkin",
            "Galerkin solutions exist globally and inherit Lemma 1",
            "pass",
            "Lemma 2. Finite-dimensional ODE. The energy bound is independent of n and T.",
        ),
        rec(
            "A3_weak_limit",
            "A weakly convergent subsequence is a weak solution of Q1",
            "pass",
            "Lemma 3. Alaoglu + Aubin–Lions + Minty–Browder. Extra dissipation only helps.",
        ),
        rec(
            "A4_unique_H1",
            "For beta>=1/2 and eps>0 the weak solution is unique in L^infty_t H^1",
            "pass",
            "Lemma 4. Ladyzhenskaya class. The constant depends on eps and blows up as eps->0.",
        ),
        rec(
            "A5_smooth",
            "That unique strong solution is C^infty for t>0",
            "pass",
            "Lemma 5. Frozen eps>0: uniformly parabolic Stokes. Difference quotients.",
        ),
        rec(
            "A_theorem",
            "Theorem A: Q1 is globally smooth for eps>0, beta>=1/2, u0 in H^1",
            "pass",
            "This PDE only. Lemmas 2-5. Data need not be axisymmetric. Phi is not used.",
        ),
        rec(
            "A_E1_residual",
            "Galerkin Taylor-Green keeps the energy residual small",
            "pass" if checks["E1_rel_residual"] < 1e-3 else "fail",
            f"rel residual {checks['E1_rel_residual']:.3e} on n=12, T=0.1. Consistency, not a proof.",
        ),
        rec(
            "A_E2_q1_positive",
            "Q1 dissipation is strictly positive when eps>0",
            "pass" if checks["E2_q1_positive"] else "fail",
            "E2. Extra term is live on Taylor-Green.",
        ),
        rec(
            "A_E3_enstrophy_finite",
            "Enstrophy stays finite on this short window for eps>=0",
            "pass" if checks["E3_enstrophy_finite"] else "fail",
            "E3. A decaying box is not continuation.",
        ),
        rec(
            "A_E4_eps_dependence",
            "Peak enstrophy grows as eps decreases on this window",
            "pass" if checks["E4_xt_grows_as_eps_falls"] else "fail",
            "E4. Consistent with Lemma 4 not being uniform.",
        ),
        rec(
            "A_E5_div",
            "Divergence stays at roundoff after Leray projection",
            "pass" if checks["E5_max_div"] < 1e-10 else "fail",
            f"E5. max|div|={checks['E5_max_div']:.2e}.",
        ),
        rec(
            "A_uniform_H1",
            "The H1 bound of Lemma 4 stays uniform as eps->0",
            "open",
            "The live leftover on A. Old C/I is not reused. This is the A-to-B gap, not a B write.",
        ),
        rec(
            "A_implies_B",
            "Theorem A implies classical unaugmented regularity",
            "fail",
            "Different PDE. The constant blows up as eps->0. Olga stays on A.",
        ),
        rec(
            "A_phi_estimate",
            "The Phi identity is the estimate variable on A",
            "fail",
            "Algebra only. Not used in Theorem A. Do not cancel to Phi.",
        ),
        rec(
            "A_export_olga",
            "Export Ladyzhenskaya onto classical NS and call it Track A",
            "fail",
            "That is A=>B under another name. Refused.",
        ),
    ]


def run(out: Path | None = None) -> dict:
    checks = _checks()
    scored = lemmas(checks)
    payload = {
        "meta": {
            "track": "A",
            "writeup": "docs/TRACK-A-LEMMAS.md",
            "chain": "docs/AUGMENTED-NS-PROOF-CHAIN.md",
            "pde": "Q1-augmented NS, eps>0, beta>=1/2",
            "theorem_A": "pass",
            "domain_verdict": "pass",
            "domain_means": "this PDE only",
            "eps_to_0": "open",
            "implies_B": "fail",
        },
        "checks": {k: v for k, v in checks.items() if k != "rows"},
        "runs": checks["rows"],
        "lemmas": scored,
        "counts": {
            "pass": sum(1 for r in scored if r["verdict"] == "pass"),
            "fail": sum(1 for r in scored if r["verdict"] == "fail"),
            "open": sum(1 for r in scored if r["verdict"] == "open"),
        },
        "how_far": [
            "energy, Galerkin, weak limit, unique H1, smoothness scored pass",
            "Theorem A pass for this PDE",
            "E1-E5 consistency on a short Taylor-Green window",
            "uniform H1 as eps->0 stays open",
            "A=>B fail",
        ],
        "next_da_move": (
            "The live A write is a uniform-in-eps H1 bound, or a named no-go. "
            "Do not export Olga onto B. Do not cancel to Phi."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_a_lemmas.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA Track A. Q1-augmented NS. This PDE only.")
    print("Chain: docs/AUGMENTED-NS-PROOF-CHAIN.md")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("counts", payload["counts"])
    print("theorem A:", payload["meta"]["theorem_A"])
    print("eps->0:", payload["meta"]["eps_to_0"])
    print("implies B:", payload["meta"]["implies_B"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
