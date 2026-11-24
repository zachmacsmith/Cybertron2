"""The backward build as a world's people stage (generation_redesign.md §6; W-107).

A world that sets `population: {build: backward}` is given its people here instead of by the forward simulation. Everything else
about writing them into the world (kin, memories, a feud, debts, friendships, crafts, tools, models, aims, beds and stores) is
generate.py's own `spec_from_tree`, so the pipeline around it (landgen's two passes, the capacity and economy checks,
livelihoods.fill, the gate check, births in a run) runs unchanged.

    population:
      build: backward
      span: 80                     # years of history (default 80)
      households:                  # any household (a line) may be pinned, by members or by form
        Reed: {members: [{age: 42, sex: m, role: head}, {age: 38, sex: f, role: spouse}, {age: 9, sex: f}]}
        Croft: {form: widow_alone}
      forms: {couple_children: 0.7, couple_old: 0.1, three_generations: 0.2}   # the rest, by keyed draws (counts >= 1 exact)
      size: [3, 7]                 # household sizes for forms with children
      off: Kingsmarket             # an off-map place spouses and founders may come from: a node of the world, or a name
      off_days: 2                  # how far off it is, if it is not a node with roads
      found: {Northby: -60}        # a village's founding year, pinned

Households are the world's `lines`, each at the node its house stands in; villages are those nodes; distances between them are the
shortest road route in days. Every draw is keyed (keyed.py), so the same world and seed give the same people.
"""
from __future__ import annotations

import heapq

from cybertron2.engine import generate as GEN

from . import demog as D
from . import present as PR
from . import solver as S
from .genealogy import Build
from .keyed import pick, u
from .write import history

FORMS = {"couple_children": 0.7, "couple_old": 0.1, "three_generations": 0.2}   # the default mix (W-107, a default taken)
SPAN = 80                                                                         # years (Q-45 asks 80 or 200; a default taken)


def homes(base) -> dict:
    """{line: node id} from the house each line's household lives in (the first node if a line has none)."""
    nodes = base.get("nodes") or {}
    houses = {bid: b for bid, b in (base.get("buildings") or {}).items() if b.get("household") and (b.get("fittings") or {}).get("beds")}
    out = {}
    for line in base["lines"]:
        pid = next((h["parcel"] for _, h in sorted(houses.items()) if h["household"] == line), None)
        node = next((nid for nid, n in nodes.items() if pid in (n.get("parcels") or {})), None)
        out[line] = node or next(iter(nodes), "home")
    return out


def road_days(base, places) -> dict:
    """The shortest road route between each pair of places, in days ({"a|b": days}); a pair no road joins is left out (FAR)."""
    adj = {}
    for r in base.get("roads") or []:
        a, b, days = r[0], r[1], float(r[2])
        adj.setdefault(a, []).append((b, days))
        adj.setdefault(b, []).append((a, days))
    out = {}
    for s in sorted(places):
        dist, todo = {s: 0.0}, [(0.0, s)]
        while todo:
            d, x = heapq.heappop(todo)
            if d > dist.get(x, 1e18):
                continue
            for y, w in adj.get(x, ()):
                if d + w < dist.get(y, 1e18):
                    dist[y] = d + w
                    heapq.heappush(todo, (d + w, y))
        for t in sorted(places):
            if t != s and t in dist:
                out[f"{s}|{t}"] = round(dist[t], 3)
    return out


def present(base, seed, home, pop) -> list:
    """The households now: each pinned one as written (members, or a form), the rest drawn from the mix by keyed draws."""
    pins = pop.get("households") or {}
    forms = pop.get("forms") or FORMS
    size = pop.get("size") or [3, 7]
    lines = sorted(base["lines"])
    form_of = {}
    for line in lines:
        if (pins.get(line) or {}).get("form"):
            form_of[line] = pins[line]["form"]
    free = [line for line in lines if line not in form_of and not (pins.get(line) or {}).get("members")]
    for f, n in sorted(forms.items()):                                       # counts first, into keyed households
        if n >= 1:
            for k in range(int(n)):
                open_ = [line for line in free if line not in form_of]
                if open_:
                    form_of[pick(seed, ("population", "slot", f, k), [(line, 1.0) for line in open_])] = f
    shares = [(f, n) for f, n in sorted(forms.items()) if n < 1] or [("couple_children", 1.0)]
    for line in free:
        form_of.setdefault(line, pick(seed, ("population", "form", line), shares))
    out = []
    for line in lines:
        pin = pins.get(line) or {}
        ms = [dict(m) for m in pin["members"]] if pin.get("members") else PR.household(seed, line, form_of[line], size)
        for k, m in enumerate(ms):
            m["id"] = m.get("id") or f"{line}.{k}"
        out.append({"id": line, "village": home[line], "form": form_of.get(line, "pinned"), "members": ms})
    return out


def head_of(b, h):
    """A household's head when none is pinned: its eldest adult man, else its eldest adult (as spec_from_tree chooses)."""
    ms = [i for i in b.hh[h]["members"] if b.P[i].age >= 18]
    men = [i for i in ms if b.P[i].sex == "m" and b.P[i].age < 60]
    return max(men or ms or b.hh[h]["members"], key=lambda i: (b.P[i].age, i))


def lines_of(b, heads) -> dict:
    """{person id: (line, line born)}: the living belong to their household's line; everyone was born into their father's line.
    A line is named by the household its head heads (the eldest head of the line first), else by the household of its eldest
    living man, else it is an old line with a keyed name (one that died out)."""
    P, C = b.P, b.C
    father = {i: (C[p.pc].f if p.pc else None) for i, p in P.items()}
    root = {}

    def top(i, depth=0):
        if i in root:
            return root[i]
        f = father.get(i)
        r = top(f, depth + 1) if f and depth < 40 and P[f].kind != "off" else (i if P[i].sex == "m" else None)
        root[i] = r
        return r

    for i in P:
        top(i)
    named = {}
    for h, i in sorted(heads.items(), key=lambda t: (P[t[1]].born, t[0])):    # a head's line is his household's
        r = root.get(i) if P[i].sex == "m" else None
        if r and r not in named and h not in named.values():
            named[r] = h
    for i, p in sorted(P.items(), key=lambda t: (t[1].born if t[1].born is not None else 0, t[0])):
        r = root.get(i)
        if p.kind == "present" and p.sex == "m" and r and r not in named and p.hh not in named.values():
            named[r] = p.hh                                                   # the eldest living man of a line names it
    used = set(named.values()) | {p.hh for p in P.values() if p.hh}
    out = {}
    for i, p in P.items():
        r = root.get(i)
        if r and r not in named:
            k = int(u(b.seed, "old line", r) * len(OLD_LINES))
            name = next((OLD_LINES[(k + j) % len(OLD_LINES)] for j in range(len(OLD_LINES)) if OLD_LINES[(k + j) % len(OLD_LINES)] not in used),
                        f"{OLD_LINES[k]} {r}")
            named[r] = name
            used.add(name)
        born = named.get(r) if r else None
        if p.kind == "present":
            line = p.hh
        else:
            husband = next((C[c].f for c in p.unions if C[c].m == i), None)
            line = named.get(root.get(husband)) if p.sex == "f" and husband and root.get(husband) else born
        out[i] = (line or born, born or line)
    return out


OLD_LINES = ["Ashdown", "Holt", "Fenn", "Brook", "Hale", "Pike", "Shaw", "Webb", "Slade", "Hurst", "Lane", "Ford", "Ridley", "Coombe",
             "Dene", "Garth", "Kemp", "Lyle", "Marlow", "Nash", "Oakes", "Pryor", "Rowe", "Sayer", "Tull", "Vane", "Wick", "Yarrow"]


def given_names(b, pinned) -> dict:
    """{person id: a unique given name}: pinned names first, then the living, then the dead; past the lists, "the younger"."""
    P = b.P
    out, used = {}, set()
    for i, n in sorted(pinned.items()):
        out[i] = n
        used.add(n)
    order = sorted((i for i in P if i not in out),                            # the off-map people last (the history names them)
                   key=lambda i: (P[i].kind == "off", P[i].kind != "present", -(P[i].born if P[i].born is not None else 0), i))
    for i in order:
        pool = GEN.MALE if P[i].sex == "m" else GEN.FEMALE
        k = int(u(b.seed, "given name", i) * len(pool))
        cands = [pool[(k + j) % len(pool)] for j in range(len(pool))]
        n = next((c for c in cands if c not in used), None)
        n = n or next((f"{c} the younger" for c in cands if f"{c} the younger" not in used), None)
        n = n or next((f"{c} the elder" for c in cands if f"{c} the elder" not in used), None)
        n = n or f"{cands[0]} {i}"
        out[i] = n
        used.add(n)
    return out


class TreeView:
    """generate.Tree's shape over the build, in years (0 now): what spec_from_tree and generate.kin read. People of the off-map
    place are left out (as generate.py leaves out an outside spouse's parents); their children name the place as their origin."""

    def __init__(self, b, N, lines, off_name, villages):
        P, C = b.P, b.C
        self.p = {}
        for i, p in P.items():
            if p.kind == "off":
                continue
            c = C.get(p.pc) if p.pc else None
            par = [N[x] for x in ((c.f, c.m) if c else ()) if P[x].kind != "off"]
            mates = [(C[cid].m if C[cid].f == i else C[cid].f) for cid in p.unions]
            living = [m for m in mates if P[m].kind == "present"]
            partner = (living or mates[-1:] or [None])[-1]
            here = p.village if p.kind == "present" else next((C[cid].res for cid in p.unions), None)
            born_at = b.born_at(i)
            line, line_born = lines[i]
            origin = None
            if born_at == "OFF":
                origin = off_name
            elif born_at and born_at not in ("came", here) and born_at in villages:
                origin = born_at
            elif born_at == here and p.unions and line_born and line_born != line:
                origin = f"the {line_born} house"                            # married from another house of the same village
            x = {"name": N[i], "sex": p.sex, "born": p.born, "died": p.died, "cause": p.cause, "parents": par,
                 "partner": N[partner] if partner and P[partner].kind != "off" else None, "line": line, "origin": origin,
                 "children": [N[k] for cid in p.unions for k in C[cid].kids if P[k].kind != "off"], "left": p.fate[1] if p.fate else None}
            if line_born and line_born != line:
                x["line_born"] = line_born
            self.p[N[i]] = x

    def age(self, n, year=0):
        return year - self.p[n]["born"]

    def alive(self, n, year=0):
        x = self.p[n]
        return x["born"] <= year and (x["died"] is None or x["died"] > year) and (x["left"] is None or x["left"] > year)


def build(base: dict, seed: int) -> dict:
    """The world's people by the backward build, written as generate.build writes them. Refuses (RuntimeError) only when a pin
    cannot be met, naming the pins."""
    pop = dict(base.get("population") or {})
    home = homes(base)
    nodes = base.get("nodes") or {}
    village_name = {nid: (n.get("name") or nid) for nid, n in nodes.items()}
    off = pop.get("off")
    ids = sorted(set(home.values()))
    days_id = road_days(base, ids + ([off] if off and off in nodes else []))
    villages = sorted(village_name.get(v, v) for v in ids)                  # the build works in the villages' names, as the
    home = {line: village_name.get(v, v) for line, v in home.items()}       # history is told
    days = {"|".join(village_name.get(x, x) for x in k.split("|")): d for k, d in days_id.items()}
    if off:
        for v in ids:
            d = days_id.get(f"{v}|{off}") if off in nodes else float(pop.get("off_days", 2.0))
            days[f"{village_name.get(v, v)}|OFF"] = d if d is not None else D.FAR
    span = int(pop.get("span") or SPAN)
    hh = present(base, seed, home, pop)
    found = {village_name.get(v, v): int(y) for v, y in (pop.get("found") or {}).items()}   # pinned by node id or by name
    spec = {"villages": {v: {} for v in villages}, "distances": days, "off": {"name": village_name.get(off, off)} if off else None,
            "span": span, "households": hh, "pins": {"found": found}}
    b = Build(spec, seed)
    try:
        assign, st = S.solve(b, seed)
    except S.Refusal as e:
        raise RuntimeError(f"the population cannot be met: {e}") from e
    pinned_names = {m["id"]: m["name"] for h in hh for m in h["members"] if m.get("name")}
    N = given_names(b, pinned_names)
    heads = {h["id"]: next((m["id"] for m in h["members"] if m.get("role") == "head"), None) for h in hh}
    heads = {h: i or head_of(b, h) for h, i in heads.items()}
    lines = lines_of(b, heads)
    off_name = village_name.get(off, off) if off else None
    T = TreeView(b, N, lines, off_name, set(villages))
    hist = [h for h in history(b, N) if all(w in T.p for w in h.get("who") or [])]
    heads = {h: N[i] for h, i in heads.items() if i}
    generated = {"seed": seed, "build": "backward", "span": span, "foundings": dict(sorted(b.F.items())),
                 "budded_from": dict(sorted(b.mother.items())),
                 "forms": {h["id"]: h["form"] for h in hh}, "decisions": st["decisions"], "backjumps": st["backjumps"]}
    return GEN.spec_from_tree(base, seed, T, hist, generated, heads=heads, living_partners=True, close_kin=True)
