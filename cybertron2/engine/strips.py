"""Flax below a whole plot: the strip (u3 §1.3; questions B35, default taken: up to a quarter of a plot; D2-264's flax close): the
feature unit of the strip crop (D2-244).

- **data:** a CROPS row with `strip` (the most of a plot it may take: flax 0.25) and `seed_kg` (kg of seed a plot); TECHNIQUES
  `pull flax` (work, kind `pull`) and `dig a strip` (work, kind `dig_strip`), in engine/data.py.
- **the record:** a holding's record (the parcel's own, or a share's) keeps `strips` = [a crop record of today's shape, one a strip
  crop], each with its own sowing, growth, area, base and left; `strip_dug`: the plots of a meadow or pasture holding whose turf is
  broken for a strip.
- **acts:** sowing a strip crop's seed of a strip's worth or less goes into a strip (farm._sow calls `sow`); above that, the crop is
  the holding's main crop, as grain is. `pull flax` pulls the strip's flax (straw, with seed rippled from it); `dig a strip` breaks
  up to a sixth of a plot a unit of a meadow or pasture plot the household holds, so a strip there takes no turf penalty.
- **process:** `night(w)`: each strip grows on the night as a crop does (farm.grow_night), rots past its window; when it is pulled
  the holding's soil steps by the strip's share of its plots.
Retting (a processing container, u4) and the spinning of retted flax are stage 3's and U4's: until then a strip's straw is kept.
"""
from __future__ import annotations

from cybertron2.engine.data import CROPS
from cybertron2.engine.here import Refused, show

PULL = {"plots": 0.05}           # plots pulled a unit (u3 §1.2: 15 to 25 person-days a hectare, a plot read as 0.1 ha)
DIG = {"plots": 1 / 6}           # plots of turf broken a unit for a strip (u3 §1.3)
SEED_BACK = 0.1                  # kg of seed rippled from each kg of straw pulled (u3 §1.2)


def strip_crops() -> list:
    return sorted(k for k, d in CROPS.items() if d.get("strip"))


def _rec(par, holder):
    from cybertron2.engine import farm as FM
    return FM.record(par, holder) or {}


def strips(par, holder) -> list:
    return list(_rec(par, holder).get("strips") or [])


def strip_of(par, holder, fam):
    return next((c for c in strips(par, holder) if c.get("crop") == fam), None)


def area_of(fam, kg) -> float:
    """Plots of ground a sowing of `kg` of a strip crop's seed takes."""
    return float(kg) / float(CROPS[fam]["seed_kg"])


def is_strip(fam, kg) -> bool:
    """A sowing of a strip's worth or less: a strip (u3 §1.3)."""
    return bool(CROPS.get(fam, {}).get("strip")) and area_of(fam, kg) <= float(CROPS[fam]["strip"]) + 1e-9


def sow(here, mind, tech, key, place_name, out, fam, a, f) -> tuple:
    """A strip sown on one's holding (u3 §1.3): its own crop record beside the main crop. Returns farm.act's (got, gives, word, thing)."""
    from cybertron2.engine import farm as FM, knowledge as KN
    from cybertron2.engine.verbs import _consume, _party, _src
    par = here.parcels()[key]
    seed_good = CROPS[fam]["seed"]
    targets = FM.sow_targets(here, key, a)
    extra = _src(here, _party(here, a["for"]) if a.get("for") else None, out)
    have = KN.available(here, seed_good, extra=extra)
    want = min(float(a.get("qty") or have), have)
    if want <= 1e-9:
        raise Refused(f"you have no {seed_good} to sow")
    held = [x for x in targets if FM.plots_of(par, x) > 0 and (x is not None or FM.whole(par))]   # None: the field held whole
    if not held:
        raise Refused(f"you hold no plots of {par['name']} to sow a strip on")
    h = held[0]
    if strip_of(par, h, fam):
        raise Refused(f"there is a strip of {fam} on {FM.the_part(FM.names_of(here), par, h)} already")
    room = float(CROPS[fam]["strip"])
    kg = round(min(want, room * float(CROPS[fam]["seed_kg"])), 3)
    area = area_of(fam, kg)
    _consume(here, {seed_good: kg}, extra=extra)
    rec = _rec(par, h)
    dug = min(area, float(rec.get("strip_dug") or 0.0))
    if dug > 0:
        FM._set(here, key, h, "strip_dug", round(float(rec.get("strip_dug") or 0.0) - dug, 4))
    eq = area * float(f["plot_seed"])
    turf = float(f["turf"]) if par["cover"] != "field" and dug < area - 1e-9 else 1.0
    g = FM.grow_days(here.year_days(), fam)
    c = {"kind": CROPS[fam]["names"][0], "crop": fam, "sown": here.day, "ripe_day": here.day + g, "window": int(f["window"]), "seed": eq,
         "area": round(area, 4), "area_left": round(area, 4), "broken": 0.0, "weeded": 0.0, "rot": 1.0, "failed": False,
         "hardy": CROPS[fam]["hardy"], "sower": here.name, "g": g, "progress": 0.0, "q": 0.0, "n": 0, "lying": True, "stand": 1.0,
         "wintered": False, "strip": True}
    c["base"] = round(FM.crop_base(f, eq, 0.0, float(rec.get("fertility", 1.0)), FM.ground_mult(here.p, par)) * float(CROPS[fam].get("yield", 1.0))
                      * turf, 4)
    c = FM.set_projection(c, here._w, par["node"], here.day, f)
    c["left"] = FM.crop_left(f, c)
    FM._set(here, key, h, "strips", strips(par, h) + [c])
    main = (rec.get("crop") or {}).get("kind")
    word = (f"You sowed {show(kg)} kg of {seed_good} in a strip of {place_name} (about {_share_words(area)} of a plot)"
            + (f", beside the {main}" if main else "") + ".")
    if turf < 1.0:
        word += " The seed lies on the turf among the grass: a strip dug first takes better (work dig a strip)."
    return 0.0, None, word, ("parcel", key)


def _share_words(area) -> str:
    for d, w in ((40, "a fortieth"), (20, "a twentieth"), (10, "a tenth"), (8, "an eighth"), (6, "a sixth"), (5, "a fifth"), (4, "a quarter")):
        if area <= 1.0 / d + 1e-9:
            return w
    return f"{area:.2f}"


def pull(here, mind, tech, key, place_name, out, m, a, f) -> tuple:
    """Pulling a ripe strip of flax by the root (u3 §1.2): up to PULL plots a unit; its straw, and seed rippled from it, to the puller.
    The holding's soil steps by the strip's share when it is all pulled."""
    from cybertron2.engine import farm as FM
    par = here.parcels()[key]
    fam = next(iter(strip_crops()), None)
    h, c = _ripe_strip(here, key, a, fam)
    c = dict(c)
    plots = min(float(c["area_left"]), float(PULL["plots"]) * m)
    got = round(float(c["left"]) * plots / max(1e-9, float(c["area_left"])), 2)
    c["area_left"] = round(float(c["area_left"]) - plots, 6)
    c["left"] = round(float(c["left"]) - got, 4)
    left = [x for x in strips(par, h) if x.get("crop") != fam]
    word = ""
    if c["area_left"] <= 1e-6:
        rec = _rec(par, h)
        share = float(c["area"]) / max(1.0, float(FM.plots_of(par, h)))
        fert = float(rec.get("fertility", 1.0))
        step = FM.soil_step(f, fert, fam, FM.base(par)) - fert
        FM._set(here, key, h, "fertility", round(fert + step * share, 4))
        FM._set(here, key, h, "strips", left)
        word = " The strip is pulled."
    else:
        FM._set(here, key, h, "strips", left + [c])
    seed = round(got * SEED_BACK, 2)
    if seed > 0:
        here.apply("create", dst=out, item=CROPS[fam]["seed"], qty=seed, why="pulled")
        word = f" You rippled {show(seed)} kg of {CROPS[fam]['seed']} from it." + word
    return got, CROPS[fam]["gives"], word, ("parcel", key)


def _ripe_strip(here, key, a, fam):
    from cybertron2.engine import farm as FM
    par = here.parcels()[key]
    for h in FM.own_records(here, key, a) + ([None] if None not in FM.own_records(here, key, a) else []):
        c = strip_of(par, h, fam)
        if c and c.get("progress", 0.0) >= 1.0 and c.get("area_left", 0) > 1e-6:
            return h, c
    c = next((strip_of(par, h, fam) for h in FM.own_records(here, key, a) if strip_of(par, h, fam)), None)
    if c:
        raise Refused(f"the {c['kind']} in {par['name']} is not ripe yet")
    raise Refused(f"there is no strip of {fam} of yours in {par['name']}")


def dig(here, mind, tech, key, place_name, m, a, f) -> tuple:
    """Breaking the turf of a meadow or pasture plot one's household holds for a strip (u3 §1.3): up to DIG plots a unit, to the
    largest strip a holding may have; the parcel stays meadow or pasture."""
    from cybertron2.engine import farm as FM
    par = here.parcels()[key]
    held = [x for x in FM.own_records(here, key, a) if FM.plots_of(par, x) > 0]
    if not held:
        raise Refused(f"you hold no plots of {par['name']}")
    h = held[0]
    most = max(float(CROPS[x]["strip"]) for x in strip_crops())
    rec = _rec(par, h)
    have = float(rec.get("strip_dug") or 0.0)
    if have >= most - 1e-9:
        raise Refused(f"a strip of {par['name']} is dug already, as large as a strip is")
    add = min(most - have, float(DIG["plots"]) * m)
    FM._set(here, key, h, "strip_dug", round(have + add, 4))
    return 0.0, None, f"You broke the turf of a strip of {place_name}, about {_share_words(have + add)} of a plot, ready to sow.", ("parcel", key)


def ready(here, tech, key, a=None) -> str:
    from cybertron2.engine import farm as FM
    from cybertron2.engine.data import TECHNIQUES
    y = TECHNIQUES[tech]["yield"]["kind"]
    par = here.parcels()[key]
    if y == "pull":
        try:
            _ripe_strip(here, key, a or {}, next(iter(strip_crops()), None))
        except Refused as e:
            return str(e)
        return ""
    if y == "dig_strip":
        if par["cover"] not in ("meadow", "pasture"):
            return f"a strip is dug on a meadow or pasture you hold; {par['name']} is {par['cover']}"
        if not any(FM.plots_of(par, x) > 0 for x in FM.own_records(here, key, a or {})):
            return f"you hold no plots of {par['name']}"
    return ""


def night(w, rec_) -> None:
    """Each strip grows on the night as a crop does (u3 §1.3): farm.grow_night; frost thins or kills a tender one; past its window it
    rots; a strip that has gone to nothing is gone."""
    from cybertron2.engine import farm as FM
    f = w.p["farming"]
    season = w.calendar()["season"]
    for pid in sorted(w.s["parcels"]):
        par = w.s["parcels"][pid]
        for hd, rec in FM.records(par):
            ss = rec.get("strips")
            if not ss:
                continue
            node = par["node"]
            new = []
            for c in ss:
                c = FM.started(dict(c), w.d)
                if c.get("progress", 0.0) < 1.0 and c["area_left"] > 1e-6:
                    c, what = FM.grow_night(c, season, w.cold(node), f)
                    if what == "ripe":
                        c["ripe_day"] = w.d + 1
                    elif what == "killed":
                        rec_["crops"].append((pid, "strip killed"))
                        continue
                elif w.d >= int(c["ripe_day"]) + int(c.get("window", f["window"])):
                    c["rot"] = round(c.get("rot", 1.0) * (1 - float(f["rot"])), 4)
                c["left"] = FM.crop_left(f, c)
                if c["area_left"] > 1e-6 and c["left"] > 0.05:
                    new.append(c)
            if new != ss:
                w.apply("set_share", node, parcel=pid, holder=hd, field="strips", value=new or None)


def words(par, holder, names=None) -> str:
    """'a strip of flax (about a fortieth of a plot), sown spring day 3' for a holding's line."""
    out = []
    for c in strips(par, holder):
        out.append(f"a strip of {c['kind']} (about {_share_words(float(c['area']))} of a plot)" + (", ripe" if c.get("progress", 0) >= 1 else ""))
    return "; ".join(out)
