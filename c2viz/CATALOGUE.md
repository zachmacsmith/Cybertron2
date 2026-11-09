# What the engine added that the visualiser should support

The engine and the generator as of 8 Nov 2026 (`6e9b0ad`), against what c2viz drew when it last caught up (4 Nov, `37b3f87`).
Each entry gives where it lives, what it leaves in the state or computes (what c2viz may draw, per CLAUDE.md "Visuals are drawn
from the engine"), what c2viz shows now, and what it should show. The order is by how much it changes a picture.

**Status:** built in the engine (a world can have it now), opt-in (a world turns it on), or decided but not built.

## 1. Weather that differs by place and day (D4-109, D4-110; `engine/climate.py`, `data.CLIMATE`)

**Status:** built; opt-in (a world's `climate:` block). Without it the engine keeps its hand-written spells, as before.

**What the engine holds** (computed from the seed and kept in a cache, not in `World.s`; c2viz gets it through touch):
- **At each node and day,** from `climate.env(w, node, day)`:
  - `temp` and `low`: the day's mean and the night's low, °C;
  - `rain`, mm;
  - `wind`, m/s;
  - `fog`;
  - `storm`: how near a storm passed, 0 to 1.
- **Labels the rest of the engine uses:** `weather` (clear, rain, heavy rain, fog, snow, gale), `frost` and `snow_lying`, all per
  node. `environment.weather`, `wet`, `snow_lying` and `since_heavy_rain` now take a `node`.
- **For the whole region:** the day's weather `type` (settled, westerly, cyclonic, northerly, easterly, storm), the season, the
  `era` (steady, warm, cold, wet, dry, stormy), and a rare `shock` (a dark year).
- **Storms:** `climate.storms(w, day)` gives each storm abroad with its position (km on a plane laid out from road distances),
  radius and wind. `storm_coming` is true the day before a storm reaches a place, and is also a sign people can see.

**c2viz now** (D4-111, 37.4, 8 Nov: every weather query names its place):
- each day's record has `places {node: {cold, weather, words, wet, snow}}`;
- a place close up draws its own weather, and snow where its own place has it;
- the region's map draws one sky, the commonest weather over the places (a presentation choice), with snow from each place it paints.

**Done (8 Nov, ENGINE.md §14):**
- each place's weather and values on both scales, blended between places on the region's map;
- rain by mm, slanted by the wind; frost rime; a passing storm darkens;
- storms still crossing drawn as masses, and a cloud mark on a place a storm reaches tomorrow;
- the day's type and era on the page, and each place's weather on hover.

**Still open:** wind in the land itself (trees and smoke leaning), and a storm's track across days for slow storms, which the
engine's storms list holds only while a storm is still crossing.

## 2. Crops that grow by the season (D4-106; `engine/farm.py`, `data.CROPS`, `PHYSICS.farming`)

**Status:** built.

**What the engine holds** (`parcels[pid].crop`, or each holding's record when a field is held in shares):
- `lying`: sown seed that has not come up yet (it waits for a growing season, and is lost a little each night meanwhile);
- `stand`: the share of the crop still standing, thinned by cold nights;
- `frost_day`;
- `winter_n` and `wintered`: winter grain counting the winter nights it needs before it heads;
- `stalled`: winter grain that met no winter and has not headed;
- `progress`, now advancing at each season's own rate;
- a crop reaped before it is ripe gives its `green` good (green grain, green rye, green beans): fodder, which spoils unless dried
  into hay ("dry fodder").

**The signs that say what should show** (`signs.py`):
- seed being broadcast, rooks following the sower;
- nothing come up yet;
- pigeons working the sown ground;
- only a scattering come up, bare soil between;
- frost-blackened tips;
- half dead after the frosts;
- light, thin ears;
- dead and black.

**c2viz now:** stages new, green, high, ripe, rotting, blighted and killed, and the sown and reaped shares. Nothing for seed
lying, a thin stand, frost damage or a stalled crop.

**To support:**
- **Sown but not up:** bare drilled soil with birds on it.
- **A thin stand:** plants with bare soil between, by `stand`.
- **Frost:** blackened tips the morning after a frost night, half dead after several.
- **Thin ears** for a crop that grew poorly.
- **Reaped green:** stubble, with green sheaves instead of gold stooks.
- **Winter grain waiting through the winter:** low green, unchanging.
- **Model change:** add `lying`, `stand`, `frost_day`, `wintered` and `stalled` to the parcel record.

## 3. Fields held in shares (D2-163, D2-172; `farm.standing`, `farm.holding_view`)

**Status:** built (2 Nov), and only half drawn. 37.4 changed `extract.py` so a field is drawn as its main holding shows it.

**What the engine holds:** a field's claims may name plots. Each holding has its own record: crop, soil, sown and reaped. One
field can carry barley for one household and beans for another.

**To support:**
- **Each holding's plots as their own strips** in the field: crop, stage and reaped share for each.
- **Who holds which strips,** on hover.
- **Model change:** the parcel record lists each holding's share and crop, not only the main one's.

## 4. Fittings that wear and are mended (D4-103 phase 2, D4-105; `engine/wear.py`, `FITTINGS.wear`)

**Status:** built (`labour.wear` on).

**What the engine holds:** `buildings[bid].worn` gives each fitting's wear. An oven cracks after its firings, millstones go dull
with the grain they grind, a mill's leat silts in a year. `wear.worn_words` names the state. New mending techniques: dress
millstones, reline oven, clear the leat.

**To support:**
- **A worn fitting drawn worn:** a cracked oven with less smoke, a silted leat, the wheel turning slower. Its state on hover.
- **Mending as an act,** with its own tools (done: make, make, dig).
- **Model change:** `worn` and `worn_words` in the building record.

## 5. Work that costs food, and tiredness (D4-103, D4-108; `engine/labour.py`, `engine/needs.py`)

**Status:** built.

**What the engine holds:**
- the day's units worked, and any pushed past the day (`today.units`: used, over);
- `people[n].tired`: units off tomorrow after pushing on;
- the walk between jobs, which now costs a little;
- the night lines saying when the work made a ration a missed meal.

**To support:**
- **Someone who pushed on, drawn working on into dusk** in the day's animation. The engine's timings already run past the day's
  budget; c2viz clips them now.
- **Tired the next morning:** a slower walk and a slump.
- **Model change:** units used and over in the timeline's budget; `tired` in the person record.

## 6. Water, fish and salt (D4-103's acceptance test; `packs` "water"; proposals/water_and_preservation.md)

**Status:** built; opt-in (`packs: [water]`); off in every other world.

**What the engine holds:**
- a water parcel's `fish` stock, and its seasonal run (`periodic` renewal);
- a saltmarsh's `salt` (pans, by season);
- goods: fish, salt fish and fishing rods;
- techniques: fish by hand, angle (needs a rod), salt pan, salt fish, make a fishing rod.

**c2viz now:** water parcels as water; no fish and no salt. Tools for the new techniques are added.

**To support:**
- **Fish rising** in a water parcel by its stock, and the run's season (many rising), from the signs "fish rising all along" and
  "the water is quiet".
- **Salt pans** on a saltmarsh: white crusts in summer, by stock.
- **Fish and salt fish** in stores and carried.
- **A rod by the door** of a house that has one.

## 7. Each stock's own renewal (D4-104; `engine/renewal.py`, `RESOURCES.renewal`)

**Status:** built. Renewal kinds: fast, slow, threshold, periodic, finite, endless, accrues. c2viz already draws wood, plants,
grass, game and dung by stock.

**To support:**
- **Periodic stocks drawn by season:** fish runs, and later the wild year (§9).
- **Threshold stocks** (game) shown as gone, not merely low, once they cross the line. The signs already say "few fresh tracks"
  and "the game is thin".

## 8. A house broken into (D4-101; the raid's break-in)

**Status:** built. An attack aimed at hurting breaks in and sets on each person inside.

**To support:**
- **A broken door** on the building that day, and the fight inside marked at it. c2viz's records hold each building's door and
  the day's fights; it draws no break-in.

## 9. Wild kinds (D2-192 to D2-199)

**Status:** being built on 37.2's `ecology` branch (D2-199), not on main. Phases 0 to 3 are there: populations by area, groups
near people, traces, watches, hunting from the populations.

**Done in c2viz (9 Nov, ENGINE.md §15):**
- kinds by count on the region's map;
- the village's own wild close up;
- groups at the wood's edge, raids by night, traces, watch fires;
- the hunting and watching techniques' tools.

Optional: on main, without the pack, nothing changes. Checked on a bot run of twin bays with the pack, in summer: a sounder of
three boar at Northby goes to the edge on day 2 and raids the corn on night 4.

**Still to support:** a hunt's outcome at its place (a carcass, a wounded hunter); kept beasts once husbandry moves onto the beasts
entity (phase 5); the later waves' kinds (hounds, wolves at the fold).

## 10. Ecosystems in motion (02zp, 37.2's deep dive)

**Status:** analysis only, nothing decided. It covers plants placed by conditions (Ellenberg-style values), succession over 10 to
45 years, wild populations, and the seasonal wild year.

**For later:** if adopted, the ground truth gains plants and succession stages per cell. c2viz would draw them as it now draws the
generator's ecosystems.

## Already drawn from the engine since 4 Nov

- **Actions in two frames** (this change): each person at work alternates two poses of the act's tool while the day plays.
  - The poses: fell, reap, dig, mine, make, hunt, forage, milk, herd, sow, carry, fish.
  - The new techniques mapped to tools: angle, fish by hand, salt pan, salt fish, fishing rod, dress millstones, reline oven,
    clear the leat, dry fodder.
  - Which tool an act shows comes from the engine's technique; the stroke itself is a presentation choice (ENGINE.md §11).

*Current as of 8 Nov 2026.*
