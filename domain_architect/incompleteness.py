"""Incompleteness reports and honest math-complete *candidates*.

When an NS-like (or other book) equation is missing required roles or
terms, Domain Architect reports what is missing and may propose
*candidate* completions drawn from the frozen domain book — not invented
Clay/Millennium physics, not a canonical SFE, and not a ToE claim.

Optional reverse direction: roles-in → candidate equation sketch (still
organizational / book-templated).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .gap_closure import gap_closure_candidates_for_incompleteness
from .hb_loop import BOOK_REQUIREMENTS, build_hb_map
from .report import AuditReport
from .schema import CANONICAL_SFE_STATUS


# Honest book templates for candidate sketches (not physical discoveries).
_BOOK_SKETCHES: dict[str, dict[str, Any]] = {
    "SND-C": {
        "full_sketch": (
            "SND-C: under X≤M, ρ≤ρ₀, X≥δ_*: bound dominant-shell flux Π_{j*} "
            "by C_*(ν,δ_*,M,ρ₀). Conditional book — not Clay Statement B."
        ),
        "role_terms": {
            "admissibility": "P ≈ Leray / div-free (inherited from NS-B)",
            "interaction": "H ≈ shell flux / vortex stretching in spread regime",
            "state": "ψ ≈ enstrophy shell profile (X_j), ρ=J/X",
            "scale_response": "λ ≈ ν plus a priori ceiling M (hypothesis)",
            "realized_output": "Φ ≈ Π_{j*} bound / spectral gap signal",
            "environment": "E ⊃ T³, IC, hypothesis X≤M",
        },
        "term_hints": {},
        "disclaimer": (
            "SND-C is a conditional spectral book. C_* depending on M does not "
            "resolve Clay Statement B. Do not glue to SND-U."
        ),
    },
    "SND-U": {
        "full_sketch": (
            "(REFUSED as proved) SND-U: J/X≥c_* for all H¹ data without X≤M. "
            "Not established in current manuscripts."
        ),
        "role_terms": {},
        "term_hints": {},
        "disclaimer": (
            "SND-U / Clay-B packaging is parked. Domain Architect refuses "
            "unconditional routing while the keystone assumes X≤M."
        ),
    },
    "SND-HYP": {
        "full_sketch": (
            "Unaugmented NS + SND as hypothesis: assume inf J/X≥c_*>0, then "
            "run conditional regularity chain (KEEP framing)."
        ),
        "role_terms": {
            "admissibility": "P ≈ Leray",
            "interaction": "H ≈ stretch under spectral gap hypothesis",
            "state": "ψ ≈ u or ω",
            "scale_response": "λ ≈ ν",
            "realized_output": "Φ ≈ controlled enstrophy production under SND",
            "environment": "E ⊃ domain, IC, SND hypothesis (not proved)",
        },
        "term_hints": {},
        "disclaimer": (
            "Honest conditional framework. SND is an assumption, not a theorem."
        ),
    },
    "NS-B": {
        "full_sketch": (
            "∂_t ω = (ω·∇)u + ν Δω   with   ∇·u = 0, "
            "u = Biot–Savart(ω), IC/BC on domain"
        ),
        "role_terms": {
            "admissibility": "P ≈ Leray / div-free constraint (∇·u=0)",
            "interaction": "H ≈ (ω·∇)u  (advection / vortex stretching)",
            "state": "ψ ≈ u or ω",
            "scale_response": "λ ≈ ν  (viscosity; dissipative scale)",
            "realized_output": "Φ ≈ p / strain / enstrophy production (observed)",
            "environment": "E ⊃ R³, IC/BC, Biot–Savart",
        },
        "term_hints": {
            "viscosity": "ν Δω or ν Δu",
            "advection": "(ω·∇)u or (u·∇)u",
            "incompressibility": "∇·u = 0",
            "time_evolution": "∂_t ω or ∂_t u",
        },
        "disclaimer": (
            "NS-B candidates are classical fluids book templates. They do "
            "not bake λ_min(Q_N)>-1/2 into NS, do not claim Clay regularity, "
            "and do not derive NS from an SFE."
        ),
    },
    "gravity-poisson": {
        "full_sketch": "∇²Φ = 4π G ρ   with spectral R(κ)=1/κ² (κ≠0), geometry + BC",
        "role_terms": {
            "realized_output": "Φ ≈ Newtonian potential",
            "source": "ρ ≈ mass density",
            "scale_response": "R(κ)=1/κ²  (Green / transfer; not κ itself)",
        },
        "term_hints": {
            "laplacian": "∇² or nabla^2",
            "source": "ρ or rho",
            "coupling": "4πG",
        },
        "disclaimer": (
            "Gravity candidates are representation templates for the known "
            "Poisson equation — not a derivation from a canonical SFE."
        ),
    },
    "NS-Q1": {
        "full_sketch": (
            "Q1: ∂_t u + (u·∇)u = −∇p + νΔu − ε(-Δ)^{1+δ}u; "
            "ε→0 limit to NS-B. SND passage is open (TH-H7-Q1)."
        ),
        "role_terms": {
            "admissibility": "P ≈ Leray",
            "interaction": "H ≈ advection under hyperdissipation",
            "state": "ψ ≈ u",
            "scale_response": "λ ≈ ν, ε",
            "realized_output": "Φ ≈ p / enstrophy response",
            "environment": "E ⊃ IC, ε→0 limit slot",
        },
        "term_hints": {},
        "disclaimer": (
            "Q1 approximants may hold SND for ε>0; liminf passage to "
            "Leray–Hopf is not established as Clay-grade."
        ),
    },
    "RING-BVB": {
        "full_sketch": (
            "Ring Lemma on shell S_{j*}: direction Lipschitz on E_c. "
            "BVB bridge — band-limited toolkit; not Clay rescue."
        ),
        "role_terms": {
            "admissibility": "P ≈ shell support / band-limit",
            "interaction": "H ≈ vorticity direction control on E_c",
            "state": "ψ ≈ ω direction field",
            "scale_response": "λ ≈ shell scale 2^{j*}",
            "realized_output": "Φ ≈ geometric bound / flux bridge",
            "environment": "E ⊃ E_c={|ω|≥c 2^{j*}||u||_{L2}}",
        },
        "term_hints": {},
        "disclaimer": (
            "Ring+BVB does not rescue Clay B or SND-U. Global CF not established."
        ),
    },
    "BOOT-M": {
        "full_sketch": (
            "Bootstrap (OPEN): M=M(||u₀‖_{H¹}) with X(t)≤M derived from "
            "data — candidate de-circularization for Theorem H input."
        ),
        "role_terms": {
            "admissibility": "P ≈ Leray / H¹ data",
            "interaction": "H ≈ enstrophy production bound",
            "state": "ψ ≈ u",
            "scale_response": "λ ≈ ν",
            "realized_output": "Φ ≈ X(t) ceiling M",
            "environment": "E ⊃ H¹ IC, energy identities",
        },
        "term_hints": {},
        "disclaimer": (
            "Candidate analytic slot only. Proving bootstrap does not alone "
            "close Clay B; c_* must still be M-free (TH-H3)."
        ),
    },
    "CSTAR-ARITH": {
        "full_sketch": (
            "c_*=6/π²=ζ(2)^{-1} — arithmetic analogy; not continuum NS floor."
        ),
        "role_terms": {},
        "term_hints": {},
        "disclaimer": (
            "Refuse routing arithmetic density to fluids SND threshold."
        ),
    },
    "generic": {
        "full_sketch": "(no frozen book sketch)",
        "role_terms": {},
        "term_hints": {},
        "disclaimer": (
            "No domain book frozen; candidate completions withheld rather "
            "than inventing physics."
        ),
    },
}


@dataclass
class CandidateCompletion:
    """One honest completion suggestion from a domain book."""

    kind: str  # missing_role | missing_term | roles_to_sketch
    proposal: str
    book_source: str
    confidence: str  # template | heuristic | withheld
    honesty_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IncompletenessReport:
    domain_book: str
    is_complete: bool
    missing_roles: list[str] = field(default_factory=list)
    missing_extras: list[str] = field(default_factory=list)
    missing_terms: list[str] = field(default_factory=list)
    present_roles: list[str] = field(default_factory=list)
    candidates: list[CandidateCompletion] = field(default_factory=list)
    equation_sketch: str = ""
    statement: str = ""
    canonical_sfe_status: str = CANONICAL_SFE_STATUS

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain_book": self.domain_book,
            "is_complete": self.is_complete,
            "missing_roles": self.missing_roles,
            "missing_extras": self.missing_extras,
            "missing_terms": self.missing_terms,
            "present_roles": self.present_roles,
            "candidates": [c.to_dict() for c in self.candidates],
            "equation_sketch": self.equation_sketch,
            "statement": self.statement,
            "canonical_sfe_status": self.canonical_sfe_status,
        }

    def narrative(self) -> str:
        lines = [
            "Incompleteness / math-complete candidates",
            f"  book: {self.domain_book}",
            f"  complete: {self.is_complete}",
            f"  present roles: {', '.join(self.present_roles) or '(none)'}",
        ]
        if self.missing_roles:
            lines.append(f"  missing roles: {', '.join(self.missing_roles)}")
        if self.missing_extras:
            lines.append(f"  missing E: {', '.join(self.missing_extras)}")
        if self.missing_terms:
            lines.append(f"  missing terms: {', '.join(self.missing_terms)}")
        if self.equation_sketch:
            lines.append(f"  book sketch: {self.equation_sketch}")
        if self.candidates:
            lines.append("  candidates (honest templates, not new physics):")
            for c in self.candidates:
                lines.append(f"    [{c.kind}/{c.confidence}] {c.proposal}")
                lines.append(f"      note: {c.honesty_note}")
        lines.append(f"  {self.statement}")
        lines.append(f"  Canonical SFE status: {self.canonical_sfe_status}.")
        return "\n".join(lines)


def _detect_missing_terms(expression: str, book: str) -> list[str]:
    """Heuristic term presence for known books (structural, not physical)."""
    text = expression.lower().replace(" ", "")
    missing: list[str] = []
    if book == "NS-B":
        has_visc = any(t in text for t in ("nu", "ν", "viscosity"))
        has_adv = any(
            t in text
            for t in (
                "(omega*nabla)",
                "(ω·∇)",
                "(u*nabla)",
                "(u·∇)",
                "advection",
                "stretch",
            )
        ) or ("omega" in text and "nabla" in text and "u" in text)
        has_time = any(t in text for t in ("partial_t", "∂_t", "partialt", "dt"))
        has_divfree = any(
            t in text for t in ("div", "∇·", "nabla·", "incompress")
        )
        if not has_visc:
            missing.append("viscosity_term")
        if not has_adv:
            missing.append("advection_or_stretch_term")
        if not has_time:
            missing.append("time_evolution")
        if not has_divfree:
            missing.append("explicit_incompressibility")
    elif book == "gravity-poisson":
        has_lap = any(t in text for t in ("nabla", "laplacian", "∇", "delta"))
        has_rho = "rho" in text or "ρ" in expression
        if not has_lap:
            missing.append("laplacian")
        if not has_rho:
            missing.append("source_density")
    return missing


def analyze_incompleteness(report: AuditReport) -> IncompletenessReport:
    """Report missing roles/terms and propose book-templated candidates."""
    hb = build_hb_map(report)
    book = hb.domain_book
    req = BOOK_REQUIREMENTS.get(book, BOOK_REQUIREMENTS["generic"])
    sketch_book = _BOOK_SKETCHES.get(book, _BOOK_SKETCHES["generic"])

    present = {r for r in hb.roles if not r.startswith("unresolved")}
    required = set(req["roles"])
    missing_roles = sorted(required - present)
    extras_l = {e.lower() for e in hb.extras}
    missing_extras = sorted(e for e in req["extras"] if e.lower() not in extras_l)
    missing_terms = _detect_missing_terms(report.input_expression, book)

    candidates: list[CandidateCompletion] = []
    role_terms = sketch_book.get("role_terms") or {}
    for role in missing_roles:
        proposal = role_terms.get(role, f"supply a defined {role} from the {book} book")
        candidates.append(
            CandidateCompletion(
                kind="missing_role",
                proposal=proposal,
                book_source=book,
                confidence="template" if role in role_terms else "withheld",
                honesty_note=sketch_book["disclaimer"],
            )
        )

    term_hints = sketch_book.get("term_hints") or {}
    term_map = {
        "viscosity_term": "viscosity",
        "advection_or_stretch_term": "advection",
        "time_evolution": "time_evolution",
        "explicit_incompressibility": "incompressibility",
        "laplacian": "laplacian",
        "source_density": "source",
    }
    for term in missing_terms:
        key = term_map.get(term, term)
        hint = term_hints.get(key)
        if hint:
            candidates.append(
                CandidateCompletion(
                    kind="missing_term",
                    proposal=f"Candidate term from {book} book: {hint}",
                    book_source=book,
                    confidence="heuristic",
                    honesty_note=sketch_book["disclaimer"],
                )
            )
        else:
            candidates.append(
                CandidateCompletion(
                    kind="missing_term",
                    proposal=f"Term '{term}' appears absent; no safe template.",
                    book_source=book,
                    confidence="withheld",
                    honesty_note=sketch_book["disclaimer"],
                )
            )

    # Weld / Clay-illegal glue → candidated closures (refuse unconditional claims).
    for weld in gap_closure_candidates_for_incompleteness(report.input_expression):
        candidates.append(
            CandidateCompletion(
                kind=str(weld.get("kind") or "gap_closure_weld"),
                proposal=str(weld.get("proposal") or ""),
                book_source=str(weld.get("book_source") or book),
                confidence=str(weld.get("confidence") or "template"),
                honesty_note=str(weld.get("honesty_note") or sketch_book["disclaimer"]),
            )
        )

    is_complete = not missing_roles and book != "generic"
    # Soft completeness: extras/terms may still be incomplete.
    soft_gaps = bool(missing_extras or missing_terms)

    if book == "generic":
        statement = (
            "No frozen domain book; incompleteness analysis cannot propose "
            "math-complete candidates without inventing structure."
        )
    elif is_complete and not soft_gaps:
        statement = (
            f"{book} inventory looks role-complete for Level 0 reconstruction. "
            "Candidates are unnecessary; this still does not solve the PDE."
        )
    elif is_complete and soft_gaps:
        statement = (
            f"{book} required roles are present, but some terms/E-structures "
            "look thin. Candidates below are book templates only."
        )
    else:
        statement = (
            f"{book} appears incomplete relative to the frozen book. "
            "Listed candidates are organizational completions, not discoveries."
        )

    return IncompletenessReport(
        domain_book=book,
        is_complete=is_complete and not soft_gaps,
        missing_roles=missing_roles,
        missing_extras=missing_extras,
        missing_terms=missing_terms,
        present_roles=sorted(present),
        candidates=candidates,
        equation_sketch=str(sketch_book.get("full_sketch") or ""),
        statement=statement,
    )


def sketch_from_roles(
    roles: list[str] | dict[str, Any],
    *,
    book: str | None = None,
) -> IncompletenessReport:
    """Roles-in → candidate equation sketch (organizational reverse path)."""
    if isinstance(roles, dict):
        role_names = [
            str(r)
            for r in roles.keys()
            if not str(r).startswith("unresolved")
        ]
    else:
        role_names = [str(r) for r in roles if not str(r).startswith("unresolved")]

    inferred = book or (
        "NS-B"
        if {"admissibility", "interaction", "state"} <= set(role_names)
        else "gravity-poisson"
        if {"realized_output", "source", "scale_response"} <= set(role_names)
        else "generic"
    )
    sketch_book = _BOOK_SKETCHES.get(inferred, _BOOK_SKETCHES["generic"])
    req = BOOK_REQUIREMENTS.get(inferred, BOOK_REQUIREMENTS["generic"])
    required = set(req["roles"])
    present = set(role_names)
    missing = sorted(required - present)

    candidates = [
        CandidateCompletion(
            kind="roles_to_sketch",
            proposal=str(sketch_book.get("full_sketch") or "(withheld)"),
            book_source=inferred,
            confidence="template" if inferred != "generic" else "withheld",
            honesty_note=sketch_book["disclaimer"],
        )
    ]
    for role in missing:
        rt = (sketch_book.get("role_terms") or {}).get(role)
        if rt:
            candidates.append(
                CandidateCompletion(
                    kind="missing_role",
                    proposal=rt,
                    book_source=inferred,
                    confidence="template",
                    honesty_note=sketch_book["disclaimer"],
                )
            )

    return IncompletenessReport(
        domain_book=inferred,
        is_complete=not missing and inferred != "generic",
        missing_roles=missing,
        present_roles=sorted(present),
        candidates=candidates,
        equation_sketch=str(sketch_book.get("full_sketch") or ""),
        statement=(
            f"Roles-in sketch under book {inferred}: organizational template "
            "only. Does not invent a canonical SFE or Clay physics."
        ),
    )


def attach_incompleteness(report: AuditReport) -> AuditReport:
    """Populate incompleteness fields on an audit report."""
    inc = analyze_incompleteness(report)
    report.incompleteness = inc.to_dict()
    report.notes = list(
        dict.fromkeys(
            list(report.notes)
            + [
                inc.statement,
                f"Book equation sketch: {inc.equation_sketch}"
                if inc.equation_sketch
                else "No book equation sketch.",
            ]
        )
    )
    return report
