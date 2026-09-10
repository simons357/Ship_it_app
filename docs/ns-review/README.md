# NS / SND review docs

| Doc | Role |
| --- | --- |
| [`FIVE-LANE-BOOKKEEPING.md`](./FIVE-LANE-BOOKKEEPING.md) | **Precision locks:** Attack 3 not strictly HH→L; `ratio_R_star_shape` ≠ `ratio_star`; 9C SoT-only |
| [`five-lane-recovery/`](./five-lane-recovery/) | Recovered PR #48 five-lane pack (+ `PR48_five_lane_export.zip`) |
| [`LEMMA-STAR-DA-NS-1.md`](./LEMMA-STAR-DA-NS-1.md) | **Lemma★ / DA-NS-1:** energy-budget Clay packaging; broken at PRODUCT-BLOCK |
| [`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md) | Exact Fourier / \(\mathcal R_\star\) formulas (shape lock-in) |
| [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md) | **Attack 9A** negative for kill; protocol + controls |
| [`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md) | **Attack 9B** exact-shell + closing → \(K_{\alpha,\beta}\); max \(K\approx0.641\) at \((4,8)\) **not** HH→L |
| [`ATTACK-9C-FIXED-GAP-SPHERES.md`](./ATTACK-9C-FIXED-GAP-SPHERES.md) | **Attack 9C** fixed-gap: natural same-shell **not a kill**; SoT-only \(0.11\to0.031\) |
| [`ATTACK-9-FIXED-GAP-SPHERES.md`](./ATTACK-9-FIXED-GAP-SPHERES.md) | Legacy alias → 9C (older notes called \(\Theta(m^2)\) “9C” — now **9D**) |
| [`ATTACK-9D-THETA-M2-LOCKED-PHASE.md`](./ATTACK-9D-THETA-M2-LOCKED-PHASE.md) | **Attack 9D** designed \(\Theta(m^2)\)-closure, locked phases |

**Inventory / tooling:** `domain_architect/kab_quantity.py`, `domain_architect/lemma_star.py`, `domain_architect/rstar_quantities.py`

**Runtime:**

```bash
python3 -m unittest tests.test_kab_quantity -v
PYTHONPATH=docs/ns-review/five-lane-recovery/scripts \
  python3 docs/ns-review/five-lane-recovery/scripts/ns_attacks/attack9b_exact_shell_K.py --help
```

**Jonathan action:** **None** (precision lock only).
