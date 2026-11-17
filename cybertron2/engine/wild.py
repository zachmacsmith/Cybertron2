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

import numpy as np

from cybertron2.engine import packs as PK

KG_PER_FOOD = 10.0             # an engine food (365/Y real person-days, node_ecology.md) as kg of grain or forage (calibrate)
DRY_STORES = ("grain", "rye", "oats", "beans", "meal", "flour")   # what wild kinds get at in a store (calibrate)
EGG_FOOD = 0.02                 # food an egg is worth at real content x Y/365 (calibrate)
ITEM_EGG_FOOD = 0.6             # the ITEMS row's food a unit of eggs (so qty x 0.6 is the food laid)
HENS_A_HOUSE = 6                # hens a household keeps, seeded with the wild pack (calibrate)
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


def eco_day(w, day=None) -> int:
    """The ecology's day count: the calendar's (its seasons begin with spring), so a world that starts in summer steps in summer."""
    return int(w.calendar(day)["year_day"])


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
    from cybertron2.wild.kinds import DISEASES
    for name, d in sorted(DISEASES.items()):                              # a disease's season's first day: its seeds are drawn
        if day % w.year_days() == int(d.get("season", 1)) * (w.year_days() // 4):
            r = w.rng("wild-dis", tag, y, name)
            out.setdefault("dis", {})[name] = [r.random() for _ in range(m.n)]
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
    k0 = eco_day(w, 0)
    from cybertron2.wild import runs as RU
    rivers = RU.active(m)                                                 # the runs along the river (brief 5 §2), where it has any
    if rivers:
        RU.seed(m, st)
    nodes = sorted(set(m.nodes))
    wx_next = weather(w, nodes, off)
    for d in range(years * Y):                                            # the history before the run, ending on the run's season
        wx = wx_next
        wx_next = weather(w, nodes, off + d + 1)
        EC.step(m, st, k0 + d, wx, draws(w, k0 + d, "history"), history=True)
        if rivers:
            RU.advance(m, st, k0 + d, wx, wx_next, weather=_runs_by_weather(w))
    if rivers:                                                            # the run's own nights start with no run under way
        st["runs"]["pulses"], st["runs"]["rain"], st["runs"]["tally"] = [], {}, {}
    st["day"] = -1
    st["mast"]["years"] = {}                                              # the trees' budget carries over; the run's years are its own
    w.s["wild"]["state"] = st
    _seed_plants(w)                                                       # the wild plant kinds in place of `plants` (D2-200)
    _seed_sites(w)                                                        # heronries, rookeries, beaver lodges (wave 5)
    _seed_legends(w)                                                      # the legendary beasts, seldom (D2-195)
    for name, k in w.s["know"].items():                                   # the old hunt is the wild one's basic hunt, renamed (D2-204)
        if "hunt" in k:
            k.setdefault("hunt the wild", dict(k["hunt"]))
    from cybertron2.wild import methods as MT
    MT.seed_by_land(w)                                                     # methods by upbringing and the land (D2-204 §6)
    for bid, b in w.s["buildings"].items():                               # each household's hens, in its house's store
        if (b.get("fittings") or {}).get("beds") and b.get("stock") and b["stock"] in w.s["containers"]:
            g = w.s["containers"][b["stock"]].setdefault("goods", {})
            g.setdefault("hen", float(HENS_A_HOUSE))


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
    harvest = _follow_harvest(w, m, st, real)                             # the vermin come in to full stores
    scale, pools = _shared_pre(w, m, st)                                  # what the land's plants hold for the wild kinds (D2-202)
    scale["stores"] = harvest
    lent = _dead_to_pool(w, m, st)                                        # the dead lying open feed the carrion eaters (brief 3 §3)
    from cybertron2.engine import waters as WA
    WA.to_wild(w, m, st)                                                  # a water body's fish, as full as its stock (D2-229)
    eff = EC.step(m, st, eco_day(w), weather(w, sorted(set(m.nodes)), w.d), draws(w, eco_day(w)), scale=scale)
    _dead_from_pool(w, m, st, eff, lent)
    _regime_kills(w, m, st)                                               # a great freeze (L4)
    place = m.nodes[0]
    w.apply("set_wild", place, path=["state"], value=st)
    out = {"mast": st.get("mast_now"), "crops": {}, "stores": {}}
    flock_budget = {}
    out["shared"] = _shared_post(w, m, scale, pools, eff)
    _plant_year(w, m, st)
    for i, aid in enumerate(m.ids):
        if not m.home[i]:
            continue
        node = m.nodes[i]
        for food in ("crops", "stores"):
            year_kg = float(m.res[food][i]) * WK.FOOD[food]["prod"] * WK.SCALE.get(food, 1.0) * m.km2[i]   # the model's year of it
            ate = float((eff["eaten"].get(food) if eff["eaten"].get(food) is not None else [0.0] * m.n)[i])
            share = min(0.5, ate / year_kg) if year_kg > 1e-9 and real[food].get(i, 0.0) > 1e-9 else 0.0   # the year's share, drawn
                                                                                  # from the real crop or store, which is a year's
            if share > 1e-6 and food == "stores":                          # by kind: what each fitting stops (brief 2 §4)
                by = (eff.get("eaten_by") or {}).get("stores") or {}
                tot_k = sum(float(v[i]) for v in by.values()) or 0.0
                shares = {k: share * float(v[i]) / tot_k for k, v in by.items() if float(v[i]) > 0} if tot_k > 0 else {None: share}
                lost = _stores(w, node, shares)
                if lost > 1e-6:
                    out[food][node] = round(lost, 4)
            elif share > 1e-6 and food == "crops":                        # a flock's part is kept for its raid (brief 4 §4.3): a
                by = (eff.get("eaten_by") or {}).get("crops") or {}            # raid takes it where the flock lands, not on top of it
                tot_k = sum(float(v[i]) for v in by.values()) or 0.0
                fl = sum(float(v[i]) for k, v in by.items() if (_near(k) or {}).get("flock")) / tot_k if tot_k > 0 else 0.0
                standing = _crop_food_qty(w, node)
                flock_budget[node] = {"qty": share * fl * standing, "standing": standing}
                lost = _crops(w, node, share * (1.0 - fl))
                if lost > 1e-6:
                    out[food][node] = round(lost, 4)
            elif share > 1e-6:
                lost = (_crops if food == "crops" else _stores)(w, node, share)
                if lost > 1e-6:
                    out[food][node] = round(lost, 4)
    eaten = {nd: dict(v, day=w.d) for nd, v in _shares(out, real, m).items()}
    if eaten or (w.s["wild"].get("eaten") or {}):
        w.apply("set_wild", place, path=["eaten"], value=eaten)
    out["loads"] = _loads(w, m, st)
    out["sick"] = _herds_sick(w, m, st)
    w._flock_budget = flock_budget
    out["groups"] = _groups(w, m, st)
    for node, fb in sorted(flock_budget.items()):                         # what the flock did not take in a raid it grazed as before
        if fb["qty"] > 1e-6 and fb["standing"] > 1e-9:
            lost = _crops(w, node, min(0.5, fb["qty"] / fb["standing"]))
            if lost > 1e-6:
                out["crops"][node] = round(out["crops"].get(node, 0.0) + lost, 4)
    w._flock_budget = {}
    out["sites"] = _sites_night(w, m, st)
    out["set"] = _set_night(w, m, w.s["wild"]["state"])                   # snares and traps set and left (brief 2 §4)
    runs = _runs_night(w, m)                                              # the weirs, the race, the otters, the runs on (brief 5)
    if runs:
        out["runs"] = runs
    _food_out_night(w)                                                    # food left out at the doors (brief 4 §4.1)
    out["store_beasts"] = _store_beasts(w, m, w.s["wild"]["state"])      # a cat at a store, a barn owl in its hole (D2-206; K1)
    out["near"] = {gid: {"n": g["n"], "pos": g["pos"], "what": g.get("what"), **({"at": g["node"], "range": g["range"]} if g.get("range") else {})}
                   for gid, g in sorted((w.s["wild"].get("groups") or {}).items())}
    _hens_lay(w)
    rec["wild"] = out


def _loads(w, m, st) -> dict:
    """The loads' harm on each home's fields tonight (crops of a family at an age, a share for each unit of the level over its
    mark, cut by a guard on the field) and what a load feeds (a parcel resource, up to its cap). Hits kept for the signs."""
    from cybertron2.engine import farm as FM
    from cybertron2.wild.kinds import LOADS
    lv = (st.get("loads") or {}).get("level") or {}
    guard = {pid: v for pid, v in ((w.s["wild"].get("guard")) or {}).items() if int(v.get("until", -9)) >= w.d}
    hits, fed = {}, {}
    for i, nd in enumerate(m.nodes):
        if not m.home[i]:
            continue
        for k, spec in sorted(LOADS.items()):
            L = float((lv.get(k) or [0.0] * m.n)[i])
            for pid, par in sorted(w.s["parcels"].items()):
                if par["node"] != nd:
                    continue
                rook = 1.0
                se = spec.get("site_eats")                                    # a colony that works the load off near it (brief 2 K1)
                if se:
                    from cybertron2.wild.kinds import SITES
                    for s_ in (w.s["wild"].get("sites") or {}).values():
                        d_ = layout_steps(w, s_["parcel"], pid) if s_.get("kind") == se["site"] and s_.get("gone") is None else None
                        if d_ is not None and d_ <= int(se["reach"]):
                            rook *= 1 - float(se["share"]) * min(1.0, float(s_["size"]) / float(SITES[se["site"]]["cap"]))
                for h in spec.get("harm_res") or []:                          # a load on a parcel's stock (moles in the hay grass)
                    r = (par.get("res") or {}).get(h["res"])
                    if not r or par["cover"] not in h["covers"]:
                        continue
                    share = min(0.5, float(h["share"]) * max(0.0, L - float(h["over"])))
                    g = guard.get(pid)
                    if g and g.get("load") == k:
                        share *= 1 - float(g["cut"])
                    q = round(float(r["S"]) * share, 4)
                    if q > 1e-6:
                        w.apply("draw", nd, parcel=pid, key=h["res"], qty=q)
                        was = hits.setdefault(pid, {}).get(k, {}).get("lost", 0.0)
                        hits[pid][k] = {"day": w.d, "share": round(share, 4), "lost": round(q + was, 4)}
                for h in spec.get("harm") or []:
                    share = min(0.5, float(h["share"]) * max(0.0, L - float(h["over"]))) * rook
                    g = guard.get(pid)
                    if g and g.get("load") == k:
                        share *= 1 - float(g["cut"])
                    if share <= 1e-6:
                        continue
                    for hd, _, c in FM.standing(par):
                        age = w.d - int(c.get("sown", w.d))
                        q = round(float(c.get("left", 0.0)) * share, 4)
                        if c.get("crop") in h["crops"] and h["age"][0] <= age <= h["age"][1] and c.get("area_left", 0) > 1e-6 and q > 1e-9:
                            w.apply("draw", nd, parcel=pid, key="crop", qty=q, **({"holder": hd} if hd is not None else {}))
                            was = hits.setdefault(pid, {}).get(k, {}).get("lost", 0.0)
                            hits[pid][k] = {"day": w.d, "share": round(share, 4), "lost": round(q + was, 4)}
            fd = spec.get("feeds")
            if fd and L > float(fd["over"]):
                for pid, par in sorted(w.s["parcels"].items()):
                    r = (par.get("res") or {}).get(fd["res"])
                    if par["node"] == nd and par["cover"] in fd["covers"] and r:
                        q = round(min(float(r["K"]) - float(r["S"]), float(fd["share"]) * (L - float(fd["over"])) * float(r["K"])), 4)
                        if q > 1e-6:
                            w.apply("add_res", nd, parcel=pid, key=fd["res"], qty=q)
                            fed[pid] = round(q, 4)
    place = m.nodes[0]
    old = w.s["wild"].get("hits") or {}
    keep = {pid: {k: v for k, v in ks.items() if w.d - int(v["day"]) <= 1} for pid, ks in old.items()}
    for pid, ks in hits.items():
        keep.setdefault(pid, {}).update(ks)
    keep = {pid: ks for pid, ks in keep.items() if ks}
    if keep != old:
        w.apply("set_wild", place, path=["hits"], value=keep)
    if guard != (w.s["wild"].get("guard") or {}):
        w.apply("set_wild", place, path=["guard"], value=guard)
    return {"hits": hits, "fed": fed}


def _herds_sick(w, m, st) -> dict:
    """Disease in kept herds (kinds.DISEASES with `kept`): each night a herd's healthy beasts are infected from the sick share of
    the herds on its parcel, beside it and in its village, from the wild hosts' prevalence on its village's land, and now and then
    from beyond; after its course a sick beast dies (a carcass that reads as the disease's) or recovers, immune. A herd carries its
    sickness where it is driven, so it travels between villages with the beasts. All through `set` and the engine's carcasses."""
    from cybertron2.engine import farm as FM, things as TH
    from cybertron2.engine.data import TECHNIQUES
    from cybertron2.wild.kinds import DISEASES
    land = w.s["wild"]["land"]
    dis = st.get("dis") or {}
    out = {}
    herds = {hid: h for hid, h in sorted(w.s["herds"].items()) if FM.head(h) > 0 and h.get("node") in w.s["nodes"]}
    for name, d in sorted(DISEASES.items()):
        if not d.get("kept"):
            continue
        hosts = {hid: h for hid, h in herds.items() if h.get("kind") in d["kept"]}
        sick = {hid: sum(int(c["n"]) for c in ((h.get("ill") or {}).get(name) or {}).get("sick", [])) for hid, h in hosts.items()}
        share = lambda pick: (sum(sick[x] for x in pick) / max(1, sum(FM.head(hosts[x]) for x in pick))) if pick else 0.0
        for hid, h in hosts.items():
            node, par = h["node"], h.get("parcel")
            rec = dict(((h.get("ill") or {}).get(name)) or {"sick": [], "immune": 0})
            rng = w.rng("wild-sick", w.d, hid, name)
            same = [x for x, o in hosts.items() if o["node"] == node and o.get("parcel") == par]
            near = [x for x, o in hosts.items() if o["node"] == node and o.get("parcel") in (w.s["parcels"].get(par) or {}).get("adj", [])]
            town = [x for x, o in hosts.items() if o["node"] == node]
            ai = land.get("home", {}).get(node)
            wild_i = float((dis.get(name) or [0.0] * m.n)[m.ids.index(ai)]) if ai in m.ids else 0.0
            press = float(d["beta"]) * share(same) + float(d["near"]) * share(near) + float(d["node"]) * share(town) + float(d["wild_beta"]) * wild_i
            n = FM.head(h)
            healthy = max(0, n - sick[hid] - int(rec["immune"]))
            new = sum(1 for _ in range(healthy) if rng.random() < 1 - math.exp(-press))
            if not any(sick[x] for x in town) and not new and hid == town[0] and rng.random() < float(d["arrive"]) / w.year_days():
                new = 1 if healthy else 0                                      # from beyond: a beast bought, a drove passing
            cohorts, died = [], 0
            for c in rec["sick"]:
                if w.d - int(c["day"]) >= int(d["course"]):
                    k = sum(1 for _ in range(int(c["n"])) if rng.random() < float(d["mortality"]))
                    died += k
                    rec["immune"] = int(rec["immune"]) + int(c["n"]) - k
                else:
                    cohorts.append(c)
            if new:
                cohorts.append({"day": w.d, "n": new})
            for _ in range(died):
                h = w.s["herds"][hid]
                roles = [r for r in ("young", "cows", "oxen", "bulls") if int(h.get(r, 0)) > 0]
                if not roles:
                    break
                role = roles[int(rng.random() * len(roles))]
                w.apply("set", node, ref=("herd", hid), field=role, value=int(h[role]) - 1)
                w.apply("set", node, ref=("herd", hid), field="count", value=FM.head(w.s["herds"][hid]))
                TH.leave_carcass(w, node, FM.ROLE_WORD[role][0], h["name"], [c["claimant"] for c in w.claims_on(("herd", hid))], "sick",
                                 TECHNIQUES["slaughter"]["yield"]["gives"][role], parcel=h.get("parcel"), by=name)
            rec["immune"] = min(int(rec["immune"]), FM.head(w.s["herds"][hid]))
            rec["sick"] = cohorts
            if new:
                rec["new"] = w.d
            ill = dict(w.s["herds"][hid].get("ill") or {})
            if rec["sick"] or rec["immune"] or name in ill:
                ill[name] = rec
                if ill != (w.s["herds"][hid].get("ill") or {}):
                    w.apply("set", node, ref=("herd", hid), field="ill", value=ill)
            if new or died:
                out[hid] = {"disease": name, "new": new, "died": died}
                if died:
                    w.event(node, "herd", f"{died} of {h['name']} died of a sickness in the night", about=[f"herd:{hid}"], salience=0.6,
                            tags=["animals", "danger"])
    return out


def guard(here, pid, y, place_name) -> str:
    """A guard on a field against a load (picking slugs by lantern, topping the beans): cuts its harm there for some days."""
    from cybertron2.wild.kinds import LIGHT
    lit = bool(y.get("night")) and here.carried().get(LIGHT["item"], 0.0) >= 1          # work at night by a tallow light (brief 3
    if lit:                                                                               # §5): it does more, and the light is used
        here.apply("destroy", src=here.hands, item=LIGHT["item"], qty=1, why="burned down")
    cut = min(0.95, float(y["cut"]) * (float(LIGHT["night_work"]) if lit else 1.0))
    here.apply("set_wild", path=["guard", pid], value={"load": y["load"], "cut": cut, "until": here.day + int(y["days"]) - 1,
                                                        "by": here.name})
    for k, share in sorted((y.get("thin") or {}).items()):              # it kills some outright: the load on the land falls
        _thin(here, pid, k, float(share))
    return y.get("done", "You worked over {place}.").format(place=place_name) + (" You worked on into the dark by a tallow light." if lit else "")


def _thin(here, pid, load, share) -> None:
    """A load cut on one field: its village's level falls by the share times the field's part of the village's fields."""
    w = here._w
    land = w.s["wild"]["land"]
    m = model(w)
    aid = land.get("home", {}).get(here.node)
    L = (w.s["wild"].get("state") or {}).get("loads") or {}
    if aid not in m.ids or load not in (L.get("level") or {}):
        return
    i = m.ids.index(aid)
    cover = here.parcels()[pid]["cover"]                                 # its part of the village's ground of its kind
    fields = [p for p in here.parcels().values() if p["cover"] == cover]
    part = min(1.0, float(here.parcels()[pid]["size"]) / max(1.0, sum(float(p["size"]) for p in fields)))
    lv = list(L["level"][load])
    lv[i] = round(float(lv[i]) * (1 - share * part), 4)
    here.apply("set_wild", path=["state", "loads", "level", load], value=lv)


def work_notices(here, mind, tech, key) -> str:
    """What one notices while working a parcel (kinds.WORK_NOTICES): by the technique (any wild hunt reads "hunt"), for a kind about
    the village (in its ring), under a condition; each row by the one rule (D4-75: own x visibility x the eye), read by the practised,
    the expert or anyone; a find picked up. A process of its own, as the road's notices and the hunt's."""
    from cybertron2.engine import environment as EV, perceive as PC, signs as SG, things as TH
    from cybertron2.engine.data import NOTICING, TECHNIQUES
    from cybertron2.wild.kinds import WORK_NOTICES, MAST
    from types import SimpleNamespace
    w = here._w
    if not on(w) or not (w.s.get("wild") or {}).get("state"):
        return ""
    y = (TECHNIQUES[tech].get("yield") or {}).get("kind")
    group = tech if tech in WORK_NOTICES else ("hunt" if y == "wild_take" else None)
    if group is None:
        return ""
    st, land = w.s["wild"]["state"], w.s["wild"]["land"]
    m = model(w)
    ri = next((i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == here.node), None)
    par = here.parcels()[key]
    rng = here.rng("wild-work-notice", here.day, here.name, tech)
    eye = TH.eye(w, here.name)
    know = PC.practised(mind)
    rows = []
    for n_ in WORK_NOTICES[group]:
        k = n_.get("kind")
        if k is not None and (ri is None or k not in st["pop"] or float(st["pop"][k][ri]) * float(m.km2[ri]) < 1.0
                              or float(st["pop"][k][ri]) < float(n_.get("least", 0.0))):
            continue
        if not cond(w, here.node, n_.get("if"), k, m, st, ri):
            continue
        if n_.get("cover") and par["cover"] not in n_["cover"]:
            continue
        if n_.get("mast_coming"):
            M = st.get("mast") or {}
            prev = (M.get("years") or {}).get(str(eco_day(w) // w.year_days() - 1))
            if prev == MAST["levels"]["heavy"] or int(M.get("budget", 0)) + 1 < int(M.get("th", 3)) or any(st.get("flower_frost") or []):
                continue
        if n_.get("berries_heavy") and float(((par.get("res") or {}).get("berries") or {}).get("f", 1.0)) < 1.25 \
                and float(((par.get("res") or {}).get("hedge fruit") or {}).get("f", 1.0)) < 1.25:
            continue
        for r in n_["rows"]:
            row = dict(when=lambda x: True, own=float(r["own"]), sense=r["sense"], text=lambda x, t=r["text"]: t)
            if r["read"] in ("lay", "knows"):
                row[r["read"]] = "hunt" if group == "hunt" else tech
            elif r["read"] == "expert":
                row["knows"] = f"familiar:{k}" if k is not None else f"expert:{'hunt' if group == 'hunt' else tech}"
            rows.append((row, n_.get("find")))

    if tech == "gather wild food":                                         # an expert gatherer reads each kind's year here
        from cybertron2.wild.plants import EXPERT as PEX
        season = here.calendar()["season"]
        for k, r in sorted(par["res"].items()):
            ex = PEX.get(k)
            if not ex or float((r.get("seasons") or {}).get(season, 0.0)) <= 0:
                continue
            f = float(r.get("f", 1.0))
            txt = ex["heavy"] if f >= 1.3 else (ex["light"] if f <= 0.6 else None)
            if txt:
                rows.append((dict(when=lambda x: True, own=0.7, sense="sight", text=lambda x, t=txt: t, knows=f"expert:{tech}"), None))

    def rule(row):
        sense = row.get("sense", "sight")
        return float(row["own"]) * EV.visibility(w, here.node, parcel=key, sense=sense, cover=par.get("cover")) * (eye if sense in NOTICING["eye_senses"] else 1.0)
    seen = []
    for row, find in rows:
        got = SG.roll([row], SimpleNamespace(), rng, know=know, rule=rule)
        if got:
            seen += got
            if find and rng.random() < float(find["p"]):
                here.apply("create", dst=here.hands, item=find["item"], qty=1, why="found")
                seen[-1] += f" (you picked up the {find['item']})"
    return (" You noticed " + "; and ".join(seen[:2]) + ".") if seen else ""


# ---------------------------------------------------------------------- wild plants (wild_plants.md; D2-200, D2-202)
def _seed_plants(w) -> None:
    """At world build: each parcel's single `plants` capacity becomes the wild plant kinds that suit it (wild/plants.niche), each
    at its season's level now. A parcel no kind suits keeps its `plants`."""
    from cybertron2.wild import plants as PL
    season = w.calendar()["season"]
    for pid, par in sorted(w.s["parcels"].items()):
        pr = par["res"].get("plants")
        if not pr or float(pr.get("K", 0) or 0) <= 0:
            continue
        from cybertron2.engine.data import ITEMS
        kinds = PL.niche(par, float(pr["K"]), food={k: v.get("food", 1.0) for k, v in ITEMS.items()})
        if not kinds:
            continue
        del par["res"]["plants"]
        for k, K in sorted(kinds.items()):
            sp = PL.PLANTS[k]
            par["res"][k] = {"S": round(K * float(sp["seasons"].get(season, 0.0)), 4), "K": K, "r": float(sp["r"]), "rot": float(sp["rot"]),
                             "seasons": dict(sp["seasons"]), "f": 1.0}


def _plant_target(r, season) -> float:
    return float(r["K"]) * float((r.get("seasons") or {}).get(season, 0.0)) * float(r.get("f", 1.0))


def in_season(here, pid) -> bool:
    """Whether a parcel has any wild plant to gather now (above what is always left: the refuge), through the place's own view."""
    from cybertron2.engine.data import RESOURCES
    par = here.parcels()[pid]
    season = here.calendar()["season"]
    return any(float(r["S"]) > (float(here.p["refuge"]) + 0.02) * float(r["K"]) * max(0.05, float((r.get("seasons") or {}).get(season, 0.0)))
               and float(r["S"]) > 1e-3 for k, r in par["res"].items() if (RESOURCES.get(k) or {}).get("plant"))


def _plant_year(w, m, st) -> None:
    """Each plant kind's year at each village (its `f`): a keyed draw, the trees' mast, the fungus load or the spring's warmth, by
    the kind's data; written to the parcels' stocks when it changes."""
    from cybertron2.wild import plants as PL
    Y = w.year_days()
    k0 = eco_day(w)
    year, si = k0 // Y, (k0 % Y) // (Y // 4)
    land = w.s["wild"]["land"]
    L = st.get("loads") or {}
    for node, aid in sorted((land.get("home") or {}).items()):
        if aid not in m.ids:
            continue
        i = m.ids.index(aid)
        fs = {}
        for k, sp in PL.PLANTS.items():
            src, amt = sp["swing"]
            if src == "draw":
                f = 1.0 + float(amt) * (2 * w.rng("wild-plant", year, node, k).random() - 1)
            elif src == "mast":
                f = min(2.5, float(st.get("mast_now") or 1.0)) if si >= 2 else 1.0
            elif src == "load":
                f = min(2.5, float(((L.get("level") or {}).get(amt) or [1.0] * m.n)[i]))
            else:
                g = (L.get("spring_gdd") or [None] * m.n)[i]
                f = 1.0 if g is None else 1.0 + float(amt) * 2 * (float(g) / PL.SPRING_GDD - 1)
            fs[k] = round(max(0.0, min(2.5, f)), 3)
        for pid, par in sorted(w.s["parcels"].items()):
            if par["node"] != node:
                continue
            for k, f in fs.items():
                r = par["res"].get(k)
                if r is not None and abs(float(r.get("f", 1.0)) - f) > 0.005:
                    w.apply("set_res", node, parcel=pid, key=k, fields={"f": f})


def _food_stocks(w, nd, food):
    from cybertron2.wild import plants as PL
    for pid, par in sorted(w.s["parcels"].items()):
        if par["node"] != nd:
            continue
        for k in PL.SHARED.get(food, []):
            r = par["res"].get(k)
            if r and float(r.get("K", 0)) > 0:
                yield pid, par, k, r


def _shared_pre(w, m, st):
    """D2-202: on a village's own land the wild kinds eat the parcels' stocks. Each shared food's availability there is the share
    of its stocks standing against their level for the season (gathered or grazed down, it is less; none on the land, none): it
    scales what the ecology lets them eat. Returns that scale and the ecology's pools before the step."""
    from cybertron2.wild import plants as PL
    season = w.calendar()["season"]
    scale, pools = {}, {}
    for food in PL.SHARED:
        a = np.ones(m.n)
        for i, nd in enumerate(m.nodes):
            if not m.home[i]:
                continue
            S = T = 0.0
            for pid, par, k, r in _food_stocks(w, nd, food):
                S += float(r["S"])
                T += _plant_target(r, season) if (r.get("seasons")) else float(r["K"])
            a[i] = 0.0 if T <= 1e-9 and S <= 1e-9 else min(1.5, S / max(T, 1e-9))
        scale[food] = a
        pools[food] = sum(np.asarray((st["stock"].get(key) if key in st["stock"] else st["pulse"].get(key)) or np.zeros(m.n), float)
                          for key in (food, food + "~coarse") if key in st["stock"] or key in st["pulse"])
    return scale, pools


def _shared_post(w, m, scale, pools, eff) -> dict:
    """What the wild kinds ate of the shared foods at a village tonight, as a share of what was there for them, drawn from the
    parcels' stocks (D2-202): foods that are the same stock (grass and sward are both the pasture) drawn once, at most SHARED_MOST a
    night (a village's land is busy: its wild grazers are few and shy), a fence keeping out its share (FENCES' through)."""
    from cybertron2.engine.data import FENCES
    from cybertron2.wild import plants as PL
    out = {}
    stocks = {}
    for food in pools:
        stocks.setdefault(tuple(PL.SHARED[food]), []).append(food)
    for keys, foods in sorted(stocks.items()):
        ate = sum(np.asarray(eff["eaten"].get(k, np.zeros(m.n)), float) for f in foods for k in (f, f + "~coarse"))
        for i, nd in enumerate(m.nodes):
            if not m.home[i]:
                continue
            there = sum(float(np.asarray(pools[f])[i]) * float(scale[f][i]) for f in foods) * float(m.km2[i])
            share = min(SHARED_MOST, float(np.asarray(ate)[i]) / there) if there > 1e-9 else 0.0
            if share <= 1e-5:
                continue
            for pid, par, k, r in _food_stocks(w, nd, foods[0]):
                fc = par.get("fence") or {}
                through = float(FENCES[fc["kind"]]["through"].get(int(fc.get("level", 0)), 1.0)) if fc.get("built") and fc.get("kind") in FENCES else 1.0
                q = round(float(r["S"]) * share * through, 4)
                if q > 1e-6:
                    w.apply("draw", nd, parcel=pid, key=k, qty=q)
                    for f in foods[:1]:
                        out.setdefault(nd, {}).setdefault(f, {})[pid] = round(out.get(nd, {}).get(f, {}).get(pid, 0.0) + q, 4)
    return out


SHARED_MOST = 0.03


def _wanted_plants(target, kinds) -> set:
    """The plant kinds a gatherer's words name: a kind, its good, or a word of what it is (nuts, berries, mushrooms); none for any."""
    from cybertron2.wild import plants as PL
    t = str(target or "").strip().lower()
    if not t or t in ("anything", "whatever", "food", "any", "wild food"):
        return set()
    out = set()
    for k in kinds:
        sp = PL.PLANTS.get(k) or {}
        words = {k, sp.get("item", ""), *[x.strip() for x in sp.get("words", "").replace(" and ", ", ").split(",")]}
        if any(t == x or t.rstrip("s") == x.rstrip("s") or (x and t in x.split()) or (x and x in t) for x in words if x):
            out.add(k)
    return out


def forage(here, mind, tech, key, place_name, out, mult, y, a) -> tuple:
    """Gathering wild food (D2-200): what is in season on the parcel, by how much stands and how easy each is, more of what one looks
    for; each kind into its good. Mushrooms gathered by one who does not know them may make one ill (D2-201): by a practised gatherer
    seldom, an expert never."""
    from cybertron2.engine import perceive as PC
    from cybertron2.engine.data import RESOURCES
    from cybertron2.wild import plants as PL
    par = here.parcels()[key]
    kinds = {k: r for k, r in sorted(par["res"].items()) if (RESOURCES.get(k) or {}).get("plant")}
    want = _wanted_plants(a.get("looking for"), kinds)
    floor = float(here.p["refuge"])
    avail = {k: max(0.0, float(r["S"]) - floor * float(r["K"]) * float((r.get("seasons") or {}).get(here.calendar()["season"], 0.0)))
             for k, r in kinds.items()}
    total = sum(avail.values())
    budget = sum(float(r["K"]) * PL.mean_season(k) for k, r in kinds.items())
    rng = here.rng("wild-forage", here.day, here.name, key)
    if total <= 1e-6 or budget <= 1e-9:
        return 0.0, f"You found nothing in season to gather at {place_name}."
    q = min(0.5 * total, float(y["base"]) * mult * min(1.5, total / budget) * (0.7 + 0.6 * rng.random()))
    wt = {k: v * float(PL.PLANTS[k]["ease"]) * ((3.0 if k in want else 0.4) if want else 1.0) for k, v in avail.items()}
    tw = sum(wt.values())
    got, food = {}, 0.0
    from cybertron2.engine.data import ITEMS
    for k, v in sorted(wt.items()):
        take = round(min(avail[k], q * v / tw), 2)
        if take <= 1e-6:
            continue
        here.apply("draw", parcel=key, key=k, qty=take)
        item = PL.PLANTS[k]["item"]
        here.apply("create", dst=out, item=item, qty=take, why=tech)
        got[item] = round(got.get(item, 0.0) + take, 2)
        food += take * float(ITEMS[item]["food"])
    PC.remember_land(mind, here.day, key, "wild food", "good" if total / budget > 0.5 else "thin", "found")
    if not got:
        return 0.0, f"You found nothing in season to gather at {place_name}."
    word = f"You gathered {', '.join(f'{v:g} {k}' for k, v in sorted(got.items()))} at {place_name}"
    sick = ""
    for k, take in ((k, got.get(PL.PLANTS[k]["item"], 0.0)) for k in kinds if PL.PLANTS[k].get("poison")):
        if take <= 0:
            continue
        know = PC.practised(mind)
        p = 0.0 if f"expert:{tech}" in know else float(PL.PLANTS[k]["poison"]) * (0.25 if tech in know else 1.0)
        if rng.random() < p * min(1.0, take):
            here.apply("harm", person=here.name, hunger=max(-2, int(here._w.s["people"][here.name].get("hunger", 0)) - 1))
            sick = " Some of them were bad: your belly cramped and you brought up what you had eaten."
            if tech not in know and rng.random() < 0.08:
                here.apply("die", person=here.name, cause=f"poisoned by {PL.PLANTS[k]['item']} gathered at {place_name}")
                sick = " Some of them were deadly."
    return food, word + "." + sick


def _follow_harvest(w, m, st, real) -> dict:
    """Within days of the harvest coming in, rats and mice move from the hedges to the barns (wild_systems.md §6, followers): the
    stores the ecology's kinds find on a village's land follow its real stores against their running mean, so a full barn after the
    harvest feeds (and draws) more of them. Returns that scale for the step."""
    from cybertron2.wild.kinds import FOLLOW_HARVEST
    seen = st.setdefault("stores_seen", [0.0] * m.n)
    a = np.ones(m.n)
    for i, nd in enumerate(m.nodes):
        if not m.home[i]:
            continue
        now = float(real["stores"].get(i, 0.0))
        base = float(seen[i]) if seen[i] > 1e-9 else now
        a[i] = 1.0 if base <= 1e-9 else float(np.clip(now / base, 0.2, 1.0 + 2.0 * max(FOLLOW_HARVEST.values())))
        seen[i] = round(0.9 * base + 0.1 * now, 4)
    return a


# ---------------------------------------------------------------------- wave 5: sites, individuals, rare regimes
def _site_candidates(w, node, where) -> list:
    out = []
    for pid, par in sorted(w.s["parcels"].items()):
        if par["node"] != node or par["cover"] not in where["covers"]:
            continue
        river = (par.get("land") or {}).get("river") not in (None, "none")
        beside = any((w.s["parcels"].get(q) or {}).get("cover") in (where.get("beside") or []) for q in par.get("adj") or [])
        if where.get("river") and not river:
            continue
        if where.get("beside") and not (beside or (where.get("or_river") and river)):
            continue
        out.append(pid)
    return out


def _seed_sites(w) -> None:
    """At world build: each village's sites where its land suits them (kinds.SITES), by a keyed draw; a beaver's dam is standing."""
    from cybertron2.wild.kinds import SITES
    sites = {}
    for node in sorted({p["node"] for p in w.s["parcels"].values()}):
        if node not in ((w.s["wild"].get("land") or {}).get("home") or {}):
            continue
        for kind, sp in sorted(SITES.items()):
            cand = _site_candidates(w, node, sp["where"])
            r = w.rng("wild-site", node, kind)
            if not cand or r.random() >= float(sp["p"]):
                continue
            pid = cand[int(r.random() * len(cand))]
            lo, hi = sp["size"]
            sites[f"{kind}@{pid}"] = {"kind": kind, "node": node, "parcel": pid, "size": float(lo + int(r.random() * (hi - lo + 1))),
                                      "last": None, "gone": None, "back": None, "dam": bool(sp.get("dam")), "k0": {}}
    w.s["wild"]["sites"] = sites
    for sid, site in sorted(sites.items()):
        if site["dam"]:
            _dam(w, sid, site, True, direct=True)


def _dam(w, sid, site, up, direct=False) -> None:
    """A beaver's dam up or down: the low ground beside it flooded (its grass's capacity cut), the water's fish raised, the drowned
    trees dead wood; down, all as it was."""
    from cybertron2.wild.kinds import SITES
    d = SITES[site["kind"]]["dam"]
    par = w.s["parcels"][site["parcel"]]
    near = [q for q in [site["parcel"]] + list(par.get("adj") or []) if q in w.s["parcels"]]
    k0 = dict(site.get("k0") or {})
    seen = set()                                                            # a water body's stock raised once (D2-229)
    for q in near:
        p_ = w.s["parcels"][q]
        for key, mult, covers in ((d["floods"]["res"], d["floods"]["K"], d["floods"]["covers"]), ("fish", d["fish"], ["water"])):
            r = (p_.get("res") or {}).get(key)
            if not r or p_["cover"] not in covers or id(r) in seen:
                continue
            seen.add(id(r))
            base = float(k0.get(f"{q}|{key}", r["K"]))
            k0[f"{q}|{key}"] = base
            K = round(base * (float(mult) if up else 1.0), 4)
            fields = {"K": K, "S": round(min(float(r["S"]), K), 4)} if K < float(r["K"]) else {"K": K}
            if direct:
                r.update(fields)
            else:
                w.apply("set_res", site["node"], parcel=q, key=key, fields=fields)
    if up and "dead" in (par.get("res") or {}):
        if direct:
            par["res"]["dead"]["S"] = round(float(par["res"]["dead"]["S"]) + float(d["dead"]), 4)
        else:
            w.apply("add_res", site["node"], parcel=site["parcel"], key="dead", qty=float(d["dead"]))
    site["k0"], site["dam"] = k0, bool(up)


def _sites_night(w, m, st) -> dict:
    """Each site's night (kinds.SITES): at the start of its season it comes back grown toward its cap, or crashed after a hard winter
    (or a great freeze); worked or hunted on in its season it may leave for good; it eats or harms the land about it; a broken dam
    is rebuilt in days while the family lives."""
    from cybertron2.engine import farm as FM
    from cybertron2.wild.kinds import SITES, REGIMES
    import copy
    sites = copy.deepcopy(w.s["wild"].get("sites") or {})
    if not sites:
        return {}
    watch = {pid for pid, v in (w.s["wild"].get("watch") or {}).items() if int(v.get("day", -9)) == w.d}
    worked = {}
    for e in w.s.get("events") or []:
        if e.get("kind") == "work":
            for ab in e.get("about") or []:
                if str(ab).startswith("parcel:"):
                    worked.setdefault(ab[7:], set()).add(e.get("tech"))
    out = {}
    for sid, site in sorted(sites.items()):
        sp = SITES[site["kind"]]
        if site.get("gone") is not None:
            continue
        node, pid = site["node"], site["parcel"]
        si, sd = _season_of(w, w.d)
        win = sp["season"]
        if si in win and sd == win[si][0]:                                # its season begins: back, grown or crashed
            site["last"] = site["size"]
            hw = sp.get("hard_winter")
            if hw and cond(w, node, {"hard_winter": int(hw["frozen"])}):
                site["size"] = round(float(site["size"]) * (1 - float(hw["crash"])), 2)
                site["why"] = "crash"
            else:
                cap = float(sp["cap"])
                fol = (sp.get("eats") or {}).get("follows")
                if fol:                                                    # the heads the village's stock can keep (brief 5 §4)
                    have = _site_stock(w, node, sp["eats"])
                    if have:
                        cap = min(cap, sum(have.values()) / float(fol))
                size0 = float(site["size"])
                site["size"] = round(size0 + float(sp["grow"]) * (cap - size0), 2)
                site["why"] = "grew" if site["size"] >= size0 or cap >= float(sp["cap"]) else "few"
            site["back"] = w.d
        for name, rg in REGIMES.items():                                   # a great freeze takes the herons
            if site["kind"] in (rg.get("site_crash") or {}) and name in REGIMES_ON(w, node) and site.get("froze") != w.d - 1:
                site["size"] = round(float(site["size"]) * (1 - float(rg["site_crash"][site["kind"]])), 2)
                site["froze"], site["why"] = w.d, "freeze"
        trouble = (worked.get(pid) or set()) & set(sp.get("troubled_by") or []) if sp.get("troubled_by") else worked.get(pid)
        if float(sp.get("leaves", 0)) > 0 and _season_window(w, w.d, win) and trouble:
            if w.rng("wild-site-leave", w.d, sid).random() < float(sp["leaves"]):
                site["gone"] = w.d                                          # troubled at the nests: gone for years (D2-198)
                out[sid] = {"gone": True}
                continue
        if sp.get("eats"):                                                 # its need, shared over the village's stock (brief 5 §4)
            e_ = sp["eats"]
            have = _site_stock(w, node, e_)
            tot = sum(have.values())
            need = float(e_["each"]) * float(site["size"])
            for q, S_ in sorted(have.items()):
                qty = round(min(float(e_["most"]) * S_, need * S_ / tot), 4) if tot > 1e-9 else 0.0
                if qty > 1e-6:
                    w.apply("draw", node, parcel=q, key=e_["res"], qty=qty)
        if sp.get("harm") and _season_window(w, w.d, win):
            h = sp["harm"]
            near = set(w.s["parcels"][pid].get("adj") or []) if h.get("beside") else {q for q, p_ in w.s["parcels"].items() if p_["node"] == node}
            for q in sorted(near):
                par = w.s["parcels"].get(q) or {}
                if par.get("node") != node or par.get("cover") != "field" or (h.get("watch_stops") and q in watch):
                    continue
                for hd, _, c in FM.standing(par):
                    age = w.d - int(c.get("sown", w.d))
                    qty = round(float(c.get("left", 0.0)) * min(0.2, float(h["share"]) * float(site["size"])), 4)
                    if c.get("crop") in h["crops"] and h["age"][0] <= age <= h["age"][1] and qty > 1e-9 and c.get("area_left", 0) > 1e-6:
                        w.apply("draw", node, parcel=q, key="crop", qty=qty, **({"holder": hd} if hd is not None else {}))
                        site["harm_day"], site["harm_at"] = w.d, q
                        out.setdefault(sid, {})["harm"] = round(out.get(sid, {}).get("harm", 0.0) + qty, 4)
        if sp.get("dam") and not site.get("dam") and float(site["size"]) >= 1 and \
                w.d - int(site.get("broken", w.d)) >= int(round(float(sp["dam"]["rebuild_seasons"]) * w.season_len)):   # down a season (brief 5 §4)
            _dam(w, sid, site, True)
            site["rebuilt"] = w.d
    if sites != (w.s["wild"].get("sites") or {}):
        w.apply("set_wild", m.nodes[0], path=["sites"], value=sites)
    return out


def _site_stock(w, node, e_) -> dict:
    """{parcel: stock standing} of a site's `eats` stock on the village's parcels of its covers."""
    from cybertron2.engine import waters as WA
    out = {}
    for q, par in sorted(w.s["parcels"].items()):
        r = (par.get("res") or {}).get(e_["res"])
        if par["node"] == node and par["cover"] in e_["covers"] and r and float(r["S"]) > 0 and WA.lead(w, q, e_["res"]):
            out[q] = float(r["S"])                                             # a water body's stock once (D2-229)
    return out


def site_work(here, key, y, place_name, mult) -> str:
    """Taking from a site (the young from a heronry or rookery, in their season), trapping at a lodge, or breaking a dam."""
    from cybertron2.wild.kinds import SITES
    import copy
    w = here._w
    sid, site = next(((k, v) for k, v in sorted((w.s["wild"].get("sites") or {}).items()) if v["parcel"] == key and v["kind"] == y["site"]
                      and v.get("gone") is None), (None, None))
    if site is None:
        return f"There is no {y['site']} at {place_name}."
    site = copy.deepcopy(site)
    sp = SITES[site["kind"]]
    if y["do"] == "take":
        t = sp["take"]
        if not _season_window(w, here.day, t["season"]):
            return f"There are no young in the nests at {place_name} now."
        k = int(min(float(t["most"]), max(1.0, round(float(site["size"]) * 0.15 * mult))))
        k = min(k, int(site["size"]))
        if k < 1:
            return f"You found nothing to take at {place_name}."
        site["size"] = round(float(site["size"]) - k, 2)
        here.apply("create", dst=here.hands, item=t["item"], qty=round(k * float(t["each"]), 2), why="taken from the nests")
        word = f"You took {k} {t['words']} at {place_name}: {round(k * float(t['each']), 2):g} {t['item']}."
    elif y["do"] == "trap":
        if float(site["size"]) < 1:
            return f"There are no beavers left at {place_name}."
        site["size"] = round(float(site["size"]) - 1, 2)
        tr = sp["trap"]
        here.apply("create", dst=here.hands, item=tr["item"], qty=1, why="trapped")
        for it, q in (tr.get("also") or {}).items():
            here.apply("create", dst=here.hands, item=it, qty=float(q), why="trapped")
        if float(site["size"]) < 1:
            site["gone"] = here.day
        word = f"You trapped a beaver at {place_name}: a pelt and the castoreum." + (" That was the last of them." if site.get("gone") is not None else "")
    else:
        if not site.get("dam"):
            return f"The dam at {place_name} is already down."
        _dam(w, sid, site, False)
        site["broken"] = here.day
        word = f"You broke open the beaver dam at {place_name}; the water runs out of the meadow."
    here.apply("set_wild", path=["sites", sid], value=site)
    return word


def _site_at(w, key, homes) -> tuple:
    from cybertron2.wild.kinds import SITES
    return next(((k, v) for k, v in sorted((w.s["wild"].get("sites") or {}).items()) if v["parcel"] == key and v.get("gone") is None
                 and SITES[v["kind"]].get("home") in homes), (None, None))


def set_work(here, mind, tech, key, place_name) -> str:
    """Setting a snare line or traps (brief 2 §4): a thing at the parcel that catches by night for its life; the setter knows it."""
    from cybertron2.engine.data import TECHNIQUES
    sp = TECHNIQUES[tech]["set"]
    cid = here.apply("new_thing", node=here.node, parcel=key, kind="set", by=here.name,
                     set={"method": tech, "life": int(sp["life"]), "base": float(sp["base"]), "set_day": here.day,
                          "line": int(sp.get("line", 1)), "holds": int(sp.get("holds", 1)) * int(sp.get("line", 1))})
    here.remember_thing(cid, "put")
    what = "traps in the water" if tech == "trap in water" else "a line of snares"
    return f"You set {what} at {place_name}; they will catch by night for about {int(sp['life'])} nights, for whoever comes to them."


def _set_night(w, m, st) -> dict:
    """Each set thing draws once a night by the take's rule (brief 2 §4): the kinds in its village's home area and ring, the method's
    table and cue rows, the setter's skill and familiarity, at a lower chance than a hunter there; a catch goes into it as the kind's
    goods; a spent one is sprung."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import RESOURCES, TECHNIQUES
    from cybertron2.wild import methods as MT
    from cybertron2.wild.kinds import HUNT
    land = w.s["wild"]["land"]
    out = {}
    pop = {k: [float(x) for x in v] for k, v in st["pop"].items()}
    run = run_density(w, m, st)                                           # a run passing tonight (brief 5 §2.4)
    runs = None
    for cid, c in sorted(w.s["containers"].items()):
        sp = c.get("set")
        if c.get("kind") != "set" or not sp or sp.get("sprung") is not None or sp.get("weir"):   # a weir's traps: its own rule
            continue
        node = c["node"]
        if w.d - int(sp["set_day"]) >= int(sp["life"]):
            w.apply("set_thing", node, cid=cid, field="set", value=dict(sp, sprung=w.d))
            continue
        tech = sp["method"]
        y = TECHNIQUES[tech]["yield"]
        areas = [i for i, a in enumerate(m.ids) if land.get("home", {}).get(node) == a
                 or (land["areas"][a]["kind"] == "ring" and land["areas"][a].get("node") == node)]
        ri = next((i for i in areas if land["areas"][m.ids[i]]["kind"] == "ring"), areas[0] if areas else None)
        if ri is None:
            continue
        rows = [r for r in (y.get("when") or []) if cond(w, node, r.get("if"), None, m, st, ri)]
        mind = SimpleMind(w, c.get("by"))
        cand = []
        for k, tw in sorted((y.get("takes") or {}).items()):
            if k not in pop:
                continue
            tk = (RESOURCES.get(k) or {}).get("taken") or {}
            tr = tk.get("traits") or {}
            x = 1.0
            for r in rows:
                if all(tr.get(t) == v for t, v in (r.get("for") or {}).items()):
                    x *= float(r.get("x", 1.0))
            for i in areas:                                                # by density on the ground the sets cover (brief 4 §2.10):
                dens = pop[k][i] + (run[k][i] if k in run else 0.0)        # the village's own land, and half that from the ring
                cnt = dens * float(m.km2[i])
                gr = min(float(m.km2[i]), float(sp.get("ground", 0.2)) * (1.0 if m.home[i] else 0.5))
                wgt = dens * gr * float(tk.get("detect", 0.2)) * float(tw) * x * MT.factor(mind, k)
                if wgt > 0 and cnt >= 1.0:
                    cand.append((k, i, wgt))
        total = sum(x[2] for x in cand)
        rng = w.rng("wild-set", w.d, cid)
        effort = float(TECHNIQUES[tech]["units"]) / 2.0 * float(sp["base"]) * int(sp.get("line", 1))
        held = int(c.get("caught", 0) or 0) if any(float(q) > 1e-9 for q in c["goods"].values()) else 0   # emptied: room again
        room = int(sp.get("holds", 1)) - held                               # a snare holds one beast, a wicker trap several
        meet = float(TECHNIQUES[tech].get("set", {}).get("meet", HUNT["set_meet"]))
        tries = _poisson(rng, meet * total * effort, max(0, room)) if total > 0 else 0   # (brief 4 §2.10:
        skill = float(((w.s["know"].get(c.get("by")) or {}).get(tech) or {}).get("skill", KN.curve(tech)[0]))   # the run shows)
        got = []
        cap = None
        if tech == "trap in water":                                       # a set trap in water holds about 3 food (D2-213)
            from cybertron2.engine.data import ITEMS, WATER_WORKS
            cap = float(WATER_WORKS["trap"]["hold"]) - sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0.0))
                                                            for i, q in c["goods"].items())
        for _ in range(tries):
            u, acc = rng.random() * total, 0.0
            for k, i, wgt in cand:
                acc += wgt
                if u < acc:
                    break
            tk = (RESOURCES.get(k) or {}).get("taken") or {}
            p = chance(0.6 * skill * float(sp["base"]) * (1 - float(tk.get("flee", 0.5))) * MT.factor(mind, k))   # brief 4c §3.1 (0.6 keeps brief 4's catch within about 6%)
            if rng.random() >= p:
                continue
            if cap is not None:                                           # no room for it: it swims free
                if _food_of(k) > cap + 1e-9:
                    continue
                cap -= _food_of(k)
            r_ = run[k][i] if k in run else 0.0
            if r_ > 0 and rng.random() < r_ / (r_ + pop[k][i]):          # one of the run's
                from cybertron2.wild import runs as RU
                import copy
                runs = runs if runs is not None else {"runs": copy.deepcopy(st["runs"])}
                if RU.take_one(m, runs, eco_day(w), k, i):
                    run[k][i] = max(0.0, run[k][i] - 1.0 / float(m.km2[i]))
                    w.apply("set_wild", node, path=["state", "runs", "pulses"], value=copy.deepcopy(runs["runs"]["pulses"]))
            else:
                pop[k][i] = max(0.0, pop[k][i] - 1.0 / float(m.km2[i]))
                w.apply("set_wild", node, path=["state", "pop", k], value=pop[k])
            for item, q in sorted((tk.get("goods") or {}).items()):
                w.apply("create", node, dst=cid, item=item, qty=float(q), why="caught in a set")
            got.append(k)
        if got:
            w.apply("set_thing", node, cid=cid, field="caught", value=held + len(got))
            had = list(c.get("catch") or []) if held else []                   # what it holds, by the night caught (brief 4c §4)
            w.apply("set_thing", node, cid=cid, field="catch", value=had + [{"kind": k, "day": w.d} for k in got])
            out[cid] = got[0] if len(got) == 1 else got
    return out


class SimpleMind:
    """A setter's mind store, for familiarity read away from them (a set thing catching by night)."""
    def __init__(self, w, name):
        self.store = (w.s.get("mind") or {}).get(name) or {}


def den_work(here, mind, tech, key, place_name, out, m_skill, y, a) -> tuple:
    """Den work (D2-204): at a lodge, the site's trap; elsewhere a take of the den-dwellers (the fox and her cubs in spring)."""
    sid, site = _site_at(here._w, key, ("lodge",))
    if site is not None:
        from cybertron2.engine import knowledge as KN
        from cybertron2.engine.data import TECHNIQUES
        KN.tried(here, mind, tech, True, units=TECHNIQUES[tech]["units"])   # practised here; a take practises in the hunt (4c §3.3)
        return 0.0, site_work(here, key, {"site": site["kind"], "do": "trap"}, place_name, m_skill), ""
    return take(here, mind, tech, key, place_name, out, m_skill, y, a)


def young(here, key, place_name, mult) -> str:
    """Gathering young (D2-204): the young from whichever colony is at the parcel (a heronry or a rookery), in its season."""
    sid, site = _site_at(here._w, key, ("colony",))
    if site is None:
        return f"There is no heronry or rookery at {place_name}."
    return site_work(here, key, {"site": site["kind"], "do": "take"}, place_name, mult)


def pest(here, key, place_name, a) -> str:
    """Pest work (D2-204): the pest named with `looking for`, else the worst on this field's village's land: its guard row (on the
    load: cut, days, what it kills) as the old rows had it."""
    from cybertron2.wild.kinds import LOADS
    from cybertron2.wild.methods import LOAD_NAMES
    from cybertron2.engine.here import Refused
    w = here._w
    crop = [k for k, r in LOADS.items() if r.get("on_crop") and r.get("guard")]
    want = str(a.get("looking for") or "").strip().lower()
    if want:
        named = [k for k in crop if want == k or want in LOAD_NAMES.get(k, ())]
        if not named:
            from cybertron2.engine.data import RESOURCES                       # a raider, not a pest of the crop: say what answers it
            raider = next((k for k, r in sorted(RESOURCES.items()) if r.get("near_people") and (want.rstrip("s") in k
                           or want in (r.get("taken") or {}).get("family", []))), None)
            if raider:
                raise Refused(f"{a.get('looking for')} are not worked off a crop like a pest: a watch on the field (guard the field) "
                              "or something to scare them keeps them off")
            raise Refused(f"you know of no pest called {a.get('looking for')!r} on a crop")
        load = named[0]
    else:
        m = model(w) if (w.s.get("wild") or {}).get("state") else None
        aid = (w.s["wild"].get("land") or {}).get("home", {}).get(here.node) if m else None
        L = ((w.s["wild"].get("state") or {}).get("loads") or {}).get("level") or {}
        i = m.ids.index(aid) if m and aid in m.ids else None
        from cybertron2.engine import farm as FM
        par = w.s["parcels"].get(key) or {}
        kinds = {c.get("crop") for _, _, c in FM.standing(par)}

        def fits(k):                                                       # a pest of this ground: of its standing crop, or of
            r = LOADS[k]                                                   # its grass (moles on a meadow)
            return any(set(h.get("crops") or []) & kinds for h in r.get("harm") or []) \
                or any(par.get("cover") in (h.get("covers") or []) for h in r.get("harm_res") or [])
        harm = [k for k in crop if LOADS[k].get("harm") or LOADS[k].get("harm_res")]   # never the ladybirds unasked
        harm = [k for k in harm if fits(k)] or harm                        # the worst of those that harm here
        load = max(harm, key=lambda k: float(L.get(k, [0.0])[i]) if i is not None and k in L else 0.0) if harm else crop[0]
    return guard(here, key, {"load": load, **LOADS[load]["guard"]}, place_name)


def _seed_legends(w) -> None:
    """At world build, seldom: a legendary beast of a kind present in the world (D2-195), in the area its kind is thickest."""
    from cybertron2.wild.kinds import LEGENDS
    st = w.s["wild"].get("state") or {}
    if not st.get("pop"):
        return
    m = model(w)
    out = {}
    for kind, lg in sorted(LEGENDS.items()):
        if kind not in st["pop"]:
            continue
        counts = [float(st["pop"][kind][i]) * float(m.km2[i]) for i in range(m.n)]
        scale = float((w.spec.get("wild") or {}).get("legend_scale", 1.0))   # an experiment's knob: how seldom
        if sum(counts) < 1.0 or w.rng("wild-legend", kind).random() >= float(lg["p"]) * scale:
            continue
        i = max(range(m.n), key=lambda j: (counts[j] * (0.0 if m.home[j] else 1.0), -j))
        out[kind] = {"name": lg["name"], "area": m.ids[i], "alive": True}
    w.s["wild"]["legends"] = out


def REGIMES_ON(w, node) -> dict:
    """The rare regimes holding at a village today (kinds.REGIMES)."""
    from cybertron2.wild.kinds import REGIMES
    st = (w.s.get("wild") or {}).get("state") or {}
    land = (w.s.get("wild") or {}).get("land") or {}
    out = {}
    for name, rg in REGIMES.items():
        if not cond(w, node, rg.get("if")):
            continue
        if rg.get("of"):
            m = model(w)
            ri = next((i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == node), None)
            if ri is None or float(st["pop"][rg["of"]][ri]) < float(rg["least"]):
                continue
        out[name] = rg
    return out


def _regime_kills(w, m, st) -> None:
    """A rare regime's kill among kinds (a great freeze: the fowl, the owls), in each area of a village where it holds."""
    from cybertron2.wild.kinds import REGIMES
    for node in sorted(set(m.nodes)):
        on_ = REGIMES_ON(w, node) if node in w.s["nodes"] else {}
        for name, rg in on_.items():
            for k, share in (rg.get("kill") or {}).items():
                if k in st["pop"]:
                    st["pop"][k] = [float(x) * (1 - float(share)) if m.nodes[i] == node else float(x) for i, x in enumerate(st["pop"][k])]


def _shares(out, real, m) -> dict:
    """What share of each home's standing crop and store the wild kinds ate tonight, for the signs (signs._wild_eaten)."""
    res = {}
    for i, nd in enumerate(m.nodes):
        if not m.home[i]:
            continue
        for food in ("crops", "stores"):
            lost, have = float(out[food].get(nd, 0.0)), float(real[food].get(i, 0.0))
            if lost > 1e-6 and have > 1e-9:
                res.setdefault(nd, {})[food] = round(lost / have, 4)
    return res


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


def _trace(traces, pid, kind, what, day, n, scare=None, by=None):
    lst = [t for t in traces.get(pid, []) if day - int(t["day"]) <= 3]
    lst.append({k: v for k, v in dict(kind=kind, what=what, day=day, n=int(n), scare=scare, by=by).items() if v is not None})
    traces[pid] = lst


# ---------------------------------------------------------------------- conditions and effects (02zq; wild_systems.md §6, §10)
LEVEL_NAMES = None


def _level_name(x) -> str:
    from cybertron2.wild.kinds import MAST
    L = MAST["levels"]
    return min(L, key=lambda k: abs(float(L[k]) - float(x)))


def _wx(w, node, day):
    return weather(w, [node], max(0, day))[node]


def _frozen_day(w, node, day) -> bool:
    v = _wx(w, node, day)
    return v["low"] < -3.0 and v["temp"] < 3.0


def frozen_run(w, node, day=None, most=6) -> int:
    day = w.d if day is None else day
    n = 0
    while n < most and day - n >= 0 and _frozen_day(w, node, day - n):
        n += 1
    return n


def _home_i(w, m, node):
    land = (w.s.get("wild") or {}).get("land") or {}
    aid = (land.get("home") or {}).get(node)
    return m.ids.index(aid) if aid in m.ids else None


def _water_parts(m, i) -> dict:
    """An area's water as shares of its land, by how long each stays open in a frost (kinds.OPEN_WATER): its lakes, its big river,
    and the rest (the small waters: pools, brooks, ponds), from the land summary (wild/areas.py) as the ecology's `water` feature."""
    a = m.land["areas"][m.ids[i]]
    km2 = max(float(m.km2[i]), 1e-6)
    total = float(m.f["water"][i])
    lake = min(total, float(a.get("lake_km2", 0.0)) / km2)
    big = min(total - lake, 0.6 * float(a.get("big_river_km", 0.0)) * float(m.land.get("km", 0.15)) / km2)
    return {"small": max(0.0, total - lake - big), "big river": big, "lake": lake}


def open_water(w, m, i, node, day=None, kind=None) -> float:
    """The cold's push at area i (brief 5 §4; kinds.OPEN_WATER, PUSHED): what a pushed kind's density at the water is multiplied by.
    1 with no hard frost at the node or no water in the area; on a frost of n nights in a row, its wet ground and water over the
    water still open (each part open while n is within its `hold`), at most the kind's `most`; 0 when all of it is frozen over."""
    from cybertron2.wild.kinds import OPEN_WATER, PUSHED
    parts = _water_parts(m, i)
    total = sum(parts.values())
    if total <= 1e-9:
        return 1.0
    hold = OPEN_WATER["hold"]
    n = frozen_run(w, node, day, most=max(int(x) for x in hold.values()) + 1)
    if n <= 0:
        return 1.0
    open_ = sum(v for k, v in parts.items() if n <= int(hold[k]))
    if open_ <= 1e-9:
        return 0.0
    most = float((PUSHED.get(kind) or {}).get("most", max([float(v["most"]) for v in PUSHED.values()] or [1.0])))
    return min(most, (float(m.f["wet"][i]) + total) / open_)


def at_water(w, pid):
    """Whether a parcel is at the water, and how: "water" (a water parcel, or one a river runs through) or "small" (only a brook);
    None off the water."""
    par = w.s["parcels"].get(pid) or {}
    riv = (par.get("land") or {}).get("river")
    if par.get("cover") == "water" or riv == "river":
        return "water"
    return "small" if riv == "brook" else None


def pushed(w, m, node, pid, kind, i, day=None) -> float:
    """A kind's density at a parcel in area i by the cold's push (open_water): 1 for a kind not pushed, or off the water; at a brook
    only while the small waters are open."""
    from cybertron2.wild.kinds import OPEN_WATER, PUSHED
    if kind not in PUSHED:
        return 1.0
    how = at_water(w, pid)
    if how is None:
        return 1.0
    f_ = open_water(w, m, i, node, day, kind)
    if how == "small" and f_ != 1.0 and frozen_run(w, node, day, most=int(OPEN_WATER["hold"]["small"]) + 1) > int(OPEN_WATER["hold"]["small"]):
        return 0.0
    return f_


def _season_of(w, day):
    cal = w.calendar(day)
    return ["spring", "summer", "autumn", "winter"].index(cal["season"]), int(cal["day"]) - 1


def cond(w, node, c, kind=None, m=None, st=None, ri=None, day=None, ctx=None) -> bool:
    """Whether a condition (kinds.WHEN's vocabulary) holds at a village on a day: every key must hold."""
    from cybertron2.engine import environment as EV
    from cybertron2.wild.ecology import RAIN_MEAN
    day = w.d if day is None else day
    st = st if st is not None else (w.s.get("wild") or {}).get("state") or {}
    for key, v in (c or {}).items():
        if key == "seasons":
            if not _season_window(w, day, v):
                return False
        elif key == "frozen_run":
            if frozen_run(w, node, day) < int(v):
                return False
        elif key == "snow":
            if bool(EV.snow_lying(w, node, day)) != bool(v):
                return False
        elif key in ("mast", "mast_last"):
            Y = w.year_days()
            k0 = eco_day(w, day)
            si, year = (k0 % Y) // (Y // 4), k0 // Y
            yr = year if key == "mast" else (year - 1 if si < 2 else year - 1)
            lv = ((st.get("mast") or {}).get("years") or {}).get(str(yr))
            if key == "mast" and si < 2:
                return False
            if lv is None or _level_name(lv) not in v:
                return False
        elif key == "hungry":
            if kind is None or ri is None or 1.0 - float(np.asarray(st["cond"][kind])[ri]) < float(v):
                return False
        elif key == "pressure":
            if kind is None or ri is None or float(((st.get("pressure") or {}).get(kind) or [0.0] * (ri + 1))[ri]) < float(v):
                return False
        elif key == "hard_winter":
            Y, S = w.year_days(), w.year_days() // 4
            k0 = eco_day(w, day)
            start = day - ((k0 % Y) - 3 * S) if (k0 % Y) >= 3 * S else day - (k0 % Y) - S
            if sum(1 for d in range(max(0, start), max(0, start) + S) if d <= day and _frozen_day(w, node, d)) < int(v):
                return False
        elif key == "open_water":
            m_ = m if m is not None else model(w)
            hi = _home_i(w, m_, node)
            f_ = open_water(w, m_, hi, node, day) if hi is not None else 1.0
            if ("frozen over" if f_ <= 0.0 else ("crowded" if f_ > 1.0 + 1e-6 else "open")) != v:
                return False
        elif key == "rain_after_dry":
            if _wx(w, node, day)["rain"] < 1.5 * RAIN_MEAN or any(_wx(w, node, day - k)["rain"] >= 0.5 * RAIN_MEAN for k in range(1, int(v) + 1)):
                return False
        elif key == "tomorrow":
            t = _wx(w, node, day + 1)
            if v.get("frozen") and not (t["low"] < -3.0 and t["temp"] < 3.0):
                return False
            if v.get("rain") and t["rain"] < RAIN_MEAN:
                return False
        elif key == "wet":
            if bool(EV.wet(w, node, day)) != bool(v):
                return False
        elif key == "wounded":
            wd = (st.get("wounded") or {})
            if not any(k_.startswith(f"{kind}@") and day - int(d_) <= 2 for k_, d_ in wd.items()):
                return False
        elif key == "river_run":                                          # the village's water on a river that runs (brief 5 §2)
            from cybertron2.wild import runs as RU
            if not (w.s.get("wild") or {}).get("land") or not st.get("pop"):
                here_run = False
            else:
                here_run = RU.on_river(m if m is not None else model(w), node)
            if here_run != bool(v):
                return False
        elif key == "not":
            if cond(w, node, v, kind, m, st, ri, day, ctx):
                return False
    return True


def effects(w, node, kind, m=None, st=None, ri=None, day=None) -> dict:
    """What a kind's conditional layers do at a village today (kinds.WHEN): drive, bold, danger, flee and detect multiply; targets
    add; lone allows a group of one."""
    from cybertron2.wild.kinds import WHEN
    out = {"drive": 1.0, "bold": 0.0, "danger": 1.0, "flee": 1.0, "detect": 1.0, "targets": [], "lone": False}
    for row in WHEN.get(kind) or []:
        if not cond(w, node, row.get("if"), kind, m, st, ri, day):
            continue
        for k in ("drive", "danger", "flee", "detect"):
            out[k] *= float(row.get(k, 1.0))
        out["bold"] = max(out["bold"], float(row.get("bold", 0.0)))
        out["targets"] += list(row.get("targets") or [])
        out["lone"] = out["lone"] or bool(row.get("lone"))
    if kind is not None:
        wd = ((st if st is not None else (w.s.get("wild") or {}).get("state") or {}).get("wounded") or {})
        d = w.d if day is None else day
        if any(k_.startswith(f"{kind}@") and d - int(v) <= 2 for k_, v in wd.items()):
            out["danger"] *= 2.0                                               # a wounded beast lying up
    return out


def _items_of(spec) -> list:
    return list(DRY_STORES) if spec == "dry" else list(spec or [])


def _targets(w, node, t) -> list:
    """What a target row names at a node: [(target id, the parcel it is on)]. A field with a standing crop; a herd at a parcel (not
    on the road, not led); a building whose store holds one of the row's items; a parcel of the row's covers holding its stock."""
    from cybertron2.engine import farm as FM
    what = t.get("what", "crop") if isinstance(t, dict) else t
    if what == "crop":
        return [(pid, pid) for pid in _fields(w, node)]
    if what == "herd":
        return [(hid, h["parcel"]) for hid, h in sorted(w.s["herds"].items()) if h.get("node") == node and h.get("parcel")
                and not h.get("with") and FM.head(h) > 0]
    if what in ("items", "hens"):
        items = _items_of(t.get("items", ["hen"])) if isinstance(t, dict) else ["hen"]
        return [(bid, b["parcel"]) for bid, b in sorted(w.s["buildings"].items()) if b.get("node") == node and b.get("stock")
                and any(float((w.s["containers"].get(b["stock"], {}).get("goods") or {}).get(i, 0)) >= 1 for i in items)]
    if what == "res":
        return [(pid, pid) for pid, par in sorted(w.s["parcels"].items()) if par["node"] == node and par["cover"] in (t.get("covers") or [])
                and float(((par.get("res") or {}).get(t["res"]) or {}).get("S", 0)) > 1.0]
    if what == "left out":                                                # food left out at a house's door (brief 4 §4.1), and
        return [(cid, w.s["buildings"][c.get("door") or c["in"]]["parcel"])  # a rack inside, reached as the store is (4c §6.2)
                for cid, c in _left_out(w, node) + _racks_in(w, node)]
    if what == "carcass":                                                 # the dead lying open, or shallow for a digger (brief 3 §3)
        return [(cid, c["parcel"]) for cid, c in _dead_at(w, node, t if isinstance(t, dict) else {})]
    return []


def _count(m, st, kind, land, node, ring_i, gather):
    import numpy as np
    idx = [ring_i] if gather != "far" else _reach(m, land, node, "far")     # the village's own land too: what the dead draw in (4b §2.5)
    return sum(float(np.asarray(st["pop"][kind])[i]) * float(m.km2[i]) for i in idx)


def _answer(rng, g, np_, scare, bold=0.0):
    """D2-198: whether a harmless scare (or the dog) turns the group tonight, and what it learns; a bold group (hungry, in snow, in
    the rut) turns that much less."""
    ans = np_["answer"]
    harm = (np_.get("harm") or {}).get(scare)
    keep = 1.0 - float(bold)
    if harm:
        turned = rng.random() < float(harm["turn_p"]) * keep
        harmed = turned and rng.random() < float(harm["harm_p"])
        return turned, harmed
    if ans["type"] == "habituate":
        turned = rng.random() < float(ans["turn_p"]) * (1 - float(g["habit"].get(scare, 0.0))) * keep
        if turned:
            g["habit"][scare] = min(1.0, float(g["habit"].get(scare, 0.0)) + float(ans["gain"]))
        return turned, False
    if ans["type"] == "scared_off":
        return rng.random() < float(ans["turn_p"]) * keep, False
    return False, False


SIZE_ORDER = ("tiny", "small", "medium", "large")


def gaps_pass(b, kind) -> bool:
    """Whether a kind gets through a building's own gaps (brief 2 §4): its structure's gaps (wattle and timber small, stone tiny; a
    damaged building one size larger) against the smallest gap the kind passes."""
    from cybertron2.engine.data import RESOURCES
    from cybertron2.wild.kinds import GAPS
    kg = ((RESOURCES.get(kind) or {}).get("body") or {}).get("gap")
    if kg not in SIZE_ORDER:
        return False
    bg = GAPS["structure"].get(b.get("structure"), "small")
    if b.get("level") is not None:                                         # in levels (brief 4 §3): as built through worn; a size
        lv = int(b["level"])                                               # larger gappy; large (the fox, a dog) holed; anything
        if lv <= 1:                                                        # failing
            return True
        if lv == 2:
            bg = "large"
        elif lv == 3:                                                       # gappy: a size larger, never fox-sized (only holed is)
            bg = SIZE_ORDER[min(SIZE_ORDER.index("small"), SIZE_ORDER.index(bg) + 1)]
    elif int(b.get("condition", 2)) < 2:
        bg = SIZE_ORDER[min(len(SIZE_ORDER) - 1, SIZE_ORDER.index(bg) + int(GAPS["damaged"]))]
    return SIZE_ORDER.index(kg) <= SIZE_ORDER.index(bg)


def _fenced(w, pid, np_, rng, kind=None) -> bool:
    """A fence round the parcel keeps the group out by its level (FENCES' through, as for herds), a leaping kind more often over; a
    kind small enough for its gaps passes any fence (brief 2 §4)."""
    from cybertron2.engine.data import FENCES, RESOURCES
    if ((RESOURCES.get(kind) or {}).get("body") or {}).get("gap") in ("tiny", "small"):
        return False
    fc = (w.s["parcels"].get(pid) or {}).get("fence") or {}
    if not fc.get("built") or fc.get("kind") not in FENCES or int(fc.get("level", 0)) <= 0:
        return False
    through = float(FENCES[fc["kind"]]["through"].get(int(fc["level"]), 1.0)) * float(np_.get("fence", 1.0))
    return rng.random() >= min(1.0, through)


def _raid(w, g, np_, kind, t, tgt, parcel, scare, rng) -> dict:
    """What a group does at its target when nothing turns it, by the target row: eats and tramples a field, kills a beast of a herd,
    takes from a store (hens, grain, hay: a door shut keeps most out), strips a parcel's stock (bark and young growth)."""
    from cybertron2.engine import farm as FM, things as TH
    from cybertron2.engine.data import TECHNIQUES
    node = g["node"]
    what = t.get("what", "crop")
    met = float(np_["met_share"]) if scare is not None else 1.0
    if what == "crop":
        share = min(0.5, float(t.get("trample", 0.0)) * g["n"] * met)
        fb = (getattr(w, "_flock_budget", None) or {}).get(node) if np_.get("flock") else None
        if fb is not None:                                                # a flock eats its night's part here (brief 4 §4.3)
            here_left = sum(float(c.get("left", 0.0)) for _, _, c in FM.standing(w.s["parcels"][tgt]))
            share = min(share, fb["qty"] / here_left) if here_left > 1e-9 else 0.0
        lost = 0.0
        for hd, _, c in FM.standing(w.s["parcels"][tgt]):
            q = round(float(c.get("left", 0.0)) * share, 4)
            if c.get("area_left", 0) > 1e-6 and q > 1e-9:
                w.apply("draw", node, parcel=tgt, key="crop", qty=q, **({"holder": hd} if hd is not None else {}))
                lost += q
        if fb is not None:
            fb["qty"] = max(0.0, fb["qty"] - lost)
        return {"lost": round(lost, 4)}
    if what == "herd":
        h = w.s["herds"][tgt]
        role = next((r for r in ("young", "cows", "oxen", "bulls") if int(h.get(r, 0)) > 0), None)
        if role is None:
            return {"killed": None}
        w.apply("set", node, ref=("herd", tgt), field=role, value=int(h[role]) - 1)
        w.apply("set", node, ref=("herd", tgt), field="count", value=FM.head(w.s["herds"][tgt]))
        TH.leave_carcass(w, node, FM.ROLE_WORD[role][0], h["name"], [c["claimant"] for c in w.claims_on(("herd", tgt))], "killed",
                         TECHNIQUES["slaughter"]["yield"]["gives"][role], parcel=parcel, by=kind)
        w.event(node, "herd", f"a {FM.ROLE_WORD[role][0]} of {h['name']} was killed in the night", about=[f"herd:{tgt}"], salience=0.6,
                tags=["animals", "danger"])
        return {"killed": role}
    if what == "left out":                                                # food at a door: taken as it lies (brief 4 §4.1)
        from cybertron2.wild.kinds import LEFT_OUT
        c = w.s["containers"].get(tgt) or {}
        took = 0.0
        if c.get("in") in w.s["buildings"] and not _gets_in(w, c["in"], kind, rng):   # inside: only as into the store (4c §6.2)
            return {"took": 0}
        for item in LEFT_OUT["items"]:
            q = float((c.get("goods") or {}).get(item, 0.0))
            if q > 1e-9:
                k = round(q * min(1.0, float(t.get("share", 0.5)) * met), 4)
                w.apply("destroy", node, src=tgt, item=item, qty=k, why=f"taken by {_a(kind)}")
                took += k
        return {"took": round(took, 4)}
    if what == "carcass":                                                 # the dead: eat a share by the group's size (brief 3 §3)
        c = w.s["containers"].get(tgt)
        if not c:
            return {"ate": 0.0}
        out = {}
        if c.get("depth") == "shallow" and c.get("dug") is None:          # a shallow grave dug open: what is left of it lies open
            w.apply("set_thing", node, cid=tgt, field="dug", value=w.d)
            w.apply("set_thing", node, cid=tgt, field="buried", value=None)
            w.apply("set_thing", node, cid=tgt, field="depth", value="dug")
            w.event(node, "death", f"something dug into the grave at {TH.parcel_name(w, c)} in the night", about=[f"parcel:{parcel}"],
                    salience=0.5, tags=["animals", "death"])
            out["dug"] = True
        ate = TH.eat_flesh(w, tgt, float(t.get("eat", 1.0)) * g["n"] * met, f"eaten by {_a(kind)}")
        if t.get("cache") and ate > 0:                                    # a bear covers its find and lies up near (brief 3 §3)
            lo, hi = t["cache"]
            w.apply("set_thing", node, cid=tgt, field="cached",
                    value={"kind": kind, "until": w.d + int(lo + rng.random() * (int(hi) - int(lo) + 1))})
        g["fed_at"] = {"node": node, "day": w.d}
        herd_rows = [r for r in (np_.get("targets") or []) if r.get("what") == "herd"]
        if herd_rows and ate > 0:                                         # the herd seen from the dead: remembered (brief 4 §4.5)
            from cybertron2.engine import layout as LY
            herds = _targets(w, node, {"what": "herd"})
            if herds:
                cp = (w.s["containers"].get(tgt) or {}).get("parcel")
                hid, hp = min(herds, key=lambda x: (LY.steps(w, cp, x[1]) if cp and LY.steps(w, cp, x[1]) is not None else 99, x[0]))
                g["seen_herd"] = {"hid": hid, "parcel": hp, "day": w.d}
        return {"ate": round(ate, 4), **out}
    if what in ("items", "hens"):
        b = w.s["buildings"][tgt]
        if t.get("door", False) and not _gets_in(w, tgt, kind, rng):
            return {"took": 0}
        goods = w.s["containers"][b["stock"]].get("goods") or {}
        took = 0.0
        for item in _items_of(t.get("items")):
            have = float(goods.get(item, 0))
            if have <= 0:
                continue
            if t.get("heads"):                                                # beasts of a kind: a few, or once in, all
                k = min(have, have if rng.random() < float(t.get("all_p", 0.0)) else float(t["heads"]))
                k = float(int(k))
            else:
                k = round(have * min(0.5, float(t.get("share", 0.01)) * g["n"] * met), 4)
            if k >= (1 if t.get("heads") else 1e-4):
                w.apply("destroy", node, src=b["stock"], item=item, qty=k, why=f"taken by {_a(kind)}")
                took += k
        return {"took": round(took, 4), **({"hens": took} if "hen" in _items_of(t.get("items")) else {})}
    if what == "res":
        r = w.s["parcels"][tgt]["res"][t["res"]]
        q = round(float(r["S"]) * min(0.3, float(t.get("share", 0.003)) * g["n"] * met), 4)
        if q > 1e-6:
            w.apply("draw", node, parcel=tgt, key=t["res"], qty=q)
        return {"stripped": q}
    return {}


def _gets_in(w, bid, kind, rng) -> bool:
    """Whether a kind that comes for what is inside a house gets in tonight: through its gaps (a holed house for a fox, brief 4 §3),
    else by the door, seldom when shut up for the night, often when left (D2-207)."""
    shut = int(((w.s["wild"].get("shut") or {}).get(bid) or {}).get("day", -9)) == w.d
    passes = gaps_pass(w.s["buildings"][bid], kind)                         # the building's own gaps against the kind's (§4)
    return rng.random() < (0.9 if passes else (0.02 if shut else 0.6))


def layout_steps(w, a, b):
    from cybertron2.engine import layout as LY
    return 0 if a == b else LY.steps(w, a, b)


def rng_l(w, gid) -> float:
    return w.rng("wild-leader", gid, w.d).random()


def cache_meet(here, pid):
    """Taking at or working the parcel of a carcass a beast has cached and lies up near (brief 3 §3): it is met by the hunters'
    danger rule (D2-193) with that kind's danger, the more for one alone. Returns the line for the one who met it, else None."""
    from cybertron2.engine.data import RESOURCES
    from cybertron2.engine import things as TH
    w = here._w
    if not pid:
        return None
    for cid, c in sorted(TH.at_node(w, here.node).items()):
        cc = c.get("cached") or {}
        if c.get("parcel") != pid or int(cc.get("until", -1)) < here.day:
            continue
        kind = cc["kind"]
        dg = ((RESOURCES.get(kind) or {}).get("taken") or {}).get("danger") or {}
        others = sum(1 for e in here.events() if e.get("day") == here.day and e.get("actor") not in (here.name, None)
                     and f"parcel:{pid}" in (e.get("about") or []))
        alone = 1.5 if others == 0 else 1.0 / (1 + others)
        rng = w.rng("wild-cache", here.day, here.name, cid)
        place = TH.parcel_name(w, c)
        if rng.random() < min(0.95, float(dg.get("wound", 0.3)) * alone):
            if rng.random() < min(0.5, float(dg.get("kill", 0.0)) * alone):
                here.apply("die", person=here.name, cause=f"killed by {_a(kind)} at its kill")
                return f"At {place}, {_a(kind)} rose from where it lay by its kill and was on you."
            here.apply("harm", person=here.name, wounded=True)
            return f"At {place}, {_a(kind)} rose from where it lay by its kill; it struck you before it went back to cover. You were hurt."
        return f"At {place}, {_a(kind)} rose from where it lay by its kill and stood over it; you backed away and did nothing there."
    return None


def _dead_to_pool(w, m, st) -> dict:
    """Lend the dead lying open at each village to its home area's carrion for the night (brief 3 §3): their flesh as kg a km2
    (THINGS carcass_kg a unit). Returns {area index: (kg a km2 lent, the pool before, [(thing id, flesh)])}."""
    from cybertron2.engine import things as TH
    from cybertron2.engine.data import THINGS
    land = w.s["wild"]["land"]
    ix = {a: i for i, a in enumerate(m.ids)}
    lent = {}
    for node, aid in sorted((land.get("home") or {}).items()):
        if aid not in ix or node not in w.s["nodes"]:
            continue
        i = ix[aid]
        dead = [(cid, TH.flesh(w, c)) for cid, c in sorted(TH.open_dead(w, node).items()) if c.get("depth") != "shallow"]
        kg = sum(f for _, f in dead) * float(THINGS["carcass_kg"]) / max(1e-9, float(m.km2[i]))
        if kg > 1e-9:
            before = float(st["carrion"][i])
            st["carrion"][i] = before + kg
            lent[i] = (kg, before, dead)
    return lent


def _dead_from_pool(w, m, st, eff, lent) -> None:
    """What the carrion eaters ate of an area's pool comes off the dead lent to it in proportion; birds were over those that lost
    enough to show (`birds`, for the ravens' sign); what is left of the loan is taken back out of the pool."""
    from cybertron2.engine import things as TH
    eaten = eff["eaten"].get("carrion")
    for i, (kg, before, dead) in sorted(lent.items()):
        pool = (kg + before) * float(m.km2[i])
        share = min(1.0, float(eaten[i]) / pool) if eaten is not None and pool > 1e-9 else 0.0
        for cid, f in dead:
            q = TH.eat_flesh(w, cid, f * share, "eaten by carrion birds and beasts")
            if q >= 0.05:                                                     # birds at it: their sign (a quarter kg and more)
                w.apply("set_thing", TH.where(w, w.s["containers"][cid]), cid=cid, field="birds", value=w.d)
        from cybertron2.wild import ecology as EC
        st["carrion"][i] = round(max(0.0, float(st["carrion"][i]) - kg * (1.0 - share) * EC.carrion_keep()), 2)   # the step's own decay


def _did(res) -> bool:
    return res.get("lost", 0) > 1e-6 or bool(res.get("killed")) or res.get("took", 0) > 0 or res.get("stripped", 0) > 1e-6 \
        or res.get("ate", 0) > 1e-6


def _dead_stage(w, c) -> str:
    """fresh, rotting or bones (brief 3 §2); a body fresh its first day, then rotting."""
    from cybertron2.engine import things as TH
    if c.get("body"):
        return "fresh" if w.d - int(c.get("died", w.d)) <= 1 else "rotting"
    return "bones" if TH.carcass_bones(w, c) else ("fresh" if TH.carcass_fresh(w, c) else "rotting")


def _dead_at(w, node, t) -> list:
    """The dead a carcass row can come to at a node (brief 3 §3): open or, for a kind that digs, shallow; in the row's stages."""
    from cybertron2.engine import things as TH
    out = []
    for cid, c in sorted(TH.open_dead(w, node).items()):
        if c.get("depth") == "shallow" and c.get("dug") is None and not t.get("digs"):
            continue
        if t.get("stages") and _dead_stage(w, c) not in t["stages"]:
            continue
        out.append((cid, c))
    return out


def _carcass_pull(w, node, t) -> float:
    """How strongly the dead at a node draw a carcass row (brief 3 §3): the most flesh there against kinds.CARCASS_PULL's ref, a
    shallow grave its `dig` share of that."""
    from cybertron2.engine import things as TH
    from cybertron2.wild.kinds import CARCASS_PULL
    best = 0.0
    for cid, c in _dead_at(w, node, t):
        x = min(1.0, TH.flesh(w, c) / float(CARCASS_PULL["ref"]))
        if c.get("depth") == "shallow" and c.get("dug") is None:
            x *= float(CARCASS_PULL["dig"])
        best = max(best, x)
    return best


RANGE_PICK = {"memory": 3.0}    # a ranging group's pull to the village it remembers (raided unopposed, a herd seen; calibrate, 4c);
                                # a village farther off draws it by exp(-distance / the range's radius, sqrt(range_km2 / pi))


def _raidable(w, node) -> bool:
    """Whether a node has anything a group could come for (brief 4c §7.2): a herd out, a field with a standing crop, a store with
    goods in it, the dead lying open. Only such a node is a village to a ranging group, and to the generator's check."""
    from cybertron2.engine import farm as FM, things as TH
    if any(h.get("node") == node and h.get("parcel") and not h.get("with") and FM.head(h) > 0 for h in w.s["herds"].values()):
        return True
    if _fields(w, node):
        return True
    if any(b.get("node") == node and b.get("stock") and any(float(q) > 0 for q in ((w.s["containers"].get(b["stock"]) or {}).get("goods")
                                                                                 or {}).values()) for b in w.s["buildings"].values()):
        return True
    return bool(TH.open_dead(w, node))


def _range_km2(m, kind) -> float:
    """The land a kind's group ranges over (brief 4c §7.2: `range_km2` on the kind's group); 0 for a group tied to one node."""
    return float(((m.kinds.get(kind) or {}).get("group") or {}).get("range_km2") or 0.0)


def _range_geom(m, km2):
    """A range of km2 about each area's centre, from the areas' positions (brief 4c §7.2): W[c, i] the share of area i inside the
    range centred on area c (each area taken as a disc of its own size about its centre, the range as a disc of km2), D[c, i] the
    distance between their centres (km), and the range's radius. None for a land without positions."""
    import numpy as np
    cache = m.__dict__.setdefault("_ranges", {})
    if km2 in cache:
        return cache[km2]
    areas = [m.land["areas"][a] for a in m.ids]
    if not areas or any("xy_km" not in a for a in areas):
        cache[km2] = None
        return None
    xy = np.array([a["xy_km"] for a in areas], dtype=float)
    D = np.hypot(xy[:, None, 0] - xy[None, :, 0], xy[:, None, 1] - xy[None, :, 1])
    R = math.sqrt(float(km2) / math.pi)
    r = np.sqrt(np.maximum(np.asarray(m.km2, float), 1e-12) / math.pi)[None, :] * np.ones_like(D)
    inner = np.pi * np.minimum(R, r) ** 2                                  # one disc inside the other
    d = np.maximum(D, 1e-9)
    with np.errstate(invalid="ignore"):
        a1 = r ** 2 * np.arccos(np.clip((d ** 2 + r ** 2 - R ** 2) / (2 * d * r), -1, 1))
        a2 = R ** 2 * np.arccos(np.clip((d ** 2 + R ** 2 - r ** 2) / (2 * d * R), -1, 1))
        a3 = 0.5 * np.sqrt(np.clip((-d + r + R) * (d + r - R) * (d - r + R) * (d + r + R), 0, None))
    lens = a1 + a2 - a3
    ov = np.where(D >= R + r, 0.0, np.where(D <= np.abs(R - r), inner, lens))
    W = np.clip(ov / (np.pi * r ** 2), 0.0, 1.0)
    cache[km2] = (W, D, R)
    return cache[km2]


def _adults(m, st, kind):
    """A kind's heads by area, the year's young left out until the next births (brief 4c §7.1: `yearling`, kept by the ecology for
    a ranging kind: born on the births' day, an area's losses taken off them first)."""
    import numpy as np
    pop = np.asarray(st["pop"][kind], float)
    y = (st.get("yearling") or {}).get(kind)
    if y is not None and len(y) == m.n:
        pop = np.maximum(pop - np.asarray(y, float), 0.0)
    return pop * np.asarray(m.km2, float)


def range_count(m, st, kind, node, land) -> float:
    """The adults of a ranging kind within its range of a node's site (the generator's check and the traces, brief 4c §7.3)."""
    geo = _range_geom(m, _range_km2(m, kind))
    aid = (land.get("home") or {}).get(node)
    if geo is None or aid not in m.ids:
        return 0.0
    return float((_adults(m, st, kind) * geo[0][m.ids.index(aid)]).sum())


def within_range(w) -> dict:
    """For each village (a node with something to come for, `_raidable`), the whole-counted kinds that come near people for their
    beasts, stores or dead (not the fields alone) and could reach it: the grown heads within a ranging kind's range of its site (brief 4c §7.2), or
    within a node-bound kind's reach, against the least group (the generator's check, §7.3).
    {village name: {kind: {"heads", "least", "range_km2" or "reach"}}}."""
    if not on(w) or not (w.s.get("wild") or {}).get("state"):
        return {}
    m, st, land = model(w), w.s["wild"]["state"], w.s["wild"]["land"]
    ix = {a: i for i, a in enumerate(m.ids)}
    rings = {a["node"]: ix[aid] for aid, a in land["areas"].items() if a["kind"] == "ring"}
    homes = sorted(nd for nd in rings if _raidable(w, nd))                # a village: a node with something to come for
    out = {}
    for node in homes:
        row = {}
        for kind in m.names:
            np_, spec = _near(kind), m.kinds[kind]
            if not np_ or spec.get("count") != "whole" or np_.get("flock") \
                    or all(t.get("what", "crop") in ("crop", "res") for t in np_.get("targets") or []):   # beasts, not the fields alone
                continue
            least = int(((spec.get("group") or {}).get("size") or [2, 10])[0])
            km2 = _range_km2(m, kind)
            if km2 > 0 and _range_geom(m, km2) is not None:
                row[kind] = {"heads": round(range_count(m, st, kind, node, land), 2), "least": least, "range_km2": km2}
            else:
                row[kind] = {"heads": round(_count(m, st, kind, land, node, rings[node], np_.get("gather")), 2), "least": least,
                             "reach": np_.get("gather") or "ring"}
        out[w.s["nodes"][node].get("name", node)] = row
    return out


def group_at(w, kind, node):
    """The group of a kind that works a village: its own (kind@node), else a ranging group there tonight, else one whose range
    takes the village in (brief 4c §7.2). (gid, group) or (kind@node, None)."""
    gs = (w.s.get("wild") or {}).get("groups") or {}
    gid = f"{kind}@{node}"
    if gid in gs and not gs[gid].get("range"):
        return gid, gs[gid]
    mine = [(k, g) for k, g in sorted(gs.items()) if g.get("kind") == kind and g.get("range")]
    for k, g in mine:
        if g.get("node") == node:
            return k, g
    for k, g in mine:
        if node in (g.get("villages") or []):
            return k, g
    return gid, gs.get(gid)


def _leader(w, g, gid, kind, count, new) -> float:
    """A group's leader, named on demand (D2-195), and what it does to the drive."""
    from cybertron2.wild.kinds import LEADERS
    ld = LEADERS.get(kind)
    if new and ld and count >= float(ld["least"]) and rng_l(w, gid) < float(ld["p"]):
        g["leader"] = {"name": ld["name"], "alive": True}
    if ld and (g.get("leader") or {}).get("alive"):
        return float(ld["drive"])
    if ld and (g.get("leader") or {}).get("died") is not None and w.d - int(g["leader"]["died"]) <= int(ld["dead"]["days"]):
        return float(ld["dead"]["drive"])
    return 1.0


def _rows_at(w, node, np_, ef) -> list:
    """A kind's target rows in season at a village tonight, the dead weighted by their pull there."""
    rows = [t for t in list(np_["targets"]) + ef["targets"] if _season_window(w, w.d, t["seasons"])]
    return [dict(t, attr=float(t["attr"]) * _carcass_pull(w, node, t)) if t.get("what") == "carcass" else t for t in rows]


def _groups(w, m, st) -> dict:
    """Whole-counted kinds with a group near a village: condense from the land around (the ring, or for a pack the land beyond),
    set out on a drive from the area's hunger and the kind's conditions (frost, snow, the mast, the rut: kinds.WHEN), leave traces on
    the way, raid their target (a field, a herd, a store, a parcel's stock) unless a fence keeps them out, a watch at the gap they use
    meets them, or a watch or a dog turns them by the kind's answer to scares (D2-198), and remember. A kind that ranges (its group's
    `range_km2`, brief 4c §7.2) condenses its adults over the range of its densest area that takes in a village, one group wherever it
    raids, and sets out for one of the villages in its range by what draws it there, how far it is and what it remembers."""
    import copy
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

    def night_of(gid, g, node, ri, kind, np_, ef, rows, attr, hunger, lmul, rng, knows_here=True):
        """One group's night at a village: the raid it is ready for, its lead at the wood's edge, or whether it sets out (D2-197,
        D2-198); `knows_here`: whether the village is where it last raided (a ranging group's memory, brief 4c §7.2)."""
        if g["pos"] == "ready" and w.d >= g["raid"]:
            g["pos"] = "home"
            t = dict(g.get("trow") or {"what": g.get("what") or "crop"})
            t.setdefault("what", "crop")
            tg = dict(_targets(w, node, t))
            tgt = g["target"] if g["target"] in tg else (next(iter(tg)) if tg else None)
            if tgt is None:
                return

            def attempt(tgt, first=True):
                """One target tonight: met at its gap, kept out by a fence, turned by a scare, or raided (D2-198)."""
                parcel = tg[tgt]
                gap = _edge_of(w, parcel)
                seen = watch.get(parcel)
                scare = seen.get("scare") if seen else None
                if scare is None and t.get("what") == "herd" and w.s["herds"][tgt].get("watched") == w.d:
                    scare = "herding"                                      # people with the herd: a watch of a kind
                if scare is None and t.get("what") in ("items", "hens") and (w.s["buildings"][tgt].get("fittings") or {}).get("dog"):
                    scare = "dog"
                if gap != parcel and watch.get(gap):                       # met at the gap they come through (L3)
                    gw = watch[gap]
                    g["rest"] = w.d + int(np_["answer"].get("rest", np_["answer"].get("off_days", 2)))
                    if rng.random() < 0.3:
                        g["wary"], g["habit"] = w.d + int(np_["wary_after_harm"]), {}
                    _trace(traces, gap, kind, "turned", w.d, g["n"], gw.get("scare"), gw.get("by"))
                    return {"at": tgt, "what": t.get("what"), "turned": True, "scare": gw.get("scare"), "gap": True}, gap
                if t.get("what") in ("crop", "herd", "res") and _fenced(w, parcel, np_, rng, kind):
                    _trace(traces, parcel, kind, "turned", w.d, g["n"], "fence", None)
                    return {"at": tgt, "what": t.get("what"), "turned": True, "scare": "fence"}, gap
                if scare is not None:
                    turned, harmed = _answer(rng, g, np_, scare, ef["bold"])
                    if harmed:
                        g["wary"], g["habit"] = w.d + int(np_["wary_after_harm"]), {}
                    if turned:
                        g["rest"] = w.d + int(np_["answer"].get("rest", np_["answer"].get("off_days", 2)))
                        _trace(traces, parcel, kind, "turned", w.d, g["n"], scare, (seen or {}).get("by"))
                        return {"at": tgt, "what": t.get("what"), "turned": True, "scare": scare}, gap
                res = _raid(w, g, np_, kind, t, tgt, parcel, scare, rng)
                tr = ("raid" if _did(res) else "tried") + (f":{t['sign']}" if t.get("sign") and _did(res) else "")
                _trace(traces, parcel, kind, tr, w.d, g["n"], scare, (seen or {}).get("by"))
                return {"at": tgt, "what": t.get("what"), "turned": False, "scare": scare, **res}, gap

            probe = int(t.get("probe") or 0) if t.get("what") in ("items", "hens") else 0
            if probe:                                                       # the lapse probe (D2-207, brief 2 §2): the doors of
                order = sorted(tg, key=lambda b: (b != g.get("target"), w.rng("wild-probe", w.d, gid, b).random()))   # the hamlet,
                res, tried = None, []                                       # the one it fed at first, then the rest, keyed
                for b in order[:probe]:
                    r, _ = attempt(b)
                    tried.append(b)
                    res = res or r
                    if not r.get("turned") and _did(r):
                        res = r
                        g["target"], g["parcel"] = b, tg[b]
                        g["found"] = w.d
                        break
                out[gid] = dict(res or {}, tried=tried)
                return
            res, gap = attempt(tgt)
            if not res.get("turned"):
                g["found"] = w.d
            elif np_.get("displace"):                                       # turned: one more target the same night, the
                near = [(b, layout_steps(w, gap, p)) for b, p in tg.items()  # nearest unwatched one from the edge it came out of
                        if b != tgt and p != tg[tgt] and not watch.get(p)]  # (D2-207, brief 2 §2)
                near = [(b, d) for b, d in near if d is not None]
                if near:
                    b2 = min(near, key=lambda x: (x[1], x[0]))[0]
                    res2, _ = attempt(b2, first=False)
                    res = dict(res, displaced_to=b2, then=res2)
                    if not res2.get("turned"):
                        g["target"], g["parcel"], g["found"], g["rest"] = b2, tg[b2], w.d, -1
            out[gid] = res
        elif g["pos"] == "edge":
            if rng.random() < float(np_["lead_sign_p"]):
                _trace(traces, _edge_of(w, g.get("parcel") or g.get("target")), kind, "edge", w.d, g["n"])
            if w.d - g["t"] >= int(np_["lead_nights"]) - 1:
                g["pos"], g["raid"] = "ready", w.d + 1
        elif g["pos"] == "home" and w.d >= g["rest"] and w.d >= g["wary"] and attr > 0:
            from cybertron2.wild.kinds import CARCASS_PULL
            fed = g.get("fed_at") or {}                                    # fed at the dead here lately: bolder, and any of its
            spill = fed.get("node") == node and 0 <= w.d - int(fed.get("day", -99)) <= int(CARCASS_PULL["spill_nights"])   # rows
            trow = max(rows, key=lambda t: t["attr"])
            sh = g.get("seen_herd") or {}
            herd_row = next((t for t in rows if t.get("what") == "herd"), None)
            if spill and herd_row and sh and w.d - int(sh["day"]) <= int(np_["memory_days"]) \
                    and sh["hid"] in dict(_targets(w, node, herd_row)):
                trow = herd_row                                            # back for the herd seen from the dead (brief 4 §4.5)
                g["target"], g["found"] = sh["hid"], int(sh["day"])
            elif spill:                                                    # (brief 3 §3: the fox at the dead calf tries the hens)
                live = [t for t in rows if t["attr"] > 0 and _targets(w, node, t)]
                if live:
                    u, acc = rng.random() * sum(t["attr"] for t in live), 0.0
                    for t in live:
                        acc += t["attr"]
                        if u < acc:
                            trow = t
                            break
            tg = _targets(w, node, trow)
            if not tg:
                return
            from cybertron2.wild.kinds import WARY
            lw = learned(float(((st.get("wary") or {}).get(kind) or [0.0] * m.n)[ri]))   # hunted game is less bold (4b §2.1)
            p = min(1.0, attr * (float(np_["drive"]["base"]) + float(np_["drive"]["hunger"]) * hunger) * ef["drive"] * lmul
                    * (float(CARCASS_PULL["spill_drive"]) if spill else 1.0) / (1.0 + float(WARY["raid"]) * lw))
            knows = knows_here and 1 <= w.d - int(g["found"]) <= int(np_["memory_days"])
            if knows:
                p = max(p, float(np_["return_p"]) * attr)
            if rng.random() < p:
                if trow.get("pick") == "most":                             # a flock lands where the most of its crop stands (§3)
                    from cybertron2.engine import farm as FM
                    tg = sorted(tg, key=lambda x: -sum(float(c.get("left", 0.0)) for _, _, c in FM.standing(w.s["parcels"][x[1]])))
                pick = tg[0] if (g.get("target") in dict(tg) or rng.random() < 0.75) else tg[int(rng.random() * len(tg))]
                if g.get("target") in dict(tg) and knows:
                    pick = (g["target"], dict(tg)[g["target"]])
                g["target"], g["parcel"], g["what"], g["trow"] = pick[0], pick[1], trow.get("what", "crop"), {"what": "crop", **trow}
                if knows:
                    g["pos"], g["raid"] = "ready", w.d + 1                  # straight back; the damage was the sign
                else:
                    g["pos"], g["t"] = "edge", w.d
                    if rng.random() < float(np_["lead_sign_p"]):
                        _trace(traces, _edge_of(w, pick[1]), kind, "edge", w.d, g["n"])
    ranging = {}                                                          # kinds whose groups range over several areas (4c §7.2)
    for kind in m.names:
        np_, spec = _near(kind), m.kinds[kind]
        if np_ and spec.get("count") == "whole" and not np_.get("flock") and _range_km2(m, kind) > 0:
            geo = _range_geom(m, _range_km2(m, kind))
            if geo is not None:                                           # a hand-made land without positions: as before
                ranging[kind] = geo
    for node, ri in sorted(rings.items()):
        for kind in m.names:
            np_ = _near(kind)
            spec = m.kinds[kind]
            if not np_ or (spec.get("count") != "whole" and not np_.get("flock")):   # a flock of a counted-by-density kind (D2-207)
                continue
            if kind in ranging:
                continue
            gid = f"{kind}@{node}"
            ef = effects(w, node, kind, m, st, ri)
            count = _count(m, st, kind, land, node, ri, np_.get("gather"))
            lo, hi = np_.get("flock") or (spec.get("group") or {}).get("size", [2, 10])
            lo = 1 if ef["lone"] else lo
            if count < lo:
                groups.pop(gid, None)
                continue
            new = gid not in groups
            g = groups.get(gid) or {"kind": kind, "node": node, "pos": "home", "t": -1, "raid": -1, "found": -99, "habit": {},
                                    "wary": -1, "rest": -1, "target": None, "what": None}
            lmul = _leader(w, g, gid, kind, count, new)
            g["n"] = int(np.clip(round((0.3 if np_.get("gather") != "far" else 0.6) * count), lo, hi))
            groups[gid] = g
            rng = w.rng("wild-group", w.d, gid)
            if np_["answer"]["type"] == "habituate":
                dec = float(np_["answer"]["decay"])
                g["habit"] = {k: max(0.0, v - dec) for k, v in g["habit"].items() if v > dec}
            rows = _rows_at(w, node, np_, ef)
            attr = max([t["attr"] for t in rows] or [0.0])
            hunger = 1.0 - float(np.asarray(st["cond"][kind])[ri])
            night_of(gid, g, node, ri, kind, np_, ef, rows, attr, hunger, lmul, rng)
    homes = {nd: ix[aid] for nd, aid in sorted((land.get("home") or {}).items()) if nd in rings and aid in ix
             and ranging and _raidable(w, nd)}                            # a village: a node with something to come for (4c §7.2)
    for kind in [k for k in m.names if k in ranging]:                     # groups that range (brief 4c §7.2)
        W, D, R = ranging[kind]
        np_, spec = _near(kind), m.kinds[kind]
        lo0, hi = (spec.get("group") or {}).get("size", [2, 10])
        adults = _adults(m, st, kind)
        efs = {}

        def ef_at(nd, kind=kind):
            if nd not in efs:
                efs[nd] = effects(w, nd, kind, m, st, rings[nd])
            return efs[nd]

        hn = list(homes)
        hd = D[:, [homes[nd] for nd in hn]] if hn else np.zeros((m.n, 0))
        near_v = [sorted((nd for j, nd in enumerate(hn) if hd[c, j] <= R), key=lambda nd, c=c: (D[c, homes[nd]], nd)) for c in range(m.n)]
        lo_c = np.array([1 if near_v[c] and ef_at(near_v[c][0])["lone"] else lo0 for c in range(m.n)], dtype=float)
        avail = np.ones(m.n)
        packs = []
        for gid in sorted(k for k, g in groups.items() if g.get("kind") == kind):
            g = groups[gid]
            if g.get("range") in ix:
                c = ix[g["range"]]
            elif g.get("node") in rings:                                  # a group from before ranging: its ring is the centre
                c = rings[g["node"]]
                g.setdefault("found_at", g["node"])
            else:
                groups.pop(gid, None)
                continue
            share = np.minimum(avail, W[c])
            count = float((adults * share).sum())
            if count < lo_c[c]:                                           # (with nothing to come for in range, it waits)
                groups.pop(gid, None)
                continue
            avail = avail - share
            packs.append((gid, c, count, share, False))
        km2 = np.asarray(m.km2, float)
        while len(packs) < len(rings):                                    # new groups: over the range of the densest area left, with a
            dens = adults * avail / np.maximum(km2, 1e-12)                # village in it, that holds a group
            c = next((int(c) for c in np.argsort(-dens, kind="stable") if dens[c] > 0 and near_v[c]
                      and float((adults * np.minimum(avail, W[c])).sum()) >= lo_c[c]), None)
            if c is None:
                break
            nd = m.nodes[c] if m.nodes[c] in rings else near_v[c][0]
            gid = f"{kind}@{nd}" if f"{kind}@{nd}" not in groups else f"{kind}@{nd}~{m.ids[c]}"
            if gid in groups:
                break
            share = np.minimum(avail, W[c])
            avail = avail - share
            groups[gid] = {"kind": kind, "node": near_v[c][0], "pos": "home", "t": -1, "raid": -1, "found": -99, "habit": {},
                           "wary": -1, "rest": -1, "target": None, "what": None}
            packs.append((gid, c, float((adults * share).sum()), share, True))
        for gid, c, count, share, new in sorted(packs):
            g = groups[gid]
            lo = int(lo_c[c])
            g["range"], g["villages"] = m.ids[c], near_v[c]
            lmul = _leader(w, g, gid, kind, count, new)
            g["n"] = int(np.clip(round(count), lo, hi))
            rng = w.rng("wild-group", w.d, gid)
            if np_["answer"]["type"] == "habituate":
                dec = float(np_["answer"]["decay"])
                g["habit"] = {k: max(0.0, v - dec) for k, v in g["habit"].items() if v > dec}
            cw = adults * share                                           # the range's hunger: its adults' condition
            hunger = float((cw * (1.0 - np.asarray(st["cond"][kind], float))).sum() / max(cw.sum(), 1e-12))
            found = g["found"]
            if g["pos"] == "home":
                if w.d < g["rest"] or w.d < g["wary"]:
                    continue
                cands = []                                                # where it sets out for: by what draws it there, how far, and
                for v in near_v[c]:                                       # what it remembers
                    rows = [t for t in _rows_at(w, v, np_, ef_at(v)) if t["attr"] > 0 and _targets(w, v, t)]
                    if not rows:
                        continue
                    a = max(t["attr"] for t in rows)
                    sh = g.get("seen_herd") or {}
                    mem = (g.get("found_at") == v and 1 <= w.d - int(g["found"]) <= int(np_["memory_days"])) or (
                        sh and w.d - int(sh["day"]) <= int(np_["memory_days"]) and (w.s["herds"].get(sh["hid"]) or {}).get("node") == v)
                    cands.append((v, a * math.exp(-float(D[c, homes[v]]) / R) * (float(RANGE_PICK["memory"]) if mem else 1.0), rows, a))
                if not cands:
                    continue
                u, acc = rng.random() * sum(x[1] for x in cands), 0.0
                pick = cands[-1]
                for x in cands:
                    acc += x[1]
                    if u < acc:
                        pick = x
                        break
                v, _, rows, attr = pick
                g["node"] = v
            else:
                v = g["node"] if g.get("node") in rings else (near_v[c] or [None])[0]
                if v is None:
                    continue
                rows = _rows_at(w, v, np_, ef_at(v))
                attr = max([t["attr"] for t in rows] or [0.0])
            night_of(gid, g, v, rings[v], kind, np_, ef_at(v), rows, attr, hunger, lmul, rng, knows_here=g.get("found_at") == v)
            if g["found"] != found:
                g["found_at"] = g["node"]
    for pid, v in sorted(watch.items()):                                 # a watch nothing came to: a quiet night
        if not any(t["day"] == w.d and t["what"].split(":")[0] in ("turned", "raid", "tried") for t in traces.get(pid, [])):
            _trace(traces, pid, None, "watched", w.d, 0, v.get("scare"), v.get("by"))
    place = m.nodes[0]
    kept = {pid: v for pid, v in (wild.get("watch") or {}).items() if int(v.get("day", -9)) >= w.d}
    if kept != (wild.get("watch") or {}):
        w.apply("set_wild", place, path=["watch"], value=kept)
    shut = {b: v for b, v in (wild.get("shut") or {}).items() if int(v.get("day", -9)) >= w.d}
    if shut != (wild.get("shut") or {}):
        w.apply("set_wild", place, path=["shut"], value=shut)
    if groups != (wild.get("groups") or {}):
        w.apply("set_wild", place, path=["groups"], value=groups)
    if traces != (wild.get("traces") or {}):
        w.apply("set_wild", place, path=["traces"], value=traces)
    return out


def _hens_lay(w) -> None:
    """Kept hens lay (wild_layer.md, wave 2): an engine day is about 11 real days, so a hen lays about five eggs a day (calibrate)."""
    for bid, b in sorted(w.s["buildings"].items()):
        if not b.get("stock"):
            continue
        n = float((w.s["containers"].get(b["stock"], {}).get("goods") or {}).get("hen", 0))
        if n >= 1:
            si = ["spring", "summer", "autumn", "winter"].index(w.calendar()["season"])
            eggs = round(n * (5.0, 4.0, 2.0, 0.5)[si] * EGG_FOOD / ITEM_EGG_FOOD, 2)
            if eggs > 0:
                w.apply("create", b["node"], dst=b["stock"], item="egg", qty=eggs, why="laid")


def shut(here) -> str:
    """Shutting up one's house and store for the night (the doors wedged, the gaps stopped): whatever comes for what is inside, a fox
    for the hens or a sounder for the grain, finds it shut (a target row's `door`)."""
    homes = [b for b in here._w.homes(here.name) if here._w.s["buildings"][b].get("stock")]
    if not homes:
        return "You have no store to shut up."
    for b in homes:
        here.apply("set_wild", path=["shut", b], value={"day": here.day, "by": here.name})
    hens = any(float((here._w.s["containers"].get(here._w.s["buildings"][b]["stock"], {}).get("goods") or {}).get("hen", 0)) >= 1 for b in homes)
    return "You shut " + ("the hens and " if hens else "") + "the store up for the night, the doors wedged and the gaps stopped."


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


def _poisson(rng, lam, most) -> int:
    """A Poisson draw by inversion from the run's keyed random numbers, capped at `most`."""
    lam = max(0.0, float(lam))
    if lam <= 0:
        return 0
    k, p = 0, math.exp(-lam)
    acc, u = p, rng.random()
    while u > acc and k < most:
        k += 1
        p *= lam / k
        acc += p
    return k


def _ground(m, land, node, areas, rng_word, km2) -> dict:
    """The ground a search covers, by area (brief 4 §2.2): all of it in the farthest areas the range reaches (home for near, the
    ring for the wood around, the bordering wild areas for far, shared), the areas crossed on the way at a fifth; none above an
    area's own size."""
    from cybertron2.wild.kinds import HUNT
    kind = {i: land["areas"][m.ids[i]]["kind"] for i in areas}
    far = {"near": "home", "the wood around": "ring", "far": "wild"}[rng_word]
    ends = [i for i in areas if kind[i] == far] or list(areas)
    out = {}
    for i in areas:
        g = km2 / len(ends) if i in ends else km2 * float(HUNT["cross"])
        out[i] = min(float(m.km2[i]), g)
    return out


def learned(wary) -> float:
    """What a kind's wariness does (brief 4b §2.1): it grows with the wariness and tops out (WARY `most`): game hunted hard is very
    shy, never impossible to come on."""
    from cybertron2.wild.kinds import WARY
    x = max(0.0, float(wary))
    return x / (1.0 + x / float(WARY["most"]))


def carry_of(here, ox=None) -> float:
    """What one hunter can bring home (brief 4 §2.4; brief 4b §3.2): on foot, a pack's more, and a led beast's."""
    from cybertron2.engine.data import HERDS, ITEMS, PHYSICS
    cap = float(PHYSICS["carry"]["foot"]) + float((ITEMS.get("pack") or {}).get("carry", 0.0)) * (1 if here.carried().get("pack", 0) >= 1 else 0)
    return cap + (float(HERDS["pack_ox"]["carry"]) if ox else 0.0)


def member(here, mind, out, m_skill, t, ox=None) -> dict:
    """One hunter of a hunt: who, where what they take goes, their skill at the method, the units they search, and their carry."""
    return {"name": here.name, "here": here, "mind": mind, "out": out, "skill": float(m_skill), "t": float(t), "ox": ox,
            "cap": carry_of(here, ox)}


def take(here, mind, tech, key, place_name, out, m_skill, y, a) -> tuple:
    """A hunt by one hunter alone (brief 4 §2): `hunt` with a party of one. Returns (food taken, a line for the hunter, what they
    noticed on the way)."""
    from cybertron2.engine.data import TECHNIQUES
    ox = (a.get("_mods") or {}).get("_ox")
    ms = [member(here, mind, out, m_skill, float(TECHNIQUES[tech]["units"]), ox)]
    r = hunt(here, ms, tech, key, place_name, y, a)
    practise(ms, tech, r)
    return r["food"][here.name], r["lines"][here.name], r["tails"][here.name]


def chance(x) -> float:
    """A chance from the product of a baseline and its multipliers (brief 4c §3.1): 1 - e^(-x), the product itself at low odds,
    never certain, with no clip."""
    return 1.0 - math.exp(-max(0.0, float(x)))


def take_chance(tech, skill, gear_x, flee, fam_x, n_out=1) -> float:
    """A beast met is taken (brief 4c §3.1): the method's baseline (a bare-handed novice's, `take_base`) times the multipliers, gear,
    skill and familiarity, and the kind's (1 - flee), as 1 - e^(-x); for a crew's method x (1 + `crew` a member past the first) of
    those out (brief 4c §5)."""
    from cybertron2.engine.data import TECHNIQUES
    from cybertron2.wild.kinds import HUNT
    crew_x = (1.0 + float(HUNT["crew"]) * (int(n_out) - 1)) if TECHNIQUES[tech].get("crew") else 1.0
    base = float(TECHNIQUES[tech].get("take_base", HUNT["take_k"]))
    return chance(base * float(skill) * float(gear_x) * (1.0 - float(flee)) * float(fam_x) * crew_x)


def find_x(tech, skill) -> float:
    """How much more game the best hunter out comes on (brief 4c §3.2): for the hunt's methods, (skill / the capable's)^find_hard
    above the capable, 1 at or below it; other methods 1."""
    from cybertron2.engine.data import SKILL, TECHNIQUES
    if TECHNIQUES[tech].get("curve") != "hard":
        return 1.0
    return max(1.0, float(skill) / float(SKILL["capable_hard"])) ** float(SKILL.get("find_hard", 0.0))


def gear(tech, carried) -> float:
    """What one carries multiplies a method's take (brief 4c §3.1; the method's `gear` row, by item): the best weapon in hand, one
    at a time, times each other piece of gear the method names."""
    from cybertron2.engine.data import ITEMS, TECHNIQUES
    have = [(it, float(x)) for it, x in sorted((TECHNIQUES[tech].get("gear") or {}).items()) if float(carried.get(it, 0) or 0) >= 1]
    weapons = [x for it, x in have if (ITEMS.get(it) or {}).get("weapon")]
    out = max(weapons, default=1.0)
    for it, x in have:
        if not (ITEMS.get(it) or {}).get("weapon"):
            out *= x
    return out


def hunt(here, members, tech, key, place_name, y, a) -> dict:
    """A hunt as a search over time (brief 4 §2), by one hunter or a declared party (brief 4b §3.1), the first member leading: the
    method's units search ground (its `sweep` a unit a hunter) in the areas the range reaches; what is met there is a number drawn by
    the kinds' densities, how easy each is to find, what this way of hunting takes, the hunters' focus and familiarity, how hunted the
    ground is and how wary its game has grown. Each meeting falls at a time in the search, a keyed draw: only the members still out
    then count (a member with fewer units turns back for home when they are spent). Each in turn may hurt one in front (D2-193; the
    danger spread across those out), flee, or be taken by the best hunter out, until those out can carry no more; a kill is dressed
    where it fell and shared across their hands up to each one's carry. What cannot be carried is cut and left, and the offal with it.
    Looking for one thing makes it likelier and the rest less likely, never impossible. Returns {"food": {name: food}, "lines":
    {name: the hunt's events in order, as that member knows them}, "tails": {name: what they noticed on the way}}."""
    from cybertron2.engine.data import ITEMS, RESOURCES, TECHNIQUES, THINGS
    from cybertron2.engine import things as TH
    import numpy as np
    w = here._w
    names = [mb["name"] for mb in members]
    if not on(w) or not (w.s.get("wild") or {}).get("state"):
        return {"food": {n: 0.0 for n in names}, "lines": {n: f"You found nothing to take at {place_name}." for n in names},
                "tails": {n: "" for n in names}, "kills": {n: 0 for n in names}, "t": {mb["name"]: float(mb["t"]) for mb in members}}
    m = model(w)
    land = w.s["wild"]["land"]
    st = w.s["wild"]["state"]
    mods = a.get("_mods") or {}
    rng_word = (mods.get("range") if isinstance(mods.get("range"), str) else None) or "near"
    areas = _reach(m, land, here.node, rng_word)
    takes = dict(y["takes"])
    from cybertron2.wild import methods as MT
    from cybertron2.wild.kinds import HUNT, HUNTED, LEAD, LEGENDS, LEADERS, WARY
    if a.get("looking for") and str(a.get("looking for")).strip().lower() not in ("anything", "whatever comes", "game", "any") \
            and not _wanted(a.get("looking for"), [k for k, r in RESOURCES.items() if r.get("taken")]):
        from cybertron2.engine.here import Refused
        raise Refused(f"you know of no beast called {a.get('looking for')!r}")      # a target resolves whether or not it is here (D2-207)
    want = _wanted(a.get("looking for"), takes)
    rng = here.rng("wild-take", here.day, here.name, tech)
    ring_i = next((i for i in areas if land["areas"][m.ids[i]]["kind"] == "ring"), areas[0] if areas else None)
    efx = {k: effects(w, here.node, k, m, st, ring_i) for k in sorted(takes)}
    run = run_density(w, m, st)
    runs = None
    when_rows = [row for row in (y.get("when") or []) if cond(w, here.node, row.get("if"), None, m, st, ring_i)]

    def when_for(k):                                                      # a way of taking that pays on its nights, for the kinds that
        tr = ((RESOURCES.get(k) or {}).get("taken") or {}).get("traits") or {}     # move on that cue (an eel night: D2-204)
        x = 1.0
        for row in when_rows:
            if all(tr.get(t) == v for t, v in (row.get("for") or {}).items()):
                x *= float(row.get("x", 1.0))
        return x
    crew = len(members)
    T = float(TECHNIQUES[tech]["units"])                                  # the method's units search; the range's are travel (§2.1)
    ts = [max(0.0, min(T, float(mb["t"]))) for mb in members]
    led = any(mb.get("ox") for mb in members)
    sweep = float(TECHNIQUES[tech].get("sweep", HUNT["sweep"]))
    ground = _ground(m, land, here.node, areas, rng_word, sweep * sum(ts))
    pressure = {k: [float(x) for x in ((st.get("pressure") or {}).get(k) or [0.0] * m.n)] for k in takes if k in st["pop"]}
    pressure0 = {k: list(v) for k, v in pressure.items()}
    wary = {k: [float(x) for x in ((st.get("wary") or {}).get(k) or [0.0] * m.n)] for k in takes if k in st["pop"]}
    wary0 = {k: list(v) for k, v in wary.items()}
    for kk in pressure:                                                   # the hunt disturbs the ground it covers (§2.8), and the
        for ii in areas:                                                  # game there learns it (brief 4b §2.1)
            share = min(1.0, ground[ii] / float(m.km2[ii]))
            pressure[kk][ii] = round(pressure[kk][ii] + float(HUNTED["hunt"]) * share * (1 + float(HUNTED["crew"]) * (crew - 1)), 4)
            wary[kk][ii] = round(wary[kk][ii] + float(WARY["hunt"]) * share, 4)
    fam = lambda mb, k: MT.factor(mb["mind"], k)
    finds = find_x(tech, max(mb["skill"] for mb in members))           # above the capable, the party's best finds more (4c §3.2)
    cand = []
    for k, tw in sorted(takes.items()):
        if k not in st["pop"]:
            continue
        tk = (RESOURCES.get(k) or {}).get("taken") or {}
        focus = (3.0 if k in want else 0.4) if want else 1.0
        x = when_for(k) * max(fam(mb, k) for mb in members) * focus * float(tw) * finds   # familiarity with the kind (D2-204 §5): the party's best
        for i in areas:
            dens = float(st["pop"][k][i]) * pushed(w, m, here.node, key, k, i) + (run[k][i] if k in run else 0.0)   # the cold's push onto open water (brief 5 §4); a run passing today (§2.4)
            shy = 1.0 + float(WARY["detect"]) * learned(wary0[k][i])        # game that has learned people is harder to come on (4b §2.1)
            lam = dens * float(tk.get("detect", 0.2)) * efx[k]["detect"] * x / (1.0 + 0.5 * min(4.0, pressure0[k][i])) / shy \
                * ground[i] * float(HUNT["meet"]) * (float(LEAD["seen"]) if led else 1.0)   # a beast led: the game knows them sooner
            if lam > 0 and dens * float(m.km2[i]) >= 1.0:                  # one met is a whole one
                cand.append((k, i, lam))
    total = sum(c[2] for c in cand)
    looked = f" looking for {a.get('looking for')}" if want else ""
    where = {"near": place_name, "the wood around": f"the woods and wastes around {place_name}", "far": "the wild land far beyond"}[rng_word]
    tails = {}
    for mb, t_ in zip(members, ts):                                       # what each noticed while out (their own eyes)
        seen = _notices(mb["here"], mb["mind"], m, st, areas, key, max(0.5, t_ / 2.0))
        tails[mb["name"]] = (" On the way you saw " + "; and ".join(seen) + ".") if seen else ""
    n_met = _poisson(rng, total, int(HUNT["most"]) * crew)                # at most `most` a hunter
    times = sorted(rng.random() * t_ for t_ in [rng.choices(ts, weights=ts)[0] if sum(ts) > 0 else 0.0 for _ in range(n_met)])
    ev = []                                                               # the hunt's events in order: (time, text by whom, who)
    load = {mb["name"]: 0.0 for mb in members}
    food = {mb["name"]: 0.0 for mb in members}
    held = {mb["name"]: {} for mb in members}
    left, left_kind, pops, extra = {}, None, {}, ""
    hurt = set()
    dead = set()
    kills = {mb["name"]: 0 for mb in members}                             # the kills each saw made while out (brief 4c §3.3)
    out_at = lambda tau: [mb for mb, t_ in zip(members, ts) if t_ > tau + 1e-9 and mb["name"] not in hurt | dead]
    for n, tau in enumerate(times):
        here_out = out_at(tau)
        if not here_out:
            break
        if all(load[mb["name"]] >= mb["cap"] - 1e-9 for mb in here_out):
            break
        u, acc = rng.random() * total, 0.0
        for k, i, lam in cand:
            acc += lam
            if u < acc:
                break
        tk = dict((RESOURCES.get(k) or {}).get("taken") or {})
        lg = (w.s["wild"].get("legends") or {}).get(k)
        legend = None
        if lg and lg.get("alive") and lg["area"] == m.ids[i]:
            cnt = max(1.0, float(st["pop"][k][i]) * float(m.km2[i]))
            if rng.random() < min(0.5, 3.0 / cnt):
                legend = LEGENDS[k]
                tk["flee"] = min(0.97, float(tk.get("flee", 0.5)) * float(legend["flee"]))
                if tk.get("danger"):
                    tk["danger"] = {kk: float(v) * float(legend["danger"]) for kk, v in tk["danger"].items()}
                tk["goods"] = {it: round(float(q) * float(legend["goods"]), 2) for it, q in (tk.get("goods") or {}).items()}
        n_out = len(here_out)
        best = max(here_out, key=lambda mb: (mb["skill"] * gear(tech, mb["here"].carried()) * fam(mb, k), -names.index(mb["name"])))
        armed = best["here"].weapon()                                       # the leader, of equals
        wpn = gear(tech, best["here"].carried())
        surprise = bool(want) and k not in want
        what = legend["name"] + " itself" if legend else _a(k)
        found = "{subj} came on " + what + (f" instead of the {a.get('looking for')} you were after" if surprise and not legend else "")
        danger = tk.get("danger")
        dmul = efx[k]["danger"]
        if danger and rng.random() < min(0.95, float(danger["wound"]) * dmul / n_out):   # the danger spread across those out
            if rng.random() < min(0.5, float(danger.get("kill", 0.0)) * dmul / n_out):
                ev.append((tau, found + "; it turned on {subj}, and {subj} {was} killed", best["name"], True))
                best["here"].apply("die", person=best["name"], cause=f"killed by {_a(k)} while hunting")
                dead.add(best["name"])
                continue
            best["here"].apply("harm", person=best["name"], wounded=True)
            ev.append((tau, found + "; it turned on {subj}, and {subj} {was} hurt before it broke away, and came home", best["name"], True))
            hurt.add(best["name"])
            continue
        flee = min(0.95, float(tk.get("flee", 0.5)) * efx[k]["flee"])
        flee = 1.0 - (1.0 - flee) / (1.0 + float(WARY["flee"]) * learned(wary0[k][i]))   # and quicker to flee
        if led:
            flee = 1.0 - (1.0 - flee) * (1.0 - float(LEAD["flee"]))
        p_take = take_chance(tech, best["skill"], wpn, flee, fam(best, k), n_out)
        if rng.random() >= p_take:
            if armed and tk.get("danger") and rng.random() < 0.3:          # hit but not down: a wounded beast lying up
                here.apply("set_wild", path=["state", "wounded", f"{k}@{i}"], value=here.day)
                ev.append((tau, found + "; {subj} hit it, but it broke away into the thicket, bleeding", best["name"], False))
            else:
                ev.append((tau, found + ", but it got away", best["name"], False))
            continue
        pressure[k][i] = round(pressure[k][i] + float(HUNTED["kill"]) * min(1.0, ground[i] / float(m.km2[i])), 4)   # on the ground hunted
        pop = pops.setdefault(k, [float(v) for v in st["pop"][k]])
        wary[k][i] = round(wary[k][i] + float(WARY["take"]) / max(1.0, pop[i] * float(m.km2[i])), 4)   # the share of them taken
        r_ = run[k][i] if k in run else 0.0
        if r_ > 0 and rng.random() < r_ / (r_ + pop[i]):                   # one of the run's (brief 5 §2.4)
            from cybertron2.wild import runs as RU
            import copy
            runs = runs if runs is not None else {"runs": copy.deepcopy(st["runs"])}
            if RU.take_one(m, runs, eco_day(w), k, i):
                run[k][i] = max(0.0, r_ - 1.0 / float(m.km2[i]))
        else:
            pop[i] = max(0.0, pop[i] - 1.0 / float(m.km2[i]))              # one head off its area's count
        lit = tk.get("litter")                                             # young taken with it (cubs at the earth in spring): the kind's
        home_need = (TECHNIQUES[tech].get("needs") or {}).get("home")       # own row, by a method that works its home (D2-204)
        if lit and home_need and lit.get("home") in (home_need if isinstance(home_need, list) else [home_need]) \
                and cond(w, here.node, lit.get("if"), k, m, st, ring_i):
            pop[i] = max(0.0, pop[i] - float(lit["n"]) / float(m.km2[i]))
        MT.raise_familiar(best["here"], best["mind"], k, MT.FAMILIAR["take"], tech)   # the one whose shot took it learns the kind (§5)
        for mb in here_out:                                                 # and those out with them see it done (brief 4c §3.3)
            kills[mb["name"]] += 1
            if mb is not best:
                MT.raise_familiar(mb["here"], mb["mind"], k, float(MT.FAMILIAR["take"]) * float(MT.FAMILIAR["party"]), tech)
        gid, g = group_at(w, k, here.node)                                 # its group, or the ranging one that works here (4c §7.2)
        if legend:
            here.apply("set_wild", path=["legends", k], value=dict(lg, alive=False, died=here.day, by=best["name"]))
            here.event("hunt", f"{best['name']} killed {legend['name']}", salience=0.9, tags=["hunting", "danger"])
            extra += f" It was {legend['name']} the old ones tell of."
        if g:                                                               # its group is one fewer, and wary of the village
            np_ = _near(k) or {}
            g2 = dict(g, n=max(0, int(g["n"]) - 1), habit={}, wary=here.day + int(np_.get("wary_after_harm", 5)))
            ld = LEADERS.get(k)
            if ld and (g.get("leader") or {}).get("alive") and rng.random() < min(1.0, float(ld["kill_odds"]) / max(1, int(g["n"]))):
                g2["leader"] = dict(g["leader"], alive=False, died=here.day)  # the leader herself: the group scatters
                extra += f" It was {ld['name']} that led them."
            here.apply("set_wild", path=["groups", gid], value=g2)
        got = {}                                                            # dressed where it fell; shared across the hands out (4b §3.1)
        meat_here = 0.0
        for item, q in sorted((tk.get("goods") or {}).items()):
            wt = float((ITEMS.get(item) or {}).get("weight", 1)) or 1.0
            need = float(q)
            order = sorted(here_out, key=lambda mb: (mb["name"] != best["name"], mb["name"]))
            rooms = {mb["name"]: max(0.0, mb["cap"] - load[mb["name"]]) / wt for mb in order}
            space = sum(rooms.values())
            given = 0.0
            for j, mb in enumerate(order):                                  # by each one's room; the last takes what is over
                fair = need * rooms[mb["name"]] / space if space > 1e-12 else 0.0
                share = round(min(rooms[mb["name"]], fair if j < len(order) - 1 else min(need, space) - given), 2)
                given += share
                if share > 1e-9:
                    mb["here"].apply("create", dst=mb["out"], item=item, qty=share, why=tech)
                    held[mb["name"]][item] = round(held[mb["name"]].get(item, 0.0) + share, 2)
                    load[mb["name"]] += share * wt
                    food[mb["name"]] += share if item in ("meat", "fish") else 0.0   # eels and salmon are fish (D2-216)
                    got[item] = round(got.get(item, 0.0) + share, 2)
            if need - got.get(item, 0.0) > 1e-9:
                left[item] = round(left.get(item, 0.0) + need - got.get(item, 0.0), 2)
                left_kind = k
            if item == "meat":
                meat_here = need
        if meat_here > 0:                                                   # the offal is left where it was gutted (§3.4)
            left["offal"] = round(left.get("offal", 0.0) + meat_here * float(THINGS["carcass_offal"]), 2)
            left_kind = left_kind or k
        ev.append((tau, found + " and took it: " + (", ".join(f"{q:g} {it}" for it, q in sorted(got.items())) or "nothing that could be carried"),
                   best["name"], False))
        if rng_word == "near" and key in here.parcels():                    # the kill's signs (signs.HUNTED)
            rec = here.parcels()[key].get("hunted") or {}
            on_ground = list(rec.get("kills") or []) if rec.get("day") == here.day else []    # not `kills`, the members' count
            on_ground.append({"by": best["name"], "meat": got.get("meat", 0.0), "hide": "hide" in got, "kind": k})
            here.apply("set", ref=("parcel", key), field="hunted", value={"day": here.day, "kills": on_ground})
    for k, pop in sorted(pops.items()):
        here.apply("set_wild", path=["state", "pop", k], value=pop)
    if runs is not None:
        here.apply("set_wild", path=["state", "runs", "pulses"], value=runs["runs"]["pulses"])
    _put_pressure(here, pressure, wary)
    flesh_left = float(left.get("meat", 0.0))
    if left and (flesh_left > 0 or left.get("offal")):                     # what could not be carried is cut and left (§2.4)
        if rng_word == "near" and key in here.parcels():
            if flesh_left > 0:
                cid = here.apply("new_thing", node=here.node, parcel=key, kind="carcass", beast=left_kind, of=f"what was left of {_a(left_kind)}",
                                 holders=[], cause="killed", died=here.day, by=here.name, mass0=round(flesh_left + left.get("offal", 0.0), 2))
                here.apply("create", dst=cid, item="meat", qty=round(flesh_left, 2), why="left by the hunter")
                if left.get("offal"):
                    here.apply("create", dst=cid, item="offal", qty=round(left["offal"], 2), why="left by the hunter")
        else:
            far_i = max(areas, key=lambda j: ground[j])
            pool = [float(v) for v in st["carrion"]]
            pool[far_i] = round(pool[far_i] + (flesh_left + float(left.get("offal", 0.0))) * float(THINGS["carcass_kg"]) / float(m.km2[far_i]), 2)
            here.apply("set_wild", path=["state", "carrion"], value=pool)
    r = _hunt_lines(members, ts, ev, held, flesh_left, where, looked, food, tails, extra, dead, hurt)
    r.update(kills=kills, t={mb["name"]: t_ for mb, t_ in zip(members, ts)}, dead=sorted(dead))
    return r


def practise(members, tech, r) -> None:
    """Practice from a hunt (brief 4c §3.3), for each member who came home: the units they searched, a trip on which a kill was made
    while they were out counting `kill_hard` times; in a party led by a better hunter, x (1 + the leader's lead over them as a share
    of the leader's skill), at most `lead_hard`. The pace by lifespan and a youth's are knowledge.tried's."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import SKILL
    lead = KN.skill(members[0]["mind"], tech)
    for mb in members:
        if mb["name"] in (r.get("dead") or []):
            continue
        u = float((r.get("t") or {}).get(mb["name"], mb["t"]))
        if (r.get("kills") or {}).get(mb["name"]):
            u *= float(SKILL["kill_hard"])
        if mb is not members[0] and lead > 0:
            u *= min(float(SKILL["lead_hard"]), 1.0 + max(0.0, lead - KN.skill(mb["mind"], tech)) / lead)
        KN.tried(mb["here"], mb["mind"], tech, True, units=u)


def _hunt_lines(members, ts, ev, held, flesh_left, where, looked, food, tails, extra, dead, hurt) -> dict:
    """Each member's account of the hunt (brief 4b §3.1): the events in order up to when they turned back (those who stayed learn all
    of it), worded from where they stood; who turned back and when; and what each carried home."""
    solo = len(members) == 1
    others = lambda me: [mb["name"] for mb in members if mb["name"] != me]
    lines = {}
    for mb, t_ in zip(members, ts):
        me = mb["name"]
        story = []
        marks = sorted([(t2, "turn", mb2["name"]) for mb2, t2 in zip(members, ts) if t2 < max(ts) - 1e-9] +
                       [(tau, "ev", (txt, who, ends)) for tau, txt, who, ends in ev])
        for tau, kind, x in marks:
            if tau > t_ + 1e-9:
                break
            if kind == "turn":
                story.append("you turned back for home, your day spent" if x == me else f"{x} turned back for home")
                if x == me:
                    break
                continue
            txt, who, ends = x
            story.append(txt.format(subj="you" if who == me else who, was="were" if who == me else "was"))
            if who == me and ends:                                          # hurt or killed: the hunt ended there for them
                break
        if not ev and solo:
            lines[me] = f"You hunted {where}{looked} and came on nothing."
            continue
        if not story:
            story = ["nothing was met"]
        story = [s if j == 0 else "then " + (s.removeprefix("you ") if solo else s) for j, s in enumerate(story)]
        party = "" if solo else " with " + ", ".join(others(me))
        carried = held[me]
        tail_ = ""
        if not solo:
            tail_ = "; you carried home " + (", ".join(f"{q:g} {it}" for it, q in sorted(carried.items())) or "nothing")
        if flesh_left > 0 and (me not in dead) and (t_ >= max(ts) - 1e-9 or solo):
            tail_ += f"; {'you' if solo else 'the party'} could carry no more, and left {flesh_left:g} meat"
        lines[me] = f"Hunting {where}{party}{looked if not solo else ''}, " + "; ".join(story) + tail_ + "." + extra
    return {"food": food, "lines": lines, "tails": tails}


NOTICE_MOST = 2


def _word(table, x) -> str:
    return next(w_ for t, w_ in table if x >= t)


def _state_words(m, st, k, areas, count) -> dict:
    """What an expert reads of a kind in the areas hunted: about how many, its condition, its wariness, its hunger (kinds' words)."""
    from cybertron2.wild.kinds import FAT_WORDS, WARY_WORDS, HUNGER_WORDS
    import numpy as np
    w8 = [float(st["pop"][k][i]) * float(m.km2[i]) for i in areas]
    tot = sum(w8) or 1.0
    cond_ = sum(float(np.asarray(st["cond"][k])[i]) * w_ for i, w_ in zip(areas, w8)) / tot
    pres = sum(float(((st.get("pressure") or {}).get(k) or [0.0] * m.n)[i]) * w_ for i, w_ in zip(areas, w8)) / tot
    n = int(round(count)) if count < 20 else int(round(count, -1))
    return {"n": n, "fat": _word(FAT_WORDS, cond_), "wary": _word(WARY_WORDS, pres), "hunger": _word(HUNGER_WORDS, 1.0 - cond_)}


def _notices(here, mind, m, st, areas, key, effort) -> list:
    """What a hunter notices of the kinds in the range they hunt, met or not (kinds.HUNT_NOTICES): a process of its own, as a
    traveller's notices on the road. Each row by the one rule (D4-75): its own plainness x how likely the kind's sign is there (its
    numbers and how easily found) x the place's visibility for the sense x the eye; read by the practised or the rest (`knows`/`lay`).
    What was seen is remembered of the place (perceive.remember_land)."""
    from cybertron2.engine import environment as EV, perceive as PC, signs as SG, things as TH
    from cybertron2.engine.data import NOTICING, RESOURCES
    from cybertron2.wild.kinds import HUNT_NOTICES
    from types import SimpleNamespace
    rng = here.rng("wild-notice", here.day, here.name)
    eye = TH.eye(here._w, here.name)
    par = here.parcels().get(key) or {}
    rows, pres = [], {}
    for k, rs in sorted(HUNT_NOTICES.items()):
        if k not in st["pop"]:
            continue
        count = sum(float(st["pop"][k][i]) * float(m.km2[i]) for i in areas)
        if count < 1.0:
            continue
        detect = float(((RESOURCES.get(k) or {}).get("taken") or {}).get("detect", 0.2))
        pres[k] = 1.0 - math.exp(-0.15 * count * detect * effort)
        fmt = _state_words(m, st, k, areas, count)
        for r in rs:
            row = dict(when=lambda x: True, own=float(r["own"]) * pres[k], sense=r["sense"], text=lambda x, t=r["text"].format(**fmt): t, kind=k)
            if r["read"] in ("lay", "knows"):
                row[r["read"]] = "hunt"
            elif r["read"] == "expert":
                row["knows"] = f"familiar:{k}"                                    # one who knows this kind well (D2-204 §5)
            rows.append(row)

    from cybertron2.wild.kinds import LEGENDS
    for k, lg in sorted((here._w.s["wild"].get("legends") or {}).items()):
        if lg.get("alive") and lg["area"] in [m.ids[i] for i in areas]:
            for r in LEGENDS[k]["rows"]:
                rows.append(dict(when=lambda x: True, own=float(r["own"]), sense=r["sense"], text=lambda x, t=r["text"]: t, kind=k,
                                 knows=f"familiar:{k}"))

    def rule(row):
        sense = row.get("sense", "sight")
        vis = EV.visibility(here._w, here.node, parcel=key, sense=sense, cover=par.get("cover"))
        return float(row["own"]) * vis * (eye if sense in NOTICING["eye_senses"] else 1.0)
    got = SG.roll(rows, SimpleNamespace(), rng, know=PC.practised(mind), rule=rule)[:NOTICE_MOST]
    from cybertron2.wild import methods as MT
    for k in sorted({r["kind"] for r in rows if r["text"](None) in got}):  # a sign noticed while working teaches a little (§5)
        MT.raise_familiar(here, mind, k, MT.FAMILIAR["notice"])
    if got and key in here.parcels():
        PC.remember_land(mind, here.day, key, "the wild", "; ".join(got), "hunted")
    return got


def _put_pressure(here, pressure, wary=None) -> None:
    w = here._w
    for name, tbl in (("pressure", pressure), ("wary", wary or {})):
        old = (w.s["wild"]["state"].get(name) or {})
        for k, v in sorted(tbl.items()):
            if v != old.get(k):
                here.apply("set_wild", path=["state", name, k], value=v)


def _a(kind) -> str:
    return ("an " if kind[0] in "aeiou" else "a ") + kind


def pick_scare(here, y, a=None) -> dict:
    """A guard's scare (D2-204): the one named with `looking for`, else the first of the method's scares one has (wood for a fire, clappers
    or a horn to hand, a dog at home)."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.here import Refused
    want = str((a or {}).get("looking for") or "").strip().lower()
    scares = y.get("scares") or []
    named = [s for s in scares if want and (want in s["names"] or want == s["scare"])]

    def have(s):
        if s.get("home_fittings"):
            return any(any(here._w.s["buildings"][b]["fittings"].get(f) for f in s["home_fittings"]) for b in here._w.homes(here.name)
                       if here._w.s["buildings"][b]["node"] == here.node)
        return all(KN.available(here, i) + 1e-9 >= float(q) for i, q in (s.get("uses") or {}).items())
    if named:                                                             # the scare one named, or why not
        s = named[0]
        if have(s):
            return s
        if s.get("home_fittings"):
            raise Refused(f"a watch with {s['with']} needs a dog at home, and you keep no dog")
        raise Refused(f"a watch with {s['with']} needs " + ", ".join(f"{q:g} {i}" for i, q in s["uses"].items()) + " to hand")
    for s in scares:
        if have(s):
            return s
    raise Refused("you have nothing to scare them off with: wood for a fire, clappers, a horn, or a dog at home")


def watch(here, pid, y, place_name, a=None) -> str:
    """A night watch over a field with a scare (the method's scares, or an older row's own): read by the night's groups (D2-198)."""
    if y.get("scares"):
        y = {**y, **pick_scare(here, y, a)}
    if y.get("burns"):                                                    # a fire burns its wood (one-off 2 in 02zq)
        from cybertron2.engine.verbs import _consume
        _consume(here, y["burns"])
    here.apply("set_wild", path=["watch", pid], value={"day": here.day, "by": here.name, "scare": y["scare"]})
    here.today().setdefault("night_watch", {})[here.name] = pid           # D2-21: the night given up, more food, tired tomorrow
    return f"You set yourself to watch {place_name} tonight with {y.get('with', y['scare'])}, and will lose the night's sleep."


def _crop_food(w, node) -> float:
    from cybertron2.engine import farm as FM
    return sum(float(c.get("left", 0.0)) for pid, par in w.s["parcels"].items() if par["node"] == node
               for _, _, c in FM.standing(par) if c.get("area_left", 0) > 1e-6)


def _store_food(w, node) -> float:
    return sum(float(q) for b in w.s["buildings"].values() if b["node"] == node and b.get("stock")
               for item, q in (w.s["containers"].get(b["stock"], {}).get("goods") or {}).items() if item in DRY_STORES)


def _crop_food_qty(w, node) -> float:
    """The standing crop on a node's fields, in its own units (what `_crops` draws a share of)."""
    from cybertron2.engine import farm as FM
    return sum(float(c.get("left", 0.0)) for pid, par in w.s["parcels"].items() if par["node"] == node
               for _, _, c in FM.standing(par) if c.get("area_left", 0) > 1e-6)


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


def _stops(b, kind, w=None) -> float:
    """What a building's fittings leave of a kind's take from its store (STORE_STOPS: a granary against what climbs and is tiny, bins
    against the tiny, a dog against all, a cat against the tiny), by the kind's body (brief 2 §4)."""
    from cybertron2.engine.data import RESOURCES
    from cybertron2.wild.kinds import STORE_STOPS
    body = (RESOURCES.get(kind) or {}).get("body") or {}
    keep = 1.0
    for f_, row in STORE_STOPS.items():
        if row.get("in_store"):                                            # a cat: a beast in the store, not a fitting (D2-206)
            have = w is not None and float((w.s["containers"].get(b.get("stock"), {}).get("goods") or {}).get(f_, 0)) >= 1
        elif row.get("occupied"):                                          # an owl in its hole
            have = w is not None and ((w.s["wild"].get(row["occupied"]) or {}).get(b.get("_id")) is not None)
        else:
            have = bool((b.get("fittings") or {}).get(f_))
        if have and (kind is None or all(body.get(t) == v for t, v in (row.get("for") or {}).items())):
            keep *= float(row["keep"])
    return keep


def _left_out(w, node) -> list:
    """Food lying at the doors of a node's houses (D2-85 things there, D4-89): [(thing id, thing)] (brief 4 §4.1)."""
    from cybertron2.wild.kinds import LEFT_OUT
    out = []
    for cid, c in sorted(w.s["containers"].items()):
        if c.get("kind") == "pile" and c.get("node") == node and c.get("door") in w.s["buildings"] and not c.get("hidden") \
                and any(float((c.get("goods") or {}).get(i, 0.0)) > 1e-9 for i in LEFT_OUT["items"]):
            out.append((cid, c))
    return out


def _racks_in(w, node) -> list:
    """Racks of food hanging inside a node's houses, at a hearth (brief 4c §6.2): [(thing id, thing)]. Part of the house: what comes
    for them comes as for its store."""
    from cybertron2.wild.kinds import LEFT_OUT
    return [(cid, c) for cid, c in sorted(w.s["containers"].items()) if c.get("kind") == "pile" and c.get("node") == node
            and c.get("in") in w.s["buildings"] and c.get("rack")
            and any(float((c.get("goods") or {}).get(i, 0.0)) > 1e-9 for i in LEFT_OUT["items"])]


def _food_out_night(w) -> None:
    """Which houses had food left out at the door tonight, for the cats that come to it (brief 4 §4.1)."""
    from cybertron2.wild.kinds import LEFT_OUT
    rec = dict(w.s["wild"].get(LEFT_OUT["record"]) or {})
    for node in sorted(w.s["nodes"]):
        for cid, c in _left_out(w, node):
            rec[c["door"]] = w.d
    if rec != (w.s["wild"].get(LEFT_OUT["record"]) or {}):
        w.apply("set_wild", sorted(w.s["nodes"])[0], path=[LEFT_OUT["record"]], value=rec)


def _store_beasts(w, m, st) -> dict:
    """At a season's turn (D2-206; brief 2 K1): a cat (kinds.CAT) settles at a store with dry food and its prey about (no dog), or
    leaves one with none or with a dog; in its season a barn owl (kinds.OWL) takes an empty owl hole in a building nobody sleeps in."""
    from cybertron2.wild.kinds import CAT, LEFT_OUT, OWL
    out = {}
    if w.calendar(w.d + 1)["season"] == w.calendar()["season"]:
        return out
    land = w.s["wild"]["land"]
    sleeping = set((w.s.get("today") or {}).get("sleep", {}).values())
    nests = dict(w.s["wild"].get(OWL["record"]) or {})
    beast = CAT["item"]
    for bid, b in sorted(w.s["buildings"].items()):
        cid = b.get("stock")
        if not cid or cid not in w.s["containers"]:
            continue
        goods = w.s["containers"][cid].get("goods") or {}
        dry = sum(float(goods.get(i, 0)) for i in DRY_STORES)
        dog = bool((b.get("fittings") or {}).get("dog"))
        have = float(goods.get(beast, 0)) >= 1
        aid = land.get("home", {}).get(b["node"])
        i = m.ids.index(aid) if aid in m.ids else None
        prey = float(st["pop"][CAT["prey"]][i]) * float(m.km2[i]) if i is not None and CAT["prey"] in st["pop"] else 0.0
        rng = w.rng("wild-cat", w.d, bid)
        fed = w.d - int(((w.s["wild"].get(LEFT_OUT["record"]) or {}).get(bid) or -99)) <= int(CAT["fed_days"])   # food left out lately
        mice = dry > 1e-6 and prey >= float(CAT["prey_least"])
        S = w.year_days() // 4
        if have and (dog or (not mice and w.d - int(((w.s["wild"].get(LEFT_OUT["record"]) or {}).get(bid) or -99)) > S)):
            w.apply("destroy", b["node"], src=cid, item=beast, qty=float(goods[beast]), why="it went off")
            out[bid] = "left"                                               # no mice and no food left out for a season (cats.md §3)
        elif not have and not dog and (mice or fed) and rng.random() < float(CAT["fed_p" if fed else "settle_p"]):
            w.apply("create", b["node"], dst=cid, item=beast, qty=1.0, why="it came in after the prey in the store")
            w.event(b["node"], beast, f"a {beast} has taken up at {b['name']}", about=[f"building:{bid}"], salience=0.3, tags=["animals"])
            out[bid] = "came"
        if (b.get("fittings") or {}).get(OWL["fitting"]) and nests.get(bid) is None and w.calendar(w.d + 1)["season"] == OWL["season"] \
                and bid not in sleeping and w.rng("wild-nest", w.d, bid).random() < float(OWL["take_p"]):
            nests[bid] = w.d
            out[bid] = "nested"
    if nests != (w.s["wild"].get(OWL["record"]) or {}):
        w.apply("set_wild", m.nodes[0], path=[OWL["record"]], value=nests)
    return out


def _stores(w, node, share) -> float:
    """Destroy a share of the grain and other dry food in the node's stores: what wild kinds took there, kind by kind ({kind: share})."""
    shares = share if isinstance(share, dict) else {None: share}
    total = 0.0
    for bid, b in sorted(w.s["buildings"].items()):
        if b["node"] != node or not b.get("stock"):
            continue
        cid = b["stock"]
        keep = sum(sh * _stops(dict(b, _id=bid), k, w) for k, sh in shares.items()) / max(1e-12, sum(shares.values()))   # what this store's fittings let
        share = sum(shares.values())                                         # through, kind by kind
        plague = 1.0 + sum(float(r.get("stores", 0.0)) for name, r in REGIMES_ON(w, node).items())
        for item, q in sorted((w.s["containers"].get(cid, {}).get("goods") or {}).items()):
            if item in DRY_STORES and q > 0:
                take = round(float(q) * share * keep * plague, 4)
                if take > 1e-6:
                    w.apply("destroy", node, src=cid, item=item, qty=take, why="eaten in store by wild kinds")
                    total += take
        from cybertron2.wild.kinds import LEFT_OUT                          # a rack inside: at the store's rate (brief 4c §6.2)
        for rid, c in [(r, c) for r, c in _racks_in(w, node) if c["in"] == bid]:
            for item in LEFT_OUT["items"]:
                q = float((c.get("goods") or {}).get(item, 0.0))
                take = round(q * share * keep * plague, 4)
                if take > 1e-6:
                    w.apply("destroy", node, src=rid, item=item, qty=take, why="eaten on the rack by wild kinds")
                    total += take
    from cybertron2.wild.kinds import LEFT_OUT                              # and what is left out at the doors, in the open: as much
    for pid_, c in _left_out(w, node):                                    # again, nothing stopping them (brief 4 §4.1)
        for item in LEFT_OUT["items"]:
            q = float((c.get("goods") or {}).get(item, 0.0))
            take = round(q * min(1.0, 2.0 * sum(shares.values())), 4)
            if take > 1e-6:
                w.apply("destroy", node, src=pid_, item=item, qty=take, why="eaten by vermin at the door")
                total += take
    return total


# ---------------------------------------------------------------------- the river: runs, weirs, the mill's gap (brief 5 §2, §3, §3a)
def _runs_by_weather(w) -> bool:
    """Whether the fish runs follow the weather's cue: with a climate, unless the world sets the runs on their windows' set nights
    (`runs_set_nights`, D2-231: the runs world's model-per-household run, until the flow rule D2-215 is built)."""
    return bool(_climate(w)) and not w.spec.get("runs_set_nights")


def _climate(w) -> bool:
    from cybertron2.engine import climate as CL
    return bool(CL.on(w))


def _river_parcel(w, pid) -> bool:
    p = w.s["parcels"].get(pid) or {}
    return p.get("cover") == "water" and (p.get("land") or {}).get("river") not in (None, "none")


def is_weir(b) -> bool:
    return (b or {}).get("monument") == "weir"


def weirs(w, node) -> list:
    """The finished weirs at a village, [(bid, building)]."""
    return [(bid, b) for bid, b in sorted(w.s["buildings"].items()) if is_weir(b) and b.get("node") == node and not b.get("unfinished")]


def mill_water(w, b):
    """A water wheel's water: the river parcel at its building, or beside it (the leat's), the first by name; else the village's own
    river water (a leat brought from it); None off a river."""
    par = w.s["parcels"].get(b.get("parcel")) or {}
    for q in [b.get("parcel")] + sorted(par.get("adj") or []):
        if _river_parcel(w, q):
            return q
    return next((q for q, p in sorted(w.s["parcels"].items()) if p.get("node") == b.get("node") and _river_parcel(w, q)), None)


def has_gap(w, b) -> bool:
    """A weir, or a water wheel on a river that a run passes (brief 5 §3a): a gap, open or shut. A mill elsewhere has none."""
    if is_weir(b):
        return True
    if not (b.get("fittings") or {}).get("water wheel") or not on(w) or not (w.s.get("wild") or {}).get("state"):
        return False
    from cybertron2.wild import runs as RU
    return mill_water(w, b) is not None and RU.on_river(model(w), b.get("node"))


def gap(b) -> str:
    """A gap's state: a new weir's and a new water wheel's are shut (as built to fish, and as a miller builds it)."""
    return str(b.get("gap") or "shut")


def mills(w, node) -> list:
    return [(bid, b) for bid, b in sorted(w.s["buildings"].items()) if b.get("node") == node and not b.get("unfinished")
            and (b.get("fittings") or {}).get("water wheel") and has_gap(w, b)]


def sections(b) -> list:
    """A weir's sections (D2-210), the first of wattle, as [{"m": wattle | timber, "foot": a stone footing, "level": 5 to 0}]; a weir
    built before the sections is its first, at the building's level."""
    from cybertron2.engine import buildings as BL
    if b.get("sections"):
        return [dict(x) for x in b["sections"]]
    return [{"m": "wattle", "foot": False, "level": BL.level(b)}]


def weir_share(b) -> float:
    """What a weir takes of each run passing tonight (D2-210): each section's share by its condition, all of it x `open` with the gap
    open."""
    from cybertron2.engine.data import WATER_WORKS
    W = WATER_WORKS["weir"]
    x = sum(float(W["sections"][sc["m"]]["share"]) * float(W["by_level"].get(int(sc["level"]), 0.0)) for sc in sections(b))
    return x * (float(W["open"]) if gap(b) == "open" else 1.0)


def weir_hold(b) -> float:
    """What a weir's traps hold a night, in food (D2-210): each section's by its condition."""
    from cybertron2.engine.data import WATER_WORKS
    W = WATER_WORKS["weir"]
    return sum(float(W["sections"][sc["m"]]["hold"]) * float(W["by_level"].get(int(sc["level"]), 0.0)) for sc in sections(b))


def _upstream(w, pid) -> int:
    """How far up its village's water a parcel lies: the steps along the parcels' `down` to where the water leaves (D2-210: weirs take
    in turn from upstream)."""
    n, q, seen = 0, pid, set()
    while q in w.s["parcels"] and q not in seen:
        seen.add(q)
        q = (w.s["parcels"][q].get("land") or {}).get("down")
        n += 1
    return n


def water_kind(w, m, pid) -> str:
    """A weir's water (D2-210): an upland beck (a brook high up), a large river (the stretch holds big river), else a lowland river."""
    from cybertron2.engine.data import WATER_WORKS
    from cybertron2.wild import runs as RU
    land = (w.s["parcels"].get(pid) or {}).get("land") or {}
    if land.get("river") == "brook" and float(land.get("elevation", 0.0)) >= float(WATER_WORKS["weir"]["wear"]["beck_m"]):
        return "beck"
    return "large" if float(RU.net(m).big.get(f"v:{w.s['parcels'][pid]['node']}", 0.0)) > 0 else "lowland"


def _food_of(kind) -> float:
    from cybertron2.engine.data import ITEMS, RESOURCES
    return sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0.0))
               for i, q in ((((RESOURCES.get(kind) or {}).get("taken") or {}).get("goods")) or {}).items())


def _weir_wear(w, m, bid, b, flow) -> list:
    """A weir's sections worn tonight (D2-210): each loses Poisson(base x material x water x flow x the gap shut in high water x ice)
    levels; the building's level is its best section's. Returns the levels each lost."""
    from cybertron2.engine import buildings as BL
    from cybertron2.engine.data import WATER_WORKS
    W = WATER_WORKS["weir"]
    E = W["wear"]
    node = b["node"]
    ice = float(E["ice"]) if w.cold(node) else (float(E["thaw"]) if w.d >= 2 and w.cold(node, w.d - 1) and w.cold(node, w.d - 2) else 1.0)
    high = flow in ("high", "spate", "flood")
    x = float(E["base"]) * float(E["water"][water_kind(w, m, b["parcel"])]) * float(E["flow"][flow]) * ice \
        * (float(E["gap_high"]) if high and gap(b) == "shut" else 1.0)
    secs = sections(b)
    lost = []
    for j, sc in enumerate(secs):
        mat = float(W["sections"]["footing"]["wear"]) if sc.get("foot") else float(W["sections"][sc["m"]]["wear"])
        n = _poisson(w.rng("weir-wear", w.d, bid, j), x * mat, 5) if int(sc["level"]) > 0 else 0
        lost.append(n)
        sc["level"] = max(0, int(sc["level"]) - n)
    if any(lost):
        w.apply("set", node, ref=("building", bid), field="sections", value=secs)
        best = max(int(sc["level"]) for sc in secs)
        if best != BL.level(b):
            BL.set_level(w, node, bid, best)
        w.apply("set", node, ref=("building", bid), field="broke", value={"day": w.d, "level": best, "by": [flow] + (["ice"] if ice > 1 else []),
                                                                          "sections": lost})
    return lost


def mill_rate(w, b) -> float:
    """A water mill's rate by its gap (brief 5 §3a.1): shut, full; open, `open_rate` (the head of water lost)."""
    from cybertron2.engine.data import WATER_WORKS
    return float(WATER_WORKS["mill"]["open_rate"]) if has_gap(w, b) and gap(b) == "open" else 1.0


def _dam_stops(w, m) -> dict:
    """Each stretch's share of a run going up held below its shut dams tonight: {stretch: share}."""
    from cybertron2.engine.data import WATER_WORKS
    out = {}
    for node in sorted({b.get("node") for b in w.s["buildings"].values()}):
        n = sum(1 for _, b in mills(w, node) if gap(b) == "shut")
        if n:
            out[f"v:{node}"] = 1.0 - (1.0 - float(WATER_WORKS["mill"]["stop"])) ** n
    return out


def weir_trap(w, bid):
    """The weir's own traps (a set thing at its parcel, `weir`: its building), or None."""
    return next((cid for cid, c in sorted(w.s["containers"].items()) if c.get("kind") == "set" and (c.get("set") or {}).get("weir") == bid),
                None)


def _weir_trap_make(w, bid, b) -> str:
    """The weir's traps, made the first night it stands: anyone's set thing by brief 4c's rules, known to its crew."""
    from cybertron2.engine import things as TH
    cid = weir_trap(w, bid)
    if cid is not None:
        return cid
    crew = list(b.get("crew") or [])
    by = crew[0] if crew else None
    cid = w.apply("new_thing", b["node"], node=b["node"], parcel=b["parcel"], kind="set", by=by, crew=crew,
                  set={"method": "trap in water", "weir": bid, "life": 0, "base": 0.0, "set_day": w.d, "line": 1, "holds": 0})
    for n in crew:
        if n in w.s["people"] and w.s["people"][n].get("alive", True):
            TH.remember(w, n, cid, "put")
    return cid


def _catch_into(w, node, cid, kind, heads, why) -> None:
    from cybertron2.engine.data import RESOURCES
    c = w.s["containers"][cid]
    tk = (RESOURCES.get(kind) or {}).get("taken") or {}
    held = any(float(q) > 1e-9 for q in c["goods"].values())
    for item, q in sorted((tk.get("goods") or {}).items()):
        w.apply("create", node, dst=cid, item=item, qty=round(float(q) * heads, 4), why=why)
    had = list(c.get("catch") or []) if held else []
    w.apply("set_thing", node, cid=cid, field="catch", value=had + [{"kind": kind, "day": w.d, "n": int(heads)}])
    w.apply("set_thing", node, cid=cid, field="caught", value=int(c.get("caught", 0) or 0) * held + int(heads))


def _runs_night(w, m) -> dict:
    """The river's night (brief 5): each weir, from upstream, takes its share of the runs at its village into its traps, up to what
    they hold (D2-210); a trap set in a shut mill's race takes its share of a run going down; the otters rob the unwatched traps in the
    water; the river's flow wears the weirs and a spate wrecks the traps; and the runs move on (with tomorrow's cue, and the dams shut
    tonight holding a run going up as it arrives)."""
    from cybertron2.engine.data import ITEMS, WATER_WORKS
    from cybertron2.wild import runs as RU
    import copy
    st = w.s["wild"]["state"]
    if not RU.active(m):
        return {}
    st = copy.deepcopy(st)
    day = eco_day(w)
    out = {}
    nt = RU.net(m)
    for node in sorted({b.get("node") for b in w.s["buildings"].values() if b.get("node") in w.s["nodes"]}):
        g = f"v:{node}"
        if g not in nt.members:
            continue
        for bid, b in sorted(weirs(w, node), key=lambda x: (-_upstream(w, x[1]["parcel"]), x[0])):   # from upstream (D2-210)
            if not _river_parcel(w, b["parcel"]):
                continue
            cid = _weir_trap_make(w, bid, b)
            worth = {k: _food_of(k) for k in RU.runners(m.kinds)}
            held = sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0.0)) for i, q in w.s["containers"][cid]["goods"].items())
            got = RU.take_share(st, day, g, weir_share(b), room=max(0.0, weir_hold(b) - held), worth=worth)
            for k, q in sorted(got.items()):
                _catch_into(w, node, cid, k, q, "the weir")
                out.setdefault("weir", {}).setdefault(bid, {})[k] = q
        for bid, b in mills(w, node):                                     # the race (§3a.2)
            if gap(b) != "shut":
                continue
            water = mill_water(w, b)
            trap = next((cid for cid, c in sorted(w.s["containers"].items()) if c.get("kind") == "set" and c.get("parcel") == water
                         and (c.get("set") or {}).get("method") == "trap in water" and not (c.get("set") or {}).get("weir")
                         and (c.get("set") or {}).get("sprung") is None), None)
            if trap is None:
                continue
            held = sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0.0)) for i, q in w.s["containers"][trap]["goods"].items())
            got = RU.take_share(st, day, g, float(WATER_WORKS["mill"]["race"]), dirs=("down",),   # a trap's hold (D2-213)
                                room=max(0.0, float(WATER_WORKS["trap"]["hold"]) - held), worth={k: _food_of(k) for k in RU.runners(m.kinds)})
            for k, q in sorted(got.items()):
                _catch_into(w, node, trap, k, q, "the mill race")
                out.setdefault("race", {}).setdefault(bid, {})[k] = q
    out_ = _robbers(w, m, st)
    if out_:
        out["robbed"] = out_
    nodes = sorted(set(m.nodes))
    wx_today = weather(w, nodes, w.d)                                     # the river's flow tonight (D2-210), from the catchment's rain
    mem = {nd: [float((wx_today.get(nd) or {}).get("rain", 0.0))] + list((st["runs"].get("rain") or {}).get(nd) or [])
           for nd in sorted(set(nodes) | set((st["runs"].get("rain") or {})))}
    flows = {}
    for node in sorted({b.get("node") for b in w.s["buildings"].values() if b.get("node") in w.s["nodes"]} |
                       {c.get("node") for c in w.s["containers"].values() if c.get("kind") == "set"}):
        g = f"v:{node}"
        if g in nt.members:
            flows[node] = RU.flow(nt, g, mem, WATER_WORKS["weir"]["wear"]["flow_at"])
    for node, fl in sorted(flows.items()):
        for bid, b in weirs(w, node):                                     # the river wears the weirs (D2-210)
            lost = _weir_wear(w, m, bid, b, fl)
            if any(lost):
                out.setdefault("wear", {})[bid] = {"flow": fl, "lost": lost}
        wreck = float((WATER_WORKS["trap"]["wreck"]).get(fl, 0.0))
        if wreck > 0:                                                     # a spate wrecks the traps in the river (D2-211)
            for cid, c in sorted(w.s["containers"].items()):
                sp = c.get("set") or {}
                if c.get("kind") != "set" or c.get("node") != node or sp.get("method") != "trap in water" or sp.get("weir") \
                        or sp.get("sprung") is not None or not _river_parcel(w, c.get("parcel")):
                    continue
                if w.rng("trap-wreck", w.d, cid).random() < wreck:
                    for item, q in sorted(c["goods"].items()):
                        if float(q) > 1e-9:
                            w.apply("destroy", node, src=cid, item=item, qty=float(q), why="swept away in the spate")
                    w.apply("set_thing", node, cid=cid, field="catch", value=[])
                    w.apply("set_thing", node, cid=cid, field="set", value=dict(sp, sprung=w.d, wrecked=fl))
                    out.setdefault("wrecked", []).append(cid)
    if flows:
        out["flow"] = flows
    eff = RU.advance(m, st, day, wx_today, weather(w, nodes, w.d + 1), stops=_dam_stops(w, m), weather=_runs_by_weather(w))
    if any(eff.values()):
        out["moved"] = eff
    held = {p["g"]: True for p in RU.today(m, st, day + 1) if p.get("held")}
    if held:
        out["held"] = sorted(held)
    w.apply("set_wild", m.nodes[0], path=["state", "runs"], value=st["runs"])
    before = w.s["wild"]["state"]["pop"]
    for k in sorted(st["pop"]):                                            # the runners that left their areas tonight
        if st["pop"][k] != before.get(k):
            w.apply("set_wild", m.nodes[0], path=["state", "pop", k], value=st["pop"][k])
    return out


def _robbers(w, m, st) -> dict:
    """An otter at the set things in the water at night (brief 5 §4): at a village with otters about (in its home area and ring), each
    set thing in water holding a catch, unwatched tonight, is robbed at 1 - e^(-rob x otters) of `share` of its heads (at most `most`),
    leaving its sign."""
    from cybertron2.wild.kinds import ROB_SETS, TAKEN, WATER_ROBBERS
    land = w.s["wild"]["land"]
    robbers = [k for k in WATER_ROBBERS if k in st["pop"]]
    if not robbers:
        return {}
    out = {}
    watch = {pid for pid, v in (w.s["wild"].get("watch") or {}).items() if int(v.get("day", -9)) == w.d}
    for cid, c in sorted(w.s["containers"].items()):
        sp = c.get("set")
        if c.get("kind") != "set" or not sp or sp.get("method") != "trap in water" or c.get("parcel") in watch:
            continue
        caught = [x for x in (c.get("catch") or []) if any(float(q) > 1e-9 for q in c["goods"].values())]
        if not caught:
            continue
        node = c["node"]
        areas = [i for i, a in enumerate(m.ids) if land.get("home", {}).get(node) == a
                 or (land["areas"][a]["kind"] == "ring" and land["areas"][a].get("node") == node)]
        n_ot = sum(float(st["pop"][k][i]) * float(m.km2[i]) for k in robbers if k in st["pop"] for i in areas)
        if n_ot < float(ROB_SETS["least"]):
            continue
        r = w.rng("wild-rob-set", w.d, cid)
        if r.random() >= 1.0 - math.exp(-float(ROB_SETS["rob"]) * n_ot):
            continue
        heads = sum(int(x.get("n", 1)) for x in caught)
        k_ = min(int(ROB_SETS["most"]), max(1, int(round(heads * float(ROB_SETS["share"])))))
        left, gone = [], 0
        for x in caught:                                                  # the freshest first, a head at a time
            n = int(x.get("n", 1))
            t = min(n, k_ - gone)
            gone += t
            for item, q in sorted(((TAKEN.get(x["kind"]) or {}).get("goods") or {}).items()):
                have = float(w.s["containers"][cid]["goods"].get(item, 0.0))
                if have > 1e-9 and t > 0:
                    w.apply("destroy", node, src=cid, item=item, qty=round(min(have, float(q) * t), 4), why="robbed in the night")
            if n - t > 0:
                left.append(dict(x, n=n - t))
        w.apply("set_thing", node, cid=cid, field="catch", value=left)
        w.apply("set_thing", node, cid=cid, field="robbed_by", value={"day": w.d, "n": gone, "kind": robbers[0]})
        out[cid] = gone
    return out


def run_density(w, m=None, st=None) -> dict:
    """{kind: [heads a km2 by area]} of the runs at their stretches today, thickened in the water people fish (RUN `dense`)."""
    from cybertron2.wild import runs as RU
    from cybertron2.wild.kinds import RUN
    m = m if m is not None else model(w)
    st = st if st is not None else w.s["wild"]["state"]
    if not st.get("runs"):
        return {}
    return {k: [x * float(RUN["dense"]) for x in v] for k, v in RU.density(m, st, eco_day(w)).items()}


def run_take(here, mind, tech, key, units) -> tuple:
    """Fishing by hand where a run is (brief 5 §3a.2: the fish held below a dam, or a run passing): the take's rule at the run's
    density on the village's water (meetings over `units`, a fifth of a km2 a unit; each taken at the method's chance). Returns
    (food, words)."""
    from cybertron2.engine.data import ITEMS, RESOURCES
    from cybertron2.wild import methods as MT, runs as RU
    from cybertron2.wild.kinds import HUNT
    w = here._w
    if not on(w) or not (w.s.get("wild") or {}).get("state") or not _river_parcel(w, key):
        return 0.0, ""
    m = model(w)
    st = w.s["wild"]["state"]
    if not st.get("runs"):
        return 0.0, ""
    i = RU.net(m).area.get(f"v:{here.node}")
    rd = run_density(w, m, st)
    if i is None or not any(v[i] > 0 for v in rd.values()):
        return 0.0, ""
    import copy
    st2 = {"runs": copy.deepcopy(st["runs"])}
    rng = here.rng("wild-run-take", here.day, here.name, tech)
    ground = min(float(m.km2[i]), 0.2 * float(units))
    skill = float(((w.s["know"].get(here.name) or {}).get(tech) or {}).get("skill", 1.0))
    got = {}
    for k in sorted(rd):
        tk = (RESOURCES.get(k) or {}).get("taken") or {}
        lam = rd[k][i] * float(tk.get("detect", 0.2)) * ground * float(HUNT["meet"]) * MT.factor(mind, k)
        for _ in range(_poisson(rng, lam, int(HUNT["most"]))):
            if rng.random() >= chance(float(HUNT["take_k"]) * skill * (1 - float(tk.get("flee", 0.5))) * MT.factor(mind, k)):
                continue
            if not RU.take_one(m, st2, eco_day(w), k, i):
                break
            got[k] = got.get(k, 0) + 1
    if not got:
        return 0.0, ""
    food = 0.0
    for k, n in sorted(got.items()):
        for item, q in sorted((((RESOURCES.get(k) or {}).get("taken") or {}).get("goods") or {}).items()):
            here.apply("create", dst=here.hands, item=item, qty=round(float(q) * n, 4), why=tech)
            food += float(q) * n * float((ITEMS.get(item) or {}).get("food", 0.0))
        MT.raise_familiar(here, mind, k, MT.FAMILIAR["take"], tech)
    here.apply("set_wild", path=["state", "runs", "pulses"], value=st2["runs"]["pulses"])
    words = " and ".join(f"{n} {k if n == 1 else _plural_of(k)}" for k, n in sorted(got.items()))
    return food, f" From the run in the water you took {words}."


def _plural_of(k) -> str:
    from cybertron2.engine import things as TH
    return TH._plural(k)
