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
end. k is an index in the chain, not a product name.

Canonical product spec: [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md).  
Sibling protocol: [`LEFTOVER-REPAIR.md`](LEFTOVER-REPAIR.md).  
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

## Default chain: Paper2 (example dataset)

Paper2 is the example **dataset**, not the operation. The filename
`Paper2_NS_Regularity_SND_FIXED.tex` was requested. The **PDF** is
filed. The **TeX source did not arrive**. Surgery uses:

- June FIXED PDF [`Paper2_NS_Regularity_SND_FIXED.pdf`](../papers/ns-snd/Paper2_NS_Regularity_SND_FIXED.pdf)
- August 1 audit [`NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md`](../papers/ns-snd/NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md)

Do not invent the missing TeX. Do not treat the August repaired TeX as
a compile of that PDF.

| # | Step | Status | What surgery does |
|---|---|---|---|
| 1 | Leray–Hopf setup; \(a(t)\) on the simplex | healthy | keep |
| 2 | Frozen gap / Route J (Hypothesis 2.1) | OPEN / numerical | keep unless you excise this k |
| 3 | Lemma 3.1 Lipschitz of \(H_N[a]=\sum a_j B_j\) | healthy | keep |
| 4 | Theorem 4.1 conditional Weyl | healthy | keep |
| 5 | Product \(C_N\|a-\mu\|_1<\delta_0\) | healthy as an implication | keep; \(\delta_0=0.20\) is manuscript safety, not all-\(N\) |
| 6 | Lemma 6.1 uniform simplex / SND stability | OPEN (the kink) | cut and re-insert as **hypothesis** |
| 7 | Local existence \(\|a-\mu\|_1\le 2\) used as the 0.039 bound | diseased | cut; do not re-insert |
| 8 | §7 “T2 Closed” Gronwall | diseased | cut; do not re-insert |
| 9 | Continuation from spectral gap to Leray–Hopf smoothness | OPEN | keep as still owed |
| 10 | Classical 3D NS regularity | not claimed | not claimed |

**Paper2 surgery** is a different named protocol: the default cut of the
known diseased/open dynamical kink (6–8). It is not “excise step 2.”

```
python -m domain_architect cycle localized-repair
```

Desktop: Cycle **Paper2 surgery (default cut 6–8)**.

Proximal tissue is step 5 (the Lipschitz target). Distal tissue is
step 9 (continuation). The hook that actually fits the interface is
Lemma 6.1 restated as an independent hypothesis.

Frozen gap at k=2 is one example of a failing step on this chain.
Neighbors are the Leray setup (1) and Lemma 3.1 (3). The accepted graft
is an independent frozen-gap hypothesis, still **OPEN**. Route J
numerics \(N\le 800\) are a diagnostic, not a theorem. The withdrawn Q6
floor is refused.

On the toy chain (`{"chain": "toy", "excise": 2}`), step 2 is
“energy implies smallness.” Neighbors are energy and continuation. The
graft is independent smallness \(\sigma\), still OPEN.

## Candidate search (finite, honest)

For the Paper2 simplex interface Weyl needs \(\|a-\mu\|_1\le\eta_*\)
with audit figure \(\eta_*\approx 0.039\) against \(\delta_0=0.20\):

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
- It does not prove continuation (step 9).
- It does not prove classical 3D Navier–Stokes.
- It does not make the June FIXED PDF a compile of the August TeX.
- It does not fix A13.
- It does not award `TRANSFORMABLE`.

Run it:

```
python -m domain_architect cycle localized-repair
python -m domain_architect cycle localized-repair --excise K
```

In the desktop app: Cycle **Paper2 surgery (default cut 6–8)**, or enter
k and **Excise this step**.
