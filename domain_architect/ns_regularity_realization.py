"""Hypothesized unaugmented NS regularity realization (not a theorem).

Domain Architect is a local FRA classifier, not a proof engine.
This module *assumes* unconditional global smoothness / regularity of
classical 3D incompressible Navier–Stokes — unaugmented, no Q1, no
hyperdissipation, no Φ-system — and classifies the other desk fingers
under that hypothesis.

The realization is NEVER endorsed. Clay NS is not claimed. RH is not claimed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CLASS_OBSTRUCTION = "obstruction"
CLASS_OPEN = "open"
CLASS_DOES_NOT_FOLLOW = "does_not_follow"
CLASS_INDEPENDENT = "independent"
ALLOWED_CLASSES = (
    CLASS_OBSTRUCTION,
    CLASS_OPEN,
    CLASS_DOES_NOT_FOLLOW,
    CLASS_INDEPENDENT,
)

DOI_ROUTE_C = "10.5281/zenodo.22050963"
DOI_PHI = "10.5281/zenodo.22050974"
DOI_Q6 = "10.5281/zenodo.22050962"
DOI_RING = "10.5281/zenodo.22050976"
DOI_STATUS = "10.5281/zenodo.22050978"

REALIZATION_NAME = "Hypothesized unconditional closed NS (unaugmented)"
REALIZATION_OPERATOR = "∂_t u + (u·∇)u = −∇p + νΔu,  ∇·u = 0"
REALIZATION_PROMPT = (
    "Hypothesized realization: unconditional global smoothness / regularity "
    "of classical 3D incompressible Navier–Stokes (unaugmented; no Q1, no "
    "hyperdissipation, no Φ-system). Run this hypothesized realization against "
    "the other desk fingers. Domain Architect does not endorse this as a theorem."
)

REPO = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO / "docs" / "domain-architect"
DEFAULT_JSON_NAME = "ns_regularity_realization.json"
DEFAULT_NOTE_NAME = "NS-REGULARITY-REALIZATION.md"
ARTIFACTS_DIR = Path("/opt/cursor/artifacts")

NEXT_ATTEMPT = (
    "Φ-cancel is an algebraic identity on an augmented swirl system; it does not imply unaugmented Clay NS.",
    "Q1 ≠ classical.",
    "Track B is missing a Mertens bridge; do not glue swirl / SND / GNC into Track B.",
    "Route C Gaps A/B still open; the live operator is 1/(gcd√ij), not the June 1/gcd poster.",
    "SND remains a hypothesis; the Ring Lemma is conditional on it.",
    "Assuming smoothness of NS does not force zeros on the critical line, Goldbach, or a spectral floor.",
    "Keep fingers separate. Next attempt should pick ONE missing lemma (Mertens bridge OR Gap A/B OR classical Beale–Kato–Majda / unaugmented enstrophy), not glue them.",
)


def _compact(text: str) -> str:
    return (
        (text or "")
        .lower()
        .replace(" ", "")
        .replace("\\", "")
        .replace("-", "")
        .replace("_", "")
        .replace("{", "")
        .replace("}", "")
        .replace("–", "")
        .replace("—", "")
        .replace("\n", "")
        .replace("³", "3")
    )


def looks_like_ns_regularity_realization(text: str) -> bool:
    """True for the hypothesized closed-NS experiment. Not the OPEN unaugmented face."""
    raw = text or ""
    if not raw.strip():
        return False
    lowered = raw.lower()
    compact = _compact(raw)
    if REALIZATION_PROMPT.lower() in lowered:
        return True
    tokens = (
        "hypothesizedrealization",
        "nsregularityrealization",
        "unconditionalclosedns",
        "unconditionalglobalsmooth",
        "unconditionalglobalregular",
        "hypothesizedunconditional",
        "realizeunconditional",
        "runthishypothesizedrealization",
    )
    if any(token in compact for token in tokens):
        return True
    if "hypothes" in compact and "realization" in compact and (
        "navier" in compact or "nstokes" in compact or "regularity" in compact
    ):
        return True
    return False


def _finger(
    *,
    finger_id: str,
    name: str,
    classification: str,
    reason: str,
    doi: str | None = None,
    if_hypothesis_were_a_theorem: str | None = None,
) -> dict[str, Any]:
    if classification not in ALLOWED_CLASSES:
        raise ValueError(f"unknown classification {classification!r}")
    row: dict[str, Any] = {
        "id": finger_id,
        "name": name,
        "classification": classification,
        "reason": reason,
        "closed_by_this_experiment": False,
    }
    if doi:
        row["doi"] = doi
    if if_hypothesis_were_a_theorem:
        row["if_hypothesis_were_a_theorem"] = if_hypothesis_were_a_theorem
    return row


def fingers() -> list[dict[str, Any]]:
    """Classify each desk finger under the hypothesized NS realization."""
    return [
        _finger(
            finger_id="swirl_with_cancel",
            name="Swirl WITH 1/r^4 cancel (Φ-renorm, Q1-augmented)",
            classification=CLASS_INDEPENDENT,
            doi=DOI_PHI,
            reason=(
                "r^{-4}∂z(Γ²)=∂z(Φ²) is an algebraic identity on the Q1-augmented "
                "Φ-system (live 10.5281/zenodo.22050974). Classical unaugmented "
                "regularity does not produce Q1 or this identity, and the identity "
                "does not produce classical regularity."
            ),
        ),
        _finger(
            finger_id="swirl_without_cancel",
            name="Swirl WITHOUT cancel (axisymmetric-with-swirl still carrying 1/r^4)",
            classification=CLASS_OPEN,
            reason=(
                "The 1/r^4 centrifugal axis term is still in the unaugmented swirl "
                "equations. Domain Architect does not endorse the hypothesized "
                "realization, so this finger stays open. The Φ-cancel identity "
                "still does not follow."
            ),
            if_hypothesis_were_a_theorem=(
                "Regularity of this subclass would follow from full 3D classical "
                "NS regularity. The algebraic 1/r^4 cancel would still not follow."
            ),
        ),
        _finger(
            finger_id="unaugmented_classical_ns",
            name="Unaugmented classical 3D NS",
            classification=CLASS_OPEN,
            reason=(
                "This is the object the experiment assumes closed. The live "
                "problem remains open. Domain Architect does not endorse the "
                "assumption. Clay Statement A/B are not claimed."
            ),
            if_hypothesis_were_a_theorem="Assumed closed inside this experiment only.",
        ),
        _finger(
            finger_id="snd",
            name="SND (spectral non-dispersal)",
            classification=CLASS_DOES_NOT_FOLLOW,
            reason=(
                "SND is a separate hypothesis. Global smoothness of classical NS "
                "does not force the SND criterion, and DA does not treat SND as "
                "an identity with NS regularity."
            ),
        ),
        _finger(
            finger_id="ring_lemma",
            name="Ring Lemma (conditional; SND still hypothesis)",
            classification=CLASS_DOES_NOT_FOLLOW,
            doi=DOI_RING,
            reason=(
                "Live Ring 10.5281/zenodo.22050976 is conditional on SND. "
                "NS regularity does not discharge SND, so the Ring Lemma stays "
                "conditional."
            ),
        ),
        _finger(
            finger_id="gnc_goldbach",
            name="GNC / Goldbach",
            classification=CLASS_DOES_NOT_FOLLOW,
            reason=(
                "Goldbach / GNC is number-theoretic. Smoothness of a fluid PDE "
                "does not give even Goldbach."
            ),
        ),
        _finger(
            finger_id="bridge",
            name="Bridge (SND ≡ GNC ≡ Bridge packaging)",
            classification=CLASS_DOES_NOT_FOLLOW,
            reason=(
                "The June triple lock SND ≡ GNC ≡ Bridge does not hold. "
                "Assuming NS smoothness does not restore that glue."
            ),
        ),
        _finger(
            finger_id="inverse_gcd_floor",
            name="inverse-GCD floor λ_min > −1/2",
            classification=CLASS_DOES_NOT_FOLLOW,
            doi=DOI_Q6,
            reason=(
                "A spectral floor on an arithmetic kernel is a different book. "
                "NS smoothness does not force λ_min(Q_N) > −1/2. Live Q6 "
                "10.5281/zenodo.22050962 is a restricted Rayleigh bound, not that floor."
            ),
        ),
        _finger(
            finger_id="route_c",
            name="Route C operator 1/(gcd√ij), Gaps A/B",
            classification=CLASS_OPEN,
            doi=DOI_ROUTE_C,
            reason=(
                "Live operator is Q_N[i,j]=1/(gcd(i,j)·√(ij)), not June 1/gcd. "
                "Gaps A and B remain open. NS regularity does not close them. "
                "RH is not claimed."
            ),
        ),
        _finger(
            finger_id="track_b_mobius",
            name="Track B μ(gcd)/gcd (Mertens bridge missing)",
            classification=CLASS_OBSTRUCTION,
            reason=(
                "Locked operator Q_N=μ(gcd)/gcd. First-row Hölder is O(N); the "
                "Littlewood–Mertens bridge is missing. Do not glue swirl, SND, "
                "or GNC into this book. NS regularity does not supply the bridge."
            ),
        ),
        _finger(
            finger_id="sfe_universe",
            name="SFE / universe program",
            classification=CLASS_OPEN,
            reason=(
                "Canonical SFE and the unified picture stay unresolved. "
                "NS regularity is not a theory of everything and does not "
                "name a canonical Simons Field Equation."
            ),
        ),
        _finger(
            finger_id="q1_vs_classical",
            name="Q1 vs classical",
            classification=CLASS_INDEPENDENT,
            reason=(
                "Q1 (and fractional hyperdissipation / the Φ-system) is a "
                "different PDE from unaugmented classical NS. The hypothesized "
                "realization is about the classical equation only."
            ),
        ),
    ]


def experiment() -> dict[str, Any]:
    rows = fingers()
    classes = {row["id"]: row["classification"] for row in rows}
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": REALIZATION_NAME,
        "title": "Hypothesized unaugmented NS regularity — finger classifications",
        "prompt": REALIZATION_PROMPT,
        "operator": REALIZATION_OPERATOR,
        "status": "hypothesized_realization_not_endorsed",
        "proof": False,
        "endorsed": False,
        "theorem": False,
        "rh_claimed": False,
        "clay_ns_claimed": False,
        "claims_rh": False,
        "claims_ns": False,
        "chatvault": False,
        "closed_fingers": 0,
        "allowed_classes": list(ALLOWED_CLASSES),
        "classifications": classes,
        "fingers": rows,
        "next_attempt": list(NEXT_ATTEMPT),
        "live_cites": [DOI_ROUTE_C, DOI_PHI, DOI_Q6, DOI_RING, DOI_STATUS],
        "notes": [
            "This is a hypothesized realization, not a theorem Domain Architect endorses.",
            "Clay Navier–Stokes is not claimed. RH is not claimed.",
            "Domain Architect is a local FRA classifier, not a proof engine.",
            "None of the other desk fingers close from this assumption.",
        ],
    }


def narrative(payload: dict[str, Any] | None = None) -> str:
    data = payload or experiment()
    lines = [
        f"Domain Architect — {data['book']}",
        "HYPOTHESIZED realization. Not endorsed. Not a theorem. Not ChatVault.",
        "Clay NS is not claimed. RH is not claimed.",
        f"Operator (assumed only): {data['operator']}",
        "",
        "Finger classifications:",
    ]
    for row in data["fingers"]:
        lines.append(f"  - {row['id']}: {row['classification']}")
        lines.append(f"      {row['reason']}")
    lines.append("")
    lines.append("Next attempt:")
    for item in data["next_attempt"]:
        lines.append(f"  - {item}")
    return "\n".join(lines)


def insight_markdown(payload: dict[str, Any] | None = None) -> str:
    data = payload or experiment()
    lines = [
        "# NS regularity realization — next attempt",
        "",
        "Domain Architect ran a **hypothesized** realization: unconditional",
        "global smoothness / regularity of classical 3D incompressible",
        "Navier–Stokes (unaugmented; no Q1; no hyperdissipation; no Φ-system).",
        "That assumption is **not** a theorem DA endorses. Clay NS is not",
        "claimed. RH is not claimed.",
        "",
        "The other fingers do not close. Classifications:",
        "",
        "| Finger | Class |",
        "|---|---|",
    ]
    for row in data["fingers"]:
        lines.append(f"| {row['name']} | `{row['classification']}` |")
    lines.append("")
    lines.append("## Insight for the next attempt")
    lines.append("")
    for item in data["next_attempt"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Keep fingers separate. DA is a local FRA classifier, not a proof engine.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(
    *,
    docs_dir: Path | None = None,
    artifacts_dir: Path | None = None,
) -> dict[str, Path]:
    """Write the classification log to docs/ and optional artifacts/."""
    data = experiment()
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    note = insight_markdown(data)
    written: dict[str, Path] = {}

    dest_docs = Path(docs_dir) if docs_dir is not None else DOCS_DIR
    dest_docs.mkdir(parents=True, exist_ok=True)
    json_path = dest_docs / DEFAULT_JSON_NAME
    note_path = dest_docs / DEFAULT_NOTE_NAME
    json_path.write_text(text, encoding="utf-8")
    note_path.write_text(note, encoding="utf-8")
    written["docs_json"] = json_path
    written["docs_note"] = note_path

    dest_art = Path(artifacts_dir) if artifacts_dir is not None else ARTIFACTS_DIR
    try:
        dest_art.mkdir(parents=True, exist_ok=True)
        art_json = dest_art / DEFAULT_JSON_NAME
        art_note = dest_art / "ns_regularity_next_attempt.md"
        art_json.write_text(text, encoding="utf-8")
        art_note.write_text(note, encoding="utf-8")
        written["artifacts_json"] = art_json
        written["artifacts_note"] = art_note
    except OSError:
        pass
    return written


face = experiment
ns_regularity_face = experiment
