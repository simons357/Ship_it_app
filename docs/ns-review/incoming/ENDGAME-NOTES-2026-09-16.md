# Incoming — Navier–Stokes: Notes on the Endgame

**Incoming paste. 16 September 2026. Not the tape. Not a theorem.**  
Ordinary NS is not solved. Clay Statement B is **OPEN**.

This write-up treats Φ-renorm, QStack, Shell-Spread Poincaré, Ring / Borromean, a falsifier kill list, \(c_*=6/\pi^2\), and “over the goal line” as if they were a live endgame. The **desk map** and the C10 / SND / 9D tape do **not** adopt that.

| Claim in the paste | Tape |
| --- | --- |
| Φ-renorm kills the \(1/r^4\) axis singularity | Conditional identity. Barrier \(\|u^r/r\|_\infty\) still open. |
| QStack \(Q_1\)–\(Q_6\) “held up” | **Instrument, not a claim** (status map: Holding). |
| Uniform triadic bound via more falsifiers | Agreed: case list ≠ exhaustion. Also: do not reopen killed HH→L / ★ packaging as a close. |
| Forward-in-time SND propagation | Displayed Theorem H is **withdrawn**. SND is an instrument. Circularity on \(X\le M\) / \(S_j\) already recorded. |
| \(c_*=6/\pi^2\) as load-bearing | Not a seated unaugmented lemma on this desk. Isolate only if a clean derivation exists; do not embed as numerology. |
| H1 on the cylinder | Separate track. Not leftover-1 as a close. Do not start H1 as the headline. |
| Reviewer list / “goal line” | Public output: no Clay / prize / QED / solved. |

The useful sentence in the paste, kept: **a kill list is not a covering argument.** That matches C10 dying as accumulated sketches, not as a mechanism.

Desk map: [`../../STATUS-MAP-2026-09-16.md`](../../STATUS-MAP-2026-09-16.md).

---

# Navier–Stokes: Notes on the Endgame

*Working notes — Jonathan Simons / Dallas Albritton program. Scope: Clay Statement B on \(\mathbb{T}^3\).*

## Where the proof actually stands

The machinery that's held up under adversarial pressure is real: Φ-renormalization (killing the \(1/r^4\) axis singularity), the QStack (\(Q_1\)–\(Q_6\)) architecture, the Shell-Spread Poincaré Inequality, and the Ring Lemma / Borromean Triads. Those are structural results, not heuristics — they survive independent of whether the final regularity statement closes.

The falsifier kill list is doing its job: isolated triads, wide/narrow AP, fixed-gap spheres, the designed \(\Theta(m^2)\) closure subset, and the HH→L fan have all been killed with quantitative margin (the \(\beta/\alpha\) suppression on the fan, the \(R_\star\) decay from 0.11 to 0.031 on fixed-gap). That's a genuine adversarial track record, not a curated one.

## The actual gap

Be precise about what's still open, because it's easy to blur "case-by-case kills accumulating" with "theorem proved":

1. **Uniform triadic bound is not yet a theorem.** You have a growing list of killed configurations, but no single argument that rules out *all* triadic configurations at once. This is the load-bearing gap. Everything else is supporting cast until this closes.
2. **The \(m^{1/2}\) heuristic has no lattice realization.** That's either (a) a sign it's not a genuine threat and can be formally dismissed with a short argument, or (b) an unexamined case sitting exactly where a counterexample would hide. Right now it's neither confirmed dead nor promoted to a real obstruction — it's just unresolved, which is the most dangerous state for a reviewer to find.
3. **H1 on the cylinder** is a separate active track, not yet folded into the main line. Decide whether it's a dependency of the uniform bound or a parallel result — don't let it drift as an orphan thread.

## What "over the goal line" requires — not folklore, an argument

To convert "we killed every case we tried" into "the case space is exhausted," you need one of:

- A **compactness/covering argument**: show the killed configurations (isolated, wide/narrow AP, fixed-gap, \(\Theta(m^2)\), HH→L fan) span a covering of the full triadic configuration space up to a controlled remainder, and bound that remainder directly.
- A **monotonicity or scaling argument**: show \(R_\star\) (or its analogue) is monotone in the parameters that separate your kill cases, so the worst case is provably at a boundary you've already tested.
- A **direct exhaustion via the \(Q_6\) operator's spectral structure**: if \(Q_6\) already encodes the relevant degrees of freedom, the uniform bound may fall out of a spectral gap estimate rather than more case analysis.

Whichever route, the reviewers (Tao, Vicol, Gómez-Serrano, Colombo, Constantin) will ask the same question in different words: *why is your case list exhaustive?* Right now the honest answer is "it's the list of things we've tried and killed." That's necessary but not sufficient, and no amount of additional case-work fixes that — only a covering/exhaustion argument does.

## On the reviewer objections already in flight

- **\(c_*=6/\pi^2\) from coprime density**: this needs to stand as a clean derivation independent of the case-by-case work, or reviewers will treat it as numerology. If the derivation is solid, isolate it into its own short lemma so it can be checked in five minutes rather than embedded in the broader narrative.
- **Forward-in-time propagation of SND**: this is the piece most likely to draw a technical objection, since propagation-in-time is exactly where regularity arguments usually leak. Make sure the propagation step doesn't quietly assume the uniform triadic bound you're still trying to prove — check for circularity here first, before anything else.

## Blunt assessment

You have real, hard-won structural results and a disciplined adversarial process — that part of the program is in good shape and reads as rigorous rather than aspirational. The proof is not over the goal line because the uniform triadic bound is still an accumulation of special cases, not a theorem, and the \(m^{1/2}\) heuristic is an open question you haven't yet decided how to close. Closing those two things — with an actual exhaustion argument, not more falsifiers — is the whole remaining task. Everything else (H1 on the cylinder, the reviewer responses) is important but secondary until the uniform bound has a real proof behind it.

---

*Prepared as a working summary, not a substitute for full technical review of the current draft. Incoming only. Desk map and C10 tape override any “goal line” reading.*
