# DA-NS Sprint 01 — Phase, symmetry, zeros, frozen charge

7 September 2026 (filed 28 September 2026).
Classical, unforced, unaugmented 3-D incompressible Navier–Stokes on \(\mathbb T^3\).
**Exact finite-Galerkin algebra and falsification results. No unconditional regularity proof.**
Fixed endpoint remains **DA-NS-2**. NS is not solved. RH is not solved.

Working code: `scripts/ns_attacks/{fourier,galerkin,phase_network,symmetry_2d3c,frozen_charge,icosahedral,reset_safe}.py`.
Machine: [`results/sprint01_phase_charge.json`](../results/sprint01_phase_charge.json).

```bash
PYTHONPATH=scripts python3 -m unittest \
  tests.test_centered_flux_identity \
  tests.test_full_helical_flow \
  tests.test_helical_phase_network \
  tests.test_phase_rotation_dynamics \
  tests.test_frozen_log_charge \
  tests.test_icosahedral_core \
  tests.test_reset_safe_network_charge -q
PYTHONPATH=scripts python3 scripts/run_sprint01_phase_charge.py
```

---

## 1. Executive verdict

The exact full-flow phase algebra survives. The dynamic interpretation does not.

The one-channel real-coupling truncation has exact \(0/\pi\) invariant rays. That signed channel is **not** invariant in the actual vector Galerkin systems. The tracked raw monomial \(W\) can still stay real because the chosen data lie in an exact coplanar 2D3C half-turn fixed-point class. Positive orientation can end through a modal-amplitude zero or through a zero of the moving radial multiplier \(C(\Lambda)\). That defeats unconditional automatic dephasing. It does not prove dangerous locking in a genuinely three-dimensional network.

The two-door lock/rotate dichotomy is retired. The admissible partition is hierarchical:

1. capacity, radial or geometric degeneracy;
2. exact regular invariant geometry (demonstrated lock is a globally regular 2D3C sector);
3. nondegenerate rotation, tracked by the raw angular current \(\mathcal J^W\) without dividing at zeros;
4. nonrotating paid charge, summed on the connected heterochiral network before positive parts.

The helical decomposition agrees with undecomposed centered drift through the radius-two cube (4,272 signed channels). The frozen logarithmic charge has exact leading-order core and narrow-band viscous cancellations at \(\theta=1\). It does **not** close the fixed-\(\theta<1\) endpoint: \((1-\theta)\nu\mathcal D_s/Y\) survives, and a bounded charge range does not control positive variation after amplitude-zero resets.

DA-NS-2 remains open.

---

## 2. Unchanged closure endpoint

\[
X=|A^{1/2}u|_2^2,\quad
Y=|Au|_2^2,\quad
Z=|A^{3/2}u|_2^2,\quad
\Lambda=Y/X,
\]

\[
\mathfrak T_c=\mathcal M-\Lambda\mathcal N,\qquad
\mathcal D_s=Z-\Lambda Y\ge 0,
\]

\[
(\log\Lambda)'=\frac{2}{Y}\bigl(\mathfrak T_c-\nu\mathcal D_s\bigr).
\]

For \(0\le\theta<1\),

\[
K_{\min,\theta}^{(n)}
=\frac{\bigl[\mathfrak T_c^{(n)}-\theta\nu\mathcal D_s^{(n)}\bigr]_+}{Y^{(n)}}.
\]

**DA-NS-2.** \(\sup_n\int_0^T K_{\min,\theta}^{(n)}\,dt\le F(\nu,T,u_0)<\infty\) without a continuation norm. Phase variables are useful only if they prove this bound rather than rename it.

In this implementation the Fourier convention is \(u=\sum_k \widehat u_k e^{ik\cdot x}\) on \([0,2\pi]^3\), \(\langle u,v\rangle=\sum_k \widehat u_k\cdot\overline{\widehat v_k}\), and \(B=-P(u\cdot\nabla u)\), so that the log-barycenter identity has the displayed sign.

---

## 3. Exact phase-resolved helical network

Helical frame: \(ik\times h_s(k)=s|k|h_s(k)\), with \(h_s(-k)=\overline{h_s(k)}\) in the default gauge, so a real field has \(a^s(-k)=\overline{a^s(k)}\).

Geometric triad \(\Delta=(k,p,q)\) with \(k+p+q=0\). Signed curl eigenvalues \(a=s_k|k|\), \(b=s_p|p|\), \(c=s_q|q|\). The \(k\)-equation of a real field is fed by \((-p,-q)\), so

\[
g_{\Delta,\sigma}
=-\bigl(h_{-p}^{s_p}\times h_{-q}^{s_q}\bigr)\cdot\overline{h_k^{s_k}},
\qquad
W=g\,\overline{a_k^{s_k}a_p^{s_p}a_q^{s_q}},
\qquad
\Theta=\operatorname{Re}W.
\]

The conjugation is essential. Then

\[
C=-(a-b)(b-c)(c-a)\bigl(a^2+b^2+c^2+ab+bc+ca-\Lambda\bigr),
\qquad
\mathfrak T_{c,\Delta,\sigma}=2C\,\Theta,
\]

\[
\boxed{\mathfrak T_c=\sum_{\Delta,\sigma}\mathcal A_{\Delta,\sigma}\cos\Psi_{\Delta,\sigma}}
\tag{3.1}
\]

with \(\mathcal Z=CW\), \(\mathcal A=2|\mathcal Z|\), \(\Psi=\arg\mathcal Z\). A sign change of the real factor \(C(\Lambda)\) reverses \(\Psi\) without rotating the raw interaction phase \(\psi=\arg W\).

Reconstruction on random symmetric cubes (numpy Generator seed 0):

| Field | Signed channels | Direct \(\mathfrak T_c\) | Phase sum | Recon error |
|---|---:|---:|---:|---:|
| Random cube, radius 1 | 176 | matches | matches | \(<10^{-12}\) |
| Random cube, radius 2 | 4,272 | matches | matches | \(<10^{-10}\) |
| Single real six-mode triad | 8 | matches | matches | \(<10^{-12}\) |

These computations certify the finite algebra. They do not establish a cutoff-uniform analytic bound. The 7 September 2026 exhibit-B/C floats were a different draw; the channel counts 176 and 4,272 are the same.

---

## 4. Projected locked rays versus the exact vector symmetry lock

The one-channel ODE obtained by projecting a single geometric triad onto one helicity-sign channel has exact \(0/\pi\) rays, and viscosity contributes no direct rotation. That ODE is **not** an invariant single-helicity subsystem of vector Galerkin NS. Leakage of the tracked signed-helicity subspace is large.

**Exact symmetry lemma.** Let \(n=(0,1,-1)/\sqrt2\), \(P=n^\perp=\{k:k_y=k_z\}\), and \(R=2nn^\top-I\). The real linear space

\[
\mathcal S=\bigl\{u:\operatorname{supp}\widehat u\subset P,\ \widehat u_k=R\overline{\widehat u_k}\bigr\}
\]

is invariant for NS and every tested symmetric Galerkin cube. Equivalently: 2D3C fields \(u=v+\vartheta n\) with \(\partial_n u=0\) and the extra half-turn parity. In the planar helical gauge \(h_s(k)=(n\times\widehat k+is n)/\sqrt2\), every helical amplitude on \(\mathcal S\) is purely imaginary and every planar \(W\) is real, so \(\psi\in\{0,\pi\}\) away from zeros. This is an exact symmetry proof. It is a separately regular 2D3C sector, not a dangerous genuinely 3-D locked example.

Seed triad: \(k=(1,0,0)\), \(p=(0,1,1)\), \(q=(-1,-1,-1)\), \(\sigma=(+,+,-)\).

Finite-Galerkin diagnostics in this repo (qualitative; not the 7 September table floats):

- Six-mode vector Galerkin and the complete radius-one cube, started in \(\mathcal S\): raw phase stays on \(\{0,\pi\}\) to \(\sim 10^{-10}\), off-plane energy stays at 0, tracked signed-helicity leaks, other cube modes fill.
- A random radius-one cube rotates: raw phase leaves the real rays and off-plane energy is positive.
- A transverse second triad in a different plane, sharing \(k=(1,0,0)\) with \(r=(0,1,0)\), \(s=(-1,-1,0)\), produces a nonzero raw angular current \(\mathcal J^W=\operatorname{Im}(\overline W\dot W)\). Rank-three coupling can generate rotation. No uniform all-data escape constant is claimed.

Two different sign changes must never be conflated: a modal-product zero (argument undefined at the root) versus a radial zero \(C(\Lambda)=0\) with \(W\neq 0\).

---

## 5. Phase-twin obstruction

The same \((++-)\) triad, with one amplitude multiplied by \(-1\), yields two fields with identical \(X,Y,Z,\Lambda,\mathcal D_s\) and opposite \(\mathfrak T_c\). Intensities and quadratic spectral moments cannot see the dangerous sign.

---

## 6. Q1 is a different PDE

The earlier adaptive coherence-viscosity \(Q_1[u]=-\varepsilon^\alpha|\nabla u|^\beta\Delta u\) changes the equation. No uniform \(\varepsilon\to 0\) de-augmentation theorem is claimed. Classical unaugmented NS is the only object on this page.

---

## 7. Heterochiral phase-to-charge bridge

For a real six-mode heterochiral channel with equal-helicity radii \(i,j\) and odd-helicity radius \(o\),

\[
H_{ij|o}=i^2+j^2+o^2+ij-o(i+j),\qquad
R_\Lambda(i,j;o)=\frac{(i+o)(j+o)(H_{ij|o}-\Lambda)}{2o},
\]

\[
\boxed{\mathfrak T_{c,\Delta}^{\mathrm{het}}=R_\Lambda\,Q_{\mathrm{abs},\Delta}}.
\]

\(Q_{\mathrm{abs}}\) is nonlinear production of \(H_a=\sum_{k,s}|k|\,|a_k^s|^2\), not conserved signed helicity. Homochiral channels have \(Q_{\mathrm{abs}}=0\) and still carry a Vandermonde centered coefficient. Certified channel-by-channel on the tests above. Signed physical-helicity production cancels on every channel in the full-network sum.

---

## 8. Frozen logarithmic charge — exact, then poisoned

\[
\mathcal C_e=\log\frac{X}{\kappa_e H_a},\qquad
\mathcal C_e'=\frac{2\mathcal N}{X}-\frac{2Q_a}{H_a}+2\nu\Bigl(\frac{D_a}{H_a}-\Lambda\Bigr).
\]

\[
G_\theta=\frac{\mathfrak T_c-\theta\nu\mathcal D_s}{Y}
=\mathcal C_e'+\mathcal R_{\mathrm{lock}}+\nu\mathcal R_{\nu,\theta},
\]

\[
\mathcal R_{\nu,\theta}=\mathcal R_{\nu,1}+(1-\theta)\frac{\mathcal D_s}{Y}.
\]

On a spectrum supported in radii \([a,b]\),

\[
\lvert\mathcal R_{\nu,1}\rvert\le\bigl[(b/a)^3-1\bigr]\mathcal D_s/Y.
\]

Verified on vector Galerkin snapshots (\(\sim 10^{-12}\)) and on 10,000 random positive spectra. Finite-difference \(\mathcal C_e'\) matches the identity on a locked seed.

**Fixed-\(\theta\) strike.** Integer triad \((k,p,q)=((-12,-11,-1),(0,11,12),(12,0,-11))\), radii \(\sqrt{266},\sqrt{265},\sqrt{265}\) (gap \(\approx 3.07\times 10^{-2}\)), locked \((++-)\) ray, \(\nu=7.06\) just above \(\mathfrak T_c/\mathcal D_s\). For every listed \(\theta\in\{0,0.5,0.99,0.999\}\), \(G_\theta>0\) while \(\mathcal C_e'<0\). Positive DA occupation can occur while the proposed charge decreases. A bounded range for \(\mathcal C_e\) controls net change, not \(\int[\mathcal C_e']_+\,dt\). Standalone frozen-charge route to DA-NS-2 is rejected.

---

## 9. Raw monomial, not the oriented product

Dynamic variable: \(W\), not \(\mathcal Z=C(\Lambda)W\). Nonsingular current \(\mathcal J^W=\operatorname{Im}(\overline W\dot W)\). At \(W=0\), \(\arg W\) is undefined and \(\mathcal J^W=0\) algebraically; that zero does not prove tangency. Viscosity contributes a real decay factor to \(W\) and no direct rotation.

**Centered icosahedron.** Twelve golden-ratio vertices in \(\mathbb Q(\varphi)\) have zero center, common radius \(R^2=2+\varphi\), and isotropic second moment \(\sum v\otimes v=4R^2 I_3\). Pair sums leave the shell. Fivefold symmetry is not a \(\mathbb Z^3\) orbit. Not a torus Fourier subsystem.

**Rational shell** \(S_{3,2}\), \(|k|^2=13\). One-shell identities: \(\Lambda(0)=K\), \(\mathfrak T_c(0)=\mathcal D_s(0)=0\). Every nonzero active quadratic output is outward, so \(\mathfrak T_c'(0)>0\) and \(\mathcal D_s''(0)>0\). Finite-difference Taylor check on the Euler Galerkin flow through \(S+S\). Core-to-halo reset test; not a long-time bound.

---

## 10–15. Reset-safe gate and Sprint 02 disposition

The four-door gate (collapse / exact regular geometry / raw rotation / net paid charge) is a research specification, not a theorem. Even a successful net-charge inequality would still need reset summability and a remedy for (8.5).

Sprint 02 already killed the charge-only form of (10.1). Exact two-triad witness:

\[
k=(1,0,0),\; p=(0,1,1),\; q=(-1,-1,-1),\; r=(0,1,0),\; s=(-1,-1,0),
\]

rank three, \(Q_{a,\Gamma}=0\), \(\mathfrak T_{c,\Gamma}^{\mathrm{het}}>0\). Identity \(\mathfrak T_c^{\mathrm{het}}=2\kappa^3 Q_a+\rho\) with \(\rho\) structurally necessary. Code: `ns_attacks.reset_safe`. Next obligation is the Joint Gap–Charge Epoch Budget, targeting \(\theta<1\) directly. That budget is not proved here.

---

## Honesty lock

- Finite symmetric Fourier–Galerkin only.
- No Serrin/BKM last line.
- No \(\int(\mathcal N/X)_+\,dt\), no \(\int\mathcal D_s/Y\,dt\), no \(\sup\Lambda\) as a close.
- Q1, Φ-renorm, SND, Lemma★ unrestricted box: not this page.
- Clay Mathematics Institute still lists Navier–Stokes as unsolved.
