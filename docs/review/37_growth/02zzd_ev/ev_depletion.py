"""Depletion (02zzd): one armed, skilled hunter stalking the wood around every day for two seasons (nights run), and one gatherer working the
same forest parcel every unit of a day; what each try gets as the stock answers.
    CYB_ROOT=<checkout> python3 ev_depletion.py SEED CONFIGURATION SEASON stalk|stalkfar|control|gather [DAYS]"""
import sys, copy, json, time
import ev_harness as E
from cybertron2.engine.world import World, Refused
from cybertron2.engine.here import Here, Mind
from cybertron2.engine import verbs as V, run as R, night as NI, knowledge as KN
from cybertron2.engine import wild as WD
seed, cfg, season, mode = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
cfg = None if cfg == "plain" else cfg
w = World(E.gen(seed, cfg, season))
adults = [n for n, p in w.s["people"].items() if p.get("stage") == "adult" and p.get("alive", True)]
who = adults[0]; node = w.s["people"][who]["at"]
wood = next(p["name"] for p in w.s["parcels"].values() if p["node"] == node and p["cover"] == "forest")
lo, hi = KN.curve("stalk" if mode != "gather" else "gather wild food")
if mode in ("stalk", "control", "stalkfar"):
    E.setup(w, who, "stalk", hi, 0.8)
    g = w.s["containers"][Here(w, who).hands]["goods"]; g["crude weapon"] = 1
    m = WD.model(w); land = w.s["wild"]["land"]
    ring = [i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a].get("node") == node]
    d0 = int(w.s.get("day", 0))
    for d in range(int(sys.argv[5]) if len(sys.argv) > 5 else 16):
        w.s["day"] = d0 + d; w.s["events"] = []
        w.s["today"] = R.blank_today(); R.dawn(w)
        h = Here(w, who); before = E.food(w.s['containers'][h.hands]['goods'])
        out = []
        for t in range(1 if mode in ("stalk", "stalkfar") else 0):
            r = V.do(h, Mind(w, who), {"do": "gather", "what": "stalk", "at": wood, "range": "far" if mode == "stalkfar" else "the wood around", "looking for": "deer"})
            out.append(r[:200])
        got = E.food(w.s['containers'][Here(w, who).hands]['goods']) - before
        st = w.s["wild"]["state"]
        heads = {k: round(sum(float(st["pop"][k][i]) * float(m.km2[i]) for i in ring), 1) for k in ("red deer", "roe deer")}
        pr = {k: round(float(((st.get("pressure") or {}).get(k) or [0]*m.n)[ring[0]]), 2) for k in ("red deer", "roe deer")}
        print(d, w.s["calendar"] if "calendar" in w.s else "", "food", round(got, 2), "ring heads", heads, "pressure", pr, out, flush=True)
        # eat the meat away so hands don't fill
        g = w.s["containers"][Here(w, who).hands]["goods"]
        for it in ("meat", "hide"): g.pop(it, None)
        t0 = time.time(); NI.night(w)
        if d == 0: print("night took", round(time.time() - t0, 1), "s", flush=True)
else:
    E.setup(w, who, "gather wild food", hi, 0.0)
    d0 = int(w.s.get("day", 0))
    for d in range(3):
        w.s["day"] = d0 + d; w.s["events"] = []
        w.s["today"] = R.blank_today(); R.dawn(w)
        row = []
        for u in range(6):
            h = Here(w, who); before = E.food(w.s['containers'][h.hands]['goods'])
            try:
                V.do(h, Mind(w, who), {"do": "gather", "what": "gather wild food", "at": wood})
            except Refused as e:
                row.append("R:" + str(e)[:30]); break
            row.append(round(E.food(w.s['containers'][Here(w, who).hands]['goods']) - before, 2))
        print("day", d, row, flush=True)
        NI.night(w)
