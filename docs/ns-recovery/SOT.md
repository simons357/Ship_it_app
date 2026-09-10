# SoT — centered drift / same-shell packet

**Locked:** 10 September 2026  
**This file is the source of truth** for the packet line. Longer notes do not override it.

Navier–Stokes is **not solved**. The uniform triadic bound is **open**.

---

## Locked

Fixed-gap spheres \(S_n\cup S_{n+d}\). This is a **packet**, not an AP.

- \(D_s\) comes from the **gap** \(d\), not from a width.
- Mixed closures of type \((n,n,n+d)\) are only \(O(m)\), not \(O(m^2)\). Checked: 48 closures at \(n=9\) (\(m=54\)); 288 at \(n=89\) (144+120 keys).
- \(\mathcal R_\star\) falls with \(n\) (0.11 → 0.031). It does **not** track \(m^{1/2}\).
- The **natural same-shell ensemble is not a kill**.

The \(O(1)\) gap is available in this model, and that still does not produce \(\mathcal R_\star\sim m\).

---

## Remaining packet falsifier

A **designed** subset of two fixed-gap shells with \(\Theta(m^2)\) closures **and locked phases** — not the full sphere. Until that object is built and \(\mathcal R_\star\) tracks \(m\), the aligned-closure heuristic stays false on the natural ensemble.

Isolated triangles, wide APs, narrow APs, and full adjacent spheres: **no kill**.

---

## Do not write

- Do not treat full lattice spheres as an additive basis of density \(\Theta(m^2)\).
- Do not restore an AP-width \(D_s\) for this construction.
- Do not claim a uniform triadic bound or Clay regularity from this ensemble.
- Do not invent a \(\mathfrak T_c\) formula that is not filed. \(\mathcal R_\star\) values above are locked as reported; the ratio’s definition is still not in git.

---

## Other live writing

H1 on the cylinder is the other live track if the packet line is shelved. It is **not** started by this lock.

---

## Pointers (do not override)

| File | Role |
|---|---|
| `scripts/same_shell_packet_probe.py` | Combinatorial probe (keys, mixed closures, two-mass \(D_s\)) |
| `tests/test_same_shell_packet.py` | Locks 48 / 288 / \(d=2\) zeros / \(O(m)\) not \(O(m^2)\) |
| `docs/ns-recovery/SAME-SHELL-PACKET-NOTE.md` | Expanded packet note |
| `docs/ns-recovery/CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md` | Prior-source recovery; exact Stokes-moment paste still missing |
