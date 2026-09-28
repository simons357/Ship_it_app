# Gate 83D — the hinge

**28 September 2026.** Explanation lock. No new witness.
Ordinary NS is not solved. DA-NS-2 stays **OPEN**.
Unrestricted \(\sup\mathcal R_\star<\infty\) stays **KILLED**.
Soft X silent.

Witness and machine stay on
[`GATE-83B2B-CURVATURE.md`](GATE-83B2B-CURVATURE.md).
This page does not search \(z_7\), does not scan \(z_1,\ldots,z_6\),
and does not enlarge the cocircular family.

Does **not** alter locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local exact-shell ★ / 71E packets.
Does **not** close (83.34).

---

## Three questions that got stacked

After the rank-8 trap died, three distinct questions were sitting
in one sentence.

| | Question | Status |
|---|---|---|
| (A) | Can \(A=D_zF\) drop rank on a real, active, volumetric cube? | **Yes.** One 13/10 witness. |
| (B) | If the extra kernel is a coordinate \(e_{z_i}\), does that rank drop give a branch? | **Yes, automatically.** This is the hinge. |
| (C) | Is there a volumetric *lattice* branch through 71E? | **Open.** That is (83.34). |

(A) is a point. (B) is a theorem about the shape of \(F\).
(C) is an ideal-membership question in the lattice coordinate
\(\lambda\). More cocircular points answer (A) again. They do
not move (B) or (C).

---

## The hinge

Each raw cube generator is a triple

\[
K\cdot(W_1\times W_2).
\]

Each \(W\) is bilinear in the two polarizations it sees, and
affine in each of those polarizations. No pair-class uses the
same node twice. Therefore, on **every** cube, not just the
13/10 witness,

\[
\deg_{z_i}F\le 1,
\qquad
\partial_{z_i}^2 F\equiv 0.
\tag{83.40}
\]

That is the hinge. It collapses the Lyapunov–Schmidt tower in
any pure polarization direction.

Write \(v=e_{z_i}\) and expand \(F(x_0+sv+\cdots)\). The
quadratic pairing is

\[
\ell^T D^2F[v,v]
=
\ell^T\partial_{z_i}^2 F
=
0
\]

identically, for every left kernel vector, at every point, on
every lattice. The cheap curvature test can never obstruct a
pure \(z_i\) kernel. There is no cubic term in \(s^3\partial_{z_i}^3 F\)
either.

The first-order column \(\partial_{z_i}F\) is itself independent
of \(z_i\). So the whole story is first order:

\[
\boxed{
F(x_0)=0
\;\text{and}\;
\partial_{z_i}F(x_0)=0
\;\Longleftrightarrow\;
F(x_0+s\,e_{z_i})=0
\text{ for all }s.
}
\tag{83.41}
\]

Activity is the only remaining filter: the line is a coherent
family only where every pair stays live. On the locked witness
that holds for all real \(s\) (the four pairs that see \(p_{100}\)
keep a constant \(\min|W|\)).

In one line:

\[
\boxed{
\text{for a polarization kernel, rank drop }\Rightarrow\text{ branch.}
}
\tag{83.42}
\]

That implication is a theorem about \(F\), not a property of the
circle. The 13/10 locus supplied one place where a column
actually vanishes and the pairs stay live. It was not needed
to make (83.40) true, and a second such place would not make
(83.42) truer.

---

## What the hinge does *not* say

Affinity is in **one** \(z_i\) at a time. Mixed directions still
have curvature.

- A kernel vector with two \(z\)-components has a cross term
  \(\partial_{z_i}\partial_{z_j}F\). That pairing can be nonzero.
- A kernel vector with a lattice component (\(\lambda\), \(b\),
  \(d\), \(r\)) is outside (83.40). The 71E cotangent computation
  already sits here: \(A\cdot\partial_\lambda R\neq 0\) at
  \(z^\star\), so \(\lambda\) is not a first-order kernel at 71E
  and (83.41) never fires in that direction.
- Scale-free (normalized \(W\)) residuals are **not** affine.
  The exact system is the raw triples. Do not mix charts.

So (83.42) is not “every rank drop is a branch.” It is “a rank
drop *along a coordinate polarization* is a branch.”

---

## Why another witness is the wrong next move

The global rank-8 trap claimed that an active cube has
\(\mathrm{rank}\,A=8\) (full in the eight \(z\)-directions, up
to the expected residual). One real, active, volumetric line
kills that as a global statement. A second line, a \(z_7\)
column, or the rest of \(z_1,\ldots,z_6\), is the same hinge
applied to a different index.

Those loci may be worth a later census. They are not the
shortest path through the present fork. The fork is already
decided:

\[
\begin{array}{lll}
\text{rank-8 trap} && \text{dead, by (A)+(83.42)}\\
\text{polarization line} && \text{exists, detached}\\
\text{71E lattice escape} && \text{(83.34), still OPEN}\\
\end{array}
\]

(83.34) asks whether \(\lambda\) lies in the radical of
\(I_{\mathrm{act}}\) localized at the planar 71E point. That is
a question about the *lattice* coordinate on the 71E thickening.
The 13/10 cube is not on that thickening. Hunting more detached
circles cannot put \(\lambda\) into that radical, and cannot
take it out.

---

## Board

```
GATE 83D
──────────────────────────────────────────
hinge                    (83.40)–(83.42)
F affine in each z_i     YES, every cube
pure-z curvature         IDENTICALLY ZERO
rank drop in e_{z_i}     ⇒ EXACT LINE
mixed / lattice kernels  NOT COVERED
new witness              NOT REQUIRED
z7 / z1..z6 census       DEFERRED
(83.34)                  OPEN
GLOBAL RANK-8 TRAP       DEAD
71E LATTICE ESCAPE       OPEN
```

\[
\boxed{\text{HINGE: POLARIZATION RANK DROP }\Rightarrow\text{ BRANCH}}
\]

\[
\boxed{\text{71E LATTICE ESCAPE: NOT YET ESTABLISHED}}
\]

Do not spend a Gröbner run on integrating a \(z_i\) kernel.
Do not spend a search on a second cocircular column. The next
object that can change the board is a lattice direction, not
another polarization.

---

## 28 September 2026 — Heavy’s exact derivation (DA gated)

Heavy proved 83D as an **internal derivation**, exact, no
factors removed. Reduced modulo the three radius conditions
and \(\mathcal G\), the hinge-mode column is identically zero
in all 12 equations. Each equation that sees the hinge mode
factors as

\[
-r_3^3\,L^2\,(R_{111}-R_i),
\]

with \(L\) a pair-activity factor. Saturation removes only
\(r_3=0\) and six of those activity factors. There is no new
geometry.

The fifth-radius condition is redundant. On this tree that
is a generic identity, not a specimen check:

\[
R_{111}-R_{000}
=
(R_{100}-R_{000})
+(R_{010}-R_{000})
+(R_{001}-R_{000})
+2\mathcal G,
\]

\[
\mathcal G
=
a_h\cdot b_h+a_h\cdot d_h+b_h\cdot d_h
=
b_1+d_1+b_1 d_1+b_2 d_2
\]

in the seated \(\lambda\)-chart \(a_h=(1,0)\). So three
radius differences plus \(\mathcal G=0\) already force the
fifth equal radius.

This tree did **not** re-run Heavy’s 12-equation saturation.
It gates that derivation as PROVED / REPORTED, proves the
redundancy identity, and files the √113 specimen Heavy did
not have.

Spec: [`../../results/da_gate_83d_sqrt113_spec.json`](../../results/da_gate_83d_sqrt113_spec.json).
Desk card:
[`../../packets/DA-GATE-83D-SQRT113-SPEC-2026-09-28.md`](../../packets/DA-GATE-83D-SQRT113-SPEC-2026-09-28.md).

On the seated \(I_{\mathrm{act}}\) Jacobian the vanishing
column of that specimen is \(z_4=p_{100}\), not seated
\(z_7=p_{111}\). Heavy should match the hinge index against
the seated / binary dictionary in the spec. Instantiating
the specimen is not a new witness hunt.

```
GATE 83D + HEAVY
──────────────────────────────────────────
hinge                    (83.40)–(83.42) ✓
Heavy column identity    PROVED / REPORTED
factorization            -r3³ L² (R111-Ri)
saturation               r3=0 and activity only
fifth radius             REDUNDANT (proved here)
√113 spec                FILED
new witness              NOT REQUIRED
(83.34)                  OPEN
```

**NS not solved.**
