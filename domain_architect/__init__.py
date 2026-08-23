"""Domain Architect — decompose, translate, synthesize.

This package is a computational framework for functional-role architecture.
It is not a physical theory and it does not assume that corresponding
functions are physically equivalent. SFE and the Harmonic Blueprint are
not part of the live import surface.

Primary operations:

    DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE
"""

from .schema import (
    PRIMARY_OPERATIONS,
    PRODUCT_DESCRIPTION,
    CompatibilityClass,
    CorrespondenceKind,
    EvidenceLevel,
    FunctionalRole,
    ValidationGate,
)
from .audit import audit_expression
from .cycle import CycleReport, CycleSpec, run_cycle
from .decompose import decompose
from .pipeline import run_benchmarks, run_named_cycle
from .report import AuditReport
from .translate import translate, translate_expressions

__all__ = [
    "PRIMARY_OPERATIONS",
    "PRODUCT_DESCRIPTION",
    "AuditReport",
    "CompatibilityClass",
    "CorrespondenceKind",
    "CycleReport",
    "CycleSpec",
    "EvidenceLevel",
    "FunctionalRole",
    "ValidationGate",
    "audit_expression",
    "decompose",
    "run_benchmarks",
    "run_cycle",
    "run_named_cycle",
    "translate",
    "translate_expressions",
]

__version__ = "1.1.0"
