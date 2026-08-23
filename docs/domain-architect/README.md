# Domain Architect v1.0

**Status:** live computational framework, August 2026  
**Specification:** [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md)  
**Mathematics:** [`OPERATIONAL-MATH.md`](OPERATIONAL-MATH.md)  
**Implementation audit:** [`ARCHITECTURE-AUDIT.md`](ARCHITECTURE-AUDIT.md) — items 1–6, 8, 9, 10 accepted in the SFE/HB dump

Domain Architect analyzes, translates and synthesizes systems by the
functional roles their components perform.

```
DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE
```

SFE, UHF, DHFA and the Harmonic Blueprint are **archived historical
reference**. They are not part of the live core. See
[`docs/archive/`](../archive/README.md).

## Commands

```bash
python -m domain_architect "m*xdd + c*xd + k*x = f"
python -m domain_architect translate --example mechanical-electrical
python -m domain_architect synthesize --target "x=1" --constraint "|u|<=6"
python -m domain_architect cycle missing-damping
python -m domain_architect cycle control
python -m domain_architect cycle drag
python -m domain_architect benchmark
python -m domain_architect --archive
python -m domain_architect app
python -m domain_architect app --install-shortcut
```

```bash
python -m unittest tests.test_domain_architect_v1 tests.test_domain_architect_acceptance tests.test_domain_architect_units
```

## What the software actually does

| Operation | Module | Working mathematics |
|---|---|---|
| DECOMPOSE | `decompose.py` | AST → functional architecture tree with role + confidence + rationale |
| TRANSLATE | `translate.py` | mechanical ↔ electrical LTI map with explicit `T` and SI-dimension breakage |
| compatibility | `compatibility.py` | DIRECTLY COMPATIBLE / TRANSFORMABLE / INCOMPATIBLE |
| SYNTHESIZE | `synthesize.py` | candidate architecture + provenance; refuses illegal substitutions |
| state / control | `dynamics.py` | RK4 of `ẋ = F(x,u,t)` and saturated PD |
| residual | `residual.py` | missing-role classification and role-restricted least squares |
| cycle | `pipeline.py` | paper §16 damping recovery, inverse design, analog, drag surrogate |

Functional correspondence is a hypothesis, not physical equivalence.
A mathematically coherent architecture is not automatically realizable.
The empirical validation gate is never self-awarded.
