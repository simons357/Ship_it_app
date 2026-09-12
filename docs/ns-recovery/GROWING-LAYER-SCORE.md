# Growing-layer family — scored on this book

**Date:** 12 September 2026  
**Review paste** cited commit `213e103` (grow-\(s\) print). The two derivations were **not** on that commit.

They later landed on the PR #24 tip as
`docs/LEMMA-STAR-GROWING-LAYER.md` and
`docs/ATTACK-9D-FULL-SUPPORT-BOUND.md`
(math/ copies are pointers). Audit:
`results/pr24_closure_review/audit.json`.

This book built the family on [`scripts/ns_lemma_star_core.py`](../../scripts/ns_lemma_star_core.py) and scored it independently.

**NS is not solved.** This is a counterexample to the **instantaneous** uniform bound, not a singular Navier–Stokes solution.

---

## Unrestricted Lemma★ — killed as a uniform bound

The family (mean-zero, real, divergence-free, finite Fourier support, \(D_s>0\)):

\[
\psi=\cos x+\cos(x+y)+\cos(2x+y),\quad
U=(-\psi_y,\psi_x),\quad
D_n(z)=\sum_{|j|\le n}e^{ijz},
\]
\[
v_n=D_n(z)\,(U_1(nx,ny),U_2(nx,ny),0).
\]

Locked core, \(n=1\ldots 8\):

| \(n\) | modes | \(E\) | \(N\) | \(T_c\) | \(\mathcal R_\star\) |
|---:|---:|---:|---:|---:|---:|
| 1 | 18 | 12 | 0 | 21 | 0.00139835966004 |
| 2 | 30 | 20 | 0 | 1824 | 0.00257488868862 |
| 3 | 42 | 28 | 0 | 26973 | 0.00377182539806 |
| 4 | 54 | 36 | 0 | 187392 | 0.00497285126300 |
| 5 | 66 | 44 | 0 | 853125 | 0.00617551098155 |
| 6 | 78 | 52 | 0 | \(2.96266\times10^6\) | 0.00737902364620 |
| 8 | 102 | 68 | 0 | \(2.1332\times10^7\) | 0.00978740288136 |

Rows \(n=1\ldots4\) **match** the review’s PR #24 `stokes_moments` table. \(T_c\) matches \(3n^5(3n^2+3n+1)\). Div-free and reality residuals are \(0\). \(\mathcal R_\star/n\) is falling toward \(\approx0.00121\), consistent with the claimed positive asymptotic.

The elementary comparison \(T_c\ge9n^7\), \(E\le12n\), \(Y\le36n^4 E\), \(D_s\le216n^6 E\) gives
\[
\mathcal R_\star(v_n)\ge\frac{n}{165888}\to\infty.
\]
Any proposed finite \(C_{\mathrm{geom}}\) fails for integer \(n>165888\,C_{\mathrm{geom}}\).

**Stamp on this book:** unrestricted
\[
\sup_v\mathcal R_\star(v)<\infty
\]
is **false**. Lemma★ as one geometry-only constant for every divergence-free field is **dead**. Kill lane for that statement has succeeded.

Specialist review should still check the closed-form derivation of \(T_c=3n^5(3n^2+3n+1)\) on paper. The evaluator match does not replace a proof-assistant check. The identity is confirmed here for \(n=1\ldots8\).

This family is **not** a uniform dilation of one field. It is **not** exact-shell. Do **not** merge with ABC_λ or with grow-\(s\).

---

## Exact-shell 9D bound — not stamped here

The review claims
\[
\|\Pi_\beta B(w,w)\|_2\le\frac43\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2
\quad(Aw=\alpha w),\qquad
K_{\alpha,\beta}\le\frac{16}{9}.
\]

The writeup now sits on the PR #24 tip. **That page itself says CLAIMED, specialist pending** — not proved. This book agrees and does **not** stamp \(C=4/3\).

The audit prints a few exact-shell \(K\) values and three weighted-count ratios \(\le 3\). Those are checks, not the lattice theorem. Finite samples (\(K\approx0.641\), \(K\approx0.456\)) sit below \(16/9\) and do not prove it.

Exact-shell 9D and unrestricted ★ are **distinct**. The growing-layer family does not live on one shell, so it does not touch that coefficient question.

---

## What this does to the rest of the desk

| Item | Status |
|---|---|
| Unrestricted ★ / finite \(C_{\mathrm{geom}}\) | **Dead** (this family) |
| Need★ signed dual as a repair of that same bound | **Cannot repair** unless hypotheses change |
| Exact-shell 9D / \(\sup K<\infty\) | **Not stamped.** Still a different statement |
| Grow-\(s\) draw / aligned 9B | Historical finite samples. Do not merge |
| Unaugmented regularity / Clay | **Open.** Needs a replacement closure ([`REPLACEMENT-CLOSURE.md`](REPLACEMENT-CLOSURE.md)). No blowup constructed |
| Soft X | Silent |
| ABC_λ SuperGrok falsifier | Still refused as *that* stamp. This is a different family |

Evaluator: [`scripts/growing_layer_counterexample.py`](../../scripts/growing_layer_counterexample.py)  
JSON: [`results/growing_layer.json`](../../results/growing_layer.json)

**NS not solved.**
