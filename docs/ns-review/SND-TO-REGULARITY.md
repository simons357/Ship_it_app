# SND-to-regularity implication (fluids book)

**Date:** 2026-09-15  
**Clay NS status:** not claimed  
**SND status:** hypothesis (open)  
**Phi-renorm / \(1/r^4\):** not in this chain  
**Numerical sweeps:** none in this pass  

This note writes the **SND \(\Rightarrow\) regularity** arrow as it actually sits in the frozen sources, before any further DNS. It does not close Clay Statement B. It does not merge the two \(\rho\) packagings. It does not feed swirl algebra into spectral \(H\).

**Sources (other branches; not merged into this freeze):**

| Object | Path | Typical branch |
|---|---|---|
| Ring + SND TeX | `docs/papers/SND_RING_LEMMA_NS.tex` | `cursor/tao-snd-h-panel-a0eb` |
| Tao panel | `docs/math/TAO-MATH-PANEL-SND-H.md` | same |
| Status companion | `docs/math/SND-H-STATUS.md` | same |
| Phi-free graph | `docs/math/PHI-FREE-SND-CHAIN.md` | same |
| T2 note | `docs/papers/submit/03_t2_shell_flux_gronwall.tex` | same |
| Tweet / DA weld | `docs/ns-review/SND-TWEET-DA-AUDIT.md` | `cursor/da-snd-gap-closure-0cc5` |
| Enstrophy barycenter | `docs/TRACK-B-CLIMB-LAW.md` | `cursor/unaugmented-r4-vorticity-f80e` |

Zenodo face of the Ring paper: `10.5281/zenodo.20518057`. Conditional KEEP face: `10.5281/zenodo.22050976`.

---

## 0. Status strings (do not “improve”)

| Object | Status |
|---|---|
| Clay Navier–Stokes | `not claimed` |
| Unaugmented NS + SND | hypothesis (open) |
| Theorem D “Clay \(\Leftrightarrow\) [SND]” | **RETIRE** (`TH-H2`) |
| Fluids Theorem H / SND-C | honest **conditional**; warn `TH-H1` (\(X\le M\)) |
| Arithmetic \(H_N\) | different object; no Clay impact |
| Triple Lock `SND \(\equiv\) GNC \(\equiv\) Bridge` | **RETIRED** |
| Axisymmetric KEEP identity | algebra in the swirl book; **no edge** into this graph |

---

## 1. Freeze the names (two opposite \(\rho\)s)

Do not merge these. The June 5 Triple Lock slogan used the **upper-bound** convention; Ring / Tao-panel SND-U is the **lower-bound** convention. They are opposites.

### 1.1 SND-U (Ring / Tao panel) — enstrophy, concentration

On a Leray–Hopf solution on \(\mathbb{T}^3\), Littlewood–Paley shells \(\Delta_j\),

\[
X_j = 2^{2j}\|\Delta_j u\|_{L^2}^2,\qquad
X = \sum_j X_j = \|\nabla u\|_{L^2}^2,\qquad
J = \max_j X_j,\qquad
\rho = J/X \in (0,1],\qquad
j_* = \operatorname{argmax}_j X_j.
\]

**[SND-U]** means

\[
\inf_t \frac{J(t)}{X(t)} \ge c_* > 0.
\]

A **uniform positive fraction of enstrophy** sits in a dominant LP shell. “Non-dispersal” here means: enstrophy is **not** spread thinly over all shells.

### 1.2 T2 \(\rho\) — energy, non-concentration

In `03_t2_shell_flux_gronwall.tex`,

\[
E_j = \|\Delta_j u\|_{L^2}^2,\qquad
X = \sum_j E_j = \|u\|_{L^2}^2,\qquad
a_j = E_j/X,\qquad
\rho = \sup_j a_j.
\]

**[SND-T2]** means \(\sup_t \rho(t) \le \rho_0 < 1\): no single **energy** shell holds the whole \(L^2\) mass. The TeX itself records that this is **not** identical to SND-U.

T2’s energy bound \(X(t)\le\|u_0\|_{L^2}^2\) is Leray (L1) and is **not** circular. Do not confuse that energy \(M\) with the enstrophy bound \(X=\|\nabla u\|_2^2\le M\) used in Theorem H.

### 1.3 Triple Lock slogan (retired identity)

“Max shell fraction \(\le\rho_0\)” is the T2-style **upper** bound. It is the opposite of SND-U. The identity `SND ≡ GNC ≡ Bridge` is retired. Do not revive it to glue these \(\rho\)s.

---

## 2. What the shell condition actually controls

SND-U is a statement about **one ratio** and **one index**:

\[
\rho(t) = \frac{X_{j_*(t)}(t)}{X(t)} = \frac{J(t)}{X(t)}.
\]

### 2.1 Objects under control (when SND-U is assumed)

| Object | What SND-U says about it |
|---|---|
| Dominant-shell share | \(X_{j_*}=J\ge c_* X\) at every time of the interval |
| Spread regime \(\rho\to 0\) | **Forbidden** as a sustained state |
| Number of comparable shells | Cannot have \(\lceil X/J\rceil\to\infty\) many shells each carrying \(\sim J\) |
| Theorem F (spread Poincaré) | The super-exponential dissipation lower bound \(\mathcal D\ge\nu\cdot 4^{N-1}\rho X\) with \(N\sim 1/\rho\) is **not** the SND-U regime; it is the regime SND-U excludes |

The intended dynamical reading is: if a uniform fraction of enstrophy lives at one dyadic scale, the cascade cannot hide the stretching in a thin film of shells.

### 2.2 Objects **not** controlled by SND-U alone

| Object | Why SND-U is silent |
|---|---|
| The value of \(X(t)\) itself | Concentration of a large enstrophy is still a large enstrophy |
| \(\|\omega\|_{L^\infty}\) | Spectral floor on \(L^2\) shells is not Beale–Kato–Majda |
| The index \(j_*(t)\) | \(\operatorname{argmax}\) can jump; SND-U does not freeze it |
| \(\sup_t j_*(t)\) or \(\int 2^{2j_*(t)}\,dt\) | The viscous factor in the shell ODE is uncontrolled if \(j_*\to\infty\) |
| The flux \(\Pi_{j_*}\) | Needs a separate estimate (SND-C / Theorem H) |
| Sign of \(\dot j_*\) or \(\frac{d}{dt}j_{\mathrm{bar}}\) | Frequency drift is extra data; see §3 |
| Axisymmetric remainder \(T_{j\leftarrow j}\) | Different class (\(\mathbb{R}^3\) swirl); not this \(\mathbb{T}^3\) chain |
| Clay Statement B | Would require SND-U for **all** Leray–Hopf data **and** an M-free implication |

### 2.3 What SND-C / Theorem H is supposed to add

Shell evolution at the dominant index (Ring TeX, Theorem G):

\[
\frac{d}{dt}X_{j_*}
= -2\nu\cdot 2^{2j_*} X_{j_*} + 2\Pi_{j_*}.
\]

**(SND-C)** is a **pointwise-in-shell** flux bound at \(j_*\):

\[
|\Pi_{j_*}|
\le C_*\Bigl(\nu\cdot 2^{2j_*} X_{j_*} + X^{1/2}\mathcal D^{1/2}\Bigr).
\]

Bony split of \(\Pi_{j_*}\): \(T\) (low\(\times\)high), \(T^*\) (high input), \(R\) (near-diagonal \(|k-j_*|\le 4\)).

**What this controls, if granted:** energy cannot drain from the **current** dominant shell faster than that shell’s own viscous damping plus a remainder of size \(X^{1/2}\mathcal D^{1/2}\). It is a shell-localized cousin of a commutator / energy-transfer bound, not a bound on \(X\).

**What the written (SND-C) is actually proved under (Theorem H):** see §4. The written hypotheses are **spread** \(\rho\le\rho_0\ll 1\) and **\(X\le M\)**. That is not the SND-U regime.

### 2.4 Intended arrows (phi-free)

From `PHI-FREE-SND-CHAIN.md`, with the circularity marked:

```text
LP shells X_j, X, J, ρ = J/X
        │
        ▼
   SND-U: inf J/X ≥ c_* > 0     (do not swap in T2’s ρ ≤ ρ_0)
        │
        ├──────────────► T2 flux |Φ_j| ≤ C 2^{-0.8 j} X^{1/2} D^{1/2}
        │                      (T2 packaging; H^{2.3} ball; Q1-augmented s=2.3)
        │
        ├──────────────► Ring Lemma (band-limited toolkit; does not imply SND-U)
        │
        └──────────────► SND-C / Theorem H
                         written for SPREAD + X ≤ M
                              │
                              ▼
                    conditional regularity under SND
                    [OPEN: remove X≤M; align regime with SND-U]
```

No edge from \(\partial_z(\Phi_{\mathrm{swirl}}^2)\) or Hardy \(r^{-4}\) into this graph. Track B swirl is parallel, not upstream of fluids Theorem H.

### 2.5 The regime mismatch (the implication is not one lemma)

The Ring paper’s own glue is **not** “assume SND-U, conclude \(H^1\)”. It is a two-regime argument:

1. **Spread** \(\rho\le\rho_0\): prove SND-C (Theorem H), then Theorem G claims \(\dot\rho>0\) whenever \(\rho\) is small, so the solution cannot stay spread, hence SND-U holds.
2. **Concentrated** \(\rho\ge c_*\): Theorem D claims Prodi–Serrin / Ladyzhenskaya–Prodi–Serrin shell-by-shell, hence no blowup.

Those are two different jobs. SND-U (concentration) is the **output** of the spread analysis and the **input** of the regularity claim. Theorem H does not run in the concentrated regime as written. Closing either job with \(X\le M\) in the hypotheses is using the \(H^1\) bound the argument is supposed to produce (`TH-H1`).

---

## 3. Frequency drift — what extra information is needed

SND-U does **not** by itself give a law for \(j_*(t)\). The shell ODE above treats \(j_*\) as if it were slowly varying. A jump of the argmax, or a steady climb of the enstrophy mass, changes the viscous coefficient \(2^{2j_*}\) independently of \(\rho\).

### 3.1 Three different “drift” objects (do not collapse)

| Symbol | Definition | Status |
|---|---|---|
| \(j_*(t)=\operatorname{argmax}_j X_j\) | Dominant-shell **index** | Can jump; no freeze from SND-U |
| \(j_{\mathrm{bar}}=\bigl(\sum_j j\,X_j\bigr)/X\) | Enstrophy **barycenter** | Continuous when \(X>0\); Track B reading, not a theorem |
| \(\tau_k\sim M/(\nu\Lambda_k^2)\) | Viscous time in the Ring large-data proposition | Uses the a priori \(M\) |

A bound on \(j_{\mathrm{bar}}\) is not a bound on \(j_*\). A DNS reading of \(\dot j_{\mathrm{bar}}\) is not an a priori.

### 3.2 What a clean SND-U \(\Rightarrow\) regularity argument still needs

State these as missing lemmas. Do not invent constants.

1. **Control of the viscous factor without \(M\).** Either \(\sup_t j_*(t)<\infty\) on the existence interval, or an integrable bound on \(\int 2^{2j_*(t)}\,dt\), from SND-U + dissipation + \(u_0,\nu\) only.
2. **A jump rule.** When \(j_*\) changes, the identity \(\rho=X_{j_*}/X\) refers to a **new** shell. Theorem G’s ODE for \(\dot\rho\) is written as if \(j_*\) were fixed on the interval where \(\rho\) is small. One needs: isolated jumps, or a modulus of continuity for \(j_*\), or a formulation in \(j_{\mathrm{bar}}\) that does not assume uniqueness of the argmax.
3. **Sign of the cascade under SND-U.** Viscosity damps high shells first, so \(j_{\mathrm{bar}}\) tends to **fall**. Nonlinear flux can still climb. The dangerous concentrated scenario is not spread; it is \(\rho\ge c_*\) **and** \(j_*\to\infty\) (enstrophy locked to a runaway scale). SND-U does not forbid that.
4. **A time-scale comparison that does not feed on \(M\).** The Ring large-data proposition compares Lipschitz \(\lvert\partial_t(J/X)\rvert\le C\Lambda_k^2/\delta\) to the viscous time \(\tau_k\sim M/(\nu\Lambda_k^2)\) and concludes the drift of \(J/X\) over \(\tau_k\) is \(O(M/(\nu\delta))\). That estimate **is** an \(M\)-estimate. Replacing \(M\) by \(\|u_0\|_{H^1}\) is exactly `TH-H3-BOOT`. Leaving \(M\) as “the bound we already have” is circular for large-data NS.

### 3.3 What Track B already measured (not this theorem)

On 3-shell CONC packets (`docs/TRACK-B-CLIMB-LAW.md`):

- \(j_{\mathrm{bar}}\) is readable (`B12`).
- Instantaneous \(c=\mathrm{d}j_{\mathrm{bar}}/\mathrm{d}t\) is a finite number from the vorticity RHS (`B12a`).
- “Random CONC at \(t=0\) produces \(c\ge 8\)”: **fail**. Euler drift \(\sim 10^{-4}\) even at \(X=40\). Viscous drift \(\approx -1.4\) (`B12b`).
- “Viscosity is a ladder”: **fail**. High shells damp first; \(j_{\mathrm{bar}}\) falls (`B12c`).
- Short or longer evolution as a saving climb: **fail**. DNS is not an a priori (`B12d`, `B13f`).
- “\(t=0\) drift is an NS a priori”: **fail** (`B12e`).

Do **not** type a climb constant \(c=8\) into the SND-U estimate. Those readings are Track B / CONC packets on a vorticity RHS, not a proved SND-U drift law on \(\mathbb{T}^3\).

### 3.4 Axisymmetric leftover (different book)

`docs/AXISYM-SHELL.md` leftover is \(T_{j\leftarrow j}\) for swirl on \(\mathbb{R}^3\). It is not SND-U, not Lemma★, not unrestricted 3D. Do not glue it onto this \(\mathbb{T}^3\) implication.

---

## 4. Does the written proof assume the desired bound?

**Yes, in the load-bearing places.** The desired bound for Clay on this track is a uniform \(H^1\) bound \(X(t)=\|\nabla u(t)\|_{L^2}^2\le M\) produced from \(u_0\) and \(\nu\) only. Several lemmas take that \(M\) (or a stronger ball) as **input**.

### 4.1 Circularity table

| Written statement | Hypothesis that is the conclusion | Verdict |
|---|---|---|
| **Theorem H** (SND-C) | \(X\ge\delta_*\), **\(X\le M\)**, and **spread** \(\rho\le\rho_0\ll 1\) | **Circular for large-data NS** (`TH-H1`). Also the **wrong regime** for SND-U |
| Theorem H, diagonal \(R\) | Young with \(X_{j_*}\le M\) | Same \(M\) |
| Theorem H, \(T^*\) | \(\|u\|_{L^\infty}\lesssim M^{1/2}\); \(C_{T^*}=C_{T^*}(\nu,M,\rho_0)\) | Same \(M\) |
| **Theorem E** | Smooth \(u\) with \(X(t)\le M\) on \([0,T]\) | SND-U as a **consequence of already-bounded smooth \(H^1\)**, not the converse |
| **Theorem G** | \(c_*=c_*(\nu,\delta_*,M,C_S)\); uses SND-C | Still \(M\)-dependent even if SND-C is granted |
| Corollary “threshold closure” | SND-C \(\Rightarrow\) Clay on \(\mathbb{T}^3\) | Packaging glue; **RETIRE** as Clay |
| **Theorem D(i)** | “Uniform [SND] with Theorem C gives \(\|u^\varepsilon\|_{H^1}\le M\)” | The SND \(\Rightarrow H^1\) arrow is asserted by quoting a bound \(M\) already in hand |
| Large-data cascade proposition | \(\delta\gg C_S\nu M^2\), \(\tau_k\sim M/(\nu\Lambda_k^2)\) | Drift control **uses \(M\)** |
| Case A (bounded \(H^2\)) | \(M=\sup_k X(t_k)^{1/2}\) | A priori \(H^1\) |
| **T2 Lemma 2** | \(\|u\|_{H^{2.3}}\le R_\varepsilon\) absorbing ball | Stronger than the regularity being concluded. Exponent \(-0.8j=(3/2-2.3)j\) is Bernstein \(+3j/2\) against **that** ball. Remark in the TeX: \(s=2.3\) is the **\(Q_1\)-augmented** parameter — a **different PDE** |
| T2 Theorem 2 | SND-T2 **and** the \(H^{2.3}\) ball | Conditional on both |
| T2 energy (L1) | \(X=\|u\|_2^2\le\|u_0\|_2^2\) | **Not circular** (Leray). Wrong \(X\) for Theorem H |
| T2 Lemma 1 | Incompressibility \(\Rightarrow\) low-frequency self-flux vanishes | **Not circular** |

### 4.2 Theorem D is not a refereed equivalence

DA disposition: **RETIRE** (`TH-H2`). Two independent defects:

1. **Forward arrow (i)** uses Theorem C to produce \(M\), then Ladyzhenskaya–Prodi–Serrin. That is not an M-free derivation from SND-U.
2. **Converse (ii)** mixes Escauriaza–Seregin–Šverák \(L^3\) blowup with the claim that \(J/X\ge c_*\) plus Sobolev would keep \(\|u\|_{L^3}\) comparable to \(\|u\|_{H^1}\). As written it is not a clean lemma that blowup of \(X\) forces \(\rho\to 0\).

Until both arrows are rewritten without feeding \(X\le M\) from the endgame, “Clay \(\Leftrightarrow\) [SND]” is packaging, not a theorem.

### 4.3 What is **not** circular (keep these)

- Leray energy inequality and finite total dissipation (T2 (L1)(L2)).
- Exact cancellation of low-frequency self-flux by \(\operatorname{div}u=0\) (T2 Lemma 1).
- The **hypothesis string** [SND-U] itself, when labelled as a hypothesis.
- Ring Lemma as a geometric toolkit that **does not** imply SND-U.
- KEEP swirl algebra in the axisymmetric book (different graph).

### 4.4 Two H’s (do not add)

| Object | Meaning | Clay impact |
|---|---|---|
| Fluids **Theorem H** | SND-C under \(X\le M\) and spread | Conditional; circular risk |
| Arithmetic **\(H_N\)** | Inverse-GCD matrix | None unless a map to Leray–Hopf is proved |

---

## 5. What would make the implication honest (no new sweeps)

These are the math jobs. They are not numerical.

1. **Rewrite Theorem D / Main Theorem as conditional on SND-U.** Do not mark Clay B proved.
2. **`TH-H3-BOOT`:** either drop \(X\le M\) from Theorem H, or produce \(M=M(\|u_0\|_{H^1},\nu)\) only — never from the conclusion.
3. **Align the regime.** Prove a flux bound that runs under **SND-U concentration** \(\rho\ge c_*\), or give a jump/drift lemma that converts spread-SND-C into “cannot enter spread” **without** \(M\). Do not quote spread hypotheses as if they were SND-U.
4. **Write the drift law** asked in §3.2: \(j_*\) vs \(j_{\mathrm{bar}}\), sign of cascade, integrable \(2^{2j_*}\), no typed \(c=8\).
5. **Keep T2 separate.** Its \(\rho\) is energy non-concentration; its flux lemma uses an \(H^{2.3}\) ball from the \(Q_1\)-augmented system. That ball is not unaugmented NS.
6. **Keep Phi-renorm + Ring as method notes.** No edge into this graph. No \(1/\gcd\) Bridge. No Triple Lock.

Tao’s barrier still applies: 3D NS is energy-supercritical; SND-U is an **extra** structural hypothesis. Until SND-U (or an equivalent critical control) is proved for all Leray–Hopf data **without assuming the \(H^1\) bound it concludes**, the implication is a conditional regularity criterion of the same genus as BKM / LPS, spectral — not Statement B.

---

## 6. One-paragraph answer

The shell condition **SND-U** controls only the **share** of enstrophy in the dominant Littlewood–Paley shell, \(\rho=J/X=X_{j_*}/X\ge c_*\). It does not control the size of \(X\), the location or speed of \(j_*\), or the flux \(\Pi_{j_*}\). Closing regularity still needs (i) a pointwise flux bound at \(j_*\) that does not assume \(X\le M\), and (ii) extra information on **frequency drift**: how \(j_*\) jumps, whether the barycenter climbs or falls, and a bound on \(\int 2^{2j_*}\,dt\) from \(u_0,\nu\) only. The written Theorem H proves the flux bound in the **opposite** (spread) regime **and** under \(X\le M\); Theorem E and Theorem D(i) likewise assume the \(H^1\) bound they want; T2’s flux lemma assumes an \(H^{2.3}\) absorbing ball from a \(Q_1\)-augmented PDE. Those are the circularities. Theorem D remains retired. Clay is not claimed.
