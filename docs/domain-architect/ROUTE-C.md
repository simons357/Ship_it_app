# Route C face in Domain Architect

**Book:** Route C (exploratory / conditional)  
**PDF:** `domain_architect/static/faces/05_route_c_conditional.pdf`  
**Site:** http://127.0.0.1:8765/faces/05_route_c_conditional.pdf  
**ChatVault:** **no.** This face is not filed into the vault.

Locked operator:

\[
Q_N[i,j]=\frac{1}{\gcd(i,j)\sqrt{ij}}.
\]

August 2026 corrected preprint. Gaps A and B remain open. RH is **not** claimed. Live DOI [10.5281/zenodo.22050963](https://doi.org/10.5281/zenodo.22050963).

This is not RH Track B \(\mu(\gcd)/\gcd\). Do not import the \(-1/(2\pi)\) limit into Track B.

```bash
python3 -m domain_architect --route-c
python3 -m domain_architect "Q_N[i,j] = 1/(gcd(i,j)*sqrt(i*j))"
python3 -m domain_architect --site
# then Inquiry → Load Route C face  (does not file into ChatVault)
```
