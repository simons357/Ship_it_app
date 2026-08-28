# Harmonic Blueprint / Domain Architect

This repository now contains three related objects. Neither research
package is a unified physical theory. AI Surgeon is a separate clinical
training game, not a Domain Architect face.

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

## AI Surgeon

Phone-first surgical residency prototype (Simons Medical Innovations).
See one / do one / teach one. Not ChatVault, not Domain Architect, and
not a clinical reference.

- Hub + modules: [`ai_surgeon/`](ai_surgeon/)
- Storyboard: [`ai_surgeon/docs/AI-Surgeon-Storyboard.pdf`](ai_surgeon/docs/AI-Surgeon-Storyboard.pdf)

```bash
python3 -m ai_surgeon          # http://127.0.0.1:8770/  (not DA's 8765)
node --test ai_surgeon/tests/*.mjs
python3 -m unittest tests.test_ai_surgeon tests.test_ai_surgeon_hub tests.test_ai_surgeon_docs tests.test_ai_surgeon_screens tests.test_ai_surgeon_brand tests.test_ai_surgeon_voices tests.test_ai_surgeon_pen
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
| `domain_architect/` | FRA / model-auditing software |
| `ai_surgeon/` | AI Surgeon hub, appendectomy, trauma module 02 (port 8770) |
| `hb_ringdown_test.py` | Spectral proximity statistic, MC null, BH-FDR, leave-one-event-out |
| `nodes.json` | Frozen node families + sigma + default observable |
| `data/qnm_events.csv` | Per-mode ringdown table with TRAIN/TEST splits |
| `scripts/build_qnm_table.py` | Rebuild CSV from measured + Kerr-fit sources |
| `tests/test_hb_ringdown.py` | Unit / smoke tests |

## Tests

```bash
python -m unittest tests/test_hb_ringdown.py tests/test_ai_surgeon.py tests/test_ai_surgeon_hub.py tests/test_ai_surgeon_docs.py
```
