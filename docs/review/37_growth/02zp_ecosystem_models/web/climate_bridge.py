"""The bridge from 37.4's climate (engine/climate.py, D4-109) to the food web: a world's weather, summed by season each year, as
growth by food, snow cover and mast odds. Anomalies against the era's own normals, so the engine's short year does not matter."""
import sys, numpy as np
sys.path.insert(0, "/home/user/cyb-climate")   # the climate-calibration worktree
from cybertron2.engine.world import World, load_spec
from cybertron2.engine import climate as CL

def seasons(spec_path, era="steady", years=80, node=None, over=None):
    spec = load_spec(spec_path); spec["climate"] = dict(spec.get("climate") or {}, era=era, **(over or {}))
    w = World(spec); yd = w.year_days(); sl = yd // 4; ref = node or sorted(w.s["nodes"])[0]
    out = []
    for y in range(years):
        rec = {}
        for si, s in enumerate(("spring", "summer", "autumn", "winter")):
            days = range(y * yd + si * sl, y * yd + (si + 1) * sl)
            e = [CL.env(w, ref, d) for d in days]; lab = [CL.label(w, ref, d) for d in days]
            rec[s] = {"temp": float(np.mean([x["temp"] for x in e])), "wet": float(np.mean([x["rain"] > 0.2 for x in e])),
                      "frost": float(np.mean([x["low"] < 0 for x in e])), "snow": lab.count("snow") / len(lab)}
        out.append(rec)
    return out

def weather_fn(series, normal=None):
    """{year -> growth by food, hard, snow, mast_p}. normal: the steady era's seasonal means (so other eras read as anomalies)."""
    normal = normal or {s: {k: float(np.mean([r[s][k] for r in series])) for k in ("temp", "wet", "frost", "snow")} for s in series[0]}
    def fn(y):
        r = series[y % len(series)]; prev = series[(y - 1) % len(series)]
        dT = {s: r[s]["temp"] - normal[s]["temp"] for s in r}
        wet = {s: r[s]["wet"] / max(normal[s]["wet"], 1e-3) for s in r}
        grow_season_T = (dT["spring"] + dT["summer"]) / 2
        water = (wet["spring"] + wet["summer"]) / 2                     # a dry spring and summer: drought
        drought = float(np.clip(water, 0.4, 1.5))
        g = {
            "grass": float(np.clip(1 + 0.06 * grow_season_T, 0.6, 1.4) * (0.4 + 0.6 * min(drought, 1.2))),
            "sward": float(np.clip(1 + 0.06 * grow_season_T, 0.6, 1.4) * (0.4 + 0.6 * min(drought, 1.2))),
            "browse": float(np.clip(1 + 0.04 * grow_season_T, 0.7, 1.3) * (0.75 + 0.25 * min(drought, 1.2))),
            "heather": float(np.clip(1 + 0.03 * grow_season_T, 0.8, 1.2)),
            "seeds": float(np.clip(1 + 0.10 * dT["summer"], 0.5, 1.6) * (1.1 if wet["summer"] < 0.9 else 0.9)),
            "fruit": float(np.clip(1 + 0.08 * dT["summer"], 0.5, 1.6) * (1 - 0.5 * r["spring"]["frost"])),
            "aquatic": float(np.clip(0.6 + 0.4 * (wet["spring"] + wet["summer"] + wet["autumn"]) / 3, 0.5, 1.4)),
            "inverts": float(np.clip(0.5 + 0.5 * water, 0.5, 1.3) * (1 - 0.3 * max(0, r["winter"]["frost"] - normal["winter"]["frost"]))),
            "roots": 1.0,
        }
        for f in ("grass", "browse", "heather", "aquatic"):
            g[f + "~coarse"] = g[f]
        snow = float(np.clip(r["winter"]["snow"] * 3, 0, 1))             # days of snow as cover through the winter
        hard = r["winter"]["frost"] > normal["winter"]["frost"] + 0.1 or snow > 0.5
        mast_p = float(np.clip(0.25 + 0.2 * dT["summer"] if prev is None else 0.25 + 0.2 * (prev["summer"]["temp"] - normal["summer"]["temp"]), 0.05, 0.7))
        return {"growth": g, "hard": hard, "snow": snow, "mast_p": mast_p}
    return fn, normal
