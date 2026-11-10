import sys, copy
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import ev_harness as E
from cybertron2.engine import wild as WD
from cybertron2.wild import ecology as EC
w = E.World(E.gen(7, "settled lowland and frontier", "autumn"))
m = WD.model(w); land = w.s["wild"]["land"]
st0 = copy.deepcopy(w.s["wild"]["state"])
node = "s1"
ring = [i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a].get("node") == node][0]
k0 = WD.eco_day(w, 0); Y = w.year_days(); off = WD.HISTORY_AHEAD_YEARS * Y + WD.HISTORY_YEARS * Y
def run(cut):
    st = copy.deepcopy(st0)
    for k in ("roe deer", "red deer"):
        p = list(st["pop"][k]); p[ring] *= (1 - cut); st["pop"][k] = p
    out = []
    for d in range(2 * Y):
        if d % 4 == 0: out.append(round(float(st["pop"]["roe deer"][ring]) * float(m.km2[ring]), 1))
        EC.step(m, st, k0 + d, WD.weather(w, sorted(set(m.nodes)), off + d), WD.draws(w, k0 + d, "history"))
    return out
a, b = run(0.0), run(0.5)
print("days:", list(range(0, 2 * Y, 4)))
print("control roe in the ring:", a)
print("halved  roe in the ring:", b)
print("gap closed (share):", [round(1 - (x - y) / max(a[0] * 0.5, 1e-9), 2) for x, y in zip(a, b)])
