# Gate 83 — reduce volumetric escape to a divisibility question

**27 September 2026.** Formulation lock, then the local ideal
computation on the 71E thickening. Ordinary NS is not solved.
DA-NS-2 stays **OPEN**. Unrestricted \(\sup\mathcal R_\star<\infty\)
stays **KILLED**. Soft X silent.

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local exact-shell ★ / 71E packets.

Machine: `scripts/da_gate_83_radical_trapping.py`.
JSON: `results/da_gate_83_radical_trapping.json`.
Desk card:
[`../../packets/DA-GATE-83-RADICAL-TRAPPING-2026-09-27.md`](../../packets/DA-GATE-83-RADICAL-TRAPPING-2026-09-27.md).
Planar point: [`GATE-71E-BRANCH-ELIMINATE.md`](GATE-71E-BRANCH-ELIMINATE.md).

---

## Gauge, volume, and \(\lambda\)

After gauge fixing the three generators of a \(2\times 2\times 2\)
additive cube,

\[
a=(1,0,0),\qquad
b=(b_1,b_2,0),\qquad
d=(d_1,d_2,\lambda),
\]

the parallelepiped volume is exactly

\[
V=\det[a,b,d]=b_2\lambda.
\]

Locally away from the planar degeneration of \(b\),

\[
b_2\neq 0
\qquad\Rightarrow\qquad
V=0\iff\lambda=0.
\]

So trapping volume is equivalent to trapping the single coordinate
\(\lambda\).

The seated 71E \(2\times 4\) patch is this cube with
\(d=2b\) (planar, \(\lambda=0\)):

\[
p_{ijk}=p_0+ia+j'b+k(2b),
\qquad
i,j',k\in\{0,1\}.
\]

That recovers the eight 71E modes. The nine cube collinearities
are the three space-diagonal constraints \(C_1,C_2,C_3\) and the
six face-diagonal constraints \(F_1,\dots,F_6\). They sit among
the eleven 71E equations. At the certified point they vanish and
every pair is live.

The laboratory thickening used for the computation is the normal
lift of that cube,

\[
d=2b+\lambda n,
\qquad
n=a\times b,
\]

with \(a,b,p_0\) frozen at the 71E lattice and the eight
projective polarizations free. This is the reduced slice through
\(\mathfrak p_{71E}\). It does **not** vary the in-plane lattice
moduli \((b_1,b_2,d_1,d_2)\).

---

## The question (locked before the compute)

Let \(I_{\mathrm{act}}=(C_1,C_2,C_3,F_1,\dots,F_6)\) be the nine
coherence equations, localized away from interaction death
(\(W\neq 0\) on every cube pair-class). Let
\(\mathfrak p_{71E}\) be the maximal ideal of the known planar
active point. The clean question is

\[
\lambda\in\sqrt{(I_{\mathrm{act}})_{\mathfrak p_{71E}}}\,?
\tag{83.34}
\]

If yes, every reduced algebraic branch through that component
satisfies \(\lambda=0\), so the 71E escape is algebraically
trapped in the plane. This is the Nullstellensatz relationship
between radical membership and the local zero set.

A certificate is an explicit integer \(N\) and a local
denominator \(h\), with \(h(\mathfrak p_{71E})\neq 0\), such that

\[
h\,\lambda^N
=
A_1C_1+A_2C_2+A_3C_3
+
B_1F_1+\cdots+B_6F_6.
\tag{83.35}
\]

On every coherent active solution with \(h\neq 0\),
\(\lambda^N=0\), hence \(\lambda=0\), hence \(V=0\).

Hierarchy, locked:

| Test | What it answers |
|---|---|
| Jacobian at \(\mathfrak p_{71E}\) | whether \(\lambda\) is absent from the tangent space |
| Formal series in \(\lambda\) | whether \(\lambda\) can appear at some higher order |
| Radical certificate (83.35) | both, on the reduced local variety |

Do not spend a ladder of orders \(1,2,3,4\) if the local radical
computation is feasible. The Jacobian remains a cheap filter:
a volumetric tangent already kills (83.34).

---

## What a yes or a no would mean

**Yes (trapped).** Every reduced branch through the 71E point is
planar. That is a compact, checkable obstruction to *this*
volumetric escape. It does **not** prove that every active
coherent cube is planar. A detached volumetric component could
still exist.

**No (escape).** There is a volumetric branch attached to 71E.
That branch becomes the next adversary.

**Inconclusive.** No certificate and no explicit escape. (83.34)
stays OPEN.

Gate 81’s census of detached cubes remains relevant in every
case. On this tree that census is **REPORTED** from the handoff
(40/40 tested volumetric cubes Outcome A) and is **not**
recomputed here.

---

## Board

\[
\begin{array}{lll}
71E &:& \text{planar active coherence exists},\\
81 &:& \text{40/40 tested volumetric cubes are A (REPORTED)},\\
83 &:& \lambda\in\sqrt{(I_{\mathrm{act}})_{\mathfrak p_{71E}}}\ ?\\
\end{array}
\]

The numerical/symbolic outcome of the reduced-slice computation
is recorded in the JSON and restated at the end of this page
after the run. The formulation (83.34)–(83.35) is the lock.
It does not, by itself, close (83.34).

**NS not solved.**
