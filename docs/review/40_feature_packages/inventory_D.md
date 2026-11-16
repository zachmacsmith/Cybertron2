# Inventory D: the perception and prompt layer (signs, perceive, prompt, view, views, memory, converse, chronicle)

Repo `/home/user/cybertron2`, engine `cybertron2/engine/`. Read-only survey, 16 Nov 2026. Line numbers are of the files as they stand.
Sizes: signs.py 1969, perceive.py 728, prompt.py 892, view.py 216, views.py 231, memory.py 244, converse.py 77, chronicle.py 149.
(A legacy pre-engine `cybertron2/perceive.py` and `cybertron2/prompt.py` also exist, used only by `cybertron2/run.py` and
`tests/test_cybertron2.py`; out of scope.)

Notation: "generic" = would sit in a core; "feature" = belongs in a feature folder. Feature names used below: **farm** (crops, fields,
soil, works), **pasture** (grass, dung), **herds** (beasts, fences, gates, strays, driving, milking, calving, slaughter), **wild**
(forage, game, timber, firewood, seam, quarry, charcoal), **sky** (weather, climate, season), **buildings** (condition, fire, fuel,
stores, fittings, tiers, works, rooms, writing), **people/life** (hunger, wounds, stages, pregnancy, infants, care, partner, elder,
succession), **things** (containers in the open: bodies, graves, heaps, caches), **carcass**, **roads** (road, traces, travellers,
passing, landmarks, hidden ways), **conflict** (fights, raids, thefts, guard, night fuse), **fire** (house fire), **death/burial**,
**dogs** (a `dog` fitting), **crafts** (make), **knowledge** (techniques, learning by watching), **agreements**, **labour**, **memory**.

---------------------------------------------------------------------------------------------------------------------------------------

## 1. SIGNS (signs.py)

### 1.1 Row shape (one dict per possible sign; "new states add rows here, not code", D4-24, docstring l.1-12)

| key | meaning | consumer |
|---|---|---|
| `when(x)` | condition on the context namespace `x` (exceptions KeyError/TypeError/ZeroDivisionError[/AttributeError] = false) | `facts.emit` l.1111, `true_rows` l.1886 |
| `text(x)` | the sentence | everywhere |
| `sense` | sight / sound / smell / touch (default sight) | noticing rule: visibility, carry, eye |
| `p` | legacy base chance (number or `p(x)`); becomes the fact's `salience`; 1 if unset. Guide: no `p` on new rows | `chance_of` base, ordering |
| `own` | conspicuousness (number or `own(x)`), the D4-75 input; default 1.0 | spot `own` -> `TH.spot_chance` |
| `tags` | topic tags (farming, harvest, food, animals, danger, season, shelter, building, timber, fuel, travel, hunting, mining, craft, smithing, weapons, family, death, place) | `perceive.relevance` (interests, hunger->food, danger) |
| `knack` | a technique: x2 if practised, x0.5 if not (x1 for basic work) | `perceive.knack` l.262 |
| `knows` / `lay` | only one who knows / does not know the technique reads it (expert vs lay reading) | `readable` l.1877, `perceive.practised` l.274 |
| `reach` | `near` (close look: step 0, attention x close), `around` (step <= 1), `count` (only when attending; heaps), else "rule" | `chance_of` l.222, `roll` l.1915, NOTICING["reach"] |
| `night` | sensed in the dark: presence from where one sleeps (`TH.night_spot`), night visibility | `TH.presence` |
| `who` | scope: `others` / `doer` / `inside`, mapped to a people list by the caller (`spot_rows(..., who={...})`) | `spot_rows` l.1674 -> fact `only` |
| `eye` | depends on the eye for the land (`eye_on="bare"`; some people have none) | `chance_of` l.230 |
| `land` | `(what, state)`: the noticer remembers the place's bareness | `perceive.remember_land` l.315, shown in prompt place line |
| `peek` | a look through an open door: never in the notice; only when attending to that building | `perceive.evening` l.406/415/455 |
| `gate` | the row means a gate is open: one of the holding household shuts it on noticing | `spot_rows` -> fact `gate`, `perceive._shut_gate` |
| `holders` | (EMPTY rows) documentary only; **never read**: the scope is passed by the caller as `only=people` l.1090 | none (dead key) |

A **fact** (what a row becomes; perceive.py docstring l.6): `{id, about:[subject keys], sense, text, salience, tags, concerns, ...kw}`.
Subjects: `person:<n>`, `building:<id>`, `parcel:<id>`, `herd:<id>`, `thing:<cid>`, `sky`. Extra keys per path: `spot{node, parcel,
own, inside, everyone}`, `knack`, `sign` ("<about0>#<table><i>"), `peek/eye/land/knows/lay/reach/night`, `only`, `gate`, `missing`,
`thing`, `ambient`, event keys (`event, actor, tech, kind, dawn, at`).

### 1.2 Every sign table

| Table (line) | rows | Feature | State read (via its context) | Producer that emits it | Notes |
|---|---|---|---|---|---|
| CROP (26) | 36 | farm | crop record on a field/holding: progress, area_left, ripe_day, window, lying, stand, sown, frost_day, never, no_winter, stalled, quality, rotting, failed/shown_failed, weeded, reaped, hardy, kind; parcel last_crop; today's work events (reap, sow), today `green_cut`; CROPS needs_winter; FM.rate by season | `facts` l.1131 (seed on turf), l.1134 (each holding of a field) | 22 rows legacy `p`, 14 `own`; knacks reap/weed/sow |
| FIELD (112) | 21 | farm | parcel broken, last_crop, fertility, ground (wet/hill), works {done,kept,ground}, dead crop record, today's plough/hoe events, `turned`, herds on it, snow, cold, weather | `facts` l.1136/1138/1143; `HOLDING_ROWS = range(3,10)` (l.855) = rows about a holding's own ground (positional!) | in shares: rows 3-9 per holding with `nm = part` |
| PASTURE (159) | 9 | pasture | res grass S/K, res dung S, herds on parcel, season, snow, cold | `facts` l.1145 (cover pasture/meadow, or grass res, or dung > 5, D2-189) | all legacy `p`; knacks herd/hay |
| HERD (182) | 19 | herds | herd: name, with/pack, last_calf, milked{day,n}, watched, hungry, bulls/cows/young/births/in_milk; FM.herd_words; adj crop standing; parcel fence level/gate | `facts` l.1148 (each herd with head > 0, context(here, parcel, h)) | row 0 own 0.95 always true |
| TRAMPLED (226) | 3 | herds x farm | crop `trampled{day,qty,by}`; the trampler's home parcel name | `_herds_out` l.1094-1096 | uses `context()` |
| ASTRAY (242) | 10 | herds | herd off home: parcel cover, main crop ripe, trampled qty by this herd, hungry, claims (whose), split_of, strayed_in | `_herds_out` l.1082-1084 (herd_context) | own + p |
| EMPTY (264) | 3 | herds | home pasture empty, home fence gap/gate open | `_herds_out` l.1085-1090, `only` = holders' people, `missing=hid` | drives `remember_beasts(..., "missing")` |
| FENCE (272) | 9 | herds (fences) | parcel fence {kind, units, built, level, gate, opened.by}, FENCES words, FM.fence_need, herd inside | `_herds_out` l.1091-1093 (fence_context) | row 1 `gate=True` |
| WAY (296) | 4 | roads (hidden ways, D2-98) | x built inline in `perceive.evening` l.437: nm, side, opened, worn, way | `perceive.evening` l.439 via `roll(..., least=True)[:1]` | NOT by the noticing rule here: the find itself is rolled in `LY.find_ways` |
| CARCASS (310) | 10 | carcass (herds/wild) | container kind carcass: died, hidden "off the road", cause starved, goods meat/hide, weather/snow/cold at it, dogs at node | `bundle()` l.1898 -> perceive.facts l.173, roads._notices l.335 | |
| SLAUGHTER (342) | 10 | herds (slaughter) | parcel `slaughter{day, kills[{beast,herd,by}]}`, herd on parcel, cover, weather/snow/warm, dog fittings | `_slaughtered` l.1719 | the worked D4-71 bundle; who others/doer |
| SLAUGHTER_DOGS (370) | 1 | dogs x herds | same ctx, read at each dog-house parcel | `_slaughtered` l.1728 | |
| FIGHT (386) | 6 | conflict | parcel `fight{day, fights[{by,target,outcome}]}` | `_aftermath` l.1761-1767 | |
| RAID (403) | 3 | conflict | building `raided{day,outcome}` | `_aftermath` l.1794 loop | who=inside |
| HUNTED (414) | 5 | wild (hunting) | parcel `hunted{day,kills[{by}]}` | `_aftermath` l.1772-1777 | |
| FIRE (430) | 7 | fire | building `fire_hit{day}` | `_aftermath` l.1794 loop | own 3 glow |
| BIRTH (449) | 1 | life | today's event kind "birth" about the building | `_aftermath` l.1801-1805 | |
| GUARD (456) | 2 | conflict | person `guarded{day, at}`, weapon | `_aftermath` l.1806-1812 | |
| DRIVEN (465) | 4 | herds | herd `driven{day, from, to, by}` | `_aftermath` l.1813-1819 | |
| THEFT (478) | 3 | conflict | building `theft{day, item}` | `_aftermath` l.1794 loop | |
| BROKE (489) | 4 | buildings (wear/night) | building `broke{day, to}` | `_aftermath` l.1794 loop | |
| BURIAL (502) | 7 | death | today's work events tech "bury" on parcel; bodies at node: grave.day, buried, cairn_day, cairn_by | `_aftermath` l.1778-1791 (lazy `things` import) | |
| DOGS (520) | 1 | dogs x conflict | fight ctx + house name | `_aftermath` l.1768-1771 | |
| SKY (527) | 33 | sky/climate | cold today/yesterday, season & days left, weather today/tomorrow, snow lying, days since heavy rain, dry/wet runs, climate day values (temp, low, rain, wind, gale threshold, turned), storm coming, a water parcel's name | `facts` l.1126 (`everyone=True`, about `sky`) | knack "sow" reads tomorrow's sky |
| WILD (613) | 34 | wild | parcel res plants/game/wood/dead/young/seam/quarry S/K; refuge; `was` forest -> scrub; today's events fell / charcoal / quarry,mine; herds on parcel; snow; gale | `facts` l.1129 (every parcel) | `_bare` l.598, `_thin` l.606 (p as a function); `eye`, `land` |
| BUILDING (698) | 47 | buildings (+ fire, fuel, crafts, family, food rot, tiers, works) | b condition, structure camp, lasts_until, fire, warm, fittings (hearth, fire ring, beds), unfinished, built_day, door, tier, monument, works{kind,to,storey}; store stock (timber, firewood, food, heat, rot items); dwellers (beds) and their stages; today's make events by tech and maker; repair/build events | `facts` l.1158-1159 (`inside=live, concerns=live`) | `peek` row l.791; `TIER_LOOK` l.943 |
| PERSON (799) | 27 | people/life (+ herds led, gear, travel, slaughter/hunt blood, guard, slept out, care) | body hunger/wounded/with_child/partner/carried; person stage, arrived, ate_raw, guarded, slept_out, sex; LF.infants_of/days_old/lifespan/elder_from; HD.led_by; parcels' slaughter/hunted kills; children born <=2 days; today care_by; ITEMS seen/camp/weight | `facts` l.1160-1163 (`inside` = household here, `concerns=[who]`) | `bereaved` computed l.1011, read by no row (D4-72 removed) |
| GRAND_AHEAD (959) | 1 | buildings (tiers) x roads | x built in roads._notices: nm, place, LY.tier_words | `roads._notices` l.350 | |
| THING (1199) | 68 | things (+ death/graves, food rot, hiding, dogs) | container: kind, of, body state, cause, buried, cairn, grave{day}, hidden, untaught, goods (seed goods, meat, rot items, food), qty vs THINGS heap thresholds, door, in (indoors), node (on road), age; weather history at it (rained, snowed over, snow laid); dogs | `bundle()` -> perceive.facts l.171-179; roads._notices l.335; roads find l.381 | `reach` near/count; `knows/lay` "hunt" |
| ROAD (1358) | 45 | roads (+ sky) | stretch terrain, landmarks and their challenge state (ford high, bridge down, pass snowed), weather/snow/cold on the road, season, spell, since heavy rain, handcart carried | `roads._notices` l.332 (`roll` with mult 1: **not** the rule) | all legacy p |
| TRACE (1454) | 19 | roads | trace {kind tracks/ruts/ashes, day, n, toward}; weather since | `roads._notices` l.343, `mult=0.3*fade*snow*sight*eye` (**custom chance**, not D4-75) | |
| TRAVELLER (1500) | 10 | roads | others' count, cart, arms, laden, pack ox, infant, toward, weather | `roads._notices` l.358, rule = own x road visibility x eye | |
| NIGHT (1524) | 17 | conflict (fuse raid) | building structure/camp/dog, riders, role watcher/inside/neighbour, weather, snow, by armed | `fuse.py` l.174-175, `roll(..., least=True)` | |
| PASSING (1933) | 10 | roads (meetings, D4-51) | other party names, count, landmark words, fog, armed, cart, laden | `roads.py` l.507-512, `least=True)[:2]` | |

Row-shape eras: older tables (CROP/FIELD/PASTURE/HERD/SKY/WILD/BUILDING/PERSON/THING/ROAD/TRACE/TRAVELLER/NIGHT/PASSING) still carry
legacy `p`; D4-71/74 tables (SLAUGHTER, FIGHT ... BURIAL, DOGS) are pure `own` + `who` + `reach` + `night`, as the guide asks.

### 1.3 Contexts (state -> `x` namespace), each feature-specific

| Context (line) | Builds x for | Feature(s) it reads | Escapes `Here` (`here._w`)? |
|---|---|---|---|
| `context(here, pid, h=None, holder=_MAIN)` (858) | CROP, FIELD, PASTURE, HERD, WILD, TRAMPLED | farm (FM.main_rec, view, named, standing, the_crop, the_part, names_of, started, rate, weed_gain), herds (herds_on, fence), wild (res, r()), sky (cold, weather, snow), events (worked, axes, charcoal, plough, hoe, reap, quarry/mine, sow), today green_cut/turned | via `here.today()` (`hasattr` guard) |
| `building_context(here, bid)` (965) | BUILDING | buildings, fittings (FITTINGS labels), stores (ITEMS food/heat/rot), make events/makers, repair/build events, life stages of dwellers, tiers/monuments | yes l.988 |
| `person_context(here, who)` (1006) | PERSON | body, life (LF), herds (HD.led_by), slaughter/hunted records, guard, slept_out, care_by, ITEMS gear | yes l.1009 |
| `sky_context(here)` (1049) | SKY | calendar, weather/wet/snow per day, climate (CL.on/state/storm_coming), parcels by cover (water, forest) | yes l.1053 |
| `thing_context(w, c)` (1575) | THING | things (TH.*), ITEMS, THINGS thresholds, EV weather at the thing, buildings with dog | engine side (takes w) |
| `herd_context(w, hid)` (1624) | ASTRAY, EMPTY | herds, farm (main_crop, standing), claims, institutions | w |
| `fence_context(w, pid)` (1645) | FENCE | FENCES data, FM.fence_need | w |
| `carcass_context(w, c)` (1678) | CARCASS | TH.carcass_fresh, THINGS carcass_bones_after | w |
| `slaughter_context(here, pid)` (1695) | SLAUGHTER, SLAUGHTER_DOGS | parcel slaughter record, herds, dog fittings | yes |
| `event_context(here, nm, day, **kw)` (1733) | FIGHT..DOGS (all aftermath) | generic: name, age, weather/snow/wet/cold/season + per-bundle kwargs | yes (unused `w`) |
| `road_context(w, name, t, pos)` (1822) | ROAD | roads (RD.stretch, challenge), WEATHER words, EV spell | w |
| `traveller_context(w, others, o, pos)` (1836) | TRAVELLER | roads, ITEMS weight, herds (pack ox), people stage | w |
| `trace_context(w, x)` (1849) | TRACE | roads, weather history | w |
| `night_context(w, e, role)` (1866) | NIGHT | buildings, fuse event | w |
| `passing_context(w, party, other, m, ...)` (1959) | PASSING | roads, LANDMARKS words, ITEMS | w |
| inline in `perceive.evening` (437) | WAY | layout (LY.side_words, opened), roads `way` | w |
| inline in `roads._notices` (347) | GRAND_AHEAD | layout tier_words | w |

### 1.4 How a row becomes a sign: generic machinery vs feature producers

**Generic machinery (core candidates):**
- `true_rows(rows, x)` l.1886: rows whose `when` holds.
- `readable(row, know)` l.1877: `knows`/`lay` gate.
- `bundle(w, c)` l.1898: a container's table by kind (`carcass` -> CARCASS, else THING): a 2-way dispatch.
- `roll(rows, x, rng, mult, know, near, at_node, least, rule)` l.1903: one observer rolls a bundle directly (road, night, way,
  passing): `p x rule(row)` (or `p x mult`); `near` rows only with `near=True`; `count` rows never; `least`: the likeliest true row
  if none came up. `at_node` unused.
- `facts(here, add)` l.1099 with its closure `emit(rows, x, about, parcel, inside, everyone, concerns, only)` l.1107: turns rows into
  facts carrying a `spot` (node, parcel, own, inside, everyone) and keys peek/eye/land/knows/lay/reach/night; sign id from an ad hoc
  `names` dict keyed by `id(table)` l.1105 (sky, wild, crop, field, pasture, herd, building, person).
- `spot_rows(here, rows, x, about, node, parcel, add, concerns, only, who, name, inside, **extra)` l.1662: the newer emitter:
  same as emit but maps `who` to `only`, sets `gate`, passes `**extra` (e.g. `missing`), sign id `<about0>#<name><i>`. Two emitters
  with slightly different key sets (emit: no `who`/`gate`/extra; spot_rows: no peek/eye/land/knows/lay).
- The **noticing rule** itself lives outside the slice: `things.spot_chance` (things.py l.317) and `things.chance` (l.350) with
  `presence` (l.239: per-technique `draws` presence, worked/passed/next door/elsewhere, sound/smell carry by parcel-graph steps,
  night from where one sleeps), `attention` (l.287), `eye` (l.208), `EV.visibility/open_air`; parameters in `data.NOTICING`
  (data.py l.741: presence, next_door_min, elsewhere_min, attention {place, search, close, own house, subject, working}, carry
  {sound, smell}, within {touch:0}, reach {near:0, around:1}, eye_senses, inside, loud, person, theft, sky_weather, eye, eye_bare,
  eye_keen, eye_practice). `perceive.chance_of` l.215 = `salience x knack x spot_chance` (or `TH.chance` for a thing), capped at 1.
- Salience/ordering: `perceive.relevance` l.243 (concerns +1, own house/household +0.5, interests +0.5, hunger&food +0.4,
  person concerns +0.4, danger +0.3) only ORDERS the candidates; the chance is the rule's (D4-75). NOTICE_MAX 5 (+2 when attending
  the place), ATTEND_MAX 9.

**Feature-specific sign producers (every function that calls emit/spot_rows/roll on a table):**

| Producer | Line | Feature | Tables |
|---|---|---|---|
| `facts` (the parcel/herd/building/person/sky walk) | 1099 | mixed: sky, wild, farm, pasture, herds, buildings, people | SKY, WILD, CROP, FIELD, PASTURE, HERD, BUILDING, PERSON (+ hard-coded "X is half built" fact l.1155 for unfinished buildings) |
| `_herds_out` | 1076 | herds (+ fences, trampled crops) | ASTRAY, EMPTY, FENCE, TRAMPLED |
| `_slaughtered` | 1719 | herds (slaughter) + dogs | SLAUGHTER, SLAUGHTER_DOGS |
| `_aftermath` | 1749 | conflict, wild hunting, death, fire, life, buildings, herds | FIGHT, DOGS, HUNTED, BURIAL, FIRE/RAID/THEFT/BROKE (table of (field, rows, most-days) l.1794), BIRTH, GUARD, DRIVEN |
| `perceive.facts` (things loop) | perceive 170 | things, carcass | THING, CARCASS via `bundle` |
| `perceive.evening` (hidden ways) | perceive 435-439 | roads/layout | WAY |
| `roads._notices` | roads 313 | roads, things, buildings | ROAD, THING/CARCASS, TRACE, GRAND_AHEAD, TRAVELLER |
| roads find look | roads 380 | things | THING/CARCASS `near=True` |
| roads passing | roads 507 | roads | PASSING |
| `fuse` detect | fuse 174 | conflict | NIGHT |

Order of emission in `facts`: SKY, then per parcel WILD, CROP (turf), CROP per holding, FIELD (whole or split), PASTURE; HERD per
herd; `_herds_out`; `_slaughtered`; `_aftermath`; per building (unfinished: fixed line, else BUILDING); per person PERSON.

---------------------------------------------------------------------------------------------------------------------------------------

## 2. PERCEPTION (perceive.py)

### 2.1 The store shapes

- **Mind store** `w.s["mind"][name]`, created by `seed` l.40: `days` (list of `{day, did, said, heard, saw, glimpse, saw_day}`,
  appended by `close_day`), `seeded` (spec memories), `lasting` (engine-marked lines, last 14), `own` (append-mode stretch memories,
  last 6, `own_memory` l.639), `beliefs` (`{subject: {day, lines, ids}}`, replaced per day seen), `today` (`_blank` l.31: dawn,
  notice, attended {target, lines}, concerned, glimpse, felt, learned, heard), `log` (ids per day), `kin` (`{name: {rel, lives,
  household, alive, seen, seen_at}}`), `places` (`{node: {name, days, ways, text, seen, buildings, parcels, herds, found?}}`,
  `place_record` l.109). Keys added elsewhere: `beasts` (remember_beasts l.295: `{hid: {name, words, where, day, how}}`), `land`
  (remember_land l.315: `{"pid|what": {day, state, how}}`), `things` (TH.remember), `found`, `landmarks`, `ways` (LY.learn_way),
  `on_the_way` (roads l.851), `read`/`read_changes` (BL.read), `memory` (MEM.keep), `kept` (MEM.kept), `childhood`, `names` (tags),
  `view`/`view_next` (view.py), `evening_shown`, `saw_day`.
- **Person record** keys set here: `notes`, `pinned`, `interests` (from spec interests + TECHNIQUES tags of known crafts) l.44-50.
- **Know** (crafts): `w.s["know"][name]` = `Mind.know` `{tech: {level, skill, source}}` (knowledge.py), read by `knack`, `practised`.

### 2.2 The daily cycle (function, line, what it does)

| Step | Function | Notes |
|---|---|---|
| seeding | `seed` 40; `seed_knowledge` 53 | kin homes; own household's herds (`remember_beasts "known"`); customs -> kept lines (MEM.seed_line); lore (LO.seed); hidden ways known (LY.learn_way); spec `kept`; come of age; places by BFS over roads skipping `unexplored` nodes (D4-47); `describe(NodeView)` |
| a node in one line | `describe(view)` 120 | **feature-aware**: houses/households (beds), covers with game/seam/quarry and standing crops, fittings anvil/cellar, herds (FM.herd_words), born trades (KN.label) |
| all facts at a node | `facts(here)` 151 | (a) per parcel `COVERS[cover]["ambient"]` lines (`ambient=True`); (b) `SG.facts`; (c) things via `SG.bundle`; (d) today's events (except speech) with `at=_event_at` |
| where an event reaches | `_event_at` 193 | `data.EVENT_EXTENT` (node / building / parcel by kind); parcel from about or actor's spot |
| dawn | `dawn(w)` 326 | events with `dawn` flag; concerned & happened to one = full presence, else `chance_of` |
| evening (the "observe") | `evening(w, attend, today, skip)` 351 | per node facts once (`by_node`); per person: **concerned** (events naming one; theft = witnesses only, D4-81) ; **notice** candidates: things (rule; skip known text), spot signs (rule; `only`, peek, readable, `_can_read`, not self), events (not own, not ROUTINE kinds, not low-salience, not about one's home unless event); close look beats glimpse; top NOTICE_MAX; hidden ways (WAY); open gate shut (`_shut_gate` 592); **attend** (resolve_target 602: place -> ambient lines; village -> `here.layout()`; subject -> its facts at attention x subject, heaps counted); **glimpses** of others (NOTICING person own 2.0, where they worked); **felt watched**; **learned by watching** (`KN.saw`, techniques not basic); remember things (TH.remember, close look text); remember own beasts (missing / saw / worked with); remember land; **beliefs** per subject; **acting** (what one worked on, attention x working, top 4 into beliefs); `_update_known`; buildings read (BL.read, writing) |
| knowing by presence | `_update_known` 571 | place record refreshed (`describe(here)`), kin seen, kin death from a `death` event |
| end of day ("close round") | `close_day(w, name, did, night_lines)` 644 | appends `days`; **lasting** by keyword match (l.660: "killed", "died", "beat", "broken into", "taught you", "missed meal", "gave", "missing", "slipped into", "now have a rough idea", "starving", "taken into", "claimed"); clears heard/dawn; `view_next` -> `view` |
| beliefs shown | `beliefs_lines(mind, names, limit=6)` 674 | person:/building: subjects not seen since yesterday, dated |
| notes | `apply_notes` 691 | note/forget/pin (D4-95 fuzzy pin) |
| testimony | not here: run.py appends heard lines into `today["heard"]` (run.py l.261, 280, 297, 334-359: said, told, explained, places and ways and crafts learned by hearsay) |

### 2.3 What each feature contributes to what is seen

| Feature | Route into perception |
|---|---|
| covers | `COVERS[c]["ambient"]` lines (data); `describe` land words |
| farm | CROP, FIELD, TRAMPLED signs; `describe` standing crops; prompt place line crop/shares words |
| pasture | PASTURE signs |
| herds | HERD, ASTRAY, EMPTY, FENCE, DRIVEN, SLAUGHTER signs; `remember_beasts` (mind `beasts`); gate shutting; glimpse via work |
| wild | WILD signs (`land` memory, eye for bare), HUNTED |
| sky | SKY signs (everyone at node), "## Now" weather words |
| buildings | BUILDING signs, FIRE/RAID/THEFT/BROKE, writing read (BL.read), unfinished line |
| people/life | PERSON signs, BIRTH; glimpses; felt watched; kin alive/dead; prompt family lines |
| things | THING/CARCASS bundles via the rule (`TH.chance`), `TH.remember`, "Lying about" |
| conflict | FIGHT, GUARD, THEFT (witness rule), NIGHT (fuse) |
| death | BURIAL, THING body/grave rows, `death` events update kin |
| knowledge | knack/knows/lay gates; learning by watching (`KN.saw`) |
| events (all verbs) | each event's `text/salience/tags/sense/own/dawn/concerns` is a fact by itself (a second channel beside signs) |
| roads | not in `facts`: on the road, `roads._notices` writes "On the way" lines into mind `on_the_way` |

---------------------------------------------------------------------------------------------------------------------------------------

## 3. PROMPT (prompt.py, view.py, views.py)

### 3.1 System prompt: `prompt.system_prompt(here, mind)` l.468 (frozen per conversation)

| # | Block | Source / feature |
|---|---|---|
| 1 | "You are {name}, {stage}, of {household} in {home}. Its head... By trade:" | people/life (stage words hard-coded), household (institutions) |
| 2 | "{home}: {place text}" | `mind.places()[home]["text"]` = perceive.describe (covers, farm, herds, fittings, trades) |
| 3 | "Your people:" + `_kin_lines` 306 | kin store |
| 4 | "How life works here:" bullets, all hard-coded prose with numbers from `here.p`: units by season, youth/elder units, "Any units you do not use are wasted" (generic/labour); ration & stores & hunger (food); food items in meals (ITEMS food/cook/raw/spoil, `PK.on`) and house_spoil (food); fuel as heat, hearth/fire ring/camp/open fire (buildings + fuel); `_labour_lines(p)` 272 (labour: work_food, guard_food, over_units, step, wear of fittings from FITTINGS wear, fade_rate); buildings are what is in them (buildings); what is whose (claims); knowing how (knowledge); what you notice (perception); evening day shape if `setting("evening")` |
| 5 | "Other places, as you know them" (shelter costs, carry capacities, `weights_text` 459) + `_map_lines` 441 | roads, places store, ITEMS weights |
| 6 | "What you know how to do:" `KN.crafts_lines(mind)` | knowledge |
| 7 | "What you can do (each action is a verb...)" `verb_lines(here, mind)` 190 | verbs registry (see 3.4) |
| 8 | `REPLY_LINES` 249 (reply field docs), with an "overwork" line spliced in if labour over_units | generic + labour |

### 3.2 Turn prompt: `prompt.turn_prompt(here, mind, opening)` l.616 (default) — sections in order

| # | Section | Built by | Feature contributing |
|---|---|---|---|
| 0 | (opening only) "## What you remember" (seeded + lasting), "## Kept for good", "## Your memory (in your own words)" or "## Your own memory of recent days" | `_memory_sections` 826 | memory |
| 1 | "## Now" season/day/left, cold, `weather_words`, units, messages, tired | inline 623 | sky, labour |
| 2 | "## What happened yesterday" You did / You said / Heard | `_yesterday_record` 530 | generic (speech) |
| 3 | "## What you saw yesterday" or "## Since last evening" (evening setting): felt, learned, What concerned you, What stood out, You paid close attention to, In passing | `saw_lines` 601 | perception |
| 4 | "## This morning" dawn lines | inline 635 | perception |
| 5 | "## What you read written on buildings yesterday" | `written_lines` 591 | buildings (writing, D2-169) |
| 6 | "## Here": You are at / Here today (`_who` 713: baby/child/near her time); arrived; "On the way:" (roads); "Arriving, what you see first" (`here.overview`, layout); place lines `_place_lines` 347; "Roads from here" (roads, landmarks known, camping food); "Lying about, that you know of" `_things_lines` 765 | farm, herds, buildings, wild, roads, things, layout |
| 7 | "## You": hunger STAGES, hurt, carry, weight/capacity (roads, packs/carts); `here.age_line()` (life); `_family_lines` 720 (life: partner, pregnancy, young fed/cared, care work rules, child keep lines, children's order, succession, heir); "Leading:" (herds, HERDS pack_ox carry); `_beast_lines` 400 (herds, BEASTS_SHOWN 4); `_house_lines` 545 (buildings: condition, door, fire, beds/floor, store, food meals, heat per night via `_heat` 707 -> night.house_heat, woodpile at door via things + FO.heat_of) | life, herds, buildings, fuel, things |
| 8 | "## Your crafts today": `KN.options` can/near; full crafts list if not opening | knowledge |
| 9 | "## Offers open here" `AG.offer_text` | agreements/exchange |
| 10 | "## Agreements (what is owed, as you know it)" `AG.lines` | agreements |
| 11 | "## As you last saw them" `PC.beliefs_lines` | perception |
| 12 | "## Your notes" pinned + titles | notes |
| 13 | "Plan your day. Reply with JSON only." | |

Place line (`_place_lines` 347), per parcel: `- {name} ({ground words; crop/shares words; held by; fence words; here one can ...;
buildings: ...; land memory}): {p.text}. Next to {adj}.` then one `building_line` 377 per finished building.
- `_ground_words` 315: built ground/scrub spaces (BL.ground_total/used); field/pasture/meadow plots (**hard-coded cover names**).
- `_share_words` 330: field -> `FM.crop_words`; `FM.LAND` covers -> `FM.held_words` (farm).
- `_holders` 434: claims (generic).
- `_fence_words` 416: herds/fences ("a wattle fence", "a dry-stone wall", levels 2/1/0, gate).
- "here one can": TECHNIQUES filter on `at.covers`, `draws` in (None, plot, crop) or in parcel res or (herd and herds there),
  `yield.ground`, crew or known level, `PK.on`, `yield.kind == "gate"` with `FM.ready` (generic over TECHNIQUES, but `"herd"`,
  `"plot"`, `"crop"`, `"gate"` are feature words).
- land memory `_land_words` 425 (wild: bare/thin/nothing caught/good, "timber" special case).
- `building_line` 377: monument label & tier words (TIERS, MONUMENTS), structure, room words, storeys, space words, works under way
  (`V._works_words`, a private verbs helper), holders, description quoted (BL.cap_text).

### 3.3 The belief-based morning message: `view.turn(here, mind, opening)` l.165 (world `view: beliefs`, `view.on` l.20)

Same order as 3.2 with differences: falls back to `PR.turn_prompt` on the road; "## Now" (`_now` 29, copy of the inline Now without
"tired"); full message ("## Here, as you see it" `_here` 64: present people capped at PRESENT_MAX 10, place lines from
`PR._place_lines` zipped with subjects and suffixed "(you saw {age}: ...)" from beliefs) only at an opening or a new node, else "## Since
your last morning" `_changes` 121 (people came/went, new belief lines per parcel/building not already told, new buildings, own
house condition/door and store diffs); "## You" `_self` 94 (house and beasts only when full; care instructions only at opening); no
"## Your crafts today" ("No computed choices", docstring); "## As you last saw them" only when full and only for subjects not here.
Snapshot `_snapshot` 108 -> `view_next` (day, node, present, stock, house condition/door/fire, buildings, belief days). It reuses
prompt internals: `PR._place_lines`, `_who`, `_things_lines`, `_family_lines`, `_house_lines`, `_beast_lines`, `_memory_sections`,
`_yesterday_record`, `saw_lines`, `written_lines`, `CONDITION`.

### 3.4 Verb manual and reply schema

- `SCHEMA` l.15: a fixed superset of every action argument across all features (do, what, at, to, item, qty, from, target, aim,
  offer, person, thing, household, name, for, feed, days, lots, agreement, hidden, method, on trouble, stop at, gather, searching,
  meeting, lead, with, units, heir, head, text, pass, structure, how, describe, description, line, storey, room, on, plots) plus
  say/tell/explain/offers/attend/note/pin/forget/open/look_up/memory/keep/drop.
- `schema_for(here, mind)` l.68: enums filled from what the mind knows (`_known` 56: people, buildings, parcels, herds, nodes,
  households): `do` = `V.VERBS` filtered by `V.verb_here` (verb `when`: roads/herds/children/evening) + every FUSE choice/also;
  `on trouble`/`meeting` from TECHNIQUES pseudo-rows; `item` = `PK.items()`; `what` = known techniques (minus MODIFIERS) + "shelter",
  "shelter and food"; modifiers' `hidden`/`method` values; aim rob/hurt (conflict); thing = door + parcels + buildings + herds;
  attend enum; `tags` setting frees names and adds `as`; `fallback` = copy of actions; `overwork` (labour); `when` (evening);
  `_drop_empty_enums` 116.
- `verb_lines(here, mind)` l.190: for each `V.VERB` entry (args, cost, doc with `{crafts}` placeholder): crafts = `_craft_note(t)` 128
  for every known technique of that verb (fittings needed, tools bare/copper multipliers, weapon, build costs from ROOMS / BLUEPRINTS /
  FITTINGS / MONUMENTS with spaces, holds, heavy, monument), cost words from `V.verb_units`; `_verb_extra` 169 (hard-coded: `name`
  with tags, `travel` with evening); `build` special-cased (rooms vs fittings split l.203-209, `_build_more` 219 with SPACE storeys,
  room/upgrade costs for one's own buildings); `MOD.lines` ways (modifiers D2-93).
- Other prompts here: `fuse_prompt` 774 (night/road urgent call: FUSE choices with a hard-coded `words` dict for raid, meeting,
  find, landmark trouble, strays), `meeting_wave_prompt` 812, `road_opening` 846, `talk_prompt` 853, `lighten_prompt` 870 (carry
  limit), `memory_prompt` 884 (append mode).

### 3.5 Feature-specific text hard-coded in prompt code (the `if crop ... if herd ...`)

- prompt.py: stage words l.470; "How life works" bullets l.479-516 (food, fuel/hearth/fire ring/camp, buildings "beds, a hearth, bins,
  a quern, an anvil", claims, crafts, noticing); `_labour_lines`; `_ground_words` covers field/pasture/meadow; `_share_words`
  field/FM.LAND; `_fence_words` wood/stone; `_land_words` timber; "here one can" draws herd/plot/crop and yield gate; build
  special-casing; `_verb_extra` name/travel; `_house_lines` hearth, fire ring, beds, children sharing beds, woodpile; "Leading:"
  pack ox; `_family_lines` care/feeding/keep/order/succession/heir; `fuse_prompt` choice words; `_who` baby/child/near her time;
  roads "Each night on the road you eat ..." camping; tier "grand".
- view.py: the same through reuse, plus "Looking after a child is work"/"While caring for a child" prefix filter l.103 (string match
  on another function's output).
- views.py: none (record reader).

---------------------------------------------------------------------------------------------------------------------------------------

## 4. MEMORY (memory.py; plus perceive.close_day/own_memory, prompt._memory_sections)

- Two modes (`mode_for` l.50): **rewrite** (default; one memory text in `mind.memory`, rewritten each stretch) and **append**
  (weak models by model-id prefix `APPEND_MODELS` (one model family prefix), or world `memory.mode: append`: last 6 `own` stretch memories
  + engine `lasting`).
- Budget (`budget_tokens` l.63): `lo + (hi-lo)(1-e^{-k age/L})/(1-e^{-k})`, DEFAULTS lo 150, hi 800, k 3, words/token 0.75, cap
  1.15; `cut` at a sentence end beyond the cap. `limit()` words text. `PROMPTS` 7 instruction variants (`settings.prompt`,
  default `keep_change`). `request()` l.92 builds the end-of-stretch message; `keep()` l.118 stores `{text, span, day, budget,
  written}`.
- **Kept for good** (D4-64): `KEPT` settings (25 words, childhood 4, per_lifespan 5, schedule evenly/every/none, refill); `kept()`
  store `{lines[{text, source, day, fixed}], start, from, shown, refused}`; `seed_line` (customs, lore, spec), `come_of_age`,
  `places()` (slots over a life via LF.lifespan), `kept_request` (prompt block), `kept_apply` (drop then keep).
- Stretches: converse.py (`chunk` days, staggered per agent by crc32); run.py asks memory at a stretch's last day.
- **Bands/summaries**: there are no generated summaries; "bands" are: seeded (spec) / lasting (engine keyword-marked) / own or
  rewritten memory (agent-written) / kept for good (agent-chosen, word for word) / notes (agent) / beliefs (engine, per subject, last
  day seen) / places & kin (engine, by presence) / beasts & land & things (engine, per feature).
- Generic or feature-aware? memory.py is **generic** except its life dependency (LF.days_old, lifespan, MINOR). Feature awareness
  leaks in via (a) `perceive.close_day` lasting keywords (conflict, death, hunger, theft, knowledge, claims, giving), (b) feature
  stores in the mind (`beasts`, `land`, `things`, `ways`, `landmarks`) each rendered by bespoke prompt code.

---------------------------------------------------------------------------------------------------------------------------------------

## 5. CONVERSE and CHRONICLE

- **converse.py**: `Conversations` (l.18): one LLM conversation per agent per stretch of `chunk` days (`offset` crc32, `starts`,
  `ends`); system prompt and schema frozen per conversation (a changed schema restarts it); `message()` returns a `llm.Turn`
  (cached CLI session, `cybertron2.infra.llm`, lazy import l.20) or a flattened prompt; `after()` keeps the exchange (a failed call
  keeps `{"why": "(no reply)"}`, mirrored by views.NO_REPLY); `end`, `close`. Feature-free. Used only by run.py l.21/830.
- **chronicle.py**: CLI `python -m cybertron2.engine.chronicle <run>`: one HTML page from `run.json`, `turns.jsonl`, `days.jsonl`,
  `memory.jsonl` (cast table, per day dawn lines scraped from the prompt text "## This morning", talk, why, results, prompts in
  expanders, memories, night summary). **Not imported anywhere in Python** (grep: no importers; only docs: spec/record/views.md l.24,
  proposals/run_record.md). run.py still writes those jsonl files (run.py l.829), so it works, but it parses prompt text by section
  headers ("## Now", "## This morning"), so renaming a section breaks it silently.
- **views.py** (record views, D1-1/2/4): `steps`, `state`, `last_step`, `beliefs(run, agent)` (mind + know), `context(run, key)`
  (exact system/schema/turns/message rebuilt from the journal), `raw_reply`, `requests`, `events`, `changes`, `calls`, `layout`
  (Fruchterman-Reingold of the road graph; parcels by `side`), `frames`. Feature-free except it knows people/transit/roads/
  institutions shape. Used by run.py CLI l.1282-1299, api.py, exchange.py, tests.

---------------------------------------------------------------------------------------------------------------------------------------

## 6. EXTENSION POINTS (dispatch, kind chains, hard-coded names, lazy imports)

### 6.1 Dispatch dicts / registries
- signs.facts `names = {id(SKY): "sky", ...}` l.1105: table -> sign-id label (keyed on object identity).
- signs `_aftermath` tuple `(("fire_hit", FIRE, 3), ("raided", RAID, 1), ("theft", THEFT, 1), ("broke", BROKE, 2))` l.1794: building
  record field -> bundle -> lingering days. The nearest thing to a registry; parcels/people/herds equivalents are hand-written blocks.
- `bundle(w, c)` l.1898: container kind -> table (carcass vs everything else).
- `TIER_LOOK` l.943 (tier x look), `x.look` map l.1001 (monument -> look key).
- `data.EVENT_EXTENT` (event kind -> node/building), `data.COVERS[*]["ambient"]`, `data.NOTICING`.
- `perceive.LAND_DRAWS` l.292 (technique draws -> land word; used by verbs.py l.442/586).
- `perceive.resolve_target` l.602: attend target string -> subject (village/place/sky words lists, person, building, parcel, herd,
  tagged thing).
- prompt `schema_for` fills enums from V.VERBS/FUSE/TECHNIQUES/PK; `verb_lines` iterates `V.VERB` (the verb registry, D4-24);
  `fuse_prompt.words` l.783-796 (choice -> words); `_verb_extra` (verb name -> extra args/doc).
- memory `PROMPTS` (variant -> instruction).

### 6.2 if/elif on a kind (and string matches)
- signs.facts: `p["cover"] != "field" and p.get("crop")`, `== "field"`, `FM.named(p)`, `cover in ("pasture","meadow") or "grass" in
  res or dung > 5`, `b.get("unfinished")` l.1130-1157.
- signs.context: `par["cover"] == "field"` l.861/894; `FM.named(par)` l.882.
- signs.building_context: `structure == "camp"`, fittings hearth/fire ring/beds/dog; monument look map.
- signs._aftermath: parcel fields `fight`, `hunted`; events `work` + tech `bury`; `birth`; person `guarded`; herd `driven`.
- perceive.facts: `e["kind"] == "speech"` skip; perceive.evening: `kind == "theft"` (witness-only) l.379/413, `ROUTINE` kinds l.24/425,
  `kind == "work"` (learning, presence), `sense != "smell"` for remembering things, `about` prefix `herd:` for beasts, `death` in
  `_update_known`.
- perceive.relevance: tag `food` with hunger, tag `danger`.
- perceive.close_day: 13 keyword substrings -> lasting l.660.
- prompt: `v == "build"` (l.141, 203, 214), `v == "name"`/`"travel"` (169-181), cover words l.322/325, `p["cover"] == "field"` l.336,
  `in FM.LAND` l.340, draws `herd/plot/crop`, yield `gate` l.353-356, `b.get("monument")`, `structure == "camp"`, tier `grand`,
  fittings hearth/fire ring/beds, stage infant/child, `"meeting" in kinds` (fuse_prompt l.803), `here.node is None` (road).
- view.py: string prefix filter on family lines l.103.

### 6.3 Hard-coded feature names in this layer (selection, exhaustive by category)
covers (field, pasture, meadow, built, scrub, water, forest), resources (grass, dung, plants, game, wood, dead, young, seam, quarry,
fish), crops (legumes, barley via CROPS kind; "needs_winter"), techniques (reap, sow, weed, hoe, plough, herd, hay, milk, fence,
forage, hunt, fell, firewood, mine, quarry, charcoal, repair, bury, care), items (grain, rye, beans, flour, bread, wild food, meat,
hide, timber, firewood, handcart, crude weapon, crude tool, wooden plough, tent, bedroll, pack, harness, smelt, copper tool, coin, oven
bread, cheese, dry meat, water mill), fittings (beds, hearth, fire ring, dog, anvil, cellar), structures (camp, wattle, timber, stone),
monuments (carved post, standing stone, cairn), herd fields (cows, bulls, young, births, in_milk, hungry, watched, milked, last_calf,
with, pack, split_of, strayed_in, base_name, driven), record fields on parcels/buildings/people (slaughter, hunted, fight, fire_hit,
raided, theft, broke, guarded, slept_out, ate_raw, arrived, with_child, partner, care_by, green_cut, turned, dead, works, fence,
trampled), weather words (rain, heavy rain, gale, fog, snow, clear), seasons, landmarks (ford, bridge, pass, narrows, spring, fruit
trees, meadow, hollow), terrains, event kinds (work, make, build, birth, speech, theft, death), FUSE choices.

### 6.4 Function-level (lazy) imports and why
| Where | Import | Why |
|---|---|---|
| signs.py l.870, 971, 1021, 1052, 1576, 1680, 1698, 1735, 1823, 1838, 1850, 1867, 1960 | `environment as EV` | habit (environment imports no slice module); in several (context, building_context, person_context, slaughter_context, event_context) EV is **unused** (Here gives weather) |
| signs l.966, 979, 1007, 1577, 1646, 1681, 1824, 1839, 1961 | `data` FITTINGS/ITEMS/THINGS/FENCES/WEATHER/LANDMARKS | style (data is cheap); could be top-level |
| signs l.1015 | `herds as HD, life as LF` | habit: life imports only data; herds not checked; no top-level cycle found |
| signs l.1045, 1061 | `climate as CL` | optional climate system (CL.on) |
| signs l.1103, 1576, 1680, 1781 | `things as TH` | habit: things imports only environment/knowledge/data at top (it lazily imports night, layout) |
| signs l.1823, 1838, 1850, 1960 | `roads as RD` | roads lazily imports signs and perceive (`_notices`); both sides lazy, so a mutual dependency, not a hard cycle |
| perceive l.55 | `here.NodeView` | engine-side view; avoids top import |
| perceive l.72, 78, 84 | `life, memory`, `lore`, `layout` | seeding only; memory lazily imports perceive (mutual); layout imports only data (habit) |
| perceive l.168 | `signs` (already imported at top l.16: redundant) | leftover |
| perceive l.170, 196, 220, 288, 342, 374 | `things` | habit (no cycle at top level) |
| perceive l.197 | `data.EVENT_EXTENT` | style |
| perceive l.298 | `farm` (already top-level FM: redundant) | leftover |
| perceive l.435 | `layout` | habit (layout imports only data) |
| perceive l.558 | `buildings` | writing read (D2-169) |
| perceive l.626 | `tags` | optional tags setting (D4-68) |
| prompt l.71, 461 | `packs` (already top-level PK: redundant) | leftover |
| prompt l.274 | `data.FITTINGS` (already top-level: redundant) | leftover |
| prompt l.709 | `night as N` | habit/weight (night imports life, needs at top; no cycle) |
| memory l.94, 120, 147 | `perceive` | mutual with perceive (perceive lazily imports memory in seed_knowledge) |
| converse l.20 | `cybertron2.infra.llm` | heavy optional backend |
| here.py (Here/Mind __init__) | `packs`, `memory` | packs CURRENT global set on every view |

---------------------------------------------------------------------------------------------------------------------------------------

## 7. What each feature folder would need to REGISTER with the perception/prompt layer

Generic registration surface implied by the code: (a) **sign tables** (rows) + a **context builder** + an **emitter** (which subjects
to walk, about keys, spot parcel, `inside`, `concerns`, `who` scope map, lingering window); (b) **thing kinds** -> table (bundle);
(c) **event kinds** with extent (EVENT_EXTENT), dawn flag, routine flag, witness-only flag, lasting keywords; (d) **ambient lines** per
cover; (e) **mind stores** + how they are updated from noticed facts (`land`, `missing`, `gate`, herd subjects) + their prompt
rendering; (f) **prompt contributions** per section (system "How life works" bullets with parameters, "## Here" place-line bits,
building-line bits, "## You" lines, extra sections); (g) **schema/verb** pieces (verb docs, args, enums, `_verb_extra`, fuse choice
words); (h) **attend targets**; (i) **noticing parameters** (presence by technique `draws`, NOTICING keys); (j) **state words** at
each resolution (data words, FM.*_words, TH.goods_est/count/words, BL.space_words...).

| Feature | Sign rows + producer | Prompt sections/lines | Mind stores / memory | Noticing params & words |
|---|---|---|---|---|
| **farm** | CROP, FIELD (+ HOLDING_ROWS split), TRAMPLED; producer = the field walk in `facts` (per holding via FM.standing/records/plots_of) + `context()` crop/soil/works part | place line: crop words & shares (`FM.crop_words`, `held_words`), "here one can" (plot/crop draws, gate yield, FM.ready); system: none specific; `describe`: standing crops | (none; crop signs land in `beliefs[parcel:]`) | knacks sow/reap/weed; presence draws "plot"/"crop" -> "work"; words: FM.the_crop, the_part, names_of, herd_words; COVERS field ambient |
| **pasture** | PASTURE; producer = cover/grass/dung test in `facts` | `_ground_words` plots; "here one can" (hay) | — | knack herd/hay; COVERS pasture/meadow ambient |
| **herds** | HERD (facts per herd), ASTRAY/EMPTY/FENCE (`_herds_out`), DRIVEN (`_aftermath`), SLAUGHTER(+DOGS) (`_slaughtered`), PERSON rows `led`, `bloodied`; context bits in `context()` (herds_on, adj_crop, fenced) | "## You" "Leading:" (pack ox carry), `_beast_lines`; place line `_fence_words`; "here one can" draws herd; schema thing enum includes herds; attend herds; verb `when: herds` | `beasts` store (remember_beasts known/saw/with/missing) and `missing` fact key; `gate` fact key -> `_shut_gate` (an act in perception!) | NOTICING presence "herd" 0.5; words FM.herd_words, FENCES words |
| **wild** | WILD (facts per parcel), HUNTED (`_aftermath`); eye/land keys | place line land memory (`_land_words`); `describe` game/seam/quarry | `land` store (remember_land; also written by verbs via LAND_DRAWS) | eye_bare, eye_practice (hunt, forage), presence game 1.0 plants 0.7; `_bare` uses `p["refuge"]` |
| **sky/climate** | SKY (facts, `everyone=True`, about `sky`) | "## Now" weather words, cold; attend "the sky" | — | `sky_weather` flag; climate values via `here.weather_values` |
| **buildings** | BUILDING (facts per building; unfinished fixed line), FIRE/RAID/THEFT/BROKE via the `_aftermath` field table, GRAND_AHEAD (roads) | system bullets (buildings, fuel, hearth/ring/camp), `_house_lines`, `building_line`, `_ground_words` spaces, verb `build` manual (`_craft_note` ROOMS/BLUEPRINTS/FITTINGS/MONUMENTS, `_build_more`), `written_lines`, view `_changes` house/store diffs | `read` (BL.read), `home_seen` on person, view snapshot stock/house | `peek` rows; attention "own house" 3; TIER_LOOK; BL.space_words, room_words, cap_text |
| **people/life** | PERSON (facts per person; `inside` household), BIRTH, GUARD (person) | identity line (stage), `_who`, `here.age_line`, `_family_lines`, kin lines, succession/heir | kin store, `kept` lines (children), lore | NOTICING person 2.0 (glimpses), felt watched (`p.felt_watched`, `p.glimpse`) |
| **things** | THING via `bundle`, emitted in `perceive.facts` (things loop) and roads | "Lying about, that you know of" (`_things_lines`, last 8), attend thing by tag | `things` store (TH.remember: texts, close look) | TH.own, hidden_factor, heap thresholds (THINGS), attention own house, `count` reach |
| **carcass** | CARCASS via `bundle` | (through "Lying about") | things store | THINGS carcass_bones_after |
| **death/burial** | BURIAL (`_aftermath`), THING body/grave rows | kin "(dead, as you know)" | kin alive via `death` event; lasting keywords died/killed | — |
| **conflict** | FIGHT+DOGS, RAID, THEFT, GUARD (`_aftermath`), NIGHT (fuse) | `fuse_prompt` (choices & words), schema aim rob/hurt, FUSE choices in `do` enum | lasting keywords beat/broken into/slipped into | theft witness-only path (`kind == "theft"`), NOTICING theft 0.4 |
| **fire** | FIRE | — | — | own 3 (own light) |
| **dogs** | SLAUGHTER_DOGS, DOGS, NIGHT dog rows, CARCASS/THING dog rows | — | — | fitting `dog` presence |
| **crafts/make** | BUILDING rows on `made` (bread, grind, smelt, cheese, weapon, hides...) | verb `make` manual; "Your crafts today" | — | event kind make extent building |
| **knowledge** | knack/knows/lay on rows of every feature | "What you know how to do", crafts today, `explain`/`look_up` enums | `know`; learned lines (`KN.saw`) | `practised`, `knack` |
| **roads** | ROAD, TRACE, TRAVELLER, PASSING, GRAND_AHEAD, WAY (hidden ways) | "Other places", `_map_lines`, "Roads from here" (landmarks known, camping), "On the way", "Arriving", fuse road choices, `road_opening`, `lighten_prompt` | places, ways, landmarks, on_the_way, found | TERRAIN sight/sound; road rule in `roads._notices`; TRACE custom multiplier |
| **agreements/exchange** | — | "## Offers open here", "## Agreements", schema offers, `talk_prompt` offers | agreements store | — |
| **labour** | — | `_labour_lines`, overwork reply line & schema, "worn out" in Now | — | — |
| **memory** | — | `_memory_sections`, `memory_prompt`/`MEM.request`, `kept_request` | memory, own, lasting, kept, seeded | — |
| **tags (D4-68)** | (tag shown in `at` words of things/carcasses) | schema frees names, `as`, `name` verb extra; `TG.render` rewrites every message | `names` | — |
| **evening (D4-65)** | (skip set `day_seen`, D4-82) | "## Since last evening", system day-shape bullet, `travel when`, evening.py prompts | evening_shown, saw_day | — |

---------------------------------------------------------------------------------------------------------------------------------------

## 8. Couplings that would be awkward to split

1. **`signs.facts` is a monolithic walker** (l.1099-1163) mixing eight features with cover tests, holdings logic and a hard-coded
   "half built" line; its sign ids depend on `id(table)` and FIELD's split on positional `HOLDING_ROWS = range(3, 10)` (reordering FIELD
   rows silently changes which rows are per-holding).
2. **`signs.context()` is a shared mega-context** (l.858-940) for CROP, FIELD, PASTURE, HERD, WILD and TRAMPLED: farm, herds,
   fences, wild resources and today's events all computed for every parcel; HERD rows read `adj_crop`/`fenced` (farm x herds),
   FIELD reads `herds_on`, WILD reads `herds_on` and `snow`. Splitting needs a context composed from per-feature contributions.
3. **Cross-feature rows** inside one table: PERSON (bloodied from herds' slaughter + wild hunting, led beast, gear from ITEMS, guard,
   care, childbed); BUILDING (crafts' `made`, food rot, fuel, tiers, works, family dwellers); THING (food rot, seed goods, graves,
   hiding with hunt technique, dogs); CARCASS (herds + wild); SKY (knack `sow`, a water parcel by cover). A feature folder cannot own
   "its" table without others adding rows to it.
4. **Two emitters and one roller with different key sets** (`emit` vs `spot_rows` vs `roll`), and two chance regimes: facts at a node
   go through `perceive.chance_of` (the D4-75 rule), but `roll` callers pass ad hoc chances: ROAD with `mult=1`, TRACE with
   `0.3*fade*snow*sight*eye`, NIGHT/PASSING/WAY with `least=True`. The "one rule" is not one code path on the road.
5. **Perception performs acts**: `_shut_gate` (perceive l.592) applies a primitive from inside the noticing step; `remember_beasts`
   and `remember_land` write feature stores from noticed facts by inspecting `about` prefixes and special keys (`missing`, `land`,
   `gate`). Each is a feature hook buried in the generic evening loop.
6. **Event-kind special cases in the generic loop**: `theft` (witness-only, D4-81), `speech` skipped, `ROUTINE` kinds, `death` updating
   kin, `work` for learning and presence (`TH._presence_here` uses TECHNIQUES `draws` -> NOTICING presence).
7. **Lasting memory by keyword substring** (perceive l.660): features influence memory through English words in result lines.
8. **Agent-facing isolation is only enforced for prompt.py** (tests/test_cybertron2_engine.py l.39 checks KN, AG, V, PR for `.s` /
   `._w`); signs.py (`here._w` 9 times) and perceive.py (6 times) reach through `Here` freely, and most sign contexts take `w`
   directly. A core that wants features to see only Here/Mind needs a richer Here or an explicit engine-side sign API.
9. **view.py depends on prompt.py private helpers** (`_place_lines`, `_house_lines`, `_family_lines`, `_beast_lines`, `_things_lines`,
   `_who`, `_memory_sections`, `_yesterday_record`) and on the exact order of `_place_lines` output (zipped with a subject list built
   separately, l.56-58: one line per parcel then per finished building; any feature adding a line there breaks the zip). It filters
   family lines by English prefix (l.103). "## Now", "Roads from here" and "## Your notes" are duplicated in both files.
10. **prompt.py uses a private verbs helper** (`V._works_words`) and night's heat rule (`N.house_heat`), forests (`FO.heat_of`,
    `fuel_words`), buildings (BL.*), farm (FM.*), modifiers (MOD.lines): the prompt is a hub importing ~10 feature modules at top level.
11. **System prompt rules are prose with numbers** from `here.p` keys of many features (units, ration, heat, labour, shelter, carry,
    camping): each feature's bullet would need registration with ordering, plus the frozen-system-prompt constraint (converse.py:
    system and schema fixed per conversation; changing schema restarts it, so registration must be deterministic per world).
12. **Schema is a fixed superset** (SCHEMA l.15) of every feature's action args; enums are filled from several registries (V.VERBS,
    FUSE, TECHNIQUES pseudo-rows "on trouble"/"meeting", MODIFIERS, PK). Features would contribute properties and enum sources.
13. **Packs (D4-103) already exist** as a data-row switch (`pack` key; `PK.on`, `PK.items`, `PK.techniques`, a module-global CURRENT set
    by every Here/Mind construction). Signs and prompt prose are not pack-gated (only lists of items/techniques are), so turning a pack
    off leaves its sign rows and bullets live unless their `when` happens to fail.
14. **Lazy imports as a habit, plus two mutual dependencies** (signs <-> roads, perceive <-> memory, each side importing the other
    inside functions). Most other lazy imports are not forced by a cycle. A package registry would invert the direction (features
    import core; core never imports features), which removes the need.
15. **chronicle.py parses prompt text by section headers** (l.78-81) and reads legacy jsonl logs; renaming sections per feature breaks it.
16. **Dead or vestigial items** to drop in a redesign: `perceive.SALIENT`, `WORDS_STAGE`, `_amount` (dup of signs `_amt`), fact `skill`
    (never set, so `_can_read` is always true), EMPTY `holders` key, `person_context.bereaved`, `sky_context.wood`, `roll(at_node=)`,
    redundant lazy re-imports (perceive l.168, l.298; prompt l.71, 274, 461), unused `EV` imports in several contexts.

*Sources read: the eight slice files in full; here.py (Here/Mind), things.py l.195-365 (the rule), data.py NOTICING/EVENT_EXTENT,
packs.py, verbs.py VERB/verb_here, roads.py l.312-360, tests/test_cybertron2_engine.py l.39, docs/cybertron2/guides/senses.md.*
