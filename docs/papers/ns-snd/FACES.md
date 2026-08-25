# Paper2 has several faces. They are not a compile pair.

Do **not** treat any PDF as a compile of the August TeX, or the reverse.
Do **not** merge the “implies” title with the conditional-framework title.

| Face | File | What it is |
|---|---|---|
| June reading PDF | [`Paper2_NS_Regularity_SND_FIXED.pdf`](Paper2_NS_Regularity_SND_FIXED.pdf) | *Spectral Non-Concentration as a Conditional Regularity Criterion.* Corrected June 2026. 7 pages. SHA-256 `7de9444d…`. GNC absent. \(C_N\eta_N\) marked numerical/conditional. T2 is a **program**, not a closed proof. |
| June FIXED TeX | **not received** | Filename `Paper2_NS_Regularity_SND_FIXED.tex` was requested. Only the PDF is on disk. Do not invent the source. Do not treat the August TeX as that compile. |
| June 14 Clay-submit | **not received** | Filename `2f30e8c4f_NS_ClaySubmit_Jonathan_Simons_2026-06-14.tex` (Mac Downloads; 1677 lines claimed). Bytes never reached this VM. **Not** FIXED. **Not** the August controlling face. Historical / withdrawn-claim face only if it later arrives. Classical regularity is **NOT CLAIMED** in current governance even if that draft claimed Clay. Do not treat it as a compile of the FIXED PDF or as a Clay solution. |
| Mac “Final Polished” TeX | [`NS_Regularity_Final_Polished.tex`](NS_Regularity_Final_Polished.tex) | Jon CloudDocs `NS Regularity Final Polished.tex`. `\documentclass[12pt]{amsart}`. Title *Global Regularity of the Three-Dimensional Incompressible Navier–Stokes Equations via Self-Adaptive Spectral Damping*. `\date{2026}` only. **825 lines** on disk (Mac open path claimed 826). SHA-256 `b9249af37f…`. **Not** `Paper2_NS_Regularity_SND_FIXED.tex`. **Not** the June FIXED PDF compile (that face is *Conditional Regularity Criterion*, Corrected June 2026, 7 pages). **Not** the August repaired TeX (no GNC, no simplex, no Lemma 6.1, \(\mathbb{R}^3\) not \(\mathbb{T}^3\)). Body: augmented GWP claimed; classical NS is **conditional** on [SND], which is **OPEN**. Title overclaims a closed global-regularity result. **Do not use as closed.** Superseded as a Clay / unaugmented claim by the Aug 1 audit and leftover 7–8 OPEN. Q6 here is dominant-shell damping, not Paper2 \(H_N\) and not GCD Q6. |
| Mac “SND 2” PDF | [`Paper2_NS_Regularity_SND.pdf`](Paper2_NS_Regularity_SND.pdf) | Local iOS/Quartz export 21 July 2026, 561 297 bytes. Running header *SND implies global regularity*. **Not** the Zenodo bytes. |
| Zenodo “implies” deposit | [`zenodo-20272545/Paper2_NS_Regularity_SND.pdf`](zenodo-20272545/Paper2_NS_Regularity_SND.pdf) | Public record [10.5281/zenodo.20272545](https://doi.org/10.5281/zenodo.20272545). 360 856 bytes. Live title prefixed **[Claim withdrawn - see errata]**. |
| August repaired TeX | [`Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`](Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex) | 1 August 2026. Title is already the *conditional framework*. GNC incomplete; false gcd removed; Route J NUMERICAL/UNDER AUDIT; T2 Gronwall **withdrawn**; simplex **OPEN**. |
| August 1 audit | [`NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md`](NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md) | Independent status of the Zenodo “implies” manuscript. Names the kink: Lemma 6.1 OPEN; §7 T2 “closed” contradicts §8 OPEN. |
| Classical unaugmented chain | [`NS_UNAUGMENTED_PROOF_CHAIN.md`](NS_UNAUGMENTED_PROOF_CHAIN.md) | Numbered Statement-B / Leray–Hopf program Domain Architect uses. Step 2 Ring Lemma is PROVED. Frozen gap is step 4. Leftover is 7–8. Clay not claimed. **Not** the June FIXED PDF compile. |

## June vs August (kept from the two-face filing)

| | June reading PDF | August repaired TeX |
|---|---|---|
| Title | *…as a Conditional Regularity Criterion* | *…and a Conditional Global-Regularity Framework* |
| Date on the face | Corrected June 2026 (original draft 18 May) | 1 August 2026 (header still 18 May) |
| GNC / false gcd | **Absent** | Present: GNC analytically incomplete; \(\gcd(2k-i,2k-j)=\gcd(i,j)\) removed |
| Frozen gap | Hypothesis 2.1, cited from Paper 1 | Route J **NUMERICAL / UNDER AUDIT**, \(N\le 800\), no all-\(N\) theorem |
| Product \(C_N\eta_N<\delta_0\) | Status table: **Numerical/conditional** | Status table: middle arrow **proved** (lemma + numerics), then a remark that those numbers are **not a theorem** |
| T2 / Gronwall | §7 is a **proof plan** | Previous “T2 Closed Gronwall” **withdrawn** |
| Simplex lemma | Lemma 6.1 **open** | SND Simplex Stability **open** |
| Classical 3D NS | **Not claimed** | **Not claimed** |
| Paper 1 citation | Zenodo `10.5281/zenodo.19842060` | Preprint, “historical reference only” |

## What the August 1 audit adds

It is about the **Zenodo “implies” manuscript** (DOI `10.5281/zenodo.20272545`), not about Domain Architect.

**Stands:** Theorem 4.1 (conditional Weyl); Lemma 3.1 (Lipschitz of \(H_N[a]\)).

**Diseased / do not use as closed:** Section 7 “T2 Closed (conditional on SND).” Local existence only gives \(\|a-\mu\|_1\le 2\), not the target 0.039 bound. Section 8 correctly lists T1 and T2 as OPEN.

**Leftover (the kink):** Lemma 6.1, uniform-in-time simplex / SND stability, **OPEN**.

**Even after a repair of 6.1:** the manuscript still owes an explicit continuation criterion from spectral gap to Leray–Hopf smoothness. Spectral stability under SND is not unconditional regularity.

Stale bibliography: `10.5281/zenodo.19842060` is a superseded Ring/SND record, not GCD Paper 1. `10.5281/zenodo.19842061` is unrelated.

## What they agree on (every honest face)

Conditional Weyl: *if* frozen gap and quantitative operator-norm closeness, then \(\lambda_{\min}>-1/2\). Lipschitz of \(H_N[a]\) is triangle inequality. Leray boundedness is not simplex smallness. The leftover is \(\|a(t)-\mu\|_{\ell^1}\). That leftover is **not** swirl’s \(\int\|u^r/r\|_\infty\,dt\).

## Which face to use

- **Later caution on Route J and GNC:** August TeX.
- **Cleaner honesty on the product \(C_N\eta_N\):** June FIXED PDF.
- **Public withdrawn “implies” claim:** Zenodo `20272545` plus the August 1 audit.
- **Mac “SND 2” export:** file it, do not cite it as the Zenodo bytes or as a closed theorem.
- **June 14 Clay-submit:** not on disk. Do not invent it. If it arrives, file as historical / withdrawn-claim — not live DA math, not FIXED, not August.
- **Mac “Final Polished” TeX:** filed as its own Q6 / \(\lambda_H\) / \(\mathbb{R}^3\) face. Title overclaims; body leaves [SND] OPEN. **Do not use as closed.** Not FIXED. Not August. Not a Clay solution.
- **Do not merge them into one claim.**
- **Localized reparation** (DA surgery) uses the **classical unaugmented chain** [`NS_UNAUGMENTED_PROOF_CHAIN.md`](NS_UNAUGMENTED_PROOF_CHAIN.md). Controlling face: August repaired TeX. Default cut is leftover **7–8**, not step 2 (Ring Lemma is already PROVED). This is **not** the June FIXED PDF compile. See [`docs/domain-architect/LOCALIZED-REPAIR.md`](../../domain-architect/LOCALIZED-REPAIR.md).

The June Paper2 PDF cites Zenodo `10.5281/zenodo.19842060` as GCD Paper1. Live record at that DOI is a superseded Ring/SND paper. Current Q6 face: [`docs/papers/gcd/`](../gcd/README.md). Current Ring face: [`docs/papers/ring/`](../ring/README.md). Errata: [`docs/papers/status-errata/`](../status-errata/README.md).
