"""The carrying capacity model (D4-102): guards that fail when the engine gains what the model does not read, and agreement with the
engine's own rules run on a real world."""
import copy

import yaml

from cybertron2.capacity import food as FD, graph as GR, levels as LV, model as M, rotation as RO, sources as SO
from cybertron2.engine import farm as FM, night as N
from cybertron2.engine.data import CROPS, ITEMS, PHYSICS, RESOURCES, TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.engine import run as R, verbs as V
from cybertron2.engine.world import World, load_spec

WEN = yaml.safe_load(open("cybertron2/specs/wenbridge.yaml"))


# ---------------------------------------------------------------------------------------------------------- guards
def test_every_edible_good_has_a_source_or_a_route():
    made = {d["gives"] for d in TECHNIQUES.values() if d.get("verb") == "gather" and isinstance(d.get("gives"), str)}
    made |= {"milk", "meat"} | {CROPS[c]["gives"] for c in CROPS} | {CROPS[c]["green"] for c in CROPS}   # milking, slaughter, reaping
    made |= {"egg"}                                     # kept hens laying (the wild pack, wild_layer.md; not yet in the capacity model)
    from cybertron2.wild import plants as PL
    made |= {v["item"] for v in PL.PLANTS.values()}      # the wild plant kinds' goods, gathered (D2-200; not yet in the capacity model)
    for t in FD.FOOD_TECHS:
        made |= set(TECHNIQUES[t]["gives"])
    assert set(FD.EDIBLE) <= made, f"edible goods no source makes: {set(FD.EDIBLE) - made}"


def test_every_yield_kind_is_read_or_placed():
    kinds = {(d.get("yield") or {}).get("kind") for d in TECHNIQUES.values()} - {None}
    unknown = kinds - set(GR.KINDS) - set(GR.ELSEWHERE)
    assert not unknown, f"yield kinds the capacity model does not read: {unknown} (proposals/process_model.md part 2)"


def test_every_resource_has_its_dynamics():
    from cybertron2.capacity import fuel  # noqa: F401
    from cybertron2.engine import renewal as RN
    missing = {k for k, d in RESOURCES.items() if d.get("renewal") not in RN.RULES}
    assert not missing, f"resources whose renewal rule is not registered: {missing}"


# ---------------------------------------------------------------------------------------------------------- agreement
def test_wild_take_at_the_models_rate_holds_the_stock():
    w = M.world_of(WEN)
    ctx = M.context(w, "standing")
    par = {**w.s["parcels"]["wb_mead"], "id": "wb_mead"}
    f = [x for x in SO.wild(ctx, par) if x.where == "wb_mead" and x.good == "wild food"][0]
    K = w.s["parcels"]["wb_mead"]["res"]["plants"]["K"]
    S = K * float(f.note.split("kept at ")[1].split("%")[0]) / 100
    w.s["parcels"]["wb_mead"]["res"]["plants"]["S"] = S
    from cybertron2.capacity import cal as CL
    now = CL.year_day_of(w, w.d)
    for k in range(w.year_days()):
        r = w.s["parcels"]["wb_mead"]["res"]["plants"]
        r["S"] = max(0.0, r["S"] - f.profile[(now + k) % w.year_days()])
        N._grow(w)
        w.s["day"] += 1
    end = w.s["parcels"]["wb_mead"]["res"]["plants"]["S"]
    assert abs(end - S) / K < 0.05, (S, end)


def test_spoilage_is_the_engines():
    w = M.world_of(WEN)
    bid = next(iter(w.s["buildings"]))
    b = w.s["buildings"][bid]
    b["fittings"]["bins"] = 1
    c = w.s["containers"][b["stock"]]
    rate, _ = N.decay_rate(w, c, "grain")
    season, cold = w.calendar()["season"], w.cold(b["node"])
    assert abs(rate - FD.rate("grain", "bins", season, cold)) < 1e-12


def test_eating_raw_is_the_engines():
    for g in FD.EDIBLE:
        assert FD.base(g, False) == N.eaten_worth(g, False)
        assert FD.worth(g, "raw")[0] == N.eaten_worth(g, False)


def test_a_sowing_gives_what_the_model_expects():
    spec = load_spec("cybertron2/specs/valley_s5.yaml")
    w = World(copy.deepcopy(spec))
    w.s["today"] = R.blank_today()
    w.s["parcels"]["long_field"]["crop"] = None
    from cybertron2.engine.world import SEASONS
    w.start = (SEASONS.index("spring"), -w.d)                                       # grain's sowing window
    w.s["containers"][w.hands("Edric")]["goods"]["grain"] = float(PHYSICS["farming"]["plot_seed"])
    V.do(Here(w, "Edric"), Mind(w, "Edric"), {"do": "work", "what": "sow", "at": "Long Field", "item": "grain"})
    c = w.s["parcels"]["long_field"]["crop"]
    lv = LV.LEVELS["standing"]
    fert = w.s["parcels"]["long_field"]["fertility"]
    model = RO._sowing("grain", fert, lv, FM.ground_mult(w.p, w.s["parcels"]["long_field"]), None) / (1 - FM.fail_chance(PHYSICS["farming"], None, "grain"))
    engine = c["base"] / c["area"]
    assert model <= engine * 1.0001 and engine <= model * (1 + float(PHYSICS["master_yield"])) + 1e-6, (model, engine)


# ---------------------------------------------------------------------------------------------------------- the model
def test_levels_rise_in_order_and_the_frost_is_seen():
    r = M.analyse(yaml.safe_load(open("cybertron2/specs/takeover/takeover.yaml")), levels=("bare", "standing", "worked", "best"))
    reg = r["nodes"]["(region)"]["levels"]
    vals = [reg[l]["supported"] for l in ("bare", "standing", "worked", "best")]
    assert vals == sorted(vals) and vals[0] < vals[-1]
    lost = r["nodes"]["wenbridge"]["first_harvest"]["lost_to_frost"]
    assert any(x["parcel"] == "wb_bottom" for x in lost)          # the field 38.59 counted, which the frost takes first


def test_gathering_draws_as_it_did():
    """The distribution form of a hunt consumes the random stream as the hand-written code did (D4-103)."""
    import random
    from cybertron2.engine import yields as YD
    y = TECHNIQUES["hunt"]["yield"]
    r = {"S": 10.0, "K": 14.0}
    for seed in range(300):
        a, b = random.Random(seed), random.Random(seed)
        got, hide = 0.0, 0
        if a.random() < y["p"] * r["S"] / r["K"]:                              # the code before D4-103
            got = round(min(r["S"], a.uniform(*y["range"]) * 1.0 * 1.0), 2)
            for _, pr in (y.get("by") or {}).items():
                hide += 1 if a.random() < pr else 0
        v = YD.dist(y, r, 1.0, weapon=1.0).sample(b)
        got2 = round(v["got"], 2) if isinstance(v, dict) else 0.0
        hide2 = sum(v["by"].values()) if isinstance(v, dict) else 0
        assert (got, hide) == (got2, hide2) and a.random() == b.random()


def test_a_hunts_mean_is_its_samples_mean():
    import random
    from cybertron2.engine import yields as YD, outcomes as OC
    d = YD.dist(TECHNIQUES["hunt"]["yield"], {"S": 3.0, "K": 14.0}, 1.0, weapon=1.0)
    rng = random.Random(1)
    n = 40000
    m = sum(OC.got(d.sample(rng)) for _ in range(n)) / n
    assert abs(m - OC.got(d.mean())) < 0.03


def test_fishing_appears_in_capacity_with_no_capacity_code():
    """The overhaul's acceptance test (D4-103): the water system, added as rows only, is read by the capacity model, which names
    no stock of its own."""
    import pathlib
    src = "".join(p.read_text() for p in pathlib.Path("cybertron2/capacity").glob("*.py"))
    assert '"fish"' not in src and "'fish'" not in src and '"salt"' not in src
    water = M.analyse(yaml.safe_load(open("cybertron2/specs/fishing/water.yaml")), levels=("standing",))
    dry = M.analyse(yaml.safe_load(open("cybertron2/specs/fishing/dry.yaml")), levels=("standing",))
    w_food = water["nodes"]["(region)"]["levels"]["standing"]["food_a_year"]
    d_food = dry["nodes"]["(region)"]["levels"]["standing"]["food_a_year"]
    assert w_food.get("fish", 0) > 0 and "fish" not in d_food
    assert water["nodes"]["(region)"]["levels"]["standing"]["supported"] > dry["nodes"]["(region)"]["levels"]["standing"]["supported"]


def test_a_stock_may_name_its_own_renewal_and_response():
    """Each ecosystem decides how its stock comes back and how the take answers its density (D4-103): a stock's own record overrides
    its resource's row, the night follows it, the act draws by it and the capacity model reads it, with no code naming the stock."""
    from cybertron2.engine import renewal as RN, yields as YD
    assert RN.of("fish") == "periodic" and RN.of("fish", {"renewal": "threshold"}) == "threshold"
    thin = {"S": 1.0, "K": 10.0, "r": 0.3}
    assert RN.step(PHYSICS, "plants", thin, {}) > 1.0                                       # fast: comes back from anywhere
    assert RN.step(PHYSICS, "plants", {**thin, "renewal": "threshold"}, {}) == 1.0          # below its threshold: does not
    y = TECHNIQUES["fish by hand"]["yield"]
    half = {"S": 5.0, "K": 10.0}
    prop, hyper = (YD.dist(y, half, refuge=0.1, b=RN.response("fish", {"response": b})).mean() for b in ("proportional", "hyperstable"))
    assert hyper > prop
    spec = yaml.safe_load(open("cybertron2/specs/fishing/water.yaml"))
    spec2 = copy.deepcopy(spec)
    spec2["nodes"]["ferrybank"]["parcels"]["fb_mere"]["state"]["fish"]["response"] = "hyperstable"
    w = M.world_of(spec2)
    assert w.s["parcels"]["fb_mere"]["res"]["fish"]["response"] == "hyperstable"
    work = {}
    for name, sp in (("proportional", spec), ("hyperstable", spec2)):
        fl = [f for f in M.flows(M.context(M.world_of(sp), "standing")) if f.where == "fb_mere"]
        work[name] = sum(f.work for f in fl)
    assert 0 < work["hyperstable"] < work["proportional"]          # the same steady take, for less work
