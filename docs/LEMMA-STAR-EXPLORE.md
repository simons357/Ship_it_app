# SuperGrok “explore boundedness” — scored against the lock

10 September 2026. Screenshots, 19:08. Papers and
the on-branch write-up, not a vote.
**★ OPEN. NS not solved. Do not start H1.
Do not glue Q-stack. Do not stop patching ★.**

Statement: [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
Identities: [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
9B: [`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md).
N-shell: [`RSTAR-SHELL-CLIMB.md`](RSTAR-SHELL-CLIMB.md).
ABC_λ: [`ns-recovery/CS-REMAINDER-VS-DA-REJECT.md`](ns-recovery/CS-REMAINDER-VS-DA-REJECT.md).

---

## Keep (matches the lock)

None of those four items stamps ★ closed.
A bound on one family is a sample of
\(C_{\mathrm{geom}}\), not ★.
Kill rule: \(\mathcal R_\star\to\infty\).
One large finite number does not.

\(D_s\) is a closed spectral identity.
Every Sobolev comparison for \(D_s\) alone
is closed. The map \(D_s\mapsto\) control of
\(T_c\) **is** Lemma★ and remains open.

H1 is a different integral. Do not start it
from this exploration.
Lu–Doering \(\dot\Omega\le C\nu^{-3}\Omega^3\),
Poincaré \(X\ge\lambda_1 E\), shell-model
moment bounds, and CF / Hölder coherence
are cousins. They do not recast as
\(\sup\mathcal R_\star<\infty\).

The numeric table matches this book:

| Probe | This book |
|---|---|
| One shell | \(D_s=T_c=0\). Vacuous. |
| 9A AP | \(\mathcal D_s\) grew faster than \(T_c\) |
| 9B \(K_{\alpha,\beta}\) | \(\varepsilon\to0\) gives \(\mathcal R_\star\to K\); sample max \(K\approx 0.641\) |
| Default-phase triad | \(\mathcal R_\star\sim 2\times 10^{-4}\) |
| Best-phase triad / later drill | \(\sim 0.022\), not the 9B peak |
| ABC exact script | λ=2, 3, 4 only; \(T_c=0\) on the 3-mode probe |
| ABC table λ=8 | \(\mathcal R_\star(-v)\approx 0.327\) (FFT, after reverse) |
| N-shell max | saturates; best \(0.610\) on \((1,2)\) |
| ABC on those grids | does not saturate |

N-shell flat while ABC climbs is a
**kill-lane clue**. Not \(\mathcal R_\star\to\infty\).
Not a falsifier.

---

## Already on disk (do not re-derive as new)

**Two-shell \(D_s\).** Sits:

\[
D_s
=
\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}
{\alpha e_\alpha+\beta e_\beta}.
\]

**Near-shell \(T_c\).** 9B, aligned closer:

\[
T_c(v_\varepsilon)
\sim
\beta(\beta-\alpha)\,\varepsilon\,\|\Pi_\beta B(w,w)\|_2,
\qquad
\mathcal R_\star\to K_{\alpha,\beta}(w).
\]

The gap \((\alpha-\beta)\) **cancels** in that
limit. A hunt that expects \(\mathcal R_\star\)
to diverge with the gap is the wrong hunt
on this family. 9A already saw \(\mathcal D_s\)
win on AP.

**Two-shell max as a number.** N-shell
maximizer: best \(\mathcal R_\star=0.610\) at
\(N=2\), shells \((1,2)\). Extra shells did
not beat two. Finite. Not a kill.
Growing \(s\) stays live (\(K\le 16s\)).

**Fourier dilation** \(v(n\cdot)\).
\(\mathcal R_\star\) is exactly invariant.
Already checked.

---

## Correct (does not sit as written)

**1. “\(T_c\) is a bilinear in the shell
energies.”** \(D_s\) is. \(T_c\) is a signed
triad sum. Phases and which triples close
enter. Do not drop \(\mathrm{Im}\). Two
Fourier keys is the wrong test, not two
shells.

**2. Gap × mass / Chebyshev / Calderón–
Zygmund symbol.** A proposed estimate.
Not on disk as a theorem. Do not seat it
as sitting. Do not replace complete signed
\(T_c\) by a symbol bound on
\(\{|\lambda-\Lambda|\ge\delta\}\).

**3. Spatial dilation** \(v_\mu(x)=v(\mu x)\)
with \(E\sim\mu^{-3}\), \(X\sim\mu^{-1}\),
\(Y\sim\mu\), \(D_s\sim\mu\).
That is a continuum / Bloch scaling.
It is **not** the lock’s uniform Fourier
dilation on \(\mathbb{T}^3\). ABC_λ is
spatial concentration on a **fixed** torus
(Gaussian cutoff + Leray), not \(v(n\cdot)\).
Do not mix those groups. \(\mathcal R_\star\)
is amplitude-invariant and Fourier-dilation
invariant by algebra. A genuine kill is still
\(\mathcal R_\star\to\infty\).

**4. Three-shell formulas as a new door.**
\(N=3,4,5\) already ran. Extra shells did
not beat two. Do not rebuild the table
and call it a close.

**5. “Near-shell / HH→L max \(\sim 2\cdot10^{-4}\).”**
That is the default-phase triad, not 9B
and not the N-shell peak. Do not merge
those three numbers.

---

## What “explore boundedness” may still do

Compatible with “do not stop patching ★”:

- Keep the two-shell / 9B identities as
  they sit. Do not invent a second \(D_s\).
- Growing \(s\) (phase-free \(K\le 16s\))
  remains legitimate. Fixed-\(s\) 9D is dead.
- ABC_λ as an evaluator: more finite λ
  only raises \(C_{\mathrm{geom}}\) unless
  \(\mathcal R_\star\to\infty\). Exact script
  stays four jobs (λ=2, 3, 4).
- Saturation diagnostic: track
  \(\mathcal R_\star\) **and** \(D_s/Z\).
  Ratio flat while \(D_s/Z\to 0\) is
  concentration (N-shell). \(D_s/Z\) away
  from 0 with a climb is the ABC-like lane.
  A climb that stays finite is not a kill.

Not allowed: stamp ★ closed; start H1;
glue Q-stack; cash Lu–Doering or CF as ★;
cash \(0.641\), \(0.610\), or \(0.327\) as
\(C_0\); mix \(v(\mu x)\) with \(v(n\cdot)\);
write “almost proved.”

There is no Lemma★ proof to walk through.
The hole is still \(\sup\mathcal R_\star<\infty\).

Stay in this chat.
