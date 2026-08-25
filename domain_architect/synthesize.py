"""SYNTHESIZE: construct candidate architectures from compatible mechanisms."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .compatibility import CompatibilityReport, Transformation
from .decompose import ArchitectureNode, Decomposition
from .schema import CompatibilityClass, ValidationGate

# A13: inverse design is fail-closed unless the target is a recognized
# setpoint / objective object. "x=1" and "x → 1.0" stay legal. Open PDEs,
# Clay slogans, and "maximize profit" must not emit a PD loop.
_RECOGNIZED_SETPOINT = re.compile(
    r"^\s*x[★*]?\s*(?:=|→|->)\s*\S",
    re.IGNORECASE,
)


@dataclass
class Provenance:
    source: str
    original_domain: str
    functional_role: str
    translation: str | None
    assumptions: list[str]
    compatibility_checks: list[str]
    modifications: list[str]
    evidence: list[str]
    validation_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "original_domain": self.original_domain,
            "functional_role": self.functional_role,
            "translation": self.translation,
            "assumptions": list(self.assumptions),
            "compatibility_checks": list(self.compatibility_checks),
            "modifications": list(self.modifications),
            "evidence": list(self.evidence),
            "validation_status": self.validation_status,
        }


@dataclass
class CandidateArchitecture:
    name: str
    components: list[str]
    replaced: dict[str, str]
    hypothesis: str
    provenance: list[Provenance]
    validation_gate: ValidationGate
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "components": list(self.components),
            "replaced": dict(self.replaced),
            "hypothesis": self.hypothesis,
            "provenance": [p.to_dict() for p in self.provenance],
            "validation_gate": self.validation_gate.value,
            "notes": list(self.notes),
        }


def synthesize(
    base: Decomposition,
    *,
    replacements: dict[str, str],
    compatibility: list[CompatibilityReport],
    name: str | None = None,
    extra_components: list[str] | None = None,
) -> CandidateArchitecture:
    """Build S★ = A + B + T(X) + D from a legal replacement of C by X.

    The candidate is a hypothesis. It is not automatically physically realizable.
    """
    illegal = [
        c
        for c in compatibility
        if c.verdict == CompatibilityClass.INCOMPATIBLE
        and c.left in replacements
    ]
    if illegal:
        raise ValueError(
            "refusing to synthesize an incompatible substitution: "
            + ", ".join(c.left for c in illegal)
        )
    missing_t = [
        c
        for c in compatibility
        if c.verdict == CompatibilityClass.TRANSFORMABLE
        and c.left in replacements
        and c.transformation is None
    ]
    if missing_t:
        raise ValueError(
            "TRANSFORMABLE substitutions require an explicit T: "
            + ", ".join(c.left for c in missing_t)
        )

    components = [n.name for n in base.mechanisms()]
    for old, new in replacements.items():
        components = [new if c == old else c for c in components]
    for extra in extra_components or []:
        if extra not in components:
            components.append(extra)

    provenance = []
    for report in compatibility:
        if report.left not in replacements:
            continue
        t: Transformation | None = report.transformation
        provenance.append(
            Provenance(
                source=report.right,
                original_domain=report.right,
                functional_role=next(
                    (
                        (h.role.value)
                        for h in base.hypotheses()
                        if h.symbol == report.left
                    ),
                    "unresolved",
                ),
                translation=None if t is None else t.name,
                assumptions=list(report.assumptions),
                compatibility_checks=[report.verdict.value, report.kind.value],
                modifications=[] if t is None else [f"{k}->{v}" for k, v in t.mapping.items()],
                evidence=list(report.reasons),
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        )

    return CandidateArchitecture(
        name=name or f"candidate[{base.tree.name}]",
        components=components,
        replaced=dict(replacements),
        hypothesis=(
            "Synthesized architecture is a hypothesis. Mathematical coherence "
            "does not imply physical realizability."
        ),
        provenance=provenance,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Validation remaining: COMPUTATIONAL then EMPIRICAL.",
        ],
    )


def required_roles_for_target(
    *,
    has_dynamics: bool,
    needs_feedback: bool,
    constrained: bool,
) -> list[str]:
    """Inverse-design: roles that must exist for a target to be reachable."""
    roles = ["state", "state_transition"]
    if has_dynamics:
        roles.append("measurement")
    if needs_feedback:
        roles.extend(["feedback", "forcing"])
    if constrained:
        roles.append("constraint")
    return list(dict.fromkeys(roles))


def is_recognized_setpoint(target: str) -> bool:
    """True only for a concrete state objective such as ``x=1`` or ``x → 1.0``."""
    return bool(_RECOGNIZED_SETPOINT.match((target or "").strip()))


def inverse_design_architecture(
    target: str,
    constraints: list[str],
    *,
    plant: str = "second_order_linear",
) -> CandidateArchitecture:
    if not is_recognized_setpoint(target):
        return _fail_closed_inverse_design(target, constraints)
    roles = required_roles_for_target(
        has_dynamics=True,
        needs_feedback=True,
        constrained=bool(constraints),
    )
    components = [
        "state x(t)",
        "measurement y = x",
        "compare e = x★ − x",
        "control u = K(x, e, C)",
        "transition ẋ = F(x, u, t)",
    ]
    if constraints:
        components.append("constraint saturation / admissible set")
    tree_note = ArchitectureNode(
        level="SYSTEM",
        name=f"inverse:{target}",
        children=[],
    )
    _ = tree_note
    return CandidateArchitecture(
        name=f"inverse_design[{plant}]",
        components=components,
        replaced={},
        hypothesis=(
            f"Target {target!r} requires roles {roles}. The synthesized "
            "loop is STATE → MEASURE → COMPARE → CONTROL → TRANSITION."
        ),
        provenance=[
            Provenance(
                source="target+constraints",
                original_domain="control",
                functional_role="feedback",
                translation=None,
                assumptions=["plant is controllable through u", "state is measured"],
                compatibility_checks=["required_roles_present"],
                modifications=[],
                evidence=[f"constraints={constraints}"],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=["Run the computational gate with domain_architect.dynamics."],
    )


def _fail_closed_inverse_design(
    target: str,
    constraints: list[str],
) -> CandidateArchitecture:
    """A13: refuse a PD plant for an unrecognized objective or an open PDE."""
    lowered = (target or "").lower()
    swirlish = any(
        token in lowered
        for token in (
            "navier",
            "swirl",
            "unaugmented",
            "global smoothness",
            "global regularity",
        )
    )
    leftover = (
        "the strain pairing ∫(u^r/r) Φ² r³ (lab: Istrain = urad/r). "
        "That is Book B continuation, still unproved."
        if swirlish
        else (
            "an independent smallness / concentration hypothesis that energy "
            "does not give. Leftover-split names it; it is not a controller."
        )
    )
    return CandidateArchitecture(
        name="inverse_design[refused]",
        components=[
            "keep coercive / energy estimates already proved",
            "independent leftover σ (not derived from energy, not a PD loop)",
            f"conditional continuation if σ holds — {leftover}",
        ],
        replaced={},
        hypothesis=(
            f"A13 fail-closed: {target!r} is not a recognized setpoint. "
            "Domain Architect will not emit STATE → MEASURE → COMPARE → "
            "CONTROL → TRANSITION as the architecture of an open PDE or an "
            "unrecognized objective. "
            f"The missing mechanism is {leftover} "
            "NS-open stays OPEN. Clay is NOT CLAIMED."
        ),
        provenance=[
            Provenance(
                source="target+constraints",
                original_domain="open-problem",
                functional_role="constraint",
                translation=None,
                assumptions=[
                    "target is not a recognized x★ setpoint",
                    "do not invent a controller for an open PDE",
                ],
                compatibility_checks=["A13 fail-closed"],
                modifications=["refused PD loop"],
                evidence=[f"constraints={constraints}"],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "A13: inverse design fail-closed.",
            "This is not a PD controller.",
            "This is not a regularity proof.",
            "Clay NOT CLAIMED.",
            "Fix path: leftover-repair (conditional σ) or localized-repair "
            "(default cut 7–8). Do not glue Ring J/X to Q6 H_N.",
        ],
    )
