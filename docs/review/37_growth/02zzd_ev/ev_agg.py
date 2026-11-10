"""Food a unit by method, range and hunter from ev_sweep's rows:  python3 ev_agg.py ROWS.jsonl [...]"""
import sys, json, collections
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
agg = collections.defaultdict(list)
for r in rows:
    if r["food"] is not None:
        agg[(r["method"], r["where"], r["hunter"], "armed" if r.get("armed") else "")].append(r)
for k in sorted(agg):
    rs = agg[k]; n = len(rs); fpu = [r["food"] / r["units"] for r in rs]
    print(k, f"n={n} success={sum(r['success'] for r in rs)/n:.2f} food/try={sum(r['food'] for r in rs)/n:.2f} "
             f"food/unit={sum(fpu)/n:.2f} (settlements {min(fpu):.2f} to {max(fpu):.2f})")
