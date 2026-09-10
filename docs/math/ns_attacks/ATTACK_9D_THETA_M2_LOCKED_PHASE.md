# ATTACK 9D — Designed \(\Theta(m^2)\)-closure subset with locked phases (stub / spec)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Status:** **SPEC / STUB** — remaining packet falsifier. Not yet run. Kill lane **LIVE**. Lemma★ **OPEN**. **NS not solved.**  
**Prior non-kill:** Attack 9C (fixed-gap spheres) — natural same-shell ensemble **NOT** a kill; \(\mathcal{R}_\star\) fell \(0.11\to 0.031\) — [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md).

## Motivation (why 9C failed → what 9D must change)

Attack 9C locked:
- \(\mathcal{D}_s\) from the **gap**, not packet width;
- natural closures only \(O(m)\);
- \(\mathcal{R}_\star\) **falls** with \(n\) and does **not** track \(m^{1/2}\).

So the remaining packet falsifier is **not** another natural same-shell random/ensemble probe. It must **design** a closure subset of size \(\Theta(m^2)\) and **lock phases** so that coherent stretching can accumulate in \((T_c)_+\) without the cancellations that keep natural ensembles bounded/decaying.

## Target family (spec)

1. **Mode set:** Choose a primary packet of cardinality \(m\) (exact shell or controlled near-shell) plus a **designed** closing / interaction subset whose cardinality (or number of active triad closures) scales as \(\Theta(m^2)\), not \(O(m)\).
2. **Phases:** Lock relative phases (and polarizations) so the signed triad Im-sum adds constructively in total \(T_c\) — no free random-phase averaging.
3. **Spectral control:** Keep \(\mathcal{D}_s\) under explicit control (fixed gap, exact-shell + \(\varepsilon\) closing, or other documented spectral support). Do **not** accidentally reintroduce 9A-style \(\mathcal{D}_s\) blowup from uncontrolled packet widening.
4. **Quotient:** Report complete
   \[
   \mathcal{R}_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
   \]
   with **total** signed \(T_c\) (not HH→L-only).

## Kill criterion

| Outcome | Meaning |
|---------|---------|
| Smooth family with \(\mathcal{R}_\star\to\infty\) (e.g. \(\sim m^{\gamma}\), \(\gamma>0\), or unbounded in designed scale) | **★ dead** |
| Bounded / decaying \(\mathcal{R}_\star\) on the designed locked-phase family | Those shapes did not kill ★ — **not a proof**; kill lane still **LIVE** |
| Uncontrolled \(\mathcal{D}_s\) growth that invalidates the design | Implementation / design bug — fix before claiming |

## Required controls (when implemented)

| Control | Expectation |
|---------|-------------|
| Amplitude: \(\mathcal{R}_\star(av)=\mathcal{R}_\star(v)\) | Exact |
| Uniform Fourier dilation invariance (when applicable) | Exact |
| Closure count / designed subset size | Document \(\Theta(m^2)\) scaling explicitly |
| Phase lock | Reproducible; no silent random re-phase |
| Report **total** signed \(T_c\) | Not HH→L-only |

## Script status

**Not implemented.** Planned name (TBD): `scripts/ns_attacks/attack9d_theta_m2_locked_phase.py`.  
Until then this note is **spec-only** in the Source of Truth.

## Reproduce (placeholder)

```bash
# Not yet available — SoT stub only
# PYTHONPATH=scripts python3 scripts/ns_attacks/attack9d_theta_m2_locked_phase.py \
#   --outdir /opt/cursor/artifacts/attack9d_theta_m2_locked_phase
```

## Related

- [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md) — natural ensemble non-kill
- [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md) — \(K_{\alpha,\beta}\)
- [`ATTACK_9A_AP_PACKET_FAILURE.md`](./ATTACK_9A_AP_PACKET_FAILURE.md) — AP fan non-kill
- [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
- [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)

**NS not solved.**
