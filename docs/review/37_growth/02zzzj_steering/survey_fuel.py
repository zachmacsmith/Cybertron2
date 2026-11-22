"""Survey 3: does the firewood fallback follow need? For each morning that shows one's house store ("fuel for about N such nights"),
whether the plan's fallback names firewood, by how many nights of fuel the store held. All decision calls whose message carries the
line (stretch openings show the house; later mornings show the store's changes and, from the house line, the same figure)."""
import collections, re, json
import load

B = [(0, 10), (10, 20), (20, 40), (40, 80), (80, 10 ** 6)]
out = {}
for run in load.available():
    t = collections.defaultdict(lambda: [0, 0, 0])
    for x in load.rows(run):
        if x["kind"] != "decision":
            continue
        m = load.blob(run, x["message_sha"]) or ""
        f = re.findall(r"fuel for about (\d+) such nights", m)
        if not f:
            continue
        n = int(f[0])
        b = next(f"{lo}-{hi if hi < 10 ** 6 else ''}" for lo, hi in B if lo <= n < hi)
        fb = [a for a in (x["reply"].get("fallback") or []) if isinstance(a, dict)]
        acts = [a for a in (x["reply"].get("actions") or []) if isinstance(a, dict)]
        t[b][0] += 1
        t[b][1] += any("firewood" in str(a.get("what", "")) for a in fb)
        t[b][2] += any("firewood" in str(a.get("what", "")) for a in acts)
    if t:
        out[run] = {k: v for k, v in sorted(t.items(), key=lambda kv: int(kv[0].split("-")[0]))}
        print(run, "  nights of fuel: [mornings, fallback names firewood, plan names firewood]")
        for k, v in out[run].items():
            print(f"   {k:>7}: {v[0]:4}  fallback firewood {v[1] / v[0]:.0%}  plan firewood {v[2] / v[0]:.0%}")
json.dump(out, open("survey_fuel.json", "w"), indent=1)
