# Five-lane Lemma★ numeric pack (handoff)

Source: PR #48 tip `origin/cursor/ns-five-lane-lemma-star-1390` (`5938802`).

## Preferred self-contained core

`scripts/ns_attacks/ns_lemma_star_core.py` is the **preferred self-contained Lemma★ shape core** (direct triad \(T_c\), dual \(D_s\) cross-check, `Field` class, shell generators, `build_closing_direction`). No external Stokes eigenbasis. Use it for \(R_★\) / polarization handoff. Existing `stokes_moments.py` + Attack 9B imports stay valid.

```bash
PYTHONPATH=jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts \
  python3 -c "from ns_attacks.ns_lemma_star_core import R_star, two_shell_field; print(R_star(two_shell_field()))"
```

**NS is NOT solved.** Numerics do not prove Lemma★.

## Run Attack 9B

```bash
cd /workspace
PYTHONPATH=jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts \
  python3 jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts/ns_attacks/attack9b_exact_shell_K.py \
  --kmax 6 --trials 60 --refine 30 --seed 1390
```

Or from repo scripts drop:

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_exact_shell_K.py --kmax 6 --trials 60 --refine 30 --seed 1390
```

SoT docs: `../lemma-star-sot/`
