# Visual journey — proof chain

Public face: pictures + clean math. Experts read the chain; node colors carry status. This pack does **not** stamp solved / unsolved verdicts.

Companion math: [`../PROOF-CHAIN-CLEAN.md`](../PROOF-CHAIN-CLEAN.md).

## Figures (generated)

| File | Role |
| --- | --- |
| [`figures/proof-chain.png`](./figures/proof-chain.png) | Main proof-chain map (PNG) |
| [`figures/proof-chain.svg`](./figures/proof-chain.svg) | Same map (SVG) |
| [`figures/proof-chain.mmd`](./figures/proof-chain.mmd) | Mermaid source |
| [`figures/chain-status-card.png`](./figures/chain-status-card.png) | Chain status (node colors), not grades |

Regenerate:

```bash
python3 scripts/visual_journey/generate_proof_chain_figures.py
```

## Reused math visuals

Source PNGs live in [`../assets/lemma-campaign/`](../assets/lemma-campaign/) (math subset only).  
`python3 scripts/visual_journey/generate_proof_chain_figures.py` copies them into `assets/` beside the captions for a self-contained folder.

| Asset | Use in the journey |
| --- | --- |
| `lemma-star-barycenter.png` | Spectral barycenter map |
| `00-barycenter-map.png` | Same map, alternate crop |
| `fig_star_david_ring_lemma.png` | Triad / Ring Lemma geometry |
| `fig_three_spheres.png` | Nested shells → transfer |
| `t3_torus_shape_render.png` | \(\mathbb{T}^3\) atmosphere |
| `03-tug-of-war-stretch-vs-spread.png` | \(T_c\) vs \(D_s\) intuition |
| `02-shape-ne-size.png` | Amplitude cancels; shape remains |
| `amp_ratios_triad.png` | Triad amplitude ratios (K=0 diagnostic) |
| `06-viscosity-melts-wrapper.png` | Viscosity as outer wrapper |

Captions: [`CAPTIONS.md`](./CAPTIONS.md).

## Monday visual

Post first: **`figures/proof-chain.png`** — one composition, the whole chain, open estimates dashed and neutral.

## Tone

Craftsman. Superior notation. Quiet confidence. No biography framing, no scarlet-letter banners on open nodes.
