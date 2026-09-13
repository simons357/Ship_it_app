# Navier–Stokes Brute-Force Extraction Ledger

**Label:** **NOT Lemma★** — Route N / LP-shell / Q6 material. See `docs/math/ARCHIVE_NOT_LEMMA_STAR.md` and `docs/math/ns_attacks/ARCHIVE_ROUTE_N_Q6_SHELL/`. Does **not** establish \(\sup\mathcal R_\star<\infty\).

**Date:** 2026-09-08  
**Branch:** `cursor/tao-snd-h-panel-a0eb`  
**Purpose:** Deduplicate recovered fragments; isolate material that can advance a rigorous classical NS bridge.  
**Labels:** `KEEP` / `REPAIR` / `CONTEXT` / `DROP`  
**Rule:** Truth-only. **NS is not solved.** No Clay / Millennium claim.

Cross-check locked against:
- `docs/math/COOL-CHECK.md`
- `docs/math/TAO-MATH-PANEL-SND-H.md`
- `docs/math/ARCHON-NS-FINAL-REVIEW-PANEL.md`
- `docs/math/CLOSURE-ATTACK-PLAN.md`
- `docs/math/DA-REPORT-2026-08-28.md`
- `docs/math/SPECTRAL-OBJECT-MAP.md` (notation: raw \(Q\) / \(\widetilde Q\) / \(H_N\) / Theorem H / \(B_{M,j}\))
- `docs/papers/submit/02_ring_lemma_snd_conditional.tex`
- `docs/papers/submit/04_q6_inverse_gcd.tex`

**Cool-check lock:** NS is **not** solved. Theorem H ≠ unconditional SND. \(H_N\) ≠ Theorem H.

---

## User content (verbatim)

**Purpose:** Deduplicate recovered fragments; isolate material that can advance a rigorous classical NS bridge.  
**Labels:** KEEP / REPAIR / CONTEXT / DROP

**Current bridge target (Route N):**  
For matrix cutoff \(M\), distinguish \(L(M)\) = number of dyadic shells:

\[
H_M[a]=\sum_{j=0}^{L(M)-1} a_j B_{M,j},\qquad a_j\ge 0,\quad \sum a_j=1.
\]

Candidate bypass via convexity:

\[
\lambda_{\min}(H_M[a])\ge \sum_j a_j\lambda_{\min}(B_{M,j})\ge \min_j\lambda_{\min}(B_{M,j}).
\]

Thus uniform shellwise \(B_{M,j}\succeq(-\tfrac12+\delta)I\) for every \(M,j\) would eliminate dynamic simplex-stability, dominant-shell ratio, and eigenvalue no-crossing for this *auxiliary* operator.

Honest caveat (user already states): this does NOT prove NS regularity; need separate PDE theorem that GCD quadratic form controls vortex-stretching / shell-transfer.

**Batch 001 - Screenshot archive** (status already assigned by user):
- IMG_0816-0818 Chladni/sand — DROP
- IMG_0900-0905 SFE audit checklist — CONTEXT
- IMG_0918-0919 PSD raw GCD also assigned negative eigenvalue — KEEP (operator hygiene)
- IMG_0962-0969 vorticity/LP/Bony/BKM claimed closure — REPAIR
- IMG_0981-0985 energy/enstrophy/BKM overview — CONTEXT
- IMG_5503,5508,5510 hexagonal/torus narrative — DROP

**Batch 002 - Ring Lemma brief** (PDFs named PDF document.pdf etc.):  
Title: A Bound on the Vorticity Direction Field via Finite Triad Geometry on T3.  
Claims: For single LP shell \(S_{j^*}\), \(E_c=\{x:|\omega(x)|\ge c\}\cap\) shell support; claimed \(\|\nabla(\omega/|\omega|)\|_{L^\infty(E_c)}\le C\,2^{j^*}\). Then spread/concentrated dichotomy + Q6 damping → claimed global regularity for threshold class.

---

## Current bridge target — Route N (formal)

### Objects

| Symbol | Meaning (working definition) |
|--------|------------------------------|
| \(M\) | Matrix cutoff / index set \(\{1,\ldots,M\}\) |
| \(L(M)\) | Number of dyadic shells covering \(\{1,\ldots,M\}\) |
| Shell \(j\) | Index block \(I_{M,j}=\{n\le M:\lfloor\log_2 n\rfloor=j\}\) (or \([2^j,2^{j+1})\cap[1,M]\)) |
| \(B_{M,j}\) | Shell-blocked / shell-restricted Hermitian operator on that block (inferred: principal submatrix of \(\widetilde Q_M\) or \(H_M\); see probe assumptions) |
| \(a=(a_j)\) | Probability vector on shells (\(a_j\ge0\), \(\sum a_j=1\)) |
| \(H_M[a]\) | Convex combination \(\sum_j a_j B_{M,j}\) (auxiliary — **not** fluids Theorem H) |

### Candidate inequality

\[
\lambda_{\min}\Bigl(\sum_j a_j B_{M,j}\Bigr)
\ge \sum_j a_j\lambda_{\min}(B_{M,j})
\ge \min_j\lambda_{\min}(B_{M,j}).
\]

### What success would buy (auxiliary only)

If \(\exists\delta>0\) s.t. \(B_{M,j}\succeq(-\tfrac12+\delta)I\) for **all** cutoffs \(M\) and shells \(j\), then for every simplex weight \(a\),

\[
\lambda_{\min}(H_M[a])\ge -\tfrac12+\delta.
\]

That would remove the need for **dynamic** simplex-stability, dominant-shell ratio tracking, and eigenvalue no-crossing arguments **for this auxiliary convex combination**. It would **not** prove Navier–Stokes regularity.

### Honest caveat (locked)

A separate PDE theorem is required: that the GCD / inverse-GCD quadratic form controls vortex-stretching or shell-transfer for Leray–Hopf solutions. **No such map is proved** (`04_q6_inverse_gcd.tex`, Tao panel Q4, Cool-check).

---

## Batch 001 — Screenshot archive (disposition confirmed)

| IDs | Content | Label | DA note |
|-----|---------|-------|---------|
| IMG_0816–0818 | Chladni / sand patterns | **DROP** | Metaphor only; no NS bridge content |
| IMG_0900–0905 | SFE audit checklist | **CONTEXT** | Operator / spell hygiene; keep near SFE-BH spellbook |
| IMG_0918–0919 | PSD / raw GCD negative eigenvalue | **KEEP** | Operator hygiene — aligns with Prop. “full-spectrum Bridge false” in `04_q6` |
| IMG_0962–0969 | Vorticity / LP / Bony / BKM “closure” | **REPAIR** | Overclaim packaging; salvage LP/BKM language only as conditional toolkit |
| IMG_0981–0985 | Energy / enstrophy / BKM overview | **CONTEXT** | Standard fluids background |
| IMG_5503, 5508, 5510 | Hexagonal / torus narrative | **DROP** | Narrative / speculative geometry |

**Images on disk:** not present in this workspace (screenshot archive not uploaded). Labels above follow the user’s assignment.

---

## Batch 002 — Ring Lemma brief (disposition)

**Source title (user extract):** *A Bound on the Vorticity Direction Field via Finite Triad Geometry on \(\mathbb{T}^3\).*

**PDF hunt:** No files named `PDF document.pdf` (or Batch-002 uploads) found under `/workspace`, `/home/ubuntu`, or common upload paths. Closest in-repo analogs:
- `docs/papers/submit/02_ring_lemma_snd_conditional.tex` (+ PDF)
- `docs/papers/SND_RING_LEMMA_NS.tex`
- Zenodo spectral `20405585/RingLemma_Borromean_Simons.tex`

**Claim split:**

| Claim fragment | Label | Cross-check |
|----------------|-------|-------------|
| Single LP shell \(S_{j^*}\); \(E_c=\{|\omega|\ge c\}\cap\) shell support; \(\|\nabla(\omega/|\omega|)\|_{L^\infty(E_c)}\le C\,2^{j^*}\) | **KEEP / REPAIR** as toolkit | Matches Ring Lemma in submit `02` (proof sketch via Bernstein). Constantin panel: band-limited only — not global CF |
| Spread / concentrated dichotomy under SND → conditional \(H^1\) control | **CONTEXT / REPAIR** | Submit `02` Theorem is explicitly **conditional on SND**; Cool-check: unconditional SND open |
| Q6 damping → claimed global regularity for a threshold class | **DROP / KILL** | Cool-check + `04_q6`: no NS map from inverse-GCD; ARCHON rejects Statement (B) packaging |

**Verdict on Batch 002 packaging:** Keep the band-limited direction bound as a geometric lemma candidate; kill any “Q6 ⇒ global regularity” wrap.

---

## DA analysis — Route N

### 1. Is convexity \(\lambda_{\min}(\sum a_j B_j)\ge\sum a_j\lambda_{\min}(B_j)\) true?

**Yes**, for a convex combination of Hermitian matrices of equal size (or after isometric embedding into a common space).

**Reason:** \(\lambda_{\min}(A)=\min_{\|x\|=1}x^*Ax\) is concave in the Hermitian argument (pointwise minimum of linear functionals). Equivalently, by Rayleigh / Courant–Fischer,

\[
x^*\Bigl(\sum_j a_j B_j\Bigr)x=\sum_j a_j\,x^*B_j x\ge\sum_j a_j\lambda_{\min}(B_j)
\]

for every unit \(x\), hence \(\lambda_{\min}(\sum a_j B_j)\ge\sum a_j\lambda_{\min}(B_j)\).

**Caveat on block form:** If \(B_{M,j}\) live on *different* subspaces (true principal submatrices of unequal size), the sum \(\sum a_j B_{M,j}\) is only well-defined after embedding each block into a common ambient matrix (zero-pad / direct-sum / shell-diagonal lift). Convexity still applies to the lifted Hermitian family; the inequality does **not** magically compare eigenvalues across incompatible dimensions without a lift.

### 2. Does this eliminate SND / simplex dynamics for auxiliary \(H_M[a]\)?

**Only if** a **uniform shellwise floor** holds:

\[
\inf_{M,j}\lambda_{\min}(B_{M,j})\ge -\tfrac12+\delta.
\]

If that floor is true, then every convex combination automatically clears \(-\tfrac12+\delta\), so dynamic tracking of \(a(t)\), dominant-shell ratio, and eigenvalue no-crossing become unnecessary **for the auxiliary operator**.

If the floor fails for some shell, convexity only recovers the (bad) minimum — it does not improve it.

### 3. Is uniform \(B_{M,j}\succeq(-\tfrac12+\delta)I\) known / false / open?

| Object | Full-spectrum \(\lambda_{\min}>-1/2\) | Shellwise status (principal submatrices) |
|--------|----------------------------------------|------------------------------------------|
| \(\widetilde Q_M\) | **FALSE** (`04_q6` Prop.; `bridge_floor_verify.py`) | **Clears \(-1/2\) in probe** through \(M=256\) (worst shell \(\approx-0.234\) at \(j=1\)); **LEAD — not a theorem** |
| Raw \(Q_M=1/\gcd\) | **FALSE** (deeply negative) | Not the Route N primary target; full spectrum kills Bridge |
| Degree-normalized \(H_M\) | \(\lambda_{\min}>-1/2\) in checked ranges; \(-3/14\) universal **killed** | **Clears \(-1/2\) in probe** through \(M=256\); **LEAD — not a theorem** |

**Why shellwise can beat full-spectrum:** bad full-matrix eigenvectors of \(\widetilde Q\) are typically **delocalized across shells**. A principal submatrix on one shell need not inherit the global \(\lambda_{\min}\) (Cauchy interlacing goes the other way for extrema of the *full* matrix vs blocks — the block floor can sit strictly above the full \(\lambda_{\min}\)). So Route N is a **genuinely different** claim from the killed full-spectrum Bridge.

**Inference used for \(B_{M,j}\):** Absent an uploaded Batch-002 matrix definition, DA treats \(B_{M,j}\) as the **principal submatrix** of \(\widetilde Q_M\) (and separately of \(H_M\)) on dyadic index shells. If the user’s \(B_{M,j}\) is a different embedding (shell-diagonal lift of the full operator, fluids commutator, etc.), the probe does not apply — mark definition **OPEN**.

**Numeric probe (2026-09-08):** `scripts/route_n_shell_floor_probe.py`

| \(M\) | \(\lambda_{\min}(\widetilde Q)\) | \(\min_j\lambda_{\min}(B^{\widetilde Q}_{M,j})\) | \(\lambda_{\min}(H)\) | \(\min_j\lambda_{\min}(B^{H}_{M,j})\) |
|------|----------------------------------|--------------------------------------------------|----------------------|----------------------------------------|
| 32 | \(-0.575\) | \(-0.234\) | \(-0.206\) | \(-0.085\) |
| 128 | \(-0.779\) | \(-0.234\) | \(-0.209\) | \(-0.068\) |
| 256 | \(-0.882\) | \(-0.234\) | \(-0.211\) | \(-0.065\) |

### 4. PDE bridge stress test

Even a proved uniform shellwise arithmetic floor would **not** solve NS:

1. Cool-check / Tao panel: unconditional SND for large data is open; Theorem H ≠ unconditional SND.  
2. \(H_N\) / \(\widetilde Q\) ≠ fluids Theorem H — wrong object without a map.  
3. ARCHON: Statement (B) / Clay packaging rejected.  
4. User caveat: need a theorem that the GCD form controls vortex-stretching / shell-transfer — **missing**.

**Explicit:** **Navier–Stokes is not solved. No Millennium claim.**

---

## Cross-check summary (locked docs)

| Locked claim | Route N implication |
|--------------|---------------------|
| Full-spectrum \(\lambda_{\min}(\widetilde Q)>-1/2\) false | Shellwise principal-block floor is a **different** claim (interlacing: \(\lambda_{\min}(B_j)\ge\lambda_{\min}(\widetilde Q)\)); probe clears \(-1/2\) — still needs a theorem |
| Bridge\* pair / multi-rep proved | Restricted Rayleigh on special vectors ≠ shell-block \(\lambda_{\min}\) |
| Ring Lemma band-limited KEEP as toolkit | Batch 002 direction bound aligns; regularity packaging does not |
| SND unconditional HARD | Route N does not close SND |
| No NS map from Q6 | Route N auxiliary success ≠ PDE success |

---

## Disposition board (working)

| Item | Label | Next action |
|------|-------|-------------|
| Route N convexity inequality | **KEEP** (true for Hermitian convex combos) | Use as lemma; do not overclaim |
| Uniform shellwise \(\widetilde Q\) / \(H\) floor (principal blocks) | **LEAD** (clears \(-1/2\) through \(M=256\)) | Lock \(B_{M,j}\) definition; prove or find counterexample at large \(M\) |
| Dynamic simplex / no-crossing bypass | **CONTEXT** | Only relevant *if* shellwise floor holds uniformly |
| PDE bridge (GCD → vortex stretch) | **HARD** | New analysis; not packaging |
| Batch 001 KEEP hygiene | **KEEP** | Cite next to `04_q6` false-floor prop |
| Batch 001 REPAIR BKM closure | **REPAIR** | Strip unconditional language |
| Batch 002 Ring bound | **KEEP/REPAIR** | Align with submit `02` |
| Batch 002 Q6→global regularity | **DROP/KILL** | Cool-check |

---

## Reproduce

```bash
python3 scripts/route_n_shell_floor_probe.py 256
python3 scripts/bridge_floor_verify.py 50
```
