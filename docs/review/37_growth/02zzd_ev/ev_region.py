"""Food a unit and kills a trip for the hunting methods on the wild region world (brief 4b as built). CYB_ROOT = the branch checkout."""
import os, sys, copy, json, statistics, yaml
ROOT = os.environ["CYB_ROOT"]; sys.path.insert(0, ROOT)
sys.path.insert(0, "/home/user/cybertron2/docs/review/37_growth/02zzd_ev")
import ev_harness as H
from cybertron2.engine.world import World
from cybertron2.engine.data import TECHNIQUES as T
SPEC = sys.argv[1]   # the world file (its cells beside it); N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
spec = yaml.safe_load(open(SPEC))
os.chdir(os.path.dirname(os.path.abspath(SPEC)))
w0 = World(spec)
who = {"Holtham": "Robin", "Corneby": "Jordan", "Stanmoor": "Osric", "Weirford": "Clement"}
forest = {n: next(p["name"] for p in w0.s["parcels"].values() if p["node"] == n and p.get("cover") == "forest") for n in who}
print(forest)
out = []
for node, p in who.items():
    for method, wood in (("hunt the wild", "the wood around"), ("stalk", "the wood around"), ("hunt the wild", "far")):
        for lvl, sk in (("novice", 0.4), ("capable", 1.0), ("master", 2.3)):
            for armed in (False, True):
                got = []
                for s in range(N):
                    act = {"do": "gather", "what": method, "range": wood, "at": forest[node]}
                    if method == "stalk": act["looking for"] = "deer"
                    g = H.attempt(w0, p, act, method, sk, 0.35 if lvl == "novice" else 0.6, f"{node}{method}{lvl}{armed}{s}", armed=armed)
                    if g is not None: got.append(g)
                if not got: continue
                u = H.units(method, wood)
                kill = sum(1 for g in got if g > 0.05) / len(got)
                out.append((node, method, wood, lvl, armed, len(got), round(kill, 3), round(statistics.mean(got) / u, 3)))
                print(*out[-1], flush=True)
json.dump(out, open(os.environ.get("EV_OUT", "ev_region.json"), "w"))   # written beside the world unless EV_OUT
