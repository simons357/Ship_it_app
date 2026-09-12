# Unrestricted Lemma★ — growing-layer counterexample

12 September 2026.
Unaugmented Navier–Stokes on \(\mathbb{T}^3\);
quantity is the locked
\(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s E Y)\);
the family is real, mean-zero, divergence-free,
finite Fourier support, \(\mathcal D_s>0\);
**unrestricted \(\sup\mathcal R_\star<\infty\) is killed.**

**This is a counterexample to the boxed instantaneous
estimate. It is not a singular Navier–Stokes solution.
Ordinary NS is not solved. Soft X silent.**

Phone lock: [`../../LEMMA-STAR-GROWING-LAYER.md`](../../LEMMA-STAR-GROWING-LAYER.md).
Statement: [`../../LEMMA-STAR-STATEMENT.md`](../../LEMMA-STAR-STATEMENT.md).
Tape: [`../../YES-NO-OPEN.md`](../../YES-NO-OPEN.md).
Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.

Specialist review of the all-\(n\) \(T_c\) identity
is pending. The live evaluators already reproduce
it on \(n=1,\dots,10\). That is not a proof assistant.

---

## Locked objects

Unchanged normalized torus. Definitions as in
[`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md):

\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\quad
\Lambda=Y/X,
\]

\[
\mathcal D_s=Z-\frac{Y^2}{X},\qquad
T_c=M-\Lambda N.
\]

The boxed claim that died is
\(\sup\mathcal R_\star<\infty\) with one
geometry-only constant. Kill rule:
\(\mathcal R_\star(v_n)\to\infty\).

---

## The family

\[
\psi(x,y)=\cos x+\cos(x+y)+\cos(2x+y),
\qquad
U=(-\psi_y,\psi_x),
\]

\[
v_n(x,y,z)=D_n(z)\,(U_1(nx,ny),U_2(nx,ny),0),
\qquad
D_n(z)=\sum_{j=-n}^{n}e^{ijz}.
\]

Complete Fourier coefficients:

\[
\widehat v_n(nr_1,nr_2,j)
=
\frac{i}{2}(-r_2,r_1,0),
\quad
r\in\{\pm(1,0),\pm(1,1),\pm(2,1)\},
\quad
\lvert j\rvert\le n.
\]

They are real-field coefficients
(\(\widehat v(-k)=\overline{\widehat v(k)}\)),
mean-zero, and divergence-free.
At least two eigenvalues carry mass, so
\(\mathcal D_s>0\).
The packet changes shape with \(n\).
It is not a uniform Fourier dilation of one field.

Energy: \(E_n=4(2n+1)\).

---

## Signed seed and the vertical factor

The planar seed has complete signed transfers
\(3/4\), \(-1\), \(1/4\) on eigenvalues \(1,2,5\).
Its energy transfer and \(N\) vanish. Its \(M=3\).

Separation of \(D_n(z)\), including every cross
derivative, cancels the terms paired with \(U\)
and \(A_h U\). The surviving term is paired with
\(A_h^2 U\). The vertical cubic is the number of
ordered pairs \((a,b)\) with
\(\lvert a\rvert,\lvert b\rvert,\lvert a+b\rvert\le n\),
which is \(3n^2+3n+1\).

\[
N(v_n)=0,
\qquad
T_c(v_n)=3n^5\langle D_n^3\rangle
=3n^5(3n^2+3n+1)>0.
\]

Keep \(\mathrm{Im}\). The signed total is retained.

---

## Elementary divergence

For every integer \(n\ge 1\):

\[
E_n=4(2n+1)\le 12n,
\qquad
\lambda_{\max}\le 6n^2,
\qquad
T_c\ge 9n^7,
\]

\[
Y_n\le 36n^4 E_n,
\qquad
0<\mathcal D_{s,n}\le Z_n\le 216n^6 E_n.
\]

Therefore

\[
\mathcal R_\star(v_n)
=
\frac{(T_c)_+^2}{\mathcal D_s E Y}
\ge
\frac{81n^{14}}{216\cdot 36\cdot 12^3 n^{13}}
=
\frac{n}{165888}
\to\infty.
\]

Any proposed finite \(C_{\mathrm{geom}}\) fails for
\(n>165888\,C_{\mathrm{geom}}\).
The sharper moment asymptotic
\(\mathcal R_\star(v_n)/n\to 496125/411555776>0\)
is not required for the kill.

---

## Live evaluators (not a second claim)

`scripts/ns_attacks/stokes_moments.py` and
`scripts/ns_lemma_star_core.py` both give:

| \(n\) | modes | \(N\) | \(T_c\) | \(\mathcal R_\star\) |
|--:|--:|--:|--:|--:|
| 1 | 18 | 0 | 21 | 0.001398359660043 |
| 2 | 30 | 0 | 1824 | 0.002574888688615 |
| 3 | 42 | 0 | 26973 | 0.003771825398057 |
| 4 | 54 | 0 | 187392 | 0.004972851263004 |

Through \(n=10\), \(T_c\) matches the closed form,
\(N=0\), \(\mathcal D_s>0\), and \(\mathcal R_\star/n\)
falls toward \(496125/411555776\).
Live Stokes was not overwritten.

Need★ cannot repair this unrestricted box
unless its hypotheses or conclusion change.

---

## What this does not do

- It does not construct a blowup of NSE.
- It does not kill H1 or \(\int\rho_j\).
- It does not prove the exact-shell 9D bound.
- It does not make Need★ a theorem.
- It does not put \(K(t)\) in the PDE.
- It does not turn A into B.

---

## Status

| Item | Verdict |
|---|---|
| Unrestricted \(\sup\mathcal R_\star<\infty\) | **NO.** Killed by \(v_n\). |
| Finite \(0.641\) / \(0.456\) as this kill | **NO.** Different objects. |
| Need★ as a repair of that same box | **NO** unless the claim changes. |
| Replacement energy-budget closure | **OPEN.** |
| Ordinary NS | **OPEN.** |
| Specialist reading of the \(T_c\) identity | **pending** |
