"""Survey B (W-110): every branch on a named thing in area B's function code.

Walks the AST of each module and reports string literals that are names of rows in the engine's registries (items, techniques,
fittings, rooms, blueprints, monuments, covers, resources, crops, herds kinds, things, processes, stores, gear lives) where they
appear in function code as: a comparison (==, !=, in, not in), a tuple/list/set literal used in a comparison or a call, a dict
literal's key, or a subscript into a registry by a literal ("TECHNIQUES['bury']"). Module-level registries are not counted.
Run: python3 -I docs/review/37_growth/02zzzm_patterns/B_branches.py [--list]
"""
import ast, sys, os, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, ROOT)
from cybertron2.engine import data as D
from cybertron2.engine import process as PROC, gear as GE, stores as SR

REG = {}
def add(cat, names):
    for n in names:
        if isinstance(n, str):
            REG.setdefault(n.lower(), set()).add(cat)
add("item", D.ITEMS); add("technique", D.TECHNIQUES); add("fitting", D.FITTINGS); add("room", D.ROOMS)
add("blueprint", D.BLUEPRINTS); add("monument", D.MONUMENTS); add("cover", D.COVERS); add("resource", D.RESOURCES)
add("crop", D.CROPS); add("thing", [k for k in D.THINGS if isinstance(D.THINGS.get(k), dict)])
add("herd", D.HERDS.get("roles", {}) if isinstance(D.HERDS.get("roles"), dict) else [])
add("herd", ["cow", "cows", "ox", "oxen", "bull", "bulls", "calf", "calves", "heifer"])
add("process", getattr(PROC, "PROCESSES", {})); add("structure", ["wattle", "timber", "stone", "camp"])
add("fence", D.FENCES if isinstance(D.FENCES, dict) else [])
add("season", ["spring", "summer", "autumn", "winter"])
add("gear", getattr(GE, "LIVES", {}))
FILES = ["verbs", "gear", "placed", "process", "stores", "buildings", "things", "farm", "herds", "night", "strips", "fuse", "yields",
         "keeping", "wear", "labour", "needs", "modifiers", "tags", "clocks", "outcomes"]
REGNAMES = {"ITEMS", "TECHNIQUES", "FITTINGS", "ROOMS", "BLUEPRINTS", "MONUMENTS", "COVERS", "RESOURCES", "CROPS", "THINGS", "HERDS",
            "PROCESSES", "LIVES", "I", "T", "F", "STORES", "FENCES", "WATER_WORKS", "DECAY", "KEEP_DAYS", "_I"}

FIELD_WORDS = {"herd", "pack", "for", "stop at", "carcass_sizes", "carcass_size", "carcass_meat", "carcass_road",
               "carcass_rot_season", "hidden", "set"}


def strs(node):
    out = []
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        out.append(node)
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        if not all(isinstance(e, ast.Constant) for e in node.elts):
            return out                                      # a ref ("herd", hid), not a list of names
        for e in node.elts:
            out += strs(e)
    return out

def scan(path):
    src = open(path).read()
    tree = ast.parse(src)
    hits = []
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    seen = set()
    for f in funcs:
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
                if s.value in FIELD_WORDS and how in ("x.get", "dict key"):
                    continue                            # a record's field ("herd", "pack", "set"), not a row's name
                if how == "x.get" and not (REG.get(s.value.lower(), set()) & {"fitting", "item", "cover", "process", "gear"}):
                    continue
                key = (s.lineno, s.col_offset)
                if key in seen:
                    continue
                cats = REG.get(s.value.lower())
                if cats:
                    seen.add(key)
                    hits.append((s.lineno, s.value, "/".join(sorted(cats)), how, f.name))
    return sorted(hits)

if __name__ == "__main__":
    total = collections.Counter(); bycat = collections.Counter(); byname = collections.Counter()
    for m in FILES:
        p = os.path.join(ROOT, "cybertron2/engine", m + ".py")
        if not os.path.exists(p):
            continue
        h = scan(p)
        total[m] = len(h)
        for ln, v, c, how, fn in h:
            bycat[c] += 1; byname[v] += 1
            if "--list" in sys.argv:
                print(f"{m}.py:{ln}\t{v!r}\t{c}\t{how}\t{fn}")
    print("by file:", dict(total), "total", sum(total.values()))
    print("by category:", dict(bycat.most_common()))
    print("most named:", byname.most_common(40))
