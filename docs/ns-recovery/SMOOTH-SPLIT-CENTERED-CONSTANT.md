# Finite universal centered constant — smooth-split derivation

**2 October 2026.** Instantaneous estimate on real mean-zero
divergence-free finite Fourier fields on the fixed \(2\pi\)
three-torus, normalized Haar measure. Symmetric orthogonal
Galerkin projections, \(A=-P\Delta\) (equals \(-\Delta\) on this
class), \(B=P_R P((u\cdot\nabla)u)\).

This is **not** a proof of global NSE regularity. It is **not**
unrestricted Lemma★. Unrestricted \(\sup\mathcal R_\star<\infty\)
stays **KILLED**. The cutoff-uniform gradient time budget stays
**OPEN**. Soft X silent. Ordinary NS is not solved.

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local-★ / 71E / 83 packets. Does **not** stamp
\(r\sim\kappa^{-1/2}\). Localized bump is not on this tree.

Machine: `scripts/da_gate_smooth_split_centered_constant.py`.
JSON: `results/da_gate_smooth_split_centered_constant.json`.
Desk card:
[`../../packets/DA-GATE-SMOOTH-SPLIT-CENTERED-CONSTANT-2026-10-02.md`](../../packets/DA-GATE-SMOOTH-SPLIT-CENTERED-CONSTANT-2026-10-02.md).
Clock: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Defs: [`../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
1 Oct scoring:
[`TC-L3-SQRT-YDS.md`](TC-L3-SQRT-YDS.md).

---

## What is proved, and what is not

Write \(E_0=\|u\|_2^2\), \(X=\|\nabla u\|_2^2\), \(Y=\|Au\|_2^2\),
\(Z=\|\nabla Au\|_2^2\), \(\Lambda=Y/X\) for \(X>0\),
\(N=-\langle Au,B\rangle\), \(M=-\langle A^2u,B\rangle\),
\(T_c=M-\Lambda N\), \(D_s=Z-\Lambda Y\), \(g=\|\nabla u\|_3\).
These are the locked moments (\(X=\|A^{1/2}u\|_2^2\),
\(Z=\|A^{3/2}u\|_2^2\)). \(C_s\) is a fixed-torus mean-zero Sobolev
constant \(\|f\|_6\le C_s\|\nabla f\|_2\), used for vectors and
Frobenius gradient tensors. Componentwise Sobolev and Minkowski
supply the same tensor extension.

**Theorem.** Choose a fixed smooth \(\chi\) on \([0,\infty)\),
\(0\le\chi\le 1\), with \(\chi=1\) on \([0,1/4]\) and \(\chi=0\) on
\([1/2,\infty)\). Put \(\varphi(\xi)=\chi(|\xi|^2)\) and

\[
K(x)=(2\pi)^{-3}\int_{\mathbb R^3}e^{ix\cdot\xi}\varphi(\xi)\,d\xi.
\]

Let \(M_{\mathrm{mult}}=1+\int_{\mathbb R^3}|K(x)|\,dx\), a finite
fixed number. Then, independently of the field and Galerkin cutoff,

\[
\lvert\Lambda N\rvert
\le
(4+6M_{\mathrm{mult}})\,C_s\,g\sqrt{YD_s},
\qquad
\lvert T_c\rvert
\le
(7+6M_{\mathrm{mult}})\,C_s\,g\sqrt{YD_s}.
\]

This proves existence of a finite \(C\) under these fixed-domain
conventions. It does not compute an optimized decimal \(C\) or
identify the smallest \(C\). The earlier exact witness \(C>0.4\) is
**REPORTED** from this handoff and was **not recovered** on the
seated families (largest seated quotient \(\approx 0.168\) on the
note triad). Under physical domain rescaling with
normalized-volume norms the constant scales with domain length.

**Not proved.** Cutoff-uniform \(\int g^2\,dt\). DA-NS-2.
Global NSE regularity. Unrestricted \(\sup\mathcal R_\star<\infty\).
A numerical value of \(M_{\mathrm{mult}}\) or \(C_s\).

The 1 Oct candidate \((\dagger)\) is this estimate. Its OPEN status
as a mere attack is replaced here by the written derivation for
the stated class. A script run verifies the coefficient
inequalities, the constant arithmetic, and the six-mode
illustration. The argument below is the reviewable mathematical
basis. Bot agreement is not a substitute for that argument.

---

## Proof

### 1. Centering

Set \(w=(A-\Lambda)u\). Parseval gives \(\|\nabla w\|_2^2=D_s\ge 0\).
The product-rule identity is

\[
T_c-\Lambda N
=
-\bigl\langle w,\,(Au\cdot\nabla)u\bigr\rangle
+2\sum_j\bigl\langle w,\,(\partial_ju\cdot\nabla)\partial_ju\bigr\rangle.
\]

Transport cancellation uses \(\mathrm{div}\,u=0\). Projection
removal is valid because the test fields are retained,
divergence-free Fourier fields. Sobolev and Hölder with exponents
\(6,2,3\) give

\[
\lvert T_c-\Lambda N\rvert
\le
3\,C_s\,g\sqrt{YD_s}.
\]

For the second term, Cauchy on the sum over \(j\) bounds the
pointwise product by \(\lvert\nabla u\rvert\,\lvert\mathrm{Hess}\,u\rvert\).
On the torus \(\|\mathrm{Hess}\,u\|_2=\|Au\|_2\).

### 2. Smooth split

Let \(v=\chi(A/\Lambda)u\) and \(h=u-v\). The support of \(v\) has
squared frequency \(s\le\Lambda/2\); \(h\) vanishes for
\(s\le\Lambda/4\). Both fields remain mean-zero, real, and
divergence-free, and stay inside the original cutoff.
Coefficientwise,

\[
\Lambda\|\nabla v\|_2\le 2\sqrt{D_s},
\qquad
\Lambda\|h\|_2\le 4\sqrt{Y},
\qquad
\|Ah\|_2\le\sqrt{Y},
\qquad
\|\nabla(A-\Lambda)h\|_2\le\sqrt{D_s}.
\]

The first uses \((s-\Lambda)^2\ge\Lambda^2/4\) on the low support
and \(\lvert\chi\rvert\le 1\). The second uses \(s^2\ge\Lambda^2/16\)
on the high support. The last two use \(\lvert 1-\chi\rvert\le 1\).

These four inequalities sit on the note triad, on \(v_1\), and on
the six-mode family below (machine: the same supports with a
\(C^0\) cutoff that matches \(\chi=1\) on \([0,1/4]\) and
\(\chi=0\) on \([1/2,\infty)\)).

### 3. Uniform \(L^3\) multiplier bound

\(\varphi\) is smooth and compactly supported, so \(K\) is rapidly
decreasing and has finite \(L^1\) norm. With \(L=\sqrt{\Lambda}\),
the normalized torus convolution kernel of \(\chi(A/\Lambda)\) is

\[
K_L^{\mathrm{tor}}(x)
=
(2\pi)^3\sum_{m\in\mathbb Z^3}L^3 K\bigl(L(x+2\pi m)\bigr).
\]

Its \(k\)th Fourier coefficient is \(\varphi(k/L)\). Its \(L^1\)
norm under normalized Haar measure is at most \(\int_{\mathbb R^3}|K|\),
by periodization and scaling. Young’s inequality, also for
finite-dimensional tensor values, gives

\[
\|\nabla h\|_3
\le
M_{\mathrm{mult}}\,\|\nabla u\|_3
=
M_{\mathrm{mult}}\,g.
\]

The bound is independent of \(L\), hence of \(\Lambda\), the field,
and \(R\). No sharp Fourier-ball projector \(L^3\) bound is assumed.
The smooth split acts on an already truncated field and commutes
with its projector. The \(1\) in \(M_{\mathrm{mult}}=1+\int|K|\) is
\(\|\nabla u\|_3+\|\nabla v\|_3\) via \(h=u-v\).

### 4. Mixed stretching terms

For divergence-free \(u\), integration by parts gives
\(N(u)=F(u,u,u)\) with

\[
F(a,b,c)
=
-\sum_{i,j,\ell}\int
(\partial_ja_i)(\partial_jb_\ell)(\partial_\ell c_i).
\]

The contraction obeys \(\lvert\mathrm{integrand}\rvert\le\lvert\nabla a\rvert\,\lvert\nabla b\rvert\,\lvert\nabla c\rvert\).
Trilinearity gives exactly

\[
N(u)-N(h)=F(v,u,u)+F(h,v,u)+F(h,h,v).
\]

In each term assign the low gradient \(\nabla v\) to \(L^2\). Assign
the remaining gradients to \(L^3\) and \(L^6\). Sobolev gives
\(\|\nabla u\|_6\le C_s\sqrt{Y}\) and
\(\|\nabla h\|_6\le C_s\|Ah\|_2\le C_s\sqrt{Y}\). Consequently

\[
\Lambda\lvert F(v,u,u)\rvert\le 2C_s g\sqrt{YD_s},
\qquad
\Lambda\lvert F(h,v,u)\rvert\le 2C_s g\sqrt{YD_s},
\qquad
\Lambda\lvert F(h,h,v)\rvert\le 2M_{\mathrm{mult}}C_s g\sqrt{YD_s}.
\]

Hence \(\Lambda\lvert N(u)-N(h)\rvert\le(4+2M_{\mathrm{mult}})C_s g\sqrt{YD_s}\).

### 5. All-high term

Energy cancellation for \(h\) gives \(\langle h,(h\cdot\nabla)h\rangle=0\).
Thus

\[
N(h)=-\bigl\langle(A-\Lambda)h,\,(h\cdot\nabla)h\bigr\rangle.
\]

The residual \((A-\Lambda)h\) is mean-zero, and its \(L^6\) norm is
at most \(C_s\sqrt{D_s}\). Hölder with exponents \(6,2,3\) therefore
gives

\[
\Lambda\lvert N(h)\rvert
\le
\Lambda\,C_s\sqrt{D_s}\,\|h\|_2\,\|\nabla h\|_3
\le
4M_{\mathrm{mult}}C_s g\sqrt{YD_s}.
\]

Steps 4 and 5 prove the \(\Lambda N\) estimate
\((4+2M_{\mathrm{mult}})+4M_{\mathrm{mult}}=4+6M_{\mathrm{mult}}\).
Adding step 1 proves the \(T_c\) estimate
\(3+(4+6M_{\mathrm{mult}})=7+6M_{\mathrm{mult}}\).

### 6. Degenerate cases

If \(D_s=0\) then \(\nabla w=0\); mean-zero gives \(w=0\). Energy
cancellation implies \(N=0\), and step 1 implies \(T_c=0\). If
\(X=0\), mean-zero \(u\) is zero; \(\Lambda\) is left undefined,
and the trivial zero field is treated separately.

---

## What this changes

The old unbounded \(\mathcal R_\star\) factor arose from applying
one bound to the entire velocity. Low gradients are paid by the
spectral residual, while high velocity amplitudes are paid by
\(Y/\Lambda^2\). The smooth split lets each term use the
appropriate payment, removing that factor.

Unrestricted \(\sup\mathcal R_\star<\infty\) used \(\sqrt{D_sEY}\)
and stays **KILLED** on \(v_n\). This estimate uses \(g\sqrt{YD_s}\)
and is a different sentence. No old energy-only inequality is
thereby repaired.

---

## What remains

Exact Galerkin dynamics imply

\[
(\log\Lambda)'
=
\frac{2}{Y}(T_c-\nu D_s)
\le
\frac{C^2 g^2}{2\nu},
\]

by AM-GM on \(T_c\le C g\sqrt{YD_s}\). That packaging sits. The
cutoff-uniform gradient time budget remains **unproved**. It is
not a consequence of the finite constant alone. Independently
proving this budget already gives enstrophy control through

\[
X'+\nu Y
\le
\frac{C_s^2}{\nu}g^2 X.
\]

Global NSE regularity and a complete full-PDE endpoint are **not**
established. DA-NS-2 stays **OPEN**.

A weaker sufficient criterion (budget reviewer): define

\[
F_X=2\bigl(C_s g\sqrt{\Lambda}-\nu\Lambda\bigr)_+.
\]

Classical \(\lvert N\rvert\le C_s g\sqrt{XY}\) implies
\((\log X)'\le F_X\). A cutoff-uniform integral of \(F_X\)
suffices to bound \(X\). Equivalently, on active times
\(g>\nu\sqrt{\Lambda}/C_s\),

\[
(\log X)'
\le
\frac{C_s^2 g^2}{2\nu}\,1_{\mathrm{active}}.
\]

These are proved implications, not independently paid budgets.
They identify the duration and intensity of growth-capable
intervals as the next question.

---

## Six-mode illustration

DA family, integer \(j\ge 3\):

\[
p=(1,0,0),\;
q=(j,j,0),\;
k=p+q,
\qquad
u_p=e_2,\;
u_q=j^{-1/2}e_3,\;
u_k=ij^{-1/2}e_3,
\]

and conjugates at the negatives. Exact \(N=-2(2j+1)\) sits.
\(D_s/(\Lambda Y)\sim 1/(4j)\) (machine: \(4j\cdot D_s/(\Lambda Y)\)
from \(1.07\) at \(j=3\) to \(1.04\) at \(j=12\)). The normalized
\(\lvert\Lambda N\rvert/(g\sqrt{YD_s})\) decreases
\(0.055\to 0.017\). \(T_c<0\) on this orientation, so
\(\mathcal R_\star=0\); the absolute quotients still fall. This
illustrates triad suppression inside the previously difficult
moment regime. The uniform proof supersedes the need to attack
that regime to establish mere finiteness of \(C\). Exact families
still inform sharpness.

No new estimate beyond the theorem is claimed. No continuation
criterion. **NS not solved.**
