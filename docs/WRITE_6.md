# WRITE (6)

**Status.** The estimate is stated. It is not proved.
**Tag.** H1 = WRITE (6) = Lemma I on the ball.
**Do not merge** with H, Lemma C, H2, or H3.

On \(Q_r\), Bad pairs only (\(|\omega|\ge\Lambda\) and \(|\sin\varphi|>C_*|x-y|^{1/2}\)):

\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

That is the write. It is not a theorem.

**Score of the write.** Aimed leftover: **yes**. Theorem: **no**.

- Bad pairs only, both ends in \(B_r\), kernel still \(|z|^{-3}\). Good / H2 / H3 are correctly off this line.
- Right-hand side matches the local identity: a slice of \(\iint|\nabla\omega|^2\phi\), plus the same \(r^{-2}\iint|\omega|^2\) Lemma C leaves. \(\nu/8\) is a conventional slice, not a sharp constant. Type I scaling of the three terms agrees (\(r^{-1}\)); there is no dimensional obstruction.
- \(A_{\mathrm{bad}}\) is defined with \(|\alpha_{\mathrm{bad}}^{\mathrm{loc}}|\). The identity only needs signed \(\alpha\). Absolute value is sufficient, not necessary. Signed \(D\) already failed for an isolated pair.
- The triple-integral form in [`H1-OBJECT.md`](H1-OBJECT.md) is a majorant (\(|D|\le C|\sin\varphi|\le C\)). Same leftover. Constants in \(|D|\) go into \(\nu/8\); the two displays are not identical symbols.
- Packet §5/§12 copies that omitted \(\phi\) on dissipation could not be absorbed into the left side of the identity. Those copies now match this file.

Kernel on Bad is still \(|z|^{-3}\). HLS gives local \(E^3\). Path-cost of \(\nabla\xi\) dies on a sheet or a gap.

Supported data (identities, literature, calculations that do **not** prove this): [`WRITE_6_SUPPORTED.md`](WRITE_6_SUPPORTED.md).
Glossary: [`H-SYSTEM.md`](H-SYSTEM.md).
