# Extracts — absolute defs + HH→L (from PR #48 pack)

Copied from `origin/cursor/ns-five-lane-lemma-star-1390` on 2026-09-10 recovery.
**NS not solved. Lemma★ OPEN.**

## Absolute defs (`LEMMA_STAR_SHAPE_FORM.md`)

Linear moments:
- \(E=\|v\|_2^2=\sum|v_k|^2\)
- \(X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2\)
- \(Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2\)
- \(Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2\)
- \(\Lambda=Y/X\)
- \(\nu\) = viscosity; \(\theta\in(0,1)\) = Young absorption parameter in viscosity packaging

Centered dissipation:
- \(\mathcal{D}_s=Z-\Lambda Y=Z-Y^2/X=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\)

Centered transfer:
- \(N=-\langle B,Av\rangle\), \(M=-\langle AB,Av\rangle\)
- \(T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k\)
- \(\Lambda'=2/X\,(T_c-\nu\mathcal{D}_s)\)

Shape★:
- \(\mathcal{R}_\star=(T_c)_+^2/(\mathcal{D}_s\,E\,Y)\)
- Viscosity form: \(T_c\le\theta\nu\mathcal{D}_s+C_0\nu^{-1}\|v\|_2^2 Y\) with \(C_0=C_{\mathrm{geom}}/(4\theta)\)

## HH→L (`ATTACK_3_BONY_HH_L.md`)

Partition bilinear form driving \(\mathfrak{T}_c\) into Bony channels HH / HL / LL.
**Claimed bottleneck:** HH→L blocks a clean product bound toward
\(|\mathfrak{T}_c|\le C\|u\|_2 X^{3/2}\).

Status: diagnostic only; no analytic closure; kill uses complete signed \(T_c\).

## Related product forms in the same pack

- Pre-Young: \(|T_c|\le C\|u\|_2 X\Lambda\) (geometry)
- Survivor \(C_*\): \(|T_c|\le C_* X^{3/2}\Lambda\)
- K=0 kill form: \(T_c/\mathcal{D}_s\) blows with amplitude
