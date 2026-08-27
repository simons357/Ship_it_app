# Domain Architect — Functional Role Analysis

**Status:** scientific rectification, August 2026 — software plus historical registry  
**Product:** Domain Architect  
**Method:** Functional Role Analysis  
**Canonical SFE status:** unresolved  
**Universe / unified picture:** unresolved — [Universe program](UNIVERSE-PROGRAM.md)  
**This folder is not a theory of everything, a canonical Simons Field Equation, or a proof of physical prime indexing.**

Approved plain-language explanation:

> Paste an equation. Domain Architect identifies what each component does, how the components connect, and which parameters can be tested or tuned.

Domain Architect is inquiry. ChatVault is search. They are not the same engine.
The live desk cites Route C `10.5281/zenodo.22050963` (exploratory),
Φ-renormalization `10.5281/zenodo.22050974` (Q1-augmented swirl; not Clay),
Ring `10.5281/zenodo.22050976`, and Q6 `10.5281/zenodo.22050962`. June posters
are a dated archive on that desk.

| Document | Purpose |
|---|---|
| [Universe program](UNIVERSE-PROGRAM.md) | What is live, what is open, what DA is for, what is not claimed |
| [00 — Audited baseline](00-AUDITED-BASELINE.md) | Frozen framework, terminology, evidence levels |
| [01 — Equation inventory](01-EQUATION-INVENTORY.md) | Historical UHF / SFE / DHFA / gravity / prime-index formulas found in this repo family |
| [02 — Conflict table](02-CONFLICT-TABLE.md) | Incompatible definitions, units, domains, and claims |
| [03 — Reconciliation](03-RECONCILIATION.md) | Six-point response to the August 2026 handoff |
| [04 — Notation collisions](04-NOTATION-COLLISIONS.md) | `P` / `p` / `ℙ`, `Φ` / `φ` / `ϕ`, and other overloaded symbols |
| [05 — Rectification](05-RECTIFICATION.md) | Software implementation of the August 2026 corrective specification |
| [RH Track B — Möbius–GCD](TRACK-B-MOBIUS.md) | Locked RH operator, exact identities, missing Mertens bridge. RH not claimed |
| [Route C](ROUTE-C.md) | Exploratory conditional face in DA only. Not ChatVault. RH not claimed |

Machine-readable provenance (original expressions are immutable):

- `data/domain_architect/historical_equations.json`
- `data/domain_architect/conflicts.json`
- `data/domain_architect/null_results.json`

```bash
python -m domain_architect "∇²Φ = 4π G ρ"
python -m domain_architect --registry
python -m domain_architect --drain-chatvault "∇²Φ = 4π G ρ" -o /tmp/da-drain.json
python3 -m domain_architect --ingest-chatvault PATH
python -m domain_architect --site   # http://127.0.0.1:8765/ — ChatVault search + DA inquiry
python -m domain_architect --track-b-mobius   # RH Track B Möbius–GCD attack; does not claim RH
python -m domain_architect --route-c          # Route C face in DA; not ChatVault; does not claim RH
python -m domain_architect --universe         # universe / SFE picture; unresolved; not a proof
python -m unittest tests.test_domain_architect_acceptance tests.test_chatvault_bridge tests.test_track_b_mobius tests.test_route_c tests.test_universe tests.test_zenodo_public_record
```

Finished inquiries and audits can file into ChatVault as `origin_class: human_record`. Domain Architect does not prove theorems. ChatVault is the search box (**OS for your AI**). Domain Architect is the inquiry box.

Related closed experiment in this repository:

- Protocol: [`docs/HB-RINGDOWN-EXPERIMENT-01.md`](../HB-RINGDOWN-EXPERIMENT-01.md)
- Report: [`docs/HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](../HB-RINGDOWN-EXPERIMENT-01-REPORT.md)

Owner restore pack for public Zenodo titles (this software does not write to zenodo.org; Domain Architect did not withdraw those deposits):

- [`docs/zenodo-public-record/README.md`](../zenodo-public-record/README.md) — strip retraction stamps; prize-claim language is walked back; files stay published.

Primary sources named in the handoff but **not present in this repository**:

- `The_Audited_Harmonic_Blueprint.{pdf,docx,md}`
- `Domain_Architect_Working_App_v1_4.zip`
- `GUIDE.md`
