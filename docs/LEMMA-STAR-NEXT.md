# Lemma★ — next (Attack 6)

10 September 2026. Ideas, then a probe. **Not a proof. NS not solved.**

Locked statement: [`LEMMA-STAR.md`](LEMMA-STAR.md).
Calculator: `scripts/ns_attacks/stokes_moments.py`.
Probe: `python3 scripts/ns_attacks/attack6_scale_law.py`

---

## Ideas (honest)

1. **Do not chase a uniform pre-Young \(C\).**
   Geometry-only \(C\) in \(|T_c|\le C\|u\|_2 X\Lambda\) cannot depend
   on the highest wavenumber. The five-lane max already sat on
   a scaled triad (`sep_32`). If \(|R_{\mathrm{pre}}|\) grows with
   \(s\), that door is dead. Measure the law. Do not draw more
   random samples at \(k_{\max}=8\).

2. **The exact ★ remainder is \(\mathcal R_\star\).**
   That is the trilinear shape estimate with \(C_{\star}^2=4\theta C_0\).
   File: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md). The Attack-2
   remainder \(|T_c|\le C_* X^{3/2}\Lambda\) is a different
   sufficient door for DA-NS-2. Do not merge those constants.
   HH→L lattice fan scored: no kill.

3. **Coherent HH→L fan — scored, no kill.**
   Partners on a high sphere. \(\mathcal R_\star\sim\beta/\alpha\).
   Multiplicity does not flip it. File: [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).

4. **Closing three-key, not two keys.**
   \(k_0+(k_0+e)=2k_0+e\). Two shells can be live. The
   near-shell limit is \(|e|/|k_0|\to 0\), and a frozen ray
   is not the supremum. File: [`LEMMA-STAR-E.md`](LEMMA-STAR-E.md).

5. **Coherent packets, not more isolated triangles.**
   \(P,Q,R=P+Q\), \(O(m^2)\) triads, heuristic
   \(\mathcal R_\star\sim m\) if \(\mathcal D_s Y\) stays
   \(O(1)\). File: [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).

Do not revive K=0. Do not glue H1. Do not add \(K(t)\) to the PDE.
Do not cash a bounded ratio as \(C_0\).

---

## What ran

Scaled resonant triad \(k\mapsto s k\), \(s=1,2,4,8,16,32,48,64\),
best of 24 random phases plus the default, unit amplitude.
Then a coherent fan \(N=2,4,8,12,16\) with frozen seeds
(uninformative; see below).

---

## What it showed

On the scaled triad:

| \(s\) | \(\lvert R_{\mathrm{pre}}\rvert\) | \(\lvert R_{\mathrm{pre}}\rvert/s\) | \(\lvert R_{C_*}\rvert\) |
|---|---|---|---|
| 1 | 0.157 | 0.157 | 0.0401 |
| 2 | 0.314 | 0.157 | 0.0401 |
| 4 | 0.637 | 0.159 | 0.0406 |
| 8 | 1.262 | 0.158 | 0.0403 |
| 16 | 2.540 | 0.159 | 0.0405 |
| 32 | 5.093 | 0.159 | 0.0406 |
| 48 | 7.608 | 0.158 | 0.0405 |
| 64 | 10.123 | 0.158 | 0.0404 |

**Pre-Young door is dead as a uniform estimate.**
\(\lvert T_c\rvert/(\|u\|_2 X\Lambda)\simeq 0.158\,s\to\infty\) as \(s\to\infty\).
A geometry-only \(C\) independent of \(u\) does not exist for
\(|T_c|\le C\|u\|_2 X\Lambda\). The five-lane “survive” used a
crude threshold \(10^3\) on that ratio. The law already kills
uniform \(C\). It does not kill the \(C_*\) form.

**\(C_*\) survives this family.**
\(\lvert T_c\rvert/(X^{3/2}\Lambda)\simeq 0.0404\), independent of \(s\).
That is the remainder to try to prove. It is not a theorem.
One triad shape is not all divergence-free fields.

**Fan:** \(T_c=0\) at every \(N\) with those polarizations.
That is not a bound. Do not rerun it frozen. If you probe a
fan again, randomize phases.

---

## What to write next

Lemma★ **is** a uniform bound on
\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}
{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
\]
Prove it from triadic geometry or cancellation, or kill
it with a near-shell / HH→L family where
\(\mathcal R_\star\to\infty\). Equivalent form: the
trilinear estimate with \(C_{\star}^2=4\theta C_0\).
File: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).

The first family is the closing three-key. Two Fourier
keys is not that test. Two shells can be live. Hunt by
\(|e|/|k_0|\to 0\) with the supremum recomputed. Attack 8
did not kill it: [`LEMMA-STAR-E.md`](LEMMA-STAR-E.md).
Live target was a growing coherent triad packet or HH→L fan.
Scored: AP, adjacent spheres, Freiman-AP subset, HH→L fan
(\(\mathcal R_\star\sim\beta/\alpha\)). No kill. The \(m^{1/2}\)
heuristic has not found a lattice home. Remaining: H1 on
one cylinder, or the uniform triadic bound.
Packets: [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).
Original five-lane JSON:
[`five-lane-export/COMPUTE.md`](five-lane-export/COMPUTE.md).
Attack 9B: [`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md).

Route A incidence (conditional continuum
\(I\ll m^{4/3}\Rightarrow C(S)=O(m^{4/3})\); lattice
transfer MISSING):
[`LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md`](LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md).

Door 1 (uniform pre-Young \(C\)) is off. K=0 stays dead.
The Attack-2 remainder \(|T_c|\le C_* X^{3/2}\Lambda\) is a
different sufficient attack on DA-NS-2, not this
\(C_{\star}\). The missing content is the uniform triadic
bound — not more viscosity bookkeeping, and not more
bounded samples.

H1 on a cylinder is a different integral. Do not merge.
