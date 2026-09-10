# Lemma★ — coherent triad packets (Attack 9)

10 September 2026. Live falsification target. **Not a proof.
NS not solved. This sample did not kill Lemma★.**

Locked form: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).
Probe: `python3 scripts/ns_attacks/attack9_packet.py`

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

## Score

**Wide AP** (\(p_0=(5,2,1)\), \(q_0=(-3,1,1)\)). \(T_c\)
grows, but \(\mathcal D_s\) and \(Y\) grow faster. The
\(O(1)\) denominator fails. \(\mathcal R_\star\) falls
(\(3.3\times 10^{-2}\) at \(m=2\) to \(2.7\times 10^{-3}\)
at \(m=16\)). Random phases sit near zero. Not a kill.

**Narrow AP** (carrier \(\sim 32\), same step, so
\(|e_{\mathrm{packet}}|/|k_0|\) starts small). Denominator
stays flatter. \(\mathcal R_\star\) grew through \(m=12\)
then rolled over as the packet width ceased to be small
compared with \(|k_0|\):

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

## Status

- isolated closed triad tested: no kill
- dilation confirmed exactly neutral
- fixed additive offset becomes safer on the tested
  isolated triangle (supremum recomputed in \(|k_0|\); a
  frozen ray alone would not have sufficed)
- polarization zero is accidental
- the live falsification target is a growing coherent
  triad packet that **stays near-shell as \(m\) grows**, or
  an HH→L fan with the same property
- this AP packet did not stay near-shell at large \(m\)
- the uniform global triadic bound remains completely open

Do not cash a peak of \(0.2\) as \(C_0\) or as a kill.
Do not merge with H1. Do not add \(K(t)\) to the PDE.
Do not write “almost proved.”
