# ATTACK 9D — Designed \(\Theta(m^2)\)-closure subset with locked phases (stub / spec)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Status:** Two writings of “9D” are **dead or excluded**. The remaining
lane is growing output-support \(s\) on the 9B family (already scored).
**No 9D close.** Kill lane **LIVE**. Lemma★ **OPEN**. **NS not solved.**  
**Prior non-kill:** Attack 9C (fixed-gap spheres) — natural same-shell ensemble **NOT** a kill; \(\mathcal{R}_\star\) fell \(0.11\to 0.031\) — [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md).

**The call (12 September):** do not implement this
stub. Setup answered:
[`../../ATTACK-9D-SETUP.md`](../../ATTACK-9D-SETUP.md).
Same \(B\) as 9B. Growing \(s\) is a 9B test,
not a new 9D object. HH→L is a different family.

**On this branch.** Two writings of “9D,” do not merge:

1. Designed \(\Theta(m^2)\) locked-phase **subset** (Freiman-AP).
   Already scored. Already dead (\(\mathcal D_s\) wins).
   Do not rebuild. [`../../LEMMA-STAR-PACKET.md`](../../LEMMA-STAR-PACKET.md).
2. Screenshot: \(\Theta(m^2)\) pairs onto **one** output, or a
   **fixed** number of outputs. **Analytically excluded.**
   Per output, \(p+q=k\) gives at most \(m\) pairs.
   \(K_{\alpha,\beta}\le 16s\). Fixed \(s\) cannot unbound \(K\).
   File: [`../../LEMMA-STAR-9B-COUNTING.md`](../../LEMMA-STAR-9B-COUNTING.md).

Growing the **number of output modes** stays a 9B test
(complex polarizations, keep \(|k|\)). That is not (1) and
not (2). Seated live write:
[`../../ATTACK-9D-GROW-S.md`](../../ATTACK-9D-GROW-S.md).
`attack9d_theta_m2_locked_phase.py` was not written.

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

## Script status (13 Sep 2026 lock)

The team **already had** the live remaining lane. It was not missing.
It lived under a 9B name:

- Analytic lock + growing-\(s\) sweep:
  `scripts/ns_attacks/attack9b_output_counting.py`
- Score: [`../../LEMMA-STAR-9B-COUNTING.md`](../../LEMMA-STAR-9B-COUNTING.md)
- JSON: `results/attack9b_counting/attack9b_counting.json`

A thin 9D entry point now calls that same sweep (does **not** rebuild
Freiman-AP or the fixed-\(s\) screenshot):

`scripts/ns_attacks/attack9d_growing_output_s.py`

**No 9D claim.** Finite \(\max K\approx 0.506\), \(\max s=24\) on the
288-field sweep is **not** \(C_0\). Lemma★ **OPEN**. Kill lane **LIVE**.
Drive/Gmail had no separate `attack9d_*.py`. Do not invent one.

## Reproduce

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9d_growing_output_s.py \
  --out /opt/cursor/artifacts/attack9d_growing_output_s.json
```

Same math as:

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_output_counting.py
```

## Related

- [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md) — natural ensemble non-kill
- [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md) — \(K_{\alpha,\beta}\)
- [`ATTACK_9A_AP_PACKET_FAILURE.md`](./ATTACK_9A_AP_PACKET_FAILURE.md) — AP fan non-kill
- [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
- [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)

**NS not solved.**
