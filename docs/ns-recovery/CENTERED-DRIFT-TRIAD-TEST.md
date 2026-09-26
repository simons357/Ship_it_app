# Centered drift: first adversarial triad test

**Program:** Classical, unforced, unaugmented three-dimensional periodic Navier–Stokes.  
**Date:** 22 September 2026.  
**Status:** Internal analytic checkpoint. **Not a closure theorem** and not independently reviewed.

Evaluator lock: `scripts/centered_drift_triad_test.py` on
`scripts/ns_lemma_star_core.py`. The numbers in §4 match that core.
The centered equation stays [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Ordinary NS is not solved. Soft X silent.

---

## 1. Purpose

Unrestricted \(B^\star\) / \(\sup\mathcal R_\star<\infty\) has been
falsified on \(v_n\). The surviving route is the signed centered term

\[
T_c=M-\Lambda N
=-\langle B(u,u),A(A-\Lambda I)u\rangle,
\qquad
\Lambda=\frac{Y}{X},
\]

with

\[
X=|A^{1/2}u|_2^2,
\quad
Y=|Au|_2^2,
\quad
Z=|A^{3/2}u|_2^2,
\quad
D_s=Z-\frac{Y^2}{X}.
\]

This note is the next rejection test: what cancellation the centered
multiplier actually supplies on exact Fourier triads.

---

## 2. Fourier transfer formula

Normalized Haar / Plancherel as \(\sum_k|\widehat u(k)|^2\) (the locked
evaluator). For a real, mean-zero, divergence-free field,

\[
\widehat{B(u,u)}(k)
=iP_k\sum_{p+q=k}(q\cdot\widehat u(p))\widehat u(q).
\]

Modal energy transfer

\[
\tau_k=-\operatorname{Re}
\bigl(\overline{\widehat u(k)}\cdot\widehat{B(u,u)}(k)\bigr).
\]

Then \(N=\sum_k|k|^2\tau_k\), \(M=\sum_k|k|^4\tau_k\), and

\[
\boxed{T_c=\sum_k|k|^2(|k|^2-\Lambda)\tau_k.}
\tag{2.1}
\]

For each closed interacting triad, energy conservation gives
\(\tau_p+\tau_q+\tau_r=0\). Writing \(f_\Lambda(s)=s(s-\Lambda)\),

\[
T_c^{(p,q,r)}
=\bigl(f_\Lambda(|p|^2)-f_\Lambda(|r|^2)\bigr)\tau_p
+\bigl(f_\Lambda(|q|^2)-f_\Lambda(|r|^2)\bigr)\tau_q,
\]

where

\[
f_\Lambda(a)-f_\Lambda(b)=(a-b)(a+b-\Lambda).
\tag{2.2}
\]

The centered expression has a genuine spectral-gap factor after triad
symmetrization. Equation (2.2) supplies neither a sign nor a bound on
the fluxes \((\tau_p,\tau_q)\).

---

## 3. Exact-shell test

If \(u\) is supported on one exact Stokes eigenshell (\(Au=\alpha u\)),
then \(\Lambda=\alpha\) and \(A(A-\Lambda I)u=0\), so

\[
\boxed{T_c=0.}
\]

Exact and instantaneous. Navier–Stokes evolution generally creates new
shells immediately. Not an all-time closure mechanism.

---

## 4. A real near-scale triad with either sign

Take

\[
p=(1,0,0),\qquad q=(0,1,0),\qquad r=p+q=(1,1,0),
\]

with transverse polarizations \(a=(0,1,0)\), \(b=(1,0,1)\),
\(c=(0,0,1)\), and

\[
\widehat u(\pm p)=a,
\qquad
\widehat u(\pm q)=b,
\qquad
\widehat u(r)=-ic,
\qquad
\widehat u(-r)=ic.
\]

The field is real and divergence-free. Direct evaluation on the locked
core gives, for each conjugate pair,

\[
\tau_p=0,\qquad\tau_q=-1,\qquad\tau_r=1.
\]

Consequently

\[
X=10,\quad Y=14,\quad Z=22,\quad\Lambda=\frac75,\quad D_s=\frac{12}{5},
\]

\[
N=2,\qquad M=6,\qquad\boxed{T_c=\frac{16}{5}>0.}
\]

(The two conjugate pairs reconstruct \(T_c=2(f_\Lambda(1)-f_\Lambda(2))\tau_q\)
with \(\tau_q=-1\).) Changing \(u\) to \(-u\) leaves
\((X,Y,Z,\Lambda,D_s)\) unchanged and sends \(T_c\) to \(-16/5\).
Therefore:

1. the centered multiplier does not impose a universal favorable sign;
2. phase information matters;
3. a proof cannot replace signed transfer by an unsigned spectral-spread
   argument.

For this normalization, \(T_c^+/D_s=4/3\). Under \(u\mapsto su\) the
ratio becomes \((4/3)s\). Hence no amplitude-independent pure absorption

\[
T_c^+\le\theta\nu D_s
\]

can hold for every smooth divergence-free field with a fixed \(\theta\).
Any surviving estimate must include an additional coefficient or
remainder whose size and time integrability are proved from admissible
data.

---

## 5. Separated low-high triads

For an integer \(L\ge 2\), take

\[
p=(1,0,0),\qquad q=(0,L,0),\qquad r=(1,L,0),
\]

with the same \(a,b\). Let \(c_L\) be the unit vector in the direction
\(P_r\bigl((q\cdot a)b+(p\cdot b)a\bigr)\). Same phase choice as §4.
Direct triad evaluation on the locked core yields

\[
T_c\sim 2\sqrt{2}\,L^3,
\qquad
D_s\sim 2L^4,
\]

and therefore

\[
\boxed{\frac{T_c}{D_s}\sim\frac{\sqrt{2}}{L}.}
\tag{5.1}
\]

Checked at \(L=4,8,16\). This fixed-amplitude separated family is not
the primary obstruction to centered absorption: relative transfer
weakens as the separation grows. That does not prove a uniform
separated-frequency estimate. It directs the next attack toward
comparable-frequency interactions.

---

## 6. Decision

Mixed result.

**What fails**

- automatic favorable sign;
- universal pure absorption by \(D_s\);
- any argument that discards phases or takes absolute values before
  using triad conservation.

**What survives**

- exact cancellation on one eigenshell;
- a triad-symmetrized spectral-gap factor (2.2);
- relative suppression in the tested widely separated family;
- the possibility of a signed, time-integrated estimate with a
  quantitatively controlled remainder.

The surviving obstruction is the near-scale, comparable-frequency
signed transfer, consistent with the high-high near-scale packet that
falsified unrestricted \(\star\).

---

## 7. Next precise avenue

Derive the fully symmetrized coefficient for a general real triad and
split the centered drift into:

1. comparable-frequency triads;
2. separated low-high / high-low triads;
3. high-high to low outputs.

The target is not another universal instantaneous norm bound. The
target is to prove or falsify

\[
T_c^+
\le\theta\nu D_s+K(t)X
\quad\text{or}\quad
T_c^+
\le\theta\nu D_s+K(t)Y,
\qquad 0<\theta<1,
\]

where the proposed formula for \(K(t)\) is explicit and its required
time integral follows from already available, non-circular control.
The near-scale piece must be tested first against concentrated annular
packets and phase-coherent triad families.

Do not put \(K(t)\) in the PDE. Tautological
\(K=(T_c-\theta\nu D_s)_+/X\) is not content.

---

## 8. Claim boundary

This note supplies an exact finite-triad rejection test and a
separated-family asymptotic calculation. It does not establish a
cutoff-uniform temporal estimate, a continuation criterion, or global
regularity for three-dimensional Navier–Stokes.
