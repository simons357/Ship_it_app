# Scan — leftover pieces, computer match, no weld

**Not a proof.** If the object is weird and you do not know what it is —
or you know the object and one slot is empty — Domain Architect breaks
itself down into rudimentary pieces and **scans** for an equation that
would actually fit.

Many views of one shape are still one object. A match is a candidate.
An empty scan is honest.

```bash
python -m domain_architect --scan B
python -m domain_architect --scan GAP-T3
```

## Anatomy first

Track B currently has three views of the same object: the PDE (`NS-B`),
packet mass (`J/X`), and conditional SND (`SND-C`). That is the
three-into-one. A hundred more charts would still be the same object.

The stacked overlay layers are the anatomy you already have. Holes do
not turn it into a different object.

## Then scan the leftover slot

Pieces come from:

- FRA slots \(P, H, \psi, \lambda, \Phi, E\)
- overlay layers (each chart)
- the historical equation inventory inside this repo

Against `CLIP-T3-WELD` the computer currently reports:

| Piece | Verdict | Fills? |
|---|---|---|
| T3a Young (cylinder) | `LOOKS_LIKE_FIT` | no — extra \(E\) |
| T5 \(I_{\mathrm{tube}}\) | `AFTER_NOT_FILL` | no |
| strain / Bernstein | `ALREADY_IN` | no |
| inverse-GCD, Cosmo, gravity, SFE | `WRONG_OBJECT` | no |

Nothing in the catalog fills the hole. Smooth stays false. Identified
stays true.

The picture is on the see-desk (`see-scan.svg`). CosmoEvolution is not
this scan.
