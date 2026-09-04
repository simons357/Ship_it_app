# Track B lemmas (DA-scored)

`python3 scripts/da_machine.py trackb`

Classical Navier–Stokes, keep \(1/r^4\). Domain Architect scores each
proposal. **The domain stays open.** A lemma pass is not regularity.

No \(Q_1\). No \(\Phi\) as the estimate variable. No Bridge*. No
A \(\Rightarrow\) B. SFE / HB stay shelved.

The plan these sit in is [`docs/UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md).

---

## How DA treats slot B

| Level | What a pass means |
|---|---|
| One lemma | An identity or cover held, or a bad close was correctly failed |
| Domain B | **Never pass.** Regularity stays open until a closed estimate for \(X=\|\omega\|_2^2\) exists |

`check B` runs the lemma tests. If they break, the domain is **fail**.
If they hold, the domain is **open** (identities held; continuation is
not done).

---

## The scored list

| id | Statement | Verdict | What it is |
|---|---|---|---|
| B1 | \(\int(u_{\le j}\cdot\nabla)u_j\cdot u_j=0\) | **pass** | T2 Lemma 1. Periodic, div-free. Parts. |
| B1b | T2 Lemma 2 (\(H^{2.3}\) ball) as input | **fail** | Circular for large-data a priori. Dropped. |
| B2 | 3-CONC \(\sigma\ge 1/2\) and SPREAD \(\sigma\le 1/2\) cover | **pass** | A cover of mass fractions, not dynamics. \(\rho\le\sigma\). |
| B3 | 3-shell \(\Rightarrow\) Bernstein and \(\|\nabla\xi\|_\infty\le C\,2^{j_*}\) on \(E_c\) | **pass** | Ring upgrade. One extra octave is a constant. |
| B3b | Ring \(\Rightarrow\cos\alpha_3\to 0\) for all data | **fail** | Forbidden Biot–Savart slogan. |
| B4 | Localized Hardy, \(g(0)=0\), plus wall term | **pass** | \(\int h^2/r\,dr\le 4\int(h')^2 r\,dr+2h(\delta)^2\). |
| B4b | Hardy absorbs \(I_{\mathrm{tube}}\) for all data | **fail** | Slow fat swirl, \(R\sim 1/\varepsilon\). |
| B4c | Packet class at \(\delta\sim 2^{-j_*}\) budgets \(I_{\mathrm{tube}}\) | **pass** | Same weight, both sides. \(R\) falls with \(j_*\). |
| B4d | Hardy wall is an off-axis charge | **pass** | Spend \(2h(\delta)^2\) on \(I_{\mathrm{off}}\). |
| B5 | Axisymmetric \((\Delta u)_\theta=\Delta u_\theta-u_\theta/r^2\) | **pass** | Identity. Angular piece lives in the tube. |
| B5b | Angular viscosity dominates \(I_{\mathrm{tube}}\) at \(\delta\sim 2^{-j_*}\) | **open** | Why we kept \(1/r^4\). Not shown. |
| B6 | \(\int X\,dt<\infty\Rightarrow X\in L^\infty\) | **fail** | \(X=(T_*-t)^{-1/2}\) is integrable and unbounded. |
| B7 | \(\Pi_j=T+T^*+R+\mathrm{self}\) | **pass** | Bony bookkeeping. |
| B7a | self-flux is T2 Lemma 1 | **pass** | The leftover \(T\) is not self-advection. |
| B7b | \(\|u_{\le j-N}\|_\infty\lesssim 2^{(j-N)/2}X^{1/2}\) | **pass** | Energy class. No \(\rho\) upgrade. |
| B7c | spread \(\Rightarrow\) uniform \(\rho^{1/2}\) as \(\rho\to 0\) | **fail** | Low sum in \(L^\infty\) grows. G is dead. |
| B8 | \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\) | **pass** | Two-regime clock. |
| B8a | high \(j_*\) hot occupation falls | **pass** | Packet ODE at B4c’s scale. |
| B8b | Leray \(\Rightarrow\) short CONC | **fail** | B6 spike, wearing a regime hat. |
| B8c | occupation closes a bound for \(X\) | **open** | Clock is not the estimate. |
| B9 | \(\Delta X=\Delta_{\mathrm{C}}+\Delta_{\mathrm{S}}\) | **pass** | Two-regime bookkeeping. |
| B9a | high \(j_*\) CONC model sits | **pass** | Packet viscosity owns the cubic. |
| B9b | low \(j_*\) CONC stays bounded | **fail** | \(j_*=2\), \(X_0=2.5\): \(X\) crosses 40. |
| B9c | switching high \(j_*\) sits | **pass** | Clock can flip. |
| B9d | glue sketch is an NS a priori | **open** | A model, not the equation. |
| B10 | packet \(X\le K^2 E\) | **pass** | Frozen support has an energy ceiling. |
| B10a | B9b unbounded path is NS-legal | **fail** | The model forgot \(E\). |
| B10b | ceiling bounds a climbing \(j_*\) | **fail** | \(K\) rises with \(j_*\). |
| B10c | climbing CONC closes \(X\) | **open** | Broken out as B11. |
| B10d | energy ceiling retunes the PDE | **fail** | No \(Q_1\), no \(\varepsilon\). Knob on the estimate. |
| B11 | climb increments add | **pass** | Prescribed \(c=\mathrm{d}j_*/\mathrm{d}t\). |
| B11a | bounded \(j_*\) ⇒ bounded \(X\) | **pass** | Necessary condition. |
| B11b | any climb saves the model | **fail** | \(c=1\): \(X\) crosses 40. |
| B11c | fast climb sits | **pass** | \(c=8\): reaches the viscous room. |
| B11d | NS forces a saving \(c\) | **open** | \(t=0\) failed (B12). Evolved law still open. |
| B11e | climb sketch is an NS a priori | **open** | A rate you typed is not the equation. |
| B12 | \(j_{\mathrm{bar}}\) readable on a packet | **pass** | Peak scale from the field. |
| B12a | \(c\) from the vorticity RHS | **pass** | The apparatus reads. |
| B12b | \(t=0\) packets produce \(c\ge 8\) | **fail** | None do. |
| B12c | viscosity forces an upward climb | **fail** | \(j_{\mathrm{bar}}\) falls. |
| B12d | a short evolution produces a saving climb | **open** | Broken out as B13. |
| B12e | \(t=0\) drift is an NS a priori | **open** | A reading is not a law. |
| B13 | short IF-RK2 run stays finite | **pass** | Viscous \(X\) falls. |
| B13a | short run produces \(c\ge 8\) | **fail** | Viscous \(c<0\). Euler \(\sim 0\). |
| B13b | resolved high shells fill | **fail** | Mass above \(j_*+1\) stays \(\sim 0\). |
| B13c | short run stays CONC | **pass** | Clock did not sneak into SPREAD. |
| B13d | evolution is a ladder | **fail** | \(j_{\mathrm{bar}}\) falls. |
| B13e | finer / longer saving climb | **open** | \(n=32\) is a short reading. |
| B13f | short DNS is an a priori | **open** | A few steps are not continuation. |
| B14 | \(\xi\cdot S\xi=\sum\lambda_i\cos^2\alpha_i\) on \(E_c\) | **pass** | Strain eigenframe. Not depletion. |
| B14a | 3-CONC \(\Rightarrow\) median \(\lvert\cos\alpha_3\rvert\le 0.25\) | **fail** | Median sits near \(1/2\). |
| B14b | Ring Lipschitz \(\Rightarrow\cos\alpha_3\to 0\) | **fail** | Same slogan as B3b. |
| B14c | small \(\lvert\cos\alpha_3\rvert\) stretches less on \(E_c\) | **pass** | CF as a conditional. Not all-data. |
| B14d | packet geometry closes \(X\) | **open** | Lipschitz + conditional \(\neq\) continuation. |
| B14e | reading alignment retunes the PDE | **fail** | Knob on the estimate. |
| B15 | \((\omega\cdot S\omega)_+\) on \(E_c\) is a stretching budget | **pass** | Who pays the cubic. |
| B15a | stretch-weighted \(\lvert\cos\alpha_3\rvert\) exceeds the unweighted mean | **pass** | CF as a budget. Field not depleted. |
| B15b | majority of \(+\)stretch from \(\lvert\cos\alpha_3\rvert>0.8\) | **pass** | Directional minority, production majority. |
| B15c | short run depletes median \(\lvert\cos\alpha_3\rvert\le 0.25\) | **fail** | Median stays \(\sim 1/2\). |
| B15d | short run drops aligned share below \(1/2\) | **fail** | \(\mathrm{frac}_{hi}\) stays \(\sim 0.65\). |
| B15e | aligned budget closes \(X\) | **open** | A share is not continuation. |
| B15f | weighting stretching retunes the PDE | **fail** | Knob on the estimate. |
| Φ | Switch the estimate to \(\Phi=\Gamma/r^2\) | **fail** | Moves the work onto \(\|\Phi\|_\infty\). Keep \(\Gamma\). |
| regularity | Classical 3D NS is globally regular | **open** | No closed estimate for \(X\). |

---

## What was actually proved or checked

**B1.** For periodic divergence-free \(u\), the low self-flux into a
dyadic block vanishes:

\[
\int_{\mathbb{T}^3}(u_{\le j}\cdot\nabla)u_j\cdot u_j
=\frac12\int u_{\le j}\cdot\nabla(|u_j|^2)
=-\frac12\int(\nabla\cdot u_{\le j})\,|u_j|^2
=0.
\]

The script repeats this on a random Leray field. Residual is at
roundoff. This is T2 Lemma 1 only.

**B2.** \(\sigma=P_{j_*}/X\) is a number in \((0,1]\). The split
\(\sigma\ge 1/2\) vs \(\sigma\le 1/2\) covers the interval. August
CONC and June SPREAD stay two names. The checker does not claim the
solution lives in either regime.

**B3.** On a field whose Fourier support sits in three consecutive
octaves around \(2^{j_*}\), Bernstein gives

\[
\|\nabla\omega\|_\infty\lesssim 2^{2(j_*+1)}\|\omega\|_2,
\]

and on \(E_c=\{|\omega|\ge c\|\omega\|_{\mathrm{rms}}\}\)

\[
\|\nabla\xi\|_\infty\le C(c)\,2^{j_*}.
\]

The script measures the constants on \(\mathbb{T}^3\). That is Ring,
not depletion of \(\sum\lambda_i\cos^2\alpha_i\).

**B4.** Classical Hardy: \(g(0)=0\) implies
\(\int_0^\delta(g/r)^2\,dr\le 4\int(g')^2\,dr\).

Tube form with wall: \(h(0)=0\) and completion of the square

\[
0\le\int_0^\delta\bigl|r h'+\tfrac12 h\bigr|^2\frac{dr}{r}
\]

gives

\[
\int_0^\delta\frac{h^2}{r}\,dr
\le 4\int_0^\delta(h')^2 r\,dr+2h(\delta)^2.
\]

If \(h=\Gamma/r\), the wall term is the off-axis match. This is the
localized Hardy the plan asked for.

**B4b / B4c / B4d.** The Hardy \(\to I_{\mathrm{tube}}\) write
lives in [`TRACK-B-HARDY-TUBE.md`](TRACK-B-HARDY-TUBE.md).
All-data absorption **fails** (slow fat swirl, \(R\sim 1/\varepsilon\)).
Packet class at \(\delta\sim 2^{-j_*}\) **passes**. The wall is a
finite off-axis charge.

**B5.** In cylindrical components, axisymmetric,

\[
(\Delta u)_\theta=\Delta u_\theta-\frac{u_\theta}{r^2}.
\]

The extra \(1/r^2\) sits in the same tube as \(1/r^4\partial_z(\Gamma^2)\).
The script records the identity and the raw ratio
\(\lvert I_{\mathrm{source}}\rvert/\)angular mass on one manufactured
field. It does not claim the viscosity wins.

**B6.** Leray’s \(\int X\,dt<\infty\) does not stop
\(\dot X\sim X^3\). A spike \(X\sim(T_*-t)^{-1/2}\) is compatible
with integrable enstrophy and is unbounded. DA fails that close.

**B7 / B7a / B7b / B7c.** The low Bony \(T\) write lives in
[`TRACK-B-BONY-T.md`](TRACK-B-BONY-T.md). Split and T2 self
**pass**. Energy-class \(L^\infty\) **pass**. Uniform
\(\rho^{1/2}\) as \(\rho\to 0\) **fails**. Theorem G is dead.
H at frozen \(\rho\le 1/4\) may still use B7b.

**B8 / B8a / B8b / B8c.** Occupation time lives in
[`TRACK-B-OCCUPATION.md`](TRACK-B-OCCUPATION.md). Clock
**pass**. High \(j_*\) short **pass**. Leray \(\Rightarrow\)
short CONC **fail**. Occupation itself does not close \(X\).

**B9 / B9a / B9b / B9c / B9d.** The two-regime glue lives in
[`TRACK-B-GLUE.md`](TRACK-B-GLUE.md). Increments add
**pass**. High \(j_*\) CONC sits **pass**. Switching high
\(j_*\) sits **pass**. Low \(j_*\) CONC **fails** on the model
ODE. Sketch \(\neq\) NS a priori **open**.

**B10 / B10a / B10b / B10c / B10d.** Energy ceiling lives in
[`TRACK-B-LOW-J.md`](TRACK-B-LOW-J.md). Packet \(X\le K^2E\)
**pass**. B9b unbounded path is not NS **fail**. Ceiling
does not follow a climbing \(j_*\) **fail**. Climbing CONC
is broken out as B11. Not a PDE retune **fail**.

**B11 / B11a / B11b / B11c / B11d / B11e.** Climbing CONC
lives in [`TRACK-B-CLIMB.md`](TRACK-B-CLIMB.md). Increments
add **pass**. Bounded \(j_*\) bounds \(X\) **pass**. Slow
climb **fails** to save. Fast climb sits **pass**. NS climb
law **open**. Sketch \(\neq\) NS a priori **open**.

**B12 / B12a / B12b / B12c / B12d / B12e.** The field climb
lives in [`TRACK-B-CLIMB-LAW.md`](TRACK-B-CLIMB-LAW.md).
Barycenter **pass**. \(c\) from the RHS **pass**. \(t=0\)
saving climb **fail**. Viscosity as a ladder **fail**.
Short evolution is broken out as B13. \(t=0\) as a priori
**open**.

**B13 / B13a / B13b / B13c / B13d / B13e / B13f.** Short
evolution lives in [`TRACK-B-EVOLVE.md`](TRACK-B-EVOLVE.md).
Run finite **pass**. Saving climb **fail**. High fill
**fail**. Stays CONC **pass**. Evolution as a ladder
**fail**. Finer/longer **open**. Not an a priori **open**.

**B14 / B14a / B14b / B14c / B14d / B14e.** Packet geometry
lives in [`TRACK-B-GEOMETRY.md`](TRACK-B-GEOMETRY.md).
Strain identity **pass**. CONC \(\Rightarrow\) depleted
\(\cos\alpha_3\) **fail**. Ring \(\Rightarrow\) alignment
**fail**. CF conditional **pass**. Geometry closes \(X\)
**open**. Not a PDE retune **fail**.

**B15 / B15a / B15b / B15c / B15d / B15e / B15f.** Stretching
budget lives in [`TRACK-B-STRETCH.md`](TRACK-B-STRETCH.md).
Budget readable **pass**. CF weights the budget **pass**.
Majority from aligned cap **pass**. Short run depletes
median \(\lvert\cos\alpha_3\rvert\) **fail**. Short run
empties the aligned share **fail**. Budget closes \(X\)
**open**. Not a PDE retune **fail**.

---

## What is still the next write

1. B5b: angular viscosity versus \(I_{\mathrm{tube}}\) at
   \(\delta\sim 2^{-j_*}\). Cartesian budget is aligned;
   the field is not depleted. A finer packet box (B13e)
   stays open.
2. Do not revive all-data Hardy absorption, G’s \(\rho\to 0\),
   Leray-as-occupation, the glue sketch as an NS a priori,
   a typed \(c=8\), all-data Biot–Savart depletion, or a
   retune of the PDE.

None of those is a pass on regularity. Checker:

```
python3 scripts/track_b_hardy_tube.py
python3 scripts/track_b_bony_t.py
python3 scripts/track_b_occupation.py
python3 scripts/track_b_glue.py
python3 scripts/track_b_low_j.py
python3 scripts/track_b_climb.py
python3 scripts/track_b_climb_law.py
python3 scripts/track_b_evolve.py
python3 scripts/track_b_geometry.py
python3 scripts/track_b_stretch.py
python3 scripts/track_b_lemmas.py
python3 -m unittest tests.test_track_b_lemmas tests.test_track_b_glue tests.test_track_b_low_j tests.test_track_b_climb tests.test_track_b_climb_law tests.test_track_b_evolve tests.test_track_b_geometry tests.test_track_b_stretch
python3 scripts/da_machine.py trackb
python3 scripts/da_machine.py check --domain B
```
