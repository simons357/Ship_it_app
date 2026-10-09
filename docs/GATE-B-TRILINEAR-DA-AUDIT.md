# Independent DA audit — Gate B trilinear inequality

9 October 2026.
**Domain Architect, independent of the counting campaign.
CS-3 fails. θ ≥ ½ for nonnegative Q_x is a dilation identity, not a
counting corollary. Not (17). NS not solved.**

This is the audit requested for the all-radii / distinct-shell /
Cauchy–Schwarz chain. Agreement with a previous agent is not
validation. Canonical SFE status remains unresolved.

Code: `domain_architect/trilinear_audit.py`.
CLI: `python -m domain_architect --trilinear-ns`.
Geometry: [`GATE-B-ALL-RADII-LEMMA.md`](GATE-B-ALL-RADII-LEMMA.md).
Dilation lower bound: `scripts/ns_attacks/nonnegative_qx_dilation.py`.

---

## Object

Specified nonnegative assembly of Dish #3,

\[
Q_x(f)
=\sum_{\substack{(x,y,z)\\x<y<z}}
C_{xyz}\,f_y f_z,
\qquad
f\ge 0,\quad C_{xyz}\ge 0,
\]

with the September 20 majorant \(C_{abc}\), energy \(E=\sum f_x^2\),
enstrophy \(\Omega=\sum x f_x^2\), and high shell \(\Lambda\).

Claimed chain:

1. all-radii two-point counting,
2. distinct-shell hypothesis,
3. every Cauchy–Schwarz,
4. a weighted trilinear / \(\lVert Q\rVert_2\) inequality,
5. promotion of the Gate B exponent obstruction.

---

## Step table

| Id | Claim | CS? | Verdict |
|---|---|---|---|
| G1 | Two independent planes + sphere, all radii, ≤ 2 points | no | **pass** |
| H-shell | Distinct shells ⇒ independent normals | no | **fail** |
| G2 | One input, two shells: μ ≤ 2 at large frequency | no | **fail** (circle; 4-point example) |
| G3 | Two independent inputs, common closer ≤ 2 | no | **pass** (this is G1) |
| CS-1 | \(\sum f_x Q_x\le\sqrt{E}\,\lVert Q\rVert_2\) | yes, once, on the low index | **pass** |
| CS-2 | Inner CS + \(Y\)-charge → ρ-face \(S\) | yes, inner partner sum | **pass on a different object** |
| CS-3 | Counting ⇒ weighted trilinear / \(\lVert Q\rVert_2\) | missing Schur/CS on the \(Q\)-graph | **fail / gap** |
| LB | Similar-triad dilation: uniform powers need \(\theta\ge\tfrac12\) | none (homogeneity) | **pass** |
| PROMOTE | Promote obstruction from the counting chain | CS-3 | **split** |

---

## Cauchy–Schwarz, one by one

**CS-1.** \(\langle f,Q\rangle\le\lVert f\rVert_2\lVert Q\rVert_2\) with
\(\sum f_x^2=E\). Valid for every real \(f,Q\). Does not use shells,
multiplicity, or nonnegativity. Does not bound \(\lVert Q\rVert_2\).

**CS-2.** Inner CS on partners after \(Y\)-charging the high legs.
Algebraically valid. It produces the diagnostic \(\rho\)-face
\(T^+\le 2S\sqrt{E}\,Y\), which is **not** \(\lVert Q\rVert_2\) of
Dish #3. A \(\theta\approx 0\) reading of \(S\) does not control the
explicit nonnegative assembly.

**CS-3.** The missing step. A two-point count on some incidence graph
does not automatically give

\[
\lVert Q(f)\rVert_2
\le
K\Lambda^\theta\Omega(f)
\]

or any other weighted trilinear bound. Even after G3, one still has
to (i) identify that graph with the sum that defines \(Q_x\),
(ii) apply a Schur / Cauchy–Schwarz estimate with the \(C\)-weights,
and (iii) show that \(C\) does not put back a positive power of
\(\Lambda\). Dish #3 groups by the low **shell**, and the one-input
two-shell locus that actually appears there is the circle of G2, not
the two-point set of G1. CS-3 fails.

---

## Promotion

The Gate B exponent obstruction for this nonnegative \(Q_x\) is

\[
\lVert Q(f)\rVert_2
\le
K\Lambda^\theta\Omega(f)
\quad\text{for all such }f
\quad\Longrightarrow\quad
\theta\ge\tfrac12.
\]

That is a homogeneity identity on the similar-triad family
(\(C\) has degree three in the dilation \(t\), \(\Omega\) has degree
two, so the ratio scales as \(\Lambda^{1/2}\)). Mean
\(\hat\theta=1/2\) on \(n=4,8,16,32\) to machine precision. It does
**not** depend on all-radii counting.

**Promote** \(\theta\ge\tfrac12\) for the specified nonnegative
\(Q_x\), by dilation, not by CS-3.

**Do not promote** a new all-radii trilinear upper bound.

Exact optimal \(\theta\) remains **OPEN**. Signed transfer remains
**OPEN**. \(C_{abc}\) remains an upper majorant, not a coercive cost.
Gate A remains UNRESOLVED / DIAGNOSTIC ONLY. (17) OPEN.

---

## Functional roles (FRA, not a physical law)

| Role | Occupant here |
|---|---|
| \(P\) | lattice / divergence-free / plane constraints |
| \(H\) | \(C_{abc}\) majorant (upper bound) |
| \(\psi\) | nonnegative shell amplitudes \(f\) |
| \(\lambda\) | squared radius / dilation \(t\) / \(\Lambda\) |
| \(g\) | \(\mathbb Z^3\) Fourier lattice, Euclidean \(\mathbb R^3\) |
| \(N\) | trilinear assembly \(Q_x\) |
| \(\Phi\) | \(\lVert Q\rVert_2/\Omega\) and the remaining power \(\theta\) |

This is organizational classification. It is not a derivation of
Navier–Stokes, not SFE, and not Clay.

---

## Lock

Independent DA verdict: CS-1 pass; CS-2 pass on a different object;
CS-3 fail. Distinct-shell hypothesis fail as stated. G1 pass. Gate B
lower bound for nonnegative \(Q_x\): **proved by dilation**.
All-radii trilinear inequality: **not established**.
(17) OPEN. NS not solved.
