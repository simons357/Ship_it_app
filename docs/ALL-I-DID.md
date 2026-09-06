# All I did — the proud pile

6 September 2026. Everything you asked to take
home: proof chains, sitting facts, equations,
constants, papers that stay true if titled
right. Leftover closes are not in the finished
pile. You still wrote those maps.

This is yours. “I did this” applies to every
line below.

---

## Finished writes (proud as finished)

**Theorem A.** Extra-stress Navier–Stokes.
Epsilon > 0, beta >= 1/2, 3-torus. Unique
global smooth H1 solution. Different equation
from ordinary NS. Known class in your notation.
Credit Ladyzhenskaya 1968/1969 and
Malek–Necas–Ruzicka 1996.

docs/A-CHAIN.md
docs/A-PROOF-CHAIN.md
docs/AUGMENTED-NS-PROOF-CHAIN.md
tex/theorem-a-q1.tex
docs/THEOREM-A-Q1.pdf
docs/THEOREM-A-DEPOSIT.md

**Theorem P.** On primes, tilde-Q is at least
-1/4.

**H_N floor.** lambda_min(H_N) >= -1 for every N.

**Bridge*.** Two-prime identity, R > -1/2.

**Nonnegative form.** If v >= 0, then
v^T tilde-Q v >= 0.

**Goldbach-shaped corollary.** If the
difference-of-primes vector for even k is
nonzero, R >= -2/9. Not Goldbach’s conjecture.

docs/DA-Q.md
docs/Q6-FLOOR-CHAIN.md
docs/GOLDBACH-CHAIN.md
docs/SPECTRAL-FLOOR-EXPLORATION.md
Zenodo 22045478

**HB thrown out** as a unifier. That throw-out
stands.

---

## Equations you can point at

Extra-stress equation (Theorem A):

d_t u + (u·∇)u = -∇p + ν Δu
  + ε^α P div( |∇u|^β ∇u ),   div u = 0

Energy for that equation:

(1/2) d/dt ||u||_2^2
  + ν ||∇u||_2^2
  + ε^α ||∇u||_{L^{β+2}}^{β+2} = 0

p = β+2.  β >= 1/2 means p >= 5/2.

Ordinary NS leftover form (map, not a close):

dX/dt + ν ||∇ω||_2^2
  <= ε ν ||∇ω||_2^2 + C_ε X R(t)
X = ||ω||_2^2

Theorem P / pairing (Q):

tilde-Q|_P = uu^T + D
u_p = p^{-1/2}
D_pp = 1/p^2 - 1/p
uu^T >= 0, min D = -1/4 at p = 2
so lambda_min(tilde-Q|_P) >= -1/4

H_N = D^{-1/2} tilde-Q D^{-1/2}
lambda_min(H_N) >= -1

Bridge* on v = e_p - e_q:

R(v) = (1/2)(1/p^2 + 1/q^2) - 1/√(pq) > -1/2
because pq >= 6

Goldbach-shaped, v_k nonzero, even k:

R(v_k) >= -2/9 > -1/2

---

## Constants you can point at

- β >= 1/2, p >= 5/2 (this PDE)
- -1/4  Theorem P
- -1    H_N floor that sits
- -1/2  Bridge* barrier (and not a full-Q floor)
- -2/9  Goldbach-shaped corollary
- Q_10 ≈ -1.90  (why full Q > -1/2 is false)
- H_4 ≈ -0.225  (why -3/14 is false)

---

## Proof chains you wrote

Finished this-PDE chain:
docs/A-CHAIN.md

Ordinary NS map (steps 1–5 there, missing
step still open):
docs/UNAUGMENTED-NS-CHAIN.md
docs/NS-PROOF-CHAIN.md
docs/TRACK-B-CHAIN.pdf
docs/DA-FROM.md

RH map (steps 1–5 there, missing step open):
docs/RH-CHAIN.md
docs/RH-PROOF-CHAIN.md

Q floor chain:
docs/Q6-FLOOR-CHAIN.md

Goldbach-shaped chain (not the conjecture):
docs/GOLDBACH-CHAIN.md

Other maps you had written (missing step
open unless said):
docs/YM-PROOF-CHAIN.md
docs/BSD-PROOF-CHAIN.md
docs/HODGE-PROOF-CHAIN.md
docs/PNP-PROOF-CHAIN.md

Poincaré: literature (Perelman). You
reprinted the map. You did not prove it.
docs/POINCARE-PROOF-CHAIN.md

Packing list:
docs/TAKE-HOME.md
docs/DA-STATUS-PACK.pdf

---

## Papers / deposits that stay true if titled right

Zenodo 22045478  inverse-GCD / Q6 hygiene
Zenodo 22045484  errata / retraction
Keep taped, do not retitle as RH or Goldbach.

Theorem A PDF / tex above: true as this PDE.

These are Q or a different equation, not BSD/RH:
22050962, 22050963 (conditional), 20552682
22045467, 22045474, 22050978

---

## Corrections you can also own

Full Q floor > -1/2: false.
H_N >= -3/14: false.
GNC: withdrawn.
Phi-cancel as ordinary NS: dropped.
HB as unifier: thrown out.

---

## Not in the finished pile

Ordinary NS. RH. BSD. Hodge. YM mass gap.
P vs NP. Axisymmetric-with-swirl ordinary NS.
Goldbach’s conjecture.

You wrote the maps. You did not finish those
closes. The maps still count as work you did.

---

GitHub PR 24, branch
cursor/unaugmented-r4-vorticity-f80e
https://github.com/simons357/Ship_it_app/pull/24

This chat:
https://cursor.com/agents/bc-01a026a4-cf05-7637-8c16-cd4b7032f80e
