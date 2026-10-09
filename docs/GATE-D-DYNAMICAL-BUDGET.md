# Gate D — dynamical budget measurements

9 October 2026.
**Accelerated Fourier solver in service. Cutoff-independent budget OPEN.
Not (17). NS not solved.**

Parent: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).
Approved S1–S3 core (explicit RK4, instantaneous power balance):
`scripts/ns_solver_core.py`.
Gate D stepper: `scripts/gate_d_fourier_budget.py`.

---

## Why Gate D now

Gate B rules out getting below \(\theta=\tfrac12\) by regrouping the
specified nonnegative \(Q_x\). Signed cancellation, on the sample that
exists, is a constant factor, not a dropped power. The remaining
analytic deficit is still half a derivative on that majorant.

That is a static estimate. The Millennium obstruction for classical
unforced 3-D Navier–Stokes is dynamical: whether a smooth solution can
regenerate high-frequency enstrophy often enough, and at high enough
amplitude, to outrun viscosity on a time that stays finite as the
cutoff \(\to\infty\).

Gate D asks for a **cutoff-independent dynamical budget**: a bound on
the time-integral of dangerous transfer that does not deteriorate when
the Fourier truncation is removed. This page does **not** supply that
bound.

---

## Instrument

Classical unforced Navier–Stokes on \(\mathbb T^3=[0,2\pi]^3\),
divergence-free, no Q1 track (\(\varepsilon=0\)).

The S1–S3 core keeps viscosity explicit. Gate D uses
**integrating-factor RK4**: the Stokes factor \(e^{-\nu\lvert k\rvert^2 t}\)
is applied exactly in Fourier space; RK4 is spent on
\(-P(u\cdot\nabla u)\). 2/3 dealiasing and Leray projection stay.

This is an acceleration of the same equation, not a new model.

Measured, not proved:

| Observable | Meaning |
|---|---|
| Regeneration | high-shell energy has a trough then a later peak |
| Turnover | steps between successive high-shell peaks |
| Danger episode | a run of times with \(\lvert\mathrm{transfer}\rvert > \mathrm{viscous}\) |

Two grids are compared only as a diagnostic. Equal episode counts on
\(n=8\) and \(n=12\) are **not** a cutoff-independent budget.

First smoke (Taylor–Green, same continuum field, \(\nu=0.05\),
\(t=0.16\)): energy \(31.006\to 29.552\) on both \(n=8\) and \(n=12\)
(relative end-energy gap \(<10^{-7}\)). Regeneration 0, danger
episodes 0. That is viscous decay of a closed eddy, not a budget.

---

## Honesty lock

- Unforced Taylor–Green decays; broadband ICs still decay in energy
  on these short runs. Decay is not regularity.
- A danger episode on a tiny torus is not a blowup.
- Do not glue this to Lemma★, SND, Φ-renorm, SAG, or Clay Statement B.
- `ns_solved` is false in every payload.
- `cutoff_independent_budget` is false in every payload.

```bash
python3 -m unittest tests.test_ns_solver_core tests.test_gate_d_fourier_budget -v
PYTHONPATH=scripts python3 scripts/ns_solver_core.py --eps 0.0
PYTHONPATH=scripts python3 scripts/gate_d_fourier_budget.py --n 8 12 --t 0.2 --dt 0.02
```

---

## Next measurements (not this page)

- Longer time, smaller \(\nu\), recorded high-shell regeneration.
- Resolution study at **fixed** initial datum, several \(n\).
- A stated criterion for what would count as a cutoff-independent
  budget (time-integral of positive transfer / viscous, uniform in \(n\)).
- Do not declare Gate D closed from one Taylor–Green or one seed.

---

## Lock

Gate D: **measurement active**.
Cutoff-independent dynamical budget: **OPEN**.
Classical unforced 3-D Navier–Stokes: **OPEN**.
(17) OPEN. NS not solved.
