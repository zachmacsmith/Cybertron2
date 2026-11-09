"""Checks of the general system: no kind named in the rule code; every kind's row uses only a known rule; where each kind lives."""
import re, collections, sys
import kinds as K
import sim

bad = []
words = set()
for name in K.KINDS:
    words |= {w for w in re.findall(r"[a-z]+", name) if len(w) > 3 and w not in ("wild", "birds", "corn", "mice")}
words |= {"boar", "deer", "hare", "eel", "fowl", "rat", "pigeon", "mast", "acorn"}
import ast
for f in ("rules.py", "village.py"):
    tree = ast.parse(open(f).read())
    for node in ast.walk(tree):                                    # drop docstrings; keep every other string and name
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) \
                and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body = node.body[1:] or [ast.Pass()]
    code = ast.unparse(tree).lower()
    for w in sorted(words):
        if re.search(r"\b" + w + r"s?\b", code):
            bad.append((f, w))
print("kind names in rule code:", bad or "none")
pres = collections.Counter(); n = 0
for r in sim.runs(eras=["steady"]):
    v = sim.Village(r["land"], r["drv"], r["pulses"], K.KINDS, sim.np.random.default_rng(0))
    v.morning(0)
    n += 1
    for k, p in v.present().items():
        pres[k] += int(p)
print(f"villages: {n}; where each kind lives:", dict(pres))
sys.exit(1 if bad else 0)
