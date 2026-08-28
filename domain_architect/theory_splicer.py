"""CRISPR-like operations on mathematical theory books.

Domain Architect splices, cuts, inserts, and screens welds between frozen
theory DNA (roles, terms, claims). It refuses illegal glue — it does NOT
prove Millennium problems or generate fake closure.
"""

from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .audit import audit_expression
from .gap_closure import diagnose_gap
from .hb_loop import BOOK_REQUIREMENTS, build_hb_map, check_reconstruction, compare_reports
from .incompleteness import analyze_incompleteness, sketch_from_roles
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, ConflictRelation, Disposition


PACKAGE_DATA = Path(__file__).resolve().parent.parent / "data" / "domain_architect"
MILLENNIUM_BOOKS_PATH = PACKAGE_DATA / "millennium_books.json"

ALLOWED_SPLICE_RELATIONS = frozenset(
    {
        ConflictRelation.COMPATIBLE_DISTINCT.value,
        ConflictRelation.IDENTICAL.value,
        ConflictRelation.NOTATIONALLY_EQUIVALENT.value,
        ConflictRelation.EQUIVALENT_UNDER_SUBSTITUTION.value,
        ConflictRelation.SPECIAL_CASE.value,
        ConflictRelation.GENERALIZATION.value,
    }
)

REFUSE_SPLICE_RELATIONS = frozenset(
    {
        ConflictRelation.INCOMPATIBLE.value,
    }
)

PROVED_CLAIM_MARKERS = (
    "proved",
    "resolved",
    "solved",
    "millennium prize",
    "clay statement b resolved",
    "global regularity proved",
)


@dataclass
class TheoryClaim:
    """One claim/lemma slot in a theory book."""

    claim_id: str
    label: str
    expression: str
    status: str  # OPEN | CONDITIONAL | RETIRE | REFERENCE | REFUSED
    equation_ref: str = ""
    roles: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TheoryWeld:
    """A weld between two claims/books — the splice junction."""

    weld_id: str
    left_id: str
    right_id: str
    relation: str
    evidence: str
    status: str = "recorded"  # COMPATIBLE | INCOMPATIBLE | OPEN
    notes: str = ""
    requires_weld_lemma: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TheoryBook:
    """Theory DNA: sequence of roles, terms, and claims."""

    book_id: str
    millennium_id: str
    label: str
    status: str  # OPEN | CONDITIONAL | REFERENCE | REFUSE | SOLVED_REFERENCE
    honest_status: str
    expression: str = ""
    roles: list[str] = field(default_factory=list)
    terms: list[str] = field(default_factory=list)
    claims: list[TheoryClaim] = field(default_factory=list)
    equation_refs: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "book_id": self.book_id,
            "millennium_id": self.millennium_id,
            "label": self.label,
            "status": self.status,
            "honest_status": self.honest_status,
            "expression": self.expression,
            "roles": self.roles,
            "terms": self.terms,
            "claims": [c.to_dict() for c in self.claims],
            "equation_refs": self.equation_refs,
            "notes": self.notes,
        }

    def claim_by_id(self, claim_id: str) -> TheoryClaim | None:
        for c in self.claims:
            if c.claim_id == claim_id:
                return c
        return None

    def active_claims(self) -> list[TheoryClaim]:
        return [c for c in self.claims if c.status not in ("RETIRE", "REFUSED", "CUT")]


@dataclass
class SpliceResult:
    """Structured outcome of any splice operation."""

    operation: str
    success: bool
    book_id: str = ""
    weld_id: str = ""
    bullshit_destroyed: bool = False
    bullshit_flags: list[str] = field(default_factory=list)
    suggested_fix: str = ""
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ScreenReport:
    """Audit of all welds in a millennium problem book."""

    millennium_id: str
    welds: list[dict[str, Any]] = field(default_factory=list)
    compatible_count: int = 0
    incompatible_count: int = 0
    open_count: int = 0
    bullshit_destroyed: bool = False
    statement: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_millennium_registry(path: Path | None = None) -> dict[str, Any]:
    p = path or MILLENNIUM_BOOKS_PATH
    if not p.exists():
        raise FileNotFoundError(f"millennium books registry missing: {p}")
    return _load_json(p)


def _claim_from_dict(raw: dict[str, Any]) -> TheoryClaim:
    return TheoryClaim(**{k: v for k, v in raw.items() if k in TheoryClaim.__dataclass_fields__})


def _book_from_dict(raw: dict[str, Any], millennium_id: str) -> TheoryBook:
    claims = [_claim_from_dict(c) for c in raw.get("claims", [])]
    return TheoryBook(
        book_id=str(raw["book_id"]),
        millennium_id=millennium_id,
        label=str(raw.get("label", raw["book_id"])),
        status=str(raw.get("status", "OPEN")),
        honest_status=str(raw.get("honest_status", "OPEN — not proved")),
        expression=str(raw.get("expression", "")),
        roles=list(raw.get("roles", [])),
        terms=list(raw.get("terms", [])),
        claims=claims,
        equation_refs=list(raw.get("equation_refs", [])),
        notes=str(raw.get("notes", "")),
    )


def get_millennium_problem(problem_id: str, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    reg = registry or load_millennium_registry()
    problems = reg.get("problems", {})
    key = problem_id.upper()
    if key not in problems:
        # allow navier-stokes style aliases
        for pid, prob in problems.items():
            if pid.upper() == key or prob.get("alias", "").upper() == key:
                return prob
        raise KeyError(f"unknown millennium problem: {problem_id}")
    return problems[key]


def get_book(book_id: str, registry: dict[str, Any] | None = None) -> TheoryBook:
    reg = registry or load_millennium_registry()
    bid = book_id.upper()
    for prob in reg.get("problems", {}).values():
        for raw in prob.get("books", []):
            if str(raw["book_id"]).upper() == bid:
                return _book_from_dict(raw, prob["id"])
    raise KeyError(f"unknown theory book: {book_id}")


def list_millennium_problems(registry: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    reg = registry or load_millennium_registry()
    out: list[dict[str, Any]] = []
    for pid, prob in reg.get("problems", {}).items():
        books = [b["book_id"] for b in prob.get("books", [])]
        out.append(
            {
                "id": prob.get("id", pid),
                "clay_name": prob.get("clay_name", pid),
                "status": prob.get("status", "OPEN"),
                "honest_note": prob.get("honest_note", ""),
                "book_count": len(books),
                "books": books,
            }
        )
    return out


def _weld_from_registry_conflict(cf: dict[str, Any]) -> TheoryWeld:
    rel = str(cf["relation"])
    status = "INCOMPATIBLE" if rel == ConflictRelation.INCOMPATIBLE.value else (
        "COMPATIBLE" if rel in ALLOWED_SPLICE_RELATIONS else "OPEN"
    )
    return TheoryWeld(
        weld_id=f"{cf['left_id']}↔{cf['right_id']}",
        left_id=str(cf["left_id"]),
        right_id=str(cf["right_id"]),
        relation=rel,
        evidence=str(cf.get("evidence", "")),
        status=status,
        notes=str(cf.get("notes", "")),
        requires_weld_lemma=rel == ConflictRelation.COMPATIBLE_DISTINCT.value,
    )


def _registry_weld(left_id: str, right_id: str, registry: EquationRegistry) -> TheoryWeld | None:
    for cf in registry.conflicts:
        ids = {cf.left_id, cf.right_id}
        if ids == {left_id, right_id}:
            return _weld_from_registry_conflict(cf.to_dict())
    return None


def _book_equation_refs(book: TheoryBook) -> list[str]:
    refs = list(book.equation_refs)
    for c in book.claims:
        if c.equation_ref and c.equation_ref not in refs:
            refs.append(c.equation_ref)
        if c.claim_id and c.claim_id not in refs:
            refs.append(c.claim_id)
    if not refs:
        refs.append(book.book_id)
    return refs


def _lookup_weld_for_books(
    book_a: TheoryBook,
    book_b: TheoryBook,
    *,
    eq_registry: EquationRegistry | None = None,
    millennium_registry: dict[str, Any] | None = None,
    weld_id: str | None = None,
) -> TheoryWeld:
    reg = millennium_registry or load_millennium_registry()
    if weld_id:
        for prob in reg.get("problems", {}).values():
            for raw in prob.get("welds", []):
                if raw.get("weld_id") == weld_id:
                    return TheoryWeld(
                        **{k: v for k, v in raw.items() if k in TheoryWeld.__dataclass_fields__}
                    )

    refs_a = _book_equation_refs(book_a)
    refs_b = _book_equation_refs(book_b)
    eq_reg = eq_registry or EquationRegistry.load_default()

    for la in refs_a:
        for rb in refs_b:
            w = _registry_weld(la, rb, eq_reg)
            if w:
                return w

    book_pair = {book_a.book_id.upper(), book_b.book_id.upper()}
    for prob in reg.get("problems", {}).values():
        for raw in prob.get("welds", []):
            left = str(raw.get("left_id", ""))
            right = str(raw.get("right_id", ""))
            # Match weld whose IDs appear in either book's refs or book_ids
            left_hit = left in refs_a or left.startswith(book_a.book_id) or left in book_a.book_id
            right_hit = (
                right in refs_b or right.startswith(book_b.book_id) or right in book_b.book_id
            )
            if left_hit and right_hit:
                return TheoryWeld(
                    **{k: v for k, v in raw.items() if k in TheoryWeld.__dataclass_fields__}
                )
            # Also match by substring on claim IDs
            if any(left in r or r in left for r in refs_a) and any(
                right in r or r in right for r in refs_b
            ):
                return TheoryWeld(
                    **{k: v for k, v in raw.items() if k in TheoryWeld.__dataclass_fields__}
                )

    la, rb = refs_a[0], refs_b[0]
    return TheoryWeld(
        weld_id=f"{la}↔{rb}",
        left_id=la,
        right_id=rb,
        relation=ConflictRelation.INSUFFICIENT_INFORMATION.value,
        evidence="No recorded weld between these books.",
        status="OPEN",
    )


def _claims_overclaim_proved(book: TheoryBook) -> list[str]:
    flags: list[str] = []
    for c in book.active_claims():
        low = (c.expression + " " + c.label).lower()
        if c.status in ("OPEN", "CONDITIONAL", "RETIRE", "REFUSED"):
            if any(m in low for m in PROVED_CLAIM_MARKERS) and c.status != "REFERENCE":
                flags.append(f"{c.claim_id}: claims proof while status={c.status}")
        if c.claim_id in ("CLAY-B001", "SND-TWEET-THM-D001", "SND-TWEET-MAIN001"):
            if "clay" in low and ("<=>" in c.expression or "resolved" in low):
                flags.append(f"{c.claim_id}: Clay glue / equivalence overclaim")
    return flags


def _refuse_proved_millennium(book: TheoryBook, operation: str) -> SpliceResult | None:
    """Honesty rule: refuse PROVED claims without reconstruction pass."""
    if book.millennium_id in ("POINCARE",):
        return None
    if operation == "SPLICE" and book.status in ("RETIRE", "REFUSE", "REFERENCE"):
        return None
    flags = _claims_overclaim_proved(book)
    gap = diagnose_gap(book.expression) if book.expression else None
    if gap and gap.refuses_unconditional_clay and operation == "EXPRESS":
        flags.append("gap_closure: refuses unconditional Clay routing")
    if flags and operation in ("EXPRESS",):
        return SpliceResult(
            operation=operation,
            success=False,
            book_id=book.book_id,
            bullshit_destroyed=True,
            bullshit_flags=flags,
            suggested_fix=(
                "Remove PROVED/resolved language; run EXPRESS after honest "
                "reconstruction; DA does not prove Millennium problems."
            ),
            message="Refused: Millennium PROVED claim without reconstruction pass.",
            details={"honesty_rule": "no_proved_without_reconstruction"},
        )
    return None


def cut(book_id: str, claim_id: str, *, registry: dict[str, Any] | None = None) -> SpliceResult:
    """CUT — remove a claim/role/term from a book."""
    book = copy.deepcopy(get_book(book_id, registry))
    claim = book.claim_by_id(claim_id)
    if claim is None:
        return SpliceResult(
            operation="CUT",
            success=False,
            book_id=book_id,
            bullshit_destroyed=False,
            suggested_fix=f"Use a valid claim_id from book {book_id}.",
            message=f"Claim {claim_id} not found in {book_id}.",
        )
    claim.status = "CUT"
    flags: list[str] = []
    if "clay" in claim.expression.lower() and "<=>" in claim.expression:
        flags.append("Removed Clay⇔SND equivalence glue (Thm D style)")
    return SpliceResult(
        operation="CUT",
        success=True,
        book_id=book_id,
        bullshit_destroyed=bool(flags),
        bullshit_flags=flags,
        suggested_fix="Re-screen welds after cut; illegal routes may now be absent.",
        message=f"Cut claim {claim_id} from {book_id}.",
        details={"book": book.to_dict(), "removed_claim": claim.to_dict()},
    )


def knockout(book_id: str, claim_id: str, *, registry: dict[str, Any] | None = None) -> SpliceResult:
    """KNOCKOUT — RETIRE a claim (gap_closure refuse semantics)."""
    book = copy.deepcopy(get_book(book_id, registry))
    claim = book.claim_by_id(claim_id)
    if claim is None:
        return SpliceResult(
            operation="KNOCKOUT",
            success=False,
            book_id=book_id,
            message=f"Claim {claim_id} not found.",
        )
    gap = diagnose_gap(claim.expression)
    claim.status = "RETIRE"
    flags = [f"retired {claim_id}: {claim.label}"]
    if gap.refuses_unconditional_clay:
        flags.append("gap_closure refused unconditional Clay glue")
    return SpliceResult(
        operation="KNOCKOUT",
        success=True,
        book_id=book_id,
        bullshit_destroyed=True,
        bullshit_flags=flags,
        suggested_fix=gap.findings[0].suggested_closure if gap.findings else "Keep RETIRE disposition.",
        message=f"Knocked out (RETIRE) claim {claim_id} in {book_id}.",
        details={"book": book.to_dict(), "gap_closure": gap.to_dict()},
    )


def insert(
    book_id: str,
    role: str,
    candidate: str,
    *,
    registry: dict[str, Any] | None = None,
) -> SpliceResult:
    """INSERT — add candidate completion at incompleteness gap."""
    book = copy.deepcopy(get_book(book_id, registry))
    expr = book.expression or candidate
    inc = sketch_from_roles(book.roles + [role], book=book.book_id)
    new_claim = TheoryClaim(
        claim_id=f"INSERT-{role.upper()[:8]}-001",
        label=f"Inserted candidate at role {role}",
        expression=candidate,
        status="OPEN",
        roles=[role],
        notes="Candidate completion — not a proved theorem.",
    )
    book.claims.append(new_claim)
    gap = diagnose_gap(candidate)
    flags: list[str] = []
    if gap.refuses_unconditional_clay:
        flags.append("insert refused: candidate claims unconditional Clay")
        return SpliceResult(
            operation="INSERT",
            success=False,
            book_id=book_id,
            bullshit_destroyed=True,
            bullshit_flags=flags,
            suggested_fix=gap.findings[0].suggested_closure if gap.findings else "Use conditional candidate.",
            message="Insert refused: candidate triggers Clay glue detection.",
            details={"incompleteness": inc.to_dict(), "gap_closure": gap.to_dict()},
        )
    return SpliceResult(
        operation="INSERT",
        success=True,
        book_id=book_id,
        bullshit_destroyed=False,
        suggested_fix=f"Prove {role} slot or wire to registry equation.",
        message=f"Inserted candidate at role '{role}' in {book_id}.",
        details={
            "book": book.to_dict(),
            "incompleteness": inc.to_dict(),
            "inserted_claim": new_claim.to_dict(),
        },
    )


def _book_expression(book: TheoryBook) -> str:
    if book.expression:
        return book.expression
    active = book.active_claims()
    if active:
        return active[0].expression
    return book.book_id


def splice(
    book_a_id: str,
    book_b_id: str,
    *,
    weld_id: str | None = None,
    registry: dict[str, Any] | None = None,
) -> SpliceResult:
    """SPLICE — join two books at a compatible weld."""
    book_a = get_book(book_a_id, registry)
    book_b = get_book(book_b_id, registry)

    for book, op in ((book_a, "SPLICE"), (book_b, "SPLICE")):
        refused = _refuse_proved_millennium(book, op)
        if refused:
            refused.book_id = f"{book_a_id}+{book_b_id}"
            return refused

    left_ref = book_a.equation_refs[0] if book_a.equation_refs else book_a.book_id
    right_ref = book_b.equation_refs[0] if book_b.equation_refs else book_b.book_id
    weld = _lookup_weld_for_books(
        book_a, book_b, millennium_registry=registry, weld_id=weld_id
    )

    expr_a = _book_expression(book_a)
    expr_b = _book_expression(book_b)
    left_audit = audit_expression(expr_a)
    right_audit = audit_expression(expr_b)
    cmp = compare_reports(left_audit, right_audit)

    flags: list[str] = []
    if weld.relation in REFUSE_SPLICE_RELATIONS or weld.status == "INCOMPATIBLE":
        flags.append(f"registry weld {weld.relation}: {weld.evidence}")
        gap = diagnose_gap(f"{expr_a} implies {expr_b} Clay Statement B resolved")
        if gap.refuses_unconditional_clay:
            flags.append("gap_closure: illegal Clay glue")
        return SpliceResult(
            operation="SPLICE",
            success=False,
            book_id=f"{book_a_id}+{book_b_id}",
            weld_id=weld.weld_id,
            bullshit_destroyed=True,
            bullshit_flags=flags,
            suggested_fix=(
                "Do not splice incompatible books. Split theorems or prove "
                "an explicit weld lemma first."
            ),
            message=f"Splice refused: {book_a_id} ↔ {book_b_id} is {weld.relation}.",
            details={"weld": weld.to_dict(), "compare": cmp.to_dict()},
        )

    if weld.relation not in ALLOWED_SPLICE_RELATIONS and weld.relation != ConflictRelation.INSUFFICIENT_INFORMATION.value:
        flags.append(f"unexpected relation {weld.relation}")

    if weld.relation == ConflictRelation.INSUFFICIENT_INFORMATION.value:
        return SpliceResult(
            operation="SPLICE",
            success=False,
            book_id=f"{book_a_id}+{book_b_id}",
            weld_id=weld.weld_id,
            bullshit_destroyed=False,
            bullshit_flags=flags,
            suggested_fix="Record explicit weld lemma and registry conflict before splice.",
            message=f"Splice withheld: insufficient weld information for {book_a_id} ↔ {book_b_id}.",
            details={"weld": weld.to_dict(), "compare": cmp.to_dict()},
        )

    if weld.requires_weld_lemma and not weld.notes.strip():
        flags.append("COMPATIBLE_DISTINCT requires explicit weld lemma slot")

    merged = TheoryBook(
        book_id=f"{book_a_id}+{book_b_id}",
        millennium_id=book_a.millennium_id,
        label=f"Spliced {book_a.label} + {book_b.label}",
        status="CONDITIONAL",
        honest_status="Spliced book — organizational only; not Clay closure.",
        expression=f"{expr_a} ;; {expr_b}",
        roles=sorted(set(book_a.roles + book_b.roles)),
        terms=sorted(set(book_a.terms + book_b.terms)),
        claims=book_a.active_claims() + book_b.active_claims(),
        equation_refs=book_a.equation_refs + book_b.equation_refs,
        notes=f"Splice at weld {weld.weld_id} ({weld.relation})",
    )

    return SpliceResult(
        operation="SPLICE",
        success=True,
        book_id=merged.book_id,
        weld_id=weld.weld_id,
        bullshit_destroyed=False,
        bullshit_flags=flags,
        suggested_fix=(
            "Run EXPRESS on spliced book; add weld lemma proof if COMPATIBLE_DISTINCT."
            if weld.requires_weld_lemma
            else "Verify reconstruction closes target roles."
        ),
        message=f"Splice allowed: {book_a_id} ↔ {book_b_id} ({weld.relation}).",
        details={"weld": weld.to_dict(), "merged_book": merged.to_dict(), "compare": cmp.to_dict()},
    )


def screen(millennium_id: str, *, registry: dict[str, Any] | None = None) -> ScreenReport:
    """SCREEN — audit all welds in a millennium problem book."""
    reg = registry or load_millennium_registry()
    prob = get_millennium_problem(millennium_id, reg)
    eq_reg = EquationRegistry.load_default()
    welds_out: list[dict[str, Any]] = []
    compatible = incompatible = open_count = 0
    bullshit = False

    for raw in prob.get("welds", []):
        w = TheoryWeld(**{k: v for k, v in raw.items() if k in TheoryWeld.__dataclass_fields__})
        entry = w.to_dict()
        if w.status == "INCOMPATIBLE" or w.relation == ConflictRelation.INCOMPATIBLE.value:
            entry["screen_verdict"] = "INCOMPATIBLE"
            incompatible += 1
            bullshit = True
            entry["bullshit_flag"] = "illegal glue — splice must refuse"
        elif w.status == "COMPATIBLE" or w.relation in ALLOWED_SPLICE_RELATIONS:
            entry["screen_verdict"] = "COMPATIBLE"
            compatible += 1
        else:
            entry["screen_verdict"] = "OPEN"
            open_count += 1
        welds_out.append(entry)

    # Also screen registry conflicts touching this problem's equation refs
    eq_ids: set[str] = set()
    for b in prob.get("books", []):
        eq_ids.update(b.get("equation_refs", []))
    for cf in eq_reg.conflicts:
        if cf.left_id in eq_ids or cf.right_id in eq_ids:
            w = _weld_from_registry_conflict(cf.to_dict())
            if not any(x["weld_id"] == w.weld_id for x in welds_out):
                entry = w.to_dict()
                if w.status == "INCOMPATIBLE":
                    entry["screen_verdict"] = "INCOMPATIBLE"
                    incompatible += 1
                    bullshit = True
                elif w.status == "COMPATIBLE":
                    entry["screen_verdict"] = "COMPATIBLE"
                    compatible += 1
                else:
                    entry["screen_verdict"] = "OPEN"
                    open_count += 1
                welds_out.append(entry)

    return ScreenReport(
        millennium_id=prob.get("id", millennium_id),
        welds=welds_out,
        compatible_count=compatible,
        incompatible_count=incompatible,
        open_count=open_count,
        bullshit_destroyed=bullshit,
        statement=(
            f"Screened {len(welds_out)} welds for {prob.get('clay_name', millennium_id)}: "
            f"{compatible} COMPATIBLE, {incompatible} INCOMPATIBLE, {open_count} OPEN. "
            "DA does not prove this problem — it maps honest splice routes."
        ),
    )


def express(book_id: str, *, registry: dict[str, Any] | None = None) -> SpliceResult:
    """EXPRESS — reconstruct book from roles; check if expression closes."""
    book = get_book(book_id, registry)
    refused = _refuse_proved_millennium(book, "EXPRESS")
    if refused:
        return refused

    expr = _book_expression(book)
    audit = audit_expression(expr)
    recon = check_reconstruction(audit)
    inc = analyze_incompleteness(audit)
    hb = build_hb_map(audit)
    req = BOOK_REQUIREMENTS.get(hb.domain_book, BOOK_REQUIREMENTS["generic"])

    closes = recon.passed and inc.is_complete
    flags = _claims_overclaim_proved(book)
    gap = diagnose_gap(expr)
    if gap.refuses_unconditional_clay:
        flags.append("expression still routes through illegal Clay glue")
        closes = False

    return SpliceResult(
        operation="EXPRESS",
        success=closes,
        book_id=book_id,
        bullshit_destroyed=bool(flags),
        bullshit_flags=flags,
        suggested_fix=(
            "Supply missing roles: " + ", ".join(recon.missing_roles)
            if recon.missing_roles
            else (
                "Remove Clay overclaims before claiming closure."
                if flags
                else "Reconstruction inventory complete — still not a Clay proof."
            )
        ),
        message=(
            f"EXPRESS {'closes' if closes else 'does not close'} {book_id} "
            f"under book {hb.domain_book}."
        ),
        details={
            "reconstruction": recon.to_dict(),
            "incompleteness": inc.to_dict(),
            "hb_map": hb.to_dict(),
            "required_roles": sorted(req.get("roles", [])),
            "honest_status": book.honest_status,
            "millennium_status": book.status,
            "canonical_sfe_status": CANONICAL_SFE_STATUS,
        },
    )


def operation_cut(book: str, claim: str) -> SpliceResult:
    return cut(book, claim)


def operation_insert(book: str, role: str, candidate: str) -> SpliceResult:
    return insert(book, role, candidate)


def operation_join(book_a: str, book_b: str) -> SpliceResult:
    return splice(book_a, book_b)
