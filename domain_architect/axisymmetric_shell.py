"""Axisymmetric-with-swirl shell estimate as a DA cycle.

Class: unaugmented axisymmetric Navier–Stokes with swirl.
Quantity: dyadic shell block Z_j = (1/2)||P_j u||_L2^2.
Remainder: Door-1 intra-shell transfer T_{j←j}.
Assumed: hypotheses in brackets; pairing closed only at 1e-16 residual.

This is not a close. Clay is NOT CLAIMED. DA-VC-01 stays FAIL.
Leftover-split strain is a different remainder. Analog 15% intensity
is a different lumped setpoint. Turbulence-reduction is PARK.
This environment has no DNS and no closed NS stepper, so
class T_{j←j}/Z_j is NOT COMPUTED. Compact-sample ratios
from origin/cursor/tjj-estimate-chain-e5c5 are labeled
samples, not a class close. Requested local Young is REFUSED.
"""

from __future__ import annotations

from typing import Any

from .cycle import CycleReport
from .decompose import decompose
from .lab_cases import (
    SHELL_REMAINDER_LAB,
    SWIRL_LEFTOVER_LAB,
)
from .schema import CorrespondenceKind, ValidationGate
from .synthesize import CandidateArchitecture, Provenance
from .translate import translate_expressions


PAIRING_RESIDUAL_TOL = 1e-16

# KEEP facts. Labeled by the class that produced them. Not imported.
TWO_D_FACTS = {
    "class": "2-D",
    "adversary_|Tc|/Ds": 0.017,
    "occupancy": 0.15,
    "imported_to_3d": False,
}
THREE_D_FACTS = {
    "class": "3-D",
    "random_phase_ratio": "O(1e-2)",
    "HHH_occupancy_on_orbits_run": 1.0,
    "alignment_alpha": 0.5,
    "occupancy_imported_to_cfm": False,
    "occupancy_alpha_is_depletion": False,
}

ENERGY_SHELL = "Z_j = (1/2)||P_j u||_L2^2 (P_j = LP projector)"
ENSTROPHY_SHELL = "Z_j = ||Δ_j ω||_L2^2"
PALINSTROPHY = "P_j palinstrophy, not the LP projector"

STANDING_LANGUAGE = {
    "spectral_shift_identity": (
        "bookkeeping; distinct from Lemma-star ratio bound; "
        "does not control nonlinear transfer"
    ),
    "rho_j_lt_nu": (
        "enstrophy-palinstrophy (A) only; not absorption on the "
        "displayed energy budget"
    ),
    "cross_scale": (
        "precise bounds and summability remain to be supplied; "
        "not established by this note"
    ),
    "routes_A_B_C": "candidate routes, not theorems",
    "step_6": (
        "proposed mechanism, needs (A), not claimed; "
        "or a depletion estimate implying (A); "
        "no e_dot_j, Z_dot, or Lambda'; "
        "not WRITE (6); not Q6; not SND leftover 7-8"
    ),
    "principal_unresolved": "T_{j←j}",
    "scope": (
        "small exact disks and stated restricted classes; "
        "no K_max→∞; no generic data"
    ),
    "occupancy_alpha_is_depletion": False,
    "identity_is_lemma_star": False,
    "rho_j_lt_nu_is_energy_absorption": False,
}

# Sept 11 Tjj chain. Labeled compact samples, not DNS, not a class ρ_j.
TJJ_CHAIN_SOURCE = "origin/cursor/tjj-estimate-chain-e5c5"
REFUSED_YOUNG = {
    "line": "|T_{j←j}| <= εν D_j + R",
    "status": "REFUSED",
    "allowed_R": "energy, Z, maybe a direction factor; not dZj; not Lambda'",
    "reason": (
        "allowed R is not seated; energy-linear R is false by "
        "λ^{3/2} concentration"
    ),
}
COMPACT_SWIRL_SAMPLES = {
    "class": "compact axisymmetric-with-swirl blobs on R^3, R=2.4<π",
    "kind": "named compact samples, not DNS, not a class bound",
    "re_run_here": False,
    "imported_to_3d_cfm": False,
    "imported_from_2d": False,
    "kmax_to_infinity": False,
    "generic_data": False,
    "pure_swirl_n32_max_|Tjj/Xj|": 3.2e-19,
    "mixed_m1_n32_max_|Tjj/Xj|": 0.00112,
    "mixed_m3_n32_max_|Tjj/Xj|": 0.00141,
    "mixed_m1_n48_max_|Tjj/Xj|": 0.000583,
    "mixed_moved_with_n": True,
}
MIXED_SPLIT_SAMPLES = {
    "class": "compact swirl+meridional, n=24, energy-carrying shells",
    "kind": "named compact samples, not DNS; rounded print",
    "T_mm_is_the_bulk": True,
    "centrifugal_only_leftover": False,
    "shells": (
        {"j": 1, "T_mm": 8.15e3, "T_ss": -62.0, "T_cross": 217.0, "Tjj": 8.30e3},
        {"j": 2, "T_mm": -1.08e4, "T_ss": 4.03e3, "T_cross": -142.0, "Tjj": -6.89e3},
        {"j": 3, "T_mm": -1.32e4, "T_ss": 622.0, "T_cross": 88.0, "Tjj": -1.25e4},
    ),
}

DISCARD_CLAIM_PHRASES = (
    "clay is solved",
    "unconditional 3-d regularity",
    "unconditional 3d regularity",
    "gcd spectral attractor",
    "e8 cathedral",
    "prime-harmonic lock",
    "borromean coherence",
    "base 44",
    "gematria",
    "q6-kabbalah",
    "lightning flash",
    "coherence-floor",
    "tao certification",
    "tao-positive",
    "depletion established",
    "lemma-star close",
    "lemma★ close",
)

# Claim-shaped strings. A hit in identity / diagnostic text is a fail.
CLAIM_TRIPWIRE = (
    "we close",
    "clay is solved",
    "small leftover",
    "t_{j←j} is o(",
    "t_{j\\leftarrow j} is o(",
    "millennium",
    "certified",
    "tao-positive",
    "tao certification",
    "depletion established",
)

REFUSED = (
    "no Clay / unconditional 3-D regularity claim",
    "no bound of Tjj by Lambda' or dZj",
    "no large-form [SND] as measured smallness",
    "no import of 2-D rho=0.02 into 3-D",
    "no import of occupancy 1 into CFM",
    "no identifying Tjj with leftover-split strain",
    "no TRANSFORMABLE without a real T",
    "no quote of sign(Lambda') unless pairing residual <= 1e-16 "
    "and a closed time series exists",
    "no seating of |Tjj| <= εν Dj + R with energy-linear R",
    "no treating compact-sample ratios as class rho_j",
    "no treating spectral-shift identity as Lemma-star or transfer control",
    "no treating rho_j<nu as energy-budget absorption",
    "no treating occupancy 1 with alpha~1/2 as depletion",
    "no using e_dot_j, Z_dot, or Lambda' in Step 6 to bound Tjj",
    "no identifying Tjj with estimate Step 6, WRITE (6), Q6, or SND leftover 7-8",
)

FIRST_SENTENCE = (
    "Class: unaugmented axisymmetric Navier-Stokes with swirl. "
    "Quantity: dyadic shell block Z_j = (1/2)||P_j u||_L2^2. "
    "Remainder after Door-1: T_{j←j}. Assumed in brackets: "
    "[smooth compactly supported divergence-free "
    "axisymmetric-with-swirl classical NS; no added field; "
    "pairing closed only at 1e-16 residual]."
)

IDENTITY = {
    "quantity": "Z_j = (1/2) ||P_j u||_{L^2}^2",
    "pairing": (
        "dot Z_j = -<P_j(u·∇u), P_j u> - ν ||∇ P_j u||_{L^2}^2"
    ),
    "piece": "T_{j←ℓm} = -<P_j((P_ℓ u)·∇(P_m u)), P_j u>",
    "dissipation": "D_j = ||∇ P_j u||_{L^2}^2",
    "locality_width_b": (
        "named grouping cutoff, not a smallness; no numerical "
        "value is used to bound T_{j←j}"
    ),
    "intra_shell": "T_{j←j} = sum_{|ℓ-j|<=b, |m-j|<=b} T_{j←ℓm}",
    "cross_shell": "T_{j←≠j} = sum of the remaining pieces",
    "door_1": "dot Z_j = T_{j←≠j} + T_{j←j} - ν D_j",
    "growing_term": "T_{j←j}",
    "only_remainder": "T_{j←j}",
    "not_bounded_by": ["dot Z_j", "Lambda'", "a new symbol of the same size"],
}

GALERKIN_PAIRING = {
    "first_sentence": (
        "Class: one closed Fourier triad of a divergence-free periodic "
        "velocity. Quantity: S = Jp+Jq+Jr. Remainder of this proposition: "
        "none (S=0). Assumed: [incompressible triad pairing; no added field]."
    ),
    "identity": "Jp + Jq + Jr = 0",
    "constants": {
        "tolerance": PAIRING_RESIDUAL_TOL,
        "other": "none",
    },
    "scope": (
        "listed triad only; not the continuum shell; not a time series; "
        "does not bound T_{j←j}"
    ),
}


def pairing_residual(jp: float, jq: float, jr: float) -> float:
    """Energy conservation of the closed-triad pairing: Jp + Jq + Jr = 0."""
    return abs(float(jp) + float(jq) + float(jr))


def pairing_closed(jp: float, jq: float, jr: float) -> bool:
    return pairing_residual(jp, jq, jr) <= PAIRING_RESIDUAL_TOL


def closed_triad_rewrite(
    omega_p: float,
    omega_q: float,
    omega_r: float,
    jp: float,
    jq: float,
) -> float:
    """τ = (ω(p)−ω(r)) Jp + (ω(q)−ω(r)) Jq. Lattice shift is ω_*, not Λ."""
    return (omega_p - omega_r) * jp + (omega_q - omega_r) * jq


def lambda_prime_bookkeeping(tc: float, nu: float, ds: float, x: float) -> float | None:
    """Λ' = 2(Tc − ν Ds)/X is bookkeeping, not the final left-hand side."""
    if x == 0.0:
        return None
    return 2.0 * (tc - nu * ds) / x


def contains_discard_claim(text: str) -> bool:
    lowered = (text or "").lower()
    return any(phrase in lowered for phrase in DISCARD_CLAIM_PHRASES)


def swirl_split_residual(t_mm: float, t_ss: float, t_cross: float, tjj: float) -> float:
    """Bilinear split identity: T_mm + T_ss + T_cross = Tjj."""
    return abs(float(t_mm) + float(t_ss) + float(t_cross) - float(tjj))


def claim_tripwire_hits(text: str) -> list[str]:
    """Return claim-shaped substrings. Empty means the tripwire is clean."""
    lowered = (text or "").lower()
    return [phrase for phrase in CLAIM_TRIPWIRE if phrase in lowered]


def axisymmetric_shell_estimate(
    *,
    jp: float = 0.25,
    jq: float = -0.10,
    jr: float | None = None,
    omega_p: float = 3.0,
    omega_q: float = 1.0,
    omega_r: float = 0.0,
    omega_star: float = 1.0,
    tc: float = 0.0,
    nu: float = 1.0,
    ds: float = 1.0,
    x: float = 1.0,
    time_series_closed: bool = False,
) -> dict[str, Any]:
    """Honest Door-1 representation. Status OPEN. Clay NOT CLAIMED."""
    if jr is None:
        jr = -jp - jq
    residual = pairing_residual(jp, jq, jr)
    closed = residual <= PAIRING_RESIDUAL_TOL
    tau = closed_triad_rewrite(
        omega_p - omega_star,
        omega_q - omega_star,
        omega_r - omega_star,
        jp,
        jq,
    )
    # No closed time series in this environment. Do not emit a Λ' value
    # that could be read as a quoted sign.
    quote_sign = bool(closed and time_series_closed)
    lam = (
        lambda_prime_bookkeeping(tc, nu, ds, x)
        if quote_sign
        else None
    )
    if not closed:
        book_reason = "pairing residual exceeds 1e-16; do not quote sign(Lambda')"
    elif not time_series_closed:
        book_reason = (
            "no closed time series (no DNS / no closed stepper); "
            "do not quote sign(Lambda')"
        )
    else:
        book_reason = None
    growing_term = "T_{j←j} is the one term that can grow Z_j"
    return {
        "protocol": "axisymmetric-shell",
        "filter": "docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md",
        "estimate": "docs/papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md",
        "first_sentence": FIRST_SENTENCE,
        "class": "axisymmetric-with-swirl",
        "quantity": "Z_j",
        "remainder": "T_{j←j}",
        "growing_term": growing_term,
        "status": "OPEN",
        "clay": "NOT CLAIMED",
        "unconditional_3d_regularity": "NOT CLAIMED",
        "da_vc_01": "FAIL",
        "lab": SHELL_REMAINDER_LAB,
        "assumptions": [
            "[axisymmetric with swirl]",
            "[unaugmented classical NS]",
            "[no added field]",
            "[pairing closed only if residual <= 1e-16]",
            "[no DNS / no closed stepper in this environment]",
        ],
        "identity": dict(IDENTITY),
        "shells_labeled": {
            "energy": ENERGY_SHELL,
            "enstrophy": ENSTROPHY_SHELL,
            "palinstrophy": PALINSTROPHY,
            "glued": False,
        },
        "standing_language": dict(STANDING_LANGUAGE),
        "bookkeeping": {
            "Lambda_prime": "2(Tc - ν Ds)/X",
            "is_final_lhs": False,
            "value": lam,
            "sign_quoted": False,
            "time_series_closed": time_series_closed,
            "reason": book_reason,
        },
        "closed_triad": {
            "name": "spectral-shift identity",
            "rewrite": "tau = (ω(p)-ω(r)) Jp + (ω(q)-ω(r)) Jq",
            "shift": "ω_* lattice constant, not Lambda",
            "is_lemma_star": False,
            "controls_nonlinear_transfer": False,
            "omega_star": omega_star,
            "tau": tau,
            "Jp": jp,
            "Jq": jq,
            "Jr": jr,
        },
        "pairing": {
            "residual": residual,
            "tolerance": PAIRING_RESIDUAL_TOL,
            "closed": closed,
            "check": "Jp + Jq + Jr = 0",
        },
        "galerkin_pairing": dict(GALERKIN_PAIRING),
        "door_3": {
            "alignment_alpha": "criterion to test",
            "separate_from": "triad-phase occupancy",
        },
        "measured_facts": {
            "2d": dict(TWO_D_FACTS),
            "3d": dict(THREE_D_FACTS),
            "swirl_removes_free_helical_HHH": (
                "class statement, not a measured 3-D CFM close"
            ),
            "tjj_chain_source": TJJ_CHAIN_SOURCE,
            "compact_swirl_samples": dict(COMPACT_SWIRL_SAMPLES),
            "mixed_split_samples": {
                "class": MIXED_SPLIT_SAMPLES["class"],
                "kind": MIXED_SPLIT_SAMPLES["kind"],
                "T_mm_is_the_bulk": MIXED_SPLIT_SAMPLES["T_mm_is_the_bulk"],
                "centrifugal_only_leftover": MIXED_SPLIT_SAMPLES[
                    "centrifugal_only_leftover"
                ],
                "shells": [dict(row) for row in MIXED_SPLIT_SAMPLES["shells"]],
            },
        },
        "refused_young": dict(REFUSED_YOUNG),
        "tjj_over_zj": {
            "status": "NOT COMPUTED",
            "reason": (
                "no DNS and no closed NS time-series stepper in this environment; "
                "compact-sample ratios are not a class rho_j"
            ),
            "class": "axisymmetric-with-swirl",
        },
        "not_the_same_as": [
            "leftover-split strain Istrain = urad/r",
            "Ring inf J/X >= cstar",
            "Paper2 ell1(a - mu)",
            "analog 15% turbulence intensity",
            "turbulence-reduction ship envelope",
        ],
        "refused": list(REFUSED),
        "validation_gate": ValidationGate.MATHEMATICAL.value,
        "kind": CorrespondenceKind.ANALOGY.value,
    }


def shell_diagnostic(
    *,
    jp: float = 0.25,
    jq: float = -0.10,
    jr: float | None = None,
) -> dict[str, Any]:
    """Smallest honest print: pairing residual, labeled facts, Tjj/Zj open.

    Class: unaugmented axisymmetric-with-swirl, algebraic pairing only.
    Quantity: Z_j. Remainder: T_{j←j}. Assumed: no DNS, no closed stepper.
    """
    payload = axisymmetric_shell_estimate(jp=jp, jq=jq, jr=jr)
    broken = pairing_residual(1.0, 1.0, 1.0)
    return {
        "first_sentence": (
            "Class: unaugmented axisymmetric-with-swirl (algebraic pairing "
            "check only). Quantity: Z_j. Remainder: T_{j←j}. Assumed: "
            "[no DNS; no closed NS stepper; recorded facts stay in class]."
        ),
        "class": payload["class"],
        "quantity": payload["identity"]["quantity"],
        "remainder": "T_{j←j}",
        "remainder_status": "OPEN",
        "identity": payload["identity"]["door_1"],
        "growing_term": payload["identity"]["growing_term"],
        "pairing": {
            "closed_triad_Jp": payload["closed_triad"]["Jp"],
            "closed_triad_Jq": payload["closed_triad"]["Jq"],
            "closed_triad_Jr": payload["closed_triad"]["Jr"],
            "closed_triad_residual": payload["pairing"]["residual"],
            "closed_triad_closed": payload["pairing"]["closed"],
            "broken_triad": (1.0, 1.0, 1.0),
            "broken_triad_residual": broken,
            "broken_triad_closed": broken <= PAIRING_RESIDUAL_TOL,
            "tolerance": PAIRING_RESIDUAL_TOL,
            "gate": "residual <= 1e-16 to call the algebraic pairing identity closed",
        },
        "time_series": {
            "closed": False,
            "reason": "no DNS and no closed NS stepper; stepper and diagnostic cannot be compared",
        },
        "lambda_prime_sign": "NOT QUOTED",
        "tjj_over_zj": dict(payload["tjj_over_zj"]),
        "recorded_2d": {
            "class": "2-D",
            "|Tc|/Ds": TWO_D_FACTS["adversary_|Tc|/Ds"],
            "occupancy": TWO_D_FACTS["occupancy"],
            "imported_to_3d": False,
            "re_run_here": False,
        },
        "recorded_3d": {
            "class": "3-D",
            "random_phase_ratio": THREE_D_FACTS["random_phase_ratio"],
            "HHH_occupancy_on_orbits_run": THREE_D_FACTS["HHH_occupancy_on_orbits_run"],
            "alignment_alpha": THREE_D_FACTS["alignment_alpha"],
            "occupancy_imported_to_cfm": False,
            "re_run_here": False,
        },
        "door_3": dict(payload["door_3"]),
        "standing_language": dict(STANDING_LANGUAGE),
        "shells_labeled": {
            "energy": ENERGY_SHELL,
            "enstrophy": ENSTROPHY_SHELL,
            "palinstrophy": PALINSTROPHY,
            "glued": False,
        },
        "swirl_removes_free_helical_HHH": (
            "class statement, not a measured 3-D CFM close"
        ),
        "galerkin_pairing": dict(GALERKIN_PAIRING),
        "refused_young": dict(REFUSED_YOUNG),
        "compact_swirl_samples": dict(COMPACT_SWIRL_SAMPLES),
        "mixed_split_samples": {
            "class": MIXED_SPLIT_SAMPLES["class"],
            "kind": MIXED_SPLIT_SAMPLES["kind"],
            "T_mm_is_the_bulk": MIXED_SPLIT_SAMPLES["T_mm_is_the_bulk"],
            "centrifugal_only_leftover": False,
        },
        "status": "OPEN",
        "clay": "NOT CLAIMED",
        "da_vc_01": "FAIL",
        "environment": "no DNS, no closed NS time-series stepper",
    }


def format_shell_diagnostic(diag: dict[str, Any] | None = None) -> str:
    """Plain-text print of the residual, labeled facts, and open leftover."""
    d = diag if diag is not None else shell_diagnostic()
    pairing = d["pairing"]
    two = d["recorded_2d"]
    three = d["recorded_3d"]
    tjj = d["tjj_over_zj"]
    lines = [
        d["first_sentence"],
        f"identity: {d['identity']}",
        f"growing term: {d['growing_term']}",
        (
            "pairing residual |Jp+Jq+Jr| "
            f"(Jp={pairing['closed_triad_Jp']}, "
            f"Jq={pairing['closed_triad_Jq']}, "
            f"Jr={pairing['closed_triad_Jr']}) "
            f"= {pairing['closed_triad_residual']:.3e}  "
            f"closed={pairing['closed_triad_closed']}  "
            f"gate={pairing['tolerance']:.0e}"
        ),
        (
            "pairing residual broken triad (1,1,1) "
            f"= {pairing['broken_triad_residual']:.3e}  "
            f"closed={pairing['broken_triad_closed']}  "
            "(gate: identity is NOT closed)"
        ),
        (
            f"2-D recorded (stay 2-D, not re-run): "
            f"|Tc|/Ds ~ {two['|Tc|/Ds']}; occupancy ~ {two['occupancy']}"
        ),
        (
            f"3-D recorded (stay 3-D, not re-run): "
            f"random-phase {three['random_phase_ratio']}; "
            f"HHH occupancy {three['HHH_occupancy_on_orbits_run']} "
            f"on orbits run; alignment alpha ~ {three['alignment_alpha']}"
        ),
        (
            "Door 3 alignment alpha: criterion to test, "
            "separate from occupancy"
        ),
        f"swirl removes free helical HHH: {d['swirl_removes_free_helical_HHH']}",
        (
            "spectral-shift identity: bookkeeping; not Lemma-star; "
            "does not control nonlinear transfer"
        ),
        (
            "rho_j<nu: enstrophy-palinstrophy (A) only; "
            "not energy-budget absorption"
        ),
        (
            "occupancy 1 with alpha~1/2: does not establish depletion"
        ),
        (
            "routes (A)-(C): candidate routes, not theorems; "
            "estimate Step 6: proposed mechanism, needs (A), not claimed; "
            "not WRITE (6); not Q6; remainder still T_{j←j}"
        ),
        (
            "scope: small exact disks / restricted classes; "
            "no K_max→∞; no generic data"
        ),
        (
            f"energy shell: {d['shells_labeled']['energy']}; "
            f"enstrophy shell: {d['shells_labeled']['enstrophy']}; "
            "not glued"
        ),
        (
            f"requested local Young {d['refused_young']['line']}: "
            f"{d['refused_young']['status']} "
            f"({d['refused_young']['reason']})"
        ),
        (
            "compact samples (not DNS, not class rho_j): "
            f"pure swirl n=32 max|Tjj/Xj| ~ "
            f"{d['compact_swirl_samples']['pure_swirl_n32_max_|Tjj/Xj|']:.1e}; "
            f"mixed m=1 n=32 ~ "
            f"{d['compact_swirl_samples']['mixed_m1_n32_max_|Tjj/Xj|']}; "
            f"mixed m=3 n=32 ~ "
            f"{d['compact_swirl_samples']['mixed_m3_n32_max_|Tjj/Xj|']}; "
            "moved with n"
        ),
        (
            "mixed split n=24: T_mm is the bulk; "
            "centrifugal-only leftover is false"
        ),
        f"sign(Lambda'): {d['lambda_prime_sign']}",
        (
            f"T_{{j←j}}/Z_j: {tjj['status']} "
            f"({tjj['reason']})"
        ),
        f"remainder T_{{j←j}}: {d['remainder_status']}",
        f"clay: {d['clay']}",
        f"DA-VC-01: {d['da_vc_01']}",
        f"environment: {d['environment']}",
    ]
    return "\n".join(lines) + "\n"


def cycle_axisymmetric_shell() -> CycleReport:
    payload = axisymmetric_shell_estimate()
    diagnostic = shell_diagnostic()
    leftover_vs_shell = translate_expressions(SWIRL_LEFTOVER_LAB, SHELL_REMAINDER_LAB)
    dec = decompose(SHELL_REMAINDER_LAB, name="shell_remainder")
    candidate = CandidateArchitecture(
        name="axisymmetric_shell_open",
        components=[
            "Door-1 shell budget (cross-shell flux moved)",
            "remainder T_{j←j} (OPEN; Tjj/Zj NOT COMPUTED)",
            "pairing residual check 1e-16",
        ],
        replaced={},
        hypothesis=(
            payload["first_sentence"]
            + " Status OPEN. Clay NOT CLAIMED. This is not leftover-split "
            "strain and not a turbulence-reduction envelope."
        ),
        provenance=[
            Provenance(
                source="axisymmetric-shell audit filter",
                original_domain="axisymmetric-ns",
                functional_role="constraint",
                translation=None,
                assumptions=list(payload["assumptions"]),
                compatibility_checks=["pairing residual", "glue refused"],
                modifications=[],
                evidence=["T_{j←j}", payload["status"], "Tjj/Zj NOT COMPUTED"],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Not TRANSFORMABLE. Not Clay.",
            "Do not quote sign(Lambda') unless pairing.closed and a time series is closed.",
        ],
    )
    payload_out = dict(payload)
    payload_out["diagnostic"] = diagnostic
    return CycleReport(
        mode="axisymmetric-shell",
        target=(
            "write the Door-1 identity; print the pairing residual; "
            "leave remainder T_{j←j} OPEN"
        ),
        constraints=[
            "do not prove NS",
            "do not import 2-D rho into 3-D",
            "do not glue strain leftover to Tjj",
            "no Clay claim",
        ],
        decomposition=dec,
        translation=leftover_vs_shell,
        candidate=candidate,
        prediction=payload_out,
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            payload["first_sentence"],
            f"status={payload['status']} clay={payload['clay']}",
            f"pairing_closed={payload['pairing']['closed']}",
            f"tjj_over_zj={payload['tjj_over_zj']['status']}",
            "Filter: docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md",
        ],
        method_credits=["axisymmetric-shell audit filter", "Door-1 shell budget"],
    )


if __name__ == "__main__":
    print(format_shell_diagnostic(), end="")
