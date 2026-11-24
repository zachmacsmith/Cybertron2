"""Aquatic ecosystems by environment, calibrated on the sweep's generated villages (W-108; 37.2, 24 Nov 2026).

    python3 calib.py            (reads ../a_sweep/data: experiments.json's per-village water areas, food.tsv's runs, worlds_index)

Every village's water is split into ecosystems by the world's landscape and the river's size above it (a Huet-style zonation),
each with a production a hectare and a season profile of what can be taken when. All on one clock (D2-273): a real year's take
x 32/365 is the world year's, shared over the seasons by the profile, 8 nights a season. Need: 11 food a night for ten people.
"""
import csv, json, os, statistics as stt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "a_sweep", "data")
FOOD_KG = 0.46            # whole fish, food a kg (data.py "fish")
TAKE = 0.5                # share of production a village can take for good (est.; Welcomme's heavily fished rivers)
NEED = 11.0               # food a night, ten people
NIGHTS = 8                # a season
YEAR = 32 / 365           # the year clock's quantity factor (D2-273, D2-259: runs and harvests)
SEASONS = ("spring", "summer", "autumn", "winter")

# production of whole fish, kg a ha a real year (lo, hi), and the share of a year's take that falls in each season
ECO = {
    "trout beck":      {"P": (20, 80),   "prof": (.25, .35, .25, .15), "fish": "brown trout, bullhead, minnow, stone loach, eel; salmon and sea trout parr"},
    "chalk stream":    {"P": (100, 300), "prof": (.25, .35, .25, .15), "fish": "brown trout, grayling, dace, eel, bullhead"},
    "mixed river":     {"P": (40, 120),  "prof": (.25, .35, .25, .15), "fish": "trout and grayling above, chub, dace, gudgeon, eel below"},
    "lowland river":   {"P": (50, 150),  "prof": (.30, .30, .25, .15), "fish": "chub, dace, roach, perch, pike, gudgeon, barbel, eel"},
    "big river":       {"P": (40, 100),  "prof": (.30, .30, .25, .15), "fish": "bream, roach, pike, perch, ruffe, eel; flounder near the tide"},
    "fen dykes":       {"P": (60, 200),  "prof": (.25, .40, .25, .10), "fish": "eel above all, pike, tench, rudd, bream, perch"},
    "lowland mere":    {"P": (30, 120),  "prof": (.30, .30, .25, .15), "fish": "pike, perch, roach, bream, tench, eel"},
    "upland tarn":     {"P": (5, 25),    "prof": (.20, .40, .30, .10), "fish": "brown trout, char, perch, minnow"},
    "estuary":         {"P": (30, 100),  "prof": (.35, .25, .25, .15), "fish": "flounder, grey mullet, bass, smelt, eel (on the river's area at the tide)"},
}
UPLAND = {"Upland and moor", "High mountains", "Cold north", "Wet west, maritime", "Coast under mountains", "river through a range",
          "two valleys over a pass", "gated valley"}


def zone(kind, upstream_km, big):
    """The river's ecosystem: by its size above the village and how steep its country is (Huet 1959's zones, by proxy)."""
    if big:
        return "big river"
    if kind == "Chalk and clay" and upstream_km < 30:
        return "chalk stream"
    if upstream_km < 5:
        return "trout beck"
    if kind in UPLAND:
        return "mixed river" if upstream_km < 40 else "lowland river"
    return "mixed river" if upstream_km < 8 else "lowland river"


def load():
    kinds = {r["id"]: r["kind"] for r in json.load(open(os.path.join(DATA, "worlds_index.json")))["rows"]}
    res = json.load(open(os.path.join(DATA, "experiments.json")))["resident"]["rows"]
    runs = defaultdict(lambda: defaultdict(lambda: [0.0] * 4))
    up = {}
    for r in csv.DictReader(open(os.path.join(DATA, "food.tsv")), delimiter="\t"):
        k = (r["world"], r["village"])
        f = lambda x, d: float(x) if x not in ("", "None") else d
        up[k] = (f(r["upstream_km"], 0.0), int(f(r["to_mouth"], 9)))
        if r["source"] in ("eel", "salmon", "lamprey"):
            runs[(r["arm"], k)][r["source"]] = [float(r[s]) for s in SEASONS]
    return kinds, res, runs, up


def village(row, kind, upk, to_mouth, lever=1.0):
    """Resident food a night by season (lo, hi), with the ecosystems it is made of."""
    ha = row["water ha"]
    parts = []
    for wk, a in ha.items():
        if wk in ("river", "big river"):
            parts.append((zone(kind, upk, wk == "big river"), a))
            if kind == "Estuary and saltmarsh" and to_mouth <= 1:
                parts.append(("estuary", a))
        elif wk == "fen":
            parts.append(("fen dykes", a))
        elif wk == "lake":
            parts.append(("upland tarn" if kind in UPLAND else "lowland mere", a))
        elif wk == "brook":
            parts.append(("trout beck", a))
    out = {s: [0.0, 0.0] for s in SEASONS}
    for eco, a in parts:
        e = ECO[eco]
        for j in (0, 1):
            year = TAKE * e["P"][j] * a * FOOD_KG * YEAR * lever          # food a world year
            for i, s in enumerate(SEASONS):
                out[s][j] += year * e["prof"][i] / NIGHTS
    return out, parts


def med(xs):
    return round(stt.median(xs), 2) if xs else None


def main():
    kinds, res, runs, up = load()
    by_kind = defaultdict(lambda: defaultdict(list))
    ecos = defaultdict(lambda: defaultdict(float))
    lever_need = []
    rows = []
    for r in res:
        k = (r["world"], r["village"])
        kind = kinds.get(r["world"], "?")
        upk, tm = up.get(k, (0.0, 9))
        out, parts = village(r, kind, upk, tm)
        for eco, a in parts:
            ecos[kind][eco] += a
        best_mid = max((out[s][0] + out[s][1]) / 2 for s in SEASONS)
        lever_need.append((NEED / 4) / best_mid if best_mid else None)
        rn = runs.get(("fix", k)) or {}
        run_season = [sum(rn.get(x, [0] * 4)[i] for x in ("eel", "salmon", "lamprey")) / NIGHTS for i in range(4)]
        sal = rn.get("salmon", [0] * 4)
        spring_salmon = 0.3 * (sal[2] + sal[3]) / NIGHTS                   # a spring share of the salmon run (30%)
        rows.append({"world": r["world"], "village": r["village"], "kind": kind, "ecosystems": [e for e, _ in parts],
                     "resident": out, "runs passing a night": run_season, "spring salmon a night": spring_salmon})
        b = by_kind[kind]
        for i, s in enumerate(SEASONS):
            b[f"res_{s}"].append((out[s][0] + out[s][1]) / 2)
            b[f"run_{s}"].append(run_season[i])
        b["spring_salmon"].append(spring_salmon)
    print("Resident fish by ecosystem (mid of lo and hi), food a night, and the runs passing (fix arm), by the world's landscape")
    print(f"{'landscape':28s} {'n':>3s} | resident spr sum aut win | runs passing spr sum aut win | +spring salmon | ecosystems (ha)")
    for kind, b in sorted(by_kind.items()):
        n = len(b["res_spring"])
        e = ", ".join(f"{x} {round(a / n, 1)}" for x, a in sorted(ecos[kind].items(), key=lambda t: -t[1]))
        print(f"{kind:28s} {n:3d} | " + " ".join(f"{med(b['res_' + s]):5.2f}" for s in SEASONS) + " | "
              + " ".join(f"{med(b['run_' + s]):6.1f}" for s in SEASONS) + f" | {med(b['spring_salmon']):5.1f} | {e}")
    L = sorted(x for x in lever_need if x)
    print(f"\nlever for the resident fish at their best season to reach a quarter of need (2.75 a night): median {med(L)}, "
          f"quartiles {round(L[len(L) // 4], 1)} to {round(L[3 * len(L) // 4], 1)}, range {round(L[0], 1)} to {round(L[-1], 1)}")
    json.dump(rows, open(os.path.join(HERE, "villages.json"), "w"), indent=0)


if __name__ == "__main__":
    main()
