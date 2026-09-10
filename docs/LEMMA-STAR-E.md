# Lemma★ — isolated closing triad (Attack 8)

10 September 2026. Isolated triangle. **Not a proof. NS not solved.**

Locked form: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).
Probe: `python3 scripts/ns_attacks/attack8_three_shell.py`

Three precision corrections, then the score.

---

## It is two Fourier keys that fail, not two shells

The dead control was \(k_0\) and \(k_0+e\) only: two
**keys**, no place for \(B(v_0,v_1)\) to land, \(T_c=0\).

Two **shells** can support a live closed triad. Example:
\[
p=(1,1,0),\qquad q=(1,-1,0),\qquad p+q=(2,0,0),
\]
with \(|p|^2=|q|^2=2\) and \(|p+q|^2=4\). Three keys, two
eigenvalues, \(T_c\) live (\(\mathcal R_\star\approx 0.031\)
on a phase search). Checked: Attack 9.

The Attack 8 candidate is three keys
\(k_0\), \(k_0+e\), \(2k_0+e\) with
\(k_0+(k_0+e)=2k_0+e\). That can sit on two shells or three.
The dummy is two keys, not two shells.

---

## \(e\to 0\) is not a literal limit on \(\mathbb Z^3\)

The rigorous near-shell limit is
\[
\frac{|e|}{|k_0|}\to 0
\]
by **fixing** \(e\) and sending \(|k_0|\to\infty\).
Varying \(|e|\) at fixed \(k_0=(6,0,0)\) is a different cut.

---

## A frozen ray is not a supremum

Decay of \(\mathcal R_\star\) along one fixed polarization
and relative-amplitude ray does **not** eliminate
\(|e|/|k_0|\to 0\) unless the polarization and
relative-amplitude supremum is recomputed at every
\(|k_0|\).

On the isolated triangle, that supremum was recomputed
(\(k_0=(N,0,0)\), \(e=(0,1,0)\)). It still fell
(\(\approx 0.053\) at \(N=2\) to \(\approx 8.6\times 10^{-4}\)
at \(N=16\)). Frozen-ray decay is weaker evidence; the
re-optimized isolated triangle still did not kill.

Dilation of a *fixed shape* (\(e\mapsto ne\),
\(\Lambda\mapsto n^2\Lambda\)) remains exactly flat
(\(\mathcal R_\star=1.935\times 10^{-3}\)).

Parallel \(e=(j,0,0)\) at one polarization gave \(T_c=0\).
Accident, not a bound.

---

## Frozen perp-\(e\) table (one ray, not the limit)

Carrier \(k_0=(6,0,0)\), amplitudes \((1,0.2,0.05)\).
\(e=(0,j,0)\). This is **not** \(|e|/|k_0|\to 0\).

| \(|e|\) | \(\mathcal R_\star\) | consecutive exponent |
|---|---|---|
| 1 | \(3.31\times 10^{-4}\) | |
| 2 | \(9.43\times 10^{-4}\) | \(+1.51\) |
| 3 | \(1.46\times 10^{-3}\) | \(+1.09\) |
| 4 | \(1.82\times 10^{-3}\) | \(+0.75\) |
| 6 | \(1.93\times 10^{-3}\) | \(+0.16\) |
| 8 | \(1.56\times 10^{-3}\) | \(-0.74\) |

Saturates, then rolls over. Phase/amplitude search on the
same keys stayed at \(\mathcal R_\star\le 0.073\). Evidence
only.

---

## Status

- isolated closed triad tested: no kill
- dilation confirmed exactly neutral
- fixed additive offset becomes safer on the tested ray
- polarization zero is accidental
- the live falsification target is a growing coherent
  triad packet or HH→L fan (same-shell scored: no kill)
- the uniform global triadic bound remains completely open

A frozen ray is not the \(|e|/|k_0|\to 0\) supremum. The
live target is not more isolated triangles. Packets:
[`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).

Do not merge with H1. Do not add \(K(t)\) to the PDE.
Do not write “almost proved.”
