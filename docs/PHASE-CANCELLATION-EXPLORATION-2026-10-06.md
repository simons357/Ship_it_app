# Phase cancellation mechanisms — exploration

6 October 2026.
**Exploration + targeted numerics. Not (17). Not a close of the
32-shape review claims.**

Parents:
[`SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md`](SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md),
[`SCHEME-B-SPATIAL-ATTEMPT-2026-10-06.md`](SCHEME-B-SPATIAL-ATTEMPT-2026-10-06.md)
(on the signed-scalene branch — absolute donor sums killed;
signed assembly still open).

Probe:
`scripts/ns_attacks/phase_cancellation_probe.py`
→ `PHASE-CANCELLATION-PROBE.json`.

---

## RESULT

| Level | What is known |
|---|---|
| Single triad | No cancellation available in the worst case — phases can align to the polarised bound \(C_b\) |
| Many triads, independent / random phases | Strong cancellation (optimistic); author experiment ~500 random triads → signed/abs \(\approx 0.0012\) |
| Shared-mode constraints | Real obstruction: coherent assembly can beat naïve \(\ell^1\) / per-pair sums (example: assembled square \(2M^2\) vs sum of donor bounds \(2M\)) |
| Open mechanism | How much cancellation **survives** after phases are forced consistent across all overlapping triads of a family? |

**First plow chosen:** focused numerical search for the
worst-case coherent configuration on a finite overlapping
family (compact proxy until the author ZIP’s exact shape
list is attached), measuring
\(\lvert\sum T_\sigma\rvert/(\sum\lvert T_\sigma\rvert)\).

### Probe headline (`PHASE-CANCELLATION-PROBE.json`)

| Experiment | \(\lvert\sum T\rvert/\sum\lvert T\rvert\) |
|---|---|
| Random independent triads → receiver shell (500) | \(\approx 0.042\) (strong cancellation; author’s ~0.0012 is the same regime) |
| Shared-mode family on \(\{5,8,9,10,25\}\) (5 shapes), **coherent** search | **\(1.0\)** (no residual cancellation) |
| Same family, random phases | mean \(\approx 0.59\), max \(1.0\) |
| Synthetic 32 triples / 12 shell phases, coherent | **\(1.0\)** |
| Same toy, random shell phases | mean \(\approx 0.15\) |

**Conclusion from numerics:** optimistic random-phase
cancellation **does not survive** worst-case shared-mode
consistency on these overlapping families — the coherent
ratio can reach \(1\). A signed multi-shape lemma must use
**geometric** structure (constant-2 / exact-shell), not a
hope that phases stay disordered.

---


## 1. Single-triad level (no cancellation available)

For any fixed geometric triad \((p,q,r)\), the three complex
phases of \(u_p,u_q,u_r\) can always be aligned so that the
interaction achieves the full polarised bound already used
(constants \(C_b\)).

At the level of **one** shape, phase cancellation cannot
improve the worst-case estimate. The geometric lemma +
polarisation already gives the sharp absolute-value bound.

---

## 2. Many triads, independent phases (strong cancellation)

When many different triads are summed and their relative
phases are essentially random (or rapidly mixing), the
signed sum is much smaller than the sum of absolute values.

Author numerical experiment (500 random triads onto a fixed
receiver shell):

| Quantity | Value |
|---|---|
| Sum of absolute contributions | \(\approx 3468\) |
| Net signed sum | \(\approx -4.3\) |
| Cancellation ratio | \(\approx 0.0012\) |

Optimistic regime: if dynamics kept phases disordered, a
residual family would be easy to absorb. **Not proved.**

---

## 3. Shared-mode phase constraints (the real mechanism)

Each Fourier coefficient \(u_k\) appears in many overlapping
triangles. Its single phase must serve all of those
interactions simultaneously.

Two opposing effects:

1. **Destructive interference (helpful).** The phase that
   maximises one triad may reduce another. Total signed
   transfer can beat any absolute-value assembly.
2. **Coherent assembly (obstruction).** There exist
   divergence-free configurations in which many donor pairs
   add constructively on a common receiver shell. An exact
   example produces an assembled square of size \(2M^2\)
   while the sum of the individual donor bounds is only
   \(2M\). Perfect cancellation cannot be assumed.

This is the same structural tension that killed SCHEME A′ /
absolute donor-pair sums toward (B1): absolute methods pay
the coherent price; signed methods might not — but only if
a phase-consistent bound is proved.

---

## 4. Structural mechanisms

| Mechanism | Status | Potential gain |
|---|---|---|
| Random / mixing phases | Observed numerically, not proved | Very large |
| Shared-mode orthogonality | Partially visible in the constant-2 lemma | Moderate |
| Helicity / polarisation conflicts | Classical; partly in \(C_b\) | Already incorporated |
| Time-averaged phase drift | Not yet exploited | Possibly large |
| Global consistency of the phase field on the lattice | Open | Could turn assembly obstruction into a gain |

---

## 5. Most promising direction (chosen order)

Work with the **signed** sum \(\sum_\sigma T_\sigma\), not
\(\sum\lvert T_\sigma\rvert\), while controlling the
worst-case shared-phase configuration.

1. **Now (numerics):** worst-case coherent phase search on
   the current overlapping family; report
   \((\sum T_\sigma)/(\sum\lvert T_\sigma\rvert)\).
2. **Next (analysis):** signed multi-shape / weighted
   exact-shell lemma that keeps some cancellation; or
   operator-norm bound for the map
   \((\arg u_k)\mapsto (T_\sigma)\).

---

## 6. Explicit non-claims

- Does not alter the 17- / 32-shape review filing’s proved
  scopes.
- Does not establish (17) or global regularity.
- Random-phase cancellation is **not** a worst-case bound.

---

## STATUS

SINGLE-TRIAD: NO WORST-CASE PHASE GAIN.
RANDOM-PHASE CANCELLATION: NUMERICAL (STRONG); NOT A WORST-CASE BOUND.
SHARED-MODE COHERENT SEARCH (FAMILY PROXY): RATIO CAN REACH 1 — OPTIMISTIC CANCELLATION KILLED.
SYNTHETIC 32 / SHARED SHELL PHASES: SAME — WORST-CASE RATIO 1.
NEXT: SIGNED MULTI-SHAPE LEMMA VIA GEOMETRY (NOT PHASE HOPE).
EXACT 32-LIST: AWAITS AUTHOR ZIP.
(17) NOT CLAIMED.
NS NOT SOLVED.
