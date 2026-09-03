"""Computing-bench desk: layers, unglued books, and legal next moves.

This is an operating-system map, not a unifier and not a Millennium closer.
Inquiry is Domain Architect. Search is ChatVault. CosmoEvolution is visualization.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION


COSMOEVOLUTION_URL: Final[str] = "https://cosmoevolution3d.base44.app"
CHATVAULT_HOME: Final[str] = (
    "chatvault/ inside Ship_it_app (branches cursor/chatvault-* "
    "and cursor/domain-architect-app-f96b). Not a separate GitHub repo."
)
DA_WORKING_APP: Final[str] = (
    "python -m domain_architect on this git; working PWA on "
    "cursor/domain-architect-app-f96b (PR #43). Not CosmoEvolution."
)

# Shape-first navigation (Jonathan R. Simons): the object is a shape.
# Textures are coordinate charts. Same shape is not a proof.
SHAPE_ROLES: Final[tuple[str, ...]] = ("P", "H", "ψ", "λ", "Φ", "E")

SHAPE_FIRST: Final[str] = (
    "Think of the math object as a shape. It has different textures, "
    "but the object is there. Navigate by shape before symbols. "
    "A texture match is not a theorem."
)

LIBRARY_OBJECTS: Final[dict[str, dict[str, str]]] = {
    "NS-B": {
        "book": "B",
        "shape": "classical NS role skeleton on T^3 / R^3",
        "texture": "velocity-pressure or vorticity PDE",
    },
    "J/X": {
        "book": "B",
        "shape": "classical NS role skeleton on T^3 / R^3",
        "texture": "dyadic packet mass J/X, 3-shell occupation",
    },
    "SND-C": {
        "book": "B",
        "shape": "classical NS role skeleton on T^3 / R^3",
        "texture": "conditional SND, X≤M weld still open",
    },
    "Q6": {
        "book": "Q",
        "shape": "inverse-GCD arithmetic operator",
        "texture": "λ_min / λ_max of a matrix",
    },
    "LAMBDA-MIN": {
        "book": "Q",
        "shape": "inverse-GCD arithmetic operator",
        "texture": "λ_min / λ_max of a matrix",
    },
    "VIZ": {
        "book": "VIZ",
        "shape": "display / proposed-model animation",
        "texture": "CosmoEvolution 3D epochs and SM hit table",
    },
    "DA": {
        "book": "DA",
        "shape": "FRA role skeleton Φ=ℱ(P,H,ψ,λ;E)",
        "texture": "inquiry report, evidence levels 0–6",
    },
}

LAYERS: Final[tuple[dict[str, str], ...]] = (
    {
        "id": "DA",
        "name": "Domain Architect",
        "job": "compiler / inquiry desk",
        "allowed": "Classify roles, record conflicts, refuse illegal splices, freeze tests.",
        "forbidden": "Unify physics, certify a lemma, prove RH or NS.",
    },
    {
        "id": "SEARCH",
        "name": "ChatVault",
        "job": "search / inbox",
        "allowed": "Find chats, papers, screenshots, and restore packs.",
        "forbidden": "Certify a lemma, write F, close Clay or RH, replace git as store of record.",
    },
    {
        "id": "VIZ",
        "name": "CosmoEvolution 3D",
        "job": "visualization only",
        "allowed": "Play labeled simulations. Show proposed-model banners.",
        "forbidden": "Write NS, RH, SM Yukawas, nodes.json, or a canonical SFE.",
    },
)

BOOKS: Final[tuple[dict[str, str], ...]] = (
    {
        "id": "A",
        "name": "Track A — Q1-augmented NS",
        "status": "separate PDE; Ladyzhenskaya-class only if ε>0 stays",
        "next": "Keep energy-law checks on this PDE. Never emit A⇒B.",
    },
    {
        "id": "B",
        "name": "Track B — classical Navier–Stokes",
        "status": "open",
        "next": "T3a Young trace is in; T3b weld to I_off and T5 I_tube stay open. Then energy-class low Bony T. Keep 1/r^4. Regularity stays open.",
    },
    {
        "id": "Q",
        "name": "Track Q — inverse-GCD / Bridge*",
        "status": "restricted floors only; full λ_min(Q_N)>-1/2 is false",
        "next": "Documented N-scans. Mark λ_min(H_N)≥-1/4 numeric, not proved. No operator→ζ lemma ⇒ no RH.",
    },
    {
        "id": "U",
        "name": "Track U — SM Lagrangian / measured numbers",
        "status": "bookkeeping; not a unifier",
        "next": "Consume PDG numbers as inputs. Do not replace them with Cosmo '16/16 hits'.",
    },
)

ILLEGAL_SPLICES: Final[tuple[tuple[str, str, str], ...]] = (
    ("VIZ", "B", "CosmoEvolution cannot write classical Navier–Stokes."),
    ("VIZ", "Q", "Manifold fly-throughs are not zeros of ζ(s)."),
    ("VIZ", "U", "The 16/16 topology table is retired as evidence; vacuum cos θ_W test already failed on-site."),
    ("VIZ", "A", "Visualization cannot alter the augmented PDE."),
    ("SEARCH", "B", "ChatVault cannot certify a fluids lemma."),
    ("SEARCH", "Q", "ChatVault cannot certify an arithmetic lemma."),
    ("SEARCH", "RH", "Search is not a decision procedure for the Riemann Hypothesis."),
    ("A", "B", "A different PDE does not imply classical regularity."),
    ("Q", "RH", "Withhold until an operator→ζ lemma exists."),
    ("Q", "B", "Inverse-GCD is not vorticity."),
    ("SFE", "B", "Canonical SFE is unresolved; do not glue into NS."),
    ("SFE", "Q", "Canonical SFE is unresolved; do not glue into RH."),
    ("EXP01", "B", "Closed ringdown null does not retune NS and must not be reopened after TEST."),
)

NEXT_MOVES: Final[tuple[dict[str, str], ...]] = (
    {
        "priority": "1",
        "move": "Navigate by shape first. Same object, different texture (NS PDE vs J/X). Different object if only the symbols rhyme (J/X vs λ_min).",
        "command": "python -m domain_architect --shape-compare J/X LAMBDA-MIN",
        "do_not": "Treat a texture translation as a proof, or use Cosmo pictures as the shape of NS or RH.",
    },
    {
        "priority": "1b",
        "move": "If two equations almost match, clip the excess, ID the clip, and measure it. Do not throw the remainder away.",
        "command": 'python -m domain_architect --clip "laplacian Phi = 4 * pi * G * rho" "laplacian Phi = 4 * pi * G * rho + Lambda * Phi"',
        "do_not": "Silent-merge after a clip. The clip is a component. Cores aligned ≠ original equations the same.",
    },
    {
        "priority": "2",
        "move": "Run this desk, not Cosmo, as Domain Architect.",
        "command": "python -m domain_architect --proceed",
        "do_not": "Treat https://cosmoevolution3d.base44.app as the DA website.",
    },
    {
        "priority": "3",
        "move": "Stop at the first open wall. Name the missing piece between it and the next candidate. Do not walk past.",
        "command": "python -m domain_architect --gap B",
        "do_not": "Treat later identities (B5, T4) as continuation past I_tube.",
    },
    {
        "priority": "3b",
        "move": "One Track B identity: Hardy → wall trace → I_tube. Regularity does not come along.",
        "command": "python -m domain_architect --tube B",
        "do_not": "Announce Clay Statement B.",
    },
    {
        "priority": "3c",
        "move": "If the shape forces the other side, fill it and measure. If you put the symmetry in, it is play, extra E, not a lemma.",
        "command": "python -m domain_architect --shape-play B",
        "do_not": "Promote even-reflect T3a to a torus identity, or treat Cosmo as this lab.",
    },
    {
        "priority": "3d",
        "move": "Put energy in a visual object. Bernstein fills enstrophy from shell energy. Do not guess the tube or X∈L^∞ from the outside of the energy.",
        "command": "python -m domain_architect --energy-play B",
        "do_not": "Treat Leray energy as a bound on X, or even-reflect off-axis energy into I_tube.",
    },
    {
        "priority": "3e",
        "move": "Break into visual pieces. Overlay only done, transposable layers. Refine one hole. Do not silent-merge open layers into the composite.",
        "command": "python -m domain_architect --overlay B",
        "do_not": "Call the stack a complete shape or a regularity proof. T3a is done on a cylinder, not transposable onto T^3.",
    },
    {
        "priority": "3f",
        "move": "See it. Pictures first; math under the fold. Open the see-desk in a browser.",
        "command": "python -m domain_architect --see B",
        "do_not": "Treat CosmoEvolution as this picture desk, or treat the pictures as a proof.",
    },
    {
        "priority": "4",
        "move": "One Track Q numeric floor, documented, with the open ≥-1/4 marked numeric.",
        "command": "recompute inverse-GCD scans; log N and λ_min",
        "do_not": "Say this proves RH.",
    },
    {
        "priority": "5",
        "move": "Keep ChatVault as search only. Put the 160-page HB2 file there if it surfaces.",
        "command": "inquiry = DA; search = ChatVault",
        "do_not": "Wait on screenshots before the next lemma.",
    },
    {
        "priority": "6",
        "move": "Banner CosmoEvolution: VIZ ONLY. Honest vacuum-fail sentence stays; 16/16 table does not enter U.",
        "command": COSMOEVOLUTION_URL,
        "do_not": "Load a private core equation into B or Q.",
    },
)

REFUSED_AS_CLOSE: Final[tuple[str, ...]] = (
    "DNS never blew up",
    "BKM from L^2",
    "A implies B",
    "Q6 implies Route C",
    "Q implies NS",
    "SFE unifies GR and QM",
    "Cosmo 16/16 parameters predicted",
    "the app said so",
    "ChatVault certified it",
    "retune nodes.json after Experiment 01 TEST",
)


@dataclass(frozen=True)
class SpliceDecision:
    source: str
    target: str
    allowed: bool
    opcode: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _norm(token: str) -> str:
    key = token.strip().upper().replace(" ", "")
    aliases = {
        "COSMO": "VIZ",
        "COSMOEVOLUTION": "VIZ",
        "COSMOEVOLUTION3D": "VIZ",
        "CHATVAULT": "SEARCH",
        "VAULT": "SEARCH",
        "DOMAINARCHITECT": "DA",
        "FRA": "DA",
        "NS": "B",
        "NAVIERSTOKES": "B",
        "TRACKB": "B",
        "TRACKA": "A",
        "TRACKQ": "Q",
        "TRACKU": "U",
        "RIEMANN": "RH",
        "RIEMANNHYPOTHESIS": "RH",
        "HB": "SFE",
        "HB2": "SFE",
        "EXPERIMENT01": "EXP01",
        "EXP-H001": "EXP01",
        "VIZ-H001": "VIZ",
        "SYS-H001": "SEARCH",
    }
    return aliases.get(key, key)


def refuse_splice(source: str, target: str) -> SpliceDecision:
    """Return REFUSED for illegal book/layer welds; ALLOWED only for same-book work."""
    src = _norm(source)
    dst = _norm(target)
    if src == dst:
        return SpliceDecision(
            source=src,
            target=dst,
            allowed=True,
            opcode="NOOP",
            reason="Same book or layer. No splice.",
        )
    for left, right, reason in ILLEGAL_SPLICES:
        if src == left and dst == right:
            return SpliceDecision(
                source=src,
                target=dst,
                allowed=False,
                opcode="REFUSED",
                reason=reason,
            )
    if src in {"VIZ", "SEARCH"} and dst in {"A", "B", "Q", "U", "RH", "DA"}:
        return SpliceDecision(
            source=src,
            target=dst,
            allowed=False,
            opcode="REFUSED",
            reason=f"{src} may not write {dst}.",
        )
    if {src, dst} <= {"A", "B", "Q", "U", "RH", "SFE"} and src != dst:
        return SpliceDecision(
            source=src,
            target=dst,
            allowed=False,
            opcode="REFUSED",
            reason="Unglued books. State an explicit lemma first; do not weld.",
        )
    return SpliceDecision(
        source=src,
        target=dst,
        allowed=False,
        opcode="REFUSED",
        reason="Unknown splice. Default is refuse until a typed lemma exists.",
    )


def _norm_object(token: str) -> str:
    key = token.strip().upper().replace(" ", "")
    aliases = {
        "NS": "NS-B",
        "NSB": "NS-B",
        "TRACKB": "NS-B",
        "B": "NS-B",
        "PDE": "NS-B",
        "JX": "J/X",
        "J/X": "J/X",
        "INFJ/X": "J/X",
        "SNDC": "SND-C",
        "SND-C": "SND-C",
        "Q": "Q6",
        "TRACKQ": "Q6",
        "LAMBDAMIN": "LAMBDA-MIN",
        "LAMBDA_MIN": "LAMBDA-MIN",
        "ΛMIN": "LAMBDA-MIN",
        "COSMO": "VIZ",
        "COSMOEVOLUTION": "VIZ",
        "FRA": "DA",
        "DOMAINARCHITECT": "DA",
    }
    return aliases.get(key, token.strip().upper() if token.strip().upper() in LIBRARY_OBJECTS else key)


@dataclass(frozen=True)
class ShapeCompare:
    left: str
    right: str
    left_book: str
    right_book: str
    left_shape: str
    right_shape: str
    left_texture: str
    right_texture: str
    verdict: str
    reason: str
    allowed_weld: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compare_shape(left: str, right: str) -> ShapeCompare:
    """Compare objects by shape first, texture second. Never a proof."""
    a = _norm_object(left)
    b = _norm_object(right)
    if a not in LIBRARY_OBJECTS or b not in LIBRARY_OBJECTS:
        return ShapeCompare(
            left=a,
            right=b,
            left_book="?",
            right_book="?",
            left_shape="unknown",
            right_shape="unknown",
            left_texture="unknown",
            right_texture="unknown",
            verdict="INSUFFICIENT_INFORMATION",
            reason="Object not in the frozen shape catalog. Do not invent a weld.",
            allowed_weld=False,
        )
    la, ra = LIBRARY_OBJECTS[a], LIBRARY_OBJECTS[b]
    if a == b:
        verdict = "SAME_OBJECT"
        reason = "Same catalog entry. No splice."
        allowed = True
    elif la["shape"] == ra["shape"] and la["book"] == ra["book"]:
        verdict = "SAME_SHAPE_DIFFERENT_TEXTURE"
        reason = (
            "Same object, different chart. Navigation is legal. "
            "Texture translation is not a theorem."
        )
        allowed = False
    elif la["book"] != ra["book"] or la["shape"] != ra["shape"]:
        verdict = "INCOMPATIBLE_SHAPE"
        reason = (
            "Different objects. Symbols may rhyme (J/X vs λ_min) and still "
            "be two books. Refuse glue."
        )
        allowed = False
    else:
        verdict = "INCOMPATIBLE_SHAPE"
        reason = "Default refuse."
        allowed = False
    return ShapeCompare(
        left=a,
        right=b,
        left_book=la["book"],
        right_book=ra["book"],
        left_shape=la["shape"],
        right_shape=ra["shape"],
        left_texture=la["texture"],
        right_texture=ra["texture"],
        verdict=verdict,
        reason=reason,
        allowed_weld=allowed,
    )


def proceed_report() -> dict[str, Any]:
    return {
        "product": "Domain Architect",
        "method": "Functional Role Analysis",
        "description": PRODUCT_DESCRIPTION,
        "canonical_sfe_status": CANONICAL_SFE_STATUS,
        "store_of_record": "git Ship_it_app (this repository)",
        "working_da_app": DA_WORKING_APP,
        "chatvault": CHATVAULT_HOME,
        "cosmoevolution": {
            "url": COSMOEVOLUTION_URL,
            "role": "visualization only",
            "banner": "VIZ ONLY. Proposed model. Cannot splice into B, Q, or U.",
            "keep": (
                "Evidence labels; vacuum λ1/λ2 crossings are not DA predictions; "
                "no tested vacuum ratio matches cos θ_W."
            ),
            "knockout": "16/16 Standard Model parameters predicted from topology.",
        },
        "layers": list(LAYERS),
        "books": list(BOOKS),
        "shape_first": SHAPE_FIRST,
        "shape_roles": list(SHAPE_ROLES),
        "library_objects": {k: dict(v) for k, v in LIBRARY_OBJECTS.items()},
        "next_moves": list(NEXT_MOVES),
        "refused_as_close": list(REFUSED_AS_CLOSE),
        "where_we_go": (
            "Shrink the machine. Navigate by shape first, then one lemma or "
            "one scan. CosmoEvolution is a planetarium. Domain Architect is a "
            "compiler. ChatVault is search. Do not let the planetarium compile."
        ),
        "bench": (
            "Turing, von Neumann, Hamming, Wilkinson, Kahan, Knuth, Dijkstra, "
            "Parnas, Lamport, Hoare, McCarthy, Shannon, Backus; program review "
            "Einstein, Weinberg, Weyl, Wigner, Feynman, Tesla; NS constraints "
            "Leray / BKM / CKN; RH constraint LMFDB / analytic NT."
        ),
    }


def format_proceed(report: dict[str, Any] | None = None) -> str:
    data = report or proceed_report()
    lines = [
        "Domain Architect — computing bench proceed",
        f"Canonical SFE status: {data['canonical_sfe_status']}.",
        "",
        data["where_we_go"],
        "",
        "Shape first (not a substitute for proofs)",
        "  " + data["shape_first"],
        "  roles: " + ", ".join(data["shape_roles"]),
        "",
        "Layers (not one website)",
    ]
    for layer in data["layers"]:
        lines.append(
            f"  {layer['id']}: {layer['name']} — {layer['job']}. "
            f"Forbidden: {layer['forbidden']}"
        )
    lines.append("")
    lines.append("Books (unglued)")
    for book in data["books"]:
        lines.append(f"  {book['id']}: {book['name']} [{book['status']}]")
        lines.append(f"      next: {book['next']}")
    lines.append("")
    lines.append("Where we go from here")
    for move in data["next_moves"]:
        lines.append(f"  {move['priority']}. {move['move']}")
        lines.append(f"      {move['command']}")
        lines.append(f"      do not: {move['do_not']}")
    lines.append("")
    lines.append("Store of record: " + data["store_of_record"])
    lines.append("ChatVault: " + data["chatvault"])
    lines.append("CosmoEvolution: " + data["cosmoevolution"]["url"] + " — visualization only")
    return "\n".join(lines)
