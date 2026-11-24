# The map, first pass: the surveys' mechanisms placed in the target (W-112 step 3)

Session arch, 24 Nov 2026. Step 3 of [architecture_overhaul.md](../../cybertron2/proposals/architecture_overhaul.md): every
mechanism the patterns surveys list (W-110) placed in a home in [target.md](target.md), and every named branch and side table
tied to the property it becomes. Design only; nothing built. The full table is generated: [map_table.md](map_table.md), by
[map_build.py](map_build.py) over [map_extract.py](map_extract.py) (run from the repository root).

**How it was made, and how far to trust it.** `map_extract.py` reads the four surveys' mechanism tables: 395 rows (A 97, B 102,
C 126, D 70). Four of B's rows belong to C and D, and a few mechanisms appear in two surveys, so there are about 385 distinct
mechanisms. `map_build.py` places each row from the pattern label its survey gave it (`TOKEN`), and 36 rows by hand where the
label was missing or misleading (`OVERRIDE`, named in the script). It is a first pass. The grades come from the surveys, parsed
from their Fit column. D's "no pattern" rows (the mind's stores) parse as ungraded, so `M.mind`'s "needs work" undercounts: all
six of them need the new mechanism. Each row is checked again when its migration step is briefed (step 4).

## 1. Where the mechanisms land

| Layer | Home | Mechanisms | General today | Fitted | Needs work (named, text, words, silent) |
|---|---|---|---|---|---|
| core | registry form and load check | 14 | 7 | 0 | 7 |
| core | conditions | 13 | 6 | 1 | 6 |
| core | resolver | 14 | 2 | 0 | **11** |
| core | prompt frame, slots, reply schema | 15 | 4 | 0 | **11** |
| core | chokepoint, space, time, phases, journal | 9 | 6 | 0 | 3 |
| mechanism | **signs** (subject rows, act bundles, observer, known and seeded lines) | **57** | 14 | 3 | **40** |
| mechanism | **acts' effects** (yield kinds, costs, sites, readiness) | **35** | 7 | 0 | **28** |
| mechanism | stocks (renewal, habitat, takes, couplings, classes) | 40 | 15 | 10 | 15 |
| mechanism | lives and wear | 23 | 10 | 6 | 7 |
| mechanism | records with terms (agreements, offers, claims, offices, the book) | 23 | 15 | 2 | 6 |
| mechanism | pulses and hazards | 21 | 5 | 7 | 9 |
| mechanism | **set gear** | 16 | 1 | 2 | **13** |
| mechanism | familiarity | 14 | 2 | 2 | 10 |
| mechanism | parts and capacity; keeping; processes | 12; 12; 11 | 6; 4; 3 | 0; 2; 2 | 6; 6; 6 |
| mechanism | works; matching; the mind; draws | 9; 8; 6; 5 | 0; 5; 0; 4 | 2; 0; 0; 0 | 7; 3; 6 (see above); 1 |
| feature | the generator and its catalogue | 18 | 7 | 3 | 8 |
| feature | wild food web; network movement; climate; memory; cast; herds; bots | 3; 2; 5; 5; 2; 1; 2 | 1; 0; 3; 3; 0; 0; 1 | | 2; 0; 0; 2; 2; 1; 1 |

In layers: about **68 core**, about **290 shared mechanisms**, about **38 owned by features**.

## 2. What the map says about the target

1. **Features are thin today because their specifics live inside the mechanisms.** Only about 38 mechanisms sit in the feature layer.
   That is not because features are small. It is because water's, the wild layer's and farming's specifics are written into the
   general paths as named branches: set gear has 13 of 16 needing work, mostly `trap in water` and the named methods; the acts have
   28 of 35. So the migration's main move is **pulling a feature's specifics out of the shared mechanisms into that feature's rows
   and registered behaviours**, not moving modules into folders. Moving folders without that, as feature_packages.md planned,
   would carry the named branches into the new folders (its own stated weakness: "it does not make content into data by itself").
2. **Signs and acts are the two largest jobs** (57 and 35 mechanisms; 40 and 28 needing work). Both are what agents see and do, so
   both change the experiment's stimulus. They need prompt snapshots and the replay decision (Q-104) before they are touched.
   That supports target.md §5's order: the yield-kind registry first (cheap, byte-identical), the sign names and subjects with
   the keyed-draw decision.
3. **Set gear deserves its own place in target.md §5's queue.** The §5 table folds it under acts and stocks. The map shows it as
   the worst-fitting mechanism by share (13 of 16). Survey B §3 reads it as a placed body with parts, sampling a stock and wearing
   by lives, so it is built from three promoted mechanisms rather than as a fourth. It should come after acts' effects, parts and
   lives, and it is the natural acceptance test: **a new kind of water gear as one row** (A §6: today at least 9 places of 45).
4. **The resolver and the prompt are core work with high need** (11 of 14, 11 of 15). They are the interface faults World 0b met
   (L-189) and W-109's unfinished half (D §9: the reply schema, the parse's word lists, the core lines by index). They belong to
   the interface thread first. The target only asks that they be built as registries: referent kinds with aliases on rows, and
   prompt lines as named slots.
5. **What already holds** (general today): records with terms (15 of 23), stocks (15 of 40 general, 10 more fitted), lives (10 of
   23), matching (5 of 8), the climate, the chokepoint. These are promotions of something that mostly exists: a registry put
   round it, the copies merged.

## 3. The named branches and side tables, and the property each becomes

Each survey has already mapped its own branches to the row property they become. This pass does not redo that. It collects the
totals and points to the tables:

| Survey | Branches on names in function code | Should become a row property | Legitimately by name | Side tables keyed by names | Table |
|---|---|---|---|---|---|
| A, physics | 393 | about 250 | about 140 (the generator's catalogue, makers' pins, core defaults) | about 45 | A §3 |
| B, making | 345 | about 265 | about 80 (dispatch on yield kind, the core kind `set`, a table's own keys) | about 30 | B §2.2, §2.3 |
| C, people | 375 | about 150, besides the founders' 195 (system-owned text, conditions to be declared) and the bots' 29 (legitimate) | stages as LIFE's rows | 192 entries | C §2 |
| D, senses | 508 (259 in functions) | about 150 | about 40 (a sign bound to a state value) | 90 in module tables | D §3.2 |
| **All** | **about 1,600** | **about 800** | **about 300** | **about 350 entries** | |

The rest (about 500) are text or words that belong in rows' words fields (stages, numbers, fences, tiers), the founders' conditions,
or dispatches that the registries remove.

Two things follow for the guard (proposal step 5):
- **The baseline is about 1,600 sites.** The named-branch guard starts from them as a list that may only shrink. The legitimate
  ones (about 300) are marked in the list with their reason, so they do not count as debt.
- **The side tables are the cheapest large win.** About 350 entries are a property kept beside its rows instead of on them. Moving
  them onto the rows changes no behaviour, and the load check can then see them. That belongs in the first build's step 1
  (target.md §8).

## 4. Not done in this pass

- A row-by-row check of the placements. Each will be checked when its migration step is briefed.
- The estimate (step 4). It needs the map's counts set against today's engine: 36,293 lines in `engine/`, plus `wild/` and
  `landgen/` (7,917).
- The w109-interface branch's registry, which is not on `origin`; it is the nearest existing model of the registry form.

*Current as of 24 Nov 2026 (82f8b92c).*
