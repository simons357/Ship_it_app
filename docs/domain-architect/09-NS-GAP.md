# Stop at the wall — missing piece — candidates after

**Not a regularity proof.** Listing the next step is not walking it.

```bash
python -m domain_architect --gap B        # live tube wall (T3b)
python -m domain_architect --gap CHAIN    # lemma-list wall (B4b)
```

## The camera rule

When the walk hits an **open** step, it **stops**. Failures before that
are clipped hypotheses; those are not walls, and the walk continues past
them. Everything listed after the wall is a **candidate** (or a refused
bypass). A later identity that already “passes” (B5 after B4b, T4 after
T3b) is **parallel**, not continuation.

```
WALKED     T0 · T1 · T2 · T3a
              |
            WALL  T3b   STOP
              |
        ┌─ MISSING PIECE ─┐
        │ GAP-T3          │
        │ CLIP-T3-WELD    │  Hardy/Young traces ≠ I_off
        │ CLIP-T3-OUTER   │  T^3 has no R with Γ(R)=0
        └────────┬────────┘
                 |
        CANDIDATES AFTER (not walked)
           T5  needs the gap     first piece after
           T4  parallel          names δ, no weld
           T6  needs the gap
           T7  needs the gap
           spread Bony T         other chart
```

The missing piece sits **between** the last walked step and the first
candidate that would need the weld (`T3a` → `T5` on the tube write;
`B4` → `B5b` on the lemma list).

## What would fill GAP-T3

A lemma that bounds \(I_{\mathrm{off}}\) by Hardy/Young traces **on
\(\mathbb{T}^3\)**: the same fields (not \(\Gamma^2\) vs
\((\Gamma\partial_z\Gamma)\,\omega^r\)), and without an outer radius
where \(\Gamma\) vanishes.

Until that lemma exists, T5 is a candidate, not a step.

Even reflection across \(r=\delta\) can *look* like a fill of
`CLIP-T3-OUTER`. That is play: extra environment, not \(\mathbb{T}^3\).
It still does not fill `CLIP-T3-WELD`. See
[`10-NS-SHAPE-PLAY.md`](10-NS-SHAPE-PLAY.md).

## Refused bypasses (not candidates)

\(\Phi\)-cancel, BKM from \(L^2\), gluing Theorem H onto the tube, picking
the optimistic \(L^2\) scaling chart. Each already has a CLIP id.

Related: [`08-NS-TUBE-ESTIMATE.md`](08-NS-TUBE-ESTIMATE.md).
