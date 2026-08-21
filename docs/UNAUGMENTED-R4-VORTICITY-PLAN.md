# Unaugmented vorticity plan, keeping \(1/r^4\)

Working note. Fluids only. No augmentation. Do not cancel the axis weight.

Sources used: August Phi note (22045467), August Ring+SND (22045474), June T2 (20552080), August Q6 hygiene (22045478). Older bundled closures are not used as load-bearing steps.

---

## 1. What you already have on vorticity

### Full 3D, periodic box

Vorticity form of the classical system:

\[
\partial_t\omega+(u\cdot\nabla)\omega=(\omega\cdot\nabla)u+\nu\Delta\omega,\qquad
\omega=\nabla\times u,\qquad \nabla\cdot u=0.
\]

Stretching identity (from the Gemini screenshots and the strain eigenframe):

\[
\omega\cdot S\omega=|\omega|^2\sum_{i=1}^3\lambda_i\cos^2\alpha_i,\qquad
\lambda_1+\lambda_2+\lambda_3=0.
\]

Littlewood–Paley shell energies (August Ring note):

\[
X_j=2^{2j}\|\Delta_j u\|_2^2,\qquad
X=\sum_j X_j=\|\nabla u\|_2^2=\|\omega\|_2^2,\qquad
J=\max_j X_j,\qquad
\rho=J/X.
\]

### Axisymmetric-with-swirl

Cylindrical field \(u=u_r\hat r+u_\theta\hat\theta+u_z\hat z\). Angular momentum

\[
\Gamma:=r u_\theta.
\]

The meridional vorticity equation carries the centrifugal source

\[
\frac1{r^4}\partial_z(\Gamma^2).
\]

That is the term you canceled by setting \(\Phi=\Gamma/r^2=u_\theta/r\). This note keeps it.

### Mechanisms already written down

| Mechanism | Where | What it actually is |
|---|---|---|
| Ring Lemma | 22045474 | One-shell Fourier support \(\Rightarrow\) \(\|\nabla\xi_0\|_{L^\infty(E_c)}\le C\,2^{j_*}\) |
| SND (August) | 22045474 | \(\inf_t J/X\ge c_*>0\): a dominant shell holds a fixed enstrophy fraction |
| SND (June T2) | 20552080 | \(\sup_t\rho(t)\le\rho_0<1\): **no** shell holds almost all enstrophy |
| T2 flux | 20552080 | Low-frequency self-flux vanishes by \(\nabla\cdot u=0\); remaining flux from high shells |
| Viscosity / shell-spread | 20552080 Thm 1 | If energy is spread, Poincaré / Bernstein give extra \(H^1\) damping |
| \(Q_1\) extra dissipation | 22045467 | **Not used here** |
| \(\Phi\) cancel | 22045467 Thm 2.2 | **Not used as the main path** |
| Inverse-GCD / Bridge\(^*\) | 22045478 | Matrix note only. Not a bound on \((u\cdot\nabla)u\) |

**Hygiene first.** August SND and June SND are opposite statements. Freeze two names:

- **Concentration.** \(J/X\ge c_*\). Dominant shell. Ring Lemma regime.
- **Spread.** \(\max_j X_j/X\le\rho_0<1\). Viscosity / T2 regime.

Do not call both SND. The two-regime argument needs both, under different names.

---

## 2. Why canceling \(1/r^4\) may have been the wrong first move

The identity

\[
\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)
\]

is true. It does not remove work. It moves the work onto \(\|\Phi\|_\infty\):

\[
\|\partial_z(\Phi^2)\|_2\le 2\|\Phi\|_\infty\|\partial_z\Phi\|_2.
\]

That is a stronger norm than the weighted \(L^2\) you started with. So the cancel can make the a priori estimate harder, not easier, unless you already have axis smoothness.

Keeping \(1/r^4\) has three structural advantages:

1. The weight is large only in a thin tube \(r<\delta\). Off the axis it is bounded.
2. The Stokes operator on the swirl component is also stronger in that same tube (the \(1/r^2\) angular terms). Danger and dissipation sit in the same place.
3. That is a concentration-versus-viscosity contest, which is the language of your Ring / T2 notes.

If the field is already smooth, \(u_\theta=O(r)\) on the axis, \(\Gamma=O(r^2)\), and \(r^{-4}\partial_z(\Gamma^2)\) is bounded. The issue is only the a priori estimate from \(H^1\), not a literal infinite source.

---

## 3. Unaugmented system (no \(Q_1\))

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,\qquad\nabla\cdot u=0.
\]

Axisymmetric-with-swirl class, or the full 3D vorticity form. No extra \(\varepsilon^\alpha P\mathrm{div}(|\nabla u|^\beta\nabla u)\).

Kinetic energy (unconditional, Leray):

\[
\frac12\|u(T)\|_2^2+\nu\int_0^T\|\nabla u\|_2^2\,dt\le\frac12\|u_0\|_2^2.
\]

Enstrophy is the object to close:

\[
\frac12\frac{d}{dt}\|\omega\|_2^2+\nu\|\nabla\omega\|_2^2
=\int(\omega\cdot S\omega)\,dx.
\]

In the swirl class the right-hand side contains the axis source. Split it.

---

## 4. Suggested proof architecture

### Step A — Keep \(\Gamma\). Do not pass to \(\Phi\) as the primary unknown

Write the meridional / swirl coupling in \(\Gamma\) and \(\omega^\theta\) (or \(\omega^r,\omega^z\)). \(\Phi\) may be recorded as a dual variable for comparison. It is not the estimate variable.

### Step B — Split the axis source at a tube radius \(\delta(t)\)

\[
\int\frac1{r^4}\partial_z(\Gamma^2)\,\omega^r\,r\,dr\,dz
=I_{\mathrm{off}}(\delta)+I_{\mathrm{tube}}(\delta).
\]

Off-axis, \(r\ge\delta\):

\[
\Bigl|\frac1{r^4}\partial_z(\Gamma^2)\Bigr|\le\delta^{-4}\,|\partial_z(\Gamma^2)|.
\]

This is a standard Sobolev term. Absorb part in \(\nu\|\nabla\omega\|_2^2\), leave a remainder depending on \(\delta^{-C}X\).

### Step C — Tube estimate, keep the weight

On \(r<\delta\),

\[
\frac1{r^4}\partial_z(\Gamma^2)=\frac{2\Gamma\,\partial_z\Gamma}{r^4}.
\]

Use \(\Gamma=r u_\theta\) and a Poincaré / Hardy inequality **localized to the tube**, not a global \(r^{-4}\) Hardy on all of \(\mathbb{R}^3\). Typical shape:

\[
|I_{\mathrm{tube}}|
\le C\nu\|\nabla\omega\|_2^2
+C_\nu\,\delta^{-\alpha}\|\Gamma/r\|_{L^2(\mathrm{tube})}^2\,X^\beta.
\]

The leftover should be controlled by kinetic energy of swirl in the tube plus viscosity. This is the estimate you avoided by canceling. It is also the estimate that matches the geometry: only the tube can be bad.

If this localized Hardy fails at the endpoint, lower \(\delta\) or add an angular Poincaré from the \(1/r^2\) swirl dissipation. Do not change variables to \(\Phi\) to escape it.

### Step D — Choose \(\delta\) from the dominant shell (concentration regime)

Let \(j_*(t)=\mathrm{argmax}_j X_j(t)\) and set

\[
\delta(t)\sim 2^{-j_*(t)}.
\]

That is the viscous scale of the concentrated enstrophy.

If **concentration** holds (\(J\ge c_* X\)):

1. Most of \(X\) lives in shell \(j_*\).
2. Approximate that piece by a band-limited field (your Ring Lemma hypothesis).
3. On \(E_c=\{|\omega|\ge c\|\omega\|_2\}\) you get \(\|\nabla\xi_0\|_\infty\le C 2^{j_*}\).
4. Feed that into a Constantin–Fefferman-type bound on \(\sum\lambda_i\cos^2\alpha_i\) **inside the tube and on \(E_c\)**.
5. Off \(E_c\), vorticity is small in \(L^2\) by definition; stretching is lower order.

The Ring Lemma as written is for exact one-shell support. You need a quantitative “almost one-shell” version: if \(X_{j_*}\ge c_* X\), control the leakage from neighboring shells \(j_*\pm 1\). That is a real lemma to write. Bernstein constants will produce a factor \(c_*^{-1}\).

### Step E — Spread regime: use T2 / viscosity, not geometry

If **spread** holds (\(\max_j X_j/X\le\rho_0<1\)):

1. Keep T2 Lemma 1 only: \(\int(u_{\le j}\cdot\nabla)\Delta_j u\cdot\Delta_j u=0\) by \(\nabla\cdot u=0\). That is unconditional and correct.
2. Use shell-spread Poincaré / extra dissipation: energy in many shells cannot all sit at the highest \(j\), so

\[
\|\nabla\omega\|_2^2\gtrsim \lambda(\rho_0)\,X
\]

with \(\lambda(\rho_0)\) larger than the single-shell worst case.

3. Do **not** use T2 Lemma 2 as written. It assumes an \(H^{2.3}\) absorbing ball. That is already a regularity assumption. For the unaugmented large-data problem it is circular. Rebuild the flux bound from Bony + energy class only, even if the decay in \(j\) is weaker than \(2^{-0.8j}\).

4. Drop every GNC / inverse-GCD line from T2. They do not enter \(\omega\cdot S\omega\).

### Step F — Glue the two regimes

On each time interval the solution is either concentrated or spread (or switching).

- Concentrated: Ring + tube \(1/r^4\) + viscosity at scale \(2^{-j_*}\).
- Spread: T2 Lemma 1 + enhanced dissipation.

You need a bound on occupation time of the “almost critical” annulus \(c_*\le J/X\le\rho_0\) if those thresholds do not meet. Pick numbers so the two regimes cover \((0,1]\). Example: concentrated if \(J/X\ge 1/4\), spread if \(J/X\le 1/4\). One threshold, no gap.

Leray’s \(\int X\,dt<\infty\) limits how long a high-\(j_*\) concentrated spike can last, but it does **not** by itself stop \(\dot X\sim X^3\). A spike \(X\sim(T_*-t)^{-1/2}\) is compatible with integrable \(X\). Viscosity or geometric depletion has to supply the extra decay. Do not close with energy integrability alone.

### Step G — What would finish the unaugmented statement

A closed estimate of the form

\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
\le \varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\cdot\mathcal{R}(t),
\]

where \(\mathcal{R}(t)\) is integrable on \([0,T]\) from:

- tube Hardy + swirl dissipation, and/or
- Ring control of \(\cos\alpha_i\) on \(E_c\), and/or
- spread Poincaré.

Then Gronwall keeps \(X\in L^\infty([0,T])\). Continuation in \(H^1\) does the rest.

No BKM-from-\(L^2\) implication is required. No Biot–Savart slogan that \(\cos\alpha_3\to 0\) for all data.

---

## 5. Concrete lemmas to write next (in this order)

1. **Localized tube Hardy for \(\Gamma\)**, radius \(\delta\), no \(\Phi\).
2. **Almost-band-limited Ring Lemma** (dominant shell + two neighbors).
3. **One-threshold regime split** \(J/X\ge 1/4\) vs \(J/X\le 1/4\).
4. **Energy-class T2 flux** (Lemma 1 kept; Lemma 2 rewritten without \(H^{2.3}\)).
5. **Swirl dissipation identity** in the tube: make the \(1/r^2\) angular viscosity explicit and compare it to \(I_{\mathrm{tube}}\).

Item 5 is the reason to keep \(1/r^4\). If the angular viscosity does not dominate the tube source at the same weight, the cancel-to-\(\Phi\) path was not the mistake — the tube is genuinely critical. If it does dominate, you never needed the cancel.

---

## 6. What not to carry over

- \(Q_1\). That is a different PDE.
- Inverse-GCD, Bridge\(^*\), GNC. Separate arithmetic note.
- June T2 corollaries that leave fluids.
- “Almost one-shell” treated as exact one-shell.
- Closing the cubic enstrophy ODE from \(\int X\,dt<\infty\) alone.

---

## 7. Status of this plan

| Piece | Status |
|---|---|
| Keep \(1/r^4\), split tube / off-axis | Setup, not proved |
| Localized tube Hardy | To write |
| Ring Lemma, exact one shell | Sketch in 22045474; needs almost-band-limited upgrade |
| Concentration \(\Rightarrow\) geometric control | Conditional outline |
| Spread \(\Rightarrow\) extra dissipation | T2 Thm 1 idea; rebuild without \(H^{2.3}\) |
| Unaugmented global \(H^1\) bound | Open |

The live question is no longer “does \(\Phi\) cancel the axis?” It is: **in the tube \(r\sim 2^{-j_*}\), does viscosity plus (almost) band-limited direction control beat \(\Gamma\partial_z\Gamma/r^4\)?**
