"""Lemma★ / DA-NS-1 energy-budget spectral drift — Domain Architect encoding.

Honest packaging of Clay Statement B as one closing estimate:

    T_c ≤ θ ν (Z − Λ Y) + C₀ ν⁻¹ ‖u‖₂² X Λ

with C₀ geometric only. Status: HYPOTHESIS. Broken at PRODUCT-BLOCK
(|T_c| ≤ C ‖u‖₂ X^{3/2} not available from energy alone via ordinary 3D
product estimates). DA will not green Lemma★ as PROVED.
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
    "T_c": "M - Lambda*N (centered spectral drift)",
    "Lambda": "spectral scale / eigenvalue marker (blowup target)",
    "X": "enstrophy / ||grad u||_L2^2 scale",
    "Y": "viscous cross term companion",
    "Z": "viscous variance companion",
    "E": "||u||_2^2 Leray energy",
    "nu": "viscosity",
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
        r"(lemma\s*[\*★]|lemma-?star|da-?ns-?1).{0,40}(proved|resolved|closed|established)",
        "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; broken at PRODUCT-BLOCK",
    ),
    (
        r"(proved|resolved|closed).{0,40}(lemma\s*[\*★]|lemma-?star|da-?ns-?1)",
        "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; broken at PRODUCT-BLOCK",
    ),
    (
        r"lemma\s*[\*★].{0,30}(closes|implies|gives)\s+(clay|millennium|global\s+regularity)",
        "REFUSE: Lemma★→Clay B is WITHHELD until PRODUCT-BLOCK closes",
    ),
)

ATTACK_ROUTES: tuple[dict[str, Any], ...] = (
    {
        "rank": 1,
        "id": "TC-STRUCTURE",
        "title": "Better structure on T_c = M − Λ N",
        "move": (
            "Exploit cancellations / divergence form / spectral moment identities "
            "so |T_c| is controlled without a raw 3D product from energy alone"
        ),
        "honesty": "Primary analytic attack; no fake proof claimed.",
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
        "id": "NEGATIVE-ENERGY-ALONE",
        "title": "Negative: energy alone cannot bound T_c that way",
        "move": (
            "Exhibit that Leray energy alone cannot yield |T_c|≤C‖u‖₂ X^{3/2} "
            "in the required form — would kill this packaging"
        ),
        "honesty": "Would falsify the energy-budget Clay route, not prove regularity.",
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
            f"Broken at: {self.blocker}",
            f"Clay implication: {self.clay_implication} (weld {self.clay_weld})",
            f"Ordinary 3D product estimates: {self.ordinary_3d_product}",
            "",
            f"Canonical: {self.expression_canonical}",
            "",
            "Headline: Broken at PRODUCT-BLOCK → close by structure on T_c "
            "or SND/shell conditional (C₀ alone does not close; negative "
            "energy-alone counterexample would kill the packaging).",
            "",
            "Proving Lemma★ ≡ Clay B in this book. DA will not green it "
            "without PRODUCT-BLOCK.",
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
        "Lemma★ packages Clay B correctly in this framing: "
        "Λ blowup prevention → finite enstrophy → global regularity.",
        "Broken at PRODUCT-BLOCK: need |T_c|≤C‖u‖₂ X^{3/2}; "
        "ordinary 3D Sobolev/product estimates INSUFFICIENT from energy alone.",
        "C₀ geometric-only is already required and does not close the product gap.",
        "Proving Lemma★ ≡ Clay B in this book; DA will not green without PRODUCT-BLOCK.",
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
        shape=shape,
        texture=texture,
        attack_routes=list(ATTACK_ROUTES),
        notes=notes,
        refused_proved_claim=bool(refusals),
        refusal_reasons=refusals,
        input_text=raw,
    )


def refuse_proved_lemma_star(text: str) -> dict[str, Any]:
    """Refuse claiming Lemma★ / DA-NS-1 as PROVED."""
    report = analyze_lemma_star(text)
    reasons = list(report.refusal_reasons)
    if not reasons and (
        "proved" in _normalize(text)
        or "resolved" in _normalize(text)
        or "closes clay" in _normalize(text)
    ):
        reasons.append(
            "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; broken at PRODUCT-BLOCK"
        )
    refused = bool(reasons) or report.refused_proved_claim
    # Always refuse EXPRESS-as-proved language on this book
    if recognize_lemma_star(text) and any(
        w in _normalize(text) for w in ("proved", "resolved", "solved", "closes clay")
    ):
        refused = True
        if not reasons:
            reasons.append(
                "REFUSE: Lemma★ / DA-NS-1 is HYPOTHESIS — not proved; broken at PRODUCT-BLOCK"
            )
    return {
        "ok": not refused,
        "refused": refused,
        "status": "HYPOTHESIS",
        "blocker": "PRODUCT-BLOCK",
        "clay_implication": "CONDITIONAL",
        "clay_weld": "WITHHELD",
        "refusal_reasons": reasons,
        "message": (
            "Refused: Lemma★ is not proved. Broken at PRODUCT-BLOCK → "
            "close by structure on T_c or SND/shell conditional."
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
            f"{len(withheld)} WITHHELD (Lemma★→Clay until PRODUCT-BLOCK); "
            "status HYPOTHESIS — DA refuses claiming PROVED."
        ),
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
            "close Clay — PRODUCT-BLOCK incomplete."
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
            "Broken at PRODUCT-BLOCK → close by structure on T_c=M−ΛN "
            "or conditional SND/dominant shell"
        ),
        "status": "OPEN",
        "need": "|T_c| <= C*||u||_2*X^{3/2}",
        "ordinary_3d": "INSUFFICIENT from energy alone",
        "book": book.to_dict(),
        "claim": claim.to_dict() if claim else None,
        "attack_routes": list(ATTACK_ROUTES),
        "clay_weld": "WITHHELD until closed",
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
    ids = {"LEMMA-STAR", "DA-NS-1", "PRODUCT-BLOCK"}
    return {
        "claims": [c for c in inv.get("claims", []) if c.get("claim_id") in ids],
        "refused_routings": [
            r
            for r in inv.get("refused_routings", [])
            if "lemma" in r.lower() or "da-ns" in r.lower()
        ],
    }
