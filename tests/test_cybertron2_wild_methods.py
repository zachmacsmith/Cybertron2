"""Brief 1 of the wild layer (D2-204, proposals/methods_and_encounters.md §9): general methods with generated take tables, skill by
method and familiarity by kind, methods known by the land, and what agents see."""
import copy
import json
import re

from cybertron2.engine.data import RESOURCES, TECHNIQUES
from cybertron2.wild import methods as MT
from cybertron2.wild.kinds import KINDS, TRAITS

from tests.test_cybertron2_wild import _do, build, generated  # noqa: F401  (the generated world fixture)

KIND_WORDS = set(KINDS) | {"deer", "boar", "hare", "hares", "fox", "eel", "eels", "heron", "herons", "rook", "rooks", "beaver",
                           "beavers", "pigeon", "fowl", "wolf", "bear", "slug", "slugs"}


def _words(x) -> set:
    return set(re.findall(r"[a-z]+", json.dumps(x).lower()))


def test_no_method_row_names_a_kind_or_carries_a_hand_written_table():
    for name, row in MT.METHODS.items():
        own = {k: v for k, v in row.items() if k != "aliases"}               # old names stay as aliases for one release (§3)
        assert not (_words(own) - {"takes"}) & KIND_WORDS, (name, (_words(own) & KIND_WORDS))
        assert "takes" not in (row.get("yield") or {}), name                  # generated at load, never written by hand
    for k, r in RESOURCES.items():
        assert len((r.get("taken") or {}).get("calibrate") or {}) <= 1, k     # at most one calibration a kind at this stage


def test_a_need_that_fails_gives_nothing_and_one_method_answers_several_kinds():
    t = {m: TECHNIQUES[m]["yield"]["takes"] for m in MT.TAKE_METHODS}
    assert "red deer" not in t["net"] and "wildfowl" not in t["snare"] and "woodpigeon" not in t["snare"]
    assert {"brown hare", "fox"} <= set(t["snare"]) and {"fox", "wolf"} <= set(t["den work"])
    assert "eel" not in t["hunt the wild"] and "wildfowl" not in t["hunt the wild"]      # land game only
    assert t["stalk"] and all(TRAITS[k]["home"] == "none" for k in t["stalk"])            # beasts that lie out, not den animals
    for m in MT.TAKE_METHODS:                                                 # the table follows the rule exactly (§4)
        row = dict(MT.METHODS[m], _name=m)
        cal = {k: (r.get("taken") or {}).get("calibrate") for k, r in RESOURCES.items() if (r.get("taken") or {}).get("calibrate")}
        assert t[m] == MT.takes(row, TRAITS, cal)


def test_old_names_resolve_as_aliases():
    from cybertron2.engine import knowledge as KN, packs as PK
    PK.CURRENT = ("wild",)
    for old, new in (("stalk deer", "stalk"), ("boar hunt", "drive"), ("snare hares", "snare"), ("fowling", "net"),
                     ("set eel traps", "trap in water"), ("dig out the fox earth", "den work"), ("trap beavers", "den work"),
                     ("take the young herons", "gather young"), ("pick slugs at dusk", "pest work"), ("top the beans", "pest work"),
                     ("watch the field (fire)", "guard the field"), ("shut the hens in", "shut"), ("hunt", "hunt the wild")):
        assert KN.resolve(old, TECHNIQUES[new]["verb"]) == new, old
    PK.CURRENT = ()


def test_familiarity_with_hares_raises_the_snares_hares_and_not_its_foxes_and_carries_to_kin():
    class M:
        store = {}
    class H:
        day = 3
    mind = M()
    MT.raise_familiar(H(), mind, "brown hare", MT.FAMILIAR["take"], "snare")
    assert MT.factor(mind, "brown hare") > 1.0 and MT.factor(mind, "fox") == 1.0
    MT.raise_familiar(H(), mind, "red deer", 0.4, "stalk")
    assert abs(MT.familiar(mind, "roe deer") - 0.2) < 1e-9 and MT.familiar(mind, "wild boar") == 0.0    # deer to deer, at half
    assert "hares" not in MT.familiar_line(mind) or "brown hare" in MT.familiar_line(mind)
    assert not re.search(r"[0-9]", MT.familiar_line(mind))                    # in words, never numbers


def test_methods_are_known_by_the_land_and_basic_ones_by_all(generated):  # noqa: F811
    from cybertron2.engine import knowledge as KN, wild as WL
    world = copy.deepcopy(generated)
    world["agents"] = {"Ann": {"household": "Ash", "stage": "adult", "sex": "f", "at": "s1", "knows": {}}}
    w = build(world, history=2)
    m = WL.model(w)
    present = MT._present(w, m, w.s["wild"]["state"], w.s["wild"]["land"], "s1")
    k = w.s["know"]["Ann"]
    water = present & {"eel", "wildfowl"}
    assert ("trap in water" in k) == bool(present & {"eel"})                  # no trap in water without water kinds in the ring
    assert ("stalk" in k) == bool(present & {"red deer", "roe deer", "wild boar"})
    heronry = any(s["node"] == "s1" and s["kind"] in ("heronry", "rookery") for s in (w.s["wild"].get("sites") or {}).values())
    assert ("gather young" in k) == heronry
    for b in MT.BASIC:
        assert KN.basic(b), b
    f = (w.s["mind"].get("Ann") or {}).get("familiar") or {}
    assert all(kind in present for kind in f if not kind.startswith("_")) and (not k or f)
    world["wild"] = {**(world.get("wild") or {}), "methods_known": {"Ash": ["net"]}}
    w2 = build(world, history=2)
    assert "net" in w2.s["know"]["Ann"] and "stalk" not in w2.s["know"]["Ann"]      # an arm's override (stage 0)
    assert water is not None


def test_what_agents_see_has_no_multipliers_or_kinds_and_refusals_no_catalogue(generated):  # noqa: F811
    from cybertron2.engine import prompt as PR
    from cybertron2.engine.here import Here, Mind
    world = copy.deepcopy(generated)
    world["agents"] = {"Ann": {"household": "Ash", "stage": "adult", "sex": "f", "at": "s1",
                               "knows": {m: {"level": "known", "skill": 1.2} for m in MT.TAKE_METHODS}}}
    w = build(world, history=2)
    from cybertron2.engine import run as R
    w.s["today"] = R.blank_today()
    text = PR.system_prompt(Here(w, "Ann"), Mind(w, "Ann"))
    for m in MT.METHODS:
        note = MT.METHODS[m]["note"]
        assert not re.search(r"x[0-9]", note) and not (_words(note) & KIND_WORDS), m
        if m in text:
            assert f"{m} ({note})" in text
    r = _do(w, "Ann", {"do": "gather", "what": "spear the moon", "at": "anywhere"})
    assert "efused" in r.upper().replace("REFUSED", "efused") and "stalk" not in r and "snare" not in r
    r = _do(w, "Ann", {"do": "gather", "what": "hunt the wild", "at": next(p["name"] for p in w.s["parcels"].values()
                                                                            if p["node"] == "s1" and p["cover"] == "forest"),
                       "looking for": "unicorn"})
    assert "no beast called" in r


def test_method_skill_is_one_record_for_every_kind_it_takes(generated):  # noqa: F811
    from cybertron2.engine import knowledge as KN, run as R
    from cybertron2.engine.here import Mind
    world = copy.deepcopy(generated)
    world["agents"] = {f"H{i}": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1",
                                 "knows": {"stalk": {"level": "known", "skill": 1.0}}} for i in range(20)}
    w = build(world, history=2)
    w.s["today"] = R.blank_today()
    wood = next(p["name"] for p in w.s["parcels"].values() if p["node"] == "s1" and p["cover"] == "forest")
    before = KN.skill(Mind(w, "H0"), "stalk")
    for _ in range(3):
        _do(w, "H0", {"do": "gather", "what": "stalk", "at": wood, "range": "the wood around"})
    assert KN.skill(Mind(w, "H0"), "stalk") > before                        # one skill: what it is used on, red deer or roe, is the same
    assert "stalk deer" not in w.s["know"]["H0"]
