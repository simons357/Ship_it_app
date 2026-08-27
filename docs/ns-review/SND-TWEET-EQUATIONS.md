# SND equations from Jonathan Simons tweet (June 2026)

**Source:** [X/Twitter post](https://x.com/simonsmedical/status/2072045366430601408/photo/1) — one-page summary *Navier-Stokes Global Regularity on T³* (June 2026).

**Image fetch:** Direct `x.com` returned HTTP 403. Image obtained via `fxtwitter.com` mirror API and saved to `/opt/cursor/artifacts/da-snd-equations/snd_tweet_image.png`.

**Registry:** Machine-readable entries in `data/domain_architect/snd_tweet_equations.json`.

---

## Tweet text (API)

> New preprint: Global Regularity of the Navier–Stokes equations on the 3-torus T³. The whole question reduced to a single spectral condition, worked step by step. Independent research, open for scrutiny. Full paper + Ring Lemma on Zenodo.

---

## Central condition (boxed in image)

\[
\inf_{t \ge 0}\ \frac{\lambda_{\min}(\tilde{H}_N[u(t)])}{\lambda_{\max}(\tilde{H}_N[u(t)])}\ >\ -\frac{1}{2}
\]

**Caption:** *The normalized shell-helical operator \(\tilde{H}_N[u]\) does not develop a ground state more negative than \(-\tfrac{1}{2}\) of its top eigenvalue.*

**DA plain text:**

```text
inf_{t>=0} lambda_min(tilde_H_N[u(t)]) / lambda_max(tilde_H_N[u(t)]) > -1/2
```

This is **not** the same token string as the repo’s canonical SND-U hypothesis (`inf J/X ≥ c_*`). The tweet’s “single spectral condition” is the **Bypass / shell-helical eigenvalue ratio** book. The table also lists **[SND]** separately (see below).

---

## [SND] — Spectral Non-Dispersal (table row)

\[
\inf_{t \ge 0}\ \frac{J(t)}{X(t)}\ \ge\ c_* > 0
\]

| Symbol | Definition |
| --- | --- |
| \(X(t)\) | \(\|\nabla u(t)\|_{L^2}^2\) |
| \(J(t)\) | \(\max_j X_j(t)\) (dominant shell enstrophy) |
| \(c_*\) | positive spectral floor |

Tweet table status: **“Proved”** in small / bounded-\(H^2\) / large-data regimes.

---

## Full argument chain (table in image)

| Result | Tweet status | Key tool |
| --- | --- | --- |
| Thm A: \(Q_1\)-augmented NS globally \(C^\infty\) | Proved | Strict dissipation |
| Thm B: Phi-Renorm cancels \(1/r^4\) axis singularity | Proved | \(\Phi=\Gamma/r^2\) gauge |
| Thm C: Convergence \(u^\epsilon\to u\), no Grönwall | Proved | Rate \(O(\epsilon^{4/(\beta+2)})\) |
| **Thm D: Clay \(\Leftrightarrow\) [SND]** | Proved | Exact equivalence |
| **[SND]** in small / bounded-\(H^2\) / large data | Proved | Three regimes |
| Thm F: Shell-Spread Poincaré | Proved | Bony paraproduct |
| **Thm H: (SND-C)** | Proved | CCFS + Young |
| **Bypass Lemma:** \(\tilde{H}_N\) norm bound, \(5\times\) margin | Proved | \(L^2\) orthogonality |
| **Ring Lemma:** Borromean triadic cancellation | Proved | Spectral topology |
| Thm I: Geometric Bridge, \(F^*\to 0\) | Proved | Constantin–Fefferman |
| **Main result: no blowup on \(T^3\)** | Proved | Full chain above |

---

## Mechanism bullets (image prose)

1. **\(Q_1\) Simons Coherence Operator** — targeted dissipation.
2. **Ring Lemma** — three interlocked Littlewood–Paley shells; Borromean topological constraint.
3. **Bypass Lemma** — normalize \(H_N[u]\) by total energy \(\Sigma(t)\); pure shell-ratio observable; **\(5\times\)** safety margin stated.

---

## Mismatch flags vs repo definitions

| Tweet object | Repo book | Mismatch |
| --- | --- | --- |
| Central \(\lambda_{\min}/\lambda_{\max}\) of \(\tilde{H}_N\) | SND-U (`J/X`) | Different observable; tweet calls both “single condition” and lists [SND] separately |
| Thm D Clay \(\Leftrightarrow\) [SND] | CLAY-B001 + SND-U001 | DA refuses unconditional Clay glue; equivalence not established in gap-closure audit |
| Thm H (SND-C) | SND-C001 / THM-H001 | **Compatible** — same conditional \(X\le M\) book |
| Ring Lemma | RING-BVB001 | **Compatible** as conditional geometry toolkit |
| Main result “proved” | CLAY-B001 | **Incompatible** with DA disposition RETIRE on unconditional Clay |
| \(H_N\) / \(\tilde{H}_N\) | Arithmetic \(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\) in ARITH-H | **Notation collision** — different books (see `docs/domain-architect/04-NOTATION-COLLISIONS.md`) |

---

## Zenodo / archive lines in image

- Zenodo `10.5281/zenodo.19842060` (May 18, 2026)
- Full paper *Global Regularity of the Navier-Stokes Equations on T³* (May 2026)

Honest KEEP framing in this repo remains **`10.5281/zenodo.22050976`** (Ring + SND hypothesis / conditional only).
