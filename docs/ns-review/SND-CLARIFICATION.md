# Clarification — SND status

**16 September 2026. Shared target. Theorem H stays withdrawn.**

The original Theorem H is withdrawn.  
The repaired shell estimate **A.2** may be retained.  
The current **A.3** inequality does not yet prove that the peak fraction \(\rho=J/X\) cannot collapse, because it gives the **wrong-sided** derivative information for that purpose (\(D^+\rho\) ceiling, not a floor).

The single remaining SND question is:

\[
\boxed{
X(t)\le M,\quad \rho(0)\ge\rho_*
\quad\Longrightarrow?\quad
\rho(t)\ge\frac{\rho_*}{2}
\text{ for }0\le t\le T(M,\nu,\rho_*).
}
\]

To answer it, derive a correctly oriented **lower** comparison inequality for \(\rho\) from the exact shell equation, using an explicitly indexed low-high, high-low, and high-high paraproduct decomposition.

Do **not** repair Theorem H again. Test this persistence statement directly.

If the comparison closes, that is a **conditional local SND-persistence** result.  
If it fails, name the paraproduct obstruction and test whether the persistence statement itself is false.

**Answer (16 Sep, this page’s working note):** the comparison does not close. Closing with \(A.2\) leaves an unbounded \(4^{j_*}\) leftover. Independently, statement (P) is **false** on unforced shears (Family H, \(F_j\equiv 0\)) for every \(\rho_*\in(0,1)\). There is no conditional local SND-persistence under only \((M,\nu,\rho_*)\). Do not repair Theorem H.

Working page: [`SND-PERSISTENCE.md`](./SND-PERSISTENCE.md).  
Arithmetic: `python3 scripts/snd_persistence_test.py`.
