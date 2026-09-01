"""Classical unaugmented 3D Navier–Stokes face (OPEN; not Clay; not ChatVault).

This is the incompressible 3D NS equation *without* Q1 / fractional
hyperdissipation / Φ-system augmentation:

    ∂_t u + (u·∇)u = −∇p + ν Δu,   ∇·u = 0

Kept visible in Domain Architect as OPEN / not proved. The May T³
prize-packaging draft 10.5281/zenodo.20405526 (title restored; prize
language walked back) is archive, not a proof. Live fluids cites are
Phi 10.5281/zenodo.22050974 (Q1-augmented swirl) and Ring
10.5281/zenodo.22050976 (conditional SND). Neither is this PDE, and
neither is a Clay NS proof.

The June T³ one-pager is a SUPERSEDED proof graphic. Do not hide the
classical equation behind a withdrawn stamp.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .swirl import looks_like_any_swirl

STATIC_FACES = Path(__file__).resolve().parent / "static" / "faces"

NS_NAME = "Classical 3D NS (unaugmented, OPEN)"
NS_OPERATOR = "∂_t u + (u·∇)u = −∇p + νΔu,  ∇·u = 0"
NS_VORTICITY = "∂_t ω + (u·∇)ω = (ω·∇)u + νΔω,  ∇·u = 0"
NS_PDF_NAME = "ns_unaugmented_classical.pdf"
NS_TITLE = "Classical 3D incompressible Navier–Stokes (unaugmented)"
NS_DOI_ARCHIVE = "10.5281/zenodo.20405526"
NS_DOI_PHI = "10.5281/zenodo.22050974"
NS_DOI_RING = "10.5281/zenodo.22050976"
NS_DOI_STATUS = "10.5281/zenodo.22050978"
T3_POSTER_NAME = "tweet_ns_t3_onepager.png"
T3_POSTER_RELATIVE = f"faces/superseded/{T3_POSTER_NAME}"
Q1_EXCLUDED = "Q_1[u] = −ε^α |∇u|^β Δu  (and fractional −ε(−Δ)^{(β+2)/2})"


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
        .replace("^", "")
        .replace("\n", "")
        .replace("–", "")
        .replace("—", "")
        .replace("³", "3")
        .replace("ℝ", "r")
        .replace("²", "2")
        .replace("ω", "omega")
        .replace("ν", "nu")
        .replace("∂", "partial")
    )


def looks_like_ns_t3_archive(text: str) -> bool:
    """June T³ one-pager / 20405526 prize packaging. Not a live proof."""
    compact = _compact(text)
    if "2072045366430601408" in compact:
        return True
    if "tweetnst3onepager" in compact or "nst3onepager" in compact:
        return True
    if "20405526" in compact:
        return True
    if "claystatementb" in compact or "claystatement(b)" in compact:
        return True
    if "noblowupont3" in compact or "noblowupon t3" in compact:
        return True
    if "globalregularity" in compact and ("t3" in compact or "onthe3torus" in compact):
        return True
    if "millenniumprizeseries" in compact and "navier" in compact:
        return True
    return False


def looks_like_ns_unaugmented(text: str) -> bool:
    """Classical 3D NS without Q1 / Φ augmentation. Swirl faces win first."""
    if looks_like_any_swirl(text):
        return False
    compact = _compact(text)
    if "honestmistake" in compact or "june2026treated" in compact:
        return False
    # Hypothesized closed-NS experiment is a different book.
    if "hypothesizedrealization" in compact or "nsregularityrealization" in compact:
        return False
    if "unconditionalclosedns" in compact:
        return False
    if "hypothes" in compact and "realization" in compact:
        return False
    if "mu(gcd" in compact or "μ(gcd" in (text or "") or "mobius" in compact:
        return False
    if "routec" in compact or "1/(gcd" in compact:
        return False
    if "unaugmented" in compact or "noq1" in compact or "withoutq1" in compact:
        return True
    if "nsunaugmented" in compact or "ns_unaugmented" in compact.replace("_", ""):
        return True
    if "20405526" in compact:
        return True
    if looks_like_ns_t3_archive(text):
        return True
    if "classical" in compact and ("navier" in compact or "nstokes" in compact):
        return True
    if "withoutaugmentation" in compact or "nohyperdissip" in compact:
        return True
    if "lerayhopf" in compact:
        return True
    # Velocity form
    if "∂tu" in compact or "partialtu" in compact or "partial_tu" in compact:
        if "nabla" in compact or "·∇" in (text or "") or "(u·∇)" in (text or "") or "(u*nabla)" in compact:
            if "nu" in compact or "ν" in (text or "") or "visc" in compact:
                return True
    if "navierstokes" in compact or "navier–stokes" in (text or "").lower().replace("–", "-"):
        if "q1" in compact and "withoutq1" not in compact and "noq1" not in compact and "unaugment" not in compact:
            return False
        return True
    if "incompressiblenavier" in compact:
        return True
    # Inventory NS-B vorticity
    if "∂tω" in compact or "partialtomega" in compact:
        if "(ω·∇)u" in compact.replace(" ", "") or "(omega·nabla)u" in compact:
            return True
    return False


def pdf_path() -> Path:
    return STATIC_FACES / NS_PDF_NAME


def t3_poster_path() -> Path:
    return STATIC_FACES / "superseded" / T3_POSTER_NAME


def face() -> dict[str, Any]:
    path = pdf_path()
    poster = t3_poster_path()
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": NS_NAME,
        "title": NS_TITLE,
        "operator": NS_OPERATOR,
        "vorticity_form": NS_VORTICITY,
        "excluded_augmentation": Q1_EXCLUDED,
        "status": "open_not_proved",
        "rh_claimed": False,
        "clay_ns_claimed": False,
        "claims_rh": False,
        "chatvault": False,
        "pdf_relative": f"faces/{NS_PDF_NAME}",
        "pdf_url": f"/faces/{NS_PDF_NAME}",
        "pdf_present": path.is_file(),
        "pdf_bytes": path.stat().st_size if path.is_file() else 0,
        "doi_archive_packaging": NS_DOI_ARCHIVE,
        "doi_live_phi": NS_DOI_PHI,
        "doi_live_ring": NS_DOI_RING,
        "doi_status_note": NS_DOI_STATUS,
        "archive_tex_url": "/faces/archive/Simons_NS_GlobalRegularity_T3.tex",
        "archive_html_url": "/faces/archive/Simons_NS_GlobalRegularity_T3.html",
        "superseded_poster_url": f"/{T3_POSTER_RELATIVE}",
        "poster_present": poster.is_file(),
        "not_claimed": [
            "Clay Millennium Statement B (T³)",
            "Clay Statement A (R³)",
            "unconditional global regularity of unaugmented 3D NS",
            "RH",
            "that 20405526 is a live proof",
            "that Phi 22050974 or Ring 22050976 close classical NS",
        ],
        "notes": [
            "OPEN. The classical unaugmented equation is kept on the DA desktop so it can be seen.",
            "Not a withdrawn stamp on the PDE. Prize-claim language on 20405526 / the June T³ one-pager is walked back.",
            "Live Phi 22050974 is Q1-augmented swirl, not this PDE. Live Ring 22050976 is conditional SND, not Clay NS.",
            "Not ChatVault. Not RH. Domain Architect is not a proof engine.",
        ],
    }


def t3_archive_face() -> dict[str, Any]:
    poster = t3_poster_path()
    live = face()
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": "NS on T³ one-pager / 20405526 packaging — SUPERSEDED as a proof",
        "operator": NS_OPERATOR,
        "status": "superseded_prize_packaging",
        "rh_claimed": False,
        "clay_ns_claimed": False,
        "claims_rh": False,
        "chatvault": False,
        "poster_url": f"/{T3_POSTER_RELATIVE}",
        "poster_present": poster.is_file(),
        "archive_tex_url": "/faces/archive/Simons_NS_GlobalRegularity_T3.tex",
        "doi_archive": NS_DOI_ARCHIVE,
        "use_instead": live["pdf_url"],
        "use_instead_status": "open_not_proved",
        "withdrawn": [
            "Clay Statement B closed / no blowup on T³ as a theorem",
            "20405526 as a live Clay proof",
            "June T³ one-pager step table marked Proved",
        ],
        "notes": [
            "Title of 20405526 was restored. Prize language is still walked back (status note 22050978).",
            "The classical unaugmented NS equation remains OPEN on the DA desktop. Do not hide it.",
            "Live fluids cites: Phi 22050974 and Ring 22050976. Neither is unconditional classical NS.",
            "Not ChatVault. Not RH.",
        ],
    }


def narrative() -> str:
    payload = face()
    lines = [
        f"Domain Architect — {payload['book']}",
        f"Title: {payload['title']}",
        f"Operator: {payload['operator']}",
        f"Vorticity form: {payload['vorticity_form']}",
        "Status: OPEN / not proved. Clay NS is not claimed. RH is not claimed.",
        "This face is not ChatVault.",
        "",
        f"PDF: {payload['pdf_url']} present={payload['pdf_present']} bytes={payload['pdf_bytes']}",
        f"Archive packaging DOI: {payload['doi_archive_packaging']}",
        f"Live Phi (not this PDE): {payload['doi_live_phi']}",
        f"Live Ring (conditional SND, not Clay): {payload['doi_live_ring']}",
        "",
        "Not claimed:",
    ]
    for item in payload["not_claimed"]:
        lines.append(f"  - {item}")
    lines.append("")
    for note in payload["notes"]:
        lines.append(note)
    return "\n".join(lines)
