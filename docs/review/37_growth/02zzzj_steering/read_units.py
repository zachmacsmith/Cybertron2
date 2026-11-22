"""Probe 1: how many of the morning's units the plan itself names (a rough cost: each work, gather, make, build, rest, watch,
learn or teach act 1 unit, a `try` its "units", a `say` 1, all else 0), against the units the morning gives; and so how many the
fallback is left to fill. Rough: some crafts cost more than one unit, and acts can be refused."""
import json, re, collections, statistics as st, sys
sys.path.insert(0, ".")
import probe_lib as P

ONE = {"work", "gather", "make", "build", "rest", "watch", "learn", "teach"}
units = {}
rows = collections.defaultdict(list)
for l in open("probe1.jsonl"):
    d = json.loads(l)
    if d["key"] not in units:
        m = P.point(d["run"], d["key"])["message"]
        units[d["key"]] = int(re.findall(r"You have (\d+) units of work today", m)[0])
    o = d["out"] or {}
    acts = [a for a in (o.get("actions") or []) if isinstance(a, dict)]
    named = sum(1 for a in acts if a.get("do") in ONE) + sum(int(a.get("units") or 1) for a in acts if a.get("do") == "try") \
        + len(o.get("say") or [])
    rows[d["variant"]].append((units[d["key"]], min(named, units[d["key"]] + int(o.get("overwork") or 0))))
print("| variant | n | units given | units the plan names | left to the fallback (or unused) |")
print("|---|---|---|---|---|")
for v in ("A", "A2", "B", "C", "H", "N"):
    xs = rows[v]
    u, n = st.mean(a for a, b in xs), st.mean(b for a, b in xs)
    print(f"| {v} | {len(xs)} | {u:.2f} | {n:.2f} | {u - n:.2f} ({(u - n) / u:.0%}) |")
