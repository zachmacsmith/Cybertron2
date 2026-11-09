# Carcasses, decay and what comes to them

**Status:** accepted: D2-205, D2-207 (9 Nov); to be built after brief 2's gate. **Build brief 3 of 3** for the wild layer's core:
stage 4 and pack K2 (docs/review/37_growth/02zv_wild_consolidation.md C9, C10, K2, as corrected against the engine by
02zw_wild_engine_comparison.md). It starts after brief 2 ([wild_raiders_and_works.md](wild_raiders_and_works.md)) has passed its
gate.
**Owner:** 37.2 (author; the wild pack's data and `engine/wild.py`, D2-199). Touches in 37.4's files (§6: `night.py`'s rot of a
carcass's meat, `data.py` THINGS and ITEMS, `verbs.py`'s burial and slaughter yields, `signs.py`'s carcass context) need 37.4's
agreement on the board.
**Affects:** spec/environment/wildlife.md; spec/world/things_in_places.md (carcasses); on branch `ecology`: `engine/wild.py`
(`_targets`, `_raid`, `_groups`), `engine/night.py`, `engine/things.py`, `engine/signs.py`, `engine/verbs.py` (`_bury`, slaughter),
`engine/data.py` (THINGS, ITEMS, TECHNIQUES), `wild/kinds.py`, `wild/ecology.py` (the carrion pool).

## Summary

The engine already leaves a carcass where a beast dies (D4-52): a thing at a parcel with meat and a hide, fresh for a day, its meat
then turning to rotting meat (`night.py`), bones after six days, conspicuous by age and read by its cause; people's bodies lie where
they die (D2-4) and are buried by units of digging (D2-96, D4-99); the ecology has a carrion pool per area that carrion eaters eat.
What is missing is the link: **nothing comes to a carcass**. This brief makes a carcass at a parcel **food for the wild kinds**
through the machinery that already exists (target rows and raids for the groups; the area's carrion pool for the rest), so that
what people do with a dead beast or a body matters: leave it and it draws foxes, ravens and wolves, which then take what is near;
butcher it promptly, burn it or bury it deep and they do not come. It also adds **tallow** from a carcass and a slaughter, and a
**tallow light**, answering the lantern one-off (02zq).

## 1. For the builder

**This file holds for this stage.** Read: briefs 1 and 2 and their tests; 02zw §1 (C9, C10); 02zu Part D (the natural history of
decay and scavenging, as background only: its timings are replaced by §2 here); on branch `ecology`: `engine/things.py`
(`leave_carcass`, `at_node`, carcass fields), `engine/night.py` (the spoilage loop: a carcass's meat to rotting meat), `engine/data.py`
THINGS (`carcass_fresh_days`, `carcass_bones_after`, `body_days`, `rot_after`, `carcass_meat`, `hidden`), `engine/signs.py`
(`carcass_context`, ravens over carrion: `RAVENS_OVER`), `engine/verbs.py` (`_bury`, `units_by: bury`, `grave_left`; slaughter's
`gives`), `engine/wild.py` (`_targets`, `_raid`, `_groups`), `wild/ecology.py` (`carrion`), `docs/cybertron2/guides/senses.md`.
**Do not** add a decay system beside the existing ages; name kinds in rule code; seed customs about the dead; cap signs. Dry runs only.
**Branch:** `ecology-carcass`, from brief 2's branch.

## 2. Stages on the day's clock, sized by the beast

Today a carcass is fresh 1 day, then its meat becomes rotting meat, bones from day 6, for every beast. Keep the stages and their
signs; size them by the beast (THINGS, `calibrate`):

| Size | Beasts | Fresh | Rotting meat lasts (no scavengers) | Bones lie |
|---|---|---|---|---|
| small | hen, hare, a fox, a gut pile from a kill | 1 day | 2 days | a season (a few feathers or bones) |
| medium | calf, pig, deer, a person's body (`body_days` as now) | 1 day | to about day 6 | about a season |
| large | cow, ox, horse | 1 to 2 days | to about day 10 | one to two seasons |

- **Weather:** the rot (rotting meat lost to decay each night) runs about 1.5 times faster in summer and half as fast in winter;
  **frost stalls it** (no loss on a frozen night: the climate's frost, D4-109); a carcass in the snow keeps.
- **What decays** is the rotting meat's mass, by a rate a night from the size row. What scavengers eat comes off the same mass (§3).
  When it is gone, the carcass is bones (its signs as now).

## 3. What comes to a carcass

**Groups (the raiders' machinery).** A target row may name `what: carcass` (new in `_targets`: carcass things at the node's parcels,
or within the ring for far-ranging kinds, with meat or rotting meat left; buried ones only if shallow, §5). Its attraction is the
row's `attr` times the carcass's mass (calibrate). Rows are added to kinds that scavenge: the fox (any stage; small and medium most),
the wolf (fresh and rotting; ranges far), the boar (rotting), the bear (fresh; it caches, below). A group that comes eats a share of
the mass (its size times a rate, calibrate), leaves its traces at the parcel (as raids do), and is remembered as having fed there
(`found`, as now).

**The rest, through the carrion pool.** Each night a carcass's remaining mass is added to its area's carrion in the ecology's step
(`wild/ecology.py`), and what the ecology's carrion eaters eat there is drawn back off the carcasses of that area in proportion. The
ravens' existing sign over carrion then shows over a real carcass; a raven's sign at the parcel (seen from far: the carcass's
conspicuousness is raised while birds are over it) leads people and wolves alike.

**Spillover.** A group that fed at a carcass at a node has, for some nights after (calibrate: 3), a raised drive there (x1.5) and may
pick any of its target rows at that node, not only the carcass: so the fox that came to the dead calf tries the hen-house beside
it, and wolves that fed at a carcass near the fold come to the fold. No new rule: the drive and the target choice of `_groups`,
read with a `fed_at` memory.

**The bear's cache.** The bear's row on fresh carcasses marks the carcass `cached` while the bear lies near (2 to 4 nights,
calibrate). Anyone who takes from or works at that parcel in those days meets it: the existing danger rule (D2-193) with the bear's
`danger`, more if alone. Its signs: the carcass half-covered with earth and leaves; an expert reads that a bear lies up near.

## 4. People's handling

Each is an existing act, or an existing act on a carcass:
- **Taking the meat and hide** (the existing `take` from a thing at a place, D4-70): while fresh, the meat is food; rotting meat is
  not (it can be given to dogs later, K6). Taking leaves a smaller mass (offal and bones) that still draws small scavengers for a day
  or two.
- **Butchering** a beast that has just died is the same take, done promptly.
- **Burning** a carcass: a new method row `burn` (work, at a carcass, uses firewood by the carcass's size, units by size; calibrate)
  removes its mass; the smoke is a sign. A cost borne for what does not come.
- **Burying** a carcass or a body: the existing burial (`_bury`, units by the ground and the cold, D2-96, `grave_left`). A grave dug
  to its full units is **deep**: no group's target and nothing to the carrion pool. A grave not finished, or dug in frozen or stony
  ground at fewer units, is **shallow**: diggers (the fox, the wolf; badgers and dogs when they exist) find it with a small chance a
  night (calibrate: about a tenth of what an open carcass draws), and a dug grave's signs are what is left. Bodies follow the same
  rule (D2-4: what is found of a body unburied or badly buried is told by its signs).
- **Leaving it** is the default and the cost (§3).

## 5. Tallow and light

- **Tallow** (an ITEMS good: weight, no food, keeps): a slaughter yields it by beast (calibrate: a cow 4, a pig 3, a sheep 1), and a
  fresh carcass holds it as it holds the hide. The existing slaughter `gives` gains it.
- **A tallow light** (a `make` recipe: 1 tallow and 1 unit for 4 lights, calibrate): carried, it lets night work be done by light. The
  wild layer's one-off "by lantern" texts (02zq) read it: night `pest work` and a night `guard` use a light if the person has one
  (otherwise as now, by moonlight or a fire). The night watch's own fire is unchanged (D2-21).
- Rendering, glue, bone, sinew and candles in moulds wait for K8.

## 6. Touches in 37.4's files

- `night.py`: the carcass's rotting meat lost by size, season and frost (§2); the spoilage loop is otherwise unchanged.
- `data.py`: THINGS gains the size rows; ITEMS gains `tallow` and `tallow light`; TECHNIQUES gains `burn` and the light recipe;
  slaughter's `gives` gains tallow.
- `verbs.py`: a grave's depth (deep or shallow) recorded from `_bury`'s units against the grave's need.
- `signs.py`: the carcass context gains `birds over` (ravens or kites at the parcel), `cached` and `dug`.

## 7. Tests (the gate)

- Unit: a carcass's stages by size (a hen gone in two days, a cow lasting about ten), faster in summer, stalled by frost; a fox
  group raids a carcass target and eats mass; carcass mass enters the area's carrion and ravens show over it; spillover (a fox fed
  at a carcass by a hen-house tries the hens in the next nights more than one that did not); the bear's cache (taking at a cached
  carcass meets the bear); burning removes the carcass; a deep grave draws nothing, a shallow one is sometimes dug; tallow from a
  slaughter; a tallow light lets night pest work be done.
- Society-level (dry, scripted): a dead cow left by the fold raises the fold's losses over the next nights against one burned or
  buried; leaving bodies unburied draws scavengers where burying them does not.
- Regression: the wild-pack worlds `cybertron2/specs/wild_probe5.json` and `wild_probe6.json` on branch `ecology` (runs 5 and 6's generated villages), run with scripted bots (`run.run(spec, out, days=8, bots=True)`); total carrion eaten and the carrion eaters' numbers within about a third of before (the carcass
  link adds food, so check the fox and the wolf do not boom; calibrate the attraction down if they do); all tests pass.
- **Gate:** the above, and a short dry-run report to Zach; then a small live run if he allows one, read against the pack off.

## Why

- Zach (9 Nov): carcasses, bodies and rotting food "don't just disappear, but are generally scavenged by creatures (tho I guess there
  should be some natural decay ...) so that stuff like butchering etc. has different effects"; stages "at least a few days" for soft
  remains, by size; "graves being dug up should be a lot less likely than if a body is left out"; predators drawn by bodies then
  attacking other things; and that everything be built from how the engine already works.
- 02zw §1 (C9, C10): carcasses, their ages, rotting meat, burial by units and the carrion pool exist; the link and the sizes are what
  is missing.

## Alternatives considered

- **A general decay-and-scavenging rule over all organic things with stages, a succession and senses** (02zu D.4): the engine's
  carcass ages, rotting meat and the carrion pool already carry it; the link through target rows and the pool is enough for now.
- **Spoiled stores and the midden as scavenging targets:** deferred (the kite and the midden, a later pack); rats already follow the
  harvest into stores.

## Open questions (for Zach)

1. ~~Bodies scavenged~~ decided: D2-205.
2. May 37.2 raise the touches in 37.4's files (§6) on the board?
3. The sizes and timings (§2): right as a first calibration?

## History

- 9 Nov 2026: written by 37.2 from 02zv's stage 4 and pack K2, built from how the engine already works (02zw), at Zach's request for
  briefs beyond stage 1; with his answers of 9 Nov on decay by size on the day's clock, graves, and spillover.

## Sources

docs/review/37_growth/02zw_wild_engine_comparison.md, 02zv_wild_consolidation.md (C9, C10, K2), 02zu_wild_chains_capital_actions.md
Part D; proposals/carcasses.md, graves.md, things_in_places.md; branch `ecology`: `engine/things.py`, `night.py`, `signs.py`,
`verbs.py`, `data.py`, `wild.py`, `wild/ecology.py`; D2-4, D2-21, D2-85, D2-96, D2-193, D2-199, D4-23, D4-52, D4-70, D4-99, D4-109.
- 9 Nov 2026: Zach decided D2-205, D2-207 (bodies scavenged: yes; the cat by itself or found; one small live run after brief 2's gate) and asked for the briefs to be built; open points take the briefs' defaults.
