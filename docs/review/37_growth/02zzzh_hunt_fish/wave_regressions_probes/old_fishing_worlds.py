"""Old fishing worlds: can a trapper set wicker traps as seeded, make them, or angle with a rod? (wave_regressions.md, finding 1)

    PYTHONPATH=. python3 docs/review/37_growth/02zzzh_hunt_fish/wave_regressions_probes/old_fishing_worlds.py cybertron2/specs/water/river.yaml
"""
import contextlib, io, copy, sys
from cybertron2.engine.world import World, load_spec
from cybertron2.engine import run as R, verbs as V
from cybertron2.engine.here import Here, Mind

def do(w, who, act):
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            return V.do(Here(w, who), Mind(w, who), act)
        except Exception as e:
            return f"CRASH {type(e).__name__}: {e}"

for spec in sys.argv[1:]:
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec(spec))
    w.s["today"] = R.blank_today()
    lv = lambda n, t: ((w.s["know"].get(n) or {}).get(t) or {}).get("level") in ("rough", "capable", "known")
    tr = [n for n in w.s["know"] if lv(n, "trap in water")]
    print(spec, "| trap in water:", len(tr), "| wicker trap (make):", sum(lv(n, "wicker trap") for n in w.s["know"]),
          "| snare:", sum(lv(n, "snare") for n in w.s["know"]), "| wicker traps held:",
          sum(float(w.goods(w.hands(n)).get("wicker trap", 0)) for n in w.s["people"]))
    if not tr:
        continue
    who = tr[0]
    node = w.s["people"][who]["at"]
    water = next((p["name"] for p in w.s["parcels"].values() if p["cover"] == "water" and p["node"] == node), None)
    print("  trap in water, as seeded:", do(copy.deepcopy(w), who, {"do": "gather", "what": "trap in water", "at": water})[:160])
    w2 = copy.deepcopy(w)
    w2.apply("create", node, dst=w2.hands(who), item="withies", qty=5, why="probe")
    print("  make wicker trap with withies in hand:", do(w2, who, {"do": "make", "what": "wicker trap", "qty": 2})[:160])
    w3 = copy.deepcopy(w)
    w3.apply("create", node, dst=w3.hands(who), item="withies", qty=1, why="probe")
    print("  make fishing rod:", do(w3, who, {"do": "make", "what": "fishing rod"})[:160])
    print("  angle with it:", do(w3, who, {"do": "gather", "what": "angle", "at": water})[:160])
