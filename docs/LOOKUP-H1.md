# Lookups for H1 — yes/no

Do not look up a new name. Look up whether a paper *proves* one of the three shapes, or the exact hypothesis on H3.

A hit is a theorem from energy (or from NSE on scale \(r^2/\nu\)) that implies H1, or that absorbs H3 without extra coherence. A miss is another *if*.

---

## 1. Thinness (shape 1)

**Question.** Does any paper *prove*, from the energy class alone, that the Bad-pair set in each \(B_r\) is small enough that HLS turns local \(E^3\) into \(E^2\) or into dissipation?

**Start with.** Grujić, *Nonlinearity* 26 (2013), 1-D sparseness. We already scored: assumes sparseness, does not prove Bad is sparse. Confirm that reading. Then: is there a later paper that *derives* sparseness / small Bad measure from \(\int E<\infty\)?

**Hit.** Yes, with the theorem number and the exact smallness (measure, capacity, or 1-D sparseness) that makes HLS gain.
**Miss.** Still an assumption.

---

## 2. Folds only (shape 2)

**Question.** Is there a published estimate that every *persistent* Bad pair in a cylinder sits in a fold (not a sheet, not a gap), with
\[
\int_{B_{2\rho}}|\nabla\omega|^2\gtrsim\Lambda^2\rho^2
\]
and a Vitali sum that closes H1?

**Start with.** Nothing in the literature pass. Search: vortex-stretching + Vitali + fold / “geometry of vortex lines” / Constantin–Fefferman style pair estimates restricted to folds.

**Hit.** The inequality, the geometry class, and that sheets/gaps are excluded by NSE, not by assumption.
**Miss.** Lemma J on generic fields (already false), or “if it is a fold.”

---

## 3. Dynamics (shape 3)

**Question.** Does NSE *forbid* persistent sheets or gaps on the time scale \(r^2/\nu\)?

**Start with.** Not an imposed waiting time. That refuse still stands. Look for a derived persistence / depletion time for misaligned high-vorticity pairs.

**Hit.** A theorem: on scale \(r^2/\nu\), alternatives to a fold cannot persist, from the equation.
**Miss.** A filter you put on which cylinders to use.

---

## 4. H3 — Grujić 2009 exact hypothesis

**Question.** In Grujić, *CMP* 290 (2009), “Localization and Geometric Depletion of Vortex-Stretching,” what *exactly* controls the exterior / nonlocal stretching? Hölder \(1/2\) of \(\xi\) on the cylinder? A weaker coherence? Something else?

**Hit for us.** If that hypothesis is weaker than Lemma C and still absorbs \(A_{\mathrm{ext}}\) from energy — then H3-from-energy might sit under a named if we do not already have.
**Miss (expected).** Exterior is controlled only under local coherence / local Lemma C. Then our \(r^{-3/2}E^{1/2}E_{\mathrm{loc}}\) bound stays the crude remainder.

---

## 5. No-hit confirmation on the exact integral

**Question.** Quote search, not slogans: does any paper bound
\[
\iint_{\{|\sin\varphi|>C|x-y|^{1/2}\}}\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}
\]
by local dissipation plus \(r^{-2}\iint|\omega|^2\) from energy alone?

**Already scored: no hit.** If you find a paper, send the theorem, not the title. If the hypothesis is still alignment / sparseness / coherence, it is Lemma C’s family, not H1.

---

Do not look up: \(K(t)\), Q-stack, \(\Phi\), leftover-close B42, \(n=64\), A\(\Rightarrow\)B, SND, matrix \(H_N\), Theorem A as ordinary NS.

---

## Scored (10 September 2026)

Arithmetic of the three shapes: [`H1-SHAPES.md`](H1-SHAPES.md).
Not a proof.

**1. Thinness — miss.**
Grujić, *Nonlinearity* 26 (2013) = arXiv:1111.0217.
Theorems 4.1–4.2: no blowup *if* the superlevel set is
linearly \(\delta\)-sparse around each point at a scale
at most the analyticity radius. Sparseness is the
hypothesis. Later \(Z_\alpha\) work (Bradshaw–Farhat–Grujić,
*Arch. Ration. Mech. Anal.* 2019; Grujić–Xu 2024) still
treats sparseness as a class. Faraco-type remarks
(*Nonlinearity* 2022) caution that some of those classes
do not rule out more than energy-level \(L^\infty_t L^2\).
No paper *derives* Bad-pair measure small enough for HLS
gain from \(\int E<\infty\).

**2. Folds only — miss.**
No published estimate that every persistent Bad pair in
a cylinder sits in a fold with
\(\int_{B_{2\rho}}|\nabla\omega|^2\gtrsim\Lambda^2\rho^2\),
sheets and gaps excluded by NSE, and a Vitali sum that
closes H1. CF/BdVB remain alignment ifs.

**3. Dynamics — miss.**
No theorem that NSE forbids persistent sheets or gaps
on the scale \(r^2/\nu\). Averaged filament-stretching
pictures (Dascaliuc–Grujić) are not that theorem.

**4. Grujić 2009 / H3 — miss (expected).**
*Comm. Math. Phys.* 290 (2009), 861–870, localizes the
Hölder-\(1/2\) coherence condition (with GrZh06).
Secondary citations (Grujić 2012 survey) are consistent:
exterior / nonlocal stretching is controlled under that
local if. Not a bound on \(A_{\mathrm{ext}}\) from energy
alone. Packet §11 crude remainder stands.
(PDF sentence not re-quoted this pass; the role of the
paper is not in dispute.)

**5. Exact integral — miss.**
Confirmed. No paper bounds
\[
\iint_{\{|\sin\varphi|>C|x-y|^{1/2}\}}\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}
\]
by local dissipation plus \(r^{-2}\iint|\omega|^2\) from
the energy class alone.

All five are misses. H1 is not under another name.
