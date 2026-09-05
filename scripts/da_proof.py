#!/usr/bin/env python3
"""
DA proof: write a proof chain from the ground floor.

The operator is not a math person. They name a problem
(NS / Track B, A / Track A, RH). DA writes the aimed
theorem and the chain. Asking is the product. Emitting
the chain is not QED. Line WRITE is the attempt.

Track A is the Q1 PDE. Theorem A already sits for that
equation. Track B is classical NS. Do not glue.
Track Q is inverse-GCD. It is not RH. Do not glue.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_from import MINE, NEEDED  # noqa: E402
from da_hunt import LEGAL, OBJECT  # noqa: E402
from da_next import WALL  # noqa: E402


def rec(
    hid: str,
    name: str,
    statement: str,
    verdict: str,
    why: str,
    **extra,
) -> dict:
    row = {
        "id": hid,
        "name": name,
        "statement": statement,
        "verdict": verdict,
        "why": why,
    }
    row.update(extra)
    return row


NS_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Energy. Leray: int_0^T X(t) dt < infinity on these packets, "
            "and the energy inequality holds."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "Enstrophy identity. Differentiating X along the NSE gives "
            "dX/dt + nu ||grad omega||_2^2 = -int omega · S omega "
            "(up to lower-order terms already controlled)."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Leftover form. Absorb a slice of dissipation to obtain "
            + WALL["looks_like"]
            + " The only term that can beat viscosity is the stretching leftover."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Split. int omega · S omega = hole 1 (aligned P+ on E_c) "
            "+ hole 2 (unaligned P+ on E_c) + hole 3 (off E_c). "
            "Scored on the n=32 box as B37."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "Named blanks. A1 = alignment in time for all data (hole 1). "
            "A2 = int ||lambda_2^+|| for all data (live cubic; Miller cut B38). "
            "On this box A1 is off and A2 is live and did not blow on the B15 path (B40, B41)."
        ),
    },
    {
        "n": 6,
        "status": "write",
        "text": (
            "WRITE. One all-data integrable residual: int_0^T R(t) dt < infinity, "
            "or all-data A1, or all-data A2, or a field that kills the stretching leftover."
        ),
    },
    {
        "n": 7,
        "status": "follows",
        "text": "Gronwall. From (3) and (6), X(t) stays finite on [0, T].",
    },
    {
        "n": 8,
        "status": "follows",
        "text": (
            "Continuation. Beale-Kato-Majda: if int_0^T ||omega||_infty dt < infinity "
            "then the solution continues. A bound that yields that integral, "
            "or an equivalent criterion, gives no blowup. L2 is not the max."
        ),
    },
    {
        "n": 9,
        "status": "follows",
        "text": (
            "Bootstrap. Standard parabolic regularity: a bound on X and no blowup "
            "of ||omega||_infty upgrades to smoothness on [0, T]. "
            "If T is arbitrary, the solution is globally regular."
        ),
    },
]


A_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "The PDE. On T^3, nu>0, eps>0, alpha>0, beta>=1/2: "
            "partial_t u + (u·grad)u = -grad p + nu Delta u "
            "+ eps^alpha P div(|grad u|^beta grad u), div u = 0. "
            "Ladyzhenskaya / p-Laplacian stress. Not classical NS. No Phi."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "Energy. Test against u: "
            "1/2 d/dt ||u||_2^2 + nu ||grad u||_2^2 "
            "+ eps^alpha ||grad u||_{L^{beta+2}}^{beta+2} = 0."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Galerkin. Finite Stokes modes, same energy, no blowup of ||u_n||_2. "
            "Weak limit is a weak solution (Minty-Browder on the extra stress)."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "beta>=1/2 in 3D. Extra integrability of grad u meets Ladyzhenskaya "
            "p>=5/2. Unique strong solution in L^infty_t H^1 cap L^2_t H^2. "
            "The constant depends on eps and blows up as eps->0."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "Bootstrap. Frozen eps>0, uniformly elliptic Stokes. "
            "Difference quotients to H^k, then C^infty."
        ),
    },
    {
        "n": 6,
        "status": "have",
        "text": (
            "Theorem A. Unique u in C^infty(T^3 x (0,infty)) cap L^infty_t H^1 "
            "for this PDE at eps>0, beta>=1/2. This PDE is closed. "
            "No Phi. Data need not be axisymmetric."
        ),
    },
    {
        "n": 7,
        "status": "write",
        "text": (
            "WRITE. ||u||_H1 <= C with C independent of eps, for all smooth "
            "divergence-free H^1 data, or a named obstruction that C must blow up. "
            "A decaying Q1 integral is not that bound (A9)."
        ),
    },
    {
        "n": 8,
        "status": "follows",
        "text": (
            "Uniform Lemma 4. From (4) and (7), the H^1 bound stays finite as eps->0."
        ),
    },
    {
        "n": 9,
        "status": "follows",
        "text": (
            "Still not B. If (7) sits you have a uniform bound on this family. "
            "Classical NS is a separate Track B write (integrable R). A=>B stays fail."
        ),
    },
]


RH_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Zeta. Riemann zeta is meromorphic, simple pole at s=1, "
            "Euler product for Re s > 1."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "xi. The completed xi-function is entire of order 1 "
            "and satisfies a functional equation xi(s) = xi(1-s)."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Strip. Every non-trivial zero lies in 0 < Re s < 1."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Prime number theorem. No zeros on Re s = 1 "
            "(Hadamard / de la Vallee Poussin)."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "The line. Infinitely many zeros on Re s = 1/2 (Hardy). "
            "A positive proportion sit on the line (Conrey and later). "
            "Literature, not a theorem of this desk."
        ),
    },
    {
        "n": 6,
        "status": "write",
        "text": (
            "WRITE. Every non-trivial zero has Re s = 1/2."
        ),
    },
    {
        "n": 7,
        "status": "follows",
        "text": (
            "Explicit formula. If (6) sits, the von Mangoldt explicit formula "
            "has all oscillatory terms on the critical line."
        ),
    },
    {
        "n": 8,
        "status": "follows",
        "text": (
            "Error term. The prime-counting error is then of the classical "
            "Riemann order (up to logs)."
        ),
    },
]


PROBLEMS = {
    "NS": {
        "id": "NS",
        "aliases": ("ns", "navier", "stokes", "xavier", "navi"),
        "slot": "B",
        "name": "3D Navier-Stokes global regularity",
        "object": {
            "name": "X",
            "slot": "B",
            "english": OBJECT["english"],
            "window": OBJECT["window"],
        },
        "theorem": (
            "Let u be a smooth solution of 3D incompressible Navier-Stokes "
            "(periodic or whole space), viscosity nu > 0, no Q1, keep 1/r^4. "
            "Let X = ||omega||_2^2. Then X stays finite on [0, T] for arbitrary T, "
            "and u remains smooth."
        ),
        "lines": NS_LINES,
        "chain_doc": "docs/NS-PROOF-CHAIN.md",
        "proceed": [row["claim"] for row in LEGAL],
        "if_write_sits": "If (6) sits, (7)-(9) give global regularity.",
        "do_not": "Do not graft Q1 onto B. Track A is a different equation.",
        "mine": MINE,
        "needed": NEEDED,
    },
    "A": {
        "id": "A",
        "aliases": ("track a", "q1", "augmented"),
        "slot": "A",
        "name": "Q1-augmented Navier-Stokes (this PDE)",
        "object": {
            "name": "Q1-augmented NS",
            "slot": "A",
            "english": "Ladyzhenskaya / p-Laplacian NS at eps>0, beta>=1/2",
            "window": [
                "this PDE, not classical NS",
                "Theorem A sits: unique C^infty at eps>0, beta>=1/2",
                "need: ||u||_H1 <= C independent of eps, or a named no-go",
                "A6: Q1 integral falls as eps falls (the renormalization)",
                "A7 fail: box enstrophy is not uniform in eps",
                "A=>B fail. F is not this object. No Phi.",
            ],
        },
        "theorem": (
            "Let nu>0, eps>0, alpha>0, beta>=1/2, and u0 in H^1(T^3) "
            "divergence-free. The Q1 system has a unique solution "
            "u in C^infty(T^3 x (0,infty)) cap L^infty(0,infty; H^1). "
            "No finite-time singularity for this PDE."
        ),
        "lines": A_LINES,
        "chain_doc": "docs/A-PROOF-CHAIN.md",
        "proceed": [
            "||u||_H1 <= C independent of eps, all smooth divergence-free H^1 data",
            "a named obstruction that C must blow up as eps->0",
            "not a decaying Q1 integral (A9 already fail)",
            "not Phi, not a slide onto Track B",
        ],
        "if_write_sits": (
            "If (7) sits, Lemma 4 is uniform in eps. Classical NS is still Track B."
        ),
        "do_not": (
            "Do not export Theorem A onto B. Do not Phi. "
            "Do not retune nodes.json. A=>B stays fail."
        ),
        "mine": [],
        "needed": [],
        "this_pde_complete": True,
    },
    "RH": {
        "id": "RH",
        "aliases": ("rh", "riemann"),
        "slot": "RH",
        "name": "Riemann hypothesis",
        "object": {
            "name": "non-trivial zeros of zeta",
            "slot": "RH",
            "english": "every non-trivial zero of zeta has real part 1/2",
            "window": [
                "xi(s) = xi(1-s), entire of order 1",
                "need: Re rho = 1/2 for every non-trivial zero rho",
                "Track Q on this desk is inverse-GCD, not RH",
                "Theorem P is not the Riemann hypothesis",
            ],
        },
        "theorem": (
            "Every non-trivial zero of the Riemann zeta function "
            "has real part equal to 1/2."
        ),
        "lines": RH_LINES,
        "chain_doc": "docs/RH-PROOF-CHAIN.md",
        "proceed": [
            "a zero-free region that reaches Re s = 1/2",
            "a positivity certificate in the explicit formula that forces the line",
            "one new estimate that puts every zero on Re s = 1/2",
        ],
        "if_write_sits": "If (6) sits, (7)-(8) are the classical consequences.",
        "do_not": (
            "Do not glue inverse-GCD / Theorem P / Bridge* onto RH. "
            "Track Q is a different object."
        ),
        "mine": [],
        "needed": [],
        "best_paper": {
            "name": (
                "August inverse-GCD (Zenodo 22045478) plus the "
                "spectral-floor retraction"
            ),
            "slot": "Q",
            "doc": "docs/SPECTRAL-FLOOR-EXPLORATION.md",
            "sits": [
                "Bridge*: R(e_p - e_q) > -1/2 on Q-tilde (pair identity)",
                "Theorem P: prime-supported Q-tilde >= -1/4",
                "H_N = D^{-1/2} Q-tilde D^{-1/2}, lambda_min(H_N) >= -1 (pairing)",
                "v >= 0 => v^T Q-tilde v >= 0",
            ],
            "false": [
                "lambda_min(Q_N) > -1/2  (Q_10 ~ -1.90)",
                "lambda_min(H_N) >= -3/14  (H_4 ~ -0.225)",
            ],
            "not": (
                "These are completed Q theorems. They are not RH line (6). "
                "A GCD matrix is not a zero. Do not glue."
            ),
        },
    },
}

# Back-compat names for existing NS tests.
THEOREM = {"aimed": PROBLEMS["NS"]["theorem"], "object": WALL["target_B"], "form": WALL["looks_like"]}
LINES = NS_LINES


CLAIMS = [
    rec(
        "C1",
        "ask_for_the_chain",
        "You can tell DA to write a proof chain by naming the problem",
        "pass",
        "NS / Track B / Track A / Q1 / RH / Riemann. The operator does not need the chops.",
    ),
    rec(
        "C2",
        "chain_is_the_argument",
        "The written chain is the aimed theorem plus have / write / follows",
        "pass",
        "Ground floor up. Line WRITE is the attempt.",
    ),
    rec(
        "C3",
        "emit_is_qed",
        "Emitting the proof chain is QED",
        "fail",
        "The chain is the argument. WRITE is still a write.",
    ),
    rec(
        "C4",
        "llm_writes_line_6",
        "An LLM writes the WRITE line into a theorem",
        "fail",
        "It may phrase a candidate. The checker scores it.",
    ),
    rec(
        "C5",
        "nothing_wrong_with_asking",
        "Asking DA to write a proof chain is a category error",
        "fail",
        "Asking is the product. A fake last line is the refuse.",
    ),
    rec(
        "C6",
        "line_write_may_sit",
        "The WRITE line may sit later",
        "open",
        "That is the attempt. The aimed theorem follows if it sits.",
    ),
    rec(
        "C7",
        "q_is_rh",
        "Track Q / Theorem P is the Riemann hypothesis",
        "fail",
        "Inverse-GCD floors are not zeta zeros. No glue.",
    ),
    rec(
        "C8",
        "more_problems",
        "More named problems may get a ground-floor chain",
        "open",
        "A problem sits when the aimed theorem and the have/write/follows lines are typed.",
    ),
    rec(
        "C9",
        "a_is_b",
        "Theorem A is classical Navier-Stokes",
        "fail",
        "Different equation. A=>B stays fail. Track B is the other chain.",
    ),
]


def _flag_problem(problem: str) -> str | None:
    raw = (problem or "").strip()
    if not raw:
        return None
    key = raw.upper().replace("TRACK ", "").replace("TRACK", "")
    if key in ("B", "NS"):
        return "NS"
    if key in PROBLEMS:
        return key
    return None


def parse_problems(ask: str = "", problem: str = "") -> list[str]:
    """Problems named in the ask, in desk order NS / A / RH."""
    text = f"{problem} {ask}".lower()
    found: list[str] = []
    flagged = _flag_problem(problem)
    if flagged:
        found.append(flagged)
    if re.search(
        r"\btrack b\b|xavier|\bnavi\b|\bstokes\b|\bnavier\b|\bunaugmented\b|\bns\b",
        text,
    ):
        if "NS" not in found:
            found.append("NS")
    if re.search(r"\btrack a\b|\bq_?1\b", text):
        if "A" not in found:
            found.append("A")
    if re.search(r"\brh\b|riemann", text):
        if "RH" not in found:
            found.append("RH")
    return found or ["NS"]


def parse_problem(ask: str = "", problem: str = "") -> str:
    return parse_problems(ask=ask, problem=problem)[0]


def is_proof_ask(ask: str) -> bool:
    """Write me the proof chain / NS / RH."""
    from da_done import is_done_ask

    text = (ask or "").lower().strip()
    if not text:
        return False
    if is_done_ask(text):
        return False
    return bool(
        re.search(
            r"\bwrite (me )?(the )?proof\b|\bproof chain\b|"
            r"\bxavier stokes\b|\bnavi(er)?.?stokes\b|"
            r"\bda proof\b|\bthe proof for (ns|navier|rh|riemann|track [ab]|q1)\b|"
            r"\btrack [ab]\b.*\bwrite\b|\bwrite\b.*\btrack [ab]\b|"
            r"\bwrite rh\b|\bmy best paper\b.*\b(rh|riemann|write)\b|"
            r"\brh\b|\briemann\b",
            text,
        )
    )


def print_problem_window(obj: dict) -> None:
    print("OBJECT WINDOW")
    print(f"  {obj['name']}  slot {obj['slot']}")
    print(f"  {obj['english']}")
    for line in obj["window"]:
        print(f"  {line}")


def _chain(pid: str) -> dict:
    spec = PROBLEMS[pid]
    write_n = next(L["n"] for L in spec["lines"] if L["status"] == "write")
    return {
        "problem": pid,
        "theorem": {"aimed": spec["theorem"], "name": spec["name"]},
        "object": spec["object"],
        "lines": spec["lines"],
        "mine": spec["mine"],
        "needed": spec["needed"],
        "proceed": spec["proceed"],
        "if_write_sits": spec["if_write_sits"],
        "do_not": spec["do_not"],
        "write_n": write_n,
        "chain_doc": spec["chain_doc"],
        "this_pde_complete": spec.get("this_pde_complete", False),
        "best_paper": spec.get("best_paper"),
        "counts": {
            "lines": len(spec["lines"]),
            "have": sum(1 for L in spec["lines"] if L["status"] == "have"),
            "write": sum(1 for L in spec["lines"] if L["status"] == "write"),
            "follows": sum(1 for L in spec["lines"] if L["status"] == "follows"),
        },
    }


def run(out: Path | None = None, problem: str = "NS", ask: str = "") -> dict:
    pids = parse_problems(ask=ask, problem=problem)
    chains = [_chain(pid) for pid in pids]
    first = chains[0]
    write_ns = [c["write_n"] for c in chains]
    payload = {
        "meta": {
            "question": "write the proof chain for " + ", ".join(pids),
            "writeup": "docs/DA-PROOF.md",
            "chain": first["chain_doc"],
            "chains": [c["chain_doc"] for c in chains],
            "problem": first["problem"],
            "nothing_wrong_with_asking": True,
            "emit_is_not_qed": True,
            "q_is_not_rh": True,
            "a_is_not_b": True,
            "operator_needs_no_chops": True,
        },
        "problem": first["problem"],
        "picked": pids,
        "problems": list(PROBLEMS),
        "chains": chains,
        "theorem": first["theorem"],
        "object": first["object"],
        "lines": first["lines"],
        "mine": first["mine"],
        "needed": first["needed"],
        "proceed": first["proceed"],
        "if_write_sits": first["if_write_sits"],
        "do_not": first["do_not"],
        "write_n": first["write_n"],
        "claims": CLAIMS,
        "counts": {
            "problems": len(PROBLEMS),
            "picked": len(pids),
            "lines": first["counts"]["lines"],
            "have": first["counts"]["have"],
            "write": first["counts"]["write"],
            "follows": first["counts"]["follows"],
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Line "
            + "/".join(f"({n})" for n in write_ns)
            + " is the write. Classify one candidate. "
            "If it sits, the THEN lines follow. That is the close. "
            "A is not B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_proof.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def _print_one_chain(chain: dict) -> None:
    print_problem_window(chain["object"])
    print()
    print(f"PROBLEM {chain['problem']}")
    print()
    print("THEOREM (aimed)")
    print(" ", chain["theorem"]["aimed"])
    print()
    print("PROOF CHAIN  (ground floor up)")
    for L in chain["lines"]:
        tag = {"have": "HAVE", "write": "WRITE", "follows": "THEN"}[L["status"]]
        print(f"  ({L['n']}) [{tag}] {L['text']}")
    print()
    print(chain["if_write_sits"])
    print(chain["do_not"])
    print("A candidate for the WRITE line:")
    for row in chain["proceed"]:
        print(f"  - {row}")
    paper = chain.get("best_paper")
    if paper:
        print()
        print(f"FROM YOUR BEST PAPER  (slot {paper['slot']}, not RH (6))")
        print(f"  {paper['name']}")
        print("  sits:")
        for row in paper["sits"]:
            print(f"    [HAVE as Q] {row}")
        print("  withdrawn:")
        for row in paper["false"]:
            print(f"    [FAIL] {row}")
        print(f"  {paper['not']}")
        print(f"  {paper['doc']}")
    print()


def print_proof(out: Path | None = None, problem: str = "NS", ask: str = "") -> dict:
    payload = run(out=out, problem=problem, ask=ask)
    print("Problems on this desk:", ", ".join(payload["problems"]))
    print("Writing:", ", ".join(payload["picked"]))
    print()
    for chain in payload["chains"]:
        _print_one_chain(chain)
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    print("chain:", ", ".join(payload["meta"]["chains"]))
    return payload


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    ask = " ".join(args)
    print_proof(problem=args[0] if args else "NS", ask=ask)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
