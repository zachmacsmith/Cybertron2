# 02zy: test worlds for the wild build briefs 1 and 2 (9 Nov)

Zach (9 Nov) asked for test worlds for the building session (37.4) to run after it finishes brief 2
(proposals/wild_raiders_and_works.md), exploring and testing the new mechanics. They complement the briefs' unit tests: each world
puts one mechanic into a whole village, with arms that differ in one thing only, so its effect can be read against a control.

**Cost.** The 20 test arms are dry: scripted bots, no model calls, a minute or two each and no money. Only the two live worlds call models, about $10 each (19 agents, 8 days): D2-207 allows one after brief 2's gate; the second needs Zach's go.

**The worlds are made by a script** on branch `ecology`: `python3 cybertron2/specs/make_wild_tests.py` writes 22 worlds (20 dry arms and 2 live worlds) to
`cybertron2/specs/wild_tests/` (generated, not committed: about 2.4 MB). Every world is the generated village of live run 6
(`wild_probe6.json`: Meadcombe and Brookford, East Wood between Middle Field and East Field, Brookford Water, 19 people, 6
households, 6 herds, a hen flock in each house). Named people do **scripted acts** (the world's `script`, done first each day, in
order); everyone else is a scripted bot. Each world's docstring in the script says what it tests and what to expect.

**How to run** (dry, no model calls), from the worktree of the branch being tested:

```
python3 cybertron2/specs/make_wild_tests.py
python3 -c "import sys; sys.path.insert(0,'.'); from cybertron2.engine import run as R; R.run('cybertron2/specs/wild_tests/<world>.json', '<out dir outside the repo>', days=<the world's days>, bots=True, seed=<7, 8 or 9>, workers=4)"
```

Run every arm on seeds 7, 8 and 9 (T8 on 7 and 9: seed 8 seeds no rookery). The worlds use brief 1's method names (`guard the field`,
`shut`, `snare`, `trap in water`, `net`, `stalk`, `pest work`, `gather young`) and brief 2's fittings (`cat`, `owl hole`), so they
run as tests only once both are built. Before then, the scripted acts are refused (checked on today's `ecology`: a two-day run of
T2 runs cleanly and refuses `shut`).

**Reading them.** Read each arm against its control, never as absolute numbers: scripted bots feed themselves poorly (six people
missed a meal on day 2 of the smoke run), so the village's food is lower than in a live run. What to read (from the run's
checkpoints and journal; the builder knows the paths): the wild traces per parcel (`state.wild.traces`: kind, what: edge, raid,
tried, turned, watched; scare; by whom), the night's raid results per group, crop and store levels per parcel and building, hens per
house, herd positions and straying, set things and their catches, the loads by parcel, the ecology's counts by area, takes by method
and kind, familiarity records, and each person's system text and refusals.

## The worlds

| World | Arms | Season, days | Scripted | What passes |
|---|---|---|---|---|
| **T1 displacement** | `none`; `watch_middle`; `watch_both` | spring, 8 | Thomasin guards Middle Field nightly; in `watch_both`, Osric guards East Field too | with only Middle watched, East Field loses more than in `none` (deer and the pigeon flock turned at Middle go to East, the same night); with both watched, both lose less than in `none`; traces show "turned" at Middle and "raid" at East on the same nights |
| **T2 the fox's lapse probe** | `all_shut`; `one_lax`; `none_shut` | spring, 8 | the heads of the Holt, Wood and Carter houses shut their houses each evening (the Carters do not in `one_lax`; nobody in `none_shut`) | in `one_lax` the Carters lose most hens, and the Holts and Woods are tried more often than in `all_shut`; after feeding at a house the fox tries it first; `all_shut` loses least |
| **T3 doors and gaps** | `wattle`; `stone`; `damaged` | spring, 8 | all three houses shut each evening | the fox does not get into a shut sound house; the stoat gets into shut wattle houses and not stone ones; the damaged Holt house lets the fox in though shut; rats and mice get into all |
| **T4 set works** | `checked`; `robbed`; `unchecked` | autumn, 8 | Thomasin sets snares on Meadcombe Common on days 1, 3, 5 and takes from them the next day (not in `unchecked`); in `robbed`, Osric takes from the Common on day 4; Everard empties and resets eel traps in Brookford Water daily | snares catch with nobody present and the catch waits in the snare; Osric sometimes finds and takes it, seen as using what another holds; unchecked catches spoil; a snare ends after its life; eel traps take more on eel nights; nothing is caught by a snare on a parcel no kind with runs uses |
| **T5 stores, the cat, the owl** | `bare`; `kept` | late summer into autumn, 16 | none | through the harvest, each kept store (Wood House granary, Carter House cat, the Holt byre's owl hole) loses less to rats and mice than in `bare`; in `bare` a cat settles by itself at a store with mice in some seeds (D2-206); an owl takes the hole only where nobody works in the byre at night |
| **T6 summer** | `open`; `herded` | summer, 8 | in `herded`, Lettice herds the Holt cattle on Cow Close daily | unwatched boar loss of corn about 3 to 10% of need (brief 2's calibration); on hot still days the Holt herd (Cow Close: no water, no wood beside it) breaks into East Field and the Leaze herds (Hazel Copse beside them) do not; herded, it does not; read across all three seeds, since hot still days depend on the weather |
| **T7 methods and familiarity** | `as_seeded`; `taught` | spring, 8 | Petronel stalks in East Wood looking for deer, Denise snares on the Leaze, Alys nets on Brookford Water, daily; in `taught`, Denise teaches Petronel to snare on day 1 | takes by method follow brief 1's generated tables; Petronel's familiarity with red and roe deer rises and her take with it; Brookford's households know `net` and `trap in water` and Meadcombe's do not (until taught); no system text lists a kind or a tool multiplier; no refusal lists the catalogue |
| **T8 moles, grubs, markers** | `left`; `worked` | autumn into winter, 16 (seeds 7, 9) | in `worked`, Gilbert does pest work on Leven Meadow every other day and Jordan takes the young rooks at Middle Wood on days 1 to 4 | Leven Meadow's mole load rises when left and falls when worked; parcels within the rookery's reach carry fewer grubs in `left` than in `worked`; marker signs naming a sowing window reach people with family lore |
| **Live 1: spring** (`live_spring_seed7`) | none | spring, 8 | none (LLM agents) | run 6's world, season, seed and cast, unchanged, read against run 6: deer and the pigeon flock at the young corn, the fox's tries, the stoat, set snares, shut doors, the cat, the new kinds' signs |
| **Live 2: late summer** (`live_late_summer_seed7`) | none | late summer into autumn, 8 | none (LLM agents) | boar at the ripening corn, cattle gadding on hot still days, the eel run, the harvest drawing rats into the stores; in both: what people do with the new methods, a raider moving to the neighbour's field, and whether anyone acts on a neighbour's loss (never forced) |

## Notes for the builder

- Meadcombe's two fields are worked in shares, not held by one household each, so T1 reads losses per field, not per household.
  T2 and T3 measure the actors' own houses by design.
- If a seed gives a world without the kind a test needs (no stoat near Meadcombe, no deer in East Wood), say so in the build log
  and use the next seed; the land, not the test, decides what lives there.
- `EEL_GOOD` at the top of the script is the eel trap's catch: `meat` (37.4: the eel's taken goods, 0.1 a lift).
- The live runs need the live backend as for runs 5 and 6 (`LLM_BACKEND=claude_code`, `bots=False`, `workers=12`, about $10); its
  outputs stay outside the repository.

## History
- 9 Nov: written by 37.2 at Zach's request, with `cybertron2/specs/make_wild_tests.py` on branch `ecology`; the worlds load on
  today's `ecology`, and a two-day dry run of T2 runs cleanly.
- 9 Nov: two live worlds in place of one (Zach wanted one or two LLM worlds); the cost of the dry arms made plain (none).
