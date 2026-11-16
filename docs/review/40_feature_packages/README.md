# 40: the engine as feature packages, its inventory (16 Nov 2026)

Session notes for [proposals/feature_packages.md](../../cybertron2/proposals/feature_packages.md) (WORK W-43). These files are a
read of every module of `cybertron2/engine/` as it stood on 16 Nov (main at 3c798181), made to find what a feature package would
have to register on a small core. Line numbers are of that commit. Nothing in the engine was changed.

| File | Modules read |
|---|---|
| [inventory_A.md](inventory_A.md) | world, here, data, schema, packs, tags, things, wear, modifiers, variants, clocks, capacity, needs: state tables, primitives, hooks, data tables, world build, `Here` and `Mind`, inverted imports |
| [inventory_B.md](inventory_B.md) | verbs, yields, outcomes, renewal, knowledge, lore, labour, buildings, layout: verbs, the technique pipeline, yield kinds, renewal rules, special cases |
| [inventory_C.md](inventory_C.md) | farm, herds, forests, climate, environment, night, needs, life: the night's exact order and its dependencies, needs, farming, herds as an entity kind, life |
| [inventory_D.md](inventory_D.md) | signs, perceive, prompt, view, views, memory, converse, chronicle: sign tables and producers, perception, the prompt's sections, memory |
| [inventory_E.md](inventory_E.md) | run, evening, fuse, settle, agreements, exchange, roads, generate (journal, branch, api skimmed): the day, the `today` record, social, roads, urgent calls, bugs |
