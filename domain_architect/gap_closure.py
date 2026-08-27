"""NS/SND/Theorem-H gap closure — locate broken welds and propose fixes.

Domain Architect does not prove regularity. This module forces honest routing:
claiming Clay Statement (B) / unconditional SND while the keystone estimate
assumes X≤M is an INCOMPATIBLE glue. Output is always of the form

    Broken weld: … → Suggested closure: …

not a status list that only says OPEN.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .schema import CANONICAL_SFE_STATUS, ConflictRelation


# Canonical expressions for dual-compare and demos (organizational strings).
EXPR_NS_B = "partial_t omega = (omega * nabla) u + nu Delta omega"
EXPR_SND_HYP = "SND hypothesis: inf_t J(t)/X(t) >= c_* > 0  (X=||grad u||_L2^2, J=max_j X_j)"
EXPR_SND_C = (
    "SND-C (conditional): under X<=M, rho=J/X<=rho_0, X>=delta_*: "
    "|Pi_{j*}| <= C_*(nu,delta_*,M,rho_0) in spread regime"
)
EXPR_SND_U = (
    "SND-U (claimed unconditional): J/X >= c_* for all t>=0, all u0 in H^1(T^3); "
    "Clay Statement B resolved"
)
EXPR_Q1 = (
    "Q1 hyperdissipative: partial_t u + (u·nabla)u = -grad p + nu Delta u "
    "- epsilon (-Delta)^{1+delta} u; claim SND passes as epsilon->0"
)
EXPR_THM_H_WRITTEN = (
    "Theorem H as written: prove SND-C given X<=M and rho<=rho_0 "
    "(C_* depends on M)"
)
EXPR_CLAY_GLUE = (
    "Broken glue claim: Theorem H (X<=M) implies unconditional SND "
    "and Clay Statement B"
)


@dataclass(frozen=True)
class ClosureMove:
    """One concrete fix path for a detected weld."""

    break_id: str
    where_da: str
    where_math: str
    why: str
    closure_move: str
    patch_sketch: str
    success_test: str
    fake_closure_risk: str
    tractability_rank: int  # 1 = most tractable organizational fix
    kind: str  # structural | analytic

    def headline(self) -> str:
        return f"Broken at {self.break_id} → close by {self.closure_move}"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["headline"] = self.headline()
        return d


# Ranked closure catalog (structural + analytic). IDs match ARCHON gaps.
CLOSURE_CATALOG: tuple[ClosureMove, ...] = (
    ClosureMove(
        break_id="TH-H1",
        where_da=(
            "INCOMPATIBLE books: SND-C (assumes X≤M) glued to SND-U / Clay-B; "
            "illegal weld refused by gap router"
        ),
        where_math="Theorem H hypotheses: X≥δ_*, X≤M, ρ≤ρ₀ → C_*=C_*(…,M,…)",
        why=(
            "Clay (B) needs an H¹ bound from data alone; feeding X≤M into the "
            "keystone estimate smuggles the conclusion."
        ),
        closure_move=(
            "Split theorems: publish Theorem H strictly as (SND-C | X≤M); "
            "forbid any auto-route from H to Clay-B until an M-free lemma exists"
        ),
        patch_sketch=(
            "Replace claim 'H ⇒ Clay B' by two arrows: "
            "(i) H: (X≤M,ρ≤ρ₀)⇒SND-C; (ii) closure target: produce "
            "M=M(‖u₀‖_{H¹}) or remove M from C_*"
        ),
        success_test=(
            "DA registry marks SND-C001 ↔ CLAY-B001 INCOMPATIBLE; audits of "
            "glue claims print Broken weld TH-H1 and refuse unconditional routing"
        ),
        fake_closure_risk=(
            "Renaming 'unconditionally under the definition' as unconditional "
            "SND — same circular M"
        ),
        tractability_rank=1,
        kind="structural",
    ),
    ClosureMove(
        break_id="TH-H3",
        where_da=(
            "SND-C → SND arrow incomplete: c_* still M-dependent in book "
            "inventory (Theorem G)"
        ),
        where_math="Theorem G: (SND-C)⇒[SND] with c_*=c_*(ν,δ_*,M,C_S)",
        why="Even the implication to spectral gap c_* carries the enstrophy ceiling.",
        closure_move=(
            "Remove M from c_*: prove a universal floor c_*(ν,δ_*) independent "
            "of any a priori X≤M, or derive M from ‖u₀‖_{H¹} only"
        ),
        patch_sketch=(
            "Target: ∃ c_*>0 depending only on (ν,δ_*,geometry) s.t. "
            "J/X≥c_* on [0,T_*) whenever SND-C holds without feeding M back"
        ),
        success_test=(
            "Candidate completion accepted only if C_*/c_* annotations drop M; "
            "dual compare SND-C vs SND-U no longer needs M on the U side"
        ),
        fake_closure_risk="Absorbing M into 'universal' constants that still scale with data size",
        tractability_rank=2,
        kind="analytic",
    ),
    ClosureMove(
        break_id="TH-H4",
        where_da=(
            "Dominant-shell propagation role incomplete under unaugmented NS-B "
            "book — extras list lacks proved all-time j_* persistence"
        ),
        where_math="Theorem G proof: ρ̇>0 when ρ small, assuming SND-C + M",
        why="Propagation is a conditional ODE under a priori bounds, not all-data dynamics.",
        closure_move=(
            "Propagate dominant shell for all Leray–Hopf data: close ρ̇ estimate "
            "without SND-C circular input, or prove j_* cannot jump forever"
        ),
        patch_sketch=(
            "Show inf_t ρ(t)≥c_* via a differential inequality on ρ that uses "
            "only energy/enstrophy identities available for Leray–Hopf weak solutions"
        ),
        success_test=(
            "Reconstruction extras include 'dominant_shell_propagation_proved'; "
            "compare NS-B vs SND-U shares that extra without X≤M marker"
        ),
        fake_closure_risk="Proving propagation only inside the spread regime already conditioned on M",
        tractability_rank=3,
        kind="analytic",
    ),
    ClosureMove(
        break_id="TH-H7-Q1",
        where_da=(
            "Q1-augmented book vs NS-B: ε→0 limit missing SND-pass finger; "
            "incompleteness flags absent limit justification"
        ),
        where_math="Q1→Leray–Hopf: uniform SND / H¹ bounds through ε→0",
        why="Hyperdissipative approximants may hold SND while the limit silently loses it.",
        closure_move=(
            "Pass SND through the Q1 limit: obtain ε-uniform J/X≥c_* and "
            "justify liminf on Leray–Hopf solutions"
        ),
        patch_sketch=(
            "Prove liminf_{ε→0} ρ_ε(t) ≥ c_* and identify limit vorticity "
            "with a Leray–Hopf solution without assuming smoothness of the limit"
        ),
        success_test=(
            "DA incompleteness for Q1 claims lists candidate "
            "'snd_limit_passage'; audits refuse Clay glue via Q1 alone"
        ),
        fake_closure_risk="Using smooth approximant SND as if it were the weak-limit law",
        tractability_rank=4,
        kind="analytic",
    ),
    ClosureMove(
        break_id="TH-H2",
        where_da=(
            "Naming fraud: status table greens 'Theorem H unconditional' while "
            "definition still carries M — registry disposition RETIRE for Clay glue"
        ),
        where_math="20405526 status table vs SND-C definition with C_*(…,M,…)",
        why="'Unconditionally' under hypotheses ≠ SND for all H¹ data.",
        closure_move=(
            "Retire/park Statement-B packaging; keep Zenodo KEEP conditional "
            "SND framing; force DA disposition RETIRE on Clay-B001"
        ),
        patch_sketch=(
            "Public text: 'Ring+SND hypothesis / conditional only'; "
            "delete greens that say Clay B resolved"
        ),
        success_test=(
            "CLAY-B001 audit_disposition=RETIRE; conflict with SND-C001 recorded; "
            "CLI refuses unconditional claim language"
        ),
        fake_closure_risk="Keeping the green table while adding a footnote nobody reads",
        tractability_rank=5,
        kind="structural",
    ),
    ClosureMove(
        break_id="TH-H3-BOOT",
        where_da=(
            "Bootstrap lemma slot BOOT-M001: candidate M=M(||u₀||_{H¹}) "
            "compatible with SND-C001; open analytic completion at TH-H3"
        ),
        where_math=(
            "Derive enstrophy ceiling from H¹ data before feeding Theorem H; "
            "must not assume X≤M as keystone input"
        ),
        why=(
            "If M is derived from u₀ alone (not from regularity we are proving), "
            "SND-C stops smuggling the Clay conclusion — but c_* must still drop M."
        ),
        closure_move=(
            "Prove bootstrap lemma: ∃ M=M(||u₀‖_{H¹}) with X(t)≤M on [0,T*) "
            "using only energy/enstrophy identities available to Leray–Hopf"
        ),
        patch_sketch=(
            "Lemma (Bootstrap-M): from u₀∈H¹ div-free, produce M depending only "
            "on ‖u₀‖_{H¹}, ν, geometry s.t. sup_{t∈[0,T)} X(t)≤M. Then feed "
            "Theorem H as conditional on derived M, not assumed M."
        ),
        success_test=(
            "DA registry marks BOOT-M001 ↔ SND-C001 COMPATIBLE_DISTINCT; "
            "incompleteness lists bootstrap candidate; H→Clay still refused "
            "until c_* is M-free"
        ),
        fake_closure_risk=(
            "Using smooth approximant enstrophy bounds as if they were "
            "Leray–Hopf a priori bounds"
        ),
        tractability_rank=2,
        kind="analytic",
    ),
    ClosureMove(
        break_id="TH-H5",
        where_da=(
            "CSTAR-ARITH001 RETIRE: c*=6/π² glued to fluids SND floor; "
            "registry INCOMPATIBLE with SND-U001"
        ),
        where_math="zeta(2)^{-1} squarefree density vs fluids c_*(δ_KT, ν)",
        why="Arithmetic packaging is analogy, not continuum NS threshold.",
        closure_move=(
            "Remove c*=6/π² from fluids SND claims; keep as arithmetic note only"
        ),
        patch_sketch=(
            "Public text: fluids c_* is data-dependent when present; "
            "6/π² is Triple Lock analogy only"
        ),
        success_test=(
            "DA refuses c*=6/pi^2 as NS SND threshold; CSTAR-ARITH001 RETIRE"
        ),
        fake_closure_risk="Renaming arithmetic density as 'universal fluids constant'",
        tractability_rank=6,
        kind="structural",
    ),
    ClosureMove(
        break_id="TH-H6",
        where_da=(
            "RING-LEM001/BVB-EC001 INCOMPATIBLE with CLAY-B001 rescue; "
            "band-limited geometry ≠ unconditional SND"
        ),
        where_math="Ring on E_c with shell support; not global CF",
        why="ARCHON panel: Ring+BVB does not replace proved SND for all data.",
        closure_move=(
            "Keep Ring+BVB as toolkit; forbid routing Ring→Clay B rescue"
        ),
        patch_sketch=(
            "Explicit: Ring Lemma hypotheses (shell support, E_c) must be "
            "stated; no Main Theorem rescue via Ring alone"
        ),
        success_test=(
            "Registry RING-LEM001↔CLAY-B001 INCOMPATIBLE; gap router refuses "
            "Ring+BVB implies Clay"
        ),
        fake_closure_risk="Treating band-limited CF as global regularity",
        tractability_rank=7,
        kind="structural",
    ),
)


@dataclass
class WeldFinding:
    break_id: str
    severity: str  # refuse | warn
    broken_weld: str
    suggested_closure: str
    markers_hit: list[str] = field(default_factory=list)
    relation: str = ConflictRelation.INCOMPATIBLE.value
    move: ClosureMove | None = None

    def narrative_line(self) -> str:
        return (
            f"Broken weld: {self.broken_weld} "
            f"Suggested closure: {self.suggested_closure}"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "break_id": self.break_id,
            "severity": self.severity,
            "broken_weld": self.broken_weld,
            "suggested_closure": self.suggested_closure,
            "markers_hit": self.markers_hit,
            "relation": self.relation,
            "headline": self.move.headline() if self.move else "",
            "move": self.move.to_dict() if self.move else None,
            "narrative": self.narrative_line(),
        }


@dataclass
class GapClosureReport:
    input_expression: str
    refuses_unconditional_clay: bool
    findings: list[WeldFinding] = field(default_factory=list)
    ranked_closures: list[dict[str, Any]] = field(default_factory=list)
    domain_book_hint: str = "generic"
    statement: str = ""
    canonical_sfe_status: str = CANONICAL_SFE_STATUS

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_expression": self.input_expression,
            "refuses_unconditional_clay": self.refuses_unconditional_clay,
            "findings": [f.to_dict() for f in self.findings],
            "ranked_closures": self.ranked_closures,
            "domain_book_hint": self.domain_book_hint,
            "statement": self.statement,
            "canonical_sfe_status": self.canonical_sfe_status,
        }

    def narrative(self) -> str:
        lines = [
            "Domain Architect — SND/Theorem-H gap closure",
            "",
            "Loop: locate weld → refuse illegal glue → propose closure move.",
            "Not a Clay proof engine; honest routing only.",
            "",
            f"Input: {self.input_expression}",
            f"Book hint: {self.domain_book_hint}",
            f"Refuses unconditional Clay claim: {self.refuses_unconditional_clay}",
            "",
        ]
        if not self.findings:
            lines.append(
                "No illegal Clay↔(X≤M) weld detected in this string. "
                "If you intended an unconditional claim, state it explicitly "
                "so DA can refuse it."
            )
        else:
            lines.append("Findings:")
            for f in self.findings:
                lines.append(f"  [{f.break_id}/{f.severity}] {f.narrative_line()}")
                if f.move:
                    lines.append(f"    Headline: {f.move.headline()}")
                    lines.append(f"    Patch: {f.move.patch_sketch}")
                    lines.append(f"    Success test: {f.move.success_test}")
        lines.append("")
        lines.append(self.statement)
        lines.append(f"Canonical SFE status: {self.canonical_sfe_status}.")
        return "\n".join(lines)


def _norm(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("\\", "")
        .replace("{", "")
        .replace("}", "")
        .replace("≤", "<=")
        .replace("≥", ">=")
    )


def _move_by_id(break_id: str) -> ClosureMove:
    for m in CLOSURE_CATALOG:
        if m.break_id == break_id:
            return m
    raise KeyError(break_id)


def detect_claim_markers(expression: str) -> dict[str, bool]:
    """Structural markers for SND/Clay claim analysis (not physics)."""
    raw = expression.lower()
    compact = _norm(expression)
    return {
        "x_le_m": (
            "x<=m" in compact
            or "x≤m" in expression.lower()
            or "enstrophyceiling" in compact
            or "apriori" in compact and "m" in compact
            or ("x<=" in compact and "m" in compact)
        ),
        "snd_c": (
            "snd-c" in raw
            or "snd_c" in raw
            or "shell-conditioned" in raw
            or "shellconditioned" in compact
            or ("spread" in raw and "rho" in compact)
        ),
        "snd_u": (
            "snd-u" in raw
            or "snd_u" in raw
            or "unconditional snd" in raw
            or "unconditionalsnd" in compact
            or ("snd" in raw and "all" in raw and "h^1" in raw)
            or ("snd" in raw and "allu0" in compact)
        ),
        "clay_b": (
            "clay" in raw
            or "statement b" in raw
            or "statement(b)" in compact
            or "millennium" in raw
        ),
        "thm_h": "theorem h" in raw or "theoremh" in compact,
        "q1": (
            "q1" in raw
            or "hyperdissipat" in raw
            or "epsilon" in compact
            or "ε" in expression
        ),
        "dominant_shell": (
            "dominant shell" in raw
            or "dominantshell" in compact
            or "j*" in raw
            or "j_*" in raw
        ),
        "m_dependent_c": (
            "c_*(nu" in compact
            or "c_*=c_*(" in compact
            or "depend" in raw and "m" in raw and ("c_*" in raw or "c*" in compact)
        ),
        "snd_hypothesis": (
            "snd hypothesis" in raw
            or "conditional snd" in raw
            or ("inf" in compact and "j" in compact and "x" in compact and "c" in compact)
        ),
        "cstar_arithmetic": (
            "6/pi^2" in compact
            or "6/pi^2" in raw
            or "zeta(2)" in compact
            or "c_*=6" in compact
        ),
        "ring_bvb": (
            "ring lemma" in raw
            or "ringlemma" in compact
            or "bvb" in raw
            or "e_c" in raw
            or "beale" in raw
        ),
        "bootstrap_m": (
            "bootstrap" in raw
            or "m=||u0||" in compact
            or "m(||u" in compact
        ),
        "bypass_lemma": (
            "bypass lemma" in raw
            or "tilde_h_n" in compact
            or "tildehn" in compact
            or "shell-helical" in raw
            or "shellhelical" in compact
            or ("lambdamin" in compact and "lambdamax" in compact)
            or ("lambda_min" in raw and "lambda_max" in raw)
        ),
        "clay_equiv": (
            ("<=>" in expression or "<->" in expression or "iff" in raw)
            and "clay" in raw
            and "snd" in raw
        ),
        "global_regularity_proved": (
            ("global regularity" in raw or "no blowup" in raw or "no finite-time blowup" in raw)
            and ("proved" in raw or "resolved" in raw or "no blowup" in raw)
        ),
        "ns_classical": (
            "partial_t" in compact
            or "∂_t" in expression
            or "navier" in raw
            or ("omega" in compact and "nu" in compact)
        ),
    }


def diagnose_gap(expression: str) -> GapClosureReport:
    """Locate broken welds in a claim/expression string and propose closures."""
    markers = detect_claim_markers(expression)
    findings: list[WeldFinding] = []

    # Cross-check sibling claim anatomizer when available (shared inventory).
    try:
        from .snd_claims import anatomize_claim

        claim_audit = anatomize_claim(expression)
        if claim_audit.refused and not (
            markers["x_le_m"] or markers["snd_c"] or markers["thm_h"]
        ):
            # Standalone overclaim language — ensure refuse path fires.
            markers["clay_b"] = markers["clay_b"] or any(
                h.claim_id == "CLAY-B" for h in claim_audit.hits
            )
            markers["snd_u"] = markers["snd_u"] or any(
                h.claim_id == "SND-U" for h in claim_audit.hits
            )
    except Exception:
        claim_audit = None

    # Primary illegal glue: X≤M (or SND-C / Thm H as written) + unconditional Clay/SND-U
    illegal_glue = (markers["x_le_m"] or markers["snd_c"] or markers["thm_h"]) and (
        markers["snd_u"] or markers["clay_b"]
    )
    if illegal_glue:
        move = _move_by_id("TH-H1")
        hit = [k for k, v in markers.items() if v]
        findings.append(
            WeldFinding(
                break_id="TH-H1",
                severity="refuse",
                broken_weld=(
                    "Claiming Clay Statement B / unconditional SND while the "
                    "keystone estimate assumes X≤M (or is only SND-C / Theorem H "
                    "as written)"
                ),
                suggested_closure=move.closure_move,
                markers_hit=hit,
                relation=ConflictRelation.INCOMPATIBLE.value,
                move=move,
            )
        )

    if markers["m_dependent_c"] and (markers["snd_u"] or markers["clay_b"]):
        move = _move_by_id("TH-H3")
        findings.append(
            WeldFinding(
                break_id="TH-H3",
                severity="refuse",
                broken_weld="c_* still depends on M while claim is unconditional SND",
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                move=move,
            )
        )

    if markers["dominant_shell"] and markers["x_le_m"] and (
        markers["snd_u"] or markers["clay_b"]
    ):
        move = _move_by_id("TH-H4")
        findings.append(
            WeldFinding(
                break_id="TH-H4",
                severity="warn",
                broken_weld=(
                    "Dominant-shell propagation cited for Clay while still "
                    "conditioned on X≤M / SND-C"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                move=move,
            )
        )

    if markers["q1"] and (markers["snd_u"] or markers["clay_b"]):
        move = _move_by_id("TH-H7-Q1")
        findings.append(
            WeldFinding(
                break_id="TH-H7-Q1",
                severity="refuse",
                broken_weld=(
                    "Q1/ε→0 path used to claim unconditional SND / Clay without "
                    "proved SND passage to the limit"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                move=move,
            )
        )

    # Tweet Thm D style: Clay ⇔ [SND] packaged as proved equivalence
    if markers["clay_equiv"] and not any(f.break_id == "TH-H2" for f in findings):
        move = _move_by_id("TH-H2")
        findings.append(
            WeldFinding(
                break_id="TH-H2",
                severity="refuse",
                broken_weld=(
                    "Clay ⇔ SND equivalence is not established; "
                    "SND-U remains open and SND-C assumes X≤M"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                move=move,
            )
        )

    # Tweet main-result style: global regularity / no blowup marked proved
    if markers["global_regularity_proved"] and not (
        markers["x_le_m"] or markers["snd_c"] or markers["thm_h"]
    ):
        move = _move_by_id("TH-H2")
        if not any(f.break_id == "TH-H2" for f in findings):
            findings.append(
                WeldFinding(
                    break_id="TH-H2",
                    severity="refuse",
                    broken_weld=(
                        "Global regularity / no-blowup on T³ marked proved "
                        "without M-free keystone — Clay Statement B NOT resolved"
                    ),
                    suggested_closure=move.closure_move,
                    markers_hit=[k for k, v in markers.items() if v],
                    move=move,
                )
            )

    # Standalone unconditional Clay / SND-U without any conditional honesty markers
    if (markers["snd_u"] or markers["clay_b"]) and not findings:
        move = _move_by_id("TH-H2")
        findings.append(
            WeldFinding(
                break_id="TH-H2",
                severity="refuse",
                broken_weld=(
                    "Unconditional Clay / SND-U claim with no proved M-free "
                    "keystone — illegal under current registry"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                move=move,
            )
        )

    # Theorem H alone (as written) — incomplete for Clay, suggest split
    if markers["thm_h"] and markers["x_le_m"] and not (
        markers["snd_u"] or markers["clay_b"]
    ):
        move = _move_by_id("TH-H1")
        findings.append(
            WeldFinding(
                break_id="TH-H1",
                severity="warn",
                broken_weld=(
                    "Theorem H as written is SND-C under X≤M — incomplete as a "
                    "Clay keystone (do not green as unconditional)"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                relation=ConflictRelation.INSUFFICIENT_INFORMATION.value,
                move=move,
            )
        )

    if markers["cstar_arithmetic"] and (markers["snd_u"] or markers["clay_b"] or markers["snd_c"]):
        move = _move_by_id("TH-H5")
        findings.append(
            WeldFinding(
                break_id="TH-H5",
                severity="refuse",
                broken_weld=(
                    "c_*=6/π² (arithmetic) cited as continuum NS SND floor "
                    "while claiming SND/Clay"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                move=move,
            )
        )

    if markers["ring_bvb"] and (markers["snd_u"] or markers["clay_b"]):
        move = _move_by_id("TH-H6")
        findings.append(
            WeldFinding(
                break_id="TH-H6",
                severity="refuse",
                broken_weld=(
                    "Ring Lemma / BVB on E_c used to rescue Clay B or "
                    "unconditional SND — band-limited toolkit only"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                move=move,
            )
        )

    if markers["bootstrap_m"] and markers["snd_c"] and not (
        markers["snd_u"] or markers["clay_b"]
    ):
        move = _move_by_id("TH-H3-BOOT")
        findings.append(
            WeldFinding(
                break_id="TH-H3-BOOT",
                severity="warn",
                broken_weld=(
                    "Bootstrap M from H¹ data is the candidate slot to "
                    "de-circularize Theorem H input — still open"
                ),
                suggested_closure=move.closure_move,
                markers_hit=[k for k, v in markers.items() if v],
                relation=ConflictRelation.INSUFFICIENT_INFORMATION.value,
                move=move,
            )
        )

    refuses = any(f.severity == "refuse" for f in findings)
    if markers["ns_classical"] and not (
        markers["snd_u"] or markers["clay_b"] or markers["snd_c"]
    ):
        book = "NS-B"
    elif markers["bootstrap_m"]:
        book = "BOOT-M"
    elif markers["snd_c"] or markers["x_le_m"]:
        book = "SND-C"
    elif markers["snd_u"] or markers["clay_b"]:
        book = "SND-U"
    elif markers["q1"]:
        book = "NS-Q1"
    elif markers["ring_bvb"]:
        book = "RING-BVB"
    elif markers["bypass_lemma"]:
        book = "SND-BYPASS"
    elif markers["cstar_arithmetic"]:
        book = "CSTAR-ARITH"
    elif markers["snd_hypothesis"]:
        book = "SND-HYP"
    else:
        book = "generic"

    ranked = [
        m.to_dict()
        for m in sorted(CLOSURE_CATALOG, key=lambda m: m.tractability_rank)
    ]

    if refuses:
        statement = (
            "DA refuses unconditional Clay / SND-U routing for this input. "
            "Broken welds listed above; apply suggested closures. "
            "Keep conditional SND hypothesis framing until an M-free weld exists."
        )
    elif findings:
        statement = (
            "Incomplete keystone detected. Close the weld before any Clay packaging."
        )
    else:
        statement = (
            "No Clay-illegal weld in this expression. Classical NS-B / conditional "
            "SND remain honest books."
        )

    return GapClosureReport(
        input_expression=expression,
        refuses_unconditional_clay=refuses,
        findings=findings,
        ranked_closures=ranked,
        domain_book_hint=book,
        statement=statement,
    )


def ranked_top_closures(n: int = 5) -> list[ClosureMove]:
    return sorted(CLOSURE_CATALOG, key=lambda m: m.tractability_rank)[:n]


def snd_c_vs_snd_u_compare() -> dict[str, Any]:
    """Dual structural compare: conditional SND-C vs claimed unconditional SND-U."""
    left = diagnose_gap(EXPR_SND_C)
    right = diagnose_gap(EXPR_SND_U)
    glue = diagnose_gap(EXPR_CLAY_GLUE)
    return {
        "left_label": "SND-C (conditional under X≤M)",
        "right_label": "SND-U (claimed unconditional)",
        "left": left.to_dict(),
        "right": right.to_dict(),
        "glue_claim": glue.to_dict(),
        "relation": ConflictRelation.INCOMPATIBLE.value,
        "why_incompatible": (
            "SND-C assumes an a priori enstrophy ceiling X≤M; SND-U / Clay B "
            "claims a bound from H¹ data alone. Gluing them is the TH-H1 weld."
        ),
        "suggested_closure": _move_by_id("TH-H1").closure_move,
        "narrative": (
            f"Broken weld: SND-C (X≤M) ≇ SND-U/Clay-B. "
            f"Suggested closure: {_move_by_id('TH-H1').closure_move}"
        ),
        "canonical_sfe_status": CANONICAL_SFE_STATUS,
    }


def gap_closure_candidates_for_incompleteness(
    expression: str,
) -> list[dict[str, Any]]:
    """Candidate completions that point at weld fixes (for incompleteness attach)."""
    report = diagnose_gap(expression)
    out: list[dict[str, Any]] = []
    for f in report.findings:
        out.append(
            {
                "kind": "gap_closure_weld",
                "proposal": f.narrative_line(),
                "book_source": report.domain_book_hint,
                "confidence": "template",
                "honesty_note": (
                    "Organizational closure move only — not a proved regularity theorem."
                ),
                "break_id": f.break_id,
            }
        )
    if report.refuses_unconditional_clay and not out:
        move = _move_by_id("TH-H1")
        out.append(
            {
                "kind": "gap_closure_weld",
                "proposal": (
                    f"Broken weld: unconditional Clay claim. "
                    f"Suggested closure: {move.closure_move}"
                ),
                "book_source": "SND-U",
                "confidence": "template",
                "honesty_note": move.fake_closure_risk,
                "break_id": "TH-H1",
            }
        )
    return out
