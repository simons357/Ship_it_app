# ATTACK 8 — Correct record (post-screenshot truth lock)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Status:** **CORRECT RECORD** (revised statement locked after user screenshot review)

**Rule:** Truth only. **Navier–Stokes is NOT solved.** Lemma★ is **OPEN**.

## What Attack 8 is

Attack 8 is the **canonical status record** for Lemma★ after the shape-form lock. It supersedes any chat/screenshot language that closed the kill lane or claimed amplitude/frequency shrinks \(\mathcal R_\star\).

## Locked truths

1. **Kill lane is LIVE.** Failure to find a numerical counterexample does **not** close the falsification lane. Both **falsification** and **proof** remain LIVE.
2. **Shape quotient invariance.** The correct complete quotient
   \[
   \mathcal{R}_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
   \]
   is **exactly invariant** under amplitude \(v\mapsto a v\) and under uniform Fourier dilation \(v(n\cdot)\). Claims that “amplitude or frequency makes the ratio smaller” refer to an **older non-optimized budget** (e.g. post-Young \(T_c/(E Y)\)), not to \(\mathcal R_\star\).
3. **Positive part.** User form uses \((T_c)_+\). Prior Galerkin code used \(T_c^2\). Alignment: when \(T_c\ge 0\), \((T_c)_+^2=T_c^2\); for kill we care about stretching \(T_c>0\). Code now uses \((T_c)_+\).
4. **Numerics hygiene.** Do **not** compare reported values \(0.065\), \(0.073\), \(1.93\times10^{-3}\) unless each used exactly the \(\mathcal R_\star\) formula above.
5. **Archive separation.** LP-shell direction estimates, Route N, Q6 damping, and numerical shell floors through \(M=256\) do **not** establish Lemma★. See [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/) and [`../ARCHIVE_NOT_LEMMA_STAR.md`](../ARCHIVE_NOT_LEMMA_STAR.md).

## What Attack 8 is not

- Not a proof of \(\sup\mathcal R_\star<\infty\).
- Not a kill of Lemma★.
- Not a Millennium / Clay claim.
- Not a Route N / Q6 success weld.

## Next live kill attempt

[`ATTACK_9_PACKET_FAN.md`](./ATTACK_9_PACKET_FAN.md) — coherent packet/fan growth of \(\mathcal R_\star(v_m)\sim m^\gamma\).

## Related

- [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)
- [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)
- [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
