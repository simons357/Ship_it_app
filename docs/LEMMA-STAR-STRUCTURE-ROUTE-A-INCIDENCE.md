# Lemma★ — Route A: Hyp-ST★ incidence

Dated 10 September 2026. **Not a theorem. ★ is not
proved. NS is not solved.**

Structure route for the \(m^{1/2}\) heuristic’s
density, not a bound on \(\mathcal R_\star\).
Packets: [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).
Exact form: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).

Do not glue this to H1. Do not add \(K(t)\).
Do not cash a continuum exponent as a lattice
theorem.

---

## Status

**Win (CONDITIONAL).** Continuum incidence
\(I\ll m^{4/3}\) would give
\[
C(S)=O(m^{4/3}),
\]
which kills \(\Theta(m^2)\) density **in the
continuum model**.

**Still MISSING for lattice:** transfer
X1–X4/X6 (lattice↔continuum, rich circles,
slice uniformity, SSZ \(q\)).

Next push: lattice transfer / **Hyp-Lat★**.
That file is not written. Do not emit it
from this page.

---

## Object

Let \(S\) be a frequency support of size \(m\).
\(C(S)\) is the number of additive closures
used by the packet heuristic: triples with
\(p\in P\), \(q\in Q\), \(p+q\in R\),
\(|P|,|Q|,|R|\sim m\).

The heuristic needs \(\Theta(m^2)\) aligned
closures and an \(O(1)\) denominator to get
\(T_c\sim m^{1/2}\) and \(\mathcal R_\star\sim m\).

Route A asks a different question: can an
unstructured set even *have* \(\Theta(m^2)\)
closures?

---

## Continuum model (Hyp-ST★)

Embed the closures as point-line incidences
in the plane (Elekes shape): a point set and
a line set of size \(\sim m\), incidence count
\(I\). Szemerédi–Trotter gives
\[
I
\ll
m^{4/3}
\]
for ordinary Euclidean lines, up to the
linear terms \(|P|+|L|\).

**Hyp-ST★.** The closure graph of the
continuum packet model is an incidence
problem of that type, so \(I\ll m^{4/3}\).

**Conditional win.** If Hyp-ST★ sits, then
\(C(S)\lesssim I=O(m^{4/3})\). That is not
\(\Theta(m^2)\). The density the heuristic
assumed dies **in this model**.

This implication is the win. It is not
Szemerédi–Trotter applied to \(\mathbb Z^3\).
It is not a bound on \(\mathcal R_\star\).
Even \(O(m^{4/3})\) closures can add; the
denominator can still fail or sit.

---

## What this does not do

Freiman’s inverse already names the
structured exception: \(\Theta(m^2)\)
closures on a genuine additive set is an
AP (or AP-like). That family **already
ran**. Wide / narrow AP: \(\mathcal D_s\)
wins. Dead as a kill. Route A does not
redo Attack 9.

A lattice sphere is not an additive basis
of density \(\Theta(m^2)\). Attack 11:
landings \(O(m)\), not \(O(m^2)\). That is
a lattice number, not ST.

HH→L fans have pair counts 2–12, not
\(\Theta(m^2)\). Attack 12. Not ST.

---

## Lattice transfer — MISSING

\(\mathbb Z^3\) is not the Euclidean plane.
Spheres, circles, and slices can be rich.
The conditional win does not move until
these sit.

| id | Transfer | Status |
|---|---|---|
| X1 | Lattice \(\leftrightarrow\) continuum | **MISSING** |
| X2 | Closures are a Euclidean point-line incidence problem of size \(\sim m\) | **MISSING** |
| X3 | Rich circles (integer points on circles / shells) | **MISSING** |
| X4 | Slice uniformity (a rich plane does not restore \(\Theta(m^2)\)) | **MISSING** |
| X5 | Freiman inverse: \(\Theta(m^2)\Rightarrow\) AP-like | named; AP already scored; not ★ |
| X6 | SSZ \(q\) ( \(q\)-rich lines, \(\lesssim m^2/q^3+m/q\) ) on the lattice | **MISSING** |

X5 is not a transfer lemma. It is why the
designed \(\Theta(m^2)\) subset was Freiman-AP
and not a new object.

**Hyp-Lat★** is X1–X4/X6 as estimates, or a
proof that they fail. Not written.

---

## Enumerator

Lattice closure enumeration still runs on
this lane. Route A does not stop it.
A conditional continuum exponent is not a
substitute for counting landings on
\(\mathbb Z^3\).

Do not paste \(m^{4/3}\) onto Attack 11’s
288 landings and call it ST.

---

## Score

| Claim | Verdict |
|---|---|
| Hyp-ST★ \(\Rightarrow C(S)=O(m^{4/3})\) in the continuum model | **conditional win** |
| That kills \(\Theta(m^2)\) density in that model | **conditional win** |
| Lattice transfer X1–X4/X6 | **MISSING** |
| Hyp-ST★ proves Lemma★ | **fail** |
| Continuum ST is a theorem on \(\mathbb Z^3\) | **fail** |
| This is H1 | **fail** |

★ remains a uniform bound on
\(\mathcal R_\star\). Samples are evidence
only. NS not solved.

Next: Hyp-Lat★, or keep enumerating lattice
closures. Not a new leftover name. Not H1.
