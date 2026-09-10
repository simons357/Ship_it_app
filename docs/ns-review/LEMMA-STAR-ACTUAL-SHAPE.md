# Lemma★ — full shape statement (canonical SoT)

**NS not solved.** Lemma★ is **OPEN**. This card is the **authoritative full Lemma★ shape statement**. It supersedes prior shape cards.

**Companion (pointer + same boxes):** [`docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`](../math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md)

**Refusal:** Near-shell \(K_{\alpha,\beta}\) tests **only a restricted limiting family**. Do **not** claim \(K_{\alpha,\beta}=\) full ★.

---

## Setup / symbols

For nonzero, mean-zero, divergence-free \(v\) on \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\):

\[
A=-P\Delta,\qquad B(v,v)=P[(v\cdot\nabla)v],
\]
\[
E=\|v\|_2^2,\quad X=\|A^{1/2}v\|_2^2,\quad Y=\|Av\|_2^2,\quad Z=\|A^{3/2}v\|_2^2,\qquad \Lambda=Y/X.
\]
\[
D_s=Z-\frac{Y^2}{X}=\|(A-\Lambda)A^{1/2}v\|_2^2,\qquad
T_c=-\langle B(v,v),A(A-\Lambda)v\rangle.
\]

(Note: when the triad moments \(M,N\) exist, \(T_c=M-\Lambda N\) is equivalent to the inner-product form above.)

Positive part: \(T_c_+=\max(T_c,0)\).

---

## Exact shape form of Lemma★

\[
\boxed{
\exists\,C_{\mathrm{geom}}<\infty\quad\forall\,v\in C^\infty_{\mathrm{div},0}(\mathbb{T}^3)\setminus\{0\}:\quad
\bigl(T_c(v)_+\bigr)^2\le C_{\mathrm{geom}}\,D_s(v)\,\|v\|_2^2\,Y(v).
}
\]

Constant depends only on fixed geometry/normalization — **not** on amplitude, Fourier support, shell count, or viscosity.

Equivalently, for \(D_s>0\):

\[
\boxed{
\sup_v\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}<\infty.
}
\]

For \(D_s=0\): field on one shell and \(T_c=0\).

---

## Viscosity packaging (\(0<\theta<1\))

\[
T_c(u)\le\theta\nu D_s(u)+C_0(\theta)\nu^{-1}\|u\|_2^2 Y(u),\qquad C_{\mathrm{geom}}=4\theta C_0(\theta).
\]

---

## This is the full lemma

**This is the full lemma.** Near-shell \(K_{\alpha,\beta}\) tests only a restricted limiting family.

Code name for the decisive quotient (when \(D_s\|v\|_2^2 Y>0\)): **`ratio_R_star_shape`**. Do **not** use legacy **`ratio_star`** \(=T_c/(E X\Lambda)\) — different packaging.

---

**NS not solved.**
