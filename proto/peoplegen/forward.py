"""The forward reference: the region simulated year by year from one founded village, with the same tables the backward build
reads (demog.py). It gives (a) a present population to pin, with its true past to compare against, and (b) the reference
statistics a backward-built past should match.

Households: a couple founds its own household on marrying if the village has room (cap), else, if a site is left, founds a new
village with chance FOUND, else stays in the husband's parents' household. Wives move to the husband's village (patrilocal); a woman
with no man to be had may marry a man from the off-map node, who moves in. Unmarried people of 16 to 30 leave for the off-map node
at LEAVE a year. Orphaned children move to kin in the village."""
from __future__ import annotations

import math

from . import demog as D
from .keyed import pick, u


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def anc2(P, x):
    """x, its parents and grandparents."""
    out = {x}
    for p in (P[x]["father"], P[x]["mother"]):
        if p:
            out.add(p)
            for q in (P[p]["father"], P[p]["mother"]):
                if q:
                    out.add(q)
    return out


def simulate(region: dict, seed: int, span=100, founders=6, cap=8) -> dict:
    sites = region["villages"]                                       # {name: {"at": [x, y]}}, the first is founded at -span
    off = region.get("off")                                          # {"name": ..., "at": [x, y]}
    names = list(sites)
    hard = D.hard_years(seed, span)
    P, C = {}, {}
    founded = {names[0]: -span}
    hh_of = {}                                                       # household id -> village
    nid = [0]

    def person(sex, born, village, hh, father=None, mother=None, kind="born", born_in=None):
        nid[0] += 1
        i = f"f{nid[0]}"
        P[i] = {"id": i, "sex": sex, "born": born, "died": None, "cause": None, "father": father, "mother": mother, "village": village,
                "hh": hh, "born_in": born_in or village, "left": None, "unions": [], "kind": kind, "last_birth": None}
        return i

    def couple(f, m, res, y):
        c = f"c{len(C) + 1}"
        C[c] = {"id": c, "f": f, "m": m, "res": res, "wed": y, "kids": []}
        P[f]["unions"].append(c)
        P[m]["unions"].append(c)
        return c

    def alive(i):
        return P[i]["died"] is None and P[i]["left"] is None

    def partner(i):
        for c in reversed(P[i]["unions"]):
            o = C[c]["m"] if C[c]["f"] == i else C[c]["f"]
            if alive(o):
                return o
        return None

    nh = [0]

    def new_hh(v):
        nh[0] += 1
        hh_of[f"h{nh[0]}"] = v
        return f"h{nh[0]}"

    y0 = -span
    for k in range(founders):                                        # the founding couples, with some children
        h = new_hh(names[0])
        am = 20 + int(u(seed, "fa", k) * 12)
        gap = int(round(D.GAP[0] + (u(seed, "fg", k) - .5) * 8))
        m = person("f", y0 - am, names[0], h, kind="came", born_in=None)
        f = person("m", y0 - am - gap, names[0], h, kind="came", born_in=None)
        c = couple(f, m, names[0], y0 - max(1, am - 19))
        for j, kb in enumerate(range(y0 - (am - 20), y0 + 1, 3)):
            if u(seed, "fk", k, j) < .6:
                x = person("m" if u(seed, "fs", k, j) < .5 else "f", kb, names[0], h, f, m)
                C[c]["kids"].append(x)
                P[m]["last_birth"] = kb
        P[m]["born_in"] = P[f]["born_in"] = "before"

    for y in range(y0 + 1, 1):
        H = y in hard
        living = [i for i in P if alive(i) and P[i]["village"] != "OFF"]
        for i in living:                                             # deaths
            a = y - P[i]["born"]
            h = D.hazard(a, H) + (.01 if P[i]["last_birth"] == y - 1 and P[i]["sex"] == "f" else 0)
            if u(seed, "die", i, y) < h:
                P[i]["died"] = y
                P[i]["cause"] = D.cause(a, y, hard, P[i]["last_birth"] == y - 1 and P[i]["sex"] == "f")
        living = [i for i in living if alive(i)]
        for i in living:                                             # births
            p = P[i]
            if p["sex"] != "f" or not p["unions"]:
                continue
            c = C[p["unions"][-1]]
            if not alive(c["f"]):
                continue
            a = y - p["born"]
            gap = 99 if p["last_birth"] is None else y - p["last_birth"]
            r = D.fert(a) * (0 if gap < 1 else .3 if gap == 1 else 1)
            if u(seed, "birth", i, y) < r:
                x = person("m" if u(seed, "sex", i, y) < .5 else "f", y, p["village"], p["hh"], c["f"], i)
                c["kids"].append(x)
                p["last_birth"] = y
        living = [i for i in P if alive(i) and P[i]["village"] != "OFF"]
        single = lambda i: not partner(i)
        men = [i for i in living if P[i]["sex"] == "m" and y - P[i]["born"] >= 18 and single(i)]
        for w in sorted([i for i in living if P[i]["sex"] == "f" and 16 <= y - P[i]["born"] <= 45 and single(i)]):   # marriages
            a = y - P[w]["born"]
            rate = D.first_marriage(a) * (.5 if P[w]["unions"] else 1)
            if u(seed, "wed", w, y) >= rate:
                continue
            A = anc2(P, w)
            cands = [(m, D.gap_w((y - P[m]["born"]) - a) * math.exp(-dist(sites[P[m]["village"]]["at"], sites[P[w]["village"]]["at"]) / D.LAMBDA))
                     for m in men if -3 <= (y - P[m]["born"]) - a <= 20 and not (anc2(P, m) & A) and single(m)]
            m = pick(seed, ("husband", w, y), cands)
            if m is None:
                if off and u(seed, "offwed", w, y) < .3:
                    m = person("m", y - a - int(round(D.GAP[0])), P[w]["village"], P[w]["hh"], kind="off", born_in="OFF")
                else:
                    continue
            v = P[m]["village"]
            mates = [o for o in P if P[o]["hh"] == P[m]["hh"] and alive(o) and o != m]
            head_of_own = P[m]["kind"] == "off" or not any(y - P[o]["born"] >= 16 and P[o]["born"] < P[m]["born"] for o in mates)
            room = lambda s: len({P[o]["hh"] for o in P if alive(o) and P[o]["village"] == s}) < cap
            heir = P[m]["father"] is not None and all(P[o]["born"] >= P[m]["born"] for o in mates
                                                       if P[o]["father"] == P[m]["father"] and P[o]["sex"] == "m")
            if head_of_own:
                h = P[m]["hh"]
            elif room(v):
                h = new_hh(v)
            else:
                near = sorted((s for s in founded if s != v and room(s)), key=lambda s: (dist(sites[s]["at"], sites[v]["at"]), s))
                if near and u(seed, "move", m, y) < .5:
                    v = near[0]
                    h = new_hh(v)
                elif len(founded) < len(sites) and u(seed, "found", m, y) < D.FOUND:
                    v = min((s for s in names if s not in founded), key=lambda s: (dist(sites[s]["at"], sites[P[m]["village"]]["at"]), s))
                    founded[v] = y
                    h = new_hh(v)
                elif heir:
                    h = P[m]["hh"]                                       # the heir marries into his father's house
                else:
                    continue                                             # no house to be had: no marriage this year
            for o in (m, w):
                P[o]["village"], P[o]["hh"] = v, h
            couple(m, w, v, y)
        for i in [i for i in P if alive(i) and P[i]["village"] != "OFF"]:   # departures, and wives from off the map
            a = y - P[i]["born"]
            if 16 <= a <= 30 and not partner(i) and u(seed, "leave", i, y) < D.LEAVE:
                P[i]["left"] = y
            elif off and P[i]["sex"] == "m" and 22 <= a <= 40 and not partner(i) and u(seed, "offwife", i, y) < .02:
                m = person("f", y - a + int(round(D.GAP[0])), P[i]["village"], P[i]["hh"], kind="off", born_in="OFF")
                couple(i, m, P[i]["village"], y)
        by_hh = {}
        for i in P:
            if alive(i) and P[i]["village"] != "OFF":
                by_hh.setdefault(P[i]["hh"], []).append(i)
        for h, ms in sorted(by_hh.items()):                          # children left with no grown kin move to kin, or a neighbour
            if all(y - P[i]["born"] < 16 for i in ms):
                v = hh_of[h]
                kin = [o for o in by_hh if o != h and hh_of[o] == v and any(y - P[j]["born"] >= 16 for j in by_hh[o])]
                if not kin:
                    continue
                A = set().union(*(anc2(P, i) for i in ms))
                kin.sort(key=lambda o: (-len(A & set().union(*(anc2(P, j) for j in by_hh[o]))), o))
                for i in ms:
                    P[i]["hh"] = kin[0]
    present = [i for i in P if alive(i) and P[i]["village"] != "OFF"]
    hhs = {}
    for i in sorted(present, key=lambda i: P[i]["born"]):
        hhs.setdefault(P[i]["hh"], []).append(i)
    return {"P": P, "C": C, "founded": founded, "hard": hard, "span": span, "present": present, "households": hhs, "hh_of": hh_of}


def to_input(region, sim) -> dict:
    """The forward run's present population as the backward build's input: households with members' ages and sexes, nothing else."""
    P = sim["P"]
    hh = []
    for h, ms in sorted(sim["households"].items(), key=lambda t: (sim["hh_of"][t[0]], t[0])):
        hh.append({"id": h, "village": sim["hh_of"][h], "members": [{"id": i, "age": -P[i]["born"], "sex": P[i]["sex"]} for i in ms]})
    return {"villages": region["villages"], "off": region.get("off"), "span": sim["span"], "households": hh}


def truth(sim) -> dict:
    """The forward run's past in the common form stats.py reads."""
    P, C = sim["P"], sim["C"]
    pres = set(sim["present"])
    out = {}
    for i, p in P.items():
        out[i] = {"sex": p["sex"], "born": p["born"], "died": p["died"], "left": p["left"], "father": p["father"], "mother": p["mother"],
                  "present": i in pres, "village": p["village"] if i in pres else None, "hh": p["hh"] if i in pres else None,
                  "born_in": p["born_in"], "kind": p["kind"]}
    unions = [{"f": c["f"], "m": c["m"], "res": c["res"], "wed": c["wed"]} for c in C.values()]
    return {"P": out, "unions": unions, "founded": dict(sim["founded"]), "span": sim["span"]}
