# The three unfinished measurements

**25 September 2026.** Ran what is defined. Did not invent the rest.
Classical NS stays open. DA-NS-2 stays **OPEN**. (17) stays **OPEN**.
L1 / BOTH SIGNS stays **OPEN**. The middle region is not payable.

Machine: [`scripts/three_unfinished_measurements.py`](../scripts/three_unfinished_measurements.py).
Results: [`results/three_unfinished_measurements.json`](../results/three_unfinished_measurements.json).

This does **not** alter the RMS/SBP, static-frontier, Fourier-triangle,
Lemma★, or narrow-danger lock packets.

---

## 1. Equation (16) — positive-part term

The Sept 20 initial datum that produced

\[
\mathcal S(1)\approx 0.001337845,\ 0.046918627,\ 0.072599898
\]

at \(N^2=6,12,20\), \(\nu=3/2\), \(K=1\) is **MISSING** from this tree.
Those numbers are **not reproduced**.

The (16) integrand is

\[
\frac{[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4]_+}{X_N}.
\]

On the locked odd Hermitian triad (\(X=52A^2\), \(Y=532A^2\),
\(\mathcal T=24A^3\)), at \(A=24\), \(\nu=3/2\), \(K=1\),

\[
[\mathcal T_{\mathrm{sc}}-\nu Y/4]_+
=
216864>0.
\]

The key term is live at \(t=0\). That is the test the \(S\equiv 0\)
Taylor–Green run never made.

Evolved, same viscosity and cutoff, **different field**: \(A=9\),
\(N^2=20\), \(T=1\), \(dt=0.002\).

| \(t\) | \(\mathcal T_{\mathrm{sc}}\) | \([\cdot]_+\) | integrand |
|---:|---:|---:|---:|
| 0 | 17496 | 1336.5 | 0.3173 |
| 1 | \(\sim 10^{-12}\) | 0 | 0 |

\[
\mathcal S_{1,20}(1)\approx 0.001083.
\]

This is **not** the missing Sept 20 number. It only shows that when
the positive part is actually on, the integral is finite on this
decaying trajectory. It does **not** prove (17).

---

## 2. Loop-defect upper bound

\(L_N\le M_N\le U_N\) was never defined. It is **not** invented.

On the locked parallelogram the LOOP-GAUGE TEST already supplies a
certified global maximum against the \(\Gamma=1\) tree baseline
\(\sum_e|g_e|\):

\[
\sum_e|g_e|\approx 1.76478,
\qquad
\max_{c\cdot\theta=\Omega}\sum_e|g_e|\cos\theta_e\approx 1.53837,
\]

\[
\boxed{\Gamma_{\mathrm{cyc}}\approx 0.8717
\quad\text{(this family, this }g\text{).}}
\]

\(\Omega_c=2\pi/3\), method `single-cycle-stationary`. That is an
upper bound for this cosine problem. It is **not** scale decay
\(\Gamma_{\mathrm{cyc}}(N)\lesssim N^{-\delta}\). It is **not** a
defect of NS. A local optimizer is still not a certificate.

---

## 3. \(\eta_{\rm DA}\) vs \(\mathcal Q\)

\(\alpha_c\) and \(\chi_\kappa\) are **not** in this tree and are
**not** invented. Therefore

\[
\eta_{\mathrm{DA}}
=
\frac{\alpha_{c,\kappa}\chi_\kappa\sqrt{X}}{\nu\sqrt{\kappa}\,r}
\]

is **NOT EVALUATED**.

What is defined, on the same \(A=9\) trajectory:

\[
\kappa=\sqrt{\Lambda},\qquad
r=\frac{\sqrt{D_s/Y}}{\kappa},\qquad
\mathcal Q_{\mathrm{actual}}=\frac{[T_c]_+}{\nu D_s},
\]

and the skeleton \(\sqrt{X}/(\nu\sqrt{\kappa}\,r)=\eta_{\mathrm{DA}}/(\alpha_c\chi)\).
\(\mathcal Q\) uses actual \([T_c]_+\), not the unreproved local
envelope (5).

| \(t\) | \(\mathcal Q_{\mathrm{actual}}\) | skeleton | \(r\) |
|---:|---:|---:|---:|
| 0 | 3.155 | 77.00 | 0.314 |
| 1 | 0.00129 | 76.32 | \(3.9\times 10^{-4}\) |

The skeleton stays large while \(\mathcal Q_{\mathrm{actual}}\)
collapses. That is the “envelope too loose / missing depletion in
signed assembly” signal, with \(\alpha_c\chi\) still unstamped.
It is **not** a close of the middle region.

---

## Attack verdict

| Ask | Done | Still open |
|---|---|---|
| (16) on Sept 20 \(S>0\) trajectories | IC **MISSING**. Positive part exercised on the locked odd triad | (17); the unlocated datum |
| Loop guaranteed upper bound | Certified \(\Gamma_{\mathrm{cyc}}\approx 0.8717\) on one family | \(L_N,M_N,U_N\); scale decay |
| \(\eta_{\rm DA}\) vs \(\mathcal Q\) | \(\mathcal Q_{\mathrm{actual}}\) and the skeleton measured | \(\alpha_c\chi\); \(\eta_{\rm DA}\) itself |

**NS not solved.**
