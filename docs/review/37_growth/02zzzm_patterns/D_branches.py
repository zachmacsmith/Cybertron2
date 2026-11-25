"""Survey D (W-110): branches on named things in area D's function code.

Walks each file's AST and finds string constants that name a registered row (a good, craft, fitting, cover, resource, building
part, structure, wild kind, gear, act) where code branches on them: in a comparison (==, !=, in, not in, including the tuple or set
on the right of `in`), as a key of a dict literal, as a subscript key or a .get() key. Text (f-strings, docstrings) is not counted.
Prints a count by file and by category, and every hit with file:line, for the survey's table.

Run from the repository root:  python3 docs/review/37_growth/02zzzm_patterns/D_branches.py [--hits]
"""
from __future__ import annotations

import ast
import sys
from collections import Counter, defaultdict
from pathlib import Path

from cybertron2.engine import data as D, verbs as V
from cybertron2.wild import kinds as K

ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path(".")
FILES = ["cybertron2/engine/signs.py", "cybertron2/engine/perceive.py", "cybertron2/engine/prompt.py", "cybertron2/engine/core.py",
         "cybertron2/engine/shapes.py", "cybertron2/engine/view.py", "cybertron2/engine/views.py", "cybertron2/engine/layout.py",
         "cybertron2/engine/evening.py", "cybertron2/wild/river.py", "cybertron2/engine/knowledge.py", "cybertron2/engine/modifiers.py"]

STRUCTURES = {"wattle", "timber", "stone", "camp", "post", "stone_m", "cairn"}
STAGES = {"infant", "child", "youth", "adult", "elder"}
CATS = [  # (category, names) in priority order: a word in two tables is put in the first
    ("weather", set(D.WEATHER)),
    ("terrain", set(D.TERRAIN)),
    ("fitting", set(D.FITTINGS) | set(D.FITTING_ALIAS)),
    ("building part", set(D.BLUEPRINTS) | set(D.ROOMS) | set(D.MONUMENTS) | set(D.FENCES) | STRUCTURES | set(D.TIERS)),
    ("cover", set(D.COVERS)),
    ("craft", set(D.TECHNIQUES)),
    ("good", set(D.ITEMS)),
    ("resource", set(D.RESOURCES)),
    ("wild kind", set(K.KINDS)),
    ("crop", set(D.CROPS) | set(D.CROP_OF)),
    ("stage", STAGES),
]
ACTS = set(V.VERB)


# a record's own field whose key happens to be a row's name (a parcel's "fence", a herd's "pack", an item's "camp" property), or a
# state value ("shut"): not a branch on the row, so not counted
FIELDS = {"fence", "built", "slaughter", "herd", "pack", "dead", "young", "for", "camp", "cairn", "weir", "hunted", "fight", "crew"}
STATES = {"shut"}


def cat(s):
    for c, names in CATS:
        if s in names:
            return c
    return None


def consts(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        for e in node.elts:
            yield from consts(e)


def _parents(tree):
    par = {}
    for n in ast.walk(tree):
        for ch in ast.iter_child_nodes(n):
            par[ch] = n
    return par


def _scope(node, par):
    """'function' (in a def), 'row' (in a lambda outside any def: a sign row's condition or words), 'data' (a module-level table)."""
    lam = False
    while node in par:
        node = par[node]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return "function"
        if isinstance(node, ast.Lambda):
            lam = True
    return "row" if lam else "data"


def _skipped(node, par):
    """Text and tag lists are not branches: inside an f-string, a docstring, or a `tags=`/`sense=` keyword."""
    while node in par:
        up = par[node]
        if isinstance(up, ast.JoinedStr):
            return True
        if isinstance(up, ast.keyword) and up.arg in ("tags", "sense", "text"):
            return True
        if isinstance(up, ast.Expr):
            return True
        node = up
    return False


def hits(path):
    tree = ast.parse((ROOT / path).read_text())
    par = _parents(tree)
    out = []
    for node in ast.walk(tree):
        found = []
        if isinstance(node, ast.Compare):
            for side in [node.left, *node.comparators]:
                found += [(c, "compare") for c in consts(side)]
        elif isinstance(node, ast.Dict):
            found += [(k, "dict key") for k in node.keys if k is not None and isinstance(k, ast.Constant)]
        elif isinstance(node, ast.Subscript):
            found += [(c, "subscript") for c in consts(node.slice)]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ("get", "setdefault", "pop") and node.args:
            found += [(c, ".get") for c in consts(node.args[0])]
        elif isinstance(node, (ast.Tuple, ast.List, ast.Set)) and not isinstance(par.get(node), (ast.Compare, ast.Subscript, ast.Tuple, ast.List, ast.Set)):
            found += [(c, "name list") for c in consts(node)]
        for c, how in found:
            if not isinstance(c.value, str) or _skipped(c, par):
                continue
            k = cat(c.value)
            if how in ("subscript", ".get") and c.value in FIELDS or c.value in STATES:
                continue
            if k:
                out.append((c.lineno, k, how, c.value, _scope(c, par)))
    return sorted(set(out))


def main():
    show = "--hits" in sys.argv
    tot = Counter()
    by = defaultdict(Counter)
    scope = defaultdict(Counter)
    tsc = Counter()
    for f in FILES:
        if not (ROOT / f).exists():
            print(f"{f}: (absent)")
            continue
        hs = hits(f)
        for ln, k, how, s, sc in hs:
            by[f][k] += 1
            tot[k] += 1
            scope[f][sc] += 1
            tsc[sc] += 1
            if show:
                print(f"{f}:{ln}\t{sc}\t{k}\t{how}\t{s}")
        print(f"{f}: {len(hs)}  [" + ", ".join(f"{k} {n}" for k, n in scope[f].most_common()) + "]  "
              + ", ".join(f"{k} {n}" for k, n in by[f].most_common()))
    print("total:", sum(tot.values()), dict(tsc), dict(tot.most_common()))


if __name__ == "__main__":
    main()
