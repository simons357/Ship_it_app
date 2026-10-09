# Packet — Gate B trilinear DA audit (9 Oct 2026)

Canonical: `docs/GATE-B-TRILINEAR-DA-AUDIT.md`.
Geometry: `docs/GATE-B-ALL-RADII-LEMMA.md`.
Board: `docs/PROGRAM-GATES-A-D.md`.
Gate D: `docs/GATE-D-DYNAMICAL-BUDGET.md`.

```bash
python -m domain_architect --trilinear-ns
python3 scripts/ns_attacks/all_radii_counting.py
python3 scripts/ns_attacks/nonnegative_qx_dilation.py
PYTHONPATH=scripts python3 scripts/gate_d_fourier_budget.py --n 8 12 --t 0.2 --dt 0.02
```

CS-3 fails. Nonnegative \(\theta\ge\tfrac12\) is dilation, not counting.
Cutoff-independent dynamical budget OPEN. Not (17). NS not solved.
