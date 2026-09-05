# Proof chain — 3D Navier–Stokes

Aimed at global regularity. Classical equation.
Keep \(1/r^4\). No \(Q_1\).

Say to DA: `python3 scripts/da_machine.py proof`  
or: `next --ask "write me the proof chain for Navier-Stokes"`

---

## Theorem (aimed)

Let \(u\) be a smooth solution of three-dimensional
incompressible Navier–Stokes (periodic or whole space),
viscosity \(\nu>0\), no \(Q_1\), keep \(1/r^4\).
Let \(X=\|\omega\|_2^2\). Then \(X\) stays finite on
\([0,T]\) for arbitrary \(T\), and \(u\) remains smooth.

---

## Proof

**(1)** **Energy.** Leray: \(\int_0^T X(t)\,dt<\infty\)
on these packets, and the energy inequality holds.
*[have]*

**(2)** **Enstrophy identity.** Differentiating \(X\)
along the NSE gives

\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
=-\int\omega\cdot S\omega
\]

up to lower-order terms already controlled.
*[have]*

**(3)** **Leftover form.** Absorb a slice of dissipation:

\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
\le\varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\cdot\mathcal{R}(t).
\]

The only term that can beat viscosity is the stretching
leftover.
*[have]*

**(4)** **Split.**

\[
\int\omega\cdot S\omega
=\underbrace{\text{hole 1}}_{\text{aligned }P_+\text{ on }E_c}
+\underbrace{\text{hole 2}}_{\text{unaligned }P_+\text{ on }E_c}
+\underbrace{\text{hole 3}}_{\text{off }E_c}.
\]

Scored on the \(n=32\) box as B37.
*[have]*

**(5)** **Named blanks.** A1 = alignment in time for all
data (hole 1). A2 = \(\int\|\lambda_2^+\|\) for all data
(live cubic; Miller cut B38). On this box A1 is off and
A2 is live and did not blow on the B15 path (B40, B41).
*[have]*

**(6)** **Write.** One all-data integrable residual:
\(\int_0^T\mathcal{R}(t)\,dt<\infty\), or all-data A1,
or all-data A2, or a field that kills the stretching
leftover.
*[the next write]*

**(7)** **Gronwall.** From (3) and (6), \(X(t)\) stays
finite on \([0,T]\).
*[follows from (6)]*

**(8)** **Continuation.** Beale–Kato–Majda: if
\(\int_0^T\|\omega\|_\infty\,dt<\infty\) then the
solution continues. A bound that yields that integral,
or an equivalent criterion, gives no blowup. \(L^2\)
is not the max.
*[follows from (6)–(7)]*

**(9)** **Bootstrap.** Standard parabolic regularity:
a bound on \(X\) and no blowup of \(\|\omega\|_\infty\)
upgrades to smoothness on \([0,T]\). If \(T\) is
arbitrary, the solution is globally regular.
*[follows from (6)–(8)]*

If (6) sits, (7)–(9) close the theorem.

---

## Candidates for (6)

Classify one:

- all-data alignment in time (A1)
- all-data \(\int\|\lambda_2^+\|\) (A2)
- a different integrable residual
- a killing field for the stretching leftover

Machine: [`DA-PROOF.md`](DA-PROOF.md)  
From your work: [`DA-FROM.md`](DA-FROM.md)
