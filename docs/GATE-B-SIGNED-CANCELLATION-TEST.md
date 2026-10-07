# Gate B — signed cancellation test

7 October 2026.
**Second assembly test. Signs kept. Not (17). NS not solved.**

The first test is finished:
[`GATE-B-SOURCE-ASSEMBLY-AND-CONCENTRATION-TEST.md`](GATE-B-SOURCE-ASSEMBLY-AND-CONCENTRATION-TEST.md).
For the explicit nonnegative \(Q_x\), any uniform power bound
requires \(\theta\ge\tfrac12\). Optimal \(\theta\) OPEN.
That rules out getting the desired gain merely by regrouping
this majorant.

The next meaningful test must preserve signed cancellation.

Checker: `scripts/ns_attacks/signed_cancellation_test.py`.
Packet: [`../packets/GATE-B-SIGNED-CANCELLATION-TEST-2026-10-07.md`](../packets/GATE-B-SIGNED-CANCELLATION-TEST-2026-10-07.md).

---

## Object

Exact receiver form (Fourier-triangle audit; one triad):

\[
\mathcal T_{abc}
=
(c-b)\,I_p
+(a-c)\,I_q
+(b-a)\,I_r,
\]

\[
I_p=(q\cdot u_p)(u_q\cdot u_r)
\quad\text{(Im taken after the cyclic sum).}
\]

One globally compatible divergence-free field: \(k\cdot\hat u_k=0\),
and on the diagnostic subnet every triad reuses the same high
mode \(w=(-n,-n,0)\).

Group on the low vertex, **without** killing signs:

\[
Q_x^{\mathrm{sgn}}
=
\sum_{\substack{\text{triads}\\ \text{low vertex }x}}
\frac{\mathcal T_{abc}}{f_x}
\qquad(f_x>0),
\]

\[
\sum_x f_x\,Q_x^{\mathrm{sgn}}
=
\sum_{\mathrm{triads}}\mathcal T_{abc}.
\]

Compare \(\lVert Q^{\mathrm{sgn}}\rVert_2/\Omega\) to the
nonnegative envelope \(\lVert Q^{+}\rVert_2/\Omega\), under
dilation of \(\Lambda\).

Forbidden: \(\lvert\sum S\rvert\to\sum\lvert S\rvert\) before
grouping. Occupancy counting is not a substitute.

---

## What the checker measures

1. **Single similar triad.** Nothing to cancel against.
   \(\lvert\mathcal T_{abc}\rvert\le C_{abc}f_a f_b f_c\).
   Signed \(\theta\) stays \(1/2\). This is a lock, not news.

2. **Diagnostic subnet, shared \(w\).** Finite DF search:
   - coherent adversary: coordinate ascent on phases and
     polarizations, maximizing \(\lVert Q^{\mathrm{sgn}}\rVert_2\);
   - random-phase baseline (optimistic, not a bound).

3. **Identity and majorant.** Reassembly
   \(\sum f_x Q_x^{\mathrm{sgn}}=\sum T\) and
   \(\sum\lvert T_{abc}\rvert\le\sum C_{abc}f_a f_b f_c\).

## Result of this run (seed 0)

Single similar triad, \(n=4\to 8\):

| | \(\hat\theta\) | \(\lvert T\rvert/Cfff\) | \(\lVert Q^{\mathrm{sgn}}\rVert_2/\lVert Q^{+}\rVert_2\) |
|---|---:|---:|---:|
| nonnegative | \(1/2\) | — | 1 |
| signed adversary | \(0.47\) | \(\approx 0.21\) | \(\approx 0.21\) |

Nothing to cancel against. The gap to \(C_{abc}\) is a
geometric prefactor. The power stays the half derivative.

Diagnostic subnet, shared \(w\), \(n=4,6,8\):

| \(n\) | triads | \(\lVert Q^{\mathrm{sgn}}\rVert_2/\lVert Q^{+}\rVert_2\) | adversary coherence | random coherence mean |
|---:|---:|---:|---:|---:|
| 4 | 4 | \(0.203\) | \(0.48\) | \(0.53\) |
| 6 | 12 | \(0.202\) | \(0.51\) | \(0.32\) |
| 8 | 16 | \(0.206\) | \(0.67\) | \(0.23\) |

The signed/nonnegative ratio is a **stable constant**
\(\approx 1/5\), not a decaying power. Pairwise
\(\hat\theta\) on this short range jumps (\(0.16\) then
\(0.64\)) and is **not** a claim that signed assembly
beats \(\tfrac12\). Random-phase coherence falls with
\(n\); that is an average-case observation, not a uniform
bound.

Honest reading: keeping signs on this sample supplies a
constant-factor discount relative to \(C_{abc}\), and does
**not** yet force \(\theta<\tfrac12\). The power question
remains OPEN. Still not (17).

---

## Scope

- Classical unaugmented NS on \(\mathbb T^3\), diagnostic
  Fourier subnet only.
- Finite search. Not a signed multi-shape lemma.
- Gate A remains UNRESOLVED / DIAGNOSTIC ONLY.
- Do not chase larger \(c\) to finish Gate A.
- Frozen multiplicity-5 / smallest-leg stands as a Gate A
  convention, unused here.
- No Clay / prize / QED language.

---

## Lock

Signs kept. One DF field. Exact \(T_{abc}\).
Nonnegative regrouping already ruled out.
Signed \(\theta\) is a measurement, not a theorem.
(17) OPEN. NS not solved.
