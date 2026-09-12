"""Axisymmetric-with-swirl shell estimate as a DA cycle.

Class: unaugmented axisymmetric Navier–Stokes with swirl.
Quantity: dyadic shell block Z_j.
Remainder: Door-1 intra-shell transfer T_{j←j}.
Assumed: hypotheses in brackets; pairing closed only at 1e-16 residual.

This is not a close. Clay is NOT CLAIMED. DA-VC-01 stays FAIL.
Leftover-split strain is a different remainder. Analog 15% intensity
is a different lumped setpoint. Turbulence-reduction is PARK.
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
)

REFUSED = (
    "no Clay / unconditional 3-D regularity claim",
    "no bound of Tjj by Lambda' or dZj",
    "no large-form [SND] as measured smallness",
    "no import of 2-D rho=0.02 into 3-D",
    "no import of occupancy 1 into CFM",
    "no identifying Tjj with leftover-split strain",
    "no TRANSFORMABLE without a real T",
    "no quote of sign(Lambda') unless pairing residual <= 1e-16",
)


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
    lam = lambda_prime_bookkeeping(tc, nu, ds, x) if closed else None
    first_sentence = (
        "Class: unaugmented axisymmetric Navier-Stokes with swirl. "
        "Quantity: dyadic shell block Z_j. Remainder after Door-1: "
        "T_{j←j}. Assumed in brackets: [smooth compactly supported "
        "divergence-free axisymmetric-with-swirl classical NS; no added "
        "field; pairing closed only at 1e-16 residual]."
    )
    growing_term = "T_{j←j} is the one term that can grow Z_j"
    return {
        "protocol": "axisymmetric-shell",
        "filter": "docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md",
        "estimate": "docs/papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md",
        "first_sentence": first_sentence,
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
        ],
        "identity": {
            "door_1": "dot Z_j = T_{j←≠j} + T_{j←j} - ν D_j",
            "only_remainder": "T_{j←j}",
            "not_bounded_by": ["dot Z_j", "Lambda'", "a new symbol of the same size"],
        },
        "bookkeeping": {
            "Lambda_prime": "2(Tc - ν Ds)/X",
            "is_final_lhs": False,
            "value": lam,
            "sign_quoted": False,
            "reason": (
                None
                if closed
                else "pairing residual exceeds 1e-16; do not quote sign(Lambda')"
            ),
        },
        "closed_triad": {
            "rewrite": "tau = (ω(p)-ω(r)) Jp + (ω(q)-ω(r)) Jq",
            "shift": "ω_* lattice constant, not Lambda",
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
        "door_3": {
            "alignment_alpha": "criterion to test",
            "separate_from": "triad-phase occupancy",
        },
        "measured_facts": {
            "2d": dict(TWO_D_FACTS),
            "3d": dict(THREE_D_FACTS),
            "swirl_removes_free_helical_HHH": "class statement, not a measured 3-D CFM close",
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


def cycle_axisymmetric_shell() -> CycleReport:
    payload = axisymmetric_shell_estimate()
    leftover_vs_shell = translate_expressions(SWIRL_LEFTOVER_LAB, SHELL_REMAINDER_LAB)
    dec = decompose(SHELL_REMAINDER_LAB, name="shell_remainder")
    candidate = CandidateArchitecture(
        name="axisymmetric_shell_open",
        components=[
            "Door-1 shell budget (cross-shell flux moved)",
            "remainder T_{j←j} (not shown small)",
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
                evidence=["T_{j←j}", payload["status"]],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Not TRANSFORMABLE. Not Clay.",
            "Do not quote sign(Lambda') unless pairing.closed.",
        ],
    )
    return CycleReport(
        mode="axisymmetric-shell",
        target=(
            "name the Door-1 remainder T_{j←j} on the axisymmetric-with-swirl "
            "class; keep the gap visible"
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
        prediction=payload,
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            payload["first_sentence"],
            f"status={payload['status']} clay={payload['clay']}",
            f"pairing_closed={payload['pairing']['closed']}",
            "Filter: docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md",
        ],
        method_credits=["axisymmetric-shell audit filter", "Door-1 shell budget"],
    )
