"""Rescore every LLM run from its logged acts (the simulation is deterministic given the acts), with the current rules and the
scripted households on the same land, weather and draws. Writes llm_runs/rescored.json."""
import glob, json, os, types
import llm_tests as L, sim, baselines as B, kinds as K

out = []
for fn in sorted(glob.glob(os.path.join(L.OUT, "T*_*.jsonl"))):
    tag = os.path.basename(fn)[:-6]
    if tag.endswith("_dry"):
        continue
    name, world0, village, level, named, lore, mkey = tag.split("_")
    T = L.TESTS[name]
    r = next(x for x in sim.runs(eras=T["eras"]) if x["world"].split()[0] == world0 and x["village"] == village
             and (x["world"], x["village"]) in T["villages"])
    calls = [json.loads(l) for l in open(fn)]
    acts = {}
    for c in calls:
        a = c["acts"]
        if "watch" in a:
            a["watch"] = {int(g): s for g, s in a["watch"].items()}
        acts[c["day"]] = a
    days = set(d for a, b in T["windows"] for d in range(a, b))
    pol = lambda v, d, obs: acts.get(d, {}) if d in days else {}
    end = max(b for a, b in T["windows"])
    ks = {k: K.KINDS[k] for k in T["kinds"]}
    v, _ = sim.simulate(r, pol, level=level, masked=(named == "masked"), days=end, kinds=ks)
    hh = types.SimpleNamespace(calls=[{"day": c["day"], "acts": acts[c["day"]], "out": c["out"]} for c in calls], window_days=days)
    res = {"test": name, "tag": tag, "world": r["world"], "village": village, "level": level, "named": named, "lore": lore == "lore",
           "model": mkey, "calls": len(calls), "complete": len(calls) == len(days), "score": L.score(v, T), "behaviour": L.behaviour(name, v, hh, T),
           "baselines": {}}
    for bname, bp in (("none", B.none), ("calendar", B.calendar), ("scripted expert", B.expert())):
        vb, _ = sim.simulate(r, L.restrict(bp, T), level="expert", days=end, kinds=ks)
        res["baselines"][bname] = L.score(vb, T)
    out.append(res)
json.dump(out, open(os.path.join(L.OUT, "rescored.json"), "w"), indent=1, default=float)
print(len(out), "runs rescored;", sum(not r["complete"] for r in out), "incomplete")
