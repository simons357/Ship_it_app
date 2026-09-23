# Progress post — unaugmented generic 3-D NS

Public language for the 11 September 2026 chain.  
Full write-up: [`docs/ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md`](ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md).

Classical incompressible Navier–Stokes only. No extra field. No force. No \(Q\).

This is a chain of reductions. It is not a proof of global regularity.

---

## What is finished

**Lemma Star** sits in the generic 3-D chain and is finished.

It is bookkeeping. Because the modal fluxes sum to zero, the cascade \(T_c\) can be centered at any constant frequency \(\omega_\ast\). The unknown spectral barycenter \(\Lambda\) does not appear on the right. That forbids the circular move of bounding the cascade by a copy of \(\Lambda'\).

Lemma Star does not control \(\Lambda\). It is not a bound on \(T_c\).

Energy is closed. The triad decomposition is an identity. The shell budget is organized. Cross-scale blocks are the standard Young / paraproduct pieces; they are not the obstruction.

---

## What remains

The remainder is the same-scale block

\[
T_{j\leftarrow j}
\]

— three waves of comparable wavelength (HHH).

The ratio \(\rho_j=\lvert T_{j\leftarrow j}\rvert/P_j\) is a palinstrophy comparison for (A). It is not absorption into the shell-energy viscous term \(\nu Z_j\).

To close generic unaugmented 3-D one still needs (A) a bound of that block by a piece of palinstrophy plus a remainder controlled by energy, or (B) a depletion factor from vorticity-direction mismatch that makes (A) true. Neither is proved here for generic data.

Small exact disks and helical samples support the organization. Occupancy \(1\) and alignment \(\approx 1/2\) are measured facts. They are not depletion. They do not pass to infinitely many modes or to generic data.

---

## What this is not

Axisymmetric-with-swirl is a subclass, written separately. It is not the next step of the generic chain.

Lemma Star is used before (A), not instead of (A).

**Lemma Star finished. Remainder \(T_{j\leftarrow j}\). Generic unaugmented 3-D regularity is not claimed.**
