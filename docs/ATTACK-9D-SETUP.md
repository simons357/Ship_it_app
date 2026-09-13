# Attack 9D — the call (do not start 9D)

12 September 2026.
**Not a close. Unrestricted ★ is killed.
Exact-shell bound claimed. NS is not solved.**
This page answers the setup question.
It does not reopen 9D as a live script.

Locked files:
[`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md),
[`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md),
[`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md),
[`math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md).

---

## The call

Do **not** implement Attack 9D.
Do **not** build a ★ sentence from the
HH→L fan numbers.

Two writings of “9D” already died:

1. Designed \(\Theta(m^2)\) locked-phase subset
   = Freiman-AP. Already ran (wide / narrow AP).
   \(\mathcal D_s\) wins. Dead.
2. Screenshot: \(\Theta(m^2)\) pairs onto one
   output, or a fixed number of outputs.
   Analytically excluded. Per output,
   \(p+q=k\) gives at most \(m\) pairs.
   \(K_{\alpha,\beta}\le 16s\). Fixed \(s\)
   cannot unbound \(K\).

What is still live on this lane is **not**
a new 9D object. It is growing **output**
occupancy \(s\) on the **9B family**.

---

## What \(B\) is

Same bilinear as everywhere on this desk:

\[
B(w,w)=P\bigl[(w\cdot\nabla)w\bigr],
\qquad
\Pi_\beta=\text{spectral projector onto shell }\beta.
\]

The field in the displayed bound is
\(\Pi_\beta B(w,w)\). It is **not** a new
9D symbol. It is the 9B closer.

9B family:

\[
v_\varepsilon=w_\alpha+\varepsilon z_\beta,
\qquad
Aw_\alpha=\alpha w_\alpha,
\qquad
Az_\beta=\beta z_\beta,
\qquad
z_\beta\parallel\Pi_\beta B(w_\alpha,w_\alpha).
\]

Boxed 9B quotient:

\[
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]

The inequality you wrote,

\[
\|\Pi_\beta B(w,w)\|_2
\le
C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\]

is the **correct uniform 9B target**.
It holds for all such \(w\) if and only if
\(\sup K_{\alpha,\beta}<\infty\).
On aligned, sign-selected \(z_\beta\),
\(\mathcal R_\star(v_\varepsilon)\to K_{\alpha,\beta}(w)\)
as \(\varepsilon\to 0\). For arbitrary
\(z_\beta\), the limit is the projection
against \(B(w,w)\), not necessarily \(K\).

A bound
\(\|\Pi_\beta B\|_2\le C\alpha\|w\|_2^2\)
is the **wrong packaging**: it leaves
\(\sqrt{\beta}\) and does not control \(K\).

---

## Same \(B\), not the same family as HH→L

Attack 12 uses the same operator \(B\).
The **field and the quotient are different**.

| | 9B / growing \(s\) | Attack 12 HH→L fan |
|---|---|---|
| Field | Exact-shell \(w_\alpha\) plus \(\varepsilon\)-closer on \(\beta\), aligned with \(\Pi_\beta B(w_\alpha,w_\alpha)\) | Partners of a low key (or the whole low shell) on a high sphere \(\alpha\) |
| Reported number | \(K_{\alpha,\beta}\), or \(\mathcal R_\star\to K\) | Full \(\mathcal R_\star(v)\) |
| Scored behaviour | Finite samples: aligned \(\max K\approx 0.641\) at \((4,8)\); counting \(\max K\approx 0.506\), \(\max\sqrt{K}\approx 0.711\); grow-\(s\) random pol \(\max K\approx 0.456\) at \((16,32)\), \(\max s=192\) | \(\mathcal R_\star\sim\beta/\alpha\); largest \(\approx 0.71\) at \(\alpha=5\), \(\beta=4\); falls as \(\alpha/\beta\) grows |
| Why | Frequency factors in \(K\) | Vertex carries \(\sqrt{\beta}\), not \(\sqrt{\alpha}\) |

Do **not** merge Attack 12’s \(0.71\) with
the counting-lock \(\sqrt{K}\approx 0.711\).
Different objects. Neither is \(C_0\).
Neither is \(\mathcal R_\star\to\infty\).
The write-up example for exact-shell
\(K\) is the three-shear field
\(w=(\sin y,\sin z,\sin x)\),
\(K_{1,2}=2/3\) by hand, not those
sweep maxima
([`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md)).

HH→L is a scored non-kill. It is not the
9B closer, and it is not 9D.

---

## Growth law — what is locked, what is open

No exponent \(s=s(\alpha,\beta)\) or
\(m=m(\alpha,\beta)\) is already a theorem.

**Locked (analytic).**

- One output \(k\): at most \(m\) ordered
  pairs. \(\Theta(m^2)\) on a fixed output
  set cannot happen.
- If \(\Pi_\beta B(w,w)\) occupies \(s\)
  keys and both inputs sit on shell
  \(\alpha\), then \(\beta\le 4\alpha\) and
  \[
  \|\Pi_\beta B(w,w)\|_2^2
  \le s\,\beta\,\|w\|_2^4,
  \qquad
  K_{\alpha,\beta}\le 16s.
  \]
  Phases do not matter for that upper bound.
- **Fixed \(s\)**: \(K\) is uniformly
  bounded. That kill shape is closed.
- Designed \(\Theta(m^2)\) **subset**
  (Freiman-AP): already dead as a new
  object. \(\mathcal D_s\) wins.

**Open (this is the remaining 9B test).**

Growing **input and output** support,
complex polarizations, frequency factors
kept. The \(16s\) line does **not** give
a uniform \(C_0\) if \(s\) may grow.
Finding whether \(s\) can grow fast
enough to send \(K\to\infty\) (or a
family with \(\mathcal R_\star\to\infty\))
**is** the open part. It is not a
missing 9D exponent sitting in a stub.

The \(m^{1/2}\) heuristic has no lattice
home **per output**. Natural same-shell
closures are \(O(m)\), not \(O(m^2)\)
(Attack 11 / 9C). Route A continuum
\(I\ll m^{4/3}\) is not a lattice theorem.
X1–X4/X6 still MISSING.

---

## Order (do not guess 9D)

1. **Do not start 9D.** Both writings are
   dead. The stub
   `attack9d_theta_m2_locked_phase.py`
   is not a hole to fill.
2. **Do not** turn Attack 12’s
   \(\mathcal R_\star\sim\beta/\alpha\)
   table into a ★ sentence. That table is
   a non-kill. Flagging extrapolations
   does not make it a proof.
3. Primary on this leftover is Need★:
   signed dual on HH→L after gap-cancel.
   Still **MISSING.**
   [`NEED-STAR-HH-L-DUAL.md`](NEED-STAR-HH-L-DUAL.md).
4. Grow \(s\) is secondary pressure.
   Same \(B(w,w)\). Keep \(|k|\).
   Report \(K_{\alpha,\beta}\) and pairing.
   A finite max only raises
   \(C_{\mathrm{geom}}\).
   Live write:
   [`ATTACK-9D-GROW-S.md`](ATTACK-9D-GROW-S.md).
   Probe:
   `scripts/ns_attacks/attack9b_grow_s.py`,
   `scripts/ns_attacks/attack9b_output_counting.py`,
   `scripts/ns_attacks/attack9b_exact_shell_K.py`.
   Do not overwrite
   `scripts/ns_attacks/stokes_moments.py`.
5. The ★ reason is written as a map:
   [`LEMMA-STAR-REASON.md`](LEMMA-STAR-REASON.md).
   Not a theorem. Do not turn Attack 12
   into that sentence.
6. H1 on the cylinder is named. The
   write sits. It is not a theorem.
   Do not start it from ABC_λ. Do not
   glue.

NS not solved. ★ open.
