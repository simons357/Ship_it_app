# SoT — H1 on one cylinder

Dated 10 September 2026. **Not a regularity theorem.
H1 is not proved. NS is not solved.**

Packet attacks on \(\mathcal R_\star\): negatives, written
([`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md)).
H1: opened here.

Two writings of leftover (6). Different integrals.
Do not merge them.

1. Bad-pair \(A_{\mathrm{bad}}\) on \(Q_r\):
   [`H1-OBJECT.md`](H1-OBJECT.md), [`WRITE_6.md`](WRITE_6.md).
   Aimed leftover yes. Theorem no.
2. Tube stretching on one cylinder (this page).
   Same leftover class. Localized Lemma★ packaging.
   Still not a theorem.

Do not glue H1 to the GCD matrix \(H_N\) / \(H_M[a]\).
Do not quote the Ring Lemma direction bound as proved.
Do not treat one computed Beltrami tube as a uniform
constant.

Probe: `python3 scripts/h1_one_cylinder.py`

---

## Why switch

Packet falsifiers for \(\mathcal R_\star\) are exhausted
as lattice objects: isolated triad, wide/narrow AP,
fixed-gap spheres, Freiman-designed subset, HH→L fan.
The \(m^{1/2}\) heuristic has no home on \(\mathbb Z^3\).
The leftover is the same trilinear stretching, now
written in physical space on one vortex tube.

---

## Object

Let \(\xi=\omega/|\omega|\) on \(E_c=\{|\omega|\ge c\}\).
A space-time cylinder \(Q\) is a region in which \(E_c\)
looks like a tube of length \(L\) and radius \(\rho\),
over a waiting time \(\tau\).

H1 (candidate, one cylinder):

\[
\int_Q|\omega\cdot\nabla u\cdot\xi|\,dx\,dt
\le
C(\text{thinness})\times(J\text{ on folds})\times(\text{waiting}).
\]

More precisely, the stretching that Lemma★ packaged as
\(T_c\) is, on one tube,

\[
\omega\cdot S\omega
=
|\omega|^2(\xi\cdot\nabla u\cdot\xi)
=
|\omega|^2\partial_s u_\parallel.
\]

Constantin–Fefferman depletion says this is small when
\(\xi\) is Lipschitz. The ledger Ring Lemma claimed

\[
\|\nabla\xi\|_{L^\infty(E_c)}\le C\,2^{j^*}
\]

on a single LP shell. That claim is **REPAIR**: it
assumes the direction bound it wants. B3 on CONC packets
is a number on those packets, not this lemma.
H1 is the restriction of that claim to one cylinder, so
the constants can depend on \((\rho,L,\tau)\) and must be
**checked, not assumed**.

---

## Three pieces that have to be estimates, not names

**1. Thinness.** If \(\rho/L\to 0\), the tube is 1-D and
stretching is along one direction. Need

\[
\rho^2\int|\omega|^2
\lesssim
\text{energy captured by the tube}
\]

from Biot–Savart, not from a picture.
Do not cash “assume thin” as this (that is Lemma C).
CS-summable volume thinness is still \(E^{3/2}\), not H1
([`H1-SHAPES.md`](H1-SHAPES.md)).

**2. J on folds.** Folds of \(\xi\) produce new stretching.
The integral that must stay bounded is the CF dissipation
identity

\[
J(Q)=\int_Q|\nabla\xi|^2|\omega|\,dx\,dt.
\]

If \(J\) stays \(O(1)\) on the cylinder, depletion holds
there. If \(J\) blows like the enstrophy, H1 fails on
that tube. Do not cash Lemma J on generic fields as this.

**3. Waiting time.** Viscosity needs time \(\sim\rho^2/\nu\)
to eat the tube. If \(\tau\ll\rho^2/\nu\) the cylinder is
inviscid and H1 cannot use dissipation. The estimate must
either (a) take \(\tau\) long enough, or (b) close without
viscosity — which is the same geometric bound as
\(\mathcal R_\star\). Do not cash an imposed waiting time
as this.

---

## What would close H1

A bound

\[
\int_0^\tau\|(\xi\cdot\nabla u\cdot\xi)_+\|_{L^\infty(\mathrm{tube})}\,dt
\le
C(\rho,L)
\]

independent of how large \(|\omega|\) is inside the tube.
That is BKM on one cylinder. It is not weaker than
Lemma★; it is Lemma★ localized. A numerical tube with
large \(J\) or short waiting is a **kill of this
packaging**, not of NS.

---

## First computation (filed)

Object: \(J\) and thinness on one explicit tube
(ABC / strained vortex), then whether \(J\) stays
bounded as amplitude grows. Snapshot integrals. Waiting
is not scored on a snapshot.

ABC: \(J\sim A\), stretch rate \(\sim A\). BKM on
that field fails. \(J/X\sim 1/A\): folds do not blow
like enstrophy. Burgers: \(J=0\), stretch \(=\gamma\)
imposed, waiting locked. Gaussian pair: thinness
\(\rho^2\int|\omega|^2\lesssim E_{\mathrm{core}}\) from
Biot–Savart; self-stretch \(=0\).

One computed tube is not \(C_0\). Burgers strain is
imposed, not Biot–Savart of the tube. ABC is not a
thin cylinder.

Scores: [`H1-TUBE.md`](H1-TUBE.md).

---

## Status

Packet attacks on \(\mathcal R_\star\): negatives, written.
H1: opened. Uniform triadic bound still open.
NS not solved.
