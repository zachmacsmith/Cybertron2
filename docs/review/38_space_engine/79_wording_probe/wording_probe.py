"""Wording probe (Zach, 17 Nov): replay real decision points from runs/water_runs_models_r1 with the day-framed wording made neutral,
and see whether plans and talk look further ahead. Cheap: Haiku 5.5 only; stops if the weekly window reaches 98.5%.

Variants per point: A (the words as run), A2 (the same again: the noise between two draws), B (neutral wording).
"""
import json, sqlite3, sys, time, zlib
sys.path.insert(0, "/home/user/c2-runs")
from cybertron2.infra import llm

RUN = "/home/user/cybertron2/runs/water_runs_models_r1"
OUT = "/tmp/claude-0/-home-user/4e92ceac-fc9e-588a-9b11-e1338cfe1c52/scratchpad/wording_probe.jsonl"
STOP = 0.99                                                   # the reading is in whole percents: stop on reaching 99%

SYS_SWAPS = [('"why": a sentence or two on what you mean to do today and why.',
              '"why": what you make of things and what you mean to do, today and further ahead, and why.')]
MSG_SWAPS = [("Plan your day. Reply with JSON only.", "Decide what to do. Reply with JSON only."),
             ('"why": what you make of the day and what you mean to do tomorrow.',
              '"why": what you make of things and what you mean to do, tomorrow and further ahead.')]

c = sqlite3.connect(f"file:{RUN}/run.db?mode=ro", uri=True)


def blob(sha):
    return zlib.decompress(c.execute("select z from blobs where sha=?", (sha,)).fetchone()[0]).decode()


turns = [json.loads(l) for l in open(f"{RUN}/turns.jsonl")]


def point(key, agent, day, kind):
    s_sha, m_sha, sc_sha = c.execute("select system_sha, message_sha, schema_sha from requests where key=?", (key,)).fetchone()
    system, schema = blob(s_sha), json.loads(blob(sc_sha))
    if kind == "decision":                                          # the full day prompt as the turn recorded it
        msg = next(t["prompt"] for t in turns if t["agent"] == agent and t["day"] == day)
    else:
        msg = blob(m_sha)
    return system, msg, schema


# each point replayed on the model that played it (Zach: "you have to use the actual model that was in that run"); cheapest first, so
# the weekly guard stops the dearest ones if it must. Day 1 (file day 0): the full opening prompt, with no conversation behind it.
AGENTS = ["Henry", "Jocelin", "Fulk", "Osric", "Warin", "Aldric", "Lambert"]
POINTS = [(f"d0.decide.{a}.1", a, 0, "decision") for a in AGENTS]


def swap(text, swaps):
    n = 0
    for old, new in swaps:
        if old in text:
            text, n = text.replace(old, new), n + 1
    return text, n


def weekly():
    return (llm.USAGE.get("windows") or {}).get("seven_day")


done = set()
try:
    for l in open(OUT):
        x = json.loads(l)
        done.add((x["key"], x["variant"]))
except FileNotFoundError:
    pass

for key, agent, day, kind in POINTS:
    try:
        system, msg, schema = point(key, agent, day, kind)
    except Exception as e:
        print("skip", key, e)
        continue
    for variant in ("A", "A2", "B"):
        if (key, variant) in done:
            continue
        s, m = system, msg
        if variant == "B":
            s, n1 = swap(system, SYS_SWAPS)
            m, n2 = swap(msg, MSG_SWAPS)
            if n1 + n2 == 0:
                print("no swap in", key)
        t0 = time.time()
        try:
            model = c.execute("select responder from requests where key=?", (key,)).fetchone()[0].split(":", 1)[1]
            out, reasoning, usage = llm.call("claude_code", model, s, m, schema)
        except Exception as e:
            print("call failed", key, variant, str(e)[:200])
            continue
        w = weekly()
        rec = {"key": key, "agent": agent, "day": day, "kind": kind, "variant": variant, "model": model, "out": out, "usage": usage,
               "weekly": w, "s": round(time.time() - t0, 1)}
        with open(OUT, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(key, variant, "weekly", w, "cost", (usage or {}).get("cost_usd"))
        if w is not None and w >= STOP:
            print("STOP: weekly window at", w)
            sys.exit(0)
