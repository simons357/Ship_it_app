# Scientific rectification — implemented software

**Date:** 2026-08-22  
**Branch purpose:** implement the August 2026 Domain Architect rectification  
**Not in scope:** inventing a unified theory or selecting a canonical SFE

This document records what the software now enforces. The historical
inventory in [01](01-EQUATION-INVENTORY.md) and the conflict table in
[02](02-CONFLICT-TABLE.md) remain the human-readable source notes. The
machine-readable registry is:

- `data/domain_architect/historical_equations.json`
- `data/domain_architect/conflicts.json`
- `data/domain_architect/null_results.json`

Permanent identifiers use the `*-H###` scheme (H = historical candidate).
Previous aliases such as `SFE-PUB` and `GRV-1` are stored on each record
and are not overwritten.

## Scope the software is allowed to claim

Every report states:

- the highest evidence level actually supported (0–6);
- `Canonical SFE status: unresolved.`;
- that `Φ = ℱ(P, H, ψ, λ; E)` is an organizational grammar.

The software must not imply that UHF, SFE, or DHFA are established laws,
that primes are physically privileged, or that an FRA rewrite derives a
known theory.

## Corrections now implemented

| Rectification | Module |
|---|---|
| Evidence hierarchy and forbidden claim language | `schema.py`, `report.py` |
| Scale coordinate `κ` vs response `R(κ)` | `checks.py`, `gravity.py` |
| Projector vs selector vs filter, with `P² = P` | `checks.classify_permission` |
| Source/state split only with an explicit rule | `checks.decompose_source_state` |
| Periodic Poisson zero-mode / solvability | `gravity.solve_periodic_poisson` |
| Canonical index audit, including degeneracy | `index_audit.py` |
| Sensitivity / local rank / conditioning / global caveat | `identifiability.py` |
| Representation recovery vs limiting-theory recovery | `recovery.py` |
| Historical provenance + conflict engine | `registry.py` + JSON stores |
| Retain / revise / retire (retired records kept) | equation `audit_disposition` |
| AST parser (no name-only role inference) | `parser.py`, `classify.py` |
| Dimensional and mathematical-type checks | `checks.py` |
| Tensor free-index check | `checks.check_types` |
| Geometry / gauge expansion of `E` | `GeometryRecord` |
| GR extra-structure warnings | `audit.py` |
| Equal-budget selector laboratory | `selectors.py` |
| Train / validation / held-out protocol hash | `protocol.py` |
| Null and counterexample registry | `null_results.json`, `EquationRegistry.record_null` |
| Computing-bench desk (layers, books, next moves) | `desk.py`, `--proceed`, `--refuse-splice` |
| Confidence taxonomy | `report.ConfidenceTaxonomy` |

## Canonical SFE

No historical candidate meets the §23 checklist. The live status string
is `unresolved`. Discovering that no single canonical SFE can be justified
is a valid scientific outcome and is stored as `NULL-SFE-CANON`.

## Acceptance tests

`tests/test_domain_architect_acceptance.py` covers Tests A–H from the
rectification report.

```bash
python -m unittest tests.test_domain_architect_acceptance tests.test_domain_architect_units
```

```bash
python -m domain_architect "∇²Φ = 4π G ρ"
python -m domain_architect --registry
python -m domain_architect --proceed
```
