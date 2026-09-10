# H1 tube scores — first computation

Dated 10 September 2026. Snapshot integrals on
\(n=48\). **Not a proof. H1 is not proved.
NS is not solved.**

SoT: [`H1-SOT.md`](H1-SOT.md).
Probe: `python3 scripts/h1_one_cylinder.py`

Two writings stay split. This is not
\(A_{\mathrm{bad}}\). This is not \(\mathcal R_\star\).
This is not matrix \(H_N\). The Ring Lemma
direction bound is not used.

Waiting is not scored on a snapshot. Do not
cash an imposed \(\tau\). One tube is not
\(C(\rho,L)\).

---

## What was asked

\(J\) and thinness on one explicit tube
(ABC / strained vortex), then whether \(J\)
stays bounded as amplitude grows.

\[
J_{\mathrm{ec}}=\int_{E_c}|\nabla\xi|^2|\omega|\,dx,
\qquad
E_c=\{|\omega|\ge 0.35\|\omega\|_\infty\}.
\]

Closing H1 would need
\(\|(\xi\cdot\nabla u\cdot\xi)_+\|_{L^\infty(E_c)}\)
independent of how large \(|\omega|\) is.
That failed on ABC. It held on Burgers by
imposed strain, which is not the estimate.

---

## ABC (not a tube)

Beltrami, \(\omega=u\). \(\xi\) does not change
with amplitude \(A\). Residual
\(\|\omega-u\|_2^2\sim 10^{-27}\).

| \(A\) | \(J_{\mathrm{ec}}\) | \(J/X\) | \(\|(\xi\cdot\nabla u\cdot\xi)_+\|_\infty\) | \(J/A\) |
| ---: | ---: | ---: | ---: | ---: |
| 0.5 | \(1.47\times 10^2\) | 0.792 | 0.653 | 295 |
| 1 | \(2.95\times 10^2\) | 0.396 | 1.307 | 295 |
| 2 | \(5.90\times 10^2\) | 0.198 | 2.613 | 295 |
| 4 | \(1.18\times 10^3\) | 0.099 | 5.226 | 295 |
| 8 | \(2.36\times 10^3\) | 0.050 | 10.45 | 295 |

\(J\sim A\), not \(O(1)\). \(J/X\sim 1/A\):
folds of \(\xi\) do not blow like enstrophy.
The stretch rate grows like \(A\). BKM on
this field fails. Kill of this packaging
on ABC, not of NS. Do not cash 295 or
1.307 as \(C_0\).

---

## Burgers (strained vortex)

\(\xi=\hat e_z\) wherever \(\omega\neq 0\).
\(J_{\mathrm{ec}}=0\). Stretch rate \(=\gamma=1\),
independent of circulation \(\Gamma\).
Core \(\rho=2\sqrt{\nu/\gamma}\). Waiting
\(\rho^2/\nu=4\) is locked to the imposed
strain. Swirl-core thinness
\(\rho^2\int_{\mathrm{core}}|\omega|^2\big/\int_{\mathrm{core}}|u_{\mathrm{swirl}}|^2\simeq 1.59\),
independent of \(\Gamma\).

Strain is not Biot–Savart of the tube.
Energy of \(\gamma z\) on \(\mathbb R^3\) is
not a tube quantity; the ratio uses swirl
only. Do not cash Burgers as H1.

---

## Gaussian pair (self-induced)

Opposite tubes, mean \(\omega=0\), velocity
from Biot–Savart on \(\mathbb T^3\). Stretch
rate \(=0\): a straight tube has no axial
strain from its own field.

Fixed \(\rho=0.40\), amplitude sweep:
\(\rho^2\int_{\mathrm{core}}|\omega|^2\big/E_{\mathrm{core}}\simeq 1.48\).
\(J_{\mathrm{ec}}\) still tracks \(A\) (the
nodal sheet between \(+\) and \(-\) is a
fold). \(J/X\) falls.

Fixed circulation, \(\rho\) down:
thinness stays \(O(1)\) (1.51 at
\(\rho=0.28\), 1.30 at \(\rho=0.60\)).
From Biot–Savart, not a picture. A sample
of an approximately low-pass field, not
Lemma P1 ([`H1-P1.md`](H1-P1.md)). Cutoff:
[`H1-P1-LOC.md`](H1-P1-LOC.md). Not H1.
Thinness without stretching is not the
close.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| H1t_abc_j_tracks_amp | **pass** | ABC \(J\sim A\), not enstrophy |
| H1t_abc_stretch_tracks_amp | **fail** | stretch rate independent of \(A\) |
| H1t_abc_j_not_enstrophy | **fail** | \(J\) blows like \(X\) |
| H1t_burgers_aligned | **pass** | \(J=0\), stretch \(=\gamma\) |
| H1t_burgers_not_h1 | **fail** | Burgers closes H1 |
| H1t_gaussian_thinness | **pass** | \(\rho^2\int|\omega|^2\lesssim E_{\mathrm{core}}\) |
| H1t_gaussian_self_stretch | **pass** | self-stretch \(\ll\) ABC |
| H1t_not_a_close | **fail** | these tubes close H1 |
| H1t_not_gcd | **fail** | H1 is \(H_M[a]\) |
| H1t_ring_not_proved | **fail** | Ring Lemma proved |

H1 remains open. Uniform triadic bound
remains open. NS not solved.
