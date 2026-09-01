"""Axisymmetric-with-swirl faces for Domain Architect (not ChatVault; not Clay NS).

WITH cancel — live Φ-renormalization, DOI 10.5281/zenodo.22050974
    r^{-4} ∂z(Γ²) = ∂z(Φ²),   Φ = Γ/r² = u_θ/r
Q1-augmented / Φ system. Classical unaugmented regularity remains open.

WITHOUT cancel — same swirl problem *before* that identity.
    D_t Ω = (1/r^4) ∂z(Γ²) + ν L_cyl Ω
The 1/r^4 centrifugal axis term is still in the equations.
No separate public “without cancel” PDF was found on Zenodo; this DA face
states that operator honestly and points at the live WITH-cancel PDF.

Domain Architect does not claim Clay NS or RH. Do not file into ChatVault.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

STATIC_FACES = Path(__file__).resolve().parent / "static" / "faces"

SWIRL_WITH_NAME = "Swirl WITH Φ-cancel (live Phi)"
SWIRL_WITHOUT_NAME = "Swirl WITHOUT Φ-cancel (axis 1/r^4 term)"
SWIRL_WITH_OPERATOR = "r^{-4} ∂z(Γ²) = ∂z(Φ²),  Φ = Γ/r² = u_θ/r"
SWIRL_WITHOUT_OPERATOR = "D_t Ω = (1/r^4) ∂z(Γ²) + ν L_cyl Ω,  Γ = r u_θ"
SWIRL_WITH_PDF_NAME = "01_phi_renormalization.pdf"
SWIRL_WITHOUT_PDF_NAME = "swirl_without_cancel.pdf"
SWIRL_WITH_DOI = "10.5281/zenodo.22050974"
SWIRL_WITH_DOI_SIBLING = "10.5281/zenodo.22050975"
SWIRL_WITH_DOI_JUNE = "10.5281/zenodo.21071991"
SWIRL_WITH_TITLE = (
    "Phi-Renormalization for Axisymmetric Navier-Stokes with Swirl: "
    "Algebraic Cancellation of the 1/r^4 Axis Term"
)
SWIRL_WITHOUT_TITLE = (
    "Axisymmetric Navier–Stokes with swirl: the 1/r^4 axis term "
    "(without Φ-renormalization)"
)
# Byte-identical to live Zenodo 22050974 file 01_phi_renormalization.pdf
# (fetched 2026-08-27). Do not regenerate or re-stamp that PDF.
LIVE_WITH_PDF_SHA256 = (
    "735ab6586a1edb0fee29e6c797a0a12c82a0d2a4e24e667b8d65c6899a2e3c55"
)

# Named citations from the live 10.5281/zenodo.22050974 PDF (fetched 2026-08-27).
# Wired as citations, not proof stamps. None of these close unaugmented 3D NS.
CITATION_DANCHIN = {
    "id": "danchin-2007",
    "name": "R. Danchin",
    "year": 2007,
    "work": "Axisymmetric incompressible flows with bounded vorticity",
    "venue": "Russian Math. Surveys 62 (2007), 73–94",
    "live_ref": "22050974 §1.2 [6]",
    "role": (
        "The live Phi note says the 1/r^4 term is explicitly identified in "
        "Danchin (2007) as the obstruction to direct energy methods."
    ),
    "fills_gap": False,
    "applies_to": "without_cancel",
    "does_not_claim": (
        "global regularity of axisymmetric-with-swirl NS; algebraic Φ-cancel; "
        "unconditional classical 3D NS"
    ),
}
CITATION_LADYZHENSKAYA_UY = {
    "id": "ladyzhenskaya-ukhovskii-yudovich",
    "name": "O. A. Ladyzhenskaya; M. R. Ukhovskii and V. I. Yudovich",
    "year": 1968,
    "work": "axial symmetry without swirl",
    "live_ref": "22050974 §1.2 [1][2]",
    "role": (
        "Without swirl (u_θ ≡ 0), global regularity is classical. "
        "That lemma does not apply to with-swirl large data."
    ),
    "fills_gap": False,
    "applies_to": "without_cancel",
    "does_not_claim": "axisymmetric-with-swirl regularity",
}
CITATION_HOU_LI = {
    "id": "hou-li-2008",
    "name": "T. Y. Hou and C. Li",
    "year": 2008,
    "work": "Dynamic stability of the 3D axisymmetric NS equations with swirl",
    "venue": "Comm. Pure Appl. Math. 61 (2008), 661–697",
    "live_ref": "22050974 §1.2 [5]",
    "role": (
        "Blow-up / dynamic-stability analysis with boundary for axisymmetric "
        "NS with swirl. Partial. Not large-data global regularity."
    ),
    "fills_gap": False,
    "applies_to": "without_cancel",
    "does_not_claim": "Clay NS; unaugmented large-data swirl regularity",
}
CITATION_CHEN_FANG_ZHANG = {
    "id": "chen-fang-zhang-2017",
    "name": "H. Chen, D. Fang, and T. Zhang",
    "year": 2017,
    "work": "Regularity of 3D axisymmetric Navier–Stokes equations",
    "venue": "Discrete Contin. Dyn. Syst. 37 (2017), 1923–1939",
    "live_ref": "22050974 §1.2 [4]",
    "role": (
        "Regularity criterion if swirl stays in L^∞_t L^3_x. A criterion, "
        "not a proof that swirl remains in that space without Φ-cancel."
    ),
    "fills_gap": False,
    "applies_to": "without_cancel",
    "does_not_claim": "that the 1/r^4 term is removed; Clay NS",
}
CITATION_CHAE_LEE = {
    "id": "chae-lee-2002",
    "name": "D. Chae and J. Lee",
    "year": 2002,
    "work": "On the regularity of the axisymmetric solutions of the NS equations",
    "venue": "Math. Z. 239 (2002), 645–671",
    "live_ref": "22050974 §1.2 [3]",
    "role": "Small-swirl regularity. Does not cover large swirl.",
    "fills_gap": False,
    "applies_to": "without_cancel",
    "does_not_claim": "large-data swirl regularity",
}
CITATION_LPS = {
    "id": "ladyzhenskaya-prodi-serrin",
    "name": "Ladyzhenskaya–Prodi–Serrin (via Bahouri–Chemin–Danchin 2011)",
    "year": 2011,
    "work": "Fourier Analysis and Nonlinear Partial Differential Equations",
    "live_ref": "22050974 Thm 3.2 [9]",
    "role": (
        "Used to bootstrap the Q1-augmented axisymmetric system to C^∞. "
        "Applies to the augmented PDE, not to unaugmented classical NS."
    ),
    "fills_gap": False,
    "applies_to": "with_cancel",
    "does_not_claim": "unconditional classical 3D NS; Clay Statement A/B",
}
CITATION_CONSTANTIN_FEFFERMAN = {
    "id": "constantin-fefferman-1993",
    "name": "P. Constantin and C. Fefferman",
    "year": 1993,
    "work": "Direction of vorticity and the problem of global regularity",
    "venue": "Indiana Univ. Math. J. 42 (1993), 775–789",
    "live_ref": "22050974 Def 4.1 [8]",
    "role": (
        "Geometric vorticity-direction criterion, cited for the direction "
        "component of the multi-component stability energy. A criterion, "
        "not a Clay stamp."
    ),
    "fills_gap": False,
    "applies_to": "with_cancel",
    "does_not_claim": "unconditional classical 3D NS",
}

GAP_WITHOUT_TO_WITH = {
    "id": "GAP-SWIRL-AXIS",
    "title": "WITHOUT cancel does not match WITH cancel",
    "filled": False,
    "statement": (
        "WITHOUT still carries (1/r^4)∂z(Γ²) in D_t Ω. WITH applies the "
        "algebraic identity r^{-4}∂z(Γ²)=∂z(Φ²) via Φ=Γ/r² = u_θ/r. "
        "Danchin (2007) names the 1/r^4 energy-method obstruction; naming "
        "it does not cancel it. Cancellation requires the Φ substitution, "
        "which is a different operator (Q1-augmented / Φ system)."
    ),
    "cited_lemma": CITATION_DANCHIN,
    "why_unfilled": (
        "Danchin's identification is a diagnosis of the WITHOUT operator. "
        "It is not the Φ identity and does not remove the 1/r^4 prefactor."
    ),
    "next_attempt": {
        "lemma": (
            "Chen–Fang–Zhang (2017): axisymmetric regularity if swirl is in "
            "L^∞_t L^3_x (live 22050974 [4])."
        ),
        "why_not_rh_goldbach": (
            "This is a fluids criterion on the swirl component. It is not "
            "RH, Goldbach, SND, or inverse-GCD glue."
        ),
        "still_open": (
            "The criterion is not a bound. Without a proof that swirl stays "
            "in that space on the WITHOUT-cancel operator, the 1/r^4 hole remains."
        ),
    },
}
GAP_WITH_TO_CLASSICAL = {
    "id": "GAP-Q1-CLASSICAL",
    "title": "Φ-cancel on Q1 does not close unaugmented classical NS",
    "filled": False,
    "statement": (
        "Even when the Φ identity holds, live 22050974 is Q1-augmented. "
        "The paper's own dashboard leaves classical regularity without "
        "augmentation OPEN. Q1 ≠ classical. Ladyzhenskaya–Prodi–Serrin "
        "bootstraps the augmented system (Thm 3.2). Constantin–Fefferman "
        "is a geometric criterion, not a Clay proof."
    ),
    "cited_lemma": CITATION_LPS,
    "why_unfilled": (
        "LPS / Q1 global smoothness is for a different PDE. Passing ε→0 "
        "is not claimed. The Φ identity is algebra, not unaugmented 3D NS."
    ),
    "next_attempt": {
        "lemma": (
            "ε-independence of C(ε)=2 sup_t ‖u^r_ε/r‖_∞ (June 21071991 OP2; "
            "Prodi–Serrin type, related to Serrin 1962). That is the remaining "
            "axis advection obstruction after the 1/r^4 term is relocated into Φ."
        ),
        "why_not_rh_goldbach": (
            "This is a uniform bound on the radial axis coefficient of the "
            "Φ-energy. It is not RH, Goldbach, or SND ≡ GNC ≡ Bridge."
        ),
        "still_open": (
            "The live August note still lists classical swirl regularity as "
            "Open Problem. Domain Architect does not stamp it proved."
        ),
    },
}


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
        .replace("²", "2")
        .replace("⁴", "4")
        .replace("θ", "theta")
        .replace("ω", "omega")
        .replace("γ", "gamma")
        .replace("φ", "phi")
        .replace("Φ", "phi")
        .replace("Γ", "gamma")
        .replace("Ω", "omega")
    )


def _desk_elsewhere(compact: str) -> bool:
    """Honest-mistake / hypothesized realization are other DA books."""
    return (
        "honestmistake" in compact
        or "june2026treated" in compact
        or "hypothesizedrealization" in compact
        or "nsregularityrealization" in compact
    )


def looks_like_swirl_compare(text: str) -> bool:
    compact = _compact(text)
    if _desk_elsewhere(compact):
        return False
    if "withvswithout" in compact or "withandwithout" in compact:
        return True
    if "compareswirl" in compact or "swirlcomparison" in compact:
        return True
    if "swirl" in compact and "withcancel" in compact and "withoutcancel" in compact:
        return True
    if "swirl" in compact and "withcancellation" in compact and "withoutcancellation" in compact:
        return True
    return False


def _explicit_without(compact: str) -> bool:
    return any(
        token in compact
        for token in (
            "withoutcancel",
            "withoutcancellation",
            "beforecancel",
            "withoutphi",
            "beforephirenorm",
            "beforephirenormalization",
            "precancel",
            "nocancel",
            "uncanceled",
            "uncancelled",
            "swirlwithout",
            "axis1/r4",
            "axistermstill",
            "withaxisterm",
        )
    )


def _strong_with_cancel(compact: str) -> bool:
    # "withoutcancel" contains the substring "withcancel" — check without first.
    if _explicit_without(compact):
        return False
    if any(
        token in compact
        for token in (
            "22050974",
            "22050975",
            "01phirenormalization",
            "phirenormalization",
            "phirenorm",
            "algebraiccancel",
            "algebraiccancellation",
        )
    ):
        return True
    if "withoutcancel" in compact or "withoutcancellation" in compact:
        return False
    if "withcancel" in compact or "withcancellation" in compact:
        return True
    has_identity = (
        "∂z(φ2)" in compact
        or "∂z(phi2)" in compact
        or "partialz(phi2)" in compact
        or "partialz(φ2)" in compact
        or "=∂z(φ" in compact
        or "r4∂z(γ2)=∂z(φ2)" in compact
        or "r4∂z(gamma2)=∂z(phi2)" in compact
        or "1/r4∂z(γ2)=∂z(φ2)" in compact
        or "1/r4∂z(gamma2)=∂z(phi2)" in compact
    )
    return has_identity


def looks_like_swirl_without_cancel(text: str) -> bool:
    """Pre-cancel swirl / axis 1/r^4 term. Distinct from the live Phi identity."""
    if looks_like_swirl_compare(text):
        return False
    compact = _compact(text)
    if _desk_elsewhere(compact):
        return False
    if _explicit_without(compact):
        return True
    if _strong_with_cancel(compact):
        return False
    if "swirlwithoutcancel" in compact or SWIRL_WITHOUT_PDF_NAME.replace("_", "").replace(".pdf", "") in compact:
        return True
    has_axis = "1/r4" in compact or "r4∂z" in compact or "r−4" in compact
    has_identity = (
        "∂z(φ2)" in compact
        or "∂z(phi2)" in compact
        or "partialz(phi2)" in compact
        or "=∂z(φ" in compact
    )
    swirlish = (
        "swirl" in compact
        or "axisym" in compact
        or "centrifugal" in compact
        or ("omega" in compact and "gamma" in compact)
        or "axissingularity" in compact
        or "axisobstruction" in compact
    )
    if has_axis and swirlish and not has_identity:
        return True
    if swirlish and not _strong_with_cancel(compact) and (
        "axisym" in compact or "swirl" in compact
    ):
        # Axisymmetric-with-swirl as a class, without naming the cancel.
        if "q1" in compact and "unaugment" not in compact:
            return False
        return "navier" in compact or "ns" in compact or "omega" in compact or "1/r4" in compact
    return False


def looks_like_swirl_with_cancel(text: str) -> bool:
    if looks_like_swirl_compare(text):
        return False
    if looks_like_swirl_without_cancel(text):
        return False
    compact = _compact(text)
    if _desk_elsewhere(compact):
        return False
    return _strong_with_cancel(compact)


def looks_like_any_swirl(text: str) -> bool:
    return (
        looks_like_swirl_compare(text)
        or looks_like_swirl_without_cancel(text)
        or looks_like_swirl_with_cancel(text)
    )


def named_citations(*, path: str | None = None) -> list[dict[str, Any]]:
    all_cites = [
        CITATION_DANCHIN,
        CITATION_LADYZHENSKAYA_UY,
        CITATION_HOU_LI,
        CITATION_CHEN_FANG_ZHANG,
        CITATION_CHAE_LEE,
        CITATION_LPS,
        CITATION_CONSTANTIN_FEFFERMAN,
    ]
    if path is None:
        return list(all_cites)
    return [item for item in all_cites if item["applies_to"] == path]


def gaps() -> list[dict[str, Any]]:
    return [GAP_WITHOUT_TO_WITH, GAP_WITH_TO_CLASSICAL]


def citation_lines(cite: dict[str, Any]) -> str:
    return (
        f"Cite {cite['name']} ({cite['year']}, {cite['live_ref']}): "
        f"{cite['role']} Does not fill the gap. Does not claim "
        f"{cite['does_not_claim']}."
    )


def gap_lines(gap: dict[str, Any]) -> list[str]:
    nxt = gap["next_attempt"]
    return [
        f"Gap {gap['id']} ({gap['title']}): UNFILLED. {gap['statement']}",
        f"Why unfilled: {gap['why_unfilled']}",
        (
            f"Next-attempt lemma (not RH/Goldbach glue): {nxt['lemma']} "
            f"{nxt['still_open']}"
        ),
    ]


def audit_notes(kind: str) -> tuple[list[str], list[str]]:
    """extra_structures and notes for WITH / WITHOUT / compare."""
    if kind == "compare":
        extra = [
            "swirl WITH vs WITHOUT Φ-cancel comparison",
            "not a Clay NS proof",
            "named citations (Danchin; Ladyzhenskaya–Ukhovskii–Yudovich; LPS)",
        ]
        notes = [
            f"WITH cancel: {SWIRL_WITH_OPERATOR} at /faces/01_phi_renormalization.pdf "
            "(DOI 10.5281/zenodo.22050974). Q1-augmented algebra. Not classical NS.",
            f"WITHOUT cancel: {SWIRL_WITHOUT_OPERATOR} at /faces/swirl_without_cancel.pdf. "
            "The 1/r^4 axis term is still present. No separate pre-cancel Zenodo PDF was found.",
            "Comparison: WITH relocates the axis term into Φ; WITHOUT leaves (1/r^4)∂z(Γ²). "
            "WITH does not solve WITHOUT. Clay NS is not claimed. Not ChatVault.",
        ]
        notes.append(citation_lines(CITATION_DANCHIN))
        notes.extend(gap_lines(GAP_WITHOUT_TO_WITH))
        notes.append(citation_lines(CITATION_LPS))
        notes.extend(gap_lines(GAP_WITH_TO_CLASSICAL))
        notes.append(
            "Domain Architect is a local FRA classifier, not a proof engine. "
            "Unconditional NS smoothness is still a hypothesized realization, not a theorem."
        )
        return extra, notes
    if kind == "without":
        extra = [
            "swirl WITHOUT Φ-cancel (axis 1/r^4 term)",
            "open axis obstruction",
            "citation: Danchin 2007",
        ]
        notes = [
            f"Swirl WITHOUT cancel: {SWIRL_WITHOUT_OPERATOR}. "
            "PDF at /faces/swirl_without_cancel.pdf.",
            "The 1/r^4 centrifugal axis term is still in the equations. "
            "Φ-renormalization is not applied. Later WITH-cancel face: "
            "/faces/01_phi_renormalization.pdf (DOI 10.5281/zenodo.22050974).",
            citation_lines(CITATION_DANCHIN),
            citation_lines(CITATION_LADYZHENSKAYA_UY),
            citation_lines(CITATION_HOU_LI),
        ]
        notes.extend(gap_lines(GAP_WITHOUT_TO_WITH))
        notes.append(
            "Clay NS is not claimed. RH is not claimed. This face is not ChatVault."
        )
        return extra, notes
    extra = [
        "swirl WITH Φ-cancel (live Phi)",
        "Q1-augmented algebraic identity",
        "citation: Ladyzhenskaya–Prodi–Serrin; Constantin–Fefferman",
    ]
    notes = [
        f"Swirl WITH cancel: {SWIRL_WITH_OPERATOR}. "
        "Live PDF at /faces/01_phi_renormalization.pdf (DOI 10.5281/zenodo.22050974).",
        "Q1-augmented / Φ system. The identity is algebra. "
        "Classical regularity without augmentation remains open on that paper's dashboard. "
        "Compare the pre-cancel operator at /faces/swirl_without_cancel.pdf.",
        citation_lines(CITATION_LPS),
        citation_lines(CITATION_CONSTANTIN_FEFFERMAN),
    ]
    notes.extend(gap_lines(GAP_WITH_TO_CLASSICAL))
    notes.append(
        "Clay NS is not claimed. RH is not claimed. This face is not ChatVault. "
        "Do not reuse swirl Φ as the FRA output symbol."
    )
    return extra, notes


def with_cancel_pdf_path() -> Path:
    return STATIC_FACES / SWIRL_WITH_PDF_NAME


def without_cancel_pdf_path() -> Path:
    return STATIC_FACES / SWIRL_WITHOUT_PDF_NAME


def with_cancel_pdf_sha256() -> str | None:
    path = with_cancel_pdf_path()
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def with_cancel_face() -> dict[str, Any]:
    path = with_cancel_pdf_path()
    digest = with_cancel_pdf_sha256()
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": SWIRL_WITH_NAME,
        "title": SWIRL_WITH_TITLE,
        "operator": SWIRL_WITH_OPERATOR,
        "status": "q1_augmented_algebraic_identity",
        "cancellation": "with",
        "rh_claimed": False,
        "clay_ns_claimed": False,
        "claims_rh": False,
        "chatvault": False,
        "pdf_relative": f"faces/{SWIRL_WITH_PDF_NAME}",
        "pdf_url": f"/faces/{SWIRL_WITH_PDF_NAME}",
        "pdf_present": path.is_file(),
        "pdf_bytes": path.stat().st_size if path.is_file() else 0,
        "pdf_sha256": digest,
        "pdf_matches_live_zenodo": digest == LIVE_WITH_PDF_SHA256,
        "doi_live": SWIRL_WITH_DOI,
        "doi_sibling": SWIRL_WITH_DOI_SIBLING,
        "doi_june_archive": SWIRL_WITH_DOI_JUNE,
        "compare_with": "/api/swirl-without-cancel",
        "citations": named_citations(path="with_cancel"),
        "gaps": [GAP_WITH_TO_CLASSICAL],
        "next_attempt": GAP_WITH_TO_CLASSICAL["next_attempt"],
        "not_claimed": [
            "unconditional classical 3D Navier–Stokes",
            "Clay Statement B",
            "Clay Statement A / R³",
            "RH",
            "regularity of the unaugmented swirl system",
        ],
        "notes": [
            "Live August 2026 Φ-renormalization note. Q1-augmented / Φ system.",
            "Identity r^{-4}∂z(Γ²)=∂z(Φ²) is algebra. It is not a Clay proof.",
            "Classical regularity without augmentation remains open on this paper's own dashboard.",
            citation_lines(CITATION_LPS),
            citation_lines(CITATION_CONSTANTIN_FEFFERMAN),
            *gap_lines(GAP_WITH_TO_CLASSICAL),
            "Sibling deposit 10.5281/zenodo.22050975. June conditional Φ is archive 10.5281/zenodo.21071991.",
            "Not ChatVault. Not RH.",
        ],
    }


def without_cancel_face() -> dict[str, Any]:
    path = without_cancel_pdf_path()
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": SWIRL_WITHOUT_NAME,
        "title": SWIRL_WITHOUT_TITLE,
        "operator": SWIRL_WITHOUT_OPERATOR,
        "status": "open_axis_obstruction",
        "cancellation": "without",
        "rh_claimed": False,
        "clay_ns_claimed": False,
        "claims_rh": False,
        "chatvault": False,
        "pdf_relative": f"faces/{SWIRL_WITHOUT_PDF_NAME}",
        "pdf_url": f"/faces/{SWIRL_WITHOUT_PDF_NAME}",
        "pdf_present": path.is_file(),
        "pdf_bytes": path.stat().st_size if path.is_file() else 0,
        "doi_live": None,
        "later_face_doi": SWIRL_WITH_DOI,
        "later_face_url": f"/faces/{SWIRL_WITH_PDF_NAME}",
        "compare_with": "/api/swirl-with-cancel",
        "hunt": (
            "No separate public without-cancel swirl PDF on Zenodo "
            "(checked 22050974/975, 22045467, 21071991, 20405405, 20405597). "
            "This DA face states the pre-cancel operator."
        ),
        "citations": named_citations(path="without_cancel"),
        "gaps": [GAP_WITHOUT_TO_WITH],
        "next_attempt": GAP_WITHOUT_TO_WITH["next_attempt"],
        "not_claimed": [
            "Clay NS",
            "global regularity of axisymmetric-with-swirl NS",
            "that the 1/r^4 term has been removed",
            "RH",
        ],
        "notes": [
            "The 1/r^4 centrifugal axis term is still in the swirl-vorticity equation.",
            "Φ-renormalization is not applied on this face.",
            citation_lines(CITATION_DANCHIN),
            citation_lines(CITATION_LADYZHENSKAYA_UY),
            citation_lines(CITATION_HOU_LI),
            *gap_lines(GAP_WITHOUT_TO_WITH),
            "Later face (WITH cancel): /faces/01_phi_renormalization.pdf "
            f"(DOI {SWIRL_WITH_DOI}).",
            "Not a Clay proof. Not ChatVault.",
        ],
    }


def compare_faces() -> dict[str, Any]:
    with_face = with_cancel_face()
    without_face = without_cancel_face()
    return {
        "ok": True,
        "lane": "inquiry",
        "engine": "domain_architect",
        "not_engine": "chatvault",
        "book": "Swirl WITH vs WITHOUT Φ-cancel",
        "chatvault": False,
        "rh_claimed": False,
        "clay_ns_claimed": False,
        "with_cancel": {
            "book": with_face["book"],
            "operator": with_face["operator"],
            "status": with_face["status"],
            "pdf_url": with_face["pdf_url"],
            "doi_live": with_face["doi_live"],
            "cancellation": "with",
        },
        "without_cancel": {
            "book": without_face["book"],
            "operator": without_face["operator"],
            "status": without_face["status"],
            "pdf_url": without_face["pdf_url"],
            "doi_live": without_face["doi_live"],
            "cancellation": "without",
        },
        "difference": [
            "WITHOUT: source (1/r^4)∂z(Γ²) remains; axis Hardy obstruction is live.",
            "WITH: algebraic identity r^{-4}∂z(Γ²)=∂z(Φ²) relocates the term into Φ; Q1-augmented.",
            "WITH is not a proof of the WITHOUT (unaugmented swirl) problem.",
            "Neither face is unconditional classical 3D NS. Clay is not claimed.",
        ],
        "citations": named_citations(),
        "gaps": gaps(),
        "gaps_filled": False,
        "next_attempt": [
            GAP_WITHOUT_TO_WITH["next_attempt"],
            GAP_WITH_TO_CLASSICAL["next_attempt"],
        ],
        "notes": [
            "Same axisymmetric-with-swirl class. Different operators.",
            "Live WITH PDF is Zenodo 22050974. WITHOUT is a DA face because no matching pre-cancel PDF was found.",
            citation_lines(CITATION_DANCHIN),
            *gap_lines(GAP_WITHOUT_TO_WITH),
            citation_lines(CITATION_LPS),
            *gap_lines(GAP_WITH_TO_CLASSICAL),
            "Not ChatVault. Not RH. Not a proof engine.",
        ],
    }


def with_cancel_narrative() -> str:
    payload = with_cancel_face()
    lines = [
        f"Domain Architect — {payload['book']}",
        f"Title: {payload['title']}",
        f"Operator: {payload['operator']}",
        "Cancellation: WITH. Q1-augmented / Φ system.",
        "Clay NS is not claimed. RH is not claimed. Not ChatVault.",
        "",
        f"Live DOI: {payload['doi_live']} (sibling {payload['doi_sibling']})",
        f"PDF: {payload['pdf_url']} present={payload['pdf_present']} bytes={payload['pdf_bytes']}",
        "",
        "Not claimed:",
    ]
    for item in payload["not_claimed"]:
        lines.append(f"  - {item}")
    lines.append("")
    for note in payload["notes"]:
        lines.append(note)
    return "\n".join(lines)


def without_cancel_narrative() -> str:
    payload = without_cancel_face()
    lines = [
        f"Domain Architect — {payload['book']}",
        f"Title: {payload['title']}",
        f"Operator: {payload['operator']}",
        "Cancellation: WITHOUT. The 1/r^4 axis term is still present.",
        "Clay NS is not claimed. RH is not claimed. Not ChatVault.",
        "",
        f"PDF: {payload['pdf_url']} present={payload['pdf_present']} bytes={payload['pdf_bytes']}",
        f"Later WITH-cancel face: {payload['later_face_url']} ({payload['later_face_doi']})",
        "",
        payload["hunt"],
        "",
        "Not claimed:",
    ]
    for item in payload["not_claimed"]:
        lines.append(f"  - {item}")
    lines.append("")
    for note in payload["notes"]:
        lines.append(note)
    return "\n".join(lines)


def compare_narrative() -> str:
    payload = compare_faces()
    lines = [
        f"Domain Architect — {payload['book']}",
        "Clay NS is not claimed. RH is not claimed. Not ChatVault.",
        "",
        f"WITH:    {payload['with_cancel']['operator']}",
        f"         status={payload['with_cancel']['status']}  {payload['with_cancel']['pdf_url']}",
        f"WITHOUT: {payload['without_cancel']['operator']}",
        f"         status={payload['without_cancel']['status']}  {payload['without_cancel']['pdf_url']}",
        "",
        "Difference:",
    ]
    for item in payload["difference"]:
        lines.append(f"  - {item}")
    lines.append("")
    for note in payload["notes"]:
        lines.append(note)
    return "\n".join(lines)


def render_without_cancel_pdf(path: Path | None = None) -> Path:
    """Rewrite the WITHOUT-cancel DA face so Danchin is cited by name."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    dest = Path(path) if path is not None else without_cancel_pdf_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    regular = "DejaVu"
    bold = "DejaVu-Bold"
    if (font_dir / "DejaVuSans.ttf").is_file():
        pdfmetrics.registerFont(TTFont(regular, str(font_dir / "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont(bold, str(font_dir / "DejaVuSans-Bold.ttf")))
    else:
        regular = "Helvetica"
        bold = "Helvetica-Bold"
    title = ParagraphStyle(
        "SwirlTitle",
        fontName=bold,
        fontSize=13,
        leading=16,
        spaceAfter=6,
    )
    kicker = ParagraphStyle(
        "SwirlKicker",
        fontName=bold,
        fontSize=9,
        leading=12,
        textColor="#444444",
        spaceAfter=8,
    )
    body = ParagraphStyle(
        "SwirlBody",
        fontName=regular,
        fontSize=9,
        leading=12,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "SwirlSmall",
        fontName=regular,
        fontSize=8,
        leading=11,
        spaceAfter=4,
        textColor="#333333",
    )
    doc = SimpleDocTemplate(
        str(dest),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.6 * inch,
        title=SWIRL_WITHOUT_TITLE,
        author="Domain Architect",
    )
    story = [
        Paragraph("Domain Architect face — Inquiry only", kicker),
        Paragraph(
            "Axisymmetric Navier–Stokes with swirl: the 1/r<sup>4</sup> axis term "
            "(without Φ-renormalization)",
            title,
        ),
        Paragraph(
            "Status: OPEN obstruction. Not a Clay proof. Not ChatVault. "
            "This is the operator <b>before</b> the algebraic cancel.",
            body,
        ),
        Paragraph(
            "<b>Hunt note.</b> Zenodo records 22050974 / 22050975 / 22045467 / 21071991 / "
            "20405405 / 20405597 all introduce Φ-renormalization. No separate public "
            "“without cancel” PDF was found. Domain Architect therefore states the "
            "pre-cancel operator here and points at the later live face.",
            body,
        ),
        Paragraph(
            "<b>Operator (still in the equations).</b> Axisymmetric-with-swirl, cylindrical "
            "(r, θ, z). Angular momentum Γ = r u<sub>θ</sub>. Renormalized azimuthal "
            "vorticity Ω = ω<sub>θ</sub>/r. The swirl-vorticity source still carries the "
            "centrifugal axis term:",
            body,
        ),
        Paragraph(
            "D<sub>t</sub> Ω = (1/r<sup>4</sup>) ∂<sub>z</sub>(Γ²) + ν L<sub>cyl</sub> Ω",
            body,
        ),
        Paragraph(
            "with D<sub>t</sub> = ∂<sub>t</sub> + u<sub>r</sub> ∂<sub>r</sub> + u<sub>z</sub> ∂<sub>z</sub>. "
            "As r → 0 the 1/r<sup>4</sup> prefactor is the classical axis obstruction. "
            "Standard H<sup>1</sup> estimates meet a Hardy inequality with weight r<sup>−4</sup>.",
            body,
        ),
        Paragraph(
            "<b>Cite R. Danchin (2007).</b> Live Φ note 10.5281/zenodo.22050974 §1.2 [6] "
            "says the 1/r<sup>4</sup> term is explicitly identified in Danchin, "
            "<i>Axisymmetric incompressible flows with bounded vorticity</i>, "
            "Russian Math. Surveys 62 (2007), 73–94, as the obstruction to direct energy "
            "methods. That is a diagnosis of this WITHOUT-cancel operator. It does "
            "<b>not</b> cancel the term, does not prove swirl regularity, and does not "
            "close unaugmented 3D Navier–Stokes.",
            body,
        ),
        Paragraph(
            "<b>Also named on that live PDF, and also not a fill.</b> Ladyzhenskaya (1968) "
            "and Ukhovskii–Yudovich (1968): without swirl, regularity is classical — does "
            "not apply to with-swirl large data. Chae–Lee (2002): small swirl. "
            "Chen–Fang–Zhang (2017): regularity <i>if</i> swirl is in L<sup>∞</sup><sub>t</sub> "
            "L<sup>3</sup><sub>x</sub> (criterion, not a bound). Hou–Li (2008): dynamic "
            "stability / blow-up analysis with boundary.",
            body,
        ),
        Paragraph(
            "<b>Gap WITHOUT → WITH (UNFILLED).</b> Matching the live WITH-cancel face "
            "requires applying Φ = Γ/r<sup>2</sup> = u<sub>θ</sub>/r so that "
            "r<sup>−4</sup>∂<sub>z</sub>(Γ²) = ∂<sub>z</sub>(Φ²). Danchin names the hole; "
            "the identity is not Danchin’s theorem. Next attempt (not RH/Goldbach): "
            "Chen–Fang–Zhang L<sup>∞</sup><sub>t</sub> L<sup>3</sup><sub>x</sub> swirl "
            "criterion — still open because the bound is not in hand on this operator.",
            body,
        ),
        Paragraph(
            "<b>What this face does not do.</b> It does not apply Φ = Γ/r<sup>2</sup>. "
            "It does not use r<sup>−4</sup> ∂<sub>z</sub>(Γ²) = ∂<sub>z</sub>(Φ²). "
            "It does not claim global regularity, Clay Statement B, or RH.",
            body,
        ),
        Paragraph(
            "<b>Later face (WITH cancel).</b> Live Φ-renormalization (Q1-augmented / Φ "
            "system): DOI 10.5281/zenodo.22050974, file 01_phi_renormalization.pdf. "
            "Sibling 10.5281/zenodo.22050975. June conditional Φ: 10.5281/zenodo.21071991 "
            "(archive). That later face still does not claim unconditional classical 3D "
            "Navier–Stokes: Q1 ≠ classical. LPS bootstrap there is for the augmented PDE.",
            body,
        ),
        Spacer(1, 8),
        Paragraph(
            "Domain Architect is a Functional Role Analysis classifier, not a proof engine. "
            "Canonical SFE unresolved. Unconditional NS smoothness is a hypothesized "
            "realization, not a theorem.",
            small,
        ),
    ]
    doc.build(story)
    return dest
