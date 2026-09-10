"""Lemma★ / DA-NS-1 — Domain Architect encoding (SHAPE STATEMENT lock-in).

USER LOCK-IN (supersedes viscosity-first wording):
Lemma★ is no longer a viscosity statement. It is a shape statement.

Viscosity form (Millennium ASCII, still locked):

    T_c ≤ θ ν (Z − Λ Y) + C₀ ν⁻¹ ‖u‖₂² X Λ

Shape form after u=av (size optimization cancels ν):

    (T_c(v)_+)² ≤ 4 θ C₀ D_s(v) ‖v‖₂² Y(v)

Decisive ratio (pure geometry; viscosity-independent):

    R_★(v) = (T_c(v)_+)² / (D_s(v) ‖v‖₂² Y(v))

Status: HYPOTHESIS. Broken at PRODUCT-BLOCK / HH→L = missing uniform
bound on R_★. Analytic bottleneck: Bony HH→L (triadic reason not written).

Five-lane (PR #48): K=0 dead ↔ D_s=0 kill lane; ★ survives numeric kill
only (≠ proved; numeric bound ≠ uniform bound); NS NOT SOLVED.

DA will not green Lemma★ as PROVED. Refuses “almost proved”,
“numerics prove ★”, greening from finite samples. No SFE glue.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .rstar_quantities import (
    DOC_PATH as RSTAR_EXACT_DOC,
    HARD_RULES as RSTAR_HARD_RULES,
    exact_formula_inventory,
)
from .shape_texture import extract_shape, extract_texture, shape_match
from .theory_splicer import (
    SpliceResult,
    express,
    get_book,
    insert,
    load_millennium_registry,
    screen,
)


PACKAGE_DATA = Path(__file__).resolve().parent.parent / "data" / "domain_architect"
INVENTORY_PATH = PACKAGE_DATA / "snd_claim_inventory.json"

EXPR_LEMMA_STAR = (
    "T_c <= theta*nu*(Z - Lambda*Y) + C_0*nu^{-1}*||u||_2^2*X*Lambda"
)
EXPR_LEMMA_STAR_UNICODE = (
    "T_c ≤ θν(Z − ΛY) + C₀ ν⁻¹ ‖u‖₂² X Λ"
)
EXPR_SHAPE_FORM = (
    "(T_c(v)_+)^2 <= 4*theta*C_0*D_s(v)*||v||_2^2*Y(v)"
)
EXPR_R_STAR = (
    "R_star(v) = (T_c(v)_+)^2 / (D_s(v)*||v||_2^2*Y(v))"
)
EXPR_PRODUCT_BLOCK = (
    "|T_c| <= C*||u||_2*X^{3/2}; ordinary 3D Sobolev/product estimates "
    "INSUFFICIENT from energy alone; equivalently missing uniform R_star"
)

QUANTITIES: dict[str, str] = {
    "T_c": "M - Lambda*N (centered spectral drift / stretching; cubic in field)",
    "D_s": "spectral spread (quadratic in field)",
    "R_star": "(T_c_+)^2 / (D_s * ||v||_2^2 * Y) — pure geometry; viscosity-independent",
    "Lambda": "spectral scale / eigenvalue marker (blowup target)",
    "X": "enstrophy / ||grad u||_L2^2 scale",
    "Y": "viscous cross term companion / shape-form Y(v)",
    "Z": "viscous variance companion",
    "E": "||u||_2^2 Leray energy",
    "nu": "viscosity (cancels under u=av size optimization)",
    "theta": "geometric/structure constant in viscous term",
    "C_0": "geometric constant only — independent of field wildness",
}

# Recognition patterns for Lemma★ expression variants
LEMMA_STAR_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"lemma\s*[\*★]|lemma-?star|da-?ns-?1", re.I),
    re.compile(
        r"t_c\s*<=?\s*.*nu.*(z\s*[-−]\s*.*lambda|z\s*[-−]\s*.*Λ).*c_?0",
        re.I,
    ),
    re.compile(
        r"t_c\s*<=?.*theta.*nu.*(z.*lambda.*y|z.*Λ.*y)",
        re.I,
    ),
    re.compile(
        r"centered\s+spectral\s+drift.*(energy.?budget|leray)",
        re.I,
    ),
    re.compile(
        r"t_c\s*=\s*m\s*[-−]\s*lambda\s*n|t_c\s*=\s*m\s*[-−]\s*Λ\s*n",
        re.I,
    ),
    re.compile(r"r[_\s]*[\*★]?star|r_star|shape.?form|u\s*=\s*a\s*v", re.I),
    re.compile(
        r"\(t_c.*_\+.*\)\^?2.*d_s|d_s\(v\).*\|v\||r_\*?star\(v\)",
        re.I,
    ),
)

PRODUCT_BLOCK_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"product.?block|product.?estimate\s+gap", re.I),
    re.compile(
        r"\|?\s*t_c\s*\|?\s*<=?\s*c.*\|\|?u\|\|_?2.*x\s*\^?\s*\{?3/2\}?",
        re.I,
    ),
    re.compile(
        r"ordinary\s+3d\s+(sobolev|product).*insufficient",
        re.I,
    ),
    re.compile(r"missing\s+uniform\s+r[_\s]*[\*★]?star|uniform\s+r_star", re.I),
)

SHAPE_FORM_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"shape\s+statement|shape.?form|r[_\s]*[\*★]?\s*star", re.I),
    re.compile(r"viscosity\s+cancell|u\s*=\s*av|size\s+optim", re.I),
    re.compile(r"d_s\s*=\s*0|almost.?single.?shell|pure\s+geometry", re.I),
)

PROVED_REFUSAL_PATTERNS: tuple[tuple[str, str], ...] = (
    (
        r"(lemma\s*[\*★]|lemma-?star|da-?ns-?1|r[_\s]*[\*★]?star|shape.?form)"
        r".{0,40}(proved|resolved|closed|established)",
        "REFUSE: Lemma★ / R-STAR / SHAPE-FORM is HYPOTHESIS — not proved; "
        "broken at PRODUCT-BLOCK / missing uniform R_★ / HH→L",
    ),
    (
        r"(proved|resolved|closed).{0,40}"
        r"(lemma\s*[\*★]|lemma-?star|da-?ns-?1|r[_\s]*[\*★]?star|shape.?form)",
        "REFUSE: Lemma★ / R-STAR / SHAPE-FORM is HYPOTHESIS — not proved; "
        "broken at PRODUCT-BLOCK / missing uniform R_★ / HH→L",
    ),
    (
        r"lemma\s*[\*★].{0,30}(closes|implies|gives)\s+(clay|millennium|global\s+regularity)",
        "REFUSE: Lemma★→Clay B is WITHHELD until PRODUCT-BLOCK / uniform R_★ closes",
    ),
    (
        r"(almost\s+proved|nearly\s+(proved|closed)|basically\s+proved|"
        r"as\s+good\s+as\s+proved|essentially\s+proved|practically\s+proved|"
        r"numeric(al)?\s+surviv(al|es?).{0,40}proof|survives?\s+numeric.{0,40}proved|"
        r"greening|green\s+lemma)",
        "REFUSE: ‘almost proved’ / greening forbidden — numeric survive ≠ proof; "
        "HH→L / PRODUCT-BLOCK / uniform R_★ still open; NS NOT SOLVED",
    ),
    (
        r"(numeric(al)?s?\s+(prove|proves|prove\s+that)|"
        r"finite\s+samples?\s+(prove|green|establish)|"
        r"samples?\s+(prove|green)\s+(lemma|★|r_?\*?star)|"
        r"r_?\*?star\s+bounded\s+on\s+(samples|tested)|"
        r"numerics?\s*=\s*proof|"
        r"numeric\s+bound\s*=\s*uniform)",
        "REFUSE: numerics do not prove ★ — finite-sample R_★ is evidence only; "
        "numeric bound ≠ uniform bound; NS NOT SOLVED",
    ),
    (
        r"(ns|navier.?stokes|clay).{0,30}(solved|proved|resolved)",
        "REFUSE: NS NOT SOLVED — Lemma★ remains HYPOTHESIS (shape statement open)",
    ),
)

# Kill / status rules for R_★ (printed by analyze/report)
R_STAR_KILL_RULES: tuple[str, ...] = (
    "If some shapes make R_★ arbitrarily large → no finite C_0 → ★ DEAD",
    "If D_s=0 (one Fourier shell) and T_c>0 → ★ DEAD on that field "
    "(aligns with five-lane K=0 dead). Pure single shell: both sides vanish "
    "(not a kill). Live kill = almost-single-shell that still stretches.",
    "If every shape has R_★ below one number → that number is ★ (up to 4θ). "
    "A list of fields with small R_★ is NOT that number — numerics = evidence only.",
)

# Five-lane drill status (PR #48) — inventory sync, not a proof upgrade
FIVE_LANE_STATUS: dict[str, Any] = {
    "pr": 48,
    "pr_url": "https://github.com/simons357/Ship_it_app/pull/48",
    "branch": "cursor/ns-five-lane-lemma-star-1390",
    "date": "2026-09-10",
    "ns_solved": False,
    "lemma_star_proved": False,
    "lanes": {
        "K0_absorption": "DEAD",
        "D_s_zero_kill": "ALIGNED_WITH_K0_DEAD",
        "lemma_star_numeric_kill": "SURVIVES_NUMERIC_ONLY_NOT_PROVED",
        "numeric_bound_vs_uniform": "NUMERIC_BOUND_NE_UNIFORM_BOUND",
        "bony_hh_to_l": "GAP_LIVE",
        "product_block_agmon": "OPEN_INSUFFICIENT_MISSING_UNIFORM_R_STAR",
    },
    "cross_link": (
        "K=0 dead ↔ D_s=0 kill lane in R_★ shape form; "
        "numeric bound ≠ uniform bound on R_★"
    ),
    "headline": (
        "K=0 dead ↔ D_s=0 kill; Lemma★ survives numeric kill only ≠ proved "
        "(numeric ≠ uniform R_★); HH→L still the gap; NS NOT SOLVED"
    ),
}

SHAPE_FORM_STATUS: dict[str, Any] = {
    "lock_in": "USER LOCK-IN: ★ is a shape statement, not a viscosity statement",
    "viscosity_cancelled": True,
    "decisive_form": "R-STAR / SHAPE-FORM",
    "expression_shape": EXPR_SHAPE_FORM,
    "expression_r_star": EXPR_R_STAR,
    "expression_viscosity": EXPR_LEMMA_STAR,
    "equivalent_claims": ["LEMMA-STAR", "R-STAR", "SHAPE-FORM"],
    "blocker": "PRODUCT-BLOCK / HH→L = missing uniform bound on R_★",
    "proof_needed": (
        "Triadic reason that stretching cannot get large unless spectrum "
        "also spreads or phases cancel; HH→L is the channel — NOT WRITTEN"
    ),
    "ns_solved": False,
    "kill_rules": list(R_STAR_KILL_RULES),
}

ATTACK_ROUTES: tuple[dict[str, Any], ...] = (
    {
        "rank": 1,
        "id": "TC-STRUCTURE-HH-L",
        "title": "Better structure on T_c = M − Λ N (control HH→L / triads)",
        "move": (
            "Exploit triad addition / cancellations / divergence form so the "
            "Bony HH→L channel is controlled and R_★ stays uniformly bounded "
            "without a raw 3D Agmon/product estimate from energy alone"
        ),
        "honesty": (
            "Primary analytic attack; HH→L still the gap (PR #48 Attack 3); "
            "triadic reason not written."
        ),
    },
    {
        "rank": 2,
        "id": "SND-SHELL-CONDITIONAL",
        "title": "Conditional under SND / dominant shell",
        "move": (
            "Assume shell concentration (J/X or dominant j_*) and reduce the "
            "product / R_★ gap to the known open SND packaging"
        ),
        "honesty": "Reduces to known open — does not close Clay alone.",
    },
    {
        "rank": 3,
        "id": "C0-GEOMETRIC-ONLY",
        "title": "Geometric C₀ only (already required)",
        "move": (
            "Keep C₀ geometry-dependent only — already in Lemma★ statement; "
            "does NOT close the product / uniform-R_★ estimate"
        ),
        "honesty": "Necessary hygiene; not a closure of PRODUCT-BLOCK.",
    },
    {
        "rank": 4,
        "id": "NEGATIVE-KILL-R-STAR",
        "title": "Negative: kill ★ with R_★→∞ or D_s=0 & T_c>0",
        "move": (
            "Exhibit smooth family with R_★(v)→∞, or D_s→0 with T_c>0 "
            "(almost-single-shell that still stretches) — kills packaging"
        ),
        "honesty": (
            "Five-lane (PR #48) did not produce a kill on tested samples; "
            "finite samples ≠ uniform bound; numeric survive ≠ proof. "
            "Would falsify the route, not prove regularity."
        ),
    },
)


@dataclass
class LemmaStarReport:
    """Structured diagnosis of Lemma★ / DA-NS-1 / R_★ shape form."""

    status: str  # HYPOTHESIS
    blocker: str  # PRODUCT-BLOCK
    clay_implication: str  # CONDITIONAL
    recognized: bool
    expression_canonical: str
    expression_shape_form: str
    expression_r_star: str
    quantities: dict[str, str]
    ordinary_3d_product: str  # INSUFFICIENT
    clay_weld: str  # WITHHELD
    analytic_gap: str = "HH→L"  # Bony HH→L still the gap
    ns_solved: bool = False
    shape_statement: bool = True
    viscosity_cancelled: bool = True
    five_lane: dict[str, Any] = field(default_factory=dict)
    shape_form: dict[str, Any] = field(default_factory=dict)
    kill_rules: list[str] = field(default_factory=list)
    exact_formulas: dict[str, Any] = field(default_factory=dict)
    hard_rules: list[str] = field(default_factory=list)
    shape: dict[str, Any] = field(default_factory=dict)
    texture: dict[str, Any] = field(default_factory=dict)
    attack_routes: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    refused_proved_claim: bool = False
    refusal_reasons: list[str] = field(default_factory=list)
    input_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def narrative(self) -> str:
        lines = [
            "Domain Architect — Lemma★ / DA-NS-1 / R_★",
            "",
            "USER LOCK-IN: ★ is a SHAPE STATEMENT (not a viscosity statement).",
            f"Status: {self.status}",
            f"Broken at: {self.blocker} / missing uniform R_★ / analytic gap: {self.analytic_gap}",
            f"Clay implication: {self.clay_implication} (weld {self.clay_weld})",
            f"Ordinary 3D product estimates: {self.ordinary_3d_product}",
            f"Viscosity cancelled under u=av: {self.viscosity_cancelled}",
            "NS NOT SOLVED",
            "",
            f"Viscosity form: {self.expression_canonical}",
            f"Shape form:     {self.expression_shape_form}",
            f"R_★:            {self.expression_r_star}",
            f"Exact formulas: {RSTAR_EXACT_DOC}",
            "",
            "R_★ kill / status rules:",
        ]
        for rule in self.kill_rules:
            lines.append(f"  • {rule}")
        lines.append("")
        lines.append("Hard rules (exact T_c / R_★):")
        for rule in self.hard_rules or list(RSTAR_HARD_RULES):
            lines.append(f"  • {rule}")
        lines.extend(
            [
                "",
                "Headline: Broken at PRODUCT-BLOCK → HH→L still the gap → "
                "missing uniform R_★ → close by triad structure on T_c or "
                "SND/shell conditional (C₀ alone does not close; "
                "numeric survive ≠ proof; R_★→∞ or D_s=0&T_c>0 would kill).",
                "",
                "Proving Lemma★ ≡ Clay B in this book. DA will not green it "
                "without PRODUCT-BLOCK / uniform R_★. Refuse ‘almost proved’ / "
                "‘numerics prove ★’. Proof reason (HH→L / triads) NOT WRITTEN.",
                "",
                f"Five-lane (PR #48): {self.five_lane.get('headline', '')}",
                f"Cross-link: {self.five_lane.get('cross_link', '')}",
            ]
        )
        if self.refusal_reasons:
            lines.append("")
            lines.append("Refusals:")
            for r in self.refusal_reasons:
                lines.append(f"  - {r}")
        for note in self.notes:
            lines.append(f"Note: {note}")
        return "\n".join(lines)


def _normalize(text: str) -> str:
    return (
        text.lower()
        .replace("★", "*")
        .replace("≤", "<=")
        .replace("≥", ">=")
        .replace("−", "-")
        .replace("Λ", "lambda")
        .replace("λ", "lambda")
        .replace("θ", "theta")
        .replace("ν", "nu")
        .replace("‖", "||")
        .replace("₂", "2")
        .replace("₀", "0")
    )


def recognize_lemma_star(text: str) -> bool:
    """True if text matches Lemma★ / DA-NS-1 / R_★ / shape-form labels."""
    if not text or not text.strip():
        return True  # bare analyze defaults to Lemma★
    for pat in LEMMA_STAR_PATTERNS:
        if pat.search(text):
            return True
    compact = re.sub(r"\s+", "", _normalize(text))
    if "t_c" in compact and "lambda" in compact and ("c_0" in compact or "c0" in compact):
        if "z" in compact and ("x" in compact or "||u||" in compact or "u_2" in compact):
            return True
    if "r_star" in compact or "r*star" in compact or "shapeform" in compact:
        return True
    return False


def recognize_product_block(text: str) -> bool:
    for pat in PRODUCT_BLOCK_PATTERNS:
        if pat.search(text):
            return True
    return False


def recognize_shape_form(text: str) -> bool:
    for pat in SHAPE_FORM_PATTERNS:
        if pat.search(text):
            return True
    return False


def detect_proved_refusal(text: str) -> list[str]:
    norm = _normalize(text)
    reasons: list[str] = []
    for pattern, reason in PROVED_REFUSAL_PATTERNS:
        if re.search(pattern, norm, flags=re.IGNORECASE):
            reasons.append(reason)
    return list(dict.fromkeys(reasons))


def _lemma_star_shape_texture() -> tuple[dict[str, Any], dict[str, Any]]:
    """Energy-budget / shape-ratio spectral drift fingers + texture."""
    try:
        shape = extract_shape("DA-NS-1").to_dict()
    except KeyError:
        shape = {
            "shape_id": "energy-budget-spectral-drift-r-star",
            "fingers": {
                "P": "admissibility",
                "H": "interaction",
                "ψ": "state",
                "λ": "scale_response",
                "Φ": "realized_output",
                "E": "environment",
            },
            "role_topology": [
                "admissibility",
                "interaction",
                "state",
                "scale_response",
                "realized_output",
                "environment",
            ],
            "compatibility_class": "DA-NS-1",
            "dependency_hints": [
                "T_c",
                "D_s",
                "R_star",
                "Lambda",
                "X",
                "Y",
                "Z",
                "E",
                "viscous_variance",
            ],
            "notes": [
                "Fingers for E (Leray energy), X (enstrophy scale), "
                "viscous variance Z−ΛY, Λ (spectral scale), D_s, R_★."
            ],
        }
        shape["source"] = "DA-NS-1"
    try:
        texture = extract_texture("DA-NS-1").to_dict()
    except KeyError:
        texture = {
            "source": "DA-NS-1",
            "notation": "energy_budget_shape_form_r_star",
            "domain": "T³",
            "hypothesis_tags": [
                "Lemma★_hypothesis",
                "R-STAR_shape_form",
                "PRODUCT-BLOCK_open",
            ],
            "book_id": "DA-NS-1",
        }
    texture.setdefault("notes", [])
    texture["notes"].append(
        "Texture: shape-form R_★ / energy-budget vs shell J/X SND vs λ_min/λ_max Bypass"
    )
    texture["notation_family"] = "energy_budget_shape_form_r_star"
    texture["contrast"] = {
        "SND-C": "shell J/X under X<=M",
        "NS-B": "classical vorticity/velocity PDE",
        "Bypass": "λ_min/λ_max shell-helical operator",
        "DA-NS-1": "shape-form R_★ / energy-budget T_c / Λ / viscous variance",
    }
    return shape, texture


def analyze_lemma_star(text: str | None = None) -> LemmaStarReport:
    """Analyze Lemma★: HYPOTHESIS shape statement; blocker PRODUCT-BLOCK / R_★."""
    raw = (text or EXPR_LEMMA_STAR).strip()
    recognized = (
        recognize_lemma_star(raw)
        or recognize_product_block(raw)
        or recognize_shape_form(raw)
    )
    refusals = detect_proved_refusal(raw)
    shape, texture = _lemma_star_shape_texture()

    inventory = exact_formula_inventory()
    notes = [
        "USER LOCK-IN: Lemma★ is a SHAPE STATEMENT via R_★ — not a viscosity statement.",
        "Under u=av, size optimization cancels ν; decisive form is uniform R_★.",
        f"Boxed shape form: {inventory['boxed_shape_form']}.",
        f"Exact Fourier identities encoded in {RSTAR_EXACT_DOC} "
        "and domain_architect/rstar_quantities.py "
        "(moments X,Y,Z,Λ; three D_s forms; two-shell; signed T_c; Λ' sign check).",
        "Lemma★ is Millennium packaging (locked), not a side lemma: "
        "Λ blowup prevention → finite enstrophy → global regularity.",
        "Broken at PRODUCT-BLOCK / Agmon-product = missing uniform R_★: "
        "need |T_c|≤C‖u‖₂ X^{3/2} ≡ R_★ ≤ 4θ C_0; ordinary 3D Sobolev/product "
        "estimates INSUFFICIENT from energy alone.",
        "Analytic bottleneck: Bony HH→L (five-lane Attack 3) — still the gap; "
        "triadic reason NOT WRITTEN. HH→L restricted ≠ complete T_c for kill.",
        "NEVER abs the triad sum. Only complete T_c decides failure.",
        "C₀ geometric-only is already required and does not close the product / R_★ gap.",
        "Five-lane PR #48: K=0 dead ↔ D_s=0 kill; ★ survives numeric kill only ≠ proved "
        "(numeric bound ≠ uniform bound); NS NOT SOLVED.",
        "Proving Lemma★ ≡ Clay B in this book; DA will not green without "
        "PRODUCT-BLOCK / uniform R_★. Refuse ‘almost proved’ / ‘numerics prove ★’ / greening.",
        "No SFE glue.",
    ]
    if recognize_product_block(raw) and not recognize_lemma_star(raw):
        notes.insert(0, "Input matches PRODUCT-BLOCK blocker (not a proved closure).")
    if recognize_shape_form(raw):
        notes.insert(0, "Input matches SHAPE-FORM / R-STAR decisive form.")

    return LemmaStarReport(
        status="HYPOTHESIS",
        blocker="PRODUCT-BLOCK",
        clay_implication="CONDITIONAL",
        recognized=recognized,
        expression_canonical=EXPR_LEMMA_STAR,
        expression_shape_form=EXPR_SHAPE_FORM,
        expression_r_star=EXPR_R_STAR,
        quantities=dict(QUANTITIES),
        ordinary_3d_product="INSUFFICIENT",
        clay_weld="WITHHELD",
        analytic_gap="HH→L",
        ns_solved=False,
        shape_statement=True,
        viscosity_cancelled=True,
        five_lane=dict(FIVE_LANE_STATUS),
        shape_form=dict(SHAPE_FORM_STATUS),
        kill_rules=list(R_STAR_KILL_RULES),
        exact_formulas=inventory,
        hard_rules=list(RSTAR_HARD_RULES),
        shape=shape,
        texture=texture,
        attack_routes=list(ATTACK_ROUTES),
        notes=notes,
        refused_proved_claim=bool(refusals),
        refusal_reasons=refusals,
        input_text=raw,
    )


def refuse_proved_lemma_star(text: str) -> dict[str, Any]:
    """Refuse claiming Lemma★ / R_★ as PROVED, almost-proved, or numerics-proved."""
    report = analyze_lemma_star(text)
    reasons = list(report.refusal_reasons)
    norm = _normalize(text)
    soft_green = (
        "proved" in norm
        or "resolved" in norm
        or "closes clay" in norm
        or "almost proved" in norm
        or "nearly proved" in norm
        or "nearly closed" in norm
        or "greening" in norm
        or "ns solved" in norm
        or "navier-stokes solved" in norm
        or "numerics prove" in norm
        or "numeric prove" in norm
        or "finite samples" in norm
        or "samples prove" in norm
        or "samples green" in norm
        or "numeric bound = uniform" in norm
    )
    if not reasons and soft_green:
        reasons.append(
            "REFUSE: Lemma★ / R-STAR is HYPOTHESIS — not proved; "
            "broken at PRODUCT-BLOCK / missing uniform R_★ / HH→L; NS NOT SOLVED"
        )
    refused = bool(reasons) or report.refused_proved_claim
    if recognize_lemma_star(text) and soft_green:
        refused = True
        if not reasons:
            reasons.append(
                "REFUSE: Lemma★ / R-STAR is HYPOTHESIS — not proved; "
                "broken at PRODUCT-BLOCK / missing uniform R_★ / HH→L; NS NOT SOLVED"
            )
    return {
        "ok": not refused,
        "refused": refused,
        "status": "HYPOTHESIS",
        "blocker": "PRODUCT-BLOCK",
        "analytic_gap": "HH→L",
        "shape_statement": True,
        "viscosity_cancelled": True,
        "clay_implication": "CONDITIONAL",
        "clay_weld": "WITHHELD",
        "ns_solved": False,
        "kill_rules": list(R_STAR_KILL_RULES),
        "five_lane": dict(FIVE_LANE_STATUS),
        "shape_form": dict(SHAPE_FORM_STATUS),
        "refusal_reasons": reasons,
        "message": (
            "Refused: Lemma★ is not proved (and not ‘almost proved’; "
            "numerics do not prove ★). Broken at PRODUCT-BLOCK / HH→L = "
            "missing uniform R_★ → close by triad structure on T_c or "
            "SND/shell conditional. Numeric bound ≠ uniform bound. NS NOT SOLVED."
            if refused
            else "No proved-claim language; Lemma★ remains HYPOTHESIS (shape statement)."
        ),
        "report": report.to_dict(),
    }


def screen_lemma_star(*, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """SCREEN Lemma★ / R_★ welds inside the NS millennium book."""
    ns = screen("NS", registry=registry)
    lemma_welds = [
        w
        for w in ns.welds
        if "LEMMA" in w.get("weld_id", "").upper()
        or "PRODUCT" in w.get("weld_id", "").upper()
        or "RSTAR" in w.get("weld_id", "").upper().replace("-", "")
        or "LEMMA" in str(w.get("left_id", "")).upper()
        or "PRODUCT" in str(w.get("left_id", "")).upper()
        or "R-STAR" in str(w.get("left_id", "")).upper()
        or "LEMMA" in str(w.get("right_id", "")).upper()
        or "PRODUCT" in str(w.get("right_id", "")).upper()
        or "R-STAR" in str(w.get("right_id", "")).upper()
    ]
    withheld = [w for w in lemma_welds if w.get("status") == "WITHHELD"]
    open_welds = [
        w
        for w in lemma_welds
        if w.get("status") in ("OPEN", "WITHHELD")
        or w.get("screen_verdict") == "OPEN"
    ]
    return {
        "operation": "SCREEN LEMMA-STAR",
        "millennium_id": "NS",
        "book_ids": ["DA-NS-1", "PRODUCT-BLOCK"],
        "claim_ids": ["LEMMA-STAR", "R-STAR", "SHAPE-FORM", "PRODUCT-BLOCK"],
        "lemma_welds": lemma_welds,
        "withheld_count": len(withheld),
        "open_count": len(open_welds),
        "bullshit_destroyed": False,  # WITHHELD is honest packaging, not fraud
        "statement": (
            f"SCREEN LEMMA-STAR: {len(lemma_welds)} welds; "
            f"{len(withheld)} WITHHELD (Lemma★→Clay until PRODUCT-BLOCK / "
            "uniform R_★ / HH→L); status HYPOTHESIS shape statement — "
            "DA refuses PROVED / ‘almost proved’ / ‘numerics prove ★’; "
            "five-lane: K=0↔D_s=0 dead, ★ survives numeric only ≠ uniform, "
            "NS NOT SOLVED."
        ),
        "kill_rules": list(R_STAR_KILL_RULES),
        "five_lane": dict(FIVE_LANE_STATUS),
        "shape_form": dict(SHAPE_FORM_STATUS),
        "parent_ns_screen": {
            "compatible_count": ns.compatible_count,
            "incompatible_count": ns.incompatible_count,
            "open_count": ns.open_count,
        },
    }


def insert_product_block_candidate(
    *,
    candidate: str | None = None,
) -> SpliceResult:
    """INSERT candidate completion for PRODUCT-BLOCK / uniform R_★ into DA-NS-1."""
    cand = candidate or (
        "Candidate: prove uniform R_star(v) <= 4*theta*C_0 "
        "(equiv. |T_c| <= C*||u||_2*X^{3/2}) via triad/HH→L structure on "
        "T_c=M-Lambda*N — OPEN, not proved"
    )
    return insert("DA-NS-1", "scale_response", cand)


def express_lemma_star_as_proved() -> dict[str, Any]:
    """Attempt EXPRESS as proved → must refuse."""
    honest = express("DA-NS-1")
    proved_attempt = refuse_proved_lemma_star(
        "Lemma★ proved; DA-NS-1 closes Clay Statement B / global regularity"
    )
    numeric_attempt = refuse_proved_lemma_star(
        "Numerics prove Lemma★; finite samples green R_star uniform bound"
    )
    return {
        "express_honest": honest.to_dict(),
        "express_as_proved": proved_attempt,
        "express_as_numerics_proved": numeric_attempt,
        "refused_proved": proved_attempt["refused"],
        "refused_numerics_prove": numeric_attempt["refused"],
        "message": (
            "EXPRESS as proved REFUSED. Numerics-prove-★ REFUSED. "
            "Honest EXPRESS on DA-NS-1 does not close Clay — "
            "PRODUCT-BLOCK / HH→L / uniform R_★ incomplete. "
            "Numeric bound ≠ uniform bound. NS NOT SOLVED."
        ),
    }


def compare_lemma_star_shapes() -> dict[str, Any]:
    """Shape-compare Lemma★ vs SND-C and vs NS-B."""
    vs_snd = shape_match("DA-NS-1", "SND-C")
    vs_nsb = shape_match("DA-NS-1", "NS-B")
    vs_boot = shape_match("DA-NS-1", "BOOT-M")
    tex = extract_texture("DA-NS-1")
    return {
        "vs_SND-C": vs_snd.to_dict(),
        "vs_NS-B": vs_nsb.to_dict(),
        "vs_BOOT-M": vs_boot.to_dict(),
        "lemma_star_texture": tex.to_dict(),
        "texture_note": (
            "Same regularity shape family; texture = shape-form R_★ / "
            "energy-budget T_c/Λ vs shell J/X SND vs classical PDE NS-B."
        ),
        "shape_form_lock_in": dict(SHAPE_FORM_STATUS),
    }


def product_block_incompleteness() -> dict[str, Any]:
    """Show PRODUCT-BLOCK incompleteness as missing uniform R_★."""
    book = get_book("PRODUCT-BLOCK")
    claim = book.claim_by_id("PRODUCT-BLOCK")
    return {
        "break_id": "PRODUCT-BLOCK",
        "headline": (
            "Broken at PRODUCT-BLOCK / Agmon-product → HH→L still the gap → "
            "missing uniform R_★ → close by triad structure on T_c=M−ΛN "
            "or conditional SND/dominant shell"
        ),
        "status": "OPEN",
        "need": "|T_c| <= C*||u||_2*X^{3/2} ≡ uniform R_star(v) <= 4*theta*C_0",
        "ordinary_3d": "INSUFFICIENT from energy alone",
        "analytic_gap": "HH→L",
        "equivalent_gap": "missing uniform bound on R_★",
        "five_lane": dict(FIVE_LANE_STATUS),
        "shape_form": dict(SHAPE_FORM_STATUS),
        "kill_rules": list(R_STAR_KILL_RULES),
        "book": book.to_dict(),
        "claim": claim.to_dict() if claim else None,
        "attack_routes": list(ATTACK_ROUTES),
        "clay_weld": "WITHHELD until closed",
        "ns_solved": False,
    }


def navigate_lemma_star() -> dict[str, Any]:
    """Navigate DA-NS-1 / LEMMA-STAR / R-STAR as a focused library view."""
    reg = load_millennium_registry()
    analysis = analyze_lemma_star()
    screen_rep = screen_lemma_star(registry=reg)
    shapes = compare_lemma_star_shapes()
    block = product_block_incompleteness()
    return {
        "navigate_target": "DA-NS-1",
        "aliases": [
            "LEMMA-STAR",
            "DA-NS-1",
            "Lemma★",
            "R-STAR",
            "SHAPE-FORM",
        ],
        "analysis": analysis.to_dict(),
        "screen": screen_rep,
        "shape_compare": shapes,
        "product_block": block,
        "statement": analysis.narrative(),
    }


def load_lemma_star_inventory() -> dict[str, Any]:
    with INVENTORY_PATH.open(encoding="utf-8") as fh:
        inv = json.load(fh)
    ids = {
        "LEMMA-STAR",
        "DA-NS-1",
        "PRODUCT-BLOCK",
        "FIVE-LANE-LEMMA-STAR",
        "R-STAR",
        "SHAPE-FORM",
    }
    return {
        "claims": [c for c in inv.get("claims", []) if c.get("claim_id") in ids],
        "refused_routings": [
            r
            for r in inv.get("refused_routings", [])
            if "lemma" in r.lower()
            or "da-ns" in r.lower()
            or "almost" in r.lower()
            or "ns solved" in r.lower()
            or "numeric" in r.lower()
            or "r_star" in r.lower()
            or "shape form" in r.lower()
            or "finite samples" in r.lower()
        ],
        "five_lane": dict(FIVE_LANE_STATUS),
        "shape_form": dict(SHAPE_FORM_STATUS),
        "kill_rules": list(R_STAR_KILL_RULES),
    }
