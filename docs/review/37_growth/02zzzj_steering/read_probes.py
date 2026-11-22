"""Read probes 1 and 2: per variant, the fallback (has one, names firewood, its first act), the plan (acts, units it names, firewood
in the plan, investing acts), the why (words, today, tomorrow, long-horizon words), notes; per point, what changed."""
import json, re, collections, statistics as st, sys

LONG = re.compile(r"\b(winter|spring|autumn|season|seasons|year|years|generations?|long run|further ahead|weeks?|"
                   r"in the days to come|days ahead|next few days|lay by|store up|before the cold|stock(?:pile)?)\b", re.I)
TODAY = re.compile(r"\btoday\b", re.I)
TOMORROW = re.compile(r"\btomorrow\b", re.I)
INVEST = {"build", "make", "claim", "teach", "learn", "watch", "partner", "found", "offers"}
WORK_INVEST = re.compile(r"clear|plough|sow|fence|manure|repair|build|smoke|salt|dry meat|trap|weir|net|snare", re.I)


def acts(o, k="actions"):
    return [a for a in (o.get(k) or []) if isinstance(a, dict)]


def sig(a):
    return f"{a.get('do')} {a.get('what') or a.get('item') or ''}".strip()


def row(o):
    why = str(o.get("why") or "")
    A, F = acts(o), acts(o, "fallback")
    return {"why_words": len(why.split()), "today": bool(TODAY.search(why)), "tomorrow": bool(TOMORROW.search(why)),
            "long": len(LONG.findall(why)), "acts": len(A), "distinct": len({sig(a) for a in A}),
            "invest": sum(1 for a in A if a.get("do") in INVEST or (a.get("do") in ("work", "gather") and WORK_INVEST.search(str(a.get("what", ""))))),
            "fb": bool(F), "fb_n": len(F), "fb_firewood": any("firewood" in str(a.get("what", "")) for a in F),
            "plan_firewood": any("firewood" in str(a.get("what", "")) for a in A), "fb_first": sig(F[0]) if F else "",
            "notes": len(o.get("note") or []), "rest": sum(a.get("do") == "rest" for a in A + F), "why": why,
            "acts_sig": [sig(a) for a in A], "fb_sig": [sig(a) for a in F]}


def table(rows, keys, label):
    by = collections.defaultdict(list)
    for r in rows:
        by[r["variant"]].append(r)
    print(f"\n{label}")
    print("| variant | n | " + " | ".join(keys) + " |")
    print("|---|---|" + "---|" * len(keys))
    for v in sorted(by, key=lambda v: "A A2 B C H N".split().index(v) if v in "A A2 B C H N".split() else 9):
        xs = by[v]
        cells = []
        for k in keys:
            vals = [x[k] for x in xs]
            cells.append(f"{sum(vals) / len(vals):.0%}" if isinstance(vals[0], bool) else f"{st.mean(vals):.2f}")
        print(f"| {v} | {len(xs)} | " + " | ".join(cells) + " |")


def probe1(path="probe1.jsonl"):
    rows = []
    for l in open(path):
        d = json.loads(l)
        r = row(d["out"] or {})
        r.update(variant=d["variant"], key=d["key"], model=d["model"])
        rows.append(r)
    table(rows, ["fb", "fb_firewood", "fb_n", "plan_firewood", "acts", "distinct", "invest", "rest", "why_words", "today", "long", "notes"],
          "Probe 1: stretch-opening mornings")
    print("\nPer point (fallback first act | plan acts):")
    by = collections.defaultdict(dict)
    for r in rows:
        by[(r["key"], r["model"])][r["variant"]] = r
    for (k, m), vs in by.items():
        print(f"- {k} ({m})")
        for v in ("A", "A2", "B", "C", "H"):
            if v in vs:
                x = vs[v]
                print(f"    {v:2}: fb [{', '.join(x['fb_sig'])}] | plan [{', '.join(x['acts_sig'])}]")
    return rows


def probe2(path="probe2.jsonl"):
    rows = []
    for l in open(path):
        d = json.loads(l)
        r = row(d["out"] or {})
        r.update(variant=d["variant"], key=d["key"], model=d["model"], step=d["step"])
        rows.append(r)
    for step in ("evening", "morning"):
        table([r for r in rows if r["step"] == step], ["why_words", "today", "tomorrow", "long", "acts", "invest", "fb_firewood", "notes"],
              f"Probe 2: {step}")
    print("\nProbe 2 whys (evening -> morning):")
    by = collections.defaultdict(dict)
    for r in rows:
        by[(r["key"], r["model"])][(r["variant"], r["step"])] = r
    for (k, m), vs in by.items():
        print(f"- {k} ({m})")
        for v in ("A", "A2", "N"):
            for s in ("evening", "morning"):
                if (v, s) in vs:
                    print(f"    {v:2} {s:7}: {vs[(v, s)]['why'][:260]}")
    return rows


if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2"]
    if "1" in which:
        probe1()
    if "2" in which:
        probe2()
