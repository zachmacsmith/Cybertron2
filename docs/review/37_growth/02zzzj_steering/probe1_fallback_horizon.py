"""Probe 1 (W-84): real stretch-opening morning prompts from runs/water_runs_models_r1 (20 Nov; `view: beliefs`, `evening: true`;
the reply format's wording unchanged in the code since, checked by git log on prompt.py, view.py, evening.py), each replayed on
the model that played it, five ways:
- A:  as run.
- A2: as run, a second draw (the noise between two draws).
- B:  the fallback's example removed: "(say, gather firewood)" dropped from the reply format; nothing else changed.
- C:  no fallback at all: the reply line and the schema's `fallback` removed (what a person does with the whole day when there is
      no filler slot; the units still "wasted" if unused).
- H:  neutral horizon (38.79's B): the why line "what you make of things and what you mean to do, today and further ahead, and why";
      the closing "Plan your day." as "Decide what to do.".
- N:  no horizon named (added after the first five): the why line with "today" dropped ("a sentence or two on what you mean to do
      and why"), the closing as in H.
Points: stretch openings (a new conversation: the message is self-contained) on days 16 to 22, chosen by model with a fixed seed among
mornings whose house line shows at least 20 nights of fuel and with at least 4 units, regardless of what the recorded reply did."""
import json, random, re, copy, sys
import load, probe_lib as P

RUN = "water_runs_models_r1"
OUT = "probe1.jsonl"
FB_OLD = ' (say, gather firewood): done in'
FB_LINE = re.compile(r'- "fallback": \[actions\].*?none of them can be done\.\n', re.S)
SYS_H = [('"why": a sentence or two on what you mean to do today and why.',
          '"why": what you make of things and what you mean to do, today and further ahead, and why.')]
SYS_N = [('"why": a sentence or two on what you mean to do today and why.', '"why": a sentence or two on what you mean to do and why.')]
MSG_H = [("Plan your day. Reply with JSON only.", "Decide what to do. Reply with JSON only.")]
PICK = {"claude-opus-5-5": 2, "claude-sonnet-5-5": 2, "claude-haiku-5-5": 2, "claude-opus-5": 1, "claude-opus-4-5": 1,
        "claude-sonnet-5": 1, "claude-sonnet-4-5": 1, "claude-haiku-4-5": 1, "claude-fable-5-2": 1}


def points():
    rng = random.Random(84)
    by = {}
    for x in load.rows(RUN):
        if x["kind"] != "decision" or x["idx"] != 0 or not (16 <= (x["day"] or 0) <= 22):
            continue
        m = load.blob(RUN, x["message_sha"]) or ""
        f = re.findall(r"fuel for about (\d+) such nights", m)
        u = re.findall(r"You have (\d+) units of work today", m)
        if f and int(f[0]) >= 20 and u and int(u[0]) >= 4:                # a day with units to fill
            by.setdefault(x["model"], []).append(x)
    out = []
    for model, k in PICK.items():
        xs = sorted(by.get(model, []), key=lambda x: x["key"])
        seen = set()
        rng.shuffle(xs)
        for x in xs:
            if x["agent"] in seen:
                continue
            seen.add(x["agent"])
            out.append(x)
            if len([o for o in out if o["model"] == model]) >= k:
                break
    return out


def variant(p, v):
    s, m, sc = p["system"], p["message"], p["schema"]
    if v == "B":
        assert FB_OLD in s
        s = s.replace(FB_OLD, ": done in")
    elif v == "C":
        assert FB_LINE.search(s)
        s = FB_LINE.sub("", s)
        sc = copy.deepcopy(sc)
        sc["properties"].pop("fallback", None)
    elif v == "N":                                            # no horizon named: "today" dropped, the closing as in H
        s, n1 = P.swap(s, SYS_N)
        m, n2 = P.swap(m, MSG_H)
        assert n1 and n2
    elif v == "H":
        s, n1 = P.swap(s, SYS_H)
        m, n2 = P.swap(m, MSG_H)
        assert n1 and n2
    return s, m, sc


if __name__ == "__main__":
    pts = points()
    print([(x["key"], x["model"]) for x in pts])
    if "--list" in sys.argv:
        sys.exit(0)
    jobs = []
    vs = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--variants=")), ["A", "B", "C", "H", "A2"])
    for v in vs:                                              # by variant, so a stop leaves every point's A and B first
        for x in pts:
            p = P.point(RUN, x["key"])
            s, m, sc = variant(p, v)
            jobs.append(({"key": x["key"], "variant": v, "agent": x["agent"], "day": x["day"], "run": RUN}, s, m, sc, x["model"]))
    n, stopped = P.run_calls(jobs, OUT)
    print("calls", n, "stopped", stopped)
