# Attack 9B re-run confirmation (SoT rewrite)

Locked SoT (committed seed-1390 sweep):
- max K all / β>α: 0.641013 at (4, 8) — NOT HH→L
- max K β<α: 0.012320 at (5, 2)

Re-run (same --seed 1390 --kmax 6; optimizer scatter):
- max K all / β>α: 0.655728 at (4, 8) — NOT HH→L
- max K β<α: 0.012554 at (5, 2)

Qualitative β-split reproduced: argmax pairs unchanged; β>α ≫ β<α.
One pair (9,10) flaked amp_R_star tolerance 2.8e-8 > 1e-8 (numeric); ε-limit all pass.
NS not solved. Kill lane LIVE.
