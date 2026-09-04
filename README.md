# Live notes: Track A, Track B, inverse-GCD floor

SFE, Harmonic Blueprint, and Millennium-packaged papers are **shelved**. See [`docs/SHELF.md`](docs/SHELF.md).

This repo’s working math is three separate tracks. Do not glue them.

| Track | Note | PDE / object |
|---|---|---|
| **A** | [`docs/AUGMENTED-NS-PROOF-CHAIN.md`](docs/AUGMENTED-NS-PROOF-CHAIN.md) | \(Q_1\)-augmented NS, \(\varepsilon>0\) |
| **B** | [`docs/UNAUGMENTED-R4-VORTICITY-PLAN.md`](docs/UNAUGMENTED-R4-VORTICITY-PLAN.md), [`docs/TRACK-B-LEMMAS.md`](docs/TRACK-B-LEMMAS.md) | Classical NS, keep \(1/r^4\) |
| **Q** | [`docs/SPECTRAL-FLOOR-EXPLORATION.md`](docs/SPECTRAL-FLOOR-EXPLORATION.md) | Inverse-GCD floors only |

## Process machine (no chops required)

Domain Architect as a **router + checker**, not a unifier: [`docs/DOMAIN-ARCHITECT-MACHINE.md`](docs/DOMAIN-ARCHITECT-MACHINE.md). DA is an anti-bullshit device. The whole desk: [`docs/DA-DESK.md`](docs/DA-DESK.md). The paper: [`docs/DA-PAPER.md`](docs/DA-PAPER.md). The name list you keep losing: [`docs/DA-THINK-TANK.md`](docs/DA-THINK-TANK.md). The working session: [`docs/DA-SESSION.md`](docs/DA-SESSION.md).

```bash
python3 scripts/da_machine.py status
python3 scripts/da_machine.py check
python3 scripts/da_machine.py cosmos
python3 scripts/da_machine.py sixteen
python3 scripts/da_machine.py fingers
python3 scripts/da_machine.py fate
python3 scripts/da_machine.py how
python3 scripts/da_machine.py flush
python3 scripts/da_machine.py wave
python3 scripts/da_machine.py game
python3 scripts/da_machine.py screen
python3 scripts/da_machine.py gq
python3 scripts/da_machine.py separate
python3 scripts/da_machine.py trackb
python3 scripts/da_machine.py sm
python3 scripts/da_machine.py smbreak
python3 scripts/da_machine.py team
python3 scripts/da_machine.py session
python3 scripts/da_machine.py lineage
python3 scripts/da_machine.py harmonic
python3 scripts/da_machine.py ground
python3 scripts/da_machine.py pipe
python3 scripts/da_machine.py desk
python3 scripts/da_machine.py compute
python3 scripts/da_machine.py alert
python3 scripts/da_machine.py classify --claim "the prime block of Q-tilde sits above -1/4"
```

## Checks

```bash
python3 -m unittest tests/test_augmented_ns_verify.py tests/test_spectral_floor_explore.py tests/test_track_b_lemmas.py tests/test_track_b_hardy_tube.py tests/test_track_b_bony_t.py tests/test_track_b_occupation.py tests/test_track_b_glue.py tests/test_track_b_low_j.py tests/test_track_b_climb.py tests/test_track_b_climb_law.py tests/test_track_b_evolve.py tests/test_track_b_geometry.py tests/test_track_b_stretch.py tests/test_track_b_balance.py tests/test_track_b_angular.py tests/test_track_b_coherent.py tests/test_track_b_field_occ.py tests/test_track_b_field_glue.py tests/test_track_b_ns_climb.py tests/test_track_b_climb_sketch.py tests/test_track_b_longer.py tests/test_track_b_dns.py tests/test_track_b_tube.py tests/test_da_machine.py tests/test_da_sixteen.py tests/test_da_fingers.py tests/test_da_how.py tests/test_da_flush.py tests/test_da_wave.py tests/test_da_game.py tests/test_da_screen.py tests/test_da_gq.py tests/test_da_separate.py tests/test_da_sm.py tests/test_da_sm_break.py tests/test_da_team.py tests/test_da_session.py tests/test_da_sm_lineage.py tests/test_da_harmonic.py tests/test_da_ground.py tests/test_da_pipe.py tests/test_da_desk.py tests/test_da_compute.py tests/test_da_alert.py
python3 scripts/augmented_ns_verify.py --n 16 --t 0.4 --dt 0.01 --nu 0.02 --eps 0.0 0.05 0.2
python3 scripts/spectral_floor_explore.py --nmax 80
```

## Shelved (do not use as input)

- HB Experiment 01: closed null. Protocol and report stay under `docs/HB-*.md`. Do not retune `nodes.json`.
- Domain Architect / Gemini unaugmented rewrite: audit only, [`docs/DOMAIN-ARCHITECT-SKETCH-AUDIT.md`](docs/DOMAIN-ARCHITECT-SKETCH-AUDIT.md).
- SFE / UHF / DHFA and any prize-packaged stack.
- Unifier-program exercise (reconstructed 16-vector, not Cosmos): [`docs/UNIFIER-EXERCISE.md`](docs/UNIFIER-EXERCISE.md).
