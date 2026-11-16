"""The land summary for the wild layer (proposals/wild_layer.md §3.1, D2-199): the generated land cut into areas, fine where people
are and coarse away from them (02zp part four: the village's own land, a ring around it, and wild blocks between give the local
behaviour of a fine grid at a thirtieth of the cost).

Areas:
- **home**: a node's own parcels (the parcels are windows onto it);
- **ring**: the land within RING_KM of a node's site that no node holds, given to the nearest node;
- **wild**: the rest of the land, in blocks of about BLOCK_KM.

Each area holds what its cells say: land area, cover and ecosystem by km2, old wood (a wood's core), wetness, height, warmth, soil
textures, rock, water (rivers by length, lakes by area), its node (for the weather by place, D4-111), and for home areas its
parcels. Links between areas carry the length of the edge they share; river areas name the area their water flows to.

Written with the world by the generator (`world["wild"]["land"]`), so a run carries it: a few kilobytes, not the land itself (G-33).
"""
from __future__ import annotations

import numpy as np

from cybertron2.landgen import vocab as V

RING_KM = 2.5
BLOCK_KM = 8.0
TEXTURE = V.TEXTURE


def build(L, nodes, km: float) -> dict:
    """L: the generator's land (cell arrays); nodes: the generator's nodes (key, site (row, col), parcels with cells)."""
    ny, nx = L.cover.shape
    land = ~np.asarray(L.sea, dtype=bool)
    label = np.full((ny, nx), -1, dtype=np.int64)
    meta = []                                                              # (kind, node key, parcels)
    unsettled = set()                                                      # vacant places: home areas no one lives in
    for s in nodes:                                                        # home: each node's parcels
        cells = [tuple(c) for p in s.parcels for c in p.cells]
        if not cells:
            continue
        i = len(meta)
        meta.append(("home", s.key, sorted(p.pid for p in s.parcels)))
        if getattr(s, "kind", "") == "vacant":
            unsettled.add(s.key)
        r, c = np.array(cells).T
        label[r, c] = i
    yy, xx = np.mgrid[0:ny, 0:nx]
    sites = [(s.key, s.site) for s in nodes if s.parcels]
    if sites:                                                              # ring: unheld land near a node, to the nearest node
        d = np.stack([np.hypot(yy - r, xx - c) * km for _, (r, c) in sites])
        near, dmin = d.argmin(0), d.min(0)
        ring_of = {}
        for j, (key, _) in enumerate(sites):
            m = (label < 0) & land & (near == j) & (dmin <= RING_KM)
            if m.any():
                ring_of[key] = len(meta)
                meta.append(("ring", key, []))
                label[m] = ring_of[key]
    b = max(1, int(round(BLOCK_KM / km)))                                  # wild: blocks of the rest
    block = (yy // b) * ((nx + b - 1) // b) + (xx // b)
    rest = (label < 0) & land
    for blk in np.unique(block[rest]):
        m = rest & (block == blk)
        meta.append(("wild", None, []))
        label[m] = len(meta) - 1
    # each area's land, from its cells
    by_node = {s.key: s for s in nodes}
    nearest = _nearest_node(L, sites, km)
    cover, eco = np.asarray(L.cover).astype(str), np.asarray(L.eco).astype(str)
    band = np.asarray(L.band) if getattr(L, "band", None) is not None else np.zeros((ny, nx))
    cell_km2 = km * km
    areas = {}
    for i, (kind, key, parcels) in enumerate(meta):
        m = label == i
        n = int(m.sum())
        if not n:
            continue
        cy, cx = float(yy[m].mean()), float(xx[m].mean())
        node = key if key is not None else nearest(cy, cx)
        cov = {str(k): round(float(v) * cell_km2, 4) for k, v in zip(*np.unique(cover[m], return_counts=True))}
        ecs = {str(k): round(float(v) * cell_km2, 4) for k, v in zip(*np.unique(eco[m], return_counts=True))}
        if kind == "home":                                                 # a node's own land is what its parcels are (fields,
            cov, ecs = {}, {}                                              # built ground), not the region's cover beneath them
            for p in by_node[key].parcels:
                k2 = len(p.cells) * cell_km2
                cov[p.cover] = round(cov.get(p.cover, 0.0) + k2, 4)
                if p.eco:
                    ecs[p.eco] = round(ecs.get(p.eco, 0.0) + k2, 4)
        tex = {TEXTURE.get(int(k), str(k)): round(float(v) / n, 3) for k, v in zip(*np.unique(np.asarray(L.tex)[m], return_counts=True))}
        riv = np.asarray(L.river)[m]
        areas[f"a{i}"] = {
            "kind": kind, "node": node, "parcels": parcels, "km2": round(n * cell_km2, 4),
            **({"settled": False} if kind == "home" and key in unsettled else {}),
            "xy_km": [round(cx * km, 2), round(cy * km, 2)],
            "cover": cov, "eco": ecs,
            "old_wood_km2": round(float(((band[m] >= 3) & (cover[m] == "forest")).sum()) * cell_km2, 4),
            "wood_edge_km2": round(float(((band[m] == 1) & (cover[m] == "forest")).sum()) * cell_km2, 4),
            "wet": round(float(np.asarray(L.wet)[m].mean()), 3), "elevation": round(float(np.asarray(L.h)[m].mean()), 1),
            "temp": round(float(np.asarray(L.temp)[m].mean()), 2), "texture": tex,
            "rock": round(float((np.asarray(L.slope)[m] >= 25).mean()), 3),
            "river_km": round(float((riv >= 1).sum()) * km, 3), "big_river_km": round(float((riv >= 3).sum()) * km, 3),
            "lake_km2": round(float(np.asarray(L.lake)[m].sum()) * cell_km2, 4),
        }
    # links: the length of shared edge, from neighbouring cells with different areas
    pairs = []
    for a, bb in ((label[:, :-1], label[:, 1:]), (label[:-1, :], label[1:, :])):
        ok = (a != bb) & (a >= 0) & (bb >= 0)
        pairs.append(np.stack([np.minimum(a[ok], bb[ok]), np.maximum(a[ok], bb[ok])], 1))
    pairs = np.concatenate(pairs) if pairs else np.zeros((0, 2), dtype=np.int64)
    links = []
    if len(pairs):
        u, cnt = np.unique(pairs, axis=0, return_counts=True)
        links = [[f"a{int(x)}", f"a{int(y)}", round(float(c) * km, 3)] for (x, y), c in zip(u, cnt)]
    # where each area's water goes: from its largest river cell downstream to the first cell in another area
    down = {}
    recv, acc = np.asarray(L.recv), np.asarray(L.acc).ravel()
    lab = label.ravel()
    for aid, a in areas.items():
        if a["river_km"] <= 0:
            continue
        i = int(aid[1:])
        idx = np.flatnonzero((lab == i) & (np.asarray(L.river).ravel() >= 1))
        j = int(idx[np.argmax(acc[idx])])
        to = "out"
        for _ in range(ny * nx):
            j = int(recv[j])
            if j < 0:
                break
            if lab[j] != i and lab[j] >= 0:
                to = f"a{int(lab[j])}"
                break
        down[aid] = to
    home = {a["node"]: aid for aid, a in areas.items() if a["kind"] == "home"}
    return {"version": 1, "km": km, "ring_km": RING_KM, "block_km": BLOCK_KM, "areas": areas, "links": links, "down": down, "home": home}


def _nearest_node(L, sites, km):
    def f(cy, cx):
        if not sites:
            return None
        d = [np.hypot(cy - r, cx - c) for _, (r, c) in sites]
        return sites[int(np.argmin(d))][0]
    return f
