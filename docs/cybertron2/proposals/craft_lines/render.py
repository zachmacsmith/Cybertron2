"""craft_lines.json as a page to read (W-205): every shown craft by shape, its lines by level; the ways and other unshown rows listed.

    python3 docs/cybertron2/proposals/craft_lines/render.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..")))
from cybertron2.engine import shapes as SH  # noqa: E402
from cybertron2.engine.data import TECHNIQUES  # noqa: E402

L = json.load(open(os.path.join(HERE, "craft_lines.json")))
by = {}
for k, v in L.items():
    by.setdefault(SH.shape_of(k) if v.get("shown", True) else None, []).append(k)
out = ["# The craft lines, by familiarity (W-205, draft for Zach)", "",
       "Generated from craft_lines.json by render.py. **does** is what doing it does (new where marked); the four levels are what a person "
       "at that familiarity is told beyond the generated recipe (inputs, units, odds and life are not repeated). Aware goes beyond "
       "D2-352, which shows the name only. Each claim's grounding in the code is in the JSON (`grounded_in`).", ""]
for sh in [s for s in SH.SHAPES if s in by]:
    out += [f"## {sh} ({len(by[sh])})", ""]
    for k in sorted(by[sh]):
        v = L[k]
        old = TECHNIQUES[k].get("does")
        out.append(f"### {k}")
        out.append(f"- **does**{' (new)' if v.get('does_is_new') else ''}: {v['does']}" +
                   (f"  \n  *was:* {old}" if old and v.get("does_is_new") else ""))
        for f in ("aware", "rough", "capable", "known"):
            out.append(f"- **{f}**: {v[f]}")
        out.append("")
rest = sorted(by.get(None, []))
out += [f"## Not shown as crafts ({len(rest)})", "", "Ways under other crafts, or rows with no shape: " + ", ".join(rest) + ".", ""]
open(os.path.join(HERE, "craft_lines.md"), "w").write("\n".join(out))
print(len(L), "rows;", sum(len(v) for s, v in by.items() if s), "shown")
