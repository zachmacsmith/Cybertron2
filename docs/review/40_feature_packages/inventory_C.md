# Inventory C: farm, herds, forests, climate, environment, night, needs, life

Read-only inventory of `cybertron2/engine/{farm,herds,forests,climate,environment,night,needs,life}.py` (plus the call sites in
`run.py`, `world.py`, `roads.py`, `renewal.py`, `verbs.py`, `signs.py`, `here.py`, `capacity/`), for a redesign as a small core plus
feature packages. Line numbers are of the files as read on 16 Nov 2026. "apply X" = `w.apply("X", ...)` / `here.apply("X", ...)`.

Notation for owned state: `s.T[*].f` is field `f` of rows of `w.s["T"]`; `par` = a parcel row, `h` = a herd row, `a` = a person
row, `b` = a building row, `c` = a crop record, `today` = `w.s["today"]` (the day's scratch record).

---------------------------------------------------------------------------------------------------------------------------------

## 1. Module by module

### 1.1 needs.py (49 lines)

- **Responsibility:** one pure function `food(p, c) -> (need, fall)` (l.21): the night's food need and "the cold's fall" (share of a
  cold-starving draw) from PHYSICS and a context dict `c` (documented l.4-16). D4-103 / proposals/process_model.md part 5.
- **State owned:** none. **Primitives:** none. **Imports:** none.
- **Data read (via `p` = w.p = PHYSICS merged with spec physics):** `ration`, `shelter`, `shelter_cold`, `heat.ring_cold`,
  `camping`, `camping_fire`.
- **Callers:** only `night.night` l.99. (The spec says analyses call it; `capacity/` does not today: it uses
  `night.eaten_worth`, `life.ration_factor`, `night.spoil_rate`.)
- Note: its context keys hard-code feature vocabulary: `state` in {housed, damaged, unsheltered, no_fuel, beds.floor},
  `structure == "camp"`, gear in {camp, bedroll, tent, out}, `hearth`, `open_fire`, `fire_gone`, `fed_on_road`, `mult/extra`
  (life), `care_fed` (life), `work` (labour). It is a fixed formula, not a sum of registered factors.

### 1.2 environment.py (259 lines)

- **Responsibility:** the day's weather *label* at a place, snow lying, days since heavy rain, and per-place/per-day visibility
  for the senses (sight/sound) (D2-69, D2-99..D2-103, D4-111). Pure: "Nothing here is stored" (l.51); all computed from seed,
  spec, state.
- **State owned:** none. Reads `w.spec["spells"]`, `w.spec["weather"]` (fixed days), `s.events` (today's events at a node, for
  smoke/loudness), `s.parcels[*].cover/res.wood/crop`.
- **Primitives:** none.
- **Data:** `COVERS` (sight/sound base), `ENV` (night, snow_melt, snow_ground, crop_high, crop_high_from, smoke, felled,
  smoke_tags/techs, mask, loud_kinds/tags/techs), `SPELLS`, `TERRAIN` (road terrain sight/sound), `WEATHER` (labels: sight, sound,
  wet, words, loud). `WET` (l.61) = labels with `wet`.
- **Functions:** `spell` l.64 (spec spells, else climate, else "normal"); `_fixed` l.77; `scheduled` l.81 (climate on and no fixed
  day/spell); `place` l.89 (validates node or road; D4-111); `weather` l.97 (fixed day > climate label > draw from SPELLS by keyed
  rng("weather", day), rain->snow if `w.cold`); `values` l.123; `wet` l.130; `snow_lying` l.134 (walks back day by day, recursive in
  weather+cold: O(days)); `since_heavy_rain` l.148; `_today_events` l.158; `_worked_techs` l.162 (unused); `crop_high` l.166
  (**lazy import farm**: `FM.main_crop`); `smoky` l.176; `loudness` l.185; `visibility` l.199; `weather_lets` l.224 (climate
  `CL.vis` or WEATHER table); `open_air` l.236; `felled` l.246 (wood S/K < ENV.felled.below); `ground_factor` l.252; `words` l.257.
- **Imports:** top: `data`. Lazy: `climate` (l.71, 84, 106, 125, 227: the scheduler, when on), `farm` (l.168: crop height for sight).
- **Callers:** `world.cold` (EV.place), `here.py` l.43-60, 381 (Here.weather/wet/snow_lying/since_heavy_rain/weather_values),
  `night` (decay_rate wet; weather_fuel; fire_goes_out), `forests.night` (gale), `renewal.context` (values, snow, wet), `things.py`
  (visibility, open_air, ground_factor), `roads.py` (visibility on roads, fords), `fuse.py`, `layout.py` l.177, `signs.py` (~14 sites:
  weather, snow, wet, spell, since_heavy_rain in sign contexts).

### 1.3 climate.py (390 lines)

- **Responsibility:** the weather scheduler (D4-109, D4-110, D4-111): eras -> year anomaly -> regional daily type (Lamb types,
  Markov hold) -> moving storms -> per-node AR(1) correlated fields of temp/rain/amount/wind/fog -> physical values per node and
  day; label, frost, visibility, spell from them. Switched on by spec `climate:` (`on` l.33).
- **State owned:** none in `w.s`. A cache object `_State` (l.104) stored as `w._climate` (l.266-270), computed from day 0
  sequentially and memoised (`days`, `years`, `storms`, `fields`, `type`). Keyed numpy rngs from seed only, no replicate salt (l.128;
  D4-4: weather is exogenous). Node geometry: `_heights` l.50 (spec `elevation` or parcel height rank -> CLIMATE.height_m),
  `_distances` l.67 (spec `xy`, else road days x km_a_day, Floyd), `_positions` l.87 (classical MDS).
- **Primitives:** none.
- **Data:** `CLIMATE` (temp, temp_sd, diurnal, wet_p, rain_mm, heavy_mm, wind, gale, gust, snow_below, fog_p, height_m, lapse,
  orographic, corr_km, km_a_day, persist, year_sd, year_persist, types, storms, eras, vis, shocks), merged with the spec block
  (`params` l.37 via `world.merge`).
- **Public reads:** `env` l.285 (values at node, or road = mean of ends), `region` l.303, `storms` l.309 (unused outside), `storm_coming`
  l.314 (signs SKY), `label` l.320 (snow/gale/heavy rain/rain/fog/clear thresholds), `vis` l.337, `frost` l.358 (low < 0), `SPELL_OF`
  l.363 + `spell` l.366 (type -> old spell words), `summary` l.379 (analysis).
- **Imports:** numpy, `data.CLIMATE`; lazy `world.merge`.
- **Callers:** `environment` (spell, weather, values, weather_lets), `world.cold` (frost), `night.night` l.23-26 (truth record),
  `renewal.context` (year anomaly), `signs.py` l.1045, 1061 (storm_coming, gale threshold).

### 1.4 forests.py (148 lines)

- **Responsibility:** woods as three stocks per parcel (`wood` trees in timber, `young` growth and `dead` wood in firewood), their
  seeding, nightly growth/shed/rot/gale, forest<->scrub cover switch; and **fuel counted in heat** (`heat_of`, `fuel_order`, `burn`,
  `fuel_words`) used by every fire (D2-156, D2-157, D2-159).
- **State owned:** `s.parcels[*].res.{wood,young,dead}` (S, K, r, kind); `par.cover` (forest<->scrub) and `par.was`.
- **Primitives:** `set_res` (young, dead, wood), `set` (parcel cover, was), `add_res` (brash l.114; unused: verbs does it itself),
  `destroy` (burn l.141).
- **Data:** `FORESTS` (kinds{trees,young,dead,grow,regrow}, shed, per_timber, rot, brash, scrub_below, gale), `ITEMS[*].heat`,
  `PHYSICS.heat.order`, `PHYSICS.regrow_winter`.
- **Functions:** `seed` l.17 (world-file `wood:{kind,...}` or legacy `{S,K,r}` or bare scrub; `year` passed as 4*season_len);
  pure steps `trees_step` l.47, `young_step` l.52, `shed_a_night` l.57, `dead_step` l.62 (also used by capacity); `night` l.67;
  `brash` l.111; `heat_of` l.118; `fuel_order` l.122; `burn` l.127 (all-or-nothing, by order); `fuel_words` l.146.
- **Imports:** top `data`; lazy `night` (slow_season), `renewal` (RULES slow/young/dead + context), `environment` (gale), `data.PHYSICS`.
- **Coupling:** `night` reads `h["count"]` of all herds to skip young regrowth on grazed parcels (l.75) -> forests depends on herds'
  state shape. Gale = `EV.weather(...) == "gale"` (label coupling).
- **Callers:** `world.__init__` l.109 (seed), `night` (burn x2, `FO.night` via `_grow`), `renewal` (pure steps), `prompt.py`
  (heat_of, fuel_words), `run.night_lines` (fuel_words), `verbs.py` l.1720, `landgen/settle.py`, `capacity/fuel.py`.

### 1.5 farm.py (1519 lines) — farming AND cattle

- **Responsibility (two features in one file):**
  (a) fields: crop records per holding, sowing, breaking/turning under, weeding, seed selection, manuring, reaping (ripe or green),
  field works (ditch/terrace), fences and gates as field works, soil fertility (crop take/restore, fallow, grazing, dung, land base),
  plot shares (D2-163, D2-172), the night's crop growth (D4-106), works upkeep;
  (b) cattle: herd counting/words/capacity (used by herds, signs, perceive, roads), herding, milking, slaughter, driving, team
  checks for the plough, and the night's grazing/fodder/hunger/starvation/milk/breeding/dung/grazed fertility.
- **State owned:**
  - parcel: `crop`, `fertility`, `broken`, `last_crop`, `last_kind`, `fallow_since`, `dead` (a crop standing dead), `shares` (list of
    holding records {holder, plots, crop, fertility, broken, last_crop, last_kind, fallow_since, dead?}), `held_whole`, `works`
    {ground, units, done, kept, pending, finished_season}, `fence` {kind, units, level, built, gate, mend, pending, since, opened},
    `slaughter` {day, kills}, reads `land.base_fertility`, `ground`, `size`, `cover`, `res.grass`, `res.dung`.
  - crop record fields: kind, crop (family), sown, ripe_day, window, seed, area, area_left, broken, weeded, base, rot, left, failed,
    shown_failed, hardy, sower, g, progress, q, n, lying, stand, wintered, winter_n, stalled, no_winter, quality, never, reaped,
    selected_by, trampled{day,by,holders,qty}, up_day, frost_day, killed, rotting.
  - herd: `watched`, `herders`{day,n,by}, `milked`{day,n,by}, `in_milk`, `births`, `last_calf`, `hungry`, `count`, role counts
    cows/oxen/bulls/young, `parcel`, `home`, `with`, `pack`, `driven`; creates herds (`new_herd`).
  - `today["turned"]`, `today["green_cut"]` (written directly by acts).
- **Primitives applied:** `set_share` (crop, fertility, broken, dead, last_crop, last_kind, fallow_since), `shares`, `set` (parcel
  works/fence/slaughter; herd fields), `draw` (key "crop" with holder; key "grass"), `create` (stone, straw, slaughter goods),
  `destroy` (fodder), `wear` (plough, harness), `set_res` (dung, with `init`), `new_herd`, `claim` (copy herd claims to new herd).
  Indirect: `verbs._consume` (seed, stone, fence inputs).
- **Inside primitives:** `world.p_draw` (crop branch calls `FM.record`), `p_set_share` (`FM.record`), `p_shares` / `p_claim` /
  `p_end_claim` / `p_plots` (all call `FM.sync`). So the core's primitive table already depends on farm.
- **Data:** `CROPS`, `CROP_OF`, `SEED_CROP`, `TURF`, `FENCES`, `FITTINGS.stalls` (fodder, dung), `ITEMS` (fodder, life), `TECHNIQUES`
  (yield kinds, animals, uses, seasons, slaughter gives), `PHYSICS.farming`, `PHYSICS.cattle`, `PHYSICS.ground`,
  `PHYSICS.master_yield`, `PHYSICS.seed_selection`, `HERDS.capacity`.
- **Imports:** top `knowledge` (skill, level, available, label, curve), `data`, `here` (Refused, show). Lazy: `data.PHYSICS` (l.58),
  `data.HERDS` (l.679), `verbs._party/_src/_consume` (l.561, 838-840, 880, 934, 962: material consumption and party), `outcomes.Bern`
  (blight l.972), `buildings` (`stall_share` l.1265, 1458), `herds` (`HD.night` l.1320), `layout` (`LY.regrow` hidden ways l.1323:
  unrelated to farming), `things` (`leave_carcass` l.1489).
- **Callers (outside):** `verbs` (FM_KINDS dispatch l.91/557 -> `act`; `drive` verb l.2007; `ready` via knowledge l.165;
  `team_shortfall`; `beasts_note`; `holdings`, `names_of`, `possessive`, `LAND`, `named`, `against`, `base`, `head`), `world`
  (seeding: fence_need, normalise_crop, grow_days, sync, seed_crops; primitives), `herds` (head, standing, record, fence_need,
  fence_word, herd_words, herd_capacity, ROLE_WORD), `signs` (field/crop/herd contexts: view, main_rec, standing, the_crop,
  the_part, started, rate, weed_gain, herd_words, head, records, plots_of, named, fence_need), `perceive`, `prompt` (crop_words,
  held_words, LAND, ready for gates), `environment` (main_crop), `layout` (main_crop), `roads` (head, herd_words), `agreements`
  (LAND, holdings), `exchange`, `lore` (grow_days, season_run), `life.on_death` (sync), `run.dawn` (standing, main_crop for the
  stray incident), `capacity/*` (pure crop and soil functions), `landgen/economy.py`.

### 1.6 herds.py (510 lines)

- **Responsibility:** herds that nobody holds and herds on the move (D2-117, D2-123, D2-124, D2-127, D2-128, D2-130..D2-132, D2-136,
  D4-54, D4-56, D4-114): fence build/wear/mend nightly accounting, splitting by handling capacity, wandering on the node toward
  attractive parcels (crops, grass, water), trampling crops, home at dusk, onto/off roads, drifting and dying on roads, merging split
  groups back, pack oxen (choose, lead, feed, let go), driving on a road, accompanying a party.
- **State owned:** herd fields `parcel`, `node` (a node **or a road id**: a herd on a road has node=road), `pos` (stretch),
  `lost`{day,from,road}, `gone`, `strayed_in`, `with` (leader), `pack`, `ate`{day,q} (handoff to farm._herds), `split_of`,
  `split_day`, `base_name`, role counts, `count`, `in_milk`, `hungry`, `name`. Parcel `fence` (night accounting). Crop
  `trampled` (via set_share).
- **Primitives:** `set` (herd, parcel fence), `draw` (crop, per holder), `set_share` (crop trampled), `split_herd`, `claim`,
  `destroy` (hay from leader's hands); via `things.leave_carcass` (`new_thing`, `create`).
- **Data:** `HERDS` (steps, good_grass, draw, dusk, trample, onto_road, own, road, capacity, split, share, call, pack_ox), `FENCES`
  (through, mend, decays), `THINGS.carcass_road`, `TECHNIQUES.slaughter.yield.gives` (carcass meat).
- **Imports:** top `farm` (head, standing, record, fence_need, fence_word, herd_words, herd_capacity, ROLE_WORD), `layout`
  (`_layers`, `path`, `road_ends`, `default_end`, `parcels_of`: the parcel graph), `data`. Lazy: `things`, `data`, `roads`
  (`position`, `stretch`, `_note`), `tags` (label of led ox).
- **Callers:** `farm.night` (HD.night), `roads.night` l.144-146 (`follow`, `feed_pack`), `roads` l.411-432 (`on_stretch`, `split` with
  drovers), l.581-610 (`drive_stretch`, `accompany`: fuse-call outcomes), `run.arrive` l.435 (`arrive_with`), `night.departures`
  l.230-238 (`pack_ox_for`, `lead_ox`), `world.capacity` l.478 (`pack_oxen`), `here.py` l.116-122 (`pack_ox_for`, `led_by`),
  `signs.person_context` l.1015 (`led_by`).

### 1.7 night.py (482 lines)

- **Responsibility:** the night step orchestrator (spec/core/round.md) plus several features' night code inlined: sleeping places
  and beds, house fires and heat, camp fires in weather, open fires, gear for sleeping out (tents/bedrolls), eating and cooking,
  hunger and cold falls, starvation hazard, spoilage by condition, camp lapse, building breaks (and painted lines fading),
  resource regrowth driver (`_grow`), offer lapse, departures at nightfall. Pure helpers shared with the capacity model:
  `spoil_rate`, `eaten_worth`, `eat_order`, `regrow`, `slow_season`, `house_heat`.
- **State owned/written:** person `hunger` (via harm), `missed`, `slept_out`, `ate_raw`, `home_seen`, deaths; building `fire`,
  `warm`, `fire_out`, `condition`, `broke`, `lines`, `changes`; containers' goods (eating, spoilage, burning, rot); offers `open`;
  `s.log` (append rec, direct); `today["_floor"]`, `today["_departed"]` (direct); parcel res S (via `set_res` in `_grow`).
- **Primitives:** `set` (person/building), `harm`, `die`, `destroy`, `create` (rotting meat; rot `becomes`), `wear` (tent, bedroll),
  `close_offer`, `set_res`, `depart`, `transit` (departures).
- **Data:** `DECAY`, `EDIBLE`, `FITTINGS` (`fire` flag -> FIRE l.13; `spoil` keeping), `ITEMS` (food, raw, cook, spoil, decay),
  `THINGS.carcass_fresh_days`, PHYSICS (`heat`, `beds`, `breaks`, `hazard`, `cold_starving`, `ration`, `house_spoil`,
  `regrow_winter`, `game_threshold`).
- **Imports:** top `life`, `needs`, `data`, `world.Refused` (unused). Lazy: `climate` (truth record), `settle` (fights), `buildings`
  (`read`, `floor`, `spot_words`), `forests` (burn, night), `labour` (work_need, fade), `herds` (pack ox at departure), `layout`
  (wear_way), `roads` (position), `life` (infants_of), `environment` (weather, wet, snow_lying), `things` (where, KINDS),
  `renewal` (rules, context), `farm` (night).
- **Callers:** `run.py` (N.departures l.1070, N.night l.1076, morning departures l.446), `prompt.py` l.709 (house_heat),
  `renewal` (regrow), `forests` (slow_season), `capacity/food.py`, `fuel.py`, `sources.py` (spoil_rate, eaten_worth, slow_season, regrow).

### 1.8 life.py (562 lines)

- **Responsibility:** life stages by days since birth, lifespan scaling, coming of age (child -> youth agent with a model), household
  succession (dawn), care gifts (food to a child, a sentence passed on into its kept memory), partnerships, children's standing-order
  work, ration factors, pregnancy (conception, road loss, birth and its risks), deaths of the young, old age, childhood memories,
  death's succession and inheritance (incl. field plots). D2-138..D2-153, D4-19, D4-20, D4-64, D4-69, D4-97.
- **State owned:** person `stage`, `born`, `parents`, `sex`, `partner`, `pregnant`, `father`, `gap_until`, `cared`, `model`,
  `widowed_of`(world.p_die); `s.mind[name].childhood` and `.lasting` (direct), `s.know[name]` (direct, come_of_age);
  institution `offices.head`, `heir`, `succession`{until, named}, `order`; `s.claims` (inheritance: ends and creates claims).
- **Primitives:** `set` (stage, model, pregnant, father, gap_until, cared), `office` (head, succession), `partner`, `born`, `die`,
  `transfer` (care gift). Inside `p_die`: `on_death` mutates `h["offices"]`, `h["succession"]`, `h["heir"]`, `c["until"]`, calls
  `w._claim` and `FM.sync` directly (inside a primitive). **Outside any primitive:** `_childhood` (l.492-500) writes
  `w.s["mind"][name]["childhood"]`; `come_of_age` (l.159-170) writes `mind.lasting` and `s.know` directly; `care_gifts` calls
  `MEM.seed_line` (memory module writes).
- **Data:** `LIFE` (lifespan, shares, conceive, pregnancy, birth, gap, infant, child, dial, old_age, succession_days,
  children_work, child_skill), `TECHNIQUES` (children's work verb; crafts as awareness), `ITEMS.food`.
- **Imports:** top `math`, `data.LIFE`. Lazy: `memory` (come_of_age, kept, seed_line, line, kept_settings), `knowledge` (basic),
  `verbs` (`V.do` for children's work), `here` (Here, Mind), `farm` (sync on inheritance), `data`.
- **Callers:** `night` (ration_factor, care_gifts, feeders, MINOR, night, infants_of), `run` (dawn, settle, children_work),
  `world` (`_person` stage_of/lifespan, `load` carried_weight, `units_for` unit_penalty, `p_die` on_death), `here`
  (showing, grows_in, on, dial, in_gap, age_line), `signs.person_context` (infants_of, days_old, lifespan, elder_from), `perceive`,
  `memory`, `generate`, `clocks` (lifespan), `lore`, `prompt` (age_line via Here), `capacity/model.py` (ration_factor, lifespan,
  elder_from), `landgen/economy.py`.

---------------------------------------------------------------------------------------------------------------------------------

## 2. THE NIGHT: exact order

The night is not one function. In `run.run` (day loop) the sequence after the day's work is:

```
run.py l.1059  LA.close_day(w, today, used, budget, names)            [labour] units used -> today["units"], fatigue
       l.1060  J.open_step(day, "settle")
       l.1061  today["partners"] = LF.settle(w, today)               [life: partnership] apply partner
       l.1062  today["children_work"] = LF.children_work(w)          [life: children] runs V.do(...) acts for each child
       l.1063  AG.settle(w); ST.settle_teaching/joins/thefts         [agreements, teaching, membership, theft]
       l.1067  w.s["left"] = ...                                     [goods left at a building, for dawn]
       l.1069  J.open_step(day, "night")
       l.1070  N.departures(w, today)                                [travel] (night.py l.213)
       l.1071  RD.night(w, today)                                    [roads] incl. HD.follow, HD.feed_pack, herd finds, driven splits
       l.1072  FU.plan(w, today) / fuse_calls(...)                    [fuse events] woken agents answer
       l.1076  rec = N.night(w)                                      [night.py l.17, below]
       l.1077  rec["fuse"], rec["road"]; PC.evening; night_lines; memory step
```

### 2.1 Before N.night (run.py)

| # | Step | Code | Feature |
|---|---|---|---|
| a | Work's food and fatigue recorded | `labour.close_day` | labour |
| b | Partnerships both chose | `life.settle` l.221 (apply `partner`, event) | life: partners |
| c | Children do the household's standing order | `life.children_work` l.235 (`V.do` acts via Here/Mind; dial `child_works`) | life: children |
| d | Departures at nightfall: home_seen snapshot, pack ox chosen, `depart`, `LY.wear_way`, `transit`, `HD.lead_ox`, infants carried | `night.departures` l.213 | travel / herds (pack ox) / life (infants) |
| e | Roads' night: `HD.follow` (led herds keep pace), `HD.feed_pack` (pack ox grazes or eats leader's hay), meetings, finds incl. `_herd_finds`, `_driven_splits` (`HD.split(drove=n)`) | `roads.night` l.138 | roads / herds |
| f | Fuse sub-step | `fuse.plan` | fuse |

Dependency: departures before roads' night and fuse (night.py l.214 docstring) so leavers are on their first stretch; before
`sleeping_places` (departed have `at=None` -> sleep out on the road).

### 2.2 Inside night.night (night.py l.17-210), in order

| # | Line | Step | Feature |
|---|---|---|---|
| 1 | 20 | `cold` flag: any node cold tonight (`w.cold`) | weather (record) |
| 2 | 23-26 | truth record: each node's climate values + label | climate (record) |
| 3 | 27-30 | `ST.settle_fights(w, today)`; killed -> `rec["deaths"]` | conflict |
| 4 | 31 | departures recorded (`today["_departed"]`, or run now if not run) | travel |
| 5 | 32 | `sleeping_places` l.307: members at home by bed share (eldest first, `STAGE_ORDER`), then chosen/guest/access buildings, else home floor (`today["_floor"]`), infants with mother | shelter / lodging (beds) / life (bed_share by stage) |
| 6 | 34-36 | `rec["slept"]`, `rec["floor"]` | shelter (record) |
| 7 | 37-40 | `BL.read(w, n, b, "slept")`: sleepers read lines written in the building | buildings (lines) / senses |
| 8 | 41-43 | set person `slept_out` {day, cold} for those out (for signs D4-74) | shelter / signs |
| 9 | 46-72 | **house and camp fires**: for each building with sleepers and a FIRE fitting: heat = camp `heat.camp x weather_fuel` or `house_heat` (cold doubles x4); `FO.burn` from the store, then woodpiles at the door; camp fire may go out in weather (`fire_goes_out`) -> `fire_out`; `warm` = spaces(hearths x12 + rings x6)/floor, ring-only house half; set `fire`, `warm`; `rec["hearth"]`, `rec["fire_need"]` | fire/heat (forests fuel), buildings, weather |
| 10 | 73 | `open_fires` l.367: those sleeping out grouped by node or road party; lighters burn `heat.open x weather_fuel` from hands; warms up to `heat.share` (4); may go out | fire/heat, weather, travel |
| 11 | 74 | `LF.care_gifts` l.176: per child, the carer giving the most food transfers it to the child's hands; sentence passed -> `MEM.seed_line` | life: care / memory |
| 12 | 76-148 | **eating loop**, per `w.living()` (alphabetical): shelter `state` (unsheltered/damaged/housed, floor -> beds.floor, works upgrade -> floor, cold & no fire -> no_fuel); `gear` (camp, or `_gear` l.280: own tent (wear), share a tent (2), bedroll (wear)); road camp; `LF.ration_factor`; `LA.work_need`; `NE.food`; stores = hands, takeable stores here (slept-in stock first), carers' hands for minors (`LF.feeders`); hearth lit or open fire -> cooking; `_eat` l.434 (`destroy` "eaten", by `eat_order`); `uncooked`, `ate_raw`; work share (`work`, `work_short`); hunger +1 / short / -1 and `missed`; **cold fall** for unsheltered on cold or soaked nights (`harm hunger=-2`) | hunger/eating, shelter, gear, fire/cooking, life (ration, feeders), labour, roads (fed, soaked), weather |
| 13 | 149-160 | **starvation hazard**: `missed >= 3` -> chance `frailty + hazard.step*(k-1)` or certain at `max_rounds`; `die` "starvation"; skipped on the last day of the run | hunger / death |
| 14 | 161-162 | `LF.night` l.337: `_conceive` (if children on), `_pregnancies` (road loss, `_birth`: risks by housed/camp/out, helped halves, `born`, `die`), `_young` (infant/child deaths by care, hunger, shelter, cold, fire), `_old_age`, `_childhood` (memories) | life: pregnancy, birth, young deaths, ageing deaths, childhood |
| 15 | 163-179 | **spoilage**: every container (skip dead people's hands): carcass meat goes off after `carcass_fresh_days` -> "rotting meat"; else `decay_rate` l.248 (stock: keeping fittings; things: open_dry/open_wet/buried; hands) x season/frost; lost share may `create` its `becomes` | goods decay, things (carcass), weather (wet, cold) |
| 16 | 180-184 | camps fall in at `lasts_until` (condition 0, `broke`, event) | buildings / lodging (camp) |
| 17 | 185-197 | **breaks**: chance by cold x structure; condition -1, `broke`; a painted line on wattle fades (`lines`, `changes`) | buildings (wear) / lines |
| 18 | 198 -> 466 | `_grow`: for each parcel stock whose rule is in `renewal.NIGHTLY` (fast, threshold, periodic): `RN.RULES[rule](p, r, RN.context(...))`, `set_res`; then `FO.night` l.67 (trees slow, young regrows unless herd on parcel, dead shed+rot, gale windfall, forest<->scrub) | renewal (wild stocks, grass, fish), forests |
| 19 | 199-200 | `LA.fade`: unpractised skills fade (direct writes to `s.know`) | labour / knowledge |
| 20 | 201-202 -> farm.night l.1316 | (20a) `_crops` l.1356: `_works_night` l.1328 (pending works count if led; seasonal upkeep or decay x0.75); per field: re-sync shares if claims ran out (`shares`); per holding record: blight shown at progress 0.5; `grow_night`; `set_projection`; frost kill; rot after window; crop slot end -> `soil_step`, `last_crop`, `fallow_since`, `dead`; fallow gain if no crop and no herd on the parcel. (20b) `HD.night` l.27: `_fences` (pending build counts if led, mending restores a level, yearly decay), per herd: on road & unled -> `_on_road` (gone, die per head with carcass, drift, off_road); led -> stays or `let_go`; `split`; then `wander` for unled herds on nodes (fence odds, road onto, `trample`, `home_at_dusk`); `_merge`. (20c) `LY.regrow` (hidden ways grow back). (20d) `_herds` l.1440: winter stall share; eat what it trampled (`h.ate`), grass `draw`, fodder from holders' stores (`destroy`); `hungry`; milk decay, hungry milk; starvation of one beast at `starve_nights` (`leave_carcass`); breeding with bull and cows when fed (`births` accumulator, `young`, `last_calf`, milk +1); dung `set_res` (stall-kept); grazed-field fertility per holding; `count` | crops/soil, field works, fences, herds (animals), layout (ways) |
| 21 | 203-208 | offers lapse (offerer gone/dead, or `until` reached) -> `close_offer` | market / offers |
| 22 | 209 | `s["log"].append(rec)` | record |

### 2.3 After N.night (run.py), and dawn

- `night_lines` l.613: per-person lines from `rec` (fire out, ate less, cold fall, births, fire need with `FO.fuel_words`, damage).
- `PC.evening`, `PC.close_day`, memory calls (memory step).
- Next day: `w.s["day"] = day` (l.867). **Dawn** `run.dawn` l.363: spec incidents (`stray`: a herd breaks into a field and eats
  `eats` from every holding's crop, FM.standing; `death`; `fire` in a store), goods left announced, **`LF.dawn`** l.111 (stage by days
  old -> `set stage`; child->youth `come_of_age` (model, childhood memories -> lasting, household crafts as awareness); succession
  naming window ends -> `office head`), arrivals (carried infants; `arrive` -> `HD.arrive_with` brings accompanied herds / pack ox),
  spec signs; then `PC.dawn`.
- **No night step at all** for: climate (pure, cached on demand), fitting/tool wear by time (wear.py computes lazily from day/year),
  clocks, fence decay outside `_fences`.

### 2.4 Ordering dependencies (what a registry must express)

1. **fights (3) before sleeping (5) and eating (12):** the dead neither sleep nor eat; fight deaths go into `rec["deaths"]`.
2. **departures (d, 4) before sleeping (5):** travellers sleep out on the road; `today["_departed"]` reused if run already.
3. **sleeping (5) before everything per-person:** `where` feeds BL.read (7), slept_out (8), fires (9: sleepers per building), open
   fires (10: who is out), eating state (12), conception (14: slept together), birth risk (14: housed/camp/out, helper in same
   building), infant shelter (14).
4. **house fires (9) before eating (12):** `b["fire"]` decides no_fuel state, cooking (`hearth`), `warm`; `fire_out` decides
   `fire_gone`. Also before life (14): `_birth` housed needs fire on a cold night; `_young` reads `fire`, `fire_out`.
   Fires burn fuel from the same store the eaters then eat from (fuel isn't food, so no contention today).
5. **open fires (10) before eating (12):** `fires` set -> `open_fire` in needs and cooking.
6. **care gifts (11) before eating (12):** the food moves into the child's hands and `care_fed` raises its need.
7. **eating order = `w.living()` sorted by name:** shared stores and shared tents are first-come; the tent allocation lives in the
   eating loop (side effect: `wear` on tent/bedroll).
8. **eating (12) before starvation (13):** uses `missed` just updated.
9. **eating (12) before life (14):** conception skips anyone in `rec["missed"]`; birth housed requires mother not missed; young
   deaths scale with `missed`.
10. **life (14) after starvation (13):** someone who starved does not conceive/give birth (they are not `living()`).
11. **spoilage (15) after eating (12):** tonight's meal is taken from undiminished stores; carcass meat rot after eating.
    Spoilage before herds' fodder (20d): fodder taken after its spoilage (hay/straw do not spoil; green crops do).
12. **camp lapse (16) before breaks (17):** a fallen camp (condition 0) cannot break further.
13. **renewal (18) before herd grazing (20d):** herds graze tonight's regrown grass.
14. **forests (18) before herds wander (20b):** young growth is suppressed by herds on the parcel *before* they move (uses
    `h["count"]`, not FM.head).
15. **crops (20a) before herds (20b):** crops grow/ripen tonight, then herds trample what stands; `grazed` (fallow vs grazed
    restore) is decided from herd positions *before* they wander.
16. **HD.night (20b) before farm._herds (20d):** `trample` writes `h["ate"]` that `_herds` counts as fodder; splits/merges/roads must
    settle before feeding (feeding skips herds on roads; a split group feeds on its own).
17. **_crops (20a) before _herds (20d):** a crop ended tonight leaves a bare record that the grazing restore can touch the same night.
18. **fences (20b, first) before wandering:** a fence finished tonight holds tonight.
19. **roads' night (e) before HD.night (20b):** `HD.follow` places led herds; `_on_road` skips led herds; `feed_pack` sets `hungry` before
    `_herds` (which skips road herds anyway).
20. **offers lapse (21) after everything:** reads `alive` and `at` after deaths.
21. **dawn: LF.dawn before arrivals:** stage changes before travellers come in; `come_of_age` after the night's memories.
22. Random streams are keyed (`w.rng(tag, day, ...)`), so reordering steps does not change draws, **except** where state written by
    an earlier step changes a later step's inputs (all the above).

---------------------------------------------------------------------------------------------------------------------------------

## 3. NEEDS: what feeds a person's food/heat need

All composed in `night.night` l.76-105 and `needs.food`. Heat itself is never a person's need: heat is fuel burnt by a fire; its
effect on the person is through the food need multiplier and the cold fall.

| Factor | Where computed | Effect in `needs.food` | Feature |
|---|---|---|---|
| base ration | `PHYSICS.ration` | need base | hunger/eating (core) |
| shelter state housed/damaged/unsheltered | night l.81 from `where`, `b.condition` | x `shelter[state]` or `shelter_cold[state]` | shelter / buildings |
| no bed -> floor; building being upgraded -> floor | night l.82-83, `beds.floor` ("damaged") | treated as damaged | lodging (beds), buildings (works) |
| cold night at the sleeper's place | `w.cold(node)` (spec cold_days / climate frost / winter) | selects `shelter_cold`; enables cold fall | weather/climate |
| no_fuel (housed, cold, fire not lit) | night l.84 | `shelter_cold.no_fuel` | fire/heat |
| partial warmth `warm` <1 on a cold night in a house (not camp) | night l.46-70 (hearth/ring spaces / floor) | no hearth: `heat.ring_cold`; else interpolate warm..no_fuel | fire/heat, buildings (floor, fittings) |
| gear: camp building | night l.87 | `camping.camp` [normal, cold, fall] | lodging (camp) |
| gear: tent / shared tent / bedroll / out | `_gear` l.280 | `camping[gear]`, sets `fall` | travel gear (items) |
| camp: cold and fire not lit or gone | needs l.40 | `camping.out` cold, fall 0 | fire/heat, weather |
| open fire (not camp), cold, not gone out | `open_fires` l.367 | `camping_fire[gear]`, fall 0 | fire/heat, weather |
| fire gone out in rain/gale | `fire_goes_out` l.416 | disables the above | weather, fire |
| fed on the road at a good place | `today.road.fed` (roads.night) | cap need at `fed` x ration | roads/travel |
| stopped at a good camp place on the road | `today.road.camp` | gear = camp | roads/travel |
| infant 0.5 / child by dial | `LF.ration_factor` l.261 | x mult | life |
| pregnancy +0.3 | `LF.ration_factor` | + extra | life |
| day's work and guard watch | `LA.work_need` (labour.py l.24) | + work | labour |
| care gift | `LF.care_gifts` l.176 | need = max(need, care_fed) | life: care |
| cooking (raw is worth less) | `eaten_worth` l.424, `eat_order` l.429; hearth = lit FIRE fitting or open fire | lowers what food gives, not need | fire/cooking, goods |
| who may be eaten from | hands, `w.takeable` stores (slept-in first), carers' hands for minors (`LF.feeders`) | supply | goods/claims, life |
| "full" threshold (short vs missed) | l.123-130: ration x mult + extra (+ work) | short meal counts as eaten | hunger |
| cold fall | l.145-148: unsheltered & (cold or `today.soaked`) chance `cold_starving x max(fall, 0.5 if soaked)` -> hunger -2 | separate from need | weather, roads (fords), gear |
| hunger effects | `world.units_for` (hunger -1/-2), `world.yield_mult` (`hunger_yield`), `missed` -> hazard | consequences | hunger |
| frailty | `a.frailty` seeded in `world._person` | starvation hazard base | hunger/death |

Heat demand of a fire (fuel, not person): `house_heat` (cold x4, per hearth count; ring alone 1), camp `heat.camp`, open `heat.open`,
x `weather_fuel` (rain/gale/snow labels, snow lying) for unroofed fires; `heat.order` firewood > timber > charcoal; woodpiles at the
door (D4-89).

---------------------------------------------------------------------------------------------------------------------------------

## 4. FARMING

### 4.1 The model

- A **field** is a parcel with `cover == "field"` counted in **plots** (`size`). Seed is in plot-seed units (`farming.plot_seed` 16).
- **Holdings (D2-163, D2-172):** claims on a parcel may name `plots`. `layout(claims, size)` l.239 -> (holders of the whole, {holder:
  plots}). The parcel's own fields (`crop, fertility, broken, last_crop, last_kind, fallow_since`, `REC` l.234) are the record of the
  ground held whole, or of the unclaimed plots (holder `None`); each part holding has a record in `par["shares"]`. `sync` l.440
  re-balances records when claims change: plots lost go to a pool carrying fertility and broken ground; gains draw from the pool,
  then unclaimed; with `carry` (seeding, inheritance) standing crops follow plots split pro rata (`scale_crop`/`merge_crop`); else a
  crop stays its sower's until reaped. `sync` mutates `par` directly; it is called only inside primitives (`claim`, `end_claim`,
  `shares`, `plots`, and `die` via `life.on_death`) and in world seeding.
- **Crop record** (one per holding): see 1.5. `left` is always recomputed by `crop_left` l.34 = base x (1+weed_gain) x
  area_left/area x rot. `base` set at sowing by `crop_base` l.66 = seed_eq x (ratio + break_gain x broken_share) x fertility x
  ground_mult x skill_yield, x CROPS yield x turf factor.
- **Growth (D4-106):** `grow_night` l.100 (pure): seed lies until the season's rate > 0 and not cold (loses `lie_loss`); tender crops
  lose `frost_loss` stand on winter/cold nights, killed below 2%; winter grain counts `vernal` winter nights, stalls at 0.9 without;
  progress += rate/g; ripe -> quality = mean rate (x `needs_winter` if unvernalised) scales base. `started` l.83 upgrades older
  records. `set_projection` l.174 re-projects `ripe_day` each night at the field's place (`never` if cold kills first).
  `season_run` l.148, `projected_ripe` l.163 (capacity model, lore).
- **Failure (blight):** at sowing, `Bern(fail_chance)` keyed rng("blight", day, key[, holder]) (l.970-973); shown at progress 0.5 at
  night (event), withers, `left` 0 once shown.
- **Soil (D4-39, D4-112):** fertility per holding; `soil_step` l.210 at crop slot end (crop takes `takes`, restores toward
  `restores` level x land base); `fallow_gain` l.197 nightly when no crop and no herd; grazed restore in `_herds` l.1512-1518
  (`farming.grazed`); `manure_gain` l.204 (act); `turned_under` gain (act); `base(par)` l.190 = `land.base_fertility`.
- **Rot:** after ripe_day + window, `rot` x (1-`farming.rot`) a night.
- **Ground:** `ground_mult` l.817: wet/hill ground penalty (`PHYSICS.ground`) lifted by field works done.

### 4.2 Acts (all via `farm.act` l.737, an if-chain on `TECHNIQUES[tech].yield.kind`)

| yield kind | techniques (data) | code | what it does |
|---|---|---|---|
| sow | sow (+ modifiers e.g. method: dibble) | `_sow` l.918, `sow_targets` l.1022, `_sow_why` l.1032 | seed from `SEED_CROP`/`CROP_OF`; fills own unsown plots then unclaimed; new crop record (blight, grow_days, seed selection, name from last_kind); uses broken ground; base; turf note; cold note |
| break | hoe, plough (animals oxen 2, uses plough+harness) | `_break` l.1094, `_turn_under` l.1065 | breaks unsown ground (stone created, plough/harness wear); over a standing crop turns it under (soil gain, broken) |
| works | ditch (wet), terrace (hill, stone) | `_works` l.830; night `_works_night` l.1328 | project units count only on a day someone who knows leads; upkeep per season |
| fence | fence (wood), wall (stone, led by "wall") | `_fence` l.868; night `herds._fences` l.60 | materials in proportion; build pending until led; mend; fallen keeps half |
| gate | open the gate / shut the gate (0 units) | `_gate` l.898 | set gate, event seen by holders |
| select | select seed | l.756-760 | marks `selected_by` (actual effect: sower's `KN.level("select seed")` at sowing) |
| tend | weed | l.765-776 | `weeded` += m; no gain when ripe or clean |
| manure | manure (inputs dung) | l.777-783 | `manure_gain` on the holding |
| crop | reap | `_reap` l.1124 | `draw` crop (area with it); green before ripe -> CROPS `green` good x (g0 + g1 progress); straw created; light ears note |
| herd / milk / slaughter | herd, milk, slaughter | l.786-803, `_slaughter` l.1165 | cattle (section 5) |

- Gating: `ready` l.1187 (season window, sow/target/team/fence/gate/works/select/herd/milk preconditions) is called by
  `knowledge.py` l.165 and `prompt.py` l.356. `target` l.624 decides whose holding (own, unclaimed, sole candidate, or `on` required);
  `against` l.660 notes working another's plots. Refusals are prose strings.
- **Data vs code:** crop families, seed goods, growth by season, hardiness, takes/restores, straw, green good, names, yields: data
  (CROPS). Fence kinds and numbers: data (FENCES). Technique rates (plots per unit, seed per unit, straw, stone): data. Everything else
  (holding model, sync, crop lifecycle, works/fence project logic, refusal prose, act result prose) is code.

### 4.3 Bespoke or hard-coded paths

- `verbs.FM_KINDS` l.91 tuple and `elif y["kind"] in FM_KINDS` l.557 -> `FM.act`; `act` is an if-chain on 12 kinds.
- `p_draw` key `"crop"` special branch (world l.647) and `p_set_share`, `p_shares`, `p_claim`/`p_end_claim`/`p_plots` -> `FM.sync`:
  the **core primitives depend on farm**.
- `cover == "field"` tests throughout (`_crops`, `named`, `main_crop`, `sync`, `ready`, `crop_high`); `LAND = ("field","pasture","meadow")`
  l.235 (claims may name plots; also `life.on_death` l.535 hard-codes the same tuple); `TURF` (data).
- `grow_days(year, "grain")` used as the fallow slot (l.1361, 1445): grain-specific.
- `_works_night`: `tech = "ditch" if wk["ground"] == "wet" else "terrace"` l.1336; `_works_word` l.914; world seeding hard-codes
  `tech_y = 40.0 if wet else 60.0` (world l.140) duplicating TECHNIQUES units.
- `KN.level(mind, "select seed") == "known"` l.975 (technique name in code).
- `tech == "plough"` for words and `item == "wooden plough"` wear rule (l.1090, 1115).
- `normalise_crop` default family "grain"; `_f_default()` reads global PHYSICS, not w.p (seeding ignores spec physics overrides).
- `frost_kills` l.185 is the pre-D4-106 rule, still used by `capacity/cal.py` (possible divergence from `grow_night`).
- Unused data: `PHYSICS.farming.dung_per_plot`, `PHYSICS.cattle.stray`, `PHYSICS.cellar_spoil`; unused code: `soil_word`,
  `environment._worked_techs`, `forests.brash`.

### 4.4 Generic or other-feature functions living in farm.py

- **Animals:** `ROLES`, `ROLE_WORD`, `ROLE_OF` l.24-26; `head` l.673; `herd_capacity` l.677; `herd_words` l.688; `_own_or_free`,
  `usable_herds`, `beasts_note`, `team_shortfall` l.694-733 (animal teams for any technique with `animals`); `_herd_on` l.807;
  `_slaughter` l.1165; `drive` l.1252; `_fodder_stores` l.1426; `_herds` l.1440 (the animals' whole night: grazing, fodder, hunger,
  starvation, milk, breeding, dung). Used by herds.py, signs.py (HERD, ASTRAY, EMPTY, herd_context), perceive.py, roads.py,
  verbs.py (`head` in technique `when`), here.py.
- **Claims/holdings words:** `names_of`, `who_words`, `short_words`, `possessive`, `owner`, `held_words` (generic holding-of-plots
  vocabulary; used by verbs claim and prompt).
- **Fences:** `fence_need`, `fence_word`, `_fence`, `_gate` (enclosure, used by herds and signs FENCE).
- **Night orchestration:** `farm.night` calls `HD.night` and `LY.regrow` (hidden ways: layout feature).
- **Stalls:** via `buildings.stall_share` (buildings feature) in `_herds` and `drive`.
- **Carcass:** via `things.leave_carcass`.

---------------------------------------------------------------------------------------------------------------------------------

## 5. HERDS (animals)

### 5.1 What a herd is

A row in `w.s["herds"]` keyed by id (`H...`, `<id>-2` for splits), its own entity kind (place-checked: `world.place_of(("herd",
hid))` -> its `node`, which may be a road id). Not a container; beasts are counts, not goods. Fields:

| Field | Set by | Meaning |
|---|---|---|
| node, parcel, home | seeding, wander, drive, onto/off_road | where; `node` = road id while on a road, `parcel` None |
| pos | onto_road, _on_road, follow, drive_stretch | stretch on a road |
| name, base_name, tag, kind ("cattle") | seeding, splits, tags | identity (TG.herds_at_start / new_herd) |
| cows, oxen, bulls, young, count | everywhere; `count` cached = head | roles (D2-63) |
| in_milk (float), milked{day,n,by} | _herds, milk act | milk |
| births (accumulator), last_calf | _herds | breeding (D4-44) |
| hungry (nights) | _herds, feed_pack | hunger |
| watched, herders{day,n,by} | herd act | herded today |
| with, pack | lead_ox, accompany, let_go, drive | led/accompanied |
| lost{day,from,road}, gone, strayed_in | herds on roads | |
| split_of, split_day | p_split_herd | for _merge |
| ate{day,q} | trample | handoff to _herds |
| driven{day,from,to,by} | drive | for signs DRIVEN |

Claims on `("herd", hid)` are the ownership (copied on split/new herd).

### 5.2 Behaviours

- **Grazing** (`_herds` l.1467-1469): draw `grass` (min reserve 5% K) up to head x 1; grass seeded on covers by
  `PHYSICS.cattle.grazing` share x `grass_per_plot` (world l.120-123), regrows as RESOURCES `grass` "fast" rule in `_grow`.
- **Fodder** (l.1470-1476): from stores of buildings at the node claimed by the herd's holders; items with `ITEMS.fodder`, perishable
  first. Winter stalls cut need (`FITTINGS.stalls.fodder`) and keep dung (`stalls.dung`).
- **Hunger/starvation:** fed if >= 90% need; `hungry` counter; >=2 milk x `hungry_milk` + event; >= `starve_nights` one beast dies
  (young first) -> carcass (`TH.leave_carcass`, "starved" meat share).
- **Milk:** `in_milk` decays by 1/(in_milk_share x year); calving adds 1 up to cows; milk act takes `min(cows a unit, in_milk - milked)`
  x `each`; milk good spoils same day (ITEMS).
- **Breeding:** fed and bull with cows: accumulator `cows x births x survive / year` -> `young` +1 per whole. No ageing of young into
  cows/oxen/bulls (young stay young). Bull kept apart (drive) prevents breeding.
- **Dung:** `res.dung` S += head x dung/year x stall factor (`set_res` with init K 1e9); `dung` gather technique draws it; manure uses it.
- **Slaughter** (act): one beast of a role -> TECHNIQUES gives (meat, hide); parcel `slaughter` record for signs.
- **Herding** (act): `watched`; herders count -> capacity 30 each (`HERDS.capacity`); unherded 6; drovers 10.
- **Driving on node** (`farm.drive` l.1252, verb "drive"): move whole or part (makes `new_herd` with same claims, or joins a herd held
  the same way); winter stalls behind a barred door refuse; covers list hard-coded l.1262.
- **Wandering / straying** (`herds.wander` l.133): unless herded; fence odds (`through`); steps 0-1 fed on good grass, up to 8 if
  hungry/drawn by ripe crop/poor grass; target by value (food share, ripe pull, water when hungry) x 0.8^dist x fence; onto a road
  from a road-end parcel (`onto_road`); `trample` crops (1% a head a day, per holding, recorded on crop); `home_at_dusk` (D4-54).
- **Splitting** (`split` l.379): chance by head vs capacity; Laplace share; `split_herd`; claims copied; `_merge` rejoins.
- **Roads** (`_on_road` l.249): gone for good, deaths per head (winter higher) with road carcasses (none/hidden/by road), random
  drift, off at an end -> home or stray at the far node (event). Finds by travellers and driven splits are roads/fuse calls
  (`roads._herd_finds`, `_driven_splits`; fuse resolutions `drive_stretch`, `accompany`).
- **Pack ox** (D2-136): `pack_ox_for` (needs a harness), `lead_ox` (split one ox, `pack`, `with`), carried capacity (`world.capacity`,
  `HERDS.pack_ox.carry`), `feed_pack` (graze on grass terrain or eat `hay` from the leader's hands), `arrive_with`, `let_go`,
  `led_by`, `pack_oxen`.
- **Predation/wolves:** none in the engine (spec environment/wildlife.md and livestock.md l.130 list wolves/night folds as open).
- **Data vs code:** numbers are data (`HERDS`, `PHYSICS.cattle`, `FENCES`, `FITTINGS.stalls`, `ITEMS.fodder`, slaughter gives). The roles,
  the single kind "cattle", role words, the young-first order (l.391, 1169, 1487), breeding rule, milk dynamics, wandering and
  value function, road dynamics are code. `kind` exists but nothing dispatches on it.

### 5.3 Is a herd a new kind of primitive object? What an "animals" package would register

Yes: a herd is a first-class entity kind alongside person, building, parcel, container: it has a place (node or road + stretch),
claims, tags, signs and its own primitives (`new_herd`, `split_herd`) and is a valid `ref` kind in `p_set`/`place_of`/`claim`.
It is a *count-of-roles aggregate*, not individual animals.

An **animals** package would register:
- **Entity kind** `herd` with schema (5.1), its table `s.herds`, its place resolution (node or road with `pos`), tag namer
  (TG.herds_at_start/new_herd), claimable (`claim` refs), `p_set` table mapping.
- **Primitives:** `new_herd`, `split_herd` (and generic `set`); ideally `move_herd`, `merge_herd`, `kill_beast` to replace raw `set`s.
- **Data rows:** species/kind table (today implicit cattle: roles, role words, breeding, milk, dung, fodder need per head, starve
  nights, slaughter gives) i.e. `PHYSICS.cattle`, `HERDS`, slaughter TECHNIQUES row; `ITEMS` fodder/milk/hide/harness/hay;
  `RESOURCES.grass`, `RESOURCES.dung`; `FITTINGS.stalls`; cover grazing shares.
- **Seeding:** spec `herds:` (roles, count, in_milk, parcel or road/stretch/home, holder -> claim), grass stocks on grazing covers
  (world l.119-123 today hard-coded in World.__init__).
- **Night processes (ordered):** (1) pack-ox follow/feed on roads [after departures, inside roads' night]; (2) herds on roads drift/
  die/gone; (3) led-herd checks, split; (4) wander/trample/home at dusk [after crops' growth, needs fences settled]; (5) merge;
  (6) feed (trampled, grass, fodder), hunger, starvation, milk, breeding, dung, grazed-soil restore [after renewal, after
  spoilage]. Must run after `renewal` and `crops`, before nothing else in the night today.
- **Dawn process:** arrivals bring accompanied herds (`arrive_with`); spec incident `stray`.
- **Verbs/techniques:** herd, milk, slaughter, drive, dung gather, hay; pack ox choice at departure (`travel` choices `lead`);
  `animals` requirement on techniques (`team_shortfall`, `usable_herds`, `beasts_note`) for plough and future teams.
- **Fuse/road calls:** herd finds on a stretch, driven splits (roads.py registers them).
- **Signs:** `signs.HERD`, `PASTURE` (grazed bare), `ASTRAY`, `EMPTY` (own pasture empty), `TRAMPLED`, `DRIVEN`, `SLAUGHTER`,
  `CARCASS`, herd contexts (`herd_context` l.1624, `_herds_out` l.1076), person context `led_by`.
- **Capacity-model declarations:** grazing carrying capacity, fodder need, births/dung per year (clocks: `PHYSICS.cattle.*`).
- **Prompt lines:** herds in `perceive` place summaries (`herd_words`), led beasts (`Here.led`).
- **Couplings that make splitting hard:** farm.py hosts the animals' night and acts; herds.py imports farm at top level and farm
  imports herds lazily (cycle); crops and herds share the trample handoff (`h.ate`) and the grazed-vs-fallow soil rule;
  forests reads `h["count"]` to stop young growth; fences live in farm (acts) and herds (night); world.capacity reads pack oxen;
  roads hosts herd fuse calls; buildings hosts stalls; things hosts carcasses; claims/sync generic.

---------------------------------------------------------------------------------------------------------------------------------

## 6. WEATHER / CLIMATE / ENVIRONMENT

- **Two regimes:** (i) no `climate:` block: label per day from `SPELLS[spell]` with one region-wide keyed draw; spell from spec
  `spells` else "normal"; cold = spec `cold_days` or every winter night; (ii) `climate:` block: the scheduler (1.3), per-node values,
  label from thresholds, cold = frost (low < 0) at the place. Spec `weather: {day: kind}` fixes a day's label in both; spec
  `spells` override the scheduler's day. Spec `cold_days` override both.
- **Scheduler internals:** era (CLIMATE.eras, chain if `moves`, `era_pace`), shocks (`shocks: true`), year anomaly AR(1),
  regional type Markov (`types.hold`, era weights), storms born upwind with heading/speed/radius/wind, tracked across node positions
  (MDS of road distances or spec xy), `hit` raises rain/wind; local AR(1) fields correlated by `exp(-dist/corr_km)` via Cholesky;
  values {temp, low, rain, wind, fog, storm}. Cached in `w._climate` (not state; replay-safe since pure in seed).
- **Snow:** label "snow" when rain at/below `snow_below` (climate) or rain on a cold day (spells); `snow_lying` until
  `ENV.snow_melt` non-frost days.
- **Frost:** `climate.frost` -> `world.cold(at, day)` (world l.352). `w.cold` is the single cold query used by night, needs, crops
  (`grow_night` cold, `set_projection`), life (birth, infant), spoilage (frozen), breaks, renewal context, sowing note, signs.
- **What registers/queries it:**
  - `world.cold` (frost or winter), `Here.cold/weather/wet/snow_lying/since_heavy_rain/weather_values`.
  - night: truth record (CL.env, CL.label), `weather_fuel`/`fire_goes_out` (labels -> `PHYSICS.heat.weather`), spoilage wet,
    breaks (cold).
  - forests: gale label -> windfall.
  - farm: crop growth/frost/projection via `w.cold`.
  - renewal.context: values, frost, snow, wet, anomaly (rules ignore them today).
  - things: decay conditions, noticing (`visibility`, `open_air`, `ground_factor`).
  - roads: visibility on stretches, fords high after heavy rain (`since_heavy_rain`), soaked.
  - signs: SKY (`sky_context` l.1049: storm coming, gale threshold), road/trace/thing contexts.
  - fuse: sound at night.
- **No night process:** weather is computed on demand. Nothing registers into the night except the truth record lines (night l.23-26).
- **Visibility** (environment l.199): cover/terrain base x weather (scheduler vis by mm/fog/snow/wind, or WEATHER table) x felled wood
  x crop high (FM) x smoke (today's events with smoke techs/tags) x night (moon) x sound masking by loudness (events, gale).

---------------------------------------------------------------------------------------------------------------------------------

## 7. LIFE

- **Stages:** `LIFE.shares` (infant 1/16, child 1/8, youth 3/16, adult 5/8, then elder) of `lifespan` (spec `lifespan`, default 32
  days). `spans` l.49, `stage_of` l.58, `elder_from` l.73, `scaled` l.44 (all spans scale by lifespan/32). `MINOR = (infant, child)`.
  Person `born` (day, negative before the run); without `born`, stage is given and only elders age (`_old_age` l.473).
- **Dawn (`LF.dawn` l.111):** stage update (`set stage`); child->youth: `come_of_age` l.142 (model: heir of the head takes the head's
  model; else `cast.youth`; household_models; bots -> "bot"; hard-coded fallback a hard-coded model id), `MEM.come_of_age`, last 6
  childhood lines -> lasting memory (direct), household's known non-basic crafts -> aware (direct to `s.know`), event "grown";
  succession window ends -> most-named living member (ties: eldest) via `office head`, then `office succession None`.
- **Day:** `settle` l.221 partnerships both chose at one place (`partner`); `children_work` l.235: each child does the household's
  standing `order` (verbs `V.do`), `dial.child_works` chance; verbs `_partner`, `_part`, `_try` (record `today.try` units), `_care`
  (today.care, care_by, care_gift), `order`/`heir`/`named` via `office` (verbs, not in slice).
- **Care (night):** `care_gifts` l.176 before eating (food transfer, kept sentence into child's memory up to
  `MEM.kept_settings.childhood`); care units recorded on child `cared` in `_young`; children eat from carers' hands (`feeders`).
- **Ration:** `ration_factor` l.261 (infant 0.5, child dial 0.7/1.0, pregnancy +0.3); `unit_penalty` late pregnancy -1 unit
  (`world.units_for`); `carried_weight` infant 2 on its mother (`world.load`); infants travel with mother (night.departures l.240,
  dawn arrival `carried_by`); babies sleep with mother (night l.354-362); beds by stage (`PHYSICS.beds`, `bed_share`).
- **Pregnancy (night `LF.night` l.337):** `_conceive` l.354 (spec `children.on`; mutual `try` same night, same building and place,
  neither missed a meal; chance `0.8(1-e^{-0.5u})`; set `pregnant`, `father`); `_pregnancies` l.378 (late on the road: `road_loss`;
  due: `_birth`); `_birth` l.392 (housed / camp / out risk; helped halves; clears pregnant; `gap_until`; apply `born` (world.p_born:
  name, household, kin, knowledge, places); infant and mother death draws); `showing` l.304, `may_conceive` l.324, `in_gap` l.319.
- **Deaths:** `_young` l.423 (infant: care vs dial `infant_care`, hunger x2, shelter x, cold w/o fire x2; child: base x unminded);
  `_old_age` l.460 (adult 0.001 "a sudden illness", elder 0.01 doubling every 20 x L/32 days); starvation is in night.py; fights in
  settle; childbirth here. All via `die` -> `world.p_die` -> `LF.on_death` (succession and inheritance).
- **Succession/inheritance (`on_death` l.504, inside `p_die`):** the head's named heir, else eldest adult and a 2-day naming window
  (`LIFE.succession_days`); heir cleared if dead; claims pass by household rule `inheritance` (eldest / partible / household); land
  covers ("field","pasture","meadow") pass in whole plots (`plot_heirs` l.549, joint last plot), then `FM.sync(carry=True)`.
- **Memories of childhood:** `_childhood` l.484 (cared by, hungry, events of kinds death/birth/raid/fire/fight/alarm), kept 12.
- **Prompt lines:** `age_line` l.82 (spec `ages: true`), Here.life/children_on/body (with_child, grows), prompt's household children
  order line.
- **State/primitives:** see 1.8. Night steps: care gifts (before eating), LF.night (after starvation), dawn step.

---------------------------------------------------------------------------------------------------------------------------------

## 8. EXTENSION POINTS (dispatch, if/elif on kinds, special names, globals)

**Registries (already pluggable):**
- `renewal.RULES` (decorator `@rule`), `renewal.NIGHTLY` tuple ("fast","threshold","periodic"); forests' rules are registered but
  called explicitly by `forests.night`, not by `_grow`. `RESOURCES[key].renewal` and per-stock `renewal` (data-driven).
- `world.PRIMITIVES` dict (world l.1038) + `w.hook(before|after, prim, fn)` (used by agreements, buildings; not by this slice).
- `packs.on(row)` row gating (only "water" pack exists; farming, cattle, life, climate are switched by spec keys instead:
  `children`, `ages`, `climate`, `lifespan`, `spells`, `weather`, `cold_days`, `lore`, `cast.youth`, `household_models`).

**Dispatch on kind (closed if-chains):**
- `farm.act` l.743-804: yield kind sow/works/fence/gate/select/break/tend/manure/crop/herd/milk/slaughter; `verbs.FM_KINDS` l.91;
  `farm.ready` l.1196-1244 the same kinds again.
- `verbs` dispatch dict l.2007 `"drive": FM.drive`, `"partner"`, `"part"`, `"try"`, care via `_care`.
- `night.decay_rate` l.255-261: container kind `stock` / `TH.KINDS` (pile, remains, carcass) / else hands; night l.164, 167:
  `hands` of the dead skipped, `carcass` + `meat` special path.
- `needs.food`: state names, `structure == "camp"`, gear names.
- `night`: `b["structure"] == "camp"` (l.51, 58, 62, 63, 87), FIRE fittings by data flag but `"hearth"`, `"fire ring"` by name (l.50,
  101, 403), `beds` fitting by name, `"works".kind == "upgrade"` (l.82), `_gear` items `"tent"`, `"bedroll"` by name (ITEMS has a
  `camp` key it ignores), `lines` `how == "paint"` and `structure == "wattle"` (l.191-192), `STAGE_ORDER` l.299.
- `herds`: `ROLES` (duplicated in farm l.24, herds l.24, world l.163/688/706/713 as literal tuples), young-first order
  `("young","cows","oxen","bulls")` (herds l.391, farm l.1169, 1487), `"harness"`, `"hay"` by name, `h["kind"]` compared in drive only.
- `farm`: `ROLE_OF` incl. "steer", "heifer"; `"grain"` default family and fallow slot; `"select seed"`, `"plough"`, `"wooden plough"`,
  `"ditch"`/`"terrace"` names; `cover == "field"`; `LAND` tuple; drive cover list l.1262; `_works_word`.
- `life`: stage names (MINOR, "youth", "adult", "elder"), `a hard-coded model id` l.150-152, `LIFE.dial` keys, inheritance rules
  `eldest`/`partible`/`household`, event kinds in `_childhood` l.498, land covers l.535, sex `"f"`.
- `climate`: `SPELL_OF` l.363 (type -> spell), label thresholds; `environment.WET`; label strings used as keys in
  `PHYSICS.heat.weather`; `forests.night` `== "gale"`.
- `forests`: `KINDS` incl. special `"scrub"` (no trees); cover switch forest<->scrub l.99-107.

**Globals / module state:** `packs.CURRENT` (module global set at World init and per Here/Mind); `w._climate` (scheduler cache);
`w._renewal_ctx` (renewal context cache, cleared at 4096); `night.FIRE` computed at import from FITTINGS (pack-blind).
`data.PHYSICS` read directly in `farm._f_default` and `forests.fuel_order` (ignores spec physics overrides; everything else uses w.p).

---------------------------------------------------------------------------------------------------------------------------------

## 9. What each feature folder would REGISTER, and couplings

Proposed features from this slice: **weather** (climate+environment), **woods & fuel** (forests + fire), **shelter & sleep**
(beds, camps, gear), **eating & hunger** (needs core), **spoilage**, **crops & soil** (fields, holdings), **field works**,
**enclosure** (fences, gates), **animals** (herds), **life** (stages, birth, death, succession), plus the generic **renewal**.

### 9.1 weather (climate.py + environment.py)
- Register: world-level query service `weather(at, day)`, `values`, `cold(at, day)` (replacing `World.cold`), `snow_lying`,
  `since_heavy_rain`, `visibility(at, parcel, sense, night)`, `open_air`, `ground_factor`; labels table (WEATHER) and spells (SPELLS);
  CLIMATE params; spec keys `climate`, `spells`, `weather`, `cold_days`; Here methods; truth-record hook at night start; sign
  context providers (SKY: storm coming).
- Visibility modifiers should be registered by other features (today hard-wired): crop high (crops), felled wood (woods), smoke
  (crafts via ENV.smoke_techs), loudness (events), cover/terrain bases (core land data).
- Couplings: `environment.crop_high` imports farm; `World.cold` is a core method calling climate; spoilage, crops, life, fires all
  read `cold`; labels are strings consumed by heat (PHYSICS.heat.weather) and forests (gale).

### 9.2 woods & fuel (forests.py + fire parts of night.py)
- Register: resource keys `wood`, `young`, `dead` with renewal rules `slow`, `young`, `dead`; FORESTS data; parcel seeding hook
  (`FO.seed` from world-file `wood:`); a night process (after generic renewal; needs herds-on-parcel query, gale query); cover
  transition forest<->scrub; fuel model (`ITEMS.heat`, `heat.order`, `burn`, `heat_of`, `fuel_words`); fire processes: house/camp
  fire (needs sleepers from shelter; buildings' fittings with `fire`, floor), open fires (sleeping-out groups); `weather_fuel`,
  `fire_goes_out`; building fields `fire`, `warm`, `fire_out`; night-line producers (fire need, fire out); capacity declarations
  (`trees_step`, `young_step`, `shed_a_night`).
- Couplings: fires sit between sleeping and eating; their output (`fire`, `warm`, `fire_out`) is read by needs, cooking, birth and
  infant risk; heat by structure "camp"; woodpiles are `things` containers at a door; `forests.night` reads herds.

### 9.3 shelter & sleep (night.sleeping_places, _gear, camps, beds)
- Register: night process "sleep" (after fights and departures; output `where`, `floor`), bed shares by stage (`PHYSICS.beds`),
  camp buildings (`lasts_until` lapse process), gear items (tent/bedroll with `camp` row key), `slept_out` sign field, BL.read on
  sleep, the shelter state function feeding needs.
- Couplings: life (infants with mother, stage beds), buildings (access, can_enter, dwellings, condition, works upgrade), roads
  (camp at good places), lodging verbs (`sleep`, host).

### 9.4 eating & hunger (needs.py + the eating loop + starvation)
- Register: a **needs factor registry**: today's `needs.food` context should be assembled from factors registered by shelter (state,
  floor), weather (cold), fire (warm/hearth/fire/open fire/gone), gear, roads (fed_on_road), life (mult/extra, care_fed), labour
  (work). Food sources registry (hands, takeable stores ordered, carers' hands from life). Cooking rule (`cook`, `raw`). Hunger
  consequences (units, yield, hazard). Night ordering: after fires/care, before starvation, life, spoilage.
- Couplings: the loop also allocates tents (`_gear` wear) and records work shortfall; first-come order by name.

### 9.5 spoilage (decay_rate, spoil_rate)
- Register: night process after eating; per container-kind condition resolver (stock -> keeping fittings; things -> open dry/wet,
  buried; hands); DECAY rows; `becomes`; carcass meat rule (from animals/things); weather (wet, cold, season) query; capacity use of
  `spoil_rate`.

### 9.6 crops & soil (farm fields)
- Register: entity sub-record "holding" on parcels (shares, held_whole) with `sync` as a claims-change hook (today hard-wired into
  `claim`, `end_claim`, `plots`, `shares`, `die`); primitives `set_share`, `shares`, `plots`, and the `draw(key="crop", holder)` branch;
  data CROPS, CROP_OF, SEED_CROP, TURF, PHYSICS.farming, PHYSICS.ground, master_yield, seed_selection; yield kinds sow, break, tend,
  select, manure, crop (act + ready handlers); spec seeding `state.crop`, `state.crops` by holding, `fertility`, `land.base_fertility`,
  `broken`, `last_crop`; night process (crop growth/ripening/rot/blight-shown/frost/slot end/fallow), ordered after renewal and before
  animals; signs CROP, FIELD (holding rows), TRAMPLED; prompt lines (crop_words, held_words); lore (sowing seasons via season_run);
  visibility modifier (crop high); capacity declarations (crop_base, grow_night, season_run, soil_step, fallow_gain, manure_gain,
  fail_chance, ground_mult); inheritance hook (land in plots, `plot_heirs`).
- Couplings: grazed restore and trampling belong to the animals feature but write crop/soil records; dung (animals) feeds manure;
  `p_draw` and claim primitives in core call farm; `life.on_death` plot inheritance; `environment.crop_high`; `run.dawn` stray incident.

### 9.7 field works (ditch/terrace)
- Register: parcel field `works`, yield kind `works`, `ground` penalty (`PHYSICS.ground`) as a crop-yield modifier, night upkeep
  process (pending led work, seasonal decay), seeding `state.works`. Couplings: name-coded ditch/terrace; world seeding constants.

### 9.8 enclosure (fences, gates)
- Register: parcel field `fence`, yield kinds `fence`, `gate` (+ ready checks), FENCES data, `through(pid)` query for animals,
  night process (build completion if led, mending, yearly decay) that must run before animals wander, seeding `fence:` on parcels,
  signs FENCE, prompt gate listing (`FM.ready` in prompt l.356). Couplings: code split across farm (acts) and herds (night);
  `KN.level(mind, led)` for walls.

### 9.9 animals (herds) — see 5.3.

### 9.10 life
- Register: person fields (stage, born, sex, parents, partner, pregnant, father, gap_until, cared), LIFE data, spec keys
  (`children`, `lifespan`, `ages`, `cast.youth`, `household_models`, `tree`), primitives `born`, `partner`, `office` (head, heir,
  succession, order, named), death hook (`on_death`: succession + inheritance, registered on `die`), dawn process (stages,
  come of age, succession end) before arrivals, night processes: care gifts (before eating), LF.night (after starvation, before
  spoilage), settle-step processes (partnerships, children's work), needs factors (ration mult/extra, care_fed), units penalty
  (`world.units_for`), carried weight (`world.load`), beds by stage, infants travel with mother (departures, arrivals), feeders as
  food source, verbs (partner, part, try, care, order, heir, name a head), signs (BIRTH, person context: babies, failing elder),
  prompt lines (age_line, children's order), memory hooks (childhood lines, kept lines, come_of_age), capacity (ration_factor,
  lifespan, elder_from), generate (stages for generated populations).
- Couplings: `world._person` calls `LF.stage_of`; `p_die` calls `LF.on_death` which calls `FM.sync`; `come_of_age` and `_childhood`
  write mind/know directly (bypassing apply); `children_work` runs verbs from the settle step; model ids hard-coded.

### 9.11 renewal (generic)
- Already a registry. A package registers `rule(name)`, whether it is NIGHTLY, its resource rows, and its context keys. Gap: the
  woods' rules are not driven by `_grow` (forests.night calls them with its own context and the gale); `accrues` (dung) is driven by
  animals; the night order of `_grow` vs forests vs animals is implicit in code.

### 9.12 Cross-cutting couplings that make the split hard
1. **Core primitives import features:** `p_draw` (crop branch), `p_set_share`, `p_shares`, `p_claim`, `p_end_claim`, `p_plots` ->
   farm; `p_die` -> life (-> farm); `World.cold` -> climate/environment; `World.capacity` -> herds; `World.load`, `units_for`,
   `_person` -> life; World `__init__` seeds forests, grass, fences, works, crops, herds inline.
2. **Night order is hand-written** in three places (run.py settle/night block, night.night, farm.night) with lazy imports; no
   declared before/after.
3. **farm.py mixes crops, soil, holdings, field works, fences, gates and cattle;** herds.py and farm.py import each other.
4. **Shared handoff fields:** `h.ate` (trample -> feeding), `b.fire/warm/fire_out` (fires -> needs, cooking, birth, infants),
   `today.*` keys (`_floor`, `_departed`, `road.fed/camp`, `soaked`, `care*`, `try`, `units`, `guards`, `fire`, `sleep`, `travel*`),
   `h.count` (forests), `rec["missed"]` (eating -> life).
5. **Direct state writes outside primitives:** life `_childhood`, `come_of_age` (mind, know), labour.fade (know), night `s.log`,
   `today` scratch keys; `sync` mutates parcels (inside primitives or seeding only).
6. **Needs is a closed formula,** not a sum of registered factors; the eating loop also does tent allocation and work accounting.
7. **Words (prose) are generated inside mechanics** (farm acts and refusals, herds events, life events) — a package would carry its
   prose with its mechanics.
8. **Capacity model reuses the pure night functions** (grow_night, spoil_rate, regrow, trees_step, ration_factor, eaten_worth):
   any package must keep those pure entry points stable and declared.
9. **Data read from the global PHYSICS** in a few places (`farm._f_default`, `forests.fuel_order`) bypasses per-world overrides.
