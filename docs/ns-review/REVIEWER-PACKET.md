# Reviewer packet — Theorem H extract, August verdict, briefing, mathematical corrections

**For:** independent specialist (fluids / harmonic analysis)  
**From:** Jonathan R. Simons  
**Date:** 15 September 2026 (packet revision after the mathematical audit of the displayed formulas)

Send these four. If only one *status* file is sent besides the extract, send the mathematical corrections with the extract.

| # | Document | Role |
| --- | --- | --- |
| **1** | [`THEOREM-H-STATEMENT-AND-PROOF.md`](./THEOREM-H-STATEMENT-AND-PROOF.md) | Manuscript extract of [SND], (SND-C), Theorem H — **object under review**, not a claimed theorem |
| **2** | [`SND-MATH-CORRECTIONS-2026-09-15.md`](./SND-MATH-CORRECTIONS-2026-09-15.md) | Binding status of the displayed estimate; counterexample; valid \(F_j\) bound; repaired first equation |
| **3** | [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md) | 25 August 2026 adversarial review ([PR #35](https://github.com/simons357/Ship_it_app/pull/35)), plus 15 Sep erratum |
| **4** | [`SND-REVIEWER-REPORT-2026-09-15.md`](./SND-REVIEWER-REPORT-2026-09-15.md) | Body-of-work briefing — [PR #101](https://github.com/simons357/Ship_it_app/pull/101) |

Public KEEP face for citation: [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976). A KEEP label is not verification of every listed lemma.

## Replacement wording (use this)

> In the supplied extract, Theorem H is not established even with \(X\le M\). Its proof drops a viscous tail, uses invalid Sobolev embeddings and does not provide a complete Bony decomposition. The displayed absolute-flux estimate fails on smooth fixed-enstrophy shear fields. A valid \(M\)-dependent bound for the nonlinear shell term can be proved separately, but its usefulness for SND propagation remains to be shown. Any SND floor asserted from time zero must respect the initial spectral distribution. Retain the spectral toolkit and rebuild the required estimate from the exact shell evolution.

## Still agreed

1. Identifying \(X\le M\) was correct and incomplete: the displayed \(|\Pi_{j_*}|\) bound fails **at fixed** \(M\).
2. That gap does **not** mean spectral research should be abandoned.
3. [SND] \(\Leftrightarrow\) Clay remains premature (Theorem D is a sketch).
4. OpenAI 8 Sep forced C/D vs Clay 11 Sep evaluation vs unforced B: as in the briefing §0A. The forced announcement does not prove unforced B.

## One-line lock

Displayed Theorem H is not proved, even under \(X\le M\). Keep the extract as an extract. Keep spectral research; replace the estimate from the exact shell equation.
