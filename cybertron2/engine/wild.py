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
    for d in range(years * Y):                                            # the history before the run, ending on the run's season
        EC.step(m, st, k0 + d, weather(w, sorted(set(m.nodes)), off + d), draws(w, k0 + d, "history"))
    st["day"] = -1
    st["mast"]["years"] = {}                                              # the trees' budget carries over; the run's years are its own
    w.s["wild"]["state"] = st
    _seed_plants(w)                                                       # the wild plant kinds in place of `plants` (D2-200)
    from cybertron2.wild.kinds import SKILL_CARRY
    for name, k in w.s["know"].items():                                   # the old hunt's practice carries to the wild ones
        for old, new in SKILL_CARRY.items():
            if old in k:
                for t in new:
                    k.setdefault(t, dict(k[old]))
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
    eff = EC.step(m, st, eco_day(w), weather(w, sorted(set(m.nodes)), w.d), draws(w, eco_day(w)), scale=scale)
    place = m.nodes[0]
    w.apply("set_wild", place, path=["state"], value=st)
    out = {"mast": st.get("mast_now"), "crops": {}, "stores": {}}
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
            if share > 1e-6:
                lost = (_crops if food == "crops" else _stores)(w, node, share)
                if lost > 1e-6:
                    out[food][node] = round(lost, 4)
    eaten = {nd: dict(v, day=w.d) for nd, v in _shares(out, real, m).items()}
    if eaten or (w.s["wild"].get("eaten") or {}):
        w.apply("set_wild", place, path=["eaten"], value=eaten)
    out["loads"] = _loads(w, m, st)
    out["sick"] = _herds_sick(w, m, st)
    out["groups"] = _groups(w, m, st)
    out["near"] = {gid: {"n": g["n"], "pos": g["pos"], "what": g.get("what")} for gid, g in sorted((w.s["wild"].get("groups") or {}).items())}
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
                for h in spec.get("harm") or []:
                    share = min(0.5, float(h["share"]) * max(0.0, L - float(h["over"])))
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
    here.apply("set_wild", path=["guard", pid], value={"load": y["load"], "cut": float(y["cut"]), "until": here.day + int(y["days"]) - 1,
                                                        "by": here.name})
    for k, share in sorted((y.get("thin") or {}).items()):              # it kills some outright: the load on the land falls
        _thin(here, pid, k, float(share))
    return y.get("done", "You worked over {place}.").format(place=place_name)


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
    fields = [p for p in here.parcels().values() if p["cover"] == "field"]
    part = float(here.parcels()[pid]["size"]) / max(1.0, sum(float(p["size"]) for p in fields))
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
                row["knows"] = f"expert:{'hunt' if group == 'hunt' else tech}"
            rows.append((row, n_.get("find")))

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
    return []


def _count(m, st, kind, land, node, ring_i, gather):
    import numpy as np
    idx = [ring_i] if gather != "far" else [i for i in _reach(m, land, node, "far") if land["areas"][m.ids[i]]["kind"] != "home"]
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


def _fenced(w, pid, np_, rng) -> bool:
    """A fence round the parcel keeps the group out by its level (FENCES' through, as for herds), a leaping kind more often over."""
    from cybertron2.engine.data import FENCES
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
        lost = 0.0
        for hd, _, c in FM.standing(w.s["parcels"][tgt]):
            q = round(float(c.get("left", 0.0)) * share, 4)
            if c.get("area_left", 0) > 1e-6 and q > 1e-9:
                w.apply("draw", node, parcel=tgt, key="crop", qty=q, **({"holder": hd} if hd is not None else {}))
                lost += q
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
    if what in ("items", "hens"):
        b = w.s["buildings"][tgt]
        if t.get("door", False):
            shut = int(((w.s["wild"].get("shut") or {}).get(tgt) or {}).get("day", -9)) == w.d
            if rng.random() >= (0.02 if shut else 0.6):                       # shut in, a door is seldom left open; left, often
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


def _did(res) -> bool:
    return res.get("lost", 0) > 1e-6 or bool(res.get("killed")) or res.get("took", 0) > 0 or res.get("stripped", 0) > 1e-6


def _groups(w, m, st) -> dict:
    """Whole-counted kinds with a group near a village: condense from the land around (the ring, or for a pack the land beyond),
    set out on a drive from the area's hunger and the kind's conditions (frost, snow, the mast, the rut: kinds.WHEN), leave traces on
    the way, raid their target (a field, a herd, a store, a parcel's stock) unless a fence keeps them out, a watch at the gap they use
    meets them, or a watch or a dog turns them by the kind's answer to scares (D2-198), and remember."""
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
    for node, ri in sorted(rings.items()):
        for kind in m.names:
            np_ = _near(kind)
            spec = m.kinds[kind]
            if not np_ or spec.get("count") != "whole":
                continue
            gid = f"{kind}@{node}"
            ef = effects(w, node, kind, m, st, ri)
            count = _count(m, st, kind, land, node, ri, np_.get("gather"))
            lo, hi = (spec.get("group") or {}).get("size", [2, 10])
            lo = 1 if ef["lone"] else lo
            if count < lo:
                groups.pop(gid, None)
                continue
            g = groups.get(gid) or {"kind": kind, "node": node, "pos": "home", "t": -1, "raid": -1, "found": -99, "habit": {},
                                    "wary": -1, "rest": -1, "target": None, "what": None}
            g["n"] = int(np.clip(round((0.3 if np_.get("gather") != "far" else 0.6) * count), lo, hi))
            groups[gid] = g
            rng = w.rng("wild-group", w.d, gid)
            if np_["answer"]["type"] == "habituate":
                dec = float(np_["answer"]["decay"])
                g["habit"] = {k: max(0.0, v - dec) for k, v in g["habit"].items() if v > dec}
            rows = [t for t in list(np_["targets"]) + ef["targets"] if _season_window(w, w.d, t["seasons"])]
            attr = max([t["attr"] for t in rows] or [0.0])
            hunger = 1.0 - float(np.asarray(st["cond"][kind])[ri])
            if g["pos"] == "ready" and w.d >= g["raid"]:
                g["pos"] = "home"
                t = dict(g.get("trow") or {"what": g.get("what") or "crop"})
                t.setdefault("what", "crop")
                tg = dict(_targets(w, node, t))
                tgt = g["target"] if g["target"] in tg else (next(iter(tg)) if tg else None)
                if tgt is None:
                    continue
                parcel = tg[tgt]
                gap = _edge_of(w, parcel)
                seen = watch.get(parcel)
                scare = seen.get("scare") if seen else None
                if scare is None and t.get("what") == "herd" and w.s["herds"][tgt].get("watched") == w.d:
                    scare = "herding"                                          # people with the herd: a watch of a kind
                if scare is None and t.get("what") in ("items", "hens") and (w.s["buildings"][tgt].get("fittings") or {}).get("dog"):
                    scare = "dog"
                if gap != parcel and watch.get(gap):                           # met at the gap they come through (L3)
                    gw = watch[gap]
                    g["rest"] = w.d + int(np_["answer"].get("rest", np_["answer"].get("off_days", 2)))
                    if rng.random() < 0.3:
                        g["wary"], g["habit"] = w.d + int(np_["wary_after_harm"]), {}
                    _trace(traces, gap, kind, "turned", w.d, g["n"], gw.get("scare"), gw.get("by"))
                    out[gid] = {"at": tgt, "what": t.get("what"), "turned": True, "scare": gw.get("scare"), "gap": True}
                    continue
                if t.get("what") in ("crop", "herd", "res") and _fenced(w, parcel, np_, rng):
                    _trace(traces, parcel, kind, "turned", w.d, g["n"], "fence", None)
                    out[gid] = {"at": tgt, "what": t.get("what"), "turned": True, "scare": "fence"}
                    continue
                if scare is not None:
                    turned, harmed = _answer(rng, g, np_, scare, ef["bold"])
                    if harmed:
                        g["wary"], g["habit"] = w.d + int(np_["wary_after_harm"]), {}
                    if turned:
                        g["rest"] = w.d + int(np_["answer"].get("rest", np_["answer"].get("off_days", 2)))
                        _trace(traces, parcel, kind, "turned", w.d, g["n"], scare, (seen or {}).get("by"))
                        out[gid] = {"at": tgt, "what": t.get("what"), "turned": True, "scare": scare}
                        continue
                res = _raid(w, g, np_, kind, t, tgt, parcel, scare, rng)
                g["found"] = w.d
                tr = ("raid" if _did(res) else "tried") + (f":{t['sign']}" if t.get("sign") and _did(res) else "")
                _trace(traces, parcel, kind, tr, w.d, g["n"], scare, (seen or {}).get("by"))
                out[gid] = {"at": tgt, "what": t.get("what"), "turned": False, "scare": scare, **res}
            elif g["pos"] == "edge":
                if rng.random() < float(np_["lead_sign_p"]):
                    _trace(traces, _edge_of(w, g.get("parcel") or g.get("target")), kind, "edge", w.d, g["n"])
                if w.d - g["t"] >= int(np_["lead_nights"]) - 1:
                    g["pos"], g["raid"] = "ready", w.d + 1
            elif g["pos"] == "home" and w.d >= g["rest"] and w.d >= g["wary"] and attr > 0:
                trow = max(rows, key=lambda t: t["attr"])
                tg = _targets(w, node, trow)
                if not tg:
                    continue
                p = min(1.0, attr * (float(np_["drive"]["base"]) + float(np_["drive"]["hunger"]) * hunger) * ef["drive"])
                knows = 1 <= w.d - int(g["found"]) <= int(np_["memory_days"])
                if knows:
                    p = max(p, float(np_["return_p"]) * attr)
                if rng.random() < p:
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


def take(here, mind, tech, key, place_name, out, m_skill, y, a) -> tuple:
    """A hunt: what the hunter comes on is drawn from the kinds in the areas the range covers, by their numbers, how easy each is to
    find and what this way of hunting takes; looking for one thing makes it likelier and the rest less likely, never impossible, so a
    deer stalker may come on the sounder. What is found may flee, be taken (off its area's count, and its group's), or hurt the
    hunter (D2-193). Returns (food taken, a line for the hunter, what they noticed on the way)."""
    from cybertron2.engine.data import RESOURCES, TECHNIQUES
    import numpy as np
    w = here._w
    if not on(w) or not (w.s.get("wild") or {}).get("state"):
        return 0.0, f"You found nothing to take at {place_name}.", ""
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
    ring_i = next((i for i in areas if land["areas"][m.ids[i]]["kind"] == "ring"), areas[0] if areas else None)
    efx = {k: effects(w, here.node, k, m, st, ring_i) for k in sorted(takes)}
    when = 1.0
    for row in (y.get("when") or []):                                     # a way of taking that pays on its nights (an eel night)
        if cond(w, here.node, row.get("if"), None, m, st, ring_i):
            when *= float(row.get("x", 1.0))
    pressure = {k: [float(x) for x in ((st.get("pressure") or {}).get(k) or [0.0] * m.n)] for k in takes if k in st["pop"]}
    pressure0 = {k: list(v) for k, v in pressure.items()}
    from cybertron2.wild.kinds import HUNTED
    crewn = 1 + sum(1 for e in here.events() if e.get("kind") == "work" and e.get("tech") == tech and e.get("actor") != here.name
                    and f"parcel:{key}" in (e.get("about") or []))
    for kk in pressure:                                                   # the hunt disturbs what it hunts (the hunted wood)
        for ii in areas:
            pressure[kk][ii] = round(pressure[kk][ii] + float(HUNTED["hunt"]) * (1 + float(HUNTED["crew"]) * (crewn - 1)), 3)
    for k, tw in sorted(takes.items()):
        if k not in st["pop"]:
            continue
        tk = (RESOURCES.get(k) or {}).get("taken") or {}
        focus = (3.0 if k in want else 0.4) if want else 1.0
        for i in areas:
            count = float(st["pop"][k][i]) * float(m.km2[i])
            wgt = count * float(tk.get("detect", 0.2)) * efx[k]["detect"] / (1.0 + 0.5 * min(4.0, pressure0[k][i])) * float(tw) * focus * when \
                / (1.0 + 0.3 * areas.index(i))
            if wgt > 0 and count >= 1.0:                                     # one met is a whole one
                cand.append((k, i, wgt))
    total = sum(c[2] for c in cand)
    effort = float(TECHNIQUES[tech]["units"]) / 2.0
    looked = f" looking for {a.get('looking for')}" if want else ""
    where = {"near": place_name, "the wood around": f"the woods and wastes around {place_name}", "far": "the wild land far beyond"}[rng_word]
    seen = _notices(here, mind, m, st, areas, key, effort)
    tail = (" On the way you saw " + "; and ".join(seen) + ".") if seen else ""
    if total <= 0 or rng.random() >= 1 - math.exp(-0.03 * total * effort):
        _put_pressure(here, pressure)
        return 0.0, f"You hunted {where}{looked} and came on nothing.", tail
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
    dmul = efx[k]["danger"]
    if danger and rng.random() < min(0.95, float(danger["wound"]) * dmul / crew):
        _put_pressure(here, pressure)
        if rng.random() < min(0.5, float(danger.get("kill", 0.0)) * dmul / crew):
            here.apply("die", person=here.name, cause=f"killed by {_a(k)} while hunting")
            return 0.0, f"Hunting {where}, {found}; it turned on you.", ""
        here.apply("harm", person=here.name, wounded=True)
        hurt = " It turned on you and you were hurt before it broke away."
        return 0.0, f"Hunting {where}, {found}.{hurt}", tail
    armed = here.weapon()
    wpn = float(TECHNIQUES[tech]["weapon"]["armed" if armed else "none"])
    flee = min(0.95, float(tk.get("flee", 0.5)) * efx[k]["flee"])
    p_take = float(np.clip(0.55 * m_skill * wpn * (1 - flee) * (1 + 0.25 * (crew - 1)), 0, 0.95))
    if rng.random() >= p_take:
        _put_pressure(here, pressure)
        if armed and tk.get("danger") and rng.random() < 0.3:              # hit but not down: a wounded beast lying up
            here.apply("set_wild", path=["state", "wounded", f"{k}@{i}"], value=here.day)
            return 0.0, f"Hunting {where}, {found}; you hit it, but it broke away into the thicket, bleeding.", tail
        return 0.0, f"Hunting {where}, {found}, but it got away.", tail
    pressure[k][i] = round(pressure[k][i] + float(HUNTED["kill"]), 3)
    _put_pressure(here, pressure)
    pop = [float(x) for x in st["pop"][k]]
    pop[i] = max(0.0, pop[i] - 1.0 / float(m.km2[i]))                      # one head off its area's count
    for kk, lit in sorted((y.get("litter") or {}).items()):              # young taken with it (cubs at the earth in spring)
        if kk == k and cond(w, here.node, lit.get("if"), k, m, st, ring_i):
            pop[i] = max(0.0, pop[i] - float(lit["n"]) / float(m.km2[i]))
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
    if rng_word == "near" and key in here.parcels():                       # gutted where it fell: the kill's signs (signs.HUNTED)
        rec = here.parcels()[key].get("hunted") or {}
        kills = list(rec.get("kills") or []) if rec.get("day") == here.day else []
        kills.append({"by": here.name, "meat": food, "hide": "hide" in (tk.get("goods") or {}), "kind": k})
        here.apply("set", ref=("parcel", key), field="hunted", value={"day": here.day, "kills": kills})
    return food, f"Hunting {where}, {found} and took it: " + ", ".join(f"{q:g} {it}" for it, q in sorted((tk.get('goods') or {}).items())) + ".", tail


NOTICE_MOST = 2


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
        for r in rs:
            row = dict(when=lambda x: True, own=float(r["own"]) * pres[k], sense=r["sense"], text=lambda x, t=r["text"]: t, kind=k)
            if r["read"] in ("lay", "knows"):
                row[r["read"]] = "hunt"
            rows.append(row)

    def rule(row):
        sense = row.get("sense", "sight")
        vis = EV.visibility(here._w, here.node, parcel=key, sense=sense, cover=par.get("cover"))
        return float(row["own"]) * vis * (eye if sense in NOTICING["eye_senses"] else 1.0)
    got = SG.roll(rows, SimpleNamespace(), rng, know=PC.practised(mind), rule=rule)[:NOTICE_MOST]
    if got and key in here.parcels():
        PC.remember_land(mind, here.day, key, "the wild", "; ".join(got), "hunted")
    return got


def _put_pressure(here, pressure) -> None:
    w = here._w
    old = (w.s["wild"]["state"].get("pressure") or {})
    for k, v in sorted(pressure.items()):
        if v != old.get(k):
            here.apply("set_wild", path=["state", "pressure", k], value=v)


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
        from cybertron2.wild.kinds import STORE_KEEP
        keep = 1.0
        for f_, x in STORE_KEEP.items():                                    # a terrier, a raised granary floor
            if (b.get("fittings") or {}).get(f_):
                keep *= float(x)
        for item, q in sorted((w.s["containers"].get(cid, {}).get("goods") or {}).items()):
            if item in DRY_STORES and q > 0:
                take = round(float(q) * share * keep, 4)
                if take > 1e-6:
                    w.apply("destroy", node, src=cid, item=item, qty=take, why="eaten in store by wild kinds")
                    total += take
    return total
