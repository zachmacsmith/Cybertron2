"""Eelmouth remade (u11_worlds.md §7; D2-316, D2-330, D2-331, D2-334): live run 1's world, from the runs world's high arm (seed 5,
`nutrition/runs_high.yaml`: the same land and people), with livelihoods, holdings and the founders' seeded lines filled both ways.

    python3 cybertron2/specs/make_eelmouth.py [--out DIR]

Writes three files beside each other (`nutrition/`):
- `eelmouth.yaml`, the main arm: the core prompt and the eleven shapes (`prompt: core`, D2-314), learning as one record (`learning:
  record`, D2-307, D2-326), the founders' seeded lines in their kept places (D2-268, D2-308, D2-311), 40 days;
- `eelmouth_old.yaml`, the comparison arm (D2-331): the same world with today's system prompt and its verb list (`prompt: old`; the
  options list stays removed, D2-286) and none of the new seeded lines (the world's generated memories as today), shorter: through the
  first autumn run;
- the bot null arm is the main file run with `--bots runs` (bots_livelihood.py), no model calls.

What the remaking changes (D2-330): the Salt House and the Fen's spring to the Brooks (C1); a rock source in reach (C2: a rock parcel,
the Scar, beside the Spinney and Hazel Copse); no other village in reach (C3, as before); six wicker traps for each capable or expert
setter and a gill net to the weir's expert (C5); a youth eats about 0.8 a night (C6, engine/life.py). Water-only (D2-316): the
resident fish and the shallows small, the runs the main part, as the runs world already is. The smoke huts are wattle huts of one
set of racks each (D2-284, D2-291), a hut room of 2 spaces (its work floor 1, u4 §4). From stage 2's gate check: the weir expert
knows the net's making with cord to be twisted within reach (M6), the rock is within a day (M4), and each who fishes by line holds a
hand line, with copper hooks in the house to mend it (nothing gives bone yet).

Generated, not run: the live arms are launched by 37.2 on Zach's go (D2-333).
"""
from __future__ import annotations

import copy
import json
import os
import sys

ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

import yaml  # noqa: E402

SRC = os.path.join(os.path.dirname(__file__), "nutrition", "runs_high.yaml")
DAYS = 40                                      # u9 / build_plan live run 1: about 36 to 40 days
OLD_DAYS = 14                                  # D2-331: through the first autumn run (the eel window: autumn, days 4 to 11 here)
SKILLS = {                                     # u11 §4.1 and §7: the three households pinned
    "depth": "full",
    "households": {"Marsh": {"livelihoods": ["fisher"], "experts": ["weir_and_nets"]},
                   "Shepherd": {"livelihoods": ["fisher"], "experts": ["keeping"]},      # fowling postponed (D2-318)
                   "Brook": {"livelihoods": ["salter", "fisher"], "experts": ["the_pan"]}},
    "couple": {"capital_knowledge": True, "livelihood_land": True, "crafts_capital": True, "gates": True},
}
MEMORY = {"kept": {"words": 40, "schedule": "every", "every": 3, "most": 30}}   # D2-266, D2-308 (B9-2)
ROCK = {"name": "the Scar", "cover": "rock", "size": 1, "side": "south", "height": 2,
        "text": "a grey scar of rock above the copse, loose stone at its foot", "terrain": "rock outcrop", "soil": "stone",
        "ecosystem": "rock", "state": {"quarry": {"K": 1000.0, "S": 1000.0, "r": 0.0}}}
QUARRY_TO = "head"                             # C2's rock is reached only by one who can quarry: each head has a rough idea of it (a default
                                               # taken for this world: no mason lives here; reported)


def remake(src=SRC) -> tuple:
    from cybertron2.engine import livelihoods as LV
    w = yaml.safe_load(open(src))
    w["name"] = "eelmouth"
    w["days"] = DAYS
    w["prompt"] = "core"
    w["learning"] = "record"
    w["memory"] = copy.deepcopy(MEMORY)
    w["llm"] = {**(w.get("llm") or {}), "week_stop": 0.99}                  # D2-334
    w["skills"] = copy.deepcopy(SKILLS)
    nodes = w["nodes"]["Eelmouth"]["parcels"]
    # C1: the Salt House and the spring to the Brooks
    sh = w["buildings"].pop("marsh_salthouse")
    sh["household"] = "Brook"
    w["buildings"]["brook_salthouse"] = sh
    spring = sh["parcel"]
    nodes[spring]["holder"] = "Brook"
    for c in w.get("claims") or []:
        if c.get("thing") == ["parcel", spring] or c.get("thing") == f"parcel:{spring}":
            c["claimant"] = "Brook"
    # C2: a rock source within reach
    rid = "Eelmouth_10"
    nodes[rid] = dict(ROCK, adj=["Eelmouth_5", "Eelmouth_6"], land=copy.deepcopy(nodes["Eelmouth_6"].get("land") or {}))
    for q in ("Eelmouth_5", "Eelmouth_6"):
        nodes[q]["adj"] = sorted(set(nodes[q]["adj"]) | {rid})
    # the smoke huts: wattle huts of one set (D2-284, D2-291)
    for bid, b in w["buildings"].items():
        if (b.get("fittings") or {}).get("smoke racks"):
            b["fittings"]["smoke racks"] = 1
            b["rooms"] = [{"kind": "hut", "floor": 2}]
    for a in w["agents"].values():                                          # no "By trade: sowing" (u11 departure 8)
        a["trade"] = ""
    report = LV.fill(w)
    for n, a in w["agents"].items():                                        # C2: the rock within reach, and a hand that can quarry it
        if a.get("role") == QUARRY_TO and a.get("stage") == "adult":
            a["knows"]["quarry"] = {"level": "rough", "skill": 0.7}
    report["skipped"].append("C2: each head given a rough idea of quarrying, so the Scar's stone can be had (no mason here)")
    return w, report


def arms(world) -> dict:
    """The main arm and the comparison arm (D2-331)."""
    main = copy.deepcopy(world)
    for a in main["agents"].values():
        if a.get("kept"):
            a.pop("memories", None)                                         # the PE lines are kept lines (u11 departure 10)
    old = copy.deepcopy(world)
    old["name"] = "eelmouth_old"
    old["prompt"] = "old"
    old["days"] = OLD_DAYS
    old["skills"]["depth"] = "none"
    for a in old["agents"].values():
        a.pop("kept", None)                                                 # none of the new seeded lines
    return {"eelmouth": main, "eelmouth_old": old}


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(__file__), "nutrition")
    world, report = remake()
    from cybertron2.landgen import gate_check as GC
    for name, w in arms(world).items():
        path = os.path.join(out, f"{name}.yaml")
        with open(path, "w") as f:
            f.write(f"# {name}: Eelmouth remade (u11 §7), made by cybertron2/specs/make_eelmouth.py; see its docstring.\n")
            yaml.safe_dump(w, f, sort_keys=False, allow_unicode=True, width=200)
        gate = GC.check(w)
        rep = {"fill": report, "gate": gate}
        with open(os.path.join(out, f"{name}.report.json"), "w") as f:
            json.dump(rep, f, indent=1, default=str)
        print(name, "gate:", gate["verdict"], "refusals", len(gate["refuse"]), "warnings", len(gate["warn"]), flush=True)


if __name__ == "__main__":
    main()
