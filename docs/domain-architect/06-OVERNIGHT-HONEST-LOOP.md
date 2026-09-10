# Overnight honest loop — Domain Architect

**Audience:** Jonathan (nap-time polish)  
**Status:** structural translator demo — not a Theory of Everything  
**Canonical SFE status:** unresolved

This note documents the full loop now available on the NS-B five-finger
router branch:

```
auto role-assign
  → reconstruct (inventory)
  → compare (unlike books)
  → tuning export (control variables)
  → incompleteness / math-complete *candidates*
  → drill-down H → (H1,H2,…) + recompose
  → put SFE in twice (dual registry compare)
```

## Run the demo

```bash
python3 scripts/overnight_honest_loop_demo.py
```

Useful CLI slices:

```bash
# Auto audit (roles + reconstruct + incompleteness + drill-down + tuning)
python3 -m domain_architect "partial_t omega = (omega * nabla) u + nu Delta omega"

# Thin NS — incompleteness candidates (book templates only)
python3 -m domain_architect --incompleteness-json "partial_t omega = nu Delta omega"

# Recursive module tree
python3 -m domain_architect --decompose-json "partial_t omega = (omega * nabla) u + nu Delta omega"

# Roles-in → candidate equation sketch
python3 -m domain_architect --roles-sketch \
  "admissibility,interaction,state,scale_response,realized_output,environment"

# Put SFE in twice (historical registry candidates)
python3 -m domain_architect --list-sfe
python3 -m domain_architect --sfe-compare SFE-H001 SFE-H002
```

## Honesty constraints (non-claims)

| Temptation | Software stance |
|---|---|
| Theory of Everything | Organizational FRA only |
| Clay / Millennium regularity | Explicitly out of scope for Track B |
| Bake `λ_min(Q_N)>-1/2` into NS | Never; NS-B is classical unaugmented book |
| `P` means prime | `P` is admissibility / Leray in NS-B; primes stay experimental |
| Canonical SFE | Status string remains `unresolved`; dual-SFE compare refuses hybrid synthesis |
| Candidate completions invent physics | Candidates are frozen **book templates**, labeled as such |

## What “math-complete candidates” means

If required roles or classical terms are missing, Domain Architect reports
the gap and may propose a *candidate* completion from the NS-B or
gravity-poisson book (e.g. restore `(ω·∇)u`). That is inventory repair
language — not a discovery of new fluids physics.

## What drill-down means

`H → (H1, H2, …)` is recorded as a first-class module tree. Recompose
checks that children cover the parent inventory. The stop rule is:

> Stop when remaining objects are defined, measurable, or standard operators.

Example terminals: viscosity `ν` (measurable), Laplacian `Δ` (standard),
Biot–Savart kernel (classical operator).

## Dual SFE

`--sfe-compare` audits two registry ids (or raw strings) side-by-side.
Distinct historical SFE candidates are flagged `INCOMPATIBLE` at the
provenance layer. Identical strings audited twice stay `IDENTICAL` and
still do **not** become canonical.
