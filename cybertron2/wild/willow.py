"""Wild willow, the withies' stock (u3 §1.1; D2-264, D2-288, D2-312): the feature unit of the withies chain (D2-244). It replaces
stage 1's bridging `cut withies` from young growth wherever willow grows.

- **data:** `WILLOW` (K a unit of size in 10 kg bundles of usable rods a year: a fen 60, a parcel bordering water 20, from 0.3 and
  0.1 t a hectare a year at the generator's 2 ha cell, A7's default; the summer harm and its mending; grazing's halving);
- **the stock:** `res["willow"]` = {S, K, K0, r: 0, renewal: "willow"} on each fen parcel and on each meadow, pasture, scrub or wood
  parcel bordering water, seeded at a world's making (`seed`);
- **process:** the renewal rule `willow` (engine/renewal.py): the rods come back to K on the first night of spring, half of it on a
  parcel with beasts on it; K mends a tenth of its summer loss each spring;
- **verbs:** `cut withies` (engine/data.py) draws the willow where it grows, else young growth in a wood or scrub (crooked rods, the
  rate the same, u3 §1.1); a bundle cut in summer lowers K (`harm`).
A withy bed (a work, U7) is stage 5's.
"""
from __future__ import annotations

WILLOW = {"K": {"fen": 60.0, "bank": 20.0},           # bundles a unit of size a year (u3 §1.1; est.: the lever whether wild willow binds, W2-9)
          "summer_harm": 0.1,                         # K lost a bundle cut in summer (the stools harmed)
          "mend": 0.1,                                # the share of the loss K gets back each spring
          "grazed": 0.5}                              # the year's regrowth on a parcel with beasts on it (D2-156's young growth)
BANK_COVERS = ("meadow", "pasture", "scrub", "forest")


def K_of(w, pid) -> float:
    par = w.s["parcels"].get(pid) or {}
    size = max(1, int(par.get("size", 1)))
    if par.get("cover") == "fen":
        return float(WILLOW["K"]["fen"]) * size
    if par.get("cover") in BANK_COVERS and (any((w.s["parcels"].get(q) or {}).get("cover") == "water" for q in par.get("adj") or [])
                                            or (par.get("land") or {}).get("river") in ("brook", "river")):
        return float(WILLOW["K"]["bank"]) * size
    return 0.0


def seed(w) -> int:
    """Every fen parcel, and every meadow, pasture, scrub or wood parcel bordering water, gets its willow, full (at a world's making).
    A parcel whose spec gives `willow` keeps its own. Returns the parcels seeded."""
    n = 0
    for pid in sorted(w.s["parcels"]):
        par = w.s["parcels"][pid]
        if "willow" in par["res"]:
            continue
        K = K_of(w, pid)
        if K <= 0:
            continue
        par["res"]["willow"] = {"S": K, "K": K, "K0": K, "r": 0.0, "renewal": "willow"}
        n += 1
    return n


def renew(res, ctx) -> float:
    """The willow's night: on the first night of spring the rods are back to K (half the year's regrowth where beasts graze); no
    regrowth on any other night (a one-year rod, u3 Departure 14)."""
    S = float(res["S"])
    if not ctx.get("first_spring"):
        return round(S, 4)
    K = spring_K(res)
    grow = (K - S) * (float(WILLOW["grazed"]) if ctx.get("grazed") else 1.0)
    return round(min(K, S + max(0.0, grow)), 4)


def spring_K(res) -> float:
    """K in a new spring: the stools mend a tenth of their summer loss a year."""
    K, K0 = float(res["K"]), float(res.get("K0", res["K"]))
    return round(K + (K0 - K) * float(WILLOW["mend"]), 4) if K < K0 else K


def harm(here, pid, bundles) -> None:
    """Bundles cut in summer lower the stools' K (u3 §1.1)."""
    r = (here.parcels().get(pid) or {}).get("res", {}).get("willow")
    if not r or here.calendar()["season"] != "summer" or bundles <= 0:
        return
    k = round(max(0.0, float(r["K"]) - float(WILLOW["summer_harm"]) * float(bundles)), 4)
    here.apply("set_res", parcel=pid, key="willow", fields={"K": k, "S": min(float(r["S"]), k)})
