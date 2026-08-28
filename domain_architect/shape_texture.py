"""Shape–Texture ontology for Domain Architect.

Jonathan Simons insight (formalized): a math object is a SHAPE (invariant role
skeleton / compatibility class) plus TEXTURE (notation, domain chart, hypothesis
tags). DA compares SHAPES first, then flags texture mismatches. Navigation only —
not proof.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from .audit import audit_expression
from .hb_loop import BOOK_REQUIREMENTS, build_hb_map, compare_reports, infer_book
from .report import AuditReport
from .schema import ROLE_GLOSSARY
from .theory_splicer import TheoryBook, get_book, load_millennium_registry


class ShapeMatchVerdict(str, Enum):
    COMPATIBLE = "COMPATIBLE"
    INCOMPATIBLE = "INCOMPATIBLE"
    SAME_SHAPE_DIFFERENT_TEXTURE = "SAME_SHAPE_DIFFERENT_TEXTURE"


# Organizational five-finger roles (HB) ↔ FRA symbols
FINGER_TO_SYMBOL: dict[str, str] = {
    "admissibility": "P",
    "interaction": "H",
    "coupling": "H",
    "state": "ψ",
    "scale_response": "λ",
    "realized_output": "Φ",
    "environment": "E",
    "source": "S",
    "evolution_operator": "D",
    "geometry": "g",
    "boundary": "ℬ",
}

SYMBOL_TO_FINGER: dict[str, str] = {
    "P": "admissibility",
    "H": "interaction",
    "ψ": "state",
    "psi": "state",
    "λ": "scale_response",
    "lambda": "scale_response",
    "Φ": "realized_output",
    "Phi": "realized_output",
    "E": "environment",
}

DOMAIN_PATTERNS: list[tuple[str, str]] = [
    (r"T\^?3|T³|torus", "T³"),
    (r"R\^?3|ℝ³|R3", "R³"),
    (r"lattice|arithmetic|Q6|prime", "arithmetic_lattice"),
    (r"black.?hole|bh.?spectrum|ringdown", "BH_spectrum"),
    (r"critical.?line|zeta|RH", "RH_operator"),
]

NOTATION_PATTERNS: list[tuple[str, str]] = [
    (r"partial_t|nabla|Delta|div\s+u", "NS_PDE"),
    (r"lambda_(min|max)|tilde_H_N|shell.?helical", "shell_helical_operator"),
    (r"J\(t\)|X\(t\)|Pi_\{?j", "SND_shell_flux"),
    (r"zeta|L\(s|critical", "RH_zeta"),
    (r"Q6|arithmetic", "Q6_lattice"),
    (r"<=>|Clay Statement", "Clay_packaging"),
    (r"bootstrap|M=\|\|u0\|\|", "bootstrap_lemma"),
]

HYPOTHESIS_TAGS: list[tuple[str, str]] = [
    (r"X\s*<=\s*M|X≤M", "X<=M"),
    (r"rho\s*<=\s*rho_0|ρ≤ρ", "rho<=rho_0"),
    (r"inf.*J.*X|c_\*", "SND-U_or_floor"),
    (r"unconditional", "unconditional_claim"),
    (r"Clay Statement B|Clay B", "Clay_B"),
    (r"hypothesis|assume", "hypothesis_framing"),
    (r"epsilon|hyperdissipat|Q1", "Q1_hyperdissipation"),
    (r"5\s*[×x]\s*safety|Bypass Lemma", "bypass_lemma"),
]


@dataclass
class MathShape:
    """Invariant structural skeleton — roles, fingers, compatibility class."""

    shape_id: str
    source: str
    fingers: dict[str, str]  # P, H, ψ, λ, Φ, E → role name
    role_topology: list[str]
    compatibility_class: str  # domain book / Q6 / etc.
    dependency_hints: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MathTexture:
    """Surface representation — notation chart, domain, hypothesis tags."""

    source: str
    notation: str
    domain: str
    hypothesis_tags: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    book_id: str = ""
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MathObject:
    """Shape + texture bundle."""

    object_id: str
    label: str
    shape: MathShape
    texture: MathTexture
    millennium_tags: list[str] = field(default_factory=list)
    status: str = "HYPOTHESIS"  # KEEP | HYPOTHESIS | PARK | REFERENCE
    source_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "label": self.label,
            "shape": self.shape.to_dict(),
            "texture": self.texture.to_dict(),
            "millennium_tags": self.millennium_tags,
            "status": self.status,
            "source_refs": self.source_refs,
        }


@dataclass
class ShapeMatchResult:
    verdict: ShapeMatchVerdict
    shared_fingers: list[str]
    only_a: list[str]
    only_b: list[str]
    texture_delta: list[str]
    statement: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["verdict"] = self.verdict.value
        return d


@dataclass
class TextureTranslation:
    """Hypothesis-only chart change — not an automatic proof."""

    from_source: str
    to_source: str
    candidate_rewrites: list[str]
    weld_required: str
    hypothesis_only: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class NavigationReport:
    """One Millennium problem at a time — library objects sharing shape."""

    millennium_id: str
    target_shape: MathShape | None
    matching_objects: list[dict[str, Any]]
    texture_mismatches: list[dict[str, Any]]
    missing_welds: list[str]
    coverage_gaps: list[str]
    statement: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "millennium_id": self.millennium_id,
            "target_shape": self.target_shape.to_dict() if self.target_shape else None,
            "matching_objects": self.matching_objects,
            "texture_mismatches": self.texture_mismatches,
            "missing_welds": self.missing_welds,
            "coverage_gaps": self.coverage_gaps,
            "statement": self.statement,
        }


def _stable_shape_id(fingers: dict[str, str], compat: str, roles: list[str]) -> str:
    payload = json.dumps(
        {"fingers": sorted(fingers.items()), "class": compat, "roles": sorted(roles)},
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode()).hexdigest()[:12]
    finger_str = "".join(k for k in ("P", "H", "ψ", "λ", "Φ", "E") if k in fingers)
    return f"shape-{compat}-{finger_str or 'generic'}-{digest}"


def _roles_to_fingers(roles: list[str]) -> dict[str, str]:
    fingers: dict[str, str] = {}
    for role in roles:
        sym = FINGER_TO_SYMBOL.get(role)
        if sym and sym not in fingers:
            fingers[sym] = role
    return fingers


def _extract_from_report(report: AuditReport, source: str) -> tuple[MathShape, MathTexture]:
    hb = build_hb_map(report)
    book = infer_book(report)
    role_topology = sorted(
        {str(r.get("candidate_role", "")) for r in report.role_assignments}
        - {"", "unresolved", "unresolved_left_factor", "unresolved_right_factor"}
    )
    if not role_topology and hb.roles:
        role_topology = sorted(hb.roles.keys())
    fingers = _roles_to_fingers(role_topology)
    # Fill from book requirements when audit is sparse
    req = BOOK_REQUIREMENTS.get(book, {})
    for role in req.get("roles", set()):
        sym = FINGER_TO_SYMBOL.get(role)
        if sym and sym not in fingers:
            fingers[sym] = role

    deps = list(hb.extras) + list(report.extra_structures or [])
    shape = MathShape(
        shape_id=_stable_shape_id(fingers, book, role_topology),
        source=source,
        fingers=fingers,
        role_topology=role_topology,
        compatibility_class=book,
        dependency_hints=sorted(set(deps)),
        notes=["Shape = invariant role skeleton; not a proof claim."],
    )
    texture = _texture_from_text(source, report.input_expression, book_id=book)
    return shape, texture


def _texture_from_text(source: str, expression: str, *, book_id: str = "") -> MathTexture:
    text = f"{source} {expression}".lower()
    domain = "unspecified"
    for pat, label in DOMAIN_PATTERNS:
        if re.search(pat, text, re.I):
            domain = label
            break

    notation = "generic"
    for pat, label in NOTATION_PATTERNS:
        if re.search(pat, expression, re.I):
            notation = label
            break

    tags: list[str] = []
    for pat, tag in HYPOTHESIS_TAGS:
        if re.search(pat, text, re.I):
            tags.append(tag)

    symbols = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|λ|ψ|Φ|π", expression)
    return MathTexture(
        source=source,
        notation=notation,
        domain=domain,
        hypothesis_tags=sorted(set(tags)),
        symbols=sorted(set(symbols))[:20],
        book_id=book_id,
        notes=["Texture = coordinate chart; same shape may wear many textures."],
    )


def extract_shape(source: str) -> MathShape:
    """Extract shape from expression string or theory book id."""
    source = source.strip()
    try:
        book = get_book(source.upper())
        expr = book.expression or source
        roles = list(book.roles)
        if not roles:
            for c in book.active_claims():
                roles.extend(c.roles)
        fingers = _roles_to_fingers(sorted(set(roles)))
        compat = book.book_id if book.millennium_id else infer_book(
            audit_expression(expr)
        )
        # Prefer hb_loop book id when available
        report = audit_expression(expr)
        compat = infer_book(report) if infer_book(report) != "generic" else book.book_id
        deps = list(book.terms)
        return MathShape(
            shape_id=_stable_shape_id(fingers, compat, sorted(set(roles))),
            source=source,
            fingers=fingers,
            role_topology=sorted(set(roles)),
            compatibility_class=compat,
            dependency_hints=deps,
            notes=[f"Extracted from theory book {book.book_id}."],
        )
    except KeyError:
        pass

    report = audit_expression(source)
    shape, _ = _extract_from_report(report, source)
    return shape


def extract_texture(source: str) -> MathTexture:
    """Extract texture (notation, domain, hypothesis tags) from source."""
    source = source.strip()
    try:
        book = get_book(source.upper())
        expr = book.expression or source
        tex = _texture_from_text(source, expr, book_id=book.book_id)
        tex.notes.append(f"Book {book.book_id} status={book.status}")
        return tex
    except KeyError:
        pass

    report = audit_expression(source)
    _, texture = _extract_from_report(report, source)
    return texture


def extract_object(source: str, *, label: str = "", status: str = "HYPOTHESIS") -> MathObject:
    """Bundle shape + texture into one library object."""
    shape = extract_shape(source)
    texture = extract_texture(source)
    obj_id = f"obj-{shape.shape_id[:24]}"
    return MathObject(
        object_id=obj_id,
        label=label or source[:60],
        shape=shape,
        texture=texture,
        status=status,
        source_refs=[source],
    )


def shape_match(a: str, b: str) -> ShapeMatchResult:
    """Compare two sources: shapes first, then textures."""
    shape_a = extract_shape(a)
    shape_b = extract_shape(b)
    tex_a = extract_texture(a)
    tex_b = extract_texture(b)

    fingers_a = set(shape_a.fingers)
    fingers_b = set(shape_b.fingers)
    shared = sorted(fingers_a & fingers_b)
    only_a = sorted(fingers_a - fingers_b)
    only_b = sorted(fingers_b - fingers_a)

    roles_a = set(shape_a.role_topology)
    roles_b = set(shape_b.role_topology)
    shared_roles = roles_a & roles_b
    union_roles = roles_a | roles_b
    role_overlap_ratio = len(shared_roles) / len(union_roles) if union_roles else 0.0

    texture_delta: list[str] = []
    if tex_a.notation != tex_b.notation:
        texture_delta.append(f"notation: {tex_a.notation} vs {tex_b.notation}")
    if tex_a.domain != tex_b.domain:
        texture_delta.append(f"domain: {tex_a.domain} vs {tex_b.domain}")
    tag_diff = set(tex_a.hypothesis_tags) ^ set(tex_b.hypothesis_tags)
    if tag_diff:
        texture_delta.append(f"hypothesis_tags: {sorted(tag_diff)}")

    classes_differ = (
        shape_a.compatibility_class != shape_b.compatibility_class
        and shape_a.compatibility_class != "generic"
        and shape_b.compatibility_class != "generic"
    )

    # Different compatibility classes with weak role overlap → incompatible books
    if classes_differ and role_overlap_ratio < 0.65:
        return ShapeMatchResult(
            verdict=ShapeMatchVerdict.INCOMPATIBLE,
            shared_fingers=shared,
            only_a=only_a,
            only_b=only_b,
            texture_delta=texture_delta,
            statement=(
                f"INCOMPATIBLE: {shape_a.compatibility_class} vs "
                f"{shape_b.compatibility_class} — different compatibility classes "
                f"(role overlap {role_overlap_ratio:.0%})."
            ),
            details={"shape_a": shape_a.to_dict(), "shape_b": shape_b.to_dict()},
        )

    # Incompatible books with no shared organizational roles
    if classes_differ and not shared_roles and len(shared) < 2:
        return ShapeMatchResult(
            verdict=ShapeMatchVerdict.INCOMPATIBLE,
            shared_fingers=shared,
            only_a=only_a,
            only_b=only_b,
            texture_delta=texture_delta,
            statement=(
                f"INCOMPATIBLE: {shape_a.compatibility_class} vs "
                f"{shape_b.compatibility_class} — different compatibility classes "
                f"with insufficient shared role topology."
            ),
            details={"shape_a": shape_a.to_dict(), "shape_b": shape_b.to_dict()},
        )

    same_shape = (
        shared_roles
        and len(shared_roles) >= max(1, min(len(roles_a), len(roles_b)) // 2)
    ) or (len(shared) >= 3)

    if same_shape and texture_delta:
        return ShapeMatchResult(
            verdict=ShapeMatchVerdict.SAME_SHAPE_DIFFERENT_TEXTURE,
            shared_fingers=shared,
            only_a=only_a,
            only_b=only_b,
            texture_delta=texture_delta,
            statement=(
                "SAME_SHAPE_DIFFERENT_TEXTURE: shared role skeleton but different "
                f"surface charts ({'; '.join(texture_delta[:3])}). "
                "Object is there — weld lemma may translate texture."
            ),
            details={"shape_a": shape_a.to_dict(), "shape_b": shape_b.to_dict()},
        )

    if same_shape or len(shared) >= 2:
        return ShapeMatchResult(
            verdict=ShapeMatchVerdict.COMPATIBLE,
            shared_fingers=shared,
            only_a=only_a,
            only_b=only_b,
            texture_delta=texture_delta,
            statement=(
                f"COMPATIBLE: shared fingers {shared} / roles {sorted(shared_roles)}."
            ),
            details={"shape_a": shape_a.to_dict(), "shape_b": shape_b.to_dict()},
        )

    return ShapeMatchResult(
        verdict=ShapeMatchVerdict.INCOMPATIBLE,
        shared_fingers=shared,
        only_a=only_a,
        only_b=only_b,
        texture_delta=texture_delta,
        statement="INCOMPATIBLE: insufficient shared shape skeleton.",
        details={"shape_a": shape_a.to_dict(), "shape_b": shape_b.to_dict()},
    )


def texture_translate(a: str, b: str) -> TextureTranslation:
    """Hypothesis-only candidate chart change between two textures."""
    match = shape_match(a, b)
    tex_a = extract_texture(a)
    tex_b = extract_texture(b)
    rewrites: list[str] = []
    notes: list[str] = ["Hypothesis only — DA does not perform automatic proof."]

    if match.verdict == ShapeMatchVerdict.INCOMPATIBLE:
        rewrites.append("No chart change recommended — shapes incompatible.")
        weld = "refuse_splice"
    elif match.verdict == ShapeMatchVerdict.SAME_SHAPE_DIFFERENT_TEXTURE:
        if "SND_shell_flux" in (tex_a.notation, tex_b.notation) and (
            "shell_helical_operator" in (tex_a.notation, tex_b.notation)
        ):
            rewrites.append(
                "Candidate: map J/X shell-flux chart ↔ λ_min/λ_max shell-helical "
                "operator chart via Bypass Lemma normalization (tilde_H_N, Sigma(t))."
            )
            notes.append("Tweet conflation: J/X ≠ λ_min/λ_max without explicit weld.")
        if tex_a.domain != tex_b.domain and tex_a.domain != "unspecified":
            rewrites.append(
                f"Domain chart: {tex_a.domain} → {tex_b.domain} requires explicit "
                "compactness / limit lemma (not automatic)."
            )
        if "X<=M" in tex_a.hypothesis_tags or "X<=M" in tex_b.hypothesis_tags:
            rewrites.append(
                "Bootstrap-M weld: derive M=M(||u0||_{H^1}) before feeding Theorem H."
            )
        weld = "explicit_weld_lemma_required"
    else:
        rewrites.append("Textures align on shared shape — splice may proceed with audit.")
        weld = "compatible_splice"

    if not rewrites:
        rewrites.append(
            f"Compare notation {tex_a.notation} vs {tex_b.notation}; "
            "record substitution map in registry before splice."
        )

    return TextureTranslation(
        from_source=a,
        to_source=b,
        candidate_rewrites=rewrites,
        weld_required=weld,
        hypothesis_only=True,
        notes=notes,
    )


def navigate_millennium(
    millennium_id: str,
    *,
    manifest: list[MathObject] | None = None,
) -> NavigationReport:
    """List library objects sharing shape with target Millennium problem."""
    from .library_index import load_manifest, scan_library

    reg = load_millennium_registry()
    prob = reg["problems"].get(millennium_id.upper())
    if not prob:
        raise KeyError(f"unknown millennium problem: {millennium_id}")

    objects = manifest or load_manifest().get("objects", [])
    if not objects:
        scanned = scan_library()
        objects = scanned.get("objects", [])

    # Build target shape from primary books
    target_books = prob.get("books", [])[:3]
    target_shapes: list[MathShape] = []
    for raw in target_books:
        bid = raw.get("book_id", "")
        if bid:
            try:
                target_shapes.append(extract_shape(bid))
            except Exception:
                pass

    mid = prob.get("id", millennium_id.upper())
    tagged = [
        o for o in objects
        if mid in (o.get("millennium_tags") or [])
        or any(mid in str(t) for t in (o.get("millennium_tags") or []))
    ]

    matching: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    missing_welds: list[str] = []
    seen_match_ids: set[str] = set()
    seen_mismatch_ids: set[str] = set()

    for obj in tagged:
        obj_shape_id = (obj.get("shape") or {}).get("shape_id", "")
        obj_id = obj.get("object_id", "")
        best_overlap: set[str] = set()
        matched = False
        for ts in target_shapes:
            if not obj_shape_id or not ts.shape_id:
                continue
            obj_roles = set((obj.get("shape") or {}).get("role_topology", []))
            ts_roles = set(ts.role_topology)
            overlap = obj_roles & ts_roles
            if len(overlap) >= 2 or obj_shape_id == ts.shape_id:
                matched = True
                best_overlap |= overlap
        if matched:
            if obj_id not in seen_match_ids:
                seen_match_ids.add(obj_id)
                matching.append(
                    {
                        "object_id": obj_id,
                        "label": obj.get("label"),
                        "status": obj.get("status"),
                        "shared_roles": sorted(best_overlap),
                        "shape_id": obj_shape_id,
                    }
                )
            tex = obj.get("texture") or {}
            if tex.get("hypothesis_tags") and obj_id not in seen_mismatch_ids:
                seen_mismatch_ids.add(obj_id)
                mismatches.append(
                    {
                        "object_id": obj_id,
                        "texture_delta": tex.get("hypothesis_tags"),
                        "notation": tex.get("notation"),
                    }
                )

    # Check welds from millennium registry
    for w in prob.get("welds", []):
        if w.get("status") in ("INCOMPATIBLE", "OPEN") or w.get("requires_weld_lemma"):
            missing_welds.append(
                f"{w.get('weld_id')}: {w.get('relation')} — {w.get('evidence', '')[:80]}"
            )

    coverage_gaps: list[str] = []
    if not tagged:
        coverage_gaps.append(f"No manifest objects tagged {mid}")
    book_ids = {b.get("book_id") for b in prob.get("books", [])}
    manifest_books = {
        (o.get("texture") or {}).get("book_id", "")
        for o in objects
        if mid in (o.get("millennium_tags") or [])
    }
    untagged_books = sorted(book_ids - manifest_books - {""})
    if untagged_books:
        coverage_gaps.append(f"Books not in manifest: {', '.join(untagged_books[:5])}")

    target = target_shapes[0] if target_shapes else None
    statement = (
        f"Navigation map for {prob.get('clay_name', mid)}: "
        f"{len(matching)} objects share shape skeleton; "
        f"{len(mismatches)} texture mismatches flagged; "
        f"{len(missing_welds)} welds need attention. "
        "DA navigates — does not prove."
    )

    return NavigationReport(
        millennium_id=mid,
        target_shape=target,
        matching_objects=matching,
        texture_mismatches=mismatches,
        missing_welds=missing_welds[:10],
        coverage_gaps=coverage_gaps,
        statement=statement,
    )


def finger_glossary() -> dict[str, str]:
    """Map HB five-finger symbols to role glosses."""
    out = dict(ROLE_GLOSSARY)
    for sym, role in SYMBOL_TO_FINGER.items():
        if sym in ROLE_GLOSSARY:
            out[f"{sym}→{role}"] = ROLE_GLOSSARY[sym]
    return out
