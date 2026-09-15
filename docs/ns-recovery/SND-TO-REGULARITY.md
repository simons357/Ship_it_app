# SND ⇒ regularity — what the shell condition actually does

**Date:** 15 September 2026  
**This book.** No more numerical sweeps. This page writes the implication,
not a Clay close. It does **not** glue SND to Lemma★, Soft X, or Theorem H
as unconditional SND.

Sources scored (other branches, not merged):
Zenodo Ring/SND paper `docs/papers/SND_RING_LEMMA_NS.tex`,
corrected note `docs/papers/submit/02_ring_lemma_snd_conditional.tex`,
Tao panel `docs/math/TAO-MATH-PANEL-SND-H.md`
on `origin/cursor/tao-snd-h-panel-a0eb`.

**NS is not solved.** Soft X silent.

---

## Definitions (frozen)

On a Leray–Hopf solution on \(\mathbb T^3\), Littlewood–Paley shells:

\[
X_j=2^{2j}\|\Delta_j u\|_{L^2}^2,\qquad
X=\sum_j X_j=\|\nabla u\|_{L^2}^2,
\]
\[
J=\max_j X_j,\qquad
\rho=J/X,\qquad
j_*=\operatorname{argmax}_j X_j.
\]

**[SND]** (Zenodo / Tao panel freeze):

\[
\inf_t\frac{J(t)}{X(t)}\ge c_*>0.
\]

This \(X\) is **enstrophy**. It is **not** the Stokes-moment
\(|A^{1/2}u|_2^2\) paired with \(Y=|Au|_2^2\). The quotient is
**concentration**, not \(\Lambda=Y/X\).

**CONC** is \(\rho\ge c_*\) (August SND). **SPREAD** is
\(\rho\le\rho_0\ll 1\) (June T2 / Theorem H’s written hypothesis).
Those two conventions are **opposites**. This page uses CONC for [SND].

---

## 1. What the shell condition controls

[SND] controls **one number**: a uniform positive fraction of enstrophy
sits in a single dominant LP shell.

It does **control:**

- \(\rho(t)\ge c_*\), so \(X_{j_*}\ge c_* X\).
- That the solution is not in the fully spread regime \(\rho\to 0\).
- A necessary condition for many LP pigeonhole / Ring arguments that
  need a distinguished scale.

It does **not** control:

- **Which** shell is dominant. \(j_*(t)\) may run to \(+\infty\).
- The **speed** of that run (\(\mathrm d j_*/\mathrm d t\), or
  \(\lvert\mathrm d\rho/\mathrm d t\rvert\)).
- Enstrophy size \(X(t)\) itself. A spike with \(\rho\ge c_*\) and
  \(X\to\infty\) at a climbing \(j_*\) is compatible with [SND] as
  written.
- The flux \(\Pi_{j_*}\) off the dominant shell.
- \(\|\omega\|_{L^\infty}\), BKM, or \(\int|Au|_2^2\,\mathrm dt<\infty\).

Ring Lemma, when it applies, bounds vorticity direction on a coherent
set \(E_c\) by a multiple of the **shell frequency** \(O(2^{j_*})\).
That bound **tracks \(j_*\)**. If \(j_*\) is unbounded, the geometric
constant is unbounded. SND alone does not freeze it.

---

## 2. What frequency-drift information is still needed

To turn [SND] into \(H^1\) control you still need information that
[SND] does not name:

1. **A law for \(j_*(t)\).** Either \(j_*\) stays bounded on \([0,T]\),
   or some time-integrable control of \(2^{c j_*}\) (or of
   \(\|\nabla\xi\|_{L^\infty}\) on \(E_c\)) holds. The corrected
   conditional note feeds Constantin–Fefferman with a constant
   \(\lesssim 2^{j_*}/c_*\). That is drift-sensitive.
2. **A Lipschitz / occupation estimate for \(\rho\).** The large-data
   “cascade incompatibility” paragraph in the Ring paper bounds
   \(\lvert\mathrm d(J/X)/\mathrm dt\rvert\) over a time
   \(\tau\sim M/(\nu\Lambda^2)\) and gets drift \(\sim CM/(\nu\delta)\).
   The \(M\) in that line is an a priori bound on \(X^{1/2}\).
3. **Flux off the dominant shell** \(\lvert\Pi_{j_*}\rvert\), without
   taking \(X\le M\) from the conclusion. That is SND-C / Theorem H,
   a different estimate, written in the **spread** regime
   \(\rho\le\rho_0\).
4. **Paper2 \(\mathrm d_{\mathrm{SND}}\)** (“shell drift, helical
   imbalance, …”) is a **different open hypothesis**. It is not [SND]
   and not \(\mathfrak T_c\).

Until (1)–(3) are supplied without circular \(M\), [SND] is a
concentration hypothesis, not a continuation criterion.

---

## 3. Does the written implication assume the desired bound?

**Yes, in the places that actually close \(H^1\).**

| Step | What it assumes | Circular for Clay? |
|---|---|---|
| Theorem D(i) as in `SND_RING_LEMMA_NS.tex` | Invokes “Prodi–Serrin shell-by-shell,” then Theorem C producing \(\|u^\varepsilon\|_{H^1}\le M\) uniformly in \(\varepsilon\) | If \(M\) is the bound D claims, **yes** |
| Theorem E | Smooth \(u\) with \(X(t)\le M\) on \([0,T]\), then concludes \(\inf J/X>0\) | **Yes** — SND from the \(H^1\) ceiling, not the reverse |
| Small-data SND | Koch–Tataru regularity first; then SND by continuity | Gets SND **from** regularity |
| Large-data cascade paragraph | \(M=\sup X^{1/2}\), \(\delta\gg C_S\nu M^2\) | **Yes** — \(M\) is input |
| Theorem H / SND-C | \(X\le M\) and (as written) **spread** \(\rho\le\rho_0\) | **Yes** for large-data Clay; also the wrong \(\rho\)-regime for [SND] |
| Corrected submit theorem | SND **and** Ring on a band-limited approximation **and** dissipative control of spread; “details deferred” | Honest outline, **not** a closed chain |

Theorem D(ii) as written is not a usable converse: it mixes ESS
(\(\|u\|_{L^3}\to\infty\) at blowup) with a line that treats
\(\|u\|_{H^1}\) as bounded while \(X\to\infty\). Do not cite that
paragraph as a theorem.

Theorem F (shell-spread Poincaré \(\mathcal D\ge\nu\cdot 4^{N-1}\rho X\))
treats “\(N=\lceil X/J\rceil\) active shells” as if they occupied an
index interval of length \(N-1\) with mass \(\ge J/2\) at the top.
If the mass sits in low shells, the dissipation lower bound fails.
The Tao/DA record already marks this as **not a theorem**.

The corrected note `02_ring_lemma_snd_conditional.tex` is the honest
shape: **if** SND **and** Ring applies to a band-limited dominant
piece **and** spread is damped, then no singularity on that interval.
It does **not** prove SND for large data. It does **not** remove
\(2^{j_*}\) from the geometric constant.

---

## One-line implication that actually sits

\[
[\mathrm{SND}]
\;\not\Rightarrow\;
\text{global regularity}.
\]

What sits is the weaker outline

\[
[\mathrm{SND}]
\;+\;
\text{Ring on a band-limited }j_*\text{-piece}
\;+\;
\text{spread damping}
\;+\;
\text{no circular }X\le M
\;\overset{?}{\Longrightarrow}\;
H^1\text{ on that interval}.
\]

The first three extra bullets are not implied by [SND]. The fourth
is currently violated by Theorem H / E / the large-data paragraph.

Unconditional SND for all Leray–Hopf \(H^1\) data, with estimates
that do not assume the \(H^1\) bound they conclude, **is** (up to
packaging) the Clay problem on \(\mathbb T^3\). That is the Tao
panel lock. It has not been done.

---

## What this is not

- Not Lemma★ and not a repair of unrestricted ★ (\(v_n\) still kills
  that box).
- Not exact-shell 9D.
- Not a continuation criterion by itself.
- Not a reason to run another \(K\) sweep.
- Not Soft X, Triple Lock, or \(1/\gcd\).

**NS not solved.**
