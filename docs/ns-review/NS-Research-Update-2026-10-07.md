# NS Research Update — 7 October 2026

**Author / desk:** Jonathan R. Simons  
**Purpose:** Handoff for phone Grok and discrete Grok bots  
**Instruction to bots:** Read this as working context. Preserve the distinction between **reported results**, **rerun computations**, **scoped analytic results**, and **open problems**. Do not claim to have run or verified anything you have not. After reading, summarize what you understand, list which source files you can actually access, and state the next concrete calculation you can perform.

---

## 0. Current priority (read this first)

**Primary:** Independently review the exact **32-shape shared-budget** argument, then investigate extending it to omitted interaction families **without uncontrolled repeated dissipation charges**.

**Reported elsewhere:** the previously missing ZIP `Shared-Budget-17-Family-Audit-and-9-25-Extension.zip` has been recovered and its finite verification script passes.  
**In this cloud workspace (checked 7 Oct):** filing lives on branch `cursor/shared-budget-32-shape-c3ed` (cover note, extension desk, constants face-check, phase probe). The packets folder currently contains the cover-note **README only** — full author ZIP body (exact shape list + enumeration script) must still be confirmed present before a bot claims a full independent audit.

**Secondary tracks (keep separate — do not merge currencies):**
1. Exact-shell / shared-budget geometry (17→32)  
2. Axisymmetric swirl signed compression (Shahmurov four doors)  
3. Diffuse-cascade numerical diagnostics (AET / \(P_j\))  
4. Ring Lemma spatial hardware (done, scoped)  
5. Main unaugmented live gate (\(T_{j\leftarrow j}\), \(\alpha_+\), product / \(\mathcal{R}_\star\))

**Still open globally:** full all-scalene budget (criterion **(17)**), classical regularity / Clay. **NS not solved.**

---

## 1. How to read every claim in this file

| Label | Meaning |
|---|---|
| **REPORTED** | Stated in a draft, screenshot, or other-agent note; not recomputed here |
| **RERUN** | Independently recomputed in a named script/session |
| **SCOPED ANALYTIC** | Proved or filed at an explicitly limited mathematical scope |
| **OPEN** | Not established |

Never promote REPORTED → SCOPED ANALYTIC without a check.

---

## 2. What we have been doing (≈ last 1–2 weeks)

### Track A — Shared-budget 17 → 32 (exact-shell geometry)

| Item | Status |
|---|---|
| Original 17-family shared energy budget | **SCOPED ANALYTIC (filed):** proved at stated scope, including high-pass conclusion that family’s positive excess is identically zero — *per cover note / author package audit verdict* |
| Controlled extension via anchor \((9,25)\) | **SCOPED ANALYTIC (filed):** 17 + 15 nonzero shapes → **32** shapes |
| Combined weighted charge | \(\rho+3\rho'\approx 3.1077752815\) (\(\rho\approx0.6318550824\), \(\rho'\approx0.8253067330\)) — **RERUN face-check** of decimal assembly on `shared_budget_32_shape_constants.py` |
| Max shell-charge multiplicity (nonzero transfer) | **Exactly 4** (filed) |
| High-pass cutoff for enlarged family | \(K=\max\{2,\,3(M-1)\}\) |
| Geometric lemmas | constant-3 fixed-shell remains valid under hypotheses; constant-2 sharpens distinct-donor; factors \(\sqrt3\), \(\sqrt2\) |
| Criterion **(17)** / arbitrary families / Clay | **OPEN / not claimed** |
| Phase experiments | **REPORTED + probe numerics:** tested configs can reinforce; coherent shared-mode ratio can hit **1.0** — does **not** settle exact 32-family or show geometric bound saturated; does **not** license “phases cancel in the worst case” |
| Next question on this track | Does combined transfer stay within the proposed budget, and under what cutoff/amplitude can viscosity absorb it? Then: enlarge to omitted families **without double-spending dissipation** |

**Key sources (branch `cursor/shared-budget-32-shape-c3ed`):**
- `docs/COVER-NOTE-17-FAMILY-32-SHAPE-REVIEW-2026-10-06.md`
- `docs/SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md`
- `docs/PHASE-CANCELLATION-EXPLORATION-2026-10-06.md`
- `packets/Shared-Budget-17-Family-Audit-and-9-25-Extension/README.md`
- `scripts/ns_attacks/shared_budget_32_shape_constants.py`
- Author ZIP name: `Shared-Budget-17-Family-Audit-and-9-25-Extension.zip`

### Track B — Axisymmetric swirl / four doors (6–7 Oct)

Separate Shahmurov-axisymmetric analysis — **not** the 32-shape package.

Plain-English feedback loop:
1. Swirl generates meridional (radial/vertical) motion  
2. That can squeeze swirl inward  
3. Inward squeeze can strengthen swirl (\(Q=\int F^4\,dx\))  
4. Viscosity opposes concentration  

**Two distinctions (locked):**
- Small energy + bounded initial gradients do **not** make the swirl budget uniformly small (Gaussian family).  
- Viscosity cannot absorb every instantaneous compression alone (amplitude scaling \(C_F\sim M^5\), \(D_F\sim M^4\)).

**Proposed next inequality (OPEN — work target on swirl branch):**
\[
C_F(t)\le\eta\nu D_F(t)+B(t)Q(t),\quad 0\le\eta<1,
\]
with \(\int_{t_0}^T B\) bounded from **already controlled same-solution data**. Defining \(B\) from the same uncontrolled compression accomplishes nothing.

Four Shahmurov doors: meridional Type-II, signed compression, noncompact high frequency, boundary entry — **none closed**.

**RERUN here (7 Oct):** Gaussian \(E,Q\) integrals; axis \(\partial_t U\) sign root; \(m_0,c_0\); pure-absorption kill — `scripts/ns_attacks/da_swirl_four_doors_verify.py`.  
**Not run:** full NSE PDE of the family; full line-by-line certification of every §7 closeness estimate.

**Sources:** `docs/ns-review/DA-SWIRL-FOUR-DOORS-2026-10-06.md`, `DA-SWIRL-NEXT-TARGET.md`, PR #167 (`cursor/da-swirl-four-doors-0cc5`).  
Grounding paper: Shahmurov, arXiv:2605.09797v3 (HTML retrieved).

### Track C — Ring Lemma (spatial hardware)

**SCOPED ANALYTIC:** Oct 2 corrected geometric note — band-limited vorticity direction bounds on strong/peak sets (\(L^{5/2}\) sharp; linear under amplitude control).  
**Not:** NS evolution, product-block close, Clay.  
Visual pack + mechanism cards on PR #164 (`cursor/ring-lemma-hardware-visuals-0cc5`). PDF on PR #163.

### Track D — Diffuse cascade / triad equidistribution (numerical draft)

**REPORTED** draft `NS_PAPER_v1` / Zenodo title *Diffuse Cascade in 3D Navier–Stokes…* (doi `10.5281/zenodo.20183673` in inventory; files not pulled here).

| Resolution | Danger events | max \(\alpha(t)\) | min AET\((t)\) |
|---|---|---|---|
| \(N=32\) | 0 | 0.187 | 0.316 |
| \(N=64\) | 0 | 0.061 | 0.319 |
| \(N=128\) | 0 | 0.066 | 0.308 |

Danger event thresholds (as stated): AET\(_j<0.05\), top-1% mass \(>30\%\), \(\alpha(t)>1\).

**Screenshot (one run only — REPORTED):**
| Setting | Value |
|---|---|
| Resolution | \(N=32\) |
| Viscosity | \(\nu=0.02\) |
| Duration | \(T=2.0\) |
| Snapshots | 51 |
| Q operators | None |
| Participation | \(P_j\approx138.7\) (or 146.8 in one column) with \(N_j=224\); ratio \(\approx0.655\)–\(0.656\) consistent with \(P_j/N_j\) |

**Do not assume** these settings apply to \(N=64\) or \(128\).

**Honesty about overclaim in the draft:**
- Broadly distributed **amplitudes** ≠ broadly distributed **signed energy transfer** (phases, geometry, cancellation matter).  
- Prefer “broadly distributed under the stated diagnostic” over unqualified “equidistributed.”  
- No detected events = none at **sampled times** under **chosen thresholds** — not exclusion of shorter events.  
- These diagnostics alone do **not** establish “no coherent structure” or rule out concentration-based blowup mechanisms.

**Defensible finding:** reported runs showed no crossings of the specified concentration thresholds at the sampled times — worth preserving and checking against code/data.

**Next concrete step on this track:** recover code defining shell participation \(P_j\) and triad-based AET; run **both** on the **same** saved snapshot and shell before treating them as equivalent. Classic participation form:
\[
P=\frac{\bigl(\sum_i w_i\bigr)^2}{\sum_i w_i^2}.
\]
Mode weights ≠ triad weights. Then separately confirm configs for \(N=64,128\).

### Track E — Claim ledger

July 23 claim-ledger copy **mixes older claims with later corrections**.  
**Do not automatically restore older PROVED labels.** Use Oct honesty audits (`CLAIM-LEDGER-AUDIT-2026-10` on claim-ledger branches) as the correction layer.

### Track F — Main unaugmented proof chain

Live gate still **OPEN:** same-scale \(T_{j\leftarrow j}\), \(\alpha_+\) depletion, product / uniform \(\mathcal{R}_\star\).  
Spectral bookkeeping ≠ geometric close. Ring is side hardware.

---

## 3. What we are focusing on **now**

### Focus #1 (shared budget) — primary for Grok bots tasked with exact-shell work
1. Obtain/confirm access to the **full** author ZIP (not only README).  
2. Independently review: geometric lemmas → overlap arithmetic → high-pass conclusions.  
3. Verdict each as: proved at stated scope / repairable gap / failed.  
4. Then ask: can omitted families be added **without uncontrolled repeated dissipation charges** (overlap counting is the hard part)?  
5. Keep criterion **(17)** and Clay **OPEN**.

### Focus #2 (swirl) — primary for bots on the swirl branch
Attack the signed compression remainder \(B\) with all localization costs paid. Reject pure absorption and low-order-only gate shortcuts.

### Focus #3 (numerics) — primary for bots with solver access
Recover \(P_j\) vs AET definitions; same-snapshot comparison; do not upgrade diffuse-cascade draft language.

### Explicit non-focus (this week)
- Claiming NS/Clay solved  
- Merging swirl, shared-budget, and AET into one “cascade proof”  
- Restoring July ledger PROVED stamps without reconciliation  
- Treating phase reinforcement as saturation of the 32-shape bound  

---

## 4. Instruction block (paste to each Grok bot)

```
Read this research handoff and use it as the working context for our Navier–Stokes work.
Preserve its distinction between reported results, rerun computations, scoped analytic results, and open problems.

Current priority: independently review the exact 32-shape shared-budget argument, then investigate extending it to omitted interaction families without uncontrolled repeated dissipation charges. The previously missing ZIP has been reported recovered elsewhere; confirm you can actually open the full package (shape list + verify script), not only the cover-note README.

Updates after the report:
- The supplied July 23 claim-ledger copy mixes older claims with later corrections; do not automatically restore its older PROVED labels.
- The diffuse-cascade draft reports zero danger events at N=32,64,128. These remain reported numerical observations.
- A screenshot documents one run with N=32, ν=0.02, T=2.0, 51 snapshots, no Q operators. Do not assume these settings apply to the other resolutions.
- Recover the code defining shell participation P_j and triad-based AET. Compare them on the same snapshot before treating them as equivalent.
- Keep the exact-shell budget, axisymmetric swirl compression, and numerical diagnostics as distinct tracks. The full all-scalene budget and classical regularity remain open.

After reading, summarize what you understand, identify which source files you can actually access, and state the next concrete calculation you can perform. Do not claim to have run or verified anything you have not.
```

Send **separately** to each bot unless you know they share context.

---

## 5. Repo / PR map (for bots that have GitHub access)

| Track | Branch / PR | Key paths |
|---|---|---|
| Shared budget 32-shape | `cursor/shared-budget-32-shape-c3ed` | `docs/COVER-NOTE-…`, `docs/SHARED-BUDGET-32-SHAPE-…`, `packets/Shared-Budget-17-Family-…/README.md` |
| Swirl four doors | `cursor/da-swirl-four-doors-0cc5` · PR #167 | `docs/ns-review/DA-SWIRL-*.md`, `PHONE-HANDOFF-2026-10-07.md`, this file |
| Ring visuals | `cursor/ring-lemma-hardware-visuals-0cc5` · PR #164 | `docs/ns-review/visual-journey/` |
| Ring PDF | `cursor/ring-lemma-pdf-0cc5` · PR #163 | `docs/ns-review/ring-lemma/` |
| Phone handoff (shorter) | same as swirl | `docs/ns-review/PHONE-HANDOFF-2026-10-07.md` |

---

## 6. One-screen status for phone Grok

> **Focus now:** independently review 32-shape shared-budget (overlap-safe dissipation); then omitted families without double-charging. **Separate:** swirl signed compression \(C_F\le\eta\nu D_F+BQ\); diffuse-cascade AET (reported 0 danger events at 32/64/128 — verify \(P_j\) vs AET on one snapshot); Ring = spatial hardware done. **Open:** all-scalene (17), Clay. **Do not** restore July ledger PROVED stamps blindly. NS not solved.

---

*End of handoff. No regularity claim.*
