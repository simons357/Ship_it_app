# Five-lane / Lemma★ — recovered pack (HIT)

**Dropped into:** `docs/ns-recovery/five-lane-pack/`  
**Date recovered:** 10 September 2026 (this agent)

**Grok Heavy:** start at [`../GROK_HEAVY.md`](../GROK_HEAVY.md). Run JSON is under `results/`.  
**Five-lane discussion and math:** [`../FIVE-LANE-DISCUSSION-AND-MATH.md`](../FIVE-LANE-DISCUSSION-AND-MATH.md). Attacks 9A–9D are **not** the five lanes.

This is **not** a proof. NS is **not** solved. Lemma★ is **OPEN**.

---

## 0. The five lanes (do not substitute 9A–9D)

Screenshot: “Five-lane drill done; K=0 dead; Lemma★ survives numeric kill only (not proved); HH→L still the gap.”  
The screenshot does **not** list the five names. PR #48 files do:

| Lane | Name | Script |
|---|---|---|
| 1 | Covariance | `attack1_covariance.py` |
| 2 | Triad / K=0 / \(C_*\) | `attack2_triad_k0_cstar.py` |
| 3 | Bony HH→L | `attack3_bony_hh_l.py` |
| 4 | Stokes | `attack4_stokes.py` |
| 5 | Route-2 kill | `attack5_route2_kill.py` |

Harness: `scripts/ns_attacks/run_all_five.py`. Later Grok “Lane two” = analytic \(X^{3/2}\) attempt; in these files Lane 2 is the triad / K=0 / \(C_*\) numeric lane. The product \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\) is false (\(a^3\) vs \(a^4\)).

---

## Repo / PR (highest priority) — FOUND

| Item | Location |
|---|---|
| Branch | `cursor/ns-five-lane-lemma-star-1390` |
| PR **#48** | https://github.com/simons357/Ship_it_app/pull/48 |
| Title | Five-lane Lemma★ drill: K=0 dead, ★ survives numeric |
| Authoring agent | https://cursor.com/agents/bc-01a00412-6516-7002-95f2-051faf8ba0eb (not fetchable from this environment) |
| Related PRs | #49 Lemma★/DA-NS-1 · #50 five-lane sync · #51 R_★ shape · **#52 exact Fourier formulas** |
| Cursor Origin `https://cursor.com/codebase/.../pull/48` | **Not found** on this VM. GitHub URL above is the live PR. |

---

## 1. Absolute defs (five-lane pack)

Source of lock: `docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md` with `LEMMA_STAR_EXACT_FORMULAS.md`  
Older proof attempt: `ARCHIVE_OLDER_LEMMA_STAR_PROOF.md` (not a theorem)  
Shape-form expansion: `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` (PR #48)  
Same formulas: `docs/ns-review/LEMMA-STAR-EXACT-FORMULAS.md` (PR #52)

Torus \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\). Stokes \(A=-P\Delta\), \(\lambda_k=|k|^2\), \((Av)_k=\lambda_k v_k\).

\[
X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,\quad
Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\quad
Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,
\]
\[
\Lambda=Y/X.
\]

\[
N=\sum\lambda_k T_k,\quad
M=\sum\lambda_k^2 T_k,\quad
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k,
\]

\[
T_k=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr]
\quad\text{(signed; never abs-value the triad sum).}
\]

\[
\mathcal D_s=Z-\Lambda Y=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2.
\]

\[
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal D_s).
\]

\(\nu\) = viscosity. \(\theta\) = Young absorption fraction in the **derived** packaging

\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2 Y
=\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2 X\Lambda,
\]

with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\) geometry-only (not a proved constant).

Canonical shape form (viscosity cancelled):

\[
\mathcal R_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)},
\qquad
(T_c)_+^2\le C_{\mathrm{geom}}\,\mathcal D_s\,\|v\|_2^2\,Y.
\]

---

## 2. Exact statement of the HH→L map (as filed)

**There is no closed theorem “HH→L ⇒ bound.”** Attack 3 is a **Bony channel partition**, diagnostic only.

Partition parent wavevectors of \(B(v,v)\) (hence of \(T_c\)) by a cutoff \(k_{\mathrm{cut}}\):

- **HH:** both \(|p|\) and \(|q|\ge k_{\mathrm{cut}}\)
- **HL:** exactly one of \(|p|,|q|\ge k_{\mathrm{cut}}\)
- **LL:** both below cutoff

Then recompute \(N,M,T_c=M-\Lambda N\) on each restricted \(B\).

**Analytic claim in the pack (gap, not a map that closes):** HH→L is the channel that **blocks** a clean product bound

\[
|T_c|\le C\|u\|_2 X^{3/2}
\quad\text{(or pre-Young }|T_c|\le C\|u\|_2 X\Lambda\text{).}
\]

**Hard rule:** HH→L-restricted partial sums are **not** complete \(T_c\). Kill / ★ decisions use **only complete signed** \(T_c\).

Code: `scripts/ns_attacks/attack3_bony_hh_l.py` (`Tc_by_channel`, `bony_HH_to_L`).

**Hyp-ST / Hyp-Lat / Lat-Emb / LAST-KEY-LEMMA-STAR:** **zero hits** on PR #48 and #52.

---

## 3. Whole PR #48 / five-lane folder

Copied here under `docs/ns-recovery/five-lane-pack/` (notes + scripts + HEADLINE). Live git:

- Branch `origin/cursor/ns-five-lane-lemma-star-1390`
- https://github.com/simons357/Ship_it_app/pull/48

Exact Fourier formulas also in PR #52: https://github.com/simons357/Ship_it_app/pull/52
