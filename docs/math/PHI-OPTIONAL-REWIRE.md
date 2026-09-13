# Phi-cancel optional rewire — does removing it fix H?

**Date:** 2026-08-15  
**Question:** Did algebraic cancel of \(1/r^4\) (Phi-renorm) help short-term but poison Theorem H / the general-\(T^3\) track? Can we drop dependence on the cancel and use T2 Gronwall instead?

---

## Short answer

1. **You cannot falsify the cancel.** Under \(\Gamma=ru_\theta\), \(\Phi=\Gamma/r^2=u_\theta/r\),
   \[
   \frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)
   \]
   is an identity. “Remove the cancellation” means **stop using that rewrite as a load-bearing step**, not make the identity false.

2. **Theorem H was not broken by Phi-renorm.**  
   Theorem H (shell-conditioned commutator / SND-C) is a **Littlewood–Paley / Bony** estimate on \(\mathbb{T}^3\). It never needs \(1/r^4\) or \(\Phi\). Its failure mode is **\(C_*=C_*(\ldots,M,\ldots)\)** — circular enstrophy ceiling — plus spread-regime hypotheses. That is independent of Track B.

3. **What Phi *did* mess with (architecturally):**
   - **Theorem C** (Gronwall-free \(u^\eps\to u\)) in the merged NS paper is **axisymmetric-only** and uses Phi to kill the Gronwall driver. That success was then treated as if Gronwall were solved for the **whole** program.
   - **Phi–Q6 correspondence** (§5 of Track B) glued a clean axisymmetric identity to the prime-lattice / \(H_N\) / Bridge story. That glue is optional packaging — and it’s where “H problems” feel connected to swirl even though the operators differ.
   - So: cool cancel → false confidence that spectral **H** was on the same clean footing.

4. **Yes, try the rewire:** keep Phi as an **optional Track B rewrite**; restore **Hardy** for classical axisymmetric energy if you refuse Phi; put **T2** in charge of shell-flux Gronwall for the SND / Theorem H track.

---

## What each piece actually does

| Piece | Job | Scope |
| --- | --- | --- |
| Phi cancel | Rewrite axis swirl singularity | Axisymmetric-with-swirl only |
| Hardy \(r^{-4}\) | Bound the singularity **without** rewriting | Same class, classical variables \(\Gamma\) |
| Theorem C Gronwall-free | Convergence of Q1 approximants | Uses Phi; **not** general \(T^3\) |
| **T2** | Shell flux \(\Phi_j\) + Gronwall on shell fractions \(a_j\) | Spectral / SND track (`20552080`) |
| **Theorem H** | Pointwise-in-shell commutator bound (SND-C) | General LP on \(T^3\); needs \(M\) fix |

T2’s own paper already says T2 ⇔ SND (structural) and that Gronwall is SND in differential form — that is the “equation for Gronwall” you remember. It does **not** need Phi cancel.

---

## Rewire proposal (Phi-optional)

### Track B′ — axisymmetric (choose one tool, don’t mix stories)

**Option B1 (keep jewel):** Phi cancel + publish as method note. No Hardy. No claim on Theorem H.

**Option B2 (your experiment):** Refuse Phi rewrite. Keep \(\Gamma=ru_\theta\). Close axis estimates with a **Hardy** (or weighted Sobolev) bound of the form
\[
\int r^{-4}|f|^2\,r\,dr\,dz \le C\int |\partial_r f|^2\,r\,dr\,dz
\]
(with the usual caveats near \(r=0\)). Accept that this is harder / more classical. Use **ordinary Gronwall** or a **T2-style** differential inequality only if you have shell structure in cylindrical coordinates — do not pretend B1’s Gronwall-free rate transfers.

### Track H′ — general \(T^3\) / SND (no Phi at all)

1. **Delete** any dependency edge: Phi-renorm → Theorem H / Main Theorem.  
2. Shell flux: use **T2** bound
   \[
   |\Phi_j(t)|\le C_\varphi\,2^{-0.8j}\,X^{1/2}\mathcal{D}^{1/2}
   \]
   and the T2 Gronwall ODE for \(h=\|a-\mu\|_{\ell^1}\).  
3. Theorem H / SND-C: attack **without** \(X\le M\) from the conclusion — or demote H to “conditional on absorbing ball.”  
4. Q6: keep as a **separate** damping hypothesis if used; do not identify with \(\Phi=u_\theta/r\).

### What we expect after rewire

| Problem | Fixed by dropping Phi dependency? |
| --- | --- |
| Theorem H circular \(M\) | **No** — still open; wrong tool |
| False “Gronwall solved everywhere” | **Yes** — scope restored |
| Phi–Q6 / \(H_N\) confusion | **Yes** — cut the correspondence as load-bearing |
| Axisymmetric \(1/r^4\) | Still need **either** Phi **or** Hardy |
| Clay Statement (B) | Still not solved |

---

## Minimal “no-cancel” energy sketch (axisymmetric)

Keep the classical swirl-vorticity term \(\frac1{r^4}\partial_z(\Gamma^2)\). After testing against \(\eta=\omega_\theta/r\) (schematic):

\[
\frac{d}{dt}\|\eta\|_{L^2}^2
+\nu\|\nabla\eta\|^2
\le C\Big\|\frac1{r^2}\partial_z(\Gamma^2)\Big\|_{L^2}\|\eta\|_{L^2}
+\text{(transport)}.
\]

Without Phi, bound the right-hand side by Hardy / weights on \(\Gamma\), then Gronwall:

\[
\frac{d}{dt}E \le C(t)\,E + F_{\mathrm{data}}(t),
\quad
E(t)\le E(0)\exp\Big(\int_0^t C\Big)+\cdots.
\]

That exponential is exactly the **Gronwall wall** Phi was invented to bypass for Q1 convergence. Replacing it for the **spectral** program is **T2** (shell fractions), not Phi.

For spectral enstrophy \(X=\|\nabla u\|_{L^2}^2\) on \(T^3\), prefer T2’s form (from `T2_CONDITIONAL_CLOSURE.tex`):

\[
\frac{d}{dt}h \le -\alpha h + \beta_N(t),\qquad
\alpha=2\nu^2\cdot 4^{1/\rho_0}\cdot\rho_0,\quad
\beta_N\sim \mathcal{D}^{1/2}/X^{1/2}.
\]

That equation does not mention \(r\) or \(\Phi\).

---

## Verdict on the experiment

| Try | Worth it? |
| --- | --- |
| Stop importing Phi into Theorem H / Main Theorem | **Yes — do this** |
| Stop treating Phi–Q6 as a theorem | **Yes** |
| Re-prove axisymmetric estimates with Hardy instead of Phi | Optional research; expect harder estimates; won’t fix H’s \(M\) bug |
| Use T2 as the Gronwall equation for SND | **Yes — already your spectral Gronwall** |
| Literally delete \(\partial_z(\Phi^2)=\frac1{r^4}\partial_z(\Gamma^2)\) from math | **Impossible / pointless** — identity stays true |

**Recommendation:** Treat Phi-renorm as a **standalone Track B credit paper** (keep the cancel). For the SND / Theorem H panel, run a **Phi-free proof graph**: T2 + Ring + (fixed) SND-C, no axis cancel, no Q6 correspondence.

---

## Next concrete edits (if you want code/tex follow-through)

1. Add a dependency graph file marking Phi ↛ H.  
2. Draft `docs/math/PHI-FREE-SND-CHAIN.md` listing only T2, Ring, SND definitions from `20518057` / `20552080`.  
3. Leave Track B Zenodo records as-is (jewel intact).

No Clay claim either way.
