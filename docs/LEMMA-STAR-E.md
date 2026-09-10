# Lemma★ — three-shell family (Attack 8)

10 September 2026. The first non-trivial test of \(\mathcal R_\star\).
**Not a proof. NS not solved.**

Locked form: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).
Probe: `python3 scripts/ns_attacks/attack8_three_shell.py`

---

## The candidate

Take three shells: \(k_0\) (carrier), \(k_0+e\), and
\(2k_0+e\), chosen so the triad
\(k_0+(k_0+e)=2k_0+e\) actually closes. Then
\(B(v_0,v_1)\) has a component on the third mode, so
\(T_c\) can be nonzero at order of the product of the two
off-shell amplitudes, while \(\mathcal D_s\) picks up both
displaced shells.

Two-shell (\(k_0\) and \(k_0+e\) only) is **not** this test.
On that control, \(T_c=0\).

---

## Scale invariance, flagged

Uniform frequency shift of a *fixed shape* is exact:
every mode \(k\mapsto nk\), so \(e\mapsto ne\) and
\(\Lambda\mapsto n^2\Lambda\). Then \(\mathcal R_\star\) is
flat. Checked: frozen three-shell with \(k_0=(N,0,0)\),
\(e=(0,N,0)\) gave \(\mathcal R_\star=1.935\times 10^{-3}\)
at every \(N=2,\ldots,12\).

That invariance is **not** exact if \(\Lambda\) is held as
an additive shift while \(A\) scales as \(n^2\), and it is
**not** exact for additive \(e\) sent to large \(|k_0|\).
Counterexample hunting should keep \(|k_0|^2\) comparable
to \(\Lambda\). The sub-leading \(\Lambda\) corrections are
the regime where a kill is most likely to hide.

Checked: frozen shape, \(e=(0,1,0)\) fixed, \(k_0=(N,0,0)\).
\(\mathcal R_\star\) *falls* like about \(|k_0|^{-2}\)
(exponents \(-1.1\) to \(-2.0\) as \(N=2\to 16\)). High
frequency with additive \(e\) is the wrong hunt.

---

## Exponents in \(e\) (frozen shape)

Carrier \(k_0=(6,0,0)\), relative amplitudes
\((1,0.2,0.05)\), one polarization. Perp \(e=(0,j,0)\):

| \(|e|\) | \(\mathcal R_\star\) | consecutive exponent |
|---|---|---|
| 1 | \(3.31\times 10^{-4}\) | |
| 2 | \(9.43\times 10^{-4}\) | \(+1.51\) |
| 3 | \(1.46\times 10^{-3}\) | \(+1.09\) |
| 4 | \(1.82\times 10^{-3}\) | \(+0.75\) |
| 6 | \(1.93\times 10^{-3}\) | \(+0.16\) |
| 8 | \(1.56\times 10^{-3}\) | \(-0.74\) |

No blow as \(e\to 0\). The lattice minimum \(|e|=1\) is the
*smallest* \(\mathcal R_\star\) on this ray, not the
largest. The ratio saturates then rolls over.

Parallel \(e=(j,0,0)\) gave \(T_c=0\) at this polarization.
That is an accident, not a bound. Same lesson as the frozen
fan.

A search over amplitudes and phases on the same keys stayed
at \(\mathcal R_\star\le 0.073\). Evidence only. Not \(C_0\).

---

## Verdict

Three-shell is the right family. Two-shell is dead as a
test. Additive high-frequency is the wrong hunt. This
sample did **not** kill Lemma★. The uniform triadic bound
is still the hole.

Do not merge with H1. Do not add \(K(t)\) to the PDE.
Do not write “almost proved.”
