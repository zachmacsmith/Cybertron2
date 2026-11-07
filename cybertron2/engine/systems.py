"""Systems as switchable packs of data (D4-103).

A row of the data (a technique, an item, a resource) may carry `"system": "<name>"`. A world turns a system on with `systems: [...]`
in its file. Rows of a system the world has not turned on do not exist for it: no technique to resolve, no good to name, nothing
listed to its people. Rows with no system are always on. So a new system leaves every older world exactly as it was (replays stay
exact), and an experiment's null arm is the same world with the system off.

CURRENT is the systems of the world being worked: set when a world is built and whenever a view of it (Here, Mind) is made, so the
code that names goods and techniques (item_of, resolve, the prompt's lists) reads the world in hand.
"""
from __future__ import annotations

CURRENT: tuple = ()


def of(w) -> tuple:
    return tuple(((getattr(w, "spec", None) or {}).get("systems")) or ())


def use(w) -> tuple:
    global CURRENT
    CURRENT = of(w)
    return CURRENT


def on(row, systems=None) -> bool:
    s = (row or {}).get("system")
    return s is None or s in (CURRENT if systems is None else systems)


def items(systems=None) -> list:
    from cybertron2.engine.data import ITEMS
    return [i for i, d in ITEMS.items() if on(d, systems)]


def techniques(systems=None, verb=None) -> list:
    from cybertron2.engine.data import TECHNIQUES
    return [t for t, d in TECHNIQUES.items() if on(d, systems) and (verb is None or d.get("verb") == verb)]
