# Five-lane simultaneous run — HEADLINE

**NS is NOT solved. Lemma★ is NOT proved.**

**Canonical ★ = shape form:** \(T_c(v)^2\le C_{\mathrm{geom}}\mathcal D_s(v)\,E(v)\,Y(v)\), \(\mathcal R_\star=T_c^2/(\mathcal D_s E Y)\). See `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`.

```json
{
  "attack1": "SURVIVE_numeric_NOT_proof",
  "attack2": "K0_DEAD_Cstar_SURVIVES_numeric",
  "attack3": "HH_INPUT_CHANNEL_LIVE_BOTTLENECK_NOT_strict_HH_to_L",
  "attack4": "STOKES_IDENTITIES_OK_absorption_needs_remainder",
  "attack5": "SURVIVE_numeric_gap_remains",
  "LemmaStar_C0_killed": false
}
```

## Key numeric bounds (this run)

- Attack1 phase diam |Rpre| ≈ 0.155 (matches prior ∼0.16)
- Attack2 K=0 DEAD: |Tc|/Ds grows ∼B (0.0035 → 349 on triad)
- Attack2 C* ≈ 0.004058 amp-invariant on fixed triad; Attack5 max |Rc*| ≈ 0.04065
- Attack5 max |Rpre| ≈ 5.0881 on scale-separated triad phases
- Attack5 shape★: max \(\mathcal R_\star\approx0.0227\) (tag `sep_1_p8`); almost-shell max \(\sim3.6\cdot10^{-6}\); pure-shell kills 0
- Lemma★ \(C_{\mathrm{geom}}\) / C0 **NOT KILLED** by this search (threshold 1e3)
- Artifacts: `/opt/cursor/artifacts/ns_five_lane_shape_star/`

## Live kill criteria

- \(\mathcal R_\star\to\infty\) on a shape family → ★ dead
- \(\mathcal D_s=0\) and \(T_c>0\) → ★ dead; pure single shell (both vanish) is vacuous
- Almost-single-shell / 9B \(K_{\alpha,\beta}\) / **9D** designed \(\Theta(m^2)\) locked-phase: live attempts
- **9B split:** \(\max_{\beta>\alpha}K\approx0.641\) at \((4,8)\) = higher shell (**not** HH→L); \(\max_{\beta<\alpha}K\approx0.0123\) at \((5,2)\) = genuine HH→L subfamily
- **9C fixed-gap** natural same-shell: **NOT** a kill (\(\mathcal R_\star\) \(0.11\to 0.031\); SoT-only — no sweep script in PR #48)
- Attack 3: HH **input** channel diagnostic — **not** strict HH→L (no low-output restriction)

## Exact inequality still open

Prove \(\sup\mathcal R_\star<\infty\) (boxed shape ★) **or** geometric C in |Tc| ≤ C ||u||₂ X Λ (pre-Young → viscosity ★) **or** |Tc| ≤ C* X^1.5 Λ, with HH-channel control (Attack 3 is not a strict HH→L map). That reason is NOT written. **NS not solved.** Kill lane **LIVE**.

Pack locator: https://github.com/simons357/Ship_it_app/pull/48 — `docs/math/ns_attacks/FIVE_LANE_PACK_LOCATOR.md`.
