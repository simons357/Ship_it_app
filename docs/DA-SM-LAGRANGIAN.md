# DA on the Standard Model Lagrangian

`python3 scripts/da_machine.py sm`

You put the expanded SM Lagrangian on the desk and said
start over. Forget the Cosmo 16. Play with an equation that
has both sides. DA did. The poster is **not** that
two-sided equation. It is a sum of terms.

\[
\mathcal{L}_{\mathrm{SM}}
=\mathcal{L}_{\mathrm{QCD}}+\mathcal{L}_{\mathrm{EW+H}}
+\mathcal{L}_{\psi A}+\mathcal{L}_{\mathrm{Yukawa}}
+\mathcal{L}_{\mathrm{ghost}}.
\]

Every coupling you care about is already **inside** those
terms as a coefficient. The Lagrangian **consumes**
\((g_s,g,g',v,\lambda,y_{ij},\mathrm{CKM})\). It does not
produce them. Hunting \(F\) in this expression is looking
on the wrong side of the map.

Tracks A, B, Q are untouched.

---

## The five blocks (one object each)

| Block | What it is | Consumes | Produce? |
|---|---|---|---|
| 1 QCD | \(SU(3)_c\) Yang–Mills, gluon cubic/quartic | \(g_s\) | no |
| 2 EW + Higgs | \(SU(2)_L\times U(1)_Y\), \(W,Z,A\), \(H\), Goldstones | \(g,g',v,\lambda\) | no |
| 3 fermion–gauge | quarks, leptons, \(W,Z,\gamma\), CKM | 3 families, CKM | no |
| 4 Yukawa | \(m = y v/\sqrt{2}\) | the \(y\)'s | no |
| 5 ghosts | Faddeev–Popov | gauge-fix | no (not a force) |

Each block **passes** as working QFT. That is a dynamics
pass, not a unifier pass. The masses in block 4 are written
in terms of Yukawas; they are not outputs of a topology.

---

## Real isomorphisms (keep)

| Iso | Verdict | Why it is real, and what it is not |
|---|---|---|
| \(SU(2)\cong\mathrm{Spin}(3)\cong Sp(1)\) | pass | Lie-group iso. No number. |
| \(U(1)\cong SO(2)\cong S^1\) | pass | Same. Does not output \(\alpha\). |
| Weinberg rotation \((Z,A)=R(\theta_W)(W^3,B)\) | pass | \(SO(2)\) on field space. \(\theta_W\) stays an input. |
| Goldstones \(\cong\) longitudinal \(W^\pm,Z\) | pass | Equivalence theorem. DOF, not a coupling. |

## Fake isomorphisms (fail)

| Claim | Why it dies |
|---|---|
| \(U(3)\times U(2)\times U(1)\) generator count = Cosmo 16 | A count is P1, not \(F\) |
| Gluon cubic \(=\) NS convection | Looks similar. Different PDE. No map onto \(\omega\cdot S\omega\) |
| Yukawa \(=\) Koide | Koide is not a term in \(\mathcal{L}_4\) |
| “Harmonic phenotype” of this Lagrangian | A nickname. Not a check |

---

## What is not on the poster

\(G_N\) and \(\Lambda\) are absent. Minimal SM also skips
neutrino masses. \(\theta_{\mathrm{QCD}}\) is usually
left off. So this equation **cannot** satisfy nature4:
one map to \((g_s,g_w,g_{\mathrm{em}},G_N)\) with \(\Lambda\)
in the sum. gauge3 already failed on SM running (the three
couplings miss).

---

## The realized two-sided equation

This is the equals sign that actually uses the poster:

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G\,T_{\mu\nu}[\mathrm{SM}].
\]

Same fact as an action:

\[
S=S_{\mathrm{EH}}[g]+\int\sqrt{-g}\,\mathcal{L}_{\mathrm{SM}}(g,\psi,A,H).
\]

Left: geometry. Right: stress-energy built from blocks 1–4
(Hilbert / Noether). That couple **already passed** as a
working pair in [`DA-GRAVITY-QUANTUM.md`](DA-GRAVITY-QUANTUM.md).
It is how the Standard Model sits in a universe model.

It does **not** output \(g_s\), \(\sin^2\theta_W\), \(G\), or
\(\Lambda\). working-couple \(\neq\) producing-map.
Collapse has not happened.

---

## What DA will not do with this

- Will not read \(F\) out of the coefficients.
- Will not glue this Lagrangian to Track B.
- Will not unshelve SFE / HB.
- Will not treat the Cosmo 16 as hidden inside \(SU(3)\times SU(2)\times U(1)\).

Breaking the five blocks into atoms, then putting them
back, is [`docs/DA-SM-BREAK.md`](DA-SM-BREAK.md).

Next: keep Einstein \(+T_{\mathrm{SM}}\). If you want a
producing-map, it has to live *outside* this Lagrangian —
the numbers already went in. Fluids stay on B.
