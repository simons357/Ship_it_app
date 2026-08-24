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
in [`docs/archive/`](docs/archive/README.md).

Specification: [`docs/DOMAIN-ARCHITECT.md`](docs/DOMAIN-ARCHITECT.md)

## Desktop app

```bash
pip install -r requirements.txt
python -m domain_architect app
```

That opens a local window at `http://127.0.0.1:8765/`. The **Mark** tab is
the slider studio for the official chrome-A + rainbow-triskelion icon
(Gold DOMAIN, All silver, live colors and geometry). Put the app on your Desktop:

```bash
python -m domain_architect app --install-shortcut
```

On macOS this writes `Domain Architect.command`. On Linux it writes
`Domain Architect.desktop`. Double-click to launch.

## Command line

```bash
python -m domain_architect "m*xdd + c*xd + k*x = f"
python -m domain_architect translate --example mechanical-electrical
python -m domain_architect cycle missing-damping
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
python -m unittest tests.test_sfe_hb_dump tests.test_domain_architect_v1 tests.test_domain_architect_acceptance tests.test_domain_architect_units tests.test_historical_archive tests.test_brand_mark
```
