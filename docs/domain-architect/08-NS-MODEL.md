# Kept NS model — enter into Domain Architect

**Status:** exploratory classification, 2026-09-14  
**Clay NS status:** not claimed  
**Riemann hypothesis status:** not claimed  
**Canonical SFE status:** unresolved  
**Run:** `python -m domain_architect --ns-model`

Enter the **good** NS model from this repo: classical unaugmented
Navier–Stokes on the axisymmetric-with-swirl class, plus the KEEP swirl
algebra (NS-Φ / NS-H002) and the open barrier \(\|u^r/r\|_\infty\).

This is not Track A, not SFE, not Clay closed, and not Hilbert–Pólya.

Source card: [`PHI-RENORM-WHAT-IS-KEPT.md`](../ns-review/PHI-RENORM-WHAT-IS-KEPT.md).  
Audit: [`PHI-RENORM-AUDIT-2026-08-22.md`](../ns-review/PHI-RENORM-AUDIT-2026-08-22.md).

---

## What happens when it is entered

DA accepts it as a **fluids book**. It does not turn it into SFE or RH.

| Seat | Occupant | What DA does |
|---|---|---|
| \(P\) | axisymmetric-with-swirl class, \(\nabla\cdot u=0\) | records the class; does not fill global regularity |
| \(H\) | convection / stretching + Stokes / viscosity | fluids coupling, **not** a Hilbert–Pólya Hamiltonian |
| \(\psi\) | \(u\), \(\omega\), or \(\Phi_{\mathrm{swirl}}=u_\theta/r\) | three presentations of one state |
| \(\lambda\) | \(\nu\), \(r\), \(\dot H^{1.3}\) packaging | scale parameters; the \(\dot H\) relabel is bookkeeping |
| FRA \(\Phi\) | globally regular \(u(t)\) on the class | **target, unfilled** |
| \(E\) | KEEP identity, Lions bookkeeping, Biot–Savart, axis \(\mathcal B\), stretching \(N\), open barrier | expanded from the subject |

Swirl \(\Phi_{\mathrm{swirl}}\) is **not** FRA \(\Phi\) and **not** Riemann’s kernel \(\Phi\).
The KEEP identity \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi_{\mathrm{swirl}}^2)\) sits in \(E\) as algebra. The prize output stays empty.

The load-bearing gap is \(\|u^r/r\|_\infty\) uniform in \(\varepsilon\), equivalent in difficulty to swirl global regularity. Conditional reduction only.

PARK items (SFE→NS, CMB as proof, Triple Lock, Lemma★ collapse, Track A as this PDE, Riemann \(\Phi\) as swirl \(\Phi\)) are refused, not ingested.

---

## What to read as DA’s output

```bash
python -m domain_architect --ns-model
```

Live narrative: `results/ns-model.txt`.

Component count is decided by the subject (interface letters plus extras).
Five letters are not a cap. Quantum Hilbert–Pólya is a different instance.

Related runs:

```bash
python -m domain_architect --pair
python -m domain_architect --breakdown-children
```
