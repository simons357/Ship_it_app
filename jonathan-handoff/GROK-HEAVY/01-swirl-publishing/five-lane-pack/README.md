# Five-lane Lemma★ numeric pack (handoff)

Source: PR #48 tip `origin/cursor/ns-five-lane-lemma-star-1390` (`5938802`).

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
