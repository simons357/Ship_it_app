# Leftover-split: SND, theory H, and the three NS failures

**Status:** a Domain Architect lab protocol, August 2026  
**Not a Navier–Stokes proof.** Each leftover stays **OPEN** after put-back.

This note records what happens when the usable Ring SND criterion and the
standing Q6 definition of \(H_N\) are decomposed in live DA, placed side by
side, and then run through a leftover-split reconstruction with the three
NS pieces that still fail.

Canonical product spec: [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md).  
Live software is still dump-era three-verb DA. This protocol does **not**
implement A13 (fail-closed inverse design). Synthesize of “prove swirl
regular” still emits a PD loop. That hole is unchanged.

## What we can use (not the “don’t use” list)

| Object | Usable equation | Don’t use |
|---|---|---|
| **SND** | Ring: \(\inf_t J(t)/X(t)\ge c_*>0\), \(X=\|\nabla u\|_{L^2}^2\), \(J\) dominant Littlewood–Paley shell of enstrophy | Paper2 operator-norm \(\|H_N[a]-\widehat H_N^\mu\|_{\mathrm{op}}<\delta_0\); `SND ≡ GNC ≡ Bridge` |
| **Theory H** | Q6 definition \(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\) | All-\(N\) floor \(\lambda_{\min}(H_N)>-1/2\); FRA coupling \(H\); Paper2 \(H_N[a]=\sum a_j B_j\); fluids “Theorem H” (not in this repo; C-GLUE-4) |

Lab strings (parser-safe):

```
J/X >= cstar
HN = D^((-1)/2)*Qtilde*D^((-1)/2)
```

## The three leftovers (what still fails)

Take only the parts that do not close. Leave what already stands.

| # | Book | Already works | Leftover (OPEN) | Lab string |
|---|---|---|---|---|
| 1 | B — swirl | \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\); \(\Gamma\) maximum principle | \(\int\|u^r/r\|_\infty\,dt\) not bounded by energy | `Istrain = urad/r` |
| 2 | Ring + SND | Ring lemma *if* SND | Energy does not give \(\inf J/X\ge c_*\) for large \(H^1\) data | `J/X >= cstar` |
| 3 | D — Paper2 | Lipschitz of \(a\mapsto H_N[a]\); Weyl *if* quantitative closeness | \(\|a-\mu\|_{\ell^1}\) not given by Leray energy; T2 Gronwall withdrawn | `ell1(a - mu) = 0` |

Same leftover *shape*: a coercive bound does not give the needed smallness.
**Not the same estimate.** Do not set \(\sigma_{\mathrm{swirl}}=\sigma_{\mathrm{ring}}=\sigma_{\mathrm{simplex}}=\sigma_H\).

## What live DA does with them

Decompose of each usable / leftover string returns `unclassified` at Level 0
plus a book warning. That is expected. Dump-era DA is not a fluids solver.

Translate **SND vs \(H_N\)** (and leftover vs leftover) returns:

- kind `analogy`
- mapping `{}` (no `J → HN`)
- broken: `no_checked_structure_map`, `different_books`, `no_executable_T`

That refusal **is** the clue, not a bug to paper over. A14 says not to
invent a letter map. The human observation that remains is a shared
*role*, not a shared formula.

## Clues about coexistence (not glue)

1. **Shared role.** Ring \(J/X\) and Q6 \(H_N\) are both concentration
   diagnostics: one is a fluids shell-mass ratio, the other is an
   arithmetic mixing matrix. They can sit in one protocol. They cannot
   sit in one operator.
2. **Shared leftover type.** Swirl strain, unconditional SND, and Paper2
   simplex are three carriers of “energy does not give smallness.”
3. **How they coexist.** Keep the coercive part of each book. Add an
   *independent* concentration hypothesis. Do not derive the diagnostic
   from energy. Do not multiply the diagnostics.
4. **What is not a clue.** Dump-era generic translate mapping `J → H` if
   glue is allowed. That is letter matching, not physics.

## The function (DA and NS)

Leftover-split is a use of `DECOMPOSE → TRANSLATE → SYNTHESIZE`. It is
also a method the NS books can cite.

```
Isolate leftover σ (smallness that energy E does not give)
        ↓
Decompose σ as its own system
        ↓
Name the missing role without naming a shared estimate
        ↓
Reconstruct:  E (keep) + σ (hypothesis)  ⇒  the rest of the estimates close
        ↓
Put that conditional theorem back into each original book
        ↓
Leave each σ OPEN
```

**Put-back (still OPEN):**

- Swirl: if \(\int\|u^r/r\|_\infty\,dt<\infty\) then continuation closes. Keep the identity.
- Ring: if \(\inf J/X\ge c_*\) then the conditional estimates run. Unconditional SND open.
- Paper2: if \(\|a-\mu\|_{\ell^1}\) is small enough then Weyl keeps the gap. Simplex lemma open.

This is how those papers are already honest when they are written as
conditional theorems. The function makes that split first-class so DA
does not try to glue the leftovers or to synthesize a PD loop as a
repair.

Run it:

```
python -m domain_architect cycle leftover-repair
python -m domain_architect translate --example snd-vs-h
```

In the desktop app: Decompose the Ring SND and Q6 \(H_N\) buttons,
Translate **SND vs H_N (lab, not glue)**, Cycle **NS leftover repair**.

## What this does not do

- It does not prove classical unaugmented Navier–Stokes.
- It does not make the three leftovers the same estimate.
- It does not revive the all-\(N\) floor, Goldbach, or `SND ≡ GNC ≡ Bridge`.
- It does not fix A13. Inverse design of NS regularity still emits a PD loop.
- It does not award `TRANSFORMABLE` or structure-preserving equivalence.
