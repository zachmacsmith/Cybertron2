"""Per-world switches that turn a wild food source off (W-69; OPEN O-3, accepted 20 Nov; the nutrition worlds of
proposals/subsistence_worlds.md, D2-256): clean isolation, a village that lives only off the river's runs, say, with no game and no
gathering. Farming is switched off as a pack (`packs_off: [farming]`, engine/packs.py); the wild's sources are switched here, in the
world's `wild:` table:

- `kinds_off: [...]`: classes (CLASSES below, or a kind's diet class in KINDS: herb, omni, gran, carn) and/or names of wild kinds,
  wild plant kinds (wild/plants.py) and sites (kinds.SITES). A kind off is in the food web with no land that suits it: it starts at
  none, no migrant arrives, nothing drifts in from beyond, so it has no stock, no group, no legend, no sign and nothing to take; a
  run of it does not run. A plant kind off is never placed on a parcel (class `plants`: none is, and the older generic `plants`
  stock is not stocked either); a site off is never placed. Class `game` also leaves the older generic `game` stock unstocked.
- `runs_off: true`, or a list of the kinds that run (kinds.RUNS): those runs never start, in the history or in the run.
- `resident_fish: false`: no resident fish for people: the parcels' `fish` stock is not stocked (no angling or fishing by hand
  outside a run), and the fish kinds (class `fish`) are taken only from a run passing (the food web keeps their numbers, which make
  the runs).

A world that sets none of these is as it was. Every name is checked: a switch naming nothing known is an error, not a no-op.
"""
from __future__ import annotations

from cybertron2.wild import kinds as WK, plants as PL

# the classes a world may switch off by name (W-69): each a list of kinds, plant kinds and sites
CLASSES = {
    "game": ["red deer", "roe deer", "wild boar", "brown hare", "lodge"],          # the beasts hunted for meat and hide; the beaver
    "fowl": ["woodpigeon", "wildfowl", "heronry", "rookery"],                      # birds taken for the pot, and the nesting colonies
    "fish": ["eel", "salmon", "lamprey"],
    "predators": ["wolf", "brown bear", "fox", "stoat", "otter", "owls"],
    "vermin": ["rats", "voles and mice"],
    "scavengers": ["raven"],
    "plants": sorted(PL.PLANTS),
}
DIET = sorted({k["cls"] for k in WK.KINDS.values()})                              # herb, omni, gran, carn: the kinds' own classes


def _wild(spec) -> dict:
    return (spec or {}).get("wild") or {}


def _named(spec) -> set:
    out = set()
    for x in _wild(spec).get("kinds_off") or ():
        x = str(x)
        if x in CLASSES:
            out |= set(CLASSES[x])
        elif x in DIET:
            out |= {k for k, d in WK.KINDS.items() if d["cls"] == x}
        elif x in WK.KINDS or x in PL.PLANTS or x in WK.SITES:
            out.add(x)
        else:
            raise ValueError(f"wild.kinds_off names {x!r}: not a class ({', '.join(list(CLASSES) + DIET)}), a wild kind, a plant kind "
                             "or a site")
    return out


def kinds_off(spec) -> frozenset:
    """The wild kinds (kinds.KINDS) a world switches off."""
    return frozenset(k for k in _named(spec) if k in WK.KINDS)


def plants_off(spec) -> frozenset:
    return frozenset(k for k in _named(spec) if k in PL.PLANTS)


def sites_off(spec) -> frozenset:
    return frozenset(k for k in _named(spec) if k in WK.SITES)


def runs_off(spec) -> frozenset:
    """The kinds whose runs do not run: those `runs_off` names (all, for true) and every kind switched off."""
    r = _wild(spec).get("runs_off")
    names = set(WK.RUNS) if r is True else set(r or ())
    bad = sorted(names - set(WK.RUNS))
    if bad:
        raise ValueError(f"wild.runs_off names {bad}: the kinds that run are {sorted(WK.RUNS)}")
    return frozenset(names | (kinds_off(spec) & set(WK.RUNS)))


def resident_fish(spec) -> bool:
    return _wild(spec).get("resident_fish", True) is not False


def resident(spec, kind) -> float:
    """What of a kind's own numbers people can take (1, or 0 for a fish kind where resident fish are off: only a run's)."""
    return 0.0 if kind in CLASSES["fish"] and not resident_fish(spec) else 1.0


def res_on(spec, key) -> bool:
    """Whether a parcel's stock `key` is stocked at a world's making: the generic `plants` and `game` stocks with their classes, a
    plant kind, and the resident `fish`."""
    if key == "fish":
        return resident_fish(spec)
    if not _wild(spec).get("kinds_off"):
        return True
    off = _named(spec)
    if key == "plants":
        return not set(CLASSES["plants"]) <= off
    if key == "game":
        return not {"red deer", "roe deer", "wild boar", "brown hare"} <= off
    return key not in off
