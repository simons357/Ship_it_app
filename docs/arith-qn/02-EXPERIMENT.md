# Computational experiment — spectral Mertens identity

**Protocol.** Verify the exact identities on a frozen list of \(N\), measure weight ranges, operator norms, and unsigned-versus-signed mass. Do **not** treat small-\(N\) size of \(|M(N)|\) as a proof of \(N^{1/2+\varepsilon}\).

**Code.** `python -m arith_qn --survey --max-n 512 --out results/mertens_spectral`

**Outputs.**

- `results/mertens_spectral/survey.json`
- `results/mertens_spectral/q6.json`
- `results/mertens_spectral/SUMMARY.md`

## What is tested

| Claim | Type | Result |
|---|---|---|
| \(M(N)=\operatorname{Tr}(D_NQ_N)\) | exact identity | holds to floating-point residual |
| \(M(N)=\sum\lambda_j w_j\) | exact identity | holds to floating-point residual |
| \(M(N)=\sum_\lambda\lambda\operatorname{Tr}(D_NP_\lambda)\) | exact identity | holds after clustering |
| \(M(N)=\operatorname{Tr}(A_N)\), \(A_N=D_N^{1/2}Q_ND_N^{1/2}\) | exact identity | holds |
| \(1\le w_j\le N\), \(\sum w_j=N(N+1)/2\) | exact constraint | holds |
| \(Q_N\neq\widetilde Q_N\) | distinction | locked at \(N=10\) and \(N=6\) |
| \(\|Q_N\|_{\mathrm{op}}\ge\sqrt{N}\) | elementary | holds; first column is all ones |
| crude bound yields \(N^{1/2+\varepsilon}\) | method claim | **fails** (bound \(\gtrsim N^{5/2}\)) |
| cancellation estimate from independent \(Q_N\) data | transfer | **OPEN**; software refuses `bridge_complete` |

## Frozen \(N\) list

\(1,2,6,10,12,16,20,24,32,48,64,80,96,128,160,192,256,320,384,512\).

Dense eigendecomposition is \(O(N^3)\). The list is a laboratory, not an asymptotic proof.

## Reading the table

- `crude/|M|` is \(\|Q_N\|_{\mathrm{op}}N(N+1)/(2|M(N)|)\). Large values mean the spectral-norm estimate is vacuous.
- `|M|/√N` is an empirical size ratio. On this range it stays moderate. That is **not** an independent derivation of the candidate bound.
- `cancel. ratio` is \(\sum|\lambda_j w_j|/|\sum\lambda_j w_j|\). Values \(\gg 1\) show that the signed spectral sum cancels relative to the unsigned mass — the cancellation that still needs a proof.
- `|λ|–w corr` is the Pearson correlation of \(|\lambda_j|\) with \(w_j\). A stable, independently proved anti-correlation would be a candidate transfer input. A numerical correlation on \(N\le 512\) is not.

## Rule

If a later note claims the bridge is complete because \(Q_N\) has a closed-form spectrum, reject the claim unless the weight (or projector) estimate is proved from a property that is not already equivalent to the Mertens bound.
