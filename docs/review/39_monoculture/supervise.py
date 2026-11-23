"""Keep one World 0 arm going to its last day (W-106): while its engine process is alive, wait; when it has stopped short of the
world's days (the weekly stop, or a day abandoned when the five-hour window ran out), wait until both usage windows have room, then
`resume --from-last`; when it has finished, publish it (D2-332). Stops for good when the weekly window passes STOP_WEEK.

    python3 docs/review/39_monoculture/supervise.py /home/user/mono1/w0_haiku55 [--workers 6]

Everything it does is a line in /home/user/mono1/log.txt.
"""
import json
import os
import subprocess
import sys
import time

REPO = "/home/user/Cybertron2"
LOG = "/home/user/mono1/log.txt"
STOP_WEEK = 0.9          # leave a tenth of the week for the other sessions
RESUME_FIVE = 0.6        # resume only when the five-hour window is below this
POLL = 600               # seconds between checks while waiting


def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " supervise " + msg + "\n")


def alive(out):
    p = subprocess.run(["pgrep", "-f", f"cybertron2.engine (run|resume) .*{os.path.basename(out)}"], capture_output=True, text=True)
    return bool(p.stdout.strip())


def days_done(out):
    try:
        return sum(1 for _ in open(os.path.join(out, "days.jsonl")))
    except OSError:
        return 0


def days_wanted(out):
    try:
        return int((json.load(open(os.path.join(out, "run.json"))).get("spec") or {}).get("days") or 0) or 200
    except (OSError, ValueError):
        return 200


def windows():
    env = dict(os.environ, LLM_BACKEND="claude_code")
    code = ("from cybertron2.infra import llm;"
            "llm._claude_code('claude-haiku-5-5','JSON only.','Say hi.',{'type':'object','properties':{'s':{'type':'string'}},"
            "'required':['s']},None);import json;print(json.dumps(llm.USAGE.get('windows') or {}))")
    try:
        p = subprocess.run([sys.executable, "-c", code], cwd=REPO, env=env, capture_output=True, text=True, timeout=180)
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception as e:  # noqa: BLE001
        log(f"usage read failed: {e}")
        return {}


def main():
    out = sys.argv[1]
    workers = sys.argv[sys.argv.index("--workers") + 1] if "--workers" in sys.argv else "6"
    name = os.path.basename(out)
    log(f"{name}: watching")
    while True:
        if alive(out):
            time.sleep(60)
            continue
        done, want = days_done(out), days_wanted(out)
        if done >= want:
            log(f"{name}: finished ({done} days); publishing")
            subprocess.run([sys.executable, "-m", "cybertron2.engine", "publish", out, "--push", "--staging",
                            f"/home/user/mono1/staging_{name}"], cwd=REPO, env=dict(os.environ, HF_HUB_DISABLE_XET="1"),
                           stdout=open(out + ".log", "a"), stderr=subprocess.STDOUT)
            log(f"{name}: published")
            return
        w = windows()
        week, five = w.get("seven_day", 0.0), w.get("five_hour", 0.0)
        if week >= STOP_WEEK:
            log(f"{name}: stopped at day {done}: the weekly window is {week:.0%} used; not resuming")
            return
        if five >= RESUME_FIVE:
            log(f"{name}: at day {done}, waiting: five-hour window {five:.0%}, week {week:.0%}")
            time.sleep(POLL)
            continue
        log(f"{name}: resuming from day {done} (five-hour {five:.0%}, week {week:.0%})")
        env = dict(os.environ, LLM_BACKEND="claude_code", CYBERTRON2_WEEK_STOP=str(STOP_WEEK), HF_HUB_DISABLE_XET="1")
        subprocess.Popen([sys.executable, "-m", "cybertron2.engine", "resume", out, "--from-last", "--workers", workers], cwd=REPO,
                         env=env, stdout=open(out + ".log", "a"), stderr=subprocess.STDOUT, start_new_session=True)
        time.sleep(120)


if __name__ == "__main__":
    main()
