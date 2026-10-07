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

## Gate B assembly tests (7 October 2026)

Diagnostic Fourier bookkeeping for unaugmented NS. **Not (17). NS not solved.**

- First test (nonnegative \(Q_x\)): any uniform power bound requires \(\theta\ge 1/2\); optimal \(\theta\) remains open. Note: [`docs/GATE-B-SOURCE-ASSEMBLY-AND-CONCENTRATION-TEST.md`](docs/GATE-B-SOURCE-ASSEMBLY-AND-CONCENTRATION-TEST.md). Checker: `python3 scripts/ns_attacks/nonnegative_qx_assembly.py`.
- Second test (signed cancellation): exact \(T_{abc}\), one divergence-free field. Note: [`docs/GATE-B-SIGNED-CANCELLATION-TEST.md`](docs/GATE-B-SIGNED-CANCELLATION-TEST.md). Checker: `python3 scripts/ns_attacks/signed_cancellation_test.py`.

```bash
python3 -m unittest tests.test_nonnegative_qx_assembly tests.test_signed_cancellation -v
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

## Tests

```bash
python -m unittest tests/test_hb_ringdown.py
```
