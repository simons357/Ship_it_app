"""Break Track B into visual pieces, overlay only those that are done, refine holes.

A piece can be finished on its own chart and still not be transposable onto
the general NS shape (T3a on a cylinder; even-reflect energy). Overlay is
architecture, not regularity. Silent-merge of open layers is forbidden.

Not a proof. CosmoEvolution is not this lab.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final


@dataclass(frozen=True)
class Layer:
    id: str
    chart: str
    glyph: str
    what: str
    done_in_piece: bool
    transposable: bool
    status: str
    clip_id: str
    hole: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Bottom of the stack is the domain. Top is swirl dissipation identity.
LAYERS: Final[tuple[Layer, ...]] = (
    Layer(
        id="L1-TORUS",
        chart="physical",
        glyph="⊞ T^3",
        what="periodic box, div-free, Leray projector",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="—",
        hole="",
    ),
    Layer(
        id="L2-FLUX",
        chart="physical",
        glyph="∮=0",
        what="B1: low self-flux into one dyadic block vanishes",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B1-HIGHFLUX",
        hole="high-high and high-low fluxes still live",
    ),
    Layer(
        id="L3-BERNSTEIN",
        chart="frequency",
        glyph="E→X",
        what="shell kinetic energy fills that shell's enstrophy, X_j=2^{2j} E_j",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B2-OCCUPATION",
        hole="occupation time of CONC vs SPREAD is not in this layer",
    ),
    Layer(
        id="L4-COVER",
        chart="frequency",
        glyph="σ|σ̄",
        what="B2: CONC σ≥1/2 and SPREAD σ≤1/2 cover (0,1]",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B2-OCCUPATION",
        hole="the cover is not dynamics; which regime, how long",
    ),
    Layer(
        id="L5-RING",
        chart="vorticity",
        glyph="E_c",
        what="B3: 3-shell Bernstein / |∇ξ| ≲ 2^{j*} on E_c",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B3b-ALIGN",
        hole="alignment / depletion is not in this layer",
    ),
    Layer(
        id="L6-STRAIN",
        chart="vorticity",
        glyph="λ+λ+λ=0",
        what="traceless strain; two eigenvalues fill the third",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B3b-ALIGN",
        hole="Σ λ_i cos² α_i is not forced to deplete",
    ),
    Layer(
        id="L7-HARDY",
        chart="swirl",
        glyph="═δ═",
        what="B4 / T2: localized Hardy inside the tube, wall 2h(δ)² ID'd",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B4-WALL",
        hole="the wall term is not absorbed",
    ),
    Layer(
        id="L8-ANGULAR",
        chart="swirl",
        glyph="1/r²",
        what="B5: (Δu)_θ = Δu_θ − u_θ/r², extra damping in the same tube",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B5b-VS-VISC",
        hole="identity is not domination of I_tube",
    ),
    Layer(
        id="L9-YOUNG",
        chart="cylinder",
        glyph=")δ(",
        what="T3a: Young from outside when h(R)=0 — done on a cylinder",
        done_in_piece=True,
        transposable=False,
        status="play",
        clip_id="CLIP-T3-OUTER",
        hole="T^3 has no outer vanishing; do not transpose onto the general shape",
    ),
    Layer(
        id="L10-WELD",
        chart="swirl",
        glyph="≠",
        what="T3b: Hardy/Young traces are not I_off (different fields)",
        done_in_piece=False,
        transposable=False,
        status="open",
        clip_id="CLIP-T3-WELD",
        hole="the live missing piece between T3a and T5",
    ),
    Layer(
        id="L11-ITUBE",
        chart="swirl",
        glyph="I_t",
        what="T5: |I_tube| vs viscosity at δ ∼ 2^{-j*}",
        done_in_piece=False,
        transposable=False,
        status="open",
        clip_id="CLIP-B4b-ITUBE",
        hole="first candidate after GAP-T3, not walked",
    ),
    Layer(
        id="L12-ENERGY",
        chart="energy",
        glyph="[E]",
        what="Leray kinetic energy tank (bounded)",
        done_in_piece=True,
        transposable=True,
        status="ready",
        clip_id="CLIP-B6-SPIKE",
        hole="seeing E does not bound X; do not stack B6 as a close",
    ),
    Layer(
        id="L13-PHI",
        chart="swirl",
        glyph="Φ!",
        what="switch unknown to Φ_θ = Γ/r²",
        done_in_piece=False,
        transposable=False,
        status="refuse",
        clip_id="CLIP-PHI-LINFTY",
        hole="never stacked; moves work onto ‖Φ_θ‖_∞",
    ),
)


STACK_GLYPH: Final[str] = """
            1/r²                 L8  ready
         ═ δ wall ═              L7  ready
          λ+λ+λ=0                L6  ready
            E_c                  L5  ready
            σ|σ̄                  L4  ready
            E→X                  L3  ready
            ∮=0                  L2  ready
          [E]  ⊞ T^3             L12+L1 ready
    ────────────────────────────────────
         COMPOSITE  (architecture)
    holes punch through:
         CLIP-T3-WELD   CLIP-B4b-ITUBE
         CLIP-B3b-ALIGN CLIP-B2-OCCUPATION
         CLIP-B6-SPIKE  CLIP-T3-OUTER
    not in the stack:
         )δ(  T3a cylinder (done in piece, not transposable)
         ≠    T3b weld (open)
         I_t  T5 (candidate after)
         Φ!   refused
"""


def overlay_report() -> dict[str, Any]:
    layers = [layer.to_dict() for layer in LAYERS]
    stacked = [layer for layer in layers if layer["done_in_piece"] and layer["transposable"]]
    done_not_stacked = [
        layer for layer in layers if layer["done_in_piece"] and not layer["transposable"]
    ]
    waiting = [layer for layer in layers if not layer["done_in_piece"] and layer["status"] != "refuse"]
    refused = [layer for layer in layers if layer["status"] == "refuse"]
    holes: list[dict[str, str]] = []
    seen: set[str] = set()
    for layer in layers:
        cid = layer["clip_id"]
        if cid in {"—", ""} or cid in seen:
            continue
        if layer["hole"]:
            seen.add(cid)
            holes.append(
                {
                    "clip_id": cid,
                    "from": layer["id"],
                    "what": layer["hole"],
                    "blocks_transpose": not layer["transposable"] or not layer["done_in_piece"],
                }
            )
    return {
        "title": "Overlay — pieces, then one general shape, then refine",
        "not_a_regularity_proof": True,
        "rule": (
            "Visualize each piece. Transpose onto the general shape only when "
            "it is done in its piece AND transposable. A finished cylinder "
            "identity is not a torus lemma. Overlay is architecture. Refine "
            "one hole at a time (gap rule). Do not silent-merge open layers."
        ),
        "layers": layers,
        "stacked": stacked,
        "done_not_stacked": done_not_stacked,
        "waiting": waiting,
        "refused": refused,
        "holes": holes,
        "stack_glyph": STACK_GLYPH,
        "composite": {
            "name": "Track B architecture shape",
            "counts": {
                "stacked": len(stacked),
                "done_not_stacked": len(done_not_stacked),
                "waiting": len(waiting),
                "refused": len(refused),
                "holes": len(holes),
            },
            "is_complete": False,
            "is_regularity": False,
            "what_it_is": (
                "T^3, div-free, energy tank, Bernstein ladder, regime cover, "
                "3-shell Ring, traceless strain, Hardy+wall, angular 1/r² identity."
            ),
            "what_it_is_not": (
                "A bound on X, a weld of traces to I_off, alignment, "
                "occupation time, or Φ-cancel."
            ),
        },
        "refine": {
            "first_hole": "GAP-T3",
            "clip_ids": ["CLIP-T3-WELD", "CLIP-T3-OUTER"],
            "between": ["T3a", "T5"],
            "command": "python -m domain_architect --gap B",
            "notes": (
                "Refinement is not a second overlay. It is filling one hole "
                "in the composite, then stacking that piece if it becomes "
                "transposable. T5 stays a candidate until GAP-T3 is filled."
            ),
        },
        "next": (
            "The composite is the general shape of what is done. Refine "
            "GAP-T3. Do not transpose T3a or even-reflect energy onto T^3. "
            "Do not announce regularity from a pretty stack."
        ),
    }


def format_overlay(report: dict[str, Any] | None = None) -> str:
    data = report or overlay_report()
    lines = [
        data["title"],
        "Not a regularity proof. " + data["rule"],
        "",
        "Pieces (each in its own chart)",
    ]
    for layer in data["layers"]:
        flag = (
            "STACK"
            if layer["done_in_piece"] and layer["transposable"]
            else (
                "DONE, not transposable"
                if layer["done_in_piece"]
                else layer["status"].upper()
            )
        )
        lines.append(f"  {layer['id']:14} [{flag}]  {layer['glyph']}  {layer['chart']}")
        lines.append(f"      {layer['what']}")
        if layer["clip_id"] != "—" and layer["hole"]:
            lines.append(f"      hole {layer['clip_id']}: {layer['hole']}")
    lines.append("")
    lines.append("Transpose the ready pieces")
    lines.append(data["stack_glyph"])
    comp = data["composite"]
    c = comp["counts"]
    lines.append(
        f"Composite: {comp['name']}  "
        f"stacked={c['stacked']}  waiting={c['waiting']}  "
        f"holes={c['holes']}  complete={comp['is_complete']}"
    )
    lines.append("  is: " + comp["what_it_is"])
    lines.append("  is not: " + comp["what_it_is_not"])
    lines.append("")
    lines.append("Done in their piece, not stacked (do not transpose)")
    for layer in data["done_not_stacked"]:
        lines.append(f"  {layer['id']}  {layer['clip_id']}  {layer['hole']}")
    lines.append("")
    lines.append("Waiting (not done — not in the overlay)")
    for layer in data["waiting"]:
        lines.append(f"  {layer['id']}  [{layer['status']}]  {layer['clip_id']}")
    lines.append("")
    lines.append("Refine one hole")
    ref = data["refine"]
    lines.append(f"  first: {ref['first_hole']}  between {ref['between'][0]} and {ref['between'][1]}")
    lines.append(f"  clips: {', '.join(ref['clip_ids'])}")
    lines.append(f"  {ref['notes']}")
    lines.append("  " + ref["command"])
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
