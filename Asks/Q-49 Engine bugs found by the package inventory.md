---
id: Q-49
kind: ask
state: open
owner: "37.4"
updated: "2026-11-20"
tags: [ask, open]
---
# Engine bugs found by the package inventory

- **state**: open
- **owner**: 37.4
- **where**: docs/review/40_feature_packages/inventory_B.md, _C.md §10, _E.md §10

## Text
**Engine bugs found by the package inventory** (16 Nov), for 37.4: (a) `branch.STEPS` has no "evening": `rewind`, `fork` and `continue` raise ValueError on any `evening:` world (checked in Python); (b) `labour.close_day` runs between two steps, so its changes are journaled under a step already committed; (c) `data.py` names `roads.CHALLENGES`, which does not exist; (d) `knowledge.ready` lines 185-209 cannot be reached; (e) `farm.frost_kills` (before [[D4-106 Can apart from works; crops grow by the season; a crop shows it|D4-106]]) is still used by `capacity/cal.py`; (f) `farm._f_default` and `forests.fuel_order` read the global PHYSICS, ignoring a world's physics; (g) young beasts never grow into cows, oxen or bulls; (h) `engine/chronicle.py` is imported nowhere

## Mentioned by
- [[W-43 The engine as feature packages (Zach, 16 Nov) a dig into every co|W-43: The engine as feature packages (Zach, 16 Nov): a dig into every core o]]
- [[feature_packages The engine as a small core and feature packages desig|The engine as a small core and feature packages: design spec]]
