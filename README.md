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

## Lemma★ (static \(\mathcal{R}_\star\) bound)

Static uniform \(\sup\mathcal{R}_\star<\infty\) is **dead**. A localized
divergence-free bump has \(\mathcal{R}_\star\sim\ell^{-3}\). Record:
[`docs/math/ns_attacks/ATTACK_10_LOCALIZED_BUMP.md`](docs/math/ns_attacks/ATTACK_10_LOCALIZED_BUMP.md).
**NS is not solved.** The remaining question is dynamical.

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack10_localized_bump.py --quick
python -m unittest tests.test_attack10_localized_bump
```

## Layout

| Path | Role |
|------|------|
| `hb_ringdown_test.py` | Spectral proximity statistic, MC null, BH-FDR, leave-one-event-out |
| `nodes.json` | Frozen node families + sigma + default observable |
| `data/qnm_events.csv` | Per-mode ringdown table with TRAIN/TEST splits |
| `scripts/build_qnm_table.py` | Rebuild CSV from measured + Kerr-fit sources |
| `scripts/ns_attacks/attack10_localized_bump.py` | Localized-bump kill of static uniform \(\mathcal{R}_\star\) |
| `tests/test_hb_ringdown.py` | Unit / smoke tests |
| `tests/test_attack10_localized_bump.py` | Attack 10 record + scaling / vacuous-shell checks |

## Tests

```bash
python -m unittest tests/test_hb_ringdown.py
```
