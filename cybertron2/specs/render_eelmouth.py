"""Live run 1's renders, without model calls (stage 4 brief §4): each founder's system prompt and first morning message, for both live
arms of Eelmouth remade (`nutrition/eelmouth.yaml`, the core prompt; `nutrition/eelmouth_old.yaml`, today's prompt, D2-331), written
as they would be sent on day 0 (the world built, its dawn read, tags rendered: run.py's own steps), with their sizes in words.

    python3 cybertron2/specs/render_eelmouth.py [--out DIR]
"""
from __future__ import annotations

import contextlib
import io
import os
import sys

ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "docs", "review", "37_growth", "02zzzh_hunt_fish", "live1_renders")
ARMS = {"main": "eelmouth.yaml", "old": "eelmouth_old.yaml"}


def render(spec_path) -> dict:
    from cybertron2.engine import perceive as PC, prompt as PR, run as R, tags as TG, view as VW
    from cybertron2.engine.here import Here, Mind
    from cybertron2.engine.world import World, load_spec
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec(spec_path))
    w.s["day"] = 0
    w.s["events"] = []
    w.s["today"] = R.blank_today()
    R.dawn(w)
    PC.dawn(w)
    turn = VW.turn if VW.on(w) else PR.turn_prompt
    out = {}
    for n in w.agents_acting():
        out[n] = {"model": w.s["people"][n].get("model"), "system": PR.system_prompt(Here(w, n), Mind(w, n)),
                  "morning": TG.render(w, n, turn(Here(w, n), Mind(w, n), opening=True))}
    return out


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else OUT
    os.makedirs(out, exist_ok=True)
    rows = []
    for arm, f in ARMS.items():
        got = render(os.path.join(os.path.dirname(__file__), "nutrition", f))
        for n, r in sorted(got.items()):
            path = os.path.join(out, f"{arm}_{n}.md")
            with open(path, "w") as h:
                h.write(f"# {n}, the {arm} arm ({f}), day 0, model {r['model']}\n\n## System prompt\n\n```\n{r['system']}\n```\n\n"
                        f"## First morning message\n\n```\n{r['morning']}\n```\n")
            rows.append((arm, n, r["model"], len(r["system"].split()), len(r["morning"].split())))
    with open(os.path.join(out, "README.md"), "w") as h:
        h.write("# Live run 1's renders (day 0, no model calls)\n\nMade by `cybertron2/specs/render_eelmouth.py` for 37.2 to read before "
                "launching live run 1 (stage 4, W-100). One file per founder who acts on day 0, per arm: `main_<name>.md` (the core "
                "prompt, the shapes, the seeded lines) and `old_<name>.md` (today's prompt and verb list, no new seeded lines: D2-331).\n\n"
                "| Arm | Person | Model | System prompt (words) | First morning (words) |\n|---|---|---|---|---|\n")
        for arm, n, m, s, t in rows:
            h.write(f"| {arm} | {n} | {m} | {s} | {t} |\n")
    print("\n".join(f"{a:5} {n:10} {m:20} system {s:5} morning {t:5}" for a, n, m, s, t in rows))


if __name__ == "__main__":
    main()
