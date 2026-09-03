# Domain Architect — Functional Role Analysis

**Status:** scientific rectification, August 2026 — software plus historical registry  
**Product:** Domain Architect  
**Method:** Functional Role Analysis  
**Canonical SFE status:** unresolved  
**This folder is not a theory of everything, a canonical Simons Field Equation, or a proof of physical prime indexing.**

Approved plain-language explanation:

> Paste an equation. Domain Architect identifies what each component does, how the components connect, and which parameters can be tested or tuned.

| Document | Purpose |
|---|---|
| [00 — Audited baseline](00-AUDITED-BASELINE.md) | Frozen framework, terminology, evidence levels |
| [01 — Equation inventory](01-EQUATION-INVENTORY.md) | Historical UHF / SFE / DHFA / gravity / prime-index formulas found in this repo family |
| [02 — Conflict table](02-CONFLICT-TABLE.md) | Incompatible definitions, units, domains, and claims |
| [03 — Reconciliation](03-RECONCILIATION.md) | Six-point response to the August 2026 handoff |
| [04 — Notation collisions](04-NOTATION-COLLISIONS.md) | `P` / `p` / `ℙ`, `Φ` / `φ` / `ϕ`, and other overloaded symbols |
| [05 — Rectification](05-RECTIFICATION.md) | Software implementation of the August 2026 corrective specification |
| [06 — Computing bench](06-COMPUTING-BENCH.md) | Where we go from here: DA compiler, ChatVault search, Cosmo viz only |
| [07 — NS geometric analysis](07-NS-GEOMETRIC-ANALYSIS.md) | Tube, shells, strain, swirl — architecture, not a regularity proof |
| [08 — NS tube estimate](08-NS-TUBE-ESTIMATE.md) | Live Hardy / wall / \(I_{\mathrm{tube}}\) write; T3a in, T3b and T5 open |
| [09 — Stop at the wall](09-NS-GAP.md) | Hit a wall: stop, name the missing piece, list candidates after |
| [10 — Play with the shape](10-NS-SHAPE-PLAY.md) | Fill the other side if the shape forces it; cylinder play is extra \(E\) |
| [11 — Energy as a visual object](11-NS-ENERGY-PLAY.md) | Bernstein fills enstrophy from shell energy; outside does not fill the tube |
| [12 — Overlay](12-NS-OVERLAY.md) | Pieces visualized; done transposable layers stacked; refine one hole |
| [13 — See](13-NS-SEE.md) | Human picture desk: SVG first, math under the fold |
| [14 — Package](14-PACKAGE.md) | Think tank + visual appendage; picture slaves the math |
| [15 — Scan](15-NS-SCAN.md) | Break into rudimentary pieces; match leftover holes; do not weld |
| [16 — Shell](16-NS-SHELL.md) | Inside plus outer shape; silhouette may already be identified |

Machine-readable provenance (original expressions are immutable):

- `data/domain_architect/historical_equations.json`
- `data/domain_architect/conflicts.json`
- `data/domain_architect/null_results.json`

```bash
python -m domain_architect "∇²Φ = 4π G ρ"
python -m domain_architect --registry
python -m domain_architect --proceed
python -m domain_architect --refuse-splice COSMO B
python -m domain_architect --shape-compare J/X LAMBDA-MIN
python -m domain_architect --chain B
python -m domain_architect --geometry B
python -m domain_architect --tube B
python -m domain_architect --gap B
python -m domain_architect --shape-play B
python -m domain_architect --energy-play B
python -m domain_architect --overlay B
python -m domain_architect --scan
python -m domain_architect --scan B
python -m domain_architect --shell B
python -m domain_architect --consult
python -m domain_architect --see B
python -m domain_architect --refuse-splice SEE B
python -m unittest tests.test_domain_architect_acceptance tests.test_domain_architect_desk tests.test_domain_architect_visual
```

Related closed experiment in this repository:

- Protocol: [`docs/HB-RINGDOWN-EXPERIMENT-01.md`](../HB-RINGDOWN-EXPERIMENT-01.md)
- Report: [`docs/HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](../HB-RINGDOWN-EXPERIMENT-01-REPORT.md)

Primary sources named in the handoff but **not present in this repository**:

- `The_Audited_Harmonic_Blueprint.{pdf,docx,md}`
- `Domain_Architect_Working_App_v1_4.zip`
- `GUIDE.md`
