# Harmonic Blueprint Experiment 01

Cross-event spectral selection test on black-hole ringdown modes.

**Status: closed — held-out TEST did not reject H0.**

The current scientific product and method are **Domain Architect** and **Functional Role Analysis**. That record is being reconciled in [`docs/domain-architect/`](docs/domain-architect/README.md). This experiment remains a closed null. It is not a gravity theory, a canonical Simons Field Equation, or evidence that nature privileges prime-indexed modes.

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
