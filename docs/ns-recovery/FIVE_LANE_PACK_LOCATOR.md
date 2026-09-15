# Five-lane pack locator (scripts)

**NS is not solved. Lemma★ is OPEN.**

**Export source:** [PR #48](https://github.com/simons357/Ship_it_app/pull/48) · `cursor/ns-five-lane-lemma-star-1390`  
**Handoff drop (this computer):** `/workspace/jonathan-handoff/GROK-HEAVY/01-swirl-publishing/`

## Absolute paths (locator)

| Need | Path |
|---|---|
| Moments / \(T_c\) / `ratio_R_star_shape` | `/workspace/scripts/ns_attacks/stokes_moments.py` |
| 9B \(K\) / polarization grow | `/workspace/scripts/ns_attacks/attack9b_exact_shell_K.py` |
| Package | `/workspace/scripts/ns_attacks/__init__.py` |
| Near-shell search | `/workspace/scripts/ns_attacks/lemma_star_near_shell_search.py` |
| Five-lane harness | `/workspace/scripts/ns_attacks/run_all_five.py` |
| Tests | `/workspace/tests/test_ns_attacks_lemma_star.py` |

**Box drop (same files):**  
`/workspace/jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts/ns_attacks/`

If you only paste one folder, paste `scripts/ns_attacks/` from that drop (or from PR #48 tip). That is enough for polarization-grow + \(R_★\) checks.

Original five lanes (`attack1`…`attack5`) are **not** 9A–9D. See [`FIVE-LANE-DISCUSSION-AND-MATH.md`](FIVE-LANE-DISCUSSION-AND-MATH.md).
