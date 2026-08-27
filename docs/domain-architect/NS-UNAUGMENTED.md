# Classical unaugmented 3D Navier–Stokes (OPEN)

**Book:** unaugmented incompressible 3D NS  
**PDF:** `domain_architect/static/faces/ns_unaugmented_classical.pdf`  
**ChatVault:** **no.**  
**Clay NS / RH:** **not claimed.**

Operator:

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,\qquad \nabla\cdot u=0.
\]

Vorticity form (inventory NS-B):

\[
\partial_t\omega+(u\cdot\nabla)\omega=(\omega\cdot\nabla)u+\nu\Delta\omega.
\]

This face is **OPEN / not proved**. It is kept visible so the classical equation can be seen. It is not a withdrawn stamp.

Excluded: Q1 / fractional hyperdissipation / Φ-system. Those belong to the swirl Phi book, not this PDE.

## Archive packaging

- [10.5281/zenodo.20405526](https://doi.org/10.5281/zenodo.20405526) — May T³ prize packaging (title restored; prize language walked back). TeX/HTML under `/faces/archive/`.
- June T³ one-pager: `/faces/superseded/tweet_ns_t3_onepager.png` — SUPERSEDED as a proof graphic.

Live fluids cites (different books, not this unaugmented PDE):

- Phi [10.5281/zenodo.22050974](https://doi.org/10.5281/zenodo.22050974)
- Ring [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976) (conditional SND)

```bash
python3 -m domain_architect --ns-unaugmented
python3 -m domain_architect "∂_t u + (u·∇)u = −∇p + νΔu,  ∇·u = 0"
python3 -m domain_architect --site
# Inquiry → Load unaugmented NS
```
