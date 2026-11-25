"""Run many arms in step (W-204; Zach, 25 Nov: "do all models running at same time so however far they get from the usage they all get
comparatively far ... it's fine to use all of the usage"): every arm runs to day STEP, waits for the rest, then all go on to 2 x STEP,
and so on to the world's days. An arm that dies out stops there and is published; an arm that reaches its last day is published.
A day lost to a usage limit is resumed when the five-hour window has room; the weekly stop is lifted (WEEK_STOP).

    python3 docs/review/39_monoculture/lockstep.py m1_haiku55=cybertron2/specs/mono/mono_m1_haiku55.yaml ... [--step 10] [--workers 6]

Each arm's output is /home/user/mono1/<name>; every start, resume, wait, step and publish is a line in /home/user/mono1/log.txt.
"""
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import supervise as S  # noqa: E402

ROOT = "/home/user/mono1"
WEEK_STOP = "0.995"       # all of the usage (Zach); the engine still stops cleanly before a day at this level
RESUME_FIVE = 0.9         # launch or resume when the five-hour window is below this
POLL = 120


def log(msg):
    with open(S.LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " lockstep " + msg + "\n")


def env():
    return dict(os.environ, LLM_BACKEND="claude_code", CYBERTRON2_WEEK_STOP=WEEK_STOP, HF_HUB_DISABLE_XET="1")


def publish(name, out):
    subprocess.run([sys.executable, "-m", "cybertron2.engine", "publish", out, "--push", "--staging", f"{ROOT}/staging_{name}"],
                   cwd=S.REPO, env=env(), stdout=open(out + ".log", "a"), stderr=subprocess.STDOUT)
    log(f"{name}: published at day {S.days_done(out)}")


def launch(name, world, out, target, workers):
    until = ["--until", f"d{target - 1}.memory"]
    if not os.path.exists(os.path.join(out, "run.json")):
        cmd = [sys.executable, "-m", "cybertron2.engine", "run", world, "--days", "200", "--out", out, "--workers", workers] + until
        what = "start"
    else:
        cmd = [sys.executable, "-m", "cybertron2.engine", "resume", out, "--from-last", "--workers", workers] + until
        what = "resume"
    subprocess.Popen(cmd, cwd=S.REPO, env=env(), stdout=open(out + ".log", "a"), stderr=subprocess.STDOUT, start_new_session=True)
    log(f"{name}: {what} from day {S.days_done(out)} to day {target}")


def main(argv):
    step = int(argv[argv.index("--step") + 1]) if "--step" in argv else 10
    workers = argv[argv.index("--workers") + 1] if "--workers" in argv else "6"
    arms = dict(a.split("=", 1) for a in argv if "=" in a and not a.startswith("--"))
    outs = {n: os.path.join(ROOT, n) for n in arms}
    ended = set()
    tries = {}                                                          # (arm, day) launches that did not move it on
    log(f"watching {len(arms)} arms, step {step}: {', '.join(sorted(arms))}")
    target = step
    while True:
        for n, out in outs.items():                                     # the ended: died out, or at their last day
            if n in ended or S.alive(out):
                continue
            if S.days_done(out) and (S.extinct(out) or S.days_done(out) >= S.days_wanted(out)):
                ended.add(n)
                log(f"{n}: ended at day {S.days_done(out)} ({'died out' if S.extinct(out) else 'its last day'})")
                publish(n, out)
        live = [n for n in arms if n not in ended]
        if not live:
            log("every arm ended")
            return
        if all(S.days_done(outs[n]) >= target and not S.alive(outs[n]) for n in live):
            log(f"step: every live arm at day {target} or past it ({', '.join(f'{n} {S.days_done(outs[n])}' for n in sorted(live))})")
            target = min(target + step, 200)
            continue
        idle = [n for n in live if not S.alive(outs[n]) and S.days_done(outs[n]) < target]
        if idle:
            w = S.windows()
            if not w:
                log(f"waiting: the usage check failed (a limit, most likely); idle {', '.join(sorted(idle))}")
            elif w.get("five_hour", 0.0) >= RESUME_FIVE:
                log(f"waiting: five-hour {w.get('five_hour', 0):.0%}, week {w.get('seven_day', 0):.0%}; idle {', '.join(sorted(idle))}")
            else:
                for n in idle:
                    k = (n, S.days_done(outs[n]))
                    tries[k] = tries.get(k, 0) + 1
                    if tries[k] > 6:                                    # six launches from one day and no day more: a fault,
                        ended.add(n)                                    # not the usage; set aside so the rest go on
                        log(f"{n}: STUCK at day {k[1]} after 6 launches; set aside (see {outs[n]}.log)")
                        publish(n, outs[n])
                        continue
                    launch(n, arms[n], outs[n], target, workers)
                time.sleep(180)
                continue
        time.sleep(POLL if not idle else 600)


if __name__ == "__main__":
    main(sys.argv[1:])
