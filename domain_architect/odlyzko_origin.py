"""Odlyzko correspondence on the origins of Hilbert–Pólya.

Primary source:
https://www-users.cse.umn.edu/~odlyzko/polya/index.html

Pólya’s 3 January 1982 letter is the only documented origin of *his*
remark. Hilbert’s independent formulation is undocumented. The 1914
remark is not a constructed Hamiltonian.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .protocol import freeze_protocol
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, RH_STATUS


SOURCE_URL: str = "https://www-users.cse.umn.edu/~odlyzko/polya/index.html"

ORIGIN_SCOPE: str = (
    "Odlyzko–Pólya origin dump. Pólya’s 1914 Göttingen remark is a "
    "conditional physical reason, not a Hamiltonian. Hilbert’s side is "
    "empty. GUE is Odlyzko’s later numerical observation; he already "
    "called that chain of reasoning very weak. RH is not claimed."
)

POLYA_1914_REMARK: str = (
    "If the nontrivial zeros of the Xi-function were so connected with "
    "the physical problem that the Riemann hypothesis would be equivalent "
    "to the fact that all the eigenvalues of the physical problem are real."
)


@dataclass
class OriginPiece:
    piece_id: str
    occupant: str
    status: str
    da_action: str
    verdict: str


def origin_pieces() -> list[OriginPiece]:
    return [
        OriginPiece(
            "OD-Q",
            "Landau to Pólya, Göttingen, ending ~beginning of 1914: "
            "you know some physics; do you know a physical reason that RH should be true?",
            "documented-as-question",
            "recorded as the prompt; not a Hamiltonian",
            "A question is not H. The load-bearing gap is still the connection.",
        ),
        OriginPiece(
            "OD-A",
            POLYA_1914_REMARK,
            "documented-remark",
            "accepted as Pólya’s own wording (letter 3 Jan 1982); refused as a fill of H",
            "Conditional: RH ≡ all eigenvalues real, *given* a connection of Ξ zeros "
            "to a physical problem. The connection is not supplied. Never published.",
        ),
        OriginPiece(
            "OD-PUB",
            "Pólya: I never published this remark, but somehow it became known.",
            "unpublished-remark",
            "recorded so folk wisdom is not mistaken for a 1910s paper",
            "KEEP as oral/letter provenance. Not a theorem.",
        ),
        OriginPiece(
            "OD-HILBERT",
            "Folk: Hilbert independently, 1910s. Taussky-Todd 25 Jan 1982: "
            "no conversations with Hilbert on number theory; at that time he "
            "had no interest in NT, only logic. She points at Weil via Kisilewsky.",
            "undocumented",
            "classified empty; do not invent Hilbert’s reasoning",
            "NULL. ‘Hilbert and Pólya independently’ is not a documented Hilbert formula.",
        ),
        OriginPiece(
            "OD-FIRST-PRINT",
            "Odlyzko: no published mention of the conjecture before Montgomery 1973 "
            "pair correlation.",
            "historiography",
            "recorded as first-print claim of this source; not a Hamiltonian",
            "The modern slogan is later than 1914. Pair correlation is HP-G1, not HP-S5.",
        ),
        OriginPiece(
            "OD-GUE",
            "Odlyzko 18 Jan 1982: if an operator exists, eigenvalues might behave "
            "like a random hermitian matrix; ‘this chain of reasoning is, of course, "
            "very weak; but surprisingly enough, it seems to work’ (graph enclosed).",
            "numerics-plus-caveat",
            "GUE laboratory already in DA; Odlyzko’s own ‘very weak’ is KEEP honesty",
            "Statistics are not identity. Pólya 26 Apr 1982: ‘I do not understand "
            "yet the graphs.’ He did not endorse GUE as H.",
        ),
        OriginPiece(
            "OD-VS-MODERN",
            "Modern slogan (Odlyzko’s first letter / HP-H001): zeros correspond to "
            "eigenvalues of a self-adjoint hermitian / positive operator.",
            "stronger-slogan",
            "kept distinct from the 1914 remark",
            "‘All eigenvalues real given a connection’ is weaker than "
            "spec(H)={γ_n} for an independently specified H. Do not upgrade the letter.",
        ),
    ]


def origin_path_guides() -> list[str]:
    return [
        "You cannot treat the 1914 remark as a constructed Hamiltonian.",
        "You cannot fill the connection from the zeros (circular).",
        "You cannot document Hilbert’s independent formulation from this source; it is empty.",
        "You cannot use Odlyzko’s GUE graph as spec(H)={γ_n}; he already called the chain weak.",
        "You cannot quote Pólya’s 1982 graphs-letter as an endorsement of random matrices.",
        "You can keep the remark as the original physical-reason shape: RH iff eigenvalues real, given a connection.",
        "You can work the missing object: the connection, or an independent H, or an RH-free LP/1926/Λ route.",
    ]


@dataclass
class OdlyzkoOriginReport:
    source_url: str
    pieces: list[OriginPiece]
    path_guides: list[str]
    registry_ids: list[str]
    rh_status: str
    canonical_sfe_status: str
    protocol_hash: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["pieces"] = [asdict(p) for p in self.pieces]
        return payload

    def narrative(self) -> str:
        lines = [
            "Domain Architect — Odlyzko–Pólya origin dump",
            "",
            ORIGIN_SCOPE,
            "",
            f"Source: {self.source_url}",
            f"Riemann hypothesis status: {self.rh_status}.",
            f"Canonical SFE status: {self.canonical_sfe_status}.",
            "",
            "What happens when this page is entered:",
            "  DA accepts Pólya’s 3 January 1982 letter as the only documented origin",
            "  of *his* Hilbert–Pólya remark. It does not become a Hamiltonian.",
            "  Hilbert’s independent 1910s formulation is empty in this source.",
            "  The 1914 wording is weaker than spec(H)={γ_n}.",
            "  Odlyzko’s GUE comparison is later, and he already called the chain weak.",
            "",
            "Pieces:",
        ]
        for piece in self.pieces:
            lines.append(f"  [{piece.piece_id}] {piece.status}")
            lines.append(f"    occupant: {piece.occupant}")
            lines.append(f"    DA action: {piece.da_action}")
            lines.append(f"    verdict: {piece.verdict}")
        lines.append("")
        lines.append("Path guidance:")
        for item in self.path_guides:
            lines.append(f"  - {item}")
        lines.append("")
        lines.append(f"Registry ids: {', '.join(self.registry_ids)}")
        lines.append(f"Protocol hash: {self.protocol_hash}")
        for note in self.notes:
            lines.append(note)
        return "\n".join(lines)


def run_odlyzko_origin() -> OdlyzkoOriginReport:
    registry = EquationRegistry.load_default()
    ids = [
        eq_id
        for eq_id in ("HP-H001", "HP-H005", "HP-H026", "HP-H028")
        if eq_id in registry.equations
    ]
    protocol = freeze_protocol(
        {
            "program": "odlyzko-polya-origin",
            "source": SOURCE_URL,
            "pieces": [p.piece_id for p in origin_pieces()],
            "forbid_upgrade_remark_to_hamiltonian": True,
            "hilbert_origin_empty": True,
        }
    )
    return OdlyzkoOriginReport(
        source_url=SOURCE_URL,
        pieces=origin_pieces(),
        path_guides=origin_path_guides(),
        registry_ids=ids,
        rh_status=RH_STATUS,
        canonical_sfe_status=CANONICAL_SFE_STATUS,
        protocol_hash=protocol.protocol_hash,
        notes=[
            "Live command: python -m domain_architect --odlyzko",
            "Do not upgrade the 1914 remark to spec(H)={γ_n}.",
        ],
    )


def render_odlyzko_origin(report: OdlyzkoOriginReport | None = None) -> str:
    if report is None:
        report = run_odlyzko_origin()
    return report.narrative()
