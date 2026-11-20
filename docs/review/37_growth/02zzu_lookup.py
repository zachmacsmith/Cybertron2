"""02zzu_lookup: the food values of 02zzu_shared_units checked against USDA FoodData Central (SR Legacy, April 2018).

D2-258 (20 Nov): the food values go onto one physical basis, each value checked against FoodData Central before the data change.
D2-259 (20 Nov): a value within about 20% of its FoodData Central figure is kept as it is; beyond 20% it changes.

    python3 -I 02zzu_lookup.py SR_CSV_DIR FOOD_DES.txt [CYB_ROOT]

SR_CSV_DIR    the unzipped FoodData_Central_sr_legacy_food_csv_2018-04 (food.csv, food_nutrient.csv, sr_legacy_food.csv)
FOOD_DES.txt  the SR28 food description file (NDB_No ... Ref_desc, Refuse): the refuse shares, which the FDC CSV release does not
              carry. Used here from the copy in github.com/alyssaq/usda-sqlite (data/FOOD_DES.txt), the USDA file unchanged;
              every row used is cross-checked by its description against SR Legacy's food.csv (the `desc_match` field).
CYB_ROOT      the cybertron2 checkout (default: three levels up), for the game's values now (ITEMS, TAKEN, slaughter, EGG_FOOD).

Writes 02zzu_lookup.json beside this file (the .md is written by hand from it). No engine state is touched; nothing else changes.
Energy is SR nutrient 1008 (number 208, kcal, Atwater specific factors as published). 1 food = 2,500 kcal (02zzu's basis).
"""
from __future__ import annotations

import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KCAL_FOOD = 2500.0
OLD = os.path.join(HERE, "02zzu_shared_units.json")
OUT = os.path.join(HERE, "02zzu_lookup.json")
KEEP_BAND = 0.20        # D2-259
FLAG_BAND = 0.10        # the brief: flag every move over 10% against 02zzu


# ------------------------------------------------------------------------------------------------------------- the data
def load_sr(sr_dir, food_des):
    food = {r["fdc_id"]: r["description"] for r in csv.DictReader(open(os.path.join(sr_dir, "food.csv"), encoding="utf-8"))}
    ndb = {r["fdc_id"]: r["NDB_number"].zfill(5) for r in csv.DictReader(open(os.path.join(sr_dir, "sr_legacy_food.csv")))}
    kcal = {}
    with open(os.path.join(sr_dir, "food_nutrient.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["nutrient_id"] == "1008":
                kcal[r["fdc_id"]] = float(r["amount"])
    des = {}
    for line in open(food_des, encoding="latin-1"):
        x = [v.strip("~") for v in line.rstrip("\r\n").split("^")]
        des[x[0]] = {"long": x[2], "ref_desc": x[7], "refuse": float(x[8]) / 100.0 if x[8] else None}
    return food, ndb, kcal, des


def sr_row(db, fdc):
    food, ndb, kcal, des = db
    n = ndb[fdc]
    d = des.get(n, {})
    return {"fdc_id": int(fdc), "ndb": n, "description": food[fdc], "kcal_100g": kcal[fdc], "refuse": d.get("refuse"),
            "refuse_desc": d.get("ref_desc") or "", "desc_match": d.get("long") == _plain(food[fdc])}


def _plain(desc):
    """SR Legacy adds this to some SR28 descriptions; the row is the same food."""
    return desc.replace(" (Includes foods for USDA's Food Distribution Program)", "")


# ------------------------------------------------------------------------------------------------------------- the matches
# A component: (fdc_id, share of the unit by weight, edible share or None to take SR's refuse, role, note). The unit's food is
# sum(share x kcal x 10 x edible) / 2,500 for a 1 kg unit. `edible_src` says where the edible share came from.
C = lambda fdc, share=1.0, edible=None, role="match", note="": dict(fdc=fdc, share=share, edible=edible, role=role, note=note)

GOODS = {
    # the grain ladder (D2-60, D4-107; 02zzu part 3): bread is the flour's energy less 2% in baking; grain, rye, meal and flour
    # are bread x (their game value / 1.3); beans are their own physical value x 0.53. Each good's own physical value is shown.
    "grain": dict(unit="1 kg threshed grain (barley, oats, wheat)", kind="ladder", rung=0.7 / 1.3,
                  comps=[C("170283", 1 / 3, 0.92, note="hulled (dehusked) barley; husk share 02zzu's"),
                         C("168890", 1 / 3, 0.92, note="wheat; 02zzu's 0.92 over the mix"),
                         C("169705", 1 / 3, 0.92, note="oats (groats); the hull of threshed oats is 0.25-0.3")]),
    "rye": dict(unit="1 kg threshed rye", kind="ladder", rung=0.7 / 1.3, comps=[C("168884", 1.0, 1.0)]),
    "beans": dict(unit="1 kg dried broad beans or peas", kind="design", design=0.53,
                  comps=[C("175205", 0.5, 1.0), C("172428", 0.5, 1.0, note="02zzu gave split peas as 341; SR has 364")]),
    "meal": dict(unit="the meal of 1 kg grain (hand-ground, unsifted)", kind="ladder", rung=1.0 / 1.3,
                 comps=[C("168893", 0.5, 1.0), C("169739", 0.5, 1.0, note="barley flour or meal")]),
    "flour": dict(unit="the flour of 1 kg grain (lightly sifted)", kind="ladder", rung=1.0 / 1.3,
                  comps=[C("168893", 1.0, 0.97, note="extraction 0.97 (02zzu); white flour 20481 is 364")]),
    "bread": dict(unit="the bread of 1 kg flour (about 1.4 kg loaves)", kind="ladder_top",
                  comps=[C("172688", 1.0, 1.4, role="check", note="direct: 1.4 kg of loaves at 252")]),
    "green grain": dict(unit="1 kg green ears and straw", kind="none", fallback=0.24,
                        other="no SR row for green cereal (immature ears, forage): 02zzu's estimate (40-90 kcal) kept"),
    "green rye": dict(unit="as green grain", kind="none", fallback=0.24, other="as green grain"),
    "green beans": dict(unit="1 kg green pods", kind="phys",
                        comps=[C("168574", 1.0, None, note="young broad beans eaten in the pod")],
                        alt="shelled instead (pods about 0.35 seed): 11088 broadbeans immature seeds 72 kcal gives about 0.10"),
    # meat and fish: the unit is defined by energy (02zzu: 1,500 kcal of meat, 1,150 of fish); the SR rows check the kcal a kg
    "meat": dict(unit="1,500 kcal of edible meat", kind="defined", kcal_unit=1500.0,
                 comps=[C("173855", role="check"), C("175297", role="check"), C("174347", role="check"), C("173845", role="check"),
                        C("168608", role="check"), C("173815", role="check")]),
    "fish": dict(unit="1,150 kcal of edible fish", kind="defined", kcal_unit=1150.0,
                 comps=[C("175154", role="check"), C("173680", role="check"), C("173678", role="check"), C("171952", role="check"),
                        C("174193", role="check"), C("173686", role="check")]),
    "dried meat": dict(unit="half the weight of the meat", kind="rule", base="meat", k=2.0,
                       comps=[C("170604", role="check", note="modern chipped dried beef, about 57% water: not a hard-dried meat"),
                              C("167536", role="check", note="jerky (formed, with additives)")]),
    "smoked meat": dict(unit="half the weight of the meat", kind="rule", base="meat", k=2.0, comps=[]),
    "drying meat": dict(unit="meat on the rack", kind="rule", base="meat", k=1.0, comps=[]),
    "smoking meat": dict(unit="meat in the smoke", kind="rule", base="meat", k=1.0, comps=[]),
    "salt meat": dict(unit="meat salted, the same weight", kind="rule", base="meat", k=0.95,
                      comps=[C("170199", role="check", note="corned (brined) beef brisket: as fresh beef brisket a kg")]),
    "salt fish": dict(unit="fish salted, the same weight", kind="rule", base="fish", k=1.0,
                      comps=[C("174190", role="check", note="salt cod dried hard (290 against 82 fresh, x3.5): a stockfish, "
                                                         "not a wet-salted fish")]),
    "drying fish": dict(unit="fish on the rack", kind="rule", base="fish", k=1.0, comps=[]),
    "smoking fish": dict(unit="fish in the smoke", kind="rule", base="fish", k=1.0, comps=[]),
    "dried fish": dict(unit="half the weight", kind="rule", base="fish", k=2.0, comps=[C("174190", role="check")]),
    "smoked fish": dict(unit="half the weight", kind="rule", base="fish", k=2.0,
                        comps=[C("173712", role="check", note="modern hot-smoked whitefish, not dried (108 against 134 raw)"),
                               C("173668", role="check", note="kippered herring 217 against 158 raw: x1.4")]),
    # dairy and eggs
    "milk": dict(unit="1 kg whole cow's milk", kind="phys",
                 comps=[C("171266", 1.0, 1.0, note="producer milk 3.7% fat, as it leaves the cow; 01077 (3.25%) is 61")]),
    "cheese": dict(unit="1 kg hard cheese", kind="phys",
                   comps=[C("173414", 1.0, 1.0, note="cheddar; parmesan 01033 (part-skim) 392, gouda 356")]),
    "egg": dict(unit="1 kg eggs in shell (02zzu's unit; the game's egg weighs 0.1)", kind="phys",
                comps=[C("171287", 1.0, None, note="refuse 12% shell")]),
    # wild plants: 1 kg as gathered
    "greens": dict(unit="1 kg nettle tops, sorrel, ramsons", kind="phys",
                   comps=[C("169819", 0.5, 0.8, note="blanched nettles; tops as gathered 0.8 eaten (02zzu)"),
                          C("170076", 0.5, None, note="dock (Rumex: sorrel's genus), refuse 30% stalks")],
                   other="ramsons (Allium ursinum leaves): no SR row; left out of the mix"),
    "roots": dict(unit="1 kg pignut and silverweed roots", kind="phys", proxy=True,
                  comps=[C("170417", 0.25, None, role="proxy"), C("169974", 0.25, None, role="proxy"),
                         C("169277", 0.25, None, role="proxy"), C("169203", 0.25, None, role="proxy", note="arrowhead, a wild tuber")],
                  other="pignut (Conopodium majus) and silverweed (Potentilla anserina): no SR rows; four SR roots as proxies"),
    "mushrooms": dict(unit="1 kg ceps, chanterelles, field mushrooms", kind="phys",
                      comps=[C("168422", 0.5, None), C("169251", 0.5, None, note="cultivated Agaricus for the field mushroom")],
                      other="ceps (Boletus edulis): no SR row; left out of the mix"),
    "watercress": dict(unit="1 kg watercress and brooklime", kind="phys", comps=[C("170068", 1.0, None)]),
    "samphire": dict(unit="1 kg marsh samphire", kind="phys", proxy=True,
                     comps=[C("169274", 1.0, None, role="proxy", note="purslane, a succulent leaf")],
                     other="samphire (Salicornia): no SR row; purslane as proxy; 02zzu's estimate was 15-30 kcal, 0.85 eaten"),
    "berries": dict(unit="1 kg brambles, bilberries, wild strawberries", kind="phys",
                    comps=[C("173946", 1 / 3, None), C("171711", 1 / 3, None, note="cultivated blueberry for the bilberry"),
                           C("167762", 1 / 3, None, note="cultivated strawberry for the wild")]),
    "hedge fruit": dict(unit="1 kg crab apples, sloes, haws, hips", kind="phys",
                        comps=[C("171721", 1 / 3, None, note="crab apples, refuse 8%"),
                               C("169820", 1 / 3, 0.7, role="proxy", note="wild plums (pitted) for sloes; stone share 02zzu's 0.3"),
                               C("168998", 1 / 3, 0.7, role="match", note="wild rose hips (prepared); seeds and hairs 0.3 (02zzu)")],
                        other="sloes (Prunus spinosa) and haws (Crataegus): no SR rows; sloes by wild plum, haws left out"),
    "hazel nuts": dict(unit="1 kg hazel nuts in shell", kind="phys", comps=[C("170581", 1.0, None)]),
    "beech nuts": dict(unit="1 kg beech mast in husk", kind="phys",
                       comps=[C("170161", 1.0, None, note="02zzu cited 12014 (pumpkin seeds); the beechnut row is 12077")]),
    "acorns": dict(unit="1 kg acorns in shell, unleached", kind="design", design=0.035, comps=[C("170157", 1.0, None)]),
    "acorn meal": dict(unit="the leached meal of 1.5 kg acorns (3 acorns make 2)", kind="acorn_meal",
                       comps=[C("170157", role="match"), C("170566", role="check", note="acorn flour 501: the dried kernel")]),
    "wild food": dict(unit="the legacy gathered mix", kind="mix",
                      mix={"hazel nuts": 0.30, "acorns": 0.25, "mushrooms": 0.15, "hedge fruit": 0.12, "berries": 0.10, "roots": 0.08}),
    "tallow": dict(unit="1 kg fat", kind="design", design=0.0, comps=[C("171400", 1.0, 1.0)]),
}

# animals: live kg (02zzu's, with its source), dressing (carcass of live; 02zzu's), edible share of the carcass (SR refuse where
# SR gives one for the carcass or ready-to-cook bird, else 02zzu's), edible offal (share of live, 02zzu's), flesh kcal from SR.
A = lambda live, dress, flesh, edible=None, offal=0.0, src="02zzu", engine=None, ref=None, note="", proxy=False, live_src="02zzu": \
    dict(live=live, dress=dress, flesh=flesh, edible=edible, offal=offal, edible_src=src, engine=engine, ref=ref, note=note,
         proxy=proxy, live_src=live_src)
ANIMALS = {
    "red deer": A(90, 0.57, "173855", 0.75, 0.03, engine=("meat", 20.0), live_src="02zzu (Mitchell et al.; engine mass 90)"),
    "roe deer": A(22, 0.60, "173855", 0.72, 0.03, engine=("meat", 4.5), live_src="02zzu (Mitchell et al.)"),
    "wild boar": A(70, 0.68, "175297", 0.70, 0.03, engine=("meat", 15.0),
                   note="02zzu used 1,600 kcal a kg (lean 122 raised for autumn fat, an estimate); SR's wild boar is 122"),
    "brown hare": A(3.5, 0.60, "174347", 0.75, 0.02, engine=("meat", 0.7), proxy=True,
                    note="no hare in SR: wild rabbit (02zzu cited 17178, which is roasted domestic rabbit)"),
    "woodpigeon": A(0.5, 0.50, "171079", None, 0.0, src="SR (squab meat only: 23% bone, 12% skin of the dressed bird)",
                    engine=("meat", 0.1), proxy=True,
                    note="squab (young farmed pigeon) for the woodpigeon; meat with skin 05160 is 294 kcal, refuse 23%"),
    "wildfowl": A(1.1, 0.60, "174468", None, 0.0, src="SR (wild duck meat and skin: 38% bone, 2% loss)", engine=("meat", 0.3),
                  note="02zzu cited 05141 (domestic duck meat); the wild duck rows are 05144 and 05145"),
    "brown bear": A(250, 0.60, "173845", 0.70, 0.03, engine=("meat", 40.0)),
    "eel": A(0.5, 1.0, "174193", 0.72, 0.0, engine=("fish", 0.2), live_src="02zzu (engine mass 0.5; Tesch 0.1-1.5)",
             note="edible share of the whole fish: 02zzu (FAO yields); SR gives none for whole fish"),
    "salmon": A(4.0, 1.0, "173686", 0.62, 0.0, engine=("fish", 2.0), live_src="02zzu (grilse 2-3.5, multi-sea-winter 4-8)"),
    "lamprey": A(0.15, 1.0, "174193", 0.80, 0.0, engine=("meat", 0.3), proxy=True,
                 note="no lamprey in SR: eel (the nearest fatty eel-shaped fish) as proxy; 02zzu estimated 2,000 kcal a kg"),
    "cow": A(300, 0.50, "168608", None, 0.03, src="SR carcass refuse 20% bone (13002, a modern select carcass)", engine=("meat", 40.0),
             ref="169431", live_src="02zzu (Albarella: medieval cattle 250-350 kg)",
             note="flesh: grass-fed beef, lean and fat (ground) 198; a modern carcass 278-291; 02zzu 200"),
    "ox": A(400, 0.52, "168608", None, 0.03, src="SR carcass refuse 20% (13002)", engine=("meat", 50.0), ref="169431"),
    "bull": A(400, 0.52, "168608", None, 0.03, src="SR carcass refuse 20% (13002)", engine=("meat", 50.0), ref="169431",
              note="not in 02zzu; the engine's slaughter gives bulls the ox's 50 meat; taken as the ox"),
    "young": A(120, 0.55, "173815", None, 0.04, src="SR veal composite refuse 31% bone", engine=("meat", 10.0),
               note="a calf or yearling; veal lean and fat 144"),
    # in the engine but not in 02zzu
    "heron (young, from the nest)": A(1.2, 0.50, "171079", None, 0.0, src="SR squab refuse (proxy)", engine=("meat", 0.3), proxy=True,
                                      live_src="estimate (grey heron 1-2 kg grown; nestlings near fledging)",
                                      note="no heron in SR: squab meat as proxy; kinds.py COLONIES heronry take 0.3 meat each"),
    "rook (young, from the nest)": A(0.35, 0.50, "171079", None, 0.0, src="SR squab refuse (proxy)", engine=("meat", 0.12), proxy=True,
                                     live_src="estimate (rook 0.4-0.5 kg grown; branchers a little less)",
                                     note="no rook in SR: squab as proxy; kinds.py COLONIES rookery take 0.12 meat each"),
    # reference rows the brief names (no engine good a head)
    "hen (a kept hen killed)": A(1.2, 0.70, "172400", None, 0.0, src="SR stewing hen refuse 30% bone", engine=None,
                                 live_src="estimate (a medieval hen 1-1.5 kg; ready-to-cook 0.7 of live)",
                                 note="the engine kills hens (raids) but gives no meat for one"),
    "rabbit": A(1.5, 0.50, "174347", 0.75, 0.0, engine=None, live_src="estimate (wild European rabbit 1.2-2 kg)",
                note="no rabbit kind in the engine; for reference"),
    "trout (a kg whole, as caught)": A(1.0, 1.0, "175181", None, 0.0, src="SR brook trout refuse 53% (skin, head, viscera, bones)",
                                       engine=("fish", 1.0),
                                       note="the fish good from fishing by hand, if a unit is a kg of whole fish as caught"),
}
REF_ONLY = ("hen (a kept hen killed)", "rabbit", "trout (a kg whole, as caught)")
BORDER = 0.03           # a verdict within 3 points of the band is marked borderline


# ------------------------------------------------------------------------------------------------------------- the reckoning
def comp_rows(db, g):
    out = []
    for c in g.get("comps", []):
        r = sr_row(db, c["fdc"])
        if c["edible"] is not None:
            ed, src = c["edible"], "02zzu" if c["edible"] not in (1.0, 1.4) else "whole"
        else:
            ed, src = 1.0 - (r["refuse"] or 0.0), "SR refuse"
        out.append(dict(r, share=round(c["share"], 4), edible=round(ed, 3), edible_src=src, role=c["role"], note=c["note"]))
    return out


def phys_of(rows):
    rows = [r for r in rows if r["role"] in ("match", "proxy")]
    if not rows:
        return None, None
    kcal_g = sum(r["share"] * r["kcal_100g"] * r["edible"] for r in rows) / sum(r["share"] for r in rows)
    return kcal_g * 10.0 / KCAL_FOOD, kcal_g


def game_now(root):
    sys.path.insert(0, root)
    from cybertron2.engine.data import ITEMS, TECHNIQUES          # noqa: E402
    from cybertron2.wild.kinds import TAKEN                       # noqa: E402
    from cybertron2.engine import wild as W                       # noqa: E402
    return ITEMS, TECHNIQUES, TAKEN, W.EGG_FOOD


def verdict(now, checked):
    if checked is None or now is None:
        return None, None
    if checked == 0:
        return (0.0 if now == 0 else None), ("keep" if now == 0 else "change")
    dev = now / checked - 1.0
    v = "keep" if abs(dev) <= KEEP_BAND + 1e-9 else "change"
    if abs(abs(dev) - KEEP_BAND) <= BORDER:
        v += " (borderline)"
    return round(dev, 3), v


def main(argv):
    sr_dir, food_des = argv[1], argv[2]
    root = argv[3] if len(argv) > 3 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    db = load_sr(sr_dir, food_des)
    old = json.load(open(OLD))["table"]
    ITEMS, TECH, TAKEN, egg_food = game_now(root)
    goods = {}
    checked = {}
    # first pass: physical values
    for k, g in GOODS.items():
        rows = comp_rows(db, g)
        p, kg = phys_of(rows)
        goods[k] = dict(unit=g["unit"], kind=g["kind"], components=rows, physical=None if p is None else round(p, 4),
                        kcal_100g_as_unit=None if kg is None else round(kg, 1), other_source=g.get("other"), alt=g.get("alt"),
                        proxy=bool(g.get("proxy")))
    # the ladder: flour's energy, less 2% in the baking, is bread; the others are bread x their rung
    bread = goods["flour"]["physical"] * 0.98
    checked["bread"] = bread
    goods["bread"]["physical_direct"] = round(goods["bread"]["components"][0]["kcal_100g"] * 14.0 / KCAL_FOOD, 4)
    for k, g in GOODS.items():
        kind = g["kind"]
        if kind == "ladder":
            checked[k] = bread * g["rung"]
        elif kind in ("design",):
            checked[k] = goods[k]["physical"] * g["design"]
        elif kind == "phys":
            checked[k] = goods[k]["physical"]
        elif kind == "defined":
            checked[k] = g["kcal_unit"] / KCAL_FOOD
            ks = [c["kcal_100g"] for c in goods[k]["components"]]
            goods[k]["kcal_100g_range"] = [min(ks), round(sum(ks) / len(ks), 1), max(ks)]
            goods[k]["kg_a_unit"] = {c["description"]: round(g["kcal_unit"] / (c["kcal_100g"] * 10), 2) for c in goods[k]["components"]}
        elif kind == "none":
            checked[k] = g["fallback"]
        elif kind == "acorn_meal":
            a = goods["acorns"]["components"][0]
            checked[k] = 3 * a["edible"] * a["kcal_100g"] * 10 * 0.85 / 2 / KCAL_FOOD
            goods[k]["note"] = ("02zzu's rule: 3 kg acorns make 2 units, leaching loses 15%; with SR's 38% shell. The kernel of 1.5 kg "
                                "acorns dried to acorn flour (501) weighs about 0.72 kg")
    for k, g in GOODS.items():
        if g["kind"] == "rule":
            checked[k] = checked[g["base"]] * g["k"]
    checked["wild food"] = sum(w * checked[x] for x, w in GOODS["wild food"]["mix"].items())

    flagged_old_ids = {"beech nuts": "12014", "wild boar": "17165", "brown hare": "17178", "woodpigeon": "05153",
                       "wildfowl": "05141", "hedge fruit": "09136"}
    for k in goods:
        it = ITEMS[k]
        o = old["goods"].get(k, {})
        c = checked[k]
        dev_old = None if not o.get("recommended") else round(c / o["recommended"] - 1.0, 3)
        dev_now, v = verdict(it["food"], c)
        if GOODS[k]["kind"] == "none":
            v = "no FDC figure: " + v + " on 02zzu's estimate"
        elif GOODS[k].get("proxy"):
            v += " (on an SR proxy)"
        raw = it.get("raw")
        goods[k].update(
            game_now=it["food"], game_raw=raw, game_weight=it["weight"], zzu=o.get("recommended"), zzu_physical=o.get("physical"),
            zzu_kcal_100g=o.get("kcal_100g"), zzu_edible=o.get("edible"), checked=round(c, 4),
            checked_raw=None if raw is None or not it["food"] else round(c * raw / it["food"], 4),
            against_zzu=dev_old, moved_over_10=bool(dev_old is not None and abs(dev_old) > FLAG_BAND),
            now_against_checked=dev_now, d2_259=v, proposed=None if v.startswith("keep") or v.startswith("no FDC") else round(c, 3),
            zzu_id_wrong=flagged_old_ids.get(k))
    # the egg as the engine lays it
    egg_each = 0.05 * 0.88 * 1430 / KCAL_FOOD
    d, v = verdict(egg_food, egg_each)
    extra = {"EGG_FOOD (an egg, 50 g in shell)": dict(game_now=egg_food, checked=round(egg_each, 4), now_against_checked=d, d2_259=v,
                                                      proposed=None if v.startswith("keep") else round(egg_each, 3), fdc_id=171287,
                                                      note="at 45 g an egg it is 0.0227 (keep); at 50 g 0.0252"),
             "egg unit as the game weighs it (0.1 kg)": dict(game_now=ITEMS["egg"]["food"],
                                                             checked=round(checked["egg"] * ITEMS["egg"]["weight"], 4),
                                                             d2_259="change unless the unit becomes 1 kg (weight 1)")}

    animals = {}
    unit_val = {"meat": checked["meat"], "fish": checked["fish"]}
    game_val = {"meat": ITEMS["meat"]["food"], "fish": ITEMS["fish"]["food"]}
    kcal_unit = {"meat": 1500.0, "fish": 1150.0}
    for k, a in ANIMALS.items():
        r = sr_row(db, a["flesh"])
        if a["edible"] is not None:
            ed = a["edible"]
        elif a["ref"]:
            ed = 1.0 - sr_row(db, a["ref"])["refuse"]
        else:
            ed = 1.0 - r["refuse"]
        kcal = a["live"] * (a["dress"] * ed + a["offal"]) * r["kcal_100g"] * 10.0
        food = kcal / KCAL_FOOD
        okey = {"bull": "ox"}.get(k, k)
        o = old["animals"].get(okey) if k != "bull" else None
        good, n = a["engine"] or (None, None)
        now = None if good is None else n * game_val[good]
        dev_now, v = verdict(now, food)
        if k in REF_ONLY:
            v = "reference (no engine good a head)" if k != "trout (a kg whole, as caught)" else \
                "reference (depends on what a fish unit is)"
        elif v and a["proxy"]:
            v += " (on an SR proxy)"
        dev_old = None if not o else round(food / o["food_a_head_basis"] - 1.0, 3)
        animals[k] = dict(flesh=r, live_kg=a["live"], live_src=a["live_src"], dressing=a["dress"], edible_of_carcass=round(ed, 3),
                          edible_src=a["edible_src"] if a["edible"] is None else "02zzu", offal_of_live=a["offal"],
                          edible_kg=round(a["live"] * (a["dress"] * ed + a["offal"]), 3), kcal=round(kcal), checked=round(food, 3),
                          engine_good=good, engine_goods=n, game_now=now, zzu=None if not o else o["food_a_head_basis"],
                          zzu_kcal_kg=None if not o else o["kcal_a_kg_eaten"], zzu_edible=None if not o else o["edible_of_carcass"],
                          against_zzu=dev_old, moved_over_10=bool(dev_old is not None and abs(dev_old) > FLAG_BAND),
                          now_against_checked=dev_now, d2_259=v,
                          goods_checked=None if good is None else round(kcal / kcal_unit[good if k != "lamprey" else "fish"], 2),
                          goods_unit=None if good is None else ("fish" if k == "lamprey" else good),
                          zzu_id_wrong=flagged_old_ids.get(k), proxy=a["proxy"], note=a["note"], reference_only=k in REF_ONLY)
    out = dict(basis={"kcal_food": KCAL_FOOD, "keep_band": KEEP_BAND, "flag_band": FLAG_BAND,
                      "release": "USDA FoodData Central SR Legacy, April 2018 (CSV, FDC 2019-10); refuse from SR28 FOOD_DES",
                      "energy": "nutrient 1008 (208, kcal)", "game": "cybertron2 main: engine/data.py ITEMS, wild/kinds.py TAKEN, "
                      "TECHNIQUES slaughter, engine/wild.py EGG_FOOD"},
               goods=goods, eggs=extra, animals=animals,
               desc_mismatch=[c["fdc_id"] for g in goods.values() for c in g["components"] if not c["desc_match"]]
               + [a["flesh"]["fdc_id"] for a in animals.values() if not a["flesh"]["desc_match"]])
    json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False)
    # a short print for the note
    for k, g in goods.items():
        print(f"{k:13s} now {g['game_now']:<5} zzu {g['zzu']!s:6s} chk {g['checked']:<7} vs02zzu {g['against_zzu']!s:7s} "
              f"now/chk {g['now_against_checked']!s:7s} {g['d2_259']}")
    for k, a in animals.items():
        print(f"{k:30s} now {a['game_now']!s:6s} zzu {a['zzu']!s:7s} chk {a['checked']:<8} vs02zzu {a['against_zzu']!s:7s} "
              f"now/chk {a['now_against_checked']!s:7s} {a['d2_259']} goods {a['goods_checked']}")
    print(extra)
    print("description mismatches:", out["desc_mismatch"])


if __name__ == "__main__":
    main(sys.argv)
