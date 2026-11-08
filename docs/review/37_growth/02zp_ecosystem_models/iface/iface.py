"""Interface levels between villages and the ecosystem (02zp part four). One lean ecology (hares, deer, boar with mast, wolves on deer)
on the generator's land, laid on five spatial structures; villages hunt by a policy, crops meet raids. Real rates; time on the year
clock with four seasons.

Structures (zones, each with an area, habitat per kind and neighbours with a coupling):
  grid(b)           a uniform grid of b-cell blocks (b=7: about 1 km)
  nested            250 m blocks within 2 km of a village, 1 km to 6 km, 5 km beyond
  graph(R)          per village: its own land, a ring out to R km; the rest in coarse wild regions (about 8 km); links by shared edge
A village reaches its own zones (weight 1) and those within 3 km (weight falling with distance). Footprint k_f multiplies what a
village's take removes; exposure k_e multiplies the raids and visits it meets.
"""
from __future__ import annotations

import numpy as np

KINDS = {   # r a year (best), K a km2 of habitat (real), habitat covers, food a head (real person-days)
    "hare": dict(r=1.0, K=25.0, hab={"pasture": 1.0, "field": 0.8, "meadow": 1.0, "heath": 0.5}, pd=2.0, move=0.05),
    "deer": dict(r=0.25, K=8.0, hab={"forest": 1.0, "scrub": 0.6, "heath": 0.5, "pasture": 0.2}, pd=45.0, move=0.15),
    "boar": dict(r=0.8, K=4.0, hab={"forest": 1.0, "scrub": 0.4}, pd=40.0, move=0.25),
    "wolf": dict(r=0.3, K=0.025, hab={"forest": 1.0, "heath": 0.6, "moor": 0.6, "scrub": 0.5}, pd=0.0, move=0.4),
}


class Zones:
    def __init__(self, label, cover, km, sites):
        """label: a zone id per cell (-1 sea); cover: the engine cover per cell."""
        self.km = km
        n = int(label.max()) + 1
        self.n = n
        cell_km2 = km * km
        self.area = np.bincount(label[label >= 0].ravel(), minlength=n) * cell_km2
        self.hab = {}
        for k, spec in KINDS.items():
            w = np.zeros(label.shape)
            for c, x in spec["hab"].items():
                w += (cover == c) * x
            self.hab[k] = np.bincount(label[label >= 0].ravel(), weights=w[label >= 0].ravel(), minlength=n) * cell_km2
        self.field = np.bincount(label[label >= 0].ravel(), weights=(cover == "field")[label >= 0].ravel() * cell_km2, minlength=n)
        self.wood = self.hab["boar"]
        # neighbours: shared boundary length between zones (in cells)
        a, b = label[:, :-1].ravel(), label[:, 1:].ravel()
        c_, d_ = label[:-1, :].ravel(), label[1:, :].ravel()
        pairs = np.concatenate([np.stack([a, b], 1), np.stack([c_, d_], 1)])
        pairs = pairs[(pairs[:, 0] != pairs[:, 1]) & (pairs >= 0).all(1)]
        key = np.minimum(pairs[:, 0], pairs[:, 1]) * n + np.maximum(pairs[:, 0], pairs[:, 1])
        u, cnt = np.unique(key, return_counts=True)
        self.edges = [(int(x // n), int(x % n), float(c) * km) for x, c in zip(u, cnt)]       # (i, j, shared edge km)
        # zone centres
        ys, xs = np.mgrid[0:label.shape[0], 0:label.shape[1]]
        m = label >= 0
        self.cy = np.bincount(label[m], weights=ys[m], minlength=n) / np.maximum(np.bincount(label[m], minlength=n), 1)
        self.cx = np.bincount(label[m], weights=xs[m], minlength=n) / np.maximum(np.bincount(label[m], minlength=n), 1)
        # each village's reach: its own zone(s) and zones whose centre is within 3 km, by distance
        self.reach = []
        for (r0, c0) in sites:
            d = np.hypot(self.cy - r0, self.cx - c0) * km
            own = label[r0, c0]
            w = np.where(d <= 3.0, np.exp(-d / 1.5), 0.0)
            w[own] = max(w[own], 1.0)
            self.reach.append(w)


def grid_labels(shape, b, sea):
    ny, nx = shape
    lab = (np.arange(ny)[:, None] // b) * ((nx + b - 1) // b) + (np.arange(nx)[None, :] // b)
    lab = np.where(sea, -1, lab)
    _, inv = np.unique(lab, return_inverse=True)
    out = inv.reshape(shape) - (1 if (lab < 0).any() else 0)
    return np.where(sea, -1, out)


def nested_labels(shape, sites, km, sea):
    ny, nx = shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    d = np.min([np.hypot(yy - r, xx - c) * km for r, c in sites], axis=0)
    fine = np.where(d <= 2.0, 2, np.where(d <= 6.0, 7, 33))           # 2 cells = 300 m; 7 = 1 km; 33 = 5 km
    lab = np.zeros(shape, dtype=np.int64); base = 0
    for b in (2, 7, 33):
        m = fine == b
        g = (yy // b) * ((nx + b - 1) // b) + (xx // b)
        lab = np.where(m, base + g, lab); base += int(g.max()) + 1
    lab = np.where(sea, -1, lab)
    _, inv = np.unique(lab, return_inverse=True)
    out = inv.reshape(shape) - (1 if (lab < 0).any() else 0)
    return np.where(sea, -1, out)


def graph_labels(shape, sites, km, sea, R):
    ny, nx = shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    ds = np.stack([np.hypot(yy - r, xx - c) * km for r, c in sites])
    near = ds.argmin(0); dmin = ds.min(0)
    region = (yy // 53) * ((nx + 52) // 53) + (xx // 53)              # about 8 km wild regions
    nv = len(sites)
    lab = np.where(dmin <= 0.45, near, np.where(dmin <= R, nv + near, 2 * nv + region))   # own land (~0.6 km2), ring, region
    lab = np.where(sea, -1, lab)
    _, inv = np.unique(lab, return_inverse=True)
    out = inv.reshape(shape) - (1 if (lab < 0).any() else 0)
    return np.where(sea, -1, out)


def run(Z, years, policy, k_f=1.0, k_e=1.0, seed=0, people=12, mast_p=0.25):
    """policy: {village index: hunting effort (0 none, 1 steady, 3 hard)} or a function of (year, season) to that dict.
    Returns per-year village records and regional totals."""
    rng = np.random.default_rng(seed)
    N = {k: Z.hab[k] * KINDS[k]["K"] * 0.8 for k in KINDS}
    nv = len(Z.reach)
    rec = {"village": [], "region": [], "local": []}
    edges = Z.edges
    mast_prev = 1.0
    for y in range(years):
        u = rng.random(); mast = 3.0 if u < mast_p else (0.2 if u > 0.75 else 1.0)
        hard = rng.random() < 0.15
        vy = [{"meat": 0.0, "crop_loss": 0.0, "stock_loss": 0.0, "units": 0.0} for _ in range(nv)]
        for s in range(4):
            pol = policy(y, s) if callable(policy) else policy
            # growth (spread over the seasons), boar with the mast, wolves on deer
            for k, sp in KINDS.items():
                K = Z.hab[k] * sp["K"] * (mast_prev ** 0.5 if k == "boar" else 1.0) + 1e-9
                r = sp["r"] / 4 * (1.0 if k != "boar" else (1.5 if mast_prev > 2 else (0.3 if mast_prev < 0.5 else 1.0)))
                N[k] = N[k] + r * N[k] * (1 - N[k] / K)
            kill = np.minimum(N["wolf"] * 25 / 4 * N["deer"] / (N["deer"] + 4 * Z.area + 1e-9), 0.5 * N["deer"])   # 25 deer a wolf a year
            N["deer"] = N["deer"] - kill
            N["wolf"] = N["wolf"] * np.exp(0.45 * (kill / np.maximum(N["wolf"] * 25 / 4, 1e-9)) / 4 - 0.25 / 4)
            # movement along shared edges toward room
            for k, sp in KINDS.items():
                dens = N[k] / np.maximum(Z.hab[k], 1e-9)
                flow = np.zeros(Z.n)
                for i, j, L in edges:
                    f = sp["move"] * L * (dens[i] - dens[j]) * 0.25 * min(Z.hab[k][i], Z.hab[k][j]) / max(Z.area[i] + Z.area[j], 1e-9)
                    flow[i] -= f; flow[j] += f
                N[k] = np.maximum(N[k] + flow, 0)
            # villages: hunting and raids
            for v in range(nv):
                w = Z.reach[v]
                effort = pol.get(v, 1.0)
                CAP = {"hare": 15.0, "deer": 1.2, "boar": 1.0}                    # heads a season a unit of effort can take (12 people)
                for k in ("hare", "deer", "boar"):
                    avail = w * N[k]
                    tot = float(avail.sum())
                    want = min(tot * min(0.9, 0.15 * effort), CAP[k] * effort)          # what their effort finds and can take
                    take = avail * (want / max(tot, 1e-9))
                    N[k] = np.maximum(N[k] - take * k_f, 0)
                    vy[v]["meat"] += float(take.sum()) * KINDS[k]["pd"]
                    vy[v]["units"] += float(take.sum()) * 0.5
                wsum = float((w * Z.hab["boar"]).sum()) + 1e-9
                boar_d = float((w * N["boar"]).sum()) / wsum / KINDS["boar"]["K"]    # boar near the fields, as a share of capacity
                wd = float((w * Z.hab["deer"]).sum()) + 1e-9
                deer_d = float((w * N["deer"]).sum()) / wd / KINDS["deer"]["K"]
                woodside = min(1.0, float((w * Z.wood).sum()) / 5.0)                   # how much wood lies by the fields
                if s in (1, 2):                                                # summer and autumn: crops standing
                    bust = 2.5 if (mast_prev > 2 and mast < 0.5) else 1.0
                    vy[v]["crop_loss"] += min(0.5, woodside * k_e * (0.02 * boar_d * bust + 0.01 * deer_d))   # share of the crop
                if s == 3:
                    wolves_near = float((w * N["wolf"]).sum())
                    vy[v]["stock_loss"] += min(3.0, wolves_near * k_e * (3.0 if hard else 1.0) * 4.0)   # beasts a winter
        mast_prev = mast
        rec["village"].append(vy)
        rec["region"].append({k: float(N[k].sum()) for k in KINDS})
        rec["local"].append([{k: float((Z.reach[v] * N[k]).sum()) for k in KINDS} for v in range(nv)])
    return rec
