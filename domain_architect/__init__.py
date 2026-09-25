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
    PRODUCT_DESCRIPTION,
    SCHEMA_VERSION,
    EvidenceLevel,
    PermissionSubtype,
    ProcessStatus,
    RecoveryKind,
    ScaleResponseSubtype,
    StampKind,
)
from .audit import audit_expression
from .process_console import ProcessConsole
from .report import AuditReport

__all__ = [
    "CANONICAL_SFE_STATUS",
    "PRODUCT_DESCRIPTION",
    "SCHEMA_VERSION",
    "AuditReport",
    "EvidenceLevel",
    "PermissionSubtype",
    "ProcessConsole",
    "ProcessStatus",
    "RecoveryKind",
    "ScaleResponseSubtype",
    "StampKind",
    "audit_expression",
]

__version__ = "0.5.0"
