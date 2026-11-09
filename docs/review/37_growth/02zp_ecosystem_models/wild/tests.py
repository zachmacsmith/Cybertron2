"""Action tests: policies by skill, answers to scares (D2-198), relevance, lags a run can see, conditions."""
import sys, json, collections, numpy as np
sys.path.insert(0, ".")
import wild as Wd
import run_wild as R
from wild import Y, S, LEVELS, FOOD_NEED, season, sday

INF, TR = R.inference()
MODELS = {k: R.fit(v) for k, v in TR.items()}


def P(ev, L, obs, d, v):
    m, prior = MODELS[(ev, L)]
    return m.get(R.features(ev, obs, d, v), prior)


def policy_for(L):
    """A household reading at level L, acting on what it reads. 'none' does nothing; 'calendar' acts by the season alone."""
    state = {"scare_i": 0, "turns": 0, "pen_until": -1}
    scares = ["fire", "clapper", "horn"]

    def pol(v, d, obs, model):
        if L == "none":
            return {}
        s, sd = season(d), sday(d)
        a = {"shut_hens": True}
        ripening = (s == 1 and sd >= 3) or (s == 2 and sd <= 1)
        if L == "calendar":
            if v.sounder is not None and ripening:
                a["watch"] = {g: "fire" for g in range(3)}
                v.add("boar", 0.0, 6.0)
            a["pen_hens"] = (s == 0 and sd >= 2) or (s == 1 and sd <= 3)
            if v.river and (s == 2 or (s == 3 and sd <= 1)):
                a["traps"] = True
                a["weir_crew"] = False
            if s in (2, 3, 0):
                a["set_nets"] = v.drv.frozen[d - 1] if d else False
                a["fowl"] = bool(v.drv.frun[d - 1] >= 1) if d else False
            if s == 1:
                a["narrow_hives"] = True
            return a
        # boar
        if v.sounder is not None and d >= 2:
            p = P("boar_raid", L, obs, d, v)
            if p > 0.3:
                gap = None
                if L == "expert":
                    for t in (d - 1, d - 2):
                        rd = obs.got(t, "boar", "gap")
                        if rd:
                            gap = rd["gap"]; break
                if L == "expert":
                    sc = "dog" if state["turns"] >= 2 and state["turns"] % 3 == 2 else scares[state["scare_i"] % 3]
                    state["scare_i"] += 1
                else:
                    sc = "fire"
                gaps = [gap] if gap is not None else list(range(3))
                a["watch"] = {g: sc for g in gaps}
                v.add("boar", 0.0, 2.0 * len(gaps))
        # fox
        if d >= 2:
            if obs.got(d - 1, "fox", "fox_kill"):
                state["pen_until"] = d + 2
            day_season = (s == 0 and sd >= 2) or (s == 1 and sd <= 3)
            pen = d <= state["pen_until"]
            if L in ("systematic", "expert") and day_season and P("fox_visit", L, obs, d, v) > 0.3:
                pen = True
            if pen:
                a["pen_hens"] = True
                v.add("fox", -0.05 * v.hens * v.hen_food / 4)                 # penned hens must be fed
            if L == "expert" and s == 0 and sd == 3 and obs.season_reading(d - 1, "voles", "owls") == "silent":
                a["den_control"] = True
        # fowl: nets set ahead on a forecast (or once the freeze has come), fowling while it holds; the expert stops at a fifth
        if s in (2, 3, 0) and d >= 2:
            if L == "novice":
                a["set_nets"] = bool(v.drv.frozen[d - 1])
            else:
                a["set_nets"] = P("freeze_start", L, obs, d + 1, v) > 0.3 or bool(v.drv.frozen[d - 1])
            a["fowl"] = bool(v.drv.frun[d - 1] >= 1) or (L != "novice" and P("freeze_start", L, obs, d, v) > 0.4)
            if L == "expert" and v.flock_taken > 0.2 * v.flock:
                a["fowl"] = False
        # eels
        if v.river and (s == 2 or (s == 3 and sd <= 1)) and d >= 2:
            pe = P("eel_night", L, obs, d, v)
            a["traps"] = True
            a["weir_crew"] = pe > 0.2
        # wasps
        if s == 1 and d >= 2:
            pw = P("wasp_year", L, obs, Y * (d // Y) + S + 5, v)
            if L in ("systematic", "expert") and pw > 0.5:
                a["narrow_hives"] = True
            if L == "expert" and pw > 0.5:
                a["take_nests"] = True
        # slugs: after a mild, wet winter the expert sows the spring corn later into warmer soil, and rolls the autumn seed bed
        if L == "expert" and v.L > 1.4 and s == 0:
            a["sow_later"] = 2
        if L in ("systematic", "expert") and s == 2 and sd == 2 and v.L > 1.3:
            a["roll"] = True
        # voles: cats where voles are thick
        if L in ("systematic", "expert") and obs.season_reading(d - 1, "voles", "voles") in ("many", "thick", "some"):
            a["cats"] = True
        return a
    return pol


def net(v, kind, unit_food=R.UNIT_FOOD):
    out = collections.defaultdict(float)
    for (y, k), r in v.ledger.items():
        if k == kind:
            out[y] += r["yield"] - r["loss"] - r["work"] * unit_food
    return out


def actions():
    pols = ["none", "calendar", "novice", "systematic", "expert"]
    res = collections.defaultdict(lambda: collections.defaultdict(list))
    rel = collections.defaultdict(list)
    for r in R.runs():
        if int(r["village"][1:]) % 2 == 0:
            continue                                                   # test villages only
        for pname in pols:
            L = pname if pname in LEVELS else None
            v, obs = R.simulate(r, policy_for(pname), level=L or "novice", seed_add=0)
            for kind in Wd.KINDS:
                n = net(v, kind)
                applies = (kind != "boar" or v.wood_km2 > 1) and (kind != "eels" or v.river)
                if applies:
                    res[kind][pname].append(sum(n.values()) / max(1, len(n)) / FOOD_NEED)
                    if pname in ("none", "expert"):
                        for y, val in n.items():
                            led = v.ledger.get((y, kind), {})
                            rel[(kind, pname)].append(max(led.get("loss", 0), led.get("yield", 0)) / FOOD_NEED)
    return {k: {p: float(np.mean(x)) for p, x in d.items()} for k, d in res.items()}, \
           {f"{k}|{p}": {"median": float(np.median(x)), "p90": float(np.percentile(x, 90)), "max": float(np.max(x))} for (k, p), x in rel.items()}


def answers():
    """D2-198: the same scare, night after night. Boar get used to it; the fox and the flock are scared off and come back."""
    out = {}
    for r in R.runs():
        if r["world"] != "settled lowland and frontier" or r["village"] not in ("s1", "s3"):
            continue
        for sc_kind in ("same", "varied"):
            seq = []
            i = [0]

            def pol(v, d, obs, m):
                a = {"shut_hens": True}
                if v.sounder is not None:
                    i[0] += 1
                    sc = "fire" if sc_kind == "same" else ["fire", "clapper", "horn"][i[0] % 3]
                    a["watch"] = {g: sc for g in range(3)}
                a["dog"] = True
                return a
            v, _ = R.simulate(r, pol)
            idx = collections.Counter()
            for d in sorted(v.events):
                e = v.events[d]
                y = d // Y
                for k, hit, turned in (("boar", "boar_scare" in e, "boar_turned" in e),
                                       ("fox", "fox_visit" in e and not e.get("fox_day"), "fox_turned" in e)):
                    if hit:
                        idx[(k, y)] += 1
                        out.setdefault(f"{k}|{sc_kind}", []).append((min(idx[(k, y)], 5), int(turned)))
    summ = {}
    for key, xs in out.items():
        by = collections.defaultdict(list)
        for i, t in xs:
            by[i].append(t)
        summ[key] = {"encounters": len(xs), "turned_by_encounter_in_year": {f"{i}{'+' if i == 5 else ''}": round(float(np.mean(by[i])), 2) for i in sorted(by)}}
    return summ


def lags_in_run(window=12):
    """In runs of `window` days, how many kinds show a sign followed by its event within 1 to 3 days (seen by a systematic
    reader), and whether a household acting on it changes the kind's outcome within the run."""
    shows = collections.defaultdict(int); changed = collections.defaultdict(int); n = 0
    per_window = []
    pairs = {"boar": ("boar", "boar_raid"), "fox": ("fox", "fox_visit"), "fowl": ("fowl", "freeze_start"),
             "eels": ("eels", "eel_night"), "slugs": ("slugs", "slug_night"), "wasps": ("wasps", None), "voles": ("voles", None)}
    for r in R.runs():
        if r["era"] not in ("steady", "cold", "wet") or int(r["village"][1:]) % 2 == 0:
            continue
        v0, obs = R.simulate(r, None, level="systematic")
        vE, _ = R.simulate(r, policy_for("expert"), level="expert")
        for start in range(0, v0.drv.n - window, 4):
            n += 1; k_here = 0
            for kind, (sk, ev) in pairs.items():
                got = False
                for d in range(start, start + window):
                    sg = [x for x in obs.seen.get(d, []) if x[0] == sk]
                    if not sg:
                        continue
                    if ev is None:
                        got = True; break
                    if any(v0.events.get(t, {}).get(ev) for t in range(d + 1, min(d + 4, start + window))):
                        got = True; break
                if got:
                    shows[kind] += 1; k_here += 1
                y0, y1 = start // Y, (start + window - 1) // Y
                a = sum(v0.ledger.get((y, kind), {}).get("loss", 0) for y in range(y0, y1 + 1))
                b = sum(vE.ledger.get((y, kind), {}).get("loss", 0) for y in range(y0, y1 + 1))
            per_window.append(k_here)
    return {"windows": n, "share_showing": {k: shows[k] / n for k in pairs},
            "kinds_per_window": {"mean": float(np.mean(per_window)), "p10": float(np.percentile(per_window, 10)),
                                 "min": int(np.min(per_window))}}


def lags_effect(window=12):
    """Within one 12-day run, does changing what the household does change the outcome? Same weather and draws, two policies,
    compared on the losses and yields inside the window only."""
    out = collections.defaultdict(list)
    for r in R.runs():
        if r["era"] != "steady" or int(r["village"][1:]) % 2 == 0:
            continue
        for start in range(0, r["drv"].n - window, 8):
            for kind, act in (("boar", "watch"), ("fox", "pen"), ("eels", "traps"), ("fowl", "nets")):
                def mk(on):
                    def pol(v, d, obs, m):
                        a = {"shut_hens": True}
                        if not (start <= d < start + window) or not on:
                            return a
                        s, sd = season(d), sday(d)
                        if act == "watch" and v.sounder is not None:
                            a["watch"] = {g: ["fire", "clapper", "horn"][d % 3] for g in range(3)}
                        if act == "pen":
                            a["pen_hens"] = True
                        if act == "traps":
                            a["traps"] = True
                        if act == "nets":
                            a["set_nets"] = True; a["fowl"] = True
                        return a
                    return pol
                va, _ = R.simulate(r, mk(False)); vb, _ = R.simulate(r, mk(True))
                def inwin(v):
                    tot = 0.0
                    for d in range(start, start + window):
                        e = v.events.get(d, {})
                    yrs = range(start // Y, (start + window - 1) // Y + 1)
                    return sum(v.ledger.get((y, kind), {}).get("yield", 0) - v.ledger.get((y, kind), {}).get("loss", 0) for y in yrs)
                diff = inwin(vb) - inwin(va)
                applies = (kind != "boar" or va.sounder is not None or vb.sounder is not None) and (kind != "eels" or va.river)
                if applies:
                    out[kind].append(abs(diff) > 0.5)
    return {k: float(np.mean(v)) for k, v in out.items()}


def conditions():
    tally = collections.defaultdict(lambda: collections.defaultdict(int)); years = collections.defaultdict(int)
    seen = set()
    for r in R.runs():
        key = (r["world"], r["era"])
        D = r["drv"]
        for y in range(D.years):
            if (key, y) in seen:
                continue
            seen.add((key, y))
            c = tally[r["era"]]; years[r["era"]] += 1
            m = r["mast"]
            c["heavy mast"] += m[y] >= 3
            c["bust (fail after heavy)"] += y > 0 and m[y - 1] >= 3
            c["hard winter"] += D.hard_winter(y)
            c["bust then hard winter"] += y > 0 and m[y - 1] >= 3 and D.hard_winter(y)
            c["vole peak"] += r["voles"][y] == "peak"
            c["vole crash (hungry year)"] += r["voles"][y] == "crash"
            c["wet winter (slugs)"] += D.anom(y - 1, 3, "wet") > 0.1 if y else 0
            c["warm spring (wasps)"] += D.anom(y, 0, "T") > 0.5
            c["frost at flowering"] += D.flower_frost[y]
    return {e: {k: v / years[e] for k, v in c.items()} for e, c in tally.items()}


if __name__ == "__main__":
    out = {"inference": INF}
    for ev, r in INF.items():
        print(f"{ev:13s} rate {r['base']['rate']:.3f} | " + " | ".join(f"{L[:3]} skill {r[L]['skill']:+.2f} auc {r[L]['auc']:.2f}" for L in LEVELS))
    act, rel = actions()
    out["actions"], out["relevance"] = act, rel
    print("\nnet by policy (share of a village's food need a year; work at", R.UNIT_FOOD, "food a unit)")
    for k, d in act.items():
        print(f"  {k:6s} " + "  ".join(f"{p} {x:+.3f}" for p, x in d.items()))
    print("\nrelevance (loss or yield, share of need, by village-year)")
    for k, x in sorted(rel.items()):
        print(f"  {k:18s} median {x['median']:.3f} p90 {x['p90']:.3f} max {x['max']:.3f}")
    out["answers"] = answers()
    print("\nanswers to scares (D2-198)", json.dumps(out["answers"], indent=0))
    out["lags"] = lags_in_run(); print("\nlags in a 12-day run", out["lags"])
    out["lags_effect"] = lags_effect(); print("acting changes the outcome within the run (share of windows)", out["lags_effect"])
    out["conditions"] = conditions()
    print("\nconditions per year, by era")
    for e, c in out["conditions"].items():
        print(f"  {e:7s} " + "  ".join(f"{k} {v:.2f}" for k, v in c.items()))
    json.dump(out, open("results.json", "w"), indent=1, default=float)
