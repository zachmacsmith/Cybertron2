"""Review 38.68: does anyone weigh another's record? Scans each turn's private reasoning ('why', and the talk waves' 'why') and what
was said, for references to a named other's past keeping or breaking of terms. Writes reputation.jsonl; prints counts."""
import glob, json, os, re, sys, collections
RX = re.compile(r"(kept (his|her|their) (word|promise|bargain)|has(n't| not) (paid|delivered|come through|done the work|worked)|"
                r"(never|didn't|did not) (paid|pay|deliver|come|show)|still owes?|owes? (us|me) (still|from)|"
                r"can(not|'t) be trusted|not to be trusted|don't trust|do not trust|trust (him|her|them)|"
                r"last time|went back on|broke (his|her|their) (word|promise)|good for (it|his word|her word)|"
                r"paid (us|me) before|has paid before|proved (honest|reliable)|reliable|unreliable|in arrears|defaulted)", re.I)
out, n_turn = [], 0
c = collections.Counter()
for d in sys.argv[1:]:
    for f in sorted(glob.glob(os.path.join(d, "*/turns.jsonl"))):
        run = f.split("/")[-2]
        for l in open(f):
            try:
                r = json.loads(l)
            except Exception:
                continue
            n_turn += 1
            reps = [r.get("reply")] + [t.get("reply") for t in (r.get("talk") or []) if isinstance(t, dict)]
            for rep in reps:
                if not isinstance(rep, dict):
                    continue
                texts = [("why", str(rep.get("why") or ""))] + [(k, str(t.get("text"))) for k in ("tell", "say") for t in (rep.get(k) or []) if isinstance(t, dict)]
                for src, t in texts:
                    m = RX.search(t)
                    if m:
                        out.append({"run": run, "day": r.get("day"), "by": r.get("agent"), "model": r.get("model"), "src": src, "hit": m.group(0), "text": t[:500]})
                        c[m.group(0).lower()] += 1
with open("reputation.jsonl", "w") as f:
    for o in out:
        f.write(json.dumps(o) + "\n")
print(n_turn, "turns;", len(out), "hits;", len({(o['run'], o['by']) for o in out}), "people")
print(c.most_common(25))
