"""Water bodies (D2-229): a lake's resident fish are one stock, and a river's one stock a reach, fished from every water parcel on it.

The generator lists the bodies in the land summary (`wild.land.waters`: {body id: {kind, km2 | river_km, areas, parcels}}) and names
each water parcel's body (`land.water_body`). The world holds each body's stocks once, in s["waters"][body] = {"kind", "parcels",
"fish": {S, K, r, renewal, ...}}, and every parcel on the body holds that same record as its own `res["fish"]`: one object, so every
reader and every primitive (draw, set_res, add_res) that goes through the parcel changes the body's stock. A saved world (JSON)
keeps the values on both; `link` makes them one object again when a world is restored.

Two rules keep the shared stock counted once: the night renews a stock once (night._grow skips a record it has renewed), and
anything that sums or scales stocks over parcels takes a body's stock at its lead parcel only (`lead`): the capacity model, a site's
share of the village's stock, a beaver dam's raise.

A world without a waters list (every world before D2-229) holds no s["waters"] and is unchanged, so its replays stay exact."""
from __future__ import annotations

SHARED = ("fish",)                       # the stocks a body holds (D2-229: its resident fish)


def seed(w, spec) -> None:
    """At a world's making: each body with water parcels in this world gets one record a stock, seeded from its parcels' own: K and
    S summed, the rest (r, renewal, response, ...) from the parcel with the largest K. Then every parcel on it shares that record."""
    waters = (((spec.get("wild") or {}).get("land") or {}).get("waters")) or {}
    if not waters:
        return
    bodies = {}
    for bid, b in sorted(waters.items()):
        pids = sorted(p for p in (b.get("parcels") or []) if p in w.s["parcels"])
        pids += sorted(p for p, par in w.s["parcels"].items() if (par.get("land") or {}).get("water_body") == bid and p not in pids)
        if not pids:
            continue
        rec = {"kind": b.get("kind", ""), "parcels": sorted(pids)}
        for key in SHARED:
            own = [(p, w.s["parcels"][p]["res"][key]) for p in rec["parcels"] if key in w.s["parcels"][p]["res"]]
            if not own:
                continue
            top = max(own, key=lambda pr: (float(pr[1]["K"]), pr[0]))[1]
            r = {k: v for k, v in top.items() if k not in ("S", "K")}
            r["S"] = round(sum(float(x["S"]) for _, x in own), 4)
            r["K"] = round(sum(float(x["K"]) for _, x in own), 4)
            rec[key] = r
        bodies[bid] = rec
    if bodies:
        w.s["waters"] = bodies
        link(w)


def link(w) -> None:
    """Every parcel on a body holds the body's own record for its shared stocks (after making, or after a world is restored)."""
    for bid, b in (w.s.get("waters") or {}).items():
        for key in SHARED:
            if key in b:
                for p in b["parcels"]:
                    if p in w.s["parcels"]:
                        w.s["parcels"][p]["res"][key] = b[key]


def body_of(w, pid) -> str | None:
    """The body a parcel's shared stocks belong to, if the world holds bodies."""
    for bid, b in (w.s.get("waters") or {}).items():
        if pid in b["parcels"]:
            return bid
    return None


def lead(w, pid, key) -> bool:
    """True if this parcel stands for its stock `key` where stocks are summed or scaled over parcels: always, unless the stock is a
    body's and another parcel on it comes first."""
    if key not in SHARED or not w.s.get("waters"):
        return True
    bid = body_of(w, pid)
    return bid is None or key not in w.s["waters"][bid] or w.s["waters"][bid]["parcels"][0] == pid
