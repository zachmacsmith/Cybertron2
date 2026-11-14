"""The economy as a network, read from the engine's own tables (02zzg). CYB_ROOT = a checkout of the branch to read.

Nodes: goods (ITEMS); acts that make or get them (TECHNIQUES); fittings and rooms (FITTINGS, ROOMS) that some acts need;
sources (land covers, herds, wild kinds); and uses (what a good is for: eating, warmth, tools, weapons, scares, carrying, ...).
Edges: a good into an act, an act out to a good, a fitting or a tool enabling an act, a source feeding an act, a good serving a use.
Every edge comes from a table row; the few roles the tables do not hold as data (a hen lays, a cat keeps a store) are listed in
HAND below, with where the rule lives. Usage: CYB_ROOT=<checkout> python3 economy_graph.py <out.json>"""
import os, sys, json, subprocess
ROOT = os.environ["CYB_ROOT"]; sys.path.insert(0, ROOT)
from cybertron2.engine import data as D
from cybertron2.engine import forests as FO
from cybertron2.wild import methods as MT, plants as PL

T, I = D.TECHNIQUES, D.ITEMS
nodes, edges = {}, []
def node(i, kind, label, **kw): nodes.setdefault(i, {"id": i, "kind": kind, "label": label, **kw})
def edge(a, b, kind, qty=None, note=None): edges.append({"from": a, "to": b, "kind": kind, **({"qty": qty} if qty is not None else {}), **({"note": note} if note else {})})

ORIGIN = {"clappers": "brief 1 (scares)", "horn": "brief 1 (scares)", "antler": "brief 1 (scares)", "cat": "brief 2 (raiders)",
          "tallow": "brief 3 (carcasses)", "tallow light": "brief 3 (carcasses)", "offal": "brief 3 (carcasses)",
          "drying meat": "brief 4 (drying)", "dried meat": "brief 4 (drying)", "salt meat": "brief 4 (salting)",
          "beaver pelt": "wild sites (beaver)", "castoreum": "wild sites (beaver)", "rotting meat": "decay (D2-87)"}
for it, v in I.items():
    node("good:" + it, "good", it, pack=v.get("pack", "core"), food=v.get("food", 0.0), weight=v.get("weight"), spoil=v.get("spoil"),
         origin=ORIGIN.get(it, {"wild": "wild layer", "water": "water pack"}.get(v.get("pack"), "core economy")))

USES = {"eat": "eaten (food)", "warmth": "burned for warmth and cooking", "fodder": "fed to beasts", "seed": "sown as seed",
        "build": "built with", "tool": "a tool for work", "weapon": "a weapon for the hunt", "scare": "a scare for guarding a field",
        "carry": "carrying more", "sleep": "sleeping out", "light": "light for night work", "money": "money for trade and dues",
        "store": "keeps a store", "fish": "gear for fishing", "plough": "gear for ploughing", "manure": "manures a field"}
for u, lab in USES.items(): node("use:" + u, "use", lab)

def src(cover): node("src:" + cover, "source", cover, group="land"); return "src:" + cover

for tech, t in T.items():
    verb = t.get("verb")
    if verb in ("modifier",) or tech.startswith(("range:", "method:", "how:", "hidden:")):
        continue
    if verb == "build":
        continue                                                         # rooms and fittings below
    y = t.get("yield") or {}
    gives = t.get("gives")
    outs = dict(gives) if isinstance(gives, dict) else ({gives: None} if gives else {})
    yk = y.get("kind")
    if yk == "wild_take" or yk == "wild_den":
        outs = {}
        for k, w in (y.get("takes") or {}).items():
            node("src:wild:" + k, "source", k, group="wild")
            edge("src:wild:" + k, "proc:" + tech, "taken by", qty=w)
            for g in ((D.RESOURCES.get(k) or {}).get("taken") or {}).get("goods") or {}:
                outs[g] = None
    if yk == "wild_forage":
        outs = {p["item"]: None for p in PL.PLANTS.values() if p.get("item") in I}
    if yk == "slaughter":
        outs = {g: None for d in (y.get("gives") or {}).values() for g in d}
    if yk == "crop":
        outs = {"grain": None, "rye": None, "beans": None, "straw": None, "green grain": None, "green rye": None, "green beans": None}
    if yk == "sow":
        for s in ("grain", "rye", "beans"): edge("good:" + s, "use:seed", "use")
    if yk == "break":
        outs["stone"] = None                                             # ploughing turns up fieldstone
    if not outs and not t.get("inputs") and yk not in ("manure", "sow", "wild_watch", "wild_shut", "wild_pest", "wild_guard"):
        continue
    node("proc:" + tech, "process", tech, verb=verb, units=t.get("units"), label2=t.get("label", ""), pack=t.get("pack", "core"),
         trade=t.get("trade"), basic=t.get("basic"))
    for g, q in (t.get("inputs") or {}).items():
        if isinstance(q, dict):
            for g2, q2 in q.items():
                if ("good:" + g2) in nodes: edge("good:" + g2, "proc:" + tech, "input", q2, note="one of")
        elif ("good:" + g) in nodes:
            edge("good:" + g, "proc:" + tech, "input", q)
    for g, q in outs.items():
        if ("good:" + g) in nodes: edge("proc:" + tech, "good:" + g, "output", q)
    at = t.get("at") or {}
    for f in at.get("fittings") or []:
        node("fit:" + f, "fitting", f); edge("fit:" + f, "proc:" + tech, "needs")
    if yk not in ("wild_take", "wild_den"):
        for c in at.get("covers") or []:
            edge(src(c), "proc:" + tech, "where")
    for g, q in (t.get("uses") or {}).items():
        if ("good:" + g) in nodes: edge("good:" + g, "proc:" + tech, "gear", q)
    for lvl, f in (t.get("tools") or {}).items():
        g = {"crude": "crude tool", "copper": "copper tool"}.get(lvl)
        if g: edge("good:" + g, "proc:" + tech, "tool", f)
    wp = t.get("weapon") or {}
    if wp and wp.get("none", 1.0) < 1.0:
        edge("good:crude weapon", "proc:" + tech, "weapon", round(1.0 / max(wp["none"], 1e-9), 2), note="x take, armed against bare hands")
    for s in (y.get("scares") or []):
        for g in (s.get("uses") or {}):
            if ("good:" + g) in nodes: edge("good:" + g, "proc:" + tech, "scare")

for f, v in D.FITTINGS.items():
    node("fit:" + f, "fitting", f, does=v.get("does", ""), units=v.get("units"), trade=v.get("trade"), pack=v.get("pack", "core"))
    for g, q in (v.get("materials") or {}).items():
        if ("good:" + g) in nodes: edge("good:" + g, "fit:" + f, "material", q)
for r, v in D.ROOMS.items():
    node("room:" + r, "fitting", r, does=f"a room: {v.get('floor')} floor, {v.get('places')} places")
    for build, spec in v.items():
        if isinstance(spec, dict) and "materials" in spec:
            for g, q in spec["materials"].items():
                if ("good:" + g) in nodes: edge("good:" + g, "room:" + r, "material", q, note=build)

# herds: the beasts that milking, slaughter and dung come from
node("src:herd", "source", "cattle", group="herd")
for p in ("milk", "slaughter", "dung"):
    if "proc:" + p in nodes: edge("src:herd", "proc:" + p, "from")

# uses read from the tables
for it, v in I.items():
    g = "good:" + it
    if v.get("food"): edge(g, "use:eat", "use", v["food"])
    h = FO.heat_of({it: 1})
    if h: edge(g, "use:warmth", "use", h)
for g in D.TOOLS: edge("good:" + g, "use:tool", "use")
for g in D.WEAPONS: edge("good:" + g, "use:weapon", "use")
for s in MT.SCARES:
    for g in (s.get("uses") or {}): edge("good:" + g, "use:scare", "use")
for it, v in I.items():
    if v.get("carry"): edge("good:" + it, "use:carry", "use", v["carry"])
# roles the tables hold as rules elsewhere (where each lives)
HAND = [("hay", "fodder", "herds eat hay in winter (herds.py, HERDS)"), ("grain", "fodder", "beasts fed grain (herds.py)"),
        ("pack", "carry", "carry +10 on foot (PHYSICS carry)"), ("bedroll", "sleep", "sleeping out (night.py _gear, D2-68)"),
        ("tent", "sleep", "sleeping out (night.py _gear, D2-68)"), ("tallow light", "light", "night work on wild acts (wild.py LIGHT)"),
        ("coin", "money", "trade and agreements (D2-34)"), ("cat", "store", "keeps mice off a store (wild.py _store_beasts)"),
        ("dung", "manure", "manure acts on fields (TECHNIQUES manure)"), ("fishing rod", "fish", "angling (TECHNIQUES angle uses)"),
        ("wooden plough", "plough", "ploughing (TECHNIQUES plough uses)"), ("harness", "plough", "ploughing (TECHNIQUES plough uses)"),
        ("timber", "build", "rooms and fittings"), ("stone", "build", "rooms and fittings"), ("straw", "build", "beds")]
for g, u, note in HAND:
    if "good:" + g in nodes: edge("good:" + g, "use:" + u, "use", note=note)
# a hen in the store lays eggs (wild.py _hens_lay)
node("proc:hens lay", "process", "hens lay", verb="night", label2="hens in a store lay eggs each night (wild.py _hens_lay)", pack="wild")
edge("good:hen", "proc:hens lay", "input", note="kept, not used up"); edge("proc:hens lay", "good:egg", "output")
# a carcass's offal and a hunt's leavings
edge("proc:slaughter", "good:offal", "output")
# the rack's nights (night.py: drying meat becomes dried meat at half the weight after 3 nights)
node("proc:on the rack", "process", "on the rack", verb="night", label2="3 nights on the rack: drying meat becomes dried meat at half the weight (night.py)", pack="core")
edge("good:drying meat", "proc:on the rack", "input"); edge("proc:on the rack", "good:dried meat", "output", 0.5)
# decay (night.py decay_rate, D2-87): fresh meat left turns to rotting meat
node("proc:decay", "process", "decay", verb="night", label2="fresh meat left out turns to rotting meat (night.py, D2-87)", pack="core")
edge("good:meat", "proc:decay", "input"); edge("proc:decay", "good:rotting meat", "output")
# a cat comes to a store with mice by itself, or is found (wild.py _store_beasts, D2-206)
node("src:comes by itself", "source", "comes by itself or is found", group="wild")
edge("src:comes by itself", "good:cat", "output")
# the beaver lodge's trap (wild/kinds.py SITES beaver: trap gives a pelt and castoreum)
node("src:wild:beaver", "source", "beaver (a lodge)", group="wild")
node("proc:trap beavers", "process", "trap beavers", verb="work", label2="den work at a beaver lodge (wild.py site_work)", pack="wild")
edge("src:wild:beaver", "proc:trap beavers", "taken by"); edge("proc:trap beavers", "good:beaver pelt", "output"); edge("proc:trap beavers", "good:castoreum", "output")

sha = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
br = subprocess.run(["git", "-C", ROOT, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
used = {e["from"] for e in edges} | {e["to"] for e in edges}
out = {"source": {"commit": sha, "branch": br}, "nodes": [n for k, n in nodes.items() if k in used or n["kind"] == "good"], "edges": edges}
json.dump(out, open(sys.argv[1], "w"), indent=0)
print(len(out["nodes"]), "nodes,", len(edges), "edges, from", br, sha)
