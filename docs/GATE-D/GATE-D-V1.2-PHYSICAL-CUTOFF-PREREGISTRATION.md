# Gate D v1.2 — physical-cutoff preregistration

9 October 2026.
**This is a new preregistration, not an amendment of v1.1.
Not approved until DA returns a decision on this file.
Not (17). NS not solved. Gate D remains OPEN.**

Identical copies (so the file is findable where it was missing):

- `docs/GATE-D/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md`
- `packets/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md`
- `packets/gate_d/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md`

Machine-readable freeze: `docs/GATE-D/GATE-D-V1.2-FREEZE.json`
(copy: `packets/gate_d/GATE-D-V1.2-FREEZE.json`).

Dated pointer: `docs/GATE-D-V1.2-PREREGISTRATION-2026-10-09.md`.

---

## 0. What this file is

v1.1 is live, with counted runs in progress. This document is the attached
v1.2 draft that was not previously on disk in the Gate D folders or the
packets. It exists so the cutoff convention can be approved or rejected,
and so conflicts can be listed against a specific text.

v1.2 does **not** re-score, reuse, continue, or amend any v1.1 run.
Design choices below use only resolution geometry, the logger rule
\(N<n/3\), the existing 2 GiB preflight, and the published \(N^3\) memory
scaling from Heavy’s one measurement of about 7 GB at grid \(n=192\).
They do **not** use v1.1 outcomes, including the tail-gate failure near
\(s\approx 0.75\).

Production readiness stays **BLOCKED** on (i) DA approval of this file
and (ii) a measured peak-RSS memory benchmark at every grid v1.2
proposes, done before the freeze.

---

## 1. Physical-cutoff convention (the decision item)

### 1.1 Frozen statement

On a periodic box of side \(L\), the **physical cutoff** is the
wavenumber

\[
\kappa_\star \;=\; 8
\]

in the same units as the Fourier frequencies \(2\pi m/L\), \(m\in\mathbb Z^3\).
The matching integer Galerkin radius is

\[
N(L) \;=\; \frac{\kappa_\star L}{2\pi}.
\]

The matching integer high-pass for signed-scalene / episode diagnostics is

\[
K(L) \;=\; \frac{\kappa_\star L}{4\pi} \;=\; \tfrac12 N(L).
\]

| Box | Integer Galerkin \(N\) | Integer high-pass \(K\) | Physical \(\kappa_\star\) | Physical high-pass |
|---|---:|---:|---:|---:|
| \(L=2\pi\) | 8 | 4 | 8 | 4 |
| \(L=4\pi\) | 16 | 8 | 8 | 4 |

These four integers are **fixed**, independent of the grid \(n\), and are
chosen in this file **before any v1.2 outcome is read**.

The evolution mask is the spherical ball \(\lvert m\rvert\le N(L)\)
intersected with the \(2/3\) cube \(\lvert m_i\rvert<n/3\). The logger
rule \(N<n/3\) is mandatory. A relative shell
`high_fraction * k_max(n)` is **not** a v1.2 cutoff.

### 1.2 Why this \(\kappa_\star\), and why it is not data-dependent

\(\kappa_\star=8\) is taken from resolution geometry only:

1. It is a fixed physical wavenumber, not a fraction of \(n\).
2. Both matched boxes sit strictly inside the \(2/3\) cube of every
   proposed grid: \(N(2\pi)=8<64/3\approx 21.33\) and \(<96/3=32\);
   \(N(4\pi)=16<21.33\) and \(<32\).
3. Each proposed grid therefore has a nonempty spectral tail
   \(\lvert k\rvert>\kappa_\star\) on which the tail bound is measured.
4. The pair \((L,N)=(2\pi,8)\leftrightarrow(4\pi,16)\) is a
   matched-resolution domain comparison at the **same** \(\kappa_\star\).

It is **not** taken from the v1.1 tail-gate failure near \(s\approx 0.75\).
It is **not** the 9 October recommendation
\((L,128)\leftrightarrow(2L,256)\) and \((L,160)\leftrightarrow(2L,320)\)
in `GATE-D-CUTOFF-CONVENTION-2026-10-09.md` on
`cursor/shared-budget-32-shape-c3ed`. That recommendation is a different
document. It is not this preregistration, and v1.2 does **not** adopt it
(see §4 and §5).

### 1.3 What “below the cutoff” means

A mode \(m\) is **below the cutoff** when its physical frequency satisfies
\(\lvert k\rvert=2\pi\lvert m\rvert/L\le\kappa_\star\), equivalently
\(\lvert m\rvert\le N(L)\).

A mode is **on the tail** when \(\lvert k\rvert>\kappa_\star\) and the
mode is still retained by the grid’s \(2/3\) cube.

**Full grid** means every retained mode of that run’s spherical-plus-cube
mask, including the tail.

---

## 2. Feasibility under 2 GiB

### 2.1 The limit (explicit)

v1.2 adopts a hard ceiling of

\[
2\,\mathrm{GiB} \;=\; 2\times 1024^3 \;=\; 2\,147\,483\,648\text{ bytes}
\]

of **measured peak RSS** at every grid it uses. This is the same ceiling
already coded as `fail_closed.preflight` (`limit_bytes=2*1024**3`).
The preflight estimate \(576 n^3\) is **not** a peak-RSS certificate.

v1.1 assumed about 7 GB (Heavy’s one measurement at \(n=192\)).
v1.2 does not inherit that assumption.

### 2.2 Scaled estimate (not a benchmark)

Scaled as \(n^3\) from Heavy’s ~7 GB at \(n=192\):

| Grid \(n\) | Scaled estimate | v1.2 status |
|---:|---:|---|
| 64 | ~0.26 GB | allowed, pending measured RSS |
| 96 | ~0.9 GB | allowed, pending measured RSS |
| 128 | ~2.1 GB | **excluded** (marginal; overhead likely exceeds 2 GiB) |
| 160 | ~4 GB | **excluded** |
| 192 | ~7 GB | **excluded** |

Under 2 GiB only \(n=96\) is clearly feasible among the historical
production sizes. That rules out v1.1’s standard base at 128 and the
whole escalated set at 160 and 192. A later preregistration may add
\(n=128\) only after a measured peak-RSS benchmark showing it fits.
That promotion is **not** part of v1.2.

### 2.3 Proposed grids

Production / certification grids for v1.2:

\[
n\in\{64,96\}.
\]

Both must pass a measured peak-RSS benchmark **before the freeze**.
Any \(n\) that fails is dropped from v1.2 and is never used as evidence.
If \(n=64\) fails, v1.2 cannot certify two-grid convergence and stays
blocked. If \(n=96\) fails, v1.2 is infeasible and is not run.

The 9 October matched pairs at integer cutoffs 128 and 160 require
\(n>384\) and \(n>480\) under \(N<n/3\). Those grids are infeasible
under 2 GiB (preflight ~31 GiB and ~60 GiB). They are not in v1.2.

---

## 3. Observables and gates — band label required

Every recorded observable and every gate states its band.

| ID | Observable / gate | Band | Notes |
|---|---|---|---|
| O1 | Energy \(E\), moments \(X\), \(Y\) | **full grid**, and also reported **below \(\kappa_\star\)** | Both numbers are stored. Scoring uses the below-cutoff pair unless the row says otherwise |
| O2 | Production \(T=\int\omega\cdot S(u)\,\omega\) | **full grid** | Not \(T_{\mathrm{sc}}\) |
| O3 | Probe \(G=T-Y/200\) | **full grid** | Diagnostic probe only. Not \(D\). Not a crossing |
| O4 | \(T_{\mathrm{sc}}(h_{K,N})\) | **below \(\kappa_\star\)**, high-pass \(K(L)\) | Distinct-radii scalene transfer on \(P_{\lvert k\rvert>K}u_N\) |
| O5 | \(D=T_{\mathrm{sc}}-\nu Y_N/4\), \(d=D/X_N\) | **below \(\kappa_\star\)** for \(T_{\mathrm{sc}}\); \(X_N,Y_N\) **full grid** as in the 9 Oct note | Sign of \(D\) on a frozen array does not certify the trajectory |
| O6 | Episode budget \(B_I=\int_I d\,dt\) | **below \(\kappa_\star\)** | Integral only. Do not add \((b-a)d(a)\) |
| O7 | Regeneration (high-pass energy trough then later peak) | **below \(\kappa_\star\)**, shell \(K(L)<\lvert m\rvert\le N(L)\) | Not a fraction of \(k_{\max}(n)\) |
| O8 | Turnover (steps between successive high-pass peaks) | **below \(\kappa_\star\)** | Same shell as O7 |
| O9 | Danger episode (\(\lvert\mathrm{transfer}\rvert>\mathrm{viscous}\) run) | **below \(\kappa_\star\)** | |
| O10 | Spectral-tail bound | **tail** \(\lvert k\rvert>\kappa_\star\) | Measured on the full grid’s tail, reported against \(\kappa_\star\) |
| O11 | Energy-identity residual | **full grid** | See §4 |
| O12 | Enstrophy-identity residual | **full grid** | See §4 |
| O13 | Galerkin closure | **full grid** | Energy outside \(N(L)\) must remain numerical zero |
| O14 | Initial-datum check | **full grid** and **below \(\kappa_\star\)** | Against the stamps in §6 |
| O15 | Memory benchmark | **full grid** | Peak RSS, before freeze |
| O16 | \(\max\) Fourier divergence | **full grid** | |
| G-cert | Two-grid / two-step / two-domain convergence | **below \(\kappa_\star\)** for dynamical scores; **full grid** for identities | Tolerances in §4, fixed now |
| G-tail | Tail gate | **tail** | Fail ⇒ run excluded, never evidence |
| G-mem | 2 GiB RSS gate | **full grid** | Fail ⇒ run excluded |

A row that omits its band is malformed and is excluded.

---

## 4. Numerical-error certification (required before any score)

Tolerances below are **fixed in this file**, before any v1.2 outcome
is read. A run that fails any check is **excluded**, never evidence.

### 4.1 Convergence (two grids, two timesteps, two domains)

Required matrix, all combinations that the memory gate accepts:

| Axis | Values |
|---|---|
| Grid | \(n=64\), \(n=96\) |
| Timestep | \(\Delta s=10^{-2}\), \(\Delta s=5\times 10^{-3}\) |
| Domain | \(L=2\pi\), \(L=4\pi\) |

At the common physical cutoff \(\kappa_\star=8\), below-cutoff observables
O1 (below-cutoff copy), O4–O9 must satisfy

\[
\frac{\lvert A(n,\Delta s,L)-A(n',\Delta s',L')\rvert}
{\max\bigl(\lvert A\rvert,1\bigr)}
\le
\begin{cases}
10^{-8} & \text{at }s=0,\\
10^{-3} & \text{at every logged }s>0\text{ that both runs reach}.
\end{cases}
\]

Identity observables O11–O13, O16 use the absolute tolerances in §4.2
on **each** run, not a pairwise difference.

If a pair cannot be formed because one run was excluded, the missing
pair is a failed certification, not a waived one.

### 4.2 Spectral tail, identities, closure, divergence

Fixed in advance:

| Check | Tolerance | Band |
|---|---|---|
| Tail energy ratio \(E(\lvert k\rvert>\kappa_\star)/E(\lvert k\rvert\le\kappa_\star)\) | \(\le 10^{-3}\) at every logged \(s\) | tail vs below-cutoff |
| Energy identity \(\lvert \dot E+2\nu Y-2T\rvert/\max(E,1)\) | \(\le 10^{-6}\) | full grid |
| Enstrophy identity residual, same normalization | \(\le 10^{-6}\) | full grid |
| Galerkin closure \(E(\lvert m\rvert>N(L))/E\) | \(\le 10^{-12}\) | full grid |
| \(\max\) Fourier divergence | \(\le 10^{-10}\) | full grid |
| Cancellation report | `rigorous_error_bound` stays **false** until a bound exists; `fail_cancellation` excludes the run | as logged |

The existing `cancellation_report` heuristic is **not** a bound.

### 4.3 Viscosity and rational arithmetic

\[
c=200,\qquad \nu=\frac1{200}.
\]

Viscosity is `Fraction(1, 200)`, never `Fraction(float(1/200))`.
A \(D\) sign is certified only from that rational, and only on
\(L=2\pi\). At \(L=4\pi\), \(D\) sign is stored as
`physical_box_sign_unverified` and cannot establish a crossing.
A sign of \(D\) on a frozen coefficient array does not certify the
trajectory that produced the array.

### 4.4 Memory benchmark, before freeze

For each \(n\in\{64,96\}\), before the freeze and before any scored
trajectory:

1. Run the production mask and one integrating-factor RK4 step plus
   one full diagnostic evaluation.
2. Record measured peak RSS.
3. Fail if peak RSS \(>2\) GiB or if `preflight` raises.

The Heavy \(N^3\) table in §2.2 is an estimate, not this benchmark.

---

## 5. Known conflicts with v1.1 (hold regardless of approval)

v1.1 remains live. These conflicts are stated here so they do not
depend on later wording.

1. **New preregistration, not an amendment.** v1.2 does not edit v1.1’s
   counted-run ledger, gates, or scores.
2. **No reuse.** No v1.1 run, partial, smoke, or continuation may be
   re-scored or imported as v1.2 evidence.
3. **No outcome peeking.** The tail-gate failure near \(s\approx 0.75\)
   is a v1.1 outcome. \(\kappa_\star\) was not chosen from it and must
   not be moved toward it after this file is filed.
4. **Memory model.** v1.1 assumed about 7 GB. v1.2 states a 2 GiB
   peak-RSS ceiling. That alone already excludes v1.1’s standard base
   at 128 and the escalated set at 160 and 192.
5. **Cutoff type.** v1.1 may use a grid-relative tail
   (`high_fraction * k_max(n)`, default `0.5` on the replacement
   scaffold). v1.2 forbids that. High-pass shells are \(K(L)\), fixed
   in physical units.
6. **Resolution target.** The recommended 9 October pairs
   \((L,128)\leftrightarrow(2L,256)\) and \((L,160)\leftrightarrow(2L,320)\)
   are **not** v1.2. They are resource-blocked under 2 GiB and under
   \(N<n/3\). v1.2 is a smaller, matched-resolution program at
   \(\kappa_\star=8\). It does not claim to be the same experiment as
   those integer-128/160 labels.
7. **Horizon.** The frozen \(c=200\), \(s\ge 4\) campaign, if still
   attached to v1.1, is not launched as a v1.2 run. v1.2’s planned
   horizon is recorded in §7 as a completion target, not as a reuse of
   that campaign’s paths or scores.
8. **Six-box / \(4H\) FFT path.** Orszag \(n\ge 768\) at cutoff \(4H\)
   is host-blocked on a 2 GiB machine. It is not in v1.2.

---

## 6. Initial datum and already-stamped constants

### 6.1 Field

Analytic vector potential, then curl, then periodization:

\[
A=e^{-r^2/2}(xy,\,xz,\,x+yz),
\qquad
u_0=\nabla\times A
\]

sampled on \([-L/2,L/2)^3\), Leray-projected, then restricted to the
v1.2 mask of §1. After sampling, projection, and the mask, the field
is **not** the \(\mathbb R^3\) Gaussian. Domain comparison is the
\(L\leftrightarrow 2L\) pair at fixed \(\kappa_\star\), not an
\(\mathbb R^3\) certificate (item 7 of the 9 October logger review
stays blocked).

### 6.2 Scaffold regression stamps (already on disk; not production)

Replacement-scaffold smoke, \(n=12\), \(L=12\), \(c=200\), \(s=0\),
componentwise \(2/3\) mask, source SHA-256
`a591e95657eadbe9f1027939ec08f696e5fbba3de67d2cdf1f15060123c15534`:

| Quantity | Stamped value |
|---|---|
| Energy | \(5.1207283333063645\) |
| \(X\) | \(32.611124080320636\) |
| \(Y\) | \(120.67914364422008\) |
| Production | \(0.19602790351705981\) |
| \(\max\) Fourier divergence | \(\sim 10^{-18}\) |

These stamps check the scaffold only. They are **not** the v1.2
production constants (\(n\), \(L\), and the mask all differ).

### 6.3 Production stamps (to be written before freeze)

Before any v1.2 trajectory is scored, write exact (binary64, 17
significant digits) constants for \(E,X,Y,T\) at \(s=0\) on each
accepted \((n,L)\) into
[`GATE-D-V1.2-FREEZE.json`](GATE-D-V1.2-FREEZE.json) under
`production_stamps`. O14 fails a run if any relative error against
those stamps exceeds \(10^{-12}\).

`T_sc` and \(D\) remain undefined for implementation until the
20 September scalene-target pages are attached and independently
validated. v1.2 may record O1–O3, O10–O16, and the memory gate
without them. O4–O9 and any crossing stay **unscored** until that
definition is attached in a later preregistration. This file does
not reconstruct them.

Locked stepper SHA-256, unchanged by v1.2:
`0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`.

---

## 7. Planned horizon and scoring rules

- Viscosity parameter \(c=200\).
- Planned completion horizon \(s_{\mathrm{end}}=4\), timesteps as in §4.1.
- Reaching \(s=4\) is a completion flag, not evidence of regularity,
  turnover, or a cutoff-independent budget.
- `cutoff_independent_budget` is **false** on every v1.2 payload.
- `ns_solved` is **false** on every v1.2 payload.
- `sign_unverified` cannot establish a crossing. `fast_value` on a
  `sign_unverified` record is not a crossing and must not be stored.
- Failed certification ⇒ excluded. Excluded runs are listed, not scored.

---

## 8. Production readiness

| Item | Status |
|---|---|
| v1.2 file attached in Gate D folders and packets | **this file** |
| DA decision on the cutoff convention | **pending** |
| Memory benchmark at \(n=64\) and \(n=96\) | **not done** — second blocker |
| Two-grid / two-step / two-domain certification | **not done** |
| \(T_{\mathrm{sc}}\) / \(D\) from the 20 September original | **blocked** (definitions not on hand) |
| Frozen v1.1 \(s\ge 4\) campaign | **not reused** |
| Cutoff-independent dynamical budget | **OPEN** |
| (17) / Clay | **OPEN** |

**Verdict requested of DA, on this file:** approve, reject, or list
conflicts against §1 (cutoff), §2 (2 GiB / grids), §3 (band labels),
§4 (tolerances), and §5 (v1.1 conflicts).

---

## STATUS

V1.2: NEW PREREGISTRATION. NOT AN AMENDMENT OF V1.1.
CUTOFF: \(\kappa_\star=8\), INDEPENDENT OF \(n\), CHOSEN BEFORE OUTCOMES.
MATCHED BOXES: \((2\pi,N=8)\leftrightarrow(4\pi,N=16)\).
GRIDS: \(n=64,96\) ONLY. \(n=128,160,192\) EXCLUDED.
MEMORY CEILING: 2 GiB PEAK RSS. V1.1’S ~7 GB ASSUMPTION IS NOT USED.
NO V1.1 RUN IS REUSED OR RE-SCORED.
\(\kappa_\star\) IS NOT TAKEN FROM \(s\approx 0.75\).
CERTIFICATION TOLERANCES: FIXED IN §4. FAILURES ARE EXCLUSIONS.
PRODUCTION: BLOCKED ON DA APPROVAL AND THE MEMORY BENCHMARK.
GATE D: OPEN.
(17) NOT CLAIMED.
NS NOT SOLVED.
