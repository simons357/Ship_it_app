# Narrow heterochiral residual

24 September 2026.
**One residual region. A finite
primitive test. Not a close.
NS not solved.**

Parent ledger:
[`CENTERED-MASTER-LEDGER.md`](CENTERED-MASTER-LEDGER.md).
Epoch budget (still the Gate
that must pay DA-NS-2):
[`JOINT-EPOCH-BUDGET.md`](JOINT-EPOCH-BUDGET.md).

Unaugmented NS. No \(Q_1\).
No \(\Phi\). No SND. No
Theorem H. No Route A weld.
Unrestricted \(\star\) stays
**KILLED**. Charge-only stays
**KILLED**. Static SAG
triangle / circle / star /
tree stay **KILLED** as
missing power. No more
single-circle searches.

---

## Rally point

\[
\boxed{
\exists\theta<1:\quad
\sup_n\int_0^T
\frac{[\mathfrak T_c^{(n)}-\theta\nu\mathcal D_s^{(n)}]_+}
{Y^{(n)}}\,dt<\infty.
}
\]

Clock:

\[
\boxed{
(\log\Lambda)'
=\frac2Y(\mathfrak T_c-\nu\mathcal D_s).
}
\]

Those stay. The live object
immediately upstream is

\[
\boxed{
\textbf{NARROW HETEROCHIRAL RESIDUAL}
\quad
2\kappa^3 Q_a
-(\Lambda-\kappa_e^2)S_\Gamma
}
\]

with

\[
\boxed{S_\Gamma=\sum_\gamma A_\gamma Q_{a,\gamma}.}
\]

First question:

\[
\boxed{
\text{does }S_\Gamma\text{ admit a uniformly conditioned
translation-invariant quadratic primitive
on the actual loop networks?}
}
\]

---

## Width and the \(\kappa^{-1/2}\) crossover — EXACT equivalence

Define, from the seated moments,

\[
\boxed{r^2=\frac{\mathcal D_s}{\Lambda Y},
\qquad\kappa=\sqrt\Lambda.}
\]

Then **identically**

\[
\boxed{\frac{\mathcal D_s}{Y}=\Lambda r^2=\kappa^2 r^2.}
\]

Hence the comparison is not a
new estimate:

\[
\boxed{
r\gtrsim\kappa^{-1/2}
\quad\Longleftrightarrow\quad
\frac{\mathcal D_s}{Y}\gtrsim\kappa.
}
\]

That is the old missing-half
derivative scale, read on
\(\mathcal D_s/Y\). Code:
`scripts/ns_attacks/narrow_het_residual.py`.

On the two-point family with
\(\lambda=\Lambda(1\pm\varepsilon)\)
and equal \(X\)-share,
\(r=\varepsilon\) exactly:
\(r\) **is** the relative
\(\lambda\)-width
\(\sigma_\lambda/\Lambda\).
Absolute \(|k|\)-width
satisfies \(\delta/\kappa\approx r/2\).

### Convention audit (do not mix)

| Symbol | Meaning |
|---|---|
| \(r\) | \(\sigma_\lambda/\Lambda\), dimensionless |
| \(\kappa^{-1/2}\) | \(\Lambda^{-1/4}\), a **torus-unit** number |
| \(\mathcal D_s/Y\) | \(\kappa^2 r^2\), not \(r\) |
| \(\sigma_\lambda/\kappa\) | \(\kappa r\), not \(r\) |

The comparison \(r\sim\kappa^{-1/2}\)
is consistent **inside** the seated
\(\mathbb T^3\) convention
\(\lambda=\lvert k\rvert^2\),
\(k\in\mathbb Z^3\). Rescaling the
box changes the number. It is a
scale split, not a
box-invariant critical value.
Do not stamp it as a theorem
about every domain.

---

## Coefficient gaps — EXACT at leading order

On-shell,
\(i=j=o=\kappa\), \(\Lambda=\kappa^2\):

\[
A=2\kappa,\qquad
H=2\kappa^2,\qquad
R=2\kappa^3.
\]

A relative \(|k|\) perturbation
of size \(r\) gives

\[
\boxed{R_\Lambda-2\kappa^3=O(\kappa^3 r)=O(\kappa^2\delta).}
\]

Linear, not cubic. Finite-difference
coefficients on the unit directions
sit between \(2.5\) and \(10\).
The linear heterochiral radial
gap is not a mix-up of
absolute and relative width.

Homochiral Vandermonde

\[
V=(x-y)(y-z)(z-x)
\]

is a cubic polynomial. On the
same relative-\(|k|\) family,
\(V/(\kappa^3 r^3)\) is constant
to printer precision. Coefficient
depletion is cubic in \(r\).

Do not promote either scaling
to a \(T_c\) bound. They classify
**where** a payment can sit.

---

## Schematic map

\[
\boxed{
\text{DANGEROUS}
\to
\begin{cases}
\text{BROAD }(r\gtrsim\kappa^{-1/2})
\to \mathcal D_s\text{ / viscosity},\\
\text{NARROW HOMO}
\to\text{cubic radial gap},\\
\text{NARROW HET RADIAL}
\to\text{linear radial gap},\\
\textbf{NARROW HET CHARGE + MOVING CENTER}
\to\text{current residual}.
\end{cases}
}
\]

The first three branches are
coefficient-level. They are
not DA-NS-2. The fourth is
the residual.

Frozen epoch:

\[
\boxed{
\mathfrak T_{c,\Gamma}^{\mathrm{het}}
=2\kappa_e^3 Q_{a,\Gamma}
+\rho_{\Gamma,e}^{\mathrm{rad}}
+\rho_{\Gamma,e}^{\mathrm{mov}}
}
\]

\[
\boxed{
\rho_{\Gamma,e}^{\mathrm{mov}}
=-(\Lambda-\kappa_e^2)S_\Gamma.
}
\]

Radial \(\rho^{\mathrm{rad}}\)
has a plausible narrow-width
payment \(O(\kappa^3 r)\).
The two hard pieces remain
\(2\kappa^3 Q_a\) and
\(-(\Lambda-\kappa_e^2)S_\Gamma\).

---

## Primitive test — EXACT linear algebra

Frozen network. Quadratic
capacity \(\mathcal H_w=\sum_m w_m\lvert a_m\rvert^2\).
Waleffe cyclic incidence on a
signed triad:

\[
(\mathsf B^{\mathrm{prim}}w)_\gamma
=
\sum_{\mathrm{cyc}}
w_k\bigl(s_p\lvert p\rvert-s_q\lvert q\rvert\bigr).
\]

Target \(b=A\) for \(S_\Gamma\),
\(b=\mathbf 1\) for net charge.
Reality identification
\((k,s)\sim(-k,-s)\).

\[
\boxed{
c^Tb=0
\quad\text{for every }
c\in\ker[(\mathsf B^{\mathrm{prim}})^T].
}
\]

Equivalent: \(b\in\mathrm{range}(B)\).
The least-squares residual
**is** a left-null witness.
No nonlinear optimizer.

Isotropic restriction:
\(w=w(\lvert k\rvert,s)\), the
translation-invariant
Fourier-multiplier subclass.

Normalization caveat: if \(Q_a\)
differs from the Waleffe cubic
by a per-channel factor
\(\xi_\gamma\), the correct
target is \(b=\xi\odot A\).
On the lattice both \(A\) and
\(\mathbf 1\) are almost
orthogonal to \(\mathrm{range}(B)\)
(relative residual \(\approx 1\)),
so the obstruction is not a
constant rescaling artifact.

---

## Computation (no optimizer)

| Network | ch / modes | \(b=A\) | left-null | cond | \(\lVert w\rVert_{\min}\) |
|---|---|---|---|---|---|
| two-triad tree | 2 / 5 | yes | 0 | \(2.05\) | \(1.47\) |
| \(L=2\) tree | 2 / 5 | yes | 0 | \(1.66\) | \(1.48\) |
| \(L=7\) tree | 2 / 5 | yes | 0 | \(1.71\) | \(1.44\) |
| \(L=16\) tree | 2 / 5 | yes | 0 | \(1.72\) | \(1.42\) |
| \(L=55\) tree | 2 / 5 | yes | 0 | \(1.73\) | \(1.42\) |
| lattice \(\lvert k\rvert^2\le 10\) | 4788 / 146 | **NO** | 4643 | \(1.60\) | — |
| lattice tree \(\lvert k\rvert^2\le 10\) | 99 / 146 | yes | 0 | \(525\) | \(18.9\) |
| lattice \(\lvert k\rvert^2\le 14\) | 14412 / 250 | **NO** | 14163 | \(1.67\) | — |

Holonomy on the full lattice:
\(\lVert r\rVert/\lVert A\rVert\approx 0.9998\)
(\(n^2\le 10\)) and
\(\approx 0.9998\)
(\(n^2\le 14\)).
Charge \(b=\mathbf 1\) fails
the same way
(\(\approx 0.999\)).

Isotropic \(w(\lvert k\rvert,s)\)
fails on the
\(\lvert k\rvert^2\le 10\)
**tree** already
(relative residual \(\approx 0.81\)).
Radius-only weights do not
produce \(S_\Gamma\) even
after loops are deleted.

\(A\) is not constant on the
two-triad witness. Charge and
\(S_\Gamma\) each have a
primitive on that tree, but
**not the same** \(w\).

---

## Verdict of the first question

\[
\boxed{
\text{full lattice het loops: no quadratic primitive for }S_\Gamma.
}
\]

Exact holonomy obstruction
for this incidence. Same
for net charge.

\[
\boxed{
\text{\(L\)-family trees: yes, cond}\sim 1.7,\ \lVert w\rVert=O(1).
}
\]

\[
\boxed{
\text{isotropic }w(\lvert k\rvert,s)\text{ fails on the lattice tree.}
}
\]

So: a uniformly conditioned
translation-invariant
(isotropic) primitive on the
**actual loop networks** is
**NO**. A modal primitive
exists on small trees and
on the \(L\)-family, with
stable condition number;
it does not survive the
lattice loops, and the
isotropic subclass does not
survive even the lattice
tree.

This is not a bound on
\(\int K\). It is a
constraint on the payment:
\(S_\Gamma\) is not the
nonlinear derivative of a
quadratic Fourier
multiplier on those loops.
Do not invent a bridge.
Do not pointwise-estimate
\(\dot S_\Gamma\).

Charge and moving covariance
cannot share one \(w\) on
the two-triad tree (\(A\)
not constant). On the
lattice loops they share
the obstruction instead.

---

## What not to compute

No more isolated circles,
stars, constant coherence
defects, generic phase
rotations, homochiral
optimizers, or exact-shell
counting unless a named
line of the residual asks
for it.

Solver-side: the missing-factor
product \(\alpha_{c,\kappa}^2\chi_\kappa^2\kappa\)
and adversarial \(J_{\theta,n}(T)\)
remain evidence only.

Loop \(\Gamma_{\mathrm{cyc}}\)
certification is a different
OPEN (phase holonomy). This
page is primitive holonomy
for \(S_\Gamma\).

---

## Lock

Clock and DA-NS-2 unchanged.
\(r^2=\mathcal D_s/(\Lambda Y)\)
and \(r\gtrsim\kappa^{-1/2}
\Leftrightarrow\mathcal D_s/Y\gtrsim\kappa\)
EXACT. Torus units.
\(R-2\kappa^3=O(\kappa^3 r)\)
linear; Vandermonde cubic.
BROAD / NARROW map is a
coefficient split, not a
close. Residual
\(2\kappa^3 Q_a-(\Lambda-\kappa_e^2)S_\Gamma\)
OPEN. Lattice-loop primitive
for \(S_\Gamma\): **NO**
(holonomy). \(L\)-family
tree primitive: yes,
\(\mathrm{cond}\sim 1.7\).
Isotropic restriction:
**NO** on the lattice tree.
Charge and \(S\) do not share
one \(w\). Not DA-NS-2.
NS not solved.
