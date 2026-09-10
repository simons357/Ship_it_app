# Lemma★ — boxed ratio \(\mathcal R_\star\)

10 September 2026. Exact reduction. **Not a proof. NS not solved.**

Locked statement: [`LEMMA-STAR.md`](LEMMA-STAR.md).
Probe: `python3 scripts/ns_attacks/attack7_rstar.py`

---

## The reduction (sits as algebra)

Write \(u=av\), \(a>0\). Then \(T_c\sim a^3\), \(\mathcal D_s\sim a^2\),
\(\Lambda\) is amplitude-invariant, and \(X\Lambda=Y\).

Optimizing Lemma★ over \(a>0\) converts it into the viscosity-free
geometric inequality
\[
\bigl(T_c(v)_+\bigr)^2
\le
4\theta C_0\,
\mathcal D_s(v)\,
\|v\|_2^2\,Y(v).
\]
(\(\mathcal D_s=D_s=Z-\Lambda Y\). Same object.)

Thus the decisive dimensionless ratio is
\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}
{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

- If \(\sup_v\mathcal R_\star(v)=\infty\), Lemma★ is dead.
- If \(\mathcal D_s(v)=0\) while \(T_c(v)>0\), it is dead immediately.
- A proof requires a uniform bound on this ratio from triadic
  geometry or cancellation.
- Numerically bounded samples remain evidence only.

Derivation (one line). After \(u=av\), ★ says
\(A+Ba^2-Ca\ge 0\) for every \(a>0\), with
\(A=\theta\nu\mathcal D_s(v)\),
\(B=C_0\nu^{-1}\|v\|_2^2 Y(v)\),
\(C=T_c(v)_+\).
The minimum is \(A-C^2/(4B)\). Nonnegativity is
\(C^2\le 4AB\), and \(\nu\) cancels.

\(C_0\) may depend on \(\theta\in(0,1)\). Finite \(\sup\mathcal R_\star\)
gives \(C_0(\theta)\ge(\sup\mathcal R_\star)/(4\theta)\). Unbounded
\(\mathcal R_\star\) kills every finite \(C_0\).

This boxed form **is** Lemma★. It is not a weaker restatement.
The Attack-2 remainder \(|T_c|\le C_* X^{3/2}\Lambda\) is a
different sufficient door for DA-NS-2. It is not this
reduction. Do not merge that \(C_*\) with \(C_{\star}\) below.

---

## What the statement means

Lemma★ is no longer a viscosity statement. It is a **shape**
statement.

**What ★ was claiming.** Stretching \(T_c\) is cubic in the
field. Spectral spread \(\mathcal D_s\) is quadratic.
Viscosity multiplies the spread and sits in the remainder as
\(1/\nu\). So the original line mixed three different scalings.
That makes it hard to see what would actually kill it.

**What \(u=av\) does.** Change only the size of a fixed shape
\(v\). Optimize over size. The worst size cancels \(\nu\).
What remains is
\[
(\text{stretching of the shape})^2
\le
(\text{one geometric constant})
\times
(\text{how spread the spectrum is})
\times
(\text{energy})
\times
Y.
\]
That is the boxed line. If it holds for every divergence-free
\(v\) on the torus, with one \(C_0(\theta)\), then the original
★ holds for every amplitude and every \(\nu\). If it fails for
even one shape, ★ is false.

**What \(\mathcal R_\star(v)\) is.** How much stretching that
shape gets per unit of spread, energy, and \(Y\). Pure geometry.
Same number for \(av\) as for \(v\). Independent of viscosity.

- If some shapes make \(\mathcal R_\star\) arbitrarily large,
  no finite \(C_0\) exists. ★ is dead.
- If \(\mathcal D_s=0\) (one Fourier shell) and \(T_c>0\)
  (it still stretches), ★ is dead on that field. A pure single
  shell does **not** do that: both sides vanish. The live kill
  would be an almost-single-shell field that still stretches.
- If every shape has \(\mathcal R_\star\) below one number,
  that number *is* ★ (up to \(4\theta\)).
- A list of fields with small \(\mathcal R_\star\) is not that
  number. It is only that those particular shapes did not kill
  it.

**What a proof would have to be.** A reason, from how triads
add, that stretching cannot get large unless the spectrum also
spreads or the phases cancel. High-high \(\to\) low is the
channel that could refuse that. That reason is not written.
NS is not solved.

---

## Scale-invariant trilinear form (live fork)

The entire problem is now a scale-invariant trilinear shape
estimate.

Centered identities (sit):
\[
T_c(v)
=
-\bigl\langle B(v,v),A(A-\Lambda)v\bigr\rangle,
\qquad
\mathcal D_s(v)
=
\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2^2.
\]
(\(T_c=M-\Lambda N\), \(\mathcal D_s=Z-\Lambda Y\). The second
line uses \(\Lambda=Y/X\).)

Lemma★ is equivalent to proving
\[
\bigl[-\langle B(v,v),A(A-\Lambda)v\rangle\bigr]_+
\le
C_{\star}\,
\|v\|_2\,\|Av\|_2\,
\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2
\]
for every smooth, mean-zero, divergence-free \(v\) on the
fixed torus, where
\[
C_{\star}^2=4\theta C_0.
\]
This \(C_{\star}\) **is** the boxed ratio:
\(C_{\star}=\sqrt{\sup\mathcal R_\star}\) when the sup is
finite. It is not the Attack-2 remainder \(C_*\) in
\(|T_c|\le C_* X^{3/2}\Lambda\).

This formulation makes three things transparent:

- A pure shell vanishes because \((A-\Lambda)v=0\).
- Multiplying \(v\) by an amplitude changes neither
  \(\mathcal R_\star\) nor the question.
- Uniform frequency dilation of a *fixed shape*
  (\(k\mapsto nk\) for every mode, so \(e\mapsto ne\) and
  \(\Lambda\mapsto n^2\Lambda\)) leaves \(\mathcal R_\star\)
  invariant. That is exact. It is **not** exact if \(\Lambda\)
  is held fixed as an additive shift while \(A\) scales as
  \(n^2\), and it is **not** exact for an additive lattice
  displacement \(e\) sent to large \(|k_0|\). Those
  sub-leading \(\Lambda\) corrections are the regime where a
  kill is most likely to hide. Hunt with \(|k_0|^2\)
  comparable to \(\Lambda\).

So the live fork is exact:

- \(\sup_v\mathcal R_\star(v)<\infty\) proves Lemma★.
- A near-shell or HH\(\to\)L sequence with
  \(\mathcal R_\star(v_n)\to\infty\) kills it.

The missing mathematical content is the uniform triadic
bound — not more viscosity bookkeeping, and not more
bounded numerical samples.

The first non-trivial family is the closing three-key
\(k_0\), \(k_0+e\), \(2k_0+e\). Two *Fourier keys* is not
that test. Two *shells* can be live. Attack 8:
[`LEMMA-STAR-E.md`](LEMMA-STAR-E.md). Packets: [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).

---

## Immediate kill does not fire on a single shell

If the field lives on one eigenvalue of \(A\), then
\(\mathcal D_s=0\) and \(T_c=M-\Lambda N=0\) identically
(\(M=\Lambda N\)). Checked on a two-mode unishell: both zero.
The “\(\mathcal D_s=0\) and \(T_c>0\)” kill needs a field that
is *not* monochromatic.

---

## What Attack 6 did *not* kill

Uniform pre-Young \(|T_c|\le C\|u\|_2 X\Lambda\) dies like \(s\).
On the same scaled triad, \(\mathcal R_\star\) is **flat**:
about \(2.26\times 10^{-4}\) at default phase, about \(0.022\)
at the best of 24 phases, independent of \(s=1\ldots 64\).
Killing the pre-Young form is not killing Lemma★.

Amplitude: \(\mathcal R_\star(av)=\mathcal R_\star(v)\). Checked.

---

## Still open

\(\sup\mathcal R_\star<\infty\) is Lemma★. It is not proved.
Lattice HH→L fan: \(\mathcal R_\star\sim\beta/\alpha\), no blow.
The uniform triadic bound is still the gap. Do not cash
\(0.71\) or \(0.022\) as \(C_0\). Numerically bounded samples
remain evidence only.

Do not merge with H1. Do not add \(K(t)\) to the PDE.
Do not write “almost proved.”
