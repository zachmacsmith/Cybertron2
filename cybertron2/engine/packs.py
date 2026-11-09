"""Packs: switchable bundles of data (D4-103).

A row of the data (a technique, an item, a resource) may carry `"pack": "<name>"`. A world turns a pack on with `packs: [...]` in
its file (an older file's `systems: [...]` is read the same way). Rows of a pack the world has not turned on do not exist for it: no
technique to resolve, no good to name, nothing listed to its people. Rows with no pack are always on. So a new pack leaves every
older world exactly as it was (replays stay exact), and an experiment's null arm is the same world with the pack off.

CURRENT is the packs of the world being worked: set when a world is built and whenever a view of it (Here, Mind) is made, so the
code that names goods and techniques (item_of, resolve, the prompt's lists) reads the world in hand.
"""
from __future__ import annotations

CURRENT: tuple = ()


def of(w) -> tuple:
    spec = getattr(w, "spec", None) or {}
    return tuple(spec.get("packs") or spec.get("systems") or ())


def use(w) -> tuple:
    global CURRENT
    CURRENT = of(w)
    return CURRENT


def on(row, packs=None) -> bool:
    """A row is on when its pack is (or it has none), and off when a pack named in its `off_with` is on: a row a newer pack
    replaces (the old generic game and its hunt, replaced by the wild layer's kinds: wild_layer.md, D2-199)."""
    live = CURRENT if packs is None else packs
    s = (row or {}).get("pack")
    if any(x in live for x in ((row or {}).get("off_with") or ())):
        return False
    return s is None or s in live


def items(packs=None) -> list:
    from cybertron2.engine.data import ITEMS
    return [i for i, d in ITEMS.items() if on(d, packs)]


def techniques(packs=None, verb=None) -> list:
    from cybertron2.engine.data import TECHNIQUES
    return [t for t, d in TECHNIQUES.items() if on(d, packs) and (verb is None or d.get("verb") == verb)]
