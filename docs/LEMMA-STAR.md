# Lemma★ — locked packaging

10 September 2026. Energy-budget writing of leftover (6).
**Dead as a closer on ABC_λ.** Write-up \(\mathcal R_\star\sim\lambda^3\)
at \(\lambda=2,4,8,16\): `docs/CS-REMAINDER.md`.
Evaluator ≠ proof. **NS is not solved.**
H1 is a different integral and was **not** run on this field.

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
\(\mathcal D_s=Z-\Lambda Y=\|(A-\Lambda)A^{1/2}u\|_2^2\ge 0\),
\(\mathfrak T_c=\mathcal M-\Lambda\mathcal N
=-\langle B(u,u),A(A-\Lambda)u\rangle\).

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
**in this packaging**. The implication is one direction.
These files have **no converse** that global regularity
would force the uniform inequality on every smooth field.
Do not write “★ equivalent to global regularity.”
The inequality is the hole.

That is why, in this packaging, Lemma★ names the
unforced leftover (Fefferman (B) on the torus).
Naming the hole is not closing it.
Working claim:
[`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md).
Identities:
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Corrections:
[`LEMMA-STAR-CORRECTIONS.md`](LEMMA-STAR-CORRECTIONS.md).

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

Equivalent trilinear form (\(C_{\star}^2=4\theta C_0\)):
\[
\bigl[-\langle B(v,v),A(A-\Lambda)v\rangle\bigr]_+
\le
C_{\star}\,
\|v\|_2\,\|Av\|_2\,
\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2.
\]
Do not merge this \(C_{\star}\) with the Attack-2 remainder
\(|T_c|\le C_* X^{3/2}\Lambda\).

Meaning: a scale-invariant trilinear shape estimate, not a
viscosity statement.
File: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).

---

## Blocked exactly here

The exact form of ★ is a uniform bound on
\(\mathcal R_\star\). Ordinary 3D product / Agmon estimates
do **not** give that from energy alone. The older
“missing inequality” \(|T_c|\le C\|u\|_2 X^{3/2}\) is
**false as a universal estimate** (left \(a^3\), right
\(a^4\) under \(u=av\)). Discarded by algebra. Not an
open gap toward ★. HH→L remains diagnostic of channels.

Five-lane rule: kill ★ with \(\mathcal R_\star\to\infty\),
or sustain numeric bounds and keep the analytic gap
explicit — **not** “almost proved.”

**Attack 6 (scored, not a new leftover).** Uniform pre-Young
\(|T_c|\le C\|u\|_2 X\Lambda\) is **dead**:
\(\lvert R_{\mathrm{pre}}\rvert\simeq 0.158\,s\) on the
scaled triad. That is not ★ dying. On the same family
\(\mathcal R_\star\) is flat (\(\sim 0.022\) at best phase).
The Attack-2 remainder \(|T_c|\le C_* X^{3/2}\Lambda\) is a
different sufficient door for DA-NS-2, not this boxed
form. One family is not a proof. Lattice HH→L did not kill.
File: [`LEMMA-STAR-NEXT.md`](LEMMA-STAR-NEXT.md).

---

## Five-lane drill (done 1) — 10 September 2026

Original five, from PR 48 (`run_all_five.py`).
**Not** 9A–9D. File:
[`five-lane-export/FIVE_LANES.md`](five-lane-export/FIVE_LANES.md).

| Lane | Verdict |
|---|---|
| 1 Covariance | Numeric support only. Not a proof. |
| 2 Triad / K=0 / \(C_*\) | K=0 **dead** (\(\lvert T_c\rvert/\mathcal D_s\) blows with amplitude). Remainder \(\lvert T_c\rvert\le C_* X^{3/2}\Lambda\) survives numeric on the triad (\(\simeq 0.004058\)). That is **not** \(C_{\star}\). Not a theorem. |
| 3 Bony HH→L | Channel diagnostic. No closure. The older \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\) target is **DEAD BY SCALING**. Not lane 2. |
| 4 Stokes | Identities sit. \(\mathcal D_s\ge 0\). \(\theta\nu\mathcal D_s\) alone is not enough. |
| 5 Route 2 | Survives numeric kill only. The 978-sample max \(\lvert R_{\mathrm{pre}}\rvert\approx 5.09\) is the *dead* pre-Young ratio, not \(\mathcal R_\star\). On the scaled triad \(\mathcal R_\star\) stayed \(\sim 0.022\). Not \(\to\infty\). **Not a proof.** |

Screenshot headline: K=0 dead; Lemma★ survives numeric
kill only (not proved); HH→L still the gap.
A later Grok note called lane 2 an analytic
\(X^{3/2}\) bound: that is the \(C_*\) remainder,
not the \(a^4\) line.

Lattice HH→L fan (Attack 12) is **later**, not lane 3.
Packets 9A–9D are **later**. Do not substitute them.

**Headline.** K=0 dead. Uniform pre-Young \(C\) dead (Attack 6:
\(\lvert R_{\mathrm{pre}}\rvert\simeq 0.158\,s\)). Attack-2
\(C_*\) survives the scaled triad (\(\simeq 0.0404\)). That
is not \(C_{\star}\). Lattice HH→L did not kill. NS not solved.

Do not cash a bounded ratio on a Galerkin sample as \(C_0\).
A family that did not blow is not a uniform geometric constant.

---

## Live door

The exact form of ★ is the scale-invariant trilinear
bound on \(\mathcal R_\star\) (or \(C_{\star}\)) from triadic
geometry or cancellation.
\(\sup\mathcal R_\star<\infty\) proves the inequality.
That implication to global regularity in this packaging
is one direction only. A near-shell or
HH→L sequence with \(\mathcal R_\star\to\infty\) kills it.
The first family is the closing three-key
\(k_0,k_0+e,2k_0+e\). Two Fourier keys is not that test.
Two shells can be live. Hunt with \(|e|/|k_0|\to 0\)
(fix \(e\), send \(|k_0|\to\infty\)); a frozen ray is not
the supremum. Attack 8 did not kill it. Lattice packets
scored: isolated triad, AP (\(D_s\) wins), adjacent
spheres (closures \(O(m)\)), Freiman-AP subset, HH→L
fan (\(\mathcal R_\star\sim\beta/\alpha\)). No kill.
The \(m^{1/2}\) heuristic has not found a lattice home.
H1 on one cylinder is the other live writing
([`H1-SOT.md`](H1-SOT.md)).
ABC_λ kills the uniform bound as a closer
(`docs/CS-REMAINDER.md`). The leftover writing is H1,
which was not run on that field.
Uniform pre-Young \(C\) is off. Attack-2 \(C_*\) is a
different door. Do not revive K=0. Do not cash a triad
\(\mathcal R_\star\) as \(C_0\). Numerically bounded samples
remain evidence only. Do not write “almost proved.”

---

## Relation to the other maps

- **H1 = WRITE (6) = Lemma I on the ball.** Bad pairs,
  kernel \(|z|^{-3}\). Geometric path. Open.
  Tube writing (same leftover class, different integral):
  [`H1-SOT.md`](H1-SOT.md).
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
Three-key: [`LEMMA-STAR-E.md`](LEMMA-STAR-E.md).
Packets: [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).
Incidence Route A (conditional, not a theorem):
[`LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md`](LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md).
Original five-lane JSON (PR 48 run, not a re-proof):
[`five-lane-export/COMPUTE.md`](five-lane-export/COMPUTE.md).
Original five lanes (not 9A–9D):
[`five-lane-export/FIVE_LANES.md`](five-lane-export/FIVE_LANES.md).
Attack 9B exact-shell \(K_{\alpha,\beta}\) (finite sample,
not a kill): [`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md).
Fixed-output \(\Theta(m^2)\) is a counting error
(\(K\le 16s\)): [`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md).
Four corrections (missing \(a^4\) inequality dead;
★ \(\Rightarrow\) GR not \(\Leftrightarrow\); test both signs;
Section 4 not proved):
[`LEMMA-STAR-CORRECTIONS.md`](LEMMA-STAR-CORRECTIONS.md).
Independent core (direct triad sum; live Stokes
file not overwritten):
[`LEMMA-STAR-CORE.md`](LEMMA-STAR-CORE.md).
Object app (pictures; bound still open):
[`THE-OBJECT-APP.md`](THE-OBJECT-APP.md).
Localized ABC (rejected recon, not a kill):
[`CS-REMAINDER.md`](CS-REMAINDER.md).
N-shell maximizer (saturates; not a bound):
[`RSTAR-SHELL-CLIMB.md`](RSTAR-SHELL-CLIMB.md).
