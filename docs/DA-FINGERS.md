# Five-finger DA on one line

`python3 scripts/da_machine.py fingers`

You asked DA to do the five-finger move on **one line**, then
do it again on each piece, and keep going. The line is the
realization score, not a unifier and not the Cosmo export.

\[
R=\exp(-\tfrac12\chi^2_{\mathrm{ext}})\,\exp(-\tfrac12\chi^2_{\mathrm{int}})
\]

A finger is a piece of that line plus a fail-able check.
Five at the top. Five on each of those. On the two leftovers
that move the default score, five again on the residual
\((x-x_\star)^2\). Then the same hand is used as five
**general categories** for the 16 candidates
(gauge / gravity-gauge / topological / harmonic / teleological).

## The first hand

| Finger | Piece | Verdict |
|---|---|---|
| 1 | \(R\) (the 16th, the product) | open — output, not a knob |
| 2 | \(\exp(-\frac12\cdot)\) | pass — shape does what it says |
| 3 | \(\chi^2_{\mathrm{ext}}\) | open — must-hits live here |
| 4 | \(\chi^2_{\mathrm{int}}\) | open — \(S_c\) and \(\delta\) move \(R\) |
| 5 | implied \(F\) (not written on the line) | **fail** — nothing here produces the couplings |

Product identity: \(\max|R-R_{\mathrm{ext}}R_{\mathrm{int}}|=0\).
\(\mathrm{corr}(R_{\mathrm{ext}},R_{\mathrm{int}})=-0.05\).
Target \(R=1\) only because we sat on the anchors.
Locking \(R\) to produce \(R\) is circular (**fail**).

## Recurse \(\chi^2_{\mathrm{ext}}\)

Five fingers: EM, strong, weak (mixing + \(m_W\)), Planck, vacuum.

Default mean contribution \(\mathbb{E}[\frac12(x-x_\star)^2]\):

| Term | default | equal \(\sigma=0.15\) |
|---|---:|---:|
| vacuum | 2.015 | 0.012 |
| Planck | 1.165 | 0.011 |
| EM / strong / weak | \(\sim 0.012\) | \(\sim 0.011\) |

**Width is a fail.** Vacuum and Planck dominate the default
score because we gave them room (\(\sigma=2.0\) and \(1.5\)),
not because the algebra singles them out. Equal width flattens
every external term.

That does **not** let you drop them from nature. “Must-hit
leftover” and “dominates this score” are different claims.
The first stays. The second was a sampling choice.

Each leftover then splits as \(x\), \(x_\star\), minus, square,
width. \(x_\star\) is a number we put in, not a prediction.
\(x\) is not derived from the other knobs on this vector.

## Recurse \(\chi^2_{\mathrm{int}}\)

| Finger | contrib | Fate |
|---|---:|---|
| \(S_c\) | 0.622 | score-mover |
| \(\delta\) | 0.359 | score-mover |
| \(\lvert\nabla C\rvert\) | 0.239 | near-miss |
| \(\kappa\) | 0.129 | decorative |
| \(A,f,\varphi\) | 0.106 | **fail** as a producer |

## Recurse implied \(F\)

Domain (names missing), codomain (four couplings), dimension
(\(n>k\), the possibility clue), affine construction
(**fail**, holdout \(0.073\) vs null \(0.072\)), rebuild
(blocked).

Per-candidate fate (same five questions on each of the 16,
then the next smaller pieces) is
[`docs/DA-SIXTEEN-FATE.md`](DA-SIXTEEN-FATE.md).

## The 16, as candidate types

Same five fingers, now as **categories** for a unification
candidate. Each of the 16 gets one category and a general
fate, then that category is broken again.

| # | Name | Category | Fate |
|---|---|---|---|
| 1–4, 7 | couplings + QCD scale | gauge | must-hit, decorative on this score |
| 5 | Planck | gravity-gauge | must-hit **and** default score |
| 6 | vacuum | gravity-gauge | must-hit **and** default score; topological fork left **open** |
| 8 | \(\theta_{\mathrm{QCD}}\) | **topological** | leftover; not a local coupling |
| 9–11 | \(A,f,\varphi\) | harmonic | decorative |
| 12 | \(\delta\) | harmonic | score |
| 13 | \(S_c\) | teleological | score |
| 14 | \(\kappa\) | teleological | decorative |
| 15 | \(\lvert\nabla C\rvert\) | teleological | near-miss |
| 16 | \(R\) | teleological | **output** |

**Topological versus gauge:** on this list only
\(\theta_{\mathrm{QCD}}\) is topological (a global angle).
The four couplings are local gauge. Vacuum *can* be read as
topological (a different book). This score treats it as a
scale leftover. That fork stays open. Do not glue \(\theta\)
to \(\alpha_s\).

Gauge as a category: you cannot drop a coupling and still
mean the four forces (**fail** to drop). Oscillators do not
write the couplings (**fail**). Gravity-gauge as a category:
equal-width flattens the leftover ranking (**fail** as
“structurally special”), must-hit stays. Harmonic as a
producer: **fail**. Teleological \(R\) as a candidate theory:
**fail** (circular).

## How far

1. The line breaks. The pieces break. The leftover residuals
   break. The 16 each get a general fate.
2. Algebra of the score is clean. Implied \(F\) is not.
3. Default vacuum/Planck dominance is a width artifact.
4. \(\theta_{\mathrm{QCD}}\) is the topological leftover;
   vacuum is a fork, not a decision.
5. **Blocked** on Cosmo names or a real producing-map.

How a program can say “possible” and emit a finite \(X\)
without having \(F\) is [`docs/DA-HOW-IT-KNEW.md`](DA-HOW-IT-KNEW.md).
The hand is not capped at five.

If the export shows up, keep this recursion and this
category table. Replace the names. Re-run the checks.
Do not call this \(F\).
