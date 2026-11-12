"""DA-NS-2 — Domain Architect encoding of the Y-cousin occupation bound.

Claim (HYPOTHESIS, not proved):

    K_min,θ = [T_c − θ ν D_s]_+ / Y
    sup_n ∫_0^T K_min,θ^(n)(t) dt ≤ F(ν, T, u_0) < ∞

without a continuation norm. Status: OPEN.

DA-NS-1 is the X-remainder packaging T_c ≤ θν D_s + K(t) X.
DA-NS-2 is the Y-cousin. They are the same leftover, two writings.
Lemma★ is a third writing (energy-budget Clay packaging) and is
also not proved. Do not merge the labels into a close.

DA will not green DA-NS-2 as PROVED. Refuses NS solved / Clay / Φ-renorm glue.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any

from .schema import CANONICAL_SFE_STATUS, EvidenceLevel


CLAIM = (
    "sup_n int_0^T [T_c^(n) - theta*nu*D_s^(n)]_+ / Y^(n) dt "
    "<= F(nu, T, u0) < infinity"
)
CLAIM_UNICODE = (
    "sup_n ∫_0^T [T_c^(n) − θν D_s^(n)]_+ / Y^(n) dt ≤ F(ν, T, u_0) < ∞"
)
K_MIN = "[T_c - theta*nu*D_s]_+ / Y"
STATUS = "OPEN"
NS_SOLVED = False
LEMMA_STAR_PROVED = False

QUANTITIES: dict[str, str] = {
    "T_c": "centered spectral drift M - Lambda N",
    "D_s": "spectral spread Z - Lambda Y >= 0",
    "X": "||A^{1/2} u||_2^2",
    "Y": "||A u||_2^2",
    "Z": "||A^{3/2} u||_2^2",
    "Lambda": "Y/X barycenter",
    "K_min": "positive occupation [T_c - theta nu D_s]_+ / Y",
    "theta": "fixed number in [0, 1)",
    "nu": "viscosity",
}

KILLED: tuple[tuple[str, str], ...] = (
    ("pure absorption T_c <= theta nu D_s", "amplitude: T_c/D_s scales as |a|"),
    ("tautological K_Y as a theorem", "defining K as the ratio makes the estimate an identity"),
    ("charge-only net coercivity", "two-triad witness; Sprint 01"),
    ("frozen log-charge at theta = 1", "(1-theta) nu D_s/Y survives; endpoint is theta < 1"),
    ("automatic dephasing", "2D3C half-turn lock is separately regular"),
    ("one-channel ODE as vector NS", "not an invariant subsystem"),
    ("Serrin / BKM last line", "continuation norm; stop"),
    ("int D_s/Y or sup Lambda as a close", "renamed hole"),
)

NEXT_WRITE = (
    "Joint Gap-Charge Epoch Budget: charge, radial covariance, "
    "moving-barycenter error, homochiral drift, cross-band flux, "
    "phase/far terms, one-use dissipation, summable resets; "
    "cutoff-uniform; theta < 1 directly"
)

DA_NS_2_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"da-?ns-?2", re.I),
    re.compile(r"k_?min\s*,?\s*theta|k_?min,θ", re.I),
    re.compile(r"y-?cousin", re.I),
    re.compile(
        r"\[?\s*t_c\s*.{0,12}theta.{0,12}d_s.{0,12}\]?_?\s*/\s*y",
        re.I,
    ),
    re.compile(r"occupation\s+bound|galerkin-uniform", re.I),
)


@dataclass
class DANS2Card:
    book: str = "DA-NS-2"
    claim: str = CLAIM
    claim_unicode: str = CLAIM_UNICODE
    k_min: str = K_MIN
    status: str = STATUS
    ns_solved: bool = NS_SOLVED
    lemma_star_proved: bool = LEMMA_STAR_PROVED
    canonical_sfe_status: str = CANONICAL_SFE_STATUS
    highest_evidence_level: int = int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY)
    identities: str = "EXACT"
    integral_bound: str = "OPEN"
    jgc_epoch_budget: str = "NOT_SEATED"
    cousin_of: str = "DA-NS-1 X-remainder; same leftover as Lemma-star packaging"
    do_not_put_K_in_the_PDE: bool = True
    quantities: dict[str, str] = field(default_factory=lambda: dict(QUANTITIES))
    killed: list[dict[str, str]] = field(
        default_factory=lambda: [{"attempt": a, "why": w} for a, w in KILLED]
    )
    next_write: str = NEXT_WRITE
    notes: list[str] = field(
        default_factory=lambda: [
            "If the integral sits, Lambda stays bounded, then X <= |u0|_2^2 Lambda, then continuation.",
            "The implication is the usual skeleton. The integral is the hole.",
            "Phase variables count only if they prove this bound rather than rename it.",
            "Do not glue to Phi-renorm, Q1, SND, or Clay Statement B.",
        ]
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def narrative(self) -> str:
        lines = [
            "DA-NS-2 — Y-cousin occupation bound",
            f"Claim: {self.claim_unicode}",
            f"Status: {self.status}",
            f"Identities: {self.identities}",
            f"Integral bound: {self.integral_bound}",
            f"JGC epoch budget: {self.jgc_epoch_budget}",
            f"ns_solved: {self.ns_solved}",
            f"lemma_star_proved: {self.lemma_star_proved}",
            f"Canonical SFE status: {self.canonical_sfe_status}",
            "Killed:",
        ]
        for row in self.killed:
            lines.append(f"  - {row['attempt']}: {row['why']}")
        lines.append(f"Next write: {self.next_write}")
        lines.append("Do not put K(t) in the PDE.")
        return "\n".join(lines)


def looks_like_da_ns_2(text: str) -> bool:
    return any(p.search(text) for p in DA_NS_2_PATTERNS)


def navigate_da_ns_2() -> DANS2Card:
    return DANS2Card()


def refuse_proved(statement: str = "DA-NS-2 is proved") -> dict[str, Any]:
    """Refuse EXPRESS/PROVED claims. The bound is OPEN."""
    return {
        "statement": statement,
        "accepted": False,
        "status": STATUS,
        "ns_solved": NS_SOLVED,
        "reason": (
            "DA-NS-2 is a named leftover, not a theorem. "
            "Defining K_min as the positive part over Y is a tautology. "
            "The Galerkin-uniform integral is the hole."
        ),
        "forbidden": True,
    }


def express_as_proved() -> dict[str, Any]:
    return refuse_proved("express DA-NS-2 as PROVED")


FORBIDDEN_LAST_LINES: tuple[str, ...] = (
    "int D_s/Y",
    "int (N/X)_+",
    "sup Lambda",
    "int Y",
    "Serrin",
    "BKM",
    "continuation norm",
    "H^1 ceiling",
    "L^infty",
    "||u||_H1",
)

JGC_BUDGET_TERMS: tuple[str, ...] = (
    "charge",
    "radial covariance",
    "moving-barycenter error",
    "homochiral drift",
    "cross-band flux",
    "phase/far terms",
    "one-use dissipation",
    "summable resets",
)


def classify_last_line(text: str) -> dict[str, Any]:
    """Refuse continuation-norm last lines. JGC language is a spec, not a theorem."""
    lowered = text.lower().replace("λ", "lambda").replace("Λ", "lambda")
    lowered = lowered.replace("∫", "int ").replace("≤", "<=")
    hits = [item for item in FORBIDDEN_LAST_LINES if item.lower() in lowered]
    jgc_hits = [item for item in JGC_BUDGET_TERMS if item.lower() in lowered]
    if hits:
        status = "REJECTED"
        reason = "last line is a continuation norm or a renamed hole"
    elif jgc_hits:
        status = "SPEC_ONLY"
        reason = "named Joint Gap-Charge terms; budget is not seated"
    else:
        status = "UNSCORED"
        reason = "not a recognized DA-NS-2 last line"
    return {
        "text": text,
        "status": status,
        "forbidden_hits": hits,
        "jgc_hits": jgc_hits,
        "da_ns_2": STATUS,
        "reason": reason,
    }


def card_json() -> str:
    return json.dumps(navigate_da_ns_2().to_dict(), indent=2) + "\n"
