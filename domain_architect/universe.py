"""Universe / SFE picture inquiry.

This is a Domain Architect book, not ChatVault search. The picture is
unresolved and exploratory. It is not a proof, not a theory of everything,
and not one Hamiltonian with three prizes.

Do not import Route C or Track B operators here. Those books stay in
their own modules.
"""

from __future__ import annotations

import re
from typing import Any

from .schema import CANONICAL_SFE_STATUS

DOI_ROUTE_C = "10.5281/zenodo.22050963"
DOI_PHI = "10.5281/zenodo.22050974"
DOI_RING = "10.5281/zenodo.22050976"
DOI_Q6 = "10.5281/zenodo.22050962"

UNIVERSE_PROMPT = (
    "Universe / SFE / unified picture. What is live on this desk, "
    "and what remains unresolved?"
)

_SFE_TOKEN = re.compile(r"(?<![a-z])sfe(?![a-z])", re.I)
_TOE_TOKEN = re.compile(r"\btoe\b", re.I)


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
    )


def _other_book(text: str) -> bool:
    """Leave Route C, June inverse-GCD, Track B, and swirl PDEs to their owners."""
    raw = text or ""
    compact = _compact(raw)
    lowered = raw.lower()
    if "mu(" in compact or "μ" in raw or "mobius" in compact:
        return True
    if ("gcd" in compact) and ("sqrt" in compact or "√" in raw):
        return True
    if "1/gcd" in compact or "1/(gcd" in compact:
        return True
    if "swirl" in lowered and "universe" not in lowered and "sfe" not in lowered:
        return True
    if "unaugmented" in lowered and "universe" not in lowered and "sfe" not in lowered:
        return True
    if "phirenorm" in compact or "phi-renormalization" in lowered:
        if "universe" not in lowered and "sfe" not in lowered:
            return True
    if "navier" in lowered and "universe" not in lowered and "sfe" not in lowered:
        return True
    return False


def looks_like_universe_inquiry(text: str) -> bool:
    """True for universe / SFE / TOE / unified-picture questions. Not a proof."""
    raw = text or ""
    if not raw.strip():
        return False
    if _other_book(raw):
        return False
    lowered = raw.lower()
    compact = _compact(raw)
    if UNIVERSE_PROMPT.lower() in lowered:
        return True
    needles = (
        "universe",
        "theory of everything",
        "canonical sfe",
        "simons field equation",
        "unified picture",
        "unified theory",
        "one hamiltonian",
        "three prizes",
        "one attractor",
        "what is sfe",
        "what is the sfe",
        "sfe-pub",
        "sfe-qm",
        "sfe-ham",
        "sfe-gcd",
        "sfe-canon",
    )
    if any(needle in lowered for needle in needles):
        return True
    if _TOE_TOKEN.search(raw):
        return True
    if _SFE_TOKEN.search(raw) and any(
        word in lowered
        for word in (
            "canonical",
            "universe",
            "picture",
            "everything",
            "prize",
            "unif",
            "hamiltonian",
        )
    ):
        return True
    if "hsfe" in compact or "ĥsfe" in compact:
        return True
    return False


def live_desk() -> list[dict[str, str]]:
    return [
        {
            "name": "Route C",
            "doi": DOI_ROUTE_C,
            "note": "exploratory; RH not claimed",
        },
        {
            "name": "Φ-renormalization",
            "doi": DOI_PHI,
            "note": "Q1-augmented swirl; not Clay",
        },
        {
            "name": "Ring lemma",
            "doi": DOI_RING,
            "note": "conditional; not a theorem",
        },
        {
            "name": "Q6 inverse-GCD note",
            "doi": DOI_Q6,
            "note": "restricted Rayleigh bound; not RH",
        },
    ]


def face() -> dict[str, Any]:
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": "Universe / SFE picture",
        "title": "Universe program — live desk, open picture",
        "prompt": UNIVERSE_PROMPT,
        "status": "unresolved",
        "exploratory": True,
        "proof": False,
        "rh_claimed": False,
        "ns_claimed": False,
        "claims_rh": False,
        "claims_ns": False,
        "claims_toe": False,
        "chatvault": False,
        "canonical_sfe_status": CANONICAL_SFE_STATUS,
        "live_desk": live_desk(),
        "open": [
            "Canonical SFE",
            "Universe / unified picture",
            "UHF / DHFA as physical laws",
        ],
        "not_claimed": [
            "theory of everything",
            "one Hamiltonian, three prizes",
            "Riemann hypothesis",
            "Clay Navier–Stokes",
            "Goldbach as a theorem",
        ],
        "notes": universe_notes(),
    }


def universe_notes() -> list[str]:
    desk = (
        f"Live desk: Route C {DOI_ROUTE_C} (exploratory); "
        f"Φ-renormalization {DOI_PHI} (Q1-augmented swirl; not Clay); "
        f"Ring {DOI_RING}; Q6 {DOI_Q6}."
    )
    return [
        "Universe / SFE / unified picture: unresolved. Exploratory, not a proof.",
        desk,
        "There is no theory of everything. There is no one Hamiltonian, three prizes.",
        "June 2026 posters are a dated archive on this desk, not the live face.",
        "Swirl and classical Navier–Stokes questions stay on their own Domain Architect faces. They are not this picture and not Clay proofs.",
        "Domain Architect is inquiry. ChatVault is search. This picture is not ChatVault.",
    ]


def narrative() -> str:
    payload = face()
    lines = [
        f"Domain Architect — {payload['book']}",
        f"Status: {payload['status']} (exploratory, not a proof).",
        "Canonical SFE status: unresolved.",
        "RH is not claimed. Clay Navier–Stokes is not claimed.",
        "This face is not ChatVault.",
        "",
        "Live desk:",
    ]
    for item in payload["live_desk"]:
        lines.append(f"  - {item['name']}: {item['doi']} — {item['note']}")
    lines.append("")
    lines.append("Open:")
    for item in payload["open"]:
        lines.append(f"  - {item}")
    lines.append("")
    lines.append("Not claimed:")
    for item in payload["not_claimed"]:
        lines.append(f"  - {item}")
    lines.append("")
    for note in payload["notes"]:
        lines.append(note)
    return "\n".join(lines)


universe_face = face
