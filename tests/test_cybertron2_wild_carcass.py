"""Brief 3 of the wild layer (D2-205, D2-207; proposals/carcass_and_decay.md §7): a carcass's stages by size, season and frost; what
comes to the dead (the groups' carcass rows, the carrion pool, spillover, the bear's cache); burning and graves deep or shallow;
tallow and the tallow light."""
import copy

from cybertron2.engine import night as N, run as R, things as TH, wild as WL
from cybertron2.engine.data import TECHNIQUES, THINGS
from cybertron2.wild import kinds as WK

from tests.test_cybertron2_wild import _do, _summer_world, build, generated  # noqa: F401
from tests.test_cybertron2_wild_raiders import _ready


def _with_people(generated, n=3):
    world = copy.deepcopy(generated)
    world["agents"] = {f"P{i}": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1", "knows": {}} for i in range(n)}
    return world


def _pasture(w, node="s1"):
    return next(pid for pid, p in sorted(w.s["parcels"].items()) if p["node"] == node and p["cover"] in ("pasture", "meadow"))


def _dead(w, beast="cow", role="cows", pid=None, cause="other"):
    pid = pid or _pasture(w)
    return TH.leave_carcass(w, "s1", beast, "the Test herd", [], cause, TECHNIQUES["slaughter"]["yield"]["gives"][role], parcel=pid)


def _nights(w, k, cold=False):
    for _ in range(k):
        if cold:
            w.cold_days.add(w.d)
        for cid, c in list(w.s["containers"].items()):
            if c["kind"] == "carcass" and c.get("beast"):
                N._carcass_night(w, cid, c)
        w.s["day"] += 1


def test_a_carcass_lasts_by_its_size_faster_in_summer_and_stalled_by_frost(generated):  # noqa: F811
    def days_to_bones(beast, role, season_day, cold=False):
        w = build(generated)
        w.s["day"] = season_day
        w.cold = lambda at, day=None: cold                                        # the night's frost held fixed
        cid = _dead(w, beast, role)
        for k in range(40):
            if TH.carcass_bones(w, w.s["containers"][cid]):
                return k
            _nights(w, 1, cold)
        return 99
    w0 = build(generated)
    season = lambda name: next(d for d in range(80) if w0.calendar(d)["season"] == name and w0.calendar(d)["day"] == 1)
    spring, summer = season("spring"), season("summer")
    calf, cow = days_to_bones("calf", "young", spring), days_to_bones("cow", "cows", spring)
    assert calf < cow and 4 <= calf <= 9 and 8 <= cow <= 13                       # medium to about day 6, large to about day 10
    assert days_to_bones("cow", "cows", summer) < cow                             # summer faster
    assert days_to_bones("cow", "cows", spring, cold=True) == 99                  # every night frozen: it keeps


def test_a_fox_group_comes_to_a_carcass_and_eats_of_it(generated):  # noqa: F811
    w, _ = _summer_world(generated, kind="fox")
    cid = _dead(w)
    before = TH.flesh(w, w.s["containers"][cid])
    trow = next(t for t in WK.NEAR_PEOPLE["fox"]["targets"] if t.get("what") == "carcass")
    _ready(w, "fox", cid, dict(trow))
    w.s["wild"]["groups"]["fox@s1"]["parcel"] = w.s["containers"][cid]["parcel"]
    rec = N.night(w)
    v = (rec.get("wild") or {}).get("groups", {}).get("fox@s1") or {}
    assert v.get("ate", 0) > 0 and TH.flesh(w, w.s["containers"][cid]) < before
    assert (w.s["wild"]["groups"]["fox@s1"].get("fed_at") or {}).get("node") == "s1"


def test_the_dead_draw_their_kinds_and_a_carcass_row_has_no_pull_without_them(generated):  # noqa: F811
    w = build(generated)
    trow = next(t for t in WK.NEAR_PEOPLE["wolf"]["targets"] if t.get("what") == "carcass")
    assert WL._carcass_pull(w, "s1", trow) == 0.0 and WL._targets(w, "s1", trow) == []
    cid = _dead(w)
    assert WL._carcass_pull(w, "s1", trow) > 0.5 and WL._targets(w, "s1", trow)[0][0] == cid


def test_the_carrion_eaters_eat_of_a_carcass_and_birds_show_over_it(generated):  # noqa: F811
    w = build(generated)
    cid = _dead(w)
    before = TH.flesh(w, w.s["containers"][cid])
    pool = list(w.s["wild"]["state"]["carrion"])
    lost, birds = 0.0, False
    for _ in range(3):
        N.night(w)
        w.s["day"] += 1
        birds = birds or w.s["containers"][cid].get("birds") is not None
    after = TH.flesh(w, w.s["containers"][cid])
    assert after < before
    assert birds
    i = WL.model(w).ids.index(w.s["wild"]["land"]["home"]["s1"])
    assert w.s["wild"]["state"]["carrion"][i] < pool[i] + 50                       # the loan goes back: the pool does not keep it


def test_a_fox_fed_at_the_dead_by_the_houses_tries_the_hens_more(generated):  # noqa: F811
    def tries(fed):
        n = 0
        for k in range(30):
            w, _ = _summer_world(generated, kind="fox")
            w.s["day"] = 12 + k
            g = {"kind": "fox", "node": "s1", "pos": "home", "t": -1, "raid": -1, "found": -99, "habit": {}, "wary": -1, "rest": -1,
                 "target": None, "what": None, "n": 2}
            if fed:
                g["fed_at"] = {"node": "s1", "day": w.d - 1}
            w.s["wild"].setdefault("groups", {})["fox@s1"] = g
            N.night(w)
            g2 = w.s["wild"]["groups"].get("fox@s1") or {}
            if g2.get("what") in ("items", "hens") and g2.get("pos") in ("edge", "ready"):
                n += 1
        return n
    assert tries(True) > tries(False)


def test_taking_at_a_bears_cached_carcass_meets_the_bear(generated):  # noqa: F811
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    cid = _dead(w)
    w.s["containers"][cid]["cached"] = {"kind": "brown bear", "until": w.d + 3}
    r = _do(w, "P0", {"do": "take", "item": "hide", "from": TH.parcel_name(w, w.s["containers"][cid])})
    assert "bear" in r and "kill" in r
    assert w.s["containers"][cid]["goods"].get("hide", 0) > 0                     # nothing taken


def test_burning_a_carcass_leaves_nothing_for_what_comes(generated):  # noqa: F811
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    cid = _dead(w)
    from cybertron2.engine.here import Here
    hands = Here(w, "P0").hands
    w.s["containers"][hands]["goods"]["firewood"] = 20
    r = _do(w, "P0", {"do": "work", "what": "burn", "at": "the dead cow"})
    assert "burned" in r, r
    c = w.s["containers"][cid]
    assert c.get("burnt") is not None and TH.flesh(w, c) == 0 and cid not in TH.open_dead(w, "s1")
    assert w.s["containers"][hands]["goods"]["firewood"] == 20 - THINGS["carcass_sizes"]["large"]["burn"]["firewood"]


def test_a_deep_grave_draws_nothing_and_a_shallow_one_is_sometimes_dug(generated):  # noqa: F811
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    deep, shallow = _dead(w), _dead(w)
    for cid, depth in ((deep, "deep"), (shallow, "shallow")):
        w.s["containers"][cid].update(buried=w.d, depth=depth)
    trow = next(t for t in WK.NEAR_PEOPLE["fox"]["targets"] if t.get("what") == "carcass")
    found = [cid for cid, _ in WL._targets(w, "s1", trow)]
    assert deep not in found and shallow in found
    assert WL._carcass_pull(w, "s1", trow) <= float(WK.CARCASS_PULL["dig"]) + 1e-9   # a tenth of an open one
    boar = next(t for t in WK.NEAR_PEOPLE["wild boar"]["targets"] if t.get("what") == "carcass")
    assert shallow not in [cid for cid, _ in WL._targets(w, "s1", boar)]          # only diggers find it


def test_a_shallow_burial_takes_half_the_digging(generated):  # noqa: F811
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    cid = _dead(w, "calf", "young")
    w.s["containers"][cid]["died"] = w.d
    for _ in range(6):
        r = _do(w, "P0", {"do": "work", "what": "bury", "at": "the dead calf", "method": "shallow"})
        if w.s["containers"][cid].get("buried") is not None:
            break
    assert w.s["containers"][cid].get("depth") == "shallow", r


def test_slaughter_gives_tallow_and_tallow_makes_lights_that_light_night_pest_work(generated):  # noqa: F811
    gives = TECHNIQUES["slaughter"]["yield"]["gives"]
    assert gives["cows"]["tallow"] > 0 and gives["young"]["tallow"] > 0
    assert TECHNIQUES["make tallow lights"]["gives"] == {"tallow light": 4}
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    from cybertron2.engine.here import Here
    here = Here(w, "P0")
    pid = next(p for p in sorted(here.parcels()) if here.parcels()[p]["cover"] == "field")
    y = {"load": "slugs", **WK.LOADS["slugs"]["guard"]}
    plain = WL.guard(here, pid, dict(y), "the field")
    cut0 = w.s["wild"]["guard"][pid]["cut"]
    w.s["containers"][here.hands]["goods"]["tallow light"] = 2
    lit = WL.guard(here, pid, dict(y), "the field")
    assert w.s["wild"]["guard"][pid]["cut"] > cut0 and "tallow light" in lit and "tallow light" not in plain
    assert w.s["containers"][here.hands]["goods"]["tallow light"] == 1


def test_society_a_dead_cow_left_by_the_herd_draws_the_wolves_and_one_burned_does_not(generated):  # noqa: F811
    """§7 society-level (dry): a dead cow left where the herd grazes draws the wolves to it; burned, nothing comes. (The brief's
    further expectation, that the herd then loses more, does not hold in this world as built: the wolves feed on the carcass
    instead of a cow while it lasts, and the spillover after does not make it up; 14 kills against 16 over 6 nights, 30 against
    33 over 12; reported at the gate, 02zx.)"""
    def came(left):
        n = 0
        for k in range(20):
            w, _ = _summer_world(generated, kind="wolf")
            w.s["day"] = 12 + k
            m = WL.model(w)
            w.s["wild"]["state"]["cond"]["wolf"] = [0.9] * m.n                     # not hungry: they come for the dead
            herds = [h for h in w.s["herds"].values() if h.get("node") == "s1" and h.get("parcel")]
            if not herds:
                return None
            cid = _dead(w, pid=herds[0]["parcel"])
            if not left:
                w.s["containers"][cid]["burnt"] = w.d
                for i in list(w.s["containers"][cid]["goods"]):
                    w.s["containers"][cid]["goods"][i] = 0.0
            for night in range(6):
                rec = N.night(w)
                w.s["day"] += 1
                n += sum(1 for g, v in ((rec.get("wild") or {}).get("groups") or {}).items() if g.startswith("wolf") and v.get("ate", 0) > 0)
        return n
    left, burned = came(True), came(False)
    if left is None:
        return
    assert left > 0 and burned == 0


def test_society_bodies_left_unburied_draw_scavengers_where_buried_ones_do_not(generated):  # noqa: F811
    def came(buried):
        n = 0
        for k in range(10):
            w, _ = _summer_world(generated, kind="fox")
            w.s["day"] = 12 + k
            pid = _pasture(w)
            cid = w.apply("new_thing", "s1", node="s1", parcel=pid, kind="remains", body=True, of="Someone", died=w.d)
            if buried:
                w.s["containers"][cid].update(buried=w.d, depth="deep")
            for night in range(3):
                rec = N.night(w)
                w.s["day"] += 1
                n += sum(1 for v in ((rec.get("wild") or {}).get("groups") or {}).values() if v.get("ate", 0) > 0)
            n += 1 if float(w.s["containers"][cid].get("eaten", 0)) > 0 else 0
        return n
    assert came(False) > came(True) == 0
