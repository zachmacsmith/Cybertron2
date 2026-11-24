"""D2-346 (the signs design's bug fixes, W-111): an attend finds what its sentence names or shows nothing (never the place's
background lines), and the covers' background lines are grounded in the state or gone."""
import contextlib
import io

import pytest

from cybertron2.engine import perceive as PC, run as R
from cybertron2.engine.data import COVERS
from cybertron2.engine.here import Here
from cybertron2.engine.world import World, load_spec


@pytest.fixture(scope="module")
def eel():
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec("cybertron2/specs/nutrition/eelmouth.yaml"))
    w.s["today"] = R.blank_today()
    return w


def test_a_name_inside_the_sentence_is_found(eel):
    here = Here(eel, "Peter")
    b = next(iter(here.buildings().values()))["name"]
    sub, label = PC.resolve_target(here, f"the soft salt fish in {b}'s store")
    assert sub.startswith("building:") and label == b
    other = next(x for x in here.people(me=False))
    assert PC.resolve_target(here, f"{other}, who looks gaunt and unsteady")[0] == f"person:{other}"
    assert PC.resolve_target(here, "the place in general")[0] == "place"         # asked for, the place is still the place


def test_nothing_named_is_nothing_shown(eel):
    here = Here(eel, "Peter")
    for x in ("the crack in the wall by the door", "rule 2", {"rule": "first", "n": 1}):
        assert PC.resolve_target(here, x)[0] == "nothing", x


def test_no_cover_speaks_of_what_is_not_there():
    texts = [row[1] for c in COVERS.values() for row in c["ambient"]]
    assert not any("cattle" in t or "dung" in t or "picks" in t for t in texts)
    water = COVERS["water"]["ambient"][0]
    assert water[3]["river"] == ("brook", "river") and set(water[3]["flow"]) <= {"low", "normal"}


def test_a_ambient_condition_is_read_from_the_state(eel):
    here = Here(eel, "Peter")
    pid, p = next((k, v) for k, v in here.parcels().items() if v["cover"] == "water")
    assert PC.ambient_holds(here, pid, p, {"people": 1})
    assert not PC.ambient_holds(here, pid, p, {"people": 10 ** 6})
    assert not PC.ambient_holds(here, pid, dict(p, land={"river": "none"}), {"river": ("brook", "river")})
    with pytest.raises(KeyError):
        PC.ambient_holds(here, pid, p, {"moon": "full"})


def test_what_hangs_is_named_not_assumed_fish():
    """wave_regressions finding 6 (W-111): the gnawed hangings and the smokehouse's smell name what hangs, not 'fish' always."""
    import inspect
    from cybertron2.engine import signs as SG
    from cybertron2.wild.kinds import EATEN_SIGNS
    assert "{what}" in EATEN_SIGNS["hung"][0]["text"] and "fish" not in EATEN_SIGNS["hung"][0]["text"]
    smell = [r for r in SG.BUILDING if r.get("sense") == "smell" and "smoke and" in inspect.getsource(r["text"])]
    assert smell and "'fish' if" not in inspect.getsource(smell[0]["text"])
