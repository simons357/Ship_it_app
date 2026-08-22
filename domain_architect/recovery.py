"""Separate representation recovery from limiting-theory recovery."""

from __future__ import annotations

from dataclasses import dataclass

from .schema import EvidenceLevel, RecoveryKind, REPRESENTATION_NOT_DERIVATION


@dataclass
class RecoveryRecord:
    kind: RecoveryKind
    target_theory: str
    independent_broader_model: bool
    controlled_limit: str | None
    evidence_level: EvidenceLevel
    statement: str


def classify_recovery(
    *,
    known_equation_rewritten: bool,
    independent_broader_model: bool,
    controlled_limit: str | None = None,
    target_theory: str = "Newtonian Poisson gravity",
) -> RecoveryRecord:
    """A rewrite of a known equation is representation, not derivation.

    Limiting-theory recovery requires a broader model that existed before
    the target theory was inserted, plus a mathematically defined limit.
    """
    if known_equation_rewritten and not (
        independent_broader_model and controlled_limit
    ):
        return RecoveryRecord(
            kind=RecoveryKind.REPRESENTATION_RECOVERY,
            target_theory=target_theory,
            independent_broader_model=False,
            controlled_limit=None,
            evidence_level=EvidenceLevel.MATHEMATICAL_COMPATIBILITY,
            statement=REPRESENTATION_NOT_DERIVATION
            if "poisson" in target_theory.lower() or "newton" in target_theory.lower()
            else (
                f"Functional Role Analysis represents {target_theory}. "
                "This is architectural compatibility, not derivation."
            ),
        )
    if independent_broader_model and controlled_limit:
        return RecoveryRecord(
            kind=RecoveryKind.LIMITING_THEORY_RECOVERY,
            target_theory=target_theory,
            independent_broader_model=True,
            controlled_limit=controlled_limit,
            evidence_level=EvidenceLevel.KNOWN_MODEL_OR_LIMIT_RECOVERY,
            statement=(
                f"An independently specified broader model reduces to "
                f"{target_theory} under the controlled limit {controlled_limit}. "
                "This is known-limit recovery, not a new physical derivation "
                "from a canonical SFE unless that SFE exists independently."
            ),
        )
    return RecoveryRecord(
        kind=RecoveryKind.REPRESENTATION_RECOVERY,
        target_theory=target_theory,
        independent_broader_model=independent_broader_model,
        controlled_limit=controlled_limit,
        evidence_level=EvidenceLevel.COHERENT_CLASSIFICATION,
        statement="Recovery kind remains unresolved.",
    )
