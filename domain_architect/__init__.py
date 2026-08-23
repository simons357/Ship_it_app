"""Domain Architect v1.0 — decompose, translate, synthesize.

This package is a computational framework for functional-role architecture.
It is not a physical theory and it does not assume that corresponding
functions are physically equivalent.

Primary operations:

    DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE
"""

from .schema import (
    ORGANIZING_GRAMMAR,
    PRODUCT_DESCRIPTION,
    CompatibilityClass,
    CorrespondenceKind,
    EvidenceLevel,
    FunctionalRole,
    ValidationGate,
)
from .audit import audit_expression
from .decompose import decompose
from .pipeline import run_benchmarks, run_named_cycle
from .report import AuditReport
from .translate import translate, translate_expressions

__all__ = [
    "ORGANIZING_GRAMMAR",
    "PRODUCT_DESCRIPTION",
    "AuditReport",
    "CompatibilityClass",
    "CorrespondenceKind",
    "EvidenceLevel",
    "FunctionalRole",
    "ValidationGate",
    "audit_expression",
    "decompose",
    "run_benchmarks",
    "run_named_cycle",
    "translate",
    "translate_expressions",
]

__version__ = "1.0.0"
