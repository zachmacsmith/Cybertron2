"""The gate check at world build (u11_worlds.md §5; D2-270, D2-279, D2-286, D2-308, scenario_design §2, §4): one runner, in three
passes: the people checks (P1 to P21, here), the making checks (u3's M1 to M8, gates.making_gates and probe_making) and the dry probe
(gates.probe: each gather and work technique tried once, every road from each end). Each finding is refuse (the world is not run as
is), warn (reported) or report (a fact for the reader). A coupling turned off in `skills.couple`, and the comparison arm's seeded
lines turned off (`skills.depth: none`, D2-331), turn their checks to report. Deterministic; no model.

    python3 -m cybertron2.landgen.gate_check <world.yaml> [out.json]
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import re
import sys

PRICE = re.compile(r"\b(graded|grade|score|points|scoring)\b|\b\d+\s*(coin|coins|pence|shillings)\b", re.I)



def pinned(line) -> bool:
    """A kept line pinned and tagged (fixed, with a tag saying what it is, e.g. the graded goal): put in on purpose, so exempt
    from the seeded-line checks on length (P6) and on naming a price, a score or a grade (P20) (D5-3, Zach 24 Nov)."""
    return isinstance(line, dict) and bool(line.get("fixed")) and bool(str(line.get("tag") or "").strip())

def _family(model) -> str:
    """A model's family from its id ("claude-haiku-4-5" and "claude-haiku-5-5": "haiku"), for the cast's tiers (P17)."""
    parts = str(model or "").lower().split("-")
    return parts[1] if len(parts) > 1 and parts[0] == "claude" else str(model or "").lower()


def _f(out, check, level, text, who=None):
    out.append({"check": check, "level": level, "who": who, "text": text})


def people_checks(world: dict) -> list:
    """P1 to P21 on a world as written (spec form), with the fill's fields on its people and buildings (livelihoods.fill)."""
    from cybertron2.engine import livelihoods as LV
    from cybertron2.engine.data import TECHNIQUES
    from cybertron2.engine.world import renamed
    renamed(world)                                                             # crafts under their current names (Q-109)
    out = []
    skills = world.get("skills") or {}
    couple = {**{"capital_knowledge": True, "livelihood_land": True, "crafts_capital": True, "gates": True}, **(skills.get("couple") or {})}
    lines_on = skills.get("depth", "full") != "none"
    agents = world.get("agents") or {}
    hhs = {}
    for n, a in agents.items():
        if a.get("household"):
            hhs.setdefault(a["household"], []).append(n)
    lvl = lambda n, t: ((agents[n].get("knows") or {}).get(t) or {}).get("level") if isinstance((agents[n].get("knows") or {}).get(t), dict) \
        else (agents[n].get("knows") or {}).get(t)  # noqa: E731
    kept_of = lambda n: [x if isinstance(x, dict) else {"text": x, "source": "seeded"} for x in agents[n].get("kept") or []]  # noqa: E731
    for hh, ms in sorted(hhs.items()):
        holds = {kind: [bid for bid, b in (world.get("buildings") or {}).items() if b.get("household") == hh and r["of"](b)]
                 for kind, r in LV.HOLDINGS.items()}
        holds = {k: v for k, v in holds.items() if v}
        lev = "refuse" if couple["capital_knowledge"] else "report"
        for kind, bids in holds.items():                                       # P1: a holding's working craft known at capable
            H = LV.HOLDINGS[kind]
            for bid in bids:
                if not any(lvl(n, t) in ("capable", "known") for n in ms for t in H["working"] if t in TECHNIQUES):
                    _f(out, "P1", lev, f"{hh}: nobody in the household knows {' or '.join(H['working'])} well enough to work {bid}", hh)
                keeper = (world["buildings"][bid] or {}).get("keeper")       # P2: the keeper's line, and the household's HL line
                srcs = [x for n in ms for x in kept_of(n) if x.get("source") == "a holding"]
                mine = [x for x in kept_of(keeper)] if keeper in agents else []
                if not keeper or not any(x.get("source") == "a holding" for x in mine) and lines_on:
                    _f(out, "P2", lev if lines_on else "report", f"{hh}: {bid} has no keeper line to its keeper ({keeper or 'none'})", hh)
                if lines_on and not srcs:
                    _f(out, "P2", lev, f"{hh}: holds {bid} and no member has a line about it", hh)
        livs = sorted({lv for n in ms for lv in agents[n].get("livelihoods") or []})
        if not livs:                                                           # P3: a livelihood's fits; none at all
            _f(out, "P3", "refuse" if couple["livelihood_land"] else "report", f"{hh}: no livelihood row (the people's crafts are not a living)", hh)
        parcels = {pid: p for nd in world["nodes"].values() for pid, p in (nd.get("parcels") or {}).items()}
        covers = {p["cover"] for p in parcels.values()}
        springs = {p.get("spring") for p in parcels.values()}
        for lv in livs:
            fits = LV.ROWS[lv]["fits"]
            ok = (not fits.get("covers") or covers & set(fits["covers"])) or (fits.get("spring") in springs)
            if fits.get("spring") and fits.get("spring") in springs:
                ok = True
            if not ok:
                _f(out, "P3", "refuse" if couple["livelihood_land"] else "report", f"{hh}: {lv} does not fit the land here", hh)
            if LV.ROWS[lv].get("status") != "built":
                _f(out, "P15", "refuse", f"{hh}: {lv} is not built", hh)
        bands = {n: agents[n].get("band") for n in ms}
        specs = [agents[n].get("specialism") for n in ms if agents[n].get("specialism")]
        if len(specs) != len(set(specs)):                                      # P12
            _f(out, "P12", "warn", f"{hh}: two experts in one specialism", hh)
        working = [n for n in ms if agents[n].get("stage") in ("youth", "adult", "elder")]
        if livs and len(specs) != LV.experts_for(len(working)) and not (skills.get("households") or {}).get(hh, {}).get("experts_n"):
            _f(out, "P13", "warn", f"{hh}: {len(specs)} experts for {len(working)} working members (D2-270: {LV.experts_for(len(working))})", hh)
        for n in ms:                                                           # P8: an apprentice to no expert
            ap = agents[n].get("apprentice")
            if ap and not any(agents[x].get("specialism") == ap.get("specialism") for x in ms):
                _f(out, "P8", "refuse", f"{n} is apprenticed to {ap.get('specialism')}, which no one in the household holds", n)
        weir = holds.get("weir")
        if weir and len([n for n in working if agents[n].get("stage") != "youth"]) < 2 and not any((world["buildings"][b].get("crew") or [])[1:] for b in weir):
            _f(out, "P19", "warn", f"{hh}: a weir with fewer than two working members and no crew", hh)
    for n, a in sorted(agents.items()):                                       # the people's own lines
        if not a.get("household") or a.get("stage") not in ("youth", "adult", "elder", "child"):
            continue
        kept = kept_of(n)
        if lines_on and kept:
            if len(kept) > 20:
                _f(out, "P5", "refuse", f"{n}: {len(kept)} seeded lines, over the cap of 20", n)
            for x in kept:
                if pinned(x):                                                  # a pinned, tagged line: put in on purpose (D5-3)
                    continue
                if len(str(x.get("text")).split()) > 40:
                    _f(out, "P6", "refuse", f"{n}: a line of {len(str(x['text']).split())} words: {x['text'][:60]}", n)
        for x in kept + [{"text": c} for c in world.get("customs") or []]:
            if pinned(x):                                                      # D5-3
                continue
            if PRICE.search(str(x.get("text") or "")):
                _f(out, "P20", "refuse", f"{n}: a seeded line names a price, a score or a grade: {str(x.get('text'))[:80]}", n)
        if a.get("role") == "head" and lines_on and kept:                      # P14 (D2-279): the head's management lines
            texts = " ".join(str(x.get("text")) for x in kept)
            if "Our store at" not in texts or "go first or go off" not in texts or "whoever heads it after me" not in texts:
                _f(out, "P14", "refuse", f"{n}: a head without HH1, HH3 and HH7", n)
    cast = [a.get("model") for a in agents.values() if a.get("stage") in ("adult", "elder", "youth") and a.get("model") not in (None, "bot")]
    from cybertron2.engine.livelihoods import CAST
    weak = _family(CAST["rest"])                                               # the weakest tier: the cast's "rest" model's family, any
    if cast and all(_family(m) == weak for m in cast) and not (world.get("cast") or {}).get("allow_weak"):   # version (W-111)
        _f(out, "P17", "warn", "every acting person on the weakest model's family (an all-Haiku society)")     # a flag, not a block (D5-4, Zach)
    for n, a in sorted(agents.items()):                                       # P16: heads and chokepoint keepers on the head model
        keeps = [bid for bid, b in (world.get("buildings") or {}).items() if b.get("keeper") == n
                 and any(LV.HOLDINGS[k]["chokepoint"] and LV.HOLDINGS[k]["of"](b) for k in LV.HOLDINGS)]
        if (a.get("role") == "head" or keeps) and a.get("model") not in (None, "bot", CAST["head"]):
            _f(out, "P16", "warn", f"{n}: a head or a chokepoint keeper on {a.get('model')}", n)
    # P10, P11: a holding's mending wants copper; a chokepoint craft needed and held nowhere in reach
    needs = {g for a in agents.values() for lv in a.get("livelihoods") or [] for g in LV.ROWS[lv]["depends"]["needs"]}
    gives = {g for a in agents.values() for lv in a.get("livelihoods") or [] for g in LV.ROWS[lv]["depends"]["gives"]}
    for b in (world.get("buildings") or {}).values():
        if (b.get("fittings") or {}).get("brine pan") and "copper" not in gives:
            _f(out, "P10", "warn", f"{b.get('name')}: the brine pan wears and wants copper to mend; no smith in reach")
    for g in sorted(needs - gives):
        if g in ("copper", "stone"):
            _f(out, "P11", "warn", f"{g}: needed by a living here and made by none in reach (a designed scarcity, or not)")
    # P18: the village rule (2 to 5 livelihoods holding capital; a chokepoint inside; a need met only from outside, with a village in reach)
    held = {lv for hh, ms in hhs.items() for n in ms for lv in (agents[n].get("livelihoods") or [])[:1]
            if any(b.get("household") == hh for b in (world.get("buildings") or {}).values() if b.get("keeper"))}
    villages = [nid for nid, nd in world["nodes"].items() if any(b.get("household") for b in (world.get("buildings") or {}).values()
                                                                 if b.get("parcel") in (nd.get("parcels") or {}))]
    if not 2 <= len(held) <= 5 or len(villages) < 2:
        _f(out, "P18", "warn", f"the village rule: {len(held)} livelihoods hold capital; {len(villages)} village(s) in the world, so a need "
                               "from outside has no village in reach to meet it")
    # P21 (D2-286): the old prompt reachable
    if (world.get("view") or "") != "beliefs":
        _f(out, "P21", "refuse", "the world has no beliefs view: the old turn prompt is reachable")
    from cybertron2.engine import knowledge as KN
    if hasattr(KN, "options"):
        _f(out, "P21", "refuse", "the options list is in the code (knowledge.options)")
    # P7: crafts at capable or above with no lesson rows (the lessons are not built: one finding listing them)
    no_lessons = sorted({t for a in agents.values() for t, v in (a.get("knows") or {}).items() if t in TECHNIQUES
                         and (v.get("level") if isinstance(v, dict) else v) in ("capable", "known") and not TECHNIQUES[t].get("lessons")
                         and not TECHNIQUES[t].get("basic")})
    if no_lessons:
        _f(out, "P7", "warn", "crafts held at capable or above with no lesson rows (their failures say only \"your hands\"): " + ", ".join(no_lessons))
    return out


def check(world: dict, probe=True) -> dict:
    """The three passes on a world as written. Returns {"verdict": pass | refuse, "refuse", "warn", "report", "making", "probe"}."""
    from cybertron2.engine.world import World
    from cybertron2.landgen import gates as G
    out = people_checks(world)
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(copy.deepcopy(world))
    from cybertron2.engine import run as R
    w.s["today"] = R.blank_today()
    making = [f.__dict__ for f in G.making_gates(w)] + [f.__dict__ for f in G.probe_making(w)]
    for f in making:
        out.append({"check": f["check"], "level": f["level"], "who": f.get("household"), "text": f["text"]})
    pr = None
    if probe:
        pr = G.summary(G.probe(copy.deepcopy(world)))
        for t in pr["shut everywhere"]:
            out.append({"check": "probe", "level": "report", "who": None, "text": f"{t}: shut everywhere in the dry probe"})
        for c in pr["crashes"]:
            out.append({"check": "probe", "level": "refuse", "who": None, "text": f"crash: {c}"})
    rep = {"refuse": [x for x in out if x["level"] == "refuse"], "warn": [x for x in out if x["level"] == "warn"],
           "report": [x for x in out if x["level"] == "report"]}
    rep["verdict"] = "refuse" if rep["refuse"] else "pass"
    rep["probe"] = pr
    return rep


def waivers(world: dict) -> dict:
    """The checks a world waives, each with its reason (`gate: {waive: {P20: "why"}}`): a waived refusal is not run silently but
    listed at the run's start and in its record (W-111 §4). A waiver without a reason is refused."""
    w = (world.get("gate") or {}).get("waive") or {}
    if not isinstance(w, dict):
        raise ValueError("gate.waive is a map of check to reason, e.g. {P20: \"the graded goal line, D5-1\"}")
    bad = sorted(k for k, v in w.items() if not str(v or "").strip())
    if bad:
        raise ValueError(f"gate.waive: no reason given for {', '.join(bad)}")
    return {str(k): str(v) for k, v in w.items()}


def at_start(world: dict) -> dict:
    """The gate at a run's start (Q-100, W-111 §4): the people and making checks (no dry probe), with the world's waivers applied.
    Returns the report with "waived" (the refusals the world waives, with their reasons) and the verdict over what is left."""
    rep = check(world, probe=False)
    wv = waivers(world)
    rep["waived"] = [{**x, "reason": wv[x["check"]]} for x in rep["refuse"] if x["check"] in wv]
    rep["refuse"] = [x for x in rep["refuse"] if x["check"] not in wv]
    rep["verdict"] = "refuse" if rep["refuse"] else "pass"
    return rep


def start_line(rep: dict | None, ungated=False) -> str:
    """One line for the run's start: what the gate found, and what was waived or overridden."""
    if rep is None:
        return "gate: not checked (no person in this run acts by a model)"
    by = {}
    for x in rep.get("waived") or []:
        by.setdefault(x["check"], (x["reason"], []))[1].append(x)
    w = "; ".join(f"{c} x{len(xs)} waived ({r})" for c, (r, xs) in sorted(by.items()))
    if rep["verdict"] == "pass":
        return "gate: pass" + (f"; {w}" if w else "")
    n = sorted({x["check"] for x in rep["refuse"]})
    return (f"WARNING: gate: UNGATED: {len(rep['refuse'])} refusals run anyway ({', '.join(n)})" if ungated else
            f"gate: refuse ({', '.join(n)})") + (f"; {w}" if w else "")


def main(argv=None) -> int:
    from cybertron2.engine.world import load_spec
    argv = argv or sys.argv[1:]
    rep = check(load_spec(argv[0]))
    for lv in ("refuse", "warn", "report"):
        for x in rep[lv]:
            print(f"{lv:7} {x['check']:6} {x['text']}")
    print("verdict:", rep["verdict"])
    if len(argv) > 1:
        with open(argv[1], "w") as f:
            json.dump(rep, f, indent=1, default=str)
    return 1 if rep["verdict"] == "refuse" else 0


if __name__ == "__main__":
    sys.exit(main())
