# Five-lane pack locator (scripts)

**NS is not solved. Lemma★ is OPEN.** Numerics ≠ proof.

**Repo / PR (export source):** [PR #48](https://github.com/simons357/Ship_it_app/pull/48) · branch `cursor/ns-five-lane-lemma-star-1390`  
**This paste:** recovery branch `cursor/centered-ns-recovery-b5c1` (PR #45) — PR #48 `scripts/ns_attacks/` plus later identity / 9D helpers.

Docs already on the shared box: this folder (`lemma-star-sot/`).  
**Scripts were missing. They are now under** `../five-lane-pack/scripts/ns_attacks/`.

---

## Drop on this computer

```
/workspace/jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts/ns_attacks/
```

Locator-style absolute copies also live at:

```
/workspace/scripts/ns_attacks/
```

If you only move one folder onto the box, move `five-lane-pack/scripts/ns_attacks/` (and `five-lane-pack/tests/` if you want the lock tests).

---

## Minimum to run numerics (polarization-grow + \(R_★\))

| # | File | Role |
|---|---|---|
| 1 | `stokes_moments.py` | \(E,X,Y,Z,\Lambda,T_c,D_s\), `ratio_R_star_shape` |
| 2 | `attack9b_exact_shell_K.py` | 9B \(K_{\alpha,\beta}\) / aligned closing packet |
| 3 | `__init__.py` | package marker |

## Strongly useful next

| # | File | Role |
|---|---|---|
| 4 | `lemma_star_near_shell_search.py` | near-shell / two-shell \(R_★\) search |
| 5 | `run_all_five.py` | original five lanes (1–5), not 9A–9D |
| 6 | `../../tests/test_ns_attacks_lemma_star.py` | formula lock |

## Optional (original five lanes — separate from 9A–9D)

`attack1_covariance.py` … `attack5_route2_kill.py`, `attack3_bony_hh_l.py`, `attack9_packet_fan.py`

## Extra on this paste (not on PR #48 tip)

`counting_cs.py`, `attack9d_growing_io.py` — retargeted 9D helpers. Not required for 9B / \(R_★\).

---

## Run (from `five-lane-pack/`)

```bash
cd /workspace/jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack
PYTHONPATH=scripts python3 -m pytest tests/test_ns_attacks_lemma_star.py -q
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_exact_shell_K.py \
  --kmax 4 --trials 8 --refine 4 --seed 1390 --outdir /tmp/attack9b_exact_shell
```

`ratio_R_star_shape` is \(\mathcal R_\star=(T_c_+)^2/(D_s E Y)\).  
9B \(\varepsilon\to0\) limit equals \(K_{\alpha,\beta}(w)\) only for aligned, sign-selected \(z_\beta\parallel\Pi_\beta B(w,w)\).

**Do not** treat a finite \(\max K\) or a finite \(\mathcal R_\star\) sample as a proof. One large finite value only raises \(C_{\mathrm{geom}}\).
