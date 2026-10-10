# Gate D September 20 signed-scalene reference — 2026-10-09

Source definition: NS_SCALENE_EVOLUTION_IDENTITY_2026-09-20.md, Eq. (4), normalized 2π torus. Phi_abc sums over p+q+r=0 and a<b<c with K²<a<b<c≤N². Includes both Hermitian partners without an extra factor 2. All products bilinear.

`phi_scalene` is a slow, independent sparse reference implementation. `ordered_transfer` separately evaluates the original ordered Fourier convolution (p+q=k). `test_signed_phi.py` verifies exact six-mode witness 4 m³ A³ for m=1,2,3 and A=1,2, plus cutoff behavior. All tests passed on this container with NumPy; this is not an exact-integer arithmetic checker, but the witness inputs are integer-valued complex and tested values are exactly representable.

RUN: `python -m unittest -v test_signed_phi`

IMPORTANT: This module is not connected to the Gaussian stepper. Its input is a dict of normalized Fourier coefficients on the 2π torus. The Gaussian code uses FFT arrays on a box of side L and dimensional wave numbers 2πk/L; a correct adapter must apply coefficient normalization, physical frequency factors and volume consistently. The frozen Galerkin cutoff N is not the grid count n. The K value and relation to N, plus periodization/domain comparison, need DA preregistration.

D = T_sc(P_{|k|>K} u_N) - νY_N/4; d=D/X_N; positive part budget ∫(d)_+ dt. G=T(v)-Y(v)/200 is distinct. The present reference does not produce D or G, no episode detection, and no production run.

STATUS: independent small-field reference PASS; driver integration and DA approval PENDING. Gate D OPEN/BLOCKED.
