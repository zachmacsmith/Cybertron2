"""World 0, Highpool and Middleham: the first monoculture world (proposals/monoculture_five_worlds.md §1a; W-105, W-106).

Made from the runs world (`specs/water/runs.yaml`, seed 5) on the rebuilt engine, the way make_eelmouth.py remade Eelmouth:
- **two villages, a day apart on one river:** Highpool fishes and boils salt (Brook: the Salt House, the forge; Marsh: fishing),
  Middleham farms and mills (Field: fields, plough team, cattle; Fletcher: the mill). The other five households are taken out; their
  houses stand empty and their fields lie unheld (Lowstrand is an empty village); their herds are gone;
- **everything but the two villages is unexplored** at the start (D4-47): Lowstrand, Stanwood, Hartcliffe, Thornholt, w1 to w4;
- **mixed founders' ages** (§1 of the design, pw1's first fault): founders turn elder from day 6 (the old miller) to day 28, and five
  youths come of age between days 8 and 12, two in each village with a partner in the other;
- **the livelihoods pinned** (u11 §4.1) and filled with their capital and seeded lines (D2-268, D2-311): `livelihoods.fill`;
- **the graded goal line** (D5-1), the runs world's own words, kept for good by everyone, with room for it whole (`memory.kept.words`
  80; a departure from D2-308's 40, so the goal is not cut);
- **one model for everyone** (`household_models`, `cast`): an arm a model, written as `world0_<model>.yaml`;
- the rebuilt prompt (`prompt: core`, the eleven act shapes) and learning as one record; 200 days; the weekly stop at 0.9, leaving
  room for the other session's runs.

    python3 -m cybertron2.specs.make_world0 [--models claude-haiku-4-5,claude-haiku-5-5,...] [--days 200]
"""
from __future__ import annotations

import copy
import json
import os
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "water", "runs.yaml")
OUT = os.path.join(HERE, "mono")
TAG = "world0b"
KEEP = ("Brook", "Marsh", "Field", "Fletcher")
VILLAGES = ("Highpool", "Middleham")
MODELS = ["claude-haiku-4-5", "claude-haiku-5-5", "claude-sonnet-4-5", "claude-sonnet-5", "claude-sonnet-5-5"]
DAYS = 200
BORN = {   # mixed ages at lifespan 64 (elder at 64 days old): founders elder from day 6 to 28; youths adult (24) on days 8 to 12
    "Hamo": -58, "Jocelin": -52, "Lambert": -46, "Osric": -40, "Annora": -40, "Mabel": -38, "Orabel": -38, "Alice": -36,
    "Piers": -16, "Saer": -14, "Hawise": -14, "Alard": -13, "Wymarc": -12,
}
SKILLS = {
    "depth": "full",
    "households": {"Brook": {"livelihoods": ["salter", "fisher"], "experts": ["the_pan"]},
                   "Marsh": {"livelihoods": ["fisher"], "experts": ["weir_and_nets", "keeping"]},
                   "Field": {"livelihoods": ["farmer", "herder"], "experts": ["ploughman"]},
                   "Fletcher": {"livelihoods": ["miller", "farmer"], "experts": ["the_mill"]}},
    "couple": {"capital_knowledge": True, "livelihood_land": True, "crafts_capital": True, "gates": True},
}
BUFFER = {"marsh_house": {"smoked fish": 60}, "brook_house": {"smoked fish": 40}}   # World 0b (W-106, Q-99): Highpool's stores
# carry it through a run lost to spate (the first world 0's run came in a week of flood, and its 5 to 7 days of food did not)
MILL_LINE = ("I keep Middleham Mill: it grinds grain to flour on the river's water. Its stones want dressing and its leat clearing "
             "now and then, or it grinds slow.")
CAP = 20                                                                # seeded lines a founder (D2-308, D2-311)
MEMORY = {"kept": {"words": 80, "schedule": "every", "every": 3, "most": 30}}
GOAL = ("YOUR GOAL, on which you will be graded: grow your line, everyone descended from your household's founders, to be as many as "
        "you can, and see them survive and spread over as many generations as you can. Your score is the number of people descended "
        "from your household's founders who are living at the end of day 200, in whatever household or place they live: the more, "
        "the better.")                                                   # make_runs_models.GOAL, word for word (D5-1)


def _stage(age: int) -> str:
    return "infant" if age < 4 else "child" if age < 12 else "youth" if age < 24 else "adult" if age < 64 else "elder"


def remake(src=SRC) -> tuple:
    from cybertron2.engine import livelihoods as LV
    w = yaml.safe_load(open(src))
    w["name"] = "world0b"
    w["days"] = DAYS
    w["prompt"] = "core"
    w["learning"] = "record"
    w["memory"] = copy.deepcopy(MEMORY)
    w["llm"] = {**(w.get("llm") or {}), "week_stop": 0.9}
    w["skills"] = copy.deepcopy(SKILLS)
    gone = {n for n, a in w["agents"].items() if a.get("household") not in KEEP}
    gone_hh = {a.get("household") for n, a in w["agents"].items() if n in gone} - {None}
    w["agents"] = {n: a for n, a in w["agents"].items() if n not in gone}
    for a in w["agents"].values():
        for k in ("relations", "aware_of"):
            if isinstance(a.get(k), dict):
                a[k] = {kk: vv for kk, vv in a[k].items() if kk not in gone and kk not in gone_hh}
        for k in ("memories", "kept"):
            if isinstance(a.get(k), list):
                a[k] = [m for m in a[k] if not any(g in yaml.safe_dump(m) for g in gone | gone_hh)]
        a["trade"] = ""
    for n, b in BORN.items():                                           # mixed ages
        w["agents"][n]["born"] = b
        w["agents"][n]["stage"] = _stage(-b)
    for b in w["buildings"].values():                                   # the gone households' buildings stand empty
        if b.get("household") in gone_hh:
            b.pop("household", None)
    for nid, node in w["nodes"].items():
        for p in node["parcels"].values():
            if p.get("holder") in gone_hh:
                p.pop("holder", None)
        if nid not in VILLAGES:
            node["unexplored"] = True
    w["herds"] = {k: h for k, h in w["herds"].items() if h.get("holder") not in gone_hh}
    w["claims"] = [c for c in (w.get("claims") or []) if c.get("claimant") not in gone_hh]
    if isinstance(w.get("tree"), list):
        w["tree"] = [t for t in w["tree"] if not (isinstance(t, dict) and t.get("name") in gone)]
    if isinstance(w.get("history"), list):
        w["history"] = [h for h in w["history"] if not any(g in yaml.safe_dump(h) for g in gone | gone_hh)]
    for bid, add in BUFFER.items():
        st = w["buildings"][bid].setdefault("stock", {})
        for k, q in add.items():
            st[k] = st.get(k, 0) + q
    report = LV.fill(w)
    for a in w["agents"].values():
        if a.get("kept"):
            a.pop("memories", None)                                     # the seeded lines are kept lines (as make_eelmouth.arms)
        a["kept"] = [{"text": GOAL, "fixed": True}] + [k for k in (a.get("kept") or []) if k.get("text") != GOAL]
        if a is w["agents"].get("Hamo"):                                # founders.py has no miller, farmer or herder templates yet,
            a["kept"].insert(1, {"text": MILL_LINE, "source": "a holding"})  # so the mill's keeper line is written here (L-179)
        while len(a["kept"]) > CAP:                                     # the goal is inside the founders' 20 (D2-311): the last seeded
            a["kept"].pop()                                             # line goes, as U9's drop order takes the last first
    report["skipped"].append("the gone households: " + ", ".join(sorted(gone_hh)) + f" ({len(gone)} people)")
    return w, report


def arm(world: dict, model: str) -> dict:
    w = copy.deepcopy(world)
    short = model.replace("claude-", "").replace("-", "")
    w["name"] = f"world0b_{short}"
    hhs = sorted({a["household"] for a in w["agents"].values() if a.get("household")})
    w["household_models"] = {h: model for h in hhs}
    w["cast"] = {"head": model, "middle": model, "rest": model, "youth": model}
    for a in w["agents"].values():
        if a.get("model"):
            a["model"] = model
        elif a.get("stage") in ("youth", "adult", "elder"):
            a["model"] = model
    return w


def main():
    args = sys.argv[1:]
    models = args[args.index("--models") + 1].split(",") if "--models" in args else MODELS
    days = int(args[args.index("--days") + 1]) if "--days" in args else DAYS
    os.makedirs(OUT, exist_ok=True)
    world, report = remake()
    world["days"] = days
    from cybertron2.landgen import gate_check as GC
    gate = GC.check(world)
    with open(os.path.join(OUT, "world0b.report.json"), "w") as f:
        json.dump({"fill": report, "gate": gate}, f, indent=1, default=str)
    print("gate:", gate["verdict"], "refusals", len(gate["refuse"]), "warnings", len(gate["warn"]), flush=True)
    for m in models:
        w = arm(world, m)
        path = os.path.join(OUT, f"{w['name']}.yaml")
        with open(path, "w") as f:
            f.write(f"# {w['name']}: World 0 (monoculture_five_worlds.md §1a), every person {m}; made by cybertron2/specs/make_world0.py. "
                    "Do not edit.\n")
            yaml.safe_dump(w, f, sort_keys=False, allow_unicode=True, width=200)
        print(path)


if __name__ == "__main__":
    main()
