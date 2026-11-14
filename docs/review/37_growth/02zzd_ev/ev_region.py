"""Food a unit and kills a trip for the hunting methods on the wild region world (brief 4c as built; brief 4b's version is on main).
CYB_ROOT = the branch checkout.

    CYB_ROOT=<checkout> python3 ev_region.py WORLD.yaml [N] [cells]       fresh ground: each try on a copy of the world at its start
    CYB_ROOT=<checkout> python3 ev_region.py WORLD.yaml deplete [DAYS]    one wood hunted daily, nights run (brief 4c §9)

`cells` (optional, comma-separated) limits the run, e.g. "hunt the wild:the wood around,hunt the wild:far". The levels are on the
hunt's multiplier curve (brief 4c §3.1): novice x1, capable x3, master x8 (its top); familiarity 0.35 for the novice, 0.6 otherwise.
Each row: village, method, range, level, armed, tries, kill share of trips, food a unit, big-game share of trips (a kill of 4 meat or
more), food a trip. Written to EV_OUT (default ev_region.json beside the world).

Brief 4c's results (ev_region_4c*.json beside this) are on the region world made by main's specs/make_wild_region.py --seeds 7 with
CYB_ROOT a peoples-worlds checkout (ecology-hunt3's generator refuses it on capacity; main's writes no wild land): 38 people, the
4b run's hunters replaced by each village's first adult where absent. _find0 is the same with SKILL find_hard 0."""
import os, sys, copy, json, statistics, yaml
ROOT = os.environ["CYB_ROOT"]; sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev_harness as H
from cybertron2.engine.world import World
from cybertron2.engine.here import Here, Mind
from cybertron2.engine import verbs as V, run as R, night as NI
from cybertron2.engine.data import TECHNIQUES as T
SPEC = sys.argv[1]
spec = yaml.safe_load(open(SPEC))
os.chdir(os.path.dirname(os.path.abspath(SPEC)))
w0 = World(spec)
who = {"Holtham": "Robin", "Corneby": "Jordan", "Stanmoor": "Osric", "Weirford": "Clement"}   # 02zze's hunters; else the first adult
for _n in list(who):
    if who[_n] not in w0.s["people"]:
        who[_n] = sorted(x for x, q in w0.s["people"].items() if q.get("at") == _n and q.get("stage") == "adult")[0]
forest = {n: next(p["name"] for p in w0.s["parcels"].values() if p["node"] == n and p.get("cover") == "forest") for n in who}
LEVELS = (("novice", 1.0, 0.35), ("capable", 3.0, 0.6), ("master", 8.0, 0.6))
if os.environ.get("EV_LEVELS") == "4b":                                  # brief 4b's levels on its curve (0.4 to 3.0), for the as-built
    LEVELS = (("novice", 0.4, 0.35), ("capable", 1.0, 0.6), ("master", 2.3, 0.6))
CELLS = (("hunt the wild", "the wood around"), ("stalk", "the wood around"), ("hunt the wild", "far"))


def meat(goods):
    return float((goods or {}).get("meat", 0.0))


def deplete(days):
    """A master, armed, hunting the wood around Holtham every day (one trip a day, the meat taken away each night)."""
    out = []
    for method in ("hunt the wild", "stalk"):
        w = copy.deepcopy(w0)
        node, p = "Holtham", who["Holtham"]
        H.setup(w, p, method, 8.0, 0.6, armed=True)
        d0 = int(w.s.get("day", 0))
        for d in range(days):
            w.s["day"] = d0 + d; w.s["events"] = []
            w.s["today"] = R.blank_today(); R.dawn(w)
            h = Here(w, p)
            before = H.food(w.s["containers"][h.hands]["goods"])
            act = {"do": "gather", "what": method, "range": "the wood around", "at": forest[node]}
            if method == "stalk":
                act["looking for"] = "deer"
            try:
                V.do(h, Mind(w, p), act)
            except Exception as e:  # noqa: BLE001
                print("refused", e); break
            got = H.food(w.s["containers"][Here(w, p).hands]["goods"]) - before
            g = w.s["containers"][Here(w, p).hands]["goods"]
            for it in ("meat", "hide"):
                g.pop(it, None)
            w.s["know"][p][method]["skill"] = 8.0                       # held at the top, so the fall is the wood's, not practice's
            out.append((method, d, round(got / H.units(method, "the wood around"), 3)))
            print(*out[-1], flush=True)
            NI.night(w)
    return out


if len(sys.argv) > 2 and sys.argv[2] == "deplete":
    res = deplete(int(sys.argv[3]) if len(sys.argv) > 3 else 16)
    json.dump(res, open(os.environ.get("EV_OUT", "ev_region_deplete.json"), "w"))
    sys.exit(0)

N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
cells = [tuple(c.split(":")) for c in sys.argv[3].split(",")] if len(sys.argv) > 3 else CELLS
out = []
for node, p in who.items():
    for method, wood in cells:
        for lvl, sk, fam in LEVELS:
            for armed in (False, True):
                got, big = [], []
                for s in range(N):
                    act = {"do": "gather", "what": method, "range": wood, "at": forest[node]}
                    if method == "stalk": act["looking for"] = "deer"
                    g = H.attempt(w0, p, act, method, sk, fam, f"{node}{method}{lvl}{armed}{s}", armed=armed)
                    if g is not None:
                        got.append(g)
                if not got: continue
                u = H.units(method, wood)
                kill = sum(1 for g in got if g > 0.05) / len(got)
                bigs = sum(1 for g in got if g >= 4.0) / len(got)
                out.append((node, method, wood, lvl, armed, len(got), round(kill, 3), round(statistics.mean(got) / u, 3), round(bigs, 3),
                            round(statistics.mean(got), 2)))
                print(*out[-1], flush=True)
json.dump(out, open(os.environ.get("EV_OUT", "ev_region.json"), "w"))   # written beside the world unless EV_OUT
