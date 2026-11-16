"""The built past as generate.py writes it (spec["tree"], spec["history"], spec["agents"] with kin and memories), so a world can
take it in place of the forward-and-reject lineage. Names are presentation: keyed by each person's id, a surname down the male line."""
from __future__ import annotations

from cybertron2.engine import generate as GEN

from .keyed import u

SURNAMES = ["Reed", "Thatcher", "Miller", "Ashdown", "Holt", "Fenn", "Brook", "Carter", "Hayward", "Wood", "Croft", "Marsh",
            "Hale", "Pike", "Shaw", "Tanner", "Webb", "Cole", "Moor", "Slade", "Hurst", "Lane", "Ford", "Ridley"]


def names(b) -> dict:
    """{person id: unique name}: a given name keyed by id, a surname from the father's line (or keyed for a line's first man)."""
    P, C = b.P, b.C
    sur = {}

    def surname(i, depth=0):
        if i in sur:
            return sur[i]
        p = P[i]
        c = C.get(p.pc) if p.pc else None
        if c and depth < 12:
            s = surname(c.f, depth + 1)
        else:
            s = SURNAMES[int(u(b.seed, "surname", i) * len(SURNAMES))]
        sur[i] = s
        return s

    out, used = {}, set()
    for i in sorted(P, key=lambda i: (P[i].born if P[i].born is not None else 0, i)):
        pool = GEN.MALE if P[i].sex == "m" else GEN.FEMALE
        k = int(u(b.seed, "name", i) * len(pool))
        s = surname(i)
        for j in range(len(pool)):
            n = f"{pool[(k + j) % len(pool)]} {s}"
            if n not in used:
                break
        else:
            n = f"{pool[k]} {s} {i}"
        used.add(n)
        out[i] = n
    return out


class TreeView:
    """generate.Tree's shape over the build, for generate.kin."""

    def __init__(self, b, N):
        self.p = {}
        for i, p in b.P.items():
            c = b.C.get(p.pc) if p.pc else None
            partner = None
            for cid in reversed(p.unions):
                o = b.C[cid].m if b.C[cid].f == i else b.C[cid].f
                partner = N[o]
                if b.P[o].kind == "present":
                    break
            self.p[N[i]] = {"name": N[i], "sex": p.sex, "born": p.born, "died": p.died, "cause": p.cause,
                            "parents": [N[c.f], N[c.m]] if c else [], "partner": partner, "line": N[i].split(" ")[1],
                            "origin": c.res if c else ("came" if p.came else None), "children": [N[k] for cid in p.unions for k in b.C[cid].kids],
                            "left": p.fate[1] if p.fate else None}


def history(b, N) -> list:
    off = (b.off or {}).get("name", "beyond the map")
    where = lambda r: off if r == "OFF" else r
    H = []
    for v, F in sorted(b.F.items(), key=lambda t: t[1]):              # the first couple to settle, dated when they settled
        start = lambda c: max(F, min([c.wed] + [b.P[k].born for k in c.kids] if c.wed is not None else [b.P[k].born for k in c.kids]))
        cs = sorted([c for c in b.C.values() if c.res == v and c.kids], key=lambda c: (start(c), c.id))[:1]
        for c in cs:
            o = b.born_at(c.f)
            frm = f" from {where(o)}" if o not in (None, "came", v) else " from elsewhere" if o in (None, "came") else ""
            bud = f", the first house beyond {b.mother[v]}'s fields" if v in b.mother and o == b.mother[v] else ""
            H.append({"year": start(c), "kind": "founding", "who": [N[c.f], N[c.m]],
                      "text": f"{N[c.f]} and {N[c.m]} came to {v}{frm} and built its first house{bud}"})
    for c in b.C.values():
        if c.wed is not None and c.res != "OFF":
            o = lambda q: (b.C[b.P[q].pc].res if b.P[q].pc else None)
            ow = o(c.m)
            at = f" at {c.res}" if c.wed >= b.F.get(c.res, -999) else ""          # before the village was there: married elsewhere
            text = f"{N[c.f]} married {N[c.m]}" + (f" of {where(ow)}" if ow and ow != c.res else "") + at
            H.append({"year": c.wed, "kind": "marriage", "who": [N[c.f], N[c.m]], "text": text})
    for i, p in b.P.items():
        if p.died is not None and (p.kind != "fill" or p.died - p.born >= 5):
            H.append({"year": p.died, "kind": "death", "who": [N[i]], "text": f"{N[i]} died ({p.cause})"})
        if p.fate:
            H.append({"year": p.fate[1], "kind": "left", "who": [N[i]], "text": f"{N[i]} went to {off}"})
    for y in sorted(b.hard):
        H.append({"year": y, "kind": "winter", "who": [], "text": "a hard winter: the frost came early and the stores ran out"})
    return sorted(H, key=lambda h: (h["year"], h["kind"], h["text"]))


def spec(b, lifespan=None, years=False) -> dict:
    """years=True writes memories in years ago (to read); the default is the engine's winters (D2-153's compressed calendar)."""
    N = names(b)
    T = TreeView(b, N)
    L = lifespan or GEN.LF.lifespan()
    date = lambda y: None if y is None else -int(round(GEN.to_days(-y, L)))
    hist = history(b, N)
    ago = (lambda n: "last year" if n <= 1 else f"{n} years ago") if years else (lambda n: GEN.winters(n, L))
    agents = {}
    for i, p in sorted(b.P.items()):
        if p.kind != "present":
            continue
        n = N[i]
        a = {"household": p.hh, "born": GEN.born_day(p.age, L), "stage": GEN.stage(p.age, L), "sex": p.sex, "relations": {}, "memories": []}
        if T.p[n]["parents"]:
            a["parents"] = T.p[n]["parents"]
        if T.p[n]["partner"] and b.P[[k for k, v in N.items() if v == T.p[n]["partner"]][0]].kind == "present":
            a["partner"] = T.p[n]["partner"]
        if p.role == "head" or b.heads.get(p.hh) is None and i == max(b.hh[p.hh]["members"], key=lambda j: (b.P[j].age >= 16 and b.P[j].sex == "m", b.P[j].age)):
            a["role"] = "head"
        agents[n] = a
    for n, a in agents.items():
        for m in T.p:
            if m == n:
                continue
            r = GEN.kin(T, n, m)
            if m in agents:
                a["relations"][m] = r or f"of the {agents[m]['household']} household"
            elif r and T.p[m]["died"] is not None and T.p[m]["died"] - T.p[n]["born"] >= 6 and r.split()[-1] in (
                    "father", "mother", "son", "daughter", "brother", "sister", "husband", "wife", "grandfather", "grandmother"):
                a["memories"].append(f"{r[5:].capitalize()} {m} died {ago(-T.p[m]['died'])} ({T.p[m]['cause']}).")
        seen = [ago(-y) for y in sorted(b.hard) if y - T.p[n]["born"] >= 6]
        if seen:
            a["memories"].insert(0, "Hard winters you remember: " + ", ".join(dict.fromkeys(seen)) + ".")
        a["memories"] = a["memories"][-8:]
    tree = [{**p, "born": date(p["born"]), "died": date(p["died"]), "left": date(p["left"])} for p in T.p.values()]
    return {"tree": tree, "history": [{**{k: v for k, v in h.items() if k != "year"}, "day": date(h["year"]), "year": h["year"]} for h in hist],
            "agents": agents}
