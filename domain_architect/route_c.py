"""Route C face for Domain Architect (exploratory; not ChatVault; not RH).

Locked operator from 05_route_c_conditional.pdf:

    Q_N[i,j] = 1 / (gcd(i,j) * sqrt(i*j))

This is not RH Track B (μ(gcd)/gcd). Gaps A and B remain open.
Domain Architect does not claim RH. Do not file this face into ChatVault.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

ROUTE_C_NAME = "Route C (exploratory / conditional)"
ROUTE_C_OPERATOR = "Q_N[i,j] = 1/(gcd(i,j)*sqrt(i*j))"
ROUTE_C_PDF_NAME = "05_route_c_conditional.pdf"
ROUTE_C_PDF_FILENAME = ROUTE_C_PDF_NAME
ROUTE_C_PDF_RELATIVE = f"faces/{ROUTE_C_PDF_NAME}"
ROUTE_C_DOI_LIVE = "10.5281/zenodo.22050963"
ROUTE_C_DOI_ARCHIVE = "10.5281/zenodo.20518388"
ROUTE_C_TITLE = (
    "Route C: A Spectral Approach to Zero-Density Estimates, "
    "Conditional on Two Analytic Gaps"
)
JUNE_POSTER_NAME = "june_2026_rh_poster.jpg"
JUNE_POSTER_RELATIVE = f"faces/superseded/{JUNE_POSTER_NAME}"
JUNE_OPERATOR = "Q_N(i,j) = 1/gcd(i,j)"

STATIC_FACES = Path(__file__).resolve().parent / "static" / "faces"


def _compact_route_text(text: str) -> str:
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


def looks_like_superseded_june_route_c(text: str) -> bool:
    """June 2026 inverse-GCD poster / RH_Riemann_final.tex. Not the August face."""
    raw = text or ""
    compact = _compact_route_text(raw)
    if "mu(" in compact or "μ" in raw or "mobius" in compact:
        return False
    if "05routecconditional" in compact:
        return False
    has_sqrt = "sqrt" in compact or "√" in raw
    if has_sqrt and "gcd" in compact:
        return False
    has_inv = "1/gcd" in compact or "1/(gcd" in compact
    has_old_doi = "20518388" in compact
    has_kappa = "6/pi^2" in compact or "6/π^2" in compact or "6/pi2" in compact
    has_limit = "1/(2pi)" in compact or "1/(2π)" in compact or "1/2π" in compact
    named = (
        "routec" in compact
        or "primelattice" in compact
        or "rhriemannfinal" in compact
        or "june2026" in compact
    )
    if has_old_doi or "rhriemannfinal" in compact:
        return True
    if has_inv and (named or has_limit or has_kappa):
        return True
    return False


def looks_like_route_c_operator(text: str) -> bool:
    if looks_like_superseded_june_route_c(text):
        return False
    raw = text or ""
    compact = _compact_route_text(raw)
    if "mu(" in compact or "μ" in raw or "mobius" in compact:
        return False
    if "05routecconditional" in compact:
        return True
    if "routec" in compact:
        return True
    has_gcd = "gcd" in compact
    has_sqrt = "sqrt" in compact or "√" in raw
    return has_gcd and has_sqrt


def pdf_path() -> Path:
    return STATIC_FACES / ROUTE_C_PDF_NAME


def face() -> dict[str, Any]:
    path = pdf_path()
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": ROUTE_C_NAME,
        "title": ROUTE_C_TITLE,
        "operator": ROUTE_C_OPERATOR,
        "status": "exploratory_conditional",
        "rh_claimed": False,
        "claims_rh": False,
        "chatvault": False,
        "pdf_relative": ROUTE_C_PDF_RELATIVE,
        "gaps_open": [
            "Gap A: v_alt^T Q_N v_alt ~ -log(N)/(2π) without assuming the constant from zero-density formulae",
            "Gap B: λ_2(Q_N)-λ_min(Q_N) ≥ c_0 > 0 uniform in N (currently numeric)",
        ],
        "not_claimed": [
            "RH",
            "unconditional zero-density",
            "λ_min(Q_N) > -1/2",
            "closure of Gaps A and B",
        ],
        "doi_live": ROUTE_C_DOI_LIVE,
        "doi_archive": ROUTE_C_DOI_ARCHIVE,
        "pdf_url": f"/faces/{ROUTE_C_PDF_NAME}",
        "pdf_present": path.is_file(),
        "pdf_bytes": path.stat().st_size if path.is_file() else 0,
        "supersedes": (
            "June 2026 inverse-GCD poster / zenodo.20518388 / RH_Riemann_final.tex"
        ),
        "superseded_poster_url": f"/{JUNE_POSTER_RELATIVE}",
        "notes": [
            "August 2026 corrected preprint. Same face as 05_route_c_conditional.tex.",
            "Normalized inverse-GCD, not Track B Möbius-GCD.",
            "Numerics to N=200 are observations, not theorems.",
            "Ring Lemma is an analogy until Gap B is proved.",
            "Not filed into ChatVault.",
            "June 2026 1/gcd poster is superseded. Do not load it as this face.",
        ],
    }


def superseded_june_face() -> dict[str, Any]:
    poster = STATIC_FACES / "superseded" / JUNE_POSTER_NAME
    live = face()
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": "Route C (June 2026 poster — SUPERSEDED)",
        "operator": JUNE_OPERATOR,
        "status": "superseded",
        "rh_claimed": False,
        "claims_rh": False,
        "chatvault": False,
        "poster_url": f"/{JUNE_POSTER_RELATIVE}",
        "poster_present": poster.is_file(),
        "use_instead": live["pdf_url"],
        "use_instead_operator": ROUTE_C_OPERATOR,
        "doi_archive": ROUTE_C_DOI_ARCHIVE,
        "doi_live": ROUTE_C_DOI_LIVE,
        "withdrawn": [
            "RH ⇔ λ_min(Q_N)/log N → -1/(2π) for Q_N = 1/gcd",
            "Q_N = 1/gcd as the live Route C operator",
            "Ring Lemma / V_N* ≈ V_alt as proved or locked on inverse-GCD",
            "κ* = 6/π² as an RH spectral floor for this operator",
        ],
        "notes": [
            "Same family as RH_Riemann_final.tex and WITHDRAW_OR_SUPERSEDE Route C.",
            "DOI 10.5281/zenodo.20518388 is archive. Live face is 10.5281/zenodo.22050963.",
            "RH is not claimed. Not ChatVault.",
        ],
    }


def narrative() -> str:
    payload = face()
    lines = [
        f"Domain Architect — {payload['book']}",
        f"Title: {payload['title']}",
        f"Locked operator: {payload['operator']}",
        "RH is not claimed. Gaps A and B remain open.",
        "This face is not ChatVault.",
        "",
        f"Live DOI: {payload['doi_live']} (archive {payload['doi_archive']})",
        f"PDF: {payload['pdf_url']} present={payload['pdf_present']} bytes={payload['pdf_bytes']}",
        "",
        "Open gaps:",
    ]
    for gap in payload["gaps_open"]:
        lines.append(f"  - {gap}")
    lines.append("")
    lines.append("Not claimed:")
    for item in payload["not_claimed"]:
        lines.append(f"  - {item}")
    lines.append("")
    for note in payload["notes"]:
        lines.append(note)
    return "\n".join(lines)


route_c_face = face
