"""Named levels of practice and technology, and what a world can reach (D4-102).

A level is a set of knobs. `reach(w)` says what the world's people could build or do (materials on the land or in store, the trades
among them, beasts); `Level.within(reach)` lowers each knob to what is reachable, so "best" in a world with no oxen has no plough
and no ox mill, and the level says what it gave up.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

from cybertron2.engine.data import FITTINGS, RESOURCES, TECHNIQUES

COOK = ("raw", "boiled", "ground", "milled")          # fittings allowed for food: none; a hearth; + a hand mill; + mills and an oven
STORE = ("open", "house", "bins", "cellar", "granary")
TOOLS = ("bare", "crude", "copper")
COOK_FITTINGS = {"raw": set(), "boiled": {"hearth", "fire ring"}, "ground": {"hearth", "fire ring", "hand mill"},
                 "milled": {"hearth", "fire ring", "hand mill", "millstones", "water wheel", "oven", "cellar"}}


@dataclass(frozen=True)
class Level:
    name: str
    words: str
    fields: bool = True            # are the fields sown at all
    rotation: str = "once"         # "once": one crop a year, the rest fallow; "best": the best sequence the year allows
    broken: bool = False           # soil broken before sowing (hoe, or plough where reachable)
    weed: float = 0.0              # weeding, units a plot a crop
    manure: bool = False           # dung on the fields (from the herds)
    master: bool = False           # a master farmer's yield (D2-64)
    selection: bool = False        # seed selection: crops ripen 15% sooner (D2-65)
    winter_crop: bool = False      # rye over the winter, where there is rye to sow
    cook: str = "boiled"
    store: str = "house"
    tools: str = "crude"
    herds: str = "milk"            # "none", "milk", "milk+offtake"
    hunt: bool = True
    clear: bool = False            # clear meadow, pasture and scrub (and fell woods) to fields, as far as fuel allows
    labour_share: float = 1.0      # the share of people's work that may go to food
    gave_up: tuple = field(default=())

    def within(self, r: "Reach") -> "Level":
        """This level lowered to what the world can reach."""
        lost = []
        cook = self.cook
        while cook != "raw" and not _cook_ok(cook, r):
            lost.append(f"cook {cook}")
            cook = COOK[COOK.index(cook) - 1]
        store = self.store
        while store not in ("open", "house") and not r.fitting(store):
            lost.append(f"store {store}")
            store = STORE[STORE.index(store) - 1]
        tools = self.tools
        while tools != "bare" and not r.tool(tools):
            lost.append(f"{tools} tools")
            tools = TOOLS[TOOLS.index(tools) - 1]
        manure = self.manure and r.dung
        if self.manure and not manure:
            lost.append("manure (no herds)")
        winter = self.winter_crop and "rye" in r.seed
        if self.winter_crop and not winter:
            lost.append("rye (no seed)")
        herds = self.herds if r.cows else "none"
        selection = self.selection and r.knows("select seed")
        if self.selection and not selection:
            lost.append("seed selection (nobody knows it)")
        return replace(self, cook=cook, store=store, tools=tools, manure=manure, winter_crop=winter, herds=herds, selection=selection,
                       gave_up=tuple(self.gave_up) + tuple(lost))


def _cook_ok(cook, r) -> bool:
    if cook == "boiled":
        return r.fitting("hearth") or r.fitting("fire ring")
    if cook == "ground":
        return r.fitting("hand mill")
    if cook == "milled":
        return (r.fitting("millstones") and r.oxen >= 1) or r.fitting("water wheel")
    return True


LEVELS = {
    "bare": Level("bare", "wild food only, eaten raw as gathered: no fields, no fire, no store", fields=False, cook="raw",
                  store="open", tools="bare", herds="none", hunt=True),
    "standing": Level("standing", "the fields as they are: one crop a year sown on unbroken ground, not weeded; grain boiled; "
                                  "kept in a house", rotation="once", cook="boiled", store="house", tools="crude", herds="milk"),
    "worked": Level("worked", "the best crops and fallow the year allows; soil broken, weeded, manured where there are beasts; grain "
                              "ground to meal; kept in bins", rotation="best", broken=True, weed=8.0, manure=True, cook="ground",
                    store="bins", tools="crude", herds="milk+offtake"),
    "best": Level("best", "everything the world's techniques reach: ploughing, full weeding, master farmers, seed selection, rye over "
                          "the winter, milled flour and bread, a granary", rotation="best", broken=True, weed=16.0, manure=True,
                  master=True, selection=True, winter_crop=True, cook="milled", store="granary", tools="copper",
                  herds="milk+offtake"),
    "ceiling": Level("ceiling", "best, and meadow, pasture, scrub and woods cleared to fields as far as the fuel the hearths need "
                                "allows", rotation="best", broken=True, weed=16.0, manure=True, master=True, selection=True,
                     winter_crop=True, cook="milled", store="granary", tools="copper", herds="milk+offtake", clear=True),
}
ORDER = ("bare", "standing", "worked", "best", "ceiling")


@dataclass
class Reach:
    """What the world's people could build and do: materials, trades, beasts, seed, existing fittings."""
    goods: set
    trades: set               # the trades of the techniques someone knows or is aware of (TECHNIQUES trade)
    known: set                # techniques someone knows or is aware of (basic ones are always reachable)
    fittings_built: set
    oxen: int
    cows: int
    seed: set
    dung: bool
    systems: tuple = ()

    def fitting(self, f) -> bool:
        if f in self.fittings_built:
            return True
        d = FITTINGS.get(f) or {}
        if d.get("trade") and d["trade"] not in self.trades:
            return False
        if d.get("needs") and not self.fitting(d["needs"]):
            return False
        return all(m in self.goods for m in (d.get("materials") or {}))

    def tool(self, grade) -> bool:
        t = TECHNIQUES.get(f"{grade} tool") or {}
        if f"{grade} tool" in self.goods:
            return True
        if t.get("trade") and t["trade"] not in self.trades:
            return False
        if any(f not in self.fittings_built and not self.fitting(f) for f in (t.get("at") or {}).get("fittings", [])):
            return False
        return all(m in self.goods for m in (t.get("inputs") or {}))

    def trade(self, tr) -> bool:
        return tr is None or tr in self.trades

    def knows(self, tech) -> bool:
        from cybertron2.engine import systems as SY
        if not SY.on(TECHNIQUES.get(tech, {}), self.systems):
            return False
        return bool(TECHNIQUES.get(tech, {}).get("basic")) or tech in self.known


def reach(w) -> Reach:
    """Read what the world holds: goods in any store or hand, goods its land gives, trades, beasts, fittings already built."""
    goods = set()
    for c in w.s["containers"].values():
        goods |= {i for i, q in (c.get("goods") or {}).items() if q > 1e-9}
    for p in w.s["parcels"].values():
        res = p.get("res") or {}
        if p["cover"] == "forest" or res.get("wood"):
            goods.add("timber")
        if res.get("quarry") or p["cover"] == "rock" and res.get("quarry"):
            goods.add("stone")
        if res.get("seam"):
            goods |= {"copper ore", "copper"}
        if res.get("game"):
            goods.add("hide")
    from cybertron2.engine import systems as SY
    for t, d in TECHNIQUES.items():                                           # what the land here gives to gathering (any system on)
        if d.get("verb") != "gather" or not SY.on(d, SY.of(w)) or not isinstance(d.get("gives"), str):
            continue
        covers = (d.get("at") or {}).get("covers") or []
        dr = d.get("draws")
        if any(p["cover"] in covers and (dr not in RESOURCES or dr in (p.get("res") or {})) for p in w.s["parcels"].values()):
            goods.add(d["gives"])
    if "copper ore" in goods:
        goods.add("copper")
    herds = list(w.s["herds"].values())
    oxen = sum(int(h.get("oxen", 0) or 0) for h in herds)
    cows = sum(int(h.get("cows", 0) or 0) for h in herds)
    if herds:
        goods.add("hide")
    known = {t for n, k in (w.s.get("know") or {}).items() if (w.s["people"].get(n) or {}).get("alive", True)
             for t, r in (k or {}).items() if t in TECHNIQUES and r.get("level") in ("aware", "rough", "capable", "known")}
    trades = {TECHNIQUES[t].get("trade") for t in known if TECHNIQUES[t].get("trade")}
    built = {f for b in w.s["buildings"].values() for f, n in (b.get("fittings") or {}).items() if n}
    seed = {g for g in ("grain", "rye", "beans") if g in goods}
    from cybertron2.engine import farm as FM
    for p in w.s["parcels"].values():
        for _, _, c in FM.standing(p):
            seed.add({"grain": "grain", "winter grain": "rye", "legumes": "beans"}.get(c.get("crop"), "grain"))
    return Reach(goods=goods, trades=trades, known=known, fittings_built=built, oxen=oxen, cows=cows, seed=seed, dung=bool(herds),
                 systems=SY.of(w))
