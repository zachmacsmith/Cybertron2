---
id: Q-49
kind: ask
state: open
updated: "2026-11-22"
---

# Engine bugs found by the package inventory (Q-49)

*open · 37.4*

## The question
(16 Nov), for 37.4: (a) `branch.STEPS` has no "evening": `rewind`, `fork` and `continue` raise ValueError on any `evening:` world (checked in Python); (b) `labour.close_day` runs between two steps, so its changes are journaled under a step already committed; (c) `data.py` names `roads.CHALLENGES`, which does not exist; (d) `knowledge.ready` lines 185-209 cannot be reached; (e) `farm.frost_kills` (before [[D4-106 Can apart from works|D4-106]]) is still used by `capacity/cal.py`; (f) `farm._f_default` and `forests.fuel_order` read the global PHYSICS, ignoring a world's physics; (g) young beasts never grow into cows, oxen or bulls; (h) `engine/chronicle.py` is imported nowhere

**Where:** docs/review/40_feature_packages/inventory_B.md, _C.md §10, _E.md §10


## Linked
- bears on: [[W-43 The engine as feature packages|The engine as feature packages (W-43)]]
- bears on: [[W-67 Extending the wildlife economy|Extending the wildlife economy (W-67)]]


## Mentioned by
- [[W-43 The engine as feature packages|The engine as feature packages (W-43)]]
- [[The engine as a small core and feature packages design specification|The engine as a small core and feature packages: design specification]]
- *and 1 index or audit notes*
