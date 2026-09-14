"""Domain Architect — Functional Role Analysis and model-auditing tools.

This package is a research architecture for classifying mathematical models
into independently meaningful roles. It is not a physical theory, a
canonical Simons Field Equation, or a proof engine.

Organizational grammar (not a universal physical equation):

    Φ = ℱ(P, H, ψ, λ; E)

P, H, ψ, λ, and Φ are role names. They do not imply that every equation
has exactly four inputs and one output.
"""

from .schema import (
    CANONICAL_SFE_STATUS,
    HILBERT_POLYA_STATUS,
    PRODUCT_DESCRIPTION,
    RH_STATUS,
    EvidenceLevel,
    PermissionSubtype,
    RecoveryKind,
    ScaleResponseSubtype,
)
from .audit import audit_expression
from .hilbert_polya import audit_candidate, default_program_audit
from .polya_probe import run_polya_probe
from .millennium_overlap import millennium_look_narrative
from .report import AuditReport

__all__ = [
    "CANONICAL_SFE_STATUS",
    "HILBERT_POLYA_STATUS",
    "PRODUCT_DESCRIPTION",
    "RH_STATUS",
    "AuditReport",
    "EvidenceLevel",
    "PermissionSubtype",
    "RecoveryKind",
    "ScaleResponseSubtype",
    "audit_candidate",
    "audit_expression",
    "default_program_audit",
    "run_polya_probe",
    "millennium_look_narrative",
]

__version__ = "0.4.4"
