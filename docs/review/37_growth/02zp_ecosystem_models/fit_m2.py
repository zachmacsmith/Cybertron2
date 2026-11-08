import itertools, io, contextlib, numpy as np, succession as SU, calib_m2 as C
def err(x, lo, hi, none=60):
    if x is None: return none
    return max(0, lo - x, x - hi)
best = []
for rec, sf, cl in itertools.product([0.015, 0.025, 0.04, 0.06], [0.02, 0.04, 0.08], [0.03, 0.05, 0.07]):
    SU.R.update(recruit=rec, seed_far=sf, close=cl)
    o1 = C.run(C.plot(6.0, 7.0, 6.5), {"crop": 1.0, "open": True}, {}, 100, wood_cols=4, track=(5, 5))
    o2 = C.run(C.plot(5.5, 4.0, 4.5), {"crop": 1.0, "open": True}, {}, 120)
    o3 = C.run(C.plot(5.2, 3.0, 2.5), {"graze": 0.2, "burn": 0.3, "cut_bracken": 0.6, "cut_gorse": 0.5}, {}, 80)
    o4 = C.run(C.plot(4.5, 8.0, 3.5, h=150), {"graze": 0.6}, {}, 80)
    o5 = C.run(C.plot(9.5, 6.2, 6.0, h=1), {"mow": 0.7, "cut_reed": 0.5}, {}, 80)
    w = lambda o: C.first(o, lambda x: x["T"] >= 0.5)
    e = (err(w(o1), 25, 40) + err(w(o2), 60, 80) + 30 * max(0, o2[29]["T"] - 0.2) + err(w(o3), 20, 40) + err(w(o5), 20, 40)
         + err(C.first(o4, lambda x: x["B"] >= 0.45 or x["T"] >= 0.3), 10, 20))
    best.append((e, rec, sf, cl, w(o1), w(o2), round(o2[29]["T"], 2), w(o3), C.first(o4, lambda x: x["B"] >= 0.45 or x["T"] >= 0.3), w(o5)))
for b in sorted(best)[:8]: print(b)
