# Excalibur — exact Gaussian \(z=0\) anatomy

**Date:** 11 October 2026.
**Status:** Initial-data figure only. Not a trajectory. Not deliverable D.

Files: `scripts/ns_attacks/excalibur_anatomy/`.

The uploaded script `anatomy.py` builds

\[
A(x)=e^{-|x|^2/2}(xy,xz,x+yz),\qquad U=\nabla\times A
\]

with SymPy derivatives, then evaluates the plane \(z=0\) on a \(101\times 101\) grid with \(x,y\in[-3,3]\). The four panels are \(|U|\), \(|\nabla\times U|^2\), the stretching \(\omega\cdot S\omega\), and the strain magnitude \(|S|\).

## Check against the locked stepper

The velocity stored in `gaussian_z0_slice.npz` agrees with `gaussian_curl` in the locked file `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py` to \(2.22\times 10^{-16}\). That file was not edited. Its SHA-256 remains `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`.

A fresh run of the same script reproduced every array in the uploaded `.npz` with maximum absolute difference \(0\). On that grid the speed reaches \(1\), the stretching runs from about \(-1.233\) to \(2.794\), the enstrophy reaches about \(5.302\), and the strain magnitude reaches about \(1.654\).

## What the figure is not

There is no time step, no viscosity, no periodic projection, and no signed-scalene transfer. The picture cannot show a crossing of \(D\), and it cannot show blowup. Deliverable D still needs a volume viewer with vorticity, stretching, and signed transfer, plus linked \(x\), \(y\), and \(z\) slices. This filing is the \(z=0\) initial slice of the first two of those layers.

The frozen \(c=200\), \(s\ge 4\) experiment was not launched. Gate D remains OPEN / BLOCKED.

## STATUS

SLICE: \(z=0\), \(101\times 101\), EXACT INITIAL \(U=\nabla\times A\).
AGREES WITH LOCKED `gaussian_curl` TO \(2.22\times 10^{-16}\).
RERUN MATCHES THE UPLOADED ARRAYS EXACTLY.
NOT A TRAJECTORY. NOT \(T_{\mathrm{sc}}\). NOT BLOWUP EVIDENCE.
DELIVERABLE D: NOT COMPLETE.
PRODUCTION \(c=200\), \(s\ge 4\): NOT LAUNCHED.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
