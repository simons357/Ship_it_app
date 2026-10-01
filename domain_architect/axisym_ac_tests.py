"""Finite-disk / algebraic tests of candidate routes (A)–(C) and occupancy.

Class: unaugmented axisymmetric-with-swirl (and labeled 3-D disk facts).
Quantity: labeled shell leftovers / diagnostics.
Remainder: T_{j←j}.
Assumed: [small exact disks / restricted classes only; no K_max→∞;
no DNS class close; NS not solved; no invented proofs].

Outcomes are pass / fail / inconclusive for the *diagnostic gate*,
never a class close of (A)–(C) or Clay.
"""

from __future__ import annotations

from typing import Any

from .axisymmetric_shell import (
    COMPACT_SWIRL_SAMPLES,
    MIXED_SPLIT_SAMPLES,
    THREE_D_FACTS,
    TWO_D_FACTS,
)

# Filed from Jonathan's unaugmented proof-chain text (11–12 Sept 2026).
# Not invented here. Not theorems for the class.
ROUTE_A = (
    "bound |T_{j←j}| <= ε ν P_j + R(X,Z) with R controlled by energy "
    "and known quantities (palinstrophy-normalized; ε<1 for absorption)"
)
ROUTE_B = (
    "depletion: a factor sinφ or (1-α) from vorticity-direction mismatch "
    "on HHH that makes (A) true; occupancy 1 alone does not supply this"
)
ROUTE_C = (
    "restriction of the data (axisymmetry-with-swirl, etc.); "
    "a different theorem path, not a generic 3-D close"
)


def condition_a_gate(
    abs_tjj: float,
    palinstrophy_p: float,
    nu: float,
    eps: float,
    r_term: float,
) -> dict[str, Any]:
    """Check the algebraic form of (A) on supplied numbers.

    Does not measure class palinstrophy. Inconclusive for the class
    whenever P_j is not a class print.
    """
    rhs = float(eps) * float(nu) * float(palinstrophy_p) + float(r_term)
    lhs = abs(float(abs_tjj))
    holds = lhs <= rhs + 1e-15
    return {
        "condition": "A",
        "form": ROUTE_A,
        "lhs_|Tjj|": lhs,
        "rhs": rhs,
        "eps": float(eps),
        "nu": float(nu),
        "P_j": float(palinstrophy_p),
        "R": float(r_term),
        "holds_on_supplied_numbers": holds,
        "class_verdict": "inconclusive",
        "why": (
            "gate is algebraic only; class P_j / Tjj are NOT COMPUTED "
            "as continuum prints in this environment"
        ),
        "is_energy_budget_absorption": False,
    }


def condition_a_on_recorded_samples(nu: float = 0.03, eps: float = 0.5) -> dict[str, Any]:
    """Try (A) using compact-sample |Tjj/Xj| as if it were |Tjj|/P_j — refused.

    Energy-shell ratios are not palinstrophy-normalized ρ_j. Report
    inconclusive / hygiene fail for that substitution.
    """
    ratio = float(COMPACT_SWIRL_SAMPLES["mixed_m1_n32_max_|Tjj/Xj|"])
    # Wrong normalization on purpose: demonstrates the hygiene refusal.
    fake = condition_a_gate(
        abs_tjj=ratio,
        palinstrophy_p=1.0,  # pretending X_j = P_j
        nu=nu,
        eps=eps,
        r_term=0.0,
    )
    return {
        "condition": "A",
        "class_verdict": "inconclusive",
        "diagnostic_verdict": "fail_hygiene",
        "why": (
            "compact-sample |Tjj/Xj| is not palinstrophy-normalized ρ_j; "
            "substituting X_j for P_j is refused as an (A) test"
        ),
        "recorded_mixed_m1_n32_max_|Tjj/Xj|": ratio,
        "fake_gate_if_X_were_P": fake["holds_on_supplied_numbers"],
        "is_energy_budget_absorption": False,
        "kmax_to_infinity": False,
    }


def condition_b_occupancy_alignment(
    occupancy: float | None = None,
    alpha: float | None = None,
) -> dict[str, Any]:
    """(B) depletion candidate: occupancy 1 + α≈1/2 does not establish (A)."""
    occ = (
        float(THREE_D_FACTS["HHH_occupancy_on_orbits_run"])
        if occupancy is None
        else float(occupancy)
    )
    alp = (
        float(THREE_D_FACTS["alignment_alpha"])
        if alpha is None
        else float(alpha)
    )
    depletion_factor = max(0.0, 1.0 - abs(alp))
    # Depletion that would make (A) needs a small stretch factor.
    # α≈1/2 ⇒ factor≈1/2, not near 0; occupancy 1 is phase lock, not geometry.
    establishes_depletion = False
    return {
        "condition": "B",
        "form": ROUTE_B,
        "occupancy": occ,
        "alignment_alpha": alp,
        "depletion_factor_1_minus_|alpha|": depletion_factor,
        "occupancy_is_one": abs(occ - 1.0) <= 1e-12,
        "establishes_depletion": establishes_depletion,
        "establishes_A": False,
        "class_verdict": "fail",
        "diagnostic_verdict": "fail",
        "why": (
            "recorded HHH occupancy 1 with alignment ≈1/2 does not establish "
            "the depletion required for (A); phase lock ≠ geometric depletion"
        ),
        "scope": "small exact disks / orbits that were run; no K_max→∞",
    }


def condition_c_axisymmetric_restriction() -> dict[str, Any]:
    """(C) data restriction: axisymmetric-with-swirl samples only."""
    pure = float(COMPACT_SWIRL_SAMPLES["pure_swirl_n32_max_|Tjj/Xj|"])
    mixed = float(COMPACT_SWIRL_SAMPLES["mixed_m1_n32_max_|Tjj/Xj|"])
    pure_near_zero = pure < 1e-15
    mixed_bulk_mm = bool(MIXED_SPLIT_SAMPLES["T_mm_is_the_bulk"])
    return {
        "condition": "C",
        "form": ROUTE_C,
        "pure_swirl_n32_max_|Tjj/Xj|": pure,
        "mixed_m1_n32_max_|Tjj/Xj|": mixed,
        "pure_swirl_near_zero": pure_near_zero,
        "mixed_T_mm_is_bulk": mixed_bulk_mm,
        "class_verdict": "inconclusive",
        "diagnostic_verdict": "pass_on_named_pure_swirl_only",
        "why": (
            "pure-swirl compact samples print ~0 (geometry removes free HHH "
            "as a class statement on those fields); mixed samples sit at "
            "O(10^{-3}) with T_mm bulk — not a class close of regularity"
        ),
        "closes_generic_3d": False,
        "closes_Tjj_for_class": False,
        "kmax_to_infinity": False,
    }


def occupancy_implication_table() -> dict[str, Any]:
    """What occupancy=1 + alignment≈1/2 does and does not imply."""
    b = condition_b_occupancy_alignment()
    return {
        "inputs": {
            "2d_occupancy_recorded": TWO_D_FACTS["occupancy"],
            "3d_HHH_occupancy_on_orbits_run": THREE_D_FACTS[
                "HHH_occupancy_on_orbits_run"
            ],
            "3d_alignment_alpha": THREE_D_FACTS["alignment_alpha"],
        },
        "implies": [
            "phase lock on the HHH orbits that were run (occupancy 1)",
            "Door-3 alignment criterion printed ≈1/2 on those orbits",
        ],
        "does_not_imply": [
            "Constantin–Fefferman geometric depletion",
            "condition (A)",
            "condition (B) as a proved factor making (A) true",
            "class T_{j←j}/Z_j small",
            "uniform conclusion as K_max→∞",
            "CFM close",
        ],
        "depletion_factor_1_minus_|alpha|": b["depletion_factor_1_minus_|alpha|"],
        "establishes_depletion": False,
        "class_verdict": "negative_for_depletion_close",
    }


def conditional_gronwall_under_A(
    *,
    eps: float,
    nu: float,
    c_shell: float,
    j: int,
    z0: float,
    r_integrable_bound: float,
    t: float,
) -> dict[str, Any]:
    """Formally correct *conditional* Gronwall template under (A).

    Hypotheses (explicit):
      [A_eps] |Tjj| <= ε ν P_j + R with 0 <= ε < 1 and R controlled
      [Poincaré-shell] P_j >= c_shell * 4^j * Z_j  (one ν in the viscous slot)
      [far] IR/UV remainders absorbed into an integrable majorant M(t)
      [no-cycle] Tjj is not bounded by ė_j, Ż, or Λ'

    Then d/dt Z + α Z <= 2 M(t) with α = 2 ν (1-ε) c_shell 4^j
    (single power of ν — not ν²).

    This does not seat (A). Cross-scale summability remains a gap.
    """
    if not (0.0 <= float(eps) < 1.0):
        return {
            "status": "refused",
            "why": "need 0 <= ε < 1 for absorption; otherwise no conditional Gronwall",
            "claimed": False,
        }
    alpha = 2.0 * float(nu) * (1.0 - float(eps)) * float(c_shell) * (4.0 ** int(j))
    # Bound: Z(t) <= Z0 e^{-α t} + (2 M_bar / α) (1 - e^{-α t}) if M <= M_bar.
    import math

    m_bar = float(r_integrable_bound)
    z0 = float(z0)
    t = float(t)
    if alpha <= 0.0:
        return {"status": "refused", "why": "α must be positive", "claimed": False}
    decay = math.exp(-alpha * t)
    z_bound = z0 * decay + (2.0 * m_bar / alpha) * (1.0 - decay)
    return {
        "status": "conditional_template",
        "claimed": False,
        "hypotheses": [
            "[A_eps] |Tjj| <= ε ν P_j + R, 0<=ε<1",
            "[Poincaré-shell] P_j >= c 4^j Z_j",
            "[far] IR/UV in integrable majorant M(t) — NOT established by this note",
            "[no-cycle] no bound of Tjj by e_dot_j, Z_dot, or Lambda'",
        ],
        "alpha": alpha,
        "nu_power_in_alpha": 1,
        "refuses_nu_squared_rate": True,
        "eps": float(eps),
        "nu": float(nu),
        "j": int(j),
        "Z_bound_under_hypotheses": z_bound,
        "gap": (
            "(A) not seated for the class; cross-scale summability not established; "
            "requested local Young REFUSED"
        ),
    }


def run_ac_occupancy_battery() -> dict[str, Any]:
    """One-shot honest battery. No class close."""
    a_sym = condition_a_gate(
        abs_tjj=0.01,
        palinstrophy_p=1.0,
        nu=0.03,
        eps=0.5,
        r_term=0.0,
    )
    # 0.01 <= 0.5*0.03*1 = 0.015 → holds on toy numbers
    a_rec = condition_a_on_recorded_samples()
    b = condition_b_occupancy_alignment()
    c = condition_c_axisymmetric_restriction()
    occ = occupancy_implication_table()
    gr = conditional_gronwall_under_A(
        eps=0.5,
        nu=0.03,
        c_shell=1.0,
        j=2,
        z0=1.0,
        r_integrable_bound=0.1,
        t=1.0,
    )
    return {
        "honesty": {
            "NS_solved": False,
            "clay": "NOT CLAIMED",
            "proofs_invented": False,
            "principal_unresolved": "T_{j←j}",
            "routes_are_theorems": False,
        },
        "routes": {"A": ROUTE_A, "B": ROUTE_B, "C": ROUTE_C},
        "A_toy_numbers": a_sym,
        "A_recorded_samples": a_rec,
        "B_occupancy_alignment": b,
        "C_axisymmetric_restriction": c,
        "occupancy_implications": occ,
        "conditional_gronwall_under_A": gr,
        "summary": {
            "A": "inconclusive (class); toy gate can hold; recorded X-ratio hygiene fail",
            "B": "fail as depletion⇒(A) on recorded occupancy 1 + α≈1/2",
            "C": "inconclusive for class close; pass only on named pure-swirl samples",
            "Gronwall": "conditional template repaired (ν^1); (A)/far still gaps",
        },
    }


def main() -> None:
    import json

    print(json.dumps(run_ac_occupancy_battery(), indent=2))


if __name__ == "__main__":
    main()
