"""Read the wording probe: per variant, how far ahead the 'why' and the talk look, and what the plan holds."""
import json, re, collections, statistics as st

P = "/tmp/claude-0/-home-user/4e92ceac-fc9e-588a-9b11-e1338cfe1c52/scratchpad/wording_probe.jsonl"
FUT = re.compile(r"\b(tomorrow|days?|weeks?|season|winter|spring|autumn|harvest|before|until|soon|later|next|future|line|"
                 r"children|generations?|years?|store up|lay by|keep for|plan|prepare|build|clear|field|seed|stock)\b", re.I)
HORIZON = re.compile(r"\b(winter|spring|autumn|season|weeks?|year|generations?|before the|by day \d+|in \d+ days|next \w+ days)\b", re.I)
INVEST = {"build", "make", "claim", "teach", "learn", "offer", "partner", "travel", "found", "admit", "join"}
WORK_INVEST = re.compile(r"clear|plough|sow|fence|manure|select seed|repair|build", re.I)

rows = [json.loads(l) for l in open(P)]
by = collections.defaultdict(list)
for r in rows:
    o = r["out"] or {}
    why = str(o.get("why") or "")
    talk = " ".join(str(x.get("text", "")) for k in ("tell", "say") for x in (o.get(k) or []) if isinstance(x, dict))
    acts = o.get("actions") or []
    inv = sum(1 for a in acts if isinstance(a, dict) and (a.get("do") in INVEST or WORK_INVEST.search(str(a.get("what", "")))))
    by[(r["kind"], r["variant"])].append({
        "why_words": len(why.split()), "why_future": len(FUT.findall(why)), "why_horizon": len(HORIZON.findall(why)),
        "talk_horizon": len(HORIZON.findall(talk)), "acts": len(acts), "invest_acts": inv,
        "notes": len(o.get("note") or []), "key": r["key"], "why": why})
for (kind, v), xs in sorted(by.items()):
    m = lambda k: round(st.mean(x[k] for x in xs), 2)
    print(f"{kind:9} {v:3} n={len(xs):2}  why words {m('why_words'):5}  future words {m('why_future'):4}  long-horizon words "
          f"{m('why_horizon'):4} (talk {m('talk_horizon'):4})  acts {m('acts'):4}  investing acts {m('invest_acts'):4}  notes {m('notes')}")
