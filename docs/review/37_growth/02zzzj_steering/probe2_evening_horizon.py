"""Probe 2 (W-84): does the evening's day-framed "why" carry into the next morning's plan? Real evenings from
runs/water_runs_models_r1 (20 Nov; wording unchanged in the code since) in the middle of a stretch, so the next morning's plan is
asked in the same conversation; each replayed on the model that played it, in two calls: the evening, then the next morning with
the conversation rebuilt from the journal up to the evening, the evening's new reply, then the recorded next-morning message.
- A:  as run (both calls).
- A2: as run, a second draw.
- N:  no horizon named, the smallest change: the system why line "a sentence or two on what you mean to do and why" (today
      dropped), the evening's "what you make of the day and what you mean to do" (tomorrow dropped), the morning's closing
      "Decide what to do." for "Plan your day.".
Measured on the morning: the why's horizon words, the acts, investing acts, notes; on the evening: the same of its why."""
import json, random, sys
import load, probe_lib as P
from cybertron2.infra import llm

RUN = "water_runs_models_r1"
OUT = "probe2.jsonl"
SYS_N = [('"why": a sentence or two on what you mean to do today and why.', '"why": a sentence or two on what you mean to do and why.')]
EVE_N = [('"why": what you make of the day and what you mean to do tomorrow.', '"why": what you make of the day and what you mean to do.')]
MOR_N = [("Plan your day. Reply with JSON only.", "Decide what to do. Reply with JSON only.")]
PICK = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5", "claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-4-5"]


def points():
    rng = random.Random(842)
    rs = load.rows(RUN)
    conv = {}
    for x in rs:
        conv.setdefault(x["conversation"], []).append(x)
    cands = {}
    for c, xs in conv.items():
        xs = sorted(xs, key=lambda x: x["idx"])
        for i, x in enumerate(xs[:-1]):
            nxt = xs[i + 1]
            if x["kind"] == "evening" and nxt["kind"] == "decision" and 10 <= (x["day"] or 0) <= 25 \
                    and nxt["day"] == x["day"] + 1 \
                    and EVE_N[0][0] in (load.blob(RUN, x["message_sha"]) or ""):     # the evening's first word, with its why line
                m = load.blob(RUN, nxt["message_sha"]) or ""
                if "Plan your day." in m:
                    cands.setdefault(x["model"], []).append((x, nxt))
    out = []
    for model in PICK:
        xs = sorted(cands.get(model, []), key=lambda t: t[0]["key"])
        rng.shuffle(xs)
        if xs:
            out.append(xs[0])
    return out


def history(run, upto_idx, conversation):
    rows = sorted((y for y in load.rows(run) if y["conversation"] == conversation and y["idx"] < upto_idx), key=lambda y: y["idx"])
    texts = []
    for y in rows:
        texts += [load.blob(run, y["message_sha"]), P.raw_reply(run, y["key"]) or json.dumps(y["reply"])]
    return texts


if __name__ == "__main__":
    pts = points()
    print([(e["key"], d["key"], e["model"]) for e, d in pts])
    if "--list" in sys.argv:
        sys.exit(0)
    done = set()
    try:
        for l in open(OUT):
            r = json.loads(l)
            done.add((r["key"], r["variant"], r["step"]))
    except FileNotFoundError:
        pass
    calls = 0
    for v in next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--variants=")), ["A", "N", "A2"]):
        for e, d in pts:
            if (d["key"], v, "morning") in done:
                continue
            system = load.blob(RUN, e["system_sha"])
            sch_e = json.loads(load.blob(RUN, e["schema_sha"]))
            sch_d = json.loads(load.blob(RUN, d["schema_sha"]))
            hist = history(RUN, e["idx"], e["conversation"])
            em = load.blob(RUN, e["message_sha"])
            dm = load.blob(RUN, d["message_sha"])
            if v == "N":
                system, a = P.swap(system, SYS_N)
                em, b = P.swap(em, EVE_N)
                dm, c = P.swap(dm, MOR_N)
                assert a and b and c, (a, b, c)
            # the evening
            prior = [r for r in (json.loads(l) for l in open(OUT)) if r["key"] == d["key"] and r["variant"] == v and r["step"] == "evening"] \
                if (d["key"], v, "evening") in done else []
            if prior:
                ev = prior[0]["out"]
            else:
                n, stop = P.run_calls([({"key": d["key"], "variant": v, "step": "evening", "evening_key": e["key"], "agent": e["agent"],
                                         "day": e["day"], "run": RUN}, system, llm.flatten(hist + [em]), sch_e, e["model"])], OUT)
                calls += n
                if stop:
                    sys.exit(0)
                ev = [json.loads(l) for l in open(OUT)][-1]["out"]
            n, stop = P.run_calls([({"key": d["key"], "variant": v, "step": "morning", "evening_key": e["key"], "agent": d["agent"],
                                     "day": d["day"], "run": RUN}, system, llm.flatten(hist + [em, json.dumps(ev), dm]), sch_d, d["model"])], OUT)
            calls += n
            if stop:
                sys.exit(0)
    print("calls", calls)
