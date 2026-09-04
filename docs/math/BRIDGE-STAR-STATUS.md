# Bridge\* — status after Tao / SND panel (updated 2026-08-25)

Companion to `docs/math/TAO-MATH-PANEL-SND-H.md`, `docs/BRIDGE-STAR-PROOF.md`,
and `docs/math/CLOSURE-ATTACK-PLAN.md`.

## Proved

**Theorem (single Goldbach pair).** For distinct primes \(p,q\),
\[
R(e_p-e_q)=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}\;>\;-\frac12.
\]
Proof: \(R+1/2>1/2-1/\sqrt{pq}\) and \(pq\ge 6\Rightarrow 1/\sqrt{pq}<1/2\).

**Theorem (multi-representation).** For even \(k\) and
\(v_k=\sum_{p\in\mathcal{R}(k)}(e_p-e_{k-p})\neq 0\),
\[
R(v_k)>-1/2.
\]
Proof: disjoint pair blocks + nonnegative cross-term factorization
\((p^{-1/2}-q^{-1/2})(r^{-1/2}-s^{-1/2})\) when \(p<q\), \(r<s\).
See `04_q6_inverse_gcd.tex` Lemma (cross) + Theorem (multi-rep).

## Numeric (sanity)

Worst multi-rep Rayleigh through \(N=200\) is \(\approx -0.183\) at \(k=8\)
(single pair \((3,5)\)), still \(>-1/2\). Richer multi-rep cases sit higher.

## Closed (was open)

Uniform multi-rep floor \(R(v_k)>-1/2\) — **proved**, not merely numeric.

## Not claimed / killed

- Full-spectrum \(\lambda_{\min}(\widetilde Q_N)>-1/2\) (**false**).
- Universal \(\lambda_{\min}(H_N)\ge-3/14\) (**false** at small \(N\)).
- Navier–Stokes / large-data SND from Bridge\*.
- Identification of Bridge\* with fluids Theorem H.

## Reproduce

```bash
python3 scripts/bridge_floor_verify.py 200
python3 -m unittest tests.test_bridge_star_h_n -v
```
