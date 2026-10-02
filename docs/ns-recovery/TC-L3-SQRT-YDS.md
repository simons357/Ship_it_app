# Half-spread candidate: \(|T_c|\le C\|\nabla u\|_3\sqrt{YD_s}\)

**1 October 2026.** Strongest next target after the local exact-shell
perturbation ★. This page locks the candidate and scores it. It does
**not** prove the bound. It is **not** unrestricted Lemma★.
Unrestricted \(\sup\mathcal R_\star<\infty\) stays **KILLED** on
\(v_n\). Ordinary NS is not solved. Soft X silent.

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local-★ / 71E / 83 packets. Does **not** stamp
\(r\sim\kappa^{-1/2}\). Localized bump is **not on this tree**.

Machine: `scripts/da_gate_tc_l3_sqrt_yds.py`.
JSON: `results/da_gate_tc_l3_sqrt_yds.json`.
Desk card:
[`../../packets/DA-GATE-TC-L3-SQRT-YDS-2026-10-01.md`](../../packets/DA-GATE-TC-L3-SQRT-YDS-2026-10-01.md).
Clock: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Defs: [`../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Near-shell identities:
[`EXACT-SHELL-PERTURBATION-STAR.md`](EXACT-SHELL-PERTURBATION-STAR.md).

\(Y\) here is the locked moment \(Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2\),
not \(\|\nabla u\|_2^2\). \(\|\nabla u\|_3\) is the physical Haar
\(L^3\) of the Frobenius gradient on \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\).
No proxy.

---

## The candidate (OPEN)

\[
\lvert T_c\rvert
\le
C\,\|\nabla u\|_3\sqrt{YD_s}.
\tag{\(\dagger\)}
\]

Status: **attack**. Not proved. No \(C\) is stamped. Homogeneous of
degree 3, same as \(T_c(av)=a^3T_c(v)\). Inserting \((\dagger)\) into
the centered equation is a different sentence from the equation.

The near-shell obstruction **motivates** \((\dagger)\) and does not establish
it. A successful script run verifies the tested identities. The uniform
inequality and its time budget remain separate proof obligations.

Unrestricted ★ used \(\sqrt{D_sEY}\). The new factor replaces
\(\sqrt{E}\) by \(\|\nabla u\|_3/\sqrt{Y}\). On a volume-1 torus
\(\|\nabla u\|_2=\sqrt{X}\le\|\nabla u\|_3\), so \(L^3\) is the
weaker (larger) majorant. It is the natural physical product norm
for \((u\cdot\nabla)u\), not a tightening of \(L^2\).

---

## Exact obstruction: why \(\sqrt{D_s}\)

On the aligned 9B family \(v_\varepsilon=w+\varepsilon z_\beta\),

\[
D_s(v_\varepsilon)\sim\beta(\alpha-\beta)^2\varepsilon^2,
\qquad
T_c(v_\varepsilon)\sim\beta(\beta-\alpha)\,\varepsilon\,\|\Pi_\beta B(w,w)\|_2.
\]

Hence

\[
\frac{T_c}{D_s}=\Theta(\varepsilon^{-1})\to\infty,
\qquad
\frac{T_c}{\sqrt{D_s}}\to\text{finite},
\qquad
\frac{\lvert T_c\rvert}{\|\nabla u\|_3\sqrt{YD_s}}\to\text{finite}.
\]

Any bound linear in \(D_s\) with a prefactor that stays finite at
the shell is **exactly obstructed**. The square-root scale is the
one the \(\varepsilon\)-family can saturate. That is why
\((\dagger)\) is the sharper candidate: it keeps the necessary
\(\sqrt{D_s}\) and asks a controlling factor that remains finite
as \(\varepsilon\to 0\).

This is not a proof that the prefactor \(\|\nabla u\|_3\sqrt{Y}\)
works. It is the reason that scale deserves the attack.

---

## How \(\|\nabla u\|_3\) is computed

Book Plancherel: \(\|v\|_2^2=(2\pi)^{-3}\int|v|^2=\sum|v_k|^2\).
The same Haar measure is used for \(L^3\). Place the finite Fourier
support on an \(N^3\) grid with \(N>4\max|k|_\infty\), invert
\(\partial_j\hat u_i=ik_j(u_k)_i\), and take

\[
\|\nabla u\|_3
=
\Bigl(\operatorname{mean}\lvert\nabla u\rvert^3\Bigr)^{1/3},
\qquad
\lvert\nabla u\rvert^2=\sum_{i,j}\lvert\partial_ju_i\rvert^2.
\]

Parseval check (exact when the grid beats \(4\max|k|\)):
\(\|\nabla u\|_2^2=X\) and \(\|u\|_2^2=E\). Both sit on every row
below. Doubling \(N\) on the note triad changes \(\|\nabla u\|_3\)
by \(1.6\cdot10^{-13}\). Amplitude \(u\mapsto 2u\) leaves the
ratio invariant.

**Certification.** \(T_c\), \(Y\), \(D_s\) are exact Fourier
arithmetic (direct triad sum). \(\|\nabla u\|_2=\sqrt{X}\) is
Parseval. Sampled quadrature of \(\|\nabla u\|_3\) **cannot certify
a counterexample**: \(|\nabla u|^3\) is not a trig
polynomial. The certified sandwich on volume 1 is

\[
\frac{\lvert T_c\rvert}{\|\nabla u\|_3^{\mathrm{up}}\sqrt{YD_s}}
\le
\frac{\lvert T_c\rvert}{\|\nabla u\|_3\sqrt{YD_s}}
\le
\frac{\lvert T_c\rvert}{\sqrt{X}\,\sqrt{YD_s}},
\]

where \(\|\nabla u\|_3^{\mathrm{up}}=\|\nabla u\|_2^{1/3}\|\nabla u\|_4^{2/3}\)
when \(N>8\max|k|_\infty\) makes \(\|\nabla u\|_4^4\) an exact
trapezoid of a trig polynomial, otherwise the triangle bound
\(\sum|k|\,|u_k|\). A kill requires the certified lower bound to
blow. Quadrature in the middle is a diagnostic only.

---

## Numbers

**§4 note triad.** \(T_c=16/5\), \(D_s=12/5\), \(Y=14\),
\(\|\nabla u\|_3=3.282\). Quadrature ratio \(0.168\). Certified
sandwich \(0.166\le\cdot\le 0.175\). Largest on-tree snapshot.
Quadrature-stable. Homogeneity holds.

**Separated \(L=8\).** \(T_c=1.44\cdot10^3\), ratio \(0.00463\).
Weaker face. Not the obstruction.

**HH\(\to\)L.** \(T_c<0\). Absolute ratio \(0.033\). Signed \(T_c\)
is used; the display is \(\lvert T_c\rvert\).

**Near-shell annular \((\alpha,\beta)=(5,4)\).**

| \(\varepsilon\) | \(T_c\) | \(T_c/D_s\) | \(T_c/\sqrt{D_s}\) | \(\|\nabla u\|_3\) | new ratio |
|---:|---:|---:|---:|---:|---:|
| \(0.20\) | \(0.195\) | \(1.26\) | \(0.496\) | \(2.337\) | \(0.0419\) |
| \(0.10\) | \(0.0971\) | \(2.45\) | \(0.487\) | \(2.308\) | \(0.0421\) |
| \(0.05\) | \(0.0485\) | \(4.86\) | \(0.485\) | \(2.301\) | \(0.0421\) |
| \(0.025\) | \(0.0242\) | \(9.70\) | \(0.485\) | \(2.299\) | \(0.0422\) |

\(T_c/D_s=\Theta(\varepsilon^{-1})\) blows. \(T_c/\sqrt{D_s}\) and
the new ratio stay. The square-root dependence is saturated here,
not merely suggested.

**Growing layer \(v_n\)** (aspect 6: comparable; in the class).

| \(n\) | \(T_c/D_s\) | \(\sqrt{\mathcal R_\star}\) | \(\|\nabla u\|_3\) | new ratio |
|---:|---:|---:|---:|---:|
| \(1\) | \(0.215\) | \(0.0374\) | \(8.46\) | \(0.0153\) |
| \(2\) | \(0.189\) | \(0.0507\) | \(23.3\) | \(0.00975\) |
| \(4\) | \(0.178\) | \(0.0705\) | \(68.2\) | \(0.00620\) |
| \(8\) | \(0.172\) | \(0.0989\) | \(208\) | \(0.00393\) |

Unrestricted ★ still grows (\(\sqrt{\mathcal R_\star}\) by
\(\approx 2.65\)). The new ratio **falls** (by \(\approx 0.26\)).
\(v_n\) does **not** kill this slot on the seated sample. That is
the point of replacing \(\sqrt{E}\) by \(\|\nabla u\|_3/\sqrt{Y}\):
the layer concentrates the gradient, and \(L^3\) pays it.
\(\|\nabla u\|_3/\|\nabla u\|_2\) rises from \(1.16\) to \(1.55\).
This is a sample, not \(n\to\infty\). The certified \(L^2\) upper
on the ratio also falls (\(0.0178\to 0.0061\)). Do not stamp a \(C\).

**Small-case attack (priority list).** Three lanes. \(T_c\), \(Y\),
\(D_s\), and \(\|\nabla u\|_2=\sqrt{X}\) are exact Fourier
arithmetic. The displayed bounds are the certified sandwich.
Quadrature is not used to claim a kill.

1. Nearly single-shell states with several interacting triads.
2. Widely separated frequencies with varied amplitudes.
3. Dense packets with coordinated phases.

| Lane | Field | cert lower | cert upper |
|---|---|---:|---:|
| near-shell | fat closer \((5,6)\), \(\varepsilon=0.05\) | \(0.0888\) | \(0.0920\) |
| near-shell | fat closer \((9,10)\), \(\varepsilon=0.05\) | \(0.0460\) | \(0.0474\) |
| near-shell | two-shell \((5,6)\), \(e_\beta=0.1,0.25,0.5\) | \(\le 0.00519\) | \(\le 0.00534\) |
| near-shell | two-shell \((9,10)\), \(e_\beta=0.25\) | \(0.00656\) | \(0.00677\) |
| separated | \(L=4\), amps \((1,0.1,1)\) | \(0.00516\) | \(0.00551\) |
| separated | \(L=4\), amps \((1,4,0.25)\) | \(0.00192\) | \(0.00205\) |
| separated | \(L=8\), four amplitude mixes | \(\le 0.00139\) | \(\le 0.00149\) |
| separated | \(L=16\), amps \((1,0.25,1)\) | \(0.00046\) | \(0.00086\) |
| packet | clustered aligned triads | \(0.0484\) | \(0.0533\) |
| packet | \(v_2\), \(v_4\) (coordinated layer) | \(\le 0.00942\) | \(\le 0.0123\) |
| packet | same-helicity box (Beltrami) | \(0\) | \(0\) |

No certified counterexample. The strongest small-case certified
upper is fat \((5,6)\) at \(0.092\), still below the note-triad
upper \(0.175\). A same-helicity box is Beltrami: \(B(u,u)=0\),
so \(T_c=0\). That is cancellation, not a kill. The live
coordinated packets on this tree are the clustered aligned-triad
bundle and \(v_n\).

A successful script run verifies the tested identities. The
uniform inequality and its required time budget remain separate
proof obligations.

---

## What this does, and what it does not

- Exact obstruction to linear-in-\(D_s\): **sits**.
- Square-root scale on near-shell: **saturates**.
- Unrestricted ★: still **dead**.
- New slot on \(v_n\) (n=1,2,4,8): **not growing**.
- Largest seated ratio: note triad \(\approx 0.168\).
- Uniform \(C\) on all divergence-free fields: **not proved**.
- Localized bump: **not scored** (not on this tree).
- DA-NS-2 / Need★ / \(K\in L^1_{\mathrm{loc}}\): still **OPEN**.
- \(r\sim\kappa^{-1/2}\): **not stamped**.

A tautological \(K=(T_c-\theta\nu D_s)_+/X\) is still not content.
Do not put \(K(t)\) in the PDE. Kill / ★ decisions still use the
complete signed \(T_c\) only.

The attack from here is to prove \((\dagger)\) with some finite
\(C\), or kill it on a field that is actually in the comparable /
near-shell class. The near-shell family cannot kill the
\(\sqrt{D_s}\) power. \(v_n\) did not kill the prefactor on this
sample. That is a concrete advance, not a closure.

No new estimate is claimed. No continuation criterion.
**NS not solved.**
