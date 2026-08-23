# Domain Architect

Computational framework for **functional-role architecture**.

```
DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE
```

Systems from different domains may be physically unrelated while still
containing mathematical structures that perform corresponding functions.
Domain Architect tests which structures survive translation and assembles
compatible mechanisms into candidate architectures. Correspondence is a
hypothesis, not physical equivalence.

Specification: [`docs/DOMAIN-ARCHITECT.md`](docs/DOMAIN-ARCHITECT.md)

```bash
pip install -r requirements.txt
python -m domain_architect "m*xdd + c*xd + k*x = f"
python -m domain_architect translate --example mechanical-electrical
python -m domain_architect cycle missing-damping
python -m domain_architect benchmark
```

## Layout

| Path | Role |
|---|---|
| `domain_architect/` | Live v1.0 package |
| `docs/DOMAIN-ARCHITECT.md` | Concept paper |
| `docs/domain-architect/` | Software and operational math |
| `docs/archive/` | Archived SFE / UHF / DHFA / Harmonic Blueprint |
| `data/domain_architect/` | Immutable historical equation inventory |
| `hb_ringdown_test.py` | Closed HB Experiment 01 (historical) |

## Tests

```bash
python -m unittest tests.test_domain_architect_v1 tests.test_domain_architect_acceptance tests.test_domain_architect_units tests.test_historical_archive
```

## Historical archive

The Simons Field Equation, Unified Harmonic Framework, DHFA, and the
Harmonic Blueprint book/experiment are retained as reference. They are
not loaded into the live decompose / translate / synthesize path.

```bash
python -m domain_architect --archive
```
