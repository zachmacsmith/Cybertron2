"""Survey 1b: the share of the day's done acts that the fallback did, by model, and its firewood share (the evening lists)."""
import collections, json
import load

out = {}
for run in ["water_runs_models_r1", "water_lake_r2", "water_lake_r1", "takeover", "orwell"]:
    t = collections.defaultdict(lambda: [0, 0, 0])
    for x in load.rows(run):
        if x["kind"] != "evening":
            continue
        m = load.blob(run, x["message_sha"]) or ""
        if "## Your day" not in m:
            continue
        for line in m.split("## Your day", 1)[1].split("\n## ", 1)[0].splitlines():
            if line.startswith("- ") and not line.startswith(("- Refused", "- Not done")):
                t[x["model"]][0] += 1
                if "(your fallback)" in line:
                    t[x["model"]][1] += 1
                    t[x["model"]][2] += "firewood" in line
    out[run] = dict(t)
    print(run)
    for mdl, (a, f, fw) in sorted(t.items()):
        print(f"   {mdl:20} done {a:5}  by fallback {f / a:4.0%}  of which firewood {fw / max(1, f):4.0%}")
json.dump(out, open("survey_fallback_models.json", "w"), indent=1)
