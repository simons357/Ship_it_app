# Transfer lemma — OPEN (kill lock, 14 Sep 2026)

**Status: OPEN.** This is **not** a proof of the Riemann Hypothesis.

**Have:** real arithmetic — inverse-GCD / Möbius–GCD \(Q_6\) matrix book.

**Missing:** a transfer lemma from a locked spectrum to

\[
M(x)=\sum_{n\le x}\mu(n)=O(x^{1/2+\varepsilon})\qquad(\forall\varepsilon>0).
\]

That bridge is **OPEN**. Inventing a field equation does not invent that arrow.

Related calculation draft (still open PR): [#86](https://github.com/simons357/Ship_it_app/pull/86) → `docs/papers/gcd/Q6_MERTENS_TRANSFER.md`.

---

## What is real (keep)

| Object | Status |
| --- | --- |
| Inverse-GCD matrix book (Track A), with the universal moat \(\lambda_{\min}\ge -1/2\) killed | arithmetic, **not RH** |
| \(Q_6(i,j)=\mu(\gcd(i,j))/\gcd(i,j)\) factorization, Rayleigh limit, one-sided parity edge | arithmetic / spectral, **not RH** |
| Classical Littlewood: \(M(x)=O(x^{1/2+\varepsilon})\Leftrightarrow\) RH | cite; **do not claim as yours** |
| Controlling \(Q_6\) paper: desktop `archive/RH_Proof_Chain_Synthesis/03_submission_draft/PAPER_B_Mobius_GCD_Q6.tex` | (It already says: **no spectral–Mertens bridge.**) |

---

## What is missing (do not fake)

- A proved identity or inequality that turns a spectral fact about **one locked operator** into \(M(x)=O(x^{1/2+\varepsilon})\) (or another catalog equivalent).
- A linear gap, a Rayleigh limit, a numerical floor through finite \(N\), or a cosine sum over primes is **not** that lemma.

---

## Destroyed arrows (do not reuse)

| Claim | Why it is dead |
| --- | --- |
| SFE / UHF / DHFA / compact \(\Delta[(PH\psi)^2\lambda]=\Phi\) / “master coherence” \(\Rightarrow\) RH | A field equation is not a Mertens bound. Canonical SFE is unresolved. |
| Explorer \(S(t)=\sum\sin(t\log p)/\sqrt{p}\) \(\Rightarrow\) RH | Prime-log oscillator. Visualization. Not \(M(x)\). |
| Route C: close \(\lambda_{\min}\) constant and a uniform gap, then “the chain to Littlewood is fully rigorous, establishing RH” | Spectral control of \(Q_N\) is not Littlewood. That sentence skips the transfer lemma. Kill it wherever it reappears (`EXTRACT_bc-019fda0f_fts_body.txt` §7). |
| Finite-\(N\) spectrum / occupancy / alignment \(\Rightarrow\) \(M(x)=O(x^{1/2+\varepsilon})\) | No uniform conclusion as \(N\to\infty\). Numerics are not the arrow. |
| Chapter X “Theorem SFE-RH proved” | Placeholder / stripped. Delete the theorem language. |
| Zenodo Route C body language “RH proved” | Superseded. Do not re-upload as a trophy. |
| Title weld “SFE / RH Explorer” as evidence | Live Base44 toy: https://sfe-rh-explorer-v1-07f8121c.base44.app/ — Primefield Explorer. Library chip reads SFE · UHF · DHFA · NAV-42 · Harmonic Blueprint. That branding is the weld. The math on the page is a cosine sum, a 3D picture, and a zeta-wave game. |

---

## Allowed next work

Prove or kill a **sharp candidate identity** linking a named spectral projection (or matrix element) of one locked matrix to \(M(N)\) or a standard transform of \(\mu\).

Label it **OPEN** until the estimate exists.

**Do not paste SFE into that note.**
