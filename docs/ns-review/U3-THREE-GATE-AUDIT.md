# \(\|u\|_3\) three-gate audit

2 October 2026.  
Companion to the 11 September generic chain and the dissipation-threshold honesty card.

**The \(\|u\|_3\) derivation is not in this deposit. Do not invent it. When it comes back, run these gates, then send the implication chain — not just the algebra.**

Chain: [`UNAUG-GENERIC-3D-PROOF-CHAIN.md`](./UNAUG-GENERIC-3D-PROOF-CHAIN.md).  
Honesty: [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md).  
Machine lock: [`data/ns_proof_chain/u3-three-gate-2026-10-02.json`](../../data/ns_proof_chain/u3-three-gate-2026-10-02.json).

Classical unaugmented NSE only. No extra field. No \(Q\). Regularity is not claimed.

---

## What this page is

The same audit style that locked \(\rho_j<\nu\) to palinstrophy/(A), not to \(\nu Z_j\). Applied to any \(\|u\|_3\) budget.

Three gates, separately. A pass on algebra is not a pass on regularity value or novelty.

---

## The three gates

### Gate 1 — Derivation

Prove the inequality cleanly:

- cutoff-uniform (Galerkin / frequency cutoff does not hide in the constant);
- constants named and finite, independent of the unknown field and of the cutoff;
- no hidden higher norm (\(L^\infty\), \(\|\nabla u\|_\infty\), BKM, \(H^s\) for \(s>1\), a copy of \(\dot e_j\), \(\dot Z\), or \(\Lambda'\)).

Fail if the constant depends on \(R\), on \(\|\nabla u\|_\infty\), or on a Serrin/ESS quantity already assumed finite.

### Gate 2 — Regularity value

Determine whether the resulting time-space condition is genuinely weaker or different from classical Prodi–Serrin–Ladyzhenskaya scaling, and specifically whether it gives anything beyond the endpoint

\[
u\in L^\infty_t L^3_x
\]

of Escauriaza–Seregin–Šverák (ESS 2003, \(L_{3,\infty}\) solutions are smooth).

Prodi–Serrin–Ladyzhenskaya (sufficient):

\[
u\in L^p_t L^q_x,
\qquad
\frac2p+\frac3q=1,
\quad q>3.
\]

Scaling. \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2 t)\). Then

\[
\|u_\lambda\|_{L^p_t L^q_x}
\quad\text{is invariant}
\iff
\frac2p+\frac3q=1.
\]

At \(q=3\): \(\frac2p+1=1\Rightarrow p=\infty\). That is ESS, not a new line.

Beirão da Veiga 1995 (gradient form, sufficient):

\[
\nabla u\in L^p_t L^q_x,
\qquad
\frac2p+\frac3q=2,
\quad q>\tfrac32.
\]

At \(q=3\): \(\frac2p+1=2\Rightarrow p=2\). So

\[
\int_0^T\|\nabla u\|_3^2\,dt<\infty
\]

is the classical \((p,q)=(2,3)\) Beirão da Veiga point. Paying that integral by assuming it is finite is a reformulation, not a new regularity mechanism.

If the new budget ultimately requires something already strong enough to imply one of those conditions, the algebra may be useful and the mechanism is not new.

### Gate 3 — Novelty

Search the literature for the exact inequality and equivalent formulations. A different-looking spectral or \(\Lambda\)-weighted expression can reduce algebraically to a known interpolation or energy estimate.

Known objects that a \(\|u\|_3\) write must be checked against, not rediscovered:

| Object | Role |
| --- | --- |
| Energy \(\tfrac12\dot X=-\nu\|\nabla u\|_2^2\) | Leray; closed on this chain (Step 0) |
| Kato 1984 mild solutions in \(L^3\) | local existence / small-data global; not a regularity close |
| Prodi–Serrin–Ladyzhenskaya | sufficient class, \(q>3\) |
| Escauriaza–Seregin–Šverák 2003 | \(L^\infty_t L^3_x\) endpoint |
| Beirão da Veiga 1995 | \(\nabla u\in L^p_t L^q_x\), \(\frac2p+\frac3q=2\) |
| Interpolation \(\|u\|_3\lesssim\|u\|_2^{1/2}\|u\|_6^{1/2}\lesssim X^{1/4}\|\nabla u\|_2^{1/2}\) | energy-class rewrite; not a new bound |

Fail Gate 3 if the displayed \(\|u\|_3\) or \(\Lambda\)-weighted form is an algebraic rearrangement of one of the above.

---

## The microscope

The interesting outcome is a **cutoff-uniform, NSE-derived** budget that controls only the **growth-capable portion** of the \(L^3\) behaviour **without first assuming** a Serrin / ESS / Beirão da Veiga-class quantity is finite.

That is the same refuse used on \(\rho_j<\nu\): a comparison that lives in a known sufficient class is not an independent payment of the remainder.

On active times (the only times that can lift \(\Lambda\) or \(X\)), ask:

- does the budget close using only energy, viscosity, and quantities already controlled by Step 0;
- or does it insert \(\|u\|_{L^\infty_t L^3}\), \(\int\|\nabla u\|_3^2\), or a Serrin pair as an assumption?

The first would be a new mechanism. The second is a criterion.

---

## Score of what is already on the desk (\(\|\nabla u\|_3\), not \(\|u\|_3\))

Other branches (PRs #149, #151, #152) attack \(g=\|\nabla u\|_3\), not \(\|u\|_3\). Do not relabel them as the \(\|u\|_3\) derivation.

| Item | Gate | Verdict |
| --- | --- | --- |
| \(\lvert T_c\rvert\le C g\sqrt{D_s}\) as a universal \(C\) | 1 | **KILLED** by amplitude |
| Instantaneous finite \(C\) for \(\lvert T_c\rvert\le C g\sqrt{Y D_s}\) on the fixed torus (smooth split) | 1 | Claimed on those branches as existence of \(C\); cutoff-uniformity of the *time* integral is not included |
| \(\int g^2\,dt<\infty\) as an independent payment | 1, 2 | **OPEN**. If assumed, Gate 2 is Beirão da Veiga \((2,3)\). Reformulation, not a new mechanism |
| Homogeneous candidate still OPEN on samples | 3 | Instantaneous pairing only. Not ESS. Not \(\|u\|_3\) |

The written implication on those notes,

\[
(\log\Lambda)'\le\frac{C^2 g^2}{2\nu},
\]

is a **proved implication**, not a paid budget. Independently proving \(\int g^2\) already gives enstrophy control — and is BdV. Lemma Star does not pay it.

---

## When the \(\|u\|_3\) derivation comes back

Do not green it from algebra alone. Return a card with four blocks:

1. **Derivation.** The inequality, the cutoff, the constant, the hidden-norm check. Pass / fail Gate 1 with the exact failure if any.
2. **Scaling.** The precise \((p,q)\) class implied by the time-space condition. Compare to \(\frac2p+\frac3q=1\) and to ESS \(p=\infty,q=3\). State whether it is weaker, equivalent, or stronger.
3. **Reduction.** Whether it rearranges to Kato, energy interpolation, Serrin, ESS, or BdV.
4. **Implication chain.** What must still be finite after the inequality sits. That chain — not the algebra — is the attack surface.

If Gate 1 fails, stop. Do not discuss novelty of a non-estimate.

If Gates 1–3 pass and the budget still assumes a Serrin/ESS/BdV quantity, record **useful reformulation, no new mechanism**.

If Gates 1–3 pass and the budget controls only growth-capable \(L^3\) mass from NSE without that assumption, that is the microscope hit. Still not Clay. Send the implication chain.

---

## Claim line

The three gates are locked.  
The \(\|u\|_3\) derivation is **not back**.  
Existing \(\|\nabla u\|_3\) work is a different object; its time budget, if assumed, is Beirão da Veiga \((2,3)\).  
Generic unaugmented 3-D regularity is not claimed.
