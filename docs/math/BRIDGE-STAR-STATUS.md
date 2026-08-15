# Bridge\* — status after Tao / SND panel (2026-08-15)

Companion to `docs/math/TAO-MATH-PANEL-SND-H.md` and `docs/BRIDGE-STAR-PROOF.md`.

## Proved

**Theorem (single Goldbach pair).** For distinct primes \(p,q\),
\[
R(e_p-e_q)=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}\;>\;-\frac12.
\]
Proof: \(R+1/2>1/2-1/\sqrt{pq}\) and \(pq\ge 6\Rightarrow 1/\sqrt{pq}<1/2\).

## Numeric (multi-rep)

For \(v_k=\sum_{p\in\mathcal{R}(k)}(e_p-e_{k-p})\) on \(\widetilde Q_N\), worst Rayleigh through \(N=200\) is \(\approx -0.183\) at \(k=8\) (single pair \((3,5)\)), still \(>-1/2\). Richer multi-rep cases sit higher.

## Open

Uniform cross-term lemma: \(R(v_k)\ge -c_0\) with absolute \(c_0<1/2\) for all even \(k\le N\).

## Not claimed

- Full-spectrum \(\lambda_{\min}(\widetilde Q_N)>-1/2\) (false).
- Navier–Stokes / Clay from Bridge\*.
- Identification of Bridge\* with fluids Theorem H or with matrix \(H_N\) floor.

## Reproduce

```bash
python3 scripts/bridge_floor_verify.py 200
python3 scripts/h_n_bridge_star_check.py 200
```
