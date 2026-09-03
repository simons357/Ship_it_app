# Live notes: Track A, Track B, inverse-GCD floor

SFE, Harmonic Blueprint, and Millennium-packaged papers are **shelved**. See [`docs/SHELF.md`](docs/SHELF.md).

This repo’s working math is three separate tracks. Do not glue them.

| Track | Note | PDE / object |
|---|---|---|
| **A** | [`docs/AUGMENTED-NS-PROOF-CHAIN.md`](docs/AUGMENTED-NS-PROOF-CHAIN.md) | \(Q_1\)-augmented NS, \(\varepsilon>0\) |
| **B** | [`docs/UNAUGMENTED-R4-VORTICITY-PLAN.md`](docs/UNAUGMENTED-R4-VORTICITY-PLAN.md) | Classical NS, keep \(1/r^4\) |
| **Q** | [`docs/SPECTRAL-FLOOR-EXPLORATION.md`](docs/SPECTRAL-FLOOR-EXPLORATION.md) | Inverse-GCD floors only |

## Process machine (no chops required)

Domain Architect as a **router + checker**, not a unifier: [`docs/DOMAIN-ARCHITECT-MACHINE.md`](docs/DOMAIN-ARCHITECT-MACHINE.md).

```bash
python3 scripts/da_machine.py status
python3 scripts/da_machine.py check
python3 scripts/da_machine.py cosmos
python3 scripts/da_machine.py sixteen
python3 scripts/da_machine.py fingers
python3 scripts/da_machine.py classify --claim "the prime block of Q-tilde sits above -1/4"
```

## Checks

```bash
python3 -m unittest tests/test_augmented_ns_verify.py tests/test_spectral_floor_explore.py tests/test_da_machine.py tests/test_da_sixteen.py tests/test_da_fingers.py
python3 scripts/augmented_ns_verify.py --n 16 --t 0.4 --dt 0.01 --nu 0.02 --eps 0.0 0.05 0.2
python3 scripts/spectral_floor_explore.py --nmax 80
```

## Shelved (do not use as input)

- HB Experiment 01: closed null. Protocol and report stay under `docs/HB-*.md`. Do not retune `nodes.json`.
- Domain Architect / Gemini unaugmented rewrite: audit only, [`docs/DOMAIN-ARCHITECT-SKETCH-AUDIT.md`](docs/DOMAIN-ARCHITECT-SKETCH-AUDIT.md).
- SFE / UHF / DHFA and any prize-packaged stack.
- Unifier-program exercise (reconstructed 16-vector, not Cosmos): [`docs/UNIFIER-EXERCISE.md`](docs/UNIFIER-EXERCISE.md).
