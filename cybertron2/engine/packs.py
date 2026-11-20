"""Packs: switchable bundles of data (D4-103).

A row of the data (a technique, an item, a resource) may carry `"pack": "<name>"`. A world turns a pack on with `packs: [...]` in
its file (an older file's `systems: [...]` is read the same way). Rows of a pack the world has not turned on do not exist for it: no
technique to resolve, no good to name, nothing listed to its people. Rows with no pack are always on. So a new pack leaves every
older world exactly as it was (replays stay exact), and an experiment's null arm is the same world with the pack off.

CURRENT is the packs of the world being worked: set when a world is built and whenever a view of it (Here, Mind) is made, so the
code that names goods and techniques (item_of, resolve, the prompt's lists) reads the world in hand.

Packs on by default (W-69; OPEN O-3): the packs in DEFAULT_ON (farming) are on in every world unless it lists them in
`packs_off: [...]`. A world's packs tuple then carries "-<name>" for each such pack switched off, so every reader that already
passes the tuple about (a Mind's packs, the capacity model, the generator's gates) sees the switch, and a tuple without the mark
(every world before W-69, and the empty tuple of code that runs before any world is built) has them on, exactly as before. A row
may name several packs (`"pack": ["wild", "farming"]`): it is on when all of them are.
"""
from __future__ import annotations

CURRENT: tuple = ()
DEFAULT_ON = ("farming",)


def of(w) -> tuple:
    spec = getattr(w, "spec", None) or {}
    off = tuple(spec.get("packs_off") or ())
    bad = [p for p in off if p not in DEFAULT_ON]
    if bad:
        raise ValueError(f"packs_off names {bad}: only a pack on by default ({', '.join(DEFAULT_ON)}) is switched off; "
                         "any other is off unless the world lists it in packs")
    live = tuple(spec.get("packs") or spec.get("systems") or ())
    return live + tuple(f"-{p}" for p in DEFAULT_ON if p in off) if off else live


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
    if s is None:
        return True
    return all((f"-{x}" not in live) if x in DEFAULT_ON else (x in live) for x in ((s,) if isinstance(s, str) else s))


def items(packs=None) -> list:
    from cybertron2.engine.data import ITEMS
    return [i for i, d in ITEMS.items() if on(d, packs)]


def techniques(packs=None, verb=None) -> list:
    from cybertron2.engine.data import TECHNIQUES
    return [t for t, d in TECHNIQUES.items() if on(d, packs) and (verb is None or d.get("verb") == verb)]
