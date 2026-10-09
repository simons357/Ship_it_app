# Harmonic Blueprint / Domain Architect

This repository now contains two related research objects. Neither is a
unified physical theory.

## Domain Architect

Functional Role Analysis and model-auditing software. It classifies
equations into independently meaningful mathematical roles, records
historical UHF / SFE / DHFA candidates without merging them, and refuses
to treat representation of a known equation as derivation.

- Package: `domain_architect/`
- Notes: [`docs/domain-architect/README.md`](docs/domain-architect/README.md)
- Canonical SFE status: **unresolved**

```bash
python -m domain_architect "∇²Φ = 4π G ρ"
python -m domain_architect --registry
python -m unittest tests.test_domain_architect_acceptance tests.test_domain_architect_units
```

## Harmonic Blueprint Experiment 01

Cross-event spectral selection test on black-hole ringdown modes.

**Status: closed — held-out TEST did not reject H0.**

- Closed report: [`docs/HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](docs/HB-RINGDOWN-EXPERIMENT-01-REPORT.md)
- Protocol: [`docs/HB-RINGDOWN-EXPERIMENT-01.md`](docs/HB-RINGDOWN-EXPERIMENT-01.md)
- Numeric summary: [`results/SUMMARY.md`](results/SUMMARY.md)

## Quick start

```bash
pip install -r requirements.txt
python scripts/build_qnm_table.py   # refresh data/qnm_events.csv if needed
python hb_ringdown_test.py \
  --csv data/qnm_events.csv \
  --nodes nodes.json \
  --mc 50000 \
  --split test
```

Exploratory TRAIN run (freeze choices before TEST):

```bash
python hb_ringdown_test.py --csv data/qnm_events.csv --nodes nodes.json --mc 50000 --split train
```

## Layout

| Path | Role |
|------|------|
| `hb_ringdown_test.py` | Spectral proximity statistic, MC null, BH-FDR, leave-one-event-out |
| `nodes.json` | Frozen node families + sigma + default observable |
| `data/qnm_events.csv` | Per-mode ringdown table with TRAIN/TEST splits |
| `scripts/build_qnm_table.py` | Rebuild CSV from measured + Kerr-fit sources |
| `tests/test_hb_ringdown.py` | Unit / smoke tests |

## Navier–Stokes gates (not a regularity proof)

Independent Domain Architect audit of the Gate B trilinear claim, plus
Gate D Fourier measurements. Classical unforced 3-D Navier–Stokes stays
**open**. Theorem (17) is not claimed.

- Board: [`docs/PROGRAM-GATES-A-D.md`](docs/PROGRAM-GATES-A-D.md)
- DA audit: [`docs/GATE-B-TRILINEAR-DA-AUDIT.md`](docs/GATE-B-TRILINEAR-DA-AUDIT.md)
- Gate D: [`docs/GATE-D-DYNAMICAL-BUDGET.md`](docs/GATE-D-DYNAMICAL-BUDGET.md)

```bash
python -m domain_architect --trilinear-ns
python3 scripts/ns_attacks/all_radii_counting.py
python3 scripts/ns_attacks/nonnegative_qx_dilation.py
PYTHONPATH=scripts python3 scripts/gate_d_fourier_budget.py --n 8 12 --t 0.2 --dt 0.02
python -m unittest tests.test_all_radii_counting tests.test_trilinear_da_audit \
  tests.test_nonnegative_qx_dilation tests.test_gate_d_fourier_budget tests.test_ns_solver_core
```

## Tests

```bash
python -m unittest tests/test_hb_ringdown.py
```
