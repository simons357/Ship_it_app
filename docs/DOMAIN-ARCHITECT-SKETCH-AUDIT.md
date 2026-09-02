# Domain Architect unaugmented sketch: what to keep

**Shelved as an outline.** SFE, HB, Domain Architect, and Millennium packaging are off the live desk (`docs/SHELF.md`). This file is only an audit of a Gemini rewrite. Steps 0–2 that are classical NS may already live on Track B; do not restart from this sketch.

Feedback on the Flash Extended rewrite (classical 3D system, LP, Bony, geometric depletion, cubic enstrophy, BKM). Fluids only. This is a table of contents, not a closed argument.

The Domain Architect / Harmonic Blueprint mark is branding. It is not an input to \(\Pi_j\) or \(\omega\cdot S\omega\). HB Experiment 01 already failed to reject its null; do not wire `nodes.json` into this track.

SFE / UHF / DHFA **are** the old Harmonic Blueprint stack, not Gemini’s LP/Bony/BKM sketch. Public names (site + 2025 DHFA/UHF note):

| Acronym | Name | What it is |
|---|---|---|
| **SFE** | Simons Field Equation | Chapter-1 field: \(\Phi(x,t)=\sum_p A_p\sin(2\pi f_p t/\varphi(x)+\delta_p)\). Prime-indexed oscillator + coherence attractor. Different PDE from NS and from \(Q_1\). |
| **UHF** | Unified Harmonics Framework | Wrapper: primes, curvature, zeta, entropy in one recursive story |
| **DHFA** | Dynamic Harmonic Field Architecture | Time-varying potential \(V_{\mathrm{DHFA}}(x,t)\); standing-wave / coherence engine |

The book text is **not** in this repo. Do not reconstruct chapters from the website one-liner or from Gemini. “Domains” in that book are the thing Domain Architect is trying to remember: more than one domain type, not primes only.

GCD-attractor + SFE was already withdrawn as a closure in the August errata. HB Experiment 01 (this repo) did not reject H0 on a prime-indexed node family. Those two facts stay on the table when Chapter 1 is SFE.

---

## Verdict

Use Steps 0–2 as the **opening of Track B**. Rewrite Steps 3–5 before they become chapters. The sketch already names the real gap (Biot–Savart does not force \(\cos\alpha_3\to 0\)). Keep that sentence. Drop the closures that ignore it.

On \(\mathbb{R}^3\) vs \(\mathbb{T}^3\): the sketch is written on \(\mathbb{R}^3\). The live notes are on \(\mathbb{T}^3\). Pick one manifold per chapter and stay there. Periodic is the right first book; whole-space decay is a later paper.

---

## Line-by-line

### Keep (Chapter 0–2)

| Sketch piece | Why it stays |
|---|---|
| Classical NS, \(\nabla\cdot u=0\), no \(Q_1\) | Track B PDE |
| Vorticity form, stretching \(S\omega\) | Correct |
| \(\omega=\sum\Delta_j\omega\), shell enstrophy | Correct. Freeze \(X_j=2^{2j}\|\Delta_j u\|_2^2\) as in the Ring note, not a second unnamed \(\|\omega_j\|_2^2\) bookkeeping |
| Bony split of \(\Pi_j=\int\Delta_j[(\omega\cdot\nabla)u]\cdot\omega_j\) | Correct skeleton |
| \(\lvert\Pi_j^{\mathrm{low}}\rvert\le C\|\nabla u\|_\infty\|\omega_j\|_2^2\) | Standard commutator. Does not need geometry |
| \(\mathrm{Tr}\,S=0\Rightarrow\lambda_1+\lambda_2+\lambda_3=0\) | Identity |
| \(\omega\cdot S\omega=\lvert\omega\rvert^2\sum\lambda_i\cos^2\alpha_i\) | Identity |
| Energy \(\frac12\|u\|_2^2+\nu\int\|\nabla u\|_2^2=\frac12\|u_0\|_2^2\) | Leray. Unconditional |

The low-frequency bound is the one T2 Lemma 1 sharpens: the self-flux of a divergence-free low field against itself vanishes. Put that lemma in Chapter 2, not a slogan.

### Rewrite or drop (old Steps 3–5)

**Step 3 — “Biot–Savart forces \(\cos\alpha_3\to 0\) as \(j\to\infty\).”**  
The kernel for \(S\) is fine to display. The dynamical claim is not a theorem. Constantin–Fefferman-type depletion is a *criterion*: if alignment is depleted, stretching is weaker. Biot–Savart does not force that for arbitrary large data, and it does not forbid singular concentrations. The sketch’s own “unresolved core” paragraph is the correct status. Chapter 3 must be **conditional geometry** (Ring on \(E_c\) under 3-CONC / EQ3), not an unconditional orthogonality law.

**Step 4 — flux \(\sum\Pi_j\le C\|\omega\|_2^{3/2}\|\nabla\omega\|_2^{3/2}\).**  
This is the classical Hölder / Sobolev bound. It does not use depletion. If you already have it, the geometric story in Step 3 did no work. After Young (\(p=4/3\), \(q=4\)) you get the cubic enstrophy inequality

\[
\frac{d}{dt}\mathcal{E}+\frac\nu2\|\nabla\omega\|_2^2\le C\nu^{-3}\mathcal{E}^3.
\]

(The screenshot dropped the \(\|\omega\|_2^6\) factor in the Young remainder; the closed form with \(\mathcal{E}^3\) is the intended one.) Cubic growth **can** blow up. This is the standard barrier, not a closing.

**Step 5 — “\(\int\mathcal{E}\,dt<\infty\) kills the cubic” and “bounded \(\|\omega\|_2\Rightarrow\) BKM.”**  
Both false.

- Leray gives \(\int_0^\infty X(t)\,dt<\infty\) with \(X=\|\omega\|_2^2\). The ODE \(\dot X\le C X^3\) still allows \(X\sim(T_*-t)^{-1/2}\), which is integrable and unbounded.
- Beale–Kato–Majda needs \(\int\|\omega\|_\infty\,dt<\infty\). Bounded enstrophy is \(L^\infty_t L^2_x\). That does not imply \(L^1_t L^\infty_x\).

Do not write a BKM chapter that starts from \(\|\omega\|_2\). If a later chapter reaches \(\int\|\omega\|_\infty<\infty\), BKM is then a citation, not a new idea.

---

## Better chapter map (use these names)

Until SFE / UHF / DHFA are on disk, the book is:

| Ch | Title | Load-bearing object | Status |
|---|---|---|---|
| 0 | Track B PDE | Classical NS on \(\mathbb{T}^3\). Energy. Enstrophy identity. No \(Q_1\), no \(\Phi\) cancel | Written |
| 1 | Littlewood–Paley bookkeeping | \(X_j\), \(X\), \(J\), \(\rho\), packet \(P_{j_*}\), \(\sigma\), \(\kappa\) | Written |
| 2 | Bony flux | \(T+T^*+R\). T2 Lemma 1. Kato–Ponce on \(T^*\). Low \(T\) isolated | Partial |
| 3 | Concentrated regime | 3-CONC \(\sigma\ge 1/2\). Almost-3-shell Ring on \(E_c\). EQ3 for clean \(R\) | Ring sketch; almost-band open |
| 4 | Spread regime | SPREAD \(\sigma\le 1/2\). Extra dissipation. SND-C without Phi, without \(H^{2.3}\) | Low \(T\) open |
| 5 | Swirl tube | Keep \(1/r^4\). Localized Hardy. Angular viscosity vs \(\Gamma\partial_z\Gamma/r^4\) | Setup |
| 6 | Glue | One threshold \(\sigma=1/2\). Occupation time. No energy-only cubic close | Open |
| A | Track A (separate book) | \(Q_1\), Ladyzhenskaya, \(\varepsilon>0\) | Drafted; different PDE |
| Q | Arithmetic (separate book) | Bridge\(^*\), Theorem P, \(H_N\ge-1\) | Not a fluids input |

SFE / UHF / DHFA are **not** chapters of Track B. They are a separate book. If Domain Architect is an app, each of those names is a *domain slot*: one equation, one test, no glue.

Drop SIMPLEX, withdrawn GCD-attractor closures, and any HB node family from the fluids chapters.

---

## Modifications that make the sketch better

1. **Change the manifold line** to \(\mathbb{T}^3\) for the first pass, or write two parallel statements.
2. **Freeze shell energy** as \(X_j=2^{2j}\|\Delta_j u\|_2^2\). One symbol through every chapter.
3. **Replace “non-dispersal”** with CONC / 3-CONC / SPREAD. Gemini’s “non-dispersal” is being used as geometric depletion. August SND is the opposite of June SND. One word cannot do both jobs.
4. **Step 3 becomes a hypothesis chapter:** “If the packet is 3-CONC and the field is almost band-limited, Ring gives \(\|\nabla\xi_0\|_{L^\infty(E_c)}\le C 2^{j_*}\).” No Biot–Savart slogan.
5. **Step 4 keeps Young only as the *obstacle*.** The chapter ends at the cubic barrier and lists what would beat it (Ring on \(E_c\), spread Poincaré, tube viscosity). It does not absorb and declare victory.
6. **Delete the BKM implication from \(\|\omega\|_2\).** BKM is a target, not a corollary of energy.
7. **Keep \(1/r^4\)** if Chapter 5 is swirl. Do not introduce \(\Phi\) in Chapter 0 “to simplify.”
8. **No inverse-GCD, no \(H_N\), no Bridge\(^*\)** in the fluids chapters. Those floors are real and stay in Book Q.
9. **Logo / DMA verbs (compose, map, reconstruct, optimize)** can label an app workflow. They are not proof steps.

---

## Reservations

- Starting from this Gemini chain and “then filling SFE → UHF → DHFA” will recreate the May T³ overclaim if Step 3–5 stay as written. The definitions we already froze are stricter and shorter. Use those as the spine; use the sketch as a narrative wrapper.
- “Domain mapping” sounds like it will assign a sign or a domain type to each shell. That is fine for software. If a later chapter treats a mapped sign as a bound on \(\Pi_j\), the argument is no longer fluids.
- I cannot line-edit the HB book until those chapters are in the repo. Public SFE is a prime oscillator, not \(\partial_t\omega+(u\cdot\nabla)\omega=(\omega\cdot\nabla)u+\nu\Delta\omega\). Putting SFE as Chapter 1 of the unaugmented NS note mixes books.

---

## What to write next, in order

1. Chapter 0–1 as a clean \(\mathbb{T}^3\) note (mostly copy from `UNAUGMENTED-R4-VORTICITY-PLAN.md` §§1–3, 9).
2. Chapter 2: Bony + T2 Lemma 1, low \(T\) marked open.
3. Chapter 3: 3-shell Ring, not Biot–Savart depletion.
4. Send the actual HB/SFE chapter files if you want them audited. Domain Architect can *route* NS vs SFE vs inverse-GCD. It cannot make SFE imply Track B.
