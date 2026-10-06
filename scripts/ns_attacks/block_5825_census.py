"""Exact (5,8,25) scalene block: lattice triangles, T from (7), Q-split.

Not a class bound. Not (17). Standard library only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from math import isqrt

src = Path(__file__).with_name("c10_full_local_exact_checks.py").read_text()
exec(src[: src.index("triad=field(")], globals())


def radius(k):
    return sum(t * t for t in k)


def lattice_shell(r2):
    R = isqrt(r2) + 1
    out = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if x * x + y * y + z * z == r2:
                    out.append((x, y, z))
    return out


def addk(p, q):
    return tuple(a + b for a, b in zip(p, q))


def neg(k):
    return tuple(-t for t in k)


A, B, C = 5, 8, 25
sa, sb, sc = lattice_shell(A), lattice_shell(B), lattice_shell(C)

def I_currents(u, triples_):
    """I_p, I_q, I_r on the same indexed set as FOURIER-TRIANGLE (7)."""
    z = [Q()] * 3
    Ip = Iq = Ir = F(0)
    for p, qq, r in triples_:
        up, uq, ur = u.get(p, z), u.get(qq, z), u.get(r, z)
        Ip += (dot(qq, up) * dot(uq, ur)).i
        Iq += (dot(r, uq) * dot(ur, up)).i
        Ir += (dot(p, ur) * dot(up, uq)).i
    return Ip, Iq, Ir


def T_abc(u, triples_):
    Ip, Iq, Ir = I_currents(u, triples_)
    return (C - B) * Ip + (A - C) * Iq + (B - A) * Ir


# Oriented triples p+q+r=0 with |p|^2=5, |q|^2=8, |r|^2=25.
triples = []
for p in sa:
    for qq in sb:
        r = neg(addk(p, qq))
        if radius(r) == C:
            triples.append((p, qq, r))

# Unique unordered geometric triangles (sort vectors)
shapes = []
seen = set()
for p, qq, r in triples:
    key = tuple(sorted((p, qq, r)))
    if key not in seen:
        seen.add(key)
        shapes.append((p, qq, r))


# Vacuous field on the three shells only: zero T.
empty = {}
assert T_abc(empty, triples) == 0

# Count
payload = {
    "block": [A, B, C],
    "shell_counts": {"5": len(sa), "8": len(sb), "25": len(sc)},
    "oriented_triples_pqr_sum0": len(triples),
    "unordered_triangles": len(shapes),
    "sample_triangles": [{"p": p, "q": qq, "r": r} for p, qq, r in shapes[:8]],
    "identity": "T_abc=(c-b)I_p+(a-c)I_q+(b-a)I_r  with a=5,b=8,c=25",
    "viscous_rate": "nu*(5+8+25)=38 nu",
    "scope": "lattice census + (7) wiring; not a bound on Q",
}

Path(__file__).with_name("BLOCK-5825-CENSUS.json").write_text(
    json.dumps(payload, indent=2) + "\n"
)
print(json.dumps(payload, indent=2))
