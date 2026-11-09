"""The wild layer in the engine (proposals/wild_layer.md §3, §4; D2-199, the ecology branch): only in a world with the `wild` pack.

- **At world build** (`seed`): the land summary the generator wrote (`spec["wild"]["land"]`) and a starting state, run forward
  through a history before the run (§3.9: the same step with no people, on the world's own climate at days far ahead of the run, so
  the past does not repeat the run's weather). Kept in `s["wild"]`.
- **Each night** (`night`, called after farm.night): the ecology step for the day (cybertron2/wild/ecology.py), with the weather at
  each area's node (D4-111) and keyed draws (`w.rng`), written back by the `set_wild` primitive so the journal holds every change.
- **The bridge out** (§3.8): what wild kinds ate of the people's crops and stores in a node's home area is drawn from the standing
  crops and the stores there, through the engine's own primitives. A share of the model's crop eaten is the share drawn from the
  real crop, so no unit has to match.

Hunts, groups near people, traces and signs come in phase 3 (wild_layer.md §6).
"""
from __future__ import annotations

import math

from cybertron2.engine import packs as PK

KG_PER_FOOD = 10.0             # an engine food (365/Y real person-days, node_ecology.md) as kg of grain or forage (calibrate)
DRY_STORES = ("grain", "rye", "oats", "beans", "meal", "flour")   # what wild kinds get at in a store (calibrate)
HISTORY_YEARS = 10              # the history before the run (calibrate)
HISTORY_AHEAD_YEARS = 200       # the climate's days used for it: this many years past the run's start


def on(w) -> bool:
    return "wild" in PK.of(w)


def model(w):
    m = w.__dict__.get("_wild_model")                                     # not state: rebuilt from the land summary on demand
    if m is None:
        from cybertron2.wild import ecology as EC
        knobs = dict((w.spec.get("wild") or {}).get("knobs") or {})
        m = EC.Model(w.s["wild"]["land"], Y=w.year_days(), knobs=knobs)
        w.__dict__["_wild_model"] = m
    return m


def weather(w, nodes, day) -> dict:
    """The weather at each node on a day: the climate's values (D4-109) when it is on, else the season's means."""
    from cybertron2.engine import climate as CL
    from cybertron2.wild.ecology import SEASON_T
    out = {}
    for nd in nodes:
        if CL.on(w):
            e = CL.env(w, nd, day)
            out[nd] = {"temp": float(e["temp"]), "low": float(e["low"]), "rain": float(e["rain"]), "snow": CL.label(w, nd, day) == "snow"}
        else:
            si = ["spring", "summer", "autumn", "winter"].index(w.calendar(day)["season"])
            t = SEASON_T[si]
            out[nd] = {"temp": t, "low": t - 5.0, "rain": 2.0, "snow": False}
    return out


def draws(w, day, tag="run") -> dict:
    """Keyed draws for the day's step: the year's mast and the summer's outbreaks per kind and area (replays exactly)."""
    m = model(w)
    y = day // w.year_days()
    out = {"mast": float(w.rng("wild-mast", tag, y).random())}
    if day % w.year_days() == w.year_days() // 4:                        # the summer's first day: outbreaks are drawn
        out["epi"] = {}
        for k in m.names:
            r = w.rng("wild-epi", tag, y, k)
            out["epi"][k] = [r.random() for _ in range(m.n)]
    return out


def seed(w) -> None:
    from cybertron2.wild import ecology as EC
    land = (w.spec.get("wild") or {}).get("land")
    w.s["wild"] = {"land": land}
    if not land:                                                          # a hand-made world without land: nothing lives yet
        w.s["wild"]["state"] = None
        return
    m = model(w)
    st = m.initial()
    Y = w.year_days()
    years = int((w.spec.get("wild") or {}).get("history_years", HISTORY_YEARS))
    off = HISTORY_AHEAD_YEARS * Y
    for d in range(years * Y):                                            # the history before the run
        EC.step(m, st, d, weather(w, sorted(set(m.nodes)), off + d), draws(w, d, "history"))
    st["day"] = -1
    st["mast"]["years"] = {}                                              # the trees' budget carries over; the run's years are its own
    w.s["wild"]["state"] = st


def night(w, rec) -> None:
    """The ecology's day, then what wild kinds took of the people's crops and stores in each home area."""
    if not on(w) or not (w.s.get("wild") or {}).get("state"):
        return
    from cybertron2.wild import ecology as EC, kinds as WK
    import copy
    m = model(w)
    st = copy.deepcopy(w.s["wild"]["state"])
    real = {"crops": {}, "stores": {}}
    for i, aid in enumerate(m.ids):                                       # the wild kinds see a real field and a real store (the
        if m.home[i]:                                                     # food web's crop at real yield); none when the engine
            nd = m.nodes[i]                                               # has none standing or stored
            real["crops"][i], real["stores"][i] = _crop_food(w, nd), _store_food(w, nd)
            for food in ("crops", "stores"):
                if real[food][i] <= 1e-9:
                    st["pulse"][food][i] = 0.0
    before = {f: list(st["pulse"][f]) for f in ("crops", "stores")}
    eff = EC.step(m, st, w.d, weather(w, sorted(set(m.nodes)), w.d), draws(w, w.d))
    place = m.nodes[0]
    w.apply("set_wild", place, path=["state"], value=st)
    out = {"mast": st.get("mast_now"), "crops": {}, "stores": {}}
    for i, aid in enumerate(m.ids):
        if not m.home[i]:
            continue
        node = m.nodes[i]
        for food in ("crops", "stores"):
            year_kg = float(m.res[food][i]) * WK.FOOD[food]["prod"] * WK.SCALE.get(food, 1.0) * m.km2[i]   # the model's year of it
            ate = float((eff["eaten"].get(food) if eff["eaten"].get(food) is not None else [0.0] * m.n)[i])
            share = min(0.5, ate / year_kg) if year_kg > 1e-9 and real[food].get(i, 0.0) > 1e-9 else 0.0   # the year's share, drawn
                                                                                  # from the real crop or store, which is a year's
            if share > 1e-6:
                lost = (_crops if food == "crops" else _stores)(w, node, share)
                if lost > 1e-6:
                    out[food][node] = round(lost, 4)
    out["groups"] = _groups(w, m, st)
    rec["wild"] = out


# ---------------------------------------------------------------------- groups near people (wild_layer.md §3.4, D2-197, D2-198)
def _near(kind):
    from cybertron2.engine.data import RESOURCES
    return (RESOURCES.get(kind) or {}).get("near_people")


def _season_window(w, day, seasons) -> bool:
    cal = w.calendar(day)
    si = ["spring", "summer", "autumn", "winter"].index(cal["season"])
    sd = int(cal["day"]) - 1
    return si in seasons and seasons[si][0] <= sd <= seasons[si][1]


def _fields(w, node) -> list:
    """The node's fields with a standing crop, the parcel ids in order."""
    from cybertron2.engine import farm as FM
    return [pid for pid, par in sorted(w.s["parcels"].items()) if par["node"] == node and any(
        c.get("area_left", 0) > 1e-6 and float(c.get("left", 0)) > 1e-9 for _, _, c in FM.standing(par))]


def _edge_of(w, pid) -> str:
    """The parcel a group comes out of on its way to a field: a wood or scrub beside it, else the field itself."""
    par = w.s["parcels"][pid]
    for q in par.get("adj") or []:
        if w.s["parcels"].get(q, {}).get("cover") in ("forest", "scrub"):
            return q
    return pid


def _trace(traces, pid, kind, what, day, n):
    lst = [t for t in traces.get(pid, []) if day - int(t["day"]) <= 3]
    lst.append({"kind": kind, "what": what, "day": day, "n": int(n)})
    traces[pid] = lst


def _groups(w, m, st) -> dict:
    """Whole-counted kinds with a group near a village: condense from the ring's count, set out on a drive, leave traces, raid a
    field unless a watch turns them by the kind's answer to scares, remember. All changes through set_wild."""
    import copy
    from cybertron2.engine import farm as FM
    import numpy as np
    wild = w.s["wild"]
    groups = copy.deepcopy(wild.get("groups") or {})
    traces = {pid: [t for t in lst if w.d - int(t["day"]) <= 3] for pid, lst in copy.deepcopy(wild.get("traces") or {}).items()}
    traces = {pid: lst for pid, lst in traces.items() if lst}
    watch = {pid: v for pid, v in (wild.get("watch") or {}).items() if int(v.get("day", -9)) == w.d}
    out = {}
    land = wild["land"]
    ix = {a: i for i, a in enumerate(m.ids)}
    rings = {a["node"]: ix[aid] for aid, a in land["areas"].items() if a["kind"] == "ring"}
    for node, ri in sorted(rings.items()):
        for kind in m.names:
            np_ = _near(kind)
            spec = m.kinds[kind]
            if not np_ or spec.get("count") != "whole":
                continue
            gid = f"{kind}@{node}"
            count = float(np.asarray(st["pop"][kind])[ri]) * float(m.km2[ri])
            lo, hi = (spec.get("group") or {}).get("size", [2, 10])
            if count < lo:
                groups.pop(gid, None)
                continue
            g = groups.get(gid) or {"kind": kind, "node": node, "pos": "home", "t": -1, "raid": -1, "found": -99, "habit": {},
                                    "wary": -1, "rest": -1, "pref": None, "target": None}
            g["n"] = int(np.clip(round(0.3 * count), lo, hi))
            groups[gid] = g
            rng = w.rng("wild-group", w.d, gid)
            fields = _fields(w, node)
            if not fields:
                g["pos"] = "home"
                continue
            if g["pref"] not in fields:
                g["pref"] = next((f for f in fields if _edge_of(w, f) != f), fields[0])
            ans = np_["answer"]
            if ans["type"] == "habituate":
                g["habit"] = {k: max(0.0, v - float(ans["decay"])) for k, v in g["habit"].items() if v > float(ans["decay"])}
            attr = max([t["attr"] for t in np_["targets"] if _season_window(w, w.d, t["seasons"])] or [0.0])
            trample = max([t["trample"] for t in np_["targets"] if _season_window(w, w.d, t["seasons"])] or [0.0])
            hunger = 1.0 - float(np.asarray(st["cond"][kind])[ri])
            if g["pos"] == "ready" and w.d >= g["raid"]:
                g["pos"] = "home"
                tgt = g["target"] if g["target"] in fields else g["pref"]
                seen = watch.get(tgt)
                scare = seen.get("scare") if seen else None
                if scare is not None:
                    harm = (np_.get("harm") or {}).get(scare)
                    if harm:
                        turned = rng.random() < float(harm["turn_p"])
                        if turned and rng.random() < float(harm["harm_p"]):
                            g["wary"], g["habit"] = w.d + int(np_["wary_after_harm"]), {}
                    elif ans["type"] == "habituate":
                        turned = rng.random() < float(ans["turn_p"]) * (1 - float(g["habit"].get(scare, 0.0)))
                        if turned:
                            g["habit"][scare] = min(1.0, float(g["habit"].get(scare, 0.0)) + float(ans["gain"]))
                    elif ans["type"] == "scared_off":
                        turned = rng.random() < float(ans["turn_p"])
                    else:
                        turned = False
                    if turned:
                        g["rest"] = w.d + int(ans.get("rest", 2))
                        _trace(traces, tgt, kind, "turned", w.d, g["n"])
                        out[gid] = {"raid": tgt, "turned": True, "scare": scare}
                        continue
                share = min(0.5, trample * g["n"] * (float(np_["met_share"]) if scare is not None else 1.0))
                lost = 0.0
                par = w.s["parcels"][tgt]
                for hd, _, c in FM.standing(par):
                    q = round(float(c.get("left", 0.0)) * share, 4)
                    if c.get("area_left", 0) > 1e-6 and q > 1e-9:
                        w.apply("draw", node, parcel=tgt, key="crop", qty=q, **({"holder": hd} if hd is not None else {}))
                        lost += q
                g["found"] = w.d
                _trace(traces, tgt, kind, "raid", w.d, g["n"])
                out[gid] = {"raid": tgt, "turned": False, "scare": scare, "lost": round(lost, 4)}
            elif g["pos"] == "edge":
                if rng.random() < float(np_["lead_sign_p"]):
                    _trace(traces, _edge_of(w, g["target"]), kind, "edge", w.d, g["n"])
                if w.d - g["t"] >= int(np_["lead_nights"]) - 1:
                    g["pos"], g["raid"] = "ready", w.d + 1
            elif g["pos"] == "home" and w.d >= g["rest"] and w.d >= g["wary"] and attr > 0:
                p = attr * (float(np_["drive"]["base"]) + float(np_["drive"]["hunger"]) * hunger)
                knows = 1 <= w.d - int(g["found"]) <= int(np_["memory_days"])
                if knows:
                    p = max(p, float(np_["return_p"]) * attr)
                if rng.random() < p:
                    g["target"] = g["pref"] if rng.random() < 0.75 else fields[int(rng.random() * len(fields))]
                    if knows:
                        g["pos"], g["raid"] = "ready", w.d + 1                  # straight back; the damage was the sign
                    else:
                        g["pos"], g["t"] = "edge", w.d
                        if rng.random() < float(np_["lead_sign_p"]):
                            _trace(traces, _edge_of(w, g["target"]), kind, "edge", w.d, g["n"])
    place = m.nodes[0]
    kept = {pid: v for pid, v in (wild.get("watch") or {}).items() if int(v.get("day", -9)) >= w.d}
    if kept != (wild.get("watch") or {}):
        w.apply("set_wild", place, path=["watch"], value=kept)
    if groups != (wild.get("groups") or {}):
        w.apply("set_wild", place, path=["groups"], value=groups)
    if traces != (wild.get("traces") or {}):
        w.apply("set_wild", place, path=["traces"], value=traces)
    return out


# ---------------------------------------------------------------------- taking wild kinds (wild_layer.md §3.7; D2-192, D2-193)
RANGE_AREAS = ("near", "the wood around", "far")


def _reach(m, land, node, rng_word) -> list:
    """The areas a hunt from a node covers: its own land (near), with the ring around (the wood around), and the wild areas that
    border the ring (far)."""
    ix = {a: i for i, a in enumerate(m.ids)}
    out = [ix[land["home"][node]]] if node in land.get("home", {}) else []
    if rng_word in ("the wood around", "far"):
        out += [ix[a] for a, x in land["areas"].items() if x["kind"] == "ring" and x["node"] == node]
    if rng_word == "far":
        ring = {m.ids[i] for i in out}
        out += sorted({ix[b if a in ring else a] for a, b, _ in land["links"] if (a in ring) != (b in ring)
                       and land["areas"][b if a in ring else a]["kind"] == "wild"})
    return sorted(set(out))


def _wanted(target, kinds) -> set:
    """The kinds a hunter's words name: a kind, or a family it is known by ("deer", "small game"); none for anything."""
    from cybertron2.engine.data import RESOURCES
    t = str(target or "").strip().lower()
    if not t or t in ("anything", "whatever comes", "game", "any"):
        return set()
    return {k for k in kinds if t == k or t in ((RESOURCES.get(k) or {}).get("taken") or {}).get("family", [])
            or t.rstrip("s") == k.rstrip("s")}


def take(here, mind, tech, key, place_name, out, m_skill, y, a) -> tuple:
    """A hunt: what the hunter comes on is drawn from the kinds in the areas the range covers, by their numbers, how easy each is to
    find and what this way of hunting takes; looking for one thing makes it likelier and the rest less likely, never impossible, so a
    deer stalker may come on the sounder. What is found may flee, be taken (off its area's count, and its group's), or hurt the
    hunter (D2-193). Returns (food taken, a line for the hunter)."""
    from cybertron2.engine.data import RESOURCES, TECHNIQUES
    import numpy as np
    w = here._w
    if not on(w) or not (w.s.get("wild") or {}).get("state"):
        return 0.0, f"You found nothing to take at {place_name}."
    m = model(w)
    land = w.s["wild"]["land"]
    st = w.s["wild"]["state"]
    mods = a.get("_mods") or {}
    rng_word = (mods.get("range") if isinstance(mods.get("range"), str) else None) or "near"
    areas = _reach(m, land, here.node, rng_word)
    takes = dict(y["takes"])
    want = _wanted(a.get("looking for"), takes)
    rng = here.rng("wild-take", here.day, here.name, tech)
    cand = []
    for k, tw in sorted(takes.items()):
        if k not in st["pop"]:
            continue
        tk = (RESOURCES.get(k) or {}).get("taken") or {}
        focus = (3.0 if k in want else 0.4) if want else 1.0
        for i in areas:
            count = float(st["pop"][k][i]) * float(m.km2[i])
            wgt = count * float(tk.get("detect", 0.2)) * float(tw) * focus / (1.0 + 0.3 * areas.index(i))
            if wgt > 0 and count >= 1.0:                                     # one met is a whole one
                cand.append((k, i, wgt))
    total = sum(c[2] for c in cand)
    effort = float(TECHNIQUES[tech]["units"]) / 2.0
    looked = f" looking for {a.get('looking for')}" if want else ""
    where = {"near": place_name, "the wood around": f"the woods and wastes around {place_name}", "far": "the wild land far beyond"}[rng_word]
    if total <= 0 or rng.random() >= 1 - math.exp(-0.03 * total * effort):
        return 0.0, f"You hunted {where}{looked} and came on nothing."
    u, acc = rng.random() * total, 0.0
    for k, i, wgt in cand:
        acc += wgt
        if u < acc:
            break
    tk = (RESOURCES.get(k) or {}).get("taken") or {}
    surprise = bool(want) and k not in want
    found = f"you came on {_a(k)}" + (f" instead of the {a.get('looking for')} you were after" if surprise else "")
    crew = 1 + sum(1 for e in here.events() if e.get("kind") == "work" and e.get("tech") == tech and e.get("actor") != here.name
                   and f"parcel:{key}" in (e.get("about") or []))
    danger = tk.get("danger")
    if danger and rng.random() < float(danger["wound"]) / crew:
        if rng.random() < float(danger.get("kill", 0.0)) / crew:
            here.apply("die", person=here.name, cause=f"killed by {_a(k)} while hunting")
            return 0.0, f"Hunting {where}, {found}; it turned on you."
        here.apply("harm", person=here.name, wounded=True)
        hurt = " It turned on you and you were hurt before it broke away."
        return 0.0, f"Hunting {where}, {found}.{hurt}"
    armed = here.weapon()
    wpn = float(TECHNIQUES[tech]["weapon"]["armed" if armed else "none"])
    p_take = float(np.clip(0.55 * m_skill * wpn * (1 - float(tk.get("flee", 0.5))) * (1 + 0.25 * (crew - 1)), 0, 0.95))
    if rng.random() >= p_take:
        return 0.0, f"Hunting {where}, {found}, but it got away."
    pop = [float(x) for x in st["pop"][k]]
    pop[i] = max(0.0, pop[i] - 1.0 / float(m.km2[i]))                      # one head off its area's count
    here.apply("set_wild", path=["state", "pop", k], value=pop)
    gid = f"{k}@{here.node}"
    g = (w.s["wild"].get("groups") or {}).get(gid)
    if g:                                                                   # its group is one fewer, and wary of the village
        np_ = _near(k) or {}
        here.apply("set_wild", path=["groups", gid], value=dict(g, n=max(0, int(g["n"]) - 1), habit={},
                                                                 wary=here.day + int(np_.get("wary_after_harm", 5))))
    food = 0.0
    for item, q in sorted((tk.get("goods") or {}).items()):
        here.apply("create", dst=out, item=item, qty=float(q), why=tech)
        food += float(q) if item == "meat" else 0.0
    return food, f"Hunting {where}, {found} and took it: " + ", ".join(f"{q:g} {it}" for it, q in sorted((tk.get('goods') or {}).items())) + "."


def _a(kind) -> str:
    return ("an " if kind[0] in "aeiou" else "a ") + kind


def watch(here, pid, y, place_name) -> str:
    """A night watch over a field with a scare (the technique's row names it): read by the night's groups (D2-198)."""
    here.apply("set_wild", path=["watch", pid], value={"day": here.day, "by": here.name, "scare": y["scare"]})
    return f"You set yourself to watch {place_name} tonight with {y.get('with', y['scare'])}."


def _crop_food(w, node) -> float:
    from cybertron2.engine import farm as FM
    return sum(float(c.get("left", 0.0)) for pid, par in w.s["parcels"].items() if par["node"] == node
               for _, _, c in FM.standing(par) if c.get("area_left", 0) > 1e-6)


def _store_food(w, node) -> float:
    return sum(float(q) for b in w.s["buildings"].values() if b["node"] == node and b.get("stock")
               for item, q in (w.s["containers"].get(b["stock"], {}).get("goods") or {}).items() if item in DRY_STORES)


def _crops(w, node, share) -> float:
    """Draw a share of every standing crop on the node's fields (as herds trample, D2-123): what wild kinds ate in the night."""
    from cybertron2.engine import farm as FM
    total = 0.0
    for pid, par in sorted(w.s["parcels"].items()):
        if par["node"] != node:
            continue
        for hd, _, c in FM.standing(par):
            left = float(c.get("left", 0.0))
            if c.get("area_left", 0) <= 1e-6 or left <= 1e-9:
                continue
            q = round(left * share, 4)
            if q <= 1e-9:
                continue
            w.apply("draw", node, parcel=pid, key="crop", qty=q, **({"holder": hd} if hd is not None else {}))
            total += q
    return total


def _stores(w, node, share) -> float:
    """Destroy a share of the grain and other dry food in the node's stores: what wild kinds took there."""
    total = 0.0
    for bid, b in sorted(w.s["buildings"].items()):
        if b["node"] != node or not b.get("stock"):
            continue
        cid = b["stock"]
        for item, q in sorted((w.s["containers"].get(cid, {}).get("goods") or {}).items()):
            if item in DRY_STORES and q > 0:
                take = round(float(q) * share, 4)
                if take > 1e-6:
                    w.apply("destroy", node, src=cid, item=item, qty=take, why="eaten in store by wild kinds")
                    total += take
    return total
