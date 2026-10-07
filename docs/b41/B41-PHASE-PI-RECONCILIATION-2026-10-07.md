# B41 — reconcile four \(\pi\)-offset phase targets

**Date:** 7 October 2026  
**Branch:** `cursor/b41-phase-convention-0cc5`  
**Rerun:** `scripts/b41_phase_pi_reconcile.py` → `results/b41/phase_pi_reconciliation.json`

---

## Audit posture (inputs)

From the Exact-Certificate conversation (source-backed there; ZIP
`B41-Exact-Certificate-Audit-2026-10-07.zip`):

| Check | Result |
|---|---|
| \(y_A\), \(y_B\), both cycle identities, six T2 phase errors | **PASS** vs rationalized JSON |
| 20 \(\Gamma\) rows vs r2 after column/row/sign alignment | **PASS** |
| Four phase **targets** vs r2 | **MISMATCH by \(\pi\)** |
| G6-A via asserted r2 identity | **Blocked** |

This note attacks **only** the four-target mismatch.

---

## The four rows (G3 transcription in `data/R2/`)

| Row | Labels | G3 \(b/(2\pi)\) | Lock-style strong zero | Diff |
|---|---|---|---|---|
| 0 | `T3:(+1,-1,+1)` | \(-1/2\) | \(0\) | \(\pi\) |
| 5 | `T3:(-1,+1,+1)` | \(-1/2\) | \(0\) | \(\pi\) |
| 10 | `T0:(+1,-1,+1)` | \(-1/2\) | \(0\) | \(\pi\) |
| 11 | `T0:(+1,-1,-1)` | \(-1/2\) | \(0\) | \(\pi\) |

All other G3 turn fractions are **not** exact half-turn flips relative to \(0\); the certificate audit’s “four differ by \(\pi\)” matches **exactly** this set when the r2 lock stores \(0\) on those rows.

Generator recipe (JSON notes / TSV header): \(b=\pi/2-\arg(g_{\mathrm{sym}})\).  
At \(b=-\pi\), one has \(\arg(g_{\mathrm{sym}})=\pi/2-(-\pi)=3\pi/2\) (mod \(2\pi\)).

---

## Convention map (hypothesis — confirmed arithmetically)

**Map:** on these four rows only, replace the G3 target by
\[
b_{\mathrm{lock}} \equiv b_{\mathrm{G3}}+\pi \pmod{2\pi}
\]
i.e. add \(1/2\) turn: \(-1/2\mapsto 0\).

**Equivalent generator story:** flip the sign of \(g_{\mathrm{sym}}\) on those
four channels before applying \(b=\pi/2-\arg(g_{\mathrm{sym}})\), because
\[
\arg(-z)=\arg(z)+\pi \pmod{2\pi}
\quad\Rightarrow\quad
\tfrac{\pi}{2}-\arg(-z)=\tfrac{\pi}{2}-\arg(z)-\pi.
\]

**Cycle check (as reported in the Exact-Certificate note):** a pure
mode-phase shift on the certificate vector **cannot** remove this
difference under the aligned \(\Gamma\) — confirmed conceptually: a global
mode phase adds \(M y\) with the same \(M\); these four rows already have
nonzero support patterns, and the mismatch is in the **target** \(\beta\),
not in a free \(y\) that zeros all residuals simultaneously without the map.

---

## What this does / does not buy

### Does
- Names the four channels and the exact half-turn discrepancy.
- Gives an explicit, local convention bridge G3 generator → lock zeros on those rows.
- Leaves B41’s **internal** rationalized-JSON certificates untouched (still PASS as reported).
- Keeps weak-row integer identities on disk \(M\) (**PASS** here).

### Does **not**
- Automatically transfer **G6-A** to the G3 object. You must cite the bridge;
  “raw identity with r2” remains false.
- Make all strong-row residuals vanish at \(y_A=0\) under raw G3 targets —
  only these four were half-turn flips; other strong rows carry other
  nonzero G3 targets by design of the generator.
- Certify evolving NSE / classical regularity.
- Replace the need for the Exact-Certificate ZIP contents if a bot
  lacks Library access — re-run that suite when the ZIP is mirrored.

---

## Decision

| Question | Answer |
|---|---|
| Are the four \(\pi\) offsets identified? | **Yes** — rows 0, 5, 10, 11 |
| Is there a clean generator-side explanation? | **Yes** — \(g_{\mathrm{sym}}\mapsto -g_{\mathrm{sym}}\) on those channels (or \(+\pi\) on \(b\)) |
| May we assert G6-A via r2 match? | **No** — only via an **explicit convention bridge** |
| Starvation-ray on the fixed finite network | Still the secured *goal*; JSON-side certificates remain the supporting PASS set |
| Next engineering step | Mirror `B41-Exact-Certificate-Audit-2026-10-07.zip` into the repo; re-run its suite with this map recorded as a named option |

---

*No DA stamp. No NS close.*
