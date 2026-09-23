# Harmonic Blueprint / Domain Architect

This repository now contains two related research objects. Neither is a
unified physical theory.

## Unaugmented generic 3-D NS — proof chain

11 September 2026 chain of reductions. Classical incompressible NS only.
Lemma Star is finished bookkeeping. The remainder is \(T_{j\leftarrow j}\).
Generic regularity is not claimed. Swirl is a subclass, not Step 7.

- Chain: [`docs/ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md`](docs/ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md)
- Lock: [`data/ns_proof_chain/2026-09-11.json`](data/ns_proof_chain/2026-09-11.json)
- Subclass: [`docs/SWIRL_AXIAL_REDUCTION.md`](docs/SWIRL_AXIAL_REDUCTION.md)

```bash
python -m unittest tests.test_unaug_generic_3d_chain
```

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

## Tests

```bash
python -m unittest tests/test_hb_ringdown.py
python -m unittest tests.test_unaug_generic_3d_chain
```
