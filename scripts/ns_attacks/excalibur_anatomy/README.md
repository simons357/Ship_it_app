Exact analytic Gaussian initial field \(U=\nabla\times A\), with

\[
A(x)=e^{-|x|^2/2}(xy,xz,x+yz).
\]

Slice \(z=0\), \(x\) and \(y\) from \(-3\) to \(3\), \(101\times 101\). SymPy derivatives, NumPy evaluation. Four diagnostic panels. These are initial-data geometry only, not a Navier–Stokes trajectory, not a signed-scalene transfer, and not blowup evidence.

`anatomy.py` is the uploaded script, unchanged. It writes to `/mnt/data/excalibur_anatomy`. The arrays in `gaussian_z0_slice.npz` and the figure `gaussian_initial_anatomy.png` are the outputs of that script.

SHA-256:

- `anatomy.py`: `8e05bd386324344ace15aa429228a19befc99d02170a28ec4d080dd65dfbd7f6`
- `gaussian_z0_slice.npz`: `41aca922af24f37ff18e571e7861133ffd640f8a707fbab0bf04c35bf9b37981`
- `gaussian_initial_anatomy.png`: `4e364161f5bd3ea67a160ba28403dae4f77ed83d1023c89b9def7c912cdd0468`

See [`docs/EXCALIBUR-ANATOMY-SLICE-2026-10-11.md`](../../../docs/EXCALIBUR-ANATOMY-SLICE-2026-10-11.md).
