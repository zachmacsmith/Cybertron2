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
    made = {"wild food", "meat", "milk"} | {CROPS[c]["gives"] for c in CROPS}
    for t in FD.FOOD_TECHS:
        made |= set(TECHNIQUES[t]["gives"])
    assert set(FD.EDIBLE) <= made, f"edible goods no source makes: {set(FD.EDIBLE) - made}"


def test_every_yield_kind_is_read_or_placed():
    kinds = {(d.get("yield") or {}).get("kind") for d in TECHNIQUES.values()} - {None}
    unknown = kinds - set(GR.KINDS) - set(GR.ELSEWHERE)
    assert not unknown, f"yield kinds the capacity model does not read: {unknown} (proposals/process_model.md part 2)"


def test_every_resource_has_its_dynamics():
    from cybertron2.capacity import fuel  # noqa: F401
    from cybertron2.engine import regimes as RG
    missing = {k for k, d in RESOURCES.items() if d.get("regime") not in RG.REGIMES}
    assert not missing, f"resources whose regime has no registered dynamics: {missing}"


# ---------------------------------------------------------------------------------------------------------- agreement
def test_wild_take_at_the_models_rate_holds_the_stock():
    w = M.world_of(WEN)
    ctx = M.context(w, "standing")
    par = {**w.s["parcels"]["wb_mead"], "id": "wb_mead"}
    f = SO.plants(ctx, par)[0]
    K = w.s["parcels"]["wb_mead"]["res"]["plants"]["K"]
    S = K * float(f.note.split("kept at ")[1].rstrip("%")) / 100
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
    season, cold = w.calendar()["season"], w.cold()
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
