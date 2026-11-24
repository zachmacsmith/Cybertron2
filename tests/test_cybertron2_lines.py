"""The founders' seeded lines for every built livelihood (W-105; u9_people.md §5.5, §5.6; D2-268): each template renders on a fixture
village holding every built livelihood with its holdings, each stated figure checked against the engine's data or the state it reads;
on a bare village every conditional line drops (reported, never a stand-in); every id the rows name has a template; every founder fits
the cap (D2-308). Interface tests (D2-298): no model calls."""
import copy

import pytest

from cybertron2.engine import founders as FD, gear as GE, livelihoods as LV, process as PROC
from cybertron2.engine.data import CROPS, FITTINGS, HERDS, ITEMS, PHYSICS, TECHNIQUES as T, WATER_WORKS


def _p(name, cover, size=1, **kw):
    return {"name": name, "cover": cover, "size": size, **kw}


def _house(name, parcel, hh, structure="wattle", **fit):
    return {"name": name, "parcel": parcel, "household": hh, "structure": structure,
            "fittings": {"beds": 4, "hearth": 1, "bins": 1, **fit}, "stock": {"grain": 40, "beans": 10, "firewood": 10}}


# households: (id, livelihoods, people [(name, stage, role, sex)], pinned experts, pinned capable, home node)
HOUSES = [
    ("Marsh", ["fisher"], [("Peter", "adult", "head", "m"), ("Nichola", "adult", None, "f"), ("Hawise", "adult", None, "f"),
                           ("Nigel", "youth", None, "m")], ["weir_and_nets", "keeping"], [], "wendle"),
    ("Brook", ["salter", "fisher"], [("Oliver", "adult", "head", "m"), ("Katherine", "adult", None, "f"), ("Osbert", "elder", None, "m"),
                                     ("Petronel", "youth", None, "f")], ["the_pan", "salting", "carrying"], [], "wendle"),
    ("Hobb", ["farmer"], [("Ralph", "adult", "head", "m"), ("Agnes", "adult", None, "f"), ("Walter", "adult", None, "m"),
                          ("Alan", "adult", None, "m"), ("Emma", "adult", None, "f"), ("Hugh", "youth", None, "m"),
                          ("Joan", "child", None, "f")], ["seed_and_harvest", "ploughman", "hedge_and_field"], ["Emma"], "wendle"),
    ("Hayward", ["herder"], [("Robert", "adult", "head", "m"), ("Mabel", "adult", None, "f"), ("Geoffrey", "adult", None, "m"),
                             ("Cecily", "adult", None, "f")], ["stock", "dairy", "hay_and_winter"], ["Cecily"], "wendle"),
    ("Smith", ["smith"], [("Simon", "adult", "head", "m"), ("Alice", "adult", None, "f"), ("Martin", "adult", None, "m"),
                          ("Isabel", "adult", None, "f")], ["smelting", "mining_and_charcoal", "fittings"], ["Isabel"], "wendle"),
    ("Miller", ["miller"], [("William", "adult", "head", "m"), ("Matilda", "adult", None, "f"), ("Roger", "adult", None, "m")],
     ["the_mill", "the_oven"], ["Roger"], "wendle"),
    ("Wright", ["builder"], [("John", "adult", "head", "m"), ("Margaret", "adult", None, "f"), ("Thomas", "adult", None, "m")],
     ["wright", "mason"], ["Thomas"], "wendle"),
    ("Wood", ["woodsman"], [("Henry", "adult", "head", "m"), ("Edith", "adult", None, "f")], ["charcoal"], ["Edith"], "wendle"),
    ("Willow", ["basket maker"], [("Adam", "adult", "head", "m"), ("Beatrice", "adult", None, "f")], ["traps_and_creels"], ["Beatrice"],
     "wendle"),
    ("Roper", ["cord and nets", "trader"], [("Richard", "adult", "head", "m"), ("Sarah", "adult", None, "f"), ("Nicholas", "adult", None, "m")],
     ["flax_and_linen", "nets"], ["Nicholas"], "wendle"),
    ("Carter", ["trader"], [("Gilbert", "adult", "head", "m"), ("Lucy", "adult", None, "f"), ("Bartholomew", "adult", None, "m")],
     ["the_road", "the_market"], ["Bartholomew"], "wendle"),
    ("Hunt", ["hunter"], [("Godfrey", "adult", "head", "m"), ("Avice", "adult", None, "f"), ("Ivo", "adult", None, "m")],
     ["stalking", "snares"], ["Ivo"], "thorpe"),
    ("Cotter", ["cottager"], [("Wat", "adult", "head", "m"), ("Maud", "adult", None, "f")], [], ["Maud"], "thorpe"),
]


def village():
    """The fixture: Wendle (fields, a common, a wood, a fen, a river with eels, rock with ore and stone, a saltmarsh), Thorpe a day
    off (a wood with game), the Holt a day beyond; thirteen households, one for each built livelihood (the trader also as a second
    living), each with its holdings."""
    w = {"name": "wendle", "seed": 3, "calendar": {"season": "summer", "day": 0, "season_days": 8}, "children": {"on": True, "dial": "low"},
         "packs": ["wild", "water", "farming"], "lifespan": 64, "wild": {"kinds": ["wolf", "red deer", "brown bear", "woodpigeon"]},
         "nodes": {}, "roads": [], "buildings": {}, "herds": {}, "claims": [], "agents": {}, "tree": [], "history": []}
    w["nodes"]["wendle"] = {"name": "Wendle", "parcels": {
        "w0": _p("the Green", "built", 6),
        "w1": _p("the Long Field", "field", 4, holder="Hobb", fertility=1.1,
                 state={"crop": {"kind": "barley", "left": 100, "ripe_day": 5}, "last_crop": "legumes"}),
        "w2": _p("the Infield", "field", 2, holder="Hobb", fertility=0.7, state={"last_crop": "fallow"}),
        "w3": _p("the Common", "pasture", 3, state={"grass": {"K": 90, "S": 70, "r": 0.32}}),
        "w4": _p("Mill Mead", "meadow", 2, holder="Miller"),
        "w5": _p("the Hanger", "forest", 3, state={"wood": {"kind": "managed wood"}, "game": {"K": 10, "S": 8, "r": 0.25}}),
        "w6": _p("Withy Fen", "fen", 2),
        "w7": _p("the Wend", "water", 2, land={"river": "river"}, state={"fish": {"K": 40, "S": 40, "r": 0.1}}),
        "w8": _p("the Scar", "rock", 1, state={"seam": {"K": 200, "S": 200, "r": 0.0}, "quarry": {"K": 1000, "S": 1000, "r": 0.0}}),
        "w9": _p("Salt Marsh", "saltmarsh", 2, holder="Brook", state={"salt": {"K": 20, "S": 20, "r": 0.0}})}}
    w["nodes"]["thorpe"] = {"name": "Thorpe", "parcels": {
        "t0": _p("Thorpe Green", "built", 2),
        "t2": _p("Thorpe Common", "pasture", 2, state={"grass": {"K": 40, "S": 40, "r": 0.32}}),
        "t1": _p("Thorpe Wood", "forest", 2, state={"wood": {"kind": "copse"}, "game": {"K": 8, "S": 8, "r": 0.25}})}}
    w["nodes"]["holt"] = {"name": "the Holt", "parcels": {
        "h0": _p("the Holt", "forest", 4, state={"wood": {"kind": "old forest"}, "game": {"K": 14, "S": 12, "r": 0.25}})}}
    w["roads"] = [["wendle", "thorpe", 1, {"way": "the track along the river", "stretches": {1: {"landmarks": ["ford"]}}}],
                  ["thorpe", "holt", 1, {"way": "a path into the trees"}]]
    for hh, livs, people, experts, capable, node in HOUSES:
        green = "w0" if node == "wendle" else "t0"
        w["buildings"][f"{hh.lower()}_house"] = _house(f"{hh} House", green, hh)
        head, partner = people[0][0], people[1][0]
        w["history"].append({"text": f"{head} and {partner} {hh} came to {w['nodes'][node]['name']} and built the first {hh} house",
                             "who": [head, partner], "day": -20})
        for k, (n, st, role, sex) in enumerate(people):
            born = {"adult": -40 + k, "elder": -55, "youth": -20, "child": -6, "infant": -1}[st]
            a = {"household": hh, "born": born, "stage": st, "sex": sex, "relations": {}, "knows": {}, "holdings": {}}
            if role:
                a["role"] = role
            if n == partner:
                a["partner"] = head
            if n == head:
                a["partner"] = partner
            if st in ("youth", "child"):
                a["parents"] = [head, partner]
            w["agents"][n] = a
    w["history"] += [{"text": "a hard winter: the frost came early and the stores ran out", "kind": "winter", "who": [], "day": d}
                     for d in (-45, -10)]
    b = w["buildings"]
    b["marsh_weir"] = {"name": "the weir", "parcel": "w7", "household": "Marsh", "monument": "weir", "structure": "timber",
                       "sections": [{"m": "timber", "level": 5}, {"m": "wattle", "level": 4}]}
    b["marsh_smokehouse"] = {"name": "the Marsh Smokehouse", "parcel": "w0", "household": "Marsh", "structure": "wattle",
                             "fittings": {"smoke racks": 1}, "stock": {}}
    b["hayward_house"]["fittings"]["cellar"] = 1
    b["brook_salthouse"] = {"name": "the Salt House", "parcel": "w9", "household": "Brook", "structure": "wattle",
                            "fittings": {"brine pan": 1}, "stock": {"salt": 12}}
    b["hobb_byre"] = {"name": "the Hobb Byre", "parcel": "w0", "household": "Hobb", "structure": "wattle", "fittings": {"stalls": 2},
                      "stock": {"hay": 20, "wooden plough": 1, "harness": 2}}
    b["smith_forge"] = {"name": "the Forge", "parcel": "w0", "household": "Smith", "structure": "stone",
                        "fittings": {"hearth": 1, "anvil": 1}, "stock": {"charcoal": 3}}
    b["miller_mill"] = {"name": "Wendle Mill", "parcel": "w4", "household": "Miller", "structure": "timber",
                        "fittings": {"millstones": 1, "water wheel": 1}, "stock": {}}
    b["miller_bakehouse"] = {"name": "the Bakehouse", "parcel": "w0", "household": "Miller", "structure": "stone",
                             "fittings": {"oven": 1}, "stock": {}}
    w["herds"]["hobb_oxen"] = {"name": "the Hobb oxen", "kind": "cattle", "parcel": "w3", "cows": 0, "oxen": 2, "bulls": 0, "young": 0,
                               "in_milk": 0, "holder": "Hobb"}
    w["herds"]["hayward_cattle"] = {"name": "the Hayward cattle", "kind": "cattle", "parcel": "w3", "cows": 4, "oxen": 0, "bulls": 1,
                                    "young": 1, "in_milk": 2, "holder": "Hayward"}
    w["skills"] = {"depth": "full",
                   "households": {hh: {"livelihoods": livs, "experts": experts, "experts_n": len(experts)} for hh, livs, _, experts, _, _ in HOUSES},
                   "agents": {n: {"band": "capable"} for _, _, _, _, cap, _ in HOUSES for n in cap}}
    return w


def bare():
    """The same households on a village with nothing their conditions read: no fields, no common, no wood, no water, no rock, no
    saltmarsh, no other place, no wild kinds, no holdings."""
    w = village()
    w["nodes"] = {"wendle": {"name": "Wendle", "parcels": {"w0": _p("the Green", "built", 6)}}}
    w["roads"] = []
    w["wild"] = {"kinds": []}
    w["herds"] = {}
    w["buildings"] = {bid: dict(b, parcel="w0", fittings={"beds": 4, "fire ring": 1}) for bid, b in w["buildings"].items() if bid.endswith("_house")}
    return w


@pytest.fixture(scope="module")
def filled():
    w = village()
    rep = LV.fill(w)
    return w, rep


@pytest.fixture(scope="module")
def emptied():
    w = bare()
    rep = LV.fill(w)
    return w, rep


def line(world, rep, who, i):
    return FD.render(world, who, rep, ids=[i])["lines"].get(i)


def keeper_of(rep, hh, kind):
    hr = rep["households"][hh]
    return hr["keepers"][hr["holds"][kind][0]]


def expert_of(rep, hh, sp):
    return rep["households"][hh]["experts"][sp]


# ---------------------------------------------------------------------- the wiring
BUILT = [lv for lv, r in LV.ROWS.items() if r.get("status") == "built"]


def _row_ids(r):
    ids = [i for band in r["lines"].values() for i in band]
    ids += [i for sp in r["specialisms"].values() for i in sp.get("lines") or []]
    ids += list((r.get("keeper_lines") or {}).values())
    return ids


def test_every_id_a_built_livelihood_names_has_a_template_and_every_livelihood_a_neighbour_line():
    missing = sorted({i for lv in BUILT for i in _row_ids(LV.ROWS[lv]) if i not in FD.TEMPLATES})
    assert not missing, missing
    assert sorted(set(BUILT) - set(FD.NB)) == []
    for kind, h in LV.HOLDINGS.items():
        if h.get("keeper_line"):
            assert h["keeper_line"] in FD.TEMPLATES and h["keeper_line"] in FD.KEEPER, kind
    assert {p for lv in BUILT for i in _row_ids(LV.ROWS[lv]) for p in [i[:2]]} <= set(FD.SOURCE)
    assert not any(k.startswith(("FO", "TA")) for k in FD.TEMPLATES)                      # D2-318, D2-327: deferred


def test_the_fill_finds_fields_an_ox_team_and_a_herd_and_names_their_keepers(filled):
    w, rep = filled
    hobb = rep["households"]["Hobb"]
    assert hobb["holds"]["fields"] == ["field:w1", "field:w2"] and hobb["holds"]["ox pair"] == ["oxen:hobb_oxen"]
    assert keeper_of(rep, "Hobb", "fields") == expert_of(rep, "Hobb", "seed_and_harvest")
    assert keeper_of(rep, "Hobb", "ox pair") == expert_of(rep, "Hobb", "ploughman")
    assert keeper_of(rep, "Hayward", "herd") == expert_of(rep, "Hayward", "stock")
    assert "herd" not in rep["households"]["Hobb"]["holds"] and "ox pair" not in rep["households"]["Hayward"]["holds"]   # a team
    assert rep["households"]["Hayward"]["holds"]["herd"] == ["herd:hayward_cattle"]                                     # is no herd
    assert w["agents"][keeper_of(rep, "Hobb", "ox pair")]["livelihood"].endswith("and you keep the ox team.")
    assert "keeper" not in w["herds"]["hobb_oxen"]                                       # only buildings record a keeper
    assert not any(d.get("built") is False and s in rep["households"][hh]["experts"]
                   for hh, h in rep["households"].items() for lv in h["livelihoods"][:1]
                   for s, d in LV.ROWS[lv]["specialisms"].items())                        # a waiting specialism is never drawn


def test_every_id_wanted_can_produce_has_a_template(filled):
    """G66: nothing is skipped silently: every id `wanted` gives anyone on the fixture or in Eelmouth (base, people, head's, the
    livelihoods' bands and specialisms, keeper lines, HL, neighbours) is a template or a neighbour line of a built livelihood."""
    from cybertron2.specs import make_eelmouth as M
    w, rep = filled
    ew, erep = M.remake()
    for world, r in ((w, rep), (ew, erep)):
        for n in world["agents"]:
            for i in FD.wanted(world, n, r):
                if i.startswith("NB-"):
                    assert i[3:].split(":")[0] in FD.NB, (n, i)
                elif i.startswith("NV-"):                                      # D2-349: another village's household
                    assert i[3:].split(":")[0] in LV.ROWS, (n, i)
                else:
                    assert i in FD.TEMPLATES, (n, i)
    import inspect
    import re
    src = inspect.getsource(FD.wanted)
    literal = set(re.findall(r'"((?:BS|PE|HH|HL)\d*)"', src)) | {"BS%d" % k for k in range(1, 10)}
    assert sorted(i for i in literal if i not in FD.TEMPLATES) == []


@pytest.mark.parametrize("kind", [k for k, h in LV.HOLDINGS.items() if h.get("keeper_line")])
def test_each_holdings_keeper_gets_its_keeper_line(filled, kind):
    """G63: the keeper dispatch reads the rows' keeper_lines and the holdings registry: every kind with a keeper line, held on the
    fixture, reaches its keeper (protected, as a holding)."""
    w, rep = filled
    hh = next(h for h, x in rep["households"].items() if x["holds"].get(kind) and (h != "Hobb" or kind != "herd"))
    k = keeper_of(rep, hh, kind)
    kl = FD.keeper_line(kind, rep["households"][hh]["livelihoods"])
    assert kl == LV.HOLDINGS[kind]["keeper_line"] and kl in FD.wanted(w, k, rep)
    assert kl in rep["lines"][k]["ids"], (kind, k, rep["lines"][k])
    assert next(y for y in w["agents"][k]["kept"] if y["text"] == line(w, rep, k, kl))["source"] == "a holding"
    keeps = {who for ref, who in rep["households"][hh]["keepers"].items() if ref in rep["households"][hh]["holds"][kind]}
    assert all(line(w, rep, n, kl) is None for n in w["agents"] if w["agents"][n].get("household") == hh and n not in keeps)


def test_the_heads_seed_and_stores_lines_and_the_elders_winters(filled, emptied):
    w, rep = filled
    hh2 = line(w, rep, "Ralph", "HH2")
    plots = 4 + 2
    assert hh2.startswith(f"Next year's {plots} plots want about {plots * PHYSICS['farming']['plot_seed']:g} kilos of seed")
    assert line(w, rep, "Simon", "HH2") is None                                        # no fields
    hh4 = line(w, rep, "Simon", "HH4")
    assert "a cat or a barn owl keeps them down" in hh4 and hh4.endswith("The bins at Smith House hold about 300 kilos.")
    pe3 = line(w, rep, "Osbert", "PE3")
    assert pe3 == "I have seen 2 hard winters, the last of them last winter: the frost came early and the stores ran out."
    assert line(w, rep, "Oliver", "PE3") is None                                       # not an elder
    w2 = copy.deepcopy(w)
    w2["history"] += [{"text": "a hard winter", "kind": "winter", "who": [], "day": -12}]   # two in one world year: no facts
    assert line(w2, rep, "Osbert", "PE3") is None
    assert "PE3" in FD.wanted(w, "Osbert", rep) and "HH2" in FD.wanted(w, "Ralph", rep) and "HH4" in FD.wanted(w, "Ralph", rep)


# ---------------------------------------------------------------------- each line, rendered and checked against what it reads
def test_every_built_template_fires_on_the_fixture(filled):
    w, rep = filled
    fired = set()
    for n in w["agents"]:
        r = FD.render(w, n, rep)
        fired |= {i.split("-")[0] if i.startswith("NB-") else i for i in r["lines"]}
        fired |= {f"NB-{i[3:].split(':')[0]}" for i in r["lines"] if i.startswith("NB-")}
    waits = {"FI13", "FI14", "HU8", "BU5", "WO3", "WO4", "BA2", "BA4", "BA5", "CO3"}     # [built: x] the engine lacks
    waits |= {"MI4"}                                    # a run going up past the mill: the fixture has no wild land (W-111; below)
    mine = {i for i in FD.TEMPLATES if i[:2] in ("FA", "HE", "HU", "SM", "MI", "BU", "WO", "BA", "CO", "TR", "CT")} | {"SA6", "SA7"}
    assert sorted(mine - waits - fired) == []
    assert sorted(f"NB-{lv}" for lv in BUILT if f"NB-{lv}" not in fired) == []
    for i in waits:                                                                      # never rendered while the engine lacks them
        assert i not in fired


def test_the_farmers_lines_state_the_engines_figures(filled):
    w, rep = filled
    f = PHYSICS["farming"]
    ralph = "Ralph"
    fa1, fa2 = line(w, rep, ralph, "FA1"), line(w, rep, ralph, "FA2")
    from cybertron2.engine import lore as LO
    lore = LO.text("sowing")
    assert fa1.startswith("Barley does best sown in spring, and well early in summer or late in winter") and fa1.split(";")[0] in lore
    assert "Rye does best sown late in autumn" in fa2 and "beans do best sown early in summer" in fa2 and "wants a winter" in fa2
    assert f"{f['plot_seed']:g} kilos of seed" in line(w, rep, ralph, "FA3") and "ripens sooner" in line(w, rep, ralph, "FA3")
    assert "a third of what is growing" in line(w, rep, ralph, "FA4") and abs(f["frost_loss"] - 1 / 3) < 0.04
    fa5 = line(w, rep, ralph, "FA5")
    assert f"more than {int(f['window'])} days" in fa5 and "a quarter each night" in fa5 and CROPS["grain"]["green"] in fa5
    fa6 = line(w, rep, ralph, "FA6")
    assert T["reap"]["tools"]["copper"] == 1.5 and "reaps half as much again" in fa6
    assert T["fell"]["tools"]["copper"] == 2.0 and "fells twice as much" in fa6 and "four times as fast as a hoe" in fa6
    plougher = keeper_of(rep, "Hobb", "ox pair")
    fa7 = line(w, rep, plougher, "FA7")
    assert f"a plot in {1 / T['plough']['yield']['plots']:g} units where a hoe takes {1 / T['hoe']['yield']['plots']:g}" in fa7
    assert "a fifth less in stalls" in fa7 and FITTINGS["stalls"]["fodder"] == 0.8
    assert line(w, rep, ralph, "FA8").startswith("Barley and rye sown year on year tires the ground; beans give it back")
    sower = keeper_of(rep, "Hobb", "fields")
    fa9 = line(w, rep, sower, "FA9")
    assert fa9 == "The Long Field stands in barley, beans last year, its soil rich; the Infield lies empty, rested last year, its soil tired."
    assert "Wendle Mill grinds for those who bring it grain" in line(w, rep, ralph, "FA10")
    assert "in spring and again in autumn" in line(w, rep, ralph, "FA11")
    assert line(w, rep, "Robert", "FA7") is None and line(w, rep, "Walter" if sower != "Walter" else "Alan", "FA9") is None


def test_the_herders_lines_state_the_engines_figures(filled):
    w, rep = filled
    he1 = line(w, rep, "Robert", "HE1")
    assert "most in summer, half as much in spring" in he1 and "none in winter" in he1
    assert f"after about {PHYSICS['cattle']['starve_nights']} hungry nights" in he1
    assert "all winter and into the first days of spring" in line(w, rep, "Robert", "HE3") and "a fence" in line(w, rep, "Robert", "HE3")
    assert "fen half as well" in line(w, rep, "Robert", "HE4") and PHYSICS["cattle"]["grazing"]["fen"] == 0.5
    he5 = line(w, rep, "Robert", "HE5")
    assert f"{T['cheese']['inputs']['milk']:g} kilos of it" in he5 and f"about {round(T['cheese']['gives']['cheese'])} of cheese" in he5
    assert he5.endswith(f"cheese keeps {FD._keep('cheese')}.")
    assert line(w, rep, "Robert", "HE6") is not None
    he7 = line(w, rep, keeper_of(rep, "Hayward", "herd"), "HE7")
    assert he7 == "Our herd is 4 cows, a bull and a calf, kept on the Common; 2 of the cows are in milk."
    assert "our 6 beasts want about 48 bundles for the 8 nights of winter" in line(w, rep, "Robert", "HE8")


def test_the_hunters_lines_state_the_engines_figures(filled):
    w, rep = filled
    hu1 = line(w, rep, "Godfrey", "HU1")
    assert all(x in hu1 for x in T["snare"]["at"]["covers"]) and "never in the wood" in hu1
    assert f"about {PHYSICS['carry']['foot']:g} kilos" in line(w, rep, "Godfrey", "HU2")
    hu3 = line(w, rep, "Godfrey", "HU3")
    assert hu3.startswith("In autumn the stags roar") and "early in summer the hinds drop their calves" in hu3
    hu4 = line(w, rep, "Godfrey", "HU4")
    assert "the wolf and, in a hungry spring, the bear" in hu4 and f"goes off in {FD._keep('meat')}" in hu4
    assert line(w, rep, "Godfrey", "HU6") == "The Holt, a day off, holds game; a camp there saves the walk home each night."
    hu7 = line(w, rep, "Godfrey", "HU7")
    assert f"about {round(1 / GE.RECIPES['snares']['inputs']['cord'])} to a kilo" in hu7
    assert GE.LIVES["snare"]["torn"] == 1 / 6 and "one night in six" in hu7


def test_the_salters_new_lines(filled):
    w, rep = filled
    sa6 = line(w, rep, expert_of(rep, "Brook", "carrying"), "SA6")
    assert f"about {PHYSICS['carry']['foot']:g} kilos" in sa6 and f"{PHYSICS['carry']['foot'] + ITEMS['pack']['carry']:g} with a pack" in sa6
    assert "Thorpe, a day off, has meat, hide and labour"[:10] in sa6 and "no salt" in sa6
    sa7 = line(w, rep, "Oliver", "SA7")
    assert sa7.startswith("The pans on Salt Marsh make salt in the sun: most in summer") and "none in winter" in sa7


def test_the_smiths_lines_state_the_engines_figures(filled):
    w, rep = filled
    sm1 = line(w, rep, "Simon", "SM1")
    assert T["charcoal"]["inputs"]["timber"] == 5 and sm1.startswith("Five loads of timber") and "as much as six loads of timber" in sm1
    assert T["smelt"]["inputs"]["fuel"] == {"charcoal": 1, "timber": 6}
    sm2 = line(w, rep, "Simon", "SM2")
    assert "half as much again as a crude one, twice as much at felling, and lasts four times as long" in sm2
    assert "the plough, the salter's pan and the fishers' hooks all want copper" in sm2
    assert "take twice as many" in line(w, rep, "Simon", "SM3")
    sm4 = line(w, rep, keeper_of(rep, "Smith", "forge"), "SM4")
    assert sm4 == "Our forge at the Forge has an anvil and bellows on its hearth; it burns charcoal by the sack, and holds 3 sacks now."
    sm5 = line(w, rep, "Simon", "SM5")
    assert "at the Scar, and wants a tool" in sm5 and "9 kilos of ore and a sack of charcoal smelt to a kilo of copper" in sm5
    sm6 = line(w, rep, "Simon", "SM6")
    assert "The Brooks' pan" in sm6 and "the Hobbs' plough" in sm6 and "the Millers' mill wheel" in sm6 and "the fishers' hooks" in sm6


def test_the_millers_lines_state_the_engines_figures(filled, monkeypatch):
    w, rep = filled
    mi1 = line(w, rep, "William", "MI1")
    assert "about half as far again" in mi1 and f"flour keeps {FD._keep('flour')}, grain {FD._keep('grain')}" in mi1
    assert "in summer" in line(w, rep, "William", "MI2")
    mi3 = line(w, rep, keeper_of(rep, "Miller", "mill"), "MI3")
    assert f"up to {T['water mill']['inputs']['grain']:g} kilos" in mi3 and "once a year" in mi3
    assert f"after about {FITTINGS['millstones']['wear']['life']:g} kilos ground" in mi3
    assert line(w, rep, keeper_of(rep, "Miller", "mill"), "MI4") is None     # no run passes a world without the wild land (W-111)
    monkeypatch.setattr(FD, "_runs_at", lambda world, node, kind: True)         # with a run going up past the mill
    mi4 = line(w, rep, keeper_of(rep, "Miller", "mill"), "MI4")
    assert WATER_WORKS["mill"]["stop"] == 0.5 and "half the fish going up are held below" in mi4 and "turns at half" in mi4
    mi5 = line(w, rep, keeper_of(rep, "Miller", "oven"), "MI5")
    assert f"up to {T['oven bread']['inputs']['flour']:g} kilos of flour" in mi5 and f"{T['oven bread']['inputs']['firewood']:g} bundles" in mi5
    assert f"after about {FITTINGS['oven']['wear']['life']} firings" in mi5


def test_the_builders_lines_state_the_engines_figures(filled):
    w, rep = filled
    assert "wattle fastest" in line(w, rep, "John", "BU1")
    bu3 = line(w, rep, "John", "BU3")
    assert bu3.endswith("at Wright House the bins hold about 300 kilos.")
    assert "about half the days" in line(w, rep, "John", "BU4")
    bu6 = line(w, rep, "John", "BU6")
    assert bu6.startswith("The mill's wheel, the plough and the handcart are a wright's work") and "the Millers" in bu6
    assert line(w, rep, "John", "BU7") == "Stone lies only where the rock shows, at the Scar; quarrying wants a tool."
    bu8 = line(w, rep, "John", "BU8")
    assert f"A hearth wants {FITTINGS['hearth']['materials']['stone']:g} stones and an oven {FITTINGS['oven']['materials']['stone']:g}" in bu8
    assert "a tenth as fast as wattle" in bu8


def test_the_woodsmans_basket_makers_and_cord_lines(filled):
    w, rep = filled
    assert "the Hanger comes again in a few years" in line(w, rep, "Henry", "WO1")
    wo2 = line(w, rep, "Henry", "WO2")
    assert ITEMS["charcoal"]["heat"] / ITEMS["firewood"]["heat"] == 4 and "as long as four bundles of firewood" in wo2
    assert line(w, rep, "Henry", "WO5") in ("The Brooks here want firewood for the pan.", "The Smiths here want charcoal for the forge.")
    ba1 = line(w, rep, "Adam", "BA1")
    assert "a third as much in summer" in ba1 and "harms the stools" in ba1
    ba3 = line(w, rep, "Adam", "BA3")
    assert f"{GE.ITEMS['creel']['carry']:g} kilos more" in ba3 and "about 25 kilos where hands carry 10" in ba3
    co1 = line(w, rep, "Richard", "CO1")
    assert "most in summer and autumn" in co1 and "a kilo in about 4 days" in co1
    assert "up to a quarter of a plot" in line(w, rep, "Richard", "CO2")
    co4 = line(w, rep, "Richard", "CO4")
    assert "a night in still water or 3 on the grass" in co4 and f"{1 / T['dress and spin']['gives']['cord']:g} kilos of retted flax" in co4
    co5 = line(w, rep, "Richard", "CO5")
    assert "rots in about 16 nights" in co5 and GE.LIVES["gill net"]["rot"][0] * 32 == 16


def test_the_traders_and_cottagers_lines(filled):
    w, rep = filled
    tr1 = line(w, rep, "Gilbert", "TR1")
    assert tr1 == "Thorpe, a day off, has meat and hide, and lacks salt."
    tr2 = line(w, rep, "Gilbert", "TR2")
    assert f"about {HERDS['pack_ox']['carry']:g} kilos" in tr2 and f"about {PHYSICS['carry']['foot'] + ITEMS['handcart']['carry']:g}" in tr2
    assert line(w, rep, "Gilbert", "TR3") == "The road to Thorpe is a day, the track along the river, with a ford on it."
    assert line(w, rep, "Gilbert", "TR4").endswith("salt, copper ore and stone only at Wendle.")
    assert line(w, rep, "Wat", "CT1").startswith("We hold a cottage and no field")
    ct2 = line(w, rep, "Wat", "CT2")
    assert "the Marshs at the eel run in autumn" in ct2 or "at reaping in summer" in ct2
    assert line(w, rep, "Wat", "CT3").startswith("What Thorpe Common gives, grass for a beast")
    assert "spin and make baskets" in line(w, rep, "Wat", "CT4")
    nb = FD.render(w, "Wat", rep, ids=["NB-trader:Carter"])["lines"]["NB-trader:Carter"]
    assert nb == "Gilbert of the Carters carries between Wendle and Thorpe; ask them for what is not made here."


def test_the_holdings_lines_name_every_holding_and_its_keeper(filled):
    w, rep = filled
    hl = line(w, rep, "Hugh", "HL")
    assert "the Long Field and the Infield, which" in hl and "the ox team and plough, which" in hl and "beasts on" not in hl
    assert len(hl.split()) <= FD.LINE_WORDS
    assert "Wendle Mill on Mill Mead, which" in line(w, rep, "Matilda", "HL") and "the Bakehouse, where" in line(w, rep, "Matilda", "HL")


# ---------------------------------------------------------------------- conditions false: each line drops, never a stand-in
CONDITIONAL = ["FA1", "FA2", "FA7", "FA9", "FA10", "HE3", "HE5", "HE6", "HE7", "HE8", "HU3", "HU6", "SA6", "SA7", "SM4", "SM5",
               "MI3", "MI4", "MI5", "BU3", "BU7", "WO1", "WO5", "TR1", "TR3", "TR4", "CT2", "CT3", "CO2",
               "FI13", "FI14", "HU8", "BU5", "WO3", "WO4", "BA2", "BA4", "BA5", "CO3"]


def test_every_conditional_line_drops_on_the_bare_village(emptied):
    w, rep = emptied
    for i in CONDITIONAL:
        for n in w["agents"]:
            r = FD.render(w, n, rep, ids=[i])
            assert i not in r["lines"] and r["skipped"] == [i], (i, n, r["lines"].get(i))
    assert FD.render(w, "Wat", rep, ids=["NB-trader:Carter"])["skipped"] == ["NB-trader:Carter"]
    alone = {"households": {"Smith": rep["households"]["Smith"]}}                      # nobody in reach wants copper work
    assert FD.render(w, "Simon", alone, ids=["SM6"])["skipped"] == ["SM6"]
    assert FD.render(w, "John", {"households": {"Wright": rep["households"]["Wright"]}}, ids=["BU6"])["skipped"] == ["BU6"]
    hu4 = line(w, rep, "Godfrey", "HU4")
    assert "the fox and the crows" in hu4 and "wolf" not in hu4                          # a clause's condition, not the line's


def test_a_bare_founders_wanted_lines_that_drop_are_reported_skipped(emptied):
    w, rep = emptied
    ralph = rep["lines"]["Ralph"]
    assert {"FA1", "FA2", "FA10"} <= set(ralph["skipped"]) and "FA1" not in ralph["ids"]


# ---------------------------------------------------------------------- the cap (u9 §5.2; D2-308, D2-340)
def test_every_founder_of_the_fixture_fits_the_cap(filled):
    w, rep = filled
    for n, x in rep["lines"].items():
        assert not x["over"] and not x["long"], (n, x)
        assert x["seeded"] <= FD.CAP_LINES and x["words"] <= FD.CAP_WORDS, (n, x)
        k = w["agents"][n].get("kept") or []
        assert len(k) == x["seeded"] and all(len(y["text"].split()) <= FD.LINE_WORDS for y in k), n
    for n in ("Ralph", "Simon", "William", "Robert"):                                    # the heads keep their protected lines
        ids = rep["lines"][n]["ids"]
        assert {"HH1", "HH3", "HH7", "HH9", "PE1"} <= set(ids), n
    for hh, kind in (("Hobb", "ox pair"), ("Hobb", "fields"), ("Hayward", "herd"), ("Smith", "forge"), ("Miller", "mill"),
                     ("Miller", "oven")):
        k = keeper_of(rep, hh, kind)
        kl = LV.HOLDINGS[kind]["keeper_line"]
        assert kl in rep["lines"][k]["ids"], (hh, kind, k)
        assert next(y for y in w["agents"][k]["kept"] if y["text"] == line(w, rep, k, kl))["source"] == "a holding"


def test_the_sowing_lore_is_not_seeded_twice_to_a_filled_farmer(filled):
    from cybertron2.engine import lore as LO
    w, _ = filled
    texts = [y["text"] for y in w["agents"]["Ralph"]["kept"]]
    assert any(t.startswith("Barley does best sown") for t in texts)
    assert LO.text("sowing") not in texts


def test_eelmouth_is_unchanged_by_the_new_templates():
    """Eelmouth's founders hold the same lines (its fisher and salter wiring as it was): FI13 and FI14 wait on bone and dressing,
    SA7 on a saltmarsh the Brooks do not hold."""
    import yaml
    from cybertron2.specs import make_eelmouth as M
    w, rep = M.remake()
    old = yaml.safe_load(open("cybertron2/specs/nutrition/eelmouth.yaml"))
    for n, a in w["agents"].items():
        assert [x["text"] for x in a.get("kept") or []] == [x["text"] for x in old["agents"][n].get("kept") or []], n
    assert "SA7" in rep["lines"]["Oliver"]["skipped"]
