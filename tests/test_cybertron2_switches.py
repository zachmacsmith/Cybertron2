"""Per-world switches that turn a food source off (W-69; OPEN O-3, accepted 20 Nov): farming as a pack on by default and switched
off by `packs_off: [farming]` (engine/packs.py), and the wild's sources switched off in the world's `wild:` table (wild/switches.py):
`kinds_off` (classes or names), `runs_off` and `resident_fish: false`. Each switch does what it says, and a world that sets none
is exactly as it was."""
import contextlib
import copy
import io
import json
import sqlite3
import zlib

import numpy as np
import pytest
import yaml

from cybertron2.engine import knowledge as KN, night as N, packs as PK, run as R, signs as SG, verbs as V, wild as WL
from cybertron2.engine.data import CROPS, TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import Refused, World
from cybertron2.wild import switches as SW

COMBE = "cybertron2/specs/combe.yaml"
HAMLET = "cybertron2/specs/hamlet_s1.yaml"
RUNS = "cybertron2/specs/nutrition/runs_medium.yaml"

FARMING = ["clear", "sow", "hoe", "plough", "ditch", "terrace", "select seed", "weed", "manure", "reap", "hay", "dung", "milk",
           "dry fodder", "cheese", "wooden plough", "method: dibble", "burn the stubble", "pest work"]


def _spec(path, **extra):
    s = yaml.safe_load(open(path))
    for k, v in extra.items():
        if k == "wild":
            s["wild"] = {**(s.get("wild") or {}), **v}
        else:
            s[k] = v
    return s


def _do(w, who, a):
    try:
        r = V.do(Here(w, who), Mind(w, who), a)
    except Refused as e:
        return f"REFUSED {e}"
    return f"REFUSED {r}" if r.startswith("Refused") else r


# ---------------------------------------------------------------------- farming, a pack on by default
def test_farming_rows_are_tagged_and_on_by_default():
    for t in FARMING:
        assert "farming" in ([TECHNIQUES[t]["pack"]] if isinstance(TECHNIQUES[t]["pack"], str) else TECHNIQUES[t]["pack"]), t
        assert PK.on(TECHNIQUES[t], ("wild",)) and PK.on(TECHNIQUES[t], ("wild", "water"))   # on in any world that does not switch it
        assert not PK.on(TECHNIQUES[t], ("wild", "-farming"))                            # off, and off where it does
    assert all(CROPS[c]["pack"] == "farming" for c in CROPS)
    assert PK.on(TECHNIQUES["burn the stubble"], ("wild",)) and not PK.on(TECHNIQUES["burn the stubble"], ())   # both packs needed
    assert not PK.on(TECHNIQUES["burn the stubble"], ("wild", "-farming"))
    assert PK.of(World.__new__(World)) == ()                                            # no spec: as before


def test_packs_off_names_only_a_pack_on_by_default():
    class W:
        spec = {"packs": ["wild"], "packs_off": ["farming"]}
    assert PK.of(W) == ("wild", "-farming")
    W.spec = {"packs": ["wild"]}
    assert PK.of(W) == ("wild",)                                                        # exactly the tuple it was
    W.spec = {"packs_off": ["water"]}
    with pytest.raises(ValueError):
        PK.of(W)


def test_with_farming_off_nothing_farming_resolves_or_is_seeded():
    on, off = World(_spec(HAMLET)), World(_spec(HAMLET, packs_off=["farming"]))
    assert any(p["crop"] for p in on.s["parcels"].values())
    assert not any(p["crop"] or p["works"] for p in off.s["parcels"].values())         # the seeded crops are not there
    PK.use(off)
    for t in FARMING:
        assert KN.resolve(t) is None and t not in PK.techniques(), t
        for al in TECHNIQUES[t].get("aliases") or []:
            assert KN.resolve(al) not in FARMING, al
    assert not {"wooden plough", "green grain", "green rye", "green beans"} & set(PK.items())
    who = sorted(off.living())[0]
    for t in ("sow", "reap", "milk", "plough", "hay"):
        assert _do(off, who, {"do": "work", "what": t}).startswith("REFUSED"), t
    assert not any(t in FARMING and KN.level(Mind(off, n), t) for n in off.living() for t in TECHNIQUES)
    assert not any("dibble" in k for n in off.living() for k, r in off.s["know"].get(n, {}).items()
                   if r.get("source") == "from your upbringing")                         # no one is given dibbling (D2-129)
    lines = json.dumps(off.s["mind"])
    assert "best sown" not in lines and "best sown" in json.dumps(on.s["mind"])          # no sowing lore (D4-105)
    assert not SG._farming()
    PK.use(on)
    assert KN.resolve("sow") == "sow" and SG._farming()


def test_farming_off_keeps_no_hens():
    on, off = World(_spec(RUNS)), World(_spec(RUNS, packs_off=["farming"]))
    hens = lambda w: sum(c.get("goods", {}).get("hen", 0) for c in w.s["containers"].values())   # noqa: E731
    assert hens(on) > 0 and hens(off) == 0


# ---------------------------------------------------------------------- the wild's kinds, by class or name
def test_kinds_off_names_classes_and_kinds_and_refuses_what_it_does_not_know():
    assert SW.kinds_off({"wild": {"kinds_off": ["game"]}}) == {"red deer", "roe deer", "wild boar", "brown hare"}
    assert SW.sites_off({"wild": {"kinds_off": ["game", "fowl"]}}) == {"lodge", "heronry", "rookery"}
    assert SW.kinds_off({"wild": {"kinds_off": ["carn", "wild boar"]}}) >= {"wolf", "salmon", "wild boar"}
    assert SW.plants_off({"wild": {"kinds_off": ["plants"]}}) == set(SW.CLASSES["plants"])
    assert SW.kinds_off({}) == frozenset() and SW.runs_off({}) == frozenset() and SW.resident_fish({})
    with pytest.raises(ValueError):
        SW.kinds_off({"wild": {"kinds_off": ["deer"]}})
    with pytest.raises(ValueError):
        SW.runs_off({"wild": {"runs_off": ["wolf"]}})


@pytest.fixture(scope="module")
def game_off():
    s = _spec(RUNS, wild={"history_years": 1})
    return World(copy.deepcopy(s)), World(_spec(RUNS, wild={"history_years": 1, "kinds_off": ["game", "fowl"]}))


def test_with_game_off_no_deer_or_boar_exist_and_hunting_finds_nothing(game_off):
    on, off = (copy.deepcopy(w) for w in game_off)
    game = SW.CLASSES["game"][:4] + ["woodpigeon", "wildfowl"]
    heads = lambda w, k: float(np.sum(np.asarray(w.s["wild"]["state"]["pop"][k]) * WL.model(w).km2))   # noqa: E731
    assert heads(on, "red deer") > 100 and heads(on, "wild boar") > 100
    assert heads(off, "wolf") > 0 and abs(heads(off, "wolf") - heads(on, "wolf")) / heads(on, "wolf") < 0.5   # the rest go on
    found = {}
    for w in (on, off):
        wood = next(p["name"] for p in w.s["parcels"].values() if p["cover"] == "forest")
        folk = sorted(n for n in w.living() if w.s["people"][n]["stage"] == "adult")
        lines = []
        for d in range(3):
            w.s["today"] = R.blank_today()
            for n in folk:
                lines.append(_do(w, n, {"do": "gather", "what": "hunt the wild", "at": wood, "range": "the wood around"}))
            N.night(w)
            w.s["day"] += 1
        found[id(w)] = " ".join(lines)
        assert not any(r.startswith("REFUSED") for r in lines), [r for r in lines if r.startswith("REFUSED")][:2]
    assert any(f"came on a {k}" in found[id(on)] or f"came on an {k}" in found[id(on)] for k in game)
    assert not any(k in found[id(off)] for k in game + ["deer", "boar", "hare"])
    assert all(heads(off, k) == 0.0 for k in game)                                       # none bred, came or drifted in
    assert not any(g.get("kind") in game for g in (off.s["wild"].get("groups") or {}).values())
    assert not (off.s["wild"].get("legends") or {}) and not any(s["kind"] in ("lodge", "heronry", "rookery")
                                                                 for s in (off.s["wild"].get("sites") or {}).values())
    said = json.dumps([e for e in off.s["events"]]) + json.dumps(off.s["mind"])
    assert not any(x in said for x in ("deer", "boar", "hares", "wildfowl", "pigeon"))


def test_with_plants_off_nothing_grows_to_gather():
    w = World(_spec(RUNS, wild={"history_years": 1, "kinds_off": ["plants"]}))
    from cybertron2.engine.data import RESOURCES
    assert not any(RESOURCES.get(k, {}).get("plant") or k == "plants" for p in w.s["parcels"].values() for k in p["res"])
    who = sorted(w.living())[0]
    wood = next(p["name"] for p in w.s["parcels"].values() if p["cover"] == "forest" and p["node"] == w.s["people"][who]["at"])
    w.s["today"] = R.blank_today()
    r = _do(w, who, {"do": "gather", "what": "gather wild food", "at": wood})
    assert "nothing" in r or r.startswith("REFUSED"), r
    one = World(_spec(RUNS, wild={"history_years": 1, "kinds_off": ["mushrooms"]}))
    ks = {k for p in one.s["parcels"].values() for k in p["res"]}
    assert "mushrooms" not in ks and "berries" in ks


# ---------------------------------------------------------------------- the runs and the resident fish
def _run_pulses(**wild):
    w = World(_spec(RUNS, wild={"history_years": 1, **wild}))
    seen = {}
    for _ in range(9):                                                        # into the autumn runs (the world starts late in summer)
        N.night(w)
        w.s["day"] += 1
        for k, v in WL.run_density(w).items():
            seen[k] = seen.get(k, 0.0) + sum(v)
    return w, seen


def test_runs_off_stops_the_runs_all_or_by_kind():
    _, seen = _run_pulses()
    assert seen.get("eel", 0) > 0 and seen.get("salmon", 0) > 0
    w, seen = _run_pulses(runs_off=True)
    assert not seen and not (w.s["wild"]["state"].get("runs") or {}).get("pulses")
    _, seen = _run_pulses(runs_off=["salmon"])
    assert seen.get("eel", 0) > 0 and not seen.get("salmon")


def test_without_resident_fish_traps_take_only_from_a_run():
    lake = World(_spec("cybertron2/specs/water/lake.yaml", wild={"history_years": 1, "resident_fish": False}))
    assert not any("fish" in p["res"] for p in lake.s["parcels"].values())
    assert not any("fish" in b for b in (lake.s.get("waters") or {}).values())
    caught = {}
    for arm in (True, False):
        w = World(_spec(RUNS, wild={"history_years": 1, "resident_fish": arm}))
        water = next(p["name"] for p in w.s["parcels"].values() if p["cover"] == "water")
        for _ in range(4):                                                    # late summer: no run yet
            w.s["today"] = R.blank_today()
            for n in sorted(n for n in w.living() if w.s["people"][n]["stage"] == "adult"):
                _do(w, n, {"do": "set", "what": "trap in water", "at": water})   # laid anew each day (named alone they are tended: W-97)
            N.night(w)
            w.s["day"] += 1
        caught[arm] = sum(sum(c.get("goods", {}).values()) for c in w.s["containers"].values() if c.get("kind") == "set")
    assert caught[True] > 0 and caught[False] == 0


# ---------------------------------------------------------------------- a world with no switch is as it was
def _before(monkeypatch):
    """The engine as it was before W-69: packs read with the old rule and farming's tags taken away; every wild switch inert."""
    def old_on(row, packs=None):
        live = PK.CURRENT if packs is None else packs
        s = (row or {}).get("pack")
        if isinstance(s, (list, tuple)):
            s = next((x for x in s if x != "farming"), None)
        s = None if s == "farming" else s
        if any(x in live for x in ((row or {}).get("off_with") or ())):
            return False
        return s is None or s in live
    monkeypatch.setattr(PK, "on", old_on)
    monkeypatch.setattr(PK, "of", lambda w: tuple((getattr(w, "spec", None) or {}).get("packs") or
                                                  (getattr(w, "spec", None) or {}).get("systems") or ()))
    for f in ("kinds_off", "plants_off", "sites_off", "runs_off"):
        monkeypatch.setattr(SW, f, lambda spec: frozenset())
    monkeypatch.setattr(SW, "res_on", lambda spec, key: True)
    monkeypatch.setattr(SW, "resident", lambda spec, kind: 1.0)
    monkeypatch.setattr(SG, "_farming", lambda: True)


def _digest(path, tmp):
    w = World(yaml.safe_load(open(path)))
    load = json.dumps(w.s, sort_keys=True, default=str)
    with contextlib.redirect_stdout(io.StringIO()):
        R.run(path, tmp, days=3, bots=True)
    con = sqlite3.connect(str(tmp / "run.db"))
    steps = [(s, json.loads(zlib.decompress(z))["world"]) for s, z in con.execute("SELECT step, z FROM checkpoints ORDER BY rowid")]
    con.close()
    return load, json.dumps(steps, sort_keys=True)


@pytest.mark.parametrize("path", ["cybertron2/specs/valley_s5.yaml", COMBE, "cybertron2/specs/wenbridge.yaml", HAMLET,
                                  "cybertron2/specs/wild_bands.yaml", "cybertron2/specs/water/lake.yaml", RUNS])
def test_every_world_without_a_switch_is_unchanged_after_load_and_three_bot_nights(path, tmp_path, monkeypatch):
    now = _digest(path, tmp_path / "now")
    with monkeypatch.context() as mp:
        _before(mp)
        before = _digest(path, tmp_path / "before")
    assert now[0] == before[0], "the state after load differs"
    assert now[1] == before[1], "the state after three nights with bots differs"
