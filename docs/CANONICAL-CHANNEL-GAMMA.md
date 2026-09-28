# Canonical channel: γ = (Δ, σ)

28 September 2026.
**Coefficient identity, then the channel stamp.
Not a close. NS is not solved. v2 not run.**

Exact full-flow source of the three-transfer identity:
the 7 September helical write-up (phase-lock and full
helical flow). Definitions Lock heterochiral split
remains: homochiral is a different object.

Code:

- `scripts/ns_attacks/helical.py` — helical frame, Waleffe \(g_W\)
- `scripts/ns_attacks/channel_coefficient.py` — identity and 24-channel catalog
- `scripts/run_channel_coefficient_identity.py` — runner
- `results/channel_coefficient_identity.json`
- `results/canonical_24_channel_payload.json`

---

## 1. What was wrong with the cyclic-output stamp

The object

\[
(T;\; x,y\to o;\; s,s,-s)
\]

with three cyclic “output channels” is **not** the
physical helical channel. The older exact derivation
writes every energy transfer of a real geometric triad
\(\Delta=(k,p,q)\) at once:

\[
\boxed{
(\tau_k,\tau_p,\tau_q)
=
\Theta_{\Delta,\sigma}
\,(b-c,\; c-a,\; a-b)
}
\]

\[
a=s_k\lvert k\rvert,\qquad
b=s_p\lvert p\rvert,\qquad
c=s_q\lvert q\rvert.
\]

One coefficient, one raw monomial \(W_{\Delta,\sigma}\),
three components of the **same** signed channel.
Choosing a different output does not create a new
channel. Cyclically reevaluating a coupling three
ways would treat one physical interaction as three
independently phased ones.

---

## 2. Frozen channel rule

For a geometric triangle \(\Delta\), choose its
deterministic ordered representative **once**,
\(p+q=k\). Then

\[
\boxed{\gamma=(\Delta,\sigma)}
\]

\[
\boxed{
\sigma=(s_k,s_p,s_q)\in\{\pm1\}^3
\text{ heterochiral}
}
\]

Six heterochiral \(\sigma\) per \(\Delta\):

* three choices of odd-helicity leg,
* two choices of overall sign,

namely

\[
\{++-,\;--+ ,\;+-+,\;-+-,\;-++,\;+--\}.
\]

Those are six **signed helical channels**, not
three cyclic output rewrites times two.

On each \(\gamma\):

* \(o\) is the unique odd-helicity radius, \(i,j\) the other two,
* \(\displaystyle A_\gamma=\frac{(i+o)(j+o)}{2o}\),
* one channel coefficient \(g_{\Delta,\sigma}:=G_{\mathrm{cross}}\),
* one phase invariant \(\chi_\gamma=\arg G_{\mathrm{cross}}\),
* \(Q_{a,\gamma}=2o\,\tau_o\),
* \(\displaystyle S_\Gamma=\sum_\gamma A_\gamma Q_{a,\gamma}\).

The old “one geometric representative plus all six
heterochiral sign triples” architecture matches this
ontology. Its old \(24\times 12\) numerics are **not**
rehabilitated. This page only freezes the channel
object and the coefficient map.

---

## 3. Three kernels on the frozen representative

Helical frame (already locked in `helical.py`):

\[
h_k^s=\frac{e_1+is\,e_2}{\sqrt{2}},\qquad
\hat k\times e_1=e_2,\qquad
i\,k\times h_k^s=s\lvert k\rvert\,h_k^s.
\]

\[
\begin{aligned}
G_{\mathrm{cross}}
&=
\bigl(h_p^{s_p}\times h_q^{s_q}\bigr)\cdot\overline{h_k^{s_k}},\\
g_{\mathrm{ordered}}
&=
(q\cdot h_p^{s_p})
\bigl(h_q^{s_q}\cdot\overline{h_k^{s_k}}\bigr),\\
g_W
&=
\tfrac12(s_p\lvert p\rvert-s_q\lvert q\rvert)\,
G_{\mathrm{cross}}.
\end{aligned}
\]

\(g_W\) is the quantity `geometric_coupling` in
`helical.py`. It is the **k-leg fold** of the channel:
it already contains the Vandermonde factor \(b-c\).
When \(\lvert p\rvert=\lvert q\rvert\) and the odd
leg is \(k\), \(b-c=0\) so \(g_W=0\) while the
channel is still live (\(G_{\mathrm{cross}}\neq 0\),
transfers on the \(p\) and \(q\) legs). That is why
\(g_W\) cannot be \(g_{\Delta,\sigma}\).

The full-flow coefficient is the common scalar in
\(\Theta_{\Delta,\sigma}\). On the frozen
representative that scalar is \(G_{\mathrm{cross}}\).

\[
\boxed{g_{\Delta,\sigma}=G_{\mathrm{cross}}}
\]

---

## 4. The last identity

**EXACT** (90° rotation in the \(p\)-plane):

\[
\boxed{
(\hat p\times q)\cdot h_p^{s_p}
=
i\,s_p\,(q\cdot h_p^{s_p})
}
\]

because \(\hat p\times h_p^{s_p}=-i s_p h_p^{s_p}\).
Hence \(q\cdot h_p^{s_p}\) carries a universal factor
\(-i s_p\) relative to the rotated real pairing.

**EXACT, certified** on the parallelogram plus five
scalene probes, six heterochiral \(\sigma\), three
reference axes (54 samples × 3 axes):

\[
\boxed{
g_{\mathrm{ordered}}
=
-i\,s_p\,\lvert\mu\rvert\,
G_{\mathrm{cross}}
}
\]

with \(\lvert\mu\rvert>0\) a real shape factor,
axis-invariant to machine precision. Shape enters
**only** \(\lvert\mu\rvert\), never the phase of the
ratio.

Consequently

\[
\boxed{
\arg g_{\mathrm{ordered}}
-
\arg G_{\mathrm{cross}}
=
-\,s_p\,\frac{\pi}{2}
}
\]

and, whenever \(g_W\neq 0\),

\[
\frac{g_W}{g_{\mathrm{ordered}}}
=
\frac{i\,(b-c)}{2 s_p\lvert\mu\rvert}
\in i\mathbb{R}.
\]

The imaginary sign is \(\mathrm{sign}((b-c)/s_p)\), a label
times Vandermonde sign, not a triangle phase. The earlier
“always \(+i\)” reading was a sample bias (it holds when
\((b-c)/s_p>0\), and fails when the odd-\(k\) legs have
\(\lvert p\rvert<\lvert q\rvert\)).

The map from the full-flow coefficient onto
`g_ordered(p,q,k,s_p,s_q,s_k)` is therefore a
**known** element of \(i\mathbb{R}\), labelled by
the frozen \(p\)-helicity, not a triangle-dependent
geometric phase.

---

## 5. What this does to \(b_\gamma\)

Loop-gauge targets use \(\chi_e=\arg g_e\).
Incidence \(B\) has rows \(e_p+e_q-e_k\), so
\(B\mathbf{1}_{\mathrm{modes}}=\mathbf{1}_{\mathrm{edges}}\).
For every cycle \(c\in\ker(B^T)\),

\[
\boxed{c^T\mathbf{1}=0}.
\]

A **uniform** \(\pi/2\) shift of every channel
argument drops out of every holonomy \(\Omega_c=c^T b\).

A **swap** \(\arg g_{\mathrm{ordered}}\leftrightarrow
\arg G_{\mathrm{cross}}\) without the label correction
shifts

\[
\Delta\Omega_c
=
-\frac\pi2\sum_e c_e s_{p_e}.
\]

That is a known helicity-label convention, not a new
shape defect. On this catalog a common \(\sigma\)-slot
around the parallelogram has \(s_{p_e}\) constant, so
\(\sum c_e s_{p_e}=s_p\sum c_e=0\) and \(\Omega_c\)
does not move. Mixed-\(\sigma\) loops must apply the
correction explicitly.

Nothing here injects an unexpected geometric phase
into \(b_\gamma\), provided one kernel is used
consistently (this page: \(G_{\mathrm{cross}}\)) or
the \(-s_p\pi/2\) translation is kept when reading
`g_ordered`.

---

## 6. Canonical 24-channel payload

Geometric \(\Delta\): the locked LOOP-GAUGE
parallelogram, four ordered representatives

\[
\begin{aligned}
T_1&: (1,0,0)+(0,1,0)=(1,1,0),\\
T_2&: (1,0,0)+(0,0,1)=(1,0,1),\\
T_3&: (1,1,0)+(0,0,1)=(1,1,1),\\
T_4&: (1,0,1)+(0,1,0)=(1,1,1).
\end{aligned}
\]

\[
\boxed{4\text{ geometric }\Delta\times 6\text{ heterochiral }\sigma=24\text{ channels}}
\]

Generated from scratch in
`results/canonical_24_channel_payload.json`.
Each row stores \(A_\gamma\), \(G_{\mathrm{cross}}\),
`g_ordered`, \(g_W\), \(\lvert\mu\rvert\), the
phase invariant \(\arg G_{\mathrm{cross}}\), and the
odd-leg identification.

The old \(24\times 12\) table is not this object and
is not reused.

v2 is not run.

---

## Status

| Claim | Status |
|---|---|
| Channel ontology \(\gamma=(\Delta,\sigma)\) | **STAMPED** |
| Six heterochiral \(\sigma\), not 3×2 cyclic outputs | **STAMPED** |
| \(g_{\Delta,\sigma}=G_{\mathrm{cross}}\) | **STAMPED** |
| \(g_{\mathrm{ordered}}=-i s_p\lvert\mu\rvert G_{\mathrm{cross}}\) | **CERTIFIED** |
| \(g_W\) is the k-leg fold, not the channel | **STAMPED** |
| Phase offset does not inject unexpected holonomy | **STAMPED** |
| Canonical 24-channel payload | **GENERATED** |
| v2 / primitive test / \(T_c\) bound | **NOT RUN** |

NS is not solved.
