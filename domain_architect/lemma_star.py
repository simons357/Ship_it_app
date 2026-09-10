"""Lemma★ / DA-NS-1 energy-budget spectral drift — Domain Architect encoding.

Canonical full shape SoT: docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md

    T_c = -⟨B(v,v), A(A−Λ)v⟩
    (equivalent to M − Λ N when those triad moments exist)

Exact shape form (full lemma — not the near-shell K_{α,β} restriction):

    ∃ C_geom < ∞ ∀ v ≠ 0:  (T_c(v)_+)^2 ≤ C_geom D_s(v) ‖v‖₂² Y(v)

Viscosity packaging (0<θ<1), with C_geom = 4 θ C_0(θ):

    T_c ≤ θ ν D_s + C₀(θ) ν⁻¹ ‖u‖₂² Y

Status: HYPOTHESIS. Broken at PRODUCT-BLOCK / Agmon-product gap
(|T_c| ≤ C ‖u‖₂ X^{3/2} not available from energy alone via ordinary 3D
product estimates). Analytic bottleneck: Bony HH→L.

REFUSE: K_{α,β} = full ★ — near-shell K tests only a restricted limiting family.

Five-lane drill (PR #48): K=0 dead; Lemma★ survives numeric kill only
(≠ proved); HH→L still the gap; NS NOT SOLVED.

DA will not green Lemma★ as PROVED. Refuses “almost proved” / greening.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

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
EXPR_PRODUCT_BLOCK = (
    "|T_c| <= C*||u||_2*X^{3/2}; ordinary 3D Sobolev/product estimates "
    "INSUFFICIENT from energy alone"
)

QUANTITIES: dict[str, str] = {
    "T_c": (
        "-<B(v,v), A(A-Lambda)v> (centered spectral drift); "
        "equivalent to M - Lambda*N when those moments exist"
    ),
    "D_s": "Z - Y^2/X = ||(A-Lambda)A^{1/2}v||_2^2",
    "Lambda": "Y/X spectral scale marker (blowup target)",
    "X": "||A^{1/2}v||_2^2 enstrophy scale",
    "Y": "||Av||_2^2",
    "Z": "||A^{3/2}v||_2^2",
    "E": "||v||_2^2 Leray energy",
    "nu": "viscosity",
    "theta": "Young/AM-GM share in viscous packaging (0<theta<1)",
    "C_0": "viscosity-packaging constant; C_geom = 4*theta*C_0(theta)",
    "C_geom": "geometry-only constant in full shape form (not amplitude/shell/nu)",
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
)

PROVED_REFUSAL_PATTERNS: tuple[tuple[str, str], ...] = (
    (
        r"k[_\s]*(\{|\\?alpha)?[αa].{0,12}(β|beta).{0,40}"
        r"(full|complete|entire|equals?|=).{0,20}(lemma\s*[\*★]|lemma-?star|\★)",
        "REFUSE: K_{α,β} ≠ full ★ — near-shell tests only a restricted limiting family",
    ),
    (
        r"(k[_\s]*(\{|\\?alpha)?|near.?shell\s+k).{0,30}"
        r"(is|equals?|=|≡).{0,15}(full|the)\s*(lemma\s*[\*★]|★)",
        "REFUSE: K_{α,β} ≠ full ★ — near-shell tests only a restricted limiting family",
    ),
    (
        r"(lemma\s*[\*★]|lemma-?star|da-?ns-?1).{0,40}(proved|resolved|closed|established)",
        "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; broken at PRODUCT-BLOCK / HH→L",
    ),
    (
        r"(proved|resolved|closed).{0,40}(lemma\s*[\*★]|lemma-?star|da-?ns-?1)",
        "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; broken at PRODUCT-BLOCK / HH→L",
    ),
    (
        r"lemma\s*[\*★].{0,30}(closes|implies|gives)\s+(clay|millennium|global\s+regularity)",
        "REFUSE: Lemma★→Clay B is WITHHELD until PRODUCT-BLOCK closes",
    ),
    (
        r"(almost\s+proved|nearly\s+(proved|closed)|basically\s+proved|"
        r"as\s+good\s+as\s+proved|essentially\s+proved|practically\s+proved|"
        r"numeric(al)?\s+surviv(al|es?).{0,40}proof|survives?\s+numeric.{0,40}proved|"
        r"greening|green\s+lemma)",
        "REFUSE: ‘almost proved’ / greening forbidden — numeric survive ≠ proof; "
        "HH→L / PRODUCT-BLOCK still open; NS NOT SOLVED",
    ),
    (
        r"(ns|navier.?stokes|clay).{0,30}(solved|proved|resolved)",
        "REFUSE: NS NOT SOLVED — Lemma★ remains HYPOTHESIS",
    ),
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
        "lemma_star_numeric_kill": "SURVIVES_NUMERIC_ONLY_NOT_PROVED",
        "bony_hh_to_l": "GAP_LIVE",
        "product_block_agmon": "OPEN_INSUFFICIENT",
    },
    "headline": (
        "K=0 dead; Lemma★ survives numeric kill only ≠ proved; "
        "HH→L still the gap; NS NOT SOLVED"
    ),
}

ATTACK_ROUTES: tuple[dict[str, Any], ...] = (
    {
        "rank": 1,
        "id": "TC-STRUCTURE-HH-L",
        "title": "Better structure on T_c = -⟨B, A(A−Λ)v⟩ ≡ M − Λ N (control HH→L)",
        "move": (
            "Exploit cancellations / divergence form / spectral moment identities "
            "so the Bony HH→L channel is controlled and |T_c| is bounded without "
            "a raw 3D Agmon/product estimate from energy alone"
        ),
        "honesty": "Primary analytic attack; HH→L still the gap (PR #48 Attack 3).",
    },
    {
        "rank": 2,
        "id": "SND-SHELL-CONDITIONAL",
        "title": "Conditional under SND / dominant shell",
        "move": (
            "Assume shell concentration (J/X or dominant j_*) and reduce the "
            "product gap to the known open SND packaging"
        ),
        "honesty": "Reduces to known open — does not close Clay alone.",
    },
    {
        "rank": 3,
        "id": "C0-GEOMETRIC-ONLY",
        "title": "Geometric C₀ only (already required)",
        "move": (
            "Keep C₀ geometry-dependent only — already in Lemma★ statement; "
            "does NOT close the product estimate"
        ),
        "honesty": "Necessary hygiene; not a closure of PRODUCT-BLOCK.",
    },
    {
        "rank": 4,
        "id": "NEGATIVE-KILL-RATIO",
        "title": "Negative: kill ★ with blowing R_pre (or energy-alone counterexample)",
        "move": (
            "Exhibit smooth family with R_pre = T_c/(‖u‖₂ X Λ)→∞, or show "
            "Leray energy alone cannot yield |T_c|≤C‖u‖₂ X^{3/2} — kills packaging"
        ),
        "honesty": (
            "Five-lane (PR #48) did not produce a kill on tested samples; "
            "numeric survive ≠ proof. Would falsify the route, not prove regularity."
        ),
    },
)


@dataclass
class LemmaStarReport:
    """Structured diagnosis of Lemma★ / DA-NS-1."""

    status: str  # HYPOTHESIS
    blocker: str  # PRODUCT-BLOCK
    clay_implication: str  # CONDITIONAL
    recognized: bool
    expression_canonical: str
    quantities: dict[str, str]
    ordinary_3d_product: str  # INSUFFICIENT
    clay_weld: str  # WITHHELD
    analytic_gap: str = "HH→L"  # Bony HH→L still the gap
    ns_solved: bool = False
    five_lane: dict[str, Any] = field(default_factory=dict)
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
            "Domain Architect — Lemma★ / DA-NS-1",
            "",
            f"Status: {self.status}",
            f"Broken at: {self.blocker} (Agmon-product) / analytic gap: {self.analytic_gap}",
            f"Clay implication: {self.clay_implication} (weld {self.clay_weld})",
            f"Ordinary 3D product estimates: {self.ordinary_3d_product}",
            "NS NOT SOLVED",
            "",
            f"Canonical: {self.expression_canonical}",
            "",
            "Headline: Broken at PRODUCT-BLOCK → HH→L still the gap → "
            "close by structure on T_c or SND/shell conditional "
            "(C₀ alone does not close; numeric survive ≠ proof; "
            "blowing R_pre would kill the packaging).",
            "",
            "Proving Lemma★ ≡ Clay B in this book. DA will not green it "
            "without PRODUCT-BLOCK. Refuse ‘almost proved’.",
            "",
            f"Five-lane (PR #48): {self.five_lane.get('headline', '')}",
        ]
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
    """True if text matches Lemma★ / DA-NS-1 expression or labels."""
    if not text or not text.strip():
        return True  # bare analyze defaults to Lemma★
    for pat in LEMMA_STAR_PATTERNS:
        if pat.search(text):
            return True
    compact = re.sub(r"\s+", "", _normalize(text))
    if "t_c" in compact and "lambda" in compact and ("c_0" in compact or "c0" in compact):
        if "z" in compact and ("x" in compact or "||u||" in compact or "u_2" in compact):
            return True
    return False


def recognize_product_block(text: str) -> bool:
    for pat in PRODUCT_BLOCK_PATTERNS:
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
    """Energy-budget spectral drift fingers + texture vs shell SND / Bypass."""
    try:
        shape = extract_shape("DA-NS-1").to_dict()
    except KeyError:
        shape = {
            "shape_id": "energy-budget-spectral-drift",
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
            "dependency_hints": ["T_c", "Lambda", "X", "Y", "Z", "E", "viscous_variance"],
            "notes": [
                "Fingers for E (Leray energy), X (enstrophy scale), "
                "viscous variance Z−ΛY, and Λ (spectral scale)."
            ],
        }
        shape["source"] = "DA-NS-1"
    try:
        texture = extract_texture("DA-NS-1").to_dict()
    except KeyError:
        texture = {
            "source": "DA-NS-1",
            "notation": "energy_budget_spectral_drift",
            "domain": "T³",
            "hypothesis_tags": ["Lemma★_hypothesis", "PRODUCT-BLOCK_open"],
            "book_id": "DA-NS-1",
        }
    # Annotate texture contrast vs sibling NS books
    texture.setdefault("notes", [])
    texture["notes"].append(
        "Texture: energy-budget form vs shell J/X SND vs λ_min/λ_max Bypass"
    )
    texture["notation_family"] = "energy_budget_spectral_drift"
    texture["contrast"] = {
        "SND-C": "shell J/X under X<=M",
        "NS-B": "classical vorticity/velocity PDE",
        "Bypass": "λ_min/λ_max shell-helical operator",
        "DA-NS-1": "energy-budget T_c / Λ / viscous variance",
    }
    return shape, texture


def analyze_lemma_star(text: str | None = None) -> LemmaStarReport:
    """Analyze Lemma★: status HYPOTHESIS, blocker PRODUCT-BLOCK, clay CONDITIONAL."""
    raw = (text or EXPR_LEMMA_STAR).strip()
    recognized = recognize_lemma_star(raw) or recognize_product_block(raw)
    refusals = detect_proved_refusal(raw)
    shape, texture = _lemma_star_shape_texture()

    notes = [
        "Lemma★ is Millennium packaging (locked), not a side lemma: "
        "Λ blowup prevention → finite enstrophy → global regularity.",
        "Broken at PRODUCT-BLOCK / Agmon-product: need |T_c|≤C‖u‖₂ X^{3/2}; "
        "ordinary 3D Sobolev/product estimates INSUFFICIENT from energy alone.",
        "Analytic bottleneck: Bony HH→L (five-lane Attack 3) — still the gap.",
        "C₀ geometric-only is already required and does not close the product gap.",
        "Five-lane PR #48: K=0 dead; ★ survives numeric kill only ≠ proved; "
        "NS NOT SOLVED.",
        "Full shape SoT: (T_c_+)^2 ≤ C_geom D_s ‖v‖₂² Y; "
        "T_c = -⟨B, A(A−Λ)v⟩ (≡ M−ΛN when both exist). "
        "K_{α,β} is restricted — not the full lemma.",
        "Proving Lemma★ ≡ Clay B in this book; DA will not green without "
        "PRODUCT-BLOCK. Refuse ‘almost proved’ / greening.",
    ]
    if recognize_product_block(raw) and not recognize_lemma_star(raw):
        notes.insert(0, "Input matches PRODUCT-BLOCK blocker (not a proved closure).")

    return LemmaStarReport(
        status="HYPOTHESIS",
        blocker="PRODUCT-BLOCK",
        clay_implication="CONDITIONAL",
        recognized=recognized,
        expression_canonical=EXPR_LEMMA_STAR,
        quantities=dict(QUANTITIES),
        ordinary_3d_product="INSUFFICIENT",
        clay_weld="WITHHELD",
        analytic_gap="HH→L",
        ns_solved=False,
        five_lane=dict(FIVE_LANE_STATUS),
        shape=shape,
        texture=texture,
        attack_routes=list(ATTACK_ROUTES),
        notes=notes,
        refused_proved_claim=bool(refusals),
        refusal_reasons=refusals,
        input_text=raw,
    )


def refuse_proved_lemma_star(text: str) -> dict[str, Any]:
    """Refuse claiming Lemma★ / DA-NS-1 as PROVED or ‘almost proved’."""
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
    )
    if not reasons and soft_green:
        reasons.append(
            "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; "
            "broken at PRODUCT-BLOCK / HH→L; NS NOT SOLVED"
        )
    refused = bool(reasons) or report.refused_proved_claim
    # Always refuse EXPRESS-as-proved / almost-proved language on this book
    if recognize_lemma_star(text) and soft_green:
        refused = True
        if not reasons:
            reasons.append(
                "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; "
                "broken at PRODUCT-BLOCK / HH→L; NS NOT SOLVED"
            )
    return {
        "ok": not refused,
        "refused": refused,
        "status": "HYPOTHESIS",
        "blocker": "PRODUCT-BLOCK",
        "analytic_gap": "HH→L",
        "clay_implication": "CONDITIONAL",
        "clay_weld": "WITHHELD",
        "ns_solved": False,
        "five_lane": dict(FIVE_LANE_STATUS),
        "refusal_reasons": reasons,
        "message": (
            "Refused: Lemma★ is not proved (and not ‘almost proved’). "
            "Broken at PRODUCT-BLOCK / HH→L → close by structure on T_c "
            "or SND/shell conditional. Numeric survive ≠ proof. NS NOT SOLVED."
            if refused
            else "No proved-claim language; Lemma★ remains HYPOTHESIS."
        ),
        "report": report.to_dict(),
    }


def screen_lemma_star(*, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """SCREEN Lemma★ welds inside the NS millennium book."""
    ns = screen("NS", registry=registry)
    lemma_welds = [
        w
        for w in ns.welds
        if "LEMMA" in w.get("weld_id", "").upper()
        or "PRODUCT" in w.get("weld_id", "").upper()
        or "LEMMA" in str(w.get("left_id", "")).upper()
        or "PRODUCT" in str(w.get("left_id", "")).upper()
        or "LEMMA" in str(w.get("right_id", "")).upper()
        or "PRODUCT" in str(w.get("right_id", "")).upper()
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
        "lemma_welds": lemma_welds,
        "withheld_count": len(withheld),
        "open_count": len(open_welds),
        "bullshit_destroyed": False,  # WITHHELD is honest packaging, not fraud
        "statement": (
            f"SCREEN LEMMA-STAR: {len(lemma_welds)} welds; "
            f"{len(withheld)} WITHHELD (Lemma★→Clay until PRODUCT-BLOCK / HH→L); "
            "status HYPOTHESIS — DA refuses PROVED / ‘almost proved’; "
            "five-lane: K=0 dead, ★ survives numeric only, NS NOT SOLVED."
        ),
        "five_lane": dict(FIVE_LANE_STATUS),
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
    """INSERT candidate completion for PRODUCT-BLOCK into DA-NS-1 book."""
    cand = candidate or (
        "Candidate: prove |T_c| <= C*||u||_2*X^{3/2} via structure on "
        "T_c=M-Lambda*N (cancellations / divergence form) — OPEN, not proved"
    )
    return insert("DA-NS-1", "scale_response", cand)


def express_lemma_star_as_proved() -> dict[str, Any]:
    """Attempt EXPRESS as proved → must refuse."""
    # EXPRESS the honest hypothesis book
    honest = express("DA-NS-1")
    # Explicit proved-claim refusal
    proved_attempt = refuse_proved_lemma_star(
        "Lemma★ proved; DA-NS-1 closes Clay Statement B / global regularity"
    )
    return {
        "express_honest": honest.to_dict(),
        "express_as_proved": proved_attempt,
        "refused_proved": proved_attempt["refused"],
        "message": (
            "EXPRESS as proved REFUSED. Honest EXPRESS on DA-NS-1 does not "
            "close Clay — PRODUCT-BLOCK / HH→L incomplete. Numeric survive ≠ proof. "
            "NS NOT SOLVED."
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
            "Same regularity shape family; texture = energy-budget T_c/Λ "
            "vs shell J/X SND vs classical PDE NS-B."
        ),
    }


def product_block_incompleteness() -> dict[str, Any]:
    """Show PRODUCT-BLOCK incompleteness as the missing weld."""
    book = get_book("PRODUCT-BLOCK")
    claim = book.claim_by_id("PRODUCT-BLOCK")
    return {
        "break_id": "PRODUCT-BLOCK",
        "headline": (
            "Broken at PRODUCT-BLOCK / Agmon-product → HH→L still the gap → "
            "close by structure on T_c=-⟨B,A(A−Λ)v⟩≡M−ΛN or conditional "
            "SND/dominant shell (K_{α,β} ≠ full ★)"
        ),
        "status": "OPEN",
        "need": "|T_c| <= C*||u||_2*X^{3/2}",
        "ordinary_3d": "INSUFFICIENT from energy alone",
        "analytic_gap": "HH→L",
        "five_lane": dict(FIVE_LANE_STATUS),
        "book": book.to_dict(),
        "claim": claim.to_dict() if claim else None,
        "attack_routes": list(ATTACK_ROUTES),
        "clay_weld": "WITHHELD until closed",
        "ns_solved": False,
    }


def navigate_lemma_star() -> dict[str, Any]:
    """Navigate DA-NS-1 / LEMMA-STAR as a focused library view."""
    reg = load_millennium_registry()
    analysis = analyze_lemma_star()
    screen_rep = screen_lemma_star(registry=reg)
    shapes = compare_lemma_star_shapes()
    block = product_block_incompleteness()
    return {
        "navigate_target": "DA-NS-1",
        "aliases": ["LEMMA-STAR", "DA-NS-1", "Lemma★"],
        "analysis": analysis.to_dict(),
        "screen": screen_rep,
        "shape_compare": shapes,
        "product_block": block,
        "statement": analysis.narrative(),
    }


def load_lemma_star_inventory() -> dict[str, Any]:
    with INVENTORY_PATH.open(encoding="utf-8") as fh:
        inv = json.load(fh)
    ids = {"LEMMA-STAR", "DA-NS-1", "PRODUCT-BLOCK", "FIVE-LANE-LEMMA-STAR"}
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
        ],
        "five_lane": dict(FIVE_LANE_STATUS),
    }
