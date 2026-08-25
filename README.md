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

SFE and the Harmonic Blueprint are **not** the live product. They remain
in [`docs/archive/`](docs/archive/README.md). The axisymmetric swirl
paper is a **separate book** in [`docs/papers/swirl/`](docs/papers/swirl/README.md).

Specification: [`docs/DOMAIN-ARCHITECT.md`](docs/DOMAIN-ARCHITECT.md)

## Open the app

This is a local desktop app. It is not a public website.

**On a Mac:** double-click `Open Domain Architect.command` in this folder.

Or in Terminal, from this folder:

```bash
python3 -m domain_architect app
```

That opens `http://127.0.0.1:8765/` on *your* computer. The **Mark** tab
hosts Lambda Lab plus the black-and-gold and all-silver 3D lockups.

To put a launcher on your Desktop after you have opened it once:

```bash
python3 -m domain_architect app --install-shortcut
```

## Command line

```bash
python -m domain_architect "m*xdd + c*xd + k*x = f"
python -m domain_architect translate --example mechanical-electrical
python -m domain_architect cycle missing-damping
python -m domain_architect cycle leftover-repair
python -m domain_architect --archive
```

## What is standard, and what is DA

Lumped mechanical–electrical analogy, RK4, saturated PD, and
equation-error least squares are **standard methods used by** Domain
Architect. They are not Domain Architect itself. DA is the role
assignment, the broken-structure record, the substitution gate, and
the provenance requirement.

## Tests

```bash
python -m unittest tests.test_sfe_hb_dump tests.test_domain_architect_v1 tests.test_domain_architect_acceptance tests.test_domain_architect_units tests.test_historical_archive tests.test_brand_mark tests.test_desktop_app tests.test_phi_geometry_bridge tests.test_challenge_01_ns
```
