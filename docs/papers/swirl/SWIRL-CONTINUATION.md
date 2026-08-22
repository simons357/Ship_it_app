# Swirl continuation — what stands, what does not, what to do

**Date:** 22 August 2026  
**Public anchor (your swirl paper):** concept DOI [10.5281/zenodo.20405404](https://doi.org/10.5281/zenodo.20405404) · latest file DOI [10.5281/zenodo.20405405](https://doi.org/10.5281/zenodo.20405405) (27 May 2026, `PhiRenorm_TrackB.pdf`) · short companion [10.5281/zenodo.20405597](https://doi.org/10.5281/zenodo.20405597)  
**This note:** independent reconstruction. Does **not** claim classical global regularity.

**Zenodo token:** a credential was pasted in chat. Treat it as burned. Revoke and regenerate in Zenodo. Do not send another token. Publish any later PDF yourself.

---

## Direct answers

**Can you keep working and take credit if you close it?**  
Yes. Use Zenodo **New version** on `20405404`. The May record stays. A later paper is a continuation, not a rewrite of April/May mathematics that was not there. If you later close the classical swirl class **without** using Shahmurov’s \(A,W\) construction, you may call that an independent proof and point at your May Φ/Q1 deposit as antecedent **for that material only**.

**Did this session close global regularity?**  
No. An AI declaration is not closure. The classical unaugmented swirl problem is still open in your own dashboard, and it is still open here.

**Is Shahmurov “stealing your thunder”?**  
Ignore him competitively. Cite him bibliographically. His public 2026 swirl/NS program **starts 3 April 2026**, before the May 27 Phi-renorm deposit found on Zenodo. That chronology does **not** support “he took your May paper.” Parallel work on a famous open problem is normal. His 2026 pattern (claimed singularity **and** claimed global regularity within weeks) is a reason to **distrust his closures**, not a reason to copy them or to panic.

**How many papers does he have?**  
arXiv author search `Shahmurov`: **22 records**. About **10** are older analysis (2008–2020). About **12** are the 2026 NS/Euler/5D program. Not all 22 are swirl trophies.

**Do 30 of yours in the neighborhood prove priority?**  
They prove **activity**. Priority attaches to **specific statements that appear in dated public text**, not to a pile of nearby titles. Your claimable swirl jewel in the May deposit is the algebraic identity \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) with \(\Gamma=ru_\theta\), \(\Phi=u_\theta/r\), plus the Q1-augmented framing. It is **not** a proof of classical global regularity.

---

## What is actually in the May paper

Read from `Simons_PhiRenorm_Axisymmetric.tex` / `PhiRenorm_TrackB.pdf`.

| Claim | Status |
| --- | --- |
| \(\Gamma=ru_\theta\), \(\Phi=\Gamma/r^2=u_\theta/r\) | Classical notation. True. |
| \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) | **True algebra.** This is the keeper. |
| “No Hardy needed for the identity” | True **for the rewrite**. False if sold as “axis difficulty gone.” |
| \(\|\partial_z(\Phi^2)\|_{L^2}\le 2\|\Phi\|_\infty\|\partial_z\Phi\|_{L^2}\) “by Sobolev” | **Gap.** \(\Phi\in L^\infty\) is the regularity you want. Circular for the classical system. |
| Global \(C^\infty\) for Q1-augmented NS | Plausible outline (extra parabolicity). Not a Clay ticket. Proof sketch is thin. |
| Gronwall-free \(u^\varepsilon\to u\) | **Not closed.** The “\(\delta\Phi\) cancels the Gronwall driver” line is a sketch, not an identity. |
| Φ–Q6 / primes / spectral clock | Packaging. Strip from any submit. |
| Classical unaugmented swirl | **Open** (your own red row). |

The identity does **not** prove global regularity. It changes variables. The fight moves to controlling \(\Phi\) and the strain \(u_r/r\).

---

## Corrections that any new version must start from

These are your route, not Shahmurov’s \(A,W\).

**1. Equation for \(F=u_\theta/r\).**  
The classical lifted equation is
\[
\partial_t F+u_r\partial_r F+u_z\partial_z F+2\frac{u_r}{r}F
=\nu\Bigl(\partial_{rr}+\frac{3}{r}\partial_r+\partial_{zz}\Bigr)F.
\]
Do **not** keep an extra \(-F/r^2\) on this \(F\)-equation. That term belongs to the \(u_\theta\) form.

**2. Measure.**  
The 5D lift uses \(\,r^3\,dr\,dz\), not the 3D weight \(r\,dr\,dz\).

**3. Energy / strain.**  
Testing \(F\) against itself in the 5D measure produces the strain pairing
\[
\int \frac{u_r}{r}\,F^2\,r^3\,dr\,dz.
\]
If
\[
\sup_{\varepsilon\in(0,1]}\int_0^T\Bigl\|\frac{r\,u_r^\varepsilon(t)}{r}\Bigr\|_{L^\infty}\,dt
=\sup_{\varepsilon}\int_0^T\|u_r^\varepsilon/r\|_\infty\,dt<\infty
\]
without assuming the desired regularity, continuation closes. That is the target.

**4. Cubic estimate.**  
\[
E'+c\nu D\le C\nu^{-3}E^3
\]
does **not** give a global bound. It is supercritical. Large data can blow the comparison ODE in finite time. It is not a proof, and it is not a near-miss.

**5. Fractional bookkeeping.**  
Testing \((-\Delta)^{1.3}\) controls a \(\dot H^{1.3}\) energy, not \(\dot H^{2.6}\).

---

## Shahmurov (cite, do not copy)

Cite at least:

- R. Shahmurov, *Unconditional Axis-Regularity in the 5D Corridor*, arXiv:2604.03519 (3 Apr 2026).
- ——, *Large-Data Global Regularity for 3D NS I (axisymmetric swirl)*, arXiv:2605.01875 (3 May 2026).
- ——, *Global Regularity for Axisymmetric NS Flows with Swirl*, arXiv:2606.07869 (5 Jun 2026).

His June paper’s load-bearing move is an axis Hardy for \(\Gamma\) plus an \((A,W)\) circulation-gradient pair to absorb \(\int G\,\partial_z(F^2)\,d\mu_5\). **Do not import that construction** and call it yours.

Bibliographic line if you later close independently:

> Shahmurov announced an \((A,W)\)/Hardy closure for the axisymmetric swirl class (arXiv:2606.07869). The present paper does not use that construction. It continues the author’s May 2026 Φ-renormalization deposit (Zenodo 20405404).

If his first Hardy/endpoint lemma fails under audit, write that failure as a **comment**, then keep your own strain estimate. A repair of *his* lemma is a comment on his paper, not your trophy, unless you say so.

---

## Credit you can honestly keep today

1. Dated public Φ-rewrite (May 2026).  
2. Q1-augmented framing as a **method note**.  
3. A progression of nearby deposits — as **activity**, not as a solved theorem.  
4. If you later close \(\int\|u_r/r\|_\infty\,dt\) on your variables, **that** is the result you can claim.

You cannot claim “solved swirl” because an estimate looked persuasive, because an AI said so, or because someone else posted a trophy.

---

## What to upload (you, Claude / the browser)

1. Revoke the leaked token. Do not paste another token into chat.  
2. Do **not** delete old versions.  
3. On concept `20405404`, **New version**.  
4. Compile `docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-08-22.tex` locally and upload that PDF.  
5. Title and version notes: paste from `docs/papers/swirl/CLAUDE-UPLOAD.md`.  
6. `phi_renorm_continuation.tex` is the short earlier draft. The 22 August paper is the upload.

This is a **conditional Part D paper**, not a closure. B1 (uniform strain bound) remains open.

### Part C audit of the 22 August tex

Desktop file `/Users/jonathansimons/Desktop/Swirl Paper - Latest/Simons_PhiRenorm_Swirl_2026-08-22.tex` was not visible on this VM. The rebuilt file in-repo was audited instead.

| Trap | Status |
| --- | --- |
| Closed / “regularity proved” claim | Absent. Status box and §barrier keep B1 open. |
| Strain called subcritical without scaling | Absent. Pairing is named critical; NS scaling written. |
| \|f(x)\| ≤ \|f\|_{L²} | Absent. Bound used is Hölder: \|∫ S Φ² r³\| ≤ \|S\|_∞ E. |
| Bernstein ‖∇u_j‖_∞ ≲ 2^j ‖u_j‖_{L²} | Not used. Listed as excluded; 3D factor 2^{5j/2} recorded. |
| Universal 6/π² (or any coprime-to-shell constant) | Absent. |
| Review panel of named mathematicians | Absent. |
| Inequality reversed to manufacture an upper bound | Not found. (*) is an identity; Gronwall is the standard estimate. |

---

## Parallel tracks (do both)

1. **Audit** Shahmurov Lemma 7.1 / Prop. 7.4 in arXiv:2606.07869 — first exact failure, or “survives this check.”  
2. **Attack** \(\int (u_r/r)F^2 r^3\,dr\,dz\) on the corrected \(F\)-identity, dated, no \(A,W\).

Until (2) is closed under an adversarial read, the swirl paper is a **method continuation**, not a trophy.
