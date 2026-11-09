# The world record's shape and its version

## Summary

The world record (`World.s`) has a version, `world_schema`.
- It is stored in every world, and so in every checkpoint of the journal.
- It is stored in the journal's meta.
- `cybertron2/engine/schema.py` declares the shape that version means: the top-level keys, the keys of the day's record, and the
  fields each record in each table may hold.
- Any change to that shape bumps the version and adds a line below.

Readers (views, c2viz, analyses) can then tell which shape a checkpoint has without reading the engine's code at that commit.

## Decided

- D4-100: the world record's shape is declared and versioned:
  - the number is in every world and in the journal's meta;
  - every change to the shape bumps it and is written here;
  - a test fails on a field the declared shape does not list, or on the declared shape changing without the version.

## Mechanics

- **The number.** `schema.WORLD_SCHEMA` is set in `World.__init__` as `s["world_schema"]`, and by `journal.start` as meta
  `world_schema`. Runs from before 4 Nov 2026 have none; they are version 0, read by their code version (the journal's
  `provenance`).
- **What counts as a change:** a field added, renamed or removed, or a field's meaning or units changed, in:
  - any table's records (nodes, roads, parcels, buildings, herds, containers, people, institutions, claims, offers, agreements);
  - the top-level keys;
  - the day's record (`today`).
- **The rule.** One commit does all of these:
  - edits `schema.py` (`TOP`, `TODAY`, `FIELDS`);
  - bumps `WORLD_SCHEMA`;
  - adds the new version's fingerprint to `FINGERPRINTS`;
  - writes a line under "Versions".
- **The checks** (`tests/test_cybertron2_schema.py`):
  - the declared shape's fingerprint must match the current version;
  - a bot run of five worlds (valley, Combe, Wenbridge, the harm and food probes) must hold only declared fields at every
    checkpoint, and carry the version.
- **Not covered here.** Each person's `mind` and `know` stores are versioned with the memory and knowledge code, not here.

## Data: version 5 (9 Nov 2026, on the ecology branch; D2-199)

As version 4, and:
- top level `wild`: the wild layer's state (proposals/wild_layer.md), held only by a world with the `wild` pack: `land` (the land
  summary the generator writes: areas, links, rivers' flow, each node's home area) and the populations and groups the ecology step
  keeps; changed only by the `set_wild` primitive;
- `parcels` gain `ecosystem` (what grows there, from the generator), kept only with the `wild` pack.

## Data: version 4 (8 Nov 2026)

Top level: `acts`, `agreements`, `buildings`, `claims`, `containers`, `day`, `events`, `fuse_calls`, `herds`, `institutions`, `know`, `left`, `life`, `log`, `mind`, `nodes`, `offers`, `parcels`, `people`, `roads`, `seq`, `tag_seq`, `today`, `traces`, `world_schema`.

The day's record (`today`): `_departed`, `_floor`, `admits`, `awake`, `care`, `care_by`, `care_gift`, `children_work`, `day_seen`, `drawn`, `fights`, `fire`, `fled`, `fuse`, `green_cut`, `guards`, `heard`, `joins`, `learn`, `left`, `memory_done`, `partner`, `partners`, `road`, `route`, `skipped_morning`, `sleep`, `soaked`, `teach`, `thefts`, `travel`, `travel_choices`, `travel_morning`, `try`, `turned`, `units`, `watch`, `worked`.

| Table | Fields a record may hold |
|---|---|
| `nodes` | `name`, `text`, `unexplored` |
| `roads` | `a`, `b`, `days`, `ends`, `stretches`, `terrain`, `track`, `way` |
| `parcels` | `adj`, `broken`, `clearing`, `clearing_built`, `cover`, `crop`, `dead`, `fallow_since`, `fence`, `fertility`, `fight`, `ground`, `height`, `held_whole`, `hunted`, `land`, `last_crop`, `last_kind`, `meeting`, `name`, `node`, `res`, `shares`, `side`, `size`, `slaughter`, `text`, `was`, `works` |
| `buildings` | `broke`, `built_day`, `changes`, `condition`, `description`, `door`, `fire`, `fire_hit`, `fire_out`, `fitting_work`, `fittings`, `lasts_until`, `lines`, `mending`, `monument`, `name`, `node`, `parcel`, `raided`, `rooms`, `size`, `stock`, `structure`, `theft`, `tier`, `unfinished`, `warm`, `works`, `worn` |
| `herds` | `ate`, `base_name`, `births`, `bulls`, `count`, `cows`, `driven`, `gone`, `herders`, `home`, `hungry`, `in_milk`, `kind`, `last_calf`, `lost`, `milked`, `name`, `node`, `oxen`, `pack`, `parcel`, `pos`, `split_day`, `split_of`, `strayed_in`, `tag`, `watched`, `with`, `young` |
| `containers` | `beast`, `body`, `buried`, `by`, `cairn`, `cairn_by`, `cairn_day`, `cause`, `day`, `died`, `door`, `goods`, `grave`, `hidden`, `holders`, `in`, `kind`, `node`, `of`, `on_road`, `parcel`, `rot`, `stretch`, `tag`, `thing`, `untaught`, `wear` |
| `people` | `aim`, `alive`, `arrived`, `arrived_by`, `at`, `ate_raw`, `attack`, `born`, `born_line`, `came_from`, `cared`, `cause`, `concerns`, `defence`, `died`, `father`, `frailty`, `gap_until`, `guarded`, `hands`, `home_seen`, `hunger`, `interests`, `messages`, `missed`, `model`, `notes`, `order`, `parents`, `partner`, `pinned`, `plan_next`, `pregnant`, `relations`, `role`, `sex`, `slept_out`, `stage`, `tired`, `trade`, `transit`, `walked`, `widowed_of`, `wounded` |
| `institutions` | `heir`, `kind`, `members`, `name`, `offices`, `order`, `rules`, `succession` |
| `claims` | `by`, `claimant`, `grounds`, `joint`, `of`, `over`, `plots`, `rights`, `since`, `thing`, `until` |
| `offers` | `by`, `closed`, `for`, `get`, `give`, `lots`, `node`, `open`, `taken`, `to`, `until` |
| `agreements` | `day`, `legs`, `made_by`, `node`, `offer`, `parties`, `seeded`, `status`, `witnesses` |

## Versions

| Version | Date | What changed | Decision |
|---|---|---|---|
| 1 | 4 Nov 2026 | First declared shape (above): the fields of every record as the engine stood after D4-99 | D4-100 |
| 1 (added within) | 7 Nov 2026 | A resource record (`parcels.res.<key>`) may carry `run_K`, `run_r`, `run_seasons` (the periodic renewal rule); new resource keys `fish` and `salt` (the water pack). Optional: absent means none; no older world holds them. Resource records' own fields are not yet in the declared shape: phase 2's version 2 declares them | D4-103 |
| 1 (added within) | 7 Nov 2026 | A resource record may also carry `renewal` (a renewal rule's name, overriding its resource's) and `response` (a number or a name: the take's answer to density); a world may name `packs: [...]` (`systems: [...]` read the same way). Optional; absent means the resource's defaults | D4-104 |
| 2 | 8 Nov 2026 | Phase 2 of the engine overhaul (labour): `today.units` (each one's units worked and pushed on, for the night's food); `people.tired` ({day, units}: units off that day, from pushing on and the walk) and `people.walked` (the walk carried, under a unit); `buildings.worn` ({fitting: {used, since}}: wear). A `know` record may carry `practised` (the day a craft was last done, for its fading) and `peak` (its best skill, D4-105); a crop record `cause` ("season": sown out of its window, D4-105). All absent where PHYSICS labour is at zero | D4-103 |
| 3 | 8 Nov 2026 | Crops grow by the season (D4-106): `today.green_cut` and `today.turned` (a crop reaped green, turned under: for their signs); `parcels.dead` (a crop the cold killed, standing until the ground is worked). A crop record (`parcels.crop`, a holding's `crop`) may carry `g`, `progress`, `q`, `n`, `lying`, `stand`, `wintered`, `winter_n`, `stalled`, `no_winter`, `quality`, `never`, `up_day`, `frost_day`; a crop record without `progress` is read as growing at the full rate toward its `ripe_day` | D4-106 |
| 4 | 8 Nov 2026 | `parcels.land`: the land's fixed properties, from the spec's `land:` block (D4-112). As built it is read for `base_fertility` (default 1.0) only; absent in every older world | D4-112 |

**Before version 1 (version 0).** Runs from 24 Oct to 4 Nov have a journal but no number. These are the known changes to the
shape in that time, reconstructed from the decisions. The list is incomplete; the git history of `cybertron2/engine/` is the
authority.

| Change | Decision |
|---|---|
| `today.route`, the day's chain of parcels. Runs before it have none; c2viz derives `routes_derived` | D4-62 |
| buildings in spaces: `rooms [{kind, floor, storey}]`, `size`, fittings by floor | D2-154, D2-155 |
| clearing land: parcels `clearing`, `was`; clearing for building: `clearing_built` | D4-60, 02zh §8 |
| tags: herds and containers `tag`, top-level `tag_seq` | D4-68 |
| events at their spot, for their signs: parcels `fight`, `hunted`, `slaughter`, `meeting`; buildings `fire_hit`, `raided`, `theft`, `broke`; herds `driven` | D4-71, D4-74 |
| herds wandering, splitting and on roads: `with`, `pack`, `pos`, `strayed_in`, `split_of`, `split_day`, `lost`, `gone` | D2-117 to D2-132 |
| plot shares: parcels `shares`; claims `plots` | D2-163, D2-172 |
| a death the survivor has not learned of: people `widowed_of` | D4-88 |
| goods at a door stay the house's: containers `door` | D4-89 |
| a begun fitting shown on its building: buildings `fitting_work` | D4-91 |
| what an act drew from the stores: `today.drawn` | D4-96 |
| graves dug over days and cairns after burial: containers `grave`, `cairn_day`, `cairn_by` | D4-99 |

## What readers should do

- Read `world_schema` from the checkpoint, or 0 if absent.
- A reader that needs a field added after the run's version must treat it as absent.
- An upgrade chain, so that readers always see the current shape, is proposed in proposals/run_data_interface.md.

## Sources

proposals/run_data_interface.md; cybertron2/engine/schema.py; spec/record/journal.md (the journal's own `schema`, which versions
its tables, not the world inside them).

*Current as of 8 Nov 2026: D4-100, D4-103 (version 2), D4-104, D4-106 (version 3), D4-112 (version 4).*
