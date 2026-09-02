"""Honest OPEN board: stop calling withdrawn / rejected / missing things OPEN.

This is a Domain Architect *use* of DECOMPOSE → TRANSLATE → SYNTHESIZE.
It does not prove Navier–Stokes, RH, or Goldbach. It closes the *status
noise* so the remaining leftovers are a short named list.

Buckets
-------
CLOSED_WITHDRAWN  — the claim is finished as a claim (do not keep saying OPEN)
CLOSED_REJECTED   — not on the DA board (dump, glue, product confusion)
CLOSED_MISSING    — no bytes here; that is a hunt, not a theorem
CLOSED_IDENTITY   — a yes/no question DA already answered
CONDITIONAL       — leftover-split: if σ then the rest closes; σ stays a hypothesis
DA_ENGINEERING    — software gates DA can actually flip (A13, A5, parser)
STILL_OPEN        — genuine remaining math / DA work
"""

from __future__ import annotations

from typing import Any

from .cycle import CycleReport
from .decompose import decompose
from .lab_cases import (
    LEFTOVER_SPLIT_STEPS,
    NS_LEFTOVERS,
    Q6_HN_LAB,
    RING_SND_LAB,
    SIMPLEX_LEFTOVER_LAB,
    SWIRL_LEFTOVER_LAB,
)
from .leftover_repair import leftover_repair
from .localized_repair import localized_repair
from .schema import CorrespondenceKind, ValidationGate
from .synthesize import inverse_design_architecture, is_recognized_setpoint
from .translate import snd_vs_h_translation


def _item(
    *,
    id: str,
    title: str,
    bucket: str,
    problem: str,
    fix: str,
    da_op: str,
) -> dict[str, str]:
    return {
        "id": id,
        "title": title,
        "bucket": bucket,
        "problem": problem,
        "fix": fix,
        "da_op": da_op,
    }


def board_items(*, a13_closed: bool) -> list[dict[str, str]]:
    a13_bucket = "CLOSED_IDENTITY" if a13_closed else "DA_ENGINEERING"
    a13_fix = (
        "Done: synthesize of NS / Clay / 'maximize profit' is inverse_design[refused]. "
        "Recognized setpoints (x=1, x → 1.0) still get a PD loop. DA-VC-01 overall "
        "stays FAIL until A5 (declared T on the swirl identity) lands. NS-open stays OPEN."
        if a13_closed
        else (
            "Implement A13: refuse a PD plant unless the target is a recognized "
            "setpoint. Do not treat A13 refuse as a DA-VC-01 pass."
        )
    )
    return [
        _item(
            id="all-n-floor",
            title="All-N floor λ_min(H_N) > -1/2",
            bucket="CLOSED_WITHDRAWN",
            problem="Was kept in the OPEN chorus after the claim was already pulled.",
            fix="Close as WITHDRAWN. Usable theory H is the Q6 definition only: "
            "HN = D^((-1)/2)*Qtilde*D^((-1)/2).",
            da_op="decompose Q6 H_N (def only)",
        ),
        _item(
            id="goldbach-dark",
            title="Dark-state ⇔ Goldbach; Goldbach 'should be closed'",
            bucket="CLOSED_WITHDRAWN",
            problem="Grok and old dumps keep reviving a withdrawn arithmetic claim.",
            fix="Close as WITHDRAWN / REJECTED. Q_N positive-definite stands as "
            "inverse-GCD arithmetic. Goldbach is not a DA gate.",
            da_op="none — not a DA plant",
        ),
        _item(
            id="ns-from-gcd",
            title="Navier–Stokes from GCD matrices",
            bucket="CLOSED_WITHDRAWN",
            problem="Letter collision: Q6 H_N is not Paper2 H_N[a] and not a fluids operator.",
            fix="Close as WITHDRAWN. Do not glue GCD spectra to NS regularity.",
            da_op="translate SND vs H_N (lab, not glue)",
        ),
        _item(
            id="t2-false-closed",
            title="Paper2 §7 'T2 Closed (conditional on SND)'",
            bucket="CLOSED_WITHDRAWN",
            problem="Local existence gives ||a-μ||_1 ≤ 2, not the 0.039 bound. The word OPEN was covering a *false close*.",
            fix="Close the false closure as WITHDRAWN. Remaining work is leftover 7–8 "
            "(Lemma 6.1 + dynamic SND), not a Gronwall slogan.",
            da_op="cycle localized-repair (default cut 7–8)",
        ),
        _item(
            id="a3-multiplier",
            title="April 2026 A3 production multiplier",
            bucket="CLOSED_REJECTED",
            problem="∫ω·Sω ≤ A3 ∫|ω|² λ_max^+ is false in general.",
            fix="Close as REJECTED. Production ≤ ∫|ω|² λ_max^+ stands. A3 is a "
            "weighted average, not a dominating multiplier. Track A archive only.",
            da_op="none — archive Track A, not live DA",
        ),
        _item(
            id="e8-nav42-product",
            title="Grok E8 / coating / vault dump as product",
            bucket="CLOSED_REJECTED",
            problem="Grok stacked dumps onto the OPEN pile as if they were DA work.",
            fix="Close as REJECTED Track C. Not live Domain Architect. Not Clay.",
            da_op="none — archive only",
        ),
        _item(
            id="gap1-same-matrix",
            title="GAP1: are operators A and B the same matrix?",
            bucket="CLOSED_IDENTITY",
            problem="Two kernels were left in an OPEN fog.",
            fix="Close as NO. Operator A is 1/(gcd√(ij)); B is μ(i/g)μ(j/g)g/√(ij). "
            "Frobenius mismatch is in the handoff. Remaining math is Step F only.",
            da_op="none — identity question answered; Step F stays STILL_OPEN",
        ),
        _item(
            id="missing-bytes",
            title="FIXED.tex, T2 Gronwall TeX, July 23 ledger, Alignment Functionals, Fluid notes",
            bucket="CLOSED_MISSING",
            problem="Missing files were spoken as if they were open theorems.",
            fix="Close as MISSING. Hunt is Cursor upload / paste / Base44 9-hex URL. "
            "Mac paths do not mount. Do not invent TeX.",
            da_op="none — bytes, not a decompose",
        ),
        _item(
            id="a13-pd-loop",
            title="DA-VC-01 S1 inverse-design PD loop",
            bucket=a13_bucket,
            problem="Synthesize of unaugmented NS emitted STATE→MEASURE→COMPARE→CONTROL→TRANSITION.",
            fix=a13_fix,
            da_op="synthesize S1 / cycle open-board",
        ),
        _item(
            id="a5-swirl-t",
            title="DA-VC-01 T1 declared map Γ ↦ r² Φ",
            bucket="DA_ENGINEERING",
            problem="Translate of the swirl identity without a declared T stays analogy / no_checked_structure_map. That is honest, but A5 wants the in-equation T with witness ∂_z(r^4)=0.",
            fix="Register T: Gamma |-> r^2 * Phi on {r>0} as a same-PDE map, not a "
            "cross-domain glue. Do not stamp TRANSFORMABLE without that T. "
            "This still does not close NS-open.",
            da_op="translate T1 (not yet a real T)",
        ),
        _item(
            id="swirl-strain",
            title="Swirl leftover ∫||u^r/r||_∞ dt",
            bucket="CONDITIONAL",
            problem="Energy does not bound intensive strain. Identity (I) already works.",
            fix="Leftover-split: keep (1/r^4)∂_z(Γ²)=∂_z(Φ²). Put back: if "
            "∫||u^r/r||_∞ dt < ∞ then continuation closes. σ stays a hypothesis. "
            "That is the only honest close DA can give this leftover.",
            da_op="decompose Istrain = urad/r ; cycle leftover-repair",
        ),
        _item(
            id="ring-snd",
            title="Unconditional Ring SND for large H¹",
            bucket="CONDITIONAL",
            problem="Energy / enstrophy does not give inf J/X ≥ c_*. Conditional Ring lemma already works.",
            fix="Leftover-split: if inf J/X ≥ c_* then the estimates run. Do not glue "
            "to Paper2 operator-norm SND.",
            da_op="decompose J/X >= cstar ; cycle leftover-repair",
        ),
        _item(
            id="paper2-simplex",
            title="Paper2 leftover 7–8 (Lemma 6.1 + dynamic SND)",
            bucket="CONDITIONAL",
            problem="Leray boundedness is not simplex smallness. Continuation (step 9) still owed.",
            fix="Localized reparation: default cut 7–8, graft independent simplex / "
            "dynamic-SND hypothesis, keep Ring Lemma (step 2, PROVED). Do not "
            "accept §7 T2 Closed. Clay Statement B not claimed.",
            da_op="cycle localized-repair",
        ),
        _item(
            id="gap1-step-f",
            title="GAP1 Step F / Fujii remainder",
            bucket="STILL_OPEN",
            problem="After log terms cancel, the Dirichlet remainder is not yet written as a Fujii oscillatory sum. 2π vs π² tension is in the handoff. C≈0.04706 is not in those bytes.",
            fix="One calculation: expand the remainder and match Fujii, or state the "
            "exact obstruction. Do not invent a 10–20 line closure. Do not claim "
            "λ_min/log N → -1/(2π) is a theorem. Do not claim RH.",
            da_op="none — arithmetic remainder; not a DA PD plant",
        ),
        _item(
            id="route-j",
            title="Frozen gap / Route J all-N",
            bucket="STILL_OPEN",
            problem="N≤800 numerical / under audit. No all-N theorem.",
            fix="Keep as NUMERICAL. Do not promote to OPEN regularity. Do not answer "
            "Route J from a missing claim ledger.",
            da_op="cycle localized-repair (keep step 4 unless you excise it)",
        ),
        _item(
            id="ns-open",
            title="Classical unaugmented NS (Clay Statement B / NS-open)",
            bucket="STILL_OPEN",
            problem="Closing NS-open is not a DA validation gate. Stamping it from DA is an automatic DA-VC-01 fail.",
            fix="Do not close. Score DA-VC-01 on honesty (A13, A5, refuse glue). "
            "Score NS-open only when the strain / simplex / SND hypotheses are proved "
            "in their own books.",
            da_op="cycle leftover-repair (shows the three carriers; does not prove them)",
        ),
    ]


def open_board() -> dict[str, Any]:
    """Classify the OPEN pile and attach live DA evidence for the leftovers."""
    ns_target = (
        "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl"
    )
    s1 = inverse_design_architecture(ns_target, ["classical NS", "no hyperviscosity"])
    a13_closed = s1.name == "inverse_design[refused]" and not any(
        "control u" in c for c in s1.components
    )
    items = board_items(a13_closed=a13_closed)
    leftover = leftover_repair()
    surgery = localized_repair()
    snd = decompose(RING_SND_LAB, name="ring_snd")
    hn = decompose(Q6_HN_LAB, name="q6_hn")
    swirl_fail = decompose(SWIRL_LEFTOVER_LAB, name="swirl_leftover")
    simplex_fail = decompose(SIMPLEX_LEFTOVER_LAB, name="simplex_leftover")
    snd_vs_h = snd_vs_h_translation()

    counts: dict[str, int] = {}
    for row in items:
        counts[row["bucket"]] = counts.get(row["bucket"], 0) + 1

    still = [row for row in items if row["bucket"] == "STILL_OPEN"]
    conditional = [row for row in items if row["bucket"] == "CONDITIONAL"]
    return {
        "protocol": "open-board",
        "headline": (
            "Most of the OPEN chorus is already closed as WITHDRAWN, REJECTED, "
            "or MISSING. DA leftover-split closes the three NS failures as "
            "conditional theorems. Clay / NS-open stays OPEN on purpose."
        ),
        "counts": counts,
        "a13_fail_closed": a13_closed,
        "recognized_setpoint_example": is_recognized_setpoint("x=1"),
        "s1": s1.to_dict(),
        "items": items,
        "still_open": still,
        "conditional": conditional,
        "leftover_split": {
            "pieces": leftover["pieces"],
            "reconstruction_closed": leftover["reconstruction"]["closed"],
            "honest_close": leftover["reconstruction"].get("honest_close"),
            "steps": list(LEFTOVER_SPLIT_STEPS),
        },
        "localized_repair": {
            "excised": [step["id"] for step in surgery.get("excised") or []],
            "graft": (surgery.get("chosen") or {}).get("name"),
        },
        "decompose": {
            "ring_snd": {"pattern": snd.classification.pattern, "warnings": list(snd.warnings)},
            "q6_hn": {"pattern": hn.classification.pattern, "warnings": list(hn.warnings)},
            "swirl_leftover": {
                "pattern": swirl_fail.classification.pattern,
                "warnings": list(swirl_fail.warnings),
            },
            "simplex_leftover": {
                "pattern": simplex_fail.classification.pattern,
                "warnings": list(simplex_fail.warnings),
            },
        },
        "translate_snd_vs_h": {
            "kind": snd_vs_h.kind.value,
            "mapping": dict(snd_vs_h.mapping),
            "broken": list(snd_vs_h.broken),
        },
        "da_vc_01": (
            "FAIL overall. S1 PD-loop hard fail is closed if A13_fail_closed. "
            "D1 still unclassified. T1 still has no declared T (A5). "
            "NS-open stays OPEN. Do not treat A13 refuse as a DA-VC-01 pass."
        ),
        "refused": [
            "no Clay / unaugmented regularity claim",
            "no Goldbach close",
            "no Grok coating / vault / E8 superstructure in live DA",
            "no letter map J→H / urad→J / a→HN",
            "no TRANSFORMABLE without a real T",
        ],
        "notes": [
            "Correspondence is a hypothesis, not physical equivalence.",
            "Closing a withdrawn claim is a close. Closing NS-open from DA is a fail.",
        ],
        "validation_gate": ValidationGate.MATHEMATICAL.value,
        "kind": CorrespondenceKind.ANALOGY.value,
    }


def cycle_open_board() -> CycleReport:
    payload = open_board()
    snd = decompose(RING_SND_LAB, name="ring_snd")
    from .synthesize import CandidateArchitecture, Provenance

    candidate = CandidateArchitecture(
        name="open_board_honest_close",
        components=[
            "withdrawn / rejected / missing items taken off the OPEN chorus",
            "three NS leftovers reconstructed as coercive part + independent σ",
            "A13 fail-closed inverse design for unrecognized targets",
        ],
        replaced={},
        hypothesis=(
            "The OPEN pile is mostly status noise. DA closes withdrawn claims, "
            "rejects dumps, and names three conditional leftovers. It does not "
            "prove classical Navier–Stokes."
        ),
        provenance=[
            Provenance(
                source="open-board protocol",
                original_domain="da-status",
                functional_role="constraint",
                translation=None,
                assumptions=["do not identify leftovers", "A13 fail-closed"],
                compatibility_checks=["glue refused", "no PD loop on NS"],
                modifications=[],
                evidence=[row["id"] for row in payload["still_open"]],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Not TRANSFORMABLE. Not Clay.",
            payload["headline"],
        ],
    )
    return CycleReport(
        mode="open-board",
        target=(
            "stop calling withdrawn/rejected/missing things OPEN; "
            "name the real leftovers and the DA fix for each"
        ),
        constraints=[
            "do not prove NS",
            "do not treat A13 refuse as a DA-VC-01 pass",
            "do not glue books",
            "no PD loop for open PDEs",
        ],
        decomposition=snd,
        translation=snd_vs_h_translation(),
        candidate=candidate,
        prediction=payload,
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            payload["headline"],
            f"A13 fail-closed: {payload['a13_fail_closed']}",
            f"still_open: {[row['id'] for row in payload['still_open']]}",
            f"conditional: {[row['id'] for row in payload['conditional']]}",
        ]
        + list(LEFTOVER_SPLIT_STEPS),
        method_credits=["open-board protocol", "leftover-split", "A13"],
    )
