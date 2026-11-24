"""Example built pasts, written to be read: each village's present as the build read it, a village's chronicle, and one family
traced back. `python -m cybertron2.peoplegen.examples` writes results/examples.md."""
from __future__ import annotations

import copy
import os

from cybertron2.engine import generate as GEN

from . import forward as FW
from . import present as PR
from . import solver as S
from . import write as WR
from .evaluate import MIXES, REGION
from .genealogy import Build


def build(spec, seed):
    b = Build(copy.deepcopy(spec), seed)
    S.solve(b, seed)
    N = WR.names(b)
    return b, N, WR.TreeView(b, N)


def rel(T, a, b):
    r = GEN.kin(T, a, b)
    return r[5:] if r else None


def head_of(b, h):
    ms = b.hh[h]["members"]
    if b.heads.get(h):
        return b.heads[h]
    men = [i for i in ms if b.P[i].sex == "m" and b.P[i].age >= 16 and b.P[i].unions]
    return max(men or ms, key=lambda i: b.P[i].age)


def households(b, N, T, village):
    out = []
    for h, d in b.hh.items():
        if d["village"] != village:
            continue
        hd = head_of(b, h)
        parts = [f"**{N[hd]}** {b.P[hd].age}"]
        for i in sorted(d["members"], key=lambda i: -b.P[i].age):
            if i != hd:
                parts.append(f"{N[i].split()[0]} {b.P[i].age} ({rel(T, N[hd], N[i]) or 'no kin of the head'})")
        out.append(f"- {h}: " + ", ".join(parts))
    return out


def origin(b, i, off):
    p = b.P[i]
    if p.came:
        return "came from outside the record"
    if p.pc is None:
        return "born before the record" if p.kind != "off" else f"of {off}"
    r = b.C[p.pc].res
    return f"born at {off}" if r == "OFF" else f"born at {r}"


def life(b, N, i, off):
    p = b.P[i]
    s = f"{N[i]} (b. {p.born}"
    if p.died is not None:
        s += f", d. {p.died} aged {p.died - p.born}, {p.cause}"
    elif p.fate:
        s += f", went to {off} in {p.fate[1]}"
    elif p.kind == "present":
        s += f", living, {p.age}, at {p.village}"
    elif p.kind == "off":
        s += f", of {off}"
    return s + ")"


def family(b, N, T, x, off):
    """x's parents, grandparents, siblings and spouse's people."""
    L = [f"**{N[x]}**, {b.P[x].age}, of {b.P[x].village}; {origin(b, x, off)}."]
    p = b.P[x]
    if p.pc:
        c = b.C[p.pc]
        L.append(f"- Parents: {life(b, N, c.f, off)} and {life(b, N, c.m, off)}, married {c.wed} at {c.res if c.res != 'OFF' else off}.")
        for q, who in ((c.f, "father's"), (c.m, "mother's")):
            qp = b.P[q]
            if qp.pc:
                g = b.C[qp.pc]
                L.append(f"- Their {who} side: {life(b, N, g.f, off)} and {life(b, N, g.m, off)}, at {g.res if g.res != 'OFF' else off}.")
            else:
                L.append(f"- The {who.replace(chr(39) + 's', '')} {N[q]}: {origin(b, q, off)}.")
        sibs = [k for k in c.kids if k != x]
        if sibs:
            L.append("- Brothers and sisters: " + "; ".join(life(b, N, k, off) for k in sorted(sibs, key=lambda k: b.P[k].born)) + ".")
    for cid in p.unions:
        c = b.C[cid]
        o = c.m if c.f == x else c.f
        what = "dead first " + ("wife" if p.sex == "m" else "husband") if c.ghost == x else ("wife" if p.sex == "m" else "husband")
        L.append(f"- {what.capitalize()}: {life(b, N, o, off)}, {origin(b, o, off)}; married {c.wed}.")
        op = b.P[o]
        if op.pc:
            g = b.C[op.pc]
            kin_living = [k for k in g.kids if k != o and b.P[k].kind == "present"]
            if kin_living:
                L.append(f"  - Her people living: " + ", ".join(f"{N[k]} at {b.P[k].village} ({rel(T, N[o], N[k])})" for k in kin_living) + "."
                         if p.sex == "m" else "  - His people living: " + ", ".join(f"{N[k]} at {b.P[k].village}" for k in kin_living) + ".")
        kids = sorted(c.kids, key=lambda k: b.P[k].born)
        if kids:
            L.append("  - Their children: " + "; ".join(life(b, N, k, off) for k in kids) + ".")
    return L


def chronicle(b, N, village, off, since=None):
    H = WR.history(b, N)
    keep = []
    names_here = {N[i] for i, p in b.P.items() if (p.kind == "present" and p.village == village)
                  or any(b.C[c].res == village for c in p.unions) or (p.pc and b.C[p.pc].res == village)}
    for h in H:
        if h["kind"] == "winter" and h["year"] >= b.F.get(village, -999) or (h["kind"] == "founding" and village in h["text"]):
            keep.append(h)
        elif set(h["who"]) & names_here and h["kind"] in ("marriage", "left", "founding"):
            keep.append(h)
        elif set(h["who"]) & names_here and h["kind"] == "death" and "cradle" not in h["text"] and "childhood" not in h["text"]:
            keep.append(h)
    return [f"- {h['year']}: {h['text']}" for h in keep if since is None or h["year"] >= since]


def world(title, spec, seed, village, n_fam=2, note=""):
    b, N, T = build(spec, seed)
    off = (b.off or {}).get("name", "beyond the map")
    L = [f"## {title}", ""]
    if note:
        L += [note, ""]
    L.append("Foundings (built): " + ", ".join(f"{v} {y}" for v, y in sorted(b.F.items(), key=lambda t: t[1])) + ".")
    L.append(f"Hard winters: {', '.join(str(y) for y in sorted(b.hard))}.")
    L += ["", f"### {village} now, as the build read each household (relation to the head)", ""]
    L += households(b, N, T, village)
    L += ["", f"### {village}'s chronicle (deaths of infants and young children left out)", ""]
    L += chronicle(b, N, village, off)
    heads = [head_of(b, h) for h, d in b.hh.items() if d["village"] == village]
    heads = sorted(heads, key=lambda i: -b.P[i].age)
    picks = [heads[len(heads) // 3], heads[-1]][:n_fam] if len(heads) > 1 else heads
    for x in picks:
        L += ["", f"### One family: {N[x]}", ""]
        L += family(b, N, T, x, off)
    return L, b, N, T


def truth_side_by_side(seed):
    """One forward household: who the truth says each person's parents are, and who the build says."""
    sim = FW.simulate(REGION, seed)
    spec = FW.to_input(REGION, sim)
    spec["hard_years"] = sorted(sim["hard"])
    b, N, T = build(spec, 1000 + seed)
    P = sim["P"]
    pres = set(sim["present"])
    rows = []
    for h, ms in sorted(sim["households"].items(), key=lambda t: -len(t[1])):
        if len(ms) < 6:
            continue
        for i in ms:
            tp = [x for x in (P[i]["father"], P[i]["mother"]) if x]
            tl = [f"{x} ({-P[x]['born']})" if x in pres else f"dead/away" for x in tp] or ["before the record"]
            c = b.C[b.P[i].pc] if b.P[i].pc else None
            bl = [f"{x} ({b.P[x].age})" if b.P[x].kind == "present" else "dead/away" for x in ((c.f, c.m) if c else ())] or ["came / before the record"]
            same = {x for x in tp if x in pres} == {x for x in ((c.f, c.m) if c else ()) if b.P[x].kind == "present"}
            rows.append(f"| {i} | {-P[i]['born']} | {P[i]['sex']} | {', '.join(tl)} | {', '.join(bl)} | {'yes' if same else 'no'} |")
        return h, rows
    return None, rows


def main():
    out = ["# Example built pasts", "",
           "Built by `cybertron2/peoplegen` (`python -m cybertron2.peoplegen.examples`). Years are counted back from now (0); the region has four "
           "village sites and an off-map market town, Kingsmarket. Names are keyed presentation; a surname follows the father.", ""]
    mix = MIXES["test_conditions"]
    spec = PR.draw(mix, 3)
    L, *_ = world("1. A world from a mix (the use case: nothing given but the mix)", spec, 3, "Northby",
                  note="The mix: 24 households in four villages; 3 widows alone, 2 stem households, 2 of three generations, "
                       "2 widowers with children, 2 single men, 1 brother and sister; the rest couples with children (80%) or old "
                       "couples (20%). The roles the forms name (head, spouse, widowed, ...) are pinned; everything else is built.")
    out += L + [""]
    spec2 = PR.draw(MIXES["default"], 11)
    L, *_ = world("2. Another mix, another seed", spec2, 11, "Westcot")
    out += L + [""]
    h, rows = truth_side_by_side(1)
    out += ["## 3. What \"the true parents\" means: one household of a forward test world", "",
            "Only in the test is there a true past: a forward simulation made this household, then everything but each person's age, "
            "sex and household was hidden, and the build made a past for it. 'Same' means the build named the same living parents "
            "as the simulation (a dead or away parent counts as matching any dead or away parent).", "",
            f"Household {h}:", "", "| Person | Age | Sex | True parents (age) | Built parents (age) | Same |", "|---|---|---|---|---|---|"] + rows
    path = os.path.join("proto", "peoplegen", "results", "examples.md")       # the prototype's results stay with its report
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
    print(path)


if __name__ == "__main__":
    main()
