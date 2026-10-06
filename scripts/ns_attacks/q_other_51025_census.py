"""Census (5,10,25) and coupling channels into (5,8,25) Q^other.

Standard library only. Not a class bound. Not (17).
"""
from fractions import Fraction as F
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


def oriented_triples(a, b, c):
    sa, sb = lattice_shell(a), lattice_shell(b)
    triples = []
    for p in sa:
        for qq in sb:
            r = neg(addk(p, qq))
            if radius(r) == c:
                triples.append((p, qq, r))
    return triples, lattice_shell(a), lattice_shell(b), lattice_shell(c)


# Blocks from the t^6 jet
t5825, s5, s8, s25 = oriented_triples(5, 8, 25)
t51025, _, s10, _ = oriented_triples(5, 10, 25)

set5, set8, set10, set25 = set(s5), set(s8), set(s10), set(s25)

# Modes of radius 10 that appear as B-output into a (5,8,25) slot:
# B(p,q) lands on k with p+q=k, and k is on {5,8,25}, with at least one of p,q on shell 10.
feed_into_5825 = []
for k in list(set5) + list(set8) + list(set25):
    for p in s10:
        q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
        rq = radius(q)
        if rq == 0:
            continue
        # partner on any shell; tag if partner is in joint support or outside
        tag = (
            "partner_in_5825"
            if q in set5 or q in set8 or q in set25
            else ("partner_in_51025" if q in set10 or q in set5 or q in set25 else "partner_outside")
        )
        # refine partner_in_51025 vs joint
        if q in set5 or q in set25:
            if q in set8:
                tag = "partner_in_5825"
            else:
                tag = "partner_shared_5_or_25"
        if q in set10:
            tag = "partner_on_10"
        if q in set8:
            tag = "partner_on_8"
        feed_into_5825.append({"k": k, "k_r2": radius(k), "from_10": p, "partner": q, "partner_r2": rq, "tag": tag})

# Unique (k, from_10) with partner on {5,8,10,25}
joint_partners = [
    row
    for row in feed_into_5825
    if row["partner_r2"] in (5, 8, 10, 25)
]
outside_partners = [
    row for row in feed_into_5825 if row["partner_r2"] not in (5, 8, 10, 25) and row["partner_r2"] > 2
]
low_partners = [row for row in feed_into_5825 if 0 < row["partner_r2"] <= 2]

# Shared geometric fact: shells 5 and 25 appear in both blocks
shared_shells = [5, 25]
only_5825 = [8]
only_51025 = [10]
joint_support = [5, 8, 10, 25]

# Count unique k on 5825 hit by some 10-input pair with partner in joint support
hit_ks = sorted({(row["k"], row["k_r2"]) for row in joint_partners})

# Also: B from (5,8) can land on 10? (generation of the other block)
gen10 = []
for p in s5:
    for qq in s8:
        k = addk(p, qq)
        if radius(k) == 10:
            gen10.append({"p": p, "q": qq, "k": k})

# B from (5,10) land on 8?
gen8 = []
for p in s5:
    for qq in s10:
        k = addk(p, qq)
        if radius(k) == 8:
            gen8.append({"p": p, "q": qq, "k": k})

payload = {
    "blocks": {
        "5_8_25": {
            "oriented_triples": len(t5825),
            "shell_counts": {"5": len(s5), "8": len(s8), "25": len(s25)},
            "viscous_rate": "38 nu",
        },
        "5_10_25": {
            "oriented_triples": len(t51025),
            "shell_counts": {"5": len(s5), "10": len(s10), "25": len(s25)},
            "viscous_rate": "40 nu",
            "T_formula": "T=(25-10)Ip+(5-25)Iq+(10-5)Ir=15 Ip -20 Iq +5 Ir",
        },
    },
    "joint_support_squared_radii": joint_support,
    "shared_shells": shared_shells,
    "Q_other_channels_into_5825_from_shell_10": {
        "pairs_with_partner_in_joint_support": len(joint_partners),
        "pairs_with_partner_low_le_2": len(low_partners),
        "pairs_with_partner_outside_joint_high": len(outside_partners),
        "distinct_5825_targets_hit_by_joint": len(hit_ks),
        "sample_joint": joint_partners[:6],
        "sample_outside": outside_partners[:6],
    },
    "cross_generation": {
        "B_from_5_and_8_to_radius_10": len(gen10),
        "B_from_5_and_10_to_radius_8": len(gen8),
        "sample_5_8_to_10": gen10[:4],
        "sample_5_10_to_8": gen8[:4],
    },
    "scope": "lattice coupling census for Q^other between (5,8,25) and (5,10,25); not a bound",
}

Path(__file__).with_name("Q-OTHER-51025-CENSUS.json").write_text(
    json.dumps(payload, indent=2) + "\n"
)
print(json.dumps(payload, indent=2))
