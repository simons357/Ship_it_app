# Swirl faces in Domain Architect

**Book:** axisymmetric Navier–Stokes with swirl  
**ChatVault:** **no.** Do not drain these faces.  
**Clay NS / RH:** **not claimed.**

Two faces sit on the DA desktop so they can be inquired side by side.

## WITH cancel (live Phi)

**PDF:** `domain_architect/static/faces/01_phi_renormalization.pdf`  
**DOI:** [10.5281/zenodo.22050974](https://doi.org/10.5281/zenodo.22050974) (sibling 22050975)  
**Operator:** \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\), \(\Phi=\Gamma/r^2=u_\theta/r\).

Q1-augmented / Φ-system. The identity is algebra. Classical regularity without augmentation remains open on that paper’s own dashboard.

June conditional Phi [10.5281/zenodo.21071991](https://doi.org/10.5281/zenodo.21071991) is archive (`/faces/superseded/june_phi_conditional.pdf`).

## WITHOUT cancel

**PDF:** `domain_architect/static/faces/swirl_without_cancel.pdf`  
**Operator:** \(D_t\Omega=(1/r^4)\partial_z(\Gamma^2)+\nu L_{\mathrm{cyl}}\Omega\), \(\Gamma=r u_\theta\).

The 1/r^4 centrifugal axis term is still in the equations. Zenodo public API (2026-08-26) did not yield a separate pre-cancel swirl PDF (22050974/975, 22045467, 21071991, 20405405, 20405597 all introduce the cancel). This DA face states the pre-cancel operator honestly.

## Compare

```bash
python3 -m domain_architect --swirl-with-cancel
python3 -m domain_architect --swirl-without-cancel
python3 -m domain_architect --swirl-compare
python3 -m domain_architect --site
# Inquiry → Load swirl WITH cancel / WITHOUT cancel / Compare swirl
```

WITH does not solve WITHOUT. Neither face is unconditional classical 3D NS.
