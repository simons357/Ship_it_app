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

## Blocked exactly here

Uniform pre-Young
\[
|\mathfrak T_c|\le C\|u\|_2 X\Lambda
\]
with \(C\) independent of \(u\) is **dead**. Attack 6: on the
scaled triad \(k\mapsto sk\),
\(\lvert T_c\rvert/(\|u\|_2 X\Lambda)\simeq 0.158\,s\to\infty\).
Ordinary 3D product / Agmon estimates do not close the other door
either.

**Live door (door 2):**
\[
|\mathfrak T_c|\le C_* X^{3/2}\Lambda
\]
with \(C_*\) absolute. On that same family the ratio is
\(\simeq 0.0404\), independent of \(s\) and of amplitude.
One family is not a proof. HH→L is still the gap.

If \(C_*\) sits, then \(K\le C_*\sqrt{X}\) and Leray plus
Cauchy–Schwarz give \(\int_0^T\sqrt{X}<\infty\), hence DA-NS-2
on every finite interval **in this packaging**. Not proved.

File: [`LEMMA-STAR-NEXT.md`](LEMMA-STAR-NEXT.md).

---

## Five-lane drill (done 1) — 10 September 2026

| Lane | Verdict |
|---|---|
| K=0 form \(\mathfrak T_c\le\theta\nu\mathcal D_s\) | **Dead.** Ratio \(\lvert T_c\rvert/\mathcal D_s\) blows with amplitude. |
| Lemma★ / geometric \(C_0\) | **Survives numeric kill only.** Max \(\lvert R_{\mathrm{pre}}\rvert\approx 5.09\) on 978 samples. Not \(\to\infty\). **Not a proof.** |
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

Prove or kill \(|T_c|\le C_* X^{3/2}\Lambda\) with HH→L
controlled. Uniform pre-Young \(C\) is off (Attack 6).
Do not revive K=0. Do not cash a triad ratio as \(C_*\).

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
