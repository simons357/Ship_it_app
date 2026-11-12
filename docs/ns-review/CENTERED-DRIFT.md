# Centered spectral drift

**12 November 2026.** Portable lock of the centered-drift object on
`main`. Identities only. **No new proof.** Ordinary unaugmented 3-D
Navier–Stokes is not solved. Lemma★ is not proved. Soft X silent.

Do not put \(K(t)\) in the PDE. Do not glue this page to Φ-renorm or
Clay Statement B.

Machine: `scripts/ns_attacks/centered_drift.py`.
JSON: `results/centered_drift.json`.
Equation: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Evaluator: `scripts/ns_lemma_star_core.py`.

---

## 1. Exact identities (KEEP)

On mean-zero divergence-free \(u\) on \(\mathbb T^3\), \(A=-P\Delta\),
\(\lambda_k=|k|^2\):

\[
X=\|A^{1/2}u\|_2^2,\quad
Y=\|Au\|_2^2,\quad
Z=\|A^{3/2}u\|_2^2,\quad
\Lambda=Y/X,
\]
\[
T_c=M-\Lambda N=-\langle B(u,u),A(A-\Lambda)u\rangle
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k,
\]
\[
D_s=Z-\Lambda Y=Z-Y^2/X
=\|(A-\Lambda)A^{1/2}u\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|u_k|^2\ge 0.
\]

**The centered equation** (exact, not an estimate):

\[
\Lambda'=-\frac{2\nu}{X}D_s+\frac{2}{X}T_c=\frac{2}{X}(T_c-\nu D_s).
\]

Also exact on this evaluator:

- two \(D_s\) writings agree (moment form vs spectral sum);
- two \(T_c\) writings agree (modal \(M-\Lambda N\) vs inner-product sum);
- barycenter: occupancy \(p_k=\lambda_k|u_k|^2/X\) gives
  \(D_s=X\,\mathrm{Var}_p(\lambda)\) and, with \(t_k=T_k/|u_k|^2\),
  \(T_c=X\,\mathrm{Cov}_p(\lambda,t)\);
- one shell \(\Rightarrow T_c=D_s=0\) (vacuous);
- two shells \(\alpha,\beta\):
  \(D_s=\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta/X\);
- homogeneity \(T_c(au)=a^3 T_c(u)\), \(D_s(au)=a^2 D_s(u)\).

If \(T_c\le\theta\nu D_s+KX\) with \(\theta<1\), then \(\Lambda'\le 2K\).
That implication is algebra after a remainder. It is not the remainder.

---

## 2. Locked finite-triad checkpoint

Section-4 near-scale triad \(p=(1,0,0)\), \(q=(0,1,0)\), \(r=(1,1,0)\):

\[
X=10,\quad Y=14,\quad Z=22,\quad\Lambda=\frac75,\quad
D_s=\frac{12}{5},\quad N=2,\quad M=6,\quad
T_c=\frac{16}{5},\quad \frac{T_c}{D_s}=\frac43.
\]

Sign is phase: \(u\mapsto -u\) flips \(T_c\) and leaves \(D_s\) fixed.
All of this \(T_c\) sits in the comparable-frequency channel.

---

## 3. What is killed

| Attempt | Status |
|---|---|
| \(T_c\le\theta\nu D_s\) (pure absorption, \(K=0\)) | **KILLED.** \(T_c/D_s\) scales with amplitude. The note triad already has \(T_c/D_s=4/3\). |
| Uniform energy-class remainder of unrestricted ★ scaling | **KILLED** on the growing-layer family \(v_n\) (recovery branch; not re-swept here). |
| Near-shell \(\varepsilon\to 0\) with aligned closer | \(T_c=\Theta(\varepsilon)\), \(D_s=\Theta(\varepsilon^2)\), so \(T_c/D_s=\Theta(\varepsilon^{-1})\to\infty\). Not a \(C_{\mathrm{geom}}\) theorem. |

Separated triads are not the obstruction: \(T_c/D_s\) tracks \(\sqrt{2}/L\).

---

## 4. What stays OPEN

**Drift estimate.** There exist \(\theta\in[0,1)\) and a coefficient
\(K\in L^1_{\mathrm{loc}}(0,T)\) such that, along the classical solution,

\[
T_c\le\theta\nu D_s+K(t)X.
\]

Useful only if \(K\) is controlled by quantities already known from the
energy inequality, or by a named dynamical bound that does not assume
the desired \(H^1\) ceiling, \(L^\infty\), or BKM.

**Tautology warning.** \(K=(T_c-\theta\nu D_s)_+/X\) makes the estimate
an identity. Content collapses to \(\int K<\infty\), which is the
original regularity question in other units.

**Need★** (signed dual on HH→L after two-shell gap-cancel) is **MISSING**.

**Smooth-split** (PR #149): finite homogeneous \(C\) for
\(\lvert T_c\rvert\le C g\sqrt{Y D_s}\) on torus Fourier fields. That is
an instantaneous estimate. It does **not** close
\(\int g^2\,dt\), Lemma★, or NS.

Unrestricted \(\sup\mathcal R_\star<\infty\) stays dead. Do not restore it.

---

## 5. What this is not

- Not Φ-renorm (wrong-variable story near the swirl axis).
- Not a Clay path.
- Not (4), Young, or a time-integrated \(F_X\) budget.
- Not a claim that the universe is regular for the same reason.

`ns_solved` is false. `lemma_star_proved` is false. `remainder_open` is true.
