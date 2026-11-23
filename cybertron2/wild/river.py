"""The river's senses (u8_signs.md; D2-265, D2-269, D2-325): the feature unit of the river's signs (D2-244, the water package). Its
data (`BANDS`, the rows `DAWN`, `DAY`, `FLOW`, `SLACK`, `ICE`, `OTTER`, the carried catch `CARRIED`), its record (`record`: the
river's night at each village, written by wild._runs_night, as `wild.eaten` is: river_signs §1), its reads (`river_now`, `band`,
`year_basis`, `flow_today`) and its emitters: `dawn_events` (the morning's cues, written as dawn events before the day's acts: the
second of the four leads) and `day_signs` (the run itself, the flow, the slackening, the ice, the otters and the fen, rolled in the
evening: the third), and `carried` (the catch carried home: the fourth, a person's body and load). Lore (the first lead) is U9's
seeded lines (founders.py).

Every row reads a state value and names the threshold that fires it (guides/senses.md rule 1); no row asserts a moon, a flood over
the land or a gull; the chance of each is the one noticing rule's (D4-53, D4-75: `own`, sense, reach, night; never `p`); no row
directs an act (D2-269). Rungs (u8 §0): anyone; one who fishes (`knows: "fish"`: any water craft from a rough idea up, D2-325;
perceive.practised); the expert (`expert:fish`); the elder; the weir's crew.
"""
from __future__ import annotations

from types import SimpleNamespace

BANDS = ((0.02, "trickle"), (0.08, "running"), (0.20, "thick"))      # u8 §1: a share of the station's year of that run; above, a glut
ORDER = ("none", "trickle", "running", "thick", "glut")
CARRIED_KG = 5.0                                                     # u8 basis row: the carried catch, 5 kg or more of fresh fish or meat
CARRIED_FULL = 10.0                                                  # "as much as they can carry" (basis §5: 10 kg on foot)
# the crafts of the water (D2-325: any of them from a rough idea up reads the fishers' signs); a basic one only when practised
WATER_CRAFTS = ("trap in water", "wicker trap", "gill net", "gill nets", "set line", "set lines", "angle", "fish by hand", "weir",
                "dip net", "hand line", "fishing rod")


def at_least(b, want) -> bool:
    return ORDER.index(b or "none") >= ORDER.index(want)


def band(n, basis) -> str:
    """The band of a night's heads against the station's year (u8 §1)."""
    if n < 1.0 or basis <= 1e-9:
        return "none" if n < 1.0 else "glut"
    share = float(n) / float(basis)
    for bound, name in BANDS:
        if share < bound:
            return name
    return "glut"


def year_basis(m, st, kind, g, day) -> float:
    """The station's year of a run (u8 §1): last year's tally here; in the first year, this year's tally so far, what is still to
    start upstream of it (the eels' quota by area, the salmon's dues) and what is on the way."""
    from cybertron2.wild import runs as RU
    R = (st.get("runs") or {})
    yr = int(day) // int(m.Y)
    ty = ((R.get("tally") or {}).get(kind) or {}).get(g) or {}
    last = float(ty.get(str(yr - 1), 0.0))
    if last >= 5.0:
        return last
    nt = RU.net(m)
    this = float(ty.get(str(yr), 0.0))
    from cybertron2.wild.kinds import RUNS
    r = RUNS.get(kind) or {}
    left = 0.0
    if r.get("dir") == "down":
        q = (R.get("quota") or {}).get(kind) or {}
        for g2, areas in nt.members.items():
            x = g2
            seen = set()
            while x is not None and x not in seen:
                if x == g:
                    left += sum(float(q.get(a, 0.0)) for a in areas)
                    break
                seen.add(x)
                x = nt.below.get(x)
    else:
        for dest, n in ((R.get("due") or {}).get(kind) or {}).items():
            if g in nt.path_up(dest):
                left += float(n)
    way = sum(float(p["n"]) for p in R.get("pulses") or [] if p["k"] == kind and int(p["d"]) >= int(day))
    return this + left + way


def flow_today(w, node) -> str | None:
    """The river's flow class tonight at a village (u8 §1, `river_now`): from the catchment's rain memory and the day's own weather,
    which is drawn before the day starts, as the night reads it (wild._runs_night), so a sign and a wreck cannot disagree."""
    from cybertron2.engine import wild as WL
    from cybertron2.engine.data import WATER_WORKS
    from cybertron2.wild import runs as RU
    st = (w.s.get("wild") or {}).get("state") or {}
    if not st.get("runs"):
        return None
    m = WL.model(w)
    nt = RU.net(m)
    g = f"v:{node}"
    if g not in nt.members:
        return None
    nodes = sorted(set(m.nodes))
    wx = WL.weather(w, nodes, w.d)
    mem = {nd: [float((wx.get(nd) or {}).get("rain", 0.0))] + list((st["runs"].get("rain") or {}).get(nd) or [])
           for nd in sorted(set(nodes) | set((st["runs"].get("rain") or {})))}
    return RU.flow(nt, g, mem, WATER_WORKS["weir"]["wear"]["flow_at"])


def river_now(w, node) -> dict:
    """The river's record at a village (u8 §1): last night's, as written by the river's night; {} where none."""
    return dict((((w.s.get("wild") or {}).get("river") or {}).get(node)) or {})


def passing(m, st, node, day) -> dict:
    """{kind: heads} passing a village's stretch on an ecology day (the pulses there, before any take)."""
    from cybertron2.wild import runs as RU
    g = f"v:{node}"
    out = {}
    for p in RU.today(m, st, day):
        if p["g"] == g and not p.get("held"):
            out[p["k"]] = out.get(p["k"], 0.0) + float(p["n"])
    return out


def record(w, m, st, day, before, flows, out) -> None:
    """The river's night record at each village on a river (u8 §1), written at the end of the night: the flow (and last night's), the
    heads that passed and their band against the station's year, the year's best night here, what each gear took and what the weir
    turned away, the ice and what it held, and the year's first and last nights."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import runs as RU, water as WT
    from cybertron2.wild.kinds import RUNS
    nt = RU.net(m)
    old = (w.s["wild"].get("river") or {})
    new = {}
    for node in sorted({p_["node"] for p_ in w.s["parcels"].values()}):
        g = f"v:{node}"
        if g not in nt.members:
            continue
        was = old.get(node) or {}
        fl = flows.get(node) or flow_today(w, node) or "normal"
        passed = {k: round(n, 2) for k, n in sorted((before.get(node) or {}).items()) if n >= 1.0}
        bands = {k: band(n, year_basis(m, st, k, g, day)) for k, n in passed.items()}
        yr = int(day) // int(m.Y)
        best = {k: v for k, v in (was.get("best") or {}).items() if int(was.get("year", yr)) == yr}
        for k, n in passed.items():
            best[k] = max(float(best.get(k, 0.0)), n)
        firsts = [k for k in passed if float(((was.get("best") or {}) if int(was.get("year", yr)) == yr else {}).get(k, 0.0)) < 1.0]
        taken = {}
        for kind, rows in out.items():
            if kind in ("weir", "trap", "race"):
                for gid, got in rows.items():
                    c = w.s["buildings"].get(gid) or w.s["containers"].get(gid) or {}
                    if c.get("node") == node:
                        taken[str(gid)] = {k: int(q) for k, q in got.items()}
        turned = {}
        for bid, b in WL.weirs(w, node):                                    # what the weir's traps had no room for (u8 §3.4)
            if WL.gap(b) != "shut":
                continue
            share = float(WL.weir_share(b))
            want = sum(float(n) * share * float(WL._kg_of(k)) for k, n in passed.items())
            got = sum(float(q) * float(WL._kg_of(k)) for k, q in (taken.get(bid) or {}).items())
            if want - got > 1.0:
                turned[bid] = round(want - got, 1)
        ended = [k for k, r in sorted(RUNS.items()) if RU.ended(m, day + 1, r["seasons"])]
        new[node] = {"day": int(w.d), "year": yr, "flow": fl, "flow_was": was.get("flow", fl), "passed": passed, "band": bands,
                     "best": {k: round(v, 2) for k, v in best.items()}, "taken": taken, "turned": turned,
                     "ice": WT.stretch_ice(w, node), "held": sorted(k for k in passed if (out.get("iced") or {}).get(g)),
                     "first": sorted(firsts), "last": ended,
                     "rain": float((WL.weather(w, sorted(set(m.nodes)), w.d).get(node) or {}).get("rain", 0.0))}
    if new != old:
        w.apply("set_wild", m.nodes[0], path=["river"], value=new)


# ---------------------------------------------------------------------- the rows (u8 §2 to §4; the chances: §6, checked in the tests)
# `own` was set by u8 §6's hand reckoning (presence 0.5 on a worked parcel, 0.3 next door) and moved until the rule lands there
# (guides/senses.md item 4): the engine's presence is about 1 on a worked parcel and 0.125 next door for a row seen "around", so the
# around rows carry about 2.4 times u8's own (next door lands on u8's figure; on the parcel they are near certain), and the roar,
# the night's splashing and the eels on the fen grass were raised to land from the Street (stage 4 report §3).
def _row(read, sense, own, text, reach=None, night=False, when=None, who=None):
    return {"read": read, "sense": sense, "own": own, "text": text, "reach": reach, "night": night, "when": when, "who": who}


# the dawn cue (u8 §2.2): written as dawn events for the morning, read from the houses by the rule; spot "place" is everyone at the
# place (as the weather lines are), "water" the village's water parcel, "fen" the fen beside it
DAWN = {
    "window": _row(("expert", "elder"), "sight", 0.35, "the nights drawing in: the eels will be moving soon"),
    "rain": _row("all", "sight", 0.4, "the first heavy rain after the dry weeks"),
    "eel_night_rain": _row("expert", "sight", 0.3, "the first heavy rain of the autumn after the dry weeks, and the night coming on dark: an eel night"),
    "eel_night_set": _row("expert", "sight", 0.3, "the dark nights of the autumn come, and the river full: an eel night"),
    "herons": _row("all", "sight", 2.5, "herons flying down to {water} from first light, one after another"),
    "roar": _row("all", "sound", 3.3, "the roar of {water} in spate, heard from the houses"),
    "spate_traps": _row("fish", "sound", 3.3, "{water} roaring in spate: wicker traps in its main stream are torn away in water like this, {share}"),
    "splash": _row("all", "sound", 2.7, "heavy splashing from {water} all night, fish throwing themselves at the shallows", night=True),
    "fen_eels": _row("all", "sight", 2.4, "eels on the wet grass of {fen} at first light, working their way through it toward {water}"),
    "upriver": _row("expert", "sound", 0.8, "{water} louder this morning than the rain here explains: it is raining hard upriver"),
    "gap_spate": _row("crew", "sight", 1.2, "the gap shut in a spate: the river is piling against the wattle"),
    "fen_ice": _row("all", "sight", 1.0, "{fen}'s pools skinned with ice, the reeds stiff with rime"),
    "edge_ice": _row("all", "sight", 1.2, "ice along the edges of {water}, the main stream still running black between"),
    "frozen": _row("all", "sight", 2.0, "{water} frozen over from bank to bank"),
    "thaw_sight": _row("all", "sight", 1.5, "the ice going out of {water} in grinding plates"),
    "thaw_sound": _row("all", "sound", 1.5, "the ice going out of {water} in grinding plates"),
    "thaw_weir": _row("crew", "sight", 0.8, "the ice going out: it will tear at the weir's stakes"),
}
# the run itself, the flow, the slackening, the otters and the fen (u8 §2.3, §3): rolled in the evening at the water
DAY = [
    _row("all", "sight", 2.9, "dark eels moving in the slack water under the banks of {water}, all one way, downstream", "around",
         when=lambda x: x.eel == "running"),
    _row("all", "sight", 3.8, "the shallows of {water} thick with eels, sliding over one another, all going down", "around",
         when=lambda x: x.eel == "thick"),
    _row("all", "sight", 4.8, "eels everywhere in {water}, in the weed, under the banks, against the stakes: more than any hands could take",
         "around", when=lambda x: x.eel == "glut"),
    _row("all", "sight", 0.6, "the water at {water} alive with eels in the dark, all going downstream", night=True,
         when=lambda x: at_least(x.eel, "running")),
    _row("all", "touch", 2.0, "eels against your legs in the water, cold and strong, all going the one way", who="doer",
         when=lambda x: at_least(x.eel, "running")),
    _row("all", "smell", 0.8, "a sweetish smell of fish and mud off {water}", when=lambda x: at_least(x.eel, "thick") or at_least(x.salmon, "thick")),
    _row("all", "sight", 3.0, "herons standing all along {water}, more together than you have seen, still as posts",
         when=lambda x: x.heronry and (at_least(x.eel, "thick") or at_least(x.salmon, "thick"))),
    _row("fish", "sight", 0.9, "an eel run in {water}: every trap in it takes a few tonight", "near", when=lambda x: x.eel == "running"),
    _row("fish", "sight", 0.9, "a heavy run in {water}: the traps take what they meet of it, and most of it goes past", "near",
         when=lambda x: at_least(x.eel, "thick")),
    _row("expert", "sight", 0.7, "a run like this is most of a year's eels in a few nights", "near", when=lambda x: x.eel == "glut"),
    _row("all", "sight", 0.9, "salmon going up through {water}, leaping at the shallows", when=lambda x: x.salmon_n >= 3),
    _row("all", "sight", 3.8, "salmon lying close in the pool below the shallows of {water}, their backs out of the water", "around",
         when=lambda x: at_least(x.salmon, "thick")),
    _row("expert", "sight", 0.6, "salmon come up behind a spate and lie in the pools: a shut weir takes them; hands and nets seldom do", "near",
         when=lambda x: x.salmon_n >= 1 and x.was in ("spate", "flood") and x.flow not in ("spate", "flood")),
    _row("all", "sight", 1.0, "lampreys on the stones of the shallows, clinging by their mouths against the current",
         when=lambda x: x.lamprey_n >= 3),
    _row("all", "sight", 3.6, "the first silver eels of the year in {water}, fat and dark-backed, going down", "around",
         when=lambda x: "eel" in x.first),
    # the flow (u8 §3.1; replacing the sky's two river rows)
    _row("all", "sight", 0.8, "{water} low and clear, stones showing at the edges and weed trailing in the current",
         when=lambda x: x.flow == "low" and x.was != "low"),
    _row("expert", "sight", 0.6, "the river too low and clear for the eels to move: they wait for rain", "near",
         when=lambda x: x.flow == "low" and x.eel_window and x.weathered),
    _row("all", "sight", 2.9, "{water} up and coloured, reed and sticks coming down on it", "around", when=lambda x: x.flow == "high" and x.was in ("low", "normal")),
    _row("all", "sight", 2.0, "{water} in spate, brown and roaring, tearing at its banks", when=lambda x: x.flow == "spate"),
    _row("all", "sight", 2.5, "{water} in flood, the whole width of it moving, whole branches turning in it", when=lambda x: x.flow == "flood"),
    _row("all", "sound", 3.3, "the roar of {water} in spate, heard from the houses", when=lambda x: x.flow in ("spate", "flood")),
    _row("all", "touch", 2.0, "the current drags at your legs: you can barely keep your feet in it", who="doer",
         when=lambda x: x.flow in ("high", "spate", "flood")),
    _row("all", "sight", 2.4, "{water} dropping and clearing, wrack and torn reed left high along its banks", "around",
         when=lambda x: x.was in ("spate", "flood") and x.flow not in ("spate", "flood")),
    _row("fish", "sight", 0.7, "{water} falling and clearing: traps in its main stream stand in water like this", "near",
         when=lambda x: x.was in ("spate", "flood") and x.flow not in ("spate", "flood")),
    # a run slackening and ending (u8 §3.2)
    _row("fish", "sight", 0.8, "fewer eels each night in {water} now: the run is passing", "near",
         when=lambda x: x.eel_n >= 1 and x.eel_best > 0 and x.eel_n < 0.5 * x.eel_best and x.eel_window),
    _row("fish", "sight", 0.8, "the eel run is over at {water} for this year", "near", when=lambda x: "eel" in x.ended),
    # otters, the weir, the fen, the resident fish (u8 §3.4)
    _row("all", "sight", 0.6, "otter tracks in the mud below the bank of {water}, webbed, with the drag of a tail", "near",
         when=lambda x: x.otters and (x.traps or x.eel_n + x.salmon_n >= 1)),
    _row("all", "sight", 2.4, "an otter rolling and diving in {water} in broad day, eating as it swims", "around",
         when=lambda x: x.otters and at_least(x.eel, "thick")),
    _row("fish", "sight", 0.8, "otters working this stretch: they go to traps with fish in them", "near",
         when=lambda x: x.otters and (x.traps or x.eel_n + x.salmon_n >= 1)),
    _row("all", "sight", 2.9, "scales and torn weed piled against the weir's wattle: more came down in the night than its traps would hold",
         "around", when=lambda x: x.turned),
    _row("all", "sight", 1.0, "the fen's dykes brim but lie still while {water} tears past", when=lambda x: x.fen and x.flow in ("spate", "flood")),
    _row("fish", "sight", 0.7, "traps in the fen's dykes stand when the river tears the rest away", "near",
         when=lambda x: x.fen and x.flow in ("spate", "flood")),
    _row("fish", "sight", 0.8, "few fish of {water}'s own, but the run going through", "near",
         when=lambda x: x.eel_n + x.salmon_n + x.lamprey_n >= 3 and x.resident is not None and x.resident < 0.35),
]
CARRIED = {"fish": ("{who} came up from {water} with their creel full of fresh fish", "{who} came up from {water} with a good load of fresh fish",
                    "{who} came up from {water} with as much fresh fish as they can carry"),
           "meat": (None, "{who} came in from {place} with a good load of fresh meat", "{who} came in from {place} with as much fresh meat as they can carry")}
FRESH_FISH = ("fish",)
FRESH_MEAT = ("meat", "venison", "game")


def _knows(read):
    if read in ("all", None):
        return {}
    if read == "fish":
        return {"knows": "fish"}
    if read == "expert":
        return {"knows": "expert:fish"}
    if read == "elder":
        return {"knows": "elder"}
    if read == "crew":
        return {"knows": "weir"}
    return {}


def _places(w, node):
    """The village's water parcel on the river (the largest), and the fen beside it, if any."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import water as WT
    ps = [pid for pid, p in sorted(w.s["parcels"].items()) if p["node"] == node]
    water = sorted((pid for pid in ps if WL._river_parcel(w, pid)), key=lambda q: (-int(w.s["parcels"][q].get("size", 1)), q))
    fen = next((pid for pid in ps if w.s["parcels"][pid]["cover"] == "fen" and WT.run_reach(w, pid) > 0), None)
    return (water[0] if water else None), fen


def _heronry(w, node) -> bool:
    return any(s.get("kind") == "heronry" and s.get("node") == node and s.get("gone") is None
               for s in ((w.s.get("wild") or {}).get("sites") or {}).values())


def _window_near(m, day, days=2) -> bool:
    from cybertron2.wild import runs as RU
    from cybertron2.wild.kinds import RUNS
    r = RUNS["eel"]
    now = RU._window(m, day, r["seasons"])[0]
    return not now and any(RU._window(m, day + k, r["seasons"])[0] for k in range(1, days + 1))


def _in_window(m, day, kind="eel") -> bool:
    from cybertron2.wild import runs as RU
    from cybertron2.wild.kinds import RUNS
    return bool(RU._window(m, day, RUNS[kind]["seasons"])[0])


def _fishers_with_traps(w, node) -> list:
    """Those with set traps of their own (or their household's) in a river parcel (u8 §2.2's spate reading)."""
    from cybertron2.engine import things as TH, wild as WL
    out = set()
    for c in w.s["containers"].values():
        sp = c.get("set") or {}
        if c.get("kind") != "set" or c.get("node") != node or sp.get("method") != "trap in water" or sp.get("weir") \
                or sp.get("state") in ("up", "spent") or not WL._river_parcel(w, c.get("parcel")):
            continue
        for n in w.living():
            if w.at(n) == node and TH.owns_set(c, n, w):
                out.add(n)
    return sorted(out)


def dawn_events(w) -> None:
    """The dawn cue (u8 §2.2) and the dawn rows of the flow and the ice (§3.1, §3.3): written as events for this morning at each
    village on a river, before the day's acts, from last night's record, today's pulses and the day's flow."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import runs as RU
    from cybertron2.wild import water as WT
    st = (w.s.get("wild") or {}).get("state") or {}
    if not st.get("runs"):
        return
    m = WL.model(w)
    if not RU.active(m):
        return
    day = WL.eco_day(w)
    for node in sorted({p["node"] for p in w.s["parcels"].values()}):
        if not RU.on_river(m, node) or not any(w.at(n) == node for n in w.agents_acting()):
            continue
        water, fen = _places(w, node)
        if water is None:
            continue
        rec = river_now(w, node)
        names = {"water": w.s["parcels"][water]["name"], "fen": w.s["parcels"][fen]["name"] if fen else ""}
        now = passing(m, st, node, day)
        fl = flow_today(w, node) or "normal"
        set_nights = bool((w.spec or {}).get("runs_set_nights"))
        rain = float((WL.weather(w, sorted(set(m.nodes)), w.d).get(node) or {}).get("rain", 0.0))
        heavy = rain >= 1.5 * RU.RAIN_MEAN
        fire = []
        if _window_near(m, day):
            fire.append(("window", "place", None))
        if now.get("eel", 0.0) >= 3.0:
            started = (rec.get("passed") or {}).get("eel", 0.0) < 1.0
            if not set_nights and heavy and started:
                fire.append(("rain", "place", None))
            fire.append(("eel_night_set" if set_nights else "eel_night_rain", "place", None))
        lb = rec.get("band") or {}
        if _heronry(w, node) and any(at_least(lb.get(k), "thick") for k in ("eel", "salmon")):
            fire.append(("herons", "water", None))
        if fl in ("spate", "flood"):
            fire.append(("roar", "water", None))
            who = _fishers_with_traps(w, node)
            if who:
                fire.append(("spate_traps", "water", who))
            if rain < RU.RAIN_MEAN:
                fire.append(("upriver", "water", None))
            if fl in ("high", "spate", "flood") and any(WL.gap(b) == "shut" for _, b in WL.weirs(w, node)):
                fire.append(("gap_spate", "water", None))
        if at_least(lb.get("salmon"), "running"):
            fire.append(("splash", "water", None))
        if fen and at_least(lb.get("eel"), "thick") and float(rec.get("rain", 0.0)) > 0.5:
            fire.append(("fen_eels", "fen", None))
        ice = WT.stretch_ice(w, node)
        if fen and WT.ice(w, fen) in ("edges", "over"):
            fire.append(("fen_ice", "fen", None))
        if ice == "edges":
            fire.append(("edge_ice", "water", None))
        elif ice == "over":
            fire.append(("frozen", "water", None))
        if WT.thawing(w, water):
            fire += [("thaw_sight", "water", None), ("thaw_sound", "water", None)]
            if WL.weirs(w, node):
                fire.append(("thaw_weir", "water", None))
        for key, spot, only in fire:
            r = DAWN[key]
            text = r["text"].format(share="nearly all of them" if fl == "flood" else "half of them or more", **names)
            reads = r["read"] if isinstance(r["read"], tuple) else (r["read"],)
            for read in reads:
                about = ["sky"] if spot == "place" else [f"parcel:{water if spot == 'water' else fen}"]
                kw = _knows(read)
                if only:
                    kw["only"] = list(only)
                w.event(node, "river", text, about=about, salience=1.0, tags=["fishing", "food"], sense=r["sense"], own=r["own"],
                        dawn=True, night=r.get("night") or False, sign=f"river#{key}{'' if len(reads) == 1 else read}", **kw)


def day_context(w, node, here_day=None):
    """The evening's reading of the river at a village (u8 §2.3, §3): tonight's bands from today's pulses against the station's year,
    the flow and last night's, the year's best night, the first and the ended runs, otters, a heronry, set traps, the weir's overflow,
    the fen, the resident fish."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import runs as RU
    from cybertron2.wild.kinds import ROB_SETS
    st = (w.s.get("wild") or {}).get("state") or {}
    m = WL.model(w)
    day = WL.eco_day(w)
    g = f"v:{node}"
    rec = river_now(w, node)
    now = passing(m, st, node, day)
    b = {k: band(n, year_basis(m, st, k, g, day)) for k, n in now.items()}
    water, fen = _places(w, node)
    land = (w.s["wild"].get("land") or {})
    aid = (land.get("home") or {}).get(node)
    otters = False
    if aid in m.ids and "otter" in (st.get("pop") or {}):
        otters = float(st["pop"]["otter"][m.ids.index(aid)]) >= float(ROB_SETS["least"])
    res = ((w.s["parcels"].get(water) or {}).get("res") or {}).get("fish") if water else None
    yr = int(day) // int(m.Y)
    best = (rec.get("best") or {}) if int(rec.get("year", yr)) == yr else {}
    return SimpleNamespace(
        eel=b.get("eel", "none"), salmon=b.get("salmon", "none"), lamprey=b.get("lamprey", "none"),
        eel_n=float(now.get("eel", 0.0)), salmon_n=float(now.get("salmon", 0.0)), lamprey_n=float(now.get("lamprey", 0.0)),
        eel_best=float(best.get("eel", 0.0)), flow=flow_today(w, node) or "normal", was=rec.get("flow") or "normal",
        first=[k for k, n in now.items() if n >= 1.0 and float(best.get(k, 0.0)) < 1.0], ended=list(rec.get("last") or []),
        eel_window=_in_window(m, day), weathered=not bool((w.spec or {}).get("runs_set_nights")),
        otters=otters, heronry=_heronry(w, node), fen=fen,
        traps=any(c.get("kind") == "set" and c.get("node") == node and (c.get("set") or {}).get("method") == "trap in water"
                  and (c.get("set") or {}).get("state") not in ("up", "spent") for c in w.s["containers"].values()),
        turned=bool(rec.get("turned")) and int(rec.get("day", -9)) == w.d - 1,
        resident=(float(res["S"]) / float(res["K"]) if res and float(res.get("K") or 0) > 0 else None))


def day_signs(here, add) -> None:
    """The run itself and the other states of the water (u8 §2.3, §3), at the village's water, by the one rule."""
    from cybertron2.engine import signs as SG
    w = here._w
    water, fen = _places(w, here.node)
    if water is None:
        return
    x = day_context(w, here.node)
    names = {"water": here.parcels()[water]["name"], "fen": here.parcels()[fen]["name"] if fen else ""}
    doers = [n for n in here.people() if water in _was_at(w, here.today(), n)]
    for j, r in enumerate(DAY):
        try:
            ok = r["when"](x)
        except (TypeError, KeyError, AttributeError, ZeroDivisionError):
            ok = False
        if not ok:
            continue
        if r["who"] == "doer" and not doers:
            continue
        spot = fen if "{fen}" in r["text"] and fen else water
        row = dict(when=lambda x: True, own=r["own"], sense=r["sense"], tags=["fishing", "food"],
                   text=lambda x, t=r["text"].format(**names): t)
        if r["reach"]:
            row["reach"] = r["reach"]
        if r["night"]:
            row["night"] = True
        SG.spot_rows(here, [row], x, [f"parcel:{spot}"], here.node, spot, add, name=f"river{j}",
                     only=doers if r["who"] == "doer" else None, **_knows(r["read"]))


def _was_at(w, today, who) -> list:
    """The parcels one worked at or tended set gear on today (W-102: a weir or traps emptied is a day at the water; a building one
    worked in stands on its parcel)."""
    out = []
    for k in list(today["worked"].get(who) or []) + list((today.get("tended") or {}).get(who) or []):
        pid = k if k in w.s["parcels"] else (w.s["buildings"].get(k) or {}).get("parcel")
        if pid and pid not in out:
            out.append(pid)
    return out


def carried(here, add) -> None:
    """The catch carried home (u8 §2.4; questions B24): one who worked today on a water or fen parcel and holds 5 kg or more of fresh
    fish at evening is seen with it at their house's ground (a presentation choice: the engine does not place a person in the evening;
    the house's ground is where a load is carried to; deterministic), by others, never by the carrier (guide rule 7); fresh meat after a
    hunt the same. The household inside sees it."""
    from cybertron2.engine import signs as SG
    from cybertron2.engine.data import ITEMS
    w = here._w
    water, _ = _places(w, here.node)
    wname = here.parcels()[water]["name"] if water else "the water"
    for who in here.people():
        if w.s["people"][who]["stage"] not in ("youth", "adult", "elder"):
            continue
        worked = _was_at(w, here.today(), who)
        hands = w.s["containers"][w.hands(who)]["goods"]
        fish = sum(float(hands.get(i, 0.0)) * float(ITEMS[i].get("weight", 1.0)) for i in FRESH_FISH if i in ITEMS)
        meat = sum(float(hands.get(i, 0.0)) * float(ITEMS[i].get("weight", 1.0)) for i in FRESH_MEAT if i in ITEMS)
        house = next((b for b in w.homes(who) if w.s["buildings"][b].get("node") == here.node
                      and (w.s["buildings"][b].get("fittings") or {}).get("beds")), None)
        if house is None:
            continue
        spot = w.s["buildings"][house]["parcel"]
        hh = w.household_of(who)
        inside = [m for m in here.people() if m != who and hh and w.household_of(m) == hh]
        others = [m for m in here.people() if m != who]
        kind, kg, place = None, 0.0, ""
        if fish >= CARRIED_KG and any((here.parcels().get(p) or {}).get("cover") in ("water", "fen") for p in worked):
            kind, kg = "fish", fish
        elif meat >= CARRIED_KG and any(e.get("actor") == who and e.get("kind") in ("hunt", "kill") for e in here.events()):
            kind, kg = "meat", meat
            place = next((here.parcels()[p]["name"] for p in worked if p in here.parcels()), "the wood")
        if kind is None:
            continue
        creel = float(hands.get("creel", 0.0)) >= 1
        texts = CARRIED[kind]
        t = texts[2] if kg >= CARRIED_FULL else (texts[0] if creel and texts[0] else texts[1])
        row = dict(when=lambda x: True, own=1.0, sense="sight", tags=["fishing" if kind == "fish" else "hunting", "food"],
                   text=lambda x, s=t.format(who=who, water=wname, place=place): s)
        SG.spot_rows(here, [row], None, [f"person:{who}"], here.node, spot, add, name=f"carried{who}", only=others, inside=inside)
