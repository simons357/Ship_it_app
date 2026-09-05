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


YM_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Gauge field. A connection on an SU(N) bundle, curvature F, "
            "Yang-Mills action (1/4) int Tr F wedge *F."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "SM block. This desk's Lagrangian contains working YM: "
            "SU(3)_c (QCD) and SU(2)_L before the VEV. Lineage both ways."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "A Lagrangian piece is not a gap. Local existence and "
            "energy for classical YM are a different literature."
        ),
    },
    {
        "n": 4,
        "status": "write",
        "text": (
            "WRITE. Mass gap: the Hamiltonian spectrum on the "
            "vacuum-orthogonal subspace is bounded below by a positive constant."
        ),
    },
    {
        "n": 5,
        "status": "follows",
        "text": (
            "If (4) sits, that gap is a theorem for this YM theory. "
            "Still not NS. Still not Q. Still not Goldbach."
        ),
    },
]


BSD_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Elliptic curve. E/Q, Weierstrass model, conductor N, "
            "finite torsion E(Q)_tors."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "Mordell-Weil. E(Q) is finitely generated: "
            "E(Q) = Z^r ⊕ E(Q)_tors. r is the algebraic rank."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Modularity. Every E/Q is modular (Wiles / BCDT). "
            "L(E,s) = L(f,s) for a weight-2 newform, entire, "
            "functional equation s <-> 2-s."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Analytic rank. r_an = ord_{s=1} L(E,s). "
            "The aimed equality is r = r_an."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "Low rank. If r_an is 0 or 1, then r = r_an and Sha is finite "
            "(Gross-Zagier / Kolyvagin; Coates-Wiles for many CM rank-0 cases). "
            "Literature, not a theorem of this desk."
        ),
    },
    {
        "n": 6,
        "status": "write",
        "text": (
            "WRITE. For every E/Q: r = r_an, Sha(E/Q) is finite, and "
            "the leading coefficient of L(E,s) at s=1 equals "
            "Omega * Reg * #Sha * prod Tamagawa / #E(Q)_tors^2."
        ),
    },
    {
        "n": 7,
        "status": "follows",
        "text": (
            "If (6) sits, the arithmetic of E(Q) is read from L(E,s). "
            "Still not RH. Still not Q. Still not Goldbach. Still not NS."
        ),
    },
]


HODGE_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Hodge decomposition. For compact Kähler X, "
            "H^k(X,C) = ⊕_{p+q=k} H^{p,q}(X)."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "Hodge classes. Hdg^p(X) = H^{2p}(X,Q) ∩ H^{p,p}(X). "
            "These are the rational (p,p) classes."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Cycle class. An algebraic cycle of codimension p maps to a "
            "Hodge class. Algebraic implies Hodge. The converse is the write."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Lefschetz (1,1). Every Hodge class of type (1,1) is algebraic "
            "(divisors). p=1 sits. Literature, not a theorem of this desk."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "Special cases. Known for some abelian varieties and some "
            "complete intersections. Literature. The integer form is false "
            "(Atiyah-Hirzebruch). The aimed statement is over Q."
        ),
    },
    {
        "n": 6,
        "status": "write",
        "text": (
            "WRITE. For every smooth complex projective X and every p, "
            "every rational Hodge class is algebraic."
        ),
    },
    {
        "n": 7,
        "status": "follows",
        "text": (
            "If (6) sits, Hodge classes are algebraic cycles. "
            "Still not BSD. Still not RH. Still not NS. Still not YM."
        ),
    },
]


POINCARE_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Object. A closed 3-manifold M. Simply connected means π_1(M)=0."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "Statement. M is homeomorphic to S^3."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Ricci flow. Hamilton: ∂_t g = -2 Ric(g). Singularities remain."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Surgery. Perelman: entropy, no local collapsing, surgery at necks."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "Extinction. On a simply connected closed 3-manifold the flow "
            "becomes extinct after finitely many surgeries. Pieces are spherical."
        ),
    },
    {
        "n": 6,
        "status": "have",
        "text": (
            "The statement sits. Every simply connected closed 3-manifold "
            "is homeomorphic to S^3 (Perelman; literature). No WRITE line."
        ),
    },
    {
        "n": 7,
        "status": "have",
        "text": (
            "Geometrization. The same method gives Thurston geometrization. "
            "Literature. Still not NS. Still not P vs NP."
        ),
    },
]


PNP_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "P. Languages decided by a deterministic Turing machine in time n^{O(1)}."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "NP. Languages with a polynomial-time verifier, equivalently a "
            "nondeterministic TM in polynomial time."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "NP-complete. Cook-Levin: SAT is NP-complete. Polynomial-time reductions."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "SFE is not the model. The letter's H(x) is a field path, not a TM. "
            "Shelved. It does not decide a language in P or NP."
        ),
    },
    {
        "n": 5,
        "status": "write",
        "text": (
            "WRITE. A proof that P=NP or that P≠NP in the Turing-machine model. "
            "Relativization, natural proofs, and algebrization are barriers, not the write."
        ),
    },
    {
        "n": 6,
        "status": "follows",
        "text": (
            "If (5) sits, every NP language is in P, or some NP language is not. "
            "Still not NS. Still not Hodge. Still not SFE."
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
    "YM": {
        "id": "YM",
        "aliases": ("yang-mills", "yang mills", "ym"),
        "slot": "U",
        "name": "Yang-Mills mass gap",
        "object": {
            "name": "Yang-Mills Hamiltonian gap",
            "slot": "U",
            "english": "spectrum of the YM Hamiltonian bounded below by a positive constant",
            "window": [
                "SU(N) connection, curvature F, YM action",
                "SM contains working YM blocks (SU(3)_c, SU(2)_L)",
                "need: mass gap, a positive lower bound on the spectrum",
                "a Lagrangian piece is not the gap",
                "not NS, not Q, not Goldbach",
            ],
        },
        "theorem": (
            "For 4-dimensional quantum Yang-Mills with compact simple "
            "gauge group, the Hamiltonian has a mass gap: the spectrum "
            "on the vacuum-orthogonal subspace is bounded below by "
            "a positive constant."
        ),
        "lines": YM_LINES,
        "chain_doc": "docs/YM-PROOF-CHAIN.md",
        "proceed": [
            "a positive lower bound on the Hamiltonian spectrum",
            "a named obstruction that the gap cannot sit on this desk",
            "not the SM Lagrangian piece (that already sits)",
            "not a slide onto Track B or Q",
        ],
        "if_write_sits": (
            "If (4) sits, the gap is a theorem. Still not NS. Still not Q."
        ),
        "do_not": (
            "Do not emit the SM YM block as the gap. "
            "Do not glue YM onto NS, Q, or Goldbach."
        ),
        "mine": [],
        "needed": [],
    },
    "BSD": {
        "id": "BSD",
        "aliases": ("bsd", "birch", "swinnerton", "swinnerton-dyer"),
        "slot": "U",
        "name": "Birch-Swinnerton-Dyer",
        "object": {
            "name": "rank of E(Q) versus L(E,s)",
            "slot": "U",
            "english": "algebraic rank equals analytic rank; Sha finite; leading term",
            "window": [
                "E/Q, Mordell-Weil rank r",
                "L(E,s) entire by modularity",
                "need: r = ord_{s=1} L(E,s) for every E/Q",
                "need: Sha finite and the leading-term formula",
                "r_an in {0,1} is literature (Gross-Zagier / Kolyvagin)",
                "best paper: Zenodo 20552682 BSD_SPECTRAL_FRAMEWORK (Q prototype, not (6))",
                "not RH, not Q, not Goldbach, not NS",
            ],
        },
        "theorem": (
            "Let E/Q be an elliptic curve. Let r = rank E(Q) and "
            "r_an = ord_{s=1} L(E,s). Then r = r_an, Sha(E/Q) is finite, "
            "and the leading coefficient of L(E,s) at s=1 equals "
            "Omega * Reg * #Sha * prod_p c_p / #E(Q)_tors^2."
        ),
        "lines": BSD_LINES,
        "chain_doc": "docs/BSD-PROOF-CHAIN.md",
        "proceed": [
            "r = r_an for every E/Q, including r_an >= 2",
            "Sha(E/Q) finite for every E/Q",
            "the leading-term formula for every E/Q",
            "not a Gross-Zagier / Kolyvagin reprint for rank 0 or 1",
            "not inverse-GCD, not zeta, not NS",
        ],
        "if_write_sits": (
            "If (6) sits, the arithmetic of E(Q) is read from L(E,s). "
            "Still not RH. Still not Q."
        ),
        "do_not": (
            "Do not glue L(E,s) onto zeta. Do not use Theorem P or Bridge*. "
            "Do not emit rank 0-1 literature as the full write. "
            "Do not emit 20552682 as BSD. Do not revive the Q floor. "
            "Do not unshelve GNC. The NS→RH→BSD ladder is not a close."
        ),
        "mine": [],
        "needed": [],
        "best_paper": {
            "name": (
                "Jonathan Robert Simons, The Prime Lattice as "
                "a Prototype for the BSD Hamiltonian "
                "(Zenodo 20552682; BSD_SPECTRAL_FRAMEWORK.pdf)"
            ),
            "slot": "Q",
            "doc": "docs/BSD-PROOF-CHAIN.md",
            "sits": [
                "Twisted Möbius of Ĥ_E: μ_E(gcd)/gcd with φ_E twist from a_p",
                "a_p=1 sends Ĥ_E to raw Q_N=1/gcd (zeta prototype)",
            ],
            "false": [
                "λ_min(H_N)>-1/2  (raw Q; Q_10 ~ -1.90; retracted)",
                "20552682 proves BSD",
                "BSD final.pdf is a second public BSD proof",
            ],
            "not": (
                "These are the prototype. They are not BSD line (6). "
                "Inverse-GCD is not L(E,s). Naming ker(Ĥ_E) is not "
                "dim ker = rank. A phone file named BSD final.pdf "
                "is not a second close. This PDF is not Hodge. "
                "GNC stays withdrawn. Do not glue."
            ),
        },
    },
    "HODGE": {
        "id": "HODGE",
        "aliases": ("hodge", "hodge conjecture"),
        "slot": "U",
        "name": "Hodge conjecture",
        "object": {
            "name": "rational Hodge classes",
            "slot": "U",
            "english": "every rational (p,p) class is an algebraic cycle",
            "window": [
                "smooth complex projective X",
                "Hdg^p(X) = H^{2p}(X,Q) ∩ H^{p,p}(X)",
                "need: every Hodge class algebraic, all X, all p",
                "p=1 sits (Lefschetz 1,1)",
                "no Simons Hodge paper on this desk",
                "BSD final.pdf is BSD, not this leftover",
                "Hodge Laplacian → Betti is not this leftover",
            ],
        },
        "theorem": (
            "Let X be a smooth complex projective variety. For every "
            "integer p >= 0, every class in H^{2p}(X,Q) ∩ H^{p,p}(X) "
            "is a Q-linear combination of classes of algebraic cycles "
            "of codimension p."
        ),
        "lines": HODGE_LINES,
        "chain_doc": "docs/HODGE-PROOF-CHAIN.md",
        "proceed": [
            "every rational Hodge class algebraic, all smooth complex projective X, all p",
            "a named obstruction that some Hodge class cannot be algebraic",
            "not Lefschetz (1,1) reprinted as the full write",
            "not the Hodge Laplacian to Betti",
            "not BSD final.pdf / 20552682",
        ],
        "if_write_sits": (
            "If (6) sits, Hodge classes are algebraic cycles. "
            "Still not BSD. Still not RH."
        ),
        "do_not": (
            "Do not glue Hodge onto BSD, Q, or NS. "
            "Do not emit Lefschetz (1,1) as the full write. "
            "Do not emit the Hodge Laplacian as the conjecture. "
            "Do not emit BSD final.pdf as Hodge. Do not emit SFE as Hodge."
        ),
        "mine": [],
        "needed": [],
    },
    "POINCARE": {
        "id": "POINCARE",
        "aliases": ("poincare", "poincaré", "point care"),
        "slot": "U",
        "name": "Poincaré conjecture",
        "object": {
            "name": "simply connected closed 3-manifolds",
            "slot": "U",
            "english": "every simply connected closed 3-manifold is S^3",
            "window": [
                "closed 3-manifold M, π_1(M)=0",
                "need: M homeomorphic to S^3",
                "Perelman sits (literature, 2002-2003)",
                "this desk reprints; it did not prove it just now",
                "not NS smoothness, not P vs NP, not SFE",
            ],
        },
        "theorem": (
            "Every closed simply connected 3-manifold is homeomorphic "
            "to the 3-sphere."
        ),
        "lines": POINCARE_LINES,
        "chain_doc": "docs/POINCARE-PROOF-CHAIN.md",
        "proceed": [
            "nothing to write; Perelman sits",
            "a reprint is not a new theorem of this desk",
        ],
        "if_write_sits": (
            "There is no WRITE. Perelman sits (literature). "
            "Still not NS smoothness."
        ),
        "do_not": (
            "Do not emit this reprint as a theorem of DA. "
            "Do not glue Poincaré onto Track B or SFE."
        ),
        "mine": [],
        "needed": [],
        "literature_complete": True,
    },
    "PNP": {
        "id": "PNP",
        "aliases": ("p vs np", "p versus np", "p=np"),
        "slot": "U",
        "name": "P versus NP",
        "object": {
            "name": "P vs NP in the Turing model",
            "slot": "U",
            "english": "a TM proof that P=NP or that P≠NP",
            "window": [
                "P = deterministic poly-time TM",
                "NP = poly-time verifier / nondeterministic TM",
                "need: P=NP or P≠NP in that model",
                "SFE H(x) is not a TM",
                "the enclosed letter is not leftover (5)",
            ],
        },
        "theorem": (
            "Either P=NP or P≠NP, proved for languages decided by "
            "Turing machines with a polynomial-time clock."
        ),
        "lines": PNP_LINES,
        "chain_doc": "docs/PNP-PROOF-CHAIN.md",
        "proceed": [
            "a TM proof that some NP language is not in P",
            "a TM proof that every NP language is in P",
            "not an SFE / resonance / harmonic-field rewrite",
            "not a barrier paper reprinted as the close",
        ],
        "if_write_sits": (
            "If (5) sits, every NP language is in P, or some NP language is not. "
            "Still not SFE."
        ),
        "do_not": (
            "Do not emit the SFE letter as P≠NP. SFE is shelved. "
            "Do not glue a field path onto a Turing machine."
        ),
        "mine": [],
        "needed": [],
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
        "NS / Track B / Track A / Q1 / RH / Riemann / Yang-Mills / BSD / Hodge / Poincaré / P vs NP. The operator does not need the chops.",
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
    rec(
        "C10",
        "finish_bad_closes",
        "Please finish bad closes leftover (6)",
        "fail",
        "The chain can be printed complete-as-written. Line (6) still does not sit.",
    ),
    rec(
        "C11",
        "bsd_final_is_hodge",
        "BSD final.pdf is the Hodge conjecture",
        "fail",
        "That file is the BSD zeta prototype. A Hodge class is not L(E,s).",
    ),
    rec(
        "C12",
        "sfe_proves_pnp",
        "The SFE harmonic convergence H(x) proves P≠NP",
        "fail",
        "SFE is shelved. H(x) is not a Turing machine. The letter assumes the close.",
    ),
    rec(
        "C13",
        "poincare_open",
        "The Poincaré conjecture is still an open WRITE on this desk",
        "fail",
        "Perelman sits in the literature. DA reprints. No WRITE line.",
    ),
    rec(
        "C14",
        "zenodo_ns_is_smoothness",
        "The Zenodo NS / Phi / SND papers are classical smoothness and existence",
        "fail",
        "Phi is Track A. SND/Ring are conditional. Status note: unconditional 3D NS is not claimed.",
    ),
    rec(
        "C15",
        "complete_versions_close",
        "Writing the final corrected complete versions closes the leftovers",
        "fail",
        "Complete means HAVE / WRITE / THEN with a ledger. WRITE still does not sit.",
    ),
    rec(
        "C16",
        "complete_is_the_exam",
        "Asking for complete versions is the study exam: understand, write, assist; not emit-as-QED",
        "pass",
        "DA can write every seated chain and refuse a fake last line. That is the job.",
    ),
    rec(
        "C17",
        "document_da_closed_bsd",
        "Document that DA completed BSD leftover (6) and closed it out",
        "fail",
        "The operator did not prove BSD. DA did not either. Help is the chain and the named write. A close certificate is the refuse.",
    ),
    rec(
        "C18",
        "sfe_proves_hodge",
        "SFE harmonic coherence proves the Hodge conjecture",
        "fail",
        "SFE is shelved. A field mode is not an algebraic cycle. Leftover (6) stays open.",
    ),
    rec(
        "C19",
        "named_write_is_filled",
        "Naming the WRITE line means DA filled the gap",
        "fail",
        "DA named the write. DA did not write it. A named blank is not a filled blank.",
    ),
]


def is_all_ask(ask: str = "", problem: str = "") -> bool:
    text = f"{problem} {ask}".lower()
    if re.search(r"^\s*all\s*$", (problem or "").strip().lower()):
        return True
    return bool(
        re.search(
            r"final.{0,48}complete|complete versions|"
            r"all (the )?(named )?proof chains|"
            r"\bproof --all\b|\ball problems\b|"
            r"master status|\bstatus report\b|"
            r"millenn|"
            r"\ball of the mp|"
            r"\bmp'?s\b|\bmps\b",
            text,
        )
    )


def _flag_problem(problem: str) -> str | None:
    raw = (problem or "").strip()
    if not raw:
        return None
    key = raw.upper().replace("TRACK ", "").replace("TRACK", "")
    if key in ("B", "NS"):
        return "NS"
    if key in ("YM", "YANG-MILLS", "YANG MILLS", "YANGMILLS"):
        return "YM"
    if key in ("BSD", "BIRCH", "SWINNERTON", "SWINNERTON-DYER"):
        return "BSD"
    if key in ("HODGE", "HODGE CONJECTURE"):
        return "HODGE"
    if key in ("POINCARE", "POINCARÉ", "POINT CARE", "POINTCARE"):
        return "POINCARE"
    if key in ("PNP", "P VS NP", "P VERSUS NP", "P=NP"):
        return "PNP"
    if key in ("ALL", "COMPLETE"):
        return None
    if key in PROBLEMS:
        return key
    return None


def parse_problems(ask: str = "", problem: str = "") -> list[str]:
    """Problems named in the ask, in desk order NS / A / RH / YM / BSD / HODGE / POINCARE / PNP."""
    text = f"{problem} {ask}".lower()
    if is_all_ask(ask=ask, problem=problem):
        return list(PROBLEMS)
    found: list[str] = []
    flagged = _flag_problem(problem)
    if flagged:
        found.append(flagged)
    if re.search(
        r"\btrack b\b|xavier|\bnavi\b|\bstokes\b|\bnavier\b|\bunaugmented\b|\bns\b|"
        r"\bfinish bad\b|\bbad for me\b|"
        r"smoothness and existence|existence and smoothness|"
        r"yang.?mills.{0,24}\b(and )?(b|bad)\b|\b(b|bad)\b.{0,24}yang.?mills",
        text,
    ):
        if "NS" not in found:
            found.append("NS")
    if re.search(r"\btrack a\b|\bq_?1\b", text):
        if "A" not in found:
            found.append("A")
    if re.search(r"\brh\b|riemann|\bzeta\b", text):
        if "RH" not in found:
            found.append("RH")
    if re.search(r"yang.?mills|\bym\b", text):
        if "YM" not in found:
            found.append("YM")
    if re.search(r"\bhodge\b", text):
        if "HODGE" not in found:
            found.append("HODGE")
    if re.search(
        r"\bbsd\b|birch|swinnerton|spectral.?framework|"
        r"bsd_spectral_framework|bsd%20final|bsd.?final",
        text,
    ):
        if "BSD" not in found:
            found.append("BSD")
    if re.search(r"poincar|point care|pointcare", text):
        if "POINCARE" not in found:
            found.append("POINCARE")
    if re.search(r"\bp\s*(versus|vs\.?)\s*np\b|\bp\s*=\s*np\b|\bp\s*≠\s*np\b", text):
        if "PNP" not in found:
            found.append("PNP")
    return found or ["NS"]


def parse_problem(ask: str = "", problem: str = "") -> str:
    return parse_problems(ask=ask, problem=problem)[0]


def is_proof_ask(ask: str) -> bool:
    """Write me the proof chain / NS / RH."""
    from da_done import is_done_ask
    from da_study import is_study_ask

    text = (ask or "").lower().strip()
    if not text:
        return False
    if is_done_ask(text) or is_study_ask(text):
        return False
    return bool(
        re.search(
            r"\bwrite (me )?(the )?proof\b|\bproof chain\b|"
            r"\bxavier stokes\b|\bnavi(er)?.?stokes\b|"
            r"\bda proof\b|\bthe proof for (ns|navier|rh|riemann|track [ab]|q1)\b|"
            r"\btrack [ab]\b.*\bwrite\b|\bwrite\b.*\btrack [ab]\b|"
            r"\bwrite rh\b|\bmy best paper\b.*\b(rh|riemann|write)\b|"
            r"\brh\b|\briemann\b|\bzeta\b|"
            r"yang.?mills|\bym\b|"
            r"\bbsd\b|birch|swinnerton|"
            r"spectral.?framework|bsd_spectral_framework|"
            r"bsd%20final|bsd.?final|"
            r"\bhodge\b|"
            r"poincar|point care|pointcare|"
            r"\bp\s*(versus|vs\.?)\s*np\b|"
            r"smoothness and existence|existence and smoothness|"
            r"final.{0,48}complete|complete versions|"
            r"all (the )?(named )?proof chains|"
            r"master status|\bstatus report\b|"
            r"millenn|"
            r"\ball of the mp|"
            r"\bmp'?s\b|\bmps\b|"
            r"\bfinish bad\b",
            text,
        )
    )


def print_problem_window(obj: dict) -> None:
    print("OBJECT WINDOW")
    print(f"  {obj['name']}  slot {obj['slot']}")
    print(f"  {obj['english']}")
    for line in obj["window"]:
        print(f"  {line}")


def _completion(spec: dict) -> dict:
    have = [L["n"] for L in spec["lines"] if L["status"] == "have"]
    write = [L["n"] for L in spec["lines"] if L["status"] == "write"]
    follows = [L["n"] for L in spec["lines"] if L["status"] == "follows"]
    leftover_sits = not write
    return {
        "done": have,
        "not_done": write,
        "waiting": follows,
        "emit_is_not_finish": not leftover_sits,
        "leftover_sits": leftover_sits,
    }


def _chain(pid: str) -> dict:
    spec = PROBLEMS[pid]
    writes = [L["n"] for L in spec["lines"] if L["status"] == "write"]
    write_n = writes[0] if writes else None
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
        "literature_complete": spec.get("literature_complete", False),
        "best_paper": spec.get("best_paper"),
        "completion": _completion(spec),
        "counts": {
            "lines": len(spec["lines"]),
            "have": sum(1 for L in spec["lines"] if L["status"] == "have"),
            "write": sum(1 for L in spec["lines"] if L["status"] == "write"),
            "follows": sum(1 for L in spec["lines"] if L["status"] == "follows"),
        },
    }


def _status_line(chain: dict) -> str:
    if chain.get("literature_complete") or chain["completion"]["leftover_sits"]:
        return "sits (literature)"
    if chain.get("this_pde_complete"):
        return f"this PDE sits; WRITE ({chain['write_n']}) open"
    return f"WRITE ({chain['write_n']}) open"


def run(out: Path | None = None, problem: str = "NS", ask: str = "") -> dict:
    pids = parse_problems(ask=ask, problem=problem)
    chains = [_chain(pid) for pid in pids]
    first = chains[0]
    write_ns = [c["write_n"] for c in chains if c["write_n"] is not None]
    dumping_all = is_all_ask(ask=ask, problem=problem)
    payload = {
        "meta": {
            "question": "write the proof chain for " + ", ".join(pids),
            "writeup": "docs/DA-COMPLETE.md" if dumping_all else "docs/DA-PROOF.md",
            "complete_is_not_qed": True,
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
        "status": [
            {"problem": c["problem"], "line": _status_line(c), "write_n": c["write_n"]}
            for c in chains
        ],
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
            (
                "Line "
                + "/".join(f"({n})" for n in write_ns)
                + " is the write. Classify one candidate. "
                "If it sits, the THEN lines follow. That is the close. "
                "A is not B."
            )
            if write_ns
            else (
                "No WRITE line on this pick. Literature sits. "
                "A reprint is not a new theorem of this desk."
            )
        )
        if not dumping_all
        else (
            "These are the complete-as-written chains. "
            "Open WRITE lines still do not sit. Emit is not QED."
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
    done = chain["completion"]
    print("COMPLETION")
    print("  done:", " ".join(f"({n})" for n in done["done"]) or "(none)")
    print("  not done:", " ".join(f"({n})" for n in done["not_done"]))
    print("  waiting on the write:", " ".join(f"({n})" for n in done["waiting"]) or "(none)")
    if done["leftover_sits"]:
        print("  Leftover sits in the literature. A reprint is not a new theorem.")
    else:
        print("  Emit is not a finish. Leftover does not sit.")
    print()
    print(chain["if_write_sits"])
    print(chain["do_not"])
    print("A candidate for the WRITE line:")
    for row in chain["proceed"]:
        print(f"  - {row}")
    paper = chain.get("best_paper")
    if paper:
        print()
        print(
            f"FROM YOUR BEST PAPER  (slot {paper['slot']}, "
            f"not {chain['problem']} ({chain['write_n']}))"
        )
        print(f"  {paper['name']}")
        print("  sits:")
        for row in paper["sits"]:
            print(f"    [HAVE as {paper['slot']}] {row}")
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
    if len(payload["status"]) > 1:
        print()
        print("STATUS  (complete-as-written, not QED)")
        for row in payload["status"]:
            print(f"  {row['problem']}: {row['line']}")
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
