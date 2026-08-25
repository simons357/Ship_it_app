"""Leftover-split protocol: take what fails, reconstruct, put it back.

This is a Domain Architect *use* of DECOMPOSE → TRANSLATE → SYNTHESIZE.
It is also a method the NS books can cite. It does not close Navier–Stokes.

Protocol
--------
1. Take only the leftover (the smallness energy does not give).
2. Decompose that leftover as its own system.
3. Translate leftovers side by side with glue refused.
4. Reconstruct from the ground: coercive part (keep) + independent
   concentration diagnostic (hypothesis) ⇒ the rest closes.
5. Put the conditional theorem back into each original book.
   Leave each diagnostic OPEN. Do not identify the leftovers.

The three NS leftovers are swirl strain, unconditional Ring SND, and
Paper2 simplex closeness. Usable Ring SND and Q6 H_N sit beside them
as concentration diagnostics that can coexist without being multiplied.
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
    SND_VS_H_NOTES,
    LeftoverSpec,
)
from .schema import CorrespondenceKind, ValidationGate
from .synthesize import CandidateArchitecture, Provenance
from .translate import snd_vs_h_translation, translate_refuse_glue


REFUSED = (
    "no letter map J→H / urad→J / a→HN",
    "no TRANSFORMABLE stamp",
    "no structure_preserving_equivalence",
    "no PD / inverse-design control loop",
    "no Clay / unaugmented regularity claim",
    "no SND ≡ GNC ≡ Bridge",
    "no identifying Q6 H_N with Paper2 H_N[a] or FRA coupling H",
    "no identifying ∫||u^r/r||_∞ dt with ||a-μ||_ℓ¹ or with J/X",
)


def leftover_repair() -> dict[str, Any]:
    """Run the leftover-split protocol and return a JSON-ready report."""
    pieces = [_describe_piece(spec) for spec in NS_LEFTOVERS]
    snd = decompose(RING_SND_LAB, name="ring_snd")
    hn = decompose(Q6_HN_LAB, name="q6_hn")
    snd_vs_h = snd_vs_h_translation()
    pair_maps = []
    for i, left_spec in enumerate(NS_LEFTOVERS):
        for right_spec in NS_LEFTOVERS[i + 1 :]:
            left = decompose(left_spec["fails_lab"], name=left_spec["id"])
            right = decompose(right_spec["fails_lab"], name=right_spec["id"])
            record = translate_refuse_glue(
                left,
                right,
                notes=[
                    f"{left_spec['id']} vs {right_spec['id']}",
                    "Shared role: independent concentration / smallness.",
                    "Not a shared estimate. Mapping refused.",
                ],
            )
            pair_maps.append(record.to_dict())

    reconstruction = {
        "ground": (
            "Keep the coercive / energy part of each book. Do not rebuild "
            "what already stands."
        ),
        "missing_role": (
            "independent concentration / smallness constraint — one role, "
            "three carriers, no identification"
        ),
        "assembly": list(LEFTOVER_SPLIT_STEPS),
        "coexist": (
            "Ring SND and Q6 H_N can coexist as two concentration "
            "diagnostics: a fluids shell-mass ratio and an arithmetic "
            "mixing matrix. They are not a joint operator. The three NS "
            "leftovers coexist the same way: same missing role, separate "
            "put-backs."
        ),
        "closed": False,
    }
    return {
        "protocol": "leftover-split",
        "pieces": pieces,
        "snd_vs_h": {
            "left": RING_SND_LAB,
            "right": Q6_HN_LAB,
            "snd_pattern": snd.classification.pattern,
            "hn_pattern": hn.classification.pattern,
            "snd_warnings": list(snd.warnings),
            "hn_warnings": list(hn.warnings),
            "translation": snd_vs_h.to_dict(),
        },
        "pairwise_leftovers": pair_maps,
        "reconstruction": reconstruction,
        "re_embed": [
            {
                "id": spec["id"],
                "book": spec["book"],
                "put_back": spec["put_back"],
                "status": spec["status"],
            }
            for spec in NS_LEFTOVERS
        ],
        "refused": list(REFUSED),
        "notes": list(SND_VS_H_NOTES)
        + [
            "This function does not prove Navier–Stokes regularity.",
            "Each leftover stays OPEN after put-back.",
        ],
        "validation_gate": ValidationGate.MATHEMATICAL.value,
        "kind": CorrespondenceKind.ANALOGY.value,
    }


def cycle_leftover_repair() -> CycleReport:
    """Named cycle: leftover-split on the three NS failures plus SND vs H_N."""
    payload = leftover_repair()
    candidate = CandidateArchitecture(
        name="leftover_split_conditional",
        components=[
            "coercive quadratic / energy (already works; keep)",
            "independent concentration diagnostic (missing; OPEN)",
            "conditional implication (if diagnostic then the rest closes)",
        ],
        replaced={},
        hypothesis=(
            "The three NS leftovers share a *role* (independent "
            "concentration / smallness), not an estimate. Reconstruct each "
            "main problem as coercive part + diagnostic hypothesis. Put "
            "that conditional theorem back into its own book. Ring SND and "
            "Q6 H_N coexist as diagnostics; they are not multiplied."
        ),
        provenance=[
            Provenance(
                source="leftover-split protocol",
                original_domain="ns-leftovers",
                functional_role="constraint",
                translation=None,
                assumptions=[
                    "do not identify leftovers",
                    "do not derive the diagnostic from energy",
                ],
                compatibility_checks=["glue refused", "no executable T"],
                modifications=[],
                evidence=[spec["id"] for spec in NS_LEFTOVERS],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Not a PD controller. Inverse design is not used.",
            "Not TRANSFORMABLE. Not Clay.",
            "Each diagnostic remains OPEN.",
        ],
    )
    snd = decompose(RING_SND_LAB, name="ring_snd")
    return CycleReport(
        mode="leftover-repair",
        target=(
            "repair the three NS leftovers as conditional theorems; "
            "let Ring SND and Q6 H_N coexist without glue"
        ),
        constraints=[
            "do not identify leftovers",
            "do not emit a PD loop",
            "books stay split",
            "no Clay claim",
        ],
        decomposition=snd,
        translation=snd_vs_h_translation(),
        candidate=candidate,
        prediction=payload,
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Leftover-split is a method, not a regularity proof.",
            "Usable SND is Ring inf J/X ≥ c_*. Usable theory H is the "
            "Q6 definition of H_N. Fluids Theorem H is not in this repo.",
        ]
        + list(LEFTOVER_SPLIT_STEPS),
        method_credits=["leftover-split protocol"],
    )


def _describe_piece(spec: LeftoverSpec) -> dict[str, Any]:
    fails = decompose(spec["fails_lab"], name=f"{spec['id']}:fails")
    works_lab = spec["works_lab"]
    if works_lab and works_lab != spec["fails_lab"]:
        works = decompose(works_lab, name=f"{spec['id']}:works")
        works_decompose = {
            "pattern": works.classification.pattern,
            "warnings": list(works.warnings),
            "architecture": works.tree.pretty(),
        }
    else:
        works_decompose = {
            "pattern": None,
            "warnings": [
                "Standing part is kept as prose. The lab string is the leftover."
            ],
            "architecture": spec["works"],
        }
    return {
        "id": spec["id"],
        "book": spec["book"],
        "name": spec["name"],
        "works": spec["works"],
        "fails": spec["fails"],
        "missing_role": spec["missing_role"],
        "status": spec["status"],
        "works_lab": spec["works_lab"],
        "fails_lab": spec["fails_lab"],
        "works_decompose": works_decompose,
        "fails_decompose": {
            "pattern": fails.classification.pattern,
            "warnings": list(fails.warnings),
            "architecture": fails.tree.pretty(),
        },
    }
