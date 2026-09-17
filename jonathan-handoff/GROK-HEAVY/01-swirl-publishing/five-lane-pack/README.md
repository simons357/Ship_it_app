# five-lane-pack — scripts drop

Paste this `scripts/ns_attacks/` folder onto the shared box.  
Docs live next door in `../lemma-star-sot/`. Locator: `../lemma-star-sot/FIVE_LANE_PACK_LOCATOR.md`.

**Minimum for polarization-grow + \(R_★\):** `stokes_moments.py`, `attack9b_exact_shell_K.py`, `__init__.py`.

```bash
PYTHONPATH=scripts python3 -m pytest tests/test_ns_attacks_lemma_star.py -q
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_exact_shell_K.py \
  --kmax 4 --trials 8 --refine 4 --seed 1390 --outdir /tmp/attack9b_exact_shell
```

NS not solved. Lemma★ open.
