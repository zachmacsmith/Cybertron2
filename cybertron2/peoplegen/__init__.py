"""The backward people build (generation_redesign.md §4.3, §4.5, §6; W-39b prototype, W-107 bridge): a world's present population
pinned (a list or a mix of household forms), its past built backward to fit it as a graph of keyed decisions, weighted by a forward
demographic model, repaired by conflict-directed backjumping and never rejected.

A feature unit (D2-244): opt-in with `population: {build: backward}` (generate.build dispatches here); no verbs, signs or processes
of its own; the world it writes is generate.spec_from_tree's.

    world.py       the people stage for a world: households from its lines and houses, distances from its roads, the present,
                   the tree in generate.py's form (the entry point: world.build)
    genealogy.py   the decisions: settlement, foundings, pairings, parents, ages, deaths, the children not living now
    solver.py      the decision graph: keyed weighted orders, a trail, conflict-directed backjumping, soft pins, refusal by pin
    demog.py       the forward model's tables and the backward weights measured against it (calibrate; OPEN L-108)
    present.py     household forms, and a mix drawn into an explicit present
    keyed.py       keyed draws (D2-70)
    write.py       names, the history, a world written in generate's form (the prototype's writer; world.py reuses its history)
    forward.py, stats.py, evaluate.py, examples.py
                   the prototype's forward reference, statistics, evaluation and readable examples
                   (python -m cybertron2.peoplegen.evaluate; results and report in proto/peoplegen/)
"""
