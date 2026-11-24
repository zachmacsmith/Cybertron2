"""Survey C (W-110): every branch on a named thing in area C's function code (people and society).

The same walk as B_branches.py (string literals that are names of rows in the engine's registries, where they appear in function
code as a comparison, a tuple/list/set of names in a comparison or a call, a dict literal's key, a subscript or .get into a
registry by a literal, a default argument), with area C's registries added: livelihoods (ROWS, HOLDINGS), life stages, landmarks,
terrain, weather, wild kinds and runs, stores' spaces and containers, processes, structures, seasons. Module-level tables are not
counted (they are data). Each hit is tagged `wave` when `git blame` puts its line after the wave's baseline f728a3b7.

Run: python3 -I docs/review/37_growth/02zzzm_patterns/C_branches.py [--list]
"""
import ast
import collections
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, ROOT)
from cybertron2.engine import data as D                                         # noqa: E402
from cybertron2.engine import process as PROC, gear as GE, stores as SR        # noqa: E402
from cybertron2.engine import livelihoods as LV                                 # noqa: E402
from cybertron2.wild import kinds as WK                                         # noqa: E402

BASE = "f728a3b7"
REG = {}


def add(cat, names):
    for n in names:
        if isinstance(n, str):
            REG.setdefault(n.lower(), set()).add(cat)


add("item", D.ITEMS); add("technique", D.TECHNIQUES); add("fitting", D.FITTINGS); add("room", D.ROOMS)
add("blueprint", D.BLUEPRINTS); add("monument", D.MONUMENTS); add("cover", D.COVERS); add("resource", D.RESOURCES)
add("crop", D.CROPS); add("thing", [k for k in D.THINGS if isinstance(D.THINGS.get(k), dict)])
add("herd", ["cow", "cows", "ox", "oxen", "bull", "bulls", "calf", "calves", "heifer", "cattle"])
add("process", PROC.PROCESSES); add("structure", ["wattle", "timber", "stone", "camp"])
add("season", ["spring", "summer", "autumn", "winter"])
add("gear", getattr(GE, "LIVES", {})); add("space", SR.SPACES); add("container", SR.CONTAINERS)
add("livelihood", LV.ROWS); add("holding", LV.HOLDINGS)
add("specialism", [s for r in LV.ROWS.values() for s in r.get("specialisms", {})])
add("stage", ["infant", "child", "youth", "adult", "elder"])
add("landmark", D.LANDMARKS); add("terrain", D.TERRAIN); add("weather", D.WEATHER)
add("wild kind", WK.KINDS); add("run", WK.RUNS)
add("trade", ["mason", "carpenter", "smith", "farmer", "fisher"])

FILES = ["life", "learning", "knowledge", "memory", "founders", "livelihoods", "book", "agreements", "exchange", "settle", "parties",
         "roads", "here", "run", "evening", "journal", "bots_livelihood"]
REGNAMES = {"ITEMS", "TECHNIQUES", "FITTINGS", "ROOMS", "BLUEPRINTS", "MONUMENTS", "COVERS", "RESOURCES", "CROPS", "THINGS", "HERDS",
            "PROCESSES", "LIVES", "I", "T", "F", "STORES", "FENCES", "WATER_WORKS", "DECAY", "KEEP_DAYS", "_I", "ROWS", "HOLDINGS",
            "LANDMARKS", "TERRAIN", "RUNS", "KINDS", "NEAR_PEOPLE", "STORE_STOPS", "SPACES", "CONTAINERS", "CLASS_OF", "NB", "_BUSY",
            "LIFE", "sp", "ct"}
# a record's own field or a word of the grammar, not a row's name, where it is read with .get or is a dict key
FIELD_WORDS = {"herd", "pack", "for", "set", "fields", "mill", "oven", "forge", "weir", "stock", "salt", "beds", "hearth", "cut",
               "fence", "hay", "milk", "dung", "youth", "child", "infant", "elder", "adult", "winter", "spring", "summer", "autumn",
               "copper", "grain", "fish", "meat", "road", "camp", "pass", "spring"}
# words that are a record's kind or a grammar's word, never a row's name, wherever they appear (checked by hand on --list)
NOT_NAMES = {"set", "stock", "built", "meeting", "lead", "care", "fittings"}
NOT_HERE = {("run", "herd"), ("parties", "ox"), ("book", "young")}


def strs(node):
    out = []
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        out.append(node)
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        if not all(isinstance(e, ast.Constant) for e in node.elts):
            return out
        for e in node.elts:
            out += strs(e)
    return out


def blame_new(path):
    """{line number: True} for lines changed after the wave's baseline."""
    try:
        txt = subprocess.run(["git", "-C", ROOT, "blame", "-s", "--abbrev=40", f"{BASE}..HEAD", "--", path], capture_output=True,
                             text=True, check=True).stdout
    except Exception:                                                           # noqa: BLE001
        return {}
    out = {}
    for i, ln in enumerate(txt.splitlines(), 1):
        out[i] = not ln.startswith("^")                                         # ^sha: from the baseline or before
    return out


def scan(path):
    tree = ast.parse(open(path).read())
    hits, seen = [], set()
    for f in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))]:
        name = getattr(f, "name", "<lambda>")
        for n in ast.walk(f):
            cands = []
            if isinstance(n, ast.Compare):
                for x in [n.left] + n.comparators:
                    cands += [(s, "compare") for s in strs(x)]
            elif isinstance(n, ast.Dict):
                cands += [(k, "dict key") for k in n.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            elif isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id in REGNAMES:
                cands += [(s, "registry[" + n.value.id + "]") for s in strs(n.slice)]
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" and \
                    isinstance(n.func.value, ast.Name) and n.func.value.id in REGNAMES and n.args:
                cands += [(s, "registry.get") for s in strs(n.args[0])]
            elif isinstance(n, ast.Call):
                for x in list(n.args) + [k.value for k in n.keywords]:
                    if isinstance(x, (ast.Tuple, ast.List, ast.Set)):
                        cands += [(s, "call arg") for s in strs(x)]
                if isinstance(n.func, ast.Attribute) and n.func.attr == "get" and n.args and isinstance(n.args[0], ast.Constant):
                    cands += [(s, "x.get") for s in strs(n.args[0])]
            elif isinstance(n, ast.arguments):
                for x in n.defaults + [d for d in n.kw_defaults if d is not None]:
                    cands += [(s, "default arg") for s in strs(x)]
            for s, how in cands:
                if s.value in NOT_NAMES or (os.path.basename(path)[:-3], s.value) in NOT_HERE:
                    continue
                if s.value in FIELD_WORDS and how in ("x.get", "dict key"):
                    continue
                if how == "x.get" and not (REG.get(s.value.lower(), set()) & {"fitting", "item", "cover", "process", "gear", "holding"}):
                    continue
                key = (s.lineno, s.col_offset)
                if key in seen:
                    continue
                cats = REG.get(s.value.lower())
                if cats:
                    seen.add(key)
                    hits.append((s.lineno, s.value, "/".join(sorted(cats)), how, name))
    return sorted(hits)


if __name__ == "__main__":
    total, wave = collections.Counter(), collections.Counter()
    bycat, byname = collections.Counter(), collections.Counter()
    for m in FILES:
        p = os.path.join(ROOT, "cybertron2/engine", m + ".py")
        if not os.path.exists(p):
            continue
        new = blame_new(os.path.relpath(p, ROOT))
        h = scan(p)
        total[m] = len(h)
        for ln, v, c, how, fn in h:
            bycat[c] += 1
            byname[v] += 1
            w = new.get(ln, False)
            wave[m] += int(w)
            if "--list" in sys.argv:
                print(f"{m}.py:{ln}\t{v!r}\t{c}\t{how}\t{fn}\t{'wave' if w else ''}")
    print("by file:", dict(total), "total", sum(total.values()))
    print("of which in the wave:", dict(wave), "total", sum(wave.values()))
    print("by category:", dict(bycat.most_common()))
    print("most named:", byname.most_common(40))
