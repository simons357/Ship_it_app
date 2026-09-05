# Unaugmented NS — chain and what closes it

5 September 2026. Classical NSE. Keep \(1/r^4\).
No \(Q_1\). Object \(X=\|\omega\|_2^2\).

This is the chain that was asked for, plus
exactly what must sit to close. It is not QED.
`check B` stays open until WRITE (6) sits.

Machine write-up: [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md).
Open chain PDF: [`TRACK-B-CHAIN.pdf`](TRACK-B-CHAIN.pdf).
Residual holes: [`TRACK-B-RESIDUAL.md`](TRACK-B-RESIDUAL.md).
From this desk: [`DA-FROM.md`](DA-FROM.md).

---

## Aimed theorem

A smooth solution of three-dimensional incompressible
Navier–Stokes (periodic or whole space), viscosity
\(\nu>0\), no \(Q_1\), Biot–Savart kept at \(1/r^4\),
stays smooth for all time: \(X\) stays finite on every
\([0,T]\).

---

## Have

**(1) Energy.** Leray: \(\int_0^T X<\infty\) on these
packets, energy inequality.

**(2) Enstrophy identity.**

\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
=-\int\omega\cdot S\omega
\]

up to lower-order terms already controlled.

**(3) Leftover form.**

\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
\le\varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\cdot\mathcal{R}(t).
\]

The only term that can beat viscosity is the
stretching leftover.

**(4) Split.**

\[
\int\omega\cdot S\omega
=\text{hole 1 (aligned }P_+\text{ on }E_c)
+\text{hole 2 (unaligned }P_+\text{ on }E_c)
+\text{hole 3 (off }E_c).
\]

Scored as B37 on the \(n=32\) box. Naming the holes
is not the estimate.

**(5) Named blanks.** A1 = alignment in time for all
data (hole 1). A2 = \(\int\|\lambda_2^+\|\) for all data
(live cubic; Miller cut B38). On this box A1 is off.
A2 is live and did not blow on the B15 path. The box
is not all data.

---

## Write — this is what closes

**(6)** Provide **one** of these, for **all data**,
on the **classical** equation:

1. \(\displaystyle\int_0^T\mathcal{R}(t)\,dt<\infty\),
   with \(\mathcal{R}\) the residual in (3), or
2. **all-data A1** — alignment in time, or
3. **all-data A2** — \(\displaystyle\int_0^T\|\lambda_2^+\|_{L^q}\,dt<\infty\)
   for a \(q\) that feeds (3), or
4. a field that **kills** the stretching leftover,
   so the cubic does not beat viscosity.

Then **(7) Gronwall** (\(X\) stays finite),
**(8) Beale–Kato–Majda** (continuation; \(L^2\) is
not \(\|\omega\|_\infty\)), **(9) bootstrap** to
smoothness on arbitrary \(T\) **follow**. You do
not write (7)–(9) as new ideas. They wait on (6).

If (6) sits, the theorem sits. If it does not,
B stays open.

---

## Exactly what to provide

A proof that one of (1)–(4) under WRITE (6) holds
for every finite-energy / \(H^1\) divergence-free
initial datum, viscosity \(\nu>0\), no extra stress,
Biot–Savart kept at \(1/r^4\).

The estimate must be an a priori bound, not a
reading on \(n=32\), not an identity, not a named
hole, not Theorem A.

---

## What does not close it

- Theorem A / \(Q_1\) / \(\varepsilon>0\)
- \(\Phi\)-cancel
- Exporting A onto B
- The B-chain PDF
- Living walls L55–L76
- Miller identity without the integral
- “A2 did not blow on B15”
- Route C, Q, SND, SFE
- DA or this chat emitting a last line

---

## Status

- (1)–(5): done
- (6): not done
- (7)–(9): waiting on (6)
