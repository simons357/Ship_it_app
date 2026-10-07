# B41 — phase-convention audit for the four \(\pi\)-offset targets

**Date:** 7 October 2026  
**Branch:** `cursor/b41-phase-pi-reconcile-a0eb`  
**Base:** `cursor/tsv-data-aa46` (G3 computed-evidence `data/R2/`)  
**Rerun:** `python3 scripts/b41_phase_convention_audit.py`  
**Payload:** `results/b41/phase_convention_audit.json`

Evidence labels: **Rerun** / **Source-backed** / **Reported** / **Conditional** / **Open**.

---

## Situation

Editorial B41 content (maximization \(\Gamma(t)\); range \(0<t\le\min(C_7,C_8)/c_2\);
weighted asymptotic with \(2-\sqrt3\) equal-weight case) is treated as already in
the note outside this checkout — **not edited here**.

Exact-Certificate conversation (**Reported**):

| Check | Result |
|---|---|
| \(y_A\), \(y_B\), both signed cycle identities, six T2 phase errors vs rationalized JSON | **PASS** |
| All 20 \(\Gamma\) rows vs r2 after column / row / sign alignment | **PASS** |
| Four phase **targets** | **MISMATCH by \(\pi\)**; mode-phase shift cannot remove it under that alignment |
| G6-A via asserted r2 identity | **Blocked** |

Named artifact (bytes **Open** here): `B41-Exact-Certificate-Audit-2026-10-07.zip`.  
In-repo stand-in: `data/R2/` from PR #144 lineage (`COMPUTED_EVIDENCE_ONLY`; hashes in
`PROVENANCE.json`). Library JSON `87745b3c…` remains **Open**.

Sibling draft PR **#169** (`cursor/b41-phase-convention-0cc5`) names the same four
rows. This branch **agrees** on identity and adds exact mod-\(1\) obstruction proofs.

---

## The four \(\pi\) targets (**Rerun**)

Generator recipe (**Source-backed**, JSON `notes` / TSV header):

\[
b=\tfrac{\pi}{2}-\arg(g_{\mathrm{sym}}),\qquad
g_{\mathrm{sym}}=g_{\mathrm{ord}}(p,q)+g_{\mathrm{ord}}(q,p).
\]

| Row | Labels | Triad | G3 turn \(b/(2\pi)\) | Lock turn (audit comparison) | Diff |
|---|---|---|---|---|---|
| 0 | `T3:(+1,-1,+1)` | T3 | \(-1/2\) | \(0\) | \(\pi\) |
| 5 | `T3:(-1,+1,+1)` | T3 | \(-1/2\) | \(0\) | \(\pi\) |
| 10 | `T0:(+1,-1,+1)` | T0 | \(-1/2\) | \(0\) | \(\pi\) |
| 11 | `T0:(+1,-1,-1)` | T0 | \(-1/2\) | \(0\) | \(\pi\) |

Lock reconstruction used for the comparison: **same** turn vector as G3
`b_exact.tsv` except those four entries replaced by \(0\) (**Source-backed** by
the Exact-Certificate “four differ by \(\pi\)” report + the unique half-turn
rows in G3).

Equivalent generator story on those channels only:

\[
\arg(-g_{\mathrm{sym}})=\arg(g_{\mathrm{sym}})+\pi
\;\Rightarrow\;
b\leftarrow b-\pi\equiv b+\pi\pmod{2\pi}.
\]

---

## Exact checks (**Rerun**)

### Identities on disk \(M\)

All six B42 weak-row integer identities hold on `data/R2/M.tsv`.

### Global convention probes

Against the lock reconstruction above:

| Map | Result |
|---|---|
| Conjugation \(\beta\mapsto-\beta\) | **Fails** (many mismatches) |
| Global \(+\pi\) on every target | **Fails** |
| Local \(+\pi\) on rows \(\{0,5,10,11\}\) only | **Matches** all 20 lock turns |

So the offset is **not** a global conjugation / global half-turn convention.
It is a **local** \(g_{\mathrm{sym}}\)-sign (or output-shell orientation) difference
on four channels.

### Mode-phase absorption (the cycle check, exact)

Solve \(M\,\delta y\equiv\Delta\beta\pmod 1\) over \((\mathbb R/\mathbb Z)^{12}\)
with Fraction RREF.

**A — strong-only \(\Delta\beta\) (audit case).**  
\(\Delta\beta=\tfrac12\) turn on rows \(0,5,10,11\); weak \(\Delta\beta=0\).

**Inconsistent** mod \(1\) on weak rows **15, 16, 17, 18** (RHS \(\pm\tfrac12\) on
zero rows of the RREF). **No** mode-phase shift removes the four-target mismatch
when weak targets stay fixed. This is the Exact-Certificate obstruction,
now machine-checked.

**B — identity-consistent extension.**  
Push the same strong \(\Delta\beta\) through `WEAK_IDENTITIES` onto weak rows.
Then \(\Delta\beta\) **is** solvable mod \(1\) (a pure mode-phase gauge).

That gauge is **not** the audit mismatch: the generator writes weak \(b\) from
each channel’s own \(g_{\mathrm{sym}}\), and the certificate audit held weak
targets fixed. Remapping weak turns to force gauge equivalence would change the
T2 residues by hand.

### T2 / certificate posture under a strong-only bridge

If one adds \(\pi\) to the four strong targets and leaves weak targets alone, then
on \(Z_K\) the frozen weak phase errors shift by

| Weak row | Error shift (turns) |
|---|---|
| 14 | \(0\) |
| 15 | \(1/2\) |
| 16 | \(1/2\) |
| 17 | \(1/2\) |
| 18 | \(1/2\) |
| 19 | \(0\) |

So the six T2 upper-bound residues are **not** automatically preserved under a
strong-only target edit. The same certificate vector \(y\) that kills G3 strong
residuals picks up a half-turn residual on those four rows after the edit.

JSON-side \(y_A\), \(y_B\), cycles, and T2 checks remain **Reported PASS** against
the **unmapped** rationalized JSON.

---

## Classification

| Option | Verdict |
|---|---|
| **(a)** Documented/global convention absorbable by a consistent redefinition | **Partial only:** local \(g_{\mathrm{sym}}\) sign on four channels explains the numbers; **not** global; strong-only edit is **not** a symmetry of the capacity functional under fixed \(M\) |
| **(b)** Local inconsistency blocking G6-A transfer | **Yes** for raw r2 identity: strong-only \(\Delta\beta\) is not mode-phase absorbable |
| **(c)** Other | Hybrid label in JSON: `hybrid_a_local_generator_b_blocks_G6A` |

---

## G6-A transfer?

| Route | Result |
|---|---|
| Asserted raw match with r2 / lock | **No** |
| Strong-only local \(+\pi\) bridge without re-proving certificates / T2 | **No** |
| Identity-consistent gauge remapping of weak targets | Not the audit object; **not** claimed as G6-A transfer |
| B41 independent JSON starvation-ray calculation | **Survives** as Reported (certificates PASS on JSON) |
| Evolving Navier–Stokes / classical regularity | **Open** — separate task |

**Secured goal (unchanged):** for this **fixed finite network**, capacity deficit
decreasing proportionally to \(t\) as T2 weights shrink. That is a JSON-side /
starvation-ray claim, **not** a G6-A transfer through r2.

---

## What each check supports

| Check | Supports |
|---|---|
| Identities on \(M\) | Disk \(\Gamma\) is the same integer network used for B42 weak-row algebra |
| Four half-turn rows named | Precise mismatch inventory for G3 vs lock zeros |
| Global maps fail; local \(+\pi\) matches tables | Generator-side \(\mathrm{sign}(g_{\mathrm{sym}})\) story |
| Strong-only insolubility mod \(1\) | Mode-phase cannot equate the two \(\beta\) systems under the audit alignment |
| Weak-error shift table | Strong-only bridge would disturb T2 residues on \(Z_K\) |
| Reported JSON certificate PASS | B41’s independent finite-network calculation is not killed by the mismatch |
| G6-A blocked | Cannot cite r2 identity as a free lunch |

---

## Next engineering step (**Open** until ZIP mirrored)

1. Mirror `B41-Exact-Certificate-Audit-2026-10-07.zip` into the repo.  
2. Re-run its suite with this strong-only obstruction recorded as a named check.  
3. Keep G6-A **untransferred** unless a separate argument shows invariance under
   the actual lock↔JSON map (not assumed here).

---

*No DA stamp. No Clay. No NSE trajectory claim.*
