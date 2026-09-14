# After the QNM–prime unification: what remains

**Jonathan Simons**  
CosmoEvolution Research Program  
14 September 2026  

**Status.** Note. Archive only. Not live Domain Architect. Clay is **NOT CLAIMED.** This is **not** a proof of the Riemann hypothesis. It is **not** a discovery that primes live in black-hole ringdown.

---

## Abstract

An August 2026 CosmoEvolution note proposed that prime distribution, the Riemann zeta function, black-hole quasinormal modes (QNMs), and horizon geometry form one harmonic signature, to be tested with LIGO ringdown. A 26 August Domain Architect audit withdrew that unification: the proposed Möbius–GCD bridge is a **NO-GO**, and the horizon spectral zeta was never computed. This note records what still stands as citation, what this repository already measured, and what would be required for a later paper. Nothing here awards a correspondence.

## 1. What this paper is

The August source is filed as a historical record:

[`QNM_Prime_Zeta_DA_Analysis_2026-08.md`](QNM_Prime_Zeta_DA_Analysis_2026-08.md)

Read that body as a **proposed interpretation that was retracted**. This note is the paper that remains after the retraction. It does not reprint the withdrawn claim as a result.

Live Domain Architect stays DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE. Gravity stays off default decompose. No `TRANSFORMABLE` stamp without an explicit map \(T\).

## 2. Citations that survive

These are locally established **outside** the withdrawn glue.

**Motl–Neitzke (2003).** For highly damped Schwarzschild QNMs,

\[
\mathrm{Re}(\omega_n) \to \frac{\ln 3}{8\pi M}
\quad (n\to\infty).
\]

The constant \(3\) enters through monodromy of the Teukolsky problem. It is **not** the prime-counting function \(\pi(x)\). A number-theoretic constant in an asymptotic is not a theorem that ringdown encodes primes.

**Berti–Cardoso–Will (2006).** Kerr fundamental-mode tables \((M\omega_R, M\omega_I)\) versus spin. This repository already uses Berti-style fits in `scripts/build_qnm_table.py`.

**Euler product / explicit formula.** Number theory:

\[
\zeta(s)=\prod_p (1-p^{-s})^{-1},
\qquad
\pi(x)\sim \mathrm{Li}(x)-\sum_\rho \mathrm{Li}(x^\rho)+\cdots.
\]

That encodes primes in \(\zeta\). It does not, by itself, encode primes in gravitational-wave ringdown.

**Textbook QNMs.** \(\omega=\omega_R+i\omega_I\). LIGO ringdown spectroscopy, when it works, measures a few low overtones of a Kerr remnant, typically \(n\approx 0,1\).

## 3. What this repository already ran

Harmonic Blueprint Experiment 01 is **closed**.

Held-out TEST did **not** reject H0. The predefined prime-neighbor frequency-ratio family was **not supported**. Nodes were frozen before TEST. Do not retune. Do not reopen (decision C15).

Report: [`HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](HB-RINGDOWN-EXPERIMENT-01-REPORT.md).  
Table: [`data/qnm_events.csv`](../../../data/qnm_events.csv).

QNM labels \((\ell,m,n)\) are not a prime-or-not integer (**C-PRIME-3**). Dimensional “5 Hz is prime” claims stay retired (**C-PRIME-4**).

## 4. What is withdrawn

Do not salvage these as results:

- Primes → zeta → zeros → QNMs → geometry as one signature.
- The Möbius–GCD operator \(Q_N(i,j)=\mu(\gcd(i,j))/\gcd(i,j)\) as an RH bridge (in-framework **NO-GO**: first row \(\mu\)-independent; linear identity circular; quadratic identity tautological; spectral bounds only \(O(N)\)).
- LIGO O5 as an RH experiment. The Motl–Neitzke tower is \(n\to\infty\). Even if that tower were measured, it is \(\ln 3\), not the zeta zeros.
- \(\zeta_{\mathrm{horizon}}(s)=\zeta(s)\). Not computed.
- Hilbert–Pólya identified with a horizon Laplacian. Stacked conjectures.
- The August note’s GWTC-5.0 / GW250114 / EHT counts. Those numbers are the source’s, **not verified** here.

## 5. Letters collide

Three different “Track B / \(Q_N\) / \(H_N\)” objects live in this project. They are not one operator.

| Name | What it is | Book |
|---|---|---|
| Möbius–GCD \(Q_N\) | \(\mu(\gcd)/{\gcd}\) as used in the August RH glue | withdrawn bridge |
| Inverse-GCD Q6 \(H_N\) | arithmetic face | [`docs/papers/gcd/`](../../papers/gcd/) |
| Swirl Track B | \(\Phi\)-renormalization for axisymmetric NS | [`docs/papers/swirl/`](../../papers/swirl/) |

Do not import any of them into `domain_architect/` as a black-hole zeta engine.

## 6. What a later paper would need

Parked, not claimed:

1. Specify a compact manifold independently of the desired conclusion.
2. Compute its spectral zeta.
3. State an explicit comparison to \(\zeta\) or to a named \(L\)-function.
4. If a map into QNMs is asserted, exhibit \(T\) (decision A5). No \(T\), no `TRANSFORMABLE`.

That would be a **new** paper. This note is not that paper. The BTZ–zeta sentence in the August §2.3 is not upgraded here.

## 7. Conclusion

The August CosmoEvolution piece can stand as a paper **only** with the 26 August correction as control: unification withdrawn. The present note is the split that remains: Motl–Neitzke, Berti, and the Euler product as citations; Experiment 01 as a closed null; RH still open.

Control for RH: [`../sfe-hb/Harmonic_Perspective_on_RH_2026-08-14.md`](../sfe-hb/Harmonic_Perspective_on_RH_2026-08-14.md). Bridge lemma **OPEN**.

## References

- Motl, L. and Neitzke, A. (2003). Asymptotic black hole quasinormal frequencies. *Adv. Theor. Math. Phys.*
- Berti, E., Cardoso, V., and Will, C. M. (2006). Gravitational-wave spectroscopy of massive black holes with the space interferometer LISA. *Phys. Rev. D* **73**, 064030.
- Riemann, B. (1859). Über die Anzahl der Primzahlen unter einer gegebenen Grösse.
- Archived August source: `QNM_Prime_Zeta_DA_Analysis_2026-08.md`.
- Closed Experiment 01: `HB-RINGDOWN-EXPERIMENT-01-REPORT.md`.
