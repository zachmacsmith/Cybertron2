"""Survey 2: other signs of steering across the runs: the why's horizon, words echoed from the reply format's examples, what is
attended (and where it sits in the enum), verbs used and never used, defaults never changed, enum order effects (on trouble,
meeting, overwork), and notes. Prints a table per question; writes survey_all.json."""
import collections, json, re
import load

FUT = re.compile(r"\b(tomorrow|next days?|days ahead|this week|season|winter|spring|autumn|harvest|year|years|future|later|"
                 r"store up|lay by|for the cold|before the|until|children|generations?|long run|further ahead)\b", re.I)
LONG = re.compile(r"\b(winter|spring|autumn|season|year|years|generations?|long run|further ahead|weeks?)\b", re.I)
TODAY = re.compile(r"\btoday\b", re.I)
OFFER_EX = {"2 bread": re.compile(r"^\s*2 bread\s*$", re.I), "copper tool by day": re.compile(r"copper tool by day", re.I),
            "every N days for N times": re.compile(r"every \d+ days? for \d+ times", re.I), "work N days": re.compile(r"^work \d+ days?$", re.I)}

res = {}
agg = collections.defaultdict(collections.Counter)
for run in load.available():
    rs = load.rows(run)
    R = collections.defaultdict(collections.Counter)
    for x in rs:
        r, k, m = x["reply"], x["kind"], x["model"]
        if k not in ("decision", "evening", "talk"):
            continue
        why = str(r.get("why") or "")
        if why:
            R[f"why:{k}"]["n"] += 1
            R[f"why:{k}"]["words"] += len(why.split())
            R[f"why:{k}"]["starts_today"] += why.lower().startswith(("today", "this morning", "this day"))
            R[f"why:{k}"]["has_today"] += bool(TODAY.search(why))
            R[f"why:{k}"]["has_tomorrow"] += bool(re.search(r"\btomorrow\b", why, re.I))
            R[f"why:{k}"]["has_long"] += bool(LONG.search(why))
            R[f"why_long_by_model:{k}"][m + " n"] += 1
            R[f"why_long_by_model:{k}"][m + " long"] += bool(LONG.search(why))
        for o in r.get("offers") or []:
            if not isinstance(o, dict):
                continue
            R["offers"]["n"] += 1
            for side in ("give", "get"):
                v = str(o.get(side) or "")
                for name, rx in OFFER_EX.items():
                    if rx.search(v):
                        R["offers"][f"{side} ~ {name}"] += 1
            R["offer_to"][str(o.get("to"))[:20] if o.get("to") == "anyone" else "a person"] += 1
        acts = [a for a in (r.get("actions") or []) if isinstance(a, dict)]
        if k == "decision":
            R["attend"][str(r.get("attend"))[:40]] += 1
            R["counts"]["plans"] += 1
            R["counts"]["acts"] += len(acts)
            R["counts"]["notes written"] += len(r.get("note") or [])
            R["counts"]["pins"] += bool(r.get("pin"))
            R["counts"]["opened notes"] += len(r.get("open") or [])
            R["counts"]["look_up"] += len(r.get("look_up") or [])
            R["counts"]["explain"] += len(r.get("explain") or [])
            R["counts"]["tell"] += len(r.get("tell") or [])
            R["counts"]["say"] += len(r.get("say") or [])
            R["counts"]["offers"] += len(r.get("offers") or [])
            if "overwork" in r:
                R["overwork"][str(r.get("overwork"))] += 1
        for a in acts + [a for a in (r.get("fallback") or []) if isinstance(a, dict)]:
            v = str(a.get("do"))
            R["verbs"][v] += 1
            if v == "travel":
                R["travel on trouble"][str(a.get("on trouble"))] += 1
                R["travel meeting"][str(a.get("meeting"))] += 1
                R["travel when"][str(a.get("when"))] += 1
            if v == "set":
                R["set"][f"{a.get('thing')} -> {a.get('to')}"] += 1
            if v == "host":
                R["host feed"][str(a.get("feed"))] += 1
            if v == "grant":
                R["grant what"][str(a.get("what"))] += 1
            if v in ("work", "gather", "make", "build"):
                R["crafts"][f"{v} {a.get('what')}"] += 1
            if v == "order":
                R["order"][str(a.get("what"))] += 1
    res[run] = {k: dict(v) for k, v in R.items()}
    for k, v in R.items():
        agg[k].update(v)
    print(f"\n==== {run} ({load.RUNS[run]})")
    for k in ("why:decision", "why:evening", "why:talk"):
        v = R.get(k)
        if v and v["n"]:
            print(f"  {k}: n {v['n']}, words {v['words'] / v['n']:.0f}, starts 'today' {v['starts_today'] / v['n']:.0%}, says today "
                  f"{v['has_today'] / v['n']:.0%}, tomorrow {v['has_tomorrow'] / v['n']:.0%}, a long horizon {v['has_long'] / v['n']:.0%}")
    print("  counts:", dict(R["counts"]))
    print("  attend:", R["attend"].most_common(6))
    print("  offers:", dict(R["offers"]))
    print("  verbs:", R["verbs"].most_common(40))
    for k in ("travel on trouble", "travel meeting", "travel when", "set", "host feed", "grant what", "order", "overwork"):
        if R[k]:
            print(f"  {k}:", dict(R[k]))
print("\n==== ALL RUNS")
for k in ("verbs", "travel on trouble", "travel meeting", "travel when", "set", "host feed", "grant what", "order", "overwork", "offers", "counts"):
    print(f"  {k}:", agg[k].most_common(45))
print("  why_long_by_model decision:", sorted(agg["why_long_by_model:decision"].items()))
json.dump({"runs": res, "all": {k: dict(v) for k, v in agg.items()}}, open("survey_all.json", "w"), indent=1)
