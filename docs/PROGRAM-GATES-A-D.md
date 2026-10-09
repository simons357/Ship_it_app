# Program gates A–D

9 October 2026.
**Gate B lower bound for nonnegative Q_x: proved by dilation.
All-radii trilinear upper bound: gap. Gate D measurements started.
Not (17). NS not solved.**

---

## Board

| Result | Status |
|---|---|
| Finite-radius multiplicity checks | Verified. One-input two-shell occupancy can exceed 2 (circle, 4-point example) |
| All-radii geometric counting | Pass as Euclidean two-plane+sphere (G1). Does not bind generic triads |
| Distinct-shell hypothesis | Insufficient. Need linear independence of wavevectors |
| Full multiplicity / trilinear inequality | **Gap.** Counting does not yield the weighted \(\lVert Q\rVert_2\) bound (CS-3 fail) |
| Gate B lower bound (nonnegative \(Q_x\)) | **Proved** by similar-triad dilation: \(\theta\ge\tfrac12\). Not conditional on CS-3 |
| Optimal exponent | **Open** |
| Signed transfer control | **Open** |
| Gate D dynamical budget | Measurement campaign started. Cutoff-independent budget **open** |
| Gate A | UNRESOLVED / DIAGNOSTIC ONLY |
| Theorem (17) | Open |
| Classical unforced 3-D Navier–Stokes | Open |

---

## Gate order

| Gate | Mission | Status |
|---|---|---|
| **A** | Positive all-shape load vs viscous gain | UNRESOLVED / DIAGNOSTIC ONLY |
| **B** | Remaining frequency loss \(\theta\) after energy sharing | Lower bound \(\theta\ge\tfrac12\) on nonnegative \(Q_x\) **proved**. Upper bound / signed \(\theta\) **open** |
| **C** | Exact missing exponent after B | Queued; optimal \(\theta\) open |
| **D** | Cutoff-independent dynamical budget; regeneration, turnover, repeated danger | **Active measurement.** Not a theorem |

---

## Independent DA audit (this branch)

[`GATE-B-TRILINEAR-DA-AUDIT.md`](GATE-B-TRILINEAR-DA-AUDIT.md)
records every Cauchy–Schwarz. CS-1 is Dish #3 energy sharing. CS-2 is
the inner \(Y\)-charge that produces a different object. CS-3, the
leap from two-point counting to a trilinear norm bound, **fails**.

Geometry: [`GATE-B-ALL-RADII-LEMMA.md`](GATE-B-ALL-RADII-LEMMA.md).

```bash
python -m domain_architect --trilinear-ns
python3 scripts/ns_attacks/all_radii_counting.py
python3 scripts/ns_attacks/nonnegative_qx_dilation.py
python3 scripts/gate_d_fourier_budget.py --n 8 12 --t 0.2 --dt 0.02
```

---

## Gate D

Structural remaining deficit after B is still half a derivative on
the nonnegative majorant, and signed cancellation has not dropped the
power. The next major objective is unchanged: a cutoff-independent
dynamical budget for classical, unforced three-dimensional
Navier–Stokes.

The accelerated Fourier solver (integrating-factor RK4) is a
**measurement** instrument for regeneration, turnover, and repeated
dangerous episodes. Matching episode counts on two small grids is
not that budget.

Note: [`GATE-D-DYNAMICAL-BUDGET.md`](GATE-D-DYNAMICAL-BUDGET.md).

---

## STATUS

GATE A: UNRESOLVED / DIAGNOSTIC ONLY.
GATE B: nonnegative obstruction \(\theta\ge\tfrac12\) PROVED (dilation).
        all-radii trilinear upper bound NOT established.
        optimal \(\theta\) OPEN. signed transfer OPEN.
GATE C: QUEUED.
GATE D: MEASUREMENT ACTIVE. cutoff-independent budget OPEN.
(17) NOT CLAIMED.
NS NOT SOLVED.
