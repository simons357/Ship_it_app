# Proof chain — Yang–Mills mass gap

Slot **U** (Standard Model / gauge). Not Track B. Not Q.

```
python3 scripts/da_machine.py proof --problem YM
python3 scripts/da_machine.py next --ask "Yang mills and bad can you finish those"
```

SM lineage: [`DA-SM-LINEAGE.md`](DA-SM-LINEAGE.md).
Track B chain: [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md).

---

## Theorem (aimed)

For 4-dimensional quantum Yang–Mills with compact simple
gauge group, the Hamiltonian has a mass gap: the spectrum
on the vacuum-orthogonal subspace is bounded below by a
positive constant.

---

## Proof

**(1)** **Gauge field.** A connection on an \(SU(N)\) bundle,
curvature \(F\), Yang–Mills action \(\frac14\int\mathrm{Tr}\,F\wedge{*}F\).
*[have]*

**(2)** **SM block.** This desk’s Lagrangian contains working
YM: \(SU(3)_c\) (QCD) and \(SU(2)_L\) before the VEV.
Lineage runs both ways.
*[have]*

**(3)** **A piece is not a gap.** Local existence and energy
for classical YM are a different literature. The SM kinetic
term already sits. That is not (4).
*[have]*

**(4)** **Write.** Mass gap: the Hamiltonian spectrum on the
vacuum-orthogonal subspace is bounded below by a positive
constant.
*[the next write]*

**(5)** **Then.** If (4) sits, that gap is a theorem for this
YM theory. Still not NS. Still not Q. Still not Goldbach.
*[follows from (4)]*

---

## Track B beside it

“Yang–Mills and B” is two objects. B is classical NS.
Its leftover is still all-data integrable \(\mathcal{R}\)
(or A1 / A2 / a killing field). Emitting this chain does
not finish B. Emitting the SM YM block does not finish (4).

Machine: [`DA-PROOF.md`](DA-PROOF.md)
