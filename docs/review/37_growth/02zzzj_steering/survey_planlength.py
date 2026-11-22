"""Survey 4: in the river run, mornings with at least 4 units: the units given and the work acts the plan names (sleep, set,
host, give, move, take, try, partner and accept left out), by model."""
import collections, re, statistics as st
import load

run = "water_runs_models_r1"
d = collections.defaultdict(list)
for x in load.rows(run):
    if x["kind"] != "decision":
        continue
    m = load.blob(run, x["message_sha"]) or ""
    u = re.findall(r"You have (\d+) units of work today", m)
    if not u or int(u[0]) < 4:
        continue
    A = [a for a in x["reply"].get("actions") or [] if isinstance(a, dict)
         and a.get("do") not in ("sleep", "set", "host", "give", "move", "take", "try", "partner", "accept")]
    d[x["model"]].append((int(u[0]), len(A)))
for mm, v in sorted(d.items()):
    print(mm, len(v), "units", round(st.mean(a for a, b in v), 1), "work acts planned", round(st.mean(b for a, b in v), 1))
