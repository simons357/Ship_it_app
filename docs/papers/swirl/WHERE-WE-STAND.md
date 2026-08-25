# Where we stand — swirl and Domain Architect

**Date:** 25 August 2026  
**For:** Jonathan Simons  
**Plain English.** This is a status note, not a proof.

---

## Did we learn anything new?

Yes. Not a new estimate that closes swirl. A **clear map** of what you already had, what was packaging, and what is still the fight.

Before, several stories were in one pile: the axis identity, the hyperviscous ε-system, primes / Q6 / CMB / Kabbalah, Domain Architect, and “did we solve it?” Those are now split.

What is new as *clarity*, not as a theorem:

- Two books. DA is not a fluids solver. Swirl is not DA.
- The May “universal geometry” essay is analogy. It is not a swirl proof.
- The 22 August paper already proves some things and leaves the hard thing open.
- Live DA fails an honest test: it will invent a PD controller if you ask it to “prove swirl regular.”
- The remaining obstruction has a name: control of \(u^r/r\), not the \(1/r^4\) writing of the centrifugal source.

---

## Keep the algebraic rewrite?

**Yes. Keep it.** Do not throw away Phi-renormalization.

What it does: you stop fighting \(\frac1{r^4}\partial_z(\Gamma^2)\) with Hardy inequalities. You write the same source as \(\partial_z(\Phi^2)\). That cancellation is real. It stays in the paper.

What it does **not** do: it does not make the axis problem disappear. After the rewrite, the intensive field still has stretching \(2(u^r/r)\Phi\). In the energy, that shows up as the pairing with \(u^r/r\). That term is **not** algebraically removed. Do not advertise “the singularity was never real” as a closed proof.

So: **with** the algebraic rewrite of the centrifugal source. **Without** pretending that rewrite is the whole swirl problem. **Without** the cosmic / prime / Kabbalah overlay in any submit.

---

## Is there a clear path to NS / swirl?

There is a clear **research path**. There is not a clear **finished proof**.

Classical unaugmented axisymmetric Navier–Stokes **with swirl** is still open. An AI saying it is closed does not close it. The ε-hyperviscous system being smooth is a different theorem. Do not cash that in as Clay or as unaugmented regularity.

The path, in order:

1. Keep \(\Gamma = r u_\theta\), \(\Phi = u_\theta/r\), and the identity.
2. Keep the circulation maximum principle. Remember it does not control \(u^r\).
3. Keep the correct \(\Phi\)-equation (no extra \(-\Phi/r^2\)) and the \(r^3\) energy bookkeeping.
4. Put every new page on this question: can you bound \(\int \|u^r/r\|_\infty\,dt\) (or the pairing it produces) **without** assuming the regularity you want, and **without** copying someone else’s \((A,W)\) / axis-Hardy gadget?
5. Do not use the cubic energy comparison as a proof. It is supercritical. Large data can blow up the comparison ODE.
6. Strip primes, Q6, spectral clock, CMB, Saturn, Tikkun from any version you submit.
7. Cite parallel 2026 work. Do not copy it. Do not panic about it.

If step 4 closes, you have a continuation theorem that can become global regularity. Until step 4 closes, the swirl paper is a **method continuation**: identity, maximum principle, energy identity, honest strain section, open status box.

---

## Where Domain Architect fits

DA can *look at* the swirl book. It must not glue swirl \(\Phi\) to gravity \(\Phi\) or to DA’s output \(\Phi\).

Today the desktop lab does not understand the PDE. It correctly refuses to treat \(\Phi\) as gravity. It incorrectly synthesizes a control loop if you ask for global smoothness. That is a software bug (fail-closed inverse design), not a fluids result.

Fixing DA and closing swirl are **two jobs**. Do not wait for DA to solve NS. Do not wait for NS to justify DA.

---

## What to do next (swirl)

Work the strain pairing on the corrected \(\Phi\)-equation in \(r^3\,dr\,dz\). Write the next estimate so it **stops at a named line** if it fails, the way the 22 August strain section already does. Compile that paper. Upload as a Zenodo **new version** on the existing concept, yourself, no tokens in chat.

Leave the geometry essay on the shelf as a personal hypothesis. It does not help close \(u^r/r\).

---

## Paper2 (periodic 3D, SND/GNC) is a different book

The repaired August 1 manuscript is filed at
[`docs/papers/ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`](../ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex).

It is **full 3D Navier–Stokes on the torus**, not axisymmetric swirl. SND means the energy is not stuck in one dyadic shell. The thin proved part is a Weyl perturbation fact: *if* a frozen spectral gap and a quantitative operator-norm closeness both hold, the evolving gap stays. The physics arrow — that unaugmented Leray–Hopf actually stays close on the simplex — is **open**. A false gcd identity was removed. “T2 Closed Gronwall” is withdrawn. Classical 3D regularity is not claimed.

Same leftover *shape* as swirl (an energy bound does not give the smallness you need). **Not the same leftover.** Do not feed Paper2’s GCD matrix \(H_N\) into the swirl strain term, and do not feed swirl \(\Phi=u_\theta/r\) into Paper2.

---

## One sentence

You keep the Phi rewrite; you do not keep the universal-geometry story as mathematics; the swirl problem is now cleanly named as control of \(u^r/r\); that line is still open. Paper2 is a separate conditional spectral framework on \(\mathbb{T}^3\); its open simplex is not a swirl estimate.
