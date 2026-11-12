# Packet — Centered drift (12 November 2026)

Repo notes:

- [`docs/ns-review/CENTERED-DRIFT.md`](../docs/ns-review/CENTERED-DRIFT.md)
- [`docs/ns-review/CENTERED-EQUATION.md`](../docs/ns-review/CENTERED-EQUATION.md)

Checkers:

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/centered_drift.py
python3 -m unittest tests.test_centered_drift -v
```

Centered equation: **EXACT**.
Drift estimate \(T_c\le\theta\nu D_s+K(t)X\): **OPEN**.
Uniform absorption \(T_c\le C\nu D_s\): **KILLED**.
Need★: **MISSING**.
`ns_solved`: false.

Do not put \(K(t)\) in the PDE. NS is not solved.
