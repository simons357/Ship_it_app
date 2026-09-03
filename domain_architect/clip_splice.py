"""Clip-splice: align two almost-identical equations without deleting the delta.

If two expressions share a core, Domain Architect may clip the excess so the
cores match. The clipped remainder is not garbage. It gets an ID, a
measurement, and a kind. Silent merge is forbidden.

This is a laboratory operation. It does not prove Navier–Stokes or RH.
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable

from .parser import ASTNode, NodeKind, parse_expression
from .schema import CANONICAL_SFE_STATUS


EXTENSION_SYMBOLS = frozenset(
    {
        "epsilon",
        "Lambda",
        "Xi",
        "xi",
        "F",
        "f",
        "S",
        "forcing",
    }
)

GLUE_MARKERS = (
    "unified",
    "millennium",
    "proved",
    "sfe",
    "clay",
)


@dataclass(frozen=True)
class Term:
    side: str
    key: str
    expression: str
    symbols: tuple[str, ...]
    kind: str


@dataclass
class Clip:
    clip_id: str
    side: str
    source: str
    expression: str
    symbols: list[str]
    term_count: int
    kind: str
    independently_specifiable: bool
    discarded: bool
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ClipSplice:
    operation: str
    left: str
    right: str
    alignment: str
    overlap_jaccard: float
    shared_core: str
    left_clips: list[Clip] = field(default_factory=list)
    right_clips: list[Clip] = field(default_factory=list)
    cores_made_same: bool = False
    silent_merge: bool = False
    weld_lemma_required: bool = False
    message: str = ""
    canonical_sfe_status: str = CANONICAL_SFE_STATUS

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["left_clips"] = [c.to_dict() for c in self.left_clips]
        payload["right_clips"] = [c.to_dict() for c in self.right_clips]
        return payload


def _pretty(node: ASTNode) -> str:
    if node.kind == NodeKind.SYMBOL:
        return node.name or "?"
    if node.kind == NodeKind.NUMBER:
        return str(node.value)
    if node.kind == NodeKind.ADD:
        return " + ".join(_pretty(c) for c in node.children)
    if node.kind == NodeKind.SUB:
        if len(node.children) == 2:
            return f"{_pretty(node.children[0])} - {_pretty(node.children[1])}"
    if node.kind == NodeKind.MUL:
        return "*".join(_pretty(c) for c in node.children)
    if node.kind == NodeKind.DIV and len(node.children) == 2:
        return f"({_pretty(node.children[0])})/({_pretty(node.children[1])})"
    if node.kind == NodeKind.POW and len(node.children) == 2:
        return f"{_pretty(node.children[0])}^{_pretty(node.children[1])}"
    if node.kind == NodeKind.APPLY:
        args = ", ".join(_pretty(c) for c in node.children)
        return f"{node.name or 'Apply'}({args})"
    if node.kind == NodeKind.OPERATOR:
        args = ", ".join(_pretty(c) for c in node.children)
        return f"{node.name or 'Op'}({args})"
    if node.kind == NodeKind.INDEXED:
        base = _pretty(node.children[0]) if node.children else (node.name or "idx")
        idx = ",".join(node.indices) if node.indices else ""
        return f"{base}_{{{idx}}}" if idx else base
    if node.kind == NodeKind.EQUALITY and len(node.children) == 2:
        return f"{_pretty(node.children[0])} = {_pretty(node.children[1])}"
    if node.kind == NodeKind.DERIVATIVE:
        return "d(" + ", ".join(_pretty(c) for c in node.children) + ")"
    return node.name or node.kind.value


def _term_key(node: ASTNode) -> str:
    bits = [node.kind.value, node.name or "", str(node.value) if node.value is not None else ""]
    if node.indices:
        bits.append("i:" + ",".join(node.indices))
    bits.extend(_term_key(c) for c in node.children)
    return "|".join(bits)


def _additive_terms(node: ASTNode) -> list[ASTNode]:
    if node.kind == NodeKind.ADD:
        out: list[ASTNode] = []
        for child in node.children:
            out.extend(_additive_terms(child))
        return out
    if node.kind == NodeKind.SUB and len(node.children) == 2:
        return _additive_terms(node.children[0]) + _additive_terms(node.children[1])
    return [node]


def _collect_terms(tree: ASTNode) -> list[Term]:
    if tree.kind == NodeKind.EQUALITY and len(tree.children) == 2:
        terms: list[Term] = []
        for side, child in (("lhs", tree.children[0]), ("rhs", tree.children[1])):
            for piece in _additive_terms(child):
                terms.append(
                    Term(
                        side=side,
                        key=f"{side}:{_term_key(piece)}",
                        expression=_pretty(piece),
                        symbols=tuple(sorted({s for s in piece.symbols() if s})),
                        kind=piece.kind.value,
                    )
                )
        return terms
    return [
        Term(
            side="expr",
            key=f"expr:{_term_key(piece)}",
            expression=_pretty(piece),
            symbols=tuple(sorted({s for s in piece.symbols() if s})),
            kind=piece.kind.value,
        )
        for piece in _additive_terms(tree)
    ]


def _classify_clip(term: Term, source_text: str) -> tuple[str, str, bool]:
    blob = (term.expression + " " + source_text).lower()
    names = {s.lower() for s in term.symbols}
    if any(m in blob for m in GLUE_MARKERS):
        return (
            "GLUE",
            "Prize or unification language in the remainder. Keep the ID; do not weld.",
            True,
        )
    if "epsilon" in names or "divergence" in blob:
        return (
            "DYNAMICS_TERM",
            "Extra evolution term. Independently specifiable. Not zero. Not A⇒B.",
            True,
        )
    if "Lambda" in term.symbols:
        return (
            "EXTENSION_ROLE",
            "Extra linear/source-like term. Record as its own component.",
            True,
        )
    if not term.symbols:
        return ("TEXTURE", "Numeric or operator-only remainder. Still ID'd, not discarded.", False)
    return (
        "UNKNOWN",
        "Remainder isolated. Measure it before calling the equations the same.",
        True,
    )


def _clip_id(term: Term) -> str:
    digest = hashlib.sha1(term.key.encode("utf-8")).hexdigest()[:8].upper()
    return f"CLIP-{term.side.upper()}-{digest}"


def _jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    left, right = set(a), set(b)
    if not left and not right:
        return 1.0
    return len(left & right) / len(left | right)


def _shared_pretty(common: list[Term]) -> str:
    lhs = [t.expression for t in common if t.side == "lhs"]
    rhs = [t.expression for t in common if t.side == "rhs"]
    other = [t.expression for t in common if t.side not in {"lhs", "rhs"}]
    if lhs or rhs:
        left_s = " + ".join(lhs) if lhs else "0"
        right_s = " + ".join(rhs) if rhs else "0"
        return f"{left_s} = {right_s}"
    return " + ".join(other) if other else "(empty core)"


def clip_splice(left: str, right: str) -> ClipSplice:
    """Clip excess so cores match; ID and measure every remainder."""
    parsed_l = parse_expression(left)
    parsed_r = parse_expression(right)
    if not parsed_l.ok or parsed_l.tree is None:
        return ClipSplice(
            operation="CLIP",
            left=left,
            right=right,
            alignment="INSUFFICIENT_INFORMATION",
            overlap_jaccard=0.0,
            shared_core="",
            message=f"Left parse failed: {parsed_l.error}",
        )
    if not parsed_r.ok or parsed_r.tree is None:
        return ClipSplice(
            operation="CLIP",
            left=left,
            right=right,
            alignment="INSUFFICIENT_INFORMATION",
            overlap_jaccard=0.0,
            shared_core="",
            message=f"Right parse failed: {parsed_r.error}",
        )

    terms_l = _collect_terms(parsed_l.tree)
    terms_r = _collect_terms(parsed_r.tree)
    keys_l = {t.key for t in terms_l}
    keys_r = {t.key for t in terms_r}
    overlap = _jaccard(keys_l, keys_r)
    common_keys = keys_l & keys_r
    common = [t for t in terms_l if t.key in common_keys]
    left_only = [t for t in terms_l if t.key not in keys_r]
    right_only = [t for t in terms_r if t.key not in keys_l]

    def make_clips(only: list[Term], source: str) -> list[Clip]:
        clips: list[Clip] = []
        for term in only:
            kind, notes, independent = _classify_clip(term, source)
            clips.append(
                Clip(
                    clip_id=_clip_id(term),
                    side=term.side,
                    source=source,
                    expression=term.expression,
                    symbols=list(term.symbols),
                    term_count=1,
                    kind=kind,
                    independently_specifiable=independent,
                    discarded=False,
                    notes=notes,
                )
            )
        return clips

    left_clips = make_clips(left_only, "left")
    right_clips = make_clips(right_only, "right")
    all_clips = left_clips + right_clips
    glue = any(c.kind == "GLUE" for c in all_clips)
    dynamics = any(c.kind == "DYNAMICS_TERM" for c in all_clips)
    cores_same = overlap == 1.0 and not all_clips

    if glue:
        alignment = "REFUSED"
        message = "Clip contains glue language. Cores are not merged."
        cores_made_same = False
        weld = False
    elif cores_same:
        alignment = "IDENTICAL"
        message = "No clip. Expressions already share the same term set."
        cores_made_same = True
        weld = False
    elif common and all_clips:
        alignment = "CLIPPED"
        cores_made_same = True
        weld = dynamics or any(c.independently_specifiable for c in all_clips)
        message = (
            "Shared core aligned. Excess clipped, ID'd, and measured. "
            "The clip is a component, not trash. Making the cores the same "
            "does not make the original equations the same."
        )
    elif overlap > 0:
        alignment = "PARTIAL"
        cores_made_same = False
        weld = True
        message = "Some overlap, not enough to call the cores the same."
    else:
        alignment = "INCOMPATIBLE"
        cores_made_same = False
        weld = False
        message = "No shared additive terms. Do not clip into a fake identity."

    return ClipSplice(
        operation="CLIP",
        left=left,
        right=right,
        alignment=alignment,
        overlap_jaccard=round(overlap, 4),
        shared_core=_shared_pretty(common),
        left_clips=left_clips,
        right_clips=right_clips,
        cores_made_same=cores_made_same,
        silent_merge=False,
        weld_lemma_required=weld,
        message=message,
    )


def format_clip_splice(result: ClipSplice) -> str:
    lines = [
        f"CLIP {result.alignment}  jaccard={result.overlap_jaccard}",
        f"Canonical SFE status: {result.canonical_sfe_status}.",
        f"Shared core: {result.shared_core or '(none)'}",
        f"Cores made the same: {result.cores_made_same}",
        "Silent merge: no",
        result.message,
    ]
    clips = result.left_clips + result.right_clips
    if not clips:
        lines.append("Clips: none")
        return "\n".join(lines)
    lines.append(f"Clips: {len(clips)} (all retained)")
    for clip in clips:
        lines.append(
            f"  {clip.clip_id}  [{clip.kind}]  side={clip.side}  "
            f"specifiable={clip.independently_specifiable}  discarded={clip.discarded}"
        )
        lines.append(f"      {clip.expression}")
        lines.append(f"      symbols={clip.symbols}")
        lines.append(f"      {clip.notes}")
    return "\n".join(lines)
