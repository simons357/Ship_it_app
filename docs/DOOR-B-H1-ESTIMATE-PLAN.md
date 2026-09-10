# Door B — H1 estimate plan

Dated 10 September 2026. **OPEN. Not a GR close.
H1 is not proved. NS is not solved.**

This is an ordered program for estimates, plus
the bar that would make the *package*
estimate-complete. Estimate-complete is still
not geometric regularity and not Navier–Stokes.

SoT: [`H1-SOT.md`](H1-SOT.md).
Object: [`H1-OBJECT.md`](H1-OBJECT.md).
First numbers: [`H1-TUBE.md`](H1-TUBE.md).
\(L^\infty\) sketch: [`DOOR-B-H1-B5-LINFTY-SKETCH.md`](DOOR-B-H1-B5-LINFTY-SKETCH.md).

Do not glue H1 to Lemma★, to \(H_N\), or to
the Ring Lemma. Do not add \(K(t)\) to the PDE.
Do not treat one Beltrami tube as \(C_0\).

---

## Status locks (10 September)

- H1 estimate package: **OPEN**. Not a GR close.
- Outside-\(\mathcal{E}\) identity: **blocked**.
  No candidate yet. Do not invent one.
- Lattice closure enumerator: still running on
  the ★ lane. Separate integral. Do not merge.
  Do not stop that lane from this file.

---

## What this door is

Door B = unaugmented NSE, leftover WRITE (6).
Two writings, different integrals:

1. Bad-pair \(A_{\mathrm{bad}}\) on \(Q_r\).
2. Tube stretching on one cylinder.

This plan is for (2), with (1) kept labeled.
It is not Track B lemma B5 (angular
\(1/r^2\)). That B5 already scored: identity
pass, domination fail.

---

## Ordered program

**P0. Split.** Keep \(A_{\mathrm{bad}}\), tube
H1, and \(\mathcal R_\star\) as three writings.
A number on one is not a bound on the others.

**P1. Thinness.** From Biot–Savart, not a
picture:

\[
\rho^2\int|\omega|^2
\lesssim
\text{energy captured by the tube}.
\]

**Lemma P1 sits** on the low-pass class
(\(\widehat{\omega}(k)=0\) for \(|k|>K\le C/\rho\)):
\(\rho^2\int|\omega|^2\le C^2\int|u|^2\).
File: [`H1-P1.md`](H1-P1.md). A Gaussian
pair was a sample, not the estimate.
NSE membership is open. Localized tube
energy (cutoff) is not written.
CS-summable volume thinness is still
\(E^{3/2}\), not H1.

**P2. J on folds.**

\[
J(Q)=\int_Q|\nabla\xi|^2|\omega|\,dx\,dt
\]

must stay \(O(1)\) on the cylinder, or be
paid by dissipation, not blow like
enstrophy. ABC: \(J\sim A\), \(J/X\sim 1/A\).
Folds do not blow like \(X\). \(J\) is not
bounded independently of amplitude. Burgers
\(J=0\) by exact alignment — do not cash.

**P3. Waiting.** Viscosity needs
\(\tau\sim\rho^2/\nu\). If \(\tau\) is
shorter, the cylinder is inviscid and the
bound is the same geometric leftover as
\(\mathcal R_\star\). Do not cash an imposed
waiting time. Burgers locks \(\rho^2/\nu=4\)
to imposed strain — not derived.

**P4. BKM on one cylinder.** The sketch:

\[
\int_0^\tau\|(\xi\cdot\nabla u\cdot\xi)_+\|_{L^\infty(\mathrm{tube})}\,dt
\le
C(\rho,L),
\]

independent of how large \(|\omega|\) is.
Every unjustified arrow is **MISSING** in
[`DOOR-B-H1-B5-LINFTY-SKETCH.md`](DOOR-B-H1-B5-LINFTY-SKETCH.md).
ABC already kills the packaging on that
field (stretch \(\sim A\)).

**P5. After P4, still not GR.** Cover of
\(E_c\) by cylinders. H2 from energy. H3.
\(R_\phi\). Local Serrin then, not CKN.
If H1 sits and H2-from-energy does not, the
cylinder is still open.

**P6. Refuse.** Ring Lemma as proved. One
computed tube as \(C(\rho,L)\). Glue to
\(H_N\). Glue to ★. Add \(K(t)\). BKM from
\(L^2\). Outside-\(\mathcal{E}\) invented.
Cash this file as geometric regularity.

---

## Honest estimate-complete bar

The package is **estimate-complete** only if
every box is an estimate, not a name.
Estimate-complete \(\neq\) GR close
\(\neq\) NS solved.

| Box | Estimate? | Now |
|---|---|---|
| P1 thinness on the low-pass class, from Biot–Savart | **yes** | [`H1-P1.md`](H1-P1.md) |
| P1 membership: NSE puts Bad on that class | no | high-pass is a counterexample |
| P2 \(J=O(1)\) independent of \(\lvert\omega\rvert\), or paid | no | ABC: \(J\sim A\) |
| P3 waiting derived, or viscosity-free geometric bound | no | snapshot; Burgers locked |
| P4 every MISSING in the B5 sketch filled | no | sketch only |
| P5 cover + H2-from-energy + H3 + \(R_\phi\) | no | labeled, open |
| Outside-\(\mathcal{E}\) identity | blocked | no candidate |
| Uniform triadic bound on \(\mathcal R_\star\) | open | enumerator still on ★ |

One box sits (P1 on a stated class). NSE-class
boxes do not. The package is not
estimate-complete. That is not a close.

---

## First computation (does not move the bar)

[`H1-TUBE.md`](H1-TUBE.md). ABC stretch tracks
amplitude. Burgers is imposed strain. Pair
thinness is Biot–Savart as a number.
A kill of packaging is not a kill of NS.

---

## Next

P1-lowpass sits. Next is still one hole
as an estimate: P1 membership, or P2, or
P3, or one MISSING in the B5 sketch.
Do not write a new leftover name.
Do not cash Lemma P1 as WRITE (6).
Do not wait for the ★ enumerator to finish
before writing H1, and do not merge the
lanes when it does.

NS not solved.
