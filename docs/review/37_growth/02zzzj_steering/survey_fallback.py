"""Survey 1: the fallback. Which acts people write as fallback, how often, whether the reply format's example ("say, gather
firewood") was in their system text, and how many units the fallback actually filled (results marked "(your fallback)")."""
import collections, re, json, sys
import load

EXAMPLE = "(say, gather firewood)"


def sig(a):
    if not isinstance(a, dict):
        return "?"
    return f"{a.get('do')} {a.get('what') or a.get('item') or a.get('thing') or ''}".strip()


out = {}
for run in load.available():
    rs = load.rows(run)
    dec = [x for x in rs if x["kind"] in ("decision", "talk", "evening")]
    # was the example in the system text?
    sy = {x["system_sha"] for x in dec[:50]}
    ex = sum(EXAMPLE in (load.blob(run, s) or "") for s in sy)
    plans = [x for x in rs if x["kind"] == "decision"]
    with_fb = [x for x in plans if x["reply"].get("fallback")]
    first = collections.Counter(sig(x["reply"]["fallback"][0]) for x in with_fb if isinstance(x["reply"]["fallback"], list))
    anyfb = collections.Counter(s for x in with_fb if isinstance(x["reply"]["fallback"], list) for s in {sig(a) for a in x["reply"]["fallback"]})
    bymodel = collections.defaultdict(lambda: [0, 0, 0])
    for x in plans:
        f = x["reply"].get("fallback") or []
        bymodel[x["model"]][0] += 1
        bymodel[x["model"]][1] += bool(f)
        bymodel[x["model"]][2] += any(isinstance(a, dict) and "firewood" in str(a.get("what", "")) for a in f)
    # what the fallback did: evening messages list the day's results; "(your fallback)" marks the fallback's
    ran = collections.Counter()
    acts_total = 0
    fb_total = 0
    for x in rs:
        if x["kind"] != "evening":
            continue
        m = load.blob(run, x["message_sha"]) or ""
        if "## Your day" not in m:
            continue
        day = m.split("## Your day", 1)[1].split("\n## ", 1)[0]
        for line in day.splitlines():
            if not line.startswith("- "):
                continue
            if line.startswith("- Refused") or line.startswith("- Not done"):
                continue
            acts_total += 1
            if "(your fallback)" in line:
                fb_total += 1
                w = re.sub(r"[\d.]+", "N", line[2:].split(" (your fallback)")[0])
                w = " ".join(w.split()[:4])
                ran[w] += 1
    out[run] = {"date": load.RUNS[run], "example_in_system": f"{ex}/{len(sy)}", "plans": len(plans), "with_fallback": len(with_fb),
                "first_fallback_top": first.most_common(8), "any_fallback_top": anyfb.most_common(8),
                "by_model": {m: v for m, v in sorted(bymodel.items())},
                "evening_results_lines": acts_total, "of_which_fallback": fb_total, "fallback_results_top": ran.most_common(8)}
    o = out[run]
    print(f"\n== {run} ({o['date']}): example in system text {o['example_in_system']}; plans {o['plans']}, with fallback {o['with_fallback']}")
    print("  first fallback act:", o["first_fallback_top"])
    print("  by model [plans, with fb, fb names firewood]:", o["by_model"])
    print(f"  day results (evening lists): {acts_total} done, {fb_total} by the fallback ({fb_total / max(1, acts_total):.0%}):", o["fallback_results_top"][:6])
json.dump(out, open("survey_fallback.json", "w"), indent=1)
