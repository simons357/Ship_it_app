# DA swirl: first probe of four open mechanisms

**Jonathan Simons research bench — 6 October 2026**  
**Ingested / independently spot-checked: 7 October 2026**

**Status:** preliminary analytic audit. No regularity closure, no novelty claim, and no deficiency alleged in Shahmurov’s proofs. Standalone bench note; live Atlas software was not accessed or modified.

**Honesty locks**
- NS / Clay not solved.
- The \(L^4\) gate is not proved from NSE.
- Generic estimate (A) remains unproved.
- Frozen-drift and initial-layer lower bounds are **not** singularity constructions.
- No door among Shahmurov’s four endpoints is closed by this pass.

---

## Grounding and scope

The relevant author is **Rishad Shahmurov**. His September synthesis, *Endpoint Architectures for Navier–Stokes*, [arXiv:2605.09797v3](https://arxiv.org/html/2605.09797v3), explicitly separates the axisymmetric **record** problem from the **recurrence/provenance** problem. Variables:

\[
F=\frac{u^\theta}{r},\qquad G=\frac{\omega^\theta}{r},\qquad \Gamma=r u^\theta.
\]

Meridional records and signed compression are receiving branches; boundary/age/frequency recession remains open. These are stated endpoints, not defects discovered in this audit.

Primary sources:
- https://arxiv.org/html/2605.09797v3 (Sections 1, 4, 5, 7) — HTML retrieved in this ingest; grounding matches.
- *Critical Structure of Axisymmetric Navier–Stokes with Swirl*, https://arxiv.org/pdf/2606.07869 (September v2). Indexed text was accessible in the original bench; **proofs have not been audited here**. Do not rely on an older indexed title for the September version.

Internal chain note named in the bench: `NS3D_GENERIC_PROOF_CHAIN_REVISED_2026-09-23.md` v10 (states \(T_{\mathrm{ax}}=\int_{r<\delta} G\partial_z(F^2)\,dm\) and proposes \(\int_0^T\|F\|_{L^4(B_\delta)}^4\,dt<\infty\)). **That file and the separate swirl-note localization were not recovered in this workspace ingest.** Generic estimate (A) remains a separate generic-3D argument.

**Measure convention for calculations below:** physical measure \(dx=2\pi r\,dr\,dz\) on axisymmetric \(\mathbb{R}^3\), smooth axis-compatible fields, \(\nu>0\), sufficient decay. Conversion to a five-dimensional Hodge measure requires a separate derivation.

---

## 1. What the \(L^4\) gate actually buys

For the standard axisymmetric \(G\) equation,

\[
\partial_t G+b\cdot\nabla G=\nu\bigl(\partial_{rr}+3r^{-1}\partial_r+\partial_{zz}\bigr)G+\partial_z(F^2),
\]

multiplication by \(G\) in physical measure yields

\[
\frac12\frac{d}{dt}\int G^2\,dx+\nu\int|\nabla G|^2\,dx+2\pi\nu\int G(0,z)^2\,dz
=\int G\partial_z(F^2)\,dx=-\int(\partial_z G)F^2\,dx.
\]

For any \(\eta>0\),

\[
\bigl|\int(\partial_z G)F^2\,dx\bigr|\le\eta\nu\int|\partial_z G|^2\,dx+(4\eta\nu)^{-1}\int|F|^4\,dx.
\]

A **supplied** global spacetime \(L^4\) gate pays the axial source in this particular \(G\) budget. Conditional only. Not a proof that NSE supplies the gate. Not continuation. Not generic (A).

With cutoff \(\chi\ge0\), an extra \(-\int(\partial_z\chi)GF^2\,dx\) appears; transport, diffusion, time-cutoff, and boundary flux terms remain. Fixed infinite cylinder ≠ bounded ball.

---

## 2. Scaling check

Under \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2 t)\): \(F_\lambda=\lambda^2 F\), \(G_\lambda=\lambda^3 G\), \(\Gamma_\lambda=\Gamma\). On rescaled spacetime,

\[
\iint|F_\lambda|^4\,dx\,dt=\lambda^3\iint|F|^4\,dx\,dt.
\]

Physical-measure scale-invariant diagnostic on a radius-\(R\) parabolic region: \(R^{-3}\iint|F|^4\,dx\,dt\) (bench writes the normalized form carefully; bounded normalized values do **not** imply a summable unnormalized tube budget over shrinking scales).

---

## 3. Analytic concentration family

Pure-swirl Gaussians:

\[
u^\theta_\varepsilon=a_\varepsilon r\exp\bigl(-(r^2+z^2)/\varepsilon^2\bigr),\quad
F_\varepsilon=a_\varepsilon\exp\bigl(-(r^2+z^2)/\varepsilon^2\bigr).
\]

Exact:

\[
E_\varepsilon=\frac{\pi^{3/2}a_\varepsilon^2\varepsilon^5}{4\sqrt2},\quad
D_\varepsilon=\frac{5\pi^{3/2}a_\varepsilon^2\varepsilon^3}{4\sqrt2},\quad
Q_\varepsilon=\frac{\pi^{3/2}a_\varepsilon^4\varepsilon^3}{8},\quad
\|\Gamma_\varepsilon\|_\infty=|a_\varepsilon|\varepsilon^2/e.
\]

With \(a_\varepsilon=\varepsilon^{-3/2}\): \(E=O(\varepsilon^2)\), \(D=O(1)\), \(\|\Gamma\|_\infty=O(\varepsilon^{1/2})\), but \(Q=O(\varepsilon^{-3})\). Low-order upper bounds alone cannot bound \(Q\) uniformly.

**Frozen drift** (\(\partial_t F=\nu L_5 F\), \(b=0\)) gives spacetime cost \(\sim\pi^{3/2}/(240\nu\varepsilon)\) for fixed \(T>0\). Not full NSE. Shows energy/circulation/passive diffusion alone do not pay the gate.

---

## 4. Four-door map (result of this pass)

| Open mechanism | Discriminating test | Must supply | This pass |
|---|---|---|---|
| Meridional Type-II records | Retain meridional + Hodge recovery while measuring swirl gate | Receiving estimate with all local/tail terms | No bridge |
| Signed critical compression | Retain signed action weight vs proposed gate | Proved action bound / contradiction from controlled data | No bridge |
| Noncompact high frequency | Concentrate packets; track gate/gradients/products | Cutoff-uniform tightness or paid spacetime source | Gaussian kills low-order shortcut; frozen drift kills passive-only payment; full NSE untested |
| Boundary entry | Tube cutoff before IBP; keep every flux | Boundary-flux/provenance bound on same unforced solution | Local Young leaves explicit boundary-layer terms; no exclusion |

---

## 5. Stopping rules (keep)

Reject a proposed closure if it: assumes the gate it claims to prove; drops a localization flux; substitutes a generic spectral identity for a swirl estimate; uses a cutoff-dependent constant as if uniform; or converts a functional hostile into an alleged NSE trajectory.

---

## 6–7. Coupled response and initial-layer NSE lower bound

Initial \(G(0)=0\), \(b(0)=0\), but \(\partial_t G(0)=\partial_z(F_0^2)\). Center: \(\partial_t U(0,0,0)=a^2/5>0\) (radial expansion). Midplane \(\partial_t U/a^2>0\); on axis first zero at \(|z|/\varepsilon\approx0.6067752158654651\).

**Coupled local NSE** (rescaled \(w_\delta\), full incompressible system): on a short normalized interval, smooth trajectories for this family have

\[
\int_0^{\varepsilon^2/(16\nu)}\int_{\varepsilon K}|F_\varepsilon|^4\,dx\,dt\ge\frac{c_0}{\nu\varepsilon},\qquad c_0\approx3.53926394\times10^{-5}.
\]

Consequence: no uniform initial-layer cost from energy / \(H^1\) / circulation max / \(\nu\) alone. Limit: obstruction across changing data at \(t=0\); does not refute finiteness for each fixed smooth datum, nor a delayed \([t_0,T]\) bound.

---

## 8–9. Localized \(G\) costs and compression target

Full \(\chi\)-localized \(G\) identity keeps every boundary-layer cost explicit. Global quartic:

\[
\frac14 Q'+ \nu D_F=C_F,\qquad C_F=-2\int U F^4\,dx.
\]

Open research target (sufficient, not proved):

\[
C_F(t)\le\eta\nu D_F(t)+B(t)Q(t),\quad 0\le\eta<1,
\]

with \(\int_{t_0}^T B\) controlled by same-solution data. **Universal** pure absorption \(C_F\le\eta\nu D_F\) for all smooth axisymmetric data is **false** by amplitude scaling (\(C_F\sim M^5\), \(D_F\sim M^4\)).

---

## Independent spot-check (this ingest)

Script: `scripts/ns_attacks/da_swirl_four_doors_verify.py`  
Artifact: `/opt/cursor/artifacts/da-swirl-four-doors/verify_report.json`

| Check | Result |
|---|---|
| Gaussian \(E,Q\) vs exact (Simpson) | relative errors \(\sim4\times10^{-12}\), \(\sim1.7\times10^{-11}\) |
| Axis \(\partial_t U\) first zero | \(\approx0.60686\) vs bench \(0.606775\) (\(\lvert\Delta\rvert\sim8.6\times10^{-5}\)) |
| Axis value at \(s=1\) | matches bench to \(\sim10^{-5}\) |
| \(m_0\), \(c_0\) constants | match to \(\sim10^{-11}\) relative |
| Pure absorption amplitude kill | confirmed by scaling |

Not verified here: full NSE PDE evolution of the family; Shahmurov critical-structure proofs; recovery of the missing swirl-note measure/tube file; generic (A).

---

## Still open

- NSE-generated \(L^4\) gate  
- Coupled-family late-time analysis  
- Signed-action bridge  
- Frequency compactness  
- Boundary payment  
- Exact original swirl-note localization  
- Generic estimate (A)  
- Shared-budget 17/32 package (separate blocker; not this note)

**No door closed. No regularity claim.**
