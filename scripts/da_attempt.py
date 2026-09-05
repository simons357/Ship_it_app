#!/usr/bin/env python3
"""
DA attempt: take the operator's best A (Q1 + renormalization)
and best RH work. Dream-team papers look. They say what they
would do, how, and DA does the legal write.

A vote does not complete a missing line. Theorem A is already
complete for this PDE. RH WRITE does not sit. Q is not RH.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


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


def chair(
    who: str,
    paper: str,
    would: str,
    how: str,
    cannot: str,
    does: str,
    sits: bool,
) -> dict:
    return {
        "who": who,
        "paper": paper,
        "would": would,
        "how": how,
        "cannot": cannot,
        "does": does,
        "sits": sits,
    }


JOBS = {
    "A": {
        "id": "A",
        "aliases": (
            "augmented",
            "q1",
            "renormal",
            "olga",
            "ladyzhenskaya",
            "track a",
        ),
        "name": "Q1-augmented NS (this PDE) plus the eps->0 renormalization",
        "slot": "A",
        "furthest": (
            "Theorem A pass: energy, Galerkin, weak limit, unique H1, "
            "C^infty at eps>0, beta>=1/2. That is the close you already have. "
            "The latest extra write is the renormalization: send the extra "
            "dissipation to zero (A6: Q1 integral falls as eps falls) and "
            "hope H1 stays. It does not, on the scored box."
        ),
        "progress": [
            {"id": "A1", "what": "energy identity", "verdict": "pass"},
            {"id": "A2", "what": "Galerkin global", "verdict": "pass"},
            {"id": "A3", "what": "weak limit is a weak solution", "verdict": "pass"},
            {"id": "A4", "what": "unique H1 at eps>0, beta>=1/2", "verdict": "pass"},
            {"id": "A5", "what": "C^infty bootstrap at eps>0", "verdict": "pass"},
            {"id": "A_theorem", "what": "Theorem A for this PDE", "verdict": "pass"},
            {"id": "A6", "what": "Q1 integral falls as eps falls (the renormalization)", "verdict": "pass"},
            {"id": "A7", "what": "enstrophy on the box is independent of eps", "verdict": "fail"},
            {"id": "A8", "what": "box non-uniformity is a no-go for all data", "verdict": "fail"},
            {"id": "A9", "what": "Q1 vanishing writes a uniform H1 bound", "verdict": "fail"},
            {"id": "A_uniform_H1", "what": "Lemma 4 stays finite as eps->0", "verdict": "open"},
            {"id": "A_implies_B", "what": "Theorem A is classical NS", "verdict": "fail"},
        ],
        "errors_corrected": [
            "Hearing Theorem A closed is not classical NS.",
            "Vanishing Q1 (the renormalization) is the gap, not a bound (A9).",
            "Phi is not the estimate variable.",
            "Exporting Ladyzhenskaya onto B is refused.",
            "A=>B is refused.",
        ],
        "needs": (
            "A bound on ||u||_H1 that stays finite as eps->0, or a named "
            "obstruction that it cannot. That write stays on A. Classical "
            "NS then still needs a separate Track B argument."
        ),
        "need_to_close": [
            "This PDE: already closed (Theorem A).",
            "Renormalization close: ||u||_H1 finite as eps->0, or a named no-go.",
            "Classical NS: that uniform bound, then a separate Track B argument.",
        ],
        "do": [
            "Stop re-proving Theorem A. Energy, Galerkin, unique H1, C^infty already sit at eps>0, beta>=1/2.",
            "Write one sentence: ||u(t)||_H1 <= C with C independent of eps, for all smooth data, or a named obstruction that C must blow up.",
            "Classify that sentence as Track A. Run: python3 scripts/da_machine.py tracka",
            "Kill it on the Taylor-Green box if it claims the box is already uniform (A7 fail). A decaying Q1 integral is not the bound (A9 fail).",
            "Do not cancel to Phi. Do not retune nodes.json. Do not slide eps onto B.",
            "If the uniform bound sits, classical NS is still a separate Track B write (integrable R). A=>B stays fail.",
        ],
        "completed": (
            "This PDE: the chain is already complete (Theorem A). "
            "The renormalization to eps=0 is not complete. "
            "Classical NS is not complete."
        ),
        "docs": (
            "docs/TRACK-A-LEMMAS.md",
            "docs/TRACK-A-GAP.md",
            "docs/AUGMENTED-NS-PROOF-CHAIN.md",
            "docs/DA-REPAIR.md",
        ),
        "team": [
            chair(
                "Ladyzhenskaya",
                "1968 modified-stress / p-Laplacian NS",
                "Keep Theorem A on this PDE. I already closed it at eps>0, beta>=1/2.",
                "Extra integrability of grad u from the monotone extra stress. p>=5/2 in 3D.",
                "Pass eps->0. A different equation is not classical NS.",
                "Restate Theorem A as complete for this PDE. Leave Olga on A.",
                True,
            ),
            chair(
                "Malek-Necas-Ruzicka",
                "Weak and Measure-valued Solutions, Ch. 5",
                "Keep the weak limit and Minty-Browder passage for the extra stress.",
                "Galerkin + monotonicity. The extra dissipation only helps compactness.",
                "A uniform H1 constant as eps->0.",
                "Keep Lemmas 2-4 as scored. A4's constant still blows up.",
                True,
            ),
            chair(
                "Temam",
                "smoothness / attractor after an H1 bound",
                "Bootstrap to C^infty once H1 is already uniform.",
                "Standard NS bootstrap. Gevrey and attractors wait on smoothness.",
                "Write the missing uniform constant.",
                "A5 stays pass only at eps>0. Do not treat the attractor as the gap.",
                True,
            ),
            chair(
                "Tao",
                "averaged / regularized cousins as different equations",
                "Treat Q1 as a different PDE. Do not export the close.",
                "Name the extra term. If it leaves, you have changed the problem back.",
                "A slide of eps onto B.",
                "Score A_implies_B fail. The renormalization is a different claim.",
                True,
            ),
            chair(
                "Fefferman",
                "Clay official NS problem; geometric ifs on the classical field",
                "If you want classical regularity, write an a priori on classical leftover.",
                "Alignment in time (A1) is an if on B, not a Q1 identity.",
                "Cash Olga as Fefferman A1.",
                "Send the classical close to the B chain. Do not mix chairs.",
                True,
            ),
            chair(
                "Constantin",
                "geometric depletion if aligned (with Fefferman)",
                "Geometry after you are on the classical vorticity field.",
                "CF-if on omega. CONC is not already aligned.",
                "Q1 dissipation as alignment. Phi as the estimate.",
                "Refuse Phi. Geometry stays off this A write.",
                True,
            ),
        ],
        "da_does": (
            "Correct the five errors. Print the A progress table. "
            "Complete the this-PDE chain (already sat). "
            "Attempt uniform H1 from the renormalization (A6/A7/A9): "
            "does not sit. Do not invent leftover B42. Do not retune nodes.json."
        ),
    },
    "B": {
        "id": "B",
        "aliases": (
            "unaugmented",
            "un-augmented",
            "classical ns",
            "track b",
            "1/r^4",
        ),
        "name": "classical NS — unaugmented, keep 1/r^4",
        "slot": "B",
        "furthest": (
            "Energy, enstrophy identity, leftover form, and the n=32 "
            "readings through B41 sit. A1 is off. A2 is live and did not "
            "blow on the B15 path. Break at S10: no all-data integrable R."
        ),
        "progress": [
            {"id": "S1", "what": "Leray energy", "verdict": "pass"},
            {"id": "S2", "what": "enstrophy identity", "verdict": "pass"},
            {"id": "S3", "what": "leftover form", "verdict": "pass"},
            {"id": "S4", "what": "B15 stretching on n=32", "verdict": "pass"},
            {"id": "S9", "what": "B41 A2 on the B15 path", "verdict": "pass"},
            {"id": "S10", "what": "all-data integrable R / A1 / A2", "verdict": "open"},
            {"id": "B_regularity", "what": "classical global regularity", "verdict": "open"},
            {"id": "A_implies_B", "what": "Theorem A is classical NS", "verdict": "fail"},
        ],
        "errors_corrected": [
            "Grafting Q1 onto B.",
            "Phi as the estimate.",
            "A box reading as an a priori.",
            "BKM from L2.",
            "Leftover-close B42 or n=64 as the write.",
        ],
        "needs": (
            "int_0^T R(t) dt < infinity for all data, or all-data A1, "
            "or all-data A2, or a field that kills the stretching leftover. "
            "Keep 1/r^4. No Q1."
        ),
        "need_to_close": [
            "Write one all-data integrable residual: int_0^T R < infinity.",
            "Or all-data A1 (alignment in time).",
            "Or all-data A2 (int ||lambda_2^+||).",
            "Or a killing field. Then Gronwall, Beale, bootstrap.",
        ],
        "do": [
            "Keep 1/r^4. Do not put Q1 or eps on this equation.",
            "Write one sentence that is an all-data bound: integrable R, or A1, or A2, or a killing field.",
            "Classify it as Track B. Run: python3 scripts/da_machine.py from",
            "The n=32 box (B15-B41) is a reading. It is not the a priori. Do not cash it.",
            "Do not cancel to Phi. Do not spawn n=64. Do not invent leftover B42.",
            "If that sentence sits, Gronwall gives X finite, Beale gives no blowup of ||omega||_infty, bootstrap gives smoothness.",
        ],
        "completed": (
            "Skeleton through S9 complete (not a priori). S10 not complete. "
            "Domain B open. One open catalog row: B_regularity."
        ),
        "docs": (
            "docs/NS-PROOF-CHAIN.md",
            "docs/DA-FROM.md",
            "docs/TRACK-B-OBJECT.md",
            "docs/TRACK-B-RESIDUAL.md",
        ),
        "team": [
            chair(
                "Tao",
                "residual honesty",
                "Write a closed estimate for X, a killing field, or one preprint identity.",
                "Name R. Do not average the equation into a cousin.",
                "An averaged cousin that blows. Leftover-close B42.",
                "Aim the next sentence at S10. Classify it.",
                True,
            ),
            chair(
                "Fefferman",
                "alignment if",
                "Depletion if vorticity stays aligned in time. That if is A1.",
                "Alignment in time for all data would make R integrable.",
                "Alignment for all data from a box. Geometry waits on the if.",
                "If you write A1, classify it. CF-if is not all-data A1.",
                True,
            ),
            chair(
                "Miller",
                "middle-strain cut",
                "The live cubic on this box is lambda_2^+. That integral is A2.",
                "int ||lambda_2^+|| for all data.",
                "A reading on n=32 as the a priori.",
                "A2 is live and did not blow on B15. Live is not all-data.",
                True,
            ),
            chair(
                "Lemarie-Rieusset",
                "The Navier-Stokes Problem in the 21st Century",
                "The map already lists the doors. Write the leftover, not another door.",
                "One all-data integral. Criteria stay criteria.",
                "The monograph as X in L^infty.",
                "Keep the picture. Take S10.",
                True,
            ),
            chair(
                "Ladyzhenskaya",
                "modified stress (Track A)",
                "I closed a different equation. Do not import me onto B.",
                "Leave Theorem A on A.",
                "eps->0 as the unaugmented close.",
                "A_implies_B stays fail.",
                True,
            ),
        ],
        "da_does": (
            "Print the unaugmented close-writes and the DO list. "
            "Walk stays at S10. Keep 1/r^4. Refuse Q1, Phi, B42, n=64."
        ),
    },
    "RH": {
        "id": "RH",
        "aliases": ("rh", "riemann", "zeta", "theorem p", "furthest"),
        "name": "Riemann hypothesis — furthest desk attempt was inverse-GCD",
        "slot": "RH / Q",
        "furthest": (
            "Classical RH chain through (5) sits (zeta, xi, strip, PNT, "
            "Hardy + proportion). The furthest original write on this desk "
            "was the inverse-GCD package: Bridge*, Theorem P "
            "(prime-supported Q-tilde >= -1/4), and the renormalized "
            "H_N = D^{-1/2} Q-tilde D^{-1/2} with H_N >= -1. "
            "Those are completed Q theorems. They were glued to zeros. "
            "That glue is the error. Full Q > -1/2 and H >= -3/14 are false."
        ),
        "progress": [
            {"id": "RH1", "what": "zeta meromorphic, Euler product", "verdict": "pass"},
            {"id": "RH2", "what": "xi entire, xi(s)=xi(1-s)", "verdict": "pass"},
            {"id": "RH3", "what": "non-trivial zeros in the strip", "verdict": "pass"},
            {"id": "RH4", "what": "no zeros on Re s = 1 (PNT)", "verdict": "pass"},
            {"id": "RH5", "what": "infinitely many / a proportion on Re s = 1/2", "verdict": "pass"},
            {"id": "RH6", "what": "every non-trivial zero has Re s = 1/2", "verdict": "open"},
            {"id": "Q_H_floor", "what": "lambda_min(H_N) >= -1 (renormalized Q)", "verdict": "pass"},
            {"id": "Q_theorem_P", "what": "prime-supported Q-tilde >= -1/4", "verdict": "pass"},
            {"id": "Q_bridge", "what": "Bridge* on e_p - e_q", "verdict": "pass"},
            {"id": "Q_full_floor", "what": "lambda_min(Q_N) > -1/2 for all N", "verdict": "fail"},
            {"id": "Q_h_314", "what": "lambda_min(H_N) >= -3/14", "verdict": "fail"},
            {"id": "Q_is_RH", "what": "Theorem P / H_N is the Riemann hypothesis", "verdict": "fail"},
        ],
        "errors_corrected": [
            "Track Q is inverse-GCD. It is not RH.",
            "Theorem P is not every zero on the line.",
            "H_N >= -1 is a matrix floor, not a zero.",
            "Bridge* is a two-prime identity, not RH.",
            "Q > -1/2 is false (Q_10 ~ -1.90).",
            "H >= -3/14 is false (H_4 ~ -0.225).",
        ],
        "needs": (
            "One write that puts every non-trivial zero on Re s = 1/2: "
            "a zero-free region that reaches the line, a positivity "
            "certificate in the explicit formula, or one new estimate "
            "that forces the line. Do not use Theorem P, Bridge*, or H_N."
        ),
        "need_to_close": [
            "RH close: every non-trivial zero has Re s = 1/2.",
            "Q floors H_N>=-1 and Theorem P: already closed as Q, not as RH.",
            "Do not close RH with a GCD matrix.",
        ],
        "completed": (
            "RH through (5): complete (literature + classical). "
            "RH WRITE (6): not complete. "
            "Q floors H_N>=-1 and Theorem P: complete as Q, not as RH."
        ),
        "docs": (
            "docs/RH-PROOF-CHAIN.md",
            "docs/SPECTRAL-FLOOR-EXPLORATION.md",
            "docs/DA-PROOF.md",
        ),
        "team": [
            chair(
                "Riemann",
                "1859 xi and the functional equation",
                "Start from zeta and xi. That is the ground floor.",
                "Completed zeta, xi(s)=xi(1-s), entire of order 1.",
                "The line from xi alone. The functional equation is a symmetry, not RH.",
                "Keep RH lines (1)-(2) as have. Do not load Q into xi.",
                True,
            ),
            chair(
                "Hadamard",
                "1896 prime number theorem / zero-free on Re s = 1",
                "Keep the prime number theorem. No zeros on Re s = 1.",
                "Zero-free region next to the line Re s = 1.",
                "Push that region all the way to Re s = 1/2.",
                "Keep RH line (4). A classical zero-free region is not RH.",
                True,
            ),
            chair(
                "de la Vallee Poussin",
                "1896 prime number theorem, independently",
                "The same PNT. Stay on the edge Re s = 1.",
                "Classical zero-free width. Error term from that width.",
                "RH, or a Q-matrix as a zero-free region.",
                "Keep RH line (4). Unglue inverse-GCD from PNT.",
                True,
            ),
            chair(
                "Hardy",
                "infinitely many zeros on Re s = 1/2",
                "Keep infinitely many zeros on the line.",
                "Moments / mollified xi on the critical line.",
                "Every zero. Infinitely many is not all.",
                "Keep RH line (5) as have. Do not cash it as (6).",
                True,
            ),
            chair(
                "Conrey",
                "positive proportion of zeros on the line",
                "Keep a positive proportion on the line.",
                "Mollifiers. Later work raises the proportion. It is not 1.",
                "Proportion 1. A proportion is not RH.",
                "Keep RH line (5). The WRITE is still every zero.",
                True,
            ),
            chair(
                "Weil",
                "explicit formula",
                "If every zero is on the line, write the explicit formula with all oscillations on Re s = 1/2.",
                "von Mangoldt explicit formula. Consequences after (6).",
                "Force (6) from a GCD matrix. H_N is not a zero.",
                "Keep RH (7)-(8) as follows. They wait on (6).",
                True,
            ),
        ],
        "da_does": (
            "Correct the six errors. Unglue Q from RH. "
            "Keep H_N>=-1 and Theorem P as completed Q. "
            "Emit the RH chain. WRITE (6) does not sit. "
            "Do not revive -3/14 or the full Q floor."
        ),
    },
    "SND": {
        "id": "SND",
        "aliases": ("snd", "conc", "spread", "3-conc"),
        "name": "SND — two regimes, one leftover write",
        "slot": "B",
        "furthest": (
            "August CONC (inf J/X >= c_*) and June SPREAD (rho <= rho0 < 1) "
            "were both called SND. The desk froze 3-CONC / EQ3 / SPREAD. "
            "Bridge* glue is withdrawn. The remaining write is SND-C in SPREAD."
        ),
        "progress": [
            {"id": "SND1", "what": "two names: CONC (sigma>=1/2) and SPREAD (sigma<1/2)", "verdict": "pass"},
            {"id": "SND2", "what": "Bridge* implies SND", "verdict": "fail"},
            {"id": "SND3", "what": "one word SND for both statements", "verdict": "fail"},
            {"id": "SND4", "what": "SIMPLEX / GCD arithmetic on this track", "verdict": "fail"},
            {"id": "SND5", "what": "Phi in front of H on this track", "verdict": "fail"},
            {"id": "SND6", "what": "uniform SND-C in SPREAD (low paraproduct as rho->0)", "verdict": "open"},
            {"id": "SND7", "what": "all-data CONC Ring / geometry bound", "verdict": "open"},
            {"id": "SND8", "what": "two-regime a priori is an all-data bound on X", "verdict": "fail"},
        ],
        "errors_corrected": [
            "One word for opposites.",
            "Bridge* glued to SND.",
            "Phi put in front of H.",
            "SIMPLEX used GCD arithmetic.",
            "Closing SND is not closing X.",
        ],
        "needs": (
            "CONC: an all-data Ring / geometry bound when sigma>=1/2. "
            "SPREAD: uniform energy-class SND-C as rho->0. "
            "X still needs integrable R after that. SND is not X."
        ),
        "need_to_close": [
            "CONC close: all-data stretching bound on sigma>=1/2 (Ring / geometry if).",
            "SPREAD close: uniform low paraproduct |T| as rho->0. That is SND-C.",
            "X close: still int_0^T R < infinity. SND sitting is not that integral.",
        ],
        "completed": (
            "Hygiene complete: two names, Bridge* cut, Phi cut. "
            "SND-C not complete. CONC a priori not complete. X not complete."
        ),
        "docs": ("docs/DA-REPAIR.md", "docs/UNAUGMENTED-R4-VORTICITY-PLAN.md"),
        "team": [
            chair(
                "Einstein",
                "program review: principle before the catalog",
                "Name the object before the list. CONC and SPREAD are two principles, not one brand.",
                "Write the occupation rho=J/X. State the regime. Then the estimate. Do not start from a slogan SND.",
                "Sit here and emit the paraproduct bound. A two-sided couple is not SND-C.",
                "Split the name. Refuse one-symbol SND. The principle is the regime.",
                True,
            ),
            chair(
                "Tesla",
                "program review: a resonator you can detune",
                "Name the knob and the script that must move. If nothing is detunable, it does not sit.",
                "Knob: rho. Script: a bound on the low Bony T as rho->0. Detune rho down. The script must still hold.",
                "Permute knobs or vote the bound. A resonator is not a sweep.",
                "Write the detunable claim: uniform |T| as rho->0, energy class, T^3, no eps. Classify it.",
                True,
            ),
            chair(
                "Constantin",
                "geometric depletion if aligned",
                "On CONC, geometry is an if. Alignment is not automatic from occupation.",
                "CF-if on omega. CONC is a shell hypothesis, not already aligned.",
                "Cash a cover of shells as the CONC close.",
                "Keep CONC geometry as an if. That if is A1 on B, not SND-C.",
                True,
            ),
            chair(
                "Fefferman",
                "alignment if on the classical field",
                "If CONC is to close stretching, write alignment in time for all data.",
                "A1: the if behind hole 1. Not a box reading.",
                "SND as Fefferman A1. Different objects.",
                "Send CONC-close to the A1 write. Do not mix with SPREAD SND-C.",
                True,
            ),
            chair(
                "Tao",
                "regularized cousins / residual honesty",
                "Keep the leftover honest. A two-regime sketch is not an a priori on X.",
                "Name the residual. Do not glue Q or an averaged cousin onto SND.",
                "Bridge* or Q1 as the SND close.",
                "Score SND8 fail. The next write is SND-C or A1, then still R.",
                True,
            ),
        ],
        "da_does": (
            "Keep two names. Cut Phi and Q. "
            "Name the two close-writes (CONC a priori, SPREAD SND-C). "
            "Refuse SND=>X. Einstein splits the principle. Tesla names rho and the script."
        ),
    },
    "H": {
        "id": "H",
        "aliases": ("theorem h", "h-floor", "h_n", "snd-c", "h problem"),
        "name": "H — two objects (fluids SND-C and arithmetic H_N)",
        "slot": "B / Q",
        "furthest": (
            "Fluids: Theorem H = SND-C in SPREAD via Bony T+T*+R. "
            "Arithmetic: lambda_min(H_N)>=-1, proved by pairing. "
            "Both sit as statements. They are not the same H. "
            "Theorem F (super-exponential) is too strong. -3/14 is false."
        ),
        "progress": [
            {"id": "H1", "what": "fluids H named as SND-C in SPREAD (Bony T+T*+R)", "verdict": "pass"},
            {"id": "H2", "what": "arithmetic H_N >= -1 by pairing", "verdict": "pass"},
            {"id": "H3", "what": "two H objects kept unglued", "verdict": "pass"},
            {"id": "H4", "what": "Theorem F: super-exponential dissipation as rho->0", "verdict": "fail"},
            {"id": "H5", "what": "Phi in front of fluids H", "verdict": "fail"},
            {"id": "H6", "what": "H_N >= -3/14", "verdict": "fail"},
            {"id": "H7", "what": "Q > -1/2 for all N", "verdict": "fail"},
            {"id": "H8", "what": "fluids H is the matrix H_N", "verdict": "fail"},
            {"id": "H9", "what": "uniform energy-class low paraproduct as rho->0", "verdict": "open"},
            {"id": "H10", "what": "H_N >= -1/4 (sharp floor)", "verdict": "open"},
        ],
        "errors_corrected": [
            "Theorem F too strong.",
            "Phi-glue on fluids H.",
            "-3/14 revived.",
            "Full Q floor revived.",
            "Fluids H glued to H_N.",
        ],
        "needs": (
            "Fluids: uniform SND-C on T^3, SPREAD, no eps, no Phi. "
            "Arithmetic: H_N>=-1 already sits; H_N>=-1/4 is the remaining floor."
        ),
        "need_to_close": [
            "Fluids H close: uniform |Pi_j*| / low Bony T in SPREAD. Same write as SND-C.",
            "Arithmetic H close: H_N>=-1 already sits. Sharp close is H_N>=-1/4.",
            "Do not close by identifying the two H's.",
        ],
        "completed": (
            "H_N>=-1 complete (Q). Fluids H statement complete; the uniform bound is not. "
            "H_N>=-1/4 not complete. Glue refused."
        ),
        "docs": (
            "docs/DA-REPAIR.md",
            "docs/UNAUGMENTED-R4-VORTICITY-PLAN.md",
            "docs/SPECTRAL-FLOOR-EXPLORATION.md",
        ),
        "team": [
            chair(
                "Einstein",
                "program review: two objects, two principles",
                "Do not call two equations by one letter. Fluids H and H_N are different additions.",
                "Name the field (velocity on T^3) or the matrix (degree-normalized Q-tilde). Then the estimate.",
                "Add the two H's into one close. A couple is two-sided, not a glue.",
                "Keep two slots. Fluids H stays B. H_N stays Q.",
                True,
            ),
            chair(
                "Tesla",
                "program review: name the knob, name the script",
                "Fluids knob: rho. Script: bound on low T as rho->0. Arithmetic knob: N. Script: lambda_min(H_N).",
                "Detune rho; the fluids script must hold. Detune N; the arithmetic script already holds at -1.",
                "Revive -3/14 or run a quantum sweep of N. A false floor is not a resonator.",
                "Write fluids H as the SND-C claim. Keep H_N>=-1. Classify H_N>=-1/4 if you want sharp.",
                True,
            ),
            chair(
                "Bony",
                "paraproduct T + T* + R",
                "State H only as a bound on the low paraproduct in SPREAD.",
                "Energy-class T+T*+R on T^3. No extra dissipation. Many shells need not be small.",
                "Super-exponential F as the theorem. Uniformity is the write.",
                "Delete F as a close. The remaining fluids write is uniform T as rho->0.",
                True,
            ),
            chair(
                "Tao",
                "residual honesty",
                "A named commutator is a claim. It is not X.",
                "Classify SND-C. Do not export it onto classical leftover as done.",
                "H_N as a vorticity bound.",
                "Keep H9 open. Keep H8 fail.",
                True,
            ),
        ],
        "da_does": (
            "Split the two H's. Keep H_N>=-1. Fail -3/14 and Q>-1/2. "
            "Name fluids close as uniform SND-C. Einstein forbids the glue. "
            "Tesla names rho / N and the two scripts."
        ),
    },
}


CLAIMS = [
    rec(
        "D1",
        "take_best",
        "DA can take the best A, furthest RH, SND, and H and name what closes",
        "pass",
        "A catalog, RH chain, SND hygiene, and both H objects are already scored.",
    ),
    rec(
        "D2",
        "dream_team_looks",
        "Field papers and program review say what they would do, how, and what they cannot",
        "pass",
        "Einstein / Tesla name principle and knob on SND and H. "
        "Field papers own the estimates. A review is not a vote.",
    ),
    rec(
        "D3",
        "da_does_legal",
        "DA does the legal corrections and restates the chains that already sit",
        "pass",
        "This-PDE Theorem A. Q floors as Q. Errors fail. Missing WRITE stays open.",
    ),
    rec(
        "D4",
        "team_writes_rh",
        "The dream team completes RH WRITE (every zero on the line)",
        "fail",
        "A council cannot write (6). Hardy and Conrey already sat and are not RH.",
    ),
    rec(
        "D5",
        "team_writes_uniform",
        "The dream team completes A_uniform_H1 or A=>B",
        "fail",
        "Olga already closed this PDE. She cannot pass eps->0. A vote cannot.",
    ),
    rec(
        "D6",
        "a_this_pde_done",
        "The Q1-augmented chain at eps>0 is already complete",
        "pass",
        "That is the close heard a half-dozen times. It stays on A.",
    ),
    rec(
        "D7",
        "q_is_rh",
        "Theorem P or H_N >= -1 is the Riemann hypothesis",
        "fail",
        "Different object. Inverse-GCD is not a zero of zeta.",
    ),
    rec(
        "D8",
        "vote_fills_write",
        "Experts looking at it write the missing line by agreeing",
        "fail",
        "would / how / cannot is a library. A vote is not an estimate.",
    ),
    rec(
        "D9",
        "uniform_later",
        "A_uniform_H1 may sit later",
        "open",
        "A bound or a named no-go. Neither sits. The write stays on A.",
    ),
    rec(
        "D10",
        "rh_write_later",
        "RH WRITE may sit later",
        "open",
        "A zero-free region to 1/2, a positivity certificate, or one new estimate. Not Q.",
    ),
    rec(
        "D11",
        "need_to_close_snd_h",
        "DA can print what has to sit to close SND and H",
        "pass",
        "CONC a priori; SPREAD SND-C; fluids uniform T; H_N>=-1 already sits; H_N>=-1/4 open.",
    ),
    rec(
        "D12",
        "einstein_tesla_write",
        "Einstein and Tesla write SND-C or H_N>=-1/4 by sitting",
        "fail",
        "Program review names the principle and the knob. They cannot output the estimate.",
    ),
    rec(
        "D13",
        "snd_is_x",
        "Closing SND closes X",
        "fail",
        "SND is two-regime hygiene plus SND-C. X still needs integrable R.",
    ),
    rec(
        "D14",
        "glue_two_h",
        "Fluids H and H_N are one close",
        "fail",
        "Different objects. Einstein splits them. Tesla gives each a script.",
    ),
    rec(
        "D15",
        "snd_c_later",
        "Uniform SND-C in SPREAD may sit later",
        "open",
        "Low paraproduct, energy class, rho->0. Tesla's fluids script.",
    ),
    rec(
        "D16",
        "h_quarter_later",
        "H_N >= -1/4 may sit later",
        "open",
        "Numeric through N=200. Pairing does not prove it.",
    ),
]


def parse_jobs(ask: str = "", job: str = "") -> list[str]:
    text = f"{job} {ask}".lower()
    found: list[str] = []
    unaug = bool(re.search(r"\bun[-\s]?augmented\b", text))
    for jid, spec in JOBS.items():
        for alias in spec["aliases"]:
            if jid == "A" and alias == "augmented" and unaug:
                continue
            if re.search(rf"\b{re.escape(alias)}\b", text):
                found.append(jid)
                break
    if unaug and "B" not in found:
        found.insert(0, "B")
    token = (job or "").strip().upper()
    if token in JOBS and token not in found:
        found.insert(0, token)
    if "A" not in found and re.search(
        r"\b(?:job|repair|fix|close|attempt|my|track|analyze)\s+a\b",
        text,
    ):
        found.insert(0, "A")
    if not found and re.search(r"\beinstein\b|\btesla\b", text):
        found = ["SND", "H"]
    if "H" not in found and re.search(
        r"\b(?:job|repair|fix|close|attempt|theorem)\s+h\b|\bh problem\b",
        text,
    ):
        found.append("H")
    return found


def parse_job(ask: str = "", job: str = "") -> str | None:
    found = parse_jobs(ask=ask, job=job)
    return found[0] if found else None


def is_attempt_ask(ask: str) -> bool:
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bdream team\b|\banalyze my\b|\bcomplete the chain\b|"
            r"\brenormali[sz]|\bfurthest\b|\bmy rh\b|"
            r"\bmy (best )?(rh|augmented)\b|"
            r"\bexperts (look|do|say)\b|\bda attempt\b|"
            r"\blook at (my )?(a|rh|augmented|snd|h)\b|"
            r"\bneed to close\b|\bwhat.{0,12}close\b|"
            r"\beinstein\b|\btesla\b|\bclose (snd|h)\b|"
            r"\bns in augmented\b|\bclose .{0,24}augmented\b|"
            r"\bclose (the )?augmented\b|\baugmented please\b|"
            r"\bun[-\s]?augmented\b|\bclose classical\b|"
            r"\bclose (track )?b\b|\bclassical ns\b",
            text,
        )
    )


def run(out: Path | None = None, job: str | None = None, ask: str = "") -> dict:
    picked = parse_jobs(ask=ask, job=job or "")
    jobs = [JOBS[j] for j in picked] if picked else list(JOBS.values())
    payload = {
        "meta": {
            "question": "what has to sit to close A, RH, SND, H; Einstein/Tesla review; legal write",
            "writeup": "docs/DA-ATTEMPT.md",
            "takes_mine": True,
            "uses_dream_team": True,
            "uses_einstein_tesla": True,
            "vote_is_not_a_close": True,
            "a_this_pde_complete": True,
            "a_uniform_not_complete": True,
            "rh_write_not_complete": True,
            "q_is_not_rh": True,
            "snd_is_not_x": True,
        },
        "jobs": jobs,
        "all_jobs": list(JOBS),
        "picked": picked,
        "claims": CLAIMS,
        "counts": {
            "jobs": len(jobs),
            "chairs": sum(len(j["team"]) for j in jobs),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Pick one remaining write: uniform H1, RH (6), CONC a priori, "
            "SND-C, or H_N>=-1/4. Classify it. Einstein names the object. "
            "Tesla names the knob. Neither writes the estimate."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_attempt.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_attempt(out: Path | None = None, job: str | None = None, ask: str = "") -> dict:
    payload = run(out=out, job=job, ask=ask)
    print("ATTEMPT  (what has to sit to close; review looks; legal write)")
    print("Jobs:", ", ".join(payload["all_jobs"]))
    print("Einstein names the object. Tesla names the knob. A vote does not write it.")
    print()
    for spec in payload["jobs"]:
        print(f"JOB {spec['id']}  {spec['name']}")
        print(f"  SLOT    {spec['slot']}")
        print("  NEED TO CLOSE")
        for line in spec.get("need_to_close") or [spec["needs"]]:
            print(f"    {line}")
        if spec.get("do"):
            print("  DO")
            for i, line in enumerate(spec["do"], 1):
                print(f"    {i}. {line}")
        print(f"  FURTHEST {spec['furthest']}")
        print("  PROGRESS")
        for row in spec["progress"]:
            print(f"    [{row['verdict']}] {row['id']}: {row['what']}")
        print("  ERRORS CORRECTED")
        for err in spec["errors_corrected"]:
            print(f"    - {err}")
        print(f"  NEEDS   {spec['needs']}")
        print(f"  DONE    {spec['completed']}")
        print("  DREAM TEAM")
        for c in spec["team"]:
            print(f"    {c['who']}  ({c['paper']})")
            print(f"      WOULD  {c['would']}")
            print(f"      HOW    {c['how']}")
            print(f"      CANNOT {c['cannot']}")
            print(f"      DOES   {c['does']}")
        print(f"  DA DOES {spec['da_does']}")
        print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    ask = " ".join(a for a in sys.argv[1:] if not a.startswith("-"))
    print_attempt(ask=ask, job=ask)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
