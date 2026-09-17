# New PR frame vs DA REJECT on ABC / λ

**Date:** 10 September 2026  
**This book:** `cursor/centered-ns-recovery-b5c1` · PR https://github.com/simons357/Ship_it_app/pull/45  
**Other book (do not merge):** `cursor/unaugmented-r4-vorticity-f80e` · PR https://github.com/simons357/Ship_it_app/pull/24  
**Other agent:** https://cursor.com/agents/bc-01a026a4-cf05-7637-8c16-cd4b7032f80e

**NS is not solved. Lemma★ is OPEN.** This note compares frames. It does **not** stamp a kill or a proof.

Watch request (decoded): look at the new PR frame — especially the λ = 2, 4, 8, 16 table and `cs_remainder_exact_check.py` — against Domain Architect’s REJECT of the prior ABC / λ reconstruction.

---

## What DA actually rejected

The Domain Architect / other-evaluator gate was **not** “localized ABC is fake.” It was:

> No Target A stamp until this field matches the exact triad core.

That rejected the **first reconstruction**, which:

1. Stamped “Target A is false” from an FFT Galerkin table alone.
2. Then compared that **full-field** table to a **99% energy cutoff** as if they were the same field.

Those are different fields. On the cutoff, about half of \(T_c\) is gone (`Tc_rel ≈ 0.53`–`0.56` at λ = 2, 3, 4). \(T_c\) lives in the tail. That gap is a field change, not a convention bug.

DA’s own Lemma★ PRs (#49–#60) do **not** contain a separate ABC / λ reject card. The reject that matters is this exact-core gate.

---

## What the new frame is

On PR #24:

| Piece | Path |
|---|---|
| FFT bump hunt | `scripts/ns_attacks/cs_remainder_bump.py` |
| Exact-core gate | `scripts/ns_attacks/cs_remainder_exact_check.py` |
| FFT JSON | `results/cs_remainder_bump/cs_remainder.json` |
| Core JSON | `results/cs_remainder_bump/exact_core_check.json` |
| Their writeup | `docs/CS-REMAINDER.md` |

Family (spatial concentration on the fixed torus):

\[
v_\lambda
=
-
\frac{P(\gamma_\lambda\,\mathrm{ABC}_\lambda)}
{\|P(\gamma_\lambda\,\mathrm{ABC}_\lambda)\|_2},
\qquad
\widehat{\gamma}_\lambda(k)=\exp(-|k|^2/(2\lambda^2)).
\]

**Target A** in that book is the CS remainder \(\|A^{1/2}B\|_2\le C\sqrt{EY}\). If it held, then \(|T_c|\le C\sqrt{D_s EY}\) and \(\mathcal R_\star\) would be bounded. The converse is false: CS can climb while \(T_c\approx 0\).

---

## The λ table that actually exists

There is **no λ = 16 row** in the JSON or in `cs_remainder_exact_check.py`. The screenshot’s “2, 4, 8, 16” table is not on disk. Present scales: **2, 3, 4, 5, 6, 8**.

### Full-field FFT (`local_abc` only)

`R_star` in the JSON is the locked \((T_c)_+\) form and is **0** on this family (\(T_c<0\)). The published column is `R_star_signed` \(= T_c^2/(D_s E Y)\). After \(v\mapsto -v\) that equals canonical \(\mathcal R_\star\) (correction 3). Compression on the computed field is not itself a stretching kill; the reverse is.

| λ | grid | CS \(\|A^{1/2}B\|/\sqrt{EY}\) | \(\mathcal R_\star\) after reverse | \(T_c\) |
|---:|---:|---:|---:|---:|
| 2 | 48 | 2.492 | 0.00517 | −27.6 |
| 3 | 48 | 4.607 | 0.0173 | −381 |
| 4 | 64 | 7.104 | 0.0409 | −2.47×10³ |
| 5 | 80 | 9.934 | 0.0798 | −1.05×10⁴ |
| 6 | 96 | 13.062 | 0.138 | −3.44×10⁴ |
| 8 | 128 | 20.114 | 0.327 | −2.23×10⁵ |

They fit CS \(\sim 0.88\,\lambda^{3/2}\) and \(\mathcal R_\star\sim 6.47\times 10^{-4}\,\lambda^3\). That is a **fit on six finite grids**, not a theorem.

### Exact-core table (99% energy cutoff — **different field**)

Script loop: `for lam, n in ((2, 32), (3, 36), (4, 48))`. **λ = 8 and λ = 16 were not run on the core.**

| λ | modes | core \(\mathcal R_\star\) (\(T_c^2\)) | \(\mathcal R_\star/\lambda^3\) | FFT vs core \(T_c\) rel |
|---:|---:|---:|---:|---:|
| 2 | 836 | 0.001748 | \(2.19\times 10^{-4}\) | 0.535 |
| 3 | 2820 | 0.005181 | \(1.92\times 10^{-4}\) | 0.565 |
| 4 | 6672 | 0.013669 | \(2.14\times 10^{-4}\) | 0.542 |

Climbs on that cutoff family. About 3× smaller than the matching full-FFT row.

### Other families (same FFT script)

`curl_gaussian`, `lp_packet`, `aligned_ball`: CS can climb (`curl_gaussian` CS ≈ 21.5 at λ = 8) but \(T_c\approx 0\), so \(\mathcal R_\star\approx 0\). Those are **not** ★ climbs. Only reversed `local_abc` is the claimed ★ climb.

N-shell maximizers on the same branch saturate (`docs/RSTAR-SHELL-CLIMB.md`). They do not climb.

---

## What sits after the DA gate

These locks in `exact_core_check.json` **do** answer the reject:

| Lock | Result |
|---|---|
| Same **truncated** field: FFT \(T_c\) vs direct triad | \(T_c\) rel \(\approx 5\times 10^{-14}\), \(\mathcal R_\star\) rel \(\approx 10^{-13}\) |
| Fourier dilation \(v(n\cdot)\) | \(\mathcal R_\star\) unchanged (rel = 0) on the λ = 2 cutoff |
| Fast triad vs `stokes_moments.probe` on a 3-mode field | \(D_s\) matches; **\(T_c=0\)** on that particular field |

So: the evaluator is not inventing a different \(T_c\) than the triad sum **on one field**. The first stamp’s FFT-vs-cutoff gap is the tail, not a sign/convention bug.

---

## What still fails this book’s kill rules

This book’s remaining job is: prove \(\sup\mathcal R_\star<\infty\), **or** a family on which \(\mathcal R_\star\) **diverges**. One large **finite** value only raises \(C_{\mathrm{geom}}\).

| Claim on PR #24 | This book |
|---|---|
| “Target A is false.” | CS remainder looks **unbounded on these grids**. That is **not** yet a continuum theorem, and it is **not** the same as killing ★. |
| “Lemma★ FALSE as a uniform bound.” (`docs/LEMMA-STAR.md` on that branch) | **Do not import.** Their own JSON still says `"lemma_star": "OPEN"`. Largest finite value on disk is \(\mathcal R_\star\approx 0.327\) at λ = 8 (FFT) and \(0.0137\) at λ = 4 (core). |
| “CS remainder also false.” | Same caveat: Galerkin, growing grid, six points, no λ = 16. |
| Fit \(\mathcal R_\star\sim c\lambda^3\) | Suggestive. Not a proof that \(\lambda\to\infty\) on smooth fields. |
| NS solved | **No.** Every artifact says `ns_solved: false`. |

Further hygiene:

- Family is **FFT Galerkin** on \(\mathbb T^3\), grid growing with λ (48 → 128). Not a proved continuum counterexample on \(\mathbb R^3\) or even a fixed-grid continuum field.
- Exact core and full FFT remain **different fields**. Publishing both as “the table” reopens the DA reject unless each row says which field it is.
- Formula lock on the 3-mode field does **not** exercise a nonzero \(T_c\). The same-field ABC lock does.
- Do **not** glue this ABC remainder to H1, five-lane 1–5, or 9A–9D.

---

## Verdict

**DA’s REJECT of the prior ABC / λ recon still stands** as a reject of the first stamp: FFT-only, then two different fields compared.

**The new frame answers that gate** on same-field identity and shows a **finite climb** of reversed-\(T_c\) \(\mathcal R_\star\) on localized ABC: core through λ = 4, FFT through λ = 8.

**It does not convert that climb into a kill of Lemma★.** There is no λ = 16 row. Exact core never ran λ = 8 or 16. A fit on finite grids is not \(\mathcal R_\star\to\infty\).

Lemma★ remains **OPEN**. Kill lane remains **LIVE**. NS is **not** solved.

If the kill lane wants this family next, the honest next measurements are: exact-core (same field definition) at λ = 8 and λ = 16; a resolution study at fixed λ; and a statement of what would count as divergence rather than a larger finite \(C_{\mathrm{geom}}\).

---

## SuperGrok filing (10 Sep 17:56) — scored

SuperGrok’s unaugmented ABC_λ audit. Shared line we **keep**: table is an evaluator, not a proof; exact core ≠ proof; ★ still open; unaugmented NSE not solved.

| SuperGrok line | This book |
|---|---|
| Family is λ-scaled ABC × Gaussian cutoff | **Sit.** Standard ABC at frequency \(k_0=\lambda\), spatial Gaussian, Leray, unit energy. |
| CS \(\sim 0.88\lambda^{3/2}\), \(\mathcal R_\star\sim 6.47\times 10^{-4}\lambda^3\), does not saturate | **Sit as a fit** on FFT rows λ = 2, 3, 4, 5, 6, 8. SuperGrok dropped λ = 6. N-shell max saturates; this field does not **on those grids**. |
| Kills Target A / CS remainder / ★ as a closer | **Refuse as a stamp.** Finite climb. ★ as a closer dies only if \(\sup\mathcal R_\star=\infty\). Not shown. |
| H1 is a different integral; named; not run on ABC_λ | **Sit.** Untested. This book has not started H1. |
| Falsifier-of-record: yes, pending exact-script confirmation | **Refuse.** Exact script **already ran** (λ = 2, 3, 4 cutoff + same-field lock). That confirms a finite climb, not a falsifier of ★. |
| Next: reprint `cs_remainder_exact_check.py` on λ = 2, 4, 8, 16; if climb continues, stop patching ★ | **Half.** λ = 8 and 16 were **never** in that script. More finite rows still only raise \(C_{\mathrm{geom}}\) unless divergence is stated. Do not “stop patching ★” from a longer table. |
| Augmented / Q-stack / coherence | **Out of this book.** Not addressed; do not glue. |

### Claude’s two items (locked)

1. **Same \(\mathcal R_\star\)?** Yes, after reverse. JSON `R_star` is \((T_c)_+\) and is **0** on this family (\(T_c<0\)). Published column is `R_star_signed` \(=T_c^2/(D_s E Y)\), which is canonical \(\mathcal R_\star(-v)\). Exact-core uses the same \(T_c^2\) quotient. Not an ABC-only variant. That is why the exact script exists, and it already answered this for the cutoff field.
2. **H1 on ABC_λ?** **Untested.** Named only. Not shown immune.

`cs_remainder_exact_check.py` does four jobs: (i) 3-mode triad vs `probe` (there \(T_c=0\)); (ii) export 99% energy modes and sum the triad; (iii) put that **same** truncated field on a grid and match FFT \(T_c\) to \(10^{-13}\); (iv) check \(v(n\cdot)\) leaves \(\mathcal R_\star\) flat. It does **not** prove ★ false and does **not** run λ = 8 or 16.

