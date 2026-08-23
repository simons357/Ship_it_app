"""DECOMPOSE: recursive functional-role architecture."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .checks import DimensionalResult, check_dimensions
from .classify import Classification, classify_parse
from .parser import ParseResult, parse_expression
from .schema import FunctionalRole
from .signature import RoleHypothesis


LEVELS = (
    "SYSTEM",
    "SUBSYSTEM",
    "FUNCTIONAL_ROLE",
    "MECHANISM",
    "OPERATOR",
    "PARAMETER",
)


@dataclass
class ArchitectureNode:
    level: str
    name: str
    role: str | None = None
    confidence: float | None = None
    rationale: str | None = None
    children: list["ArchitectureNode"] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "name": self.name,
            "role": self.role,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "attributes": dict(self.attributes),
            "children": [c.to_dict() for c in self.children],
        }

    def pretty(self, indent: int = 0) -> str:
        pad = "  " * indent
        role = f"  [{self.role}]" if self.role else ""
        conf = f"  c={self.confidence:.2f}" if self.confidence is not None else ""
        lines = [f"{pad}{self.level}: {self.name}{role}{conf}"]
        if self.rationale:
            lines.append(f"{pad}  {self.rationale}")
        for child in self.children:
            lines.append(child.pretty(indent + 1))
        return "\n".join(lines)

    def walk(self) -> Iterable["ArchitectureNode"]:
        yield self
        for child in self.children:
            yield from child.walk()


@dataclass
class Decomposition:
    expression: str
    parsed: ParseResult
    classification: Classification
    tree: ArchitectureNode
    dimensions: DimensionalResult | None
    warnings: list[str] = field(default_factory=list)

    def hypotheses(self) -> list[RoleHypothesis]:
        return list(self.classification.hypotheses)

    def mechanisms(self) -> list[ArchitectureNode]:
        return [n for n in self.tree.walk() if n.level == "MECHANISM"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "expression": self.expression,
            "pattern": self.classification.pattern,
            "tree": self.tree.to_dict(),
            "hypotheses": [h.to_dict() for h in self.hypotheses()],
            "warnings": list(self.warnings),
            "dimensions": None
            if self.dimensions is None
            else {
                "consistent": self.dimensions.consistent,
                "message": self.dimensions.message,
                "unknown": list(self.dimensions.unknown),
            },
        }


def decompose(
    expression: str,
    *,
    context: dict | None = None,
    name: str | None = None,
) -> Decomposition:
    """Recursively separate a system according to function.

    Depth follows independently functioning parts. Levels are not padded.
    """
    context = dict(context or {})
    parsed = parse_expression(expression)
    classification = classify_parse(parsed, context)
    warnings = list(parsed.warnings) + list(classification.warnings)
    dimensions = None
    if parsed.tree is not None:
        dimensions = check_dimensions(parsed.tree, context.get("units"))
        warnings.append(dimensions.message)

    system = ArchitectureNode(
        level="SYSTEM",
        name=name or expression,
        attributes={"pattern": classification.pattern},
    )
    if classification.pattern != "unclassified":
        subsystem = ArchitectureNode(
            level="SUBSYSTEM",
            name=classification.pattern,
            attributes={"ast": parsed.tree.pretty() if parsed.tree is not None else ""},
        )
        system.children.append(subsystem)
        parent = subsystem
    else:
        parent = system

    by_role: dict[str, list[RoleHypothesis]] = {}
    for hyp in classification.hypotheses:
        by_role.setdefault(hyp.role.value, []).append(hyp)

    if not by_role:
        parent.children.append(
            ArchitectureNode(
                level="FUNCTIONAL_ROLE",
                name=FunctionalRole.UNRESOLVED.value,
                role=FunctionalRole.UNRESOLVED.value,
                confidence=0.15,
                rationale="No structural role could be assigned.",
            )
        )
    for role, hyps in by_role.items():
        role_node = ArchitectureNode(
            level="FUNCTIONAL_ROLE",
            name=role,
            role=role,
            confidence=max(h.confidence for h in hyps),
        )
        for hyp in hyps:
            mechanism = ArchitectureNode(
                level="MECHANISM",
                name=hyp.symbol,
                role=hyp.role.value,
                confidence=hyp.confidence,
                rationale=hyp.rationale,
                attributes={
                    "subtype": hyp.subtype,
                    "signature": hyp.signature.to_dict(),
                    "alternate_roles": list(hyp.alternate_roles),
                },
            )
            if hyp.subtype and hyp.subtype not in {"unknown", hyp.symbol}:
                operator = ArchitectureNode(
                    level="OPERATOR",
                    name=hyp.subtype,
                    role=hyp.role.value,
                    attributes={"math_type": hyp.signature.math_type.value},
                )
                mechanism.children.append(operator)
            role_node.children.append(mechanism)
        parent.children.append(role_node)

    return Decomposition(
        expression=expression,
        parsed=parsed,
        classification=classification,
        tree=system,
        dimensions=dimensions,
        warnings=_unique(warnings),
    )


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))
