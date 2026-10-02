# Notation glossary

Single card for symbols that appear on the proof journey. Full exposition: [`../ns-review/PROOF-CHAIN-CLEAN.md`](../ns-review/PROOF-CHAIN-CLEAN.md). Collision audit: [`../domain-architect/04-NOTATION-COLLISIONS.md`](../domain-architect/04-NOTATION-COLLISIONS.md).

---

## \(\mathbb{T}^3\) / Lemma★ trunk

| Symbol | Meaning |
| --- | --- |
| \(v\), \(u\) | Smooth mean-zero divergence-free velocity (shape field / strong solution) |
| \(P\), \(\mathbb{P}\) | Leray projector |
| \(A=-P\Delta\) | Stokes operator; \(\lambda_k=\lvert k\rvert^2\) |
| \(B(v,v)=P[(v\cdot\nabla)v]\) | Projected bilinear form |
| \(E=\|v\|_2^2\) | Kinetic energy |
| \(X=\|A^{1/2}v\|_2^2\) | Enstrophy-scale moment |
| \(Y=\|Av\|_2^2\), \(Z=\|A^{3/2}v\|_2^2\) | Higher Stokes moments |
| \(\Lambda=Y/X\) | Spectral scale (enstrophy-weighted mean eigenvalue) |
| \(D_s=Z-\Lambda Y\) | Spectral spread (\(\ge 0\)) |
| \(N=-\langle B(v,v),Av\rangle\), \(M=-\langle AB(v,v),Av\rangle\) | Cascade moments |
| \(T_c=M-\Lambda N\) | Centered cascade / stretching |
| \((T_c)_+\) | \(\max(T_c,0)\) — upward stretch only |
| \(\mathcal{R}_\star=(T_c)_+^2/(D_s E Y)\) | Lemma★ shape quotient |
| \(\nu\) | Viscosity |

**Identity:** \(\Lambda'=2(T_c-\nu D_s)/X\) along a strong solution.

**Open estimate (trunk):** a product-class bound on \(T_c\) (or equivalent structure feeding Young in \(\nu\)) — historically probed via Bony high×high input channels in the five-lane diagnostics.

---

## Φ-renorm branch

| Symbol | Meaning |
| --- | --- |
| \(\Gamma=r u_\theta\) | Extensive swirl |
| \(\Phi=\Gamma/r^2=u_\theta/r\) | Intensive swirl (**not** FRA output \(\Phi\)) |
| \(u^r,u^\theta,u^z\) | Cylindrical velocity components |
| \(\dot H^{1.3}\) | Dissipation label after Aug 22 relabel (was mis-written \(\dot H^{2.6}\) as energy norm) |

**KEEP identity:** \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\).

**Open estimate (branch):** \(\sup_\eps\int_0^T\|u^r_\eps/r\|_{L^\infty}\,\mathrm{d}t<\infty\).

---

## SND / Ring texture

| Symbol / phrase | Meaning |
| --- | --- |
| SND | Spectral Non-Dispersal — **hypothesis** for unaugmented NS in KEEP framing |
| Ring Lemma | Band-limited vorticity-direction geometry |
| Shell flux / \(J\) | Shell bookkeeping — **not** the same object as \(T_c\) |
| T2 under SND | Conditional shell-flux Gronwall (KEEP `22050965`) |

---

## Q6 / DA (adjacent)

| Symbol / phrase | Meaning |
| --- | --- |
| \(Q_N\) / Q6 | Inverse-GCD operator note (KEEP `22050962`) |
| FRA / Domain Architect | Functional Role Analysis — model-audit methods; repo `docs/domain-architect/` |
| FRA \(\Phi\) | Output map symbol in DA notes — **collision** with swirl \(\Phi\); never identify |

---

## Cleanup pointers

1. Prefer KEEP Φ-algebra DOIs over older TeX still carrying \(\dot H^{2.6}\) as if it were the energy norm.
2. Journey / campaign faces label open needs as the analytic object — not FAILED banners.
3. Do not glue swirl \(\Phi\), FRA \(\Phi\), and spectral programmes into one symbol.
4. Alignment table: §8 of [`PROOF-CHAIN-CLEAN.md`](../ns-review/PROOF-CHAIN-CLEAN.md).
