# STTP normal-form diagnostic

**Audience:** Jonathan + agents filing the ChatGPT Stokes-primitive canvas  
**Date:** 1 October 2026  
**Status:** useful diagnostic. **Centered drift remains OPEN. NS is not solved.**

ChatGPT ran a fixed-λ Stokes-type test potential (STTP) on a fundamental cubelet and reported:

| Checkout | ChatGPT-reported result |
| --- | --- |
| \(D\Phi_\lambda[-\nu A u]=C_\lambda\) | max numerical error \(2.84\times 10^{-13}\) |
| Quartic remainder, 100 random fields | 54 positive, 46 negative |
| Amplitude scaling | \(C_\lambda\sim a^3\), \(R_4\sim a^4\) |

That canvas is **not in this tree**. This note files the finding and closes the three gaps the canvas itself named. It does not reconstruct ChatGPT's exact \(\Phi_\lambda\) symbol, and it does not claim their Exhibit C number \(0.00275742\).

Evaluator: `scripts/ns_attacks/sttp_normal_form.py`.  
Fail-fast tests: `tests/test_sttp_normal_form.py`.  
Live run (seed 7, 100 cubelet fields): `results/sttp_normal_form.json`.

| Checkout | This tree |
| --- | --- |
| \(C_\lambda^{\mathrm{slots}}=C_\lambda^{\mathrm{polarization}}\) | max error \(7.86\times 10^{-14}\) |
| Quartic remainder, 100 random cubelets | 100 positive, 0 negative |
| Amplitude scaling | \(C_\lambda\sim a^3\), \(R_4\sim a^4\) (slopes \(3.00\), \(4.00\)) |
| Exhibit C moving-\(\lambda\) term | \(0.1046\) (\(\dot\Lambda\,\partial_\lambda\Phi\)) |

---

## 1. Declared primitive

On mean-zero divergence-free Fourier fields,

\[
\Phi_\lambda(u)=\langle B(u,u),(A+\lambda)^{-1}u\rangle,
\qquad
B(u,w)_k=iP_k\sum_{p+q=k}(\widehat u(p)\cdot q)\,\widehat w(q),
\]

with \(\lambda>0\) frozen when the Fréchet derivative \(D\Phi\) is taken. Plancherel pairing as in the five-lane Stokes-moment scripts.

\[
\begin{aligned}
D\Phi[v]
&=\langle B(v,u)+B(u,v),G_\lambda u\rangle+\langle B(u,u),G_\lambda v\rangle,\\
C_\lambda
&=D\Phi[-\nu A u],\\
R_4
&=D\Phi[-B(u,u)],\\
\partial_\lambda\Phi
&=\langle B(u,u),-G_\lambda^2 u\rangle.
\end{aligned}
\]

Along Navier–Stokes, \(u_t=-B(u,u)-\nu A u\). At **frozen** \(\lambda\),

\[
\frac{d}{dt}\Phi_\lambda(u(t))=C_\lambda+R_4.
\]

\(C_\lambda\) is the viscous cubic of **this** primitive. It is not claimed equal to the centered transfer \(T_c=M-\Lambda N\).

---

## 2. The three named limitations

### 2.1 Moving \(\lambda\)

If the parameter is slaved to the live barycenter \(\lambda(t)=\Lambda(u(t))=Y/X\), the Stokes-moment identity is

\[
\dot\Lambda=\frac{2(T_c-\nu D_s)}{X},
\qquad
D_s=Z-\Lambda Y.
\]

ChatGPT wrote \(\dot\lambda=2(T_c-\nu L)/X\). The identity forces \(L=D_s\). The omitted term is \(\dot\Lambda\,\partial_\lambda\Phi\). Along NS,

\[
\frac{d}{dt}\Phi_{\lambda(t)}(u(t))=C_\lambda+R_4+\dot\Lambda\,\partial_\lambda\Phi.
\]

The script computes that last term. On the deterministic cubelet called Exhibit C here it is nonzero. The ChatGPT canvas omitted it and then checked a different Exhibit C by hand (\(\approx 0.00275742\)). Those two numbers are **not** identified.

### 2.2 Comparable-triad filter is vacuous on this cubelet

The support is the \(3\times 3\times 3\) lattice cube minus the origin: 26 modes, frequency lengths in \([1,\sqrt{3}]\). Every pair of lengths has ratio \(\le\sqrt{3}<2\). A ratio-2 comparable-triad filter therefore passes every triad on this support. For larger supports the selected potential must also be differentiated along the full NS nonlinearity — that is already what \(R_4=D\Phi[-B(u,u)]\) does, but the cubelet itself does not stress a ratio-2 cutoff.

### 2.3 Fail-fast assertions

The canvas only printed results. The tests here fail the process unless:

- \(\max|C_\lambda^{\mathrm{slots}}-C_\lambda^{\mathrm{polarization}}|<10^{-10}\), and the Euler identity \(D\Phi[u]=3\Phi\)
- log-log amplitude slopes are within \(0.15\) of \(3\) and \(4\)
- \(R_4\) is finite and not identically zero; signs are recorded, not forced
- the moving-\(\lambda\) term on Exhibit C is computed and nonzero
- honesty locks stay false: `centered_drift_closed=False`, `ns_solved=False`

---

## 3. What this does and does not show

**Does:**

- Verifies a declared cubic Stokes primitive numerically (fixed-\(\lambda\) identity).
- Exposes a quartic remainder. On this declared resolvent primitive every
  cubelet / \(|k|_\infty\le 2\) sample so far has \(R_4>0\). That is **not**
  a positivity theorem, and it is **not** ChatGPT's 54/46 sign-indefinite
  remainder (their \(\Phi_\lambda\) is not in this tree).
- Shows remainder smallness cannot be read from amplitude alone (\(R_4\sim a^4\)).
- Includes the moving-\(\lambda\) term instead of omitting it.

**Does not:**

- Close centered drift.
- Rule out every possible normal-form estimate.
- Identify \(C_\lambda\) with \(T_c\).
- Restore unrestricted Lemma★, Ring/SND glue, or Clay Statement B.

Keep it as a diagnostic. The next estimate, if any, has to control \(R_4+\dot\Lambda\,\partial_\lambda\Phi\) on supports that actually stress a triad cutoff — not this cubelet.
