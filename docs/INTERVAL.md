# Short-time interval of \(N\) and \(T_c\)

23 September 2026.
**Stokes keeps \(N=0\) on \(v_n\)
for a positive time, not only
at first order.
NSE generates \(N<0\).
\(R_{mn}\) stays 1.
Large-amp \(K_{1/2}\) grows.
A short path is not a
useful \(K\) and not a death
of G4.
Not a close. ★ stays killed.
Catalog B open stays 1.**

First jet:
[`PATHWISE.md`](PATHWISE.md).
Instantaneous \(MN\):
[`MN-CANCEL.md`](MN-CANCEL.md).
L-doors:
[`L-DOOR.md`](L-DOOR.md).
Energy-class:
[`ENERGY-K.md`](ENERGY-K.md).
Target:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
Machine: `python3 scripts/interval.py`.
Does not overwrite `stokes_moments.py`.
Do not start leftover 1.
Do not weld \(\star\).
Do not cash B★ as G5.
This is **not**
[`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).
This is **not**
[`PATHWISE.md`](PATHWISE.md).

---

## Three kinds of sentence

**Exact.** Stokes path
\(u(t)=e^{-\nu A t}u_0\).
Galerkin energy
\(E'=-2\nu X\).
\(\Lambda'=2(T_c-\nu\mathcal D_s)/X\).

**Numerical.** Printed
paths. Finite is not \(C\)
and not a remainder.

**Illustrative.** A cutoff
Galerkin path is not a
singular NSE solution.

---

## Stokes interval (exact field)

On \(v_n\), \(N\) stays at
working-precision zero on
the printed interval.
\(R_{mn}\) stays 1.
The knife-edge is
Stokes-invariant, not only
a first jet.

| Family | \(t\) | \(T_c(t)/T_c(0)\) | \(R_E(0)\to R_E(t)\) |
|---|---|---|---|
| \(v_1\) | \(0.05\) | \(0.616\) | \(0.114\to 0.143\) |
| \(v_4\) | \(0.01\) | \(0.236\) | \(13.0\to 23.5\) |
| \(v_8\) | \(0.004\) | \(0.102\) | \(144\to 305\) |
| live \(2,2,4\) | \(0.05\) | \(0.693\) | \(0.093\to 0.099\) |

\(T_c\) decays because high
modes die. \(R_E\) *grows*.
The energy-class death
persists and gets worse
as the field cools.
Do not seat \(N\equiv 0\)
for all \(t\) as a closed
form. Lock the printed
interval.

Live-triangle \(R_{mn}\)
stays \(1/3\), amplitude-flat.

---

## NSE interval (IF-RK2)

Jet lock on \(v_1\): one
tiny step matches the
Gateaux of
[`PATHWISE.md`](PATHWISE.md).
Energy lock: \(E+2\nu\int X\)
holds to \(10^{-5}\).

| Path | \(t\) | \(N(t)\) | \(T_c(t)/T_c(0)\) | \(R_{mn}\) |
|---|---|---|---|---|
| \(v_1\), \(\nu=1\) | \(0.02\) | \(-0.210\) | \(1.059\) | \(1\) |
| \(v_1\times 4\) | \(0.006\) | \(-18.6\) | \(1.317\) | \(1\) |
| \(v_1\), \(\nu=0\) | \(0.006\) | \(-0.081\) | \(1.103\) | \(1\) |
| live \(2,2,4\) | \(0.02\) | — | \(1.65\) | \(1/3\) |

\(N\) becomes negative.
\(-\Lambda N\) *adds* to
\(T_c\). So \(R_{mn}=1\)
even after \(N\) leaves 0.
Instantaneous \(MN\) death
persists on the interval.

\(R_E\) on \(v_1\):
\(0.114\to 0.162\).
The energy-class death
does not heal.

---

## Large amplitude: viscosity
does not catch \(K\)

On \(v_1\times 4\),
\(\nu=1\),
\(K_{1/2}=(T_c-\tfrac12\nu\mathcal D_s)_+/X\)
goes \(0.663\to 1.26\).
The tautological remainder
*grows* on the nonlinear
time. Do not cash
\(K_{1/2}=0\) at amplitude 1
as viscosity winning.
That was a units choice,
already named on
[`PATHWISE.md`](PATHWISE.md).

---

## What this is not

A short computed path is
not a useful
\(K\in L^1_{\mathrm{loc}}\).
Every smooth Galerkin path
has a tautological \(K\).
That is forbidden as a
proof.

It is not a named death
of G4. \(v_n\) is still
an admissible class. The
ODE is a cutoff Galerkin
trajectory, not a blowup.

Tautological \(K\) is
still forbidden.

---

## What remains

Energy-class \(K(E)\) is
dead, including along
these paths. Tight CS is
★. LE is dead. LX is not
seated. Instantaneous
\(MN\) is dead, including
along these paths. The
\(t=0\) jet is not a \(K\).
This interval is not a
\(K\) and not a G4 death.

G4 stays OPEN only for a
named bound that is more
than a snapshot, more
than a \(t=0\) Taylor
coefficient, and more
than a short computed
path: a useful \(K\) on a
classical solution, or a
named death of G4 that
is not this interval.

---

## What this page is not

- A close. Catalog B open
  stays 1.
- A seating of B★ or of LX.
- A restoration of ★.
- A singular NSE solution.
- Leftover 1. Do not start
  H1.
- [`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).

---

## Lock

Stokes keeps \(N=0\) on
the printed interval.
NSE keeps \(R_{mn}=1\).
Large-amp \(K_{1/2}\) grows.
A path is not a useful \(K\).
G4 stays OPEN. ★ stays killed.
NS not solved.
