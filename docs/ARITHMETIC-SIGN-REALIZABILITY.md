# Arithmetic sign realizability

24 September 2026.
**The loop-gauge / telescopic
capacity board is frozen.
This gate is run, not
reinterpreted.
NS not solved.**

Parent:
[`LOOP-GAUGE-AND-TELESCOPIC-CAPACITY.md`](LOOP-GAUGE-AND-TELESCOPIC-CAPACITY.md)
is **not altered**.
JGC parent:
[`JOINT-EPOCH-BUDGET.md`](JOINT-EPOCH-BUDGET.md).

Code:
`scripts/ns_attacks/sign_realizability.py`.

```bash
PYTHONPATH=scripts python3 -m unittest tests.test_sign_realizability -q
PYTHONPATH=scripts python3 scripts/ns_attacks/sign_realizability.py
```

Unaugmented NS on \(\mathbb{T}^3\).
No occupancy envelope. No new
potential. No new clock.

---

## Notation safeguard

The discrete expansion is EXACT
in the actual neighboring
transfer \(T\):

\[
T_c
=
\Lambda\langle\delta,T\rangle
+
\sum_m\delta_m^2 T_m,
\qquad
\delta_m=\lambda_m-\Lambda.
\]

The neighboring \(T_m\) itself
varies with the deformation.
Do **not** substitute
\(T^{(0)}\) into that finite-gap
identity.

The first-variation object is

\[
\boxed{
L_{1,N}
=
\Lambda_N\langle\delta_N,T_N^{(0)}\rangle
}
\]

on the asymptotic
neighboring-shell family, so
the transfer variation is next
order. Heavy keeps the actual
neighboring \(T_m\) as a
remainder check:

\[
\boxed{
R_{2,N}
:=
T_{c,N}
-
\Lambda_N\langle\delta_N,T_N^{(0)}\rangle.
}
\]

A legitimate first-variation
sequence has \(R_{2,N}\) of
higher order than \(L_{1,N}\).
If not, the deformation changed
polarization, amplitudes, or
topology too strongly to
represent this gate.

On the locked family (unit
lattice move off an exact
shell \(p+q=k\), \(\lvert p\rvert^2
=\lvert q\rvert^2=\lvert k\rvert^2=N\)),
the median \(\lvert R_2/L_1\rvert\)
falls with \(N\):

| \(N\) | median \(\lvert R_2/L_1\rvert\) |
|---:|---:|
| 6 | 0.263 |
| 14 | 0.211 |
| 18 | 0.233 |
| 26 | 0.199 |
| 42 | 0.150 |
| 50 | 0.139 |
| 74 | 0.118 |

That is the predicted
higher-order behaviour. The
family is a legitimate
first-variation sequence.

\(\rho_N\) is the geometric
correlation of the child gap
against the frozen parent
transfer, at canonical real
helical amplitudes \(a=1\).
Phase-twin amplitude flips are
recorded and are **not** by
themselves BOTH SIGNS.

---

## Outcome tree

\[
\boxed{\textbf{STATIC FRONTIER:
arithmetic sign realizability}}
\]

\[
\Downarrow
\]

\[
\boxed{\textbf{DYNAMIC FRONTIER:
dangerous-state persistence}}
\]

### BOTH SIGNS — seated on this scan

Persistent heterochiral
legitimate samples with

\[
\lvert\rho_N^\pm\rvert\ge c=0.05
\]

appear at every live scale
scanned (\(N=6,14,18,26,42,50,74\)).
Opposite unit moves, and
distinct parents, realize both
signs. This is geometry, not a
phase twin.

\[
\boxed{
\text{universal first-order
one-sided narrow depletion
is false.}
}
\]

Static closure work on this
question **stops**. The
positive branch goes to
evolution.

The canonical seed
\(\mathcal A_N^{+}\) is saved
in
`results/adversarial_seeds/A_N_plus.json`:
integer vectors, helicity
labels, polarizations, and
amplitudes — not merely
\(\delta\) and \(T^{(0)}\).

Locked plus seed of this scan
(\(N=74\)):

\[
p=(-7,-3,4),\;
q=(2,-4,-7),\;
k=(-5,-7,-3),
\]
\[
\sigma=(-,+,+),\qquad
a\equiv 1,
\qquad
\rho_N\approx 0.984,
\]
\[
L_{1,N}\approx 11141,\qquad
R_{2,N}\approx 151
\qquad
(\lvert R_2/L_1\rvert\approx 0.014).
\]

Then

\[
\Theta_N=\nu\kappa_N^2\tau_{U,N}
\approx 17.676
\quad(\nu=1).
\]

It is a diagnostic, not a
bound. The NSE gets the next
move on this field.

### ZERO ONLY — homochiral, separate

On the exact parent shell,
homochiral \(T^{(0)}\) vanishes
to machine precision
(Vandermonde:
\(\sigma_p\lvert p\rvert-\sigma_q\lvert q\rvert=0\)
when \(\lvert p\rvert=\lvert q\rvert\)
and \(\sigma_p=\sigma_q\)).
This scan: \(672/672\)
homochiral samples are zero
at the frozen transfer.
So \(L_{1,N}\) is not the
leading homochiral object.
That is consistent with the
Vandermonde delay. It does
**not** rescue NSE.
Heterochiral remains separate.

### ONE SIGN — not the scan

Not realized heterochirally
on this family. If a later
family produces only one
sign, the question is whether
the restriction is the
Gram / lattice realization
problem — the first serious
bridge from \(I_3\) arithmetic
into the centered dynamics,
rather than merely into
occupancy.

### NO NEIGHBOR — own category

\(N=7,15,\ldots\) are not sums
of three squares. \(N=10,30,66\)
have a nonempty shell and
**no** exact-shell triad
\(p+q=k\). That is arithmetic
rigidity. It is **not** sign
depletion.

---

## What this does not do

- It does not alter the
  loop-gauge gate.
- It does not close DA-NS-2.
- It does not bound \(T_c\).
- It does not invent a new
  potential or a new clock.
- Homochiral zero is not a
  heterochiral theorem.
- \(\Theta_N\) is not a
  continuation criterion.

The NSE itself gets the next
move, on \(\mathcal A_N^{+}\).

---

## Lock

\[
\boxed{
\text{universal first-order
one-sided narrow depletion
is false}
}
\]

on this neighboring-shell
heterochiral family.
\(R_{2,N}\) is higher order.
NO NEIGHBOR stays its own
category.

Static frontier closed as a
**sign-realizability
verdict**, not as regularity.
Dynamic frontier:
dangerous-state persistence.

The Fourier-triangle audit
[`FOURIER-TRIANGLE-AUDIT.md`](FOURIER-TRIANGLE-AUDIT.md)
does not reopen this gate. It
records the seated identities,
the I3 Gram/Hilbert test, and
the open scalene budget (17).

NS not solved.
