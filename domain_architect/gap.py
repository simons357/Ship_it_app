"""Stop at a wall; show the missing piece and the candidates after.

A pass is not continuation past an open weld. Failures before the wall
are clipped and the walk continues. The first open step is a STOP.
Everything listed after is a candidate or a refused bypass, not a step
already taken.

The missing piece sits BETWEEN the last walked step and the first
candidate that would need the weld. Seeing the candidates does not
fill the gap.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Final, Iterable, Mapping, Sequence


WALK_STATUSES: Final[frozenset[str]] = frozenset(
    {"pass", "given", "setup", "architecture"}
)
REFUSE_STATUSES: Final[frozenset[str]] = frozenset({"fail"})
STOP_STATUSES: Final[frozenset[str]] = frozenset({"open"})


def _status(step: Mapping[str, Any]) -> str:
    return str(step.get("status") or step.get("verdict") or "")


def _label(step: Mapping[str, Any]) -> str:
    return str(step.get("step") or step.get("id") or "?")


def _clip(step: Mapping[str, Any]) -> str:
    return str(step.get("clip_id") or step.get("remainder_id") or "—")


def _remainder(step: Mapping[str, Any]) -> str:
    return str(
        step.get("remainder")
        or step.get("clip")
        or step.get("inequality")
        or step.get("statement")
        or ""
    )


def _body(step: Mapping[str, Any]) -> str:
    return str(
        step.get("inequality")
        or step.get("statement")
        or step.get("geometric_picture")
        or step.get("what")
        or ""
    )


@dataclass(frozen=True)
class Candidate:
    step: str
    status: str
    relation: str
    why: str
    clip_id: str
    body: str
    in_chain: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MissingPiece:
    gap_id: str
    between: tuple[str, str]
    wall_step: str
    clips: tuple[dict[str, str], ...]
    would_fill: str
    not_filled_by: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["between"] = list(self.between)
        d["clips"] = [dict(c) for c in self.clips]
        d["not_filled_by"] = list(self.not_filled_by)
        return d


@dataclass
class GapReport:
    book: str
    chain: str
    stopped: bool
    walked: list[dict[str, Any]] = field(default_factory=list)
    refused_before_wall: list[dict[str, Any]] = field(default_factory=list)
    wall: dict[str, Any] | None = None
    missing: dict[str, Any] | None = None
    candidates_after: list[dict[str, Any]] = field(default_factory=list)
    refused_bypasses: list[dict[str, Any]] = field(default_factory=list)
    rule: str = (
        "Hit a wall: stop. Name the missing piece between the wall and "
        "the next candidate. Listing candidates is not walking them."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "book": self.book,
            "chain": self.chain,
            "stopped": self.stopped,
            "rule": self.rule,
            "walked": list(self.walked),
            "refused_before_wall": list(self.refused_before_wall),
            "wall": self.wall,
            "missing": self.missing,
            "candidates_after": list(self.candidates_after),
            "refused_bypasses": list(self.refused_bypasses),
        }


# How each later tube step sits relative to the T3 wall.
TUBE_RELATIONS: Final[dict[str, tuple[str, str]]] = {
    "T4": (
        "parallel",
        "Architecture only: δ ∼ 2^{-j*} names the scale. Does not weld traces to I_off.",
    ),
    "T5": (
        "needs_gap",
        "First piece after the gap: |I_tube| vs viscosity. Cannot walk this until the weld is filled or a different tube estimate is written.",
    ),
    "T6": (
        "needs_gap",
        "Angular 1/r² vs I_tube. Sits after T5, or a direct contest in the same tube. Does not fill CLIP-T3-WELD.",
    ),
    "T7": (
        "needs_gap",
        "Gronwall R ∈ L¹ would close X. Needs R from T5/T6 and/or Ring and/or spread. Not a fill of this gap.",
    ),
}

TUBE_EXTRAS: Final[tuple[dict[str, Any], ...]] = (
    {
        "step": "spread Bony T",
        "status": "open",
        "relation": "other_chart",
        "why": "Cartesian T^3 paraproduct on the SPREAD chart. No Γ, no tube. Does not fill CLIP-T3-WELD. Do not glue H onto the cylinder.",
        "clip_id": "CLIP-T4-SPREAD",
        "body": "energy-class low Bony T, no Φ, no Q1",
        "in_chain": False,
    },
    {
        "step": "Ring on E_c",
        "status": "pass",
        "relation": "parallel",
        "why": "Already have B3 (Bernstein / |∇ξ| on a 3-shell). Parallel vorticity chart. Does not control I_off.",
        "clip_id": "CLIP-B3b-ALIGN",
        "body": "3-shell Ring; alignment still clipped",
        "in_chain": False,
    },
)

TUBE_BYPASSES: Final[tuple[dict[str, str], ...]] = (
    {
        "step": "Φ-cancel",
        "why": "1/r^4 ∂_z(Γ²)=∂_z(Φ_θ²) is true and moves the work onto ‖Φ_θ‖_∞. Not a fill.",
        "clip_id": "CLIP-PHI-LINFTY",
    },
    {
        "step": "BKM from L²",
        "why": "Integrable enstrophy is not L^∞ (B6). Not a fill.",
        "clip_id": "CLIP-B6-SPIKE",
    },
    {
        "step": "glue Theorem H onto the tube",
        "why": "H is a Cartesian paraproduct. The tube is cylindrical swirl. Wrong manifold.",
        "clip_id": "CLIP-T4-SPREAD",
    },
    {
        "step": "pick the L² scaling chart",
        "why": "L² makes the wall look small; Bernstein L^∞ makes it look large. Choosing the optimistic chart is not a lemma.",
        "clip_id": "CLIP-T3-WELD",
    },
)

TUBE_MISSING: Final[dict[str, Any]] = {
    "gap_id": "GAP-T3",
    "between": ("T3a", "T5"),
    "would_fill": (
        "A lemma that bounds I_off by Hardy/Young traces on T^3: same "
        "fields (not Γ² vs (Γ ∂_z Γ) ω^r), and without an outer radius "
        "where Γ vanishes. Until that lemma exists, T5 is a candidate, "
        "not a step."
    ),
    "not_filled_by": (
        "T3a (cylinder identity, extra E)",
        "T4 (names δ, no weld)",
        "spread Bony T (other chart)",
        "Φ-cancel",
        "L² scaling slogan",
    ),
}

CHAIN_RELATIONS: Final[dict[str, tuple[str, str]]] = {
    "B5": (
        "parallel",
        "Cylindrical Laplacian identity. Already known. Does not absorb I_tube. Walking past B4b on this identity is a camera cheat.",
    ),
    "B5b": (
        "needs_gap",
        "Angular viscosity vs I_tube. First live candidate after the Hardy wall. Needs CLIP-B4b-ITUBE or a different tube estimate.",
    ),
    "B6": (
        "refused",
        "∫X dt < ∞ ⇒ X ∈ L^∞ already failed. Not a candidate after the wall.",
    ),
    "B-Φ": (
        "refused",
        "Change of unknown to Φ_θ already failed. Not a candidate.",
    ),
    "B-reg": (
        "needs_gap",
        "Regularity would sit after a constructed R. Not this gap, and not walked.",
    ),
}

CHAIN_EXTRAS: Final[tuple[dict[str, Any], ...]] = (
    {
        "step": "T3a Young trace",
        "status": "pass",
        "relation": "parallel",
        "why": "Cylinder identity from outside, already in --tube B. Extra E (CLIP-T3-OUTER). Does not fill B4b.",
        "clip_id": "CLIP-T3-OUTER",
        "body": "h(R)=0 ⇒ h(δ)² ≤ ε∫ r(h')² + ε^{-1}∫ h²/r",
        "in_chain": False,
    },
    {
        "step": "spread Bony T",
        "status": "open",
        "relation": "other_chart",
        "why": "Spread chart on T^3. Does not fill I_tube.",
        "clip_id": "CLIP-T4-SPREAD",
        "body": "energy-class low Bony T",
        "in_chain": False,
    },
)

CHAIN_BYPASSES: Final[tuple[dict[str, str], ...]] = TUBE_BYPASSES

CHAIN_MISSING: Final[dict[str, Any]] = {
    "gap_id": "GAP-B4b",
    "between": ("B4", "B5b"),
    "would_fill": (
        "A bound |I_tube| ≤ ε ν‖∇ω‖_2² + remainder with the remainder "
        "controlled at δ ∼ 2^{-j*}, keeping 1/r^4 and Γ. Hardy+wall is "
        "the tool. This bound is the missing piece. B5 is not it."
    ),
    "not_filled_by": (
        "B4 (Hardy identity + wall clip)",
        "B5 (Laplacian identity)",
        "B6 (energy slogan, failed)",
        "Φ-cancel",
    ),
}


def locate_gap(
    steps: Sequence[Mapping[str, Any]],
    *,
    book: str = "B",
    chain: str = "tube",
    relations: Mapping[str, tuple[str, str]] | None = None,
    extras: Iterable[Mapping[str, Any]] | None = None,
    bypasses: Iterable[Mapping[str, str]] | None = None,
    missing_spec: Mapping[str, Any] | None = None,
) -> GapReport:
    """Split a chain at the first open step. Do not walk past it."""
    walked: list[dict[str, Any]] = []
    refused: list[dict[str, Any]] = []
    wall: dict[str, Any] | None = None
    after: list[Mapping[str, Any]] = []
    hit = False
    for raw in steps:
        step = dict(raw)
        st = _status(step)
        if not hit:
            if st in STOP_STATUSES:
                wall = {
                    "step": _label(step),
                    "status": st,
                    "clip_id": _clip(step),
                    "body": _body(step),
                    "remainder": _remainder(step),
                    "geometry": str(step.get("geometry") or step.get("looks_like") or ""),
                }
                hit = True
            elif st in REFUSE_STATUSES:
                refused.append(
                    {
                        "step": _label(step),
                        "status": st,
                        "clip_id": _clip(step),
                        "body": _body(step),
                        "remainder": _remainder(step),
                    }
                )
            else:
                walked.append(
                    {
                        "step": _label(step),
                        "status": st,
                        "clip_id": _clip(step),
                        "body": _body(step),
                        "remainder": _remainder(step),
                    }
                )
        else:
            after.append(step)

    rels = dict(relations or {})
    candidates: list[dict[str, Any]] = []
    for step in after:
        name = _label(step)
        relation, why = rels.get(
            name,
            (
                "unspecified",
                "Listed after the wall. Not walked. Relation not catalogued.",
            ),
        )
        candidates.append(
            Candidate(
                step=name,
                status=_status(step),
                relation=relation,
                why=why,
                clip_id=_clip(step),
                body=_body(step),
                in_chain=True,
            ).to_dict()
        )
    for extra in extras or ():
        item = dict(extra)
        item["in_chain"] = bool(item.get("in_chain", False))
        candidates.append(item)

    last_walked = walked[-1]["step"] if walked else "?"
    first_need = next(
        (c["step"] for c in candidates if c.get("relation") == "needs_gap"),
        candidates[0]["step"] if candidates else "?",
    )
    spec = dict(missing_spec or {})
    clips: list[dict[str, str]] = []
    if wall is not None:
        clips.append(
            {
                "clip_id": wall["clip_id"],
                "from": wall["step"],
                "what": wall["remainder"],
            }
        )
        # Unabsorbed clips on the last walked step also sit in the gap.
        if walked and walked[-1]["clip_id"] not in {"—", "", wall["clip_id"]}:
            clips.append(
                {
                    "clip_id": walked[-1]["clip_id"],
                    "from": walked[-1]["step"],
                    "what": walked[-1].get("remainder") or walked[-1]["body"],
                }
            )
    missing = None
    if wall is not None:
        missing = MissingPiece(
            gap_id=str(spec.get("gap_id") or f"GAP-{wall['step']}"),
            between=tuple(spec.get("between") or (last_walked, first_need)),  # type: ignore[arg-type]
            wall_step=wall["step"],
            clips=tuple(clips),
            would_fill=str(
                spec.get("would_fill")
                or f"A lemma that fills {wall['clip_id']} and lets the walk continue."
            ),
            not_filled_by=tuple(spec.get("not_filled_by") or ()),
        ).to_dict()

    return GapReport(
        book=book,
        chain=chain,
        stopped=hit,
        walked=walked,
        refused_before_wall=refused,
        wall=wall,
        missing=missing,
        candidates_after=candidates,
        refused_bypasses=[dict(b) for b in (bypasses or ())],
    )


def gap_tube(steps: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Live wall on the swirl tube write."""
    from .ns_tube import TUBE_STEPS

    raw = steps if steps is not None else [s.to_dict() for s in TUBE_STEPS]
    return locate_gap(
        raw,
        book="B",
        chain="tube",
        relations=TUBE_RELATIONS,
        extras=TUBE_EXTRAS,
        bypasses=TUBE_BYPASSES,
        missing_spec=TUBE_MISSING,
    ).to_dict()


def gap_chain(steps: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Lemma-list wall: first open is B4b (I_tube). B5 after it is not continuation."""
    from .ns_chain import STEPS

    raw = steps if steps is not None else [s.to_dict() for s in STEPS]
    return locate_gap(
        raw,
        book="B",
        chain="lemmas",
        relations=CHAIN_RELATIONS,
        extras=CHAIN_EXTRAS,
        bypasses=CHAIN_BYPASSES,
        missing_spec=CHAIN_MISSING,
    ).to_dict()


def gap_report(which: str = "B") -> dict[str, Any]:
    """Default live gap is the tube write. CHAIN / LEMMAS selects the scored list."""
    key = which.strip().upper().replace(" ", "")
    if key in {"CHAIN", "LEMMAS", "NS-CHAIN", "B-CHAIN"}:
        payload = gap_chain()
    elif key in {"B", "NS", "TRACKB", "TUBE", "NAVIERSTOKES", "NAVIER-STOKES"}:
        payload = gap_tube()
    else:
        payload = {
            "book": key,
            "chain": "none",
            "stopped": False,
            "error": "Only Track B / NS gap is wired. RH is a different book.",
        }
    payload["not_a_regularity_proof"] = True
    return payload


def format_gap(report: dict[str, Any] | None = None) -> str:
    data = report or gap_report()
    if data.get("error"):
        return data["error"]
    lines = [
        "STOP at the wall — missing piece — candidates after",
        "Not a regularity proof. " + data["rule"],
        f"Book {data['book']}  chain {data['chain']}",
        "",
        "Walked",
    ]
    if data["walked"]:
        lines.append("  " + " · ".join(f"{s['step']} [{s['status']}]" for s in data["walked"]))
    else:
        lines.append("  (nothing walked)")
    if data["refused_before_wall"]:
        lines.append("Clipped before the wall (not a stop)")
        for row in data["refused_before_wall"]:
            lines.append(f"  {row['step']} [{row['status']}] {row['clip_id']}: {row['remainder']}")
    lines.append("")
    wall = data.get("wall")
    if not data.get("stopped") or wall is None:
        lines.append("No wall. The chain has no open step.")
        return "\n".join(lines)
    lines.append(f"WALL  {wall['step']}  [{wall['status']}]  STOP")
    lines.append(f"  {wall['body']}")
    if wall.get("geometry"):
        lines.append(f"  {wall['geometry']}")
    lines.append(f"  clip {wall['clip_id']}: {wall['remainder']}")
    lines.append("")
    miss = data["missing"]
    left, right = miss["between"]
    lines.append(f"MISSING PIECE  {miss['gap_id']}  (between {left} and {right})")
    for clip in miss["clips"]:
        lines.append(f"  {clip['clip_id']}  from {clip['from']}")
        lines.append(f"      {clip['what']}")
    lines.append("  would fill it:")
    lines.append("      " + miss["would_fill"])
    if miss["not_filled_by"]:
        lines.append("  not filled by: " + "; ".join(miss["not_filled_by"]))
    lines.append("")
    lines.append("CANDIDATES AFTER (not walked)")
    for cand in data["candidates_after"]:
        where = "in chain" if cand.get("in_chain") else "off chain"
        lines.append(
            f"  {cand['step']}  [{cand['status']}]  {cand['relation']}  ({where})"
        )
        lines.append(f"      {cand['why']}")
        if cand.get("clip_id") and cand["clip_id"] != "—":
            lines.append(f"      clip {cand['clip_id']}")
    lines.append("")
    lines.append("REFUSED BYPASSES (not candidates)")
    for bypass in data["refused_bypasses"]:
        lines.append(f"  {bypass['step']}  {bypass['clip_id']}")
        lines.append(f"      {bypass['why']}")
    return "\n".join(lines)
