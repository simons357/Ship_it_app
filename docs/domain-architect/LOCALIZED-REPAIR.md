# Localized reparation (surgery)

**Status:** a Domain Architect lab protocol, August 2026  
**Not a Navier–Stokes proof.** The graft stays **OPEN**.

If you have an **n-step** proof chain and **step k** is not working,
Domain Architect can **excise k**, keep the tissue on both sides of the
cut, search a finite catalog for the most logical hook, and **re-insert**
a graft at that slot. (e.g. k=2.) The graft is allowed to be an
independent hypothesis. It is not allowed to be
energy-implies-smallness, local-existence-bound-2, a PD loop, or a glue
of a different book.

This is leftover-split applied to a numbered chain. Jon’s metaphor is
the right one: you cut out the bad part and hook the good part to each
end. k is an index in the chain, not a product name. **`#2` was an
example index.** On the controlling classical chain, **#2 is Ring Lemma
and is already PROVED.**

Canonical product spec: [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md).  
Sibling protocol: [`LEFTOVER-REPAIR.md`](LEFTOVER-REPAIR.md).  
Classical chain: [`docs/papers/ns-snd/NS_UNAUGMENTED_PROOF_CHAIN.md`](../papers/ns-snd/NS_UNAUGMENTED_PROOF_CHAIN.md).  
Paper2 faces: [`docs/papers/ns-snd/FACES.md`](../papers/ns-snd/FACES.md).

Live software is still dump-era three-verb DA. This protocol does
**not** implement A13. Synthesize of “prove NS regular” still emits a
PD loop. That hole is unchanged.

## Operation: `excise k`

```
python -m domain_architect cycle localized-repair --excise K
```

POST `/api/localized-repair` with `{"excise": k}`.

In the desktop Cycle tab: enter a step number and **Excise this step**.

The repaired chain keeps its numbering. Slot k is the graft. Neighbors
stay in order.

## Default chain: classical unaugmented NS (controlling dataset)

This is the **controlling classical chain**. Controlling face: August
repaired TeX
[`Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`](../papers/ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex)
(Desktop pack name:
`06_navier_stokes_shelf/03_conditional_unaugmented_SND/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`).
Cross-check: [`NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md`](../papers/ns-snd/NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md).

This chain is **not** the June FIXED PDF compile.

Step 2 Ring Lemma (NS-6) is **not** Ring-book fluids
\(\inf J/X\ge c_*\) unless the source says so. Paper2 \(H_N[a]\) is not
Q6 \(H_N\).

| # | Step | Status | What surgery does |
|---|---|---|---|
| 1 | Leray–Hopf energy; \(a(t)\) on the simplex | healthy — STANDARD / INHERITED | keep |
| 2 | Ring Lemma (NS-6), standalone | healthy — **PROVED** | keep (already proved; not the default cut) |
| 3 | Lemma 3.1 Lipschitz of \(H_N[a]\) | healthy — PROVED | keep |
| 4 | Frozen gap / Route J, \(N\le 800\) | OPEN — NUMERICAL / UNDER AUDIT | keep unless you excise this k; no all-\(N\) |
| 5 | Weyl master implication | healthy — PROVED on SND+FG | keep |
| 6 | Conditional \(H^1\) (NS-7, NS-8) | healthy — PROVED on [SND] | keep |
| 7 | Lemma 6.1 simplex stability | OPEN leftover | **default cut**; re-insert as **hypothesis** |
| 8 | Dynamic SND (NS-10) | OPEN leftover | **default cut**; re-insert as **hypothesis** |
| 9 | Continuation to smooth Leray–Hopf | OPEN / INCOMPLETE | keep as still owed |

NS-11 / Clay Statement B is **not claimed**.

Default auto-excise is leftover **7 and 8**, not step 2, and not a
“diseased T2 closed” slot unless that false closure is still present
as a cut.

```
python -m domain_architect cycle localized-repair
```

Desktop: Cycle **Classical unaugmented (default cut 7–8)**.

Proximal tissue is step 6 (conditional \(H^1\)). Distal tissue is
step 9 (continuation). The hook that fits is Lemma 6.1 / dynamic SND
restated as an independent OPEN hypothesis.

Generic `excise=2` still works as **cut slot 2**. On this chain that
slot is Ring Lemma. Neighbors are step 1 and step 3. The accepted graft
is an independent ring-geometry hypothesis, still **OPEN**. That does
**not** prove Clay.

On the toy chain (`{"chain": "toy", "excise": 2}`), step 2 is
“energy implies smallness.” Neighbors are energy and continuation. The
graft is independent smallness \(\sigma\), still OPEN.

## Candidate search (finite, honest)

For the simplex / dynamic-SND interface Weyl needs
\(\|a-\mu\|_1\le\eta_*\) with audit figure \(\eta_*\approx 0.039\)
against \(\delta_0=0.20\):

| Candidate | Score | Re-insert? |
|---|---|---|
| Independent simplex hypothesis (Lemma 6.1, OPEN) | 1.0 | yes, as OPEN |
| Local existence bound 2 | 0 | no — \(2\) is \(\sim 51\times\) too large |
| Leray energy | 0 | no — boundedness \(\neq\) smallness |
| Dirichlet(\(1,\ldots,1\)) samples on \(\Delta_{N-1}\) | 0.15 | no — typical \(\|a-\mu\|_1\) is order 1 |
| Glue Ring \(\inf J/X\ge c_*\) | refused | no — different book |
| Glue withdrawn Q6 floor | refused | no — different \(H_N\) |
| Inverse-design PD loop | refused | no — A13 |

The Dirichlet samples are a bounded computation (400 draws, \(N=32\),
fixed seed). They show the leftover is not “what random \(a\) already
satisfy.” They are not a proof.

## What this does not do

- It does not prove Lemma 6.1.
- It does not prove dynamic SND (NS-10).
- It does not prove continuation (step 9).
- It does not prove classical 3D Navier–Stokes / Clay Statement B.
- It does not make the June FIXED PDF a compile of the August TeX.
- It does not identify NS-6 with Ring-book \(\inf J/X\).
- It does not fix A13.
- It does not award `TRANSFORMABLE`.

Run it:

```
python -m domain_architect cycle localized-repair
python -m domain_architect cycle localized-repair --excise K
```

In the desktop app: Cycle **Classical unaugmented (default cut 7–8)**,
or enter k and **Excise this step**.
