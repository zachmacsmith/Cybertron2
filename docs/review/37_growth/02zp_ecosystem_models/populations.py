"""M3: wild populations on 1 km patches of a generated land, coupled to the woods (M2's browsing result) and to people.

Kinds (densities a km2; first values from the European literature, see the note §M3):
- red deer: browse in woods and their edges; r 0.25 a year; food-limited ~12 a km2 of wood without predators;
- wild boar: mast-driven: litters after a mast year, losses in a bust; up to ~6 a km2 of oak and beech wood;
- hare: open grass and arable; r ~1.0; ~30 a km2 of open land;
- wolf: individuals over a range of ~15 km radius; kills up to ~25 deer-equivalents a wolf a year (Holling II, half at 2 a km2);
  numerical response; a territorial ceiling of ~3 a 100 km2; switches to stock when wild prey runs short;
- the wood: canopy share per patch; old trees die ~0.8% a year and are replaced only where browsing lets seedlings through
  (M2: about 8 deer a km2 stops recruitment; thorny shrubs shelter some).
People: villages at the generator's sites; hunting within 8 km by a policy; a bounty on wolves; felling.
"""
from __future__ import annotations

import numpy as np

P = {   # calibrate
    "deer": {"r": 0.25, "K_wood": 12.0, "K_edge_open": 3.0, "move": 0.10, "meat_kg": 55, "kill_eq": 1.0},
    "boar": {"r_mast": 0.9, "r_normal": 0.25, "r_bust": -0.35, "K_mast": 6.0, "move": 0.20, "meat_kg": 50, "kill_eq": 0.8},
    "hare": {"r": 1.0, "K_open": 30.0, "move": 0.05, "meat_kg": 2.5},
    "wolf": {"kmax": 25.0, "half": 4.0, "conv": 0.45, "m": 0.25, "cap_100": 3.0, "radius": 15, "switch": 0.35},
    "wood": {"die": 0.008, "recruit": 0.05, "browse_stop": 10.0, "nurse": 0.25, "s_need": 0.3},
    "mast": {"p_mast": 0.25, "p_bust": 0.25},           # an oak region: a heavy crop about one year in four (calibrate)
    "people": {"hunt_km": 8, "q": 0.02, "price": 1.0, "cost": 0.6, "effort_rate": 5.0},
}


def box(x, r):
    p = np.pad(x, r, mode="edge")
    c = np.pad(np.cumsum(np.cumsum(p, 0), 1), ((1, 0), (1, 0)))
    n = 2 * r + 1
    return (c[n:, n:] - c[:-n, n:] - c[n:, :-n] + c[:-n, :-n]) / (n * n)


def patches(d, wood_cells, block=7):
    """Aggregate 150 m cells into ~1 km patches: wood share, open share, mast share (oak and beech woods), water."""
    h = d["h"]
    ny, nx = h.shape[0] // block, h.shape[1] // block
    def agg(a):
        a = a[: ny * block, : nx * block].astype(float)
        return a.reshape(ny, block, nx, block).mean((1, 3))
    land = ~d["sea"] & ~d["lake"] & (d["eco"] != "water")
    mastwood = np.isin(d["eco"], ["oak-ash wood", "beech wood", "upland oak wood"])
    sites = [(int(r) // block, int(c) // block) for r, c in d["sites"]] if len(d["sites"]) else []
    return {"wood": agg(wood_cells & land), "open": agg(land & ~wood_cells), "mast": agg(mastwood & land), "land": agg(land),
            "sites": sites, "shape": (ny, nx), "km": float(d["km"]) * block}


def dist_to_sites(pt):
    ny, nx = pt["shape"]
    yy, xx = np.mgrid[0:ny, 0:nx]
    if not pt["sites"]:
        return np.full((ny, nx), 99.0)
    return np.min([np.hypot(yy - r, xx - c) * pt["km"] for r, c in pt["sites"]], axis=0)


def disperse(N, K, m):
    """A share m moves to the 4 neighbours, weighted by their room (K - N)+, toward the ideal free distribution."""
    room = np.clip(K - N, 0, None) + 1e-6
    out = np.zeros_like(N)
    mov = m * N
    stay = N - mov
    tot = np.zeros_like(N)
    nbrs = []
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rn = np.roll(room, (dy, dx), (0, 1))
        nbrs.append((dy, dx, rn)); tot += rn
    for dy, dx, rn in nbrs:
        share = rn / tot
        out += np.roll(mov * share, (-dy, -dx), (0, 1))
    return stay + out


class World:
    def __init__(self, pt, seed=0, wolves=True):
        self.pt = pt
        self.rng = np.random.default_rng(seed)
        self.W = pt["wood"].copy()                        # canopy share per patch
        self.W0 = pt["wood"].copy()
        self.dsite = dist_to_sites(pt)
        self.D = self.K_deer() * 0.6
        self.B = self.K_boar(1.0) * 0.5
        self.H = self.K_hare() * 0.6
        self.wild = (self.dsite > 6.0) * pt["land"]       # where wolves may den: far from villages
        self.L = (0.02 * self.W * self.wild) if wolves else np.zeros(pt["shape"])
        self.E = np.zeros(pt["shape"])                     # hunting effort (open access)
        self.year = 0
        self.log = []

    def K_deer(self):
        edge = np.clip(box(self.W, 1) - self.W, 0, 1)    # open land beside wood
        return P["deer"]["K_wood"] * self.W + P["deer"]["K_edge_open"] * np.minimum(self.pt["open"], edge * 3)

    def K_boar(self, mastf):
        return P["boar"]["K_mast"] * self.pt["mast"] * (self.W / np.maximum(self.W0, 1e-6)).clip(0, 1) * mastf

    def K_hare(self):
        return P["hare"]["K_open"] * self.pt["open"]

    def step(self, policy):
        pw, pd = P["wolf"], P["people"]
        u = self.rng.random()
        mast = "mast" if u < P["mast"]["p_mast"] else ("bust" if u > 1 - P["mast"]["p_bust"] else "normal")
        mastf = {"mast": 1.6, "normal": 1.0, "bust": 0.5}[mast]
        # felling (people)
        fell = policy.get("fell", lambda w: 0.0)(self)
        self.W = np.clip(self.W - fell, 0, 1)
        Kd, Kb, Kh = self.K_deer(), self.K_boar(mastf), self.K_hare()
        # wolves: a range-wide kill rate on deer and boar
        r = pw["radius"]
        prey = box(self.D * P["deer"]["kill_eq"] + self.B * P["boar"]["kill_eq"], r)          # deer-equivalents a km2 in range
        kill = pw["kmax"] * prey / (pw["half"] + prey)                                    # a wolf a year
        Lr = box(self.L, r)
        # predation removes prey in proportion to the wolves in range and the prey here
        pred_frac = np.clip(Lr * kill / np.maximum(prey, 1e-6), 0, 0.6)
        dpred = pred_frac * self.D * P["deer"]["kill_eq"]
        bpred = pred_frac * self.B * P["boar"]["kill_eq"]
        short = np.clip(pw["kmax"] * 0.7 - kill, 0, None)                                 # what a wolf lacks
        stock_kills = self.L * short * pw["switch"] * (self.dsite < 8)                    # taken from herds near villages
        stock_kills = stock_kills + self.L * short * pw["switch"] * 0.3 * (self.dsite >= 8)
        # people's hunting
        near = self.dsite <= pd["hunt_km"]
        mode = policy.get("hunt", "light")
        if mode == "none":
            hd = np.zeros_like(self.D)
        elif mode == "light":
            hd = 0.05 * self.D * near
        elif mode == "regulated":                         # take half the growth while above half capacity
            hd = np.where(self.D > 0.5 * Kd, 0.5 * P["deer"]["r"] * self.D * (1 - self.D / np.maximum(Kd, 1e-6)), 0) * near
            hd = np.clip(hd, 0, None)
        elif mode == "open":                              # effort follows profit (Gordon-Schaefer)
            catch_rate = pd["q"] * self.D
            self.E = np.clip(self.E + pd["effort_rate"] * (pd["price"] * catch_rate - pd["cost"] * pd["q"]) * near, 0, 30) * near
            hd = np.clip(self.E * pd["q"] * self.D, 0, 0.8 * self.D)
        hb = (0.1 if mode != "none" else 0.0) * self.B * near
        bounty = policy.get("bounty", 0.0)
        hl = bounty * self.L
        # growth
        D = self.D + P["deer"]["r"] * self.D * (1 - self.D / np.maximum(Kd, 1e-6)) - dpred - hd
        rb = {"mast": P["boar"]["r_mast"], "normal": P["boar"]["r_normal"], "bust": P["boar"]["r_bust"]}[mast]
        B = self.B + rb * self.B * (1 - self.B / np.maximum(Kb, 1e-6)) * (1 if rb > 0 else 1) - bpred - hb
        B = np.where(rb < 0, self.B * (1 + rb) - bpred - hb, B)
        H = self.H + P["hare"]["r"] * self.H * (1 - self.H / np.maximum(Kh, 1e-6)) - 0.1 * self.H * near
        cap = pw["cap_100"] / 100.0 * self.wild
        gL = pw["conv"] * kill / pw["kmax"] - pw["m"]
        L = self.L + gL * self.L * (1 - box(self.L, r) / np.maximum(box(cap, r), 1e-9)) - hl
        L = np.where(box(self.L, r) > box(cap, r), self.L * 0.9, L) if self.L.sum() > 0 else L
        # the wood: replacement where browsing lets it through
        pw_ = P["wood"]
        shelter = np.clip(1 - D / pw_["browse_stop"], 0, 1) + pw_["nurse"] * np.clip(D / pw_["browse_stop"], 0, 1) * 0.3
        sh_ = np.clip(shelter, 0, 1)
        regrow = pw_["recruit"] * sh_ * np.clip(self.W0 - self.W, 0, None)                 # back into felled or lost ground
        die = pw_["die"] * self.W * (1 - np.clip(sh_ / pw_["s_need"], 0, 1))              # old trees' gaps not refilled
        self.W = np.clip(self.W + regrow - die, 0, 1)
        # movement and the edge
        D = disperse(np.clip(D, 0, None), Kd, P["deer"]["move"])
        B = disperse(np.clip(B, 0, None), Kb, P["boar"]["move"])
        H = disperse(np.clip(H, 0, None), Kh, P["hare"]["move"])
        for A, K_, f in ((D, Kd, 0.5), (B, Kb, 0.4), (H, Kh, 0.5)):        # the map's edge: exchange with land beyond
            A[0, :] = 0.8 * A[0, :] + 0.2 * f * K_[0, :]; A[-1, :] = 0.8 * A[-1, :] + 0.2 * f * K_[-1, :]
            A[:, 0] = 0.8 * A[:, 0] + 0.2 * f * K_[:, 0]; A[:, -1] = 0.8 * A[:, -1] + 0.2 * f * K_[:, -1]
        self.D, self.B, self.H, self.L = D, B, H, np.clip(L, 0, None)
        # crop damage by boar near villages: higher after a mast year when numbers are up and the woods are bare
        damage = (self.B * (self.dsite < 3) * (1.5 if mast == "bust" else 0.5)).sum()
        self.year += 1
        woodm = self.pt["wood"] > 0.3
        nearw = (self.dsite <= P["people"]["hunt_km"]) & woodm
        farw = (self.dsite > 15) & woodm
        rec = {"year": self.year, "mast": mast,
               "deer_near": float((self.D * nearw).sum() / max((self.W * nearw).sum(), 1e-9)),
               "deer_far": float((self.D * farw).sum() / max((self.W * farw).sum(), 1e-9)), "deer_wood": float((self.D * woodm).sum() / max((self.W * woodm).sum(), 1e-9)),
               "deer": float(self.D.sum()), "boar": float(self.B.sum()), "hare": float(self.H.sum()), "wolves": float(self.L.sum()),
               "kill_rate": float((kill * self.L).sum() / max(self.L.sum(), 1e-9)), "stock_kills": float(stock_kills.sum()),
               "people_deer": float(hd.sum()), "wood": float(self.W.sum()), "boar_damage": float(damage),
               "meat_kg_people": float(hd.sum() * P["deer"]["meat_kg"] + hb.sum() * P["boar"]["meat_kg"] + (0.1 * self.H * near).sum() * P["hare"]["meat_kg"])}
        self.log.append(rec)
        return rec
