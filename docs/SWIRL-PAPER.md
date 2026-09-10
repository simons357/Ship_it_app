# Swirl, alignment, and the leftover in three-dimensional Navier–Stokes

**A map, not a proof.**

Jonathan Robert Simons  
Prime Field Technologies  
10 September 2026

---

## Abstract

The geometric swirl leftover after Constantin–Fefferman (1993) and Beirão da Veiga–Berselli (2002) is recorded. Alignment of vorticity direction at Lipschitz scale, and then at Hölder exponent \(1/2\), is a theorem as an *if*. The pairs those papers refused — intense, misaligned vorticity — remain. This note names the missing local bound WRITE (6) and does not prove it. A forced finite-time construction with a smooth external force, announced 8 September 2026, addresses a different official statement (Fefferman (C)/(D)) from unforced regularity ((A)/(B)). It is not WRITE (6). A separate note records global regularity for a Ladyzhenskaya / \(p\)-Laplacian augmentation; that is a different equation.

Magazine cut: [`SWIRL-MAGAZINE.md`](SWIRL-MAGAZINE.md).  
Deposit this week: [`SWIRL-DEPOSIT.md`](SWIRL-DEPOSIT.md).  
Classification of the announcement: [`OPENAI-NS-CLAIM.md`](OPENAI-NS-CLAIM.md).

---

## 1. What swirl is, in this note

Let \(u\) be a divergence-free velocity in three dimensions, \(\omega=\nabla\times u\), \(\xi=\omega/|\omega|\) on \(\{\omega\neq 0\}\), and \(\varphi(x,y)\) the angle between \(\xi(x)\) and \(\xi(y)\). Vortex stretching is
\[
\alpha(x)=\mathrm{P.V.}\int D(\hat z,\xi(x),\xi(y))\frac{|\omega(y)|}{|x-y|^3}\,dy,
\qquad
|D|\le C|\sin\varphi|.
\]
The local enstrophy identity on a cutoff \(\phi\) supported in a ball of radius \(r\) has stretching \(\int\alpha|\omega|^2\phi\) on the right and dissipation \(\nu\int|\nabla\omega|^2\phi\) on the left. Pressure is absent in vorticity form.

This is the classical unaugmented equation. No extra stress. No \(\Phi\)-cancel of the axisymmetric tube source. Keep \(1/r^4\) if the class is axisymmetric with swirl; that class is not closed here.

---

## 2. The cut that sits, as an if

**Constantin–Fefferman 1993.** If \(|\sin\varphi(x,y)|\le|x-y|/\rho\) whenever both \(|\omega|\ge\Lambda\), the solution is strong on \([0,T]\).

**Beirão da Veiga–Berselli 2002.** Hölder \(1/2\) suffices: \(|\sin\varphi|\le C|x-y|^{1/2}\).

Mechanism: alignment puts \(|\sin\varphi|\) in the numerator and drops the kernel to \(|z|^{-2}\) (Lipschitz) or \(|z|^{-5/2}\) (Hölder \(1/2\)). That is absorbable into dissipation plus energy. Below \(1/2\) in that argument remains open (Beirão da Veiga 2016).

Call those pairs **Good**. The complementary pairs, still intense, with \(|\sin\varphi|>C_*|x-y|^{1/2}\), are **Bad**. Good pairs are their theorem. Bad pairs are the pairs they refused.

Grujić (2009) localizes the *condition*, not the bad-pair integral. Later papers weight coherence or assume sparseness. Those are still *ifs*.

---

## 3. WRITE (6)

On a parabolic cylinder \(Q_r\), Bad pairs only, both ends in the local ball:
\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]
Here \(A_{\mathrm{bad}}\) is the contribution of local Bad pairs to stretching (absolute value of the kernel, sufficient for a close). Equivalent majorant, up to the constant in \(|D|\le C|\sin\varphi|\):
\[
\iint\!\!\int_{\mathrm{Bad}}
\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}\,\phi
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

Kernel on Bad is still \(|z|^{-3}\). Hardy–Littlewood–Sobolev returns local \(E^3\), the cubic wall. The Hölder cut changes the set, not the exponent. A thin Bad set would save it; assuming thinness is the Good-pair theorem again. Path-cost of \(\nabla\xi\) dies on a sheet or a gap. Morrey: \(W^{1,2}\not\subset C^{0,1/2}\) in three dimensions, so energy does not empty the Bad set.

\(\nu/8\) is a conventional slice of local dissipation, not a sharp constant. Parabolic scaling of the three terms agrees. There is no dimensional obstruction. There is also no proof.

**Aimed leftover: yes. Theorem: no.**

---

## 4. A cylinder still needs more than (6)

Do not merge letters.

- **Lemma C.** Good pairs. An *if*. Localization leaves a cutoff error on the annulus.
- **H1 = WRITE (6).** Bad pairs. Open.
- **H2.** Skin flux \(r^{-1}\iint|u||\omega|^2\). Smallness: Caffarelli–Kohn–Nirenberg 1982, energy level. From \(\int E<\infty\) alone: open.
- **H3.** Exterior Biot–Savart. Crude bound
  \(A_{\mathrm{ext}}\le C r^{-3/2}\int E^{1/2}E_{\mathrm{loc}}\,dt\).
  Not absorbed as \(r\to 0\) from energy. This remainder is why a localization paper exists.

If H1, H2-from-energy (or CKN-small), H3, and the cutoff error all sit, local Serrin (1962) gives smoothness on a smaller cylinder. That implication is not CKN. If (6) sits and H2-from-energy does not, the cylinder is still open. If the cylinder is already CKN-small, (6) was not needed on *that* cylinder.

NRS 1996 rules out Leray backward self-similar profiles. It is not a blanket Type-I theorem.

---

## 5. A forced vortex is not this leftover

Fefferman’s official statement has four alternatives. (A) and (B): unforced, smooth data stay smooth on \(\mathbb{R}^3\) or on the torus. (C) and (D): a smooth force is allowed, and one asks for breakdown.

On 8 September 2026 a finite-time singularity with a smooth external force was announced, pictured as a vortex that spirals inward. If that write-up holds, its slot is (C) or (D). It does not decide (A) or (B). It does not bound WRITE (6). I did not write that construction. I do not claim it.

This note is a map of the unforced geometric leftover. Dates already public on the author’s trail include Zenodo deposits and a GitHub record; Theorem A is dated 5 September 2026. The naming of WRITE (6) in this form is 10 September 2026. The problem those symbols name is 1993.

---

## 6. What this author claims, and what he does not

**Claims.** The map above. A separate write-up of global regularity for Navier–Stokes plus Ladyzhenskaya / \(p\)-Laplacian stress \(Q_1\) at \(\varepsilon>0\), \(\beta\ge 1/2\), on the three-torus (this PDE only; known class; cite Ladyzhenskaya 1968/1969 and Málek–Nečas–Růžička 1996). Inverse-GCD matrix facts posted as Zenodo 22045478, not as the Riemann hypothesis.

**Does not claim.** Ordinary unforced Navier–Stokes. Axisymmetric ordinary NS with swirl as finished. Uniform \(H^1\) as \(\varepsilon\to 0\) for the augmented equation. WRITE (6) as a theorem. The forced construction of 8 September 2026.

Axisymmetric swirl, keeping \(1/r^4\): a localized Hardy inequality does not absorb all data (slow fat swirl). A \(\Phi\)-cancel of the tube source was dropped; it was not the unforced path.

---

## References

1. J. Leray, *Acta Math.* 63 (1934).
2. J. Serrin, *Arch. Rational Mech. Anal.* 9 (1962).
3. L. Caffarelli, R. Kohn, L. Nirenberg, *Comm. Pure Appl. Math.* 35 (1982), 771–831.
4. P. Constantin, C. Fefferman, *Indiana Univ. Math. J.* 42 (1993), 775–789.
5. H. Beirão da Veiga, L. C. Berselli, *Diff. Int. Eq.* 15 (2002), 345–356.
6. J. Nečas, M. Růžička, V. Šverák, *Acta Math.* 176 (1996).
7. L. Escauriaza, G. Seregin, V. Šverák, *Uspekhi Mat. Nauk* 58 (2003).
8. Z. Grujić, *Comm. Math. Phys.* 290 (2009), 861–870.
9. C. L. Fefferman, *Existence and smoothness of the Navier–Stokes equation*, Clay Mathematics Institute.
10. O. A. Ladyzhenskaya, *The Mathematical Theory of Viscous Incompressible Flow*, 1969.
11. J. Málek, J. Nečas, M. Růžička, *Weak and Measure-valued Solutions to Evolutionary PDEs*, 1996.

Desk packet (open leftover, not a close): `docs/UNAUGMENTED-NS-CHAIN.md`, `docs/WRITE_6.md`, `docs/H-SYSTEM.md`, `docs/DREAM-TEAM-H.md`.
