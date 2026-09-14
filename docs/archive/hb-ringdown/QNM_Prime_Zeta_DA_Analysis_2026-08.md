> **Filing banner (14 September 2026).** Chat paste of *Prime Number
> Distribution in Black Hole Quasinormal Mode Spectra: A Domain Architect
> Analysis* (CosmoEvolution Research Program, August 2026), including the
> 26 August 2026 DA-audit correction already in the source.
>
> **Archive only.** Not live Domain Architect. Clay is **NOT CLAIMED.**
> This does **not** prove RH. Do **not** import into `domain_architect/`.
> Do not reopen Experiment 01 (C15: closed, off the DA import graph).
> Decision A11: gravity / Einstein stay off default decompose.
>
> **Can it be salvaged?** Yes as a **split**. Not as one harmonic
> signature. The 26 Aug correction already says that. Keep it.
>
> **Keep as citations (locally established, not a DA glue):**
> Motl–Neitzke (2003) highly damped Schwarzschild
> \(\mathrm{Re}(\omega_n)\to\ln 3/(8\pi M)\). The \(3\) is a monodromy
> constant, **not** prime-counting \(\pi(x)\). Berti–Cardoso–Will Kerr
> QNM tables (already used in `scripts/build_qnm_table.py`). Euler
> product and the explicit formula as **number theory**. Textbook QNMs
> \(\omega=\omega_R+i\omega_I\).
>
> **Already run here:** HB Ringdown Experiment 01
> ([`HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](HB-RINGDOWN-EXPERIMENT-01-REPORT.md)).
> Held-out TEST did **not** reject H0. The prime-neighbor family was
> **not supported**. Do not retune after TEST.
>
> **Withdrawn (do not salvage as a claim):** primes → zeta → zeros →
> QNMs → geometry as one signature. The Möbius–GCD
> \(Q_N(i,j)=\mu(\gcd(i,j))/\gcd(i,j)\) RH bridge as used in that audit
> (**NO-GO**). LIGO O5 as an RH experiment: LIGO ringdown is
> \(n\approx 0,1\), not the Motl–Neitzke \(n\to\infty\) tower; even that
> tower is \(\ln 3\), not the zeta zeros. Horizon spectral zeta coinciding
> with \(\zeta(s)\): **not computed**. Hilbert–Pólya identified with the
> horizon Laplacian: stacked conjectures. “Mode 220 is prime”: **C-PRIME-3**
> / **C-PRIME-4**.
>
> **Park:** an independently specified manifold whose spectral zeta is
> actually computed, then compared to \(\zeta\) or an \(L\)-function.
> That is a **new** paper. No \(T\), no `TRANSFORMABLE`. The BTZ–zeta
> sentence in §2.3 is **not** upgraded here.
>
> **Letters collide.** This note’s “Track B” is Möbius–GCD \(Q_N\).
> Swirl Track B is \(\Phi\)-renormalization. Inverse-GCD Q6 \(H_N\) is
> the arithmetic book in [`docs/papers/gcd/`](../../papers/gcd/). Those
> three are **not** the same object.
>
> GWTC-5.0 / GW250114 / EHT catalog numbers in the body are **the
> paper’s**, **not verified** in this repo. The measured/fit table that
> exists here is [`data/qnm_events.csv`](../../../data/qnm_events.csv).
>
> Control for RH remains
> [`../sfe-hb/Harmonic_Perspective_on_RH_2026-08-14.md`](../sfe-hb/Harmonic_Perspective_on_RH_2026-08-14.md).
> Bridge lemma **OPEN**.

---

# Prime Number Distribution in Black Hole Quasinormal Mode Spectra: A Domain Architect Analysis

**CosmoEvolution Research Program — August 2026**

## Abstract

We investigate the remarkable connection between black hole quasi-normal mode (QNM) frequencies and the distribution of prime numbers, mediated by the Riemann zeta function. Building on the Motl-Neitzke (2003) result that asymptotic QNM frequencies of Schwarzschild black holes are determined by number-theoretic quantities, we apply the Domain Architect (DA) framework to interpret this connection: the event horizon is a compact manifold whose spectral geometry determines the ringdown frequencies. If the horizon topology's spectral zeta function coincides with the Riemann zeta function, then black hole ringdown could encode prime number distribution through horizon geometry. **[SPECULATIVE — proposed interpretation, not an established result]** We catalog the most commonly measured parameters for binary black hole mergers (from LIGO GWTC-5.0, 390 total detections) and supermassive black holes (from EHT imaging of M87* and Sgr A*), and identify the specific QNM measurements from LIGO's O5 observing run (2026–2028) that could test this prediction. The connection is speculative but falsifiable, and represents one of the most beautiful intersections of number theory and physics.

## Correction — 2026-08-26 DA Audit (read first)

This paper was written before the Track B operator analysis. It feeds into the broader "harmonic chain" (primes → zeta → zeros → QNMs → geometry) described in Paper 9. A subsequent rigorous DA audit examined the proposed RH↔GCD bridge — the operator \(Q_N(i,j) = \mu(\gcd(i,j))/\gcd(i,j)\) meant to link the Riemann zeros to the gcd/prime structure underpinning that chain. That bridge is falsified in-framework (**NO-GO**): the first row of \(Q_N\) is \(\mu\)-independent, so the linear identity is circular; the quadratic identity is tautological; spectral bounds give only \(O(N)\); no analytic input exists inside Track B.

**Consequence:** the unifying claim — that primes, zeta, BH ringdown, and geometry are one harmonic signature — is **not** supported by the current operator analysis, and the triad thesis is **retracted** pending an independently specified manifold. The locally established facts this paper rests on (Motl–Neitzke asymptotics, Berti–Cardoso–Will tables, the Euler product) remain valid; only the unification is withdrawn. Read the body below as a record of a proposed interpretation, not a supported result.

## 1. Introduction

In 1859, Bernhard Riemann published his seminal paper "On the Number of Primes Less Than a Given Magnitude," introducing the zeta function:

\[\zeta(s) = \sum_{n=1}^{\infty} n^{-s}\]

Riemann showed that the non-trivial zeros of \(\zeta(s)\) encode the distribution of prime numbers. The Riemann hypothesis (still unproven) states that all non-trivial zeros lie on the critical line \(\mathrm{Re}(s) = 1/2\).

Nearly 150 years later, in 2003, Luboš Motl and Andrew Neitzke discovered that the asymptotic quasi-normal mode (QNM) frequencies of certain black holes are determined by number-theoretic quantities related to the Riemann zeta function. For the Schwarzschild black hole, the highly damped QNM frequencies approach:

\[\mathrm{Re}(\omega_n) \to \ln(3) / (8\pi M) \quad \text{as } n \to \infty\]

The number 3 is not arbitrary — it is related to the quantum group structure of the horizon, and for other black hole types, different number-theoretic constants appear.

This paper asks: Why should the eigenfrequencies of a black hole have anything to do with prime numbers? The Domain Architect framework provides a candidate answer: the event horizon is a compact manifold, its Laplacian eigenvalues determine the QNM frequencies, and the spectral zeta function of certain topologies naturally connects to the Riemann zeta function.

## 2. Black Hole Quasinormal Modes

### 2.1 What Are QNMs?

When a black hole forms (e.g., via stellar collapse or binary merger), it "rings" — emitting gravitational waves at characteristic frequencies determined by its mass \(M\) and spin \(a\). These quasinormal modes are the black hole's natural frequencies, analogous to the harmonics of a bell.

The QNM frequencies are complex: \(\omega = \omega_R + i\cdot\omega_I\), where \(\omega_R\) is the oscillation frequency and \(\omega_I\) is the damping rate (the mode decays as \(e^{-\omega_I\cdot t}\)).

### 2.2 The Berti-Cardoso-Will Tables

The fundamental QNM (\(l=m=2\), \(n=0\)) for Kerr black holes, from Berti, Cardoso & Will (2006):

| Spin (\(a/M\)) | Frequency \(M\omega_R\) | Damping \(M\omega_I\) |
|---|---|---|
| 0.0 (Schwarzschild) | 0.3737 | 0.0890 |
| 0.5 | 0.4538 | 0.0952 |
| 0.7 | 0.5306 | 0.0999 |
| 0.9 | 0.6611 | 0.0977 |
| 0.99 (near-extremal) | 0.8461 | 0.0749 |

Source: Berti, Cardoso & Will, Phys. Rev. D 73, 064030 (2006).

### 2.3 Asymptotic QNMs and Number Theory

The Motl-Neitzke result concerns the highly damped QNMs (\(n \to \infty\)). For Schwarzschild black holes, as \(n\) increases:

\[\mathrm{Re}(\omega_n) \to \ln(3) / (8\pi M) \approx 0.0437/M\]

The constant \(\ln(3)\) arises from the monodromy properties of the Teukolsky equation around the black hole horizon. For other black hole types:

- BTZ black hole (2+1 dimensions): QNM spectrum directly related to zeros of the Riemann zeta function
- Kerr black holes: asymptotic behavior depends on spin, with connections to quantum group invariants
- Higher-dimensional black holes: different number-theoretic constants appear

The key insight: the asymptotic QNM spectrum is determined by the topology of the horizon, not by the details of the metric.

## 3. The Riemann Zeta Function and Prime Numbers

### 3.1 The Euler Product

The Riemann zeta function satisfies the Euler product:

\[\zeta(s) = \prod_{p\ \mathrm{prime}} (1 - p^{-s})^{-1}\]

This directly connects the zeta function to prime numbers: the zeros of \(\zeta(s)\) encode the distribution of primes through the explicit formula:

\[\pi(x) \sim \mathrm{Li}(x) - \sum_{\rho} \mathrm{Li}(x^{\rho}) + \cdots\]

where \(\pi(x)\) is the prime counting function and the sum is over non-trivial zeros \(\rho\) of \(\zeta(s)\).

### 3.2 The Spectral Interpretation

The Hilbert-Pólya conjecture proposes that the non-trivial zeros of \(\zeta(s)\) correspond to eigenvalues of a self-adjoint operator:

\[\mathrm{Re}(\rho) = 1/2 + i\cdot\lambda_n\]

where \(\lambda_n\) are eigenvalues of some unknown Hermitian operator. If such an operator exists, the Riemann hypothesis (all zeros on \(\mathrm{Re}(s) = 1/2\)) follows immediately.

The connection to black holes: if the "unknown operator" is related to the Laplacian on a compact manifold (the black hole horizon), then the QNM frequencies — which are eigenvalues of the horizon's wave equation — could correspond to the Riemann zeros.

## 4. DA Analysis: Horizon Topology and Prime Numbers

### 4.1 The DA Hypothesis

The Domain Architect framework proposes that the event horizon is not merely a coordinate singularity (as in classical GR) but a compact manifold with non-trivial topology. The QNM frequencies are the eigenvalues of the Laplace-Beltrami operator on this manifold:

\[\omega_n^2 \sim \lambda_n(\text{horizon manifold})\]

The spectral zeta function of the horizon manifold:

\[\zeta_{\mathrm{horizon}}(s) = \sum_n \lambda_n^{-s}\]

is the quantity that connects to the Riemann zeta function.

### 4.2 The Key Claim

**[SPECULATIVE]** If the horizon manifold's spectral zeta function coincides with (or is a quotient of) the Riemann zeta function, then the black hole's QNM spectrum could encode the distribution of prime numbers. This is a proposed interpretation, not an established mathematical theorem. The spectral zeta function of the horizon manifold has not been computed.

This is not as far-fetched as it sounds:

- Spectral zeta functions of compact manifolds are well-studied objects in mathematical physics. For simple manifolds (sphere, torus), they can be computed exactly.
- The Riemann zeta function is closely related to a spectral zeta function — specifically, the spectral zeta of the circle \(S^1\) is \(\zeta_{S^1}(s) = 2\zeta(2s)\), whose zeros derive directly from the Riemann zeta (the non-trivial zeros sit at \(s = 1/4 + it/2\)).
- If the horizon topology is related to \(S^1\) (as it is for axisymmetric black holes, where the horizon has a \(U(1)\) isometry), then the spectral zeta function naturally involves \(\zeta(s)\).
- For more complex horizon topologies (e.g., quotient spaces \(S^1/\mathbb{Z}_n\)), the spectral zeta function involves Dirichlet \(L\)-functions, which generalize the Riemann zeta function and are deeply connected to prime distributions in arithmetic progressions.

### 4.3 The DA Prediction

The DA framework makes a specific, falsifiable prediction:

**[SPECULATIVE — proposed prediction]** The highly damped QNM frequencies of a black hole should exhibit a spectral structure that matches the zeros of the Riemann zeta function (or a related \(L\)-function), with the matching improving as the mode number \(n\) increases. This prediction extends beyond the Motl-Neitzke asymptotic result and has not been tested.

This prediction differs from the Motl-Neitzke result (which only concerns the asymptotic limit) by predicting the full spectral structure, not just the asymptotic behavior.

### 4.4 Why This Is Beautiful

The connection would mean:

- Prime numbers — the "atoms" of arithmetic — are encoded in the ringdown of black holes
- The event horizon's topology determines which primes are "visible" in the gravitational wave spectrum
- The Riemann hypothesis could be tested experimentally (in principle) by measuring enough black hole QNMs
- The deepest connection between number theory and physics would be established

## 5. Commonly Measured Black Hole Parameters

### 5.1 Binary Black Hole Mergers (LIGO/Virgo/KAGRA)

From GWTC-5.0 (May 2026, 390 total detections):

| Parameter | Symbol | Typical Range | Measurement Method |
|---|---|---|---|
| Chirp mass | \(\mathcal{M} = (m_1 m_2)^{3/5}/(m_1+m_2)^{1/5}\) | 10–60 \(M_\odot\) | Most accurately measured; from GW phase evolution |
| Component masses | \(m_1, m_2\) | 5–100 \(M_\odot\) | From waveform morphology (less precise than \(\mathcal{M}\)) |
| Mass ratio | \(q = m_2/m_1\) | 0.1–1.0 | Formation channel indicator |
| Effective spin | \(\chi_{\mathrm{eff}}\) | −0.5 to +0.9 | Aligned spin combination; from phase corrections |
| Precession spin | \(\chi_p\) | 0–0.5 | In-plane spin; from waveform modulations |
| Luminosity distance | \(d_L\) | 100–5000 Mpc | From GW amplitude (degenerate with inclination) |
| Inclination | \(\iota\) | 0–180° | Angle to orbital normal (degenerate with distance) |
| Final mass | \(M_f\) | ~95% of \(M_{\mathrm{total}}\) | From energy radiated in GWs |
| Final spin | \(a_f\) | 0.6–0.8 | From ringdown frequency + area theorem |
| Ringdown frequency | \(f_{\mathrm{QNM}}\) | 100–300 Hz | Fundamental mode of remnant (Berti-Cardoso-Will) |
| Sky localization | \(\Delta\Omega\) | 10–1000 deg² | From time delay + amplitude differences between detectors |

Table 1. Binary black hole merger parameters. The chirp mass is measured to ~1% precision; individual masses to ~10-20%; spins to ~0.1-0.5. GW250114 (January 2025) is the loudest event to date.

### 5.2 Supermassive Black Holes (EHT, reverberation mapping, stellar dynamics)

| Parameter | Symbol | Typical Range | Measurement Method |
|---|---|---|---|
| Mass | \(M_{\mathrm{BH}}\) | \(10^6\)–\(10^{10}\,M_\odot\) | Stellar dynamics, gas dynamics, reverberation mapping |
| Spin | \(a/M\) | 0–0.998 | X-ray reflection (iron K-α line profile), continuum fitting |
| Accretion rate | \(\dot M\) | 0.01–1.0 \(\dot M_{\mathrm{Edd}}\) | From bolometric luminosity (\(L = \eta\dot M c^2\)) |
| Schwarzschild radius | \(R_s = 2GM/c^2\) | 0.3–300 AU | Derived from mass |
| Shadow diameter | \(d_{\mathrm{shadow}}\) | \(\sim 5 R_s\) | Direct imaging (EHT: M87*, Sgr A*) |
| Photon ring radius | \(r_{\mathrm{ph}}\) | \(\sim 1.5 R_s\) (Schwarz.), \(\sim 0.5 R_s\) (extremal) | Theoretical + EHT imaging |
| ISCO radius | \(r_{\mathrm{ISCO}}\) | 1–6 \(M\) | Derived from spin (spin-dependent) |
| Jet power | \(P_{\mathrm{jet}}\) | \(10^{38}\)–\(10^{40}\) erg/s | Radio/X-ray jet luminosity |
| Magnetic field | \(B\) | 1–100 Gauss | From polarization (EHT: Sgr A* in polarized light) |
| Eddington luminosity | \(L_{\mathrm{Edd}}\) | \(1.26\times 10^{38} (M/M_\odot)\) erg/s | Theoretical maximum |

Table 2. Supermassive black hole parameters. M87* (\(M = 6.5\times 10^9 M_\odot\)) and Sgr A* (\(M = 4.0\times 10^6 M_\odot\)) are the only two directly imaged. The EHT polarized-light image of Sgr A* (March 2024) revealed organized magnetic field structure spiraling from the horizon.
