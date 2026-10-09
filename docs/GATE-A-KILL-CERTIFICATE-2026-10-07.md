# Gate A — legitimate kill certificate

7 October 2026.
**\(L_{z_n}\) load note only. Not (17).**

Scope warning (9 October 2026).
[`sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt`](sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt)
explicitly leaves Gate A diagnostic and unresolved. This \(L_{z_n}\)
argument is not that source’s Gate A, and it is not a premise of Gate C.
Do not carry “Gate A killed” into the band-exponent chain.

Parent: [`GATE-A-POSITIVE-ASSEMBLY-2026-10-07.md`](GATE-A-POSITIVE-ASSEMBLY-2026-10-07.md).
Probe: `scripts/ns_attacks/analytic_load_lower_bound.py`.

---

## Kill statement

Under Convention F2 and the authorized coefficient
\[
\rho_a(z)
=
\frac1{2z}
\left(\sum_{b\in B_a(z)}\frac{C_{a,b;z}^2}{b^2}\right)^{1/2},
\]
define the all-shape load
\[
L_z
:=
\sum_a\rho_a(z).
\]

**Theorem.** There exists an infinite sequence of high shells
\(z_n\to\infty\) such that
\[
\boxed{L_{z_n}\to\infty.}
\]
Consequently, straight positive shared-budget assembly cannot keep the
equal-allocation load uniformly controlled as the high shell tends to
infinity. Finite-family success (17/32/51) is not withdrawn — it remains
laboratory evidence at finite scope.

---

## Sequence

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

## Load lower bound

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
representationsations as a sum of two squares. Therefore
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
L_{z_n}\to\infty.
\]

---

## What is not claimed

- Criterion (17), Clay, global regularity.
- Withdrawal of the 17/32/51 restricted-family theorems.
- That \(\mathcal R(z)=L_z/\sqrt{z}\) diverges (the subnet only forces
  \(L\to\infty\); full F2 may give stronger relative growth).
- Any substitute of swirl / Ring / B41 for this kill.

---

## Program consequence

The subnet forces \(L_{z_n}\to\infty\) for this positive load. That is not
the sharp-band source’s Gate A, and it does not close Gate C.

---

## STATUS

\(L_{z_n}\to\infty\) FOR THIS LOAD (\(z_n=2n^2\)).
GATE A, AS NAMED BY THE SHARP-BAND SOURCE: DIAGNOSTIC AND UNRESOLVED.
NOT A PREMISE OF GATE C.
(17) NOT CLAIMED.
NS NOT SOLVED.
