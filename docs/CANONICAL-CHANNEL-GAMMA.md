# Canonical channel: γ = (Δ, σ)

28 September 2026.
**Sprint 01 source of truth. Coefficient identities certified.
Not a close. NS is not solved. v2 not run. DA-NS-2 open.**

Exact full-flow source: [`DA-NS-SPRINT-01-PHASE-LOCK-AND-FULL-HELICAL-FLOW-2026-09-07.md`](DA-NS-SPRINT-01-PHASE-LOCK-AND-FULL-HELICAL-FLOW-2026-09-07.md).
Definitions Lock heterochiral split remains: homochiral is a different object.

Code:

- `scripts/ns_attacks/helical.py` — helical frame, Waleffe \(g_W\)
- `scripts/ns_attacks/channel_coefficient.py` — \(p+q=k\) identity onto `g_ordered`
- `scripts/ns_attacks/full_flow.py` — official \(k+p+q=0\) algebra, conjugation, charge
- `scripts/run_channel_coefficient_identity.py` — runner
- `results/channel_coefficient_identity.json`
- `results/full_flow_identity.json`
- `results/canonical_24_channel_payload.json`

---

## 1. What was wrong with the cyclic-output stamp

The object

\[
(T;\; x,y\to o;\; s,s,-s)
\]

with three cyclic “output channels” is **not** the
physical helical channel. Sprint 01 writes every energy
transfer of a real geometric triad \(\Delta=(k,p,q)\)
with \(k+p+q=0\) at once:

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

\[
\boxed{\gamma=(\Delta,\sigma)}
\]

\[
\boxed{
k+p+q=0
}
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

Frames are consistent under \(k\mapsto -k\):

\[
h_s(-k):=\overline{h_s(k)}
\]

on a lexicographic hemisphere. Independent frames on
\(\pm k\) break mixed-amplitude \(\Theta\) reconstruction.

On each \(\gamma\):

* \(o\) is the unique odd-helicity radius, \(i,j\) the other two,
* \(\displaystyle A_\gamma=\frac{(i+o)(j+o)}{2o}\),
* one channel coefficient \(g_{\Delta,\sigma}\),
* \(\displaystyle
  \Theta_{\Delta,\sigma}
  =\operatorname{Re}\bigl(g_{\Delta,\sigma}\,
  \overline{a_k^{s_k}a_p^{s_p}a_q^{s_q}}\bigr)\),
* \(Q_3=2o\,\tau_o\) is the **three-mode reduction**,
* \(\displaystyle
  Q_{\mathrm{abs}}
  =\sum_{m\in\Delta,\,\pm}\lvert m\rvert\,\tau_m
  =2Q_3\)
  is the six-mode charge of Sprint 01 §7,
* \(\displaystyle S_\Gamma=\sum_\gamma A_\gamma Q_{a,\gamma}\).

The old “one geometric representative plus all six
heterochiral sign triples” architecture matches this
ontology. Its old \(24\times 12\) numerics are **not**
rehabilitated.

---

## 3. Three kernels, two representatives

Helical frame (already locked in `helical.py`):

\[
h_k^s=\frac{e_1+is\,e_2}{\sqrt{2}},\qquad
\hat k\times e_1=e_2,\qquad
i\,k\times h_k^s=s\lvert k\rvert\,h_k^s.
\]

On the official \(k+p+q=0\) representative,

\[
G_0
=
\bigl(h_p^{s_p}\times h_q^{s_q}\bigr)\cdot h_k^{s_k}.
\]

On the flipped \(p+q=k'\) representative \(k'=-k\),
\(s_{k'}=s_k\),

\[
\begin{aligned}
G_{\mathrm{cross}}(p,q,k')
&=
\bigl(h_p^{s_p}\times h_q^{s_q}\bigr)\cdot\overline{h_{k'}^{s_k}}
=G_0,\\
g_{\mathrm{ordered}}
&=
(q\cdot h_p^{s_p})
\bigl(h_q^{s_q}\cdot\overline{h_{k'}^{s_k}}\bigr),\\
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
channel is still live (\(G_0\neq 0\), transfers on the
\(p\) and \(q\) legs). That is why \(g_W\) cannot be
\(g_{\Delta,\sigma}\).

---

## 4. The last identity, still exact

**EXACT** (90° rotation in the \(p\)-plane):

\[
\boxed{
(\hat p\times q)\cdot h_p^{s_p}
=
i\,s_p\,(q\cdot h_p^{s_p})
}
\]

**EXACT, certified** on the parallelogram plus five
scalene probes, six heterochiral \(\sigma\), three
reference axes (54 samples × 3 axes) on \(p+q=k\),
and independently on the \(k+p+q=0\) flip:

\[
\boxed{
g_{\mathrm{ordered}}
=
-i\,s_p\,\lvert\mu\rvert\,
G_0
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
\arg G_0
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
times Vandermonde sign, not a triangle phase.

---

## 5. Operational \(g\) versus the frame kernel \(G_0\)

The scalar that actually enters \(\Theta=\operatorname{Re}(g\,\overline{aaa})\)
is the energy-fitted \(g\). Two samples (\(aaa=1\) and
\(aaa=-i\)) determine \(\operatorname{Re}g\) and
\(\operatorname{Im}g\).

Certified on the seed plus the four parallelogram triads:

\[
\lvert g_{\mathrm{energy}}\rvert=\lvert G_0\rvert.
\]

The unimodular ratio

\[
U=\frac{g_{\mathrm{energy}}}{G_0}
\]

is a **frame/triangle convention**, not identically \(+1\).
On the default axis \((0,0,1)\) with consistent frames:

| \(\Delta\) | \(U\) |
|---|---|
| T1 | \(+1\) (\(\arg 0\)) |
| T2 | \(-1\) (\(\arg\pi\)) |
| T3 | \(\pm i\) (\(\arg\pm\pi/2\)) |
| T4 and Sprint 01 seed | \(\arg\in\{\pm\pi/6,\;\pm 5\pi/6\}\) |

T1/T2 odd-\(k\) channels are k-leg Vandermonde zeros:
energy-fit of the \(k\)-leg is skipped; \(\Theta\) is
read from the live \(p\) and \(q\) legs.

**Do not treat \(U=1\) as universal.** Loop-gauge
\(b_\gamma\) must use the energy-fit \(g\), or apply
\(U\) to \(G_0\) explicitly. A uniform \(\pi/2\) still
drops from every cycle holonomy because
\(c\in\ker(B^T)\Rightarrow c^T\mathbf{1}=0\). A
triangle-dependent \(U\) is a known convention, not a
new geometric defect, provided one kernel is used
consistently.

Dropping the conjugation in \(\Theta\) assigns the
wrong phase to mixed-amplitude channels. The residual
without conjugation is \(O(1)\) on the mixed test
sample; with conjugation it is \(\sim 10^{-16}\).

---

## 6. Centered drift and heterochiral charge

On a real six-mode channel,

\[
\boxed{
\mathfrak T_{c,\Delta,\sigma}
=2C_{\Delta,\sigma}\Theta_{\Delta,\sigma}
}
\]

\[
C_{\Delta,\sigma}
=-(a-b)(b-c)(c-a)
\bigl(a^2+b^2+c^2+ab+bc+ca-\Lambda\bigr).
\]

Heterochiral reduction (Sprint 01 §7):

\[
\boxed{
\mathfrak T_{c,\Delta}^{\mathrm{het}}
=R_\Lambda(i,j;o)\,Q_{\mathrm{abs},\Delta}
}
\]

\[
R_\Lambda(i,j;o)
=\frac{(i+o)(j+o)}{2o}\,(H_{ij\lvert o}-\Lambda),
\qquad
H_{ij\lvert o}=i^2+j^2+o^2+ij-o(i+j).
\]

Reality gives \(\tau_{-m}=\tau_m\), so
\(Q_{\mathrm{abs}}=2Q_3\). These identities are certified
on 30 heterochiral samples (seed + parallelogram × 6)
to \(\sim 10^{-16}\). They certify the finite algebra;
they do not prove DA-NS-2.

---

## 7. Canonical 24-channel payload

Geometric \(\Delta\): the locked LOOP-GAUGE
parallelogram, rewritten as \(k+p+q=0\):

\[
\begin{aligned}
T_1&: (-1,-1,0)+(1,0,0)+(0,1,0)=0,\\
T_2&: (-1,0,-1)+(1,0,0)+(0,0,1)=0,\\
T_3&: (-1,-1,-1)+(1,1,0)+(0,0,1)=0,\\
T_4&: (-1,-1,-1)+(1,0,1)+(0,1,0)=0.
\end{aligned}
\]

\[
\boxed{4\text{ geometric }\Delta\times 6\text{ heterochiral }\sigma=24\text{ channels}}
\]

Generated from scratch in
`results/canonical_24_channel_payload.json`.
Each row stores \(A_\gamma\), \(G_0\), `g_ordered`,
the energy-fit \(g\) and \(U\) when the k-leg
Vandermonde is live, and the odd-leg identification.

The old \(24\times 12\) table is not this object and
is not reused.

v2 is not run.

---

## Status

| Claim | Status |
|---|---|
| Channel ontology \(\gamma=(\Delta,\sigma)\) | **STAMPED** |
| Official representative \(k+p+q=0\) | **STAMPED** |
| Six heterochiral \(\sigma\), not 3×2 cyclic outputs | **STAMPED** |
| \(\Theta=\operatorname{Re}(g\,\overline{aaa})\), conjugation essential | **CERTIFIED** |
| \(\mathfrak T_c=2C\Theta\), \(\mathfrak T_c^{\mathrm{het}}=R_\Lambda Q_{\mathrm{abs}}\) | **CERTIFIED** |
| \(Q_{\mathrm{abs}}=\sum_{\pm}\lvert m\rvert\tau_m=2Q_3\) | **STAMPED** |
| \(g_{\mathrm{ordered}}=-i s_p\lvert\mu\rvert G_0\) | **CERTIFIED** |
| \(\lvert g_{\mathrm{energy}}\rvert=\lvert G_0\rvert\); \(U\) not identically \(+1\) | **CERTIFIED** |
| \(g_W\) is the k-leg fold, not the channel | **STAMPED** |
| Canonical 24-channel payload (\(k+p+q=0\)) | **GENERATED** |
| DA-NS-2 / v2 / primitive test | **OPEN / NOT RUN** |

NS is not solved.
