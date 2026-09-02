# Domain Architect v1.0

**Status:** live computational framework, August 2026  
**Operator contract:** [`DA-MODE.md`](DA-MODE.md) — honesty, missing claim ledger, NS not reopened, four-slot turbulence program  
**Specification:** [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md)  
**Mathematics:** [`OPERATIONAL-MATH.md`](OPERATIONAL-MATH.md)  
**Implementation audit:** [`ARCHITECTURE-AUDIT.md`](ARCHITECTURE-AUDIT.md) — items 1–6, 8, 9, 10 accepted in the SFE/HB dump  
**Validation challenge 01:** [`DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md`](DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md) — live score **FAIL** (A13 S1 refuse is in; A5 T1 still owed)  
**Leftover-split lab:** [`LEFTOVER-REPAIR.md`](LEFTOVER-REPAIR.md) — usable Ring SND + Q6 \(H_N\); three NS leftovers are conditional closes  
**Localized reparation:** [`LOCALIZED-REPAIR.md`](LOCALIZED-REPAIR.md) — `excise k` on an n-step chain; default dataset is the classical unaugmented 9-step chain; leftover cut is 7–8; graft stays a hypothesis  
**Honest OPEN board:** [`OPEN-BOARD.md`](OPEN-BOARD.md) — withdrawn / rejected / missing taken off the OPEN chorus  
**Intensity vs control:** [`TURBULENCE-INTENSITY.md`](TURBULENCE-INTENSITY.md) — lumped \(x\to x^\star\) against a no-actuation arm; not 3D NS  
**Available-tech stack:** [`AVAILABLE-TURBULENCE.md`](AVAILABLE-TURBULENCE.md) — riblets + discrete suction; 15% is the **desired** analog state  
**Ship-hull package:** [`SHIP-RIBLET-PACKAGE.md`](SHIP-RIBLET-PACKAGE.md) — Maersk-class fouling-release riblets; 8–12% Cf is desired; 12% is outside the durable literature  
**Turbulence-reduction program:** [`docs/projects/turbulence-reduction/README.md`](../projects/turbulence-reduction/README.md) — one DA project, four applications (ships ACTIVE; aircraft including drones, submarines, hypersonic QUEUED)

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
python -m domain_architect synthesize --target "x → 0.85" --constraint "|u| ≤ 6" --constraint "hardware already available"
python -m domain_architect cycle missing-damping
python -m domain_architect cycle control
python -m domain_architect cycle drag
python -m domain_architect cycle leftover-repair
python -m domain_architect cycle localized-repair
python -m domain_architect cycle localized-repair --excise 2
python -m domain_architect cycle open-board
python -m domain_architect cycle turbulence-intensity
python -m domain_architect cycle available-turbulence
python -m domain_architect cycle turbulence-reduction
python -m domain_architect translate --example snd-vs-h
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
| cycle | `pipeline.py` | paper §16 damping recovery, inverse design, analog, drag surrogate, available-tech stack, turbulence-reduction program |

Functional correspondence is a hypothesis, not physical equivalence.
A mathematically coherent architecture is not automatically realizable.
The empirical validation gate is never self-awarded.
