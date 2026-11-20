"""02zzu applied: the shared-units model (02zzu_shared_units.py) re-run on the engine's data after the data change (D2-258, D2-259).

37.2, 20 Nov 2026 (W-64). The model's "now" column is what each method was measured at on the old values (02zzd, 4c, 38.73); its
"after" column was 02zzu's prediction. Here the factor is taken from the engine's tables as they now stand against the old values
(02zzu's GOODS and ANIMALS `now`), so the column "applied" is what the measured rates become on the data that was written, at the
same kilograms a unit, with the gathering's kg a unit (wild/plants.py `kg`) applied to each kind in the mix. Then the weir: the run
pulses recorded by `02zzu_shared_units.py runs` on the new data (a JSON of its own, given as an argument) against a one-section
wattle weir whose hold is in kg (data.WATER_WORKS, D2-258).

    CYB_ROOT=. python3 -I docs/review/37_growth/02zzu_applied.py methods
    CYB_ROOT=. python3 -I docs/review/37_growth/02zzu_applied.py weir RUNS_JSON [food]

RUNS_JSON is the `runs` object of a 02zzu_shared_units.json written by its `runs` mode on the engine being read.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("CYB_ROOT", "."))
_spec = importlib.util.spec_from_file_location("zzu", os.path.join(HERE, "02zzu_shared_units.py"))
Z = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Z)

from cybertron2.engine import data as D          # noqa: E402
from cybertron2.wild import plants as PL         # noqa: E402

KG = {sp["item"]: float(sp.get("kg", 1.0)) for sp in PL.PLANTS.values()}   # kg a unit of gathering by good (D2-258)
FOOD_NOW = {k: g["now"] for k, g in Z.GOODS.items()}                      # the old values (02zzu's `now`)


def food_new(good) -> float:
    return float(D.ITEMS[good]["food"])


def kill_new(kind) -> float:
    """Food a head on the engine's data now: its taken goods (or the slaughter's) x the goods' food."""
    if kind in ("cow", "ox", "young"):
        g = D.TECHNIQUES["slaughter"]["yield"]["gives"][{"cow": "cows", "ox": "oxen", "young": "young"}[kind]]
    else:
        g = D.RESOURCES[kind]["taken"]["goods"]
    return sum(float(q) * food_new(i) for i, q in g.items() if float(D.ITEMS.get(i, {}).get("food", 0)) > 0)


def factor(name, m) -> float:
    goods = m["goods"]
    if name in Z.HUNT_MIX:
        mix = Z.HUNT_MIX[name]
        return sum(w * kill_new(k) for k, w in mix.items()) / sum(w * Z.kill_food_now(k) for k, w in mix.items())
    old = new = 0.0
    for k, w in goods.items():
        if k in ("eel", "salmon"):
            old += w * Z.kill_food_now(k)
            new += w * kill_new(k)
        else:
            old += w * FOOD_NOW[k]
            new += w * food_new(k) * (KG.get(k, 1.0) if name.startswith("gathering") else 1.0)
    return new / old if old else 1.0


def legacy_rows() -> dict:
    """The legacy techniques the model did not have: the forage (`gather`) and the hunt, at a full stock and armed."""
    h = D.TECHNIQUES["hunt"]["yield"]
    hunt_old = 0.35 * 4.0 * 1.5 / 2.0                                            # p x mean of [2, 6] x meat 1.5, 2 units
    hunt_new = float(h["p"]) * sum(h["range"]) / 2.0 * food_new("meat") / float(D.TECHNIQUES["hunt"]["units"])
    gb = float(D.TECHNIQUES["forage"]["yield"]["base"])
    return {"legacy hunt (full stock, armed)": (hunt_old, hunt_new, (500, 1500)),
            "legacy forage (full stock)": (gb * 1.0, gb * food_new("wild food"), (300, 3000))}


def methods() -> list:
    b = Z.BASIS
    be = Z.breakeven(b)
    rows = []
    for name, m in Z.METHODS.items():
        lo, hi, alo, ahi, rlo, rhi, fix = Z.method_after(name, b)
        f = factor(name, m)
        pred = fix if fix and name.startswith("gathering") else (alo, ahi)
        rows.append({"method": name, "before": [round(lo, 2), round(hi, 2)], "predicted": [round(pred[0], 2), round(pred[1], 2)],
                     "applied": [round(lo * f, 2), round(hi * f, 2)], "real": [round(rlo, 2), round(rhi, 2)],
                     "verdict": Z.verdict((lo * f, hi * f), (rlo, rhi), be)})
    for name, (old, new, real) in legacy_rows().items():
        r = tuple(x * b["hours_unit"] / b["kcal_food"] for x in real)
        rows.append({"method": name, "before": [round(old, 2)] * 2, "predicted": None, "applied": [round(new, 2)] * 2,
                     "real": [round(r[0], 2), round(r[1], 2)], "verdict": Z.verdict((new, new), r, be)})
    return rows


def weir(path, by="kg") -> list:
    """A one-section wattle weir's year at each station on the recorded pulses: the share each night, capped by the hold in kg
    (the catch's goods' weight), valued at the engine's food a head; the work as 02zzu's weir_year. `by` "food": the hold read as
    food, as it was before D2-258 (for the engine before the change, CYB_ROOT at that checkout)."""
    rec = json.load(open(path))
    W = D.WATER_WORKS["weir"]
    share, hold = float(W["sections"]["wattle"]["share"]), float(W["sections"]["wattle"]["hold"])
    kg = {k: sum(float(q) for i, q in D.RESOURCES[k]["taken"]["goods"].items() if float(D.ITEMS[i]["food"]) > 0)
          for k in ("eel", "salmon", "lamprey")}
    out = []
    for wname, r in rec.items():
        for v, inf in r["villages"].items():
            N = len(r["nights"])
            heads = {k: [0.0] * N for k in kg}
            for i, n in enumerate(r["nights"]):
                for key, q in n["run"].items():
                    vv, k, how = key.split("|")
                    if vv == v and k in heads and how != "held":
                        heads[k][i] += q
            food = taken_kg = 0.0
            nights = capped = peak = 0
            for d in range(N):
                want = {k: share * heads[k][d] for k in heads}
                wkg = sum(want[k] * (kg[k] if by == "kg" else kill_new(k)) for k in want)
                if wkg <= 1e-9:
                    continue
                nights += 1
                peak = max(peak, wkg)
                f = min(1.0, hold / wkg)
                capped += f < 1.0
                taken_kg += wkg * f
                food += sum(want[k] * f * kill_new(k) for k in want)
            build = Z.WEIR["build_units"] + Z.WEIR["timber"] * Z.WEIR["fell_units_a_timber"]
            work = Z.WEIR["upkeep_share"] * build + Z.WEIR["shut_units"] + Z.WEIR["open_units"] + Z.WEIR["lift_units"] * nights
            out.append({"world": wname, "station": v, "catchment_km2": inf["catchment_km2"],
                        "heads_year": {k: round(sum(x), 1) for k, x in heads.items()}, "run_nights": nights,
                        f"peak_night_{by}_offered": round(peak, 1), "nights_hold_binds": capped, f"{by}_taken": round(taken_kg, 1),
                        "food": round(food, 1), "work": round(work, 1), "food_a_unit": round(food / work, 2)})
    return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "methods"
    res = methods() if mode == "methods" else weir(sys.argv[2], *(sys.argv[3:4]))
    print(json.dumps(res, indent=1))
