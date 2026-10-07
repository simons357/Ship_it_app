# Gate A — diagnostic \(\ell^1\) load certificate

7 October 2026.
**Diagnostic only.** \(L_{z_n}\) grows along \(z_n=2n^2\) on the
\(C\)-majorant face. That is **not** a kill, not Outcome B, and
does not close Gate A. Not (17).

Parent: [`GATE-A-POSITIVE-ASSEMBLY-2026-10-07.md`](GATE-A-POSITIVE-ASSEMBLY-2026-10-07.md).
Probe: `scripts/ns_attacks/analytic_load_lower_bound.py`.
Main line: [`GATE-B-THETA.md`](GATE-B-THETA.md).

---

## Why this is not a kill

Under Convention F2 and the *diagnostic* coefficient
\[
\rho_a(z)
=
\frac1{2z}
\left(\sum_{b\in B_a(z)}\frac{C_{a,b;z}^2}{b^2}\right)^{1/2},
\]
define the all-shape \(\ell^1\) load
\[
L_z
:=
\sum_a\rho_a(z).
\]

Along \(z_n=2n^2\) one has \(L_{z_n}\to\infty\) *on this face*.
That is an \(\ell^1\) diagnostic. It is **not** a proved divergent
allocation cost, because:

1. September 20 \(C_{abc}\) is an **upper** bound. It does not by
   itself force the positive allocation to pay that size.
2. The factor \(1/(2z)\) is the algebraic \(c=25\) face written at
   variable \(z\). That is **not** a filed general-\(c\) allocation
   lemma under the frozen smallest-leg convention.
3. Nothing currently filed establishes an infinite lattice sequence
   with a proved divergent *allocation cost*.

Do not manufacture a stronger infinite-sequence note just to finish
Gate A. Frozen multiplicity-5 / smallest-leg stands. 17/32/51 remain
valid at stated finite scope.

---

## Sequence (diagnostic)

\[
z_n = 2n^2,\qquad n=2,3,4,\ldots
\]

---

## Subnet

For integers \((k,\ell)\) in the rectangle
\[
\mathcal R_n
=
\bigl\{\lceil 3n/10\rceil,\ldots,\lfloor 7n/10\rfloor\bigr\}
\times
\bigl\{0,\ldots,\lfloor 2n/5\rfloor\bigr\},
\]
set
\[
u=(k,0,\ell),\quad
v=(n-k,n,-\ell),\quad
w=(-n,-n,0).
\]
Then
\[
|u|^2=a:=k^2+\ell^2,\quad
|v|^2=b:=n^2+(n-k)^2+\ell^2,\quad
|w|^2=z_n,
\]
with \(a<b<z_n\), non-collinear, and \(\Delta_{a,b;z_n}>0\).
Each such triple is an active F2 shape with geometric max \(z_n\).

---

## Uniform face bound

Write \(\theta=k/n\), \(\varphi=\ell/n\), and
\[
g(\theta,\varphi)
=
\frac{\sqrt{3\widetilde\Delta}\;
W(\theta,\varphi)}{\widetilde b},
\]
the continuum scaling of \(C_{a,b;z_n}/(b\,n)\). On the closed rectangle
\([3/10,7/10]\times[0,2/5]\) one has \(\widetilde\Delta>0\) and
\[
g(\theta,\varphi)\ge g(3/10,0)=\kappa_0>1.48.
\]
(The minimum is attained at the corner \((\theta,\varphi)=(3/10,0)\), where
\(\widetilde\Delta=9/100\) exactly; dense-grid certification on the compact
set confirms no smaller value. Integer samples match \(\kappa_0\) to machine
precision.) Hence every subnet shape satisfies
\[
\frac{C_{a,b;z_n}}{b}\ge\kappa\,n
\qquad\text{with}\qquad
\kappa:=1.48.
\]

---

## Load lower bound (still an upper-bound face)

Restrict F2 to subnet anchors. One-term estimate:
\[
L_n^\star
\ge
\sum_a\frac1{2z_n}\max_{b}\frac{C}{b}
\ge
\frac{\kappa}{4n}
\cdot
N_n,
\qquad
N_n
:=
\#\{\,k^2+\ell^2:(k,\ell)\in\mathcal R_n\,\}.
\]
The rectangle has \(\lvert\mathcal R_n\rvert\ge c_0 n^2\) pairs. Each integer
\(m\le O(n^2)\) has
\[
r_2(m)\le 4\,d(m)\ll_\varepsilon m^\varepsilon\ll_\varepsilon n^{2\varepsilon}
\]
representations as a sum of two squares. Therefore
\[
N_n
\ge
\frac{c_0 n^2}{C_\varepsilon n^{2\varepsilon}}
=
c_\varepsilon\,n^{2-2\varepsilon}.
\]
Choose \(\varepsilon<1/2\). Then
\[
L_n^\star
\ge
\frac{\kappa\,c_\varepsilon}{4}\,n^{1-2\varepsilon}
\to\infty.
\]
Since \(L_{z_n}\ge L_n^\star\),
\[
L_{z_n}\to\infty
\]
*as an \(\ell^1\) sum of \(C\)-majorant coefficients*. That is the
diagnostic. It is not a coercive allocation-cost theorem.

---

## What is not claimed

- Criterion (17), Clay, global regularity.
- That Gate A is CLOSED, FAILED, or DEAD.
- Withdrawal of the 17/32/51 restricted-family theorems.
- That \(\mathcal R(z)=L_z/\sqrt{z}\) diverges (the subnet only forces
  \(L\to\infty\) on this face).
- That the \(C\)-majorant is a cost the positive allocation must pay.
- A filed general-\(c\) allocation lemma.
- Any substitute of swirl / Ring / B41 for this diagnostic.

---

## Program consequence

Stop extending finite families by brute force. Do not chase larger
\(c\). Proceed to Gate B: one global Cauchy–Schwarz on
\(\sum_x f_x^2=E\), then extract \(\theta\).

---

## STATUS

GATE A: **UNRESOLVED / DIAGNOSTIC ONLY.**
SEQUENCE: \(z_n=2n^2\), \(L_{z_n}\to\infty\) ON THE \(C\)-MAJORANT FACE.
THAT GROWTH IS NOT A KILL.
(17) NOT CLAIMED.
NS NOT SOLVED.
