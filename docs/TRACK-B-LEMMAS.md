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
| B4b | Hardy absorbs \(I_{\mathrm{tube}}\) for all data | **open** | The live tube question. |
| B5 | Axisymmetric \((\Delta u)_\theta=\Delta u_\theta-u_\theta/r^2\) | **pass** | Identity. Angular piece lives in the tube. |
| B5b | Angular viscosity dominates \(I_{\mathrm{tube}}\) at \(\delta\sim 2^{-j_*}\) | **open** | Why we kept \(1/r^4\). Not shown. |
| B6 | \(\int X\,dt<\infty\Rightarrow X\in L^\infty\) | **fail** | \(X=(T_*-t)^{-1/2}\) is integrable and unbounded. |
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
localized Hardy the plan asked for. It does **not** finish
\(I_{\mathrm{tube}}\).

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

---

## What is still the next write

1. Analytic Hardy \(\to I_{\mathrm{tube}}\) with \(\delta\sim 2^{-j_*}\)
   and the wall term matched to the off-axis piece.
2. Energy-class low Bony term \(T\) (the open piece of H).
3. Then occupation time of the two regimes.

None of those is a pass on regularity. Checker:

```
python3 scripts/track_b_lemmas.py
python3 -m unittest tests.test_track_b_lemmas
python3 scripts/da_machine.py trackb
python3 scripts/da_machine.py check --domain B
```
