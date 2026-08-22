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
| [06 — Overnight honest loop](06-OVERNIGHT-HONEST-LOOP.md) | Auto → reconstruct → compare → tuning → incompleteness → SFE×2 |
| [OVERNIGHT-DEMO](OVERNIGHT-DEMO.md) | Wake-up copy-paste commands + artifact index |
| [GROK-RIGOR-HANDOFF](GROK-RIGOR-HANDOFF.md) | Pasteable working note for adversarial rigor review |
| [GROK-ATTACK-CHECKLIST](GROK-ATTACK-CHECKLIST.md) | Bullet attack surface for Grok / external review |

Machine-readable provenance (original expressions are immutable):

- `data/domain_architect/historical_equations.json`
- `data/domain_architect/conflicts.json`
- `data/domain_architect/null_results.json`

```bash
python -m domain_architect "∇²Φ = 4π G ρ"
python -m domain_architect --registry
python -m domain_architect --sfe-compare SFE-H001 SFE-H002
python -m domain_architect --incompleteness-json "partial_t omega = nu Delta omega"
python scripts/overnight_honest_loop_demo.py
python -m unittest tests.test_domain_architect_acceptance
```

Related closed experiment in this repository:

- Protocol: [`docs/HB-RINGDOWN-EXPERIMENT-01.md`](../HB-RINGDOWN-EXPERIMENT-01.md)
- Report: [`docs/HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](../HB-RINGDOWN-EXPERIMENT-01-REPORT.md)

Primary sources named in the handoff but **not present in this repository**:

- `The_Audited_Harmonic_Blueprint.{pdf,docx,md}`
- `Domain_Architect_Working_App_v1_4.zip`
- `GUIDE.md`
