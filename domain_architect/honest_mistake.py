"""Honest-mistake note for Domain Architect (inquiry, not ChatVault).

One careful paragraph. Not crime tape. Not a claim that files were fake.
Titles stay unrestamped. RH and Clay NS are not claimed.
"""

from __future__ import annotations

from typing import Any

DOI_ROUTE_C = "10.5281/zenodo.22050963"
DOI_PHI = "10.5281/zenodo.22050974"
DOI_Q6 = "10.5281/zenodo.22050962"
DOI_RING = "10.5281/zenodo.22050976"
DOI_STATUS = "10.5281/zenodo.22050978"

HONEST_MISTAKE_PROMPT = "Honest mistake on the June 2026 packaging."

# Locked copy. Keep as one paragraph.
HONEST_MISTAKE_PARAGRAPH = (
    "June 2026 treated a very complex problem as closed: unconditional "
    "classical 3D incompressible Navier–Stokes smoothness/regularity packaged "
    "as prize-ready, often glued to RH / Goldbach via SND ≡ GNC ≡ Bridge / "
    "inverse-GCD floor. That packaging does not hold. Walking back prize "
    "language was necessary. Stamping every Zenodo title with [Claim withdrawn] "
    "was a second mistake; titles were restored 26 Aug 2026. Public cite stack "
    "stays live: Route C 10.5281/zenodo.22050963, Φ-renorm 10.5281/zenodo.22050974, "
    "inverse-GCD note 10.5281/zenodo.22050962, Ring Lemma 10.5281/zenodo.22050976, "
    "status 10.5281/zenodo.22050978."
)

LIVE_CITES = (
    DOI_ROUTE_C,
    DOI_PHI,
    DOI_Q6,
    DOI_RING,
    DOI_STATUS,
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
    )


def looks_like_honest_mistake(text: str) -> bool:
    """True for the June-packaging honest-mistake note. Not a retraction banner."""
    raw = text or ""
    if not raw.strip():
        return False
    lowered = raw.lower()
    compact = _compact(raw)
    if HONEST_MISTAKE_PROMPT.lower() in lowered:
        return True
    if HONEST_MISTAKE_PARAGRAPH[:80].lower() in lowered:
        return True
    if "honestmistake" in compact:
        return True
    if "june2026treated" in compact:
        return True
    if "stampingeveryzenodotitle" in compact:
        return True
    if "secondmistake" in compact and ("zenodo" in compact or "title" in compact):
        return True
    return False


def face() -> dict[str, Any]:
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": "Honest mistake (June 2026 packaging)",
        "title": "An honest mistake, not a closed theory",
        "prompt": HONEST_MISTAKE_PROMPT,
        "paragraph": HONEST_MISTAKE_PARAGRAPH,
        "status": "walked_back_packaging",
        "proof": False,
        "endorsed": False,
        "rh_claimed": False,
        "clay_ns_claimed": False,
        "claims_rh": False,
        "claims_ns": False,
        "chatvault": False,
        "titles_restamped": False,
        "live_cites": list(LIVE_CITES),
        "not_claimed": [
            "Riemann hypothesis",
            "Clay Navier–Stokes",
            "Goldbach as a theorem",
            "that the deposits were unpublished",
        ],
        "notes": [
            HONEST_MISTAKE_PARAGRAPH,
            "Domain Architect is inquiry. ChatVault is search. This note is not ChatVault.",
            "Do not re-stamp Zenodo titles. Prize language stays walked back. Files stay published.",
        ],
    }


def narrative() -> str:
    payload = face()
    lines = [
        f"Domain Architect — {payload['book']}",
        "Careful note. Not a proof. Not ChatVault.",
        "",
        payload["paragraph"],
        "",
        "Live cites:",
    ]
    for doi in payload["live_cites"]:
        lines.append(f"  - {doi}")
    lines.append("")
    lines.append("Not claimed:")
    for item in payload["not_claimed"]:
        lines.append(f"  - {item}")
    return "\n".join(lines)


honest_mistake_face = face
