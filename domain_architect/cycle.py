"""Domain Architect cycle engine.

TARGET + CONSTRAINTS → DECOMPOSE → TRANSLATE → SYNTHESIZE
→ PREDICT → TEST → RESIDUAL ↺

Named demonstrations live in ``pipeline.py`` and call this engine.
They are examples, not the product.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .decompose import Decomposition, decompose
from .schema import ValidationGate
from .synthesize import CandidateArchitecture, inverse_design_architecture
from .translate import TranslationRecord


@dataclass
class CycleSpec:
    target: str
    constraints: list[str]
    plant: str | None = None
    plant_name: str | None = None
    observations: dict[str, Any] | None = None


@dataclass
class CycleReport:
    mode: str
    target: str
    constraints: list[str]
    decomposition: Decomposition | None
    translation: TranslationRecord | None
    candidate: CandidateArchitecture | None
    prediction: dict[str, Any] | None
    residual: Any | None
    validation_gate: ValidationGate
    notes: list[str] = field(default_factory=list)
    method_credits: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        residual = self.residual
        residual_payload = None
        if residual is not None:
            residual_payload = residual.to_dict() if hasattr(residual, "to_dict") else residual
        return {
            "mode": self.mode,
            "target": self.target,
            "constraints": list(self.constraints),
            "decomposition": None if self.decomposition is None else self.decomposition.to_dict(),
            "translation": None if self.translation is None else self.translation.to_dict(),
            "candidate": None if self.candidate is None else self.candidate.to_dict(),
            "prediction": self.prediction,
            "residual": residual_payload,
            "validation_gate": self.validation_gate.value,
            "notes": list(self.notes),
            "method_credits": list(self.method_credits),
        }


def run_cycle(
    spec: CycleSpec,
    *,
    mode: str = "analysis",
    translator: Callable[[Decomposition], TranslationRecord | None] | None = None,
    synthesizer: Callable[[Decomposition | None], CandidateArchitecture] | None = None,
    predictor: Callable[[CandidateArchitecture], dict[str, Any] | None] | None = None,
    residual_fn: Callable[[dict[str, Any] | None], Any] | None = None,
    notes: list[str] | None = None,
    method_credits: list[str] | None = None,
    gate: ValidationGate = ValidationGate.MATHEMATICAL,
) -> CycleReport:
    """Walk one cycle. Callers supply the methods; DA supplies the order."""
    decomposition = None
    if spec.plant:
        decomposition = decompose(spec.plant, name=spec.plant_name)

    translation = translator(decomposition) if translator and decomposition else None

    if synthesizer is not None:
        candidate = synthesizer(decomposition)
    elif spec.target:
        candidate = inverse_design_architecture(spec.target, spec.constraints)
    else:
        candidate = None

    prediction = predictor(candidate) if predictor and candidate else None
    residual = residual_fn(prediction) if residual_fn else None

    return CycleReport(
        mode=mode,
        target=spec.target,
        constraints=list(spec.constraints),
        decomposition=decomposition,
        translation=translation,
        candidate=candidate,
        prediction=prediction,
        residual=residual,
        validation_gate=gate,
        notes=list(notes or []),
        method_credits=list(method_credits or []),
    )
