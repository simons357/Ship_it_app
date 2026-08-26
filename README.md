# Harmonic Blueprint / Domain Architect / ChatVault

This repository is a workshop. It now contains three related objects.
Neither research package is a unified physical theory. ChatVault is a
local product prototype, not an App Store release.

## ChatVault

Local-first vault — tagline **OS for your AI**. Git PWA in `chatvault/` is
the canonical engine (`ChatVaultEntry`, CLAIM_LEDGER, hybrid search,
`origin_class` AI vs real). Base44 glass is a different schema.

- App: [`chatvault/`](chatvault/)
- Operational report: [`docs/chatvault-audit/CHATVAULT-OPERATIONAL.md`](docs/chatvault-audit/CHATVAULT-OPERATIONAL.md)
- Audit packet: [`docs/chatvault-audit/README.md`](docs/chatvault-audit/README.md)

```bash
cd chatvault
python3 -m http.server 4173   # open http://127.0.0.1:4173/
node --test tests/*.mjs
```

Drain a Domain Architect FRA audit (not a proof) into ChatVault JSON:

```bash
python3 -m domain_architect --drain-chatvault "∇²Φ = 4π G ρ" -o /tmp/da-drain.json
python3 -m domain_architect --ingest-chatvault PATH   # any source → chatvault/inbox JSON (+ media copy)
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
python -m domain_architect --site
python3 -m unittest tests.test_domain_architect_acceptance tests.test_domain_architect_units tests.test_chatvault_bridge tests.test_chatvault_ingest
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
| `chatvault/` | Local-first ChatVault PWA (Steel default; origin split; DA drain hook) |
| `hb_ringdown_test.py` | Spectral proximity statistic, MC null, BH-FDR, leave-one-event-out |
| `nodes.json` | Frozen node families + sigma + default observable |
| `data/qnm_events.csv` | Per-mode ringdown table with TRAIN/TEST splits |
| `scripts/build_qnm_table.py` | Rebuild CSV from measured + Kerr-fit sources |
| `tests/test_hb_ringdown.py` | Unit / smoke tests |

## Tests

```bash
python -m unittest tests/test_hb_ringdown.py
```
