# Energy-class low Bony \(T\)

`python3 scripts/track_b_bony_t.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. Spread side. The kingdoms stayed on
one term.

---

## The split

On \(\mathbb{T}^3\), the flux into the peak shell is

\[
\Pi_j=\int\Delta_j\bigl[(u\cdot\nabla)u\bigr]\cdot u_j\,dx.
\]

Cut \(u=u_{\le j-N}+u_{\mathrm{near}}+u_j+u_{\mathrm{high}}\). Then

\[
\Pi_j=T+T^*+R_{\mathrm{near}}+\mathrm{self}.
\]

B1 / T2 Lemma 1 already kills the self piece:

\[
\int(u_{\le j}\cdot\nabla)u_j\cdot u_j=0.
\]

What remains of the **low** paraproduct is \(u_{\mathrm{low}}\)
feeding neighboring shells into \(\Pi_j\), plus the commutator
\([\Delta_j,u_{\mathrm{low}}\cdot\nabla]\). That is the open
piece of H.

---

## Energy class (B7b)

Bernstein plus Cauchy–Schwarz on the low sum:

\[
\|u_{\le j-N}\|_\infty
\lesssim 2^{(j-N)/2}X^{1/2}.
\]

The script’s ratio \(\|u_{\mathrm{low}}\|_\infty/2^{(j-N)/2}X^{1/2}\)
stays \(\approx 0.02\) as more low modes are stacked. **Pass.**
No \(\rho\) improvement is used.

---

## The \(\rho^{1/2}\) hope (B7c)

Under SPREAD each shell satisfies \(X_k\le\rho X\). The hope in H
was that this upgrades the low sum to

\[
\|u_{\le j-N}\|_\infty\lesssim\rho^{1/2}X^{1/2}
\]

uniformly as \(\rho\to 0\), which is what G needs to push you out
of deep SPREAD.

Stack aligned low plane waves. Each shell is \(\le\rho X\). The
\(L^\infty\) sum is not:

| \(M\) low modes | \(\rho\) | \(\|u_{\mathrm{low}}\|_\infty/(\rho^{1/2}X^{1/2})\) |
|---|---|---|
| 1 | 0.40 | 0.11 |
| 2 | 0.12 | 0.22 |
| 4 | 0.022 | 0.44 |
| 6 | 0.007 | 0.66 |

The ratio climbs as \(\rho\) drops. **Fail** of the uniform
hope. CCFS locality does not turn the sum into
\(O(\rho^{1/2}X^{1/2})\).

G is dead. H at a *frozen* \(\rho\le 1/4\) can still use the
energy-class bound. That is a different sentence.

---

## They work it

**Kato.** T2 Lemma 1 is ours in spirit: the self-flux is zero.
Do not rename the leftover \(T\) into a continuation criterion.

**Leray.** Energy class only. You have \(\|u\|_{H^1}\). You do
not have an \(H^{2.3}\) ball. Lemma 2 stays dropped.

**Majda.** Spread means no shell owns the mass. It does not
mean the low sum is small in \(L^\infty\). That was the wish.

**Feynman.** The missable number is
\(\|u_{\mathrm{low}}\|_\infty/(\rho^{1/2}X^{1/2})\). It moves
when you stack modes. G cannot have it.

**Tesla.** \(M\) is a knob. Turn it up, the \(\rho^{1/2}\)
ratio climbs, the energy-class ratio sits. Apparatus.

**Fefferman.** Do not call this alignment. Cartesian
paraproduct. The tube is the other column.

**Ladyzhenskaya.** I am not on this column. Frozen \(\rho\le 1/4\)
is a smaller class, like my \(\varepsilon>0\). It is not the
limit \(\rho\to 0\).

**Caffarelli.** A dead estimate is not a blowup.

**Beale.** Nobody votes this into global regularity.

**Einstein.** The object stayed named. Classical \(u\) on
\(\mathbb{T}^3\). No \(\Phi\) in \(\Pi_j\).

**Operator.** One term. Next: occupation time of 3-CONC vs
SPREAD, with B4c on the packet side and energy-class \(T\) on
the spread side.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B7 | **pass** | \(\Pi_j=T+T^*+R+\mathrm{self}\) |
| B7a | **pass** | self-flux is T2 Lemma 1 |
| B7b | **pass** | energy-class \(L^\infty\) on the low sum |
| B7c | **fail** | uniform \(\rho^{1/2}\) as \(\rho\to 0\) |
| Theorem G | **fail** | needed B7c |
| H at frozen \(\rho\le 1/4\) | **open** | energy-class \(T\) is legal there |
| domain B | **open** | \(X\) is not bounded |

Next write: occupation time of the two regimes.
