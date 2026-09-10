# Lemma★ — canonical claim (working foundation)

**Date:** 2026-09-10  
**Status:** **OPEN.** Evaluator ≠ proof. Exact core ≠ proof.
A finite ABC_λ climb raises \(C_{\mathrm{geom}}\); it does not kill ★.
`docs/CS-REMAINDER.md`. **NS not solved.**
H1 / WRITE (6) is a different integral and was not run on ABC_λ.

Identities: [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md).  
Phone lock of the four corrections: [`../../LEMMA-STAR-CORRECTIONS.md`](../../LEMMA-STAR-CORRECTIONS.md).  
Older attempt: [`LEMMA_STAR_OLDER_ATTEMPT_ARCHIVE.md`](./LEMMA_STAR_OLDER_ATTEMPT_ARCHIVE.md) (annotated archive, not a claim).

Do not treat [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md) as a second independent claim box. Edit this file for the claim; edit the exact-formulas note for identities.

---

## Central target (sits as the statement)

On divergence-free fields on \(\mathbb{T}^3\), with \(E=\|v\|_2^2\), \(Y=\|Av\|_2^2\), \(\mathcal D_s=Z-\Lambda Y\), and \(T_c=M-\Lambda N\), there is one geometric constant \(C_{\mathrm{geom}}\) (independent of amplitude and of \(\nu\)) such that
\[
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal D_s(v)\,
E(v)\,
Y(v).
\]
Equivalent quotient:
\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{\mathcal D_s(v)\,E(v)\,Y(v)}
\qquad(\mathcal D_s>0).
\]
Lemma★ is this uniform bound: \(\sup_v\mathcal R_\star<\infty\). A finite peak on a sample only raises the constant a proof would need. It does not kill the existence of a finite constant, and it is not that constant.

Amplitude reduction, spectral identities, and viscosity packaging agree with [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md). Write \(u=av\). Then \(T_c\sim a^3\), \(\mathcal D_s\sim a^2\), \(E\sim a^2\), \(Y\sim a^2\). Optimizing the viscous form over \(a>0\) recovers the boxed line, with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\):
\[
T_c
\le
\theta\nu\mathcal D_s
+C_0\nu^{-1}E\,Y.
\]
\(\mathcal R_\star(av)=\mathcal R_\star(v)\). Uniform Fourier dilation \(v(n\cdot)\) likewise leaves \(\mathcal R_\star\) invariant.

---

## Four corrections

### 1. The older “missing inequality” is false as a universal estimate

It proposes
\[
\lvert T_c(u)\rvert
\le
C\,\|u\|_2\,X(u)^{3/2}.
\]
Under \(u=av\), the left side scales as \(a^3\) and the right as \(a^4\). For any field with \(T_c(v)\ne 0\), taking \(a\to 0\) contradicts it. That route is discarded by algebra. It is not an open product gap toward ★.

Do **not** apply this scaling death to the Attack-2 remainder
\[
\lvert T_c\rvert\le C_* X^{3/2}\Lambda.
\]
That object is amplitude-invariant (\(a^3/a^3\)). It is a different sufficient door, not the boxed form. Uniform pre-Young \(|T_c|\le C\|u\|_2 X\Lambda\) is already dead for a different reason (\(\sim s\)).

HH→L remains a diagnostic of channels. It is not a path to the false \(a^4\) bound.

### 2. Lemma★ implies global regularity in this packaging; it is not equivalent to it

The quotient argument is one direction: if the boxed bound sits, then \(\Lambda\) cannot blow in finite time in this packaging, hence \(X\le\|u_0\|_2^2\Lambda\) stays finite, hence global regularity on \(\mathbb{T}^3\) **in this packaging**.

These files provide **no converse** showing that global regularity would force the uniform inequality over every smooth field. Do not write “★ equivalent to global regularity.” The implication is the skeleton. The inequality is the hole.

### 3. The positive-part distinction disappears when testing all fields

\[
T_c(-v)=-T_c(v),
\]
while \(\mathcal D_s\), \(E\), and \(Y\) stay unchanged. A universal bound for \((T_c)_+^2\) is therefore equivalent to a universal bound for \(T_c^2\). Keep \((T_c)_+\) in the boxed form (the viscous remainder only fights stretching). Do not ignore a large **negative** value: reversing the field makes it positive. A probe that reports \(\mathcal R_\star=0\) because \(T_c<0\) has not tested the opposite orientation.

### 4. Section 4 of the older proof attempt does not establish its advertised theorem

Its opening remainder involving \(\|\nabla u\|_\infty^2 X\) is followed by incomplete estimates and is eventually replaced with a different conditional statement. The “proved” label cannot apply to that opening claim. Keep that attempt as an annotated archive. Do not cite it as a theorem.

---

## Near-shell precision

Attack 9B studies
\[
v_\varepsilon=w_\alpha+\varepsilon z_\beta,
\qquad
Aw_\alpha=\alpha w_\alpha,
\qquad
Az_\beta=\beta z_\beta.
\]
The displayed limit
\[
\lim_{\varepsilon\to 0}\mathcal R_\star(v_\varepsilon)=K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
\]
holds only for an aligned, sign-selected closer
\[
z_\beta
=
\pm
\frac{\Pi_\beta B(w,w)}{\|\Pi_\beta B(w,w)\|_2}
\]
(sign so that \(T_c(v_\varepsilon)_+>0\)). For arbitrary unit \(z_\beta\) on shell \(\beta\), the limit depends on the projection of \(z_\beta\) against \(B(w,w)\):
\[
\lim_{\varepsilon\to 0}\mathcal R_\star(w+\varepsilon z_\beta)
=
\frac{\beta\,\bigl|\langle\Pi_\beta B(w,w),z_\beta\rangle\bigr|^2}{\alpha^2\|w\|_2^4\|z_\beta\|_2^2}.
\]
That is \(K_{\alpha,\beta}(w)\) times the squared cosine of the angle in the \(\beta\)-shell. A misaligned closer is not the 9B quotient.

---

## Remaining target

ABC_λ is a finite climb on the grids they ran (FFT through λ=8,
core through λ=4). Largest FFT \(\mathcal R_\star(-v)\approx 0.327\).
That raises \(C_{\mathrm{geom}}\). It is not \(\mathcal R_\star\to\infty\).
Do not stamp a falsifier. Do not stop patching.
Phone: [`../../CS-REMAINDER.md`](../../CS-REMAINDER.md).
Score: [`../../ns-recovery/CS-REMAINDER-VS-DA-REJECT.md`](../../ns-recovery/CS-REMAINDER-VS-DA-REJECT.md).

N-shell Fourier samples still saturate. They are not this field.
Fourier dilation \(v(n\cdot)\) stays invariant.

K=0 is dead. The \(a^4\) “missing inequality” is dead. Uniform pre-Young \(C\) is dead. Attack-2 \(C_*\) is a different door. Fixed-output \(\Theta(m^2)\) is a counting error. Freiman-AP is already dead. ★ is not a close of unaugmented NSE. H1 / WRITE (6) is a different integral and was not run on ABC_λ.

**NS not solved.** Lemma★ OPEN. Leftover (6) still open.
