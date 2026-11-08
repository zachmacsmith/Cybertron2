"""Crops grow by the season (D4-106; proposals/crop_growth.md): can apart from works, seed lying in cold ground, the cold thinning a
tender crop, winter grain wanting a winter, reaping green, turning under, sowing turf, hay by the season, and the signs of each."""
import copy

from cybertron2.capacity import levels as LV, rotation as RO
from cybertron2.engine import farm as FM, lore as LO, perceive as PC, prompt as PR, run as R, verbs as V
from cybertron2.engine.data import CROPS, ITEMS, PHYSICS
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import SEASONS, World, load_spec

SPEC = load_spec("cybertron2/specs/valley_s5.yaml")
F = PHYSICS["farming"]
SEAS = lambda d: SEASONS[(d // 8) % 4]                                         # noqa: E731
COLD = lambda d: SEAS(d) == "winter"                                            # noqa: E731


def world(season=None, **patch):
    s = copy.deepcopy(SPEC)
    s.update(patch)
    w = World(s)
    w.s["today"] = R.blank_today()
    if season:
        w.start = (SEASONS.index(season), -w.d)
    return w


def do(w, who, **a):
    return V.do(Here(w, who), Mind(w, who), a)


def run(fam, start):
    return FM.season_run(fam, start, SEAS, FM.grow_days(32, fam), F, cold_of=COLD)


def nights(w, n):
    for _ in range(n):
        FM.night(w)
        w.s["day"] += 1


def texts(w, who="Edric"):
    return [f["text"] for f in PC.facts(Here(w, who))]


def test_when_one_sows_decides_how_well_it_does_and_nothing_is_refused():
    full = run("grain", 0)[1]
    assert abs(full - 1.0) < 1e-9                                               # barley in spring: a full crop
    assert run("grain", 12)[1] < 0.8                                            # late in summer: smaller
    assert run("grain", 18)[0] is None or run("grain", 18)[1] < 0.2           # in autumn: the cold takes it
    assert 0.3 < run("grain", 24)[1] < 0.7                                     # in winter: the seed lies and is lost a while
    assert run("winter grain", 18)[1] > 0.7 and run("winter grain", 2)[1] < 0.45   # rye wants a winter
    w = world("autumn")
    w.s["parcels"]["long_field"]["crop"] = None
    w.s["containers"][w.hands("Edric")]["goods"]["grain"] = 10.0
    assert do(w, "Edric", do="work", what="sow", at="Long Field", item="grain").startswith("You sowed")


def test_seed_lies_in_cold_ground_and_comes_up_when_it_can():
    w = world("winter")
    w.s["parcels"]["long_field"]["crop"] = None
    w.s["containers"][w.hands("Edric")]["goods"]["grain"] = 10.0
    r = do(w, "Edric", do="work", what="sow", at="Long Field", item="grain")
    assert "cold and hard" in r                                                 # felt by the sower, not explained
    base = w.s["parcels"]["long_field"]["crop"]["base"]
    nights(w, 3)
    c = w.s["parcels"]["long_field"]["crop"]
    assert c["lying"] and c["base"] < base and any("nothing has come up yet" in t for t in texts(w))
    while w.calendar()["season"] == "winter":
        nights(w, 1)
    nights(w, 1)
    assert not w.s["parcels"]["long_field"]["crop"]["lying"]


def test_reaping_green_gives_fodder_and_frees_the_plot():
    w = world("spring")
    w.s["parcels"]["long_field"]["crop"] = None
    w.s["containers"][w.hands("Edric")]["goods"].update({"grain": 48.0, "crude tool": 1.0})
    for _ in range(8):
        do(w, "Edric", do="work", what="sow", at="Long Field", item="grain")
    nights(w, 3)
    r = do(w, "Edric", do="work", what="reap", at="Long Field")
    assert "soft and milky" in r and w.goods(w.hands("Edric")).get("green grain", 0) > 0
    assert any("cut green" in t for t in texts(w, "Hamo"))
    assert ITEMS["green grain"]["fodder"] > ITEMS["green grain"]["food"]
    for _ in range(60):
        if not w.s["parcels"]["long_field"].get("crop"):
            break
        do(w, "Edric", do="work", what="reap", at="Long Field")
        w.s["today"] = R.blank_today()
        FM.night(w)
    assert not w.s["parcels"]["long_field"].get("crop")                         # all cut: the ground is free
    w.s["containers"][w.hands("Edric")]["goods"]["green grain"] = 20.0
    assert do(w, "Edric", do="make", what="dry fodder").startswith("You made")   # dried, it is hay


def test_a_crop_is_turned_under_with_the_hoe_and_another_sown():
    w = world("spring")
    w.s["parcels"]["long_field"]["crop"] = None
    w.s["containers"][w.hands("Edric")]["goods"].update({"grain": 48.0, "beans": 20.0, "crude tool": 1.0})
    for _ in range(8):
        do(w, "Edric", do="work", what="sow", at="Long Field", item="grain")
    nights(w, 2)
    r = do(w, "Edric", do="work", what="sow", at="Long Field", item="beans")
    assert r.startswith("Refused") and "turn it under" in r
    fert = w.s["parcels"]["long_field"]["fertility"]
    for _ in range(120):
        if not w.s["parcels"]["long_field"].get("crop"):
            break
        r = do(w, "Edric", do="work", what="hoe", at="Long Field")
        assert "under" in r
    assert not w.s["parcels"]["long_field"].get("crop") and w.s["parcels"]["long_field"]["fertility"] > fert
    assert do(w, "Edric", do="work", what="sow", at="Long Field", item="beans").startswith("You sowed")


def test_weeding_a_ripe_crop_is_done_and_gains_nothing():
    w = world("spring")
    w.s["parcels"]["long_field"]["crop"] = None
    w.s["containers"][w.hands("Edric")]["goods"]["grain"] = 16.0
    do(w, "Edric", do="work", what="sow", at="Long Field", item="grain")
    nights(w, 9)
    r = do(w, "Edric", do="work", what="weed", at="Long Field")
    assert r.startswith("You weeded") and "no good" in r


def test_seed_thrown_on_turf_takes_poorly():
    w = world("spring")
    w.s["containers"][w.hands("Edric")]["goods"]["grain"] = 6.0
    r = do(w, "Edric", do="work", what="sow", at="Brook Meadow", item="grain")
    assert r.startswith("You sowed") and "turf" in r
    turf = w.s["parcels"]["mb_meadow"]["crop"]["base"]
    w2 = world("spring")
    w2.s["parcels"]["long_field"]["crop"] = None
    w2.s["containers"][w2.hands("Edric")]["goods"]["grain"] = 6.0
    do(w2, "Edric", do="work", what="sow", at="Long Field", item="grain")
    assert turf < 0.2 * w2.s["parcels"]["long_field"]["crop"]["base"]
    nights(w, 2)
    assert w.s["parcels"]["mb_meadow"]["cover"] == "meadow" and w.s["parcels"]["mb_meadow"]["crop"]


def test_hay_by_the_season_and_beasts_eat_green_fodder():
    w = world("winter")
    w.s["containers"][w.hands("Edric")]["goods"]["crude tool"] = 1.0
    r = do(w, "Edric", do="gather", what="hay", at="Brook Meadow")
    assert not r.startswith("Refused") and w.goods(w.hands("Edric")).get("hay", 0) == 0
    fod = sorted((i for i, d in ITEMS.items() if d.get("fodder")), key=lambda i: (-float(ITEMS[i].get("spoil", 0)), i))
    assert fod[0].startswith("green")                                            # the perishable fodder goes first


def test_the_cold_shows_on_a_tender_crop_and_a_thin_stand_shows():
    w = world("spring")
    w.s["parcels"]["long_field"]["crop"] = None
    w.s["containers"][w.hands("Edric")]["goods"]["grain"] = 16.0
    do(w, "Edric", do="work", what="sow", at="Long Field", item="grain")
    nights(w, 2)
    w.start = (SEASONS.index("winter"), -w.d)
    nights(w, 1)
    assert any("blackened the tips" in t for t in texts(w))
    nights(w, 3)
    T = texts(w)
    assert any("lies dead after the frosts" in t or "scattering" in t or "dead and black" in t for t in T)


def test_the_lore_is_the_engines_growth_and_the_rules_do_not_tell_it():
    best = LO.best_seasons()
    assert best["grain"] == ["spring"] and best["winter grain"] == ["autumn"]
    t = LO.text("sowing")
    assert "barley does best sown in spring" in t.lower() and "rye does best sown late in autumn" in t and len(t.split()) <= 60
    times = LO.sowing_times()
    assert ("early", "summer") in times["grain"][1]                              # a family knows a second window (D4-114)
    w = World(load_spec("cybertron2/specs/wenbridge.yaml"))
    assert "in spring" not in PR.system_prompt(Here(w, "Tom"), Mind(w, "Tom")).split("Your people:")[1].split("What you can do")[0]


def test_the_capacity_model_finds_the_best_sowing_day_from_the_engine():
    yr = RO.best_year((0, 24), 32, LV.LEVELS["standing"])
    sown = [(k, s) for k, s, d in yr.plan if k != "rest"]
    assert sown and sown[0][0] == "grain" and SEAS(sown[0][1]) == "spring"
