# Overlay — pieces, then one general shape, then refine

**Not a regularity proof.** A pretty stack is architecture. Silent-merge
of open layers is forbidden. CosmoEvolution is not this lab.

```bash
python -m domain_architect --overlay B
```

## Break it into parts and see each one

Each layer is a visual piece on its own chart: torus, shells, strain,
Hardy wall, angular viscosity, energy tank, cylinder Young, tube weld.

A piece can be **done in its piece** and still **not transposable** onto
the general Navier–Stokes shape. T3a is finished as a cylinder identity.
Transposing it onto \(\mathbb{T}^3\) is `CLIP-T3-OUTER`.

## Transpose only what is ready

Stack a layer when it is done **and** transposable:

```
         1/r²              angular identity
      ═ δ wall ═           Hardy
       λ+λ+λ=0             strain
         E_c               Ring
         σ|σ̄               cover
         E→X               Bernstein
         ∮=0               low flux
       [E]  ⊞ T^3          energy tank + domain
────────────────────────────────
      COMPOSITE architecture
```

That overlay is one general shape of **what is already proved as
identities**. It is not \(X\in L^\infty\). Holes punch through the stack:
`CLIP-T3-WELD`, `CLIP-B4b-ITUBE`, `CLIP-B3b-ALIGN`, occupation, B6, outer
vanishing.

Waiting beside the stack: T3b, T5, \(\Phi\)-cancel (refused, never stacked).

## Refine from there

Refinement is not a second, thicker overlay. It is filling **one hole**
(gap rule), then stacking that piece only if it becomes transposable.

First hole: **GAP-T3** between T3a and T5. Command:
`python -m domain_architect --gap B`.

Related: [`09-NS-GAP.md`](09-NS-GAP.md), [`11-NS-ENERGY-PLAY.md`](11-NS-ENERGY-PLAY.md).
