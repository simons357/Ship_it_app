# Connected signed-scalene diagnostic

The September 20 evaluator is called on FFT states laid out like the Gaussian driver. `gaussian_gate_d.py` is imported and is not edited. `step` is the existing Navier–Stokes stepper.

`Phi_abc` uses integer radii. The cutoff in force here is \(K^2<a<b<c\le N^2\), with \(a=|k|^2\) and \(k\) the integer mode index. The physical wavenumber \(2\pi|k|/L\) is recorded beside that cut. It is not substituted into \(\Phi_{abc}\).

The same integer pair \((K,N)=(1,5)\) therefore sits at physical wavenumber \(2\pi/L\) on a box of side \(L\) and at \(\pi/L\) on a box of side \(2L\). That comparison is not resolved. DA resolves it before any experiment approval.

\(D=T_{\mathrm{sc}}-\nu Y/4\) uses \(\nu=1/c\) and the integer-lattice \(Y=\sum|k|^4|\hat u|^2\). The driver's physical \(X\), \(Y\), and \(G=T-Y/c\) stay in the other convention and are not mixed into \(D\).

Run: `python -m unittest -v test_connected`

The five checks are the packaged witness checks: the \(4m^3A^3\) family, agreement with the ordered convolution, \(K=2\) gives 0, \(N=4\) gives 0, and \(K=1\), \(N=5\) gives \(+32\) with the ordered convolution also \(+32\).

These checks do not certify the original Lemma 19 coefficients. The frozen \(c=200\) production experiment is not launched. Gate D remains OPEN / BLOCKED.
