"""Symbolic AST parser for Domain Architect.

The parser converts an entered expression into an abstract syntax tree. It
does not assign physical roles from familiar symbol names. ``H`` is an
identifier, not a Hamiltonian, unless a later audit supplies that context.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class NodeKind(str, Enum):
    EQUALITY = "Equality"
    ADD = "Add"
    SUB = "Sub"
    MUL = "Multiply"
    DIV = "Divide"
    POW = "Power"
    APPLY = "Apply"
    SYMBOL = "Symbol"
    NUMBER = "Number"
    INDEXED = "Indexed"
    DERIVATIVE = "Derivative"
    TENSOR = "Tensor"
    OPERATOR = "Operator"
    COMPOSITION = "Composition"
    UNKNOWN = "Unknown"


SPECIAL_OPERATORS = {
    "laplacian": "Laplacian",
    "nabla2": "Laplacian",
    "box": "dAlembertian",
    "dalembertian": "dAlembertian",
    "grad": "Gradient",
    "div": "Divergence",
    "curl": "Curl",
    "partial": "Partial",
}

# Capital Δ is the fluids Laplacian; lowercase δ stays a free identifier.
_LAPLACIAN_TOKENS = frozenset({"Delta", "laplacian", "nabla2"})

LATEX_MACROS = {
    "nabla": "nabla",
    "partial": "partial",
    "Phi": "Phi",
    "phi": "phi",
    "varphi": "varphi",
    "psi": "psi",
    "Psi": "Psi",
    "lambda": "lambda",
    "Lambda": "Lambda",
    "rho": "rho",
    "pi": "pi",
    "mu": "mu",
    "nu": "nu",
    "alpha": "alpha",
    "beta": "beta",
    "gamma": "gamma",
    "Gamma": "Gamma",
    "delta": "delta",
    "Delta": "Delta",
    "epsilon": "epsilon",
    "theta": "theta",
    "omega": "omega",
    "Omega": "Omega",
    "xi": "xi",
    "Xi": "Xi",
    "sigma": "sigma",
    "kappa": "kappa",
    "ell": "ell",
    "cdot": "*",
    "times": "*",
    "left": "",
    "right": "",
    "mathrm": "",
    "text": "",
    "bar": "bar",
    "hat": "hat",
    "tilde": "tilde",
    "Box": "Box",
    "square": "Box",
    "infty": "infty",
    "sum": "sum",
    "int": "int",
}

UNICODE_MAP = {
    "∇": "nabla",
    "∂": "partial",
    "Φ": "Phi",
    "φ": "phi",
    "ϕ": "varphi",
    "ψ": "psi",
    "Ψ": "Psi",
    "λ": "lambda",
    "Λ": "Lambda",
    "ρ": "rho",
    "π": "pi",
    "μ": "mu",
    "ν": "nu",
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "Γ": "Gamma",
    "δ": "delta",
    "Δ": "Delta",
    "ε": "epsilon",
    "θ": "theta",
    "ω": "omega",
    "Ω": "Omega",
    "κ": "kappa",
    "ξ": "xi",
    "Ξ": "Xi",
    "□": "Box",
    "·": "*",
    "×": "*",
    "∞": "infty",
    "²": "^2",
    "³": "^3",
    "⁻": "^-",
}


@dataclass
class ASTNode:
    kind: NodeKind
    name: str | None = None
    value: float | int | None = None
    children: list["ASTNode"] = field(default_factory=list)
    indices: list[str] = field(default_factory=list)
    source_span: str | None = None

    def walk(self) -> Iterable["ASTNode"]:
        yield self
        for child in self.children:
            yield from child.walk()

    def symbols(self) -> list[str]:
        return [n.name for n in self.walk() if n.kind == NodeKind.SYMBOL and n.name]

    def pretty(self, indent: int = 0) -> str:
        pad = "  " * indent
        label = self.kind.value
        extra = ""
        if self.name:
            extra += f" {self.name}"
        if self.value is not None and self.kind == NodeKind.NUMBER:
            extra += f" {self.value}"
        if self.indices:
            extra += f"_{{{','.join(self.indices)}}}"
        lines = [f"{pad}{label}{extra}"]
        for child in self.children:
            lines.append(child.pretty(indent + 1))
        return "\n".join(lines)


@dataclass
class ParseResult:
    original: str
    tree: ASTNode | None
    tokens: list[str]
    warnings: list[str]
    parser_confidence: float
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.tree is not None and self.error is None


def _normalize(text: str) -> str:
    out = text.strip()
    for src, dst in UNICODE_MAP.items():
        # Space alphabetic replacements so νΔω → nu Delta omega, not nuDeltaomega.
        if dst and dst[0].isalpha():
            out = out.replace(src, f" {dst} ")
        else:
            out = out.replace(src, dst)
    # Prefer explicit Laplacian tokens before / after spaced unicode maps.
    out = out.replace("∇²", "laplacian ")
    out = out.replace(r"\nabla^2", "laplacian ")
    out = out.replace("nabla^2", "laplacian ")
    out = re.sub(r"\bnabla\s*\^\s*2\b", "laplacian ", out)
    # Common glued ASCII forms from CLI smoke inputs.
    out = re.sub(r"\bpartialt\b", "partial_t", out, flags=re.IGNORECASE)
    out = re.sub(r"\bnablap\b", "nabla p", out, flags=re.IGNORECASE)
    out = re.sub(r"\bDelta([A-Za-z])\b", r"Delta \1", out)
    out = re.sub(r"\blaplacian([A-Za-z])\b", r"laplacian \1", out, flags=re.IGNORECASE)
    out = re.sub(r"\bdiv\b", "div ", out, flags=re.IGNORECASE)
    out = re.sub(r"\\([A-Za-z]+)", lambda m: LATEX_MACROS.get(m.group(1), m.group(1)) + " ", out)
    out = out.replace("{", " ").replace("}", " ")
    out = re.sub(r"\s+", " ", out)
    return out.strip()


_TOKEN_RE = re.compile(
    r"""
    (\d+\.\d+|\d+)                # number
    | ([A-Za-z][A-Za-z0-9]*)      # identifier
    | (==|=|\+|\-|\*|/|\^|\_)     # operators
    | ([\(\)\[\],])               # grouping
    | (\S)                        # leftover
    """,
    re.VERBOSE,
)

# Multi-letter identifiers that must not be split into implicit products.
_ATOMIC_IDENTIFIERS = frozenset(LATEX_MACROS) | frozenset(SPECIAL_OPERATORS) | {
    "Phi",
    "phi",
    "varphi",
    "psi",
    "Psi",
    "rho",
    "pi",
    "lambda",
    "Lambda",
    "nabla",
    "laplacian",
    "Box",
    "partial",
    "kappa",
    "infty",
    "munu",
    "barh",
    "hbar",
    "Delta",
    "omega",
    "Omega",
    "nu",
}


def _expand_identifier(tok: str) -> list[str]:
    if tok in _ATOMIC_IDENTIFIERS or not tok.isalpha():
        return [tok]
    if tok.islower() and 2 <= len(tok) <= 4:
        return list(tok)
    for size in range(len(tok) - 1, 0, -1):
        head, tail = tok[:size], tok[size:]
        if tail in _ATOMIC_IDENTIFIERS and (size == 1 or head in _ATOMIC_IDENTIFIERS):
            return [head, tail]
    return [tok]


def tokenize(text: str) -> list[str]:
    normalized = _normalize(text)
    raw = [m.group(0) for m in _TOKEN_RE.finditer(normalized) if m.group(0).strip()]
    tokens: list[str] = []
    for tok in raw:
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", tok):
            tokens.extend(_expand_identifier(tok))
        else:
            tokens.append(tok)
    return tokens


class _Parser:
    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.i = 0

    def peek(self) -> str | None:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self, expected: str | None = None) -> str:
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        if expected is not None and tok != expected:
            raise ValueError(f"expected {expected!r}, got {tok!r}")
        self.i += 1
        return tok

    def parse(self) -> ASTNode:
        node = self.parse_equality()
        if self.peek() is not None:
            # Keep leftover tokens as a soft warning by wrapping.
            rest = self.tokens[self.i :]
            extra = ASTNode(kind=NodeKind.UNKNOWN, name=" ".join(rest))
            return ASTNode(kind=NodeKind.COMPOSITION, children=[node, extra])
        return node

    def parse_equality(self) -> ASTNode:
        left = self.parse_add()
        if self.peek() in {"=", "=="}:
            self.take()
            right = self.parse_add()
            return ASTNode(kind=NodeKind.EQUALITY, children=[left, right])
        return left

    def parse_add(self) -> ASTNode:
        node = self.parse_mul()
        while self.peek() in {"+", "-"}:
            op = self.take()
            rhs = self.parse_mul()
            kind = NodeKind.ADD if op == "+" else NodeKind.SUB
            node = ASTNode(kind=kind, children=[node, rhs])
        return node

    def parse_mul(self) -> ASTNode:
        node = self.parse_pow()
        while True:
            nxt = self.peek()
            if nxt in {"*", "/"}:
                op = self.take()
                rhs = self.parse_pow()
                kind = NodeKind.MUL if op == "*" else NodeKind.DIV
                node = ASTNode(kind=kind, children=[node, rhs])
                continue
            if self._starts_implicit_mul(nxt):
                rhs = self.parse_pow()
                node = ASTNode(kind=NodeKind.MUL, children=[node, rhs])
                continue
            break
        return node

    def _starts_implicit_mul(self, tok: str | None) -> bool:
        if tok is None:
            return False
        if tok in {")", "]", ",", "+", "-", "=", "==", "*", "/", "^", "_"}:
            return False
        return True

    def parse_pow(self) -> ASTNode:
        node = self.parse_postfix()
        if self.peek() == "^":
            self.take()
            exp = self.parse_pow()
            if (
                node.kind == NodeKind.SYMBOL
                and node.name == "nabla"
                and exp.kind == NodeKind.NUMBER
                and exp.value == 2
            ):
                return ASTNode(
                    kind=NodeKind.OPERATOR,
                    name="Laplacian",
                    children=[],
                )
            return ASTNode(kind=NodeKind.POW, children=[node, exp])
        return node

    def parse_postfix(self) -> ASTNode:
        node = self.parse_primary()
        while self.peek() == "_":
            self.take()
            idx = self.parse_primary()
            names = _flatten_index_names(idx)
            existing = list(node.indices) if node.kind == NodeKind.INDEXED else []
            node = ASTNode(
                kind=NodeKind.INDEXED,
                name=node.name,
                children=[node, idx],
                indices=existing + names,
            )
        return node

    def parse_primary(self) -> ASTNode:
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        if tok == "(":
            self.take()
            node = self.parse_equality()
            if self.peek() == ")":
                self.take()
            return node
        if tok == "-":
            self.take()
            inner = self.parse_pow()
            return ASTNode(
                kind=NodeKind.MUL,
                children=[ASTNode(kind=NodeKind.NUMBER, value=-1), inner],
            )
        if re.fullmatch(r"\d+\.\d+|\d+", tok):
            self.take()
            value: float | int
            value = float(tok) if "." in tok else int(tok)
            return ASTNode(kind=NodeKind.NUMBER, value=value, name=tok)
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", tok):
            self.take()
            if tok == "nabla":
                return self._parse_nabla_operator()
            if tok in _LAPLACIAN_TOKENS or tok.lower() in {"laplacian", "nabla2"}:
                operand = None
                if self._starts_implicit_mul(self.peek()) or self.peek() == "(":
                    operand = self.parse_pow()
                children = [operand] if operand is not None else []
                return ASTNode(
                    kind=NodeKind.APPLY,
                    name="Laplacian",
                    children=children,
                )
            if tok.lower() in SPECIAL_OPERATORS:
                op_name = SPECIAL_OPERATORS[tok.lower()]
                operand = None
                if self._starts_implicit_mul(self.peek()) or self.peek() == "(":
                    operand = self.parse_pow()
                children = [operand] if operand is not None else []
                if op_name == "Laplacian":
                    return ASTNode(
                        kind=NodeKind.APPLY,
                        name="Laplacian",
                        children=children,
                    )
                return ASTNode(
                    kind=NodeKind.APPLY,
                    name=op_name,
                    children=children,
                )
            return ASTNode(kind=NodeKind.SYMBOL, name=tok)
        self.take()
        return ASTNode(kind=NodeKind.UNKNOWN, name=tok)

    def _parse_nabla_operator(self) -> ASTNode:
        """Parse ∇·u as Divergence and ∇p as Gradient; bare ∇ stays a symbol."""
        nxt = self.peek()
        if nxt == "*":
            self.take()
            operand = self.parse_pow()
            return ASTNode(
                kind=NodeKind.APPLY,
                name="Divergence",
                children=[operand],
            )
        if nxt is not None and self._starts_implicit_mul(nxt) and nxt not in {
            "*",
            "/",
            "+",
            "-",
            "=",
            "==",
            ")",
            "]",
            ",",
            "^",
            "_",
        }:
            # Avoid treating (u·∇) as Gradient: after nabla the next token is ')'.
            operand = self.parse_pow()
            return ASTNode(
                kind=NodeKind.APPLY,
                name="Gradient",
                children=[operand],
            )
        return ASTNode(kind=NodeKind.SYMBOL, name="nabla")


def _flatten_index_names(node: ASTNode) -> list[str]:
    if node.kind == NodeKind.SYMBOL and node.name:
        # Common packed indices: mu nu written as munu after latex flatten.
        name = node.name
        if name in {"munu", "mu_nu"}:
            return ["mu", "nu"]
        if len(name) == 2 and name.isalpha() and name.islower():
            return [name[0], name[1]]
        return [name]
    if node.kind == NodeKind.NUMBER and node.name:
        return [node.name]
    names: list[str] = []
    for child in node.children:
        names.extend(_flatten_index_names(child))
    return names or ([node.name] if node.name else [])


def parse_expression(text: str) -> ParseResult:
    """Parse ``text`` into an AST. Role inference is intentionally absent."""
    warnings: list[str] = []
    if not text or not str(text).strip():
        return ParseResult(
            original=text,
            tree=None,
            tokens=[],
            warnings=["empty expression"],
            parser_confidence=0.0,
            error="empty expression",
        )
    tokens = tokenize(text)
    try:
        tree = _Parser(tokens).parse()
    except ValueError as exc:
        return ParseResult(
            original=text,
            tree=None,
            tokens=tokens,
            warnings=[str(exc)],
            parser_confidence=0.15,
            error=str(exc),
        )
    confidence = 0.9 if tree.kind != NodeKind.UNKNOWN else 0.4
    if any(n.kind == NodeKind.UNKNOWN for n in tree.walk()):
        warnings.append("parser retained one or more unrecognized tokens")
        confidence = min(confidence, 0.55)
    return ParseResult(
        original=text,
        tree=tree,
        tokens=tokens,
        warnings=warnings,
        parser_confidence=confidence,
    )


def find_equalities(tree: ASTNode) -> list[ASTNode]:
    return [n for n in tree.walk() if n.kind == NodeKind.EQUALITY]


def looks_like_laplacian_poisson(tree: ASTNode) -> bool:
    if tree.kind != NodeKind.EQUALITY or len(tree.children) != 2:
        return False
    left, right = tree.children
    has_lap = any(
        (n.kind == NodeKind.APPLY and n.name == "Laplacian")
        or (n.kind == NodeKind.OPERATOR and n.name == "Laplacian")
        for n in left.walk()
    )
    names = {s.lower() for s in right.symbols()}
    return has_lap and ("rho" in names or "g" in names)
