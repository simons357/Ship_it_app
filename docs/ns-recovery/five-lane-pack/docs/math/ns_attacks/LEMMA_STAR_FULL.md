# Lemma★ — the full statement (shape form)

**Date:** 10 September 2026  
**Status:** **OPEN.** This locks the lemma. It does **not** prove it. **NS is not solved.**

This is the **full lemma**. The near-shell quantity \(K_{\alpha,\beta}\) tests only a **restricted limiting family**. It is not a substitute for ★.

---

For a nonzero, mean-zero, divergence-free field \(v\) on the normalized torus
\[
\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
\]
set
\[
A=-P\Delta,\qquad
B(v,v)=P[(v\cdot\nabla)v],
\]
\[
E=\|v\|_2^2,\qquad
X=\|A^{1/2}v\|_2^2,\qquad
Y=\|Av\|_2^2,\qquad
Z=\|A^{3/2}v\|_2^2,\qquad
\Lambda=\frac{Y}{X}.
\]
Define
\[
D_s
=Z-\frac{Y^2}{X}
=\|(A-\Lambda)A^{1/2}v\|_2^2,
\]
\[
T_c
=-\bigl\langle B(v,v),\,A(A-\Lambda)v\bigr\rangle.
\]

**Exact shape form of Lemma★:**
\[
\exists\,C_{\mathrm{geom}}<\infty
\quad\forall\,v\in C^\infty_{\mathrm{div},0}(\mathbb T^3)\setminus\{0\}:
\]
\[
\boxed{
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,
\|v\|_2^2\,
Y(v)
}
\]
with \(T_c_+=\max(T_c,0)\). The constant depends only on the **fixed geometry and normalization** — not on amplitude, Fourier support, shell count, or viscosity.

Equivalently, for \(D_s>0\),
\[
\sup_v
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}
<\infty.
\]

For \(D_s=0\), the field lies on **one shell** and \(T_c=0\). (Then \(A(A-\Lambda)v=0\), so both sides of the inequality vanish. This is not a kill.)

For any fixed \(0<\theta<1\), the equivalent viscosity packaging is
\[
T_c(u)
\le
\theta\nu D_s(u)
+C_0(\theta)\,\nu^{-1}\|u\|_2^2\,Y(u),
\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta).
\]

Fourier / triad expansions that agree with these operator identities are in [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md). Code: `scripts/ns_attacks/stokes_moments.py`.

**NS not solved.**
