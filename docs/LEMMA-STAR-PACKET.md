# Lemma★ — coherent triad packets (Attacks 9–10)

10 September 2026. Live falsification target. **Not a proof.
NS not solved. These samples did not kill Lemma★.**

Locked form: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).
AP probe: `python3 scripts/ns_attacks/attack9_packet.py`
Same-shell: `python3 scripts/ns_attacks/attack10_same_shell.py`

---

## The heuristic

Take three Fourier packets \(P,Q,R\) with \(R=P+Q\), each
with about \(m\) modes. After normalizing energy, each
coefficient is about \(m^{-1/2}\). There can be \(O(m^2)\)
aligned triads, each cubic contribution \(O(m^{-3/2})\), so
\[
T_c\sim m^{1/2},
\qquad
\mathcal D_s\|v\|_2^2 Y\sim O(1),
\qquad
\mathcal R_\star\sim m,
\]
**if** the denominator stays \(O(1)\) and the triads add.

If incompressibility, phase cancellation, or triadic
conservation does not destroy that coherent \(m^{1/2}\)
growth, Lemma★ is false. If numerics stay bounded as packet
size grows, a proof needs the matching square-summation or
orthogonality estimate.

Isolated triangles (Attack 8) are not this test.

---

## What ran

Arithmetic-progression packets: \(P=\{p_0+ie\}\),
\(Q=\{q_0+je\}\), \(R=\{p_0+q_0+ke\}\). \(O(m^2)\) closures.
Energy normalized. Coherent phases, plus a random-phase
control, plus an HH→L fan with mass on the low mode and
randomized polarization (the Attack 6 frozen fan was not
this).

Two-key vs two-shell check, as corrected:
- two Fourier keys: \(T_c=0\)
- two shells, three keys \(p=(1,1,0)\), \(q=(1,-1,0)\),
  \(p+q=(2,0,0)\): \(T_c\) live, \(\mathcal R_\star\approx 0.031\)

---

## Diagnosis

The wide AP packet made \(T_c\) grow, but \(\mathcal D_s\)
grew faster, so the \(O(1)\) denominator heuristic failed.

A near-shell (narrow) packet is the next construction:
keep \(|e_{\mathrm{packet}}|/|k_0|\) small so \(\mathcal D_s\)
can stay \(O(1)\). If \(\mathcal R_\star\) then grows like
\(m\), the heuristic is live. If \(\mathcal D_s\) still
outruns \(T_c\), or the packet leaves the shell as \(m\)
grows, that construction is not a kill.

---

## Score

**Wide AP** (\(p_0=(5,2,1)\), \(q_0=(-3,1,1)\)). \(T_c\)
grows, but \(\mathcal D_s\) and \(Y\) grow faster. The
\(O(1)\) denominator fails. \(\mathcal R_\star\) falls
(\(3.3\times 10^{-2}\) at \(m=2\) to \(2.7\times 10^{-3}\)
at \(m=16\)). Random phases sit near zero. Not a kill.

**Narrow AP** (carrier \(\sim 32\), same step, so
\(|e_{\mathrm{packet}}|/|k_0|\) starts small). Denominator
stays flatter while \(m\ll|k_0|\). \(\mathcal R_\star\)
grew through \(m=12\) then rolled over as the packet width
ceased to be small compared with \(|k_0|\):

| \(m\) | \(\mathcal R_\star\) (narrow) |
|---|---|
| 2 | \(0.0095\) |
| 4 | \(0.042\) |
| 6 | \(0.059\) |
| 8 | \(0.115\) |
| 12 | \(0.20\) |
| 16 | \(0.093\) |
| 20 | \(0.0064\) |
| 24 | \(0.027\) |

Peak \(\approx 0.25\), then down. Finite-\(m\) growth is
not \(\mathcal R_\star\to\infty\). The heuristic is not
destroyed at moderate \(m\) on this construction; spectral
spread stops it from diverging. Not a kill.

**HH→L fan** (randomized, low mode populated):
\(\mathcal R_\star\) small, not growing like \(m\).

---

The AP construction above is one packet, not that target
closed. Do not cash a peak of \(0.25\) as \(C_0\) or as a
kill.

---

## Attack 10 — same-shell coherent packet

Probe: `python3 scripts/ns_attacks/attack10_same_shell.py`

P and Q on one eigenvalue \(N\), R on the most popular
sum-shell \(T\neq N\). \(O(m^2)\) closures among those
pairs. Energy normalized. Aligned swirl, one phase per
shell. Small \(m\) keeps actual T-pairs (edge-preserving
subset), so the packet does not collapse to an empty
field.

Eigenvalues do not spread with \(m\). \(\mathcal D_s\) is
the shell gap, not AP width. That is the test the wide
and narrow APs could not run.

Fixed shell \(N=54\) (\(|S|=96\), \(T=126\)):

| \(m\) | pairs | \(\mathcal R_\star\) | \(T_c\) | \(\mathcal D_s\) |
|---|---|---|---|---|
| 5 | 8 | \(4.16\times 10^{-3}\) | \(1.91\times 10^{3}\) | \(1.01\times 10^{5}\) |
| 12 | 20 | \(1.31\times 10^{-3}\) | \(1.08\times 10^{3}\) | \(1.01\times 10^{5}\) |
| 18 | 32 | \(6.29\times 10^{-4}\) | \(7.53\times 10^{2}\) | \(1.00\times 10^{5}\) |
| 24 | 46 | \(1.04\times 10^{-3}\) | \(9.61\times 10^{2}\) | \(1.01\times 10^{5}\) |
| 36 | 80 | \(1.15\times 10^{-3}\) | \(9.76\times 10^{2}\) | \(1.02\times 10^{5}\) |
| 48 | 148 | \(7.25\times 10^{-4}\) | \(8.23\times 10^{2}\) | \(9.51\times 10^{4}\) |
| 72 | 288 | \(4.29\times 10^{-4}\) | \(6.32\times 10^{2}\) | \(8.71\times 10^{4}\) |
| 96 | 480 | \(5.46\times 10^{-4}\) | \(7.13\times 10^{2}\) | \(8.71\times 10^{4}\) |

\(\mathcal D_s\) stayed flat in \(m\) (max/min \(\approx 1.17\)).
The \(O(1)\)-denominator heuristic now has the denominator
it asked for.

\(T_c\) did not grow like \(m^{1/2}\). It fell or wandered.
Pair count is still \(O(m^2)\) (480 pairs at \(m=96\)).
The cubic terms did not add. Random phases on the full
shell: \(\mathcal R_\star\approx 5\times 10^{-7}\).

Full shells \(N=2,5,14,18,26,41,54,90\): every
\(\mathcal R_\star\le 1.7\times 10^{-3}\). Peak on the
\(m\)-sweep \(\approx 4.2\times 10^{-3}\). Do not cash
that as \(C_0\) or as a kill.

**Score.** Same-shell is not a kill. The AP failure mode
(Ds outrunning \(T_c\)) is off. The remaining failure
mode on this construction is the numerator: incompressibility,
phases, or triadic counting. That is the estimate a proof
has to write. It is not written. Finite \(m\) on two
shells is not \(\sup\mathcal R_\star<\infty\).

---

## Status

- isolated closed triad tested: no kill
- dilation confirmed exactly neutral
- fixed additive offset becomes safer on the tested ray
- polarization zero is accidental
- wide AP: \(T_c\) grew, \(\mathcal D_s\) faster; not a kill
- narrow AP: finite-\(m\) rise then rollover; not a kill
- same-shell: \(\mathcal D_s\) stayed the gap, \(T_c\)
  did not grow like \(m^{1/2}\); not a kill
- the remaining packet target is an HH→L fan that
  actually grows, or H1 on one cylinder
- the uniform global triadic bound remains completely open

Do not: more isolated triangles, more frozen rays, more
uniform dilations, more \(k_{\max}=8\) samples, another AP,
K=0, or gluing this to H1.

The other live writing is still H1 on one cylinder
(thinness / J on folds / waiting time). Same leftover
class, different integral. Work one.

The uniform triadic bound is still completely open.
NS is not solved.

Say **fan** for the remaining packet target, or **H1**
for the cylinder.

Do not merge with H1. Do not add \(K(t)\) to the PDE.
Do not write “almost proved.”
