# Lemma★ — coherent triad packets (Attacks 9–12)

10 September 2026. Live falsification target. **Not a proof.
NS not solved. These samples did not kill Lemma★.**

Locked form: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).
Working claim: [`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md).
Corrections: [`LEMMA-STAR-CORRECTIONS.md`](LEMMA-STAR-CORRECTIONS.md).
AP probe: `python3 scripts/ns_attacks/attack9_packet.py`
Same-shell: `python3 scripts/ns_attacks/attack10_same_shell.py`
Adjacent spheres: `python3 scripts/ns_attacks/attack11_adjacent_spheres.py`
HH→L fan: `python3 scripts/ns_attacks/attack12_hh_l_fan.py`

These packet attacks are **later**. They are not the
original five lanes of PR 48:
[`five-lane-export/FIVE_LANES.md`](five-lane-export/FIVE_LANES.md).

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

**HH→L fan** (Attack 9 randomized control): small, not \(\sim m\).
The sphere fan is Attack 12.

---

The AP construction above is one packet, not that target
closed. Do not cash a peak of \(0.25\) as \(C_0\) or as a
kill.

---

## Attack 10 — same-shell coherent packet

Probe: `python3 scripts/ns_attacks/attack10_same_shell.py`

P and Q on one eigenvalue \(N\), R on the most popular
sum-shell \(T\neq N\). Energy normalized. Aligned swirl,
one phase per shell. That sweep is not the natural
adjacent-sphere ensemble (Attack 11). Do not read its
cartesian pair list as \(\Theta(m^2)\) aligned closures.

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
The pair list at \(N=54\) (480 ordered pairs at 96 keys) is
not \(\Theta(m^2)\) additive density. Random phases on the
full shell: \(\mathcal R_\star\approx 5\times 10^{-7}\).

Full shells \(N=2,5,14,18,26,41,54,90\): every
\(\mathcal R_\star\le 1.7\times 10^{-3}\). Peak on the
\(m\)-sweep \(\approx 4.2\times 10^{-3}\). Do not cash
that as \(C_0\) or as a kill.

**Score.** Same-shell at fixed \(N\) (popular partner \(T\)) is not a kill.
Do not read the cartesian pair list as \(\Theta(m^2)\) aligned closures.
A lattice sphere is not an additive basis of that density.
The natural ensemble is Attack 11.

---

## Attack 11 — full adjacent spheres (the natural same-shell ensemble)

Probe: `python3 scripts/ns_attacks/attack11_adjacent_spheres.py`

Two Fourier spheres \(|k|^2=n\) and \(|k|^2=n+d\). Energy split.
\(m=\#\)keys grows with \(n\). No AP width. \(\mathcal D_s\) is the
gap: \(\lambda\sim n\), so \(\mathcal D_s\sim O(n)\) at fixed \(d\).

**What grew.** On \(d=1\) (the live gap), closures exist — 48 landings
at \(n=9\) to 288 at \(n=89\) — but they scale like \(O(m)\), not
\(O(m^2)\). At \(n=89\): 144+120 keys, 288 landings. \(d=2\): no
landings on the range tested. \(d=3\): sporadic landings, same decay.

**What \(\mathcal R_\star\) did.** Largest at the smallest shell:
\(n=9\), \(\mathcal R_\star\simeq 0.11\). At \(n=89\),
\(\mathcal R_\star\simeq 0.031\). The ratio falls. It does not
track \(m^{1/2}\).

The \(O(1)\) denominator is available (gap, not width). \(T_c\) still
does not produce \(\mathcal R_\star\sim m\). Whole-sphere packets do
not supply the \(O(m^2)\) aligned closures the heuristic assumed.

**Score.** Isolated triangles, wide APs, narrow APs, full adjacent
spheres: no kill. Finite \(n\) is not \(\sup\mathcal R_\star<\infty\).
Do not cash \(0.11\) as \(C_0\).

A designed subset with \(\Theta(m^2)\) closures is Freiman-AP.
That family already ran (wide / narrow AP). \(D_s\) wins. Dead
as a new object.

---

## Attack 12 — HH→L fan (one key or whole low shell)

Probe: `python3 scripts/ns_attacks/attack12_hh_l_fan.py`

**Single low key.** Partners of \(k\) on a high sphere \(\alpha\).
Pair counts 2–12. \(\mathcal R_\star\) is largest when
\(\alpha\sim\beta\) (e.g. \(0.71\) at \(\alpha=5\), \(\beta=4\))
and falls as \(\alpha/\beta\) grows, tracking \(\sim\beta/\alpha\).
That is the incompressibility factor: the vertex carries
\(\sqrt{\beta}\), not \(\sqrt{\alpha}\). More pairs at higher
\(\alpha\) do not flip it.

**Whole low shell.** Up to 144 pairs, 96 high keys. Same decay.
\(\beta=2\), \(\alpha=9\): \(\mathcal R_\star\simeq 0.060\).
\(\beta=2\), \(\alpha=85\): \(\mathcal R_\star\simeq 7\times 10^{-4}\).
Multiplicity did not beat the \(\beta/\alpha\) suppression.

**Score.** HH→L fan, one key or whole low shell: no kill.
Do not cash \(0.71\) as \(C_0\).

---

## Status, updated

- isolated triad: no kill
- wide / narrow AP: \(\mathcal D_s\) wins
- fixed-gap spheres: closures \(O(m)\), \(\mathcal R_\star\) falls
- designed \(\Theta(m^2)\) subset: Freiman-AP, already dead
- screenshot \(\Theta(m^2)\) on one / fixed outputs:
  counting error, excluded (\(K\le 16s\))
  [`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md)
- HH→L fan, one key or whole low shell:
  \(\mathcal R_\star\sim\beta/\alpha\), no blow

The \(m^{1/2}\) heuristic has not found a lattice home
**per output**: at most \(m\) pairs land on a fixed \(k\).
Growing the number of output modes remains legitimate.
The uniform 9B target is
\(\|\Pi_\beta B\|_2\le C(\alpha/\sqrt{\beta})\|w\|_2^2\),
i.e. \(\sup K_{\alpha,\beta}<\infty\). A bound
\(C\alpha\|w\|_2^2\) is the wrong packaging.
Sweep (288 fields): pairs \(\le m\), CS, and
\(K\le 16s\) all sat; max \(K\approx 0.506\),
max \(\sqrt{K}\approx 0.711\). Not \(C_0\).
File: [`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md).
The uniform global triadic bound remains completely open.

Do not: more isolated triangles, more frozen rays, more
uniform dilations, more \(k_{\max}=8\) samples, another AP,
another full sphere, another fan, K=0, or gluing this to H1.

The other live writing is H1 on one cylinder
(thinness / J on folds / waiting time). Same leftover
class, different integral. SoT:
[`H1-SOT.md`](H1-SOT.md). First tube numbers:
[`H1-TUBE.md`](H1-TUBE.md). Estimate package
(OPEN, not a GR close):
[`DOOR-B-H1-ESTIMATE-PLAN.md`](DOOR-B-H1-ESTIMATE-PLAN.md).
Do not quote the Ring Lemma as proved. Do not glue H1 to \(H_N\).
Lattice enumerator still running on this lane.

Route A incidence (conditional continuum win, not a
theorem): [`LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md`](LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md).
\(I\ll m^{4/3}\Rightarrow C(S)=O(m^{4/3})\) kills
\(\Theta(m^2)\) in the continuum model. Lattice transfer
X1–X4/X6 MISSING. Next: Hyp-Lat★. Do not cash ST as ★.

Original five-lane JSON (PR 48 run):
[`five-lane-export/COMPUTE.md`](five-lane-export/COMPUTE.md).
Attack 9B exact-shell closer (\(K_{\alpha,\beta}\),
\(\max K\approx 0.641\) at \((4,8)\); controls PASS;
not a kill):
[`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md).
9C is Attack 11 here. 9D Freiman-AP already dead.
Screenshot \(\Theta(m^2)\) on a fixed output set:
excluded. [`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md).

Do not merge with H1.

NS is not solved.

Say **H1** for the cylinder.

Do not merge with H1. Do not add \(K(t)\) to the PDE.
Do not write “almost proved.”
