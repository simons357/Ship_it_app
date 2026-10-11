# Operation Excalibur — architecture and adversarial research plan

**Date:** 2026-10-10.
**Filed:** 2026-10-11.
**Status:** Proposed design. Not deployed.
**Repository:** https://github.com/simons357/Ship_it_app

This file records the plan as received. It does not deploy the module layout, and it does not approve a mathematical result.

## Grounding

The default GitHub branch was inspected: root includes scripts, docs, tests, data, results, and domain_architect. The expected `scripts/ns_attacks` path was not found on that default branch. PR and feature branches and uploaded archives must be inventoried before selecting canonical source files.

Deliverable A of that inventory is [`EXCALIBUR-INVENTORY-A-2026-10-11.md`](EXCALIBUR-INVENTORY-A-2026-10-11.md). The locked stepper is present on `cursor/shared-budget-32-shape-c3ed` and absent from `main`.

## Invariants

- Classical unforced incompressible 3D Navier–Stokes only in the conventional NSE lane.
- No source mutation in place. Preserve historical hashes and raw results.
- One canonical core evolution engine, with diagnostics strictly downstream.
- Each result links the exact code commit, input, environment, grid, timestep, and validation.
- Finite Galerkin evidence is not a cutoff-independent theorem.
- No bot can self-approve its own mathematical result.

## Proposed module layout (new branch only)

```
ns_core/            # velocity state, Fourier masks, projection, RHS, time integration
ns_diagnostics/     # energy/enstrophy, signed scalene transfer, strain, spectral budgets
ns_validation/      # exact rational small-state oracle, independent reference, convergence
ns_visualization/   # volume, physical slices, spectral shells, synchronized time viewer
research_graph/     # claim IDs, source dependency DAG, assumptions, counterexamples
agents/             # Nazgul task definitions, read-only worker harness, judge
benchmarks/         # fair reference solver comparisons, profiles, reproducible reports
archive/            # immutable originals, historical scripts and rejected claims
```

These directories were not created by this filing.

## Agent tasks

- **Rootbreaker:** locate source lemmas and attack quantifiers, circularity, and missing hypotheses.
- **Triad Hunter:** signed and unsigned transfer, all-radii multiplicity, phase, and geometry.
- **Cascade Hunter:** dynamical turnover, regeneration, once-per-shell budget, and recurrence.
- **Geometry Hunter:** vorticity alignment and stretching, C10, and alternate criteria.
- **Numerical Assassin:** wrong-sign cancellation, FFT aliasing, projection, convergence, and memory.
- **Judge:** reproduce independently, and rule SURVIVES, BROKEN, CONDITIONAL, or UNRESOLVED.

## Research dependency graph

Claim nodes carry an id, the exact statement, the source commit and file, the status, the dependencies, a witness or proof, and the last independent reviewer. A directed edge means "requires". Mark a downstream claim blocked when a required upstream claim fails. Do not automatically infer that the downstream statement is false. Generate branch-survival and counterexample maps from this graph.

## Alternative routes to investigate

These routes are not asserted as proved.

1. Vorticity-direction coherence and geometric depletion of stretching.
2. Scale-localized strain depletion with an integrable remainder (C10).
3. Signed nonlinear flux budget from dynamic phase decorrelation, rather than static universal cancellation.
4. Time-frequency occupation and turnover or recurrence estimates.
5. Localized regularity criteria translated into checkable sufficient conditions.
6. Exact spectral triad conservation identities and coercive shared-resource candidates.

## Observatory layers

Physical x, y, and z slices, a movable oblique plane, vorticity magnitude, stretching \(\omega\cdot S\omega\), strain eigenvalues, velocity arrows and streamlines, pressure, enstrophy density, local alignment cosines, and a temporal difference. Spectral mode view: radial shells, scalene triad links, signed flux, and high-shell occupancy. Display synchronized physical and spectral views, with a time slider and a single reproducible field id. Never treat image appearance as blowup evidence.

## First deliverables

| Id | Job | Status of this filing |
| --- | --- | --- |
| A | Inventory branches and archives, map runtime imports, freeze the core hash | Filed in the inventory note |
| B | Independent baseline against spectralDNS on identical periodic initial data | Not started |
| C | Proof dependency graph and root failures before expensive descendant tests | Not started |
| D | Three-layer volume viewer: vorticity, stretching, signed transfer, linked slices | Not started |
| E | Prioritized surviving-branches ledger with citations to exact source files | Not started |

## Constraints

No cloud spending, no merge, no deletion, and no production Gate D launch without explicit approval. A numerical blowup or no-blowup badge is only a diagnostic unless it is mathematically justified.

## STATUS

PROPOSED. NOT DEPLOYED.
MODULE TREE: NOT CREATED.
DELIVERABLE A: FILED.
DELIVERABLES B–E: NOT STARTED.
PRODUCTION GATE D: NOT LAUNCHED.
NO TURNOVER, REGENERATION, SHARED BUDGET, OR REGULARITY.
NS NOT SOLVED.
