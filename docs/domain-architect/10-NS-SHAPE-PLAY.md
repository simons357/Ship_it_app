# Play with the shape — fill the other side, then measure

**Not a regularity proof.** A filled side is not continuation past GAP-T3.
CosmoEvolution is not this lab.

```bash
python -m domain_architect --shape-play B
```

## The visual rule

If you can *see* the shape, some missing pieces are forced:

| Shape | Have | Fill | Status |
|---|---|---|---|
| Strain frame \(\lambda_1+\lambda_2+\lambda_3=0\) | two eigenvalues | the third | **identity** |
| Div-free \(\mathbf k\cdot\hat u(\mathbf k)=0\) | two components of \(\hat u\) | the third along \(\mathbf k\) | **identity** (B1) |
| Cylinder wall \(r=\delta\) | inside \(h\) with \(h(0)=0\) | outside by a chosen symmetry | **play** (extra \(E\)) |
| 3-shell packet | two shells | the third mass | **cannot fill** |
| \(I_{\mathrm{off}}\) | radial \(h=\Gamma/r\), even filled | \(\partial_z\Gamma\), \(\omega^r\) | **cannot fill** |

The cylinder looks symmetric. It is not a mirror of Navier–Stokes. The
wall \(r=\delta\) is a **cut you chose**, not a symmetry of the PDE.

## Play: even reflection

Take the inside. Reflect across the wall:

\[
h(\delta+s)=h(\delta-s)\implies h(2\delta)=h(0)=0.
\]

Young from the outside then fires. You can **see** it:

```
inside | wall | filled outside
▁▂▃▄▅▆█|█▆▅▄▃▂▁
```

That measurement is real on the manufactured field. It is also
`CLIP-T3-OUTER`: you put outer vanishing in by hand. Periodic
\(\mathbb{T}^3\) does not give it.

Inversion \(\rho=\delta^2/r\) is the Hardy dual of the same idea: another
playable copy, still extra \(E\).

Refusing to fill is the honest NS cut: the outside stays unknown.

## What play does not buy

Radial completion, even a pretty one, never produces \(\partial_z\Gamma\)
or \(\omega^r\). So even-reflect can buy **T3a** on a toy field and still
miss **T3b** (`CLIP-T3-WELD`). That is GAP-T3.

Strain is the contrast: filling \(\lambda_3\) is forced by the shape.
It still does not fill alignment (`CLIP-B3b-ALIGN`).

Related: [`09-NS-GAP.md`](09-NS-GAP.md), [`08-NS-TUBE-ESTIMATE.md`](08-NS-TUBE-ESTIMATE.md).
