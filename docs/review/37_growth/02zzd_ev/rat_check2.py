import sys, copy
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import ev_harness as E
from cybertron2.engine import wild as WD
from cybertron2.wild import ecology as EC
season = sys.argv[1]
w = E.World(E.gen(7, "settled lowland and frontier", season))
m = WD.model(w); st = copy.deepcopy(w.s["wild"]["state"])
def tot(k): return round(sum(float(st["pop"][k][i]) * float(m.km2[i]) for i in range(m.n)))
k0 = WD.eco_day(w, 0); Y = w.year_days(); off = WD.HISTORY_AHEAD_YEARS * Y; years = WD.HISTORY_YEARS
row = []
for d in range(Y):   # the pure ecology, continuing the history a year past day 0
    if d % 4 == 0: row.append((d, tot("rats"), tot("fox")))
    EC.step(m, st, k0 + d, WD.weather(w, sorted(set(m.nodes)), off + years * Y + d), WD.draws(w, k0 + d, "history"))
print(season, "start year_day", k0, "pure ecology (day, rats, foxes):", row)
