# Solver core and S measurement

**Private. On hold.** Measured evidence only. Not a regularity proof.
Classical unaugmented 3-D Navier–Stokes stays **open**. The solver says
nothing about whether smooth solutions stay smooth.

Gate: filed. Core: approved with the three small edits below.
S measurement: the first run is superseded by the unique-count re-run.

---

## Honesty lock

- Do not read a small residual, a zero S, or a Taylor–Green peak as a close.
- Do not glue this to Lemma★, SND, Φ-renorm, SAG, or Clay Statement B.
- Per-field β tables from the first (6×) run stay **inconclusive**.
- Loop-defect: lower-bound trend only. A guaranteed upper bound is
  required before calling anything a defect.

---

## Three solver edits (S1–S3)

The approved Fourier–Galerkin core is `scripts/ns_solver_core.py`.

| Id | Edit |
|---|---|
| **S1** | Instantaneous power balance `⟨u, u_t⟩ + ⟨u, visc⟩ + ⟨u, Q1⟩ = 0` replaces the integrated trapezoidal residual. That residual printed **3–5e-4** on the Q1 Taylor–Green run and was not a conservation defect. |
| **S2** | Diagnostics are taken on the accepted, re-projected state, not the RK predictor field. |
| **S3** | Dissipation is the actual inner product `⟨u, rhs_term⟩`, not the analytic `‖∇u‖_{β+2}^{β+2}` proxy that produced the 3–5e-4 number under dealiasing. |

The retired integrated residual is still recorded as
`retired_integrated_residual` so the old 3–5e-4 figure can be compared
and discarded. On the Q1 Taylor–Green box (`n=16`, `ε=0.2`, `t=0.4`):

| Check | Value |
|---|---|
| Instantaneous inner-product residual (live) | `7.1e-15` |
| Relative residual | `3.2e-16` |
| Retired integrated residual (the misleading number) | `2.71e-4` |

---

## Three measurement edits (M1–M3)

`scripts/s_measurement.py`

| Id | Edit |
|---|---|
| **M1** | Each unordered triangle `{k,p,q}` with `k+p+q=0` is counted **once**. The kernel `Φ` is the same for all 6 labelings (locked to ~13 decimals). The first pass added `Φ` once per labeling, so it counted every triangle 6 times. Coherence is a ratio and was unaffected. S compares transfer to a viscous amount that was **not** multiplied by 6, so S was inflated. |
| **M2** | A thresholded `S=0` always prints transfer, viscous, coherence, and `|T|/visc`. A zero is not a reason to hide the numbers. |
| **M3** | Peak tables are re-run with the unique count. First-run per-field β results stay inconclusive until that re-run is read from `results/s_measurement_peak_tables.json`. |

With the count corrected, the transfer at the Taylor–Green peak is
smaller by 6 against an unchanged viscous amount. The result that S
comes out zero there gets **stronger**, not weaker.

Live machine, unique count, `n=16`, `ν=0.02` (do not splice a
different viscous convention onto these):

| Quantity | Unique count | 6× overcount |
|---|---|---|
| Peak time | `t=4.5` | same snapshot |
| `\|transfer\|` | **2.764** | 16.581 |
| Viscous `ν‖∇u‖²` | **3.357** | 3.357 (not ×6) |
| Coherence | 0.00329 | 0.00329 |
| S | **0** | would have been `16.58/3.36 > 1` |
| Count ratio | 1 | 6.000000000000195 |

Numbers behind that zero: `|T|/visc = 0.823`. Desk figure “≈2.8 against
≈19.4” used a different viscous convention; the unique transfer matches
≈2.8. Under this solver’s own viscous amount, the 6× bug would have
printed a false `S>0`. The unique count keeps `S=0`.

First-run per-field β tables stay **inconclusive**. The unique-count
re-run wrote 160 shell buckets at the peak into the JSON; they are
evidence, not a close.

---

## Loop-defect

Heavy finished the loop-family run. It shows a trend on **lower bounds
only**. That is inconclusive. A guaranteed upper bound is required
before calling anything a defect. This branch does not stamp a defect.

---

## Machine

```bash
python3 -m unittest tests.test_ns_solver_core tests.test_s_measurement
PYTHONPATH=scripts python3 scripts/ns_solver_core.py
PYTHONPATH=scripts python3 scripts/s_measurement.py --n 16 --t 5 --dt 0.1
```

`ns_solved` is false in every payload.
