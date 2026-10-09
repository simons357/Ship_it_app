# Gate D September 20 \(\Phi_{abc}\) reference

9 October 2026.
**The six-mode test is not certified. The Gaussian stepper is unchanged. Gate D remains OPEN / BLOCKED.**

Archive: `gate_d_phi_reference_2026-10-09.zip`.
SHA-256: `bfe47670a892531547dd713173c594ac0048ec2d45e7f3ff54e19afd39ed2f85`.
Files: `scripts/ns_attacks/gate_d_phi_reference/`.

The archive contains `signed_phi.py`, `test_signed_phi.py`, and a README. It does not contain `NS_SCALENE_EVOLUTION_IDENTITY_2026-09-20.md`. The README states that `phi_scalene` implements that note’s equation (4) on the normalized \(2\pi\) torus: sum over \(p+q+r=0\) with \(K^2<a<b<c\le N^2\), both Hermitian partners, no extra factor of two, bilinear products.

## Correction

The Lemma 19 witness requires \(+4m^3 A^3\). Under \(T=-\operatorname{Re}\langle B,-\Delta h\rangle\), the ordered convolution for one polarization is \(-4m^3 A^3\). A negative value on a different polarization is not a contradiction, and it is not a pass.

Acceptance still requires the original witness coefficients to reproduce \(+4m^3 A^3\) under the documented convention, with the three terms of \(\Phi_{abc}\), the Hermitian-conjugate contributions, and an independent ordered convolution in agreement. The difference may be polarization, Fourier sign, or an implementation error. That is unresolved.

## Numerical observation, not a certification

The packaged `witness()` coefficients and the two functions in `signed_phi.py` agree with each other at \(+4m^3 A^3\). That internal agreement is not the Lemma 19 audit.

`python3 -m unittest -v test_signed_phi` passed: six-mode cases \(m=1,2,3\) and \(A=1,2\), and the cutoff checks.

An independent pure-Python evaluation of the same two formulas, not the packaged assertions, reproduced the witness exactly:

| \(m\) | \(A\) | \(4m^3 A^3\) | `phi_scalene` | ordered convolution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 4 | 4 |
| 1 | 2 | 32 | 32 | 32 |
| 2 | 1 | 32 | 32 | 32 |
| 2 | 2 | 256 | 256 | 256 |
| 3 | 1 | 108 | 108 | 108 |
| 3 | 2 | 864 | 864 | 864 |

At \(m=1\), \(A=1\) the radius-block sum uses two Hermitian partners, each contributing \(2\). The ordered convolution visits 12 scalene pairs. Eight are zero. The four nonzero terms are \(10\), \(-8\), \(-8\), and \(10\).

Cutoff on the \(m=2\), \(A=1\) witness, whose squared radii are \(4,16,20\): \(K=2\) gives \(0\) because \(a=K^2\) fails the strict lower bound; \(N=4\) gives \(0\) because \(c=20>N^2\); \(K=1\), \(N=5\) gives \(32\). A one-shell field gives \(0\).

## What this does not certify

The 7 October `signed_scalene.py`, fed the same six coefficients packed into an FFT array, returns \(4(2\pi)^3\) for every side length \(L\) tried, including \(L=2\pi\) and \(L=1\). The extra \((2\pi)^3\) is \((2\pi/L)^3 L^3\). That evaluator is a different normalization. It remains a reference, not this formula.

This module does not compute \(D\), \(d\), \(B_I\), or \(\mathcal S_{K,N}\). It does not compute the production probe \(G=T-Y/200\). It is not called by the Gaussian stepper. The frozen cutoff \(N\) is not the grid count. \(K\), its relation to \(N\), and the periodization protocol are still for DA review before any production run.

The locked \(G\) unit test was not rerun. No turnover, regeneration, or cutoff-independent budget is claimed. The frozen experiment has not been launched.

## STATUS

ZIP SHA-256: `bfe47670a892531547dd713173c594ac0048ec2d45e7f3ff54e19afd39ed2f85`.
SIX-MODE TEST: NOT CERTIFIED.
LEMMA 19 REQUIREMENT: \(+4m^3 A^3\) ON THE ORIGINAL WITNESS COEFFICIENTS.
ONE POLARIZATION, ORDERED CONVOLUTION, \(T=-\operatorname{Re}\langle B,-\Delta h\rangle\): \(-4m^3 A^3\). NOT A PASS.
SIGN GAP: UNRESOLVED. POLARIZATION, FOURIER SIGN, OR IMPLEMENTATION ERROR.
PACKAGED `witness()` INTERNAL AGREEMENT AT \(+4m^3 A^3\): NOT THE LEMMA 19 AUDIT.
STEPPER: UNCHANGED.
\(G\) UNIT TEST: NOT RERUN.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
