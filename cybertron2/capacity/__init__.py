"""Carrying capacity: how many people a world's land feeds, at named levels of practice and technology (D4-102).

The question is a ratio: food eaten in a year against food needed in a year (people x ration x days). Food eaten is what the land
yields net of seed, worth what its processing makes it worth (raw grain 0.2 of a meal, boiled 0.7, bread 1.3 a unit), less what
spoils between harvest and eating; it is capped by the work people can give it. Stores are a buffer, reported apart, with the days
to the first harvest the people can bring in themselves (the timing check that a ratio alone misses).

Every number is read from the engine's tables (ITEMS, CROPS, DECAY, FITTINGS, TECHNIQUES, PHYSICS) and the engine's own functions
(farm.soil_step, farm.weed_gain, farm.ground_mult, capacity.wood_flow): nothing here is a constant of its own, so when the engine's
numbers change, capacity follows.

Modules:
- levels.py    the named levels (bare, as it stands, worked, best, ceiling) as knobs, and what a world can reach (technology)
- food.py      what a good is worth eaten, by the fittings at hand (a search over the engine's food techniques), and how fast it spoils
- rotation.py  a field's year under a level: the best sequence of crops and fallow, its steady-state soil, yield and work
- sources.py   the registry of food sources; each turns a parcel (or herd) into flows with a daily profile and the work they take
- model.py     the year simulated (stores, spoilage, the lean season), people supported, the labour share, the buffer, a run's horizon
- space.py     by node, the whole region, and what a short node could draw from a neighbour over the road
- figures.py   SVG figures (bounds, sensitivity, the region and node maps), drawn with c2viz's layouts
- __main__.py  python -m cybertron2.capacity SPEC_OR_RUN ... --out DIR

To extend: a new food source is one function registered with @source in sources.py; a new food technique joins food.py's search by
being in TECHNIQUES (verb make, tag food); a new knob is a field on Level. tests/test_cybertron2_capacity.py fails when the engine
gains an edible good or a food technique that no source or method accounts for.
"""


def __getattr__(name):                     # lazy, so the submodules import without each other
    if name in ("analyse", "people_supported", "run_horizon"):
        from cybertron2.capacity import model
        return getattr(model, name)
    if name in ("LEVELS", "Level"):
        from cybertron2.capacity import levels
        return getattr(levels, name)
    raise AttributeError(name)
