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

## Gate D v1.2 (physical-cutoff preregistration)

New preregistration, not an amendment of v1.1. Attached as a file so the
cutoff convention can be approved or rejected.

- [`docs/GATE-D/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md`](docs/GATE-D/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md)
- [`packets/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md`](packets/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md)
- [`packets/gate_d/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md`](packets/gate_d/GATE-D-V1.2-PHYSICAL-CUTOFF-PREREGISTRATION.md)

Frozen \(\kappa_\star=8\), grids \(n=64,96\), ceiling 2 GiB peak RSS.
DA decision pending. Memory benchmark not done. Gate D OPEN. NS not solved.

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

## Tests

```bash
python -m unittest tests/test_hb_ringdown.py
```
