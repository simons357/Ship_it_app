# Replacement closure — after unrestricted Lemma★ is dead

**Date:** 12 September 2026  
**This book.** Unrestricted ★ is dead (`GROWING-LAYER-SCORE.md`).
This page is the live analytic job. It is **not** a theorem.

Ordinary Navier–Stokes regularity is **still open**.
This page does **not** construct a singular solution and does
**not** close Clay.

The score pasted on this turn is **confirmed**:
the two statements are distinct; unrestricted ★ is dead on \(v_n\);
exact-shell 9D is not stamped; Need★ cannot repair the old box;
specialist review of the paper derivations has not happened.

---

## What died

One finite geometric constant \(C_{\mathrm{geom}}\) such that

\[
\sup_v\mathcal R_\star(v)<\infty
\]

for **every** mean-zero divergence-free field on \(\mathbb T^3\)
(with \(D_s>0\)).

The growing-layer family \(v_n\) is admissible and
\(\mathcal R_\star(v_n)\to\infty\).

---

## What did not die

| Object | Status on this book |
|---|---|
| Exact-shell 9D coefficient \(K\le 16/9\) | **CLAIMED.** Writeup scored: [`ATTACK-9D-FULL-SUPPORT-SCORE.md`](ATTACK-9D-FULL-SUPPORT-SCORE.md). Occupancy gone on one input shell *if* it holds. **Not** a regularity close. |
| Finite \(K\) sweeps (aligned 9B, grow-\(s\)) | Historical. Not a universal constant. |
| Three-shear \(K_{1,2}=2/3\) | Write-up **floor** \(\sup K\ge 2/3\). Not \(C_0\), not \(16/9\). |
| Soft X, SND, Theorem H, Phi-renorm, Triple Lock, Route N/Q6, Domain Architect “five fingers” | **Still silent.** Do not glue. |
| Need★ signed dual as written | Cannot repair **this** unrestricted bound unless hypotheses or conclusion change. |

---

## Bounded aspect does not exclude \(v_n\)

An earlier draft of this page guessed that \(v_n\) had aspect
\(\lambda_{\max}/\lambda_{\min}\sim n^2\). That is **false**.

The occupied eigenvalues are
\[
\lambda=n^2|r|^2+j^2,\qquad
|r|^2\in\{1,2,5\},\qquad |j|\le n.
\]
Hence
\[
\lambda_{\min}=n^2,\qquad \lambda_{\max}=6n^2,\qquad
\frac{\lambda_{\max}}{\lambda_{\min}}=6
\]
for every integer \(n\ge 1\). Checked on the locked core
(`scripts/growing_layer_replacement_factors.py`).

A restriction “\(\lambda_{\max}/\lambda_{\min}\le R\)” for any
fixed \(R\ge 6\) **still contains** \(v_n\). It cannot restore
\[
\sup\mathcal R_\star<\infty
\]
on that class. The same ★ ratio on aspect-bounded fields is
already false.

Exact one-shell fields remain vacuous (\(D_s=0\), \(T_c=0\)).
Whether a **two-shell** (or other sparse-spectrum) class restores
a finite \(\sup\mathcal R_\star\) is a **new claim**. \(v_n\)
occupies \(\Theta(n)\) eigenvalues and is not two-shell.

---

## Extra-factor diagnostics — not a replacement theorem

On this family \(\mathcal R_\star(v_n)\) grows like \(n\).
Two homogeneous field functionals also grow like \(n\):

\[
\sqrt{\frac{X}{E}}=\frac{\|A^{1/2}v\|_2}{\|v\|_2},\qquad
\sqrt{\lambda_{\max}}.
\]

Their ratios on the evaluator sample do **not** climb with \(n\):

| \(n\) | shells | \(\mathcal R_\star\) | \(\mathcal R_\star\big/\sqrt{X/E}\) | \(\mathcal R_\star\big/\sqrt{\lambda_{\max}}\) |
|---:|---:|---:|---:|---:|
| 1 | 5 | 0.00139836 | 0.000665383 | 0.000570878 |
| 2 | 8 | 0.00257489 | 0.000624502 | 0.000525597 |
| 4 | 14 | 0.00497285 | 0.000609047 | 0.000507540 |
| 8 | 26 | 0.00978740 | 0.000602373 | 0.000499461 |

JSON: [`results/growing_layer_replacement_factors.json`](../../results/growing_layer_replacement_factors.json).

A **different** inequality of the form
\[
(T_c_+)^2
\le
C\,D_s\,E\,Y\,\sqrt{\frac{X}{E}}
\quad\text{or}\quad
C\,D_s\,E\,Y\,\sqrt{\lambda_{\max}}
\]
would be compatible with this family. That is **not proved**.
It is not “★ with a larger \(C_{\mathrm{geom}}\)”.
It has not been checked on any other family.
It is not known to be strong enough for a regularity closure.

Do **not** invent a Need★ dual whose only job is to restore the
dead box. If a signed dual is written, its hypotheses must be
stated first and checked on \(v_n\).

---

## What the regularity program needs

The unaugmented program used unrestricted ★ as closure.
That closure is gone. A new closure must:

- be an inequality that is **true** on every field it claims,
  including \(v_n\) if \(v_n\) is in the class;
- be strong enough, **if** one still wants a regularity theorem,
  to feed the existing energy/enstrophy estimates **without**
  smuggling SND / Soft X / Theorem H;
- be checked on the growing-layer family **before** it is sent
  as a kill or a close.

This book will not send Domain Architect a Clay/regularity close
from a guessed replacement.

**NS not solved.**
