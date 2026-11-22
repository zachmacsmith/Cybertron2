"""Replay a recorded call from a run's journal on the model that played it, with text swaps, through the repo's own model code
(cybertron2.infra.llm, the claude_code backend, as the runs use), keeping every result at once in this folder's jsonl files.

A point is a request key. Its system text and schema are the recorded ones. Its message is the recorded message; for a call that
continued a conversation (idx > 0), the conversation before it is rebuilt from the journal (each earlier message and the reply the
model gave) and flattened the way the engine does when a session cannot be resumed (llm.flatten), so the model sees what it saw.
The weekly window is read from every call's rate-limit event; the probe stops when it reaches STOP."""
import json, sys, time
import pandas as pd
sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.infra import llm
import load

STOP = 0.90


def weekly():
    return (llm.USAGE.get("windows") or {}).get("seven_day")


def raw_reply(run, key):
    r = pd.read_parquet(f"{load.path(run)}/responses.parquet", columns=["key", "attempts", "parsed"])
    r = r[r.key == key]
    if r.empty:
        return None
    try:
        at = json.loads(r.iloc[0].attempts)
        ok = [a for a in at if a.get("ok") and a.get("raw")]
        if ok:
            return ok[-1]["raw"]
    except Exception:
        pass
    return r.iloc[0].parsed


def point(run, key):
    rows = {x["key"]: x for x in load.rows(run)}
    x = rows[key]
    system, schema = load.blob(run, x["system_sha"]), json.loads(load.blob(run, x["schema_sha"]))
    msg = load.blob(run, x["message_sha"])
    if x["idx"] and x["idx"] > 0:
        conv = sorted((y for y in rows.values() if y["conversation"] == x["conversation"] and y["idx"] < x["idx"]), key=lambda y: y["idx"])
        texts = []
        for y in conv:
            texts += [load.blob(y["run"], y["message_sha"]), raw_reply(run, y["key"]) or json.dumps(y["reply"])]
        msg = llm.flatten(texts + [msg])
    return {"system": system, "message": msg, "schema": schema, "model": x["model"], "agent": x["agent"], "day": x["day"], "kind": x["kind"]}


def swap(text, swaps):
    n = 0
    for old, new in swaps:
        if old in text:
            text, n = text.replace(old, new), n + 1
    return text, n


def run_calls(jobs, out_path):
    """jobs: [(tag dict, system, message, schema, model)]; skips tags already in out_path; appends each result at once."""
    done = set()
    try:
        for l in open(out_path):
            d = json.loads(l)
            done.add((d["key"], d["variant"], d.get("step")))
    except FileNotFoundError:
        pass
    n = 0
    for tag, system, message, schema, model in jobs:
        if (tag["key"], tag["variant"], tag.get("step")) in done:
            continue
        t0 = time.time()
        try:
            out, reasoning, usage = llm.call("claude_code", model, system, message, schema)
        except Exception as e:
            print("call failed", tag, str(e)[:200])
            continue
        n += 1
        w = weekly()
        rec = {**tag, "model": model, "out": out, "usage": usage, "weekly": w, "five_hour": (llm.USAGE.get("windows") or {}).get("five_hour"),
               "s": round(time.time() - t0, 1)}
        with open(out_path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(tag["key"], tag["variant"], model, "weekly", w, "5h", rec["five_hour"], "usd", (usage or {}).get("cc_equiv_usd"), flush=True)
        if w is not None and w >= STOP:
            print("STOP: weekly window at", w)
            return n, True
    return n, False
