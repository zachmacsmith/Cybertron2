"""Summarise the targeted LLM tests: each arm against the scripted households on the same land and draws."""
import json, sys, collections, numpy as np
res = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "llm_runs/results_T1_T2_T3.json"))
by = collections.defaultdict(list)
for r in res:
    by[(r["test"], r["model"], r["level"], r["named"], r["lore"])].append(r)
for key in sorted(by):
    rs = by[key]
    n = lambda f: float(np.mean([f(r) for r in rs]))
    beh = collections.defaultdict(list)
    for r in rs:
        for k, v in r["behaviour"].items():
            if isinstance(v, (int, float)) and v is not None:
                beh[k].append(v)
    print(f"{key[0]} {key[1]:6s} {key[2]:7s} {key[3]:6s} lore={str(key[4])[0]} | net {n(lambda r: r['score']['net']):+6.1f} "
          f"(none {n(lambda r: r['baselines']['none']['net']):+6.1f}, calendar {n(lambda r: r['baselines']['calendar']['net']):+6.1f}, "
          f"scripted {n(lambda r: r['baselines']['scripted expert']['net']):+6.1f}) loss {n(lambda r: r['score']['loss']):5.1f} "
          f"work {n(lambda r: r['score']['work']):5.1f} child {n(lambda r: r['score']['child']):4.1f} | "
          + " ".join(f"{k}={np.mean(v):.2f}" for k, v in beh.items()) + f" | ${sum(r.get('cost_usd', 0) for r in rs):.2f} calls {sum(r['calls'] for r in rs)}")
