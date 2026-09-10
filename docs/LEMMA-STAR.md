# Lemma★ — locked packaging

10 September 2026. Energy-budget writing of leftover (6).
**Hypothesis. Not proved. NS is not solved. Not “almost.”**

Drill: [PR 48](https://github.com/simons357/Ship_it_app/pull/48)
(`cursor/ns-five-lane-lemma-star-1390`).
Registry packaging: [PR 49](https://github.com/simons357/Ship_it_app/pull/49).

This is **not** H1 / \(A_{\mathrm{bad}}\). Same leftover
class as WRITE (6) and DA-NS-2. Different integral.
Do not merge with H, Lemma C, H1, H2, H3.
Do not weld SND, Route N, \(K(t)\), or \(Q_1\).

---

## The statement (not a theorem)

On divergence-free fields on \(\mathbb{T}^3\),
\(X=\|A^{1/2}u\|_2^2\), \(Y=\|Au\|_2^2\),
\(Z=\|A^{3/2}u\|_2^2\), \(\Lambda=Y/X\),
\(\mathcal D_s=Z-\Lambda Y\ge 0\),
\(\mathfrak T_c=\mathcal M-\Lambda\mathcal N\).

**Lemma★.** For every \(\theta\in(0,1)\) there is a
geometry-only \(C_0\) (independent of \(u,\nu\)) such that
\[
\mathfrak T_c
\le
\theta\nu(Z-\Lambda Y)
+C_0\nu^{-1}\|u\|_2^2\,X\Lambda.
\]

If this sits, \(\Lambda\) cannot blow in finite time
**in this packaging**, hence \(X\le\|u_0\|_2^2\Lambda\)
stays finite, hence global regularity on \(\mathbb{T}^3\)
**in this packaging**. The implication is the skeleton.
The inequality is the hole.

That is why, in this packaging, Lemma★ *is* the
unforced leftover (Fefferman (B) on the torus).
Naming the hole is not closing it.

---

## Exact reduction (algebra sits)

Write \(u=av\), \(a>0\). \(T_c\sim a^3\), \(\mathcal D_s\sim a^2\),
\(\Lambda\) amplitude-invariant, \(X\Lambda=Y\). Optimizing ★
over \(a>0\) converts it into the viscosity-free geometric
inequality
\[
\bigl(T_c(v)_+\bigr)^2
\le
4\theta C_0\,
\mathcal D_s(v)\,
\|v\|_2^2\,Y(v).
\]
Decisive ratio:
\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}
{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
\]
- If \(\sup_v\mathcal R_\star=\infty\), ★ is dead.
- If \(\mathcal D_s=0\) and \(T_c>0\), dead immediately
  (does not fire on a single shell: both vanish).
- A proof is a uniform bound on \(\mathcal R_\star\) from
  triadic geometry or cancellation.
- Numerically bounded samples remain evidence only.

File: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).

---

## Blocked exactly here

The exact equivalent of ★ is a uniform bound on
\(\mathcal R_\star\). Ordinary 3D product / Agmon estimates
do **not** give that from energy alone.

Five-lane rule: kill ★ with \(\mathcal R_\star\to\infty\),
or sustain numeric bounds and keep the analytic gap
explicit — **not** “almost proved.”

**Attack 6 (scored, not a new leftover).** Uniform pre-Young
\(|T_c|\le C\|u\|_2 X\Lambda\) is **dead**:
\(\lvert R_{\mathrm{pre}}\rvert\simeq 0.158\,s\) on the
scaled triad. That is not ★ dying. On the same family
\(\mathcal R_\star\) is flat (\(\sim 0.022\) at best phase).
The \(C_*\) remainder \(|T_c|\le C_* X^{3/2}\Lambda\) is a
different sufficient door for DA-NS-2, not this boxed
form. One family is not a proof. HH→L is still the gap.
File: [`LEMMA-STAR-NEXT.md`](LEMMA-STAR-NEXT.md).

---

## Five-lane drill (done 1) — 10 September 2026

| Lane | Verdict |
|---|---|
| K=0 form \(\mathfrak T_c\le\theta\nu\mathcal D_s\) | **Dead.** Ratio \(\lvert T_c\rvert/\mathcal D_s\) blows with amplitude. |
| Lemma★ / geometric \(C_0\) | **Survives numeric kill only.** The 978-sample max \(\lvert R_{\mathrm{pre}}\rvert\approx 5.09\) is the *dead* pre-Young ratio, not \(\mathcal R_\star\). On the scaled triad \(\mathcal R_\star\) stayed \(\sim 0.022\). Not \(\to\infty\). **Not a proof.** |
| HH→L | **Still the gap.** High triad is the HH channel. No analytic closure. |
| Stokes identities | Sit. \(\mathcal D_s\ge 0\). \(\theta\nu\mathcal D_s\) alone is not enough. |
| \(C_* X^{3/2}\Lambda\) remainder | Numeric support on tested families. Not a theorem. |

**Headline.** K=0 dead. Uniform pre-Young \(C\) dead (Attack 6:
\(\lvert R_{\mathrm{pre}}\rvert\simeq 0.158\,s\)). \(C_*\)
survives the scaled triad (\(\simeq 0.0404\)). HH→L still the
gap. NS not solved.

Do not cash a bounded ratio on a Galerkin sample as \(C_0\).
A family that did not blow is not a uniform geometric constant.

---

## Live door

The exact equivalent of ★ is a uniform bound on
\(\mathcal R_\star\) from triadic geometry or cancellation.
Uniform pre-Young \(C\) is off. \(C_*\) is a different door.
Do not revive K=0. Do not cash a triad \(\mathcal R_\star\)
as \(C_0\). Numerically bounded samples remain evidence
only. Do not write “almost proved.”

---

## Relation to the other maps

- **H1 = WRITE (6) = Lemma I on the ball.** Bad pairs,
  kernel \(|z|^{-3}\). Geometric path. Open.
  [`WRITE_6.md`](WRITE_6.md)
- **DA-NS-2.** \(\int K\,dt<\infty\) with
  \(K=[T_c-\theta\nu\mathcal D_s]_+/Y\). If Lemma★ sits,
  DA-NS-2 sits. Identities already have. The integral
  does not. [`DA-NS-2.md`](DA-NS-2.md)
- **Lemma C.** Good pairs. An *if*. Not ★.

Work one writing. Do not glue them into one object.
Do not add \(K(t)\) to the PDE. Do not retune nodes.

Packet: [`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md).
H-system: [`H-SYSTEM.md`](H-SYSTEM.md).
