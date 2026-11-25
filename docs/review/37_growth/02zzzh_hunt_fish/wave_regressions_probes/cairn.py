"""Build a cairn with no stone in hand or store (wave_regressions.md): what it costs at each commit."""
import contextlib, io
from cybertron2.engine.world import World, load_spec
from cybertron2.engine.here import Here, Mind
from cybertron2.engine import run as R, verbs as V
with contextlib.redirect_stdout(io.StringIO()):
    w = World(load_spec("cybertron2/specs/valley_s5.yaml"))
w.s["today"] = R.blank_today()
who = sorted(n for n, p in w.s["people"].items() if p.get("stage") == "adult")[0]
node = w.s["people"][who]["at"]
pid = next(pid for pid, p in w.s["parcels"].items() if p["node"] == node and p["cover"] in ("meadow", "pasture", "built ground", "field"))
stone = sum(float(c["goods"].get("stone", 0)) for c in w.s["containers"].values() if c.get("node", node) == node)
print("stone at the node:", stone, "| in hand:", w.goods(w.hands(who)).get("stone", 0))
with contextlib.redirect_stdout(io.StringIO()):
    r = [V.do(Here(w, who), Mind(w, who), {"do": "build", "what": "cairn", "at": w.s["parcels"][pid]["name"]}) for _ in range(3)]
for x in r:
    print(" ", x[:220])
cairns = {b: (x.get("unfinished"), x.get("monument")) for b, x in w.s["buildings"].items() if "cairn" in str(x.get("monument") or x.get("kind") or x.get("name", "")).lower()}
print("cairns after three acts:", cairns)
