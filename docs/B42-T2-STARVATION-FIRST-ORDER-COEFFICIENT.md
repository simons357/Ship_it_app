# B42 — Exact first-order coefficient on the T2 starvation ray

29 September 2026.
Independent analysis of the rationalized 20-row quotient used in B41.
Canonical locked-r2 identity unverified. Classical Navier–Stokes
remains **open**. Not a trajectory, not a drag reduction, not a close.

Packet: [`packets/DA-NS-B42-T2-STARVATION-COEFFICIENT-2026-09-29.md`](../packets/DA-NS-B42-T2-STARVATION-COEFFICIENT-2026-09-29.md)

```bash
PYTHONPATH=scripts python3 -m unittest tests.test_b42_t2_coefficient -q
PYTHONPATH=scripts python3 scripts/run_b42_t2_coefficient.py
```

Code: `scripts/ns_attacks/t2_starvation_coefficient.py`.
Report: `results/b42_t2_starvation_coefficient.json`.
Expected lock inputs: [`data/b42/README.md`](../data/b42/README.md).

---

## What sits

Fix positive channel coefficients \(C_\gamma>0\). On the B39 T2
amplitude ray, factor \(t^{1/2}\) out of the six weak amplitudes and
write the rationalized quotient as

\[
1-\Gamma(t)
=
\min_y
\frac{F_K(y)+t F_J(y)}{C_K+t C_2},
\]

where \(K=\{0,\ldots,13\}\), \(J=\{14,\ldots,19\}\),

\[
d_\gamma(y)=1-\cos\bigl(2\pi(M_\gamma y-\beta_\gamma)\bigr),
\quad
F_K=\sum_{\gamma\in K} C_\gamma d_\gamma,
\quad
F_J=\sum_{\gamma\in J} C_\gamma d_\gamma,
\]

\(C_K=\sum_K C_\gamma\), and \(C_2=\sum_J C_\gamma\). The alignment set

\[
Z_K=\bigl\{y\in(\mathbb R/\mathbb Z)^{12}: F_K(y)=0\bigr\}
\]

is compact. It is nonempty once a certificate \(y_A\) with \(F_K(y_A)=0\)
is granted (B40/B41). Then \(m_J(C)=\min_{Z_K} F_J\) exists, and

\[
\lim_{t\downarrow 0}\frac{1-\Gamma(t)}{t}
=
\frac{m_J(C)}{C_K}.
\]

If the six integer row identities of the rationalized JSON hold, every
point of \(Z_K\) has the same six weak phase residues, \(m_J=D_A\), and
the limit is exactly \(D_A/C_K\) with

\[
D_A
=
\frac{C_{14}+C_{15}+C_{18}+C_{19}+3(C_{16}+C_{17})}{2}.
\]

---

## First-order limit (no matrix)

Let \(z\in Z_K\) minimise \(F_J\). The numerator at \(z\) is \(t m_J\),
so the minimum is at most \(t m_J\). Let \(y_t\) minimise the numerator.
Then \(0\le F_K(y_t)\le t m_J\). Every cluster point of \(y_t\) as
\(t\downarrow 0\) lies in \(Z_K\). Continuity gives
\(\liminf F_J(y_t)\ge m_J\). Also

\[
m_J
\ge
\frac{F_K(y_t)}{t}+F_J(y_t)
\ge
F_J(y_t).
\]

The two bounds force the middle expression to \(m_J\), and in particular
\(F_K(y_t)/t\to 0\). Divide by \(C_K+t C_2\). No phase-grid, Hessian, or
unique-minimiser assumption is used.

A one-dimensional synthetic ray with \(Z_K=\{0\}\) and
\(m_J=1-\cos(\pi/3)=1/2\) reproduces the limit numerically.

---

## Two-row lower bound

The network cycle obstruction says no point of \(Z_K\) can kill all six
weak deficits, so \(m_J>0\) for positive coefficients. The B41
four-cycle on rows 7, 8, 15, 16 gives the explicit lower bound

\[
m_J
\ge
C_{15}+C_{16}-\sqrt{C_{15}^2+C_{16}^2+C_{15}C_{16}}
=:F_{15,16}>0.
\]

Rows 7 and 8 vanish on \(Z_K\). The remaining relative phase is
\(\pi/3\). Minimising
\(C_{15}(1-\cos\theta)+C_{16}(1-\cos(\theta+\pi/3))\) is the modulus
identity

\[
\max_\theta\bigl(C_{15}\cos\theta+C_{16}\cos(\theta+\pi/3)\bigr)
=
\bigl|C_{15}+C_{16}e^{i\pi/3}\bigr|
=
\sqrt{C_{15}^2+C_{16}^2+C_{15}C_{16}}.
\]

The two-row expression is a valid lower bound. It is **not** the leading
coefficient. On the unit vector \(C_\gamma\equiv 1\),
\(F_{15,16}=2-\sqrt 3\approx 0.268\) while \(D_A=5\).

Evaluating at a certificate with the six B40 residues gives the matching
upper bound \(m_J\le D_A\). Equality throughout \(Z_K\) is the content of
the integer-row calculation, not of the two-row cycle.

---

## Integer identities pin the weak phases

Direct \(\mathbb Z\)-arithmetic on a \(20\times 12\) integer matrix \(M\)
gives the six identities (zero-based rows)

| Weak row | Identity in strong rows |
|---|---|
| 14 | \(m_{14}=-m_1+m_3+m_{12}\) |
| 15 | \(m_{15}=m_0-m_1-m_2+m_3-m_5+m_7+m_{10}\) |
| 16 | \(m_{16}=m_0-m_1-m_2+m_4-m_5+m_7+m_{10}\) |
| 17 | \(m_{17}=-m_0+m_3+m_{12}\) |
| 18 | \(m_{18}=-m_0+m_4+m_{12}\) |
| 19 | \(m_{19}=-m_2+m_4-m_5+m_7+m_{10}\) |

On \(Z_K\) every strong row satisfies \(M_i y\equiv\beta_i\pmod 1\).
Integer coefficients therefore freeze each weak phase error on the whole
of \(Z_K\):

\[
M_j y
\equiv
\sum_i a_{ji}\beta_i
\pmod 1.
\]

There is no remaining continuous, or disconnected-component, optimisation
of \(F_J\) on \(Z_K\). The B40 certificate \(y_A\) is then only a
*reader* of those six constants, not a special minimiser.

The stated errors, in units of \(\pi/12\), are
\((20,-4,16,8,4,4)\) on rows 14–19. Their cosines are
\((1/2,1/2,-1/2,-1/2,1/2,1/2)\). The deficits
\(1-\cos\) are \((1/2,1/2,3/2,3/2,1/2,1/2)\), which is exactly \(D_A\).
Hence every \(y\in Z_K\) would have \(F_J(y)=D_A\), and

\[
\lim_{t\downarrow 0}\frac{1-\Gamma(t)}{t}
=
\frac{D_A}{C_K}.
\]

At positive \(t\) an optimiser may move the 14 strong phases. Those
deficits are \(o(t)\). The six weak phases still converge to the frozen
residues. The leading weak deficit cannot be reassigned onto rows 15 and
16 alone.

This algebraic implication is checked on a synthetic \(20\times 12\)
integer matrix that obeys the identities by construction. It is **not**
a substitute for reading the identities off the hashed JSON.

---

## What this checkout could and could not open

| Claim | Status here |
|---|---|
| First-order limit \(m_J/C_K\) | **Verified** (analysis + 1-D numeric) |
| Two-row formula \(F_{15,16}\) | **Verified** (modulus identity + grid) |
| Cosines of \((20,-4,16,8,4,4)\pi/12\) and the shape of \(D_A\) | **Verified** |
| Integer identities \(\Rightarrow\) constant \(F_J=D_A\) on \(Z_K\) | **Verified** as an implication |
| The six identities on the Library JSON | **Not verified** — JSON absent |
| \(y_A\) residues on that JSON | **Not verified** — JSON absent |
| Comparison with locked `M.tsv`, `b_exact.tsv` | **Not verified** — files absent |
| Sprint 01 parallelogram 20-row incidence = JSON identities | **Rejected** |
| Canonical locked-r2 identity | **Unverified** |
| Symmetrized coefficient convention | **Unverified** |
| Classical NS / a dynamical trajectory / drag reduction | **Not claimed** |

The Library JSON SHA-256 named in B42 is

```
87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898
```

No file of that hash is in this repository. Locked `M.tsv` and
`b_exact.tsv` are likewise absent (`data/b42/`).

A natural 20-row quotient of the Sprint 01 parallelogram (drop the four
T1/T2 odd-\(k\) Vandermonde zeros, take \(J=\) T4) is \(20\times 12\) and
does **not** satisfy the six identities. Do not identify that incidence
with the rationalized JSON.

---

## Scope

The coefficient pertains to fixed positive channel coefficients and one
instantaneous amplitude ray in the rationalized JSON. It does not imply
that a Navier–Stokes trajectory follows that ray. It is not a drag
reduction. It does not close classical NSE.

Before a canonical statement: compare every row and every exact target
with locked `M.tsv` and `b_exact.tsv`, and independently verify the
symmetrized coefficient convention.
