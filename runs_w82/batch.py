"""W-82: the bot batch. Each world x arm x seed is one engine run (bots only, no model calls), kept at once under
runs_w82/<world>/<arm>_s<seed>/ with its act log (C2_W82_ACTLOG) and measure.json.

Arms: null (no building layer, today's prices), today (the engine's prices), f40, f15, f7 (capital at real hours x 1/40, 1/15, 1/7;
cybertron2/engine/capital_clock.py).

    python3 runs_w82/batch.py [--worlds a,b] [--arms ...] [--seeds 1,2,3] [--days 64] [--jobs 6]
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W82 = os.path.join(ROOT, "runs_w82")
ARMS = {"null": None, "today": None, "f40": "1/40", "f15": "1/15", "f7": "1/7"}


def one(world, arm, seed, days, knobs=None, tag=""):
    out = os.path.join(W82, world, f"{arm}{tag}_s{seed}")
    if os.path.exists(os.path.join(out, "measure.json")):
        return out, "kept"
    os.makedirs(os.path.join(W82, world, "specs"), exist_ok=True)
    spec = yaml.safe_load(open(os.path.join(W82, "worlds", f"{world}.yaml")))
    spec["seed"] = int(spec.get("seed", 0)) * 100 + seed
    spec["days"] = days
    bl = dict(spec["bot_livelihood"])
    bl["build"] = arm != "null"
    spec["bot_livelihood"] = bl
    bl.update(knobs or {})
    spec["bot_livelihood"] = bl
    sp = os.path.join(W82, world, "specs", f"{arm}{tag}_s{seed}.yaml")
    yaml.safe_dump(spec, open(sp, "w"), sort_keys=False, width=140)
    if os.path.exists(out):
        subprocess.run(["rm", "-rf", out])
    os.makedirs(out)
    env = dict(os.environ, C2_W82_ACTLOG=os.path.join(out, "actlog.jsonl"))
    env.pop("C2_CAPITAL_FACTOR", None)
    if ARMS[arm]:
        env["C2_CAPITAL_FACTOR"] = ARMS[arm]
    with open(os.path.join(out, "arm.json"), "w") as f:
        json.dump({"world": world, "arm": arm, "seed": seed, "spec_seed": spec["seed"], "days": days,
                   "capital_factor": ARMS[arm], "build": arm != "null", "knobs": knobs or {}, "tag": tag}, f)
    log = open(os.path.join(out, "engine.log"), "w")
    r = subprocess.run([sys.executable, "-m", "cybertron2.engine", "run", sp, "--out", out, "--bots", "--days", str(days)],
                       cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        return out, f"failed ({r.returncode})"
    subprocess.run([sys.executable, os.path.join(W82, "measure.py"), out], cwd=ROOT, stdout=subprocess.DEVNULL)
    return out, "done"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", default="frontier_w82,brookend_w82,runs_w82")
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--seeds", default="1,2,3")
    ap.add_argument("--days", type=int, default=64)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--knob", action="append", default=[], help="KEY=NUMBER for the bot setting (a sensitivity arm)")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    jobs = [(w, arm, int(s)) for w in a.worlds.split(",") for arm in a.arms.split(",") for s in a.seeds.split(",")]
    with cf.ProcessPoolExecutor(a.jobs) as ex:
        knobs = {k: float(v) for k, v in (x.split("=", 1) for x in a.knob)}
        for out, st in (f.result() for f in [ex.submit(one, *j, a.days, knobs, a.tag) for j in jobs]):
            print(st, out, flush=True)
