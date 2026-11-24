---
id: docs/review/37_growth/02zzzm_patterns/A_physics.md
kind: note
updated: "2026-11-24"
---
# Survey A: the world's physics against the patterns (W-110)

*note · `docs/review/37_growth/02zzzm_patterns/A_physics.md`*

> **Mechanisms: 97** in the area (table §2), by fit: **rows 37, fitted 22, named 33, text 2, words 1, silent 2**. Of the 33 named, 13 came in the wave or were made named by it (the water, the willow, placed gear's night, the wrecks, the river's signs, the gate check's makings). The general part is rea


Session 37.2, 24 Nov 2026, survey agent A. Brief: [brief.md](brief.md), area A: `engine/world.py`, `data.py`, `renewal.py`,
`waters.py`, `wild.py`, `cybertron2/wild/` (all), `climate.py`, `environment.py`, `forests.py`, `capacity.py`, `cybertron2/landgen/`
(all), `generate.py`. Read from the code on `main` at 6b609f48 (line numbers are there); the wave's baseline is f728a3b7 (23 Nov
07:17, so "the wave" here is the [[W-97 Build stage 1, the basis in code|W-97]] to [[W-104 Build the after-runs list from live run 1|W-104]] builds of 23 Nov). No engine file was edited and nothing was run but three counting
scripts beside this file:

- `a_named.py`: every branch on a named thing in the area's code (an AST walk: `==`, `!=`, `in` against a string literal or a
  tuple of them that names a row; a registry subscripted by a literal name; a dict literal keyed by row names inside a function; a
  module-level tuple of row names used in a function). `--list` prints each hit. The categories are the registries' own keys
  (ITEMS, TECHNIQUES, FITTINGS, COVERS, RESOURCES, the wild kinds, foods, runs, loads, diseases, plants, crops, forest kinds,
  ecosystems, terrains) and the water types; door states, a ref's kind, a stock's S/K/r fields, a herd's roles and the seasons and
  weather labels are left out. It undercounts (a name held in a variable, a name in a docstring-driven branch) and overcounts a
  little (a name that is both a cover and a habitat feature); the per-file counts below were read through by hand.
- `a_wave.py`: which of those hits were written in the wave (`git blame f728a3b7..HEAD`).
- `a_dated.py`: the hits by the date their line was last written, against the lines standing from each period (the trend, §8).

The history needed the full clone: the checkout was shallow (from 13 Nov) and was unshallowed with `git fetch --unshallow` (2,223
commits) before §8 was written.

Grades used for fit (the brief's): **rows** general over rows; **fitted** general with fitted constants; **named** a special case by
name; **text** hand-written text; **words** a word-list parse; **silent** a silent skip.

## Summary

**Mechanisms: 97** in the area (table §2), by fit: **rows 37, fitted 22, named 33, text 2, words 1, silent 2**. Of the 33 named,
13 came in the wave or were made named by it (the water, the willow, placed gear's night, the wrecks, the river's signs, the gate
check's makings). The general part is real and large: the renewal registry, the food web over the kinds' rows, the take tables
generated from traits, loads and sites as rows, the climate over its own tables, the condition vocabulary, the runs over any kind
with a RUNS row.

**Branches on named things in function code: 393** sites by the script (compare 309, registry lookups by a literal 46, dicts of
names in functions 22, module tuples of names used in functions 16), **87 of them written in the wave**. By file: `landgen/write.py`
55, `landgen/settle.py` 57, `engine/wild.py` 70, `landgen/ecology.py` 33, `wild/river.py` 19, `landgen/economy.py` 19, `wild/water.py`
15, `wild/ecology.py` 15, `landgen/gates.py` 14, `landgen/names.py` 13, `engine/forests.py` 11, `landgen/roads.py` 11,
`landgen/macro.py` 10, the rest 51. By the category named: covers 167, goods 54, techniques 52, water types 28, terrains 26,
resources 21, wild kinds 21, building parts 9, fittings 5, forest kinds 5, ecosystems 4. About 140 of the 393 are legitimately by name
(the generator's own catalogue: which terrain becomes which ecosystem and cover, the household seeds a maker pins, a core default);
about 250 should become a property of a row (§3). Beside them stand **about 45 side tables**: module-level dicts or tuples that hold
one property of a category's rows keyed by the rows' names, away from the rows (covers 16, the wild kinds 18 of which 5 are folded
into the rows at load by `kinds.rows()`, water types 7 with no row at all, techniques 6).

**What does not fit** (§4): the hypothesis's set has no place for eight things this area does, each with a pattern it would need:
(1) **habitat**: where a stock lives and its K, seeded today by nine different functions in three places (generator, world build,
makers); (2) **couplings**: one population or stock acting on another (eats, floods, harms, feeds, grazes off, robs), interpreted by
six separate readers; (3) **coupled populations**: the food web is not a set of independent S, K, r stocks; (4) **movement along a
network**: the runs down and up the river, the wild kinds between areas, the ranging packs, the storms; (5) **driven layers and the
conditions derived from their memory**: frost (two definitions), hard frost, frozen nights in a row, snow lying, heavy rain since,
a hard winter, rain after dry, the spate, the flow, the ice, written in four modules; (6) **type transitions**: forest to scrub, a dam
up and down, ice open to over, a site gone and back: the parcel's and the place's analogue of a process; (7) **places that group
places**: a water body sharing one stock record over its parcels, by aliasing Python objects; the wild areas; the river's stretches;
(8) **analyses that re-derive the physics**: two capacity models, the economic check and the gate check, each with its own numbers
or named crafts.

**Verdict for area A:** the set is **too few and partly wrongly cut**, though its centre is right. Pattern 1 (typed rows) holds in
principle and fails in practice by **transposition**: a category's properties live in column tables keyed by its rows' names (the
covers' 16; the water types' 7, with no row), so "the row" is assembled nowhere and checked nowhere (there is no load-time check of
any registry in the area, §5). Pattern 2 (behaviour on properties) is where the wave regressed: named-branch density in the engine
and wild code rose from about 0.7 to 1.2 per 100 lines (23 Oct to 14 Nov) to 3.4 to 3.9 (15 to 24 Nov), §8. Pattern 3a (stocks) is
cut too narrow (no habitat, no couplings, no clock field) and lumps the food web with independent stocks; 3b (pulses) needs a shared
condition vocabulary to be a pattern at all; 3c (processes) should be one "a thing of one kind becomes another under conditions"
pattern for lots, parcels, ice and sites alike; 3d (set gear) fits, and the code is closest to it, but its hazards are by name. Pattern
4 (one resolver) does not exist in the area: seven alias and class tables. Pattern 5 (generated worlds entire) fails for open-water
fish (generality.md §2) and is structurally unreachable while habitat has no single home.

**The restructuring** (§6): about 3,000 to 4,500 lines rewritten and 1,500 moved in the area, about 8 to 14 builder-days, most of it
inside feature_packages.md §9 phase 2 (wild as a package) and phase 5 (populations in one form, layers first-class); the risk is in
the calibrated takes (the hunt, the sets, the runs), which must stay byte-identical on golden journals. What it saves: a new water type
today touches at least 8 places, a new kind of water gear at least 9 (counted in §6); after it, one row each.

**In [[D2-354 The architecture is a healthy balance, not a strict one|D2-354]]'s terms** (§9): a general primitive should own stocks and their renewal, habitat and seeding, takes, couplings, hazards
and transitions, and the condition vocabulary; the wild food web, the runs' network and the climate legitimately own their dynamics
(P3's "a process with its own dynamics"), and should keep their specifics inside their own rows and modules; the extension points
the primitives lacked are named, and the history shows which features went ad hoc because they had to (the shallows and willow
rules, which could not get their context or change K through the renewal registry) and which went ad hoc though they need not have
(water types as column tables, set gear's ice by name the same day edge techniques got an `ice` property).

## 1. The area's taxonomy (Zach's addition 1)

### 1.1 Categories and kinds of row

| Category (feature_packages §2) | Kinds in the area, and where their rows are |
|---|---|
| **Space** | node, parcel (`world.py:120-164`; its cover is its kind), road with terrain and stretches (`world.py:168-177`); the wild layer's areas (home, ring, far: `wild/areas.py:27-133`); water bodies (lake, reach, brook, pool: `wild/areas.py:135-181`, held by `engine/waters.py`); river stretches (`v:<node>`, `wild/runs.py:48-147`); the generator's 150 m cells (`landgen/physical.py`) |
| **Types (rows)** | COVERS 12 (`data.py:226`); RESOURCES 42 (`data.py:245`: 15 stocks, the wild kinds and plants folded in at `data.py:270-275`); FORESTS kinds 4 (`data.py:279`); CLIMATE eras, types, storms (`data.py:1001`); WEATHER 6 labels, SPELLS (`data.py:984-1000`); ENV (`data.py:1049`); WATER_WORKS weir, trap, mill (`data.py:461`); the wild KINDS 18, FOOD about 20, RUNS 3, LOADS 6, DISEASES 4, SITES, REGIMES, LEGENDS, LEADERS (`wild/kinds.py`); PLANTS and LAYERS (`wild/plants.py:16-69`); METHODS and SETS (`wild/methods.py:44-118`); the generator's TERRAINS, ECOSYSTEMS, SYSTEMS, CONFIGS (`landgen/vocab.py:73`, `landgen/ecology.py:23`, `landgen/macro.py:42`, `vocab.py:137`); **water types 6 (brook, pool, fen, river, big river, lake), which have no table: only columns** (`wild/water.py:21-30`) |
| **Layers** | the weather (driven: `climate.py`); snow lying, the ice, the river's flow (derived, never stored: `environment.py:86`, `water.py:116`, `runs.py:282`); the food web's soil bucket, mast and load levels (in `s["wild"]["state"]`); parcel stocks (coupled) |
| **Populations** | parcel stocks `{S, K, r}`; the wild kinds' densities by area (`ecology.py`); the runs as pulses on stretches (`runs.py:207-316`); sites as sized colonies (`wild.py:712-736`); a body's one fish record (`waters.py:24-61`) |
| **Bodies** | storms (in the climate's cache, not in state: `climate.py:209-217`); wild groups near people and legends (`s["wild"]["groups"]`, `wild.py:1947`, `:1193`); a weir's own traps (`wild.py:3195-3208`); hens as goods (`wild.py:125-130`) |

### 1.2 The kinds of property rows carry, or code reads off them

| Group | Properties (examples, with where they are) |
|---|---|
| **Quantities** | `S`, `K` and `spec_unit` (`data.py:245-266`); `size` of a parcel; a kind's `mass`, `ref`, `terr` (`kinds.py:23-31`); `cap`, `each`, `most` of a site (`kinds.py:476`); a trap's `hold` 10 kg and a weir section's (`data.py:461-478`); SHALLOWS K by water type (`water.py:21`); WILLOW K fen and bank (`willow.py:16`); PER_UNIT stocks by cover (`landgen/vocab.py:111`); a run's `cap_km`, `seed_km` (`kinds.py:885-893`) |
| **Rates and clocks** | `r` (a night, unless the rule says; the woods' and the shallows' on the year clock: `renewal.py:20-21`, `water.py:22`); a kind's `b`, `m` a year; FOOD `grow` by season; growth shares by season (CROPS, SHALLOWS r, plants' `seasons`); windows `{season index: (first, last)}` (RUNS, SITES, WHEN); half-lives (CARRION, WARY: `kinds.py:830-837`); `persist`, `hold` of the climate's chains. **No row declares its clock**: it is in the rule's code or a comment ([[D2-273 Three clocks, each system on one|D2-273]]'s year clock is applied by hand per rule) |
| **Conditions** | thresholds: `scrub_below` 0.4 (`data.py:292`), `felled.below` (ENV), `snow_below`, `gale`, `heavy_mm` (CLIMATE); frost as a low under 0 (`climate.py:358-360`) and hard frost as a low under -3 with a day under 3 (`wild.py:1315-1317`, `ecology.py:241`); ICE nights in a row by water type (`water.py:24-25`); a run's cue `rain_after_dry`, `spate` (`kinds.py:885-893`); `if` rows in WHEN's vocabulary (`wild.py:1395-1466`); `at.covers` of a technique; a plant's `needs: wet | coast` (`plants.py:108-111`) |
| **Capabilities** | `renewal` (a rule's name), `response`; the traits `runs`, `flies`, `swims`, `social`, `home`, `mover` (`kinds.py:856-871`); `climbs`, `gap` (BODY, `kinds.py:810`); `shy`, `fidelity`, `hibernate`, `migrant`, `litters`; a site's `dam`, `home`; a technique's `ice: bank | edge` (`data.py`, the rows `angle` and `fish by hand`), `set`, `gear`, `run_gear`; an item's `vermin`, `heat`, `seen`; a plant's `coppice`, `fertile` |
| **Links to other rows** | a kind's `diet` (foods and kinds) and `hab` (features); `taken.goods` (kind to items, `kinds.py:639`); a site's `eats {res, covers}` and `harm {crops}`; a load's `harm_res`, `harm`, `feeds`, `site_eats` (`kinds.py:675`); a technique's `draws` (a resource), `yield.takes` (kinds), `at` (covers); a plant's `item`; a wood's `kind` (a FORESTS row); a parcel's `ecosystem`; CLEARED (terrain to ecosystem, `landgen/ecology.py:49`); STORE_KIND, LOAD_READ (`kinds.py:818`, `:732`) |
| **Words** | RESOURCES `low` and `high`; COVERS `words` and `ambient`; WEATHER `words`; a kind's `uses`, `damage`; sign rows `R(read, sense, own, ages, text, ...)` (`kinds.py:204-258`); FAT, WARY, HUNGER words (`kinds.py:605-607`); the generator's per-cover words (`landgen/names.py:74-101`) |

### 1.3 Families of mechanisms that could be one general mechanism each

| Family | Members today (file:line) | What they share | What a general version would read |
|---|---|---|---|
| **F1 Stock renewal** | fast, threshold (`night.py:620-628` via `renewal.py:35-46`); periodic (`renewal.py:47-64`); seasonal (`:82-92`); shallows (`water.py:105-112`); willow (`willow.py:50-64`); slow, young, dead (`forests.py:49-67`, called by name at `forests.py:80-89`) | a logistic step toward K at r, scaled by the season, stopped by a condition (ice, winter), with a floor refill or a yearly reset | a rule row: logistic or step-to-target, the clock (night or year), a season table, the conditions that stop or slow it (iced, grazed, winter), what it changes (S, or S and K), a year factor `f` |
| **F2 Habitat and seeding** | grass on grazing covers (`world.py:134-139`); forest stocks (`forests.py:18-46`); the generator's stocks (`landgen/write.py:108-128`); wild plants' niche (`plants.py:96-133`, `wild.py:476-496`); the shallows (`water.py:79-102`); willow (`willow.py:23-46`); sites' candidates (`wild.py:697-736`); a body's fish (`waters.py:24-50`, from the makers' records) | for each parcel: its cover, its land (river, wet, position, sea distance), its ecosystem and its neighbours decide whether a stock is there and its K a unit of size | a `habitat` field on the resource row: covers with weights, beside (covers or water), land conditions, ecosystem weights, K a unit of size (by water type where it is water), seeded once, by one function, at the generator or the world's build |
| **F3 Takes from a population** | the parcel draw with its response (`world.py:698-711`, `renewal.py:172-180`); the hunt (`wild.py:2398-2655`); the set's night (`wild.py:975-1131`); a run taken by hand (`wild.py:3491-3535`); a site's take (`wild.py:865-905`); a run shared by gear (`runs.py:256-280`); the gill net's open-water draw (`wild.py:1098-1109`) | meetings at a rate (density x ground x detect x effort), each taken at a chance (skill x (1 - flee) x familiarity), capped by room, the heads drawn out of the count | one take primitive: λ, p, room, draw-out and return (feature_packages §2.3), reading the kind's `taken` row and the method's `set` and `yield` rows |
| **F4 Gear's night** | set gear (`wild.py:975-1131`); the snare untended (`:929-972`); the weir's traps and the race (`:3240-3290`); otters robbing (`:3384-3428`); flow and thaw wrecks (`:3309-3366`); idle under ice (`:1016-1021`) | a placed thing that each night samples a stock or a run, holds up to its capacity, and suffers hazards (a flow, the thaw, a robber, a scavenger, an escape), and wears | a gear row: what it samples, `in_water`, `hold` kg, a list of hazards `{when, rate, takes: catch | pieces}`, wear (feature_packages §2's body with condition) |
| **F5 Hazards on conditions** | a gale throws trees (`forests.py:90-96`); weir wear by flow (`wild.py:3142-3169`); trap wreck by flow (`data.py:476`, `wild.py:3309-3346`); fen wreck, thaw wreck (`water.py:167-189`); a great freeze (`wild.py:1213-1240`); a site crashes after a hard winter (`wild.py:795-800`); outbreaks (`wild.py:68-83`); the mast fails on flower frost (`ecology.py:242-245`); a snare's catch scavenged (`wild.py:929-972`) | a chance or a Poisson rate a night from declared conditions, applied to a target | hazard rows `{when: condition, target: kind or stock, rate, effect}`: pattern 3b, which needs F6 |
| **F6 Conditions derived from the weather's memory** | frost (`world.py:391-402`, `climate.py:358`); hard frost and frozen nights in a row (`wild.py:1315-1325`); snow lying (`environment.py:85-97`); heavy rain since (`:99-106`); a hard winter, rain after dry, tomorrow (`wild.py:1426-1446`); the spate cue (`runs.py:189-203`); the flow (`runs.py:282-289`); the ice (`water.py:116-165`); open water (`wild.py:1345-1362`); a crop standing high, smoke, loudness (`environment.py:117-147`) | a function of the driven layer over a window of days, with a threshold, at a place | one condition registry: a key, its reader, its parameters, its place; WHEN's vocabulary (`wild.py:1395`) is the start, but it is the wild layer's own and the others do not use it |
| **F7 Transitions of kind** | forest to scrub and back (`forests.py:100-110`); a dam up and down (`wild.py:738-767`); ice open, edges, over (`water.py:116-135`); a site gone and back (`wild.py:816-821`, `:795-811`); (B's) carcass stages, lots becoming goods | a thing of one kind or state becomes another when a property crosses a threshold, with effects | a transition row `{of: category, from, to, when, effects}`; pattern 3c widened from lots in containers to any kinded thing |
| **F8 Couplings** | body to food web (`waters.py:79-93`); plant pools shared (`wild.py:557-610`); crops and stores eaten (`wild.py:132-217`); vermin follow the harvest (`:679-693`); loads harm and feed (`:219-289`); sites eat and harm (`:822-845`); a dam floods (`:738-767`); beasts stop young growth (`forests.py:77`, `:86`) and halve willow (`night.py:650`, `willow.py:57`); brash (`forests.py:113`) | one population or stock changes another's S or K, on covers or within a reach, by a share | effect rows on the source's row `{target, covers or reach, share, when}`, one interpreter |
| **F9 Movement on a network** | the runs (`runs.py:316-437`); kinds moving between areas (`ecology.py`, `links` `:70-78`); ranging groups (`wild.py:1813-1940`); storms crossing (`climate.py:205-226`) | counts or bodies moving along a declared graph, a share a day, held at gates | a flow on a declared graph (edges, direction, gates such as a shut dam or ice), with what moves and its cue |
| **F10 Driven layers** | the climate (`climate.py:104-265`); the hand-written spells (`environment.py:15-72`); the wild's seasonal means when the climate is off (`wild.py:47-60`, `ecology.py:25-27`); spec cold days (`world.py:397`) | values a place and day, from the seed | one driven layer with its fallbacks declared, read through `environment` (§2.2 of feature_packages) |
| **F11 Classes by name lists** | `switches.CLASSES` (`switches.py:23-31`); methods' GENERIC (`methods.py:230`); the diet `cls`; TRAITS; four water classifications (`water.py:57`, `wild.py:1334-1342`, `wild.py:3117-3124`, `runs.py:141-144`); the generator's FIELD_OK, BUILT_OK, MEADOW_OK, WOOD_OK (`vocab.py:92-95`) | membership of a row in a class, by a list of names | a `class` or `tags` property on the row, one resolver (pattern 4) |
| **F12 Analyses that re-derive physics** | `capacity.py:39-50`; `cybertron2/capacity/sources.py:125-133` (which does use `RN.step`); `landgen/economy.py:98-130`; `landgen/gates.py:255-300` | what a place can sustain, or whether a chain can be completed | the same rows and rules the night runs (`renewal.step`, the techniques' inputs and sites) |

## 2. The mechanisms

Wave: **W** written in the wave (since f728a3b7); **w** changed by it; blank: before.

| # | Mechanism | Where | Pattern(s) it is or should be | Fit | Wave |
|---|---|---|---|---|---|
| 1 | Parcel stocks from a world's spec, in goods' units, by pack and switch | `world.py:125-133` | 3a stocks | rows (seam by name, `:129`) | |
| 2 | Forest stocks from a forest kind | `world.py:125`, `forests.py:18-46` | 3a, F2 habitat | named (`copse` for old worlds `:35`, `scrub` `:41-42`) | |
| 3 | Grass on grazing covers | `world.py:134-139`, `data.py:967` | F2 | fitted (a side table by cover; the generator gives grass too, `vocab.py:111`) | |
| 4 | The world build's four seeders in sequence (bodies, wild, shallows, willow) | `world.py:270-278` | F2 | named (one call each) | w |
| 5 | Draw, add, set a stock; set the wild state | `world.py:698-711`, `:934-950`, `:736-746` | the chokepoint | rows (the crop branch `:699` is farming's hook, feature_packages §3) | |
| 6 | A cold night at a place: a spec's day, the climate's frost, or every winter night | `world.py:391-402` | F6, F10 | fitted | |
| 7 | The calendar | `world.py:378-384` | the calendar | rows | |
| 8 | An entity's place by its kind | `world.py:410-427` | space (§2.1 registry) | named (by ref kind) | |
| 9 | The renewal registry: a stock's rule from its record or its resource | `renewal.py:23-33`, `:162-169` | 3a | rows | |
| 10 | fast and threshold regrowth | `renewal.py:35-46`, `night.py:620-628` | 3a | rows | |
| 11 | periodic: a run as a stock in its seasons | `renewal.py:47-64` | 3a, 3b | fitted (run_K from makers) | |
| 12 | seasonal: a wild plant's crop | `renewal.py:82-92` | 3a | rows | |
| 13 | The shallows' rule, nothing under ice | `renewal.py:66-72`, `water.py:105-112`, `night.py:645-647` | 3a | named (iced passed by a branch on the rule's name in the driver) | W |
| 14 | The willow's rule: back to K on spring's first night; summer cutting lowers K | `renewal.py:74-80`, `willow.py:50-73`, `night.py:648-655` | 3a, F8 | named (first_spring and grazed by branch; K written outside the rule) | W |
| 15 | The woods' trees, young growth and dead wood | `forests.py:49-67`, called at `:80-89` | 3a | fitted (called by rule name, outside `RN.step`) | |
| 16 | finite, population, endless, accrues | `renewal.py:112-131` | 3a | rows | |
| 17 | The renewal context (weather, land) offered to rules | `renewal.py:134-159` | F6 | silent (no rule reads it, `:143`) | |
| 18 | The take's answer to density | `renewal.py:172-180` | 3a, F3 | rows | |
| 19 | The woods' night: growth, regrowth unless grazed, shed, rot, a gale | `forests.py:69-110` | 3a, F5, F8 | fitted | |
| 20 | Forest to scrub under 40% of its trees, and back | `forests.py:100-110` | F7 | named (`forest`, `scrub`) | |
| 21 | Brash left as dead wood | `forests.py:113-117` | F8 | fitted | |
| 22 | Fuel in heat, by the household's order | `forests.py:120-146` | rows | rows | |
| 23 | "2 firewood or 0.5 timber" | `forests.py:148-150` | (g) signs | text | |
| 24 | A node's capacity a year | `capacity.py:30-50` | F12 | named (`field`, `forest`, `scrub`; PLOT and WILD constants) | |
| 25 | The weather scheduler: eras, years, types, fields, storms | `climate.py:104-265` | F10 | rows | |
| 26 | The weather's label, visibility and frost from its values | `climate.py:320-361` | F10, F6 | rows | |
| 27 | The hand-written spells, and the old spell words from the scheduler | `environment.py:15-72`, `climate.py:363-377` | F10 | fitted (two paths) | |
| 28 | Snow lying | `environment.py:85-97` | F6 | rows | |
| 29 | Days since heavy rain | `environment.py:99-106` | F6 | rows | |
| 30 | How much a place lets a sense through | `environment.py:150-172` | (g), F6 | named (crop high on `field` `:121`; smoke and noise by lists of technique names, `data.py:1057`) | |
| 31 | A felled wood seen through | `environment.py:197-200` | F7 | rows | |
| 32 | The wild's weather when the climate is off | `wild.py:47-60` | F10 | fitted | |
| 33 | One fish record a water body, shared by aliasing | `waters.py:24-61` | space, 3a | rows (but a space kind made by aliasing records; §4.7) | |
| 34 | A body's lead parcel, so a shared stock is counted once | `waters.py:71-77` | space | rows | |
| 35 | The body's fullness set on the food web's fish, one way | `waters.py:79-93` | F8 | fitted (no write-back, [[L-116 The wild layer's fish and a water body, two ways|L-116]]) | |
| 36 | The wild history before the run | `wild.py:86-131` | F10, 3a | rows | |
| 37 | Hens a house at the world's making | `wild.py:125-130` | F2 | named (`hen`, HENS_A_HOUSE) | |
| 38 | The food web's foods grow and rot | `ecology.py:250-275` | coupled populations (§4.3) | named (WATERED `:257`; mast, fruit, nuts, seeds `:264-265`) | |
| 39 | Eating by Kleiber, condition, hunger, breeding, movement, migrants | `ecology.py:275-512` | coupled populations | rows | |
| 40 | Habitat and presence from the land summary | `ecology.py:31-195` | F2 | rows | |
| 41 | The mast | `ecology.py:200-220` | 3b | fitted | |
| 42 | Snow buries forage | `ecology.py:319-320` | F6 | named (a list of foods) | |
| 43 | Loads: their levels, harm on crops and stocks, feeding | `loads.py:39-100`, `wild.py:219-289` | F8 | rows | |
| 44 | Disease in the wild and in kept herds | `diseases.py:19-52`, `wild.py:292-360` | 3b, F8 | rows | |
| 45 | The voles' cycle and phases | `ecology.py:477-493`, `kinds.py:442-450` | coupled populations | named (side tables by kind) | |
| 46 | Vermin follow the harvest | `wild.py:679-693`, `kinds.py:451` | F8 | named (side table by kind) | |
| 47 | Crops and stores eaten by wild kinds | `wild.py:132-217`, `:2865-3023` | F8 | named (`crops`, `stores`; `smoke loft` `:3000`, `:3008`; STORE_KIND) | w |
| 48 | The land's plants shared with people | `wild.py:557-610` | F8 | rows | |
| 49 | Wild plants seeded by niche | `wild.py:476-496`, `plants.py:96-133` | F2 | rows (the best habitat code in the area) | |
| 50 | The plants' year factor (a draw, the mast, a load) | `wild.py:511-545` | 3b | rows | |
| 51 | Sites: seeding, the season, grow or crash, leave, eat, harm, a dam rebuilt | `wild.py:697-852` | 3a, F8, F7 | rows | |
| 52 | A beaver dam up or down | `wild.py:738-767` | F7, F8 | fitted (`fish`, `dead` by name `:749`, `:762`) | |
| 53 | Taking at a site (young, a lodge's trap, breaking the dam) | `wild.py:865-905`, `:1135-1152` | F3 | rows | |
| 54 | Legends and leaders | `wild.py:1193-1212`, `:1928-1940` | bodies drawn out | named (side tables by kind, `kinds.py:512-533`) | |
| 55 | A great freeze | `wild.py:1213-1240` | F5 | rows | |
| 56 | The condition vocabulary | `wild.py:1395-1466` | F6 | rows (the wild layer's own) | |
| 57 | A kind's conditional layers (drive, bold, danger, flee) | `wild.py:1469-1487`, `kinds.py:276` | F6 | rows | |
| 58 | Open water and the cold's push on the fowl | `wild.py:1334-1388` | F6 | named (OPEN_WATER's own water classes; PUSHED by `wildfowl`) | |
| 59 | Groups near people: condense, drive, traces, raid, fences, watches, scares, memory | `wild.py:1947-2240` | bodies drawn out, F8 | rows (targets by kind of thing; `dog` fitting) | |
| 60 | Ranging packs | `wild.py:1813-1940` | F9 | fitted | |
| 61 | Carcasses to the carrion pool and back | `wild.py:1732-1806` | F8 | fitted | |
| 62 | Hens lay | `wild.py:2243-2254` | 3a | named | |
| 63 | A cat at a store, a barn owl in its hole | `wild.py:2936-2975`, `kinds.py:846-851` | F8 | named (one row each: CAT, OWL) | |
| 64 | The hunt by method | `wild.py:2398-2655` | F3 | rows (goods `meat`, `fish`, `hide` `:2612-2627`; `game` `:2289`, `:2425`) | |
| 65 | Take tables built from traits at load | `methods.py:174-210` | 1, 2 | rows | |
| 66 | Familiarity by kind | `methods.py:212-283` | (learning) | rows | |
| 67 | Methods known by the land | `methods.py:288-347` | (knowledge) | named (BASIC, NOT_BY_LAND lists `:170`, `:285`) | |
| 68 | Pest work: which load one means | `wild.py:1154-1190` | 4 resolver | words (LOAD_NAMES, `want.rstrip("s") in k` `:1166-1170`) | |
| 69 | A run taken by hand | `wild.py:3491-3535` | F3 | fitted | |
| 70 | Set gear's night | `wild.py:975-1131` | 3d, F3, F4 | named (ice by a technique tuple `:1016`; snare `:1023`, `:1114`; SET_HOLD_KG `:920`; trap's hold `:1069-1072`; open-water fish for two named nets `:1098`) | W |
| 71 | The snare line untended | `wild.py:929-972` | F4 | named (SNARE_NIGHT) | W |
| 72 | The runs: network, cue, window, advance, return, held, iced | `runs.py:48-437` | F9, 3b | fitted (generality.md §4) | w |
| 73 | Gear sharing a run | `gear.py:114-200`, `wild.py:3240-3290` | 3d | named (weirs found by `monument == "weir"` `:3043`, mills by the `water wheel` fitting `:3062`) | w |
| 74 | A weir's sections: share, hold, wear, cost | `gear.py:39-112`, `wild.py:3082-3169` | 3d, 3e | fitted ([[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]) | w |
| 75 | A weir's water: beck, large, lowland | `wild.py:3117-3124` | F11 | named (a third water classification) | |
| 76 | A mill's gap, its rate, the dam holding a run | `wild.py:3172-3186` | 3d, F9 | fitted | |
| 77 | Gear torn by the flow, in the fen, at the thaw | `wild.py:3309-3366`, `water.py:167-189` | F4, F5 | named (three technique tuples `:3322`, `:3355`, `:3340`; the gill net's own rule `:3326`) | W |
| 78 | Otters rob the traps | `wild.py:3384-3428` | F4, F8 | named (WATER_ROBBERS; `trap in water` only `:3397`) | |
| 79 | The river's flow tonight | `runs.py:282-289`, `wild.py:3468-3488` | F6 | silent (`except Exception: return "normal"` `:3487`) | |
| 80 | The river's record (what passed, banded) | `river.py:113-159` | (h)-like record | rows | W |
| 81 | The river's signs (D's area) | `river.py:167-508` | (g) | named (eel, salmon, lamprey; generality.md) | W |
| 82 | A parcel's water type | `water.py:57-76` | 1 (a missing category) | named | W |
| 83 | The shallows' K and seeding | `water.py:79-102` | F2 | named (SHALLOWS by water type) | W |
| 84 | The ice | `water.py:116-165` | F6, F7 | named (ICE by water type; silent `except` to `open` `:127-129`) | W |
| 85 | A run's reach into the fen, and the pinch | `water.py:176-206` | 3d | named (RUN_REACH, PINCH) | W |
| 86 | Wild willow: K, seeding, summer harm | `willow.py:23-73` | F2, F8 | named (WILLOW by cover, BANK_COVERS) | W |
| 87 | A world's wild switches, checked at load | `switches.py:23-99` | 4, 1 | named (CLASSES lists; `game` kinds listed again `:97`; raises on unknown names `:51`) | |
| 88 | The generator's physical field | `landgen/physical.py` | the generator | fitted | |
| 89 | Configurations and systems | `landgen/macro.py` | the generator | rows | |
| 90 | Natural ecosystems and the cleared land | `landgen/ecology.py:72-196` | the generator's catalogue | named (legitimately: a decision table as code) | |
| 91 | Settlement and land allotment | `landgen/settle.py` | the generator | named (FORBIDDEN `:20`; `:371-395`) | |
| 92 | Roads and their terrain | `landgen/roads.py`, `vocab.py:100-102` | the generator | named (PACE_KMH, ROAD_TERRAIN by cover) | |
| 93 | Place and parcel words | `landgen/names.py:74-101` | (g) | text | |
| 94 | A parcel's land block | `landgen/write.py:66-87` | 5 | rows | |
| 95 | A parcel's stocks | `landgen/write.py:108-128` | F2, 5 | fitted (PER_UNIT by cover; no fish) | |
| 96 | Households, buildings and herds by trade | `landgen/write.py:393-420` | 5 (makers pin people) | named (TRADES, FARMING; C's livelihood rows, build_gaps G68) | |
| 97 | The economic check, and the access-gate check | `landgen/economy.py:98-130`, `landgen/gates.py`, `gate_check.py` | F12 | named (named stocks and goods; makings by named crafts `gates.py:258-300`, GEAR_OF `:144`) | w |

`generate.py` (the society generator) and the land summary's areas and bodies (`wild/areas.py:27-181`, fitted, generality.md §1)
are the remaining generator steps; generate.py is people, and is C's in substance.

## 3. The branches on named things, and the property each becomes

Counts by file (`a_named.py`; `a_wave.py` for the wave):

| File | Branches | In the wave | File | Branches | In the wave |
|---|---|---|---|---|---|
| engine/wild.py | 70 | 24 | landgen/settle.py | 57 | 0 |
| landgen/write.py | 55 | 0 | landgen/ecology.py | 33 | 0 |
| wild/river.py | 19 | 19 | landgen/economy.py | 19 | 0 |
| wild/water.py | 15 | 15 | wild/ecology.py | 15 | 0 |
| landgen/gates.py | 14 | 11 | landgen/names.py | 13 | 0 |
| engine/forests.py | 11 | 1 | landgen/roads.py | 11 | 0 |
| landgen/macro.py | 10 | 0 | engine/data.py | 8 | 5 |
| wild/willow.py | 7 | 7 | engine/world.py | 5 | 0 |
| wild/methods.py | 5 | 1 | landgen/gate_check.py | 4 | 4 |
| engine/capacity.py | 3 | 0 | engine/waters.py, wild/areas.py, plants.py, runs.py, switches.py | 3 each | 0 |
| environment.py, generate.py, gear.py, physical.py | 1 each | 0 | renewal.py, climate.py, loads.py, diseases.py | 0 | 0 |
| **Total** | **393** | **87** | | | |

What each family of branch should become (the 393 grouped; each group's sites cited by example):

| Branch (examples) | Count (about) | Becomes | Under |
|---|---|---|---|
| Set gear by technique name: `tech in ("trap in water", "gill net", "set line")` for ice idle, wreck, thaw (`wild.py:1016`, `:3322`, `:3355`); `tech == "snare"` (`:1023`, `:1036`, `:1114`); `== "trap in water"` for the hold, the race and the robbers (`:1069`, `:3259`, `:3340`, `:3397`); open water fish for gill net and set line (`:1098`, `:3326`) | 19 | the method's `set` row: `in_water: true` (ices, torn by flow and thaw, robbed by water robbers), `hold_kg {run, open}` (SET_HOLD_KG folded in), `draws_open: fish`, `untended: {dies, escapes, scavenged}` for the snare, `wreck: {spate, flood}` for the net. The edge techniques already carry `ice: bank` and `ice: edge` (rows `angle`, `fish by hand`): the same property, on the same day, by the other road | F4 |
| Water types by name: `water_type` (`water.py:62-76`), SHALLOWS, ICE, PINCH, THAW_WRECK, SMALL, RUN_REACH (`water.py:21-30`), OPEN_WATER's small/big river/lake (`wild.py:1342`, `kinds.py:399`), a weir's beck/large/lowland (`wild.py:3117-3124`), runs' `river`/`big river` (`runs.py:133-144`), `at_water` (`wild.py:1365-1372`), willow's brook/river (`willow.py:29`) | 34 | a **WATER_TYPES table** (a new row category): `shallows_K`, `ice {edges, over}`, `pinch`, `small`, `thaw_wreck`, `run_reach`, `open_water_hold`, `weir_wear`, `flow_scale`; one `water_type(parcel)` resolver that every reader calls | 1 |
| Covers by name in rules that read a cover's property: forest and scrub (`forests.py:101-107`, `capacity.py:42`, `economy.py:103`, `wild.py:1279`, `areas.py:93`); field (`capacity.py:41`, `environment.py:121`, `wild.py:836`); water and fen (`water.py:62-95`, `river.py:339`, `willow.py:26-28`, `wild.py:3040`, `:3325`); the generator's FORBIDDEN, PACE, ROAD_TERRAIN (`settle.py:20`, `vocab.py:100-102`) | about 110 | COVERS properties: `wooded` (and `succession: {to: scrub, below: 0.4}`), `farmland`, `wet: water or fen`, `habitable` (FORBIDDEN), `pace_kmh`, `road_terrain`, `turf` (TURF), `grazing` (PHYSICS cattle), `clearing {to_field, to_built, fertility}` (CLEARING), `plant_layers` (LAYERS), `hunt`, `field_edge` (HUNT_COVERS, FIELD_COVERS), `bank_willow` (BANK_COVERS), `tint` (picture) | 1, 2 |
| Covers in the generator's own catalogue: terrain to ecosystem (`landgen/ecology.py:77-111`), the natural woods and the settled land (`:117-184`), settle's land uses (`settle.py:371-395`, `:442-528`), the words by cover (`names.py:74-101`) | about 100 | legitimately by name: the generator's classification rules; a candidate for an ordered rule table (`{where: terrain and condition, then: ecosystem}`) only if more biomes come ([[D2-354 The architecture is a healthy balance, not a strict one|D2-354]]: the generator owns its specifics) | (system-owned) |
| Goods by name in the takes: `meat`, `fish`, `hide` (`wild.py:2612-2627`), `wild food` (`:617`), `hen` (`:1676`, `:125-130`), `pack` (`:2338`); the economic check's grain, wild food, meat, milk, firewood, timber (`economy.py:105-195`) | about 35 | item properties already there (`food > 0`, `heat`, `carry`); `taken.goods` of the kind; an `offal_of` on the meat good; the checks read `ITEMS[i]["food"]` and `heat` over the stocks' `taken`/`gives` rows | 2, F12 |
| Resources by name: `seam` (`world.py:129`), `young`/`dead`/`wood` (`forests.py:32-44`, `world.py:757-775`, `wild.py:762`), `game` and `plants` (`switches.py:95-97`, `wild.py:2289`), `fish` (`waters.py:21`, `switches.py:90`, `wild.py:749`), `shallows`, `willow` (`water.py:95`, `willow.py:40`) | 21 | the resource row's `renewal` and `role` (`fuel_of: forest`, `finite`), the switch class on the row; the dam's `raises: {res: fish}` in its SITES row | 1, 2 |
| Wild kinds and foods by name: WATERED, mast, fruit, nuts, seeds (`ecology.py:253-265`, `:319`); `crops`, `stores` (`wild.py:140-190`); `mast` (`:529`, `:1411-1417`); `eel` (`river.py:219-293`), `otter` (`:411`) | 21 | FOOD row properties: `watered`, `warm_boost`, `snow_buries`, `bridge: crop | store`; a kind's `run.window` read off its RUNS row (not "eel" by name); `robs: water_gear` on the kind | 2 |
| Building parts by name: `is_weir` by monument (`wild.py:3043`), mills by the `water wheel` fitting (`:3062-3080`), `smoke loft` (`:3000`, `:3008`), `trap` and `weir` rows of WATER_WORKS (`:1070`, `:3148`, `:3266`) | 13 | fitting and monument properties: `gap: true` (a weir, a wheel on a run), `hangs_lots: true` (the smoke loft), the WATER_WORKS row looked up from the fitting's `works:` field | 2 |
| Techniques by name in the gate check: `dress and spin` (`gates.py:258`, `:292`), GEAR_OF, SEASON_GEAR, SKIP (`gates.py:26`, `:144-145`), `cut withies` (`:279`) | 14 | the checks derived from rows: a craft's `inputs` and `at.covers` give its chain (flax seed, retting water), the method's `gear` field (present, empty, on every set method) names its good, `crew` and `needs` say what it waits on | F12 |
| Forest kinds by name: `copse` (`forests.py:35`), `managed wood` (`plants.py:112`, `write.py:385`) | 5 | FORESTS row properties: `old_world_default: true`, `coppiced: true` | 1 |

**Legitimately by name (kept):** the generator's terrain-to-ecosystem-to-cover catalogue (about 100 sites, above); the household
seeds a maker pins (`write.py:396-420`: pattern 5 lets makers pin people, though these belong in C's livelihood rows, build_gaps G68);
a core default such as the heat order's `firewood, timber, charcoal` (`data.py:910`), which is already a data list; the weather labels
the climate emits (`climate.py:320-334`), which are the layer's own vocabulary.

**The side tables** (a category's property held off its rows, keyed by the rows' names): covers 16 (`TURF` `data.py:215`, `CLEARING`
`:296`, the cattle `grazing` `:967`, `WATER_COVERS` `wild.py:394`, `HUNT_COVERS`, `FIELD_COVERS` `methods.py:16-17`, `LAYERS`
`plants.py:16`, `BANK_COVERS` `willow.py:20`, `FORBIDDEN` `settle.py:20`, `PACE_KMH`, `ROAD_TERRAIN`, `PER_UNIT` `vocab.py:100-111`,
`COVER_TINT` `picture.py:11`, `WILLOW.K`, the smoke and noise lists by technique `data.py:1057`, GAPS by structure `kinds.py:814`);
water types 7 (above); the wild kinds 18 (`kinds.py`: BODY, NEAR_PEOPLE, TAKEN, TRAITS and PRESENCE folded into the rows by
`rows()` at `:921-926`; CYCLE, PHASES, FOLLOW_HARVEST, STORE_KIND, PUSHED, WATER_ROBBERS, LEADERS, LEGENDS, WHEN, the hunted `flee`
`:453`, and the sign tables SIGNS, EXPERT_SIGNS, KILL_READINGS, EXPERT_KILL, HUNT_NOTICES not); techniques 6 (SET_HOLD_KG, SNARE_NIGHT
`wild.py:920-921`, SWEEP, TAKE_BASE `methods.py:110`, `:118`, GEAR_OF, SEASON_GEAR `gates.py:144-145`). `kinds.rows()` is the model to
copy: side tables folded into the row once, at load, so every reader finds them on the row.

## 4. What does not fit, and the pattern it would need

The candidates the brief names that are this area's (weather and the calendar, travel, fire and heat in part) are taken here; the
rest are B's and C's.

### 4.1 Habitat: where a stock lives and how much (none of the patterns)

Pattern 3a says a stock is S, K, r on a declared clock; it says nothing about **where** a stock is or **what K** a place gives it.
That decision is written nine times: grass (`world.py:134-139`, from a cattle table by cover, and again by the generator,
`vocab.py:111`); the woods (`forests.py:18-46`); the generator's plants, game, quarry and seam (`write.py:108-128`); the wild plants'
niche (`plants.py:96-133`, the only one that reads covers, ecosystem, wetness, coast, coppice and fertility from the row); the shallows
(`water.py:79-102`); willow (`willow.py:23-46`); sites' candidates (`wild.py:697-711`); a body's fish (`waters.py:24-50`, from what
three makers wrote, generality.md §2); the hens (`wild.py:125-130`). **Pattern needed:** a `habitat` block on every resource row
(covers with weights, beside water or a cover, land conditions, ecosystem weights, K a unit of size, by water type for water), read
by one seeder at one moment (the generator, or the world's build for hand-made worlds). Without it pattern 5 cannot hold: the
generator does not stock fish because the fish's habitat is in no row the generator reads.

### 4.2 Couplings: one thing acting on another's stock (none of the patterns)

Loads harm crops and stocks and feed others (`wild.py:219-289`); sites eat a stock and harm crops (`:820-845`); a dam cuts the
grass's K and raises the fish's (`:738-767`); beasts on a parcel stop young growth (`forests.py:77`, `:86`) and halve willow's
regrowth (`night.py:650`); felling adds dead wood (`forests.py:113`); the vermin follow the harvest (`wild.py:679`); the body's
fullness sets the food web's fish (`waters.py:79-93`); the wild kinds eat the crops and stores (`wild.py:132-217`). The LOADS and SITES
rows already carry `harm`, `harm_res`, `feeds`, `eats` and `dam` fields (`kinds.py:476-490`, `:675-711`), but each has its own reader,
and the grazing cut is written twice. **Pattern needed:** effect rows on the source `{target: res | crop | store, covers or reach,
share, when}`, one interpreter, every effect through `draw`, `add_res` and `set_res`. This is the "economy web" of feature_packages
§2.3's populations meeting each other.

### 4.3 Coupled populations: the food web (pattern 3a is wrongly cut)

The wild kinds are RESOURCES rows with `renewal: population` (`kinds.py:921`), but the rule is the identity (`renewal.py:117-122`):
their dynamics are `ecology.step` (`ecology.py:222-512`), where every kind eats from foods and other kinds by Kleiber's law, its
condition follows what it got, and it breeds and moves by it. That is not S, K and r, and no per-stock rule could be: the state is
the whole web. Feature_packages P3 allows it ("a process with its own dynamics"). The hypothesis should say so: **3a is two
patterns**, independent stocks (the renewal registry) and **coupled populations** (a web stepped as a whole, reading its kinds' rows:
mass, class, diet, habitat, breeding, movement), with **draw-out and return** between them and people (§2.3) as the seam.

### 4.4 Movement along a network (none of the patterns)

The runs are not pulses: a run is a population moving along the river's graph from `land.down` (`runs.py:48-147`), down or up, a
share a night on a cue, held below a shut dam (`wild.py:3178-3186`), held at an iced stretch (`runs.py:316`), met by gear upstream or
downstream first (`gear.py:127-176`). The food web moves kinds between areas (`ecology.py:70-78`); ranging packs choose a village by
distance and memory (`wild.py:1813-1940`); storms cross the region (`climate.py:205-226`). **Pattern needed:** a flow on a declared
graph (nodes, directed edges, gates with conditions, a cue), carrying counts or bodies. Pattern 3b covers only the cue.

### 4.5 Driven layers and the conditions read off their memory (3b needs it to be a pattern)

The weather is a driven layer (feature_packages §2.2) with two fallbacks (`environment.py:14-73`, `wild.py:47-60`). What the
mechanisms read is not the weather but conditions over its recent days, each written where it was needed: frost as a low under 0
(`climate.py:358-360`, `world.py:391-402`) and hard frost as a low under -3 with a day under 3 (`wild.py:1315-1317`, and again in
`ecology.py:241`); frozen nights in a row (`wild.py:1320-1325`); snow lying (`environment.py:85-97`); heavy rain since
(`:99-106`); a hard winter, rain after dry, tomorrow's frost (`wild.py:1426-1446`); the spate cue (`runs.py:195-203`); the flow
(`runs.py:282-289`); the ice (`water.py:116-165`); open water (`wild.py:1345-1362`). The wild layer's `cond` (`wild.py:1395-1466`) is
already a vocabulary of keys read by rows (WHEN, the methods' `when`, the notices), but it lives in `wild.py`, and the renewal
context (`renewal.py:134-159`), which was built to give rules the weather, is read by no rule. **Pattern needed:** one condition
registry: a key, its reader over a driven layer's window at a place, its parameters; every `if`, `when` and hazard row in every
package reads it. Pulses (3b) and hazards (F5) are then rows of `{when, chance, effect}`.

### 4.6 Transitions of kind (3c is cut too narrow)

A forest under 40% of its trees becomes scrub and comes back (`forests.py:100-110`); a dam goes up and down (`wild.py:738-767`); a
water's ice goes open, edges, over and back (`water.py:116-135`); a site goes and comes back (`wild.py:816-821`, `:795-811`). Pattern 3c names only
a lot in a container becoming another good. **Pattern needed:** 3c widened: a kinded thing (a lot, a parcel's cover, a water's state,
a site, a carcass) becomes another kind or state when a condition on its properties holds, with effects. Then succession (feature
packages §2.5) is a row, not a branch.

### 4.7 Places that group places (no pattern; feature_packages §2.6 is open)

A water body's fish are one record that every parcel on it holds by **Python object identity** (`waters.py:51-61`); every reader that
sums over parcels must remember `lead` (`waters.py:71-77`) and the night must skip a record it has seen by `id(r)` (`night.py:641`).
The wild areas are a second grid with a bridge (`wild/areas.py`), and the river's stretches a third (`v:<node>`). **Pattern needed:**
a population's `where` is a declared place of any space kind (a parcel, a body, an area, a stretch), as feature_packages §2.3 says;
the aliasing goes.

### 4.8 Analyses that re-derive the physics (pattern 2's blind spot)

`capacity.py:39-50` counts fields, woods and constants (PLOT, WILD 8) by cover name, though `renewal.py:6-8` says the capacity model
calls the same rules (the newer `cybertron2/capacity/sources.py:125-133` does); `landgen/economy.py:98-130` sums named stocks into
named goods; the gate check names its crafts (`gates.py:258-300`). **Pattern needed:** none new: analyses must read the rows and rules
the night runs. But no pattern says it, and the duplicates drift (two capacity models, the same grass seeded with two numbers).

### 4.9 Also not captured, smaller

- **Classes and the resolver (pattern 4):** seven tables of aliases and classes in the area (FITTING_ALIAS `data.py:359`, CROP_OF
  `:214`, methods' OLD_NAMES and LOAD_NAMES `methods.py:165-171`, GENERIC `:230`, switches' CLASSES `switches.py:23-31`), and one
  word-list parse (`wild.py:1166-1170`). Pattern 4 is right and absent.
- **Clocks:** no row declares its clock (§1.2); [[D2-273 Three clocks, each system on one|D2-273]]'s year clock is applied by hand in each rule, and the rivers' fish stay on the
  night clock against it (generality.md §2). Pattern 3a's "declared clock" is not built anywhere.
- **Hand-written text** is small here: the generator's place words (`names.py`) and fuel words (`forests.py:148`); the signs are D's.

**Weather and the calendar** need §4.5's driven layer and condition registry; **travel and roads** in this area are only the
generator's (`roads.py`, PACE_KMH), a cover property; **fire and heat** here are fuel in heat (`forests.py:120-146`), which is already
rows (ITEMS `heat`).

**Is the set enough?** For the world's physics, **too few and partly wrongly cut**. Add habitat (on 3a), couplings, coupled
populations (split from 3a), movement on a network, the condition registry over driven layers (under 3b), transitions (3c widened)
and places of any space kind. Keep 1, 2, 3d, 3e, 3f and 4, with 1 amended: a category's properties live on its rows, never in column
tables keyed by its names.

## 5. Checks at load

There is **no load-time check of any registry in the area**: `data.py`, `wild/kinds.py`, `wild/methods.py`, `wild/water.py`,
`renewal.py` declare no required fields and raise nothing on a missing or misspelt one (searched for `raise`, `assert`, `check`,
`validate`). The one check is the world switches' (`switches.py:51`, `:72-75`: an unknown class or kind named in `kinds_off` or
`runs_off` raises, [[W-69 Nutrition worlds|W-69]]). `methods.build` (`methods.py:199-210`) builds the take tables from the traits at load but checks nothing;
a method whose `needs` matches no trait gets an empty table silently. A renewal rule named on a record that RULES lacks fails at the
first night with a KeyError (`renewal.py:172`), not at load.

## 6. The restructuring for area A: cost and saving

Counted from this survey, in feature_packages.md §10's units (shared-file code re-expressed at about 300 to 400 lines a builder-day;
own files moved at about 2,000).

| Step | Lines rewritten | Lines moved | Risk | §9 phase |
|---|---|---|---|---|
| Rows whole: COVERS gathers its 16 side tables; a WATER_TYPES table replaces 7 dicts and 4 classifications; the wild kinds' 13 unfolded tables folded by `rows()`; set methods get `in_water`, `hold_kg`, `untended`, `draws_open`, `wreck`; a load-time check of every registry's required fields | about 600 data, 250 code | about 300 | low: no behaviour change if values are copied (golden journals) | 1 (registries), 2 |
| The 250 property branches rewritten to read the properties (§3) | about 700 | 0 | low to medium: each a local change; the set's and the river's are calibrated | 2 |
| Renewal extended (§9: rules declare their context keys and may return K); the shallows and willow branches in `night.py:645-655` go; the woods through `RN.step` | about 150 | 0 | low | 1 |
| One habitat seeder (§4.1) replacing nine | about 400 (replaces about 450) | 0 | **medium**: K changes unless each seeder's numbers are carried as rows exactly; the generator's worlds change | 5 |
| One condition registry (§4.5): `wild.cond`, `environment` and `water`'s readers, the runs' cue, behind keys | about 300 | about 450 | low if each reader is moved, not rewritten | 1b/5 |
| Couplings and hazards as rows (§4.2, F5) | about 600 | 0 | medium: the order of draws within a night must be kept (keyed draws by name keep them) | 2 |
| One take primitive (F3) under the hunt, the sets, the run by hand and the site | about 900 | 0 | **high**: the hunt and sets were calibrated over briefs 4 to 4c and [[W-108 The waters calibrated across many generated environments|W-108]]; byte-identical journals need the same draws in the same order | 5 |
| Water bodies as a space kind (§4.7) | about 200 | 0 | medium: saved worlds (schema 11) | 5 |
| **Total** | **about 3,000 to 4,500** (with tests) | **about 1,500** | | |

**At 300 to 400 lines a builder-day, 8 to 14 builder-days**, of which the take primitive and the habitat seeder are half and carry the
behaviour risk; the rows-whole and property-branch steps (about 4 to 5 days) carry little and give most of the saving.

**What it saves**, measured by what a new row costs today:
- **A new water type** (an estuary, a mere in a fen) must be added to SHALLOWS K, ICE edges, ICE over, PINCH, THAW_WRECK's small/river
  choice, SMALL, `water_type`'s branches (`water.py:57-76`), OPEN_WATER's classes, the weir's water kind (`wild.py:3117-3124`), and the
  runs' `where`: **at least 8 places in 4 files**; after, one row.
- **A new kind of water gear** (an eel basket, a fyke): `"trap in water"` is named 9 times in `wild.py`, 7 in `placed.py`, 5 in
  `signs.py` and `livelihoods.py`, 4 in `things.py`, 3 in `methods.py` and `river.py`, 2 in `gates.py`, `kinds.py` and
  `bots_livelihood.py`, and once each in `gear.py`, `learning.py` and `night.py` (`grep`): **45 sites in 13 files**, of which the new gear
  must join the ones that mean "in water": at least 9; after, `in_water: true` on its row.
- **A new cover** (a reedbed, a salt pan as a cover): 16 side tables plus the generator's catalogue.
- In §11's terms: the wild layer's shared-file edits (1,835 lines on `ecology-hunt3`, and the wave's 87 named branches in about 2,000
  changed lines here) are the integration share that grows faster than linearly; with properties on rows a feature's new behaviour
  extends a row and a reader once, instead of adding a branch in each of the 8 to 13 readers that already exist.

## 7. How the area was built (Zach's addition 2)

From `git log` on the area's files (220 commits touching them, 23 Oct to 23 Nov; the clone unshallowed for it).

| Period | What came | Commits |
|---|---|---|
| 23-31 Oct | the core (ce24b6f3): world, data, the society generator; packages A to F: weather and visibility (ff52fb35), forests and fuel (fc4c6831) | 41 |
| 1-8 Nov | the landscape generator (98bdc3ff, 1 Nov; ecosystems 53d4d4aa, 2 Nov; economic checks 3ca5d994); the night's rules as pure functions (5a85a95e, 7 Nov); the renewal registry (92cfdbf6, 7 Nov); the weather scheduler (a0bbdd53, 8 Nov) | 47 |
| 9-14 Nov | the wild layer (9d418ff2, 9 Nov) and its waves: methods from traits (6e527209), plants (8b4379d4), loads (7eac5da0), disease (1ff123fb), the condition vocabulary (dbdb2afd), briefs 4 to 4c | 66 |
| 15-19 Nov | the river (55f41aa3, brief 5), water bodies (b3f2ef81, [[D2-229 One fish stock per water body|D2-229]]) | 32 |
| 20-23 Nov | [[W-69 Nutrition worlds|W-69]]'s water fixes (gear sharing a run 099c9d38, switches 2e885c9f); the [[W-73 Fishing, hunting and their materials developed together|W-73]] wave (23 Nov: [[W-97 Build stage 1, the basis in code|W-97]] to [[W-104 Build the after-runs list from live run 1|W-104]]) | 34 |

### 7.1 New ad hoc system, built into a general one, or generalising one

| Kind | Examples (date, commit) |
|---|---|
| **New ad hoc system** | the water bodies as aliased records (17 Nov, b3f2ef81): a new space kind with no kind registry to put it in; the climate beside the hand-written spells (8 Nov, a0bbdd53): a second path kept for old worlds, never retired; the water's own module (23 Nov, 07eec413): water types as 7 column tables with no row; willow (23 Nov, eff4c7e9): its own K table, seeder and rule, with branches in the night's driver; the river's signs by named kinds (23 Nov, ada5c3a4); the snare's untended night (23 Nov, 653737c4); the gate check's makings by named crafts (23 Nov, eff4c7e9, 0012b5ea) |
| **Built into an existing general system** | the wild kinds as RESOURCES rows, "one registry" (9 Nov, 9d418ff2); the wild plants as RESOURCES rows on the `seasonal` rule (9 Nov, 8b4379d4); loads and sites as rows with their own fields (9 Nov, 7eac5da0); the runs "as a rule over any kind with a RUNS row" (16 Nov, 55f41aa3); the shallows as a RESOURCES row and a renewal rule (23 Nov, 07eec413), though its context came by a branch |
| **Generalised and extended one** | the renewal registry (7 Nov, 92cfdbf6, [[D4-104 Renewal and packs; each stock its own rule|D4-104]]: "regime is now renewal ... a stock's own record may name its renewal rule and its response to density"); the methods (9 Nov, 6e527209, [[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]]: "general methods with take tables generated from the kinds' traits", replacing per-kind hunts); the weather scheduler feeding every reader at its place (8 Nov, a0bbdd53, [[D4-111 Every weather query names its place|D4-111]], [[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]); gear sharing a run in one rule for weirs, the race and set traps (20 Nov, 099c9d38, [[W-69 Nutrition worlds|W-69]]) |

### 7.2 The trend: getting worse

Named branches per 100 lines standing, by when the line was written (`a_dated.py`):

| Period | engine/ files of the area | wild/ | landgen/ |
|---|---|---|---|
| 23-31 Oct | 0.72 (15 in 2,095) | | |
| 1-8 Nov | 0.73 (8 in 1,100) | | 5.08 (169 in 3,327) |
| 9-14 Nov | 0.87 (24 in 2,756) | 1.18 (24 in 2,026) | 10.94 (21 in 192) |
| 15-19 Nov | 3.35 (22 in 657) | 0.36 (2 in 557) | 7.30 (10 in 137) |
| 20-24 Nov | 3.52 (33 in 938) | 3.89 (48 in 1,234) | 3.83 (17 in 444) |

The engine and wild code held below about 1.2 named branches per 100 lines until 14 Nov; from the river (15 Nov) and in the wave it
is 3.4 to 3.9, three to five times higher. The generator was always high (its catalogue is by name, legitimately, §3), and its newer
lines (the gate check) are lower than its first. The wave's own new modules: `water.py` 15 in 216 lines (6.9), `willow.py` 7 in 73
(9.6), `river.py` 19 in 508 (3.7), against the wild layer's first modules `runs.py` 3 in 437 (0.7), `ecology.py` 15 in 514 (2.9),
`methods.py` 4 in 359 (1.1). **Worse**, and the turn is datable: the first two weeks generalised (renewal, methods, the scheduler),
the river added gear by name (`is_weir`, the robbers' `trap in water`), and the wave added water types and gear behaviour by name.

### 7.3 Which went ad hoc because the general system could not be extended, and which need not have

- **Forced (the primitive lacked an extension point):**
  - the shallows and willow rules (23 Nov): a renewal rule is `rule(p, res, ctx) -> S` (`renewal.py:4-6`); it cannot ask for context
    (iced, the first night of spring, beasts on the parcel) or change K, so the driver branches on the rule's name and writes K itself
    (`night.py:645-655`);
  - the water bodies (17 Nov): no space kind could hold a stock for several parcels (feature_packages §2.1, §2.6 unbuilt), so the
    record is aliased;
  - the woods' rules (24 Oct, still): the young growth needs the grazed parcels and the dead wood the trees' S, which the registry
    could not pass, so `forests.night` calls the rules by name with its own context (`forests.py:80-89`);
  - the climate's fallbacks (8 Nov): a driven layer with no declared fallback keeps the spells as a second path.
- **Avoidable (the general system could have been extended):**
  - water types as column tables (23 Nov): RESOURCES, COVERS and FORESTS show the row form; the design (u1 §2, §4, its file table at
    `u1_water.md:242`) specified the dicts, and the build followed it;
  - set gear's ice by a technique tuple (`wild.py:1016`, 23 Nov, 653737c4) on the day the edge techniques got an `ice` property in
    their rows (eff4c7e9);
  - SET_HOLD_KG (`wild.py:920`) beside the method rows' own `set: {holds}` and WATER_WORKS trap `hold`;
  - GEAR_OF in the gate check (`gates.py:144`) though every set method has a `gear` field (empty);
  - `game` kinds listed twice in the switches (`switches.py:24`, `:97`) though the kinds carry traits;
  - the river's signs by named kinds (generality.md: "a new run kind passes unseen") though the RUNS rows hold the windows.

### 7.4 What in the process let the ad hoc in (Zach's addition 3)

- **The design set prescribed the shapes.** u1 specified `SHALLOWS`, `ICE`, `RUN_REACH`, `FEN_WRECK`, `THAW_WRECK`, `PINCH` as dicts
  keyed by water type in `kinds.py` (`u1_water.md:146-152`, `:242`), and the build did exactly that. No design rule said a new
  category's properties go on its rows.
- **The feature-unit rule asked for grouping, not properties.** [[D2-244 The engine's reworking into feature packages|D2-244]] ("its data, verbs, signs and processes listed together",
  `build_plan.md:10-12`; `u1_water.md:258`, `u2_taking.md:288`) was met by putting the tables and functions in one module
  (`water.py`'s header names its unit); a unit of named branches passes it.
- **The stage tests are behavioural.** The build plan's acceptance per stage ("set needs gear in hand; a piece wears and is mended",
  `build_plan.md:25`) checks what happens, never how: nothing failed on a new branch on a name. [[D2-353 Everything new in the engine is built within the agreed architecture…|D2-353]]'s guard test is the missing check.
- **The reviews checked citations and numbers.** `build_plan.md:13` ("every file:line a spec cites is checked against the code") and
  the calibration reviews ([[W-108 The waters calibrated across many generated environments|W-108]]'s generality.md is the first that asks "general or fitted?", after the wave).
- **No registry check.** With no required fields (§5), a side table is as valid as a row field, and nothing assembles or checks a row.
- **Speed and one test world.** The wave built four stages in one day (23 Nov) against Eelmouth; a branch on a name passes every
  test on one world (build_gaps.md: "what is missing is mostly what Eelmouth did not need").
- **The primitives' missing extension points** (§7.3) made the branch the only fast way for some features: [[D2-354 The architecture is a healthy balance, not a strict one|D2-354]]'s warning, seen.

## 8. The verdict in [[D2-354 The architecture is a healthy balance, not a strict one|D2-354]]'s terms

**Where a general primitive should own the behaviour:**
- stocks and their renewal (one registry, rules as rows of a few shapes, the clock declared);
- habitat and seeding (one seeder, a `habitat` block on each resource row);
- takes from a population (one take, §2.3's draw-out and return);
- couplings and hazards (effect rows and hazard rows over one interpreter);
- transitions of kind or state (3c widened);
- the condition vocabulary over the driven layers (one registry, keys with readers);
- the categories themselves: every cover, water type, forest kind, wild kind and set method a whole row, checked at load.

**Where a system legitimately owns its specifics** (and how to keep them inside it):
- **the food web** (`ecology.step`): its eating, condition and breeding are its own dynamics (P3). Keep its specifics in its kinds'
  and foods' rows (the named foods at `ecology.py:257-265`, `:319` become FOOD properties) and its code in `wild/ecology.py`; meet the
  rest only through draw-out and return and the coupling rows;
- **the runs' network** (`runs.py`): its movement and cue are its own. Keep the kinds' specifics on the RUNS rows (window, cue,
  direction, return), the water's on WATER_TYPES, and let gear meet it only through the take primitive and `share_run`;
- **the climate** (`climate.py`): a driven layer with its own tables. Keep it a pure layer; every consumer reads conditions through
  the registry, never the climate's internals;
- **the generator's catalogue** (`landgen/ecology.py`, `settle.py`, `names.py`): terrain to ecosystem to cover is its own rule set,
  by name. Keep it in `landgen/`, and let it write only rows' values the engine reads (habitat K, the land block), never parallel
  numbers (PER_UNIT grass beside the cattle table).

**The extension points the primitives need** (so new features extend them, not bypass them):
- the renewal rule: declare its context keys (each a condition-registry key: `iced`, `grazed`, `first_of_season`) and return a dict
  of changed fields (S, K), not S;
- the stock row: `habitat`, `clock`, `class`, and the effect and hazard lists;
- the condition registry: a package registers a key with its reader (the runs register `spate`, the water `ice`);
- the set method's row: `in_water`, `hold_kg`, `untended`, `draws_open`, `wreck`, read by the gear's night;
- a space kind registry (feature_packages §2.1) so a body, an area or a stretch can hold a population;
- a registry check at load that names the required fields of each category and fails on a misspelt or missing one.

**From the history:** the shallows and willow rules (23 Nov), the water bodies (17 Nov), the woods' rules (24 Oct) and the climate's
fallbacks (8 Nov) went ad hoc **because** the general system could not be extended; the water types, set gear's ice, SET_HOLD_KG,
GEAR_OF, the switches' classes and the river's signs by kind went ad hoc **though** it could have been, by the row form already beside
them. The first are fixed by the extension points above; the second by the [[D2-353 Everything new in the engine is built within the agreed architecture…|D2-353]] guard and a design rule that a new category is a
table of rows.

Current as of 24 Nov 2026 (6b609f48).
