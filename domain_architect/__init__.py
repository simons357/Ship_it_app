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
from .gap import gap_report
from .shape_play import shape_play
from .energy_play import energy_play
from .overlay import overlay_report
from .scan import scan_report
from .visual import follow, write_see
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
    "gap_report",
    "ns_chain",
    "ns_geometry",
    "proceed_report",
    "tube_estimate",
    "refuse_splice",
    "shape_play",
    "energy_play",
    "overlay_report",
    "scan_report",
    "write_see",
    "follow",
]

__version__ = "0.2.0"
