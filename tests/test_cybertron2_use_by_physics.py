"""D4-114: what is physically there can be used; a claim makes the use seen, it does not stop it. Beasts here can be worked (the
millstones, the plough, a pack ox) whoever holds them; fences wear by the year and a fallen one keeps half its build."""
import copy

from cybertron2.engine import farm as FM, herds as HD
from cybertron2.engine.data import FENCES
from cybertron2.engine.here import Here
from cybertron2.engine.world import World, load_spec

SPEC = load_spec("cybertron2/specs/plenty/brookend.yaml")


def world():
    return World(copy.deepcopy(SPEC))


def test_another_households_ox_can_turn_the_millstones_and_it_is_seen():
    w = world()
    here = Here(w, "Walter")
    hid = next(iter(w.s["herds"]))
    assert not FM._own_or_free(here, hid)                                     # the Crofts' herd
    assert FM.usable_herds(here, "oxen", 1) == [hid]                          # physics: it is here, so it can be worked
    t = {"animals": {"oxen": 1}}
    assert FM.team_shortfall(here, t) == ""
    n = len(w.s["events"]) if isinstance(w.s.get("events"), list) else None
    note = FM.beasts_note(here, t)
    assert "which the Crofts hold" in note
    crofts = Here(w, "Hugh")
    assert FM.beasts_note(crofts, t) == ""                                    # one's own: nothing to note


def test_fences_wear_by_the_year_and_a_fallen_one_keeps_half():
    w = world()
    pid = "bk_west"
    par = w.s["parcels"][pid]
    need = FM.fence_need(par, "wood")["units"]
    par["fence"] = {"kind": "wood", "units": need, "level": 2, "built": True, "gate": "shut", "mend": 0.0, "pending": {}, "since": w.d}
    year = w.year_days()
    for _ in range(year):                                                    # a whole year: a new fence loses nothing in it
        rec = {"herds": []}
        HD._fences(w, rec)
        w.s["day"] += 1
    assert par["fence"]["level"] == 2
    par["fence"].update(level=0)
    here = Here(w, "Hugh")
    w.s["containers"][here.hands]["goods"]["timber"] = 10.0
    FM._fence(here, None, "fence", pid, par["name"], here.hands, 1.0, {}, {"fence": "wood"})
    assert abs(w.s["parcels"][pid]["fence"]["units"] - FENCES["wood"]["kept"] * need) < 1e-3
