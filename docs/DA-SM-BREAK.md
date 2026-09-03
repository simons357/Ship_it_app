# Break \(\mathcal{L}_{\mathrm{SM}}\), then put it back

`python3 scripts/da_machine.py smbreak`

Five poster blocks were a printing. DA opened them until the
pieces stopped being sums of other pieces, then rebuilt.

This is still slot U. Not a unifier. Tracks A, B, Q untouched.

---

## Down

Six trunks, not five blocks:

| Trunk | What is in it |
|---|---|
| principles | spacetime, gauge principle, representations, dim ≤ 4, three copies |
| gauge group | \(SU(3)\times SU(2)\times U(1)\) — three factors |
| fields | gluons, \(W\), \(B\), Higgs doublet, quarks, leptons, ghosts |
| operators | \(F^2\), \(\lvert DH\rvert^2\), \(V(H)\), \(\bar\psi iD\psi\), Yukawa, \(\theta F\tilde F\), ghosts |
| parameters | \(g_s,g,g',v,\lambda,y_{ij},\mathrm{CKM},\theta_{\mathrm{QCD}}\) — all consumed |
| not in \(\mathcal{L}\) | \(G_N\), \(\Lambda\), dynamical \(g_{\mu\nu}\), \(\nu\) masses |

Leaves are the atoms. Parameters **fail** as outputs: they
went in. \(G\) and \(\Lambda\) **fail** as SM fields. Ghosts
**pass** as bookkeeping. Three generations stay **open** as
a copy, not a derivation.

---

## Back

1. Spacetime + gauge principle + \(G\) → covariant derivative and three \(F_{\mu\nu}\).
2. Assign the SM representations → a **finite** list of dim-4 operators.
3. Write every allowed dim-4 operator → \(\mathcal{L}_{\mathrm{SM}}\), up to numbers.
4. Drop ghosts → same classical equations.
5. Paste the measured couplings → working SM, three forces, no gravity.
6. Replace \(\eta\) by \(g\), add Einstein–Hilbert \(+\Lambda\) →

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G\,T_{\mu\nu}[\mathrm{SM}].
\]

7. Ask the rebuilt \(\mathcal{L}\) to output \(g_s\), \(\theta_W\), \(G\), \(\Lambda\) → **fail**.

Step 3 is the uniqueness. The poster *is* that list, written
in components after symmetry breaking. Step 6 is the
two-sided couple. Step 7 is why this is not nature4.

---

## Drop one

| Drop | Still the SM? |
|---|---|
| \(SU(3)\), \(SU(2)\), \(U(1)\), Higgs, dim-4, 3 families | no |
| ghosts | yes (classical) |
| \(G_N\) | yes (SM never had it); universe model loses gravity |

---

Winding those atoms backwards through Maxwell, QED, Fermi,
Yang–Mills, GWS, and QCD is [`docs/DA-SM-LINEAGE.md`](DA-SM-LINEAGE.md).

Stop inventing new atoms inside \(\mathcal{L}_{\mathrm{SM}}\).
A producing-map has to live **outside** this list. Fluids
stay on Track B.
