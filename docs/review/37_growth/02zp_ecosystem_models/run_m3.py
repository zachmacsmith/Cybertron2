import numpy as np, json, sys, populations as PO
FOREST = ["oak-ash wood", "beech wood", "alder carr", "birch and pine wood", "upland oak wood"]
def load(fn):
    d = dict(np.load(fn, allow_pickle=True))
    return d, PO.patches(d, np.isin(d["eco"], FOREST))
def run(fn, policy_fn, years=100, seed=0, wolves=True):
    d, pt = load(fn)
    w = PO.World(pt, seed=seed, wolves=wolves)
    for y in range(years):
        w.step(policy_fn(y))
    return w
def summ(w, a, b):
    L = w.log[a:b]
    return {k: round(float(np.mean([r[k] for r in L])), 2) for k in ("deer_wood", "deer_near", "deer_far", "boar", "wolves", "kill_rate", "stock_kills", "people_deer", "wood", "meat_kg_people", "boar_damage")}
if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "lands/settled_lowland_and_frontier_1.npz"
    d, pt = load(fn)
    area = pt["land"].sum() * pt["km"] ** 2
    print(fn, "land km2", round(area), "wood km2", round((pt["wood"] * pt["km"]**2).sum()), "patches", pt["shape"])
    out = {}
    pols = {
        "X1 wolves, light hunting": lambda y: {"hunt": "light"},
        "X2 wolves killed off (bounty from year 10)": lambda y: {"hunt": "light", "bounty": 0.5 if y >= 10 else 0.0},
        "X2b no wolves, no hunting": lambda y: {"hunt": "none", "bounty": 1.0},
        "X3 half the big wood felled in years 30-34": None,
        "X4 open-access deer hunting": lambda y: {"hunt": "open"},
        "X4b regulated deer hunting": lambda y: {"hunt": "regulated"},
    }
    for name, pol in pols.items():
        if name.startswith("X3"):
            d_, pt_ = load(fn); w = PO.World(pt_, seed=1)
            big = pt_["wood"] > 0.6
            for y in range(100):
                fell = (lambda ww, y=y: 0.1 * ww.W * big if 30 <= y < 35 else 0.0)
                w.step({"hunt": "light", "fell": fell})
        else:
            w = run(fn, pol, seed=1)
        out[name] = {"years 1-10": summ(w, 0, 10), "years 41-50": summ(w, 40, 50), "years 91-100": summ(w, 90, 100),
                     "series": {k: [round(r[k], 2) for r in w.log] for k in ("deer_wood", "deer_near", "deer_far", "wolves", "stock_kills", "wood", "boar", "boar_damage", "people_deer")},
                     "mast": [r["mast"] for r in w.log]}
        print(name)
        for k in ("years 1-10", "years 41-50", "years 91-100"): print("   ", k, out[name][k])
    json.dump(out, open("m3_" + fn.split("/")[1][:-4] + ".json", "w"))
