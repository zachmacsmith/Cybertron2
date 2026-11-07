"""Capacity across the land (D4-102): each node on its own, the region pooled, and what a short node could draw from its neighbours.

The world has no coordinates: nodes are joined by roads measured in days. Food carried d days on foot costs the carrier's meals both
ways: a load of `carry` (PHYSICS carry foot, and a pack's carry where packs can be made) delivers carry - 2 d x ration, so a share
e(d) = max(0, 1 - 2 d x ration / carry) arrives. A short node's reach is its own people supported plus each neighbour's surplus
times e(d) over the quickest way there (each neighbour counted whole for each node: an upper bound when several nodes draw on one).
"""
from __future__ import annotations

import heapq

from cybertron2.engine.data import ITEMS, PHYSICS


def days_between(w) -> dict:
    adj = {n: [] for n in w.s["nodes"]}
    for r in (w.s.get("roads") or {}).values():
        a, b = r.get("a"), r.get("b")
        if a in adj and b in adj:
            d = float(r.get("days") or 1)
            adj[a].append((b, d))
            adj[b].append((a, d))
    out = {}
    for s in adj:
        dist = {s: 0.0}
        q = [(0.0, s)]
        while q:
            d, u = heapq.heappop(q)
            if d > dist.get(u, 1e18):
                continue
            for v, dd in adj[u]:
                if d + dd < dist.get(v, 1e18):
                    dist[v] = d + dd
                    heapq.heappush(q, (d + dd, v))
        out[s] = dist
    return out


def carry(reach) -> float:
    c = float(PHYSICS["carry"]["foot"])
    if "pack" in reach.goods or "hide" in reach.goods:
        c += float(ITEMS["pack"]["carry"])
    return c


def efficiency(d, load) -> float:
    return max(0.0, 1.0 - 2.0 * d * float(PHYSICS["ration"]) / load)


def reach_table(w, report, level, reach) -> dict:
    """{node: {own, people, from: [(node, days, surplus, arrives)], with_reach}} at a level."""
    D = days_between(w)
    load = carry(reach)
    nodes = {k: v for k, v in report["nodes"].items() if k != "(region)"}
    out = {}
    for a, ra in nodes.items():
        own = ra["levels"][level]["supported"]
        got = []
        for b, rb in nodes.items():
            if b == a or b not in D.get(a, {}):
                continue
            surplus = rb["levels"][level]["supported"] - rb["people"]
            if surplus <= 0:
                continue
            e = efficiency(D[a][b], load)
            got.append((b, D[a][b], round(surplus, 1), round(surplus * e, 1)))
        out[a] = {"own": own, "people": ra["people"], "from": sorted(got, key=lambda x: x[1]),
                  "with_reach": round(own + sum(x[3] for x in got), 1)}
    return out


def frontier(w, report, level, home=None) -> dict:
    """Expansion outward from a home node, nodes taken in order of road days from it. Two curves of people supported:
    - settle: each node taken is lived in and feeds its own (people move to the land);
    - carry: everyone stays at home and each node's food is carried home over the road, a share e(d) arriving.
    With the capital each step needs (the level's houses, fittings and stores, in units with their materials, for the people the
    step adds) and the road days to the new land."""
    from cybertron2.capacity import levels as LV
    D = days_between(w)
    nodes = {k: v for k, v in report["nodes"].items() if k != "(region)"}
    if home is None:
        home = max(nodes, key=lambda k: (nodes[k]["people"], nodes[k]["levels"][level]["supported"]))
    order = sorted((n for n in nodes if n in D.get(home, {})), key=lambda n: (D[home][n], n))
    load = carry(LV.reach(w))
    steps, settle, carried = [], 0.0, 0.0
    for n in order:
        sup = nodes[n]["levels"][level]["supported"]
        cap = (nodes[n]["levels"][level].get("at_supported") or {}).get("capital") or {}
        e = efficiency(D[home][n], load)
        settle += sup
        carried += sup * e if n != home else sup
        steps.append({"node": n, "days": D[home][n], "supported": sup, "settle": round(settle, 1), "carry": round(carried, 1),
                      "arrives": round(e, 2), "capital": cap.get("with_materials")})
    return {"home": home, "level": level, "steps": steps, "carry_load": load}
