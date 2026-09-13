# Lemma★ — statement from the lock, not a reconstruction

12 September 2026. Phone.
**The boxed unrestricted claim is killed
by the growing-layer family.**
Replacement closure **OPEN.** Not a proof.
NS not solved.
This page still quotes the claim that died.
It is not a reconstruction.
The kill: [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).

Sources (in this order):

- Boxed claim: [`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md)
- Identities: [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md)
- Viscous line first: [`LEMMA-STAR.md`](LEMMA-STAR.md)
- Ratio: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md)
- Four corrections: [`LEMMA-STAR-CORRECTIONS.md`](LEMMA-STAR-CORRECTIONS.md)
- ABC_λ score: [`ns-recovery/CS-REMAINDER-VS-DA-REJECT.md`](ns-recovery/CS-REMAINDER-VS-DA-REJECT.md)

Evaluator ≠ proof. Exact core ≠ proof.
H1 / WRITE (6) is a different integral.

---

## The boxed claim (this is Lemma★)

One line, every symbol below:
no finite \(C_{\mathrm{geom}}\) satisfies
\((T_c)_+^2\le C_{\mathrm{geom}}\,\mathcal D_s E Y\)
on the class written here. That line is
**killed** by \(v_n\).

On divergence-free fields on \(\mathbb{T}^3\),
\(E=\|v\|_2^2\), \(Y=\|Av\|_2^2\),
\(\mathcal D_s=Z-\Lambda Y\), \(T_c=M-\Lambda N\):

\[
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal D_s(v)\,
E(v)\,
Y(v).
\]

Equivalent, when \(\mathcal D_s>0\):

\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{\mathcal D_s(v)\,E(v)\,Y(v)},
\qquad
\sup_v\mathcal R_\star<\infty.
\]

Viscosity packaging (Young on the same inequality):

\[
T_c
\le
\theta\nu\mathcal D_s
+C_0\nu^{-1}E\,Y,
\qquad
C_0(\theta)=C_{\mathrm{geom}}/(4\theta).
\]

Phone lock writes the same line as
\(T_c\le\theta\nu(Z-\Lambda Y)+C_0\nu^{-1}\|u\|_2^2 X\Lambda\).
Those agree: \(X\Lambda=Y\), \(\mathcal D_s=Z-\Lambda Y\).

Equivalent trilinear form (\(C_{\star}^2=4\theta C_0\)):

\[
\bigl[-\langle B(v,v),A(A-\Lambda)v\rangle\bigr]_+
\le
C_{\star}\,
\|v\|_2\,\|Av\|_2\,
\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2.
\]

This \(C_{\star}\) is ★. It is not Attack-2 \(C_*\).

---

## Setup that sits (algebra + Fourier)

\[
A=-P\Delta,\qquad B(v,v)=P[(v\cdot\nabla)v].
\]

\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\quad
\Lambda=Y/X.
\]

\[
\mathcal D_s
=Z-\frac{Y^2}{X}
=\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2^2.
\]

\[
T_c
=-\langle B(v,v),A(A-\Lambda)v\rangle
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

If \(\mathcal D_s=0\), the field is one shell,
\(T_c=0\), and the claim is vacuous. Not a kill.
If \(\mathcal D_s=0\) and \(T_c>0\), ★ is dead
immediately. A pure shell does not do that.

Amplitude: \(T_c\sim a^3\), \(\mathcal D_s,E,Y\sim a^2\).
\(\mathcal R_\star(av)=\mathcal R_\star(v)\).
Uniform Fourier dilation \(v(n\cdot)\) is invariant.

---

## What a proof of ★ would have to be

A uniform bound on \(\mathcal R_\star\) over
\(C^\infty_{\mathrm{div},0}(\mathbb{T}^3)\setminus\{0\}\).
Not a bound on one family (ABC_λ, \(K_{\alpha,\beta}\),
N-shell, …). A sample bound on a restricted family
does not prove ★. Finite computed values only raise
a candidate \(C_{\mathrm{geom}}\).

Kill rule (this book): \(\mathcal R_\star\to\infty\)
along some sequence. One large finite number does not.

---

## If ★ closed (locked implication)

Correction 2, quoted: ★ \(\Rightarrow\) global
regularity **in this packaging**. One direction.
No converse. Do not write “★ equivalent to GR.”

The inequality is the hole. The implication is the
skeleton. The boxed claim is dead, so this packaging
does not give unaugmented regularity.
That is not a singular NSE solution.

DA-NS-2: if ★ sits, DA-NS-2 sits. The integral
does not sit yet. Do not add \(K(t)\) to the PDE.

---

## What is proved vs open (from the lock)

| Item | Status |
|---|---|
| \(A,B,E,X,Y,Z,\Lambda,\mathcal D_s,T_c,\mathcal R_\star\) | closed (algebra + triad) |
| One shell: \(\mathcal D_s=0\Rightarrow T_c=0\) | closed |
| \(T_c(-v)=-T_c(v)\); reverse to test stretching | closed (correction 3) |
| \(\sup\mathcal R_\star<\infty\) | **NO.** Killed by \(v_n\) |
| Bound on \(C_{\mathrm{geom}}\) | **NO.** No finite constant |
| Kill of that box | sits. [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md) |
| Replacement energy-budget closure | **open** |
| Unaugmented NSE solved by ★ | no (the box is dead) |
| H1 / WRITE (6) | different integral; outside this statement |

K=0 dead. Uniform pre-Young \(C\) dead. Older
\(|T_c|\le C\|u\|_2 X^{3/2}\) dead by scaling
(\(a^3\) vs \(a^4\)). Not Attack-2 \(C_*\).

---

## ABC_λ relative to this lemma

Evaluator for the quotient. ABC_λ did not
kill ★. Largest gate-table number after
reverse: \(0.327\) at λ=8. A finite climb,
not the \(v_n\) family.

H1 was not run on ABC_λ. Do not start it here.

Explore-boundedness score (SuperGrok 19:08):
[`LEMMA-STAR-EXPLORE.md`](LEMMA-STAR-EXPLORE.md).
Family check vs lock (that paste; not a kill):
[`LEMMA-STAR-FAMILY-CHECK.md`](LEMMA-STAR-FAMILY-CHECK.md).
Cube family (named, computed; not a kill):
[`LEMMA-STAR-CUBE.md`](LEMMA-STAR-CUBE.md).
Cube analytic review (files absent; \(M_0\) not locked):
[`LEMMA-STAR-CUBE-REVIEW.md`](LEMMA-STAR-CUBE-REVIEW.md).
Two-shell \(D_s\) already sits. \(T_c\) is not
shell energies alone. Spatial \(v(\mu x)\) is
not Fourier dilation. Do not stop patching.

---

## Score of the incoming explanation

Keep: evaluator ≠ proof; exact boxed ratio; one-shell
vacuous; the unrestricted claim had to be uniform;
finite samples are not a kill; the named kill is
\(\mathcal R_\star\to\infty\); H1 outside this statement.

The unrestricted box is dead. The leftover is a
different energy-budget estimate that \(v_n\)
does not kill. Need★ cannot repair this box.
If a different estimate holds, GR in this
packaging is a separate implication. No converse.

Stay in this chat.
