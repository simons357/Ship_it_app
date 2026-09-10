# DA-NS-2 — what was kept from the overnight note

7 September 2026. Classical unaugmented NS.
No Q1. Keep 1/r^4. Not RH. Not a close.

Taken from the September 6–7 showdown
dossier. Useful parts only. The Joint
Gap–Charge budget is a target, not a
theorem.

Reproduce the finite checks:
python3 -m unittest tests.test_centered_barycenter

---

## Leftover (same hole as WRITE (6))

On Galerkin n, fixed θ in [0, 1):

K = [T_c − θ ν D_s]_+ / Y

DA-NS-2: sup_n ∫_0^T K dt ≤ F(ν, T, u0) < ∞.

If that sits, Λ stays bounded, then
X ≤ |u0|_2^2 Λ, then continuation.
The implication is the usual skeleton.
The integral is the hole.

**Lemma★ (locked 10 September 2026).**
Energy-budget writing of the same leftover:
T_c ≤ θ ν (Z−Λ Y) + C_0 ν^{-1} ||u||_2^2 X Λ,
C_0 geometry-only. Would freeze Λ in this
packaging. **Not proved.** Blocked at a
3D product / Agmon bound on T_c (HH→L).
K=0 absorption is dead. Numeric survival
is not a proof. File: docs/LEMMA-STAR.md
PR 48 is the five-lane drill, not a close.

Live geometric path: H1 (A_bad a priori).
Same leftover class, different integral.
Do not merge. Do not add K(t) to the PDE.
Packet: docs/UNAUGMENTED-NS-CHAIN.md

---

## Identities that sit (algebra)

X = |A^{1/2} u|_2^2,  Y = |A u|_2^2,
Z = |A^{3/2} u|_2^2,  Λ = Y/X.

N = −⟨B(u,u), A u⟩,
M = −⟨A B(u,u), A u⟩,
T_c = M − Λ N.

D_s = Z − Λ Y = |A^{1/2}(A − Λ)u|_2^2 ≥ 0.

(log Λ)' = 2/Y (T_c − ν D_s).

If p_m = a_m |u_m|^2 / X, then
Λ = Σ p_m a_m and D_s/X = Σ p_m (a_m − Λ)^2.

T_c is centroid velocity, not “variance
growth.” An identity is not DA-NS-2.

---

## Kills that stay killed

- Variance absorption T_c ≤ c ν D_s: false
  (cubic vs quadratic under amplitude).
- Charge-only close: two-triad state has
  Q_a,Γ = 0 and T_c,Γ^het > 0. Exact split
  T_c^het = 2 κ^3 Q_a + ρ, and ρ is needed.
- Quadratic data decide the sign: phase
  twins share X,Y,Z,Λ,D_s and flip T_c.
- Automatic dephasing: 2D3C half-turn
  lock keeps 0/π rays. That sector is
  separately regular.
- Frozen log-charge at θ = 1: the needed
  endpoint is θ < 1; (1−θ) ν D_s/Y is
  leftover.
- SND as a close: still fail.
- Q1 / de-augmentation: still fail.
  Theorem A is a different PDE.
- Serrin / BKM as the last line: still
  an if.

---

## Next write (not sitting)

Joint Gap–Charge Epoch Budget: charge,
radial covariance, moving-barycenter
error, homochiral drift, cross-band
flux, phase/far terms, one-use
dissipation, summable resets. All
together, cutoff-uniform. If the last
line is ∫ D_s/Y, sup Λ, ∫ Y, or a
continuation norm, stop.

---

## Share

Title: Map of ordinary NS — centered
barycenter identities and named hole
DA-NS-2, not a proof.

docs/UNAUGMENTED-NS-CHAIN.md
docs/SHARE-MAPS.md
