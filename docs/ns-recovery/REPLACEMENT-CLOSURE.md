# Replacement closure — after unrestricted Lemma★ is dead

**Date:** 12 September 2026  
**This book.** Unrestricted ★ is dead (`GROWING-LAYER-SCORE.md`).
This page is the live analytic job. It is **not** a theorem.

Ordinary Navier–Stokes regularity is **still open**.
This page does **not** construct a singular solution and does
**not** close Clay.

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
| Exact-shell 9D coefficient \(K\le 16/9\) | **Not stamped.** Other book: CLAIMED, specialist pending. Different statement. \(v_n\) is not exact-shell. |
| Finite \(K\) sweeps (aligned 9B, grow-\(s\)) | Historical. Not a universal constant. |
| Soft X, SND, Theorem H, Phi-renorm, Triple Lock, Route N/Q6, Domain Architect “five fingers” | **Still silent.** Do not glue. |
| Need★ signed dual as written | Cannot repair **this** unrestricted bound unless hypotheses or conclusion change. |

---

## What a replacement must be

A replacement is a **different estimate**, or the **same ratio on
a strictly smaller class**. Examples of smaller classes (not
theorems):

1. **Exact one-shell fields.** Then \(D_s=0\) and \(T_c=0\).
   No ★ statement. The 9D coefficient is a **different** bound
   (\(B\)-norm, not \(\mathcal R_\star\)).
2. **Bounded eigenvalue aspect.** Fields whose occupied
   eigenvalues satisfy \(\lambda_{\max}/\lambda_{\min}\le R\)
   for a fixed \(R\). The family \(v_n\) has aspect
   \(\sim n^2\) and would be excluded. Whether \(\mathcal R_\star\)
   is then bounded is **open** and is a new claim.
3. **An extra moment in the denominator.** A bound of the form
   \((T_c_+)^2\le C\,D_s\,E\,Y\cdot\Phi\) with \(\Phi\) a
   documented higher moment (or \(\lambda_{\max}\) factor) that
   grows at least like \(n\) on \(v_n\). That is a **different
   inequality**. It is not “★ with a larger \(C_{\mathrm{geom}}\)”.

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

---

## Next concrete check (if anyone continues here)

Do **not** start H1 or 9C to save ★.

If the next page is a **restricted-class** claim, write the class
first, then evaluate \(\mathcal R_\star(v)\) only on that class.
If the next page is a **new inequality**, write the extra factor
and test it on \(v_n\) with `scripts/growing_layer_counterexample.py`.
