# Gate D — Gaussian packet experiment preregistration

**Version:** v1.2 — Proposed DA review.
**Date:** 9 October 2026.
**Program:** Classical, unforced, unaugmented 3D Navier–Stokes.
**Status:** PROPOSED / NOT APPROVED.
**Research gate:** D — dynamical turnover and resource budget.

No production run is authorized. The frozen \(c=200\), \(s\ge 4\) experiment was not launched. Research Gate D remains OPEN / BLOCKED. The letters A–G in section 12 are preregistration approval gates. They are not research Gates A–D.

## 1. Objective

Determine whether the specified Gaussian initial field produces a reproducible downward crossing of the signed-scalene deficit under numerical Navier–Stokes evolution.

A completed, converged episode would be a numerical milestone only. It would not prove regeneration, repeated-episode summability, a cutoff-independent budget, or global regularity.

## 2. Frozen initial condition

The original initial field is defined on \(\mathbb R^3\), using unnormalized Lebesgue measure:

\[
A(x)=e^{-|x|^2/2}(xy,xz,x+yz),\qquad U=\nabla\times A.
\]

The dimensional initial velocity is

\[
u(x,0)=aU(Kx),\qquad a=c\nu K,\qquad c=200.
\]

With \(s=aKt\) and \(u(x,t)=av(Kx,s)\), the nondimensional equation is

\[
\partial_s v=-\mathbb P((v\cdot\nabla)v)+\frac1{200}\Delta v,
\qquad v(0)=U.
\]

The reported audit thresholds \(c_T\approx 3.894\) and \(c_X\approx 145.706366\) are reference diagnostics, not regularity thresholds.

The symbol \(K\) in the original dimensional rescaling must be distinguished from the diagnostic high-pass cutoff \(K_{\mathrm{hp}}\).

The locked stepper curl in `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py` agrees with \(\nabla\times A\) at five random sample points to about \(10^{-11}\). That file was not edited. Its SHA-256 remains `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`. A periodic sample of this field is not the \(\mathbb R^3\) datum.

## 3. Numerical solver

Use the existing periodic Fourier Galerkin solver with a 2/3-dealiased pseudospectral integrating-factor RK4 method.

The time-stepping algorithm must remain unchanged.

The spherical Galerkin mask is

\[
\mathcal M_N=\{m\in\mathbb Z^3:0<|m|\le N\}.
\]

The same mask governs initial projection, nonlinear evolution, and full-field diagnostics.

The high-pass mask \(|m|>K_{\mathrm{hp}}\) is separate and applies only to the signed-scalene diagnostic.

The nonlinear evolution retains interactions involving lower-frequency modes.

## 4. Frozen experiment parameters

| Parameter | Frozen value |
| --- | --- |
| Nondimensional parameter | \(c=200\) |
| Minimum horizon | \(s\ge 4\) |
| Reference cutoffs | \(N=128,160\) |
| Box comparison | \(L,2L\) |
| Timestep comparison | \(\Delta s,\Delta s/2\) |
| Acceptance | Reproducible downward crossing of \(D\) |

The numerical value of \(L\), the baseline timestep, the high-pass cutoff, the periodization method, the checkpoint schedule, and the numerical tolerances are not fixed in this filing. They must be fixed and recorded before production.

No parameter may be silently changed to obtain a crossing.

## 5. Physical-cutoff convention — proposed

On a periodic cube of side \(L\),

\[
k_{\mathrm{phys}}=\frac{2\pi}{L}m.
\]

The frozen labels \(N=128,160\) designate integer-mode cutoffs on the reference box.

For a fixed physical maximum wave number, the proposed matched comparisons are:

| Reference box | Doubled box |
| --- | --- |
| \((L,128)\) | \((2L,256)\) |
| \((L,160)\) | \((2L,320)\) |

The originally specified \((2L,128)\) and \((2L,160)\) cases remain in the protocol and are reported separately.

The matched-resolution cases are additional comparisons, not replacements.

**DA decision required:** Approve or amend this interpretation before any production run.

Under \(N<n/3\), \(N=320\) needs \(n>960\). The current preflight \(576 n^3\) against a 2 GiB ceiling rejects that grid, and it also rejects the reference grids. Those runs stay resource-blocked. See [`GATE-D-CUTOFF-CONVENTION-2026-10-09.md`](GATE-D-CUTOFF-CONVENTION-2026-10-09.md).

## 6. Resource and memory policy

For the existing dealiasing requirement,

\[
N<n/3.
\]

The minimum admissible integer grid size must satisfy this strict inequality.

A planning estimate for twelve live complex128 vector grids is

\[
M_{\mathrm{estimate}}=576n^3\text{ bytes}.
\]

The validation resource ceiling is 2 GiB.

Any configuration whose preflight estimate exceeds that ceiling receives `BLOCKED_RESOURCE` before FFT allocation.

The estimate is not a hard peak-memory guarantee. Where supported, the execution environment must additionally enforce process-level resource limits and record actual peak memory.

No automatic reduction in cutoff, grid size, or precision is permitted.

## 7. Signed-transfer definitions

Use the authoritative 20 September 2026 radius-block definition \(\Phi_{abc}\), with

\[
K_{\mathrm{hp}}^2<a<b<c\le N^2.
\]

Both Hermitian-conjugate triples are counted, with no additional factor of two.

The three September 20 markdown pages are still not in this checkout. This protocol states the counting rules. It does not certify the original Lemma 19 coefficients. The packaged witness agreement \(+4m^3 A^3\) remains uncertified as that lemma. One polarization under \(T=-\operatorname{Re}\langle B,-\Delta h\rangle\) gives \(-4m^3 A^3\). That negative value is not a pass.

The high-pass field is

\[
h=P_{|m|>K_{\mathrm{hp}}}v_N.
\]

The signed deficit is

\[
D(s)=T_{\mathrm{sc}}(h)-\frac{Y_N}{800},
\]

because the nondimensional viscosity is \(1/200\), so \(\nu Y_N/4=Y_N/800\).

Define

\[
X_N=\|\nabla v_N\|_2^2,\qquad
Y_N=\|\Delta v_N\|_2^2,\qquad
d(s)=\frac{D(s)}{X_N(s)}.
\]

For a completed dangerous episode \(I\),

\[
B_I=\int_I d(s)\,ds.
\]

The positive-part budget is tracked separately:

\[
\mathcal S_{K_{\mathrm{hp}},N}(S)=\int_0^S(d(s))_+\,ds.
\]

The production probe is

\[
G(s)=T(v_N(s))-\frac{Y_N(s)}{200}.
\]

Full production \(T\), the signed-scalene transfer \(T_{\mathrm{sc}}\), and \(G\) must never be interchanged. \(B_I\) integrates signed \(d\), including negatives. \(\mathcal S\) is not \(B_I\).

## 8. Numerical evidence policy

The diagnostic must reject invalid Fourier states, including non-finite coefficients, excessive divergence, broken Hermitian symmetry, and coefficients outside the Galerkin mask.

It must not silently repair invalid states or delete small coefficients.

Record:

- \(T_{\mathrm{sc}}\), \(T_{\mathrm{full}}\), and \(T_{\mathrm{rep}}\)
- \(X_N\), \(Y_N\), \(D\), \(d\), and \(G\)
- High-shell energy and mass diagnostics
- Cancellation severity and estimated numerical error
- Numerical verification status
- Runtime, memory, solver hash, and checkpoint identifiers

A heuristic FFT error estimate is not a certified numerical bound.

If supplied certified absolute error bounds are \(E_T\) and \(E_Y\), then the uncertainty in the deficit is bounded by

\[
E_D=E_T+\frac{\nu}{4}E_Y.
\]

A sign is accepted only when its certified interval excludes zero.

A `sign_unverified` or `fail_cancellation` result must never be accepted as a crossing.

Exact-rational arithmetic on stored coefficients certifies those represented coefficients only, not the continuous Navier–Stokes trajectory.

No such certified bounds \(E_T\) and \(E_Y\) are in hand. Large-field certification stays blocked.

## 9. Episode acceptance criteria

A dangerous episode begins when \(D\) crosses upward through zero and ends when \(D\) subsequently crosses downward through zero.

The primary numerical milestone is a downward crossing that survives:

- Cutoff comparison
- Timestep refinement
- Domain-size comparison
- Independent diagnostic verification
- Numerical uncertainty assessment

An initially positive prefix with no downward crossing is not a completed episode.

Regeneration requires a later upward crossing on the same trajectory, together with high-shell mass refill. It is not part of the initial acceptance criterion.

## 10. Periodic approximation and domain convergence

The sampled, projected periodic Gaussian is not identical to the original \(\mathbb R^3\) initial field.

Before interpreting periodic computations as evidence about the original Gaussian, document:

- Periodization and initialization procedure
- Physical box size and its doubling
- Spectral resolution and matching physical cutoffs
- Initial-data approximation errors
- Domain convergence of relevant diagnostics
- Boundary-periodicity and truncation effects

A periodic numerical episode does not by itself establish an episode for the \(\mathbb R^3\) problem.

## 11. Required reproducibility record

Each run must record the source-code commit and SHA-256 hashes, dependencies, FFT normalization, mask geometry, grid size, physical box length, timestep, solver tolerances, diagnostic definitions, checkpoint times, and resource usage.

Failed, incomplete, resource-blocked, and numerically unverified runs must remain in the record.

No unsuccessful run may be discarded merely because it does not exhibit the desired crossing.

## 12. DA approval gates

These rows are preregistration gates. They are not research Gates A–D.

| Gate | Requirement | Current status |
| --- | --- | --- |
| A | Guarded logger and unchanged RK4 stepper | Local PASS; DA approval pending |
| B | Signed-transfer and mask conventions | Local PASS at tested sizes |
| C | Physical-cutoff preregistration | PROPOSED |
| D | Large-field numerical-error certification | BLOCKED |
| E | Resource feasibility and enforcement | PARTIAL |
| F | \(\mathbb R^3\) comparison protocol | BLOCKED |
| G | Frozen production authorization | NOT APPROVED |

DA must return an explicit PASS, FAIL, or BLOCKED verdict for every gate, with evidence and unresolved requirements.

## 13. Claims boundary

This preregistration is a prospective experimental protocol. It is not a proof of turnover, regeneration, resource-budget summability, cutoff-independent control, or Navier–Stokes global regularity.

No production result is claimed.

## STATUS

PREREGISTRATION v1.2: PROPOSED. NOT APPROVED.
\(L\), BASELINE \(\Delta s\), \(K_{\mathrm{hp}}\), PERIODIZATION, CHECKPOINTS, TOLERANCES: NOT FIXED.
MATCHED PAIRS PROPOSED: \((L,128)\leftrightarrow(2L,256)\), \((L,160)\leftrightarrow(2L,320)\).
\((2L,128)\) AND \((2L,160)\): RETAINED AND REPORTED SEPARATELY.
MATCHED GRIDS: RESOURCE-BLOCKED.
SEPTEMBER MARKDOWN PAGES: NOT IN THIS CHECKOUT. LEMMA 19 NOT CERTIFIED.
LOCKED STEPPER: UNCHANGED.
FROZEN \(c=200\), \(s\ge 4\): NOT LAUNCHED.
PREREGISTRATION GATES A–B: LOCAL PASS, DA PENDING. C: PROPOSED. D, F: BLOCKED. E: PARTIAL. G: NOT APPROVED.
RESEARCH GATE D: OPEN / BLOCKED.
NO TURNOVER, REGENERATION, SHARED BUDGET, OR REGULARITY.
NS NOT SOLVED.
