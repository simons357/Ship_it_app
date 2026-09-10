# Lemma★ — exact formulas (working foundation)

**Companion:** [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md)  
**Status:** identity lock. Lemma★ **OPEN**. **NS not solved.**

Do not use \(|T_c|\le C\|u\|_2 X^{3/2}\) as a universal estimate — it fails by amplitude scaling. See Canonical, correction 1.

---

## Domain

Normalized torus \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\). Nonzero, mean-zero, divergence-free
\[
v(x)=\sum_{k\neq 0}v_k e^{ik\cdot x},\qquad k\cdot v_k=0,\qquad v_{-k}=\overline{v_k}.
\]
\[
\lambda_k=|k|^2,\qquad A=-P\Delta,\qquad (Av)_k=\lambda_k v_k,
\qquad
B(v,v)=P[(v\cdot\nabla)v].
\]

---

## Linear moments

\[
E=\|v\|_2^2=\sum|v_k|^2,\quad
X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,\quad
Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\quad
Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,
\]
\[
\Lambda=Y/X\quad(X>0).
\]

Under \(u=av\) (\(a>0\)): \(E\mapsto a^2 E\), \(X\mapsto a^2 X\), \(Y\mapsto a^2 Y\), \(Z\mapsto a^2 Z\), \(\Lambda\) invariant.

---

## Spectral spread

\[
D_s
=Z-\frac{Y^2}{X}
=\|(A-\Lambda)A^{1/2}v\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac1{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2
\ge 0.
\]

Two-shell: \(D_s=\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta/(\alpha e_\alpha+\beta e_\beta)\).  
If \(D_s=0\), one shell and \(T_c=0\).  
\(D_s(av)=a^2 D_s(v)\).

---

## Centered transfer

\[
\widehat B_k=i P_k\sum_{p+q=k}(q\cdot v_p)v_q,
\qquad
T_k=-\mathrm{Re}(\widehat B_k\cdot\overline{v_k})
=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr]
\quad\text{(signed; never abs)}.
\]
\[
N=-\langle B,Av\rangle=\sum\lambda_k T_k,\qquad
M=-\langle AB,Av\rangle=\sum\lambda_k^2 T_k,
\]
\[
T_c=-\bigl\langle B(v,v),\,A(A-\Lambda)v\bigr\rangle
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

Oddness: \(T_c(-v)=-T_c(v)\). Homogeneity: \(T_c(av)=a^3 T_c(v)\).

Sign check: \(\Lambda'=2(T_c-\nu D_s)/X\).

---

## Shape quotient

\[
T_c_+=\max(T_c,0),\qquad
\mathcal R_\star=\frac{(T_c_+)^2}{D_s\,E\,Y}\quad(D_s E Y>0).
\]

On **all** fields, a uniform bound on \((T_c_+)^2\) is equivalent to a uniform bound on \(T_c^2\), because reversing \(v\) flips the sign of \(T_c\) and leaves \(D_s,E,Y\) fixed.

Invariance: \(\mathcal R_\star(av)=\mathcal R_\star(v)\), \(\mathcal R_\star(v(n\cdot))=\mathcal R_\star(v)\).

Viscosity packaging (derived): \(T_c\le\theta\nu D_s+C_0\nu^{-1} E Y\) with \(C_{\mathrm{geom}}=4\theta C_0(\theta)\).

---

## Near-shell (restricted family)

\[
K_{\alpha,\beta}(w)=\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
\quad(Aw=\alpha w).
\]
\(\lim_{\varepsilon\to0}\mathcal R_\star(w+\varepsilon z_\beta)=K_{\alpha,\beta}(w)\) **only** for aligned, sign-selected \(z_\beta\parallel\Pi_\beta B(w,w)\). Arbitrary \(z_\beta\): the limit depends on \(\langle z_\beta,B(w,w)\rangle\).

---

## Discarded as a universal estimate

\[
|T_c(u)|\le C\|u\|_2\,X(u)^{3/2}
\]
fails under \(u=av\) (\(a^3\) vs \(a^4\)). Algebra, not numerics.

Code: `scripts/ns_attacks/stokes_moments.py`.

**NS not solved.**
