import sys, os
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import ev_harness as E
from cybertron2.engine import run as R, night as NI, wild as WD
w = E.World(E.gen(7, "settled lowland and frontier", sys.argv[1] if len(sys.argv) > 1 else "autumn"))
m = WD.model(w)
def tot(k): st = w.s["wild"]["state"]; return round(sum(float(st["pop"][k][i]) * float(m.km2[i]) for i in range(m.n)))
def home(k): st = w.s["wild"]["state"]; return round(sum(float(st["pop"][k][i]) * float(m.km2[i]) for i in range(m.n) if m.home[i]))
d0 = int(w.s.get("day", 0))
for d in range(9):
    st = w.s["wild"]["state"]
    car = sum(float(st["carrion"][i]) * float(m.km2[i]) for i in range(m.n))
    print(d, "carrion kg", round(car), "rats all", tot("rats"), "rats home", home("rats"), "foxes", tot("fox"), "wolves", tot("wolf") if "wolf" in st["pop"] else None, flush=True)
    w.s["day"] = d0 + d; w.s["events"] = []; w.s["today"] = R.blank_today(); R.dawn(w); NI.night(w)
