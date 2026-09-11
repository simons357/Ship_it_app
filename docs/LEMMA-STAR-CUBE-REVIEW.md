# SuperGrok analytic review — scored against the lock

11 September 2026. They sent a review of
§§3–5, two filenames, and a boxed
\(c_{\mathrm{box}}n^3+O(n^2)\).
**★ OPEN. NS not solved.
Do not start H1. Do not stamp a kill.
Do not rewrite the boxed claim.**

Cube family: [`LEMMA-STAR-CUBE.md`](LEMMA-STAR-CUBE.md).
Identities: [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Core: [`LEMMA-STAR-CORE.md`](LEMMA-STAR-CORE.md).

Probe: `python3 scripts/lemma_star_cube_review.py`

`Lemma_Star_Analytic_Review_2026-09-11.md`
and `verify_box_integrals.py` are **not**
on this branch. Attachment marks only.

---

## What they claimed

No defect in the asymptotic argument
in §§3–5. Fresh exact-arithmetic
recompute of the polynomial integrals.
Every reported constant matches, including

\[
N_0=0,\qquad M_0=\frac{89567}{134534400}>0.
\]

Explicit \(n\)-independent error constants.
Faces of the cube justify \(O(1/n)\) by
polyhedral Riemann-sum theory. Therefore

\[
\mathcal R_\star(v_n)=c_{\mathrm{box}}n^3+O(n^2),
\qquad
c_{\mathrm{box}}\approx 3.967267736160021\times 10^{-8}>0.
\]

Larger numerical samples unnecessary.
External specialist review pending.

---

## What this book recomputed

Profile \(F(\xi)=\xi_1(-\xi_1^2+i\xi_2)(-\xi_2,\xi_1,0)\)
on \([-1,1]^3\). Quadratic moments of
\(|F|^2\) are exact fractions:

\[
\begin{aligned}
E_0&=\frac{736}{315},&
X_0&=\frac{21536}{5775},\\
Y_0&=\frac{91342432}{14189175},&
Z_0&=\frac{280364512}{23648625},\\
\Lambda_0&=\frac{2854451}{1653561},&
D_0&=\frac{87136986657536}{117313332010875}.
\end{aligned}
\]

Their \(L_1,L_2,L_3\) match \(X_0,Y_0,Z_0\).
Their \(L_0=7360/315\) is \(10E_0\)
(extra zero). Their \(\Lambda_0\)
denominator is \(1653661\), not
\(1653561\). Their \(D_0\) denominator
is ten times too large, up to a few
trailing digits.

If \(M_0=89567/134534400\) is granted,

\[
c_{\mathrm{box}}
=
\frac{M_0^2}{D_0 E_0 Y_0}
=
\frac{15230857789248289399575}{383913030381722309395629473792}
\approx 3.967267736160021\times 10^{-8}.
\]

The new float matches that corrected
quotient. The old dump fraction was
off by \(100\). “Every reported constant
matches” is false of the dump they
reviewed.

---

## What the lock still does not give

\(N=0\) on the discrete cube (exact on
even \(n\)). That matches \(N_0=0\) as
a sample, not as a hexagon expansion.

\(M_0\) is the transfer / hexagon claim.
It is not regenerated here from the
locked triad. Locked \(T_c/n^2\):

| \(n\) | \(T_c/n^2\) | vs \(M_0\) |
|---|---|---|
| 2 | \(0.03783\) | \(57\times\) |
| 4 | \(0.00775\) | \(12\times\) |
| 6 | \(0.00365\) | \(5.5\times\) |
| 7 | \(0.00291\) | \(4.4\times\) |

A linear fit of \(T_c/n^2\) against
\(1/n\) has a **negative** intercept.
A two-parameter \(a+b/n+c/n^2\) fit
on \(n=4,5,6\) intercepts near
\(0.003\), not \(0.000666\).
Through \(n=7\) the claimed leading
term is not dominant.

\(\mathcal R_\star/n^3\) at \(n=7\) is
\(5.75\times 10^{-8}\), about
\(1.45\times\) the corrected
\(c_{\mathrm{box}}\). A short
quadratic intercept near \(4.0\times 10^{-8}\)
is a clue. It is not
\(\mathcal R_\star\to\infty\).

Polyhedral \(O(1/n)\) for a polynomial
on a cube covers \(E,X,Y,Z\).
\(T_c\) is a constrained 6-D triad sum.
Faces of \(Q=[-1,1]^3\) do not by
themselves give \(n\)-independent
constants for that kernel.

§§3–5 are not on this branch.
A review of a missing manuscript is
not a lock.

---

## Keep

- Exact quadratic integrals of \(|F|^2\)
  can be checked. They were.
- \(N=0\) on the locked samples.
- Growing cube \(\neq\) \(v(n\cdot)\).
- External specialist still pending.
  They said it.
- ★ \(\Rightarrow\) GR one way.
  This is not NSE, not H1.

---

## Correct

**“No defect in §§3–5.”**
Those sections are not here.
The dump they treated as clean had
digit defects in \(L_0\), \(\Lambda_0\),
\(D_0\), and \(c_{\mathrm{box}}\).

**“Every reported constant matches.”**
\(L_1,L_2,L_3\) match. The rest need
corrections. \(M_0\) was not recomputed
from the locked \(T_c\).

**“Larger samples are unnecessary.”**
Not for this book. At \(n=7\) the
claimed \(M_0\) is still a small
piece of \(T_c/n^2\).

**Boxed unrestricted ★ is false.**
The implication needs \(M_0\) and a
remainder theorem for the locked
triad, both still off-branch.
Kill is \(\mathcal R_\star(v_n)\to\infty\).
Largest locked value is
\(1.97\times 10^{-5}\) at \(n=7\).
N-shell still sits at \(0.610\).

**Rewrite the working-file status.**
No. Restricted replacements stay
new lemmas.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| LSrev_files_on_branch | **fail** | review file and script absent |
| LSrev_quad_moments | **pass** | \(E_0,X_0,Y_0,Z_0,D_0\) sit |
| LSrev_reported_constants_clean | **fail** | digit defects in the dump |
| LSrev_N0_discrete | **pass** | \(N=0\) on the lock |
| LSrev_M0_from_lock | **fail** | \(T_c/n^2\) has not settled |
| LSrev_no_defect_35 | **fail** | §§3–5 not here |
| LSrev_samples_unnecessary | **fail** | \(n=7\) still far from \(M_0\) |
| LSrev_unrestricted_killed | **fail** | unrestricted ★ is OPEN |
| LSrev_ns_h1 | **fail** | not NSE; not H1 |

★ stays OPEN. Kill lane stays LIVE.
Do not start H1.
Do not stop patching.

NS not solved.
