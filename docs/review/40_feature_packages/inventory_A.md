# Inventory A: world.py, here.py, data.py, schema.py, packs.py, tags.py, things.py, wear.py, modifiers.py, variants.py, clocks.py, capacity.py, needs.py

All paths under `cybertron2/engine/`. Line numbers are as of this read (16 Nov 2026). Feature labels used throughout:

- **kernel**: places, containers, goods moving, people existing, time, rng, chokepoint, events, acts.
- **places**: nodes and the parcel graph (adj, side, height). **roads**: roads/travel/traces/landmarks.
- **farming**: crops, shares/holdings, works, fences, clearing, soil. **herds**: livestock.
- **buildings**: rooms, fittings, stores, lines, monuments, tiers, fitting wear, repair.
- **goods**: items, decay, tools/weapons, carry. **forests/resources**: stocks and renewal.
- **life**: birth, death, stages, partners, succession. **households**: institutions.
- **claims**: rights from claims. **exchange**: offers, agreements, debts.
- **knowledge**: techniques, skill, modifiers. **perception**: mind, noticing, signs, events' extent.
- **weather**: climate, environment, cold. **things**: piles, remains, carcasses, graves.
- **tags**: H/T referent tags. **combat**: attack, defence, raids, fuse. **labour**: units, fatigue.
- **converse**: messages. **water**: the fishing/salt pack.

---------------------------------------------------------------------------------------------------------------------------------

## 1. Entity kinds / state tables

`World.s` is made in `World.__init__` (world.py:99-101) with keys: day, seq, nodes, roads, parcels, buildings, herds, containers,
people, institutions, claims, offers, agreements, know, mind, events, acts, log, left. Then `world_schema` (l.103).
Keys made elsewhere: `today` (run.py:869 `blank_today()`), `fuse_calls` (fuse.py:63), `life` (run.py:410), `traces` (p_traces
world.py:891), `tag_seq` (tags.give l.24), `salt` (branch.py:144; NOT in schema.TOP, so `schema.unknown` would flag it),
`_seed_things` (transient during __init__, l.231, popped l.242).

The declared shape: schema.py `TOP` (l.19), `TODAY` (l.21), `FIELDS` per table (l.23-35). `mind`, `know` are not field-listed
(versioned with memory/knowledge code). WORLD_SCHEMA = 4, FINGERPRINTS (l.44). Every feature adds fields here, so a package
system needs per-package schema fragments (FIELDS is a single closed list; test fails on unlisted fields).

### Top-level scalars / lists

| key | shape | made by | feature |
|---|---|---|---|
| day | int | __init__; advanced by run.py | kernel (time) |
| seq | int counter for ids (E, C, O, A, b, remains:, kind:) | __init__; bumped in event, _claim, p_die, p_new_thing, p_raise, p_offer, p_agree | kernel |
| world_schema | int | __init__ l.103 | kernel (record) |
| events | today's events `{id, day, place, kind, actor, target, about[], text, salience, tags[], sense, concerns[], **extra}` | World.event l.444-455 | kernel (+ perception reads) |
| acts | `{day, actor, verb, tech, for, node, **extra}` | World.record l.457 | kernel (action record; duties D2-39 read it) |
| log | one record per night | run/night | kernel (record) |
| left | things left yesterday/today (`{..., day}`) | run.py:1067 | perception/things (what was left at doors) |
| today | day's working record; keys in schema.TODAY (l.21): worked, units, road, route, travel*, fights, guards, thefts, care*, partner(s), sleep, fire, fuse, learn, teach, try, watch, children_work, green_cut, drawn, heard, joins, admits, soaked, turned, skipped_morning, memory_done, day_seen, awake, fled, left, _departed, _floor | run.py `blank_today` | mixed: kernel container for every feature's per-day scratch; each key belongs to a feature (worked: kernel/perception; road/route/travel*: roads; fights/guards/thefts/fuse: combat; care*/partner*/children_work: life; sleep/fire/_floor: buildings/night; learn/teach/try: knowledge; green_cut: farming; drawn/turned: herds; heard: converse/perception) |
| traces | `[{kind, day, ...}]` road traces | p_traces | roads |
| tag_seq | `{"H": n, "T": n}` | tags.give | tags |
| fuse_calls | | fuse.py | combat/fuse |
| life | `[{day, dawn}]` growth log | run.py:410 | life |
| salt | replicate salt for rng | branch.py | kernel (branching) |
| know | `{person: {tech: {level, skill, seen, wins, fails, source, since}}}` | knowledge.seed (KN.seed, via __init__ l.237), p_learn | knowledge |
| mind | `{person: {days, seeded, lasting, own, beliefs, today, log, kin, places, things?, names?, landmarks?, found?}}` | perceive.seed (PC.seed l.238); p_born copies places/kin; things.remember adds `things`; tags._learn adds `names` | perception/memory (+ things, tags, roads landmarks) |

### Record tables

**nodes** `{id: {name, text, unexplored}}`, made __init__ l.106. Feature: kernel/places (`unexplored` is roads/exploration D4-47;
read by `World.knows_place` l.345 which reads `mind[name]["places"]`).

**roads** `{"road:a-b": {a, b, days, track, way, ends, stretches, terrain, bare?...}}`, made __init__ l.150-158.
`a, b, days` kernel/places (graph edge + travel time); `track` goods/transport (carts); `way` roads (unexplored way name);
`**RD.build(extra,k)` -> terrain, stretches (roads); `ends` via `LY.build_ends` (layout, hidden ways D2-90). Feature: roads.

**parcels** `{id: {...}}` made __init__ l.123-146 (one per spec node parcel). Fields (schema FIELDS l.26) and owner:
- kernel/places: node, name, size, adj (made symmetric l.147-149), text, cover (also changed by farming clearing / forests `was`)
- layout/places: side, height (D2-114; also weather: height_m)
- resources: res `{key: {S, K, r, run_K?, run_r?, run_seasons?, renewal?, response?}}`; keys from RESOURCES filtered by pack,
  plus forests' trees/young/dead (`FO.seed`), plus `grass` (herds, l.118-122 from PHYSICS cattle.grazing)
- farming: crop, fertility, broken, last_crop, last_kind, fallow_since, shares `[{holder, plots, crop, fertility, broken,
  last_crop, last_kind, fallow_since, dead?}]` (farm.py; D2-163, D2-172), works `{ground, done, kept, pending, units}`,
  fence `{kind, units, level, built, gate, mend, pending, since}` (farming/herds D2-130), clearing, clearing_built, held_whole,
  dead (via set_share)
- land/weather: ground (wet|hill: farming works and burial), land `{base_fertility, ...}` (D4-112)
- combat: fight `{day, fights}` (settle.py)
- herds/hunting signs: hunted, slaughter
- social: meeting `{day, by, about, at}` (D4-77; read by Here.meeting_today)
- forests: was (cover before felling)
So the generic parcel is node/name/size/adj/text/cover/res; ~20 of 29 fields are feature fields.

**buildings** `{bid: {...}}` made by `World._new_building` (l.271-296) from __init__ and p_raise. Fields (schema l.27):
- kernel-ish (a place with a container): node, parcel, name, stock (container id `stock:<bid>`), door (open|barred: claims/access),
- buildings: structure, size, rooms `[{kind, floor, storey}]`, fittings `{name: n}`, condition (CONDITION 2/1/0), tier,
  unfinished `{blueprint, units_left, materials_left, by}`, works (room/tier/upgrade in progress), mending, monument,
  description `{text, by, day}`, lines `[{slot, text, by, day, how, was}]`, changes, fitting_work `{f: {n, units_left}}`,
  lasts_until (camps), built_day, worn `{fitting: {used, since}}` (wear.py), warm, fire, fire_out, fire_hit, broke
- combat/crime: raided, theft
Owner: buildings.py (rooms via `BL.seed_rooms`), night.py (fire, warm, broke), settle.py (raided, theft).

**herds** `{hid: {...}}` made __init__ l.162-177, p_new_herd l.680, p_split_herd l.696. Fields: node, parcel, home, name, kind,
cows, oxen, bulls, young, count, in_milk, milked `{day, n}`, births, hungry, watched; road-lost: pos, lost `{day, from, road}`;
later: ate, base_name, driven, gone, herders, last_calf, pack, split_day, split_of, strayed_in, tag, with. Entire record = herds
feature (tag = tags). Note herds have a place but are not containers: beasts are counts on the record, not goods.

**containers** `{cid: {...}}` kinds:
- `hands:<name>` `{kind:"hands", of, goods, wear}`: made `_person` l.252. kernel.
- `stock:<bid>` `{kind:"stock", of, goods, wear}`: made `_new_building` l.274-276. kernel (container) owned by buildings.
- `remains:<seq>` `{kind:"remains", of, node, parcel, goods, wear, on_road, body, died, in, stretch}`: made p_die l.848-852. life/things.
- `<kind>:<seq>` from p_new_thing l.972-979: `{kind, node, parcel, goods, wear, day, **fields}`. Kinds in use: `pile`
  (verbs.py:1394 give/put/hide; buildings.py:400 overflow at door: `door`), `carcass` (things.leave_carcass l.186: beast, of,
  holders, cause, died, stretch?, hidden?). Seeded things l.216-231 (any `kind`, default pile; of/body/died/cause).
- Fields (schema l.29): goods, wear, kind, of, node, parcel (kernel: a container with a place); by, day, hidden, untaught, door,
  in, tag, stretch, on_road (things/roads/tags); body, died, cause, buried, grave, cairn, cairn_by, cairn_day, rot (life/burial);
  beast, holders (herds carcass); thing (?).
- `wear {item: uses}` is goods/tool wear (D2-46) on every container; travels with last unit in p_transfer l.628-630.
things.KINDS = ("pile","remains","carcass") (things.py:16) is the "things at a spot" kind list.

**people** `{name: {...}}` made `World._person` l.247-269 (and p_born). Fields (schema l.30), by feature:
- kernel: alive, at, transit `{road, from, to, left, arrive, ...}` (roads adds fields via p_transit), hands, model (agent model)
- life: stage, sex, born, born_line, parents, partner, pregnant, gap_until, died, cause, widowed_of, father, cared, order
- needs/night: hunger (STAGES 0/-1/-2), missed, ate_raw, slept_out, frailty (night hazard)
- combat: attack, defence, wounded, guarded
- persona/agent: role, trade, aim, concerns, relations, notes, pinned, interests (perception), plan_next (run)
- converse: messages (daily message limit, `_message_limit` l.324)
- roads: arrived, arrived_by, came_from, home_seen
- labour: tired, walked
Name is the key (no id).

**institutions** `{iid: {kind, name, members[], offices {head}, rules {admit, grant}, heir?, order?, succession?}}` made __init__
l.180-190 (spec households + agents' `household`), p_found l.740. Only kind used: "household" (if-checks here.py:205,349;
world.py:504). heir/order/succession: life (D2-143, D2-148). Feature: households.

**claims** `{C<n>: {thing:[kind,id], claimant, rights[], grounds, since, until, by, plots?, of?, over?, joint?}}` made
`World._claim` l.517-527 (seeded l.191-198, 206-209; p_claim, p_plots). `plots/of/over/joint` are farming holdings (D2-163).
Things claimable: parcel, building, herd (p_claim place refs l.1051). Feature: claims.

**offers** `{O<n>: {node, by, to, give, get, lots, taken, until, open, closed, for}}` made p_offer l.1000. exchange.
**agreements** `{A<n>: {parties, legs[{from,to,item?,work?,done,when,paid,arrears,...}], node, day, witnesses, status, made_by,
offer, seeded}}` made p_agree l.1013 (and seeded l.232-233). exchange.

---------------------------------------------------------------------------------------------------------------------------------

## 2. Primitives (world.py:1038-1075)

Registry: `PRIMITIVES = {name: (fn, refs(kw)->[(kind,key)])}`. `refs` lists entities that must be at `place` (checked by
`World.apply` l.425-427 via `place_of`). Helpers `_r(kind,*keys)` l.1030, `_rc(*keys)` l.1034 (container refs).
Users per primitive from grep of `apply("<p>"`.

| prim | fn (line) / signature | changes | place refs | feature | generic? | users |
|---|---|---|---|---|---|---|
| transfer | p_transfer 622 `(src,dst,item,qty)` | goods src->dst; wear follows last unit; Refused if short | src,dst containers | kernel/goods | generic | agreements buildings fuse life roads settle verbs |
| create | p_create 634 `(dst,item,qty,why)` | goods appear | dst | kernel | generic | farm night roads things verbs |
| destroy | p_destroy 639 `(src,item,qty,why)` | goods removed (clipped) | src | kernel | generic | farm forests herds night roads run verbs |
| draw | p_draw 646 `(parcel,key,qty,holder)` | res[key].S down; if key=="crop": **calls farm.record** to take from a holding's crop (left, area_left, reaped) | parcel | resources + farming branch | generic except crop branch | farm herds run verbs |
| add_res | p_add_res 863 `(parcel,key,qty)` | res S up, K=max | parcel | resources/forests (brash) | generic | forests verbs |
| set_res | p_set_res 873 `(parcel,key,fields,init)` | res record update/create | parcel | resources (nature's night) | generic | farm forests night verbs |
| wear | p_wear 662 `(container,item,uses)` | container.wear up; at ITEMS life: destroy 1 | container | goods (tools D2-46) | generic-ish (reads ITEMS.life) | farm night settle verbs |
| set | p_set 673 `(ref,field,value)` | any field on building/parcel/herd/person/offer (hard-coded kind->table dict l.675) | ref | kernel | fully generic setter; ~60 (kind,field) pairs across 14 modules | agreements branch farm forests herds labour life night perceive roads run settle verbs wear |
| new_herd | p_new_herd 680 `(like,parcel)` | new empty herd copied from `like`; **calls tags.new_herd** | herd like, parcel | herds | specific | farm |
| split_herd | p_split_herd 696 `(like,take)` | herd split by role counts; **calls tags.new_herd** | herd like | herds | specific | herds |
| admit | p_admit 720 `(person,inst)` | move membership, re-head old | person | households | specific | settle |
| leave | p_leave 731 `(person,inst)` | remove member, re-head | person | households | specific | verbs |
| found | p_found 740 `(person,name)` | new household, head | person | households | specific | verbs |
| claim | p_claim 753 `(thing,claimant,rights,grounds,until,by,plots,of,over,joint)` | new claim; **if parcel: farm.sync** | thing if parcel/building/herd | claims (+farming) | specific | farm herds roads verbs |
| end_claim | p_end_claim 761 `(claim)` | until=d-1; **if parcel: farm.sync** | none | claims (+farming) | specific | verbs |
| set_share | p_set_share 770 `(parcel,holder,field,value)` | **farm.record(par,holder)[field]=value** | parcel | farming | feature-only | farm herds |
| shares | p_shares 777 `(parcel,carry)` | **farm.sync** | parcel | farming | feature-only | farm verbs |
| plots | p_plots 784 `(parcel,frm,to,n,why)` | shrink/end giver's claims, new claim of n plots, **farm.sync** | parcel | farming + claims + exchange (an agreement leg) | feature | agreements |
| depart | p_depart 808 `(person,road,to)` | at=None, transit={road,from,to,left,arrive} | person | kernel/roads (movement) | generic movement | night |
| arrive | p_arrive 816 `(person)` | at=transit.to, transit=None | none (person on road) | kernel/roads | generic | run |
| transit | p_transit 882 `(person,fields)` | transit.update | person | roads | generic-ish | night roads run |
| traces | p_traces 888 `(add,day)` | s.traces extend + expire by ROADS.trace_days | none | roads | feature | roads |
| harm | p_harm 823 `(person,wounded,hunger)` | wounded/hunger | person | needs/combat | semi-generic | night settle |
| die | p_die 832 `(person,cause,to)` | alive False; remains container with hands' goods (or to killer); **calls things.spot_of, things.house_at_death, life.on_death, roads.position (via _stretch_of 967)**; un-partners | person | life/kernel | kernel act with 4 feature callouts | life night roads run settle |
| born | p_born 896 `(mother,father)` | new person via _person; household; **knowledge.seed, perceive.seed, generate.MALE/FEMALE names, LIFE children_work**; mind places copied; kin relations both ways (writes mind directly) | mother | life | feature | life |
| partner | p_partner 939 `(person,other,on)` | partner fields | person, other | life | feature | life verbs |
| office | p_office 953 `(inst,field,value,by)` | succession.named / offices.head / pop succession / any inst field | by | households/life (succession) | semi-generic setter for institutions | life verbs |
| learn | p_learn 987 `(person,tech,level,source)` | **knowledge._set** (writes s.know) | person | knowledge | feature | knowledge modifiers run settle |
| new_thing | p_new_thing 972 `(node,parcel,kind,**fields)` | new container at a spot; **calls tags.new_thing** | parcel | kernel/things | generic (container factory) | buildings things verbs; __init__ |
| set_thing | p_set_thing 982 `(cid,field,value)` | container field | container cid | kernel/things | generic setter | roads verbs |
| raise | p_raise 992 `(node,parcel,rec)` | new building via _new_building (stock container too) | parcel | buildings | feature | verbs |
| offer | p_offer 1000 `(by,rec)` | new offer at by's place | person by | exchange | feature | here.new_offer |
| close_offer | p_close_offer 1007 `(offer,why)` | open False | offer | exchange | feature | agreements night |
| agree | p_agree 1013 `(node,rec)` | new agreement | none | exchange | feature | here.new_agreement; __init__ seeded debts |
| leg | p_leg 1025 `(agreement,leg,**fields)` | leg update | none | exchange | feature | agreements |
| close_agreement | p_close_agreement 1020 `(agreement,status)` | status | none | exchange | feature | agreements |

Notes:
- No primitive for institutions' generic set (p_office covers), nodes, roads, claims fields (p_plots edits claims in place),
  mind/know (written directly by perception/knowledge: architecture.md allows it).
- Several primitives bypass `apply` internally (p_die calls `_add`, p_wear calls `p_destroy` directly; p_found calls `p_admit`
  directly; p_born calls `w._person`); only the outer call is journaled.
- Writes outside the chokepoint inside my slice: `World.__init__` seeding (direct), `tags.give_name/_learn` (mind), `things.remember`
  (mind), `p_born` (mind kin/places), `herds_at_start` (direct herd edit at seed).
- Feature callouts from primitives (inverted deps): draw->farm.record; claim/end_claim/plots/shares/set_share->farm.sync/record;
  new_herd/split_herd/new_thing->tags; die->things, life, roads; born->generate, knowledge, perceive, data.LIFE; learn->knowledge;
  traces->data.ROADS; raise->_new_building->buildings.seed_rooms.

---------------------------------------------------------------------------------------------------------------------------------

## 3. Hooks

Mechanism: `World.hooks = {}` (l.95) keyed `(when, prim) -> [fn]`; `World.hook(when, prim, fn)` l.419; run in `apply` l.429-437.
Before-hooks get `(w, call)` and may raise to refuse; after-hooks get `(w, call, out)`. `call = {prim, place, kw, cause, day}`
where cause is the innermost `World.cause(...)` context (l.411-417: `{actor, verb, for, node}`).
Journal is NOT a hook: `apply` calls `self.journal.change(call, out)` directly (l.438-441) and `event` calls `journal.event`
(l.453-454); nested applies marked `within`.

Registrations (whole repo):
1. agreements.install (agreements.py:367-370): `after transfer -> _credit`: when cause.verb in (give, leave), credits goods given
   to a creditor against open agreement legs. Feature: exchange (debts). Called from __init__ l.235.
2. buildings.install (buildings.py:379-382): `after create` and `after transfer -> overflow(dst,item)`: goods that do not fit a
   building's stores spill to a `pile` at its door (calls apply("new_thing")). Feature: buildings (storage D2-155). Called l.245.
No before-hooks are registered anywhere. Hooks are not serialized: a World rebuilt from state must re-run the installs
(only via __init__ today). proposals/law.md (architecture.md "Open") plans laws on hooks.

---------------------------------------------------------------------------------------------------------------------------------

## 4. Data tables

### data.py (pack-capable rows marked P)

| table (line) | row fields | feature | consumers (grep, non-test) | pack? |
|---|---|---|---|---|
| ITEMS (20) | weight, food, spoil, cook, raw, decay, fodder, heat, tool, weapon, life, seen, carry, track, camp, rot, pack | goods (food: needs; tool/weapon: knowledge/combat; carry/track: transport; heat: buildings fire; fodder: herds; camp: roads/night) | act agreements buildings capacity/* clocks farm forests fuse knowledge landgen life night packs perceive prompt roads settle signs things verbs world | P (fish, salt fish, fishing rod: water) |
| DECAY (68) | open_dry, open_wet, buried, warm, frozen, abs, becomes | goods (decay) | capacity night clocks | no |
| CROPS (86) | seed, gives, share, growth{season}, green, yield, hardy, takes, restores, straw, names, needs_winter | farming | capacity farm lore signs clocks | no |
| CROP_OF (97) derived name->crop | | farming | farm, world (via FM.CROP_OF) | - |
| TURF (98) list of covers | | farming | farm | - |
| LORE (103) `{sowing: {to}}` | | farming/knowledge | lore | no |
| SEED_CROP (104) derived | | farming | farm | - |
| EDIBLE (105), TOOLS (106), WEAPONS (107) derived from ITEMS; NOT pack-filtered | | goods | world (food_value, best_tool, weapon), buildings, night, perceive, run, settle, capacity | derived at import |
| COVERS (109) | words, ground, sight, sound, dig, ambient[(sense,text,sal)] | places (+perception sight/sound, buildings ground, burial dig) | buildings environment layout perceive things verbs | no |
| RESOURCES (128) | renewal, low, high (words), pack | resources | world (seed filter) capacity clocks knowledge perceive renewal | P (fish, salt) |
| FORESTS (146) | kinds{trees,young,dead,grow,regrow}, shed, per_timber, rot, brash, scrub_below, gale | forests | forests capacity(.py) clocks landgen | no |
| CLEARING (161) | per-cover units, fertility, built | farming/buildings | verbs capacity | no |
| FITTINGS (173) | label, materials, units, per, basic, trade, fire, spaces, holds, by, heavy, spoil, needs, site, structure, wear{life,count,mend / years}, fodder, dung, ground, room, fireproof, aliases, does | buildings (+herds stalls, +food mills) | buildings capacity clocks farm knowledge night perceive prompt signs verbs wear | no |
| FITTING_ALIAS (211) derived | | buildings | world._new_building | - |
| ROOMS (214) | floor, places, per-structure {materials, units, trade} | buildings | buildings capacity prompt verbs | no |
| BLUEPRINTS (226) | label, materials, units, structure, basic, trade, size, fittings, lasts | buildings | knowledge prompt verbs | no |
| SPACE (237) | added, storeys, upgrade, order, camp_floor, camp_store, monument_ground, seed_free, seed_keep_ground | buildings | buildings prompt verbs world._fit_seed_free | no |
| STORES (249) | kinds, order, floor, words | buildings | buildings | no |
| MONUMENTS (258) | label, materials, units, basic, trade, structure, aliases | buildings | buildings layout prompt verbs | no |
| TIERS (267), TIER_ORDER (273) | materials, work, words | buildings | buildings prompt verbs | no |
| LINES (276) | places, words, chars, units, other, carve_tools, carve_wear, spots, how | buildings (writing) | buildings verbs | no |
| TECHNIQUES (289; updated 470, 503, 833) | verb, label, aliases, basic, at{covers|fittings|building|children|things}, draws, yield{kind,...}, tools, weapon, wear, units, units_by, gives, inputs, uses, animals, by_season, trade, crew, tags, pack; modifiers: modifies, key, value, changes, untaught, values | knowledge (registry of all acts across features) | capacity/* clocks farm generate herds here knowledge landgen life modifiers packs perceive prompt run settle things verbs wear | P (fish by hand, angle, fishing rod, salt pan, salt fish) |
| (503-505 loop) | auto-adds a `build` technique for each BLUEPRINTS/FITTINGS/MONUMENTS row | buildings->knowledge | | |
| MODIFIERS (500, recomputed 849) | set of technique names with `modifies` | knowledge | modifiers prompt | - |
| KNOWN_SOMEWHERE (509) | tech -> trade words | knowledge | knowledge | no |
| LEVELS (510), TRY (511), SKILL_WORDS (512), SKILL (513) | | knowledge | knowledge verbs settle capacity | no |
| PHYSICS (515) | nested dict; groups: units, youth_units, elder_units (labour); ration, shelter, shelter_cold, cold_starving, fuel, camping_fire, heat, camping, beds (needs/night/buildings); labour{...}; land_blind (perception); house_spoil, cellar_spoil (goods/buildings); breaks, repair (buildings); hunger_yield, frailty, hazard (needs); refuge, regrow_winter, game_threshold (resources); combat, watch (combat); teach (knowledge); notes, felt_watched, glimpse (perception/memory); messages, say_units (converse); carry (transport); ground, master_yield, seed_selection, farming{...} (farming); cattle{...} (herds); bury, untaught | one bag for all features; merged with spec `physics` into `World.p` (world.py:90) | buildings capacity clocks farm forests labour landgen lore needs night wear world | no (no pack on PHYSICS) |
| WEATHER (593) | sight, sound, wet, words, loud | weather | climate environment roads signs | no |
| SPELLS (601) | kind->p | weather | environment | no |
| CLIMATE (610) | temp, wet_p, types, storms, eras, vis, shocks, ... | weather (scheduler D4-109) | climate | no |
| ENV (658) | night, snow_*, crop_high*, smoke*, felled, mask, loud_*, inside_sound, ford_high_after | weather/perception (visibility) | environment | no |
| THINGS (676) | body, heap*, pack, camp, trace, bands, body_days, rot_after, carcass*, hidden{how:[taught,untaught]} | things (+perception conspicuousness) | herds night signs things | no |
| FENCES (696) | wood/stone: inputs, units, through, decays, mend, kept, led, words | farming/herds | farm herds signs clocks | no |
| HERDS (706) | steps, good_grass, draw, dusk, trample, onto_road, own, road, capacity, split, share, call, pack_ox | herds (+roads pack ox) | farm herds prompt roads world.capacity | no |
| LAYOUT (727) | height words, seen fittings, overview | places/perception | layout | no |
| EVENT_EXTENT (735) | node:[kinds], building:[kinds] | perception (event reach) | perceive | no (a registry of event kinds from many features) |
| NOTICING (741) | presence, *_min, attention, carry, within, reach, eye_*, inside, loud, person, theft, sky_weather | perception | perceive roads settle signs things | no |
| FUSE (772; updated 820) | sense, label, detect, acts, riders, choices, also | combat/fuse (raid) + roads (meeting, find, crossing) + herds (herd, split) | fuse prompt | no |
| TERRAIN (784) | sight, sound, meet | roads | environment roads | no |
| LANDMARKS (793) | words, meet, challenge, default, push, good, seasons, sight, cold_night | roads | roads signs landgen | no |
| ROADS (805) | experience, call, good, flee, waves, notices, trace_days, hidden, meet_landmark, terrain | roads | layout roads run world.p_traces | no |
| TECHNIQUES.update (833) | travel modifiers: on trouble, stop at, meeting, gather on the way, lead, searching | roads (+herds lead) | | no |
| LIFE (854) | lifespan, shares, conceive, pregnancy, birth, gap, infant, child, dial, old_age, succession_days, children_work, child_skill | life | life verbs world.p_born landgen | no |

Observations: data.py is ordered roughly by feature already (goods, farming, places, resources, forests, buildings, techniques,
physics, environment, things, fences, herds, layout, perception, fuse, roads, life). TECHNIQUES/FUSE/MODIFIERS are mutated by
later sections (`.update`), i.e. features already "register" rows into shared tables. Only ITEMS, RESOURCES and TECHNIQUES carry
`pack`; derived tuples (EDIBLE, TOOLS, WEAPONS, CROP_OF, SEED_CROP, FITTING_ALIAS, MODIFIERS) are computed at import, unfiltered.

### Tables defined outside data.py in my slice

| table | where | what | feature |
|---|---|---|---|
| SEASONS, STAGES, CONDITION | world.py:44-46 | season names; hunger stage words; building condition words | kernel time / needs / buildings |
| ALL_RIGHTS, MEMBER_RIGHTS | world.py:47-48 | the five rights; members' default | claims/households |
| PRIMITIVES | world.py:1038 | the chokepoint registry | kernel |
| TOP, TODAY, FIELDS, FINGERPRINTS, WORLD_SCHEMA | schema.py:17-44 | shape | kernel record (but lists every feature's fields) |
| CURRENT | packs.py:73 | module global: active packs | kernel (data switching) |
| TAG regex | tags.py:114 | `[HT]\d+` | tags |
| KINDS | things.py:16 | thing container kinds | things |
| RATES, KNOWN_LATER | clocks.py:19-38 | glob path -> clock for every rate in data | kernel (clocks), but names paths in every feature's tables |
| PLOT, WILD, PEOPLE_A_HEARTH, FIREWOOD_HEAT | capacity.py:73-76 | capacity model constants (duplicates of farming/forest numbers) | analysis (farming+forests+buildings) |
| (in modifiers) none; reads MODIFIERS/TECHNIQUES | | | |
| order dict in `_eldest` | world.py:320 | stage ranking | life |
| table map in p_set / place_of | world.py:385-386, 675 | kind -> s-table name | kernel (entity-kind registry, hard-coded) |

---------------------------------------------------------------------------------------------------------------------------------

## 5. World construction (World.__init__, world.py:84-245)

Step-by-step, with the feature each is (= candidate "seed" step a package would register):

1. l.85-87 `self.spec`; `packs.use(self)` sets `packs.CURRENT`. kernel (data switching).
2. l.88-94 seed, days, `self.p = merge(PHYSICS, spec.physics)`, calendar (season_len, start), cold_days. kernel time + weather
   (cold_days).
3. l.95-98 hooks, _cause stack, journal, _depth. kernel.
4. l.99-103 empty `s` with all tables; `world_schema`. kernel.
5. l.105-146 per node: node record (kernel/places, unexplored: roads). Per parcel:
   a. l.108-117 `st = parcel.state`; `FO.seed(cover,size,st,year)` -> woods stocks (forests); drop `wood` dict; build `res` from
      st keys in RESOURCES filtered by `PK.on(RESOURCES[k], PK.of(self))` (resources+packs); `seam` special-cased (mining).
   b. l.118-122 grass stock from PHYSICS cattle.grazing by cover (herds).
   c. l.123-127 parcel record: kernel/places fields + farming (crop None, fertility, broken, last_crop, last_kind, works None)
      + ground, side, height (layout).
   d. l.128-129 `land` (D4-112: land/farming).
   e. l.130-136 fence via `FM.fence_need` (farming/herds).
   f. l.137-141 seeded field works (farming D2-66).
   g. l.142-145 seeded crop via `FM.CROP_OF, FM.normalise_crop, FM.grow_days` (farming).
6. l.147-149 make adjacency symmetric. places.
7. l.150-158 roads: `road:a-b` with days, track, way; `RD.build(extra,k)` terrain/stretches; `LY.build_ends` (roads/layout).
8. l.159-160 buildings: `_new_building` per spec (stock container; FITTING_ALIAS; `BL.seed_rooms`; description/lines,
   fitting_work, lasts_until, monument). buildings.
9. l.161 `_fit_seed_free` (l.298-317: shrink seeded free floor to keep SPACE.seed_keep_ground; BL.ground_total, ground_used,
   seed_rooms). buildings.
10. l.162-177 herds: by role (cows/oxen/bulls/young) or count; on a road (lost) or on a parcel. herds.
11. l.178-179 `TG.herds_at_start` tags. tags.
12. l.180-182 spec households -> institutions. households.
13. l.183-190 agents -> `_person` (hands container, people record, rng frailty/attack/defence, messages limit; `LF.stage_of`,
    `LF.lifespan` when `born` given) and household membership/head. kernel (person, hands) + life + combat + converse + households.
14. l.191-193 spec claims -> `_claim`. claims (+farming plots/of/over/joint).
15. l.194-198 `holder:` on parcel/herd -> claim. claims.
16. l.199-205 for each field parcel: `FM.sync(carry=True)`, `FM.seed_crops`. farming.
17. l.206-209 building `household:` -> claim. claims/buildings.
18. l.210-212 people `at` = spec at, else home building's node, else first node. kernel (+ claims via homes()).
19. l.213-215 default head = eldest. households/life.
20. l.216-231 spec `things`: on a road (stretch) or at a parcel via `p_new_thing` (direct call, not apply); body fields; goods;
    age; `known_by` queued. things (+roads).
21. l.232-233 seeded agreements via `p_agree` (direct). exchange.
22. l.234-235 `AG.install(self)` (hook). exchange.
23. l.236-238 per agent `KN.seed` (know) and `PC.seed` (mind; notes, pinned, interests). knowledge, perception.
24. l.239 `KN.seed_world` (KNOWN_SOMEWHERE). knowledge.
25. l.240 `PC.seed_knowledge` (kin, places, herds known, customs/lore lines; uses here.NodeView). perception/memory/lore.
26. l.241-243 `TH.remember` for seeded things' `known_by`. things/perception.
27. l.244-245 `BL.install(self)` (overflow hooks). buildings.

Order dependencies a package registry must respect: places before roads (ends need parcels); buildings before herds? (no);
herds before tags; people before claims-derived homes (step 18 needs claims 14-17); farming sync after claims; knowledge seed
before perception seed_knowledge; things after people (known_by needs mind) -> step 26 after 23; hooks any time.
Not done in __init__ but needed for a run: `today` (run.py), weather scheduler state (climate), life log.

Other World methods (kernel API used by features):
- time/chance: `d` l.331, `rng(*parts)` l.335 (salted, deterministic), `calendar` l.339, `year_days` l.349, `cold(at,day)` l.352
  (weather: climate/environment), `knows_place` l.345 (roads/perception).
- places: `node_of` 365, `at` 368, `place_of(ref)` 371 (hard-coded kinds person/container(hands|stock|other)/parcel/building/
  herd/offer), `living` 389, `present` 392, `company` 395 (roads: transit parties and today.road.meetings), `agents_acting` 407
  (life stages).
- chokepoint: `cause` 411, `hook` 419, `apply` 422, `event` 444, `record` 457.
- goods: `goods` 462, `hands` 465, `food_value` 468 (EDIBLE), `capacity` 471 (ITEMS carry/track; herds pack oxen via HD +
  HERDS), `load` 485 (ITEMS weight + LF.carried_weight), `best_tool` 489 (TOOLS), `weapon` 498 (WEAPONS).
- households/claims: `household_of` 503, `members` 506, `head` 509, `claims_on` 513, `_claim` 517, `rights` 529, `may_grant`
  541, `holders` 549, `homes` 552 (buildings claimed with access; sorted by beds), `dwellings` 560 (beds), `may_take` 564,
  `takeable` 572 (hands, stocks with withdrawal, door piles), `can_enter` 586 (door barred + access).
- budget: `units_for` 592 (PHYSICS units by season/stage/hunger/wound/arrival; LA.tired_units; LF.unit_penalty), `yield_mult`
  609 (hunger_yield).
- `save` 612. Module funcs: `show` 59, `merge` 63, `load_spec` 70 (spec `base:` variants), exceptions Refused 51, PlaceError 55.

---------------------------------------------------------------------------------------------------------------------------------

## 6. Here and Mind (here.py)

`Here(w, name, transit=False)` l.13-22: calls `packs.use(w)`; node = w.at(name); Refused if on the road unless transit; `place` =
node or road. Holds `_w` (private; a test checks agent-facing modules reference only Here/Mind).

### Here, by feature

kernel / generic queries:
- `day` 26, `p` 30, `calendar` 33, `rng` 63, `year_days` 66, `node_name` 70, `place_name` 238, `setting(key)` 235 (raw spec read)
- me: `me` 95, `hands` 99, `carried` 102, `wear(cid)` 105 (tool wear), `load` 108, `capacity(track,oxen)` 111, `units` 124,
  `yield_mult` 132, `best_tool(table)` 135, `weapon` 138
- people: `people(me)` 142 (company; roads parties), `person(x)` 146, `someone(x)` 151, `hands_of(x)` 156, `person_stage` 193
- containers: `contents(cid)` 300 (place-checked), `stock(bid)` 283
- events/acts: `events` 307 (by node), `acts_today` 309
- acting: `apply(prim,**kw)` 465 (= w.apply at own place), `event` 468, `record` 471, `cause` 474, `today()` 483 (raw today dict)

places/layout/roads:
- `road_to(x)` 73, `roads()` 82 (LY.way_known; knows_place), `layout()` 364, `overview()` 369 (layout), `landmarks_known(nid)` 374
  (reads mind landmarks), `parcels()` 213, `parcel(x)` 216

weather (all lazy EV/CL): `cold` 39, `weather` 42, `wet` 46, `snow_lying` 50, `since_heavy_rain` 54, `weather_values` 58,
`weather_words` 380

labour: `tired` 127 (LA.tired_units)

herds: `pack_ox(want)` 114 (HD.pack_ox_for), `led()` 119 (HD.led_by), `herds()` 223, `herd(x)` 263 (tags-aware resolution;
FM.head for live head count; string aliases "cattle", "the herd")

life: `body(x)` 161 (stage, hunger, wounded, carried, sex, with_child LF.showing, partner, widowed_of, parents, cared, grows
LF.grows_in), `children_on` 182, `life()` 186 (LF.on/dial/in_gap + household succession/order/heir), `age_line` 259,
`kept_of(x)` 172 (memory MEM.kept, kept_settings: perception/memory of children)

buildings: `buildings()` 196, `building(x)` 199 (name or household-name resolution via claims), `fittings(kind)` 278,
`stock` 283, `living_in(bid)` 440, `household_name(bid)` 443, `house_of(party)` 384

social (households/claims): `rights` 313, `may_grant` 316, `claims` 319, `claim_records` 322, `takeable` 327, `may_take` 330,
`can_enter` 333, `homes_here` 336, `dwellings_here` 339, `household` 342, `institution` 345, `households` 348, `head` 351,
`party_container(party)` 354 (D2-37 acting for), `meeting_today` 227 (D4-77; scans building/parcel `meeting`), `born_trades` 446
(repute: knowledge + households)

exchange: `offers` 290, `offer(oid)` 294, `agreements(who)` 449, `works_for(party)` 454 (work legs), `new_offer` 477,
`new_agreement` 480

things: `remains` 286, `things` 394, `thing(cid)` 398, `bodies` 402, `grave_left` 406, `graves` 411, `spot_name` 416,
`bury_units` 420, `search_thing` 424, `find_thing` 428, `remember_thing` 432 (writes mind), `known_things` 436

tags: `tag_of(x)` 241, `tagged_here(tag)` 250, `give_name(tag,name)` 255 (writes mind)

Generic vs feature: ~35 methods are generic kernel/social reads; ~45 are thin feature wrappers that lazily import a feature module
and forward `self._w` (weather 7, things 12, life 5, herds 4, tags 3, layout 3, labour 1, memory 1). These are the natural
"Here extensions" a package would register (e.g. `here.weather.*`, `here.things.*`).
Note leaks: `setting(key)` reads raw spec; `today()` returns the whole mutable today dict; `institution(iid)` returns any
institution (not place-scoped); `someone(x)` searches all living; `me` returns the mutable record.

Module helpers: `_household_name(w,bid)` 487 (claims with alienation), `_born_trades(w,node)` 493 (TECHNIQUES non-basic known).
`NodeView(w,node)` 507-526: engine-side read view (parcels, buildings, herds, household_name, born_trades) used by
perceive.seed_knowledge.

### Mind (l.529-565)
`Mind(w,name)`: `packs = PK.use(w)`, name, `know` (s.know[name], setdefault), `store` (s.mind[name]), `person` (people record),
`_cal`, `day`, `p`, `memory_mode` (MEM.mode_for: weak models append, D4-61), household, household_name, members, head.
Methods: `calendar` 551, `notes` 555 (person.notes), `kin` 558, `places` 561, `home_seen` 564.
All generic except memory_mode (memory) and household fields (households). Mind holds direct references to mutable state.

---------------------------------------------------------------------------------------------------------------------------------

## 7. Lazy (function-level) imports = inverted dependencies

world.py:
| line | in | imports | why |
|---|---|---|---|
| 86, 104 | __init__ | packs | set CURRENT; filter RESOURCES by pack |
| 102 | __init__ | schema.WORLD_SCHEMA | stamp shape version |
| 109 | __init__ | forests | FO.seed woods stocks |
| 132, 143, 199 | __init__ | farm | fence_need; CROP_OF/normalise_crop/grow_days; sync/seed_crops |
| 153 | __init__ | roads | RD.build terrain/stretches |
| 157 | __init__ | layout | LY.build_ends |
| 178 | __init__ | tags | herds_at_start |
| 234 | __init__ | agreements, knowledge, perceive | AG.install hook; KN.seed, seed_world; PC.seed, seed_knowledge |
| 241 | __init__ | things | TH.remember seeded things |
| 244 | __init__ | buildings | BL.install hook |
| 257 | _person | life | stage_of, lifespan |
| 272, 301 | _new_building, _fit_seed_free | buildings | seed_rooms, ground_total, ground_used |
| 302 | _fit_seed_free | data.SPACE | seed_keep_ground |
| 355 | cold | climate, environment | EV.place (validate), CL.on, CL.frost |
| 478 | capacity | herds | pack_oxen |
| 481 | capacity | data.HERDS | pack_ox carry |
| 486 | load | life | carried_weight (infants) |
| 605 | units_for | life, labour | unit_penalty; tired_units |
| 648 | p_draw | farm | record (holding's crop) |
| 691, 715 | p_new_herd, p_split_herd | tags | new_herd |
| 756, 765, 772, 779, 803 | p_claim, p_end_claim, p_set_share, p_shares, p_plots | farm | sync, record, shares |
| 835, 855 | p_die | things, life | spot_of, house_at_death; on_death |
| 890 | p_traces | data.ROADS | trace_days |
| 899, 916 | p_born | generate, knowledge, perceive; data.LIFE | names; seed know/mind; children_work, child_skill |
| 968 | _stretch_of | roads | position on road |
| 977 | p_new_thing | tags | new_thing |
| 988 | p_learn | knowledge | _set |
Top-level world.py imports only data (EDIBLE, FITTING_ALIAS, ITEMS, PHYSICS, RESOURCES, TOOLS, WEAPONS) and yaml.

here.py: top-level `from world import CONDITION, STAGES, Refused, show`. Lazy: packs (16, 534); environment (43,47,51,55,60,381);
layout (85, 366, 371); herds (116, 121); labour (129); life (166, 183, 187, 260); memory (176, 543); tags (243, 252, 256, 265);
things (252, 395-433, 9 sites); farm (265: FM.head); data.TECHNIQUES (495).

things.py: top-level environment, knowledge, data(COVERS, ITEMS, NOTICING, TECHNIQUES, THINGS). Lazy: night.sleeping_places (215),
layout (223, 270: worked_parcels, passed, next_door), tags (394), math (469, redundant).

clocks.py: life (53) for lifespan. packs.py: data.ITEMS (93), data.TECHNIQUES (98) (avoid cycle). modifiers.py: top-level
knowledge, data, world.Refused (no lazy). wear.py, capacity.py, needs.py, schema.py, tags.py, variants.py: none.

Summary of what the core reaches into: farm (8 sites), tags (4), life (6), buildings (4), knowledge/perceive (3), roads/layout (3),
herds (1), climate/environment (1), labour (1), things (2), generate (1), agreements (1). Each is a feature hook the core should
instead expose (seed step, primitive-after hook, capacity/load/units modifiers, cold provider, death handlers, entity-created
hooks for tags).

---------------------------------------------------------------------------------------------------------------------------------

## 8. Other extension points

Registries / dispatch dicts:
- `PRIMITIVES` (world.py:1038) name -> (fn, refs). Already a registry; features add primitives by editing it.
- `World.hooks` (l.95) `(when,prim)->[fn]`; only after-hooks used (agreements, buildings).
- `place_of` kind chain (l.375-387): if person / container(hands|stock|else node) / parcel|building|herd|offer via a hard-coded
  table dict. Adding an entity kind means editing it. Same hard-coded dict in `p_set` (l.675) and in the `claim` refs (l.1051:
  claimable kinds parcel/building/herd).
- Container kind chains: `place_of` (hands, stock), `may_take` (l.564-570: hands, stock, else False), `takeable` (piles at doors),
  `things.where` (l.297-305), `things.at_node`/`search` (KINDS), `Here.remains` (kind=="remains").
- `TECHNIQUES` is the act registry: `verb` (gather|work|make|build|modifier), `yield.kind` dispatched in verbs/yields (stock,
  chance, fixed, pool, clear, sow, break, works, select, tend, manure, crop, herd, care, fence, gate, milk, slaughter, mend,
  repair, clear_built, bury), `at` keys (covers|fittings|building|children|things), `draws` (a resource key, or plot|crop|herd|
  child). The handlers for these kinds live outside my slice (verbs.py/yields.py) but the vocabulary is defined here.
- Modifiers (modifiers.py): data rows with `modifies` [verb | verb:tech | verb:place], `key`, `value` ("*" any), `changes` dict
  merged; verbs read change keys (destination, hidden, units, yield, word, inputs, tier). `untaught`: tryable|no. `resolve` l.121
  writes knowledge via apply("learn"). `keys()`, `available()`, `units()`, `lines()`, `practise()`.
- `FUSE` kinds (data.py:772, 820): raid, meeting, find, crossing, herd, split: each feature adds a row.
- `EVENT_EXTENT` (data.py:735): event kinds -> reach (node|building; default parcel): a cross-feature registry of event kinds.
- `RATES` (clocks.py:19): glob over data paths -> clock (day|year|life|use|event); `per_night` converts. A test fails on unnamed
  rate fields, so each package must contribute its rate globs.
- `schema.FIELDS/TOP/TODAY`: closed field lists; per-feature fragments needed.
- `packs.CURRENT` (packs.py:73): module global, set by World.__init__, Here(), Mind(); `on(row)` filters any row with `pack`;
  `items()`, `techniques(verb)`. Risk: global state across worlds in one process (Here/Mind re-set it each construction).
- `tags.on(w)` = spec `tags: true`; feature switch read inline (here.herd, things.find). Other spec switches read in my slice:
  `children` via LF.on, `climate` via CL.on, `cold_days`, `packs/systems`, `physics` overrides, `lore`, `customs`, `tree`
  (p_born forebears), `spells`. Each is a per-feature config key at the spec's top level.
- Wear rules (wear.py): FITTINGS row `wear` = {life, count: act|inputs, mend} or {years, mend}; `on(p)` = PHYSICS labour.wear;
  `is_worn`, `factor` (0.5 when worn), `worn_words`, `use(here,bid,fittings,qty)`, `mend` (writes building.worn via set);
  `worked()` follows `needs` chain (water wheel -> millstones). Mend techniques: TECHNIQUES yield kind "mend".
  Separate tool wear: ITEMS `life` + p_wear + TECHNIQUES `wear`.
- Needs (needs.py): `food(p, c)` pure function; context keys state (housed|damaged|unsheltered|no_fuel), cold, structure, warm,
  hearth, fire, gear (camp|bedroll|tent|out), open_fire, fire_gone, fed_on_road, mult, extra, care_fed, work. Factors come from
  buildings (shelter/warm/hearth), roads (gear, fed_on_road), life (mult/extra/care_fed), labour (work), weather (cold). An
  extension point that is today a closed if-chain: each feature's factor is hard-coded rather than registered.
- Clocks (clocks.py): day/year/life/use/event; exchange rates `days_a_year` (World.year_days = 4*season_len) and
  `lifespan_days` (life).
- Capacity (capacity.py): `node(w,nid)` food from fields + woods, heat from wood_flow; constants duplicate farming/forest data
  (PLOT, WILD, a hard-coded 24-day year in wood_flow l.95). Analysis, consumes farming+forests+buildings.
- `World.units_for` (l.592-607): if-chain over season, stage, hunger, wounded, arrived midday, labour tired, life pregnancy:
  a modifier stack features contribute to.
- `World.capacity` / `load` (l.471-487): carry sources (ITEMS carry/track, pack oxen) and extra weight (carried infant): also a
  contributor stack.
- `World.cold` (l.352): providers in order: spec cold_days, climate scheduler frost, winter default.
- `World.homes/dwellings` read `fittings.beds` (buildings) and claim grounds.
- variants.py: spec transforms `one_node` (filters nodes, roads, buildings, herds, agents, claims, agreements, incidents, signs,
  customs, holdings) and `bare_roads` (strips terrain/stretches; sets `bare`). Each spec section a package owns would need a
  filter rule for `one_node`.
- Stage strings hard-coded: ("infant","child") in agents_acting l.408; ("adult","elder") in _eldest l.321; youth/elder units l.595.
- String-keyed resolution: Here.herd aliases ("cattle", "the herd", "herd"), Here.building household-name matching, Here.road_to
  prefix stripping, tags.resolve, things.find by parcel/door/dead person's name.
- RNG streams are string-keyed (`w.rng("born", d, mother)`, `"search"`, `"eye"`, `|frailty|`, `|attack|`, `|defence|`,
  `|messages|`): packages must keep their keys to preserve replays.

---------------------------------------------------------------------------------------------------------------------------------

## 9. Kernel vs feature in this slice

KERNEL (any world):
- World: spec load/merge (`load_spec`, `merge`), seed, days, `p` merge, calendar/season/year_days, `rng`, `d`.
- State skeleton: day, seq, nodes, parcels (node, name, size, adj, text, cover, res), roads (a, b, days), containers
  (kind, of, node, parcel, goods, wear), people (alive, at, transit, hands, model, name), events, acts, log, world_schema.
- Places: `place_of`, `node_of`, `at`, `living`, `present`, `company` (minus road meetings), `PlaceError`.
- Chokepoint: `apply`, `hook`, `cause`, `event`, `record`, journal calls, `Refused`, PRIMITIVES registry.
- Generic primitives: transfer, create, destroy, draw (minus crop branch), add_res, set_res, set, set_thing, new_thing (minus tag),
  depart, arrive, transit, harm (hunger part), die (body as remains container; minus feature callouts), wear (item wear).
- Goods: `goods`, `hands`, `_add`, item weight/load, `takeable/may_take` for hands.
- Here/Mind skeleton: place-scoped view, `apply/event/record/cause`, people/person/contents/events/acts, Mind with know/store/notes.
- packs (row switching), clocks (rate clocks), schema mechanism (not its lists), needs.food as a pure-function pattern (not its
  factors), modifiers mechanism (resolve/merge), the noticing rule in things.py (spot_chance, presence, attention, eye, steps)
  arguably kernel perception.
- Data: ITEMS core columns (weight, food, spoil), COVERS core (words, sight, sound), RESOURCES renewal, PHYSICS units/ration.

FEATURE:
- farming: parcel crop/soil/shares/works/fence/clearing; p_set_share, p_shares, p_plots, farm.sync callouts in claim/end_claim/draw;
  CROPS, CROP_OF, TURF, SEED_CROP, LORE, CLEARING, FENCES, PHYSICS.farming/ground/master_yield/seed_selection; farming techniques.
- herds: herd records, p_new_herd, p_split_herd, grass seeding, HERDS, PHYSICS.cattle, pack-ox capacity, Here.herd/herds/pack_ox/led.
- buildings: _new_building, _fit_seed_free, p_raise, stock overflow hook, homes/dwellings (beds), can_enter (door), FITTINGS,
  ROOMS, BLUEPRINTS, SPACE, STORES, MONUMENTS, TIERS, LINES, wear.py, PHYSICS breaks/repair/heat/shelter.
- households/claims: institutions, claims, rights/may_grant/holders, p_admit/leave/found/claim/end_claim/office, ALL_RIGHTS.
- exchange: offers, agreements, p_offer/close_offer/agree/leg/close_agreement, agreements hook, Here.offers/agreements/works_for.
- life: stage, born, partner, pregnancy, p_born/p_partner/p_office, LF callouts in units/load/die, LIFE.
- roads: road terrain/stretches/ends/way/track, traces, transit details, TERRAIN, LANDMARKS, ROADS, FUSE road kinds, travel modifiers.
- weather: cold(), Here weather wrappers, WEATHER, SPELLS, CLIMATE, ENV.
- forests/resources: FO.seed, FORESTS, seam/quarry special cases.
- things: piles/remains/carcasses/graves, THINGS, things.py (description, burial, search/find, remember).
- perception/memory: mind seeding, NOTICING, EVENT_EXTENT, LAYOUT, Here.layout/overview/kept_of, Mind.memory_mode.
- knowledge: know, p_learn, TECHNIQUES (as act registry is arguably kernel; its rows are per-feature), LEVELS/TRY/SKILL, modifiers rows.
- tags: tags.py, tag fields, tag_seq.
- combat: attack/defence/wounded/guarded, FUSE raid, PHYSICS.combat/watch, building raided/theft, parcel fight.
- converse: messages limit, PHYSICS messages/say_units.
- labour: tired/walked, PHYSICS.labour, LA.tired_units in units_for.
- water pack: fish/salt rows (already a pack, the model for others).
- analysis: capacity.py (consumes farming+forests+buildings), variants.py (spec transforms over every feature's spec sections).
