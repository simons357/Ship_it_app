# Unaugmented vorticity plan, keeping \(1/r^4\)

Working note. Fluids only. No augmentation. Do not cancel the axis weight.

SFE, Harmonic Blueprint, and Millennium-packaged notes are shelved (`docs/SHELF.md`). They are not inputs here.

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

Occupation time is broken out in [`TRACK-B-OCCUPATION.md`](TRACK-B-OCCUPATION.md). One threshold \(\sigma=1/2\), no gap. The clock **passes**. High \(j_*\) hot time **passes** on the packet ODE. Leray \(\Rightarrow\) short CONC **fails**.

The two-regime glue is broken out in [`TRACK-B-GLUE.md`](TRACK-B-GLUE.md). Increments add. High \(j_*\) CONC sits. Switching high \(j_*\) sits. Low \(j_*\) CONC **fails** on the model ODE. The sketch is **not** an a priori bound for classical \(X\).

Frozen low-\(j_*\) is hygiene, not a retune of the PDE. Packet support \(|k|\le K\) gives \(X\le K^2 E\). That write lives in [`TRACK-B-LOW-J.md`](TRACK-B-LOW-J.md). The B9b unbounded path is **not** NS-legal. The ceiling does **not** follow a climbing \(j_*\).

Climbing CONC is broken out in [`TRACK-B-CLIMB.md`](TRACK-B-CLIMB.md). The knob is \(c=\mathrm{d}j_*/\mathrm{d}t\) on the estimate. Slow climb still blows. Fast climb sits.

The field climb is broken out in [`TRACK-B-CLIMB-LAW.md`](TRACK-B-CLIMB-LAW.md). Instantaneous \(t=0\) on random CONC packets does **not** produce the saving \(c=8\). Viscosity pulls \(j_{\mathrm{bar}}\) down. A short evolution is written in [`TRACK-B-EVOLVE.md`](TRACK-B-EVOLVE.md): still no saving climb on \(n=32\).

Packet geometry is written in [`TRACK-B-GEOMETRY.md`](TRACK-B-GEOMETRY.md). The strain identity on \(E_c\) **passes**. 3-CONC does **not** force depleted \(\cos\alpha_3\). Ring Lipschitz is **not** alignment. Constantin–Fefferman holds as a **conditional** (small \(\lvert\cos\alpha_3\rvert\) stretches less). That does not close \(X\).

The stretching budget is written in [`TRACK-B-STRETCH.md`](TRACK-B-STRETCH.md). Stretch-weighted \(\lvert\cos\alpha_3\rvert\) sits near \(0.81\) against an unweighted mean near \(0.50\). A majority of \((\omega\cdot S\omega)_+\) on \(E_c\) comes from the aligned cap. A short run does **not** deplete the median and does **not** empty that share. The share is **not** an a priori ([`TRACK-B-PAYERS.md`](TRACK-B-PAYERS.md)).

Fluids look at the net in [`TRACK-B-BALANCE.md`](TRACK-B-BALANCE.md). The identity \(\dot X=2\int\omega\cdot S\omega-2\nu\|\nabla\omega\|_2^2\) **passes**. On the same random-phase packets, plus and minus stretch **cancel** and viscosity owns the net. That is **not** BKM, and **not** every 3-CONC field.

Leray’s \(\int X\,dt<\infty\) limits how long a high-\(j_*\) concentrated spike can last, but it does **not** by itself stop \(\dot X\sim X^3\). A spike \(X\sim(T_*-t)^{-1/2}\) is compatible with integrable \(X\). Viscosity or geometric depletion has to supply the extra decay. Do not close with energy integrability alone. All-data geometric depletion is **not** what the packets gave. An aligned *budget* is also not a depleted *field*. A cancelled *net* is also not every CONC packet.

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

## 5. Concrete lemmas (DA-scored; regularity still open)

Scored in [`docs/TRACK-B-LEMMAS.md`](TRACK-B-LEMMAS.md). `python3 scripts/da_machine.py trackb`.

1. **Localized tube Hardy for \(\Gamma\)**, radius \(\delta\), no \(\Phi\). Hardy + wall term **pass**. All-data \(I_{\mathrm{tube}}\) domination **fail**. Packet class at \(\delta\sim 2^{-j_*}\) **pass**. Write: [`TRACK-B-HARDY-TUBE.md`](TRACK-B-HARDY-TUBE.md).
2. **Almost-band-limited Ring Lemma** (three shells). Bernstein **pass**. All-data depletion **fail**. Strain identity on \(E_c\) **pass**. CONC \(\Rightarrow\) depleted \(\cos\alpha_3\) **fail**. CF as a conditional **pass**. Stretching budget: CF weights it **pass**; majority from aligned cap **pass**; short run does not empty it **fail** of depletion. Enstrophy balance: identity **pass**; visc owns this ensemble **pass**; \(P_+\) as a net cubic **fail**. Coherent CONC: signed-strain blob nets **pass**; working-box cubic live **fail**; \(z\)-independent tube also nets **fail**. Writes: [`TRACK-B-GEOMETRY.md`](TRACK-B-GEOMETRY.md), [`TRACK-B-STRETCH.md`](TRACK-B-STRETCH.md), [`TRACK-B-BALANCE.md`](TRACK-B-BALANCE.md), [`TRACK-B-COHERENT.md`](TRACK-B-COHERENT.md).
3. **One-threshold regime split** 3-CONC \(\sigma\ge 1/2\) vs SPREAD \(\sigma\le 1/2\). Cover **pass**.
4. **Energy-class T2 flux.** Lemma 1 **pass**. Lemma 2 dropped (**fail** as input). Low Bony \(T\): split **pass**, energy-class **pass**, uniform \(\rho^{1/2}\) **fail**. Write: [`TRACK-B-BONY-T.md`](TRACK-B-BONY-T.md).
5. **Swirl dissipation identity** in the tube. \((\Delta u)_\theta\) **pass**. Angular \(1/r^2\) vs \(I_{\mathrm{tube}}\) **fail** (\(R_{\mathrm{ang}}\) climbs with \(j_*\)). Full \(D_{\mathrm{tube}}\) still budgets the packet (B4c). Do not cancel to \(\Phi\). Write: [`TRACK-B-ANGULAR.md`](TRACK-B-ANGULAR.md).

Item 5 was the reason to keep \(1/r^4\). The extra angular piece, alone, does **not** dominate the tube source at packet scale. The cancel-to-\(\Phi\) path was not the missing absorption — full \(\nabla\omega\) dissipation (B4c) is. Domain B does not pass.

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
| Localized tube Hardy | **pass** as Hardy + wall; all-data domination **fail**; packet class **pass** (`docs/TRACK-B-HARDY-TUBE.md`) |
| Angular \(1/r^2\) vs \(I_{\mathrm{tube}}\) | **fail** of domination on packets; \(R_{\mathrm{ang}}\) climbs; B4c still budgets (`docs/TRACK-B-ANGULAR.md`) |
| Ring Lemma, exact one shell | Upgraded to 3-shell Bernstein check; depletion **fail** as a slogan |
| Concentration \(\Rightarrow\) geometric control | Identity **pass**; CONC not depleted; CF conditional **pass**; stretching budget aligned, net cubic cancels; coherent blob nets, working-box cubic not live; field occupation stays CONC (`docs/TRACK-B-GEOMETRY.md`, `docs/TRACK-B-STRETCH.md`, `docs/TRACK-B-BALANCE.md`, `docs/TRACK-B-COHERENT.md`, `docs/TRACK-B-FIELD-OCC.md`) |
| Spread \(\Rightarrow\) extra dissipation | T2 Lemma 1 **pass**; Lemma 2 dropped; energy-class \(T\) **pass**; uniform \(\rho^{1/2}\) **fail** |
| Unaugmented global \(H^1\) bound | Open |

The live question is no longer “does \(\Phi\) cancel the axis?” and no longer “does the extra \(1/r^2\) piece, alone, beat \(I_{\mathrm{tube}}\)?” B4c still budgets packets. Coherent CONC is scored. Field occupation is scored. Field glue is scored: typed \(j_*=2\) grows; the NS packet falls. NS climb law is scored: the field did not force \(c=8\). Climb sketch is scored: prescribed \(c=8\) is not this window. Longer \(n=32\) past the room time did not produce \(c=8\). DNS is not an a priori (B13f). Finer stays B22e. Do not spawn \(n=64\).

---

## 8. Theorem H and the SND dictionary

Source for H: May T³ note (20405526, archive). Fluids content only. The old closure packaging is ignored.

### 8.1 What Theorem H actually says

Shell flux into the dominant block:

\[
\Pi_{j_*}=\int_{\mathbb{T}^3}\Delta_{j_*}\bigl[(u\cdot\nabla)u\bigr]\cdot\Delta_{j_*}u\,dx.
\]

**(SND-C).** There is \(C_*<\infty\) such that whenever \(X\ge\delta_*/4\) and \(\rho=J/X\le\rho_0\) (spread),

\[
|\Pi_{j_*}|\le C_*\bigl(\nu\,2^{2j_*}X_{j_*}+X^{1/2}\mathcal{D}^{1/2}\bigr),
\qquad
\mathcal{D}=\nu\|\Delta u\|_2^2.
\]

**Theorem H (as written).** SND-C holds in that spread class, by a Bony split \(\Pi_{j_*}=T+T^*+R\):

- diagonal \(R\): Bernstein + Theorem F + Young
- high \(T^*\): Kato–Ponce + \(X_k\le\rho X\)
- low \(T\): CCFS locality + “spread makes low shells small”

**Theorem G (as written).** SND-C \(\Rightarrow\) concentration \(\inf J/X\ge c_*\), because if \(\rho(t_k)\to 0\) then F makes \(\mathcal{D}\) explode and SND-C forces \(\dot\rho>0\).

H is a **Cartesian, periodic, velocity-paraproduct** statement. It never sees \(r\), \(\Gamma\), or \(\Phi\).

### 8.2 Where the \(\Phi\) cancel actually hits H

The cancel does not change the Bony algebra on \(\mathbb{T}^3\). It breaks the **glue**.

In the May note the chain was:

\[
Q_1\ \xrightarrow{\ A\ }\ \text{smooth }u^\varepsilon
\ \xrightarrow{\ B,\ C\ }\ \Phi\text{-cancel, no Gronwall}
\ \xrightarrow{\ I\ }\ \text{uniform }H^1\text{ as }\varepsilon\to 0
\ \xrightarrow{\ H,\ G\ }\ \text{SND-C on the limit }u.
\]

Three collisions:

1. **Wrong manifold.** \(\Phi=\Gamma/r^2\) lives in cylindrical swirl. H lives in Fourier shells on \(\mathbb{T}^3\). After the cancel, the nonlinearity you are estimating is \(\partial_z(\Phi^2)\), not \(\Delta_{j_*}[(u\cdot\nabla)u]\). H’s \(T+T^*+R\) does not apply to that term unless you rebuild LP in cylindrical modes.

2. **Hidden \(\|\Phi\|_\infty\).** Theorem C uses the cancel to kill Gronwall. The cancel is free only if \(\|\Phi\|_\infty\) is already controlled. That bound is what you do not have. So C does not deliver a uniform \(H^1\) family, and I cannot pass H to an unaugmented limit.

3. **H never needed B.** The commutator estimate is supposed to be a spread-regime bound on \(\Pi_{j_*}\) for Leray–Hopf \(u\) on \(\mathbb{T}^3\). Putting Phi in front of it makes H look dependent on a swirl identity it does not use. That is why H feels broken after you drop the cancel: the **package** broke, not the paraproduct.

**Reconcile:** delete B, C, and I from the H track. State H only for the classical velocity on \(\mathbb{T}^3\), spread class, no \(\varepsilon\), no \(\Phi\). Keep the \(1/r^4\) tube work on a **separate swirl track**.

### 8.3 What is still open inside H itself

Even after the glue is cut, H is not finished.

- **Theorem F is too strong.** \(\mathcal{D}\ge\nu\cdot 4^{N-1}\cdot\rho\cdot X\) with \(N=\lceil X/J\rceil\) treats “\(N\) active shells” as if they sat at exponentially higher frequency. They can be \(N\) consecutive low shells. Super-exponential dissipation as \(\rho\to 0\) is not a theorem. The diagonal step that writes \(2^{j_*}\le(\mathcal{D}/(\nu X_{j_*}))^{1/2}\) from F inherits this.
- **Low Bony term \(T\).** “Each low shell is \(\le\rho X\)” is true under spread. The **sum** of many low shells need not be small in \(L^\infty\). CCFS locality does not turn that sum into \(O(\rho^{1/2}X^{1/2})\) uniformly as \(\rho\to 0\), which is exactly the limit G uses.
- **G needs uniformity down to \(\rho\to 0\).** H assumes \(\rho\le\rho_0\). If \(C_*\) blows up as \(\rho_0\to 0\), G’s contradiction fails.

So: cut Phi from H, then the remaining job is a **uniform energy-class bound on the low paraproduct** in the spread class. That is the real Theorem H.

### 8.4 Every SND re-iteration, named so they can be used

Do not use one symbol. Five different statements were all called SND.

| Name to use now | Old label | Formula | Job |
|---|---|---|---|
| **CONC** | August SND, May Def, Thm D/G | \(\inf J/X\ge c_*\) | Dominant shell. Ring Lemma. Geometry. |
| **SPREAD** | June T2 “SND”, May H hypothesis | \(\rho=J/X\le\rho_0<1\) | Extra dissipation. T2 Lemma 1. H’s class. |
| **SIMPLEX** | May Paper 2 | \(\|a-\mu\|_{\ell^1}\le 0.039\) | Not used. Relied on GCD arithmetic. |
| **SND-C** | May Def before H | the \(\Pi_{j_*}\) bound above | Commutator in SPREAD only. |
| **T2-ODE** | June Thm 2–3 | \(\frac{d}{dt}\|a-\mu\|_1\le-\alpha\|a-\mu\|_1+\beta\) | Quantitative SPREAD, if rebuilt without \(H^{2.3}\). |

August CONC and June SPREAD are opposites. That is useful, not a contradiction, once they have two names.

**Two-regime machine (how to mobilize them):**

\[
\begin{align*}
\rho&\ge\tfrac14 &&\text{CONC}\ \to\ \text{almost-band-limited Ring}\ \to\ \text{direction on }E_c\\
\rho&\le\tfrac14 &&\text{SPREAD}\ \to\ \text{T2 Lemma 1 + attempted SND-C (H without Phi)}.
\end{align*}
\]

One threshold. No gap. G, if it can be made uniform, is the statement “you cannot stay in deep SPREAD,” i.e. CONC eventually returns. That is optional. The unaugmented bound only needs **each** regime controlled while you are in it.

Drop SIMPLEX. Drop any identification of CONC/SPREAD with inverse-GCD.

### 8.5 How H and the \(1/r^4\) track sit side by side

```
                classical u, no Q1
                     /          \
                    /            \
            T³ Cartesian                    swirl, keep 1/r^4
         CONC | SPREAD                      tube | off-axis
              |                                  |
     Ring (3-shell / EQ3)               localized Hardy +
     SND-C / H (spread only)            angular viscosity
              \                                  /
               \                                /
                 glue by occupation time of each regime
```

No arrow from \(\Phi\) into \(\Pi_{j_*}\). No arrow from inverse-GCD into either column.

---

## 9. Three-shell equidistribution

This is the older Ring / Borromean object: not one shell, and not all shells. Three consecutive dyadic blocks around the peak.

### 9.1 Definitions

Let \(j_*=\mathrm{argmax}_j X_j\) and write the **triad packet**

\[
P_{j_*}:=X_{j_*-1}+X_{j_*}+X_{j_*+1},\qquad
\sigma:=\frac{P_{j_*}}{X}\in(0,1].
\]

**Packet mass.** \(\sigma\) is the enstrophy fraction in the three adjacent shells.

**Equidistribution on the packet.** There is \(\kappa\ge 1\) such that

\[
\max_{|k-j_*|\le 1}X_k
\le\kappa\min_{|k-j_*|\le 1}X_k.
\]

The clean case is \(\kappa=1\): \(X_{j_*-1}=X_{j_*}=X_{j_*+1}=P_{j_*}/3\), hence

\[
\rho=\frac{J}{X}=\frac{\sigma}{3}.
\]

A fully occupied, equidistributed triad (\(\sigma=1\)) has \(\rho=1/3\).

Do not confuse this with strain-axis equidistribution \(\cos^2\alpha_i=1/3\), which would send \(\sum\lambda_i\cos^2\alpha_i=0\). That is a different “three.” Here “shell” means \(\Delta_j\).

### 9.2 Why three, not one

Local NS / Bony interactions that feed \(\Pi_{j_*}\) live on frequencies \(|k|\sim 2^{j_*}\). A product of two dyadic pieces is supported in a bounded number of neighboring shells. The diagonal remainder \(R\) in Theorem H is exactly \(|k-j_*|\le 2\) or \(\le 4\). The smallest packet that can host a local triad is three consecutive shells.

The August Ring Lemma used **one** shell. That makes Bernstein clean and makes CONC look like \(\rho\ge c_*\approx 1\). It is also narrower than the interaction. Three-shell support is the natural Ring hypothesis.

**Almost-band-limited Ring (3-shell).** If \(\mathrm{supp}\,\hat u\subset S_{j_*-1}\cup S_{j_*}\cup S_{j_*+1}\), Bernstein still gives

\[
\|\nabla\omega\|_\infty\lesssim 2^{2(j_*+1)}\|\omega\|_2\lesssim 4\cdot 2^{2j_*}\|\omega\|_2,
\]

so on \(E_c=\{|\omega|\ge c\|\omega\|_2\}\)

\[
\|\nabla\xi_0\|_{L^\infty(E_c)}\le C(c)\,2^{j_*}.
\]

One extra octave costs a fixed factor, not a derivative. So 3-shell Ring is the same lemma, not a weaker theory.

If only a fraction \(\sigma\) of the enstrophy sits in the packet, apply Ring to the band-limited piece \(u_{\mathrm{pkt}}=\sum_{|k-j_*|\le 1}\Delta_k u\) and treat \(u-u_{\mathrm{pkt}}\) as a remainder of size \((1-\sigma)^{1/2}X^{1/2}\). That is the quantitative “almost 3-shell” statement.

### 9.3 Where it sits in CONC / SPREAD

The one-threshold split \(\rho\gtrless 1/4\) was a placeholder. The 3-shell packet is the right concentrated object.

| Regime | Test | Tools |
|---|---|---|
| **3-shell CONC** | \(\sigma\ge 1/2\) | 3-shell Ring on the packet; remainder \(\le X/2\) |
| **equidistributed 3-shell** | \(\sigma\ge 1/2\) and \(\kappa\le 2\) | same Ring; \(\rho=\sigma/3\in[1/6,1/3]\) |
| **1-shell spike** | \(X_{j_*}\ge\sigma/2\) inside a heavy packet | August Ring, special case |
| **SPREAD** | \(\sigma\le 1/2\) (mass outside every triad) | T2 Lemma 1; attempted SND-C / H |

An equidistributed full triad has \(\rho=1/3>1/4\), so it was already on the CONC side of the old split. Good: the phenomenology you care about (local cascade in a triad) is concentrated, not spread.

SPREAD now means: **no three consecutive shells hold half the enstrophy.** That is stronger than “no single shell holds almost everything,” and it matches H’s need that the diagonal neighborhood is not the whole field.

### 9.4 What equidistribution does for H

Helps **only the diagonal** \(R\).

If the three shells around \(j_*\) are comparable, Bernstein constants on \(\Delta_{j_*-1},\Delta_{j_*},\Delta_{j_*+1}\) are of the same order. You do not have one neighbor hiding a much larger \(L^\infty\) piece. That is the right setup for the \(R\) estimate, without Theorem F’s \(4^{N-1}\).

Does **not** help the low paraproduct \(T\) (\(k\le j_*-4\)). Those shells are outside the triad by definition. Equidistribution inside the packet says nothing about the far infrared. That remains the open piece of H.

T2 Lemma 1 still kills the low self-flux into each \(\Delta_j\). Keep that.

### 9.5 What it does not do

- It does not follow from \(\nabla\cdot u=0\) or from Leray. It is a regime, like CONC.
- It does not cancel \(\omega\cdot S\omega\). Frequency equidistribution is not alignment equidistribution.
- It does not replace viscosity in the \(1/r^4\) tube. The swirl track is unchanged: \(\delta\sim 2^{-j_*}\) is still the packet scale.
- Borromean “linkage forces localization” is a picture, not an estimate, until it is rewritten as the 3-shell Bernstein bound above.

### 9.6 Freeze these as the SND re-iterations that matter

\[
\sigma=\frac{X_{j_*-1}+X_{j_*}+X_{j_*+1}}{X},\qquad
\rho=\frac{\max_j X_j}{X}.
\]

- **3-CONC:** \(\sigma\ge 1/2\). Mobilize Ring on three shells.
- **EQ3:** 3-CONC plus \(\kappa\le 2\). Mobilize the clean diagonal \(R\).
- **SPREAD:** \(\sigma\le 1/2\). Mobilize T2 Lemma 1 and the open low term of H.

One-shell August SND is the special case \(X_{j_*}\approx P_{j_*}\). June “no shell above \(\rho_0\)” is implied by SPREAD if \(\rho_0\ge 1/2\), but SPREAD is the better name because H’s diagonal is a three-shell object.

---

## 10. Which spectral pieces might apply

Filter: can it enter an estimate for \(\Pi_{j_*}\), \(\omega\cdot S\omega\), or the \(1/r^4\) tube, on the classical system, no \(Q_1\).

### Use now

| Tool | Role |
|---|---|
| LP shells \(X_j\), \(X\), \(J\), \(\rho\), \(j_*\) | Language of every estimate |
| Triad packet \(P_{j_*}\), \(\sigma\), EQ3 | 3-CONC / SPREAD split |
| 3-shell Ring (Bernstein on \(E_c\)) | Direction bound in 3-CONC |
| Bony \(T+T^*+R\) | Split of \(\Pi_{j_*}\) |
| T2 Lemma 1 (\(\nabla\cdot u=0\) kills low self-flux) | Unconditional, keep |
| CCFS locality (as a *target* for \(T\)) | Only if restated in energy class |
| Kato–Ponce on high \(T^*\) | Standard; use in SPREAD |
| Strain identity \(\sum\lambda_i\cos^2\alpha_i\) | Geometry after Ring, not a spectral closer |
| Leray \(\int X<\infty\), \(\nu\|\nabla\omega\|_2^2\) | Viscosity budget |
| Tube split of \(1/r^4\) at \(\delta\sim 2^{-j_*}\) | Swirl track; packet scale |

### Regime hypotheses only (do not treat as proved)

| Tool | Why it is only a regime |
|---|---|
| August SND / CONC | \(\inf J/X\ge c_*\) is an assumption |
| 3-CONC \(\sigma\ge 1/2\), EQ3 | Same |
| June SND / SPREAD | Opposite of CONC; useful as the other side |
| SND-C / Theorem H | Wanted bound; low \(T\) open |
| Theorem G | Needs uniform H as \(\rho\to 0\) |
| T2-ODE / \(\alpha=2\nu^2 4^{1/\rho_0}\rho_0\) | Rebuild without \(H^{2.3}\) and without F’s \(4^{N-1}\) |
| “SND on smooth intervals” (Thm E) | True for already-smooth \(u\); does not start the a priori estimate |
| Small-data / bounded-\(H^2\) pigeonhole | Separate small or subcritical classes |

### Do not put on this track

| Tool | Why |
|---|---|
| \(Q_1\) / coherence operator | Different PDE |
| \(\Phi\) cancel as input to H | Wrong manifold; hidden \(\|\Phi\|_\infty\) |
| Theorem C / I (\(\varepsilon\to 0\) uniform \(H^1\)) | Glue that fed H; drop |
| Theorem F as \(4^{N-1}\rho X\) | False as stated |
| SIMPLEX \(\|a-\mu\|_1\le 0.039\) | Used GCD arithmetic |
| Inverse-GCD \(Q_N\), \(\widetilde Q_N\), \(H_N\) | Matrix. Not a bound on \((u\cdot\nabla)u\) |
| Bridge\(^*\) | Single prime-pair Rayleigh; keep in the arithmetic note only |
| Full-spectrum \(\lambda_{\min}>-1/2\) | False |
| Triple Lock / GNC / SND \(\equiv\) Bridge | Identification withdrawn |
| Route C, \(\lambda_{\min}/\log N\), Montgomery–Dyson Q6 | Other equations. Stale “Gap 1 complete” logs are false against the Aug 2026 Q6 audit: spectral-limit, normalization (\(Q_N\) vs \(\widetilde Q_N\) vs \(H_N\)), and operator-to-Mertens are still open. Use the corrected 2026 drafts only; no submission until an independent proof/numeric pass. |
| “\(Q_6\) with \(\gamma>3/2\) enforces SND” | Not a fluid mechanism |
| HB / prime node families (ringdown) | Different spectral test; not a commutator |
| Quantum Lens / prime-manifold Hamiltonian | Off-track |

### How to load the usable spectral stack

```
classical u
    LP {X_j}
        σ = P_{j*}/X
        σ ≥ 1/2  →  3-shell Ring → ∇ξ on E_c → stretching
        σ ≤ 1/2  →  T2 Lemma 1 + Bony
                      R  (EQ3 helps)
                      T* (Kato–Ponce)
                      T  (open)
    swirl: keep 1/r^4, δ ~ 2^{-j*}
```

Nothing else from the spectral stack needs to sit on those arrows.

---

## 11. Triple lock vs Bridge\(^*\)

June drafts asserted \(\mathrm{SND}\equiv\mathrm{GNC}\equiv\mathrm{Bridge}\) (20552400 and clones). That triple is withdrawn. Your memory is right that **Bridge was the vertex that had to come out**. What remains is a smaller theorem with the same name family.

### 11.1 What “Bridge” used to mean (withdrawn)

\[
\lambda_{\min}(Q_N)>-\tfrac12
\quad\text{for all }N\ge 1
\]

(or the same floor on \(\widetilde Q_N\) or \(H_N\)). That was the third leg of the triple: one matrix inequality supposed to be SND and GNC. It is **false**. Already \(\lambda_{\min}(Q_{10})\approx-1.90\) and \(\lambda_{\min}(\widetilde Q_{20})\approx-0.505\). So the triple cannot be repaired by putting that floor back.

GNC (dark-state / prime-indicator difference) is also withdrawn as a detector: \(v_k(j)=1_P(j)-1_P(k-j)\) **vanishes** on an actual Goldbach pair. On raw \(Q_N\), \(\langle e_p-e_q,Q_N(e_p-e_q)\rangle=1/p+1/q-2\) is typically \(<-1/2\). So GNC \(\Leftrightarrow\) Bridge was wrong on both sides.

SND (fluids) was never the same statement as a Rayleigh quotient on \(1/\gcd\). That identification is the part that must stay walked back.

### 11.2 What still works: Bridge\(^*\) (single pair)

August note 22045478, Theorem 3.1. On \(\widetilde Q_N(i,j)=1/(\gcd(i,j)\sqrt{ij})\), for distinct primes \(p,q\) and \(v=e_p-e_q\),

\[
R(v)=\frac{v^\top\widetilde Q_N v}{\|v\|_2^2}
=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}
>-\frac12,
\]

because \(pq\ge 6\) so \(1/\sqrt{pq}\le 1/\sqrt6<1/2\). Two-line identity. Also: \(v\ge 0\Rightarrow v^\top\widetilde Q_N v\ge 0\).

This is a **restricted** floor on one pair of standard-basis vectors, not \(\lambda_{\min}\). \(R\) can be negative (\((2,3)\approx-0.228\)) and still sit above \(-1/2\).

### 11.3 Do not put Bridge\(^*\) back in a triple

| Statement | Status |
|---|---|
| \(\mathrm{SND}\equiv\mathrm{GNC}\equiv\mathrm{Bridge}\) (full floor) | Withdrawn, and the floor is false |
| Bridge\(^*\) on \(e_p-e_q\) | Proved, arithmetic note only |
| Multi-rep Bridge\(^*\) on \(\sum(e_p-e_{k-p})\) | Open (numeric through \(N=200\) is not a proof) |
| Bridge\(^*\Rightarrow\) 3-CONC / H / tube | No. Remark 1.4 and §5.3 of that note: no map onto \(\|(u\cdot\nabla)u\|\) |
| T2-ODE \(\Leftrightarrow\) SPREAD | Fluids-only, separate; not a third vertex |

Keep Bridge\(^*\) as the public claim for the inverse-GCD matrix. Do not reattach it to SND or GNC. The fluids equivalences you can still *try* are T2 Lemma 1 (unconditional) and, later, a rebuilt T2-ODE \(\Leftrightarrow\) SPREAD — both without \(Q_N\).

A later scan (`docs/SPECTRAL-FLOOR-EXPLORATION.md`) keeps that split. Two arithmetic floors stand: \(\lambda_{\min}(H_N)\ge-1\) on the full index, and \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\) on primes. Neither is a fluids input.

### 8.6 Next writes, in order, for the H track

1. Restate SND-C with frozen SPREAD (\(\rho\le 1/4\)), no Phi, no \(\varepsilon\).
2. Prove the diagonal and high Bony pieces from Bernstein + T2 Lemma 1 only. Do not quote F’s \(4^{N-1}\).
3. Isolate the low paraproduct as the single open estimate.
4. Only then ask whether G can push you out of deep SPREAD.

The swirl track stays the tube lemmas in §5. That is how H is reconciled with dropping the cancel: **H never used the cancel, so stop feeding it through Theorem C.**
