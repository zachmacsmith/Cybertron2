# Inventory B: verbs, techniques, renewal, knowledge, lore, labour, buildings, layout

Slice read in full: `cybertron2/engine/verbs.py` (2009 l), `yields.py` (34), `outcomes.py` (119), `renewal.py` (143),
`knowledge.py` (409), `lore.py` (103), `labour.py` (96), `buildings.py` (511), `layout.py` (344). Skimmed: `data.py` table shapes,
`packs.py`, `modifiers.py`, `world.py` (apply, PRIMITIVES l.1038), `here.py` (Here/Mind), `prompt.py` verb lines, `farm.act`.
Line numbers are `file:line` in `cybertron2/engine/`. Read-only; nothing in the repo was edited.

Conventions below: **P:** = primitives applied via `here.apply` (-> `World.apply`); **T:** = data tables read; **F:** = feature.
**DIRECT** = a state write that bypasses `World.apply` (no journal, no hooks) - important for a core whose only write path is apply.

---------------------------------------------------------------------------------------------------------------------------------

## 0. Shape of the verb layer (verbs.py)

- `VERB` (verbs.py:17-89): verb -> `{args (manual text), cost, doc (manual text, may hold "{crafts}"), when?}`. `VERBS`, `FREE`
  derived (l.90-92). `HANDLERS` (l.2003-2008): verb -> `fn(here, mind, a, party)`; `assert set(HANDLERS) == set(VERB)` (l.2009).
- `cost` kinds (l.101-142): int; list path into PHYSICS (`["watch","units"]`, `["teach","units_teacher"]`,
  `["teach","units_learner"]`, `["combat","units"]`); `"craft"` (technique's `units` x qty for make, + `MOD.units`, + bury's
  `units_by`); `"units"` (agent-chosen, `try`); `"write"` (`write_units`).
- `when` gates (l.95-98, string switch): `roads` (here.roads()), `herds` (any herd with head>0), `children`
  (here.children_on()), `evening` (setting). Used by `do` and by `prompt.verb_lines`/reply schema.
- `do` (l.206-222): `ALIASES` rewrite (leave/put/drop/hide -> give, l.1423), unknown/when refusal, `for` parsed only for
  {gather, work, make, build, give, accept, claim} (l.216, hard list), `_drew_reset`, `with here.cause(v, party)`, dispatch,
  append `_drew_words` (what came out of shared stores). `Refused` -> `"Refused: v: ..."`.
- Shared helpers every goods-touching feature uses: `_qty`, `item_of` (l.238; hard alias dict loaves/greens/food/weapon/tool/
  tools/wood/ore/hides/stones; pack-filtered), `_party`, `_out` (hands or party's store), `_src`, `_level`, `_consume` (l.307:
  all-or-nothing from hands then takeable stores; alt-input dicts via `KN.pick_inputs`; P: destroy), `_drawn`/`_drew_*`/`_short_note`
  (**DIRECT** append to `today["drawn"]`), `_top_up` (P: transfer), `_full_note` (BL.room_for), `_against`/`_holding_people`/
  `_holders_people` (claims -> "allowed and seen" text + event concerns).
- `cost()` is called by run.py/evening.py before `do()`; prompt.py renders `VERB` docs (prompt.py:191-215) with a `build`
  special case (rooms vs fittings) and `_verb_extra` adding text for `name` (tags) and `travel` (evening).
- Offers are not a verb: made from the reply's offers field via `agreements.py:158` (`new_offer`); `accept/withdraw/release` are verbs.

## 1. VERBS (all 38 in VERB)

| verb | handler (l.) / real work | P: primitives | T: tables | F: feature | generic? |
|---|---|---|---|---|---|
| gather | `_gather` 484 -> `_technique` 494 | draw, create, wear, add_res (fell), set (parcel.hunted), learn (via KN.tried) | TECHNIQUES, RESOURCES (via RN), ITEMS | gathering / woods / fishing / salt / hay / dung | data-driven by yield kind |
| work | `_work` 488 -> `_care` 1870 if tech=="care", else `_technique` | as gather + FM.act prims (farm.py), set/claim/shares (clear), set (building repair/mending), set_thing (bury), destroy (mend inputs) | TECHNIQUES, CLEARING, PHYSICS.repair/bury, FITTINGS(wear) | farming, herds, clearing, building upkeep, burial, child care | data-driven dispatch, bespoke per yield kind |
| make | `_make` 620 | destroy (_consume), create, learn; WE.use (fitting wear) | TECHNIQUES (verb make), TRY, FITTINGS.wear (wear.py) | making/crafts, milling, baking, smithing | fully generic recipe |
| build | `_build` 716 -> `_new_building` 749 / `_monument` 794 / `_add_room` 829 / `_upgrade` 867 / `_fitting` 962; progress `_build_work` 1046, `_works_progress` 931, `_fitting_work` 1016 | raise, claim, set (unfinished, works, fitting_work, fittings, rooms, size, structure, tier, description, built_day, lasts_until), destroy | BLUEPRINTS, ROOMS, FITTINGS, MONUMENTS, TIERS, SPACE, TRY, COVERS.ground | building | bespoke code over data tables |
| move | `_move` 1238 | transfer | ITEMS | goods/stores | bespoke |
| take | `_take` 1266 | transfer; **DIRECT** today["thefts"], mind.store["found"] | ITEMS, TH.KINDS | goods, theft, things-in-places, tags | bespoke |
| give | `_give` 1318 -> `_into_store` 1376 / `_put_down` 1389 | transfer, new_thing; **DIRECT** today["left"] | ITEMS, TECHNIQUES (modifier key "hidden") | goods/exchange, hiding (modifier) | bespoke |
| (leave, put, drop, hide) | `ALIASES` 1423 -> give | - | - | goods | alias table |
| accept / withdraw / release | `_accept` 1729 etc. -> `agreements.accept/withdraw/release` (lazy import) | (agreements.py) | - | exchange/agreements | delegated |
| host | `_host` 1436 | claim (granted, until today) | - | household/shelter | bespoke |
| grant / revoke | `_grant` 1450 / `_revoke` 1465 | claim / end_claim | - | rights/shelter | bespoke |
| join / admit | `_join` 1478 / `_admit` 1488 | **DIRECT** today["joins"/"admits"] (settled in settle.py) | institution rules | household | bespoke |
| leave_household / found | 1500 / 1510 | leave / found | - | household | bespoke |
| claim | `_claim` 1519, `_claim_plots` 1547 | claim (plots, of, over) | FM.LAND, FM.holdings | rights/land (plots: farming) | bespoke |
| drive | lambda -> `FM.drive` (farm.py) | (farm.py) | - | herds | delegated; `when: herds` |
| sleep | `_sleep` 1580 | **DIRECT** today["sleep"] | - | shelter/night | bespoke |
| set | `_set` 1591 | set (building.door) | - | buildings/rights | bespoke (only "door") |
| travel | `_travel` 1610 | **DIRECT** today["travel"/"travel_morning"/"travel_choices"] | ITEMS.track | travel/roads; pack ox (herds) | bespoke; `when: roads` |
| watch | `_watch` 1655 | **DIRECT** today["watch"] (perceive/settle read) | - | knowledge/teaching (+ senses) | bespoke |
| teach / learn | `_teach` 1663 / `_learn` 1676 | **DIRECT** today["teach"/"learn"] (settle.py:168-192 resolves) | TECHNIQUES | knowledge/teaching | bespoke |
| attack | `_attack` 1687 | **DIRECT** today["fights"] | - | force | bespoke |
| guard | `_guard` 1706 | set (person.guarded); **DIRECT** today["guards"] | - | force | bespoke |
| fire | `_fire` 1717 -> `forests.heat_of/fuel_words` | **DIRECT** today["fire"] | PHYSICS.heat | fire/fuel | bespoke |
| partner / part | 1833 / 1843 | **DIRECT** today["partner"] / partner | - | family/life | bespoke |
| try | `_try` 1853 | **DIRECT** today["try"] | - | family/children | bespoke; `when: children` |
| name | `_name` 1924 / `_name_thing` 1909 | office (heir, named) / here.give_name | - | household offices; tags | bespoke, two features in one verb |
| order | `_order` 1984 | office (order) | LIFE.children_work, TECHNIQUES | children's work | bespoke; `when: children` |
| meet / come | `_meet` 1960 / `_come` 1977 | set (building/parcel.meeting) / none | - | evening meetings | bespoke; `when: evening` |
| write / erase | `_write` 1141 / `_erase` 1193 | set (lines, description, changes), wear (carving tool) | LINES, ROOMS.places | writing on buildings | bespoke over LINES |
| rest | `_rest` 1713 | - | - | core | trivial |

Note `work` also covers `care` (yield kind `care` exists in data but is never reached in `_technique`; `_work` intercepts it, l.489),
and the `for` modifier lists `offer` as a target although offers are not a verb.

### 1a. Special cases keyed on names inside generic code (features hiding in the generic path)

verbs.py:
- l.120-136 `cost`: `units_by == "bury"`; `method == "cairn"` -> `here.bury_units`/`grave_left` (burial inside the cost function); l.137
  `v == "make"` multiplies by qty.
- l.216 hard list of verbs that accept `for`.
- l.240 `item_of` alias dict (food words, tools, wood, ore, hides, stones).
- l.407-453 `_site`: `at.things` + `method: cairn` (graves); `sites[0][0] == "thing"` (bodies); **string-matching refusal text**
  `"picked bare"`/`"no standing timber"` (l.443) to write `PC.remember_land` (land memory); `PC.LAND_DRAWS` mapping; DIRECT
  `today["worked"]` when one "went and tried".
- l.489 `_work`: technique resolved to `"care"` -> `_care`.
- l.502 `t.get("crew")` skips the know check.
- l.520 `t.get("draws") != "dead"` (dead wood is anyone's: no claim note).
- l.523-585 the yield-kind if/elif chain (section 2).
- l.550 `tech == "fell"` -> `add_res(dead)` (branches become dead wood).
- l.548 `fixed` kind draws only if the parcel holds that resource with K>0 and its renewal rule is not `"endless"` (string compare on
  a renewal rule name).
- l.567 `"method: cairn" in a["_mods"]["_used"]`.
- l.580 `structure == "stone"` -> `_mason(mind)` for repair.
- l.586-591 land memory for `stock`/`chance` kinds ("thin"/"good"/"nothing caught").
- l.597 list of yield kinds that count as practice success at zero output (sow, tend, repair, slaughter, break, manure, herd, bury,
  fence, gate) - a second copy of farm-ish kind names.
- l.607 `y["kind"] == "slaughter"` result wording; l.611 `chance` -> "You hunted"; l.615 `.replace("You gathered","You took")
  .replace("You worked","You got")`.
- l.657 make: `t.get("animals")` -> `FM.beasts_note` (others' oxen at the millstones).
- l.676-694 `_mason`/`_lvl_for`: stone work gated by knowledge of the **`wall` technique** (a fencing technique); `trade == "mason"`.
- l.721 `what in ("storey","upper storey",...)`; l.719 `UPGRADE` words; l.734 `what != "camp"`; l.753 `structure == "camp"`; l.986
  camp takes only `("beds","fire ring")`; l.909 big rooms `("hall","medium room")`; l.892/936/956 default tech `"small room"`;
  l.1038 fitting with `room` (vault) becomes a room; l.1060 blueprint `fittings`/`lasts` (camp).
- l.1110-1114 write `how` words; carve in stone -> `"stone"` + `_mason`.
- l.1393 `TECHNIQUES[m]["key"] == "hidden"`; l.1400 verb words for `"under brush"`/`"buried"`; l.1423 `hide` -> `"under brush"`.
- l.1622-1627 travel `lead` -> pack ox via `here.pack_ox`, `FM._own_or_free` (private farm fn), `FM.beasts_note`; l.1630
  `ITEMS[i].get("track")` (cart).
- l.1925 `name` with `as` -> tag naming (tags feature); l.1957 refusal text varies with tags setting.
- l.1994 `order` restricted to `LIFE["children_work"]`.

knowledge.py:
- l.163 duplicate of FM_KINDS list -> `FM.ready`; l.166-209 per-`draws` checks keyed on resource names (`dead`, `young`, `grass`,
  `dung`, `seam`, `plants`, `fish`, `wood`, `herd`) with display-name map `{plants: wild food, grass: grass to cut, ...}` (l.170).
  Lines 185-209 (sow/crop/tend/milk/slaughter on parcels) appear **unreachable** because l.163 already returns for those kinds.
- l.215 cairn; l.220 `y == "repair"` and condition; l.223 `y == "clear_built"` with a standing crop (FM.standing).
- l.69-73 `seed`: any mason trade technique seeds `wall` (stone-building gate).
- l.340-343 `options`: `crew` techniques listed for all; `verb == "build"` and `clear_built` excluded (shown on build's line).
- l.360 `mentions` skips build techniques.

## 2. TECHNIQUES machinery

### 2a. Resolution
1. `KN.resolve(x, verb)` (knowledge.py:24): lower-case; candidates = `PK.techniques()` (rows whose `pack` is on, packs.py:37);
   exact key with matching verb, else first of (same-verb first) whose key / `aliases` / full `label` / `label` before " (" matches.
2. `_as_modified` (verbs.py:145): a modifier row written as the technique (e.g. "dibble") -> base technique (`modifies` entry
   `verb:base`) with `a[key] = value`.
3. Verb check: `TECHNIQUES[tech]["verb"] == verb` else refusal listing `PK.techniques(verb=verb)`.
4. Knowledge: `_level` (unless `crew`): None -> "not among your crafts"; `aware` -> "no idea how". Level drives `TRY[lvl]`
   (inputs multiplier, success chance) in make/build.
5. Modifiers: `MOD.resolve(here, mind, verb, a, tech)` -> merged `changes` + `_used`/`_untaught` (applies `learn` to aware/rough).
6. Site: `KN.where` (knowledge.py:137) from `at`: `{covers:[...]}` -> parcels by cover; `{fittings:[...]}` -> buildings with that
   fitting (`here.fittings`); `{building: True}` -> finished buildings; `{things: "body"}` -> bodies (+ graves with cairn);
   no `at` -> `("anywhere", None)`. (`{children: True}` on `care` is not read by `where`.) `_site` picks the named or first ready site.
7. Readiness: `KN.ready` (season gate `seasons` - no row uses it; farm kinds -> `FM.ready`; per-resource exhaustion checks; bodies;
   repair; clear_built).
8. Shortfall: `KN.shortfall` (knowledge.py:249): no site; wrong site; `tools` (via `here.best_tool`; hint if a tool sits in a store);
   `animals`/`uses` -> `FM.team_shortfall`; `inputs` (with alternatives) x mult; then all sites not ready.
9. Multipliers: skill `KN.skill` x hunger `here.yield_mult()`; tool `here.best_tool(t["tools"])` -> (tool, grade multiplier;
   `"bare"` grade allowed if listed; absent grade = refused).
10. Yield (gather/work: yield-kind chain below; make: fixed `gives` dict x worn-fitting factor, success `TRY[lvl]["chance"]`).
11. Output: `create` into `_out` (hands or party store); `wear` on tool (`wear` uses) and on weapon (hunt); `KN.tried` practice;
    `MOD.practise`; `here.event("work"|"make", ..., tags=t["tags"], tech=tech)`; `here.record(verb, tech, party, site=)`.
12. Packs: `packs.on(row)` filters TECHNIQUES/ITEMS/RESOURCES rows by `pack` (only `"water"` used today: fish, salt fish, fishing
    rod, fish by hand, angle, fishing rod, salt pan, salt fish; resources fish, salt). `packs.CURRENT` is a module global set by
    `PK.use(w)` in `Mind.__init__`.

### 2b. Yield kinds (`TECHNIQUES[t]["yield"]["kind"]`) and where their code is

| kind | techniques | code | draws |
|---|---|---|---|
| `stock` | forage, fish by hand, angle | yields.py:23 (Const of base*(S/K)^b*m*tm, floor at refuge*K); verbs.py:523 `draw` | plants, fish |
| `chance` | hunt | yields.py:26 (If p*(S/K) -> Joint(Scaled(Uniform(range), m*weapon, cap=S), by: Bern)); verbs.py:527-543 (`by` goods created, `hunted` record, weapon wear) | game |
| `fixed` | fell, cut, mine, quarry, hay, dung, salt pan | yields.py:29; verbs.py:544-551 (`by_season`, endless/no-resource -> no draw, fell -> dead wood) | wood, young, seam, quarry, grass, dung, salt |
| `pool` | firewood | yields.py:31 (base*m*sqrt(S/K)); verbs.py:554 | dead |
| `clear` | clear | verbs.py:552 -> `_clear` 1789 (cover->field, fertility from CLEARING, claim "cleared" or `shares`) | plot |
| `clear_built` | clear for building | verbs.py:584 -> `_clear_built` 1762 (cover->built, grass zeroed by `set_res`, claim) | plot |
| `sow`,`break`,`tend`,`manure`,`crop`,`select`,`works`,`fence`,`gate` | sow; hoe, plough; weed; manure; reap; select seed; ditch, terrace; fence, wall; open/shut the gate | verbs.py:557 -> `FM.act` (farm.py:737 dispatch: `_sow`, `_works`, `_fence`, `_gate`, `_break`, inline tend/select/crop...) | plot, crop |
| `herd`,`milk`,`slaughter` | herd; milk; slaughter | same `FM.act` | herd |
| `bury` | bury (+ modifier method: cairn) | verbs.py:566 -> `_bury` 155 (set_thing grave/buried/cairn) | (things) |
| `mend` | dress millstones, reline oven, clear the leat | verbs.py:570 -> `wear.mend` (lazy import), inputs in hand | (fitting) |
| `repair` | repair | verbs.py:579 -> `_repair` 1744 (BL.repair_need, mending record, condition+1) | (building) |
| `care` | care | never reached here: `_work` -> `_care` 1870 (DIRECT today["care"/"care_by"/"care_gift"]) | child |

`yields.KINDS = ("stock","chance","fixed","pool")` (yields.py:11): the kinds with a distribution; `capacity/sources.py:95-111` uses
them (with `dist(...).mean()`) and `RN.step`/`RN.response` for the carrying-capacity model. All other kinds are imperative code.
`verbs.FM_KINDS` (l.91) and the copy in `knowledge.py:163` are the farm registry, as tuples of strings.

### 2c. Outcome kinds (outcomes.py)
`Dist` base (l.47) with `sample(rng)`/`mean()`; `Const` (55), `Uniform` (66), `Scaled(d,k,cap)` (77, exact mean for capped uniform),
`Bern(p)` (100), `If(p, then, otherwise)` (112, draws condition first), `Joint(got, by)` (130, value `{"got","by"}`); helpers
`_as_joint`, `got`, `by`. Used by yields.py; `farm.py:972` imports `Bern`; capacity uses `.mean()`. Random-stream order is part of
replay exactness.

### 2d. Technique-row fields and what each triggers

| field | read by | triggers |
|---|---|---|
| `verb` | resolve, _technique/_make, prompt, options, packs.techniques | dispatch by verb; `"modifier"` rows; `"build"` rows auto-made from BLUEPRINTS/FITTINGS/MONUMENTS (data.py after TECHNIQUES) |
| `label`, `aliases` | resolve, label, mentions, cards | naming |
| `basic` | KN.basic | known to all (if pack on), skill curve `SKILL.basic` |
| `trade` | KN.seed (mason->wall), _lvl_for (`mason`), seed_world (people's trade words), farm | masonry gate |
| `pack` | packs.on | row existence per world |
| `at` {covers, fittings, building, things, children} | KN.where | site kinds |
| `draws` | yields/RN/KN.ready/_technique/PC.LAND_DRAWS | which parcel resource; pseudo-keys `plot`, `crop`, `herd`, `child` are not RESOURCES (and `draw` primitive special-cases `crop`, world.py:647) |
| `yield` {kind, base, p, range, by, seed, worth, plots, stone, straw, ground, units, upkeep, fence, gate, cows, each, gives, fitting, inputs} | yields.dist, FM.act, _technique | section 2b |
| `tools` {bare/crude/copper: mult} | shortfall, _technique, KN (TOOLS hint) | tool required/multiplier |
| `wear` | _technique | tool/weapon wear per act |
| `weapon` {none, armed} | chance kind | weapon multiplier |
| `inputs` (dict; value may be an alternatives dict, e.g. smelt `fuel`, dry fodder `green crop`) | shortfall, _consume, pick_inputs, card, `_short_note` | consumption |
| `gives` (str for gather/work, dict for make) | _technique/_make, _short_note | output |
| `units` | cost, KN.tried (practice units), card | day budget |
| `units_by: "bury"` | cost | burial units from ground/cold |
| `by_season` | fixed kind | seasonal multiplier |
| `seasons` | KN.ready | season gate (unused by any row) |
| `animals` {oxen:n}, `uses` {item:n} | FM.team_shortfall, FM.beasts_note, farm | draught beasts/gear |
| `crew` | _technique, options, prompt | anyone may work it |
| `tags` | events, perceive (interest), settle | salience/noticing |
| `modifies`, `key`, `value`, `untaught`, `changes` {destination, hidden, units, yield, word, inputs, tier} | modifiers.py, _as_modified, _put_down (`hidden`), _bury (`inputs`), farm._sow (`yield`,`word`), _how (`tier`), MOD.units | modifiers |

Other tables the technique path reads: `TRY` (level -> inputs, chance), `LEVELS`, `SKILL`, `SKILL_WORDS`, `KNOWN_SOMEWHERE`,
`MODIFIERS`, `TOOLS`, `WEAPONS`, `ITEMS`, `RESOURCES`, `CLEARING`, `PHYSICS` (`refuge`, `repair`, `bury`, `farming`, `labour`,
`heat`, `teach`, `watch`, `combat`), `LIFE.children_work`.

## 3. RENEWAL (renewal.py)

Registry: `RULES = {}` filled by `@rule(name)` decorator (l.181). Signature: `rule(p, res, ctx) -> S` (pure; `res` = the parcel's
stock record `{S, K, r, ...}`; `ctx` = `context(w, par, **base)`).

| rule | l. | body | resources (data.RESOURCES default) | stepped by |
|---|---|---|---|---|
| `fast` | 188 | `night.regrow(p,"fast",...)` logistic + 1% gap refill, winter slowed | plants, grass | night._grow (NIGHTLY) |
| `threshold` | 194 | `night.regrow(p,"threshold",...)`: none below `game_threshold`*K | game | night._grow |
| `periodic` | 200 | run toward `run_K` in `run_seasons` at `run_r`, else back; else fast regrow | fish (pack water) | night._grow |
| `slow` | 219 | `forests.trees_step` | wood | forests.night (forests.py:83) |
| `young` | 225 | `forests.young_step` | young | forests.night |
| `dead` | 231 | `forests.dead_step(S, trees, year)` | dead | forests.night |
| `finite` | 237 | identity | seam | never (constant) |
| `endless` | 242 | identity | quarry, salt (pack water) | never; also verbs.py:549 skips the draw for it |
| `accrues` | 247 | identity (dung added by beasts in farm.py) | dung | never |

- `NIGHTLY = ("fast","threshold","periodic")` (l.177): which rules night._grow (night.py:466-480) applies; the woods' three are run by
  forests.night. The split is a tuple of names, not a property of the rule.
- `RESPONSES` (l.178): `proportional 1.0`, `hyperstable 0.4`, `hyperdepleted 2.0`; `response(key, res)` (l.290) -> exponent b;
  stock record overrides resource row.
- `of(key, res)` (l.280): stock record's `renewal` else RESOURCES row's (per-parcel override: an ecosystem picks its own rule).
- `step(p, key, res, ctx)` (l.286) used by capacity/sources.py:133.
- `context(w, par, **base)` (l.252): cached per (day, node) in `w.__dict__["_renewal_ctx"]` (a cache on the World object):
  place, frost (w.cold), snow, wet (environment), weather (EV.values), anomaly (climate), land (parcel `land` block), plus caller
  keys (winter, slow, trees, year, season). No rule reads the weather keys yet.

## 4. KNOWLEDGE / LORE / LABOUR

### 4a. knowledge.py
State: `w.s["know"][person][tech] = {level: aware|rough|capable|known, skill, seen, wins, fails, source, since, practised?, peak?}`.
`Mind.know` is a live reference (here.py: `self.know = w.s["know"].setdefault(name, {})`).
- Writes: `_set` (l.95) is the body of the `learn` primitive (world.py:987 `p_learn` -> `KN._set`) - a core primitive calling a
  feature module. `seed` (l.58, from agent spec `knows`/`aware_of`; called world.py:237 and :917 for children's work),
  `seed_world` (l.76, KNOWN_SOMEWHERE; world.py:239) write w.s directly at setup.
- **DIRECT** at run time: `tried` (l.369) mutates `r["wins"/"fails"/"skill"/"practised"/"peak"]` and even creates a basic record
  (l.374) without apply; only level rises go through `learn`. `saw` (l.398) mutates `r["seen"]` directly. `labour.fade` mutates
  skill/peak directly.
- Skill curve: `curve` (basic vs trade from `SKILL`), `skill_of_practice`/`practice_of_skill` (exp approach, tau); `skill_word`.
- Levels rise: 2 wins (fail=0.5) rough->capable->known (`tried`); 3 sightings (watch=2) aware->rough (`saw`, called from
  perceive.py:506); teaching resolved in settle.py:168-192 (`PHYSICS.teach.skill_share`); speech makes aware via `mentions`
  (run.py:353); modifiers tried untaught -> aware/rough (modifiers.py).
- Views for prompts: `card` (run.py:326 "look_up"), `crafts_lines` (prompt.py:521, 682), `options` (prompt.py:677, run.py:46 bot),
  `inputs_words`.
- Gameplay checks used by every technique feature: `resolve`, `level`, `skill`, `where`, `ready`, `available`, `pick_inputs`,
  `shortfall`.
- Plug-ins into knowledge: farm (FM.ready, FM.team_shortfall), verbs (`_short_note` imported lazily from verbs, l.279), labour
  (`p.labour.fade_rate/relearn` read in `tried`), modifiers (practice), perceive (saw), settle (teach), prompt/run (cards,
  options, mentions), life/world (children's skills), agreements (KN lazy imports at agreements.py:124,198,344), things.py.

### 4b. lore.py
State: none of its own; seeds kept memory lines via `memory.seed_line(w, name, text, "family lore")` (l.103).
- `LORE = {"sowing": {"to": "farmers"}}` (data.py:103). `text(key)` (l.13) is an if-switch with one key `"sowing"` (raise KeyError
  otherwise); `fits(w, name, to, holders)` (l.83) supports only `to == "farmers"`.
- `sowing_times` (l.44) runs `farm.grow_days`/`farm.season_run` over CROPS with `PHYSICS.farming` to compute best/good sowing
  halves: the lore is computed from the farm engine. `best_seasons`, `farmers` (field claimants via `w.claims_on`).
- Registration point: `perceive.py:78-79` calls `LO.seed(w, name)` when seeding a person's knowledge of places; world spec `lore:
  false | {key: false}` switches it off.

### 4c. labour.py
State: `PHYSICS["labour"]` params (work_food, over_food, guard_food, over_units, fatigue, step, free_steps, fade_rate, fade_after,
fade_keep, relearn); person fields `tired {day, units}`, `walked` (via `set` primitive); `today["units"]` (DIRECT, l.168);
know records `peak`, `practised`.
- `work_need(p, today, name)` (l.127) -> night.py:98 adds to the night's food need.
- `close_day(w, today, used, budget, names)` (l.140) -> run.py:1059: fatigue from overwork and from the walk (`today["route"]`
  produced by `layout.routes`); writes person `walked`, `tired` via `w.apply("set", ...)`.
- `tired_units(w, name)` -> here.py:130 (`Here.tired`).
- `fade(w)` (l.176) -> night.py:200: **DIRECT** writes `r["peak"]`, `r["skill"]` in `w.s["know"]`.
- Overwork cap read in run.py:953 (`over_units`). All zero -> no-op (replay-safe).

## 5. BUILDINGS / LAYOUT

### 5a. Data (data.py)
- `ROOMS` (214): small/medium room, hall -> `{floor, places, <structure>: {materials, units, trade?}}` (wattle only for small room).
- `BLUEPRINTS` (226): small room, medium room, hall (materials from ROOMS), camp `{size 4, structure camp, fittings {beds 4, fire
  ring 1}, lasts 10}`.
- `FITTINGS` (173): beds, hearth, bins, hand mill, granary, fire ring, oven, anvil, cellar, millstones, water wheel, stalls, woodshed,
  vault; fields `label, materials, units, basic, trade, spaces, per (bed|stall), holds {kind: qty}, by (footprint|space), heavy,
  needs, site (cover adjacent), structure (oven: stone), ground (woodshed), room (vault), fire, spoil, fireproof, fodder, dung, wear
  {life, count act|inputs, years, mend}, does, aliases`. `FITTING_ALIAS`.
- `MONUMENTS` (258): carved post, standing stone, cairn (`materials, units, basic, trade, structure, aliases`).
- `TIERS`/`TIER_ORDER` (267), `SPACE` (237: added, storeys, upgrade, order, camp_floor, camp_store, monument_ground, seed_free,
  seed_keep_ground), `STORES` (249: kinds, order, floor, words), `LINES` (276: places, words, chars, units, other, carve_tools,
  carve_wear, spots, how), `COVERS[*].ground`, `CLEARING.built`, `PHYSICS.repair`, `PHYSICS.breaks`.
- Every BLUEPRINT/FITTING/MONUMENT is also auto-registered as a `verb: "build"` TECHNIQUE (data.py after MODIFIERS) for knowledge.

### 5b. Building record (world `_new_building` + buildings.py docstring l.11-13)
`name, node, parcel, structure (wattle|timber|stone|camp), fittings {name: n}, stock (container id), condition (0 ruin..2 sound),
door, rooms [{kind, floor, storey}], size, tier, monument, unfinished {blueprint, units_left}, built_day, lasts_until, works {kind:
room|upgrade|tier, ...units_left, tech, by}, fitting_work {fitting: {n, units_left}}, mending {units_left, day}, description {text,
by, day, was}, lines [{slot, text, by, day, how, was, was_by}], changes [{day, text, by}], meeting, fire`; wear records (wear.py).

### 5c. Code (buildings.py: pure functions over records, plus engine-side)
- Floor/space: `exempt` (camp, monument), `rooms`, `floor`, `footprint` (incl. works and vault under way), `storeys`, `places`
  (lines), `tier`, `fitting_spaces`, `room_words` (imports `layout._count`), `free_floor`, `space_words`.
- Ground: `ground_total` (COVERS.ground x size), `ground_of` (footprint + woodshed ground; monument/camp constants), `ground_used`,
  `ground_free`.
- Storage: `_kind_items` (`food` = EDIBLE, `weight` = any, else STORES.kinds), `stores`, `alloc`, `fits`, `room_for` (bisection),
  `full_words`, `camp_weight`, `vaulted` (run.py:394, fire), `stall_share` (farm.py:1268, 1462 - winter housing of beasts).
- Costs: `room_cost`, `upgrade_cost` (trade mason/carpenter), `base_cost`, `tier_cost`, `tier_up`, `repair_need` (PHYSICS.repair).
- Seeding: `best_rooms` (itertools search), `seed_rooms` (world.py:278, 316).
- Engine side: `install(w)` (l.379) registers `w.hook("after","create"|"transfer", overflow)` (world.py:245) - the only hook
  registration in the slice; `overflow` (l.385) moves what does not fit to a pile at the door (P: new_thing, transfer; event "left").
- Writing: `spot_words`, `line_words`, `cap_text`, `people_of`, `read(w, name, bid, how)` (night.py:40 "slept", perceive.py:564
  "day") **DIRECT** writes `w.s["mind"][name]["read_changes"/"read"]`; `entered` scans today's events by kind (work, make, build,
  store, give, speech, write).
- Verbs side (verbs.py 669-1220): build family (section 1) and write/erase. Work units per action = `2 * KN.skill * yield_mult`
  (three copies: `_works_progress` 936, `_fitting_work` 1023, `_build_work` 1050; `_repair` 1753 uses `2*m`).
- Mending: `work repair` (verbs `_repair`), `work dress millstones/reline oven/clear the leat` (yield `mend` -> wear.py `mend`);
  breaking is elsewhere (PHYSICS.breaks, night). Fitting wear: wear.py (`worked`, `factor`, `use`, `worn_words`) called from `_make`.
- Monuments: `_monument` (l.794), aliases via `MONUMENT_ALIAS` (l.672), places from `LINES.places.monument`; `layout.tier_words`.

### 5d. layout.py - correction to the brief
layout.py is **not** positions of buildings in parcels: the engine has none (a building has only `parcel`). It is the **parcel
graph inside a node** (D2-114..116): `side`, `height`, `parcels_of`, BFS `_layers`, `steps`, `path` (keyed tie-break rng),
`slept_at`, `worked_parcels` (reads `today["worked"]`, a building counts as its parcel), `night_at`, `route`/`routes` (writes
`today["route"]` DIRECT, read by labour and perceive), `passed`, `next_door`; road ends (`road_ends`, `default_end`, `build_ends`);
hidden ways (`opened`, `way_own`, `way_known`, `learn_way` DIRECT `w.s["mind"][name]["ways"]`, `wear_way` and `regrow` DIRECT on
`w.s["roads"][rid]["ends"]`, `find_ways` noticing via `things.spot_chance`); words (`side_words`, `height_words`, `layout_lines`,
`tier_words` (building tiers), `overview` (buildings with `LAYOUT.seen` fittings, tiers, smoke, houses on built ground, main crop
via `FM.main_crop`, covers, people, herds), `_count`, `_and`). Callers: here.py (layout, overview, roads), herds.py (paths),
farm.py:1323 (regrow at night), night.py:234 (wear_way), perceive.py (find_ways, learn_way), roads.py:349 (tier_words), run.py:342.
Positions inside a parcel are a c2viz presentation choice (CLAUDE.md).

## 6. EXTENSION POINTS (registries, dispatch, string switches, lazy imports)

### 6a. Registries / dispatch tables
| where | kind | keys |
|---|---|---|
| verbs.py:17 `VERB` | dict registry | 38 verbs; `cost` mini-language; `when` |
| verbs.py:2003 `HANDLERS` | dict dispatch | verb -> handler (drive is a lambda into farm) |
| verbs.py:1423 `ALIASES` | dict | leave/put/drop/hide -> give |
| verbs.py:91 `FM_KINDS` (+ knowledge.py:163 copy) | tuple membership | farm yield kinds |
| verbs.py:523-585 | if/elif on `y["kind"]` | stock, chance, fixed, clear, pool, FM_KINDS, bury, mend, repair, clear_built |
| verbs.py:597 | tuple | kinds that count as success at zero output |
| verbs.py:95-98 `verb_here` | if-chain on `when` | roads, herds, children, evening |
| verbs.py:101-123 `verb_units`/`cost` | switch on cost type | int, list path, craft, units, write |
| verbs.py:216 | tuple | verbs accepting `for` |
| verbs.py:240 `item_of` | dict | good-name aliases |
| verbs.py:670 `STRUCTURE_WORDS`, 672 `MONUMENT_ALIAS`, 673 `UPGRADE` | dicts/tuple | build words |
| verbs.py:1111, 1183 | dicts | write how words |
| verbs.py:1400-1401 | dicts | hidden words |
| yields.py:19 `dist` | if-chain | stock, chance, fixed, pool (`KINDS`) |
| renewal.py:176 `RULES` + `@rule` | decorator registry | 9 rules; `NIGHTLY` tuple; `RESPONSES` dict |
| knowledge.py:157 `ready` | if-chain on yield kind and `draws` name | see 1a |
| knowledge.py:137 `where` | if-chain on `at` keys | things, covers, fittings, building |
| lore.py:13 `text` | if key == "sowing" | one lore key |
| lore.py:83 `fits` | if to == "farmers" | one audience |
| buildings.py:112 `_kind_items` | switch | food, weight, STORES.kinds |
| buildings.py:136 `stores` | switch on fitting `by` | footprint, space, count |
| buildings.py:379 `install` | `w.hook` | after create/transfer |
| buildings.py:474 `entered` | event kinds tuple | work, make, build, store, give, speech, write |
| layout.py:283 `tier_words` | tier names rich/grand | |
| packs.py `on/items/techniques` | row filter | `pack` field |
| modifiers.py `resolve/units/lines` | data registry | `MODIFIERS` with `modifies` targets `verb`, `verb:tech`, `verb:place` |

### 6b. Function-level (lazy) imports in the slice
| at | imports | needs | why lazy |
|---|---|---|---|
| verbs.py:135, 159, 193, 413 | `things as TH` | grave_words (TH also imported at top l.11, so redundant) | leftover |
| verbs.py:242, 497, 623 | `packs as PK` | items(), techniques() | none strong (packs is a leaf) |
| verbs.py:571, 632 | `wear as WE` | mend, worked, factor, use, worn_words, on | cycle avoidance/optional fitting wear |
| verbs.py:1270 | `tags as TG` | tag_in | tags feature |
| verbs.py:1720 | `forests as FO` | heat_of, fuel_words | fire/fuel feature |
| verbs.py:1730, 1735, 1740 | `agreements as AG` | accept/release/withdraw | AG imports verbs helpers -> cycle |
| verbs.py:1765, 1792 | `data.CLEARING` | clearing costs | none |
| verbs.py:1985 | `data.LIFE` | children_work | none |
| knowledge.py:16, 27, 115 | `packs` | on, techniques | cycle-safe habit |
| knowledge.py:164, 222, 270 | `farm as FM` | ready, standing, team_shortfall | farm imports knowledge (cycle) |
| knowledge.py:265 | `data.TOOLS` | tool hint | none |
| knowledge.py:279 | `verbs._short_note` | who drew it today, recipe source | verbs imports knowledge (cycle); knowledge depends on a private verbs helper |
| knowledge.py:79 | `data.KNOWN_SOMEWHERE` | seed_world | none |
| renewal.py:190, 196, 205 | `night as NI` | regrow | night imports renewal (cycle) |
| renewal.py:221, 227, 233 | `forests as FO` | trees/young/dead_step | forests imports renewal (cycle) |
| renewal.py:266 | `climate as CL, environment as EV` | weather context | heavy, cycle |
| renewal.py:282, 292 | `data.RESOURCES` | default rule/response | none |
| lore.py:49-50 | `farm as FM`, `data.PHYSICS` | grow_days, season_run | farm heavy/cycle |
| lore.py:90 | `life as LF, memory as MEM` | MINOR, seed_line | cycle |
| labour.py:182 | `knowledge as KN` | curve | cycle-safe |
| buildings.py:81 | `layout._count` | number words | private helper reuse |
| buildings.py:216, 409 | `world.show` | number formatting | world imports buildings (cycle) |
| buildings.py:323 | `data.PHYSICS` | repair | none |
| buildings.py:338 | `itertools` | best_rooms | none |
| layout.py:177 | `environment as EV` | felled | cycle |
| layout.py:230 | `things as TH` | spot_chance | cycle |
| layout.py:281 | `data.MONUMENTS` | tier_words | none |
| layout.py:309 | `farm as FM` | main_crop | cycle |

## 7. Features in this slice and what each folder would REGISTER on a core

Core assumed: World/apply/PRIMITIVES (transfer, create, destroy, draw, set, set_res, add_res, wear, claim, end_claim, raise,
new_thing, set_thing, learn, office, ...), Here/Mind, verb registry + `do`/`cost`, day record (`today`), events, records, packs,
outcome distributions (outcomes.py is generic and belongs in core), goods helpers (`_consume`, `_out`, `item_of`, `_party`),
knowledge core (levels, skill curve, resolve, where/ready/shortfall hooks), renewal registry.

1. **techniques (core-ish generic act)**: `_technique`/`_make` pipeline, `TRY/LEVELS/SKILL`, yield-kind registry (`register_yield(kind,
   fn, dist=None, ready=None, counts_as_practice=bool)`), site-kind registry for `at` keys (`covers`, `fittings`, `building`,
   `things`), field hooks (`tools`, `wear`, `inputs` with alternatives, `by_season`, `crew`). Manual text for gather/work/make with
   `{crafts}`. Tests: test_cybertron2_engine, act_fixes.
2. **gathering (land stocks)**: rows TECHNIQUES forage, hunt, fell, firewood, cut, mine, quarry, dung, hay; RESOURCES plants, game,
   wood, young, dead, seam, quarry, dung, grass; ITEMS wild food, meat, hide, timber, firewood, copper ore, stone; yield kinds
   stock/chance/fixed/pool (dist fns); renewal rules fast/threshold/finite/endless/accrues; readiness checks per resource (now in
   KN.ready) and their refusal words; land-memory hook (`PC.LAND_DRAWS`, `remember_land`); hunt's `hunted` record + kill signs;
   fell -> dead wood hook. Tests: capacity, package_f.
3. **woods/fuel** (with forests.py): renewal slow/young/dead + forests.night stepping; `fire` verb (args/doc, PHYSICS.heat); firewood/
   cut rows; charcoal recipe; `heat` item field.
4. **fishing & salt (pack "water")**: already a pack: rows fish by hand, angle, fishing rod, salt pan, salt fish; RESOURCES fish
   (periodic), salt (endless); `periodic` renewal rule; ITEMS fish, salt fish, fishing rod; readiness "fished out" text.
5. **farming** (with farm.py): yield kinds sow, break, tend, manure, crop, select, works, fence, gate (`FM.act`, `FM.ready`); clear
   (`_clear`), clear_built (shared with building); techniques sow, hoe, plough, ditch, terrace, select seed, weed, manure, reap,
   fence, wall, gates, clear; modifier `method: dibble`; KNOWN_SOMEWHERE; CROPS, CLEARING; `claim` with `plots` (`_claim_plots`,
   `FM.holdings`); `draw` primitive's `crop` branch; lore `sowing` (LORE row, text fn, audience `farmers`); `work.on`/`plots` args.
   Tests: farm, plot_shares, crop_growth, base_fertility, package_c.
6. **herds/cattle** (farm.py/herds.py): yield kinds herd, milk, slaughter; techniques herd, milk, slaughter, cheese, harness;
   `drive` verb (`when: herds`); `animals`/`uses` row fields + `team_shortfall`/`beasts_note`; travel `lead` pack ox; stalls
   (`BL.stall_share`); `accrues` dung renewal. Tests: use_by_physics, slaughter_signs, package_c.
7. **making/crafts**: `make` verb; recipe rows (grind, mill, water mill, dry fodder, pack, handcart, bread, oven bread, dry meat,
   charcoal, wooden plough, bedroll, tent, crude tool/weapon, smelt, copper tool, coin); fitting wear (wear.py) + `mend` yield kind
   + mend techniques; `TRY` chance/inputs.
8. **building**: verb `build` (+ args/doc, `{crafts}` split into rooms/fittings in prompt), data ROOMS, BLUEPRINTS, FITTINGS,
   MONUMENTS, TIERS, SPACE, STORES, COVERS.ground; modifiers how: fine/rich/grand; techniques repair (yield `repair`), clear for
   building (yield `clear_built`); primitive `raise`; hook `after create/transfer -> overflow`; seeding `seed_rooms`; the mason gate
   (`wall` knowledge); readers for other features: `stores/alloc/room_for/full_words` (goods), `vaulted` (fire), `stall_share` (herds),
   `tier_words` (layout/roads/signs), `entered/read` (perception). Tests: buildings, fittings_ground, act_fixes.
9. **writing on buildings**: verbs write/erase (`cost: "write"` -> `write_units`), LINES, ROOMS.places, `read/entered/line_words/
   cap_text/_changed`, mind fields `read`, `read_changes`; prompt.written_lines. Tests: buildings.
10. **goods/stores/exchange**: verbs move, take, give (+ aliases), accept, withdraw, release; theft record; `_drawn` ledger and
    `_drew_words`/`_short_note`; overflow at the door; agreements.py; modifier `for`. Tests: exchange, act_fixes, kept.
11. **things in places / hiding** (things.py): give to a place, `new_thing` piles, modifiers hidden: under brush/buried, `hide`
    alias, take from a spot/search, `found` mind list; tags naming (`name` + `as`, `take` by tag). Tests: package_a.
12. **burial**: technique bury (`units_by`, `at.things`), modifier method: cairn, yield `bury`, `_bury`, `_thing_site`, cost special
    case, `PHYSICS.bury`, `COVERS.dig`; monument "cairn" is a different thing. Tests: package_a.
13. **household/rights/shelter**: verbs host, grant, revoke, join, admit, leave_household, found, claim (whole), sleep, set (door),
    name (heir/head); settle.py resolves joins/admits. Tests: engine, infant_partner.
14. **family/life**: verbs partner, part, try (`cost: units`, `when: children`), order (`LIFE.children_work`), work care (`_care`,
    today care keys). Tests: package_d, infant_partner.
15. **force**: attack, guard (PHYSICS.combat). **travel**: travel (roads; evening variant). **evening meetings**: meet, come.
16. **knowledge/teaching**: verbs watch, teach, learn (PHYSICS.watch/teach costs); `saw`, `tried`, `mentions`, cards, options;
    settle.py teaching. **labour**: PHYSICS.labour, close_day/work_need/tired/fade (night & run hooks), "overwork" reply field.
    Tests: labour.
17. **layout (parcel graph)**: core-level geometry (routes, steps) plus hidden-ways sub-feature (roads) and overview words.

Each needs, generically: data rows (with `pack` tag), verb rows (`args`, `doc`, `cost`, `when`) + handler, yield kinds (+ dist
for capacity), readiness/refusal text, renewal rules, event tags/salience, `today` keys it owns (and who settles them), night/day
hooks, prompt text fragments, knowledge rows (auto build-techniques), tests.

## 8. Cross-feature couplings that would be awkward to split

1. **`_technique` is a hub**: one function (verbs.py:494-616) owns land-memory, claims notes, kill signs, fell->dead wood, tool and
   weapon wear, practice-success list, result wording per kind. A yield-kind registry must carry: dist, apply-fn returning
   (got, gives, word, thing, suffix, holding), practice-success flag, memory hook, result-text override.
2. **Farm kinds listed in three places** (verbs.FM_KINDS l.91, knowledge.ready l.163, practice list l.597) plus `a["_on"]` set by
   `FM.act` and read back in `_technique` (l.561) - mutation of the action dict as a side channel.
3. **Stone building <-> walling**: `_mason` gates stone rooms, storeys, upgrades, stone repair and carving in stone on knowing the
   `wall` technique (a fencing/farming row); `KN.seed` auto-grants `wall` to masons. Building cannot be split from farming fences
   without moving `wall` or introducing a "masonry" skill.
4. **knowledge <-> verbs cycle**: `KN.shortfall` imports `verbs._short_note` (private), which reads TECHNIQUES `gives`/`inputs` and
   today's `drawn` ledger owned by the goods code.
5. **knowledge.ready knows every resource and farm/herd/burial/repair/building state** (string-keyed); needs per-feature `ready`
   hooks keyed by `draws`/yield kind/site kind.
6. **`learn` primitive body lives in knowledge.py** (world.py:987); `draw` primitive special-cases `crop` via farm (world.py:647).
   Core primitives depend on feature modules.
7. **DIRECT state writes bypass apply/journal**: KN.tried/saw (skill, wins, fails, seen, peak), labour.fade, buildings.read
   (mind.read), layout.learn_way/wear_way/regrow, `today[...]` lists/dicts from ~20 verbs, mind.store["found"] (_take). A core
   that requires apply for all writes must add primitives (e.g. `practise`, `note_mind`, `day_mark`) or declare `today` as
   scratch state.
8. **`today` record schema is global** (run.py:38 `blank_today`): keys owned by teaching, travel, force, family, child care,
   households, sleeping, fire, route; each feature would need to register its day keys and its settle step.
9. **Building storage serves goods**: `_full_note`, `_move`, `_into_store`, overflow hook and `BL.room_for` make the goods feature
   depend on the buildings' storage model; camps' `camp_store` special case lives in buildings.
10. **Burial is threaded through generic code**: `cost` (units_by), `_site` (cairn/graves), `KN.where` (`things`), `KN.ready`
    (thing kind), `_technique` (`bury` kind, `"method: cairn"` string), modifiers (cairn inputs).
11. **Modifiers are techniques**: `MOD.resolve` writes `learn`, and modifiers' `changes` are read by whichever feature (hidden ->
    give, tier -> build, yield/word -> farm sow, inputs -> bury, units -> cost). A modifier row belongs to the feature that reads it,
    but the registry is TECHNIQUES-wide.
12. **Lore is computed from farm physics** (`farm.season_run`, `grow_days`) and seeded through memory/perceive; it is part of farming,
    not a separate system.
13. **Herds leak into making/travel/building**: `make` -> `FM.beasts_note` (millstones' ox), travel -> `FM._own_or_free` (private)
    and `beasts_note`, stalls in buildings -> `BL.stall_share` read by farm.
14. **layout reads farm/buildings/herds/roads** for `overview` and `tier_words`; `buildings.room_words` imports `layout._count`.
15. **Prompt rendering is coupled to verbs internals**: prompt.py reads `V.VERB`, `V.verb_units`, `V.verb_here`, `V._works_words`
    and special-cases `build`/`name`/`travel` text; a feature-registered verb needs a text hook.
16. **packs.CURRENT is a module global** set from `Mind.__init__`: code that resolves items/techniques without a Mind in hand uses
    whatever world last made a Mind.
17. **Renewal stepping split**: NIGHTLY rules by night._grow, woods' rules by forests.night, finite/endless/accrues never stepped;
    verbs.py:549 compares the rule name to `"endless"`. Renewal rules need a "stepped by" attribute rather than a name tuple.
18. **Capacity model** (cybertron2/capacity/sources.py) reads `yields.KINDS`, `dist().mean()`, `RN.step`, `RN.response` and
    TECHNIQUES `draws/gives/yield`: any change to the yield-kind registry must keep `dist` for analysable kinds.
