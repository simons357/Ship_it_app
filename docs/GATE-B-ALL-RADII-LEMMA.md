# All-radii geometric counting

9 October 2026.
**Euclidean two-plane+sphere: pass. Generic triad multiplicity ≤ 2: fail.
Counting does not give the Dish #3 trilinear bound. Not (17).**

Parents: [`GATE-B-TRILINEAR-DA-AUDIT.md`](GATE-B-TRILINEAR-DA-AUDIT.md),
[`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).
Checker: `scripts/ns_attacks/all_radii_counting.py`.

---

## Lemma G1 (all radii)

Let \(n_1,n_2\in\mathbb R^3\) be linearly independent, and let
\(c_1,c_2,R^2\in\mathbb R\). The system

\[
n_1\cdot x=c_1,\qquad
n_2\cdot x=c_2,\qquad
\lvert x\rvert^2=R^2
\]

has at most two solutions \(x\in\mathbb R^3\), hence at most two
lattice solutions. The count does not depend on \(R\).

Proof: the two planes cut out an affine line
\(x=x_0+t\,\widehat d\) with \(\widehat d\parallel n_1\times n_2\).
Substituting into the sphere produces a quadratic in \(t\).

---

## What the two-output geometry actually is

Three spheres \(\lvert r\rvert^2=\rho\), \(\lvert r+p\rvert^2=\gamma\),
\(\lvert r+q\rvert^2=\delta\) are equivalent to G1 with normals \(p\)
and \(q\). That is a **common closer** of two input wavevectors:

\[
2p\cdot r=\gamma-\rho-\lvert p\rvert^2,\qquad
2q\cdot r=\delta-\rho-\lvert q\rvert^2.
\]

This is **not** the geometry of a single Fourier triad with one fixed
leg. For fixed \(p\) and two partner shells \(\lvert q\rvert^2=\beta\),
\(\lvert p+q\rvert^2=\gamma\), the radical plane plus residual sphere
is a **circle**. Lattice occupancy can exceed two at every scale.

Counterexample, arbitrarily dilatable:

\[
p=(0,0,2),\qquad
\lvert q\rvert^2=5,\qquad
\lvert p+q\rvert^2=5
\]

has four partners \(\{(\pm 2,0,-1),(0,\pm 2,-1)\}\). Dilating by an
integer \(t\) keeps four points on a larger circle.

---

## Distinct-shell hypothesis

\(\lvert p\rvert^2\neq\lvert q\rvert^2\) does **not** make the normals
independent. \(p=(1,0,0)\), \(q=(2,0,0)\) are distinct shells and
parallel. The correct extra hypothesis is linear independence of the
wavevectors.

---

## What this does not do

It does not bound the number of lattice realizations of a shell triad
\((a,b,c)\). It does not identify the incidence graph summed in

\[
Q_x=\sum C_{xyz}\,f_y f_z.
\]

It does not, by itself, produce a weighted trilinear inequality.
See CS-3 in the DA audit.

Finite-radius scans with independent \(p,q\) stayed at most two for
the common-closer system. That supports G1 on that system. It does
not close Gate B's \(\lVert Q\rVert_2\) bound.

---

## Lock

G1: pass (Euclidean, all radii).
One-input two-shell \(\mu\le 2\): fail (circle).
Distinct-shell \(\Rightarrow\) independent normals: fail.
Two-input common closer \(\mu\le 2\) given independence: pass on the
scanned sample, as G1 predicts.
Trilinear / \(\lVert Q\rVert_2\) from counting: **gap**.
(17) OPEN. NS not solved.
