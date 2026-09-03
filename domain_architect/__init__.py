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
    EvidenceLevel,
    PermissionSubtype,
    RecoveryKind,
    ScaleResponseSubtype,
)
from .audit import audit_expression
from .clip_splice import clip_splice
from .desk import compare_shape, proceed_report, refuse_splice
from .ns_chain import ns_chain
from .ns_geometry import ns_geometry
from .ns_tube import tube_estimate
from .report import AuditReport

__all__ = [
    "CANONICAL_SFE_STATUS",
    "PRODUCT_DESCRIPTION",
    "AuditReport",
    "EvidenceLevel",
    "PermissionSubtype",
    "RecoveryKind",
    "ScaleResponseSubtype",
    "audit_expression",
    "clip_splice",
    "compare_shape",
    "ns_chain",
    "ns_geometry",
    "proceed_report",
    "tube_estimate",
    "refuse_splice",
]

__version__ = "0.2.0"
