"""The river's gear (proposals/river_and_water.md §3b; D2-210, D2-213; W-69, 20 Nov): the weir in sections, and the gear sharing a run.

Unit seams (D2-244, feature_packages.md §9): pure functions over the state's records and WATER_WORKS; the engine (engine/wild.py,
engine/verbs.py) calls them, so the cut into feature packages can move this whole.
  - data: WATER_WORKS["weir"] (`position`, `material`, `footing`) and ["trap"]; a weir's `sections` record on its building;
  - verbs: none of its own (verbs._monument, _weir_part and _weir_mend cost a section by `cost`);
  - signs: none (signs read a weir's `sections` and `broke` as before);
  - processes: `share_run`, called by wild._runs_night for each village's stretch of river.

**A weir's sections.** A section's place in the weir decides what it takes and holds: the first (index 0) `position.first`, each
added one `position.added`, up to `most` added. Its material decides its wear and its cost: wattle or timber (`material`), and a stone
footing under it wears at `footing` wear. Any section may be built in either material, the first included; a wattle section is
upgraded to timber for the difference of the two materials' costs. A weir's `sections` is a list of {"m": material, "foot": bool,
"level": 5 to 0}; a material's name alone stands for a sound section of it at the building's level (an old world's list), and a weir
with no list is one wattle section at the building's level. Before 20 Nov the names stood for position (the first was always
wattle, the added ones timber), so an old list means what it did.

**Gear sharing a run.** Tonight's run at a village's stretch is taken by its gear: the weirs, a trap in a shut mill's race, and the
traps set in the water. Within a parcel there is no position between them, so they share the run passing at the same time: each
takes its share of what reaches the parcel, a share in proportion to what it would take alone (scaled down together when the shares
pass the whole run), and capped by its own hold. Between parcels the river decides: a run going down (the eels) passes the gear
upstream first, a run going up (salmon, lampreys) the gear downstream first (D2-210: weirs on a stretch take in turn from upstream,
for the run's way). A weir's or the race's share is its own (`weir_share`, `race`); a set trap's is the heads it met in the night
(wild._set_night: its draws on the run, against the run as it arrived) over the run's heads at the stretch.
"""
from __future__ import annotations

import math

MATERIALS = ("wattle", "timber")


def _W():
    from cybertron2.engine.data import WATER_WORKS
    return WATER_WORKS["weir"]


# ---------------------------------------------------------------------- a weir's sections
def normal(secs, level=5) -> list:
    """A weir's sections as records: a material's name alone (an old world's list) is a sound section of it at `level`."""
    out = []
    for x in secs or []:
        if isinstance(x, str):
            out.append({"m": x, "foot": False, "level": int(level)})
        else:
            out.append(dict(x))
    return out


def position(j) -> dict:
    """The row for the section at index j: the first, or an added one."""
    P = _W()["position"]
    return P["first"] if int(j) == 0 else P["added"]


def most_added() -> int:
    return int(_W()["position"]["added"]["most"])


def wear_of(sc) -> float:
    """A section's material rate of wear: its footing's if it stands on one, else its material's."""
    W = _W()
    return float(W["footing"]["wear"]) if sc.get("foot") else float(W["material"][sc["m"]]["wear"])


def share(secs, gap="shut") -> float:
    """What a weir takes of each run passing (D2-210): each section's share by its place and condition; x `open` with the gap open."""
    W = _W()
    x = sum(float(position(j)["share"]) * float(W["by_level"].get(int(sc["level"]), 0.0)) for j, sc in enumerate(secs))
    return x * (float(W["open"]) if gap == "open" else 1.0)


def hold(secs) -> float:
    """What a weir's traps hold a night, in kg (D2-210, D2-258): each section's by its place and condition."""
    W = _W()
    return sum(float(position(j)["hold"]) * float(W["by_level"].get(int(sc["level"]), 0.0)) for j, sc in enumerate(secs))


def _add(a, b, k=1.0) -> dict:
    out = dict(a)
    for i, q in b.items():
        out[i] = out.get(i, 0) + float(q) * k
    return out


def cost(j, material, foot=False) -> dict:
    """A section's build: {"materials": {...}, "units": n}: its material's, the first's with the weir's stakes and trap, a footing's
    added under it."""
    W = _W()
    mat = W["material"][material]
    mats, units = dict(mat["materials"]), float(mat["units"])
    if int(j) == 0:
        mats = _add(mats, W["position"]["first"]["materials"])
        units += float(W["position"]["first"]["units"])
    if foot:
        mats = _add(mats, W["footing"]["materials"])
        units += float(W["footing"]["units"])
    return {"materials": mats, "units": units}


def upgrade_cost(frm="wattle", to="timber") -> dict:
    """Rebuilding a section in a better material: the difference of the two materials' costs (D2-210), none below nothing."""
    M = _W()["material"]
    mats = {i: max(0.0, float(q) - float(M[frm]["materials"].get(i, 0))) for i, q in M[to]["materials"].items()}
    return {"materials": {i: q for i, q in mats.items() if q > 0}, "units": max(0.0, float(M[to]["units"]) - float(M[frm]["units"]))}


# ---------------------------------------------------------------------- gear sharing a run
def _kinds_of(g, pulses, d) -> list:
    sh = g["share"]
    if d not in g.get("dirs", ("down", "up")):
        return []
    ks = sorted({p["k"] for p in pulses if p["dir"] == d})
    return [k for k in ks if (sh.get(k, 0.0) if isinstance(sh, dict) else sh) > 0]


def _share_of(g, k) -> float:
    sh = g["share"]
    return float(sh.get(k, 0.0)) if isinstance(sh, dict) else float(sh)


def _order(gear, d) -> list:
    """The parcels the run meets in turn: going down, the upstream first (`pos`: steps up the water); going up, the downstream
    first. [(parcel, [gear there])]."""
    by = {}
    for g in gear:
        by.setdefault(g["parcel"], []).append(g)
    key = (lambda q: (-by[q][0]["pos"], str(q))) if d == "down" else (lambda q: (by[q][0]["pos"], str(q)))
    return [(q, sorted(by[q], key=lambda g: str(g["id"]))) for q in sorted(by, key=key)]


def _pass(pulses, gear, f, whole) -> dict:
    """One pass of the run past the gear, with each gear's share cut by f[id]: {id: {kind: heads}}, the pulses thinned (on copies when
    not `whole`). `whole`: heads taken whole, each gear's held to its room in kg."""
    left = {g["id"]: (None if g.get("room") is None else max(0.0, float(g["room"]))) for g in gear}
    out = {g["id"]: {} for g in gear}
    for d in ("down", "up"):
        ps = [p for p in pulses if p["dir"] == d and float(p["n"]) > 1e-9]
        if not ps:
            continue
        for _, here in _order(gear, d):
            for k in sorted({p["k"] for p in ps}):
                pk = [p for p in ps if p["k"] == k]
                n = sum(float(p["n"]) for p in pk)
                takers = [g for g in here if k in _kinds_of(g, ps, d)]
                if n <= 1e-9 or not takers:
                    continue
                nominal = sum(_share_of(g, k) for g in takers)
                scale = 1.0 if nominal <= 1.0 else 1.0 / nominal          # shares past the whole run: scaled down together
                took = 0.0
                for g in takers:
                    x = f[g["id"]] * _share_of(g, k) * scale * n
                    if whole:
                        q = math.floor(x + 0.5) if n >= 1.0 - 1e-9 else 0
                        q = min(q, int(math.floor(n - took + 1e-9)))
                        kg = float((g.get("worth") or {}).get(k, 0.0))
                        if left[g["id"]] is not None and kg > 0:
                            q = min(q, int(math.floor(left[g["id"]] / kg + 1e-9)))
                        q = max(0, q)
                        if left[g["id"]] is not None:
                            left[g["id"]] -= q * kg
                        x = float(q)
                    if x > 0:
                        out[g["id"]][k] = out[g["id"]].get(k, 0.0) + x
                        took += x
                if took > 0:                                              # thinned in proportion, the largest pulse its share
                    for p in pk:
                        p["n"] = round(max(0.0, float(p["n"]) - took * float(p["n"]) / n), 4)
    return out


def share_run(pulses, gear) -> dict:
    """The run at one stretch tonight shared by its gear (the rule above). `pulses`: the pulses there today (thinned in place).
    `gear`: [{"id", "parcel", "pos": steps up the water, "share": a share of every kind or {kind: share}, "dirs": the run's ways it
    takes, "room": kg it can still hold or None, "worth": {kind: kg a head}}]. Returns {id: {kind: heads}} of whole heads, none
    holding more than its room. Each gear's share is first cut, the same for every kind it takes, until what it would take fits its
    room (as a weir's hold cut its take kind by kind in proportion before); what it does not take passes on down the river."""
    import copy
    gear = [g for g in gear if g.get("room") is None or float(g["room"]) > 1e-9]
    if not gear or not pulses:
        return {}
    f = {g["id"]: 1.0 for g in gear}
    for _ in range(12):
        got = _pass(copy.deepcopy(pulses), gear, f, whole=False)
        moved = False
        for g in gear:
            if g.get("room") is None:
                continue
            kg = sum(q * float((g.get("worth") or {}).get(k, 0.0)) for k, q in got[g["id"]].items())
            if kg > float(g["room"]) + 1e-6:
                f[g["id"]] *= float(g["room"]) / kg
                moved = True
        if not moved:
            break
    got = _pass(pulses, gear, f, whole=True)
    return {gid: {k: int(round(q)) for k, q in sorted(x.items()) if q > 0} for gid, x in sorted(got.items(), key=lambda t: str(t[0])) if x}
