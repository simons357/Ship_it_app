# Packet: B42 T2 starvation first-order coefficient

29 September 2026.
Independent analysis of the rationalized 20-row quotient.
Locked-r2 identity unverified. NS not solved.

Working page: [`docs/B42-T2-STARVATION-FIRST-ORDER-COEFFICIENT.md`](../docs/B42-T2-STARVATION-FIRST-ORDER-COEFFICIENT.md)

## Frozen statement

On the B39 T2 ray, after factoring \(t^{1/2}\),

\[
\lim_{t\downarrow 0}\frac{1-\Gamma(t)}{t}
=
\frac{m_J(C)}{C_K}.
\]

If the JSON integer identities hold, \(m_J=D_A\) constantly on \(Z_K\)
and the limit is \(D_A/C_K\),

\[
D_A
=
\frac{C_{14}+C_{15}+C_{18}+C_{19}+3(C_{16}+C_{17})}{2}.
\]

This improves B41’s \(\Theta(t)\) to an exact first-order asymptotic
for the rationalized quotient only.

## Independent checks in this packet

- First-order limit argument (no Hessian, no unique minimiser).
- Two-row four-cycle bound \(F_{15,16}\) with relative phase \(\pi/3\).
- Cosines of the stated \(\pi/12\) residues, and the shape of \(D_A\).
- Integer identities freeze weak phases on \(Z_K\) (synthetic matrix).
- Sprint 01 parallelogram 20-row incidence is **not** those identities.

## Not checked here

- The six identities on the hashed Library JSON
  `87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898`
  (file not in this checkout).
- Certificate \(y_A\) against that JSON.
- Locked `M.tsv` / `b_exact.tsv`.
- Canonical r2 identity.
- Symmetrized coefficient convention.

## Not claimed

No trajectory. No drag reduction. No Serrin/BKM last line.
No de-augmentation of \(Q_1\). No RH. Classical NS remains open.

```bash
PYTHONPATH=scripts python3 -m unittest tests.test_b42_t2_coefficient -q
PYTHONPATH=scripts python3 scripts/run_b42_t2_coefficient.py
```

Payload: `results/b42_t2_starvation_coefficient.json`.
