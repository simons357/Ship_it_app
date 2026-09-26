# Exact-shell perturbation ★ — local, with \(\beta^{-1/2}\)

**26 September 2026.** Stop exploring. This page proves the
**restricted** exact-shell statement that the 9B perturbation
reduces to. It uses the seated pair-vector \(S_{pq}\) and a
sphere-incidence bound. It is **not** unrestricted Lemma★.
Unrestricted \(\sup\mathcal R_\star<\infty\) stays dead on
\(v_n\) and on the localized bump. Ordinary NS is not solved.
Soft X silent.

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) packets. Does **not** stamp \(r\sim\kappa^{-1/2}\) as a
crossover theorem. That scale remains arithmetic of the
definitions.

Machine: `scripts/da_gate_exact_shell_perturbation_star.py`.
JSON: `results/da_gate_exact_shell_perturbation_star.json`.
Desk card:
[`../../packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md`](../../packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md).

Clock: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Pair vector: [`../../packets/FOURIER-TRIANGLES-S-PQ-2026-09-20.md`](../../packets/FOURIER-TRIANGLES-S-PQ-2026-09-20.md).
9B family: [`../math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md`](../math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md).

---

## What is proved, and what is not

**Proved here (local ★).** If \(Aw=\alpha w\) and \(\beta>0\),

\[
\bigl\|\Pi_\beta B(w,w)\bigr\|_2^2
\le
\frac34\,\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)\,\|w\|_2^4.
\tag{9}
\]

Hence, with \(r=\beta/\alpha\in(0,4]\),

\[
K_{\alpha,\beta}(w)
=
\frac{\beta\,\bigl\|\Pi_\beta B(w,w)\bigr\|_2^2}{\alpha^2\|w\|_2^4}
\le
\frac34 r^2\Bigl(1-\frac r4\Bigr)
\le
\frac{16}{9},
\]

and equivalently the half-derivative form

\[
\bigl\|\Pi_\beta B(w,w)\bigr\|_2
\le
\frac43\,\alpha\,\beta^{-1/2}\,\|w\|_2^2.
\tag{\(\star_{\mathrm{loc}}\)}
\]

The constant \(4/3\) is the sharpest number **this argument**
gives: it is \(\sqrt{16/9}\), attained as the maximum of the
polynomial bound at \(r=8/3\). Attainment by a field is **not**
asserted. The three-shear floor \(K_{1,2}=2/3\) sits strictly
below.

On the 9B family \(v_\varepsilon=w+\varepsilon z_\beta\) with
\(z_\beta\) aligned to \(\Pi_\beta B(w,w)\),

\[
\lim_{\varepsilon\to 0}\mathcal R_\star(v_\varepsilon)
=
K_{\alpha,\beta}(w)
\le
\frac{16}{9}.
\]

That is the local perturbation ★. Extreme satellites
(\(r\to 0\) or \(r\to 4\)) are **locally neutralized** by (9):
the bound itself goes to zero. Conservation geometry
(in-plane cancellation, factor \(1-\beta/(4\alpha)\)) is not
refuted by those satellites.

**Not proved.** Unrestricted \(\sup\mathcal R_\star<\infty\).
DA-NS-2. A remainder \(T_c\le\theta\nu D_s+KX\) on comparable
or multi-shell data. The \(r\sim\kappa^{-1/2}\) crossover as a
decision theorem. Occupancy-gone as a regularity close.

---

## 1. Exact shell, then one satellite

If \(Aw=\alpha w\), then \(\Lambda=\alpha\) and
\(A(A-\Lambda)w=0\), so \(T_c(w)=0\) and \(D_s(w)=0\). Vacuous,
not a kill.

The 9B perturbation is the next object:

\[
v_\varepsilon=w+\varepsilon z,\qquad Az=\beta z,\qquad \|z\|_2=1.
\]

Two-shell identities already inventoried:

\[
D_s(v_\varepsilon)
=
\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}
\sim\beta(\alpha-\beta)^2\varepsilon^2,
\]

and, for \(z\) along \(\Pi_\beta B(w,w)\) with the stretch sign,

\[
T_c(v_\varepsilon)
\sim
\beta(\beta-\alpha)\,\varepsilon\,\bigl\|\Pi_\beta B(w,w)\bigr\|_2.
\]

The gap cancels in the quotient. For \(\|w\|_2=1\),

\[
\lim_{\varepsilon\to 0}\mathcal R_\star(v_\varepsilon)
=
\frac{\beta\,\bigl\|\Pi_\beta B(w,w)\bigr\|_2^2}{\alpha^2}
=
K_{\alpha,\beta}(w).
\]

For a general closer the limit is
\(\beta\tau^2/(\alpha^2\|z\|_2^2\|w\|_2^4)\) with
\(\tau=-\mathrm{Re}\langle\Pi_\beta B(w,w),z\rangle\), hence
\(\le K_{\alpha,\beta}(w)\). So the whole family is controlled
once (9) sits. This is a local calculation around one exact
shell. It is not Littlewood–Paley / Hölder counting on a thick
annulus.

---

## 2. Seated pair vector on an exact input shell

From the seated identities: \(a=b=\alpha\), \(c=\beta\),

\[
S_{pq}
=
\sqrt{\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)}
\,(A_1 B_2+A_2 B_1)\,e_2.
\tag{3}
\]

The in-plane transverse piece cancels. At \(\beta=4\alpha\) the
pairs are collinear and \(S_{pq}=0\). No division by
\(1-\beta/(4\alpha)\). Cauchy–Schwarz on the two complex
polarizations gives

\[
\lvert A_1 B_2+A_2 B_1\rvert
\le
\lvert w_p\rvert\,\lvert w_q\rvert.
\]

The Fourier convention already locked on this book is

\[
\widehat B(w,w)_k
=
\frac i2\sum_{p+q=k}S_{pq}
=
i\,P_k\sum_{p+q=k}(q\cdot w_p)w_q.
\]

Therefore

\[
\bigl\lvert\widehat B_k\bigr\rvert
\le
\frac12
\sqrt{\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)}
\,L_k,
\qquad
L_k
=
\sum_{p+q=k}\lvert w_p\rvert\,\lvert w_q\rvert.
\]

---

## 3. Sphere incidence — EXACT

Let \(r_p=\lvert w_p\rvert\ge 0\) on the integer sphere
\(\lvert p\rvert^2=\alpha\), and \(F=\sum r_p^2=\|w\|_2^2\).
For \(\beta>0\),

\[
\sum_{\lvert k\rvert^2=\beta}L_k^2
\le
3F^2.
\tag{8}
\]

**Diagonal** \(p=p'\):

\[
\sum_k\sum_p r_p^2 r_{k-p}^2
=
\sum_{\lvert p+q\rvert^2=\beta}r_p^2 r_q^2
\le
\Bigl(\sum r_p^2\Bigr)\Bigl(\sum r_q^2\Bigr)
=F^2.
\]

**Off-diagonal** \(p\neq p'\). The conditions
\(\lvert k\rvert^2=\beta\), \(k\cdot p=\beta/2\),
\(k\cdot p'=\beta/2\) are a line meeting a sphere in \(\mathbb R^3\).
At most two real \(k\), hence at most two integer \(k\).
If \(p=-p'\) then \(\beta=0\), excluded. Distinct points on a
common sphere through the origin are parallel only when they
are antipodes. So \(\lvert I(p,p')\rvert\le 2\).

AM–GM on each configuration:

\[
r_p r_{p'} r_{k-p} r_{k-p'}
\le
\tfrac12\bigl(r_p^2 r_{p'}^2+r_{k-p}^2 r_{k-p'}^2\bigr).
\]

The partner side is a bijection of the same set of pairs. Thus

\[
\sum_{p\neq p'}\sum_{k\in I(p,p')}
r_p r_{p'} r_{k-p} r_{k-p'}
\le
\sum_{p\neq p'}\lvert I(p,p')\rvert\,r_p^2 r_{p'}^2
\le
2\sum_{p\neq p'}r_p^2 r_{p'}^2
\le
2F^2.
\]

Add the diagonal. That is (8). The constant \(3\) is what this
splitting gives. It is not claimed optimal. The lock on
\(\alpha\le 13\) sees \(\sum L_k^2\le\tfrac43 F^2\); that sample is
not a smaller proved constant.

This is not output-occupancy \(s\). A large fiber on one \(k\)
is paid inside \(L_k\), then controlled by the global \(3F^2\).

---

## 4. Assembly of (9) and the \(\beta^{-1/2}\) form

\[
\bigl\|\Pi_\beta B(w,w)\bigr\|_2^2
=
\sum_{\lvert k\rvert^2=\beta}\lvert\widehat B_k\rvert^2
\le
\frac14\,\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)
\sum_k L_k^2
\le
\frac34\,\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)\,\|w\|_2^4.
\]

That is (9). Divide by \(\alpha^2\|w\|_2^4\) and multiply by
\(\beta\):

\[
K_{\alpha,\beta}(w)
\le
\frac34 r^2\Bigl(1-\frac r4\Bigr).
\]

The elementary identity

\[
\frac{16}{9}-\frac34 r^2\Bigl(1-\frac r4\Bigr)
=
\frac{(3r+4)(3r-8)^2}{144}
\ge 0
\]

holds for all real \(r\), and on \((0,4]\) the polynomial bound
is maximized at \(r=8/3\) with value \(16/9\).

Rewrite (9) as an operator bound:

\[
\bigl\|\Pi_\beta B\bigr\|_2
\le
\frac{\sqrt3}{2}
\sqrt{\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)}
\,\|w\|_2^2
=
\Bigl(\frac{\sqrt3}{2}\,r\sqrt{1-r/4}\Bigr)
\alpha\,\beta^{-1/2}\,\|w\|_2^2.
\]

The coefficient \(\frac{\sqrt3}{2}\,r\sqrt{1-r/4}\) has maximum
\(4/3\) at \(r=8/3\). That is \((\star_{\mathrm{loc}})\).

A bound \(\|\Pi_\beta B\|_2\le C\alpha\|w\|_2^2\) (missing
\(\beta^{-1/2}\)) only gives \(K\le C^2\beta\), which can grow
with the output shell. The half-derivative is the piece that
stops that. It comes from the exact-shell symbol \(\sqrt{\beta}\)
together with the \(1/\alpha\) in \(K\), not from a global
Littlewood–Paley count.

---

## 5. Extreme satellites, locally neutralized

Conservation geometry on an exact input shell is the in-plane
cancellation in (3) and the factor \(1-\beta/(4\alpha)\).

| Satellite | \(r=\beta/\alpha\) | Bound on \(K\) |
|---|---|---|
| Extreme low | \(r\to 0^+\) | \(\frac34 r^2\to 0\) |
| Extreme high / flat | \(r\to 4^-\) | \(\frac34 r^2(1-r/4)\to 0\) |
| Worst in this bound | \(r=8/3\) | \(16/9\) |

An extreme satellite is not a counterexample to that geometry.
It is the regime where the geometry is strongest. The
comparable / near-shell face (\(r\sim 1\)) is the one the
polynomial actually spends its constant on.

Unequal-length triangles never had \(1-\beta/(4\alpha)\).
The growing layer \(v_n\) (aspect 6) and the localized bump
remain outside this page. They still kill unrestricted ★.

---

## 6. What this does not do

It does not restore \(\sup\mathcal R_\star<\infty\).
It does not give DA-NS-2.
It does not write a comparable-channel \(K\in L^1_{\mathrm{loc}}\).
It does not stamp \(r\sim\kappa^{-1/2}\).
It does not claim \(16/9\) is attained, or that \(3\) in (8) is
optimal.
It does not run Q4-0.

Three-shear \(K_{1,2}=2/3\) remains a floor, not the ceiling.

No new estimate is claimed on general data.
**NS not solved.**
