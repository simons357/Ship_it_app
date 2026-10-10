# Gate D vorticity-form evaluator — October 9, 2026

Candidate `vorticity_signed.py` implements `T_sc=T_full-T_rep` by using the identity `(u·∇)u=∇(|u|²/2)-u×curl(u)` and divergence-free receivers. Each squared-radius shell requires inverse FFTs of velocity and vorticity but no per-shell forward nonlinear FFT or Leray projection.

**Input assumptions:** Hermitian-symmetric, divergence-free Fourier coefficients; same spherical Galerkin mask used by the stepper; high-pass K is diagnostic only. No silent coefficient threshold. Original stepper unchanged.

**Tests:** `python -m unittest -v test_vorticity_signed` — 2 tests passed, covering positive six-mode witness and random dense fields at N=4,5,7.

**One-off benchmark, OPENBLAS_NUM_THREADS=1, L=2π** (times seconds, not stabilized):
| grid | N | shells | previous FFT | vorticity | speedup | abs diff |
| 18³ | 4 | 14 | 0.0274 | 0.0161 | 1.71× | 0 |
| 24³ | 5 | 22 | 0.1121 | 0.0334 | 3.35× | 1.5e-15 |
| 30³ | 7 | 42 | 0.4483 | 0.1204 | 3.72× | 0 |
| 39³ | 12 | 121 | 4.1375 | 1.3052 | 3.17× | 4.9e-14 |

**Not production certified:** no N=128/160 benchmark, no hard memory cap, no rigorous floating-point forward-error bound, no demonstrated R³ domain convergence, no DA cutoff preregistration. The per-shell inverse FFTs still scale with shell count. A numerical error certificate must account for cancellation in `T_full-T_rep` and FFT accumulation; measured agreement alone is insufficient.

**Gate D OPEN / BLOCKED. No frozen Gaussian trajectory run.**
