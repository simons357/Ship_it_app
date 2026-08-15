# ARCHON — NS Final Review Panel

**Mission:** Unconditional verification before Zenodo submission as Clay Statement (B)  
**Date of review:** 2026-08-15  
**Papers examined:**
- Zenodo `10.5281/zenodo.20518057` — *Conditional* framework (`docs/papers/SND_RING_LEMMA_NS.tex`)
- Zenodo `10.5281/zenodo.20405526` — *Claims* Statement (B) (`docs/papers/Simons_NS_GlobalRegularity_T3.tex`)
- Prior audit: Claude Drive read of `NS_FINAL_MERGED_UNCONDITIONAL.tex` (file **not** present in this VM)

**Important:** The favorable “PANEL CONSENSUS VERDICT” text in the briefing is **rejected**. It mislabels Theorem H and is not consistent with the manuscripts.

**User note (2026-08-15):** The Zenodo sources above are the **old** papers. The current target named in the ARCHON briefing — `NS_FINAL_MERGED_UNCONDITIONAL.tex` / `NS_PROOF_CHAIN.html` (June 10, 2026 E_c-gap merge) — is **not present** in this VM, this git repo, or Zenodo under those filenames. Prior agent notes place it on Google Drive only.

**Closeout:** Panel is **complete on available Zenodo sources**. Re-open only if the June 10 merge is added under `docs/papers/`. See `docs/math/CLOSEOUT.md`.

---

## Executive verdict (old papers only)

| Question | Answer |
| --- | --- |
| Is Theorem H “SND holds unconditionally for all \(H^1\) data”? | **No.** Theorem H proves a **shell-conditioned commutator bound (SND-C)** under hypotheses that already include an a priori enstrophy ceiling \(M\) and a **spread** regime \(\rho\le\rho_0\). |
| Is Clay Statement (B) proved? | **No.** |
| Submit to Zenodo as “unconditional regularity / Statement (B)”? | **Do not.** Submit only as a **conditional** framework (as `20518057` already does in the abstract), or withdraw Statement-(B) claims from `20405526`. |
| One remaining question from the briefing | Correct keystone: **Is SND proved without presupposing \(X\le M\)?** Current answer: **No.** |

---

## Version conflict (must fix before any upload)

| Record | Title / claim | Honest reading |
| --- | --- | --- |
| `20518057` | Conditional framework; abstract: “does not claim unconditional resolution”; Open Problem: prove SND for arbitrary large data | **Aligned with evidence** |
| `20405526` | “resolving Clay … Statement (B)”; status table greens Main Theorem | **Overclaim** — same Theorem H object, same \(M\)-dependence |
| Briefing title | “Unconditional Regularity Proof…” | **Does not match** the theorem that is actually proved |

`NS_FINAL_MERGED_UNCONDITIONAL.tex` / `NS_PROOF_CHAIN.html` were **not found** in this repository or on Zenodo under those filenames. Review proceeds on the two Zenodo sources above + prior referee notes.

---

## Expert-by-expert answers

### 1. Terence Tao — Harmonic analysis / PDE regulator

| Briefing question | Panel answer |
| --- | --- |
| Is SND \(X\ge c_* J\) (i.e. \(J/X\ge c_*\)) provable for all time? | **Not proved.** Conditional paper leaves it as Open Problem. Claim paper asserts it via G+H, but H/G depend on \(M\). |
| Does the dominant-shell condition propagate under NS? | Theorem G claims propagation **assuming SND-C**. SND-C’s constant \(C_*=C_*(\nu,\delta_*,M,\rho_0,C_S)\) **already uses \(M\)**. Propagation under an a priori bound is not unconditional propagation. |
| Is \(c_*\) universal or data-dependent? | In small-data props: \(c_*=c_*(\delta_{\mathrm{KT}},\nu)\) — **data-dependent**. Briefing’s \(c_*=6/\pi^2\) is **arithmetic squarefree density**, not derived as the fluids SND threshold in these proofs. |

**Tao verdict:** Theorem H is **not** airtight unconditional SND. Labeling SND-C “unconditional” while \(C_*\) depends on \(M\) fails the skeptic test. Averaged-NS / supercriticality barrier still applies to any argument that smuggles large-data \(H^1\) control into the hypotheses.

**Would Tao call this non-trivial if SND were unconditional?** Yes — *if* SND were proved for all \(H^1\) data without circular bounds. That hypothesis is exactly what is missing.

---

### 2. Charles Fefferman — Clay Statement (B)

| Briefing question | Panel answer |
| --- | --- |
| All \(u_0\in H^1(\mathbb{T}^3)\) or dense subset? | Claim paper asserts all; proof chain only covers all data **if** SND/SND-C close without size restriction — they do not. |
| \(\mathbb{T}^3\) Clay-compatible? | **Yes** — Statement (B) is \(\mathbb{T}^3\). Domain is fine. |
| Hidden compactness? | **Risk:** Q1 approximation + passing to limits; Aubin–Lions / \(\varepsilon\to0\) steps must not silently use smoothness of the limit. More serious: **hidden a priori bound \(X\le M\)** is the actual compactness/control being assumed. |

**Fefferman verdict:** Domain OK. **Statement (B) not established.** Do not submit as prize closure.

---

### 3. Peter Constantin — Vorticity direction / CF

| Briefing question | Panel answer |
| --- | --- |
| Does Ring Lemma deliver CF (1993)? | **Only in the band-limited / concentrated regime**, on \(E_c=\{|\omega|\ge c\cdot 2^{j^*}\|u\|_{L^2}\}\), under Fourier support in one shell. That is a **conditional geometric bound**, not global CF for arbitrary Leray–Hopf fields. |
| BVB 2002 weighted CF invoked correctly? | Not fully checkable from the short Global Regularity writeup; longer conditional paper sketches CF via Ring + corollary. Briefing’s “E_c gap closed June 10” file is absent here. |
| Is \(E_c\) measurable / complement handled? | \(E_c\) is measurable (level set of continuous \(|\omega|\) for smooth approximants). Complement control “\(|\omega|\) small ⇒ absorbed by dissipation” needs a **quantitative** estimate uniform in the approximation — not verified as Clay-grade in the short paper. |

**Constantin verdict:** Ring Lemma is a plausible **band-limited** tool (keep as toolkit). **Not** enough, alone, for Statement (B). Briefing’s “BVB accepts / gap closed” is **not endorsed** without the missing June 10 appendix under line-by-line check.

---

### 4. Hugo Beirão da Veiga — BVB author

| Briefing question | Panel answer |
| --- | --- |
| Is \(\int|\omega|^2|\nabla\xi_0|^2\) finite from Ring? | On \(E_c\), Ring gives \(\|\nabla\xi_0\|_{L^\infty(E_c)}\le C\cdot 2^{j^*}\). Finiteness of the **weighted** integral still needs control of \(\int_{E_c}|\omega|^2\) and the complement. Not automatic from Lipschitz on \(E_c\) alone. |
| Siran Li 2018 Hölder variant? | Not substantively present in `20405526` short tex. |
| \(\alpha>1/2\)? | Briefing asserts Lipschitz \(\Rightarrow\alpha=1\). That only holds **on \(E_c\)** under band-limited hypotheses — not globally on \(\mathbb{T}^3\times[0,T]\). |

**BVB verdict:** **Do not accept** the briefing’s automatic pass. Application incomplete / sketch-level for prize standards.

---

### 5. Jean Leray — foundational skeptic

| Briefing question | Panel answer |
| --- | --- |
| Is the weak solution Leray–Hopf? | Q1 scheme aims to converge to Leray–Hopf (Theorem C in conditional paper). Acceptable as a regularization route **if** limits are careful. |
| Uniqueness? | Correctly should **not** claim uniqueness beyond energy-class facts. Claim Main Theorem’s “the” solution language should stay inside Leray–Hopf. |
| Energy inequality direction? | Must use Leray–Hopf energy **inequality** (≤), not pretend equality. Conditional paper is closer to honest; Clay-claim paper’s Main Theorem proof is too short to verify. |

**Leray verdict:** Class is fine **if** claims stay conditional. Overclaiming Statement (B) violates foundational caution.

---

### 6. Vlad Vicol — modern attacks

| Briefing question | Panel answer |
| --- | --- |
| SND vs Onsager / convex integration? | Onsager constructions live at low Hölder regularity for **Euler**. They do not automatically give an \(H^1\) NS counterexample to SND — but they show **geometric/energy methods can fail** without dissipative structure. SND still needs proof. |
| Known \(H^1\) datum violating SND? | **No known counterexample** — absence of counterexample ≠ theorem. |
| Q1 hyperdissipative consistent? | Legitimate regularization **idea**; must not alter the supercritical balance in the limit. Tao’s barrier: methods that only use abstract energy-compatible estimates are insufficient. |

**Vicol verdict:** Q1 is OK as a tool. **No pass** on unconditional NS. Briefing’s “no known counterexample ⇒ accept” is logically invalid.

---

### 7. Maria Colombo — endpoint regularity

| Briefing question | Panel answer |
| --- | --- |
| Energy estimate in correct Lebesgue space? | Spread-regime Poincaré / dissipation estimates need careful constants; not Clay-checked here. |
| \(L^2\to H^1\) bootstrap? | Standard parabolic bootstrap **after** \(H^1\) control. Getting \(H^1\) is the issue. |
| Hidden log losses? | Theorem H sketch uses Young / Bernstein; log losses may hide in LP summations. Conditional paper is more explicit; still not prize-ready. |

**Colombo verdict:** Briefing’s “bootstrap clean” is **unsupported**. Conditional framing only.

---

### 8. Dallas Albritton — forced / non-uniqueness

| Briefing question | Panel answer |
| --- | --- |
| Forced NS? | Unforced NS is the Clay setting. Papers should state **\(f=0\)** explicitly everywhere (including Q1). |
| \(\mathbb{T}^3\) vs \(\mathbb{R}^3\)? | Statement (B) only. Statement (A) correctly left open in both versions. |

**Albritton verdict:** Domain choice OK. Does **not** rescue the keystone failure.

---

### 9. Elias Stein — singular integrals

| Briefing question | Panel answer |
| --- | --- |
| Riesz / CZ on \(\mathbb{T}^3\)? | Periodic LP theory is standard. Not the failure point. |
| Estimates failing on \(\mathbb{T}^3\)? | Unlikely the blocker. |

**Stein verdict:** LP setting **acceptable**. Does not imply the nonlinear closure works.

---

### 10. Gómez-Serrano / computational

| Briefing question | Panel answer |
| --- | --- |
| Is \(c_*=6/\pi^2\) the SND constant? | **No — category error.** \(6/\pi^2=\zeta(2)^{-1}\) is squarefree density / Triple Lock arithmetic vacuum. Fluids SND uses \(c_*>0\) with **data/ν dependence** in proved regimes. |
| Q1 numerically verifiable? | In principle yes; not a Clay proof. |
| Spectral gap of \(Q_N\)? | Full-spectrum \(\lambda_{\min}(Q_N)>-1/2\) is **false** (verified: \(\lambda_{\min}(Q_{200})\approx-29.7\)). Do **not** cite \(Q_N\) gap as NS evidence. |

**Computational verdict:** Briefing’s numeric consensus is **wrong**. Mixing \(6/\pi^2\) into SND is a **disqualifier** for submission.

---

## Proof-chain audit (briefing Steps 1–5)

| Step | Briefing claim | Panel finding |
| --- | --- | --- |
| 1. Q1 + Thms A/B/C | Augmented smooth; Phi-renorm; converge to LH | **Keep as method notes** (Phi-renorm algebraic cancel is the strongest brick). Convergence must stay non-circular. |
| 2. SND + “Theorem H = SND unconditional” | Keystone | **False labeling.** H = SND-C under \(M,\rho_0\). G needs H. Neither is unconditional SND. |
| 3. Ring Lemma | Three shells / \(\|\nabla\xi_0\|_{L^\infty(E_c)}\le C\cdot 2^{j^*}\) | **Conditional geometric lemma** — interesting; not Statement (B). |
| 4. \(E_c\) gap + BVB | Closed June 10 | **File missing**; not verified. |
| 5. Thm D + Clay (B) | Resolved | **Rejected.** |

### The circularity in one line

SND-C / Theorem H uses a constant depending on \(M\sim\sup X(t)\).  
Theorem G produces SND with \(c_*\) depending on that same \(M\).  
Main Theorem needs SND to bound \(X(t)\).  
**Using \(M\) to get the bound that defines \(M\) is not unconditional.**

Claude’s earlier Drive note on `NS_FINAL_MERGED_UNCONDITIONAL.tex` matches: *“regular ⇒ regular”* unless \(M\) is derived from \(\|u_0\|_{H^1}\) alone.

---

## Corrected panel consensus (replace the briefing’s)

| Expert | Pass / Fail | One-liner |
| --- | --- | --- |
| Tao | **Fail keystone** | H ≠ unconditional SND; \(M\)-dependence fatal |
| Fefferman | **Fail Statement (B)** | \(\mathbb{T}^3\) OK; proof not |
| Constantin | **Conditional only** | Ring useful; global CF not sealed |
| BVB | **Not accepted** | Weighted integral / complement incomplete |
| Leray | **Conditional OK** | Do not overclaim |
| Vicol | **Fail** | No counterexample ≠ theorem |
| Colombo | **Fail “clean bootstrap”** | Not verified |
| Albritton | **Domain OK** | Irrelevant to keystone |
| Stein | **LP OK** | Irrelevant to keystone |
| Gómez-Serrano | **Fail** | \(c_*=6/\pi^2\) wrong object; \(Q_N\) floor false |

**Collective focus:** The briefing was right that Theorem H is the keystone — and **wrong** that “everything else is solid.” Several other steps are sketch-level or mislabeled. The keystone **fails** as an unconditional SND proof.

---

## What may still be submitted (honest)

1. **Conditional regularity framework** under SND (as `20518057` abstract already states).  
2. **Phi-renormalization** method note (algebraic cancel).  
3. **Ring Lemma** as band-limited CF tool (with clear hypotheses).  
4. Explicit Open Problem: prove SND (or produce \(M\) from data) for all \(u_0\in H^1(\mathbb{T}^3)\).

## What must not be submitted

1. “Unconditional regularity proof / Clay Statement (B) resolved.”  
2. Status tables greening Main Theorem / Statement (B).  
3. “Theorem H = SND holds for all \(H^1\) data.”  
4. \(c_*=6/\pi^2\) as the fluids SND threshold.  
5. Any glue to false full-spectrum Bridge \(\lambda_{\min}(Q_N)>-1/2\).

---

## Recommendation

**Hold Zenodo unconditional submission.**  
Retitle / version-note `20405526` to match `20518057` (conditional).  
If `NS_FINAL_MERGED_UNCONDITIONAL.tex` exists on Drive, drop it into `docs/papers/` and re-run this panel on **that** file’s derivation of \(M\); until then, treat Statement (B) as **open**.

**Bottom line:** Theorem H is **not** fully proved as unconditional SND. The panel does **not** clear this manuscript for Clay Statement (B).
