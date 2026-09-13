# Unrestricted Lemma★ — growing-layer family

12 September 2026.
Unaugmented Navier–Stokes on \(\mathbb{T}^3\);
quantity is the locked
\(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s E Y)\);
the family below is divergence-free, real, mean-zero,
finite Fourier support, \(\mathcal D_s>0\);
**unrestricted \(\sup\mathcal R_\star<\infty\) is killed
in this review.**

**This is a counterexample to the boxed instantaneous
estimate.** The admissible class is
divergence-free, real, mean-zero, finite
Fourier support, \(\mathcal D_s>0\) on
\(\mathbb{T}^3\). \(v_n\) sits in that
class. It is not an NSE trajectory and
not a singular Navier–Stokes solution.
Ordinary NS is not solved. Soft X silent.

The named kill of leftover 4 was
\(\mathcal R_\star(v_n)\to\infty\).
That sequence sits on the locked evaluators
for every checked \(n\). A finite sample is
not this. \(K\approx 0.641\) and grow-\(s\)
\(K\approx 0.456\) are not this.

Need★ cannot repair the same unrestricted bound
unless its hypotheses or conclusion change.
H1 and the axisymmetric shell door are other
integrals. Do not glue.

Specialist review of the all-\(n\) \(T_c\)
identity is still pending. The live
evaluators already reproduce the
identity on \(n=1,\dots,10\), not only
\(n\le 8\). That is not a proof assistant.
Specialist questions:
[`PR24-SPECIALIST-QUESTIONS.md`](PR24-SPECIALIST-QUESTIONS.md).

Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`
Audit: `results/pr24_closure_review/audit.json`
Math pointer: [`math/ns_attacks/LEMMA_STAR_GROWING_LAYER_COUNTEREXAMPLE.md`](math/ns_attacks/LEMMA_STAR_GROWING_LAYER_COUNTEREXAMPLE.md).
Locked statement: [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).

---

## The family

On the normalized torus of
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md),
with the unchanged \(E,X,Y,Z,\Lambda=Y/X\),
\(\mathcal D_s=Z-Y^2/X\), \(T_c=M-\Lambda N\):

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
mean-zero, and divergence-free
(\(k\cdot\widehat v_n(k)=0\)).
Six planar seeds times \(2n+1\) vertical
copies give \(6(2n+1)\) modes.
The \(j=0\) copies already occupy
eigenvalues \(n^2\), \(2n^2\), and
\(5n^2\), which are distinct for every
\(n\ge 1\). So \(\mathcal D_s>0\) for
every \(n\ge 1\), not only on computed
rows.
The packet changes shape with \(n\).
It is not a uniform Fourier dilation of one field.

Each mode has \(|\widehat v|^2=1/4\), so
\[
E_n=6(2n+1)\cdot\frac14=4(2n+1).
\]

---

## Signed seed and the vertical factor

The planar seed (\(n=1\) without the extra
vertical copies, or equivalently the
\((x,y)\)-field \(U\)) has complete signed
transfers \(3/4\), \(-1\), \(1/4\) on
eigenvalues \(1,2,5\). Its energy transfer
and \(N\) vanish. Its \(M=3\).
The locked evaluator prints that table.

Separation of \(D_n(z)\), including every
cross derivative, cancels the terms paired
with \(U\) and \(A_h U\). The surviving term
is paired with \(A_h^2 U\). The vertical
cubic is the number of ordered pairs
\((a,b)\) with
\(\lvert a\rvert,\lvert b\rvert,\lvert a+b\rvert\le n\),
which is \(3n^2+3n+1\).
That count is elementary for every
\(n\ge 1\): for \(a\ge 0\), \(b\) has
\(2n-a+1\) values; for \(a<0\),
\(2n+a+1\) values; the sums add to
\(3n^2+3n+1\).
The remaining \(3n^5\) and the
vertical cancellation that drops the
terms paired with \(U\) and \(A_h U\)
are the identities a specialist must
still accept. If that \(T_c\) formula
fails, the elementary lower bound
fails. Those identities were matched
on \(n=1,\dots,10\). They are not a
hand proof for general \(n\).

A consistent change of torus measure
or amplitude does not flip
\(\mathcal R_\star\to\infty\).
\(\mathcal R_\star(av)=\mathcal R_\star(v)\).
Omitting the \(n\) in \(U(nx,ny)\)
writes a different field, not a
renormalization of \(v_n\).

\[
N(v_n)=0,
\qquad
T_c(v_n)=3n^5\langle D_n^3\rangle
=3n^5(3n^2+3n+1)>0.
\]

Keep \(\mathrm{Im}\). The signed total is retained.
The growing packet is not a uniform dilation,
so \(\mathcal R_\star\) may grow.

---

## Elementary divergence

For every integer \(n\ge 1\):

\[
E_n=4(2n+1)\le 12n,
\qquad
\lambda_{\max}\le n^2\cdot 5+n^2=6n^2,
\qquad
T_c=3n^5(3n^2+3n+1)\ge 9n^7,
\]

\[
Y_n\le\lambda_{\max}^2 E_n\le 36n^4 E_n,
\qquad
0<\mathcal D_{s,n}\le Z_n\le\lambda_{\max}^3 E_n\le 216n^6 E_n.
\]

Therefore

\[
\mathcal R_\star(v_n)
=
\frac{(T_c)_+^2}{\mathcal D_s E Y}
\ge
\frac{81n^{14}}{216\cdot 36\cdot 12^3 n^{13}}
=
\frac n{165888}
\to\infty.
\]

Any proposed finite \(C_{\mathrm{geom}}\) fails for
\(n>165888\,C_{\mathrm{geom}}\).
The sharper moment asymptotic
\(\mathcal R_\star(v_n)/n\to 496125/411555776>0\)
is not required for the kill.

The elementary bound uses the closed \(T_c\)
identity. Specialist review should check
seed transfer signs, vertical cancellation,
and match to the unrestricted statement
in [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
A mathematical objection should name a
failing equation or an admissibility
condition the family violates.

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

These checks resolve sign, normalization
and evaluator compatibility. They are not
a formal proof-assistant verification.

---

## What this does not do

- It does not construct a blowup of NSE.
- It does not kill H1 or \(\int\rho_j\).
- It does not prove the exact-shell 9D bound.
- It does not make Need★ a theorem.
- It does not put \(K(t)\) in the PDE.
- It does not turn A into B.

The unaugmented regularity program needs a
replacement energy-budget closure.

---

## Status

| Item | Verdict |
|---|---|
| Unrestricted \(\sup\mathcal R_\star<\infty\) | **NO.** Killed by \(v_n\) in this review. |
| Finite \(0.641\) / \(0.456\) as this kill | **NO.** Different objects. |
| Need★ as a repair of that same box | **NO** unless the claim changes. |
| Replacement energy-budget closure | **OPEN.** |
| Ordinary NS | **OPEN.** |
| Specialist reading of the \(T_c\) identity | **pending** |

NS not solved. The boxed unrestricted ★ is dead.
The door that remains is a different closure.
