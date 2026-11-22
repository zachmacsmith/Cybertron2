"""Render, with the code as it is now, the runs world's (specs/nutrition/runs_high.yaml: view beliefs, evening) system prompt and
day-0 morning message for one acting person, the way run.py builds them (view.turn, the tags pass). Read only: nothing is run."""
import sys
sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.engine.world import World, load_spec
from cybertron2.engine.here import Here, Mind
from cybertron2.engine import prompt as PR, view as VW, tags as TG
spec = load_spec(sys.argv[1] if len(sys.argv) > 1 else "/home/user/cybertron2/cybertron2/specs/nutrition/runs_high.yaml")
w = World(spec)
names = list(w.agents_acting())
n = sys.argv[2] if len(sys.argv) > 2 else names[0]
print("AGENTS", names, file=sys.stderr)
s = PR.system_prompt(Here(w, n), Mind(w, n))
try:
    m = VW.turn(Here(w, n), Mind(w, n), True)
    m = TG.render(w, n, m)
except Exception as e:
    m = f"(morning not rendered here: {e!r})"
print("=== SYSTEM ===\n" + s + "\n\n=== MORNING ===\n" + m)
