"""Survey A (W-110): count the branches on named things in the area's function code.

Run from the repo root: python3 docs/review/37_growth/02zzzm_patterns/a_named.py [--list]
A branch is a comparison (==, !=, in, not in) whose one side is a string literal, or a tuple, list or set of them, naming a row of a
category (a good, technique, fitting, cover, resource or wild kind, crop, building part, water type ...); or a subscript of a registry
by a literal name (ITEMS["firewood"]); or a dict literal inside a function whose keys are row names. Module-level side tables keyed
by row names are counted apart (they are data, but data off the row)."""
import ast, sys, os, collections
sys.path.insert(0, os.getcwd())
from cybertron2.engine import data as D
from cybertron2.wild import kinds as WK, plants as WP, methods as WM

CATS = collections.OrderedDict()
CATS["good"] = set(D.ITEMS)
CATS["technique"] = set(D.TECHNIQUES) | {a for t in D.TECHNIQUES.values() for a in t.get("aliases", [])}
CATS["fitting"] = set(D.FITTINGS) | set(D.FITTING_ALIAS)
CATS["building"] = set(D.BLUEPRINTS) | set(D.ROOMS) | set(D.MONUMENTS) | set(D.WATER_WORKS) | {"wattle", "timber", "stone", "camp", "house", "barn", "mill", "weir"}
CATS["cover"] = set(D.COVERS) | {"bank"}
CATS["resource"] = set(D.RESOURCES)
CATS["wild kind"] = set(WK.KINDS) | set(WK.RUNS) | set(WK.LOADS) | set(WK.DISEASES) | set(WP.PLANTS) | set(WK.FOOD)
CATS["crop"] = set(D.CROPS) | set(D.CROP_OF)
CATS["water type"] = {"brook", "pool", "river", "big river", "lake", "small", "sea", "estuary"}
CATS["forest kind"] = set(D.FORESTS["kinds"])
from cybertron2.landgen import ecology as LE, vocab as LV, macro as LM
CATS["ecosystem"] = set(LE.ECOSYSTEMS)
CATS["terrain"] = set(LV.TERRAINS) | set(LM.SYSTEMS)
CATS["season"] = {"spring", "summer", "autumn", "winter"}
CATS["weather"] = set(D.WEATHER) | {"gale", "snow", "heavy rain", "fog", "clear", "rain"}
REG = {"ITEMS", "TECHNIQUES", "FITTINGS", "RESOURCES", "COVERS", "CROPS", "FORESTS", "KINDS", "WK.KINDS", "RUNS", "PLANTS", "METHODS",
       "BLUEPRINTS", "ROOMS", "MONUMENTS", "WATER_WORKS", "HERDS", "LOADS", "DISEASES", "FOOD", "SHALLOWS", "ICE", "WILLOW", "SETS"}

NOT_ROWS = {"herd", "person", "parcel", "building", "container", "offer", "shut", "open", "S", "K", "r", "shallow", "young",
            "hunt", "small", "wind"}   # a ref's kind, a door's or gap's state, a stock's fields, a carcass stage, a herd role, a yield
                                        # kind, the water class "small" (kept as water type below)

def cat_of(s):
    if s in NOT_ROWS and s != "small":
        return []
    out = [c for c, names in CATS.items() if s in names]
    return out

def strs(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)) and node.elts and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
        return [e.value for e in node.elts]
    return []

def regname(n):
    if isinstance(n, ast.Name):
        return n.id
    if isinstance(n, ast.Attribute):
        return n.attr
    return None

def scan(path):
    src = open(path).read()
    tree = ast.parse(src)
    hits = []
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            funcs.append(node)
    infunc = set()
    for f in funcs:
        for n in ast.walk(f):
            infunc.add(id(n))
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            sides = [node.left] + list(node.comparators)
            if not any(isinstance(o, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)) for o in node.ops):
                continue
            for sd in sides:
                for s in strs(sd):
                    c = cat_of(s)
                    if c and c != ["season"] and c != ["weather"]:
                        hits.append(("compare", node.lineno, s, c, id(node) in infunc))
                    elif c:
                        hits.append(("compare-time", node.lineno, s, c, id(node) in infunc))
        elif isinstance(node, ast.Subscript):
            rn = regname(node.value)
            key = node.slice
            if rn in REG:
                for s in strs(key):
                    c = cat_of(s)
                    if c:
                        hits.append(("lookup", node.lineno, s, c, id(node) in infunc))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get" and regname(node.func.value) in REG and node.args:
            for s in strs(node.args[0]):
                c = cat_of(s)
                if c:
                    hits.append(("lookup", node.lineno, s, c, id(node) in infunc))
        elif isinstance(node, ast.Dict) and node.keys:
            ks = [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            named = [k for k in ks if cat_of(k) and cat_of(k) not in (["season"], ["weather"])]
            if len(named) >= 2 and len(named) >= len(ks) / 2:
                hits.append(("dict" if id(node) in infunc else "side-table", node.lineno, ",".join(named[:6]) + ("..." if len(named) > 6 else ""),
                             sorted({c for k in named for c in cat_of(k)}), id(node) in infunc))
    # module-level names holding row names (a tuple, list or set of them, or a dict keyed by them): their uses in function code
    named_consts = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            v = node.value
            if isinstance(v, ast.Dict):
                continue                                  # a dict keyed by names is a side table (counted at module level)
            ks = strs(v)
            if isinstance(v, ast.Call) and v.args:
                ks = strs(v.args[0])
            named = [k for k in ks if cat_of(k) and cat_of(k) not in (["season"], ["weather"])]
            if named and len(named) >= max(1, len(ks) / 2):
                named_consts[node.targets[0].id] = sorted({c for k in named for c in cat_of(k)})
    for f in funcs:
        for n in ast.walk(f):
            if isinstance(n, ast.Name) and n.id in named_consts and isinstance(n.ctx, ast.Load):
                hits.append(("via-constant", n.lineno, n.id, named_consts[n.id], True))
    return hits

FILES = ["cybertron2/engine/" + f for f in ("world.py", "data.py", "renewal.py", "waters.py", "wild.py", "climate.py", "environment.py",
         "forests.py", "capacity.py", "generate.py")]
FILES += sorted("cybertron2/wild/" + f for f in os.listdir("cybertron2/wild") if f.endswith(".py"))
FILES += sorted("cybertron2/landgen/" + f for f in os.listdir("cybertron2/landgen") if f.endswith(".py"))

if __name__ == "__main__":
    tot = collections.Counter()
    bycat = collections.Counter()
    rows = []
    for f in FILES:
        h = scan(f)
        c = collections.Counter(k for k, *_ in h)
        tot.update(c)
        for k, ln, s, cs, inf in h:
            if k in ("compare", "lookup", "dict", "via-constant"):
                for x in cs[:1]:
                    bycat[x] += 1
            rows.append((f, ln, k, s, "/".join(cs)))
        print(f"{f:40s} compare {c['compare']:4d}  lookup {c['lookup']:4d}  dict {c['dict']:3d}  side-table {c['side-table']:3d}  via-constant {c['via-constant']:3d}  (time words {c['compare-time']})")
    print("total", dict(tot))
    print("by category (first match)", dict(bycat.most_common()))
    if "--list" in sys.argv:
        for r in sorted(rows):
            print("%s:%d %s %r [%s]" % r)
