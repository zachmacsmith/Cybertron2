---
id: docs/review/37_growth/02zzzh_hunt_fish/engine_audit.md
kind: note
updated: "2026-11-21"
---
# The inside view: hunting, fowling, fishing and their materials as the engine and the records hold them (21 Nov 2026)

*note · `docs/review/37_growth/02zzzh_hunt_fish/engine_audit.md`*


21 Nov 2026, 37.2 (subagent). Thread: fishing, hunting and their materials developed together ([[W-73 Fishing, hunting and their materials developed together|W-73]]), under the nutrition worlds
([[W-69 Nutrition worlds|W-69]]). Companion to the four research notes on the real ladders (fishing; hunting and fowling; fibre and cord; withies and wood
materials) in this folder. No code changed.

Zach (21 Nov): "recalibrating the fishing / hunting signs and mechanisms alongside the relevant parts of the economies and
resources, including stuff like withies and cords, exploring the different potentially relevant techniques, capital, each of the
resources and little relevant capital or supply chains."

**Read with:** the river's signs audit, [02zzz2](../02zzz2_river_signs_audit.md) (every state of the water and what reaches a
person; this note does the same for game and fowl, more briefly, and does not repeat the river); the fishing methods compared,
[02zzy2](../02zzy2_fishing_methods_compared.md); the food values applied, [02zzu_lookup.md](../02zzu_lookup.md) "Applied".

**Sources:** the code on main as of 21 Nov (file:line below): `cybertron2/engine/data.py`, `wild/methods.py`, `wild/kinds.py`,
`wild/gear.py`, `wild/runs.py`, `wild/switches.py`, `engine/wild.py`, `verbs.py`, `knowledge.py`, `perceive.py`, `signs.py`,
`keeping.py`, `farm.py`, `packs.py`. The records through `tools/records.py show` and `find`; the proposals named in §2.

## The short answer

- **What exists.** About 35 goods, 45 techniques and modifiers, nine fittings and works, and 14 taken kinds touch hunting, fowling,
  fishing, the kill and wood. The wild layer's seven take methods (hunt the wild, stalk, drive, snare, net, trap in water, den
  work) are generated from the kinds' traits; the river has the runs, the weir in sections, the gap and the mill; keeping has the
  hearth rack, the smokehouse and salting.
- **Gear is almost absent.** The only hunting gear is the crude weapon (one timber). Snares, wicker traps and nets cost nothing
  to set, are not goods, and leave nothing behind. The rod is the only fishing gear, and it is never worn. No withies, poles,
  bark, cord, fibre, leather, bone, sinew, feathers or fur as such exist. "Wattle" is costed in timber everywhere.
- **The kill arrives dressed.** A kill gives meat and a hide (none for a hare or a bird), a quarter of its meat left as offal; no
  butchering, no skill in it, no tallow, bone or antler from a wild kill. Fish arrive gutted.
- **What was designed and benched.** The materials and gear stages of the economy web (butchering, leather and tan pits, bark,
  withies and poles, cord, bone and antler, fur; line and hook, traps, nets, the spear, snares of cord) are the hunting and
  resources build ([[L-111 The hunting and resources build, a soon follow-up|L-111]]), benched twice by Zach (16 Nov) and now [[W-73 Fishing, hunting and their materials developed together|W-73]]'s. Traps as a good were decided in the tool set ([[D2-23 The tool set|D2-23]]) and
  costed (recipes.md: 1 timber, 0.25 hide, 20 nights) but never built. Nets wait on fibre ([[L-13 Economy options kept out of the first worlds|L-13]]). Wildlife packs K3 and K8 ([[L-117 Wildlife pack K3 forays, methods and knowing|L-117]],
  [[L-121 Wildlife pack K8 crafts and wild goods|L-121]]) hold cord, nets, bows, tanning, horn, bone, furs and feathers.
- **The hunter's signs.** Game near the fields is shown well (traces, raids, leaders, seasons). Game in the wood is shown mostly
  while one hunts it, two lines a trip, and through seven presence rows at the village that leave out the hare, the roe, the
  pigeon, the fowl, the fox, the stoat and the otter. The one sign of hunted game, "hunted too often here", fires on the day
  learned wariness crosses a line, which for deer and boar is usually the day of the first kill; it names every kind the method
  could take (so "the salmons break and run" after netting the river), and is never shown again. The expert's "wary from the
  hunting" reads a different number (the short-lived pressure), not the wariness that makes game hard to find.

## 1. The engine as built

### 1a. Goods

`engine/data.py` ITEMS (line in brackets). Weight in the game's units; food in meals a unit (2,500 kcal, [[D2-258 The food values are put on one physical basis|D2-258]]); spoil a night
in hand.

| Good | Weight, food, spoil | Life | Made or got by | Used by | Notes |
|---|---|---|---|---|---|
| meat (61) | 1, 0.6, 0.30 | | kills, slaughter, gather young | eating; dry, smoke, salt meat | 1,500 kcal a unit; raw 0.32 |
| drying meat, dried meat (92, 31) | 1, 0.6 / 1.2, 0.15 / 0.02 | | dry meat (hearth or fire ring rack) | eating | half weight, same food |
| smoking meat, smoked meat (94, 95) | 1, 0.6 / 1.2, 0.15 / 0.005 | | smoke meat (smoke racks) | eating | |
| salt meat (93) | 1, 0.57, 0.003 | | salt meat: 4 meat + 1 salt | eating | 0.95 x meat |
| offal (96) | 1, 0, 0 | | left with a kill: 0.25 of its meat (`THINGS.carcass_offal`, data.py:946) | nothing: rots, draws the wild | no bait, no dog food |
| rotting meat (111) | 1, 0, 0.3 | | fresh meat in the open | nothing | |
| hide (89) | 1, 0, 0 (decays in the open: DECAY abs) | | slaughter (2 a cow, 1 a young beast), wild kills (1; bear 2), the legacy hunt (1 in 4) | bedroll 1, tent 3, harness 1, pack 1 (transport), anvil fitting 2, fishing rod 0.1 | one good for a cow's hide, a deer's skin and a fox's, otter's or wolf's pelt |
| tallow (90) | 1, 0, 0 | | slaughter only (4 a cow, 1 a young beast) | tallow lights | none from a wild kill; food 0 by choice ([[L-107 Tallow's real uses|L-107]]) |
| tallow light (98) | 0.2 | | make tallow lights: 1 tallow -> 4 | night work at a load, x1.3 (`kinds.LIGHT`) | |
| antler (82) | 1 | | found: a cast antler, 0.15 chance when hunting near red deer in early spring (kinds.py:421) | make a horn | no antler from a killed stag |
| horn (85) | 0.5 | | make a horn: 1 antler, 2 units | a scare in a field watch | a horn to blow, not horn the material |
| beaver pelt, castoreum (83, 86) | 1, 0.2 | | den work at a lodge (the site's trap, kinds.py:488) | nothing | the only fur as its own good |
| clappers (84) | 0.5 | | 0.5 timber | a field watch | |
| fish (49) | 1, 0.46, 0.30; x2 in a store | | trap in water, the weir, net, fish by hand, angle, run take | eating; salt, dry, smoke fish | 1,150 kcal, about 1 kg gutted and headed |
| salt fish (50) | 1, 0.46, 0.01 | | salt fish: 4 fish + 1 salt, 1 unit | eating | |
| drying, dried fish (57, 58) | 1, 0.46 / 0.92, 0.15 / 0.02 | | dry fish (rack, up to 8) | eating | [[D4-122 Fish on the hearth rack|D4-122]] |
| smoking, smoked fish (54, 55) | 1, 0.46 / 0.92, 0.15 / 0.005 | | smoke fish (smoke racks, up to 40) | eating | |
| salt (33) | 1 | | salt pan (saltmarsh), boil salt (brine pan) | salting, cheese | |
| fishing rod (51) | 1 | life 30, **never worn** (§3) | 0.5 timber + 0.1 hide, 1 unit, basic | angle (`uses`) | "a line of hair or gut" in its comment, hide in its recipe |
| crude weapon (104) | 1; weapon 2.0 | life 10 | 1 timber, 1 unit, basic ("club", "spear") | gear in hunt the wild x2, stalk x5, drive x6, den work x1.25; fights | worn only in the legacy hunt and in fights |
| crude tool, copper tool (102, 103) | 1 | 10, 40 | timber + stone; copper at an anvil | fell, cut, clear, fence, mine, quarry | the hand-tool grades; no knife, billhook or spade |
| timber (87) | 2; heat 2 | | fell: 3 a unit with a crude tool | every building, fence, weir, racks, gear | the only wood material |
| firewood (44) | 1; heat 0.5 | | dead wood 3 a unit by hand; young growth 5 a unit with a tool | fires, the smokehouse, boiling salt | "coppice" and "cut poles" are aliases of cutting young growth for firewood |
| charcoal (43) | 2; heat 6 | | 5 timber, a woodsman | smelting, a hearth | |
| pack, bedroll, tent, harness (105, 109, 110, 108) | | 60, 40, 30, 80 | hide with or without timber | carrying, camping, the pack ox | leather is hide here |

**Not in the engine:** withies, poles, rods (the material), bark, hurdles as a good, cord, twine, bast, nettle fibre, flax, hemp,
reeds, rushes, leather, sinew, gut, bone, feathers, down, fur by quality, fish oil, glue, a knife, a spear (other than the crude
weapon), a bow, arrows, hooks, a net, a snare or a trap as goods, a basket, a boat.

### 1b. Hunting and fowling methods

`wild/methods.py` METHODS (44 to 83), with the sets (86), sweeps (93), take bases (101); generated into TECHNIQUES at load
(`methods.build`, methods.py:181; called at data.py:1153). Each take table is built from `kinds.TRAITS` (kinds.py:843) by the
method's `needs` and `favours`, with at most one `taken.calibrate` a kind. All draw `wild`, give their goods by kind, `reads_as`
hunt, carry `wear` 0.3 (never applied: §3).

| Method | Who | Units | Where (covers) | Gear (x) | Takes (weight) | How it takes | Skill curve |
|---|---|---|---|---|---|---|---|
| hunt the wild | basic | 2 | forest, scrub, heath, moor, fen, pasture, meadow | crude weapon x2 | red deer, roe, boar, hare, fox, stoat, wolf 0.99; bear, woodpigeon 0.33 | a search over the range's areas, sweep 1.0 km2 a unit; take_base 0.25 | hard, x1 to x8 |
| stalk | untaught tryable | 3 | forest, scrub, heath, moor | x5 | red and roe deer 2.5; boar 0.3 | sweep 0.4; take_base 0.06 | hard |
| drive | known only; crew; led by the household head (seed) | 4 | forest, scrub, fen | x6 | boar, wolf 3.0; red deer 0.45 | sweep 2.0; take_base 0.1; x(1 + 0.25 a member past the first) | hard |
| snare | basic | 1 | pasture, meadow, heath, field, scrub, **water** | none | hare 3.0; fox, stoat, **otter** 2.0; roe 0.06 | a set thing: a line of 5, 4 nights, 1 head each, meet 0.08 | basic, 1.0 to 1.5 |
| net ("netting birds with nets and decoys") | untaught tryable | 2 | fen, water, meadow, saltmarsh | none | wildfowl, **salmon** 3.0; woodpigeon 0.2 | a search, sweep 0.3; take_base 0.25 | trade, 0.5 to 2.0 |
| trap in water ("wicker traps") | untaught tryable | 1 | water, fen | none | eel, lamprey 3.0; wildfowl 0.3 | a set thing: 1 trap, 8 nights, 20 heads and 10 kg (data.py:388), meet 0.3; EEL_NIGHTS x2, x3 where no river runs (methods.py:41) | trade |
| den work | known only | 3 | forest, scrub, heath, pasture, meadow | x1.25 | fox, stoat, wolf, bear 4.0; cubs with a vixen in spring | sweep 3.0; at a lodge, the site's trap (beaver pelt, castoreum) | trade |
| gather young | known only (seeded by a colony at the village) | 1 | forest, scrub | | a heronry (0.37 meat a head, up to 4) or rookery (0.11, up to 10) in spring | the site's own take | |
| break a dam | untaught tryable | 2 | forest, scrub, meadow | | the beavers' dam | site work | |
| hunt (legacy, off with the wild pack) | basic | 2 | forest | weapon none 0.3, armed 1 (worn 0.3 a use) | the parcel's `game` stock | chance 0.35 of 5 to 15 meat, a hide 1 in 4 (data.py:417) | |

**Hunting modifiers** (data.py:505 to 526, 1115): range near (0 units), the wood around (+1), far (+3); hunt with, hunt alone,
hunt only with; looking for (a kind or sort; x3 on it, x0.4 on the rest); lead on the hunt (a pack ox with a harness to carry the
kill). Carry binds: 10 on foot, +10 a pack, + an ox (`wild.carry_of`, wild.py:2222).

**The take** (`wild.hunt`, wild.py:2285): meetings ~ Poisson over the kinds' density x detect x the kind's effects x familiarity x
focus x the method's table weight / (1 + 0.5 x pressure) / (1 + 1.5 x learned wariness) x ground searched x 0.21; each met is
taken at 1 - e^(-take_base x skill x gear x (1 - flee) x familiarity) (wild.py:2252), flee raised by wariness; danger (boar,
wolf, bear) wounds or kills the one in front; a kill dressed where it fell into meat and hide, shared to each one's carry, the
rest and its offal left as a carcass (near) or carrion (further).

**Sets** (`wild.set_work`, wild.py:909; `_set_night`, wild.py:921): a container `kind: set` with `{method, life, base, line,
holds}`; no inputs, no gear, no materials; once a night it draws on the kinds in the village's home area (and half the ring) at
the setter's skill; a catch becomes the kind's goods inside it, kept alive for fish ([[D2-211 Fresh fish keep as meat in hand, and alive in a trap or a weir until…|D2-211]]); spent after its life (`sprung`), and
nothing is returned or reusable. A run passing is drawn on in the river's night and shared with the weir by kg (gear.py:172).
Otters rob unwatched traps holding fish (wild.py:3185). Lifting is a `take` from the set (verbs.py:1608, 1813).

### 1c. Fishing, the river works and keeping

| Row | Who | Inputs, units | Where | Gives | Notes (file:line) |
|---|---|---|---|---|---|
| fish by hand | basic | 1 unit | water | resident `fish` stock 0.6 a unit at full, spread 0.5; and the run passing (`run: True`) | refused before the run is reached where no resident stock (knowledge.py:207; [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]) (data.py:597) |
| angle | basic | 1 unit, a rod to hand | water | resident stock 1.5 a unit | never takes from a run (no `run`); the rod is not worn (data.py:601) |
| fishing rod | basic | 0.5 timber, 0.1 hide, 1 | anywhere | a rod | (data.py:605) |
| weir (monument) | **basic** (known to all, [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]) | first wattle section 12 timber, 24 units, crew 2 | a river water parcel | 30% of a run passing (first), 7% each added, up to 3; holds 100 kg, 70 each added | sections, gap, wear by flow and ice, mending 6% a level (data.py:345, 376; gear.py) |
| the gap | anyone who works the weir | 2 units shut, 1 open | the weir | shut: traps in, takes; open: 0.1 of the share | (data.py:389; verbs.py:120) |
| water wheel's gap | the mill | | the race | a trap in the race takes half an eel run down; shut holds half a run up | (data.py:391) |
| salt fish, salt meat | basic | 4 fish or meat + 1 salt, 1 unit | anywhere | 4 salt fish or meat | 4 kg a unit; [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]] open (10 to 100 times too slow) (data.py:639, 641) |
| dry fish, dry meat | basic | up to 8, 1 unit | hearth or fire ring rack | half the weight over 3 nights | one batch a rack (data.py:643, 647) |
| smoke fish, smoke meat | basic | up to 40, 1 unit; tend 1 unit a day; about 1 firewood a night | smoke racks in a building of their own | half the weight over 3 nights | a wattle smokehouse catches fire 2% a night (data.py:623 to 638; PHYSICS smokehouse, data.py:835) |
| salt pan, boil salt, mend the brine pan | basic; salter | sun 1 a unit by season; 4 firewood -> 4 salt | saltmarsh; a brine pan at a spring | salt | (data.py:607 to 621) |

### 1d. The kill and its by-products

| Kind (kinds.py TAKEN, 631) | Goods a head | Food a head | Uses in its row (KINDS) | Missing from what a kill gives |
|---|---|---|---|---|
| red deer | 33 meat, 1 hide | 19.8 | venison, hide, antler | antler, tallow, bone, sinew |
| roe deer | 8.1 meat, 1 hide | 4.9 | venison, hide | |
| wild boar | 29 meat, 1 hide | 17.4 | pork, fat, hide | fat (tallow or lard) |
| brown bear | 121 meat, 2 hide | 72.6 | great pelt, fat | fat; the pelt is two "hide" |
| brown hare | 1.25 meat | 0.75 | meat; coursing | the skin |
| woodpigeon | 0.15 meat | 0.09 | | feathers |
| wildfowl | 0.56 meat | 0.34 | meat, feathers, down | feathers and down |
| fox, stoat, otter, wolf | 1 hide | 0 | pelt; ermine; pelt; pelt, bounty | the pelt as fur |
| eel, salmon, lamprey | 0.58, 3.06, 0.19 fish | 0.27, 1.41, 0.09 | food that keeps; rent; the lord's table | gutting work, oil |
| herd beasts (slaughter, data.py:548) | cow 150 meat, 2 hide, 4 tallow; ox 210; young 48, 1, 1 | 90; 126; 29 | | bone, horn, sinew, offal as food |

A slaughter is a `work` of 2 units on the herd's parcel; a wild kill is dressed in the hunt itself at no further work. There is no
butchering or gutting act, no skill in it, and no share of a carcass lost to poor dressing.

### 1e. Wood materials

| Row | Who | Draws, units | Gives | Notes |
|---|---|---|---|---|
| fell (data.py:421) | basic | trees (`wood`); 2 units; bare x0.25, crude x1, copper x2; tool wear 1 | 3 timber | leaves 1 firewood of brash as dead wood a timber (FORESTS brash) |
| firewood (424) | basic | dead wood (`dead`, a pool) | 3 firewood a unit | no tool |
| cut (434) | basic | young growth (`young`); crude x1, copper x1.5 | 5 firewood a unit | aliases "coppice", "coppicing", "cut poles"; young growth is a stock with its own regrowth by forest kind (FORESTS, data.py:207: a managed wood 400 young a unit of size, regrow 1.0) |
| charcoal (655) | woodsman | 5 timber, 2 units, at a forest | 1 charcoal | |
| "wattle" in costs | | | | a small wattle room 8 timber (data.py:292); a wattle fence 4 timber x the square root of the size, 10 units (FENCES, data.py:966); a wattle weir section 6 timber (380); smoke racks "hurdles" 2 timber (275); the weir's "wicker traps" nothing |

The deer's bark-stripping (RAID_SIGNS bark, kinds.py:378) and the sign "the coppice regrowth will die back" refer to a coppice the
engine does not have as a state (no panels, no rotation, no cycle: [[L-120 Wildlife pack K7 land works and infrastructure|L-120]]).

### 1f. Fittings and works that host this capital

| Fitting or work | Materials, units, who | Does | Wear |
|---|---|---|---|
| smoke racks (data.py:275) | 2 timber, 2 units, basic; 3 spaces; a building apart | a batch of 40 smoked over 3 nights | none (the building can burn) |
| hearth, fire ring (237, 248) | stone | one rack of 8 | |
| brine pan (278) | 1 copper, 2 timber, 4 units, salter; at a brine spring | boiling salt | 60 boilings, mended with 0.25 copper |
| woodshed (270) | 2 timber; a lean-to | 40 timber or firewood kept dry | |
| anvil (254) | 6 stone, 2 hide, 1 timber, smith | the smithy's bellows | |
| weir (345; WATER_WORKS 376) | sections: wattle 6 timber 16 units, timber 10 and 25, the first section +6 timber +8 units; a stone footing 10 stone 15 units | the river's take; its traps hold the catch | Poisson wear a night by material, water, flow, gap, ice; mend 0.06 of a section a level |
| owl hole (240) | 1 timber | a barn owl against mice | |

### 1g. Yields a unit of work now

From [02zzu_lookup.md](../02zzu_lookup.md) "Applied", after [[D2-258 The food values are put on one physical basis|D2-258]] (food a unit of work), with the live runs of 02zzy2 and the bots
of [[W-64 Food, weight and work on one basis|W-64]] where they measure what the table does not.

| Method | Food a unit | Real range (02zzu part 1) | Source and reading |
|---|---|---|---|
| hunting, novice armed, near | 0.14 to 0.21 | 0.08 to 0.32 | Applied; never pays, as in life |
| hunting, capable armed, near | 0.50 | 0.4 to 1.2 | Applied |
| hunting, master armed, near | 1.74 | 1.2 to 3.2 | Applied; under the ploughman (2.35), as [[D2-258 The food values are put on one physical basis|D2-258]] asks; no figure yet for [[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]]'s far trips |
| snares, lifted (hares) | 0.64 | 0.4 to 1.2 | Applied; the runs world's snares 48 to 84 food a run (02zzy2) |
| netting fowl (2 units) | 0.08 to 0.52 | 0.24 to 2.2 | Applied; live nets at the river took nothing from 48 salmon (02zzy2) |
| gather young (heronry; rookery) | up to about 0.9; 0.66 | | from the site rows (4 x 0.37 meat; 10 x 0.11), in spring only |
| legacy hunt (full stock, armed) | 1.05 | 0.4 to 1.2 | Applied |
| fishing by hand (full resident stock) | 0.28 | 0.16 to 0.72 | Applied; 0 where no resident fish (refused) |
| angling | 0.69 | 0.24 to 1.4 | Applied |
| wicker traps (live, the runs world) | about 0.18 to 0.31 | 0.16 to 1.2 | 02zzy2 (sets and lifts); the fishing bots 0.53 to 0.84 a unit of fishing ([[W-64 Food, weight and work on one basis|W-64]]) |
| the weir, one wattle section, a year | 1.24 to 8.09 by station | | Applied, on recorded pulses; 5.7 food a lift in the high arm (02zzy2) |
| farming, hoe to plough | 1.37 to 2.80 | 1.2 to 6.0 | for comparison |
| milking | 4.6 | 6.4 to 11 | [[D2-260 Milking at its real yield|D2-260]] |

What a catch costs to keep (no mechanic added since): salting 4 kg a unit; a smokehouse batch of 40 for 3 nights, tended daily; a
rack of 8; fresh fish lose 0.30 a night in hand, 0.60 in a store.

### 1h. The hunter's signs: every state of the game, and what of it reaches a person

As 02zzz2 §1 did for the river. "Practised" means a technique in `perceive.practised` (perceive.py:289): any wild method known at
"known" (all `reads_as` hunt, so a trapper or a netter reads the hunter's signs), or a basic one practised past its novice
start; "expert" a method's top fifth, or a kind at familiarity 0.6 (`familiar:{kind}`).

| State | Where it lives | How fast it changes | What reaches a person now |
|---|---|---|---|
| **A kind's numbers round the village** | `wild.state.pop[kind]` by area (density a km2) | daily | **At the village:** `_wild_presence` (signs.py:2000): the highest PRESENCE row (kinds.py:604) for **seven kinds only** (voles and mice, owls, rats, wolf, wild boar, red deer, raven), at the village's first forest, scrub or heath parcel, own 0.5, read lay, knows or expert. No presence row for the hare, roe, woodpigeon, wildfowl, fox, stoat or otter. **While hunting:** `_notices` (wild.py:2608): HUNT_NOTICES (kinds.py:572) for ten kinds, at most two lines a trip, "On the way you saw ...", the expert's line with "about {n}" for one familiar with the kind; remembered of the place ("hunting from here you saw ...") |
| **Condition and hunger** | `state.cond` by kind and area | daily | Only in an expert's hunt notice ("fat and in good fettle", "lean"; hunger for wolf, fox, bear) |
| **Groups near people** (boar, deer, wolf, fox; pigeons and hares at the crops) | `wild.groups`; traces on parcels | nightly | The richest bundle in the engine: edge, raid, turned and tried traces (SIGNS, kinds.py:206; EXPERT_SIGNS 381; RAID_SIGNS 369), by sight, sound and smell, at night and in snow, the leader's rows (LEADERS 511), the watcher's own night; eaten crops and stores (EATEN_SIGNS 552) |
| **Seasons and phases** (rut, calving, farrowing, antlers cast, roe kids, wolf pups, dispersal, fox cubs, the bear's hungry spring) | `kinds.WHEN` conditions | the day a row starts | `_wild_when` (signs.py:2241), at the village's first forest or scrub parcel, mostly knows or expert. Nothing for the hare's or the pigeon's year; nothing that the summer leaf hides deer (detect 0.8) |
| **Snow** | the weather; detect x1.5 for deer and boar | daily | Snow traces at the edge; "the first lying snow: the deer will be down at the ricks"; nothing says the wood is easier to track in |
| **The mast** | `state.mast` | yearly | MAST_SIGNS (kinds.py:559): flowering, frost, fallen; the boar's bare years (REGIMES) |
| **Pressure** (a hunt's disturbance: game leaves the area, `HUNTED.flee`; meetings / (1 + 0.5 x pressure)) | `state.pressure` by kind and area; x0.75 an engine day (ecology.py:472) | fast | Only as the expert's words "wary from the hunting" or "a little wary" (`_state_words`, wild.py:2596, reads pressure against WARY_WORDS, kinds.py:598). Nothing says the deer have left the wood, or come back |
| **Learned wariness** (detect / (1 + 1.5 x learned), flee raised; half-life 32 days) | `state.wary` by kind and area (WARY, kinds.py:826) | slow | One line, "the {kinds} break and run long before you are near: hunted too often here" (signs.py:2375), for the practised, at the parcel hunted from, **only on the day `learned` crosses 0.3** (wild.py:2211, 2507). Never again while it stays high; nothing as it fades |
| **A wounded beast** | `state.wounded` | days | WORK_NOTICES hunt: the boar's blood trail (kinds.py:424), boar only |
| **Legends** | `wild.legends` | rare | expert rows and the elders' tale |
| **Carrion and kills by predators** | `state.carrion`; carcasses | days | ravens over the wood (RAVENS_OVER); a predator's kill read by a hunter (KILL_READINGS, kinds.py:259) |
| **One's own kill** | the parcel's `hunted` record | that day and the next | HUNTED bundle (signs.py:441): gutting seen by others, the weight in one's hands, crows at the guts, blood in snow, the smell; only for a hunt in range near |
| **A hunt's outcome** | the result line | | "came on a red deer, but it got away"; "took it: 33 meat, 1 hide"; "came on nothing"; the carry limit and what was left. No word of the density met, the ground searched, or why (wariness, pressure, the season) |
| **Snares** | the set thing | nightly | the setter's look and a stranger's (as for traps, 02zzz2 §1a); `THINGS.set` conspicuousness (data.py:957) |
| **Wildfowl** | `pop.wildfowl` (a migrant, autumn and winter); the cold's push (OPEN_WATER) | daily | crowded on the last open water, the water frozen over, back with the thaw (kinds.py:357; signs.py:2379), the great freeze; "duck and geese on the open water" only while hunting. Nothing of the fowl arriving in autumn, leaving in spring, flighting at dusk, or a flight line; nets that meet nothing say "You hunted ... and came on nothing" |
| **Woodpigeons** | `pop.woodpigeon` | daily | "woodpigeons in flocks along the wood's edge" (hunt notice, knows); their raids on the crop when the mast fails (EATEN) |
| **Hares** | `pop.brown hare` | daily | "a hare going away over the open ground" (hunt notice, all, own 0.25); the expert's forms; no sign at the village and none of runs (where a snare goes) |
| **Otters** | `pop.otter` | | only after a robbery (02zzz2) |
| **Colonies and the lodge** | `wild.sites` | seasonal | SITE_SIGNS (kinds.py:490): back, gone, the dam, the pond |
| **What one knows of kinds** | the mind's `familiar` | slow | `familiar_line` (methods.py:250): "you know something of the brown hare, eel, fox, ..." with nothing behind it (02zzz2 §2) |

**What misleads or hides** (beyond the river's, 02zzz2 §2):

| Text or rule | Where | Why it misleads |
|---|---|---|
| "hunted too often here" on the first kill | wild.py:2499 to 2511 | A kill adds `WARY.take` 30 / the kind's heads in the area (wild.py:2436). In an area of under about 100 head of a kind one kill alone passes `WARY_SEEN`; a red deer or boar area usually holds fewer. So the sign usually fires the day of the first kill, not after hunting "too often" |
| "the salmons break and run" | signs.py:2071 (`_kinds_word`), 2362 | A hunt raises the wariness of **every kind in the method's take table** over the ground searched (wild.py:2345), met or not; the net's table holds salmon, so netting fowl at the river makes salmon "hunted too often". `_kinds_word` adds an s when the plural is the word itself |
| "wary from the hunting, lying up by day" | wild.py:2603 | Reads `pressure` (fades in days), not `wary` (half-life 32 days), so the expert's reading and the one sign disagree, and neither tracks what lowers the catch |
| A hunt with no catch | wild.py:2573 | "came on nothing" whether the wood is empty, the game wary, or the ground small; the hunter cannot tell thin game from shy game |
| The hunt's notices name what the land holds, not the hunted parcel | wild.py:2608 | Rows are for kinds counted over the areas reached; a hunt on a pasture can show "slots in the soft ground of the rides" |
| WORK_NOTICES' hunt group for any take | wild.py:406 | Setting a wicker trap or netting at the river can turn up "a cast antler lying in the leaves" or "a fox earth in the bank" (no cover check on those rows) |

**Seeded knowledge, hunters against farmers** (02zzz2 §3 for fishers): a household learns the take methods its land holds at
"known" and its members start familiar with their kinds at 0.35 an adult (`seed_by_land`, methods.py:270), so a hunter's line is
"you know something of the ..." and a list of methods. No lore line (LORE has sowing only, data.py:154): nothing of when the rut
comes, where the deer lie in winter, that one kill makes them shy, or what a kill gives beyond meat.

## 2. The design records

| Record | Status | What it would have built | Waits on | Superseded? |
|---|---|---|---|---|
| The tool set ([[D2-23 The tool set|D2-23]]), proposals/tools.md | decided 23 Oct; partly built | hand tools (built), the plough, carts, weapons (built), **traps as a good** (catch overnight while elsewhere; 1.6 units, timber and hide strips, about 20 nights), harness (built), saddle | traps: never briefed; the wild layer's sets took their place without the good | traps in part: by the free sets of [[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]]'s methods, never recorded as a replacement |
| Recipes (recipes.md §1, §6) | largely accepted | trap: 1 timber, 0.25 hide, 1 unit, the trapper's trade; wear 20 nights | as above | no; the trapper trade (spec production.md:167) has no row |
| Specialised tools ([[D2-48 Specialised tools|D2-48]]) | decided | felling axe, miner's pick, scythe, chisels, reaping hook, each a master smith's | the smith's recipes | no; no billhook or knife in its list |
| Weapons wear ([[D2-46 Weapons wear|D2-46]]) | decided, built for fights and the legacy hunt | a weapon on the one wear scale | | contradicted by the wild hunts (§4) |
| Options for later (economy_later.md; [[L-13 Economy options kept out of the first worlds|L-13]]) | deferred 23 Oct | nets (fibre), boats, metal-jawed traps, hide armour, flax, rope, cloth | fibre (02g §1f), clothing ([[D2-10 Clothing is parked|D2-10]]), iron ([[D2-19 First worlds start with a short metal ladder|D2-19]]) | nets in name: a `net` method exists without cord |
| The economy as a web (economy_web.md) | discussion 15 Nov; nothing decided | **stage 1 materials:** butchering and gutting with skill, leather and tan pits, bark, withies and poles from a coppice, cord from bast and nettle, bone and antler, fur, consolidations, the anvil, harness and pack taking leather, wattle taking withies. **Stage 2 gear and kept beasts:** line and hook, traps, nets, the spear, snares of cord; hens, cats, dogs. Stages 3 to 5: the water (built as brief 5), flax and retting, peat, the bow; the deer park, the warren | Zach's go on stage 1 (its question 1); the coppice as a rotation or a yield (question 2) | stage 3 is built (brief 5); stages 1 and 2 are [[L-111 The hunting and resources build, a soon follow-up|L-111]], now [[W-73 Fishing, hunting and their materials developed together|W-73]] |
| The hunting and resources build ([[L-111 The hunting and resources build, a soon follow-up|L-111]]) | deferred, open; "a soon follow-up" (Zach, 16 Nov) | economy_web stages 1 and 2, with withies and cord for fishing gear too ([[D2-209 Brief 5 (river and water) is built|D2-209]] answer 7) | Zach; now [[W-73 Fishing, hunting and their materials developed together|W-73]] | live: this thread |
| River and water, brief 5 (river_and_water.md; [[D2-209 Brief 5 (river and water) is built|D2-209]], [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]], [[D2-213 A set trap holds at most about 3 food a night|D2-213]], [[D2-216 Eels and salmon are fish|D2-216]], [[D2-218 Set traps in high water|D2-218]]) | decided; built on main (gear.py, runs.py, keeping.py) | the runs, the weir in sections, the gap, the mill, salt boiled inland, the smokehouse, the kinds on the water | its §5 left out the fen half (decoy pond, reedbeds), boats, the hunting economy, the fishpond, fishing-commons rules, retting and tanning | its numbers in part by [[D2-258 The food values are put on one physical basis|D2-258]] and [[D2-262 The runs at a real river's size|D2-262]] (§4); status line still "accepted for building" |
| Water and preservation (water_and_preservation.md §4) | discussion (7 Nov), "nothing to build" | a gear ladder: by hand, rod and line and a fish spear, wicker traps of withies (2 to 4 eels a trap a night), the weir, fowling nets (fibre), the seine (flax or hemp); reeds and peat (§5); boats (§8) | [[L-13 Economy options kept out of the first worlds|L-13]] (fibre), boats ([[L-53 Transport and traders, built out|L-53]]) | largely built as brief 5 and [[D4-119 Luck in a catch by hand or by rod|D4-119]] to [[D4-122 Fish on the hearth rack|D4-122]]; the spear, withies, nets of fibre, the seine, reeds and peat are not; its status is stale |
| Wildlife (wildlife.md; [[D2-192 The first wild kinds come in four waves|D2-192]] to [[D2-196 Hounds in wave 2, with the wolves|D2-196]]) | partly accepted, "Not built" | the kinds, what each gives (meat, fat, hide, fur, feathers and down, antler, castoreum), the ways to take them (stalking with a bow, a boar spear, snares of cord, traps for fur, fowling nets of fibre) | K3, K8 | the kinds and methods are built ([[D2-199 The wild layer is built on 37.2's own ecology branch|D2-199]], [[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]]); the goods and gear are not; its status is stale |
| Methods and encounters ([[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]], [[D2-207 The three wild build briefs are built|D2-207]]) | accepted, "to be built" | general methods, take tables from traits, skill in two layers | | built; status stale |
| Hunt calibration, brief 4c (hunt_calibration.md) | built and gated 14 Nov; awaiting Zach ([[Q-46 Brief 4c as built|Q-46]]) | baseline x multipliers; gear "later a hunting spear, a bow, nets and a dog each their own multiplier" (§3.1); snares lifted; tallow as food dropped ([[L-107 Tallow's real uses|L-107]]) | | built; the gear beyond the crude weapon is not |
| Husbandry (husbandry.md) | discussion 8 Nov | trades (warrener, fowler, woodward, basket-maker, tanner, rope-maker), chains (leather, withies, rope and nets), tools and gear in one list (§2d: snares of cord, wicker traps of withies, nets of cord, a boar spear) | Zach | no; its §2d is the nearest thing to [[W-73 Fishing, hunting and their materials developed together|W-73]]'s gear list |
| Wildlife packs K3 ([[L-117 Wildlife pack K3 forays, methods and knowing|L-117]]), K6 ([[L-119 Wildlife pack K6 keeping|L-119]]), K7 ([[L-120 Wildlife pack K7 land works and infrastructure|L-120]]), K8 ([[L-121 Wildlife pack K8 crafts and wild goods|L-121]]) | deferred, open; parent [[W-67 Extending the wildlife economy|W-67]] | K3: cord and the coppice's products, nets, bow and arrows, decoys and calls, stalking into the wind, hares' forms, flight lines. K6: dogs, the warren, purse nets, the fishpond. K7: coppice rotation and hedge-laying, rides, high seats. K8: tanning and leather, sinew, gut, glue, bowstrings, horn, bone and antler, furs by quality, feathers and down, oil | [[Q-32 02zv §6's decisions still open|Q-32]], [[Q-33 forays.md's open questions|Q-33]], the forays ([[L-105 Forays as their own track|L-105]]), the belief store, core C12, clothing ([[D2-10 Clothing is parked|D2-10]]) | overlaps [[L-111 The hunting and resources build, a soon follow-up|L-111]] and [[W-73 Fishing, hunting and their materials developed together|W-73]] wholly in cord, nets, leather and bone; not superseded |
| Tallow's real uses ([[L-107 Tallow's real uses|L-107]]) | deferred | candles, soap, grease | K8, evening acts ([[L-102 Acting at different times of the day, as one general system|L-102]]) | no |
| Livelihood archetypes (livelihood_archetypes.md; [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]) | discussion, scoping | the fisher ("from understanding nets to building a full weir"), the hunter-trapper (core snares and the hunt; specialist stalking, drives, den work) | [[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]], [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] | no; it replaces [[D4-121 A fishing household in the water worlds (a stopgap)|D4-121]]'s stopgap when built |
| A fishing household ([[D4-121 A fishing household in the water worlds (a stopgap)|D4-121]]) | decided, a stopgap | the largest household by fish knows nets and wicker traps | archetypes | to give way to [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] |
| The fishing bugs ([[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]) | ask, open | hand fishing refused in a run; set mistaken for lift; nets meet salmon and take none; the weir known to all; the Brook taken for Brook House | Zach | no |
| Signs of the river ([[W-72 Signs of the river|W-72]]; river_signs.md) | waiting on Zach's seven questions | the water's states as bundles; hand fishing that tells the truth; fishers seeded with the runs | Zach; then a brief with [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]], the shallows stock and [[L-111 The hunting and resources build, a soon follow-up|L-111]]'s gear materials | no; [[W-73 Fishing, hunting and their materials developed together|W-73]] would take its gear half |
| Seeded memory by livelihood ([[L-141 How much seeded memory each livelihood starts with|L-141]]) | deferred | how much each livelihood is seeded with | [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] | no |
| Salting rate ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]) | ask, default unchanged (23 Nov) | 40 fish and 10 salt to 40 salt fish a unit, gutting folded in | Zach | no |
| The rod's line ([[Q-57 Fishing, from the lake run|Q-57]] b) | closed into [[W-67 Extending the wildlife economy|W-67]] | a line of cord or hair as well as hide | cord or hair as resources | no |
| Food values ([[D2-258 The food values are put on one physical basis|D2-258]] to [[D2-262 The runs at a real river's size|D2-262]]) | decided, applied 20 Nov | meat and fish on their real energy; the runs at a real river's size; the gear's holds in kg ("a trap about 10 kg, a weir section about 100 kg on a peak night, nets when built"); keeping as the bind | | replaces [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]'s and [[D2-213 A set trap holds at most about 3 food a night|D2-213]]'s numbers without marking them (§4) |
| A skilled hunter's return ([[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]]) | decided | a master brings in a disproportionate amount, more on trips to other nodes; the limit is the game | | built in part: the master near 1.74 a unit; far trips not measured |
| Ladder of detail by familiarity ([[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]]) | decided [no spec] | every technique, fitting and build says what it does, by familiarity | [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] | no; the wild methods carry one `note` each, gear multipliers unsaid |
| Feature packages ([[D2-244 The engine's reworking into feature packages|D2-244]]; [[L-133 The engine as feature packages postponed, kept in mind|L-133]]; feature_packages.md §9, §10) | postponed, flagged | the engine cut into packages (`land`, `woods`, `wild`, `water`, `making`, `animals` ...) | Zach's go after [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] | no; every change keeps to its seams now |

## 3. The seams: where a new material or tool plugs in

| Seam | How it works now | What a richer chain needs of it |
|---|---|---|
| **A good** | an ITEMS row: weight, food, spoil, `decay`, `life`, `tool` (grade), `weapon`, `carry`, `seen`, `pack` (data.py:20) | withies, poles, bark, cord, leather, bone, sinew, feathers, pelts as rows; DECAY rows for those that rot (bark, hides in a pit); STORES kinds (data.py:325: `timber` takes timber and firewood) for poles and withies |
| **A recipe** | a `make` technique: `inputs` (alternatives as a dict; `batch` for up to), `gives`, `units`, `at` (covers, fittings, building), `basic` or `trade`, `untaught`; levels scale inputs (TRY, data.py:730) | twisting cord, weaving a trap or a hurdle, tanning; the existing rows (rod, crude weapon, bedroll, harness, tent, clappers, smoke racks) would take the new goods in place of timber and hide |
| **A tool a technique needs** | `tools` keyed by **grade** (bare, crude, copper), the best in hand chosen and worn by `wear` (verbs.py:726); TOOLS is sorted by `("crude", "copper").index` (data.py:157) | a knife, billhook, needle or spade is not a grade: it can only be a `uses` item or a `gear` multiplier. A new grade (bone, flint) breaks the TOOLS sort |
| **Equipment a technique needs** | `uses` {item: n}: checked to hand (`farm.team_shortfall`, farm.py:724), **worn only by ploughing and hoeing** (farm.py:1115) | the rod's 30 uses never run down; a net, a line or a trap carried as `uses` would not wear either until the wear moves to the technique handler |
| **Gear that multiplies a take** | a method's `gear` {item: x}: the best weapon, times every other item named (`wild.gear`, wild.py:2272); **not worn** (verbs.py:685 calls `WL.take` and applies no wear; parties.py none) | a spear, bow, dog, decoys or a net as gear rows; wear applied in `wild.hunt` per use |
| **A set work** | a container `kind: set` with `set` {method, life, base, line, holds}; its catch as goods inside plus a `catch` list; a wicker trap's hold in kg in WATER_WORKS["trap"] (data.py:388), its heads in SETS (methods.py:86); spent when its life ends; nothing returned | the set made from a carried trap, snare line or net (consumed, or kept and returned with wear on lifting); its hold from the gear; theft of the gear, not only of the catch |
| **What a method takes** | traits on the kinds (size, runs, social, home, water, mover), needs and favours on the method, one `calibrate` a kind (methods.py:165) | the gear's own reach: a net's mesh, a trap's throat, where it is set (a run, a flight line, a hare's run). Today a trait match lets the fowling net take salmon (a run is a "flock") and the snare take otters at the water |
| **Skill** | `curve`: basic 1.0 to 1.5, trade 0.5 to 2.0, the hunt's `hard` 1 to 8 (data.py:732; knowledge.py:41); familiarity by kind (methods.py:194) | net, trap in water and den work are on the trade curve, so a household that learns them from its land (`seed_by_land`, methods.py:316, at the curve's foot) starts at x0.5 of the bare novice's baseline; the generator's specialists start at 0.8 to 1.8 (generate.py:363). A craft of making gear (netting, basketry, tanning) would sit on the trade curve as making does |
| **Who knows it** | `basic`, `trade`, `untaught: tryable or no`; `seed_by_land` (methods.py:270); [[D4-121 A fishing household in the water worlds (a stopgap)|D4-121]]'s fishing household; the generator's trades (generate.py:363) | a basket-maker, netter, tanner or fowler as trades; seeding by archetype ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]) |
| **A building's or work's materials** | dicts on FITTINGS, ROOMS, BLUEPRINTS, MONUMENTS, FENCES and WATER_WORKS["weir"]["material"]; structure "wattle" is a cost row, not a material | "wattle" rows taking withies and stakes (poles); a wattle fence, room, weir section and hurdles of the same goods; the weir's traps as made traps |
| **A by-product of a kill** | TAKEN `goods` a head (kinds.py:631); slaughter `gives` by role (data.py:548); offal as a share (data.py:946) | a carcass to butcher (a `work` at a thing, as `bury` and `burn` are, data.py:708), its goods by skill; antler, bone, sinew, tallow, feathers, fur from the kinds' rows |
| **A wood's young growth** | FORESTS `young` stock with `regrow` by kind (data.py:207); `cut` draws it | withies and poles drawn from young growth (or a coppice state with panels, [[L-120 Wildlife pack K7 land works and infrastructure|L-120]]), firewood the rest |
| **A plant fibre** | none: wild plants are food rows (wild/plants.py) | nettle and bast as plant kinds with a non-food item; flax as a crop (CROPS) with retting as a rack-like process over nights |
| **Signs** | rows in kinds.py (SIGNS, WHEN, HUNT_NOTICES, PRESENCE, RUN_SIGNS), read by `reads_as` and familiarity | gear in a place seen (a net hung to dry, stakes cut); the guide's checklist (docs/cybertron2/guides/senses.md) |
| **Packs** | a row's `pack` (a name or a list), `off_with`; `packs.on` (packs.py:43); `wild` and `water` today; smoke meat, salt meat and the hide goods are in no pack | a materials pack, or rows in `wild`/`water` with a list (`["wild", "water"]`) for gear that serves both |
| **Feature packages ([[D2-244 The engine's reworking into feature packages|D2-244]])** | postponed; gear.py already declares its seams (data, verbs, signs, processes: gear.py:3) | [[W-73 Fishing, hunting and their materials developed together|W-73]]'s work written as its own unit with its rows, verbs, signs and processes listed; in the §7 cut it spans `woods`, `wild`, `water` and `making`, so it wants `requires` integration files (`with_woods.py`) rather than edits through verbs.py's technique hub |

## 4. Gaps and contradictions between the records and the code

| Where | The record says | The code does |
|---|---|---|
| [[D2-213 A set trap holds at most about 3 food a night|D2-213]]; spec/environment/wildlife.md:84; [[D2-216 Eels and salmon are fish|D2-216]] | a set trap holds at most about 3 food a night, about 15 eels | 10 kg (4.6 food), 20 heads (data.py:388; methods.py:86), by [[D2-258 The food values are put on one physical basis|D2-258]]; [[D2-213 A set trap holds at most about 3 food a night|D2-213]] not marked replaced, the spec not rewritten |
| [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]] | a weir section holds about 10 food a night, a full weir 30 | 100 kg the first, 70 each added (310 kg, 143 food), by [[D2-258 The food values are put on one physical basis|D2-258]] and [[D2-262 The runs at a real river's size|D2-262]]; not marked replaced |
| [[D4-122 Fish on the hearth rack|D4-122]] | dried fish food 2.0 | 0.92 ([[D2-258 The food values are put on one physical basis|D2-258]]); [[D2-216 Eels and salmon are fish|D2-216]]'s "a salmon about 2 food" against 1.41 |
| [[D2-46 Weapons wear|D2-46]] | weapons wear | the wild hunts never wear the weapon (verbs.py:685; only the legacy hunt, verbs.py:628, and fights) |
| [[D2-23 The tool set|D2-23]]; recipes.md; tools.md; spec/economy/production.md:86 and goods.md:37 | traps are a good (1 timber, 0.25 hide, about 20 nights, the trapper's trade, set at a forest site) | no trap good; snares and wicker traps are free sets of 4 and 8 nights on pasture, meadow, heath, field, scrub, water and fen |
| economy_later.md; [[L-13 Economy options kept out of the first worlds|L-13]]; water_and_preservation.md §4 | nets wait on fibre | a fowling `net` method needs nothing, and takes salmon |
| items.fishing rod (data.py:51); 02zzy2 §1 | lasts 30 uses | never worn (`uses` worn only in farm._break) |
| KINDS uses (kinds.py:37 to 92) | venison, hide, antler; pork, fat; meat, feathers, down; pelt; ermine | a kill gives meat and one "hide"; no antler, fat, feathers or fur |
| WARY_WORDS and the wary sign | "wary" | two states: the expert reads `pressure`, the sign `wary` (§1h) |
| methods.py:208 docstring | familiarity x (1 + 0.5 x familiar) | `FAMILIAR.factor` 0.35 |
| data.py:385 comment | a set trap 10 kg "(17 eels, 3 salmon)" | holds 20 heads, so 10 kg binds; consistent, but the trap cannot take a salmon run's worth (3) for its kg |
| `cut` aliases (data.py:435) | "coppice", "coppicing", "cut poles" | gives firewood; no poles, no coppice state |
| Statuses | water_and_preservation.md "nothing to build"; wildlife.md "Not built"; methods_and_encounters.md "to be built"; hunt_and_fixes.md and hunt_followups.md "Not merged"; wild_layer.md "brief 5 on unmerged branches"; river_and_water.md "accepted for building" | all built and on main (wild_layer.md: merged 16 Nov; gear.py, runs.py, keeping.py on main) |
| [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]'s net puzzle | 48 salmon met, none taken (02zzy2 did not trace it) | at skill 0.5 a meeting is taken at 1 - e^(-0.25 x 0.5 x 0.6 x 1.12), about 8%, and about 15% at skill 1; wariness raising flee brings the low end to about 5%. Forty-eight misses in a row is then about 1 in 12 at the very lowest odds and far less likely at the seeded skills, so the chance alone does not explain it; still untraced |

## Findings

1. **The gear layer is the missing middle.** The engine has the ends of every chain (the wood, the kinds, the river, the eating
   and the keeping) and almost nothing between: one weapon of one timber, a rod of half a timber, sets that cost nothing, a weir
   whose wattle and traps are timber. Every material the research notes will propose (withies, poles, bark, cord, leather, bone,
   sinew, feathers) enters as a new good with no existing consumer, so the build is as much re-pointing the consumers (the rod,
   the crude weapon, the weir's sections, the wattle room and fence, the smoke racks' hurdles, the bedroll, pack and harness, the
   anvil's bellows) as adding the makers.

2. **Sets are the first seam to change, and the riskiest.** A snare line or a wicker trap is today a free container with a life.
   Making it a carried good that is set, lifted and set again with wear ([[D2-23 The tool set|D2-23]]'s trap, recipes.md's numbers) changes the economics
   of every trapping world: today a trapper sets eight traps a day for nothing. The lift-and-reset act also answers [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]'s "set
   mistaken for lift", since a reset needs the trap in hand.

3. **Wear does not reach the take methods.** Neither the weapon (`gear`) nor the rod (`uses`) wears in the act that uses it.
   Any gear [[W-73 Fishing, hunting and their materials developed together|W-73]] adds inherits the gap until wear is applied where the take is made (`wild.hunt`, `_set_night`, the stock yield).

4. **The tool table cannot name a tool.** Techniques ask for a grade of hand tool, not a knife or a billhook; TOOLS is sorted by
   a two-grade index. Cutting withies, splitting poles, skinning and gutting all want a specific edge. Either `uses` becomes the
   general "needs this item, worn by this much", or tools gain kinds within grades ([[D2-48 Specialised tools|D2-48]]'s specialised tools are the decided
   form).

5. **What a method takes is decided by the kind's traits, not by the gear.** This is why the fowling net takes salmon and the
   snare takes otters at the water. Gear with its own reach (mesh, throat, where set) needs a filter on the gear side; otherwise
   each new net or trap becomes a new method row, against [[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]]'s general methods.

6. **The kill is dressed for free.** A butchering step (a `work` at the carcass thing, by skill, as `bury` and `burn` already
   are) is where hide, tallow, antler, bone, sinew and feathers would come from, and where gutting's work for fish ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]) would
   sit. Today tallow comes only from slaughter, antler only from a lucky find, and every pelt is a cow's hide.

7. **Knowledge flags flatten the ladder.** The snare and the hunt are basic; the weir is basic (known to all, [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]); net and trap
   in water are tryable by anyone; salting, drying and smoking are basic. The trade curve's 0.5 start makes a netter or trapper who learned it from the
   land worse than a bare novice. A gear chain with makers and specialists needs non-basic rows and seeding by archetype ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]), and the curve's
   start read as a craft's, not a take's.

8. **The hunter's signs are good at the field's edge and thin in the wood.** Game is shown in the wood only while one hunts it
   (two lines a trip), and at the village through seven presence rows that skip the small game and the fowl. The hunted-ground
   sign fires once, usually on the first kill, on every kind in the method's table, and is never shown again; the expert's
   "wary" reads a different number. A hunter cannot tell thin game from shy game, which is the decision that matters for [[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]]'s
   trips out.

9. **The records lag the code in five places** ([[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]], [[D2-213 A set trap holds at most about 3 food a night|D2-213]], [[D2-216 Eels and salmon are fish|D2-216]], [[D4-122 Fish on the hearth rack|D4-122]] numbers; six proposal status lines). They should
   be marked "replaced by [[D2-258 The food values are put on one physical basis|D2-258]]" and the statuses set to built before [[W-73 Fishing, hunting and their materials developed together|W-73]] designs on them, or the next session will design
   against a 3-food trap.

10. **Wood is one stock with three cuts.** Young growth already exists with its own regrowth by forest kind, the natural source
    of withies and poles; a coppice as a rotation is a separate, larger step ([[L-120 Wildlife pack K7 land works and infrastructure|L-120]], economy_web's question 2). The deer's
    bark-stripping sign already speaks of a coppice the engine does not hold.
