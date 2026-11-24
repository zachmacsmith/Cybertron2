"""Eelmouth (view: beliefs) at main: does a fisher with broken traps see "Of your gear" in the morning? (wave_regressions.md)"""
import contextlib, io
from cybertron2.engine.world import World, load_spec
from cybertron2.engine.here import Here, Mind
from cybertron2.engine import view as VW, prompt as PR, run as R, gear as GE
with contextlib.redirect_stdout(io.StringIO()):
    w = World(load_spec("cybertron2/specs/nutrition/eelmouth.yaml"))
w.s["today"] = R.blank_today()
c = w.s["containers"][w.hands("Peter")]
for _ in range(400):                                    # wear two pieces down to broken
    GE.wear(w, c, "wicker trap", 1.0)
    if "broken" in " ".join(Here(w, "Peter").gear_words()):
        break
print("gear_words:", Here(w, "Peter").gear_words())
print("prompt.turn_prompt (no beliefs view) shows it:", "Of your gear" in PR.turn_prompt(Here(w, "Peter"), Mind(w, "Peter")))
for op in (True, False):
    print(f"view.turn opening={op} (what Eelmouth's people get) shows it:", "Of your gear" in VW.turn(Here(w, "Peter"), Mind(w, "Peter"), opening=op))
