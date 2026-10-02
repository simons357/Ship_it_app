# NS3D progress note — measurements, not theorems

Companion to the 11 September 2026 generic unaugmented 3-D chain.

**These are measured facts on exact (non-aliased) Galerkin pairings.**  
**They do not pass to \(K_{\max}\to\infty\) or to generic data.**  
**They do not prove (A) or (B). They do not close regularity.**

Chain: [`docs/ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md`](ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md).  
Public language: [`PROGRESS_POST.md`](PROGRESS_POST.md).

---

## What was measured

On exact (non-aliased) Galerkin pairings:

| Setting | Observation | What it is not |
| --- | --- | --- |
| 2-D / 2.5-D disks | Identity residual \(10^{-16}\). Adversarial \(\rho\) parks near \(0.02\) and relaxes under evolution. Growing \(K_{\max}\) to \(O(10^2)\) modes did not produce an \(O(1)\) leak on the restricted class. | Not a uniform leak bound. Not 3-D generic. |
| 3-D helical snapshots, small \(K_{\max}\) | Cancellation \(C\sim 1/2\). Snapshot \(\rho=O(10^{-2})\). Sign of HHH flips with phases. | Not a bound on \(T_{j\leftarrow j}\). Not depletion. |
| 3-D helical orbits that were run | Triad-phase occupancy on HHH sat at \(1\). Vorticity-direction alignment stayed \(\approx 1/2\). | Phase lock \(\neq\) geometric depletion. Occupancy \(1\) does not supply \(\sin\phi\) or \(1-\alpha\). |
| 32-mode exact 3-D disk, \(\nu=0.03\) | \(\lvert T_c\rvert/D_s\) fell from \(0.021\) to \(0.002\). | Finite disk. Not \(K_{\max}\to\infty\). Not generic data. |

These support the organization of Steps 1–3 (barycenter, triads, shells). They are not estimates.

---

## Two facts that must stay separate

1. **Phase occupancy.** On the orbits that were run, HHH triad-phase occupancy sat at \(1\). Phase rotation is not, by itself, the depletion required for (B).
2. **Direction alignment.** Vorticity-direction alignment stayed \(\approx 1/2\). That is a measured geometric diagnostic. It is not a factor \(\sin\phi\) or \(1-\alpha\) proved on generic HHH.

Phase lock and geometric depletion are different facts.

---

## Scope lock

- Exact (non-aliased) pairings only.
- Restricted classes (disks, helical snapshots / orbits, 32-mode disk).
- No uniform conclusion as \(K_{\max}\to\infty\).
- No generic-data theorem.
- \(\rho_j<\nu\) on a sample is not (A).
- \(\lvert T_c\rvert/D_s\) falling on one disk is not a bound on \(T_c\).

**Organization supported. Remainder still \(T_{j\leftarrow j}\). Regularity not claimed.**
