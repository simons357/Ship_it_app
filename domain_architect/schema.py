"""Frozen scientific vocabulary for Domain Architect v1.0.

The live organizing operations are

    DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE

They are an organizational interface, not a restriction on mathematical
ontology and not a universal physical equation.
"""

from __future__ import annotations

from enum import Enum, IntEnum
from typing import Final


PRODUCT_DESCRIPTION: Final[str] = (
    "Domain Architect analyzes, translates and synthesizes systems by the "
    "functional roles their components perform. It decomposes a system into "
    "roles, mechanisms, operators and parameters; tests which mathematical "
    "structure survives a cross-domain map; and assembles compatible "
    "mechanisms into candidate architectures. Functional correspondence is a "
    "hypothesis, not physical equivalence."
)

ORGANIZING_GRAMMAR: Final[str] = "DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE"

# Historical research constructs. Not part of the live computational core.
CANONICAL_SFE_STATUS: Final[str] = "archived — not part of Domain Architect v1.0"

OPEN_ROLES: Final[tuple[str, ...]] = (
    "selection",
    "interaction",
    "transport",
    "feedback",
    "dissipation",
    "forcing",
    "constraint",
    "state_transition",
    "measurement",
)


class FunctionalRole(str, Enum):
    """Open role list from the v1.0 paper. Additional roles may be declared."""

    SELECTION = "selection"
    INTERACTION = "interaction"
    TRANSPORT = "transport"
    FEEDBACK = "feedback"
    DISSIPATION = "dissipation"
    FORCING = "forcing"
    CONSTRAINT = "constraint"
    STATE_TRANSITION = "state_transition"
    MEASUREMENT = "measurement"
    STATE = "state"
    PARAMETER = "parameter"
    OUTPUT = "output"
    UNRESOLVED = "unresolved"


class CompatibilityClass(str, Enum):
    DIRECTLY_COMPATIBLE = "DIRECTLY_COMPATIBLE"
    TRANSFORMABLE = "TRANSFORMABLE"
    INCOMPATIBLE = "INCOMPATIBLE"


class CorrespondenceKind(str, Enum):
    ANALOGY = "analogy"
    MATHEMATICAL_CORRESPONDENCE = "mathematical_correspondence"
    STRUCTURE_PRESERVING_EQUIVALENCE = "structure_preserving_equivalence"


class ValidationGate(str, Enum):
    MATHEMATICAL = "MATHEMATICAL"
    COMPUTATIONAL = "COMPUTATIONAL"
    EMPIRICAL = "EMPIRICAL"


class EvidenceLevel(IntEnum):
    """Highest claim a report may make. Higher levels include the lower ones."""

    COHERENT_CLASSIFICATION = 0
    MATHEMATICAL_COMPATIBILITY = 1
    KNOWN_MODEL_OR_LIMIT_RECOVERY = 2
    COMPUTATIONAL_ADVANTAGE = 3
    DISTINCT_QUANTITATIVE_PREDICTION = 4
    EMPIRICAL_SUPPORT = 5
    REPLICATED_GENERAL_PHYSICAL_THEORY = 6

    @property
    def label(self) -> str:
        return {
            EvidenceLevel.COHERENT_CLASSIFICATION: "Level 0 — Coherent classification",
            EvidenceLevel.MATHEMATICAL_COMPATIBILITY: "Level 1 — Mathematical compatibility",
            EvidenceLevel.KNOWN_MODEL_OR_LIMIT_RECOVERY: (
                "Level 2 — Known-model or known-limit recovery"
            ),
            EvidenceLevel.COMPUTATIONAL_ADVANTAGE: (
                "Level 3 — Computational advantage under frozen fair tests"
            ),
            EvidenceLevel.DISTINCT_QUANTITATIVE_PREDICTION: (
                "Level 4 — Distinct quantitative prediction"
            ),
            EvidenceLevel.EMPIRICAL_SUPPORT: "Level 5 — Empirical support",
            EvidenceLevel.REPLICATED_GENERAL_PHYSICAL_THEORY: (
                "Level 6 — Replicated general physical theory"
            ),
        }[self]


class ScaleResponseSubtype(str, Enum):
    SPECTRAL_COORDINATE = "spectral_coordinate"
    EIGENVALUE = "eigenvalue"
    WAVELENGTH = "wavelength"
    INVERSE_EIGENVALUE = "inverse_eigenvalue"
    TRANSFER_FUNCTION = "transfer_function"
    PROPAGATOR = "propagator"
    GREEN_FUNCTION = "Green_function"
    SPECTRAL_WEIGHT = "spectral_weight"
    UNKNOWN = "unknown"


COORDINATE_LIKE_SCALE: Final[frozenset[ScaleResponseSubtype]] = frozenset(
    {
        ScaleResponseSubtype.SPECTRAL_COORDINATE,
        ScaleResponseSubtype.EIGENVALUE,
        ScaleResponseSubtype.WAVELENGTH,
    }
)
RESPONSE_LIKE_SCALE: Final[frozenset[ScaleResponseSubtype]] = frozenset(
    {
        ScaleResponseSubtype.INVERSE_EIGENVALUE,
        ScaleResponseSubtype.TRANSFER_FUNCTION,
        ScaleResponseSubtype.PROPAGATOR,
        ScaleResponseSubtype.GREEN_FUNCTION,
        ScaleResponseSubtype.SPECTRAL_WEIGHT,
    }
)


class PermissionSubtype(str, Enum):
    IDENTITY = "identity"
    ORTHOGONAL_PROJECTOR = "orthogonal_projector"
    OBLIQUE_PROJECTOR = "oblique_projector"
    BINARY_SELECTOR = "binary_selector"
    ADMISSIBILITY_CONSTRAINT = "admissibility_constraint"
    GAUGE_CONSTRAINT = "gauge_constraint"
    BOUNDARY_CONSTRAINT = "boundary_constraint"
    SOFT_FILTER = "soft_filter"
    WEIGHTING_OPERATOR = "weighting_operator"
    UNKNOWN = "unknown"


PROJECTOR_SUBTYPES: Final[frozenset[PermissionSubtype]] = frozenset(
    {
        PermissionSubtype.ORTHOGONAL_PROJECTOR,
        PermissionSubtype.OBLIQUE_PROJECTOR,
    }
)


class MathType(str, Enum):
    SCALAR = "scalar"
    VECTOR = "vector"
    COVECTOR = "covector"
    MATRIX = "matrix"
    TENSOR = "tensor"
    OPERATOR = "operator"
    FUNCTIONAL = "functional"
    DISTRIBUTION = "distribution"
    FIELD = "field"
    STATE_VECTOR = "state_vector"
    DENSITY_MATRIX = "density_matrix"
    KERNEL = "kernel"
    MEASURE = "measure"
    SET = "set"
    MANIFOLD = "manifold"
    UNKNOWN = "unknown"


class RecoveryKind(str, Enum):
    """Architectural rewrite versus genuine controlled-limit recovery."""

    REPRESENTATION_RECOVERY = "representation_recovery"
    LIMITING_THEORY_RECOVERY = "limiting_theory_recovery"


class ConflictRelation(str, Enum):
    IDENTICAL = "IDENTICAL"
    NOTATIONALLY_EQUIVALENT = "NOTATIONALLY_EQUIVALENT"
    EQUIVALENT_UNDER_SUBSTITUTION = "EQUIVALENT_UNDER_SUBSTITUTION"
    SPECIAL_CASE = "SPECIAL_CASE"
    GENERALIZATION = "GENERALIZATION"
    COMPATIBLE_DISTINCT = "COMPATIBLE_DISTINCT"
    INCOMPATIBLE = "INCOMPATIBLE"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"


class Disposition(str, Enum):
    RETAIN = "RETAIN"
    REVISE = "REVISE"
    RETIRE = "RETIRE"
    UNRESOLVED = "UNRESOLVED"
    ARCHIVED = "ARCHIVED"


class MathValidationStatus(str, Enum):
    NOT_PERFORMED = "not_performed"
    PASSED = "passed"
    FAILED = "failed"
    INCONCLUSIVE = "inconclusive"


class PhysicalValidationStatus(str, Enum):
    NONE = "none"
    BENCHMARK_REPRESENTATION = "benchmark_representation"
    CONTROLLED_LIMIT = "controlled_limit"
    EMPIRICAL = "empirical"


FORBIDDEN_CLAIM_PHRASES: Final[tuple[str, ...]] = (
    "proves",
    "demonstrates new physics",
    "derives gravity",
    "derives newtonian gravity",
    "derivation of gravity",
    "confirms the sfe",
    "validates uhf",
    "validates dhfa",
    "discovers",
    "fundamental structure of nature",
    "unified theory",
    "universal physical equation",
    "physically privileged",
    "prime structure is fundamental",
)

PREFERRED_CLAIM_VERBS: Final[tuple[str, ...]] = (
    "maps",
    "represents",
    "is compatible with",
    "reproduces the stated equation under the supplied definitions",
    "suggests",
    "exhibits",
    "passes this test",
    "fails this test",
    "remains unresolved",
    "is consistent with",
    "provides an organizational correspondence",
)

SCOPE_PROHIBITIONS: Final[tuple[str, ...]] = (
    "all equations contain exactly four inputs and one output",
    "all physical theories reduce to the same hidden equation",
    "UHF, SFE, and DHFA are already established physical laws",
    "prime selection is physically privileged",
    "rewriting a known theory in functional-role notation "
    "constitutes a derivation of that theory",
    "agreement between AI systems constitutes independent validation",
    "functional correspondence implies physical equivalence",
)

SOURCE_STATE_WARNING: Final[str] = (
    "Source and state have been proposed as separate functional components, "
    "but the available equation does not uniquely identify them. The "
    "decomposition should not be interpreted as two independent physical "
    "degrees of freedom without an explicit definition."
)

REPRESENTATION_NOT_DERIVATION: Final[str] = (
    "Domain Architect represents the Newtonian Poisson equation by functional "
    "roles. This establishes representational compatibility, not derivation "
    "of gravity from a more general theory."
)

IDENTIFIABILITY_FULL_RANK: Final[str] = (
    "The local Jacobian is full rank at the tested point."
)

IDENTIFIABILITY_SENSITIVITY: Final[str] = (
    "Local sensitivity analysis indicates distinguishable parameter "
    "directions under the stated observables and evaluation conditions."
)

FORBIDDEN_IDENTIFIABILITY: Final[str] = "The parameters are identifiable."
