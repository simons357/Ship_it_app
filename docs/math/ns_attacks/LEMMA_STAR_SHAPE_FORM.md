# Lemma★ — shape form (pointer card)

**Canonical SoT (full statement):** [`docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md`](../../ns-review/LEMMA-STAR-ACTUAL-SHAPE.md)

**NS not solved.** Lemma★ is **OPEN**. This file mirrors the SoT boxes only; do not treat it as a second, competing lock.

**Refusal:** \(K_{\alpha,\beta}\) is **not** the full lemma — near-shell tests only a restricted limiting family.

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

(When \(M,N\) exist: \(T_c=M-\Lambda N\) is equivalent.)

---

## Exact shape form of Lemma★

\[
\boxed{
\exists\,C_{\mathrm{geom}}<\infty\quad\forall\,v\in C^\infty_{\mathrm{div},0}(\mathbb{T}^3)\setminus\{0\}:\quad
\bigl(T_c(v)_+\bigr)^2\le C_{\mathrm{geom}}\,D_s(v)\,\|v\|_2^2\,Y(v).
}
\]

\(T_c_+=\max(T_c,0)\). Constant depends only on fixed geometry/normalization — **not** on amplitude, Fourier support, shell count, or viscosity.

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

**This is the full lemma.** Near-shell \(K_{\alpha,\beta}\) tests only a restricted limiting family.

**NS not solved.**
