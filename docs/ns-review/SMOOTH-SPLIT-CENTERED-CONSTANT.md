# Finite universal centered constant — smooth-split derivation

**Date:** 2 October 2026  
**Status of the instantaneous estimate:** existence of a finite \(C\) is **proved** for the class below.  
**Status of Navier–Stokes:** **NOT** established. The cutoff-uniform gradient time budget remains **OPEN**.

This note transcribes the reviewable derivation. Bot agreement is not a proof; the argument below is the basis. An optimized decimal \(C\) is not computed. A prior exact witness \(C>0.4\) remains a necessary lower bound.

---

## Scope

Real, mean-zero, divergence-free **finite Fourier** fields on the fixed \(2\pi\) three-torus, **normalized Haar measure**. Symmetric orthogonal Galerkin projections,

\[
A=-\Delta,\qquad
B=P_R\mathbb P\bigl((u\cdot\nabla)u\bigr).
\]

On this class \(A=-P\Delta\) agrees with \(-\Delta\). This is an **instantaneous** estimate, not a proof of global regularity.

\[
E_0=\|u\|_2^2,\quad
X=\|\nabla u\|_2^2,\quad
Y=\|Au\|_2^2,\quad
Z=\|\nabla Au\|_2^2.
\]

For \(X>0\): \(\Lambda=Y/X\), \(N=-\langle Au,B\rangle\), \(M=-\langle A^2u,B\rangle\),
\(T_c=M-\Lambda N\), \(D_s=Z-\Lambda Y\). Write \(g=\|\nabla u\|_3\).

\(C_s\) is a fixed-torus mean-zero Sobolev constant \(\|f\|_6\le C_s\|\nabla f\|_2\), applied to vectors and gradient tensors with Frobenius norms (componentwise Sobolev + Minkowski).

---

## Theorem

Fix a smooth cutoff \(\chi\) on \([0,\infty)\) with \(0\le\chi\le 1\), \(\chi=1\) on \([0,1/4]\), and \(\chi=0\) on \([1/2,\infty)\). Set \(\varphi(\xi)=\chi(|\xi|^2)\) and

\[
K(x)=(2\pi)^{-3}\int_{\mathbb R^3}e^{ix\cdot\xi}\varphi(\xi)\,d\xi.
\]

Let \(M_{\mathrm{mult}}=1+\int_{\mathbb R^3}|K(x)|\,dx\), a finite fixed number. Then, independently of the field and Galerkin cutoff,

\[
|\Lambda N|
\le
(4+6M_{\mathrm{mult}})\,C_s\,g\sqrt{Y D_s},
\qquad
|T_c|
\le
(7+6M_{\mathrm{mult}})\,C_s\,g\sqrt{Y D_s}.
\]

This proves existence of a finite \(C\) under these fixed-domain conventions. Under physical domain rescaling with normalized-volume norms the constant scales with domain length. No old unrelated constant or killed energy-only inequality is repaired.

---

## Proof

### 1. Centering

Set \(w=(A-\Lambda)u\). Parseval gives \(\|\nabla w\|_2^2=D_s\ge 0\). The product-rule identity is

\[
T_c-\Lambda N
=
-\langle w,(Au\cdot\nabla)u\rangle
+
2\sum_j\langle w,(\partial_j u\cdot\nabla)\partial_j u\rangle.
\]

Transport cancellation uses \(\mathrm{div}\,u=0\). Projection removal is valid because the test fields are retained, divergence-free Fourier fields. Sobolev and Hölder with exponents \(6,2,3\) give

\[
|T_c-\Lambda N|\le 3\,C_s\,g\sqrt{Y D_s}.
\]

For the second term, Cauchy on the sum over \(j\) bounds the pointwise product by \(|\nabla u|\,|\mathrm{Hess}\,u|\). On the torus \(\|\mathrm{Hess}\,u\|_2=\|Au\|_2\).

### 2. Smooth split

Let \(v=\chi(A/\Lambda)u\) and \(h=u-v\). The support of \(v\) has squared frequency \(s\le\Lambda/2\); \(h\) vanishes for \(s\le\Lambda/4\). Both remain mean-zero, real, divergence-free, and inside the original cutoff. Coefficientwise,

\[
\Lambda\|\nabla v\|_2\le 2\sqrt{D_s},
\qquad
\Lambda\|h\|_2\le 4\sqrt{Y},
\qquad
\|Ah\|_2\le\sqrt{Y},
\qquad
\|\nabla(A-\Lambda)h\|_2\le\sqrt{D_s}.
\]

On the low support \((s-\Lambda)^2\ge\Lambda^2/4\) and \(|\chi|\le 1\). On the high support \(s^2\ge\Lambda^2/16\). The last two use \(|1-\chi|\le 1\).

### 3. Uniform \(L^3\) multiplier bound

\(\varphi\) is smooth and compactly supported, so \(K\) is rapidly decreasing and has finite \(L^1\) norm. With \(L=\sqrt{\Lambda}\), the normalized torus convolution kernel of \(\chi(A/\Lambda)\) is

\[
K_L^{\mathrm{tor}}(x)
=
(2\pi)^3\sum_{m\in\mathbb Z^3}L^3 K\bigl(L(x+2\pi m)\bigr).
\]

Its \(k\)th Fourier coefficient is \(\varphi(k/L)\). Its \(L^1\) norm under normalized Haar measure is at most \(\int_{\mathbb R^3}|K|\), by periodization and scaling. Young’s inequality (including finite-dimensional tensor values) gives

\[
\|\nabla h\|_3\le M_{\mathrm{mult}}\,g.
\]

The bound is independent of \(L\), hence of \(\Lambda\), the field, and \(R\). No sharp Fourier-ball projector \(L^3\) bound is assumed. The smooth split acts on an already truncated field and commutes with its projector.

### 4. Mixed stretching terms

For divergence-free \(u\), integration by parts gives \(N(u)=F(u,u,u)\) with

\[
F(a,b,c)
=
-\sum_{i,j,\ell}\int
(\partial_j a_i)(\partial_j b_\ell)(\partial_\ell c_i).
\]

The contraction obeys \(|\mathrm{integrand}|\le|\nabla a|\,|\nabla b|\,|\nabla c|\). Trilinearity gives

\[
N(u)-N(h)=F(v,u,u)+F(h,v,u)+F(h,h,v).
\]

Assign the low gradient \(\nabla v\) to \(L^2\). Assign the remaining gradients to \(L^3\) and \(L^6\). Sobolev gives \(\|\nabla u\|_6\le C_s\sqrt{Y}\) and \(\|\nabla h\|_6\le C_s\|Ah\|_2\le C_s\sqrt{Y}\). Consequently

\[
\begin{aligned}
\Lambda|F(v,u,u)|&\le 2\,C_s\,g\sqrt{Y D_s},\\
\Lambda|F(h,v,u)|&\le 2\,C_s\,g\sqrt{Y D_s},\\
\Lambda|F(h,h,v)|&\le 2M_{\mathrm{mult}}\,C_s\,g\sqrt{Y D_s}.
\end{aligned}
\]

(The middle term pays \(\nabla h\) in \(L^6\) by \(Ah\), so it does not carry \(M_{\mathrm{mult}}\).) Hence

\[
\Lambda|N(u)-N(h)|\le(4+2M_{\mathrm{mult}})C_s\,g\sqrt{Y D_s}.
\]

### 5. All-high term

Energy cancellation for \(h\) gives \(\langle h,(h\cdot\nabla)h\rangle=0\), so

\[
N(h)=-\langle(A-\Lambda)h,(h\cdot\nabla)h\rangle.
\]

The residual \((A-\Lambda)h\) is mean-zero, and its \(L^6\) norm is at most \(C_s\sqrt{D_s}\). Hölder with exponents \(6,2,3\) gives

\[
\Lambda|N(h)|
\le
\Lambda\,C_s\sqrt{D_s}\,\|h\|_2\,\|\nabla h\|_3
\le
4M_{\mathrm{mult}}\,C_s\,g\sqrt{Y D_s}.
\]

Steps 4 and 5 give the \(\Lambda N\) estimate. Adding step 1 gives the \(T_c\) estimate:

\[
(4+6M_{\mathrm{mult}})+3=7+6M_{\mathrm{mult}}.
\]

### 6. Degenerate cases

If \(D_s=0\) then \(\nabla w=0\); mean-zero gives \(w=0\). Energy cancellation implies \(N=0\), and step 1 implies \(T_c=0\). If \(X=0\), mean-zero \(u\) is zero; \(\Lambda\) is left undefined, and the zero field is treated separately.

---

## What this changes

The old unbounded \(R_{\mathrm{spread}}\) factor came from applying one bound to the entire velocity. Low gradients are paid by the spectral residual; high velocity amplitudes are paid by \(Y/\Lambda^2\). The smooth split lets each term use the appropriate payment.

The small-case board in [`SQRT-ESTIMATE-SMALL-CASE.md`](./SQRT-ESTIMATE-SMALL-CASE.md) remains a **sharpness / identity** board. It no longer carries an OPEN existence question for \(C\).

---

## What remains OPEN

Exact Galerkin dynamics imply

\[
(\log\Lambda)'=\frac{2(T_c-\nu D_s)}{Y}\le\frac{C^2 g^2}{2\nu}.
\]

The cutoff-uniform gradient time budget is **not** a consequence of the finite constant alone. Independently proving that budget already gives enstrophy control through

\[
X'+\nu Y\le\frac{C_s^2}{\nu}g^2 X.
\]

A weaker sufficient criterion (budget reviewer):

\[
F_X=2\bigl(C_s g\sqrt{\Lambda}-\nu\Lambda\bigr)_+,
\qquad
(\log X)'\le F_X.
\]

A cutoff-uniform integral of \(F_X\) would bound \(X\). Equivalently, on active times \(g>\nu\sqrt{\Lambda}/C_s\),

\[
(\log X)'\le\frac{C_s^2 g^2}{2\nu}\,1_{\mathrm{active}}.
\]

These are **proved implications**, not independently paid budgets. Duration and intensity of growth-capable intervals are the next question.

**Global NSE regularity and a complete full-PDE endpoint are not established.**

---

## Six-mode family

\[
p=(1,0,0),\;
q=(j,j,0),\;
k=p+q,\quad j\ge 3,
\]

\[
u_p=e_2,\quad
u_q=j^{-1/2}e_3,\quad
u_k=i\,j^{-1/2}e_3,
\]

plus conjugates. Exact Fourier arithmetic on perfect-square \(j\) verifies

\[
N=-2(2j+1)
\]

and the linear-moment law \(D_s/(\Lambda Y)\sim 1/(4j)\). The normalized \(\Lambda N\) quotient **decreases** with \(j\) (square-\(j\) samples: \(\lvert\Lambda N\rvert/\sqrt{YD_s}\) from \(\approx 0.30\) at \(j=4\) to \(\approx 0.12\) at \(j=36\)). That is triad suppression inside the old large-\(R_{\mathrm{spread}}\) moment regime. The smooth-split proof supersedes attacking that regime to get mere finiteness of \(C\); exact families still inform sharpness.

---

## Local coefficient check (this filing)

Checked here, not a substitute for the product-rule identity in §1:

- Low-support bound \(\Lambda\|\nabla v\|_2\le 2\sqrt{D_s}\) from \((s-\Lambda)^2\ge\Lambda^2/4\).
- High-support bound \(\Lambda\|h\|_2\le 4\sqrt{Y}\) from \(s^2\ge\Lambda^2/16\).
- Mixed-term assembly \(2+2+2M_{\mathrm{mult}}=4+2M_{\mathrm{mult}}\).
- Plus all-high \(4M_{\mathrm{mult}}\) gives \(4+6M_{\mathrm{mult}}\).
- Plus centering \(3\) gives \(7+6M_{\mathrm{mult}}\).
- Degenerate \(D_s=0\) forces \(T_c=N=0\) on this class (already in the identity suite).
- Six-mode \(N=-2(2j+1)\) on \(j=4,9,16,25,36\).

\(C_s\) and \(M_{\mathrm{mult}}\) are not evaluated numerically in this repository.

---

## Runtime

```bash
python3 scripts/ns_attacks/smooth_split_board.py
python3 -m unittest tests.test_smooth_split_constant tests.test_sqrt_estimate_attack -v
```

---

## Do not glue

- Instantaneous finite \(C\) \(\neq\) paid \(\int g^2\) budget \(\neq\) enstrophy bound \(\neq\) Clay Statement B.
- Lemma★ / \(\mathcal R_\star\) is a different quotient. This note does not green ★.
- Φ-renorm swirl algebra is a different book.
