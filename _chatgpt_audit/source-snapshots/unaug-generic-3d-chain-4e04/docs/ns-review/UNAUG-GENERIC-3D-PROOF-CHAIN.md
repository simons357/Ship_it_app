# Unaugmented generic 3-D Navier–Stokes — proof chain

Jonathan Simons  
11 September 2026

**Scope.** Classical incompressible Navier–Stokes only. No extra field. No force. No \(Q\)-operator.

**This is a chain of reductions. It is not a proof of global regularity.**

---

## Claim line

Lemma Star is in the generic 3-D chain and is finished.  
The remainder is \(T_{j\leftarrow j}\).  
Generic unaugmented 3-D regularity is not claimed.

---

## PDE

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,
\qquad
\nabla\cdot u=0
\quad\text{on }\mathbb{T}^3\text{ or }\mathbb{R}^3.
\]

Finite energy \(X=\|u\|_{L^2}^2\). Vorticity \(\omega=\nabla\times u\). Enstrophy \(Z=\|\omega\|_{L^2}^2\). Palinstrophy \(P=\|\nabla\omega\|_{L^2}^2\).

The frequency weight in Step 1 is also written \(\omega(k)=|k|\). That is not vorticity.

---

## Step 0 — energy (closed)

\[
\tfrac12\dot X=-\nu\|\nabla u\|_{L^2}^2\le 0.
\]

No remainder. Keep.

---

## Step 1 — spectral center and Lemma Star (\(\Lambda_\ast\), \(\omega_\ast\))

Define the energy-weighted barycenter of the spectrum

\[
\Lambda=\frac1X\sum_k\omega(k)\,|u_k|^2,
\qquad
\omega(k)=|k|.
\]

The exact organizing identity is

\[
\Lambda'=\frac2X\bigl(T_c-\nu D_s\bigr),
\qquad
T_c=\sum_k\omega(k)\,J_k,
\qquad
\sum_k J_k=0.
\]

\(D_s\ge 0\) is the viscous spread in the same weighting. The identity names it. \(J_k\) is the modal energy flux; the nonlinear piece sums to zero. Lemma Star does not bound \(D_s\) or \(T_c\).

**Lemma Star.** Fix any constant \(\omega_\ast\in\mathbb{R}\). Because \(\sum J_k=0\),

\[
T_c=\sum_k\bigl(\omega(k)-\omega_\ast\bigr)J_k.
\]

The unknown \(\Lambda\) does not appear on the right. This is bookkeeping. It is not a bound on \(T_c\). It forbids the circular move “bound \(T_c\) by a copy of \(\Lambda'\).”

Keep Lemma Star in every later identity. Do not claim it controls \(\Lambda\).

---

## Step 2 — triad decomposition of \(T_c\) (closed as an identity)

Nonlinear transfer factors through closed triads \(p+q+k=0\) (or \(p+q=k\)). Write

\[
T_c=\sum_{\text{triads}}\tau(p,q,k).
\]

Each triad conserves energy: the three modal fluxes sum to zero. Signed cancellation

\[
C=\frac{\sum_{\tau>0}\tau}{\sum|\tau|}
\]

is a diagnostic, not an estimate.

Keep the decomposition. Do not bound \(\sum_{\tau>0}\tau\) by \(\Lambda'\).

---

## Step 3 — shell budget (Door 1)

Dyadic shells \(S_j=\{k:|k|\sim 2^j\}\), shell energy \(e_j\), shell enstrophy \(Z_j\), shell palinstrophy \(P_j\).

\[
\tfrac12\dot e_j = T_{j\leftarrow j}+\sum_{\ell\neq j}T_{j\leftarrow\ell}-\nu Z_j.
\]

- Cross-scale blocks \(T_{j\leftarrow\ell}\), \(\ell\neq j\): Young / paraproduct. Treat as standard. Constants exist; they are not the obstruction. Precise bounds and summability are **not supplied** by this note.
- Same-scale block \(T_{j\leftarrow j}\): three waves of comparable wavelength (HHH). This is the remainder.

Define

\[
\rho_j=\frac{\lvert T_{j\leftarrow j}\rvert}{P_j}.
\]

Because \(\rho_j\) is normalized by palinstrophy \(P_j\), the comparison \(\rho_j<\nu\) belongs to the enstrophy–palinstrophy estimate in (A). **It is not an absorption criterion for the displayed shell-energy budget, whose viscous term is \(\nu Z_j\).** If \(\rho_j<\nu\) held on every shell, the same-scale block would be absorbed by palinstrophy in (A). That comparison is not proved for generic data, and it does not close \(\dot e_j\).

Lemma Star still applies inside each shell: shift the shell weight by a constant before summing fluxes.

---

## Step 4 — measured facts (not theorems)

On exact (non-aliased) Galerkin pairings:

- 2-D / 2.5-D disks: identity residual \(10^{-16}\). Adversarial \(\rho\) parks near \(0.02\) and relaxes under evolution. Growing \(K_{\max}\) to \(O(10^2)\) modes did not produce an \(O(1)\) leak on the restricted class.
- 3-D helical snapshots at small \(K_{\max}\): cancellation \(C\sim 1/2\), snapshot \(\rho=O(10^{-2})\), sign of HHH flips with phases.
- 3-D helical orbits that were run: triad-phase occupancy on HHH sat at \(1\). Vorticity-direction alignment stayed \(\approx 1/2\). Phase lock and geometric depletion are different facts.
- 32-mode exact 3-D disk, \(\nu=0.03\): \(\lvert T_c\rvert/D_s\) fell from \(0.021\) to \(0.002\).

These support the organization. They do not pass to \(K_{\max}\to\infty\) or to generic data.

Recorded separately: [`NS3D_PROGRESS_NOTE.md`](../NS3D_PROGRESS_NOTE.md).

---

## Step 5 — where the generic 3-D chain stops

To close generic unaugmented 3-D NS one still needs one of the following, with no copy of \(\dot e_j\), \(\dot Z\), or \(\Lambda'\):

**(A)** A bound

\[
\lvert T_{j\leftarrow j}\rvert \le \varepsilon\nu P_j +R(X,Z)
\qquad\text{with \(R\) controlled by energy and known quantities.}
\]

**(B)** Depletion: a factor \(\sin\phi\) or \(1-\alpha\) from vorticity-direction mismatch on HHH that makes (A) true. Occupancy \(1\) on small orbits means phase rotation is not supplying this by itself.

**(C)** A restriction of the data (axisymmetry, etc.). That is a different theorem, written in the swirl note, not here.

None of (A)–(B) is proved for generic 3-D in this chain.

---

## Step 6 — what would finish the chain (not claimed)

Assume (A) with \(\varepsilon<1\). Sum on shells, absorb, use energy from Step 0 and standard Sobolev interpolation. Then \(Z\) stays finite on any finite interval, BKM applies, the solution stays smooth. That last paragraph is the shape of a proof. The missing hypothesis is (A) or (B).

Lemma Star is used before (A), not instead of (A).

---

## Relation to the swirl paper

The swirl note is not a step in this chain. It is a subclass:

- axisymmetric with swirl, unaugmented;
- bulk pairing as in Steps 2–4;
- axial remainder \(T_{\mathrm{ax}}=\int_{r<\delta}G\,\partial_z(F^2)\,dm\);
- Young: \(\int_0^T\|F\|_{L^4(B_\delta)}^4\,dt<\infty\) prevents blow-up from the swirl source.

Deposit swirl separately. Do not insert it as “Step 7 of generic 3-D.”

Subclass note: [`SWIRL_AXIAL_REDUCTION.md`](../SWIRL_AXIAL_REDUCTION.md). Existing Φ-renorm faces: [`docs/papers/swirl/`](../papers/swirl/).

---

## Files this chain uses

| File | Role |
| --- | --- |
| [`SWIRL_AXIAL_REDUCTION.md`](../SWIRL_AXIAL_REDUCTION.md) | subclass only — not Step 7 |
| [`NS3D_PROGRESS_NOTE.md`](../NS3D_PROGRESS_NOTE.md) | measurements — not theorems |
| [`PROGRESS_POST.md`](../PROGRESS_POST.md) | public language of the claim line |
| [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md) | honesty card — dissipation threshold and refuse list |

Machine lock: [`data/ns_proof_chain/2026-09-11.json`](../../data/ns_proof_chain/2026-09-11.json).

---

## Terminology lock (do not upgrade)

This document’s **Lemma Star** is the \(\omega_\ast\) centering identity in Step 1. It is finished as bookkeeping. It does **not** bound \(T_c\), control \(\Lambda\), or close regularity.

It is **not** the later unrestricted ratio bound \(\sup\mathcal{R}_\star<\infty\) discussed on other branches. Establishing the identity does not establish that bound.

Do not:

- bound \(T_c\) or \(\sum_{\tau>0}\tau\) by a copy of \(\Lambda'\);
- bound \(T_{j\leftarrow j}\) by \(\dot e_j\), \(\dot Z\), or \(\Lambda'\);
- treat \(\rho_j<\nu\) as shell-energy absorption into \(\nu Z_j\);
- treat \(\rho_j<\nu\) as a proved theorem for generic data;
- treat occupancy \(1\) and alignment \(\approx 1/2\) as depletion;
- insert swirl, \(Q\), or an extra field as a later step of this chain;
- claim Clay Statement B / generic 3-D regularity from this page.

---

## Status map

```
Step 0  energy                 CLOSED
Step 1  Lemma Star (ω_* shift) FINISHED as bookkeeping — not a bound
Step 2  triad decomposition    CLOSED as an identity
Step 3  shell budget (Door 1)  ORGANIZED — remainder named
Step 4  measurements           FACTS on finite exact disks — not theorems
Step 5  (A) or (B)             NOT PROVED for generic 3-D
Step 6  absorb + BKM           SHAPE of a proof — hypothesis missing
swirl                          SEPARATE subclass — not Step 7
```

**One line.** Lemma Star finished. Remainder \(T_{j\leftarrow j}\). Generic unaugmented 3-D regularity not claimed.
