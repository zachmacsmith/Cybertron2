"""The access-gate probe (scenario_design §4: "verify every access gate in a dry run, per action"), for any world file with people.

    python -m cybertron2.landgen.gates <world.yaml> [out.json]

For each place and each gather or work technique, the best-suited person there tries it once, on a fresh copy of the world: someone
who knows the craft if anyone there does; at an unexplored place, someone who knows the place walks in (else anyone). Then every
road is tried from each end, and each unexplored place both by name (by one who knows it) and by its way (by a stranger, D4-47).
It reports what works where and every refusal's reason, so a gate that is shut for everyone (no one knows mining; rock with no
stone) shows before a run, which a bot run does not show: bots wander and starve whatever the world (review 02zn).
"""
from __future__ import annotations

import collections
import contextlib
import copy
import io
import json
import math
import sys

from cybertron2.engine import run as R, verbs as V
from cybertron2.engine.data import ITEMS, TECHNIQUES, WATER_WORKS
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

SKIP = {"care", "herd"}                     # need a child or a herd named; checked by their own tests
ARGS = {"sow": {"item": "grain", "qty": 2}}  # what a technique needs said to be tried at all
# refusals that are the moment or the inputs, not a shut gate: a crop not ripe or standing, no seed or dung to hand, no such ground
SITUATIONAL = ("not ripe", "has a crop in it", "say which", "you have 0.0 to hand", "there is no dung", "nowhere here",
               "sown as thick", "say whose", "needs", "no gate", "no fence", "nothing to", "no one lying", "not wet ground",
               "not hill ground", "is sound", "no ripe crop", "need a tool", "no dead beast", "no strip of", "strip is dug on",
               "you hold no plots", "no line to fish with", "here you can use")


def situational(r: str) -> bool:
    """A refusal that is the moment or the inputs, not a shut gate. Gear or inputs wanted in hand count only where the refusal says
    the person can get them: inputs to bring ("takes ... in hand") or gear they can make ("are made: make ..."); "no traps in hand"
    with no one able to make them is a shut gate (wave_regressions.md findings 1, 9; W-111)."""
    if any(k in r for k in SITUATIONAL):
        return True
    return "in hand" in r and (" takes " in r or "are made: make" in r)


def _ok(out: str) -> bool:
    return not out.startswith(("Refused", "CRASH", "Not done"))


def probe(spec: dict) -> dict:
    with contextlib.redirect_stdout(io.StringIO()):
        base = World(copy.deepcopy(spec))
    base.s["today"] = R.blank_today()
    agents = spec.get("agents") or {}
    knows = lambda n, t: t in ((agents.get(n) or {}).get("knows") or {})
    grown = lambda w, n: w.s["people"][n].get("stage") in ("adult", "elder", "youth") and w.s["people"][n].get("alive", True)
    from cybertron2.engine import packs as PK
    techs = sorted(k for k, t in TECHNIQUES.items() if t.get("verb") in ("gather", "work") and k not in SKIP
                   and PK.on(t, PK.of(base)))                                 # only what the world's packs switch on (D4-103)

    def attempt(w, who, a):
        try:
            return V.do(Here(w, who), Mind(w, who), a)
        except Exception as e:                                             # noqa: BLE001 (a crash is a finding)
            return f"CRASH {type(e).__name__}: {e}"

    gates = collections.defaultdict(dict)
    for nid, node in base.s["nodes"].items():
        covers_here = {p["cover"] for p in base.s["parcels"].values() if p["node"] == nid}
        for tech in techs:
            want = set((TECHNIQUES[tech].get("at") or {}).get("covers") or [])
            if want and not want & covers_here:                            # no such ground here: nothing to gate
                gates[node["name"]][tech] = {"who": None, "walked in": False, "result": "Refused: nowhere here: no such ground"}
                continue
            w = copy.deepcopy(base)
            tool = lambda n: any(q >= 1 and (ITEMS.get(i) or {}).get("tool") for i, q in w.goods(w.hands(n)).items())
            folk = sorted((n for n, a in w.s["people"].items() if a.get("at") == nid and grown(w, n)),
                          key=lambda n: (not knows(n, tech), not tool(n), n))     # one who knows it and holds a tool, as one would send
            moved = False
            if not folk:
                knowers = [n for n, a in agents.items() if nid in (a.get("places") or []) and n in w.s["people"] and grown(w, n)]
                folk = sorted(knowers, key=lambda n: (not knows(n, tech), n)) or sorted(n for n in w.s["people"] if grown(w, n))
                if not folk:
                    continue
                w.s["people"][folk[0]]["at"] = nid
                moved = True
            who = folk[0]
            if tech == "reap":                                             # try reaping on the day the first crop here ripens
                ripe = [int(c["ripe_day"]) for pid, par in w.s["parcels"].items() if par["node"] == nid
                        for c in ([par.get("crop")] + [sh.get("crop") for sh in par.get("shares") or []]) if c and c.get("ripe_day") is not None]
                if ripe:
                    w.s["day"] = max(w.s["day"], min(ripe))
            out = attempt(w, who, {"do": TECHNIQUES[tech]["verb"], "what": tech, **ARGS.get(tech, {})})
            gates[node["name"]][tech] = {"who": who, "walked in": moved, "result": out}
    roads = []
    names = {n["name"] for n in base.s["nodes"].values()}
    for rd in base.s["roads"].values():
        for a, b in ((rd["a"], rd["b"]), (rd["b"], rd["a"])):
            if base.s["nodes"][a].get("unexplored"):
                continue
            folk = [n for n, p in base.s["people"].items() if p.get("at") == a and grown(base, n)]
            if not folk:
                continue
            tries = []
            if base.s["nodes"][b].get("unexplored"):
                knowers = [n for n in folk if b in ((agents.get(n) or {}).get("places") or [])]
                strangers = [n for n in folk if n not in knowers]
                if knowers:
                    tries.append((knowers[0], base.s["nodes"][b]["name"]))
                if strangers:
                    w = copy.deepcopy(base)
                    way = next((n for _, n, d, t in Here(w, strangers[0]).roads() if n not in names), "an unexplored way")
                    tries.append((strangers[0], way))
            else:
                tries.append((folk[0], base.s["nodes"][b]["name"]))
            for who, to in tries:
                w = copy.deepcopy(base)
                roads.append({"from": base.s["nodes"][a]["name"], "to": base.s["nodes"][b]["name"], "as": to, "who": who,
                              "result": attempt(w, who, {"do": "travel", "to": to})})
    return {"gates": gates, "roads": roads}


def summary(res: dict) -> dict:
    """What works where; the techniques no one can do anywhere; crashes; roads that refuse."""
    works = {node: sorted(t for t, r in g.items() if _ok(r["result"])) for node, g in res["gates"].items()}
    anywhere = set().union(*works.values()) if works else set()
    every = set(t for g in res["gates"].values() for t in g)
    moment = {t for g in res["gates"].values() for t, r in g.items() if situational(r["result"])}
    nowhere = every - anywhere
    return {"works": works, "shut everywhere": sorted(nowhere - moment), "only the moment or inputs": sorted(nowhere & moment),
            "crashes": [(n, t, r["result"]) for n, g in res["gates"].items() for t, r in g.items() if r["result"].startswith("CRASH")],
            "roads refused": [(r["from"], r["to"], r["as"], r["result"]) for r in res["roads"] if not _ok(r["result"])]}


# ---------------------------------------------------------------------------------------------------------------------- making
# The making chains' gates at world build (u3_making.md §7; D2-270: on by default, off only by an explicit setting in the world's
# spec, `gates: {making: false}` for all or `gates: {M4: false}` for one). M1 inputs within a day; M2 seed for a sown craft; M3 gear
# needed before its season with no time to make it; M4 tools that cannot be remade; M5 a process with no site; M6 no one capable in
# reach; M7 a work's whole need more than the house can gather in its season; M8 every make tried with its inputs in hand. There are
# no livelihood rows yet (U11, stage 4): a household's crafts are those its members know (core: one knows it at `known`), and the
# gear its taking needs (a trap-setter's traps). Run on every world (the engine has no materials pack: a departure from u3 §7).
from dataclasses import dataclass, asdict  # noqa: E402


@dataclass
class Finding:
    check: str          # "M1" .. "M8"
    level: str          # "refuse" | "warn" | "report"
    village: str
    household: str | None
    text: str           # the line written to the build report, in plain words


LEVELS = ("rough", "capable", "known")
GEAR_OF = {"trap in water": "wicker trap", "gill net": "gill net", "set line": "set line", "snare": "snare"}
WEIR_UPKEEP = 0.25                          # a weir's yearly upkeep, a share of its build (D2-302's quarter to a third; the low end)
SEASON_GEAR = {"trap in water": 6}          # pieces a setter wants by the first run night (D2-330's C5: six a setter)


def _within_a_day(w) -> dict:
    out = {nid: {nid} for nid in w.s["nodes"]}
    for rd in w.s["roads"].values():
        if int(rd.get("days", 1)) <= 1:
            out[rd["a"]].add(rd["b"])
            out[rd["b"]].add(rd["a"])
    return out


def _households(w) -> list:
    out = []
    for iid, h in sorted(w.s["institutions"].items()):
        if h.get("kind") != "household":
            continue
        ms = [m for m in h["members"] if w.s["people"].get(m, {}).get("alive", True)]
        if ms:
            out.append((iid, h, ms, w.s["people"][ms[0]].get("at")))
    return out


def _crafts(w, ms) -> dict:
    """{technique: "core" | "secondary"}: what the household's members know (core: at `known` by one of them)."""
    from cybertron2.engine import knowledge as KN
    out = {}
    for m in ms:
        for t, r in (w.s["know"].get(m) or {}).items():
            if t in TECHNIQUES and r.get("level") in LEVELS and not KN.basic(t) and TECHNIQUES[t].get("verb") in ("make", "gather", "work"):
                out[t] = "core" if r["level"] == "known" or out.get(t) == "core" else "secondary"
    return out


def _gives(t) -> list:
    g = t.get("gives")
    return [g] if isinstance(g, str) and g else list((g or {}).keys())


def _source_within(w, nodes, ms, good, depth=0) -> bool:
    """Whether a good can be had within a day (u3 §7): held by the household; a store there holds some; a gather or work that gives
    it has its ground and a stock there; or a make that gives it has its own inputs so (two steps deep)."""
    from cybertron2.engine import packs as PK
    if any(float(w.goods(w.hands(m)).get(good, 0.0)) > 1e-9 for m in ms):
        return True
    if any(b["node"] in nodes and float(w.goods(b["stock"]).get(good, 0.0)) > 1e-9 for b in w.s["buildings"].values()):
        return True
    for tech, t in TECHNIQUES.items():
        if good not in _gives(t) or not PK.on(t, PK.of(w)) or t.get("modifies"):
            continue
        if t["verb"] in ("gather", "work"):
            covers = set((t.get("at") or {}).get("covers") or [])
            for pid, par in w.s["parcels"].items():
                if par["node"] not in nodes or (covers and par["cover"] not in covers):
                    continue
                d = t.get("draws")
                if d in par["res"] and float(par["res"][d]["S"]) > 0:
                    return True
                if t.get("draws_else") in par["res"] and float(par["res"][t["draws_else"]]["S"]) > 0:
                    return True
                if not d or d not in __import__("cybertron2.engine.data", fromlist=["RESOURCES"]).RESOURCES:
                    return True                                              # drawn from nothing (twist cord, salt pans' sun)
        elif t["verb"] == "make" and depth < 2:
            ins = t.get("inputs") or {}
            if all(any(_source_within(w, nodes, ms, i, depth + 1) for i in (q if isinstance(q, dict) else {g: q}))
                   for g, q in ins.items()):
                return True
    return False


def _first_run_day(w) -> int | None:
    """The first ecology day a run's window opens from today (the fisher's year), or None without runs."""
    from cybertron2.engine import wild as WL                           # a failure here raises: M3 is never skipped silently (W-111)
    from cybertron2.wild import runs as RU
    if not WL.on(w) or not (w.s.get("wild") or {}).get("state"):
        return None
    m = WL.model(w)
    if not RU.active(m):
        return None
    d0 = WL.eco_day(w)
    for j in range(int(w.year_days()) + 1):
        if any(RU._window(m, d0 + j, r["seasons"])[0] for r in RU.runners_of(m).values()):
            return j
    return None


def making_gates(w, spec=None) -> list:
    """The making chains' gates (u3 §7) on a built world `w`; changes nothing. Returns [Finding]."""
    from cybertron2.engine import clocks as CK, gear as GE, knowledge as KN
    spec = spec if spec is not None else (w.spec or {})
    off = spec.get("gates") or {}
    if off.get("making") is False:
        return []
    on = lambda c: off.get(c) is not False
    reach = _within_a_day(w)
    out = []
    for iid, h, ms, node in _households(w):
        if node is None:
            continue
        village = w.s["nodes"][node]["name"]
        name = h.get("name", iid)
        nodes = reach.get(node, {node})
        crafts = _crafts(w, ms)
        for tech, core in sorted(crafts.items()):                                                      # M1
            t = TECHNIQUES[tech]
            for good, q in sorted((t.get("inputs") or {}).items()):
                alts = list(q) if isinstance(q, dict) else [good]
                if on("M1") and not any(_source_within(w, nodes, ms, g) for g in alts):
                    out.append(Finding("M1", "refuse" if core == "core" else "warn", village, iid,
                                       f"{name}: {KN.label(tech)} needs {' or '.join(alts)}, and none is to be had within a day"))
        if on("M2") and "dress and spin" in crafts and not _source_within(w, nodes, ms, "flax seed"):         # M2
            out.append(Finding("M2", "refuse", village, iid, f"{name} spin flax, and there is no flax seed within a day"))
        first = _first_run_day(w)
        for tech, want in SEASON_GEAR.items():                                                         # M3
            setters = [m for m in ms if ((w.s["know"].get(m) or {}).get(tech) or {}).get("level") in LEVELS
                       and w.s["people"][m].get("stage") in ("adult", "elder")]
            if not on("M3") or not setters or first is None:
                continue
            item = GEAR_OF[tech]
            held = sum(GE.sound_count(w.s["containers"][w.hands(m)], item, w) for m in ms)
            short = max(0, want * len(setters) - held)
            if short <= 0:
                continue
            rt = TECHNIQUES.get(GE.craft_of(item) or "", {})
            lv = max((((w.s["know"].get(m) or {}).get(GE.craft_of(item) or "") or {}).get("level") for m in setters),
                     key=lambda x: LEVELS.index(x) if x in LEVELS else -1, default=None)
            from cybertron2.engine.data import TRY
            tr = TRY.get(lv or "rough") or TRY["rough"]                     # a rough hand's materials and odds (u3 §5)
            units = math.ceil(math.ceil(short / max(1, CK.batch_of(rt, w))) / float(tr["chance"])) if rt else 0
            withies = short * float((rt.get("inputs") or {}).get("withies", 0.0)) * float(tr["inputs"]) / float(tr["chance"])
            season = w.calendar()["season"]
            cut = 1.5 * float(TECHNIQUES["cut withies"]["by_season"].get(season, 1.0))
            units += math.ceil(withies / max(1e-9, cut)) if withies else 0
            spare = first * 2 * len([m for m in ms if w.s["people"][m].get("stage") == "adult"])
            if units > spare:
                out.append(Finding("M3", "warn", village, iid, f"{name}: {short} {GE.plural(item)} needed by the first run in {first} days; "
                                                              f"about {units} units to make them, the {season} rods at {cut:g} bundles a unit"))
        cuts = True                                                                                   # M4: everyone cuts withies
        stone = any(par["node"] in nodes and "quarry" in par["res"] for par in w.s["parcels"].values()) or \
            any(b["node"] in nodes and float(w.goods(b["stock"]).get("stone", 0.0)) >= 0.04 for b in w.s["buildings"].values())
        if on("M4") and cuts and not stone:
            tool = any(float(w.goods(w.hands(m)).get(x, 0.0)) >= 1 for m in ms for x in ("crude tool", "copper tool"))
            out.append(Finding("M4", "warn", village, iid, f"{name}: no stone within a day: crude tools cannot be "
                                                          + ("remade once these wear out" if tool else "made, and the house holds none")))
        if on("M5") and "dress and spin" in crafts and not any(par["node"] in nodes and par["cover"] in ("water", "fen")
                                                               for par in w.s["parcels"].values()):     # M5: retting water
            out.append(Finding("M5", "refuse", village, iid, f"{name}: no water within reach to ret flax in"))
        for tech in sorted(crafts):                                                                    # M6: the gear's making
            item = GEAR_OF.get(tech)
            craft = GE.craft_of(item) if item else None
            if not on("M6") or not craft or KN.basic(craft):
                continue
            near = [m for m, p in w.s["people"].items() if p.get("alive", True) and p.get("at") in nodes]
            if not any(((w.s["know"].get(m) or {}).get(craft) or {}).get("level") in ("capable", "known") for m in near):
                out.append(Finding("M6", "refuse" if crafts[tech] == "core" else "warn", village, iid,
                                   f"{name}: no one capable of {KN.label(craft)} in the house or within a day, for {KN.label(tech)}"))
        for bid, b in sorted(w.s["buildings"].items()):                                                # M7: a wattle weir's withies
            if not on("M7") or b.get("monument") != "weir" or not any(c.get("claimant") == iid for c in w.claims_on(("building", bid))):
                continue                                                       # held by a claim in the state (it never read before: W-111)
            wattle = sum(1 for sc in (b.get("sections") or []) if sc.get("m") == "wattle")
            if not wattle:
                continue
            cost = WATER_WORKS["weir"]["cost"]                                 # the sections' withies, read from the data (W-111)
            first = float(cost["first"]["wattle"]["materials"].get("withies", 0.0))
            added = float(cost["added"]["wattle"]["materials"].get("withies", 0.0))
            need = WEIR_UPKEEP * (first + added * max(0, wattle - 1))
            have = sum(float(par["res"]["willow"]["K"]) for par in w.s["parcels"].values() if par["node"] in nodes and "willow" in par["res"])
            if have < need:
                out.append(Finding("M7", "warn", village, iid, f"{name}: the weir's wattle wants about {need:g} bundles of withies a year; "
                                                              f"the willow within a day gives {have:g}"))
    if on("M8"):
        out += probe_making(w)
    return out


def probe_making(w) -> list:
    """M8 (u3 §7): every make technique the world's packs switch on, at each village, tried by one person there on a fresh copy of the
    world with its inputs (one act's batch) put into their hands, its craft known to them, and the fitting it needs in their house.
    A refusal that is not of the moment, or a crash, is a finding: the code's gate, not the world's."""
    from cybertron2.engine import knowledge as KN, packs as PK
    out = []
    techs = sorted(k for k, t in TECHNIQUES.items() if t.get("verb") == "make" and PK.on(t, PK.of(w)) and not t.get("modifies")
                   and not t.get("mend_gear"))
    for nid in sorted(w.s["nodes"]):
        folk = sorted(n for n, p in w.s["people"].items() if p.get("at") == nid and p.get("alive", True) and p.get("stage") == "adult")
        if not folk:
            continue
        for tech in techs:
            t = TECHNIQUES[tech]
            w2 = copy.deepcopy(w)
            w2.s["today"] = R.blank_today()
            who = folk[0]
            w2.s["know"].setdefault(who, {})[tech] = {"level": "known", "skill": 1.0, "seen": 0, "wins": 0, "fails": 0, "source": "",
                                                       "since": -1}
            hands = w2.hands(who)
            for good, q in (t.get("inputs") or {}).items():
                g, n = next(iter(q.items())) if isinstance(q, dict) else (good, q)
                w2.apply("create", nid, dst=hands, item=g, qty=float(n) * 2.0, why="probe")
            fits = (t.get("at") or {}).get("fittings") or []
            if fits:
                home = next((b for b in w2.homes(who) if w2.s["buildings"][b]["node"] == nid), None)
                if home is None:
                    continue
                fs = dict(w2.s["buildings"][home].get("fittings") or {})
                for f in fits[:1]:
                    fs.setdefault(f, 1)
                w2.s["buildings"][home]["fittings"] = fs
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    r = V.do(Here(w2, who), Mind(w2, who), {"do": "make", "what": tech})
            except Exception as e:                                             # noqa: BLE001 (a crash is a finding)
                r = f"CRASH {type(e).__name__}: {e}"
            if r.startswith("CRASH") or (r.startswith("Refused") and not (situational(r) or any(k in r for k in ("spring", "racks", "full")))):
                out.append(Finding("M8", "report", w.s["nodes"][nid]["name"], None, f"{KN.label(tech)}: {r[:200]}"))
    return out


def making_report(path) -> dict:
    """The making gates of a world file: {"findings": [...], "by_check": {check: n}}."""
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec(path))
    fs = making_gates(w)
    return {"findings": [asdict(f) for f in fs], "by_check": dict(collections.Counter(f.check for f in fs))}


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    res = probe(load_spec(argv[0]))
    s = summary(res)
    for node, ts in s["works"].items():
        print(f"{node}: {', '.join(ts)}")
    print("shut everywhere:", ", ".join(s["shut everywhere"]) or "none")
    print("not now (the moment or inputs):", ", ".join(s["only the moment or inputs"]) or "none")
    print("crashes:", s["crashes"] or "none")
    print("roads refused:", s["roads refused"] or "none")
    if len(argv) > 1:
        with open(argv[1], "w") as f:
            json.dump(res, f, indent=1)
    return 1 if s["crashes"] or s["roads refused"] or s["shut everywhere"] else 0


if __name__ == "__main__":
    sys.exit(main())
