# Gate 71E — branch, eliminate, classify

**27 September 2026.** Finite algebraic test of the 3-D
unequal-length \(2\times 4\) additive patch.
Ordinary NS is not solved. DA-NS-2 stays **OPEN**.
Unrestricted \(\sup\mathcal R_\star<\infty\) stays **KILLED**.
Soft X silent.

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local exact-shell ★ packets. Does **not** stamp
\(r\sim\kappa^{-1/2}\). Does **not** insert a coherence governor
into the equation.

Machine: `scripts/da_gate_71e_branch_eliminate.py`.
JSON: `results/da_gate_71e_branch_eliminate.json`.
Desk card:
[`../../packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md`](../../packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md).

---

## What was asked

The 27 Sep coherence handoff reduced same-time HH danger to

\[
\lvert F_k\rvert^2=\rho_k^2 N_{\mathrm{eff}}(k)\,Q_k,
\qquad
A_k=\rho_k^2 N_{\mathrm{eff}}(k).
\]

Universal \(\rho_k\le 1-\delta\) is false. Rank-3, energy
normalization, cycle rank, and near-planar closure are parked.
The surviving same-time question is finite:

\[
\text{Can the 3-D unequal-length }2\times 4
\text{ additive patch sustain perfect active coherence?}
\]

That is Gate 71E. The three outcomes are all useful:

| Outcome | Meaning |
|---|---|
| A | no active real solution — first finite intrinsic obstruction |
| B | isolated/tuned active solutions — algebraic rigidity |
| C | positive-dimensional active family — new adversary |

---

## The laboratory

Modes

\[
p_{ij}=p_0+ia+jb,
\qquad
i\in\{0,1\},\quad j\in\{0,1,2,3\},
\]

with \(p_0=(1,1,1)\), \(a=(1,0,1)\), \(b=(0,1,1)\). Then
\(\det[p_0,a,b]=-1\), so the eight wavevectors span \(\mathbb R^3\)
while lying in an affine plane with normal \(n=a\times b=(-1,-1,1)\)
and \(n\cdot p_{ij}=-1\).

Indexed \(z_0,\dots,z_7\):

\[
(1,1,1),\;(1,2,2),\;(1,3,3),\;(1,4,4),\;
(2,1,2),\;(2,2,3),\;(2,3,4),\;(2,4,5).
\]

Eighteen parent pairs. Seven repeated outputs

\[
(2,5,5),\;(3,3,4),\;(3,7,8),\;(4,5,7),\;
(3,4,5),\;(3,6,7),\;(3,5,6)
\]

with multiplicities \(2,2,2,2,3,3,4\). Independent collinearities:
\(\sum(m-1)=11\).

Polarizations are projective in each \(p^\perp\). The seated
\(e_1\)-chart is

\[
U_p=(p\times e_1)+z\,\bigl(p\times(p\times e_1)\bigr).
\]

For two contributions feeding the same output \(K\), coherence is
the frame-free condition

\[
K\cdot(W_{ij}\times W_{mn})=0,
\qquad
W_{pq}=(q\cdot U_p)U_q+(p\cdot U_q)U_p.
\]

Leray drops because \(K\perp W\) is not required to write the
triple; the raw bilinear form already lives in a plane to which
the test is insensitive once \(K\) is dotted into the cross
product. No polarization normalization and no arbitrary coherent
direction are introduced.

The handoff cubic is recovered exactly:

\[
z_0 z_1 z_2-3z_0 z_1 z_3+3z_0 z_2 z_3-z_1 z_2 z_3=0.
\]

It is the first-row output \((2,5,5)\) (pairs \((p_{00},p_{03})\)
and \((p_{01},p_{02})\)). The whole harmonic line

\[
z_j=\frac{t}{j+1},\qquad j=0,1,2,3
\]

satisfies that cubic for every scale \(t\). One factor of the
\((3,3,4)\) equation matches the handoff,

\[
A=4z_0 z_5+3z_0-10z_5-1.
\]

The second factor is chart-dependent. In this frame it is

\[
B=27z_1 z_4-53z_1+53z_4+3.
\]

(The handoff wrote \(45z_1 z_4+8z_1-8z_4+5\). Different
\(p^\perp\) bases are Möbius-related; the factor changes. This
page uses \(B\) as written in the seated \(e_1\)-chart.)

The projected-normal family \(U_p=P_p n\) aligns equal-length
parents and is **not** a solution of the unequal-length system.

---

## Certified active point

\[
z^\star
=
\Bigl(
3,\;\tfrac32,\;1,\;\tfrac34,\;
\tfrac{9}{11},\;\tfrac{15}{19},\;\tfrac{21}{31},\;\tfrac{27}{47}
\Bigr).
\]

Equivalently: first row \(z_j=3/(j+1)\); second row

\[
z_{4+j}=\frac{9+6j}{2j^2+6j+11},\qquad j=0,1,2,3.
\]

**Exact arithmetic.** All eleven triples
\(K\cdot(W_0\times W_i)\) vanish identically over \(\mathbb Q\).
All eighteen parent pairs are live:

\[
\min\lvert W\rvert^2=\frac{440422}{2209}\neq 0.
\]

Branch location:

\[
A(z^\star)=\frac{182}{19}\neq 0,
\qquad
B(z^\star)=0,
\qquad
\text{cubic}(z^\star)=0.
\]

So \(z^\star\) lies on Branch B, not Branch A. After unit
normalization of the eight polarizations, every pair still has
\(\lvert W\rvert>0.04\). This is a fully active real solution.

The first-row harmonic family is therefore **not** a solution
curve of the full system. The cubic allows every \(t\); the
remaining ten equations pin \(t=3\) and determine the second
row.

---

## Isolation (Outcome B, not C)

Three independent checks, all on this book:

1. **\(t\)-scan.** Restrict to first-row harmonics
   \(z_j=t/(j+1)\) and optimize the second row. Cost is machine
   zero at \(t=3\) and \(>10^{-4}\) at \(t=2.5\) and \(t=3.5\).
   Nearby scales are not solutions.

2. **Kernel walk.** The finite-difference Jacobian at \(z^\star\)
   has six stable singular values and two at difference-noise
   level. Walking those two directions produces quadratic
   residual growth \(\lvert r\rvert\sim\varepsilon^2\). You cannot
   travel along them and stay on the variety.

3. **Compact search.** Random starts on the compact chart
   \(\theta\in[0,\pi)^8\cong(\mathbb{RP}^1)^8\) collapse onto
   \(z^\star\) as the dominant active attractor. A second
   numerical hit with unit-\(\lvert W\rvert\) of the same order
   appears; it is **not** given an exact formula here. A third
   hit sits next to a near-dead stratum and is rejected.

Classification:

\[
\textbf{Outcome B — isolated / tuned active solutions.}
\]

Perfect same-time coherence on this patch is possible, but only
through a tuned polarization. It is not empty (not A) and not a
positive-dimensional family (not C). That is algebraic rigidity,
not a universal coherence deficit, and not a same-time HH bound.

Projected-normal remains inactive. Sign-flips and reciprocals of
\(z^\star\) are not solutions.

---

## What this is not

- Not a Navier–Stokes regularity proof.
- Not DA-NS-2.
- Not unrestricted Lemma★ (still killed on \(v_n\)).
- Not a pointwise \(\rho_k\le 1-\delta\) theorem. Single outputs
  can still have \(\rho=1\); this patch shows that *shared-mode
  reuse across eleven repeated-output constraints* can still be
  satisfied, but only when the eight polarizations sit at a
  rigid point.
- Not Leray memory. The test is same-time and uses raw \(W\).
- Not an intrinsic curvature tensor. Frames remain conventional;
  the equations are the intrinsic triples.
- Not a license to re-open parked near-planar closure.

The classical comparable-scale HH problem remains open. The
next honest question is whether \(z^\star\) extends to a larger
additive patch (\(2\times 5\), \(3\times 3\)) or dies there.
That is **not** claimed here.

**NS not solved.**
