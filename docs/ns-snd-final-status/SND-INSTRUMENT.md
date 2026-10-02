# SND instrument — diagnostics, not persistence

16 September 2026.
**Instrument first. No theorem.
No persistence claim. Not leftover 1.
Catalog B open stays 1.**

Handoff: [`NS-STATUS.md`](NS-STATUS.md).
Implication (still not a bound on
\(X\)):
[`SND-TO-REGULARITY.md`](SND-TO-REGULARITY.md).
Theorem H stays withdrawn:
[`SND-H-REVIEW.md`](SND-H-REVIEW.md).
Partition dictionary:
[`UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md)
§8.1 (object under review, not a
proved estimate).

Arithmetic:
`python3 scripts/snd_instrument.py`.

---

## Frozen partition

Littlewood–Paley enstrophy shells on
\(\mathbb{T}^3\) (or a listed discrete
mass vector with the same labels):

\[
X_j=2^{2j}\|\Delta_j u\|_2^2,\qquad
X=\sum_j X_j=\|\omega\|_2^2.
\]

The instrument never changes this
definition. Dyadic labels \(j\) are
integers. Empty shells are stored as
zero, not dropped from a listed
support, so \(\operatorname{argmax}\)
is well-defined.

---

## Exact diagnostics

On a frozen mass vector
\((X_j)_{j\in\mathcal J}\):

\[
J=\max_j X_j,\qquad
\rho=\frac{J}{X}\quad(X>0),\qquad
j_*=\min\operatorname{argmax}_j X_j.
\]

The left-most peak is the tie-break.
That is a convention, not a dynamical
claim.

Packet and occupation:

\[
P_{j_*}=X_{j_*-1}+X_{j_*}+X_{j_*+1},
\qquad
\sigma=\frac{P_{j_*}}{X}\in(0,1].
\]

Missing neighbors count as zero.

Barycenter and tail:

\[
\bar j=\frac{\sum_j j\,X_j}{X},\qquad
\tau=\frac{1}{X}\sum_{j>j_*}X_j.
\]

**Tail profile.** For \(j>j_*\) set
\(r_j=X_j/J\). The diagnostic envelope
parameter is the largest \(\gamma\ge 0\)
such that

\[
X_j\le J\,2^{-\gamma(j-j_*)}\qquad
\text{for every listed }j>j_*,
\]

or \(\gamma=0\) if some listed tail
shell exceeds \(J\) (it cannot, by
definition of \(J\)) or if the only
constraint is the trivial \(X_j\le J\).
If a tail shell is positive at
arbitrarily large \(j\) with
\(X_j/J\) not decaying, the recorded
\(\gamma\) is \(0\).

This \(\gamma\) is a number attached
to a snapshot. It is not a regularity
assumption and not a BKM criterion.

**Flux \(F_j\).** If a flux vector is
supplied, it is recorded shell by
shell. On the audit shear family
\(F_j=0\) identically. The instrument
does not invent a flux from
occupation.

**Peak migration.** Given two
snapshots, record

\[
\Delta j_*=j_*(t_2)-j_*(t_1),\qquad
\Delta\bar j=\bar j(t_2)-\bar j(t_1).
\]

A nonzero \(\Delta j_*\) is a
diagnostic. It is not a climb law
and not prescribed \(c=8\).

---

## What the instrument refuses

It does not assert \(\rho\ge\rho_*\).
It does not assert \(j_*\le J_0\).
It does not assert a uniform tail.
It does not restore Theorem H.
It does not close leftover 1, 4, or 5.
It does not merge with C10 or \(T_c\).

The audit already showed why
\(\rho\) plus a bounded peak are not
enough: the remaining \(1-\rho\) can
sit at arbitrarily high frequency.
The instrument prints that split. It
does not repair it.

---

## Locked samples

1. **Packet shear** (SND-H review).
   Unique peak at \(j_*=0\),
   \(\rho=2/(N+2)\), high tail of
   weight \(Nb\), \(F\equiv 0\).
2. **Equal-enstrophy \(v_L\).**
   \(\rho=1/L\), every listed shell
   is a peak; left-most \(j_*\) is
   the convention. No universal
   floor.
3. **High-tail one-peak.** Peak at
   a low \(j_*\) with a single far
   shell of mass \((1-\rho)X\).
   \(\rho\) can be large while the
   tail frequency is arbitrary.
   Prints the missing piece: tail
   location, not only \(\rho\).

---

## Verdict

| Claim | Status |
|---|---|
| Partition and diagnostics | **PROVED** as definitions / arithmetic. |
| Persistence of \(\rho\) | **Not claimed.** |
| Theorem H / SND-C | **DEAD** as a bridge. |
| BKM from assumed \(\gamma\) | Useful later. **Not** the primary. |

---

## Lock

Frozen X_j, J, ρ, j_*, P, σ, τ,
γ_diag, F_j, j_bar, Δj_*.
Instrument, not a theorem.
Do not assert persistence.
NS not solved.
