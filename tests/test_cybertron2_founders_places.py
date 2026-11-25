"""The founders' lines follow the world (W-111): the eel lore only where the eels run, read as the engine runs them (wave_regressions
finding 8); other households by where they live and what is known (D2-349): one's own village the neighbour lines, another known
village a line of its own, an unknown village nothing."""
import contextlib
import io

import yaml

from cybertron2.engine import founders as FD, livelihoods as LV
from tests.test_cybertron2_lines import village


def _ids(w, rep, who):
    return FD.wanted(w, who, rep)


def test_eels_run_where_the_engine_runs_them():
    eel = yaml.safe_load(open("cybertron2/specs/nutrition/eelmouth.yaml"))
    lake = yaml.safe_load(open("cybertron2/specs/water/lake.yaml"))
    assert any(FD._runs_at(eel, n, "eel") for n in eel["nodes"])                # the Isel runs to the sea past Eelmouth
    assert not any(FD._runs_at(lake, n, "eel") for n in lake["nodes"])          # Meresby's water is a lake, off the run
    hand = village()                                                            # a hand-written world: no wild land, no runs
    assert not any(FD._runs_at(hand, n, k) for n in hand["nodes"] for k in ("eel", "salmon", "lamprey"))
    eel["wild"]["runs_off"] = ["eel"]
    assert not any(FD._runs_at(eel, n, "eel") for n in eel["nodes"])            # a run switched off is not run


def test_no_eel_lore_where_no_eels_run(monkeypatch):
    w = village()
    with contextlib.redirect_stdout(io.StringIO()):
        rep = LV.fill(w)
    lines = FD.render(w, "Peter", rep, ids=["FI1", "FI2", "HH10"])["lines"]
    assert "FI1" not in lines and "FI2" not in lines and "eels" not in lines.get("HH10", "")
    monkeypatch.setattr(FD, "_runs_at", lambda world, node, kind: kind == "eel")
    lines = FD.render(w, "Peter", rep, ids=["FI1", "FI2", "HH10"])["lines"]
    assert "The eels go down" in lines["FI1"] and "eels run" in lines["HH10"] and "FI2" in lines


def test_other_villages_get_lines_of_their_own_and_unknown_ones_none():
    w = village()
    with contextlib.redirect_stdout(io.StringIO()):
        rep = LV.fill(w)
    ids = _ids(w, rep, "Peter")                                                 # Peter lives at Wendle; the Hunts and Cotters at Thorpe
    assert "NV-hunter:Hunt" in ids and not any(i.endswith(":Hunt") and i.startswith("NB-") for i in ids)
    assert FD.render(w, "Peter", rep, ids=["NV-cottager:Cotter"])["lines"]["NV-cottager:Cotter"].endswith(
        "the Cotters live by work for others and their garden.")
    assert any(i.startswith("NB-") and i.endswith(":Marsh") for i in _ids(w, rep, "Oliver"))     # a neighbour in one's own village
    t = FD.render(w, "Peter", rep, ids=["NV-hunter:Hunt"])["lines"]["NV-hunter:Hunt"]
    assert t.startswith("In Thorpe, a day away, the Hunts live by hunting")
    w["nodes"]["thorpe"]["unexplored"] = True                                   # a place the Marshes have never heard of
    assert not any(i.endswith((":Hunt", ":Cotter")) for i in _ids(w, rep, "Peter"))
    w["agents"]["Nigel"]["places"] = ["thorpe"]                                 # one of the house has been there
    assert "NV-hunter:Hunt" in _ids(w, rep, "Peter")


def test_other_villages_lines_drop_before_any_neighbour():
    assert FD.DROP[0][0] == "other villages' households"
