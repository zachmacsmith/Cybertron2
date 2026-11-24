"""The history's end keeps the up-runs' spawners (W-111; sweep.md §7 bug 1): the pulses still travelling when the world's history
ends are counted as spawned where they were bound, so no spawning stretch is left empty for good."""
import contextlib
import io

from cybertron2.wild import runs as RU


def test_up_pulses_in_flight_land_where_bound():
    st = {"runs": {"pulses": [{"k": "lamprey", "g": "s1", "d": 5, "n": 3.0, "dir": "up", "to": "head"},
                              {"k": "lamprey", "g": "s2", "d": 5, "n": 2.0, "dir": "up", "to": "head"},
                              {"k": "eel", "g": "s1", "d": 5, "n": 9.0, "dir": "down"}],
                   "spawned": {"lamprey": {"head": 1.0}}}}
    out = RU.land_in_flight(st)
    assert out == {"lamprey": 5.0}
    assert st["runs"]["spawned"]["lamprey"]["head"] == 6.0
    assert st["runs"]["pulses"] == [] and "eel" not in st["runs"]["spawned"]


def test_every_spawning_stretch_keeps_spawners_at_build():
    from cybertron2.engine import wild as WL
    from cybertron2.engine.world import World, load_spec
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec("cybertron2/specs/nutrition/eelmouth.yaml"))
    m = WL.model(w)
    nt, R = RU.net(m), w.s["wild"]["state"]["runs"]
    assert R["pulses"] == []                                              # the run's own nights start with no run under way
    for k, r in RU.runners_of(m).items():
        if r["dir"] == "up":
            sp = R["spawned"].get(k) or {}
            empty = [g for g in nt.spawns(r.get("where", "river"), r.get("spawn")) if float(sp.get(g, 0.0)) <= 1e-6]
            assert not empty, f"{k}: spawning stretches left with no spawners: {empty}"
