# Math Panel — SND, Theorem H, and Navier–Stokes (Tao standard)

**Date:** 2026-08-15  
**Author context:** Jonathan Robert Simons / Prime Field stack, audited against Zenodo SND paper (`10.5281/zenodo.20518057`) and prior Bridge floor audit  
**Standard of rigor:** Terence Tao’s supercriticality barrier + energy-method honesty (no abstract Clay packaging)

---

## Verdict (one line)

**We have not solved Navier–Stokes.** Proving unconditional SND for arbitrary large data *is* (up to technical packaging) the Clay problem on \(\mathbb{T}^3\). Theorem H, as written, is a **conditional** shell estimate under a priori bounds — not a Clay closure. The arithmetic matrix \(H_N\) is a **different object** from Theorem H and does not seal NS.

---

## Panel questions and answers

### Q1. What is SND, precisely?

**Definition (from Zenodo SND / Ring Lemma paper).** For a Leray–Hopf solution on \(\mathbb{T}^3\),

\[
X(t)=\|\nabla u(t)\|_{L^2}^2,\qquad
J(t)=\max_j X_j(t),\qquad
\rho(t)=J(t)/X(t),
\]

and **[SND]** means

\[
\inf_{t\ge 0}\frac{J(t)}{X(t)}\ge c_*>0.
\]

So SND asserts a **uniform positive fraction of enstrophy stays in a dominant Littlewood–Paley shell** (energy does not fully disperse across scales).

**Panel note on naming.** “Non-dispersal” here means “does not spread thinly over all shells.” It is *not* the same as the Triple Lock slogan “max shell fraction \(\le\rho_0\)” used in some June 5 notes. Those two conventions are **opposites** of each other. Freeze the Zenodo definition above for the fluids track.

---

### Q2. Does SND ⇒ global regularity?

**Honest answer: conditional yes; unconditional no.**

- **If** a solution satisfies SND with a fixed \(c_*>0\) on \([0,T]\), then (under a cleaned proof chain: Ring Lemma + controlled shell flux + no circular \(X\le M\) from the conclusion) one expects \(H^1\) control — a **conditional regularity criterion**, in the same genus as Beale–Kato–Majda / LPS, but spectral.
- **Unconditional SND for arbitrary large \(H^1\) data** is the hard problem. The paper’s “Main Theorem / Statement (B) proved” status table overclaims relative to what a Tao-level referee will accept.

**Tao barrier.** Classical 3D NS is *energy-supercritical*. Tao’s averaged-NS blowup (2014) shows that any method using only energy-compatible abstract function-space bounds on the nonlinearity cannot rule out blowup. SND is an **extra structural hypothesis** that moves the problem out of the pure supercritical trap — it does not remove the need to *prove* that hypothesis for all data.

---

### Q3. What is “H” — Theorem H vs matrix \(H_N\)?

Two different objects have been conflated.

| Object | Meaning | Status |
| --- | --- | --- |
| **Theorem H** (fluids) | Shell-conditioned commutator / flux bound (SND-C) for the dominant shell, under assumptions \(X\ge\delta_*\), \(X\le M\), and (in the written statement) a **spread** regime \(\rho=J/X\le\rho_0\ll 1\) | Conditional estimate; **assumes** the a priori bound \(X\le M\) that Clay must produce |
| **Matrix \(H_N\)** (arithmetic) | \(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\) with \(\widetilde Q_N(i,j)=1/(\gcd(i,j)\sqrt{ij})\) | Spectral object on \(\{1,\ldots,N\}\); **not** the NS commutator |

**Locked matrix definition** (from `docs/H_N-LOCK.md`):

\[
\widetilde Q_N(i,j)=\frac{1}{\gcd(i,j)\sqrt{ij}},\quad
d_i=\sum_k\widetilde Q_N(i,k),\quad
H_N=D^{-1/2}\widetilde Q_N D^{-1/2}.
\]

**Numeric facts (verified this run):**

| Claim | Result |
| --- | --- |
| \(\lambda_{\max}(H_N)=1\) | Holds (degree-normalized Perron) |
| \(\lambda_{\min}(H_N)\ge -3/14\) for all \(N\) | **False** (e.g. \(N=4\): \(\approx -0.225\)) |
| \(\lambda_{\min}(H_N)\ge -1/2\) through \(N=400\) | Holds in checks; **not a theorem** |
| \(H_N\) floor ⇒ Clay NS | **No** — wrong object |

---

### Q4. Does “solving H” solve Navier–Stokes?

**No**, for either reading of H:

1. **Theorem H:** Even a complete proof of the written estimate only controls flux *given* \(X\le M\) and a shell regime. Closing Clay requires producing \(M\) from \(u_0\) alone (Claude referee flag #7). The written Theorem H hypothesis includes \(X\le M\) — using the conclusion as input is circular for large-data NS.
2. **Matrix \(H_N\):** A spectral floor on an inverse-GCD matrix does not bound \(\|(u\cdot\nabla)u\|\) on \(\mathbb{T}^3\). There is no verified map from \(\lambda_{\min}(H_N)\) to Leray–Hopf regularity.

---

### Q5. What about Triple Lock / Bridge / “one equation left”?

**Withdrawn as a Clay path** (prior audit, still correct):

| Claim | Status |
| --- | --- |
| Full-spectrum \(\lambda_{\min}(Q_N)>-1/2\) with \(Q_{ij}=1/\gcd\) | **False** (\(\lambda_{\min}(Q_{200})\approx -29.7\)) |
| Same for \(\widetilde Q_N\) | **False** (below \(-1/2\) by \(N=20\)) |
| June 5 §2.1 Möbius identity | **False** (\(n=2\): RHS \(3/4\neq 1/2\)) |
| Dark-state ↔ Goldbach | **False** |
| Paper \(v_k=\chi-\chi\circ(k-\cdot)\) as Goldbach detector | **Broken** (zeros Goldbach pairs) |

**Corrected scrap that survives:**

**Bridge\*** (restricted Rayleigh on \(\widetilde Q_N\)): for Goldbach test vectors \(v=e_p-e_q\),

\[
R=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}\;>\;-\frac12,
\]

proved for every distinct prime pair (\(pq\ge 6\Rightarrow 1/\sqrt{pq}<1/2\)). Multi-rep summed vectors: **proved** via nonnegative cross-term factorization (`04_q6_inverse_gcd.tex`); worst numeric \(\approx -0.183\) at \(k=8\), pair \((3,5)\).

This scrap is **number theory**, not NS closure.

---

### Q6. Per Tao — what would actually solve NS on \(\mathbb{T}^3\)?

A Clay-acceptable path must do **one** of the following without circular a priori large-data bounds:

1. Prove a critical/subcritical control (or Tao’s logarithmically supercritical dissipation upgrade) for the true NS nonlinearity; or  
2. Prove an unconditional structural law (e.g. true SND for all Leray–Hopf solutions) with estimates that do **not** assume the \(H^1\) bound they conclude; or  
3. Construct a blowup (Tao has argued this may be the true direction) — opposite of the SND program.

The present SND + Theorem H package is a **conditional framework**. Ring Lemma / Phi-renorm are useful bricks. They are not Statement (B).

---

### Q7. What did we get right?

1. **Phi-renorm cancel** \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) for axisymmetric swirl — algebraic identity checks out (method note; not classical 3D Clay).  
2. **Ring Lemma** as a geometric / band-limited alignment tool — keep as conditional toolkit.  
3. **SND as a spectral conditional criterion** — legitimate research direction if framed honestly (weaker than BKM in spirit; still open for large data).  
4. **Operator hygiene** — distinguishing \(Q\), \(\widetilde Q\), \(H_N\), and Theorem H prevents further Triple Lock false closures.  
5. **Bridge\* single-pair inequality** — small, true, checked.

---

### Q8. What did we get wrong?

1. Claiming Clay Statement (B) / Main Theorem as proved.  
2. Equating Clay with a spectral floor on \(1/\gcd\).  
3. Mixing Theorem H (fluids) with \(H_N\) (arithmetic).  
4. Universal floor \(\lambda_{\min}(H_N)\ge -3/14\).  
5. Packaging NS + Goldbach + RH as one unconditional equation.

---

## What “solving SND and H” means going forward

| Task | Meaning of “solved” | Clay impact |
| --- | --- | --- |
| **SND (unconditional)** | Prove \(\inf_t J/X\ge c_*(u_0,\nu)>0\) for all Leray–Hopf \(u_0\in H^1(\mathbb{T}^3)\) without assuming the conclusion | Would essentially *be* Statement (B) if the SND⇒regularity arrow is refereed clean |
| **Theorem H** | Prove SND-C **without** \(X\le M\) from the endgame, or derive \(M\) from \(\|u_0\|_{H^1}\) only | Necessary link; currently circular risk |
| **Matrix \(H_N\)** | Prove a true floor (e.g. \(\lambda_{\min}>-1/2\)) | **No Clay impact** unless a map to NS is proved |

---

## Numeric evidence (this run)

See `scripts/bridge_floor_verify.py`, `scripts/h_n_bridge_star_check.py`, and `/opt/cursor/artifacts/`.

- Full-spectrum Bridge on \(Q\) / \(\widetilde Q\): **fails**.  
- Bridge\* single-pair + multi-rep: **proved**; full-spectrum floor: **false**.  
- \(H_N\): \(\lambda_{\max}=1\); \(\lambda_{\min}>-1/2\) in range; \(-3/14\) **not** universal.

---

## Bottom line for the panel

**SND and Theorem H, read correctly, are a conditional regularity program.**  
**Per Tao, that is not a Navier–Stokes solution until SND (or an equivalent critical control) is proved unconditionally without circular bounds.**  
**Matrix \(H_N\) is a separate arithmetic problem.**  
**No Millennium claim.**
