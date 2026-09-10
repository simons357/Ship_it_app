# Five-lane Lemma★ numerics pack (handoff)

**NS is NOT solved. Lemma★ remains OPEN. Kill lane LIVE.**

| Item | Value |
|------|-------|
| Tip SHA | `59388025f1e176c01e969d7de89386de206d5659` |
| Branch | `cursor/ns-five-lane-lemma-star-1390` |
| PR | https://github.com/simons357/Ship_it_app/pull/48 |
| Source | Full `scripts/ns_attacks/` + `tests/test_ns_attacks_lemma_star.py` from that tip |

## Layout

```
five-lane-pack/
  README.md                 (this file)
  scripts/ns_attacks/       (entire folder from PR tip)
  tests/test_ns_attacks_lemma_star.py
```

Sibling SoT docs (if present): `../lemma-star-sot/`

## Scripts included

Required:
- `stokes_moments.py` — Stokes moments / `ratio_R_star_shape` (= \(\mathcal{R}_\star\))
- `attack9b_exact_shell_K.py` — exact-shell \(K_{\alpha,\beta}\) probe (report β>α and β<α separately)
- `__init__.py`

Also included (full tip folder):
- `lemma_star_near_shell_search.py`, `run_all_five.py`
- `attack1_covariance.py` … `attack5_route2_kill.py`
- `attack3_bony_hh_l.py`, `attack9_packet_fan.py`

Repo locator copies (same tip): `/workspace/scripts/ns_attacks/`, `/workspace/tests/test_ns_attacks_lemma_star.py`

## Quick smoke

From repo root (or with `PYTHONPATH` pointing at `five-lane-pack/scripts`):

```bash
# Import + ratio_R_star_shape on a high-triad sample
PYTHONPATH=jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts \
  python3 -c "
from ns_attacks.stokes_moments import high_triad_field, probe, format_probe
r = probe(high_triad_field(amp=1.2))
print(format_probe(r))
assert r.ratio_R_star_shape == r.ratio_R_star
print('R_star_shape', r.ratio_R_star_shape)
"

# Tiny 9B sample (slow if trials large — keep small)
PYTHONPATH=jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts \
  python3 -m ns_attacks.attack9b_exact_shell_K --kmax 4 --trials 4 --refine 2 --max-modes 4

# Unit tests (from pack)
PYTHONPATH=jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts \
  python3 -m pytest jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/tests/test_ns_attacks_lemma_star.py -q
```

Canonical quotient code name: `ratio_R_star_shape`. Legacy `ratio_star` is a different (post-Young) quantity.
