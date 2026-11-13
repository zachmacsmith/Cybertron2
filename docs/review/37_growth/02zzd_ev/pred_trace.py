import sys, json, collections
"""A world run dry with bots; each night, the count of each whole-counted kind within reach of each node (brief 4c §7).
Usage: CYB_ROOT=<checkout> python3 pred_trace.py <world.yaml> <days> <out dir>"""
import os
sys.path.insert(0, os.environ["CYB_ROOT"])
from cybertron2.engine import run as R, wild as WD
import numpy as np
log = collections.defaultdict(dict)
orig_count = WD._count
def count(m, st, kind, land, node, ri, gather):
    c = orig_count(m, st, kind, land, node, ri, gather)
    if kind in ("wolf", "wild boar", "brown bear", "red deer", "roe deer"):
        log[kind + "@" + node][WD_day[0]] = round(c, 2)
    return c
WD._count = count
WD_day = [0]
orig_groups = WD._groups
def groups(w, m, st):
    WD_day[0] = w.d
    # the areas' hunger for wolves, if the state holds it
    return orig_groups(w, m, st)
WD._groups = groups
R.run(sys.argv[1], sys.argv[3], days=int(sys.argv[2]), bots=True)
json.dump(log, open(os.path.join(sys.argv[3], "pred_trace.json"), "w"))
for k in sorted(log):
    if k.startswith(("wolf", "wild boar", "brown bear")) or k.split("@")[1] in ("Ashford", "Brockley"):
        print(k, list(log[k].values()))
