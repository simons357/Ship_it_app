# Line audit of pasted June 5 Unified text

Source: user paste of *A Universal Non-Concentration Principle: SND = GNC = Bridge* (June 5, 2026).  
Local PDF/txt: `docs/papers/SND_GNC_BRIDGE_UNIFIED.*`  
Corrected draft: `docs/papers/SND_GNC_BRIDGE_REVISED.md`

| Section / claim | Verdict | Note |
| --- | --- | --- |
| Status: equivalence proved; MP not claimed | Keep intent | Equivalence must be rewritten after operator/floor fix |
| \(Q_N(i,j)=1/\gcd\) | OK as named matrix | Full-spectrum Bridge on it is false |
| §2.1 \(1/\gcd=\sum\mu\varphi/d^2\) | **False** | \(n=2\): RHS \(3/4\neq 1/2\); use \(g=\mu*(1/\mathrm{id})\) |
| §2.1 \(H_N=\sum(\mu\varphi/d^2)P_d\) = \(Q_N\) | **False ID** | Different operator |
| §2.2 \(\lambda_{\min}\to 6/\pi^2-1/2\) | **False** for \(Q_N\) | Floor \(\to-\infty\); mixes \(\sum\mu/d^2\) vs \(\sum\mu\varphi/d^2\) |
| §2.2 numeric \(\lambda_{\min}>-1/2\) for \(N\le 5000\) | **False** | Fails by \(N=20\) |
| SND definition (shell \(\rho\le\rho_0\)) | Keep as def | NS apps conditional on companions |
| \(v_k=\chi(j)-\chi(k-j)\) | **Broken detector** | Zero on every Goldbach pair |
| Dark-state ↔ Goldbach | **False** | Raw: \(\langle e_p-e_q,Q(e_p-e_q)\rangle=1/p+1/q-2<0\) |
| GNC with \(\kappa_*=6/\pi^2\) | Suspend | Needs correct vector + operator |
| Bridge \(\lambda_{\min}(Q)>-1/2\) | **Withdrawn** | Replace by Bridge\* on \(\tilde Q\) |
| Main Thm Bridge⇒GNC via floor | Collapses | Premise false |
| Main Thm GNC⇒Bridge contrapositive | Collapses | Same |
| Main Thm Bridge iff SND via \(d_{\mathrm{gcd}}\) | Not kept | Needs cone/Bridge\* rewrite |
| Cor. “one proof closes all three” | Not kept as stated | Conditional apps only after restricted floor |
| \(\kappa_*\) “universal floor of \(Q_N\)” | **Withdrawn** as \(\lambda_{\min}\) | Remains squarefree density |
| Open: prove \(\lambda_{\min}(Q)>-1/2\) | **Abandoned as stated** | Open A = multi-rep Bridge\* |
| Routes A–D | Heuristic only | Do not treat as proofs |
| Phi-renorm / T2 pointers | Separate tracks | Swirl cancel still the clean credit paper |

**Live math target after this paste:** Bridge\* single-pair **proved** (`docs/BRIDGE-STAR-PROOF.md` §2); multi-rep lemma open; NS needs \(H_N\) (−3/14) from Drive.
