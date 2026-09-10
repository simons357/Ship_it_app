# `ns_lemma_star_core.py` — self-contained SoT identities

**NS is NOT solved. Lemma★ remains OPEN.** This note documents a numerics module only; it does **not** prove or kill ★.

## What it is

`scripts/ns_attacks/ns_lemma_star_core.py` is a **self-contained exact finite-support** implementation of the Lemma★ shape identities from `LEMMA_STAR_SHAPE_FORM.md` / `LEMMA_STAR_EXACT_FORMULAS.md`:

- Moments \(E,X,Y,Z,\Lambda\) and both \(\mathcal{D}_s\) forms (moment vs direct spectral sum), cross-checked on every `R_star` call
- Signed \(T_c\) via **direct triad summation** (no FFT / no grid truncation / no aliasing)
- Reality \(v_{-k}=\overline{v_k}\) and Leray projection enforced at `Field.set_mode`
- Quotient \(\mathcal{R}_\star=(T_c)_+^2/(\mathcal{D}_s\,E\,Y)\)

No external Stokes/eigenbasis code is imported. Independence from `stokes_moments.py` is intentional.

## Relation to `stokes_moments.py`

Same SoT formulas; different field representation (`Field` class vs `dict` of modes). Numerical cross-checks on shared two-shell / mapped fields should agree on \(E,X,Y,Z,\Lambda,\mathcal{D}_s,T_c,\mathcal{R}_\star\) when modes are mapped 1–1. Disagreement would indicate a bug, not a different lemma.

## Handoff

Also shipped under:

`jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack/scripts/ns_attacks/ns_lemma_star_core.py`
