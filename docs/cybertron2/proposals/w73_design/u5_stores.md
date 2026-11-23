# U5. Stores and containers: a space and what is in it, each removing named risks, at real capacities; vermin basic

**Status:** discussion (component spec of the integrated design, W-85). The parts decided are cited; nothing built.
**Owner:** 37.2 (the store layer, keeping by portion, vermin, the illness hook). 37.4 is named on the merge for what lands in its
areas: `buildings.py` (stores, `alloc`, the floor), the fittings' and rooms' costs (U7), the store lines in the prompt.
**Thread:** the integrated design (W-85), under the network (W-73).


> **Decisions since this spec was written (binding over its text; the build reads this table first):**
> - **D2-313:** 37.2 owns every engine file this wave changes (read every '37.4' in the code tables as 37.2 for this wave).

## Extends

- **D2-272** (a food's base rate is its rate well kept; stores remove outside penalties and never slow below base; better stores
  each remove a particular risk), **D2-279** (stores as answered: no good kept at a building's best fitting; each kind of store
  removes risks; every good has a place, set behind the rules but visible and changeable; a store is a space and its containers,
  each made separately with its capacity, what it protects and suits; real capacities; storage.md's set; vermin basic: a share a
  night by exposure, cats, owls and terriers cut it, spilt or heaped food draws more, more vermin bring signs and raise the baseline
  chance of sudden illness; the head's seeded ways; the locked chest deferred), **D2-274** (the book runs the stores; moving free
  within a building, provisional between), **D2-289** (the keeping curve), **D2-264** and **D2-288** (weights in kg; handling units).
- **store_rules.md** (D2-274, D2-279: the defaults, labour, visibility), **storage.md** (§3 each store, §5 the two layers, §6 vermin,
  §7 penalties, §8 changes; §9 manual moves read; the lock deferred), **hunt_fish_materials.md §7.4**, **wave1_physical_basis.md
  §2.3** (the penalties table) and **§3.3, §3.4** (containers and fittings, priced), **wave3_keeping.md §2.4** (the smokehouse as a
  store).
- **wave_conflicts.md** C23, C24, C26, G10, G11, K3, K10, E7, E10, E11; S3 (goods.md's body still says the old rule), S4
  (buildings.md's cellar).
- **The code** (read 22 Nov): `buildings.py:112-258` (`stores`, `alloc`, `room_for`, `full_words`, `space_words`), `:412-439`
  (`overflow`), `data.py:117-130` (DECAY), `:242-256`, `:270`, `:283-285` (bins, granary, cellar, woodshed, vault), `:325-332`
  (STORES), `:776-777` (`house_spoil`, `cellar_spoil`), `night.py:311-352` (`decay_rate`, `spoil_rate`), `wild.py:24` (DRY_STORES),
  `:674` (`_follow_harvest`), `:2716` (`_store_food`), `:2747-2763` (`_stops`), `:2839-2860` (`_stores`), `wild/kinds.py:552-556`
  (EATEN_SIGNS stores), `:612-614` (PRESENCE rats), `:805-839` (BODY, STORE_STOPS, CAT, LEFT_OUT, OWL), `life.py:474-495`
  (`_old_age`, the adult's "sudden illness"), `data.py:1144`, `here.py:378-386` (`party_container`), `prompt.py:513` ("a store keeps
  food 3 times better"), `prompt.py:652-700` (`_house_lines`), `view.py:107-170` (the store in the morning's changes).

## Departures

| # | From | This spec | Why |
|---|---|---|---|
| 1 | storage.md §7 and wave1 §2.3 keep fresh fish's ×2 in a store (D2-212) as a store factor | dropped as a store factor; fresh fish's base (0.17 under D2-289) already holds its shorter life | D2-272: a store never adds to a good's own rate (wave1 §2.3 agrees; storage §7 kept it) |
| 2 | storage.md §9: every container tagged (D4-68), manual `keep ... in C3` by tag | containers are counted goods of a building (6 sacks), addressed by kind and building ("the chest in Holt House"); a tag only for a container someone holds apart, later with the lock (L-156) | D2-279's "visible and changeable in more detail if they want" is met by kind; tags on every sack are state nobody has asked for |
| 3 | storage.md §3.11 and §8: a cellar's costs and digging rates | costs are U7's (wave1 §3.4's table at the capital factor); this spec keeps only what the cellar holds and removes | D2-276; the costs live in one place |
| 4 | storage.md's proposed set adds the root clamp, the hay rick and the barn | not in this build: D2-279's set does not name them; deferred (Gaps, 5) | D2-279 lists the set |
| 5 | D2-279: barrels in the set, and "barrels later" in the same sentence (C26) | barrels are a data row now; making one waits on the cooper (a trade, later); the salting tub (G10) holds brine now | both halves of D2-279 kept |
| 6 | store_management.md D7 ("what one carries home is put away at night") | no such default | D2-274: people set their own rule for what they put away |
| 7 | DECAY's `frozen` factor slows a good below its base in a frost | kept as a season's effect, not a store's | D2-272 is about stores; a frost is the weather. Named so it is not read as a store slowing food |

## Purpose

What runs showed (storage.md §0, §2): houses held five to nine times their bins and kept all of it at the bins' rate, safe from
vermin; overflow at the door never met a rat. D2-272 and D2-279 replace that with stores that remove named risks and hold real
amounts. The unit gives each good a place (a space and a container), keeps and exposes each portion by where it lies, lets vermin
take what is exposed and draw more by it, and tells the household what it has and where, so it knows what to build or move.

## The design

### 1. Spaces

A space holds goods loose on its floor and gives the climate. Capacities are real (D2-279).

| Space | Where (engine) | Holds loose | Removes (penalties, §3) | Adds | Vermin, space factor | Notes |
|---|---|---|---|---|---|---|
| a room's ground floor | a room (ROOMS) | 30 kg a free space (STORES `floor`, kept) | the open (sun, rain) | floor damp | 1.0 | wear: gappy, holed as now (`wear.damp`) |
| an upper storey's floor | a room on storey 2 or 3 | 30 kg a free space | the open; floor damp | | 1.0 | boarded and dry (store_management §1 scenario 1) |
| a granary floor | fitting `granary` (a boarded loft) | 400 kg a space × its 3 (storage §3.7) | the open; floor damp | | 0.6 | grain, rye, beans loose |
| a granary on staddles | a building (a raised small timber room; U7 prices it) | 400 kg a space × 6 (2,400 kg) | the open; floor damp | | 0.25 | stands apart; can burn |
| a cellar | fitting `cellar`, by footprint, on dry ground only (not fen, saltmarsh or a parcel that floods; U7 for the digging) | 30 kg a space of its footprint, and containers | the open; heat (the warm season, for the goods heat ruins); frost (roots) | cellar damp | 1.0 | grain, meal, flour and salt keep badly there |
| a smoke loft | fitting `smoke loft` (hooks in the roof) in a room with a hearth, or a timber or stone smokehouse's roof | 40 kg a space of the room's floor, hung goods only (storage §3.12) | the open; floor damp; flies | | 0.3 (hung) | smoked, dried, salt and hard-cured fish and meat |
| a smokehouse's racks, once a lot is done | U4's `smoke racks` | the lot (U4) | the open; floor damp; flies | | 0.3 (hung) | the smokehouse with no fire is a store at base (D2-284) |
| a woodshed | fitting `woodshed` (a lean-to; ground 2) | 9,600 kg of fuel (storage §3.13: the engine's figure is real) | rain on fuel | | | the wet-wood penalty waits on W-76 (Gaps, 6) |
| a vault | fitting `vault` (a stone room of its own) | 30 kg a space × 4, and containers | the open; fire | | 1.0 | theft through its door and lock, as now |
| a sealed pit | a thing on a parcel (as a buried cache) | up to 2,000 kg of grain or beans (storage §3.16) | everything while sealed | once opened, ×3 a night until emptied (est.) | 0.05 | about 2% of what goes in lost at the walls (est.); found and robbed as a cache |
| a door pile | a pile at the door (D4-89) | any | nothing | the open | 1.5 | dry goods are taken there too (today only LEFT_OUT) |

### 2. Containers

Each is a good made separately (U3 prices the making) and kept in a building's store, counted (`"sack": 6`). It takes floor, holds
some kinds up to a weight, removes named risks, and wears out over world years (D2-276: a life of real years as world years; its
nightly share 1 / (life × days a year); basis §1's lives are open).

| Container | Holds (kg each) | Takes floor | Suits | Removes | Vermin exposure (rats, mice) | Life | Pack | Making (U3) |
|---|---|---|---|---|---|---|---|---|
| sack | 50 | 12 a space | grain, rye, beans, meal, flour, nuts, salt | floor damp halved (×1.5 for ×2) | 0.8, 0.7 | 3 world years | materials | 0.6 cord (wave1 §3.3) |
| basket | 25 | 10 a space | roots, nuts, fruit, eggs, dried, smoked and hard-cured goods, cheese | the heap; floor damp halved | 0.8, 0.7 | 2 | materials | 0.3 withies |
| bins (a fitting, built in) | 300 a fitting | 1 space | dry goods | floor damp | 0.5, 0.4 | 10 | core | U7 |
| chest (an ark) | 400 | 1 space | dry goods | floor damp | 0.2, 0.15 | 30 | core | a carpenter, 4 timber (wave1 §3.3) |
| salting tub (G10) | 120, salt goods in brine | 3 a space (est.) | salt fish, salt meat | out of brine; flies | 0.05, 0.05 | 5 (est.) | water | U3: a basic tub or trough, no cooper (Basis rows needed, 2) |
| barrel | 120, salt goods in brine or dry goods | 4 a space | salt fish, salt meat; dry goods | out of brine; flies; floor damp | 0.05, 0.05 | 10 | water | a cooper (later) |
| (crock) | 20 | 15 a space | | | 0.05 | | | deferred until clay |

A tub and a barrel differ in what matters later: a barrel travels (salt fish sold by the barrel), a tub stays where it is.

### 3. Penalties: what each portion keeps at

Each portion keeps at its good's base (U4 §3 and Basis rows needed, 1), times every penalty its space and container leave.
Penalties multiply the hazard, never the share: r' = 1 − (1 − r)^k (wave1 §2.1), so no penalty takes more than everything.

| Penalty | Goods | Factor | Removed by |
|---|---|---|---|
| the open, dry | everything | DECAY `open_dry` (as now: fresh meat and fish 2, grain 4, bread 3, cheese 3, dried 2, default 2) | any roof |
| the open, wet | everything | DECAY `open_wet` (as now); hay and straw 10, bark 5 (wave1 §2.3, est.) | any roof |
| in hand | fresh foods | 1.5 (wave1 §2.3, est.) | a covered creel or basket |
| the warm season | fresh meat and fish, milk, cheese, eggs; others | DECAY `warm` 1.5; others 1.2 | a cellar (the first group only) |
| flies (warm season) | fresh and in-process meat and fish, cheese | 1.5 (storage §7, est.) | smoke (a loft, racks), a tub, a barrel |
| floor damp | grain, rye, beans, meal, flour, salt, bread: ×2 (×1.5 in sacks or baskets); dried, smoked and hard-cured fish and meat: ×3 (×1.5 in baskets) | wave1 §2.3 (est.) | bins, a chest, a barrel, a granary floor or staddles, an upper storey, a smoke loft or the racks |
| cellar damp | the same goods, the same factors | | none in the cellar: they belong elsewhere |
| frost | roots | 3 (storage §7, est.) | a cellar |
| the heap | roots loose | 1.5 | baskets |
| out of brine | salt fish, salt meat | 1.5 (wave1 §2.3: on a floor packed in salt) | a salting tub, a barrel |
| a store's wear | everything inside | `wear.damp` (as now: gappy 1.5, holed 3) | mending |

`house_spoil` (0.3), `cellar_spoil` (0.25) and every fitting's `spoil` multiplier go (D2-272). DECAY's `store` factor for fresh fish
goes (Departure 1). A good with no base loss (salt, timber, stone, leather) takes only the open's penalties, as now (`abs`).

### 4. Where each good goes: the sort

Every good in a building lies in a **portion**: a space and, inside it, a container or none (loose). Portions are not stored state:
`buildings.alloc(b, goods, book)` computes them each time from the building's goods, its spaces, its containers and the book's
`keep` and `hold back` rules (U6), so the night, the store line and the vermin all read one deterministic answer.

1. **The book first:** a `keep` rule that names where a good lies ("the seed barley in the chest") puts it there, up to room; a
   `hold back` portion is set apart from drawing (U6).
2. **Then the best place with room** for each good (D2-279: "every good has a place it is stored in, usually set behind the standing
   rules"): candidates ranked by the hazard factor the good would keep at (fewest penalties left), then the vermin exposure, then a
   fixed order (the table order of §1 and §2). Goods are placed in a fixed order (the most perishable first, then by name).
3. **Then loose** on the floor of a space that takes it, at 30 kg a free space; containers' floor counts against it.
4. **Full:** what does not fit goes to the household's next store at the place, then the door, as store_rules' defaults say
   (`overflow`, `buildings.py:418`), with its line.

Moving within a building is free (basis §5), so the sort costs nothing; taking down a hung lot is U4's quantity work.

### 5. Vermin, basic (D2-279)

**The take.** Tonight's share for a kind *k* from the ecology (as now, `wild._stores`: its eaten over its year of store) is taken from
each portion *a* of each building holding vermin goods:

`take = q_a × share_k × exposure(container, k) × space factor × stops(building, k) × plague`

- **Vermin goods:** a `vermin: true` mark in ITEMS: grain, rye, oats, beans, meal, flour, bread, nuts, acorns, acorn meal, roots,
  cheese, eggs, and the dried, smoked, hard-cured and salt fish and meat (in brine they are in a tub, at 0.05). DRY_STORES is replaced
  by the mark.
- **Exposure** is §2's column; loose on a floor 1.0; hung 0.3; a door pile 1.5 (dry goods too).
- **Stops by kind** (storage §6, from Elton 1953, est. in the numbers): a cat mice ×0.4, rats ×0.7; a barn owl in its hole mice ×0.6,
  rats ×0.9; a dog (a terrier) rats ×0.5, mice ×0.8. STORE_STOPS's `granary` and `bins` rows move into the space factor and the
  exposure (they would count twice otherwise).
- **The draw.** `_store_food` and `_follow_harvest` read the **exposed** store, Σ q_a × exposure, not the dry goods' total: grain
  heaped on floors and at doors feeds and draws the rats; a village of chests starves them down. Spilt food is not a separate act:
  the exposure of loose and sacked grain stands for it (storage §6).
- **Calibration targets** (storage §6, est.; the wild tests world's `kept` arm): over a world year in an ordinary year, loose on a
  floor 15 to 25% lost, in sacks 10 to 15, in bins 6 to 10, in chests with a cat 2 to 4, on staddles about 2. A loose 20% a year is
  about 0.007 a night at exposure 1; the exposures above then give a chest with a cat about 0.0004 to 0.001 a night, inside its
  target.
- **What it binds (K3).** Under D2-289 grain keeps about 221 nights well kept (0.0013 a night): spoiling hardly binds grain, so
  **vermin are what binds a grain store**, and the containers and the cat are what a household buys against them. The scale gap
  (L-154) is read with this in live runs.

**The signs** (EATEN_SIGNS "stores" made specific by where the loss was; storage §6). Each is a change (a loss last night), grounded
in a portion's take, for those of the household and anyone who looks in the store; chances through the noticing rule, intended
values stated for U8 to check (guides/senses.md item 5):

| Where | Sign | Sense, own | Intended |
|---|---|---|---|
| loose on a floor | "grain scattered and trodden into the floor of {place}, mouse droppings in it" | sight, 0.8, near | likely for one who sleeps there |
| sacks | "the sacks in {place} gnawed through at the bottom, grain run out on the floor" | sight, 0.8, near | likely |
| a chest | "fresh gnaw marks at a corner of the chest in {place}" | sight, 0.5, near | even |
| a door pile | "the heap outside {place}'s door dug into and scattered in the night" | sight, 1.0, around | near certain by day |
| hung goods | "something has been at the fish hanging in {place}: tails chewed, droppings beneath" | sight, 0.7, near | likely |

The PRESENCE row for rats at home (density 60 a km² and over, `kinds.py:612`) stays: it reads the numbers the draw raises.

### 6. Vermin and sudden illness (G11): a first magnitude

D2-279: more vermin "raise the baseline chance of sudden illness". The only hook is the adult's 0.001 a night (`life.py:474-495`,
D2-149; about 3% a world year, about 6% over a 64-day life). Proposed first magnitude (est., calibrate):

`p = 0.001 × (1 + 2 × min(1, R / 120) × E_h)`

- R: the rats' density a km² in the household's home area (the ecology's `pop["rats"]`, as PRESENCE reads it).
- E_h: the household's exposure index: its vermin goods' exposure-weighted share, Σ q_a × exposure / Σ q_a over its buildings,
  capped at 1 (a house of chests about 0.2; of loose floors and door piles about 1).
- At its most, three times the baseline (about 9% a world year), in a house with rats about and its food lying open; a house with its
  grain in chests and a cat stays near the baseline. The death's cause stays "a sudden illness" (no new words the state does not
  decide).

It is weak on purpose: a death a lifetime in a few households. Sickness that costs work rather than life, sanitation, middens and
disease from hides wait on L-155 (vermin fleshed out) and L-157 (rest days, health, fatigue and illness). The adult hazard's own
scaling with the lifespan (E11) is left to its owner.

### 7. What a person sees

**By default** (the morning's house lines, `prompt._house_lines`; store_management §5), a line a building, by portion, with room left
and what is outside:

> Holt House's store: 735 grain (400 in the chest, 300 in 6 sacks, 35 loose on the floor), 9 beans in a basket, 80 salt fish in brine
> in the salting tub; room for about 600 more dry goods; 335 grain lie outside its door.

**Attending to the store** (the reply's `attend` naming one's store, or a building of one's household):

- each space and container by kind: its fill, room, state and life ("6 sacks, 2 gnawed through; about a world year left in them";
  "the chest, sound"); the room's own condition ("the roof gappy: the damp gets in");
- last night's spoiling by where ("35 grain loose on the floor lost about 0.3; nothing in the chest");
- vermin by where, and the signs; the cat or the owl if any;
- what is held back, and by which rule (U6); the rules in force for these goods and what they did (U6 §6).

**The system prompt's line** "a store keeps food 3 times better" (`prompt.py:513`) goes; how stores keep is the head's seeded lines
(wave4 §3.4, HH4, which renders the store the household has), not the core (D2-279: the system prompt gives the rules' grammar only).

**Facts, never advice.** "335 grain lie outside its door; the Granary has room for 300" tells them what to build or move without
saying to.

## Code changes

| File, line | Change | Owner |
|---|---|---|
| `data.py` ITEMS | container goods (sack, basket, chest, salting tub, barrel) with `container: {holds_kg, per_space, suits, removes, exposure, life}`; `vermin: true` on §5's goods | 37.2 |
| `data.py:117-130` DECAY | penalty rows `floor_damp`, `cellar_damp`, `flies`, `heap`, `brine`, `frost`, `in_hand`; `fresh fish.store` removed | 37.2 |
| `data.py:242-256`, `:270`, `:283-285` FITTINGS | `spoil` fields removed; `removes`, `adds`, `holds_kg` and `exposure` in their place (bins 300; granary 400 a space; cellar by footprint with `site`; vault; woodshed 9,600 kg); new `smoke loft` | 37.2 data, 37.4 named (fittings) |
| `data.py:325-332` STORES | `order` replaced by the sort's ranking; `floor` 30 kept | 37.4 (buildings) |
| `data.py:776-777` PHYSICS | `house_spoil`, `cellar_spoil` removed (D2-272) | 37.2 |
| `buildings.py:124-171` `stores`, `alloc` | portions: [{space, container, goods}] by §4; reads the book's `keep` and `hold back` (U6) | 37.4 (buildings), 37.2 writes it under the thread |
| `buildings.py:192-258` `room_for`, `full_words`, `space_words` | by portion; containers' floor | 37.4 |
| `buildings.py:418-439` `overflow` | the household's next store at the place before the door (store_rules D3) | 37.4 |
| `night.py:311-352` `decay_rate`, `spoil_rate` | per portion: the good's base × the penalties its space and container leave (§3); `house_spoil` and the fittings' multipliers gone | 37.2 |
| `night.py:176-202` (the spoilage loop) | a store's goods spoiled by portion (`alloc`), not as one stock | 37.2 |
| `wild.py:24` DRY_STORES | replaced by ITEMS `vermin` | 37.2 |
| `wild.py:2716`, `:674` | the exposed store | 37.2 |
| `wild.py:2747-2763` `_stops` | split by kind (cat, owl, dog) | 37.2 |
| `wild.py:2839-2860` `_stores` | per portion, with exposure; door piles of dry goods at 1.5 | 37.2 |
| `wild/kinds.py:552-556` EATEN_SIGNS, `:808` STORE_STOPS | the signs by portion (§5); the granary and bins rows moved to exposures | 37.2 (signs checked with U8) |
| `life.py:474-495` `_old_age` | the adult's chance × §6's factor | 37.2 |
| `prompt.py:513` | the "3 times better" line removed | 37.4 (prompt) |
| `prompt.py:652-700` `_house_lines`; `view.py:146-163` | the store line by portion (§7); the morning's changes by portion | 37.4 (prompt, view), lines from `buildings` (37.2) |
| `here.py:378-386` `party_container` | replaced by the book's `go` rules, then home (store_rules D1, E10) | 37.4 (with U6) |
| `clocks.py` RATES | `ITEMS.*.container.life` on the year clock; `FITTINGS.*.spoil` removed | 37.2 (U0) |
| spec `economy/goods.md:84-90`, `:122`; `economy/buildings.md:27`, `:80-81` | the old house rate and cellar quarter rewritten when Zach decides the build (S3, S4) | goods.md 37.2; buildings.md 37.4 |

## Tests

1. A house with grain: 300 in the bins, 400 in a chest, the rest in sacks then loose; each portion keeps at its own factor; nothing
   keeps below the grain's base (D2-272).
2. Fresh fish in a store keeps at its base (no ×2); in hand at ×1.5; at the door in the open's penalty.
3. A cellar: fresh meat in summer loses the warm penalty there; grain in it takes cellar damp.
4. Salt fish in a tub keeps at base; out of a tub at ×1.5.
5. Vermin: the same share takes about five times more from loose grain than from a chest; a cat cuts mice more than rats; a door pile
   of grain is taken.
6. The draw: moving a village's grain from floors into chests lowers the exposed store the ecology reads.
7. The illness factor: 1 with no rats; 3 at R 120 and E_h 1; a house of chests about 1.4 at R 120.
8. The store line and the attending view read the portions as the night spoiled them.
9. A container wears out over its life and the line says so ("a sack has worn through").
10. The wild tests world's `kept` arm reaches §5's yearly targets within their ranges (a calibration check, not a pass/fail on
    behaviour).

**What live runs should read** (against a null arm with today's stores): where grain lies by the end of the year; vermin losses by
household; whether households make or buy sacks, chests and tubs; door piles; deaths by sudden illness by household (few; read only
as a direction); the scale gap (L-154).

## Basis rows needed

| # | Row | Value | Mark |
|---|---|---|---|
| 1 | Base rate a night of each kept good | as U4's Basis rows needed, 1 | follows D2-289 |
| 2 | The salting tub | 120 kg in brine, 3 a space, 5 world years | default, est. |
| 3 | The capacities of §1 and §2 (sack 50, basket 25, bins 300, chest 400, barrel 120, granary 400 a space, staddle granary 2,400, sealed pit 2,000, smoke loft 40 a space, woodshed 9,600, floor 30 a space) | storage.md §3, wave1 §3.3 | default (D2-279: real capacities; numbers est.) |
| 4 | The penalties of §3 | wave1 §2.3 (est.) | default, calibrate |
| 5 | Vermin exposures and stops (§2, §5) | storage §6 (est.) | default, calibrate |
| 6 | Vermin's illness factor | p × (1 + 2 × min(1, R / 120) × E_h) | default, est., calibrate |

## Gaps

1. **Barrels or something that holds brine (G10): designed** as the salting tub now, barrels with the cooper later (§2).
2. **Vermin's illness (G11): a first magnitude** (§6); the fuller system deferred to L-155 and L-157.
3. **Spilling:** no act; exposure stands for it (storage §6). A finer rule (0.5% of grain moved lies spilt for a season) only if live
   runs show heaps without loss.
4. **A curve by a lot's age in stores** (D2-289's later step): stores hold one quantity a good; dated portions wait on it.
5. **The clamp, the rick and the barn: deferred.** They wait on roots and hay mattering in the open (hay spoiling in the open wet;
   roots in frost) and on the crops pack; D2-279's set does not name them.
6. **Wet fuel:** the woodshed removes rain from fuel, but fuel in the open does not yet burn worse wet (Q-24 (7): about 0.7 of its
   heat, est.). It waits on the timber economy (W-76, D2-290).
7. **The locked chest and its key: deferred** (L-156).
8. **Theft from stores by people** is as now (taking from a store one may not use is theft); a household's store against its own
   members is the head's (D4-23).

## Open questions for Zach

1. **The salting tub now, before the cooper** (Q-U5-1; G10, wave3 W80-Q9). (a) A basic tub of timber, 120 kg in brine, made without a
   cooper, now; barrels later with the cooper, for trade; (b) nothing in brine until barrels. Recommend (a): without brine salt fish
   keeps at ×1.5 and salt's long keeping is hard to see; it costs one container row. Default taken: (a). Blocks: salt's value in this
   build.
2. **Vermin's illness magnitude** (Q-U5-2; G11). (a) §6's first magnitude, up to three times the adult's baseline in a house with rats
   about and its food open; (b) none until L-155; (c) larger. Recommend (a): it makes D2-279's sentence true at a size that cannot
   dominate, and gives chests and cats a second reason. Blocks: nothing else.
3. **Containers addressed by kind, not tag** (Q-U5-3; Departure 2). (a) By kind and building, tags only with the lock later; (b) a tag
   on every container. Recommend (a). Blocks: the `keep` rule's targets (U6).

## Sources

storage.md §0 to §10 (§3 the stores, §5 the layers, §6 vermin, §7 penalties, §8 the changes); store_management.md §1, §3, §5;
store_rules.md; hunt_fish_materials.md §7.4; wave1_physical_basis.md §2.1 to §2.3, §3.3, §3.4; wave3_keeping.md §2.4;
wave4_people.md §3.4 (HH4); wave_conflicts.md as listed; catch_basis.md §1 (D2-289's rates); basis.md; DECISIONS D2-272, D2-274,
D2-279, D2-289 and the others cited; the code under Extends; OPEN L-131, L-154, L-155, L-156, L-157.

## History

- **22 Nov 2026:** written by a 37.2 design subagent for W-85 from the sources above.

*Current as of 22 Nov 2026: D2-263 to D2-298.*
