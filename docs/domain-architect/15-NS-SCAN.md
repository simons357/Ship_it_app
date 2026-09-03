# Scan — leftover pieces, computer match, no weld

**Not a proof.** This is a **general** anatomy machine. Track B was the
worked example used to show it, not the only object it applies to.

If an object is weird and you do not know what it is — or you know the
object and one slot is empty — Domain Architect breaks itself down into
rudimentary pieces and **scans** for an equation that would actually fit.

Many views of one shape are still one object. A match is a candidate.
An empty scan is honest.

```bash
python -m domain_architect --scan      # the method, every book
python -m domain_architect --scan B    # worked example
python -m domain_architect --scan Q    # same machine, other object
python -m domain_architect --consult   # method tank (Weyl, Shannon, Hamming)
python -m domain_architect --consult B # fluids tank on the example
```

## The method

1. Name the views of one object.
2. Break DA into pieces (FRA slots, layers, inventory).
3. List leftover holes (order-1 changes the walk; order-2 is extra texture).
4. Computer-match. `LOOKS_LIKE_FIT` is not a weld. `WRONG_OBJECT` stays out.
5. Endpoint: **identified** from anatomy, or **smooth** if an order-1 hole fills.

## Worked example (Track B)

Three views of one object: the PDE (`NS-B`), packet mass (`J/X`), and
conditional SND (`SND-C`). Against `CLIP-T3-WELD`:

| Piece | Verdict | Fills? |
|---|---|---|
| T3a Young (cylinder) | `LOOKS_LIKE_FIT` | no — extra \(E\) |
| T5 \(I_{\mathrm{tube}}\) | `AFTER_NOT_FILL` | no |
| strain / Bernstein | `ALREADY_IN` | no |
| inverse-GCD, Cosmo, gravity, SFE | `WRONG_OBJECT` | no |

Identified: yes. Smooth: not yet.

## Same machine, other books

| Book | Order-1 leftover | Fluids pieces fill it? |
|---|---|---|
| Q | operator→ζ lemma | no — `WRONG_OBJECT` |
| SFE | canonical SFE unresolved | no |
| A / U | no order-1 weld of that kind | do not glue onto B |

The picture is on the see-desk (`see-scan.svg`). CosmoEvolution is not
this scan. After a scan, `--jigsaw B` puts the same pieces on a table
and classifies leftover holes as damage versus identity.
