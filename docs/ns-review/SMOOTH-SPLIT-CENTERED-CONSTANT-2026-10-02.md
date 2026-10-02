# Finite universal centered constant — smooth-split derivation

**Date:** 2 October 2026  
**Machine:** [`scripts/ns_attacks/smooth_split_constant.py`](../../scripts/ns_attacks/smooth_split_constant.py)  
**Lock:** Instantaneous estimate only. **★ NOT proved. NS NOT solved. Kill lane LIVE.**

This writes the 2 October smooth-split argument as a reviewable estimate
for a **finite** constant in

\[
\lvert T_c\rvert\le C\,g\sqrt{Y\,D_s},
\qquad g=\|\nabla u\|_3.
\]

It does **not** compute an optimized decimal \(C\). It does **not** pay
the cutoff-uniform time budget. It does **not** prove Lemma★ or global
Navier–Stokes regularity.

Do **not** splice this into Φ-renorm, DA-NS-2, or Clay Statement B.

---

## Scope

Real mean-zero divergence-free finite Fourier fields on the fixed
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), normalized Haar measure.
Symmetric orthogonal Galerkin projections. \(A=-\Delta\) (equals \(-P\Delta\)
on this class). \(B=P_R P((u\cdot\nabla)u)\). Inner products against
retained divergence-free test fields ignore the leftover projection.

\[
E_0=\|u\|_2^2,\quad
X=\|\nabla u\|_2^2,\quad
Y=\|Au\|_2^2,\quad
Z=\|\nabla Au\|_2^2.
\]
For \(X>0\): \(\Lambda=Y/X\), \(N=-\langle Au,B\rangle\),
\(M=-\langle A^2u,B\rangle\), \(T_c=M-\Lambda N\), \(D_s=Z-\Lambda Y\).

\(C_s\) is a fixed-torus mean-zero Sobolev constant
\(\|f\|_6\le C_s\|\nabla f\|_2\), taken to apply to vectors and
Frobenius tensors. \(C_s\) and \(M_{\mathrm{mult}}\) depend on the
domain length if the torus is rescaled; here the domain is fixed.

---

## Theorem (existence of finite \(C\))

Fix a smooth cutoff \(\chi\) on \([0,\infty)\) with \(0\le\chi\le 1\),
\(\chi=1\) on \([0,1/4]\), and \(\chi=0\) on \([1/2,\infty)\). Set
\(\varphi(\xi)=\chi(|\xi|^2)\) and

\[
K(x)=(2\pi)^{-3}\int_{\mathbb R^3}e^{ix\cdot\xi}\varphi(\xi)\,d\xi,
\qquad
M_{\mathrm{mult}}=1+\int_{\mathbb R^3}|K(x)|\,dx<\infty.
\]

Independently of the field and of the Galerkin cutoff,

\[
\lvert\Lambda N\rvert\le(4+6M_{\mathrm{mult}})C_s\,g\sqrt{Y D_s},
\qquad
\lvert T_c\rvert\le(7+6M_{\mathrm{mult}})C_s\,g\sqrt{Y D_s}.
\]

This is existence of a finite \(C=(7+6M_{\mathrm{mult}})C_s\) under
these conventions. The earlier exact witness \(C>0.4\) remains a
necessary lower bound. Machine near-shell \(\varepsilon=1/8\) gives
\(\lvert T_c\rvert/(g\sqrt{Y D_s})\approx 0.237\).

**Independent review.** The centering identity, the \(F\)-grouping, the
periodized kernel prefactor, projection removal, and the \(D_s=0\)
case were re-checked. Coefficient inequalities and the two identities
were machine-checked. Bot agreement is not the proof; the argument
below is.

---

## Proof

### 1. Centering

Set \(w=(A-\Lambda)u\). Parseval: \(\|\nabla w\|_2^2=D_s\ge 0\).
The product-rule identity (machine-checked on the locked triad)

\[
T_c-\Lambda N
=-\langle w,(Au\cdot\nabla)u\rangle
+2\sum_j\langle w,(\partial_j u\cdot\nabla)\partial_j u\rangle
\]

uses \(\operatorname{div}u=0\) and drops \(P\) against the retained
field \(w\). Hölder \(6,2,3\) and \(\|w\|_6\le C_s\|\nabla w\|_2\) give
\(\lvert\langle w,(Au\cdot\nabla)u\rangle\rvert\le C_s g\sqrt{Y D_s}\).
The Hessian term uses
\(\lvert\sum_j(\partial_j u\cdot\nabla)\partial_j u\rvert\le\lvert\nabla u\rvert\lvert\operatorname{Hess}u\rvert\)
and \(\|\operatorname{Hess}u\|_2=\|Au\|_2=\sqrt Y\) on the torus.
Thus

\[
\lvert T_c-\Lambda N\rvert\le 3 C_s\,g\sqrt{Y D_s}.
\]

### 2. Smooth split

\(v=\chi(A/\Lambda)u\), \(h=u-v\). Support of \(v\) has \(s\le\Lambda/2\);
\(h\) vanishes for \(s\le\Lambda/4\). Both stay real, mean-zero,
divergence-free, and inside the original cutoff. Using
\((s-\Lambda)^2\ge\Lambda^2/4\) on the low support and
\(s^2\ge\Lambda^2/16\) on the high support, together with
\(\lvert\chi\rvert\le 1\) and \(\lvert 1-\chi\rvert\le 1\),

\[
\Lambda\|\nabla v\|_2\le 2\sqrt{D_s},\qquad
\Lambda\|h\|_2\le 4\sqrt Y,\qquad
\|Ah\|_2\le\sqrt Y,\qquad
\|\nabla(A-\Lambda)h\|_2\le\sqrt{D_s}.
\]

Machine: these four inequalities hold on the spread triad, the
\(\varepsilon=1\) near-shell (where \(v=0\)), and the six-mode family.

### 3. Uniform \(L^3\) multiplier

\(\varphi\) is smooth and compactly supported, so \(K\) is Schwartz and
\(\|K\|_1<\infty\). With \(L=\sqrt\Lambda\), the normalized torus kernel
of \(\chi(A/\Lambda)\) is

\[
K_L^{\mathrm{tor}}(x)=(2\pi)^3\sum_{m\in\mathbb Z^3}L^3 K\bigl(L(x+2\pi m)\bigr).
\]

Its \(k\)-th Fourier coefficient is \(\varphi(k/L)\). Under normalized
Haar measure, \(\|K_L^{\mathrm{tor}}\|_1\le\int_{\mathbb R^3}|K|\) by
periodization and scaling (the \((2\pi)^3\) in the kernel cancels the
Haar factor \((2\pi)^{-3}\)). Young, including for finite-dimensional
tensors, gives

\[
\|\nabla h\|_3\le M_{\mathrm{mult}}\,g.
\]

Independent of \(L\), hence of \(\Lambda\), the field, and \(R\). No
sharp ball-projector \(L^3\) bound is used. The split acts on an already
truncated field and commutes with its projector.

A numerical \(L^1\) integral of the cubic \(C^1\) cutoff is only an
illustration that such kernels are integrable. The theorem uses a
smooth \(\chi\).

### 4. Mixed stretching

For divergence-free fields, integration by parts gives \(N(u)=F(u,u,u)\)
with

\[
F(a,b,c)
=-\sum_{i,j,\ell}\int(\partial_j a_i)(\partial_j b_\ell)(\partial_\ell c_i)\,d\mu.
\]

The integrand is bounded by \(\lvert\nabla a\rvert\lvert\nabla b\rvert\lvert\nabla c\rvert\).
Machine: \(N=F(u,u,u)\) on the locked triad (exactly \(N=2\)) and
\(N=-2(2j+1)\) on the six-mode family. Trilinearity gives exactly

\[
N(u)-N(h)=F(v,u,u)+F(h,v,u)+F(h,h,v)
\]

(machine on the six-mode field). Assign \(\nabla v\) to \(L^2\). The
remaining gradients go to \(L^3\) and \(L^6\). Then
\(\|\nabla u\|_6\le C_s\sqrt Y\) and \(\|\nabla h\|_6\le C_s\|Ah\|_2\le C_s\sqrt Y\),
so

\[
\Lambda\lvert F(v,u,u)\rvert\le 2 C_s g\sqrt{Y D_s},\quad
\Lambda\lvert F(h,v,u)\rvert\le 2 C_s g\sqrt{Y D_s},\quad
\Lambda\lvert F(h,h,v)\rvert\le 2 M_{\mathrm{mult}} C_s g\sqrt{Y D_s}.
\]

(The middle term uses \(\|\nabla h\|_6\), not \(\|\nabla h\|_3\).)
Hence \(\Lambda\lvert N(u)-N(h)\rvert\le(4+2M_{\mathrm{mult}})C_s g\sqrt{Y D_s}\).

### 5. All-high term

Energy cancellation on \(h\) gives \(\langle h,(h\cdot\nabla)h\rangle=0\), so
\(N(h)=-\langle(A-\Lambda)h,(h\cdot\nabla)h\rangle\). Hölder \(6,2,3\) and
\(\|(A-\Lambda)h\|_6\le C_s\sqrt{D_s}\) yield

\[
\Lambda\lvert N(h)\rvert
\le\Lambda C_s\sqrt{D_s}\,\|h\|_2\,\|\nabla h\|_3
\le 4 M_{\mathrm{mult}} C_s g\sqrt{Y D_s}.
\]

Adding step 4 proves the \(\Lambda N\) bound. Adding step 1 proves the
\(T_c\) bound: \(3+(4+6M_{\mathrm{mult}})=7+6M_{\mathrm{mult}}\).

### 6. Degenerate cases

If \(D_s=0\) then \(\nabla w=0\); mean-zero gives \(w=0\). Energy
cancellation gives \(N=0\), and step 1 gives \(T_c=0\). Machine: a
pure \(\lambda=1\) shell has \(D_s=N=T_c=0\). If \(X=0\), mean-zero
\(u\) is zero and \(\Lambda\) is left undefined.

---

## What this changes

Yesterday’s amplitude-homogeneous *candidate*
\(\lvert T_c\rvert\le C g\sqrt{Y D_s}\) is now a **proved existence
statement** for the stated class. The killed bound
\(\lvert T_c\rvert\le C g\sqrt{D_s}\) (no \(Y\)) stays killed.

The old unbounded \(R_{\mathrm{spread}}\) factor came from paying every
gradient with the same estimate. The split lets low gradients be paid
by \(D_s\) and high amplitudes by \(Y/\Lambda^2\).

This does **not** prove Lemma★. The shape quotient is still

\[
\mathcal R_\star=\frac{(T_c)_+^2}{D_s\,\|v\|_2^2\,Y}.
\]

The new estimate says \(T_c^2\le C^2 g^2 Y D_s\), which would imply ★
only if \(g^2/\|v\|_2^2\) were uniformly bounded — it is not.

---

## What remains OPEN

Exact Galerkin dynamics still give

\[
(\log\Lambda)'=\frac{2}{Y}(T_c-\nu D_s)\le\frac{C^2 g^2}{2\nu}
\]

once the estimate is in. The **cutoff-uniform** integral of \(g^2\) is
not a consequence of a finite \(C\). Independently, enstrophy satisfies
the weaker sufficient bound

\[
X'+\nu Y\le\frac{C_s^2}{\nu}g^2 X.
\]

Define \(F_X=2(C_s g\sqrt\Lambda-\nu\Lambda)_+\). Then
\((\log X)'\le F_X\). A cutoff-uniform integral of \(F_X\) would bound
\(X\). Equivalently, on active times \(g>\nu\sqrt\Lambda/C_s\),

\[
(\log X)'\le\frac{C_s^2 g^2}{2\nu}\,1_{\mathrm{active}}.
\]

These are proved implications, not paid budgets. Duration and intensity
of growth-capable intervals are the next question.

Global NSE regularity and a full-PDE endpoint are **not** established.

---

## Six-mode family (sharpness, not finiteness)

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
plus conjugates. Machine: \(N=-2(2j+1)\) exactly,
\(D_s/(\Lambda Y)\sim 1/(4j)\), and the normalized
\(\lvert\Lambda N\rvert/(g\sqrt{Y D_s})\) **decreases** in \(j\).
\(T_c<0\) on this family, so \(\mathcal R_\star=0\) (compression; not a
★ kill). The uniform proof supersedes attacking this regime for mere
finiteness of \(C\). Exact families still inform sharpness.

---

## How to rerun

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/smooth_split_constant.py \
  --out data/smooth_split_constant_2026-10-02.json
python3 -m unittest tests.test_smooth_split_constant tests.test_centered_flux_q3
```

`ns_solved` is false. `lemma_star_proved` is false. `global_regularity` is false.
