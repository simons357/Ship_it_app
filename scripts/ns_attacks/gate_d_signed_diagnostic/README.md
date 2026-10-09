# Gate D — signed-scalene reference diagnostic, October 9

This is an **independent, small-field reference evaluator**, not a production Gate D implementation or approved replacement for the missing September 20 source. `signed_scalene.py` implements the ordered-convolution signed-scalene definition from the user-provided October 7 sharp-band note. It excludes interactions unless all three squared Fourier radii are distinct, with optional high-pass restriction applied to all legs. It uses physical wavenumbers 2πk/L and the physical box volume L³; the October 7 note uses normalized torus measure. The September 20 Gate D cutoff/normalization convention must be checked against the original before production use.

The included existing Gaussian driver has G = production - Y/c, and leaves T_sc and D null intentionally. This reference evaluator is **not wired into the time stepper**: direct mode-pair enumeration is expensive at N=128/160. The test compares its signed transfer against a separately evaluated pseudospectral full production on an exact 3-radius triad, plus a one-shell zero test. This does not verify arbitrary scalene filtering or continuum R³ convergence.

Run: `python -m unittest -v test_signed_scalene test_G` (requires numpy).

Gate D remains OPEN / BLOCKED. Do not run the frozen experiment before DA preregistration.
