# Raiders, displacement and set works: what every village meets

**Status:** accepted: D2-206, D2-207 (9 Nov); to be built after brief 1's gate. **Build brief 2 of 3** for the wild layer's core:
stages 2 and 3 and pack K1 (docs/review/37_growth/02zv_wild_consolidation.md, as corrected against the engine by
02zw_wild_engine_comparison.md). It starts only after brief 1 ([methods_and_encounters.md](methods_and_encounters.md)) has passed
its gate.
**Owner:** 37.2 (author; the wild pack's data and `engine/wild.py`, D2-199). Two touches fall in 37.4's files (§6: `things.py` for a
new kind of thing, `herds.py` for a herd's straying on a gadding day): they need 37.4's agreement on the board.
**Affects:** spec/environment/wildlife.md; on branch `ecology`: `engine/wild.py` (`_groups`, `_targets`, `_raid`, `shut`, `watch`,
`_sites_night`, `_loads`), `engine/data.py` (RESOURCES `near_people` and `taken.traits`, FITTINGS, THINGS), `wild/kinds.py`
(KINDS, LOADS, STORE_KEEP, MARKERS, SITES), `wild/ecology.py` (a new kind), `engine/things.py`, `engine/herds.py`.

## Summary

The engine already has raiders: groups of red deer, boar, foxes and wolves that come out of the ring on a drive, leave traces at
the edge, raid a field, a herd or a store unless a fence, a watch at the gap or a scare turns them, learn by the kind of scare
(D2-198) and remember where they fed (`wild._groups`). This brief extends that machinery, without a new system, so that what every
village meets behaves as it does in life: **a turned raider goes to the next field** (the neighbour's problem becomes everyone's);
**a fox tries the hamlet's doors and feeds at the first left open**; **birds at the corn become a flock that watches and clappers act
on**; **a snare or an eel trap can be set and left**, catching in the night for whoever comes; **doors, stores and fences stop what
their gaps and heights stop**, by the kind's size; and a handful of new kinds and fittings that every village has (the stoat, the
cat, the owl hole, moles, the rooks' grubs, cattle gadding in the heat) enter as data on these rules.

## 1. For the builder

**This file holds for this stage.** Read: brief 1 and its tests (they must pass); 02zw §1 (C5, C6, C7) and §2; on branch `ecology`:
`engine/wild.py` `_groups` (the raid loop: positions home, edge, ready; `_answer`, `_fenced`, `_raid`, `_trace`), `_targets`,
`shut`, `watch`, `_sites_night`, `_loads`, `_follow_harvest`, `_stores`; `wild/kinds.py` (STORE_KEEP, FOLLOW_HARVEST, LOADS, SITES,
MARKERS); `wild/ecology.py` (movement, refill); `engine/things.py` (piles and the noticing rule); `docs/cybertron2/guides/senses.md`.
**Do not** add institutions, cap signs, convert acts into real days, or name kinds in rule code (kinds' behaviour is data on their
rows; D2-203 modules only where data cannot express it, and none is needed here). Dry runs only.
**Branch:** `ecology-raiders`, from brief 1's branch.

## 2. Stage 2: displacement and the lapse probe (C6)

What exists: refill (the ecology moves populations toward better land along links, so an emptied area fills; pressure makes hunted
kinds leave and return, `HUNTED`). What changes, in `_groups`:

**Displacement.** A kind's `near_people` row gains `displace` (true or false). When a group with `displace: true` is turned at its
target (a scare, a fence, a watch at the gap), it tries **one more target the same night**: the next target of the same row at the
node that is not watched tonight and not the one it was turned from, preferring the nearest by parcel steps from the edge it came
out of. If that one is open, it raids it (`_raid`, as now) and leaves its traces there; its memory (`found`, `target`) moves to the
new target. Kinds with `displace: false` rest as now (the fox and wolf, scared off for days). Set `displace: true` for boar, red deer
and the woodpigeon flock (§3).

**The lapse probe.** For rows whose target is `items` or `hens` (the fox now; the stoat, §5), a row may carry `probe: k`. The group
tries up to `k` of the node's matching buildings in a keyed order each raid night, starting with the one it fed at last
(`found`/`target`), and raids the first one it can enter (§4: not shut against its size, no dog fitting); if none, it is "tried" at
each (the trace exists). Because the remembered target comes first, a household that left its hens open brings the fox back, and
its neighbours are tried on the way. Set `probe: 3` for the fox.

Nothing else in `_groups` changes. Refill needs nothing.

## 3. Birds at the corn as a flock

Today woodpigeons eat crops only as a density in the ecology's diet (no group, so no watch or clapper acts on them); rooks pull corn
from the rookery's site, stopped by any watch on the field (`watch_stops`). Change:
- **Woodpigeon gains a `near_people` row** (data, as red deer have): targets `crop` in sowing and young-corn seasons, and greens and
  winter corn when the mast fails (the existing `WHEN` vocabulary: `mast: low`); `answer: habituate` with a fast decay (a still
  scare is soon a post: D2-198), `displace: true`; group size from the flock (calibrate); its share of crops through the ecology's
  diet near home is cut by the same amount, so the total is not counted twice (calibrate on the wild_year probes).
- **"Lands where others feed"** is the flock's choice of target: it picks the field it fed at last if that field still has the crop
  (its memory, as now), else the field with the most of its crop; a displaced flock lands on the next field of the same crop (§2).
- The rookery stays as it is (it already works and answers any watch).

## 4. Stage 3: set works, and barriers and stores by size (C7)

**Set works.** A method row may carry `set: true` (stage 3: `snare` and `trap in water`). Doing it costs its units today and leaves a
thing at the parcel: a new kind of thing, `set` (things.py `KINDS`, 37.4's file), holding the method, the setter, the day set, its
`life` in nights (calibrate: snares 4, eel traps 8) and its catch (goods, empty at first). Each night (in `wild.night`, after the
groups), each set thing draws once by `take`'s rule against the kinds in its parcel's area, with the method's table, the setter's
method skill and familiarity, and a lower base chance than a person present (calibrate); a catch goes into the thing as goods (the
kind's `taken.goods`). Then:
- **Checking** is the existing `take` from a thing at a place (a search, D4-70): whoever finds it and takes the catch has it;
  possession is whoever takes (D4-23). The setter knows where it is; others find it by the noticing rule (a set thing is hidden:
  low conspicuousness, calibrate), so a neighbour may rob a snare line, and it is seen and remembered as using what others hold.
- **Lifting** it is taking the thing itself back. When its life runs out it is gone (a sprung, rotten snare).
- A catch left unchecked spoils as the item does (meat's `spoil`), and from brief 3 it is a carcass that draws scavengers.
- Eel traps no longer resolve inside the act: they are set at dusk and hold the night's catch (the eel night's `when` rows apply to
  the night they fish).

**Barriers and stores by size.** Kinds gain a trait `gap` (the smallest gap they pass: tiny for mice and rats, small for a stoat or
weasel, medium for a fox, large for a dog or wolf) and `climbs` (true for rats and mice, the stoat). Then, with no new system:
- **A shut door** (`wild.shut`) keeps out kinds whose `gap` is larger than the building's own gaps: a building's gaps follow its
  structure and condition (wattle and timber `small`, stone `tiny`; a damaged building one size larger; calibrate). So a shut wattle
  hen-house stops the fox and not the stoat; a mended stone one stops both; rats and mice are stopped by neither.
- **Stores** (`STORE_KEEP`) gain rows by property: a `granary` fitting (raised on staddles) cuts what kinds with `climbs: true` and
  `gap: tiny` take (rats, mice) by its keep (calibrate); `bins` cut mice; the dog fitting as now; the cat (§5).
- **Fences** keep their levels and `through`; a kind's `gap` and size join the existing leaping rule (a stoat passes any fence;
  a hare a wattle one).

## 5. Pack K1: the kinds and fittings every village meets

Each is data on the rules above unless said.

| Item | What exists | What to add | Test |
|---|---|---|---|
| **boar and red deer at the field** | groups, gaps, fences, scares (built) | `displace: true`; calibrate boar's unwatched loss to about 3 to 10% of need in a wooded village (02zr) | a watched field's loss moves to the unwatched neighbour |
| **the fox** | raids hens and stores; `shut`; refill | `probe: 3` (§2); winter dispersal's faster refill is the ecology's (check) | one lax house raises its neighbours' tries and its own losses |
| **birds at the corn** | rooks (site); pigeons as a density | the woodpigeon row (§3) | clappers turn the flock for a few nights, then it habituates; a displaced flock lands next door |
| **stoat and weasel** | none | a kind: RESOURCES and ecology KINDS rows (in the ring; diet voles, rabbits when they exist, eggs, hens), `gap: small`, `climbs: true`, `near_people` targets `hens` (`probe: 3`, `answer: scared_off`), `taken.goods: hide` (ermine in winter, a goods quality later) | a shut wattle hen-house loses hens to the stoat and not the fox; mending it (stone or repair) stops both |
| **the cat** | the dog fitting halves store loss (`STORE_KEEP`) | a fitting `cat` (no one builds it; D2-206): each season a building with a store and mice in its area gains a cat with a keyed chance, unless it has a dog; or a person working near the village finds a stray (a find, keyed) and may bring it to a building they may use; it keeps tiny kinds off that store (STORE_KEEP cat, calibrate) and leaves if the store is empty for a season | a barn with a cat loses less to mice and rats; a dog keeps cats away |
| **the owl hole** | owls are a kind | a fitting `owl hole` built in a barn (a build like other fittings, timber and a unit); a barn owl takes it with a keyed chance in spring if no one worked in that building at night; mice in that building's store fall by a share | a barn with an owl loses less to mice |
| **moles** | loads (slugs, aphids, ladybirds, fungi) | a load `moles` on meadow and pasture (wet spring and autumn raise it); its harm is a cut of hay from that parcel at mowing; `pest work` answers it (the load's row: trapped in its runs, a cut for some days) | an untended meadow gives less hay in a mole year; one worked by someone familiar with moles loses little |
| **the rooks' grubs** | the rookery's site and corn pulls | a load `grubs` (leatherjackets) on fields and pasture, raised by a wet autumn; the rookery's birds lower it on parcels within reach of the site each night (a share, calibrate); taking many young (gather young) or felling the rookery's wood lowers that share | a parcel near a rookery has fewer grubs; a rookery destroyed raises grub harm in its radius the next season |
| **markers with a lever** | markers built as signs; sowing lore names windows (D4-114) | each marker sign gains, for those with family lore, the saying it times ("the blackthorn's in flower: sow the barley") from the lore's windows; markers that time nothing stay as they are | a marker shown names a sowing window that the crop model rewards |
| **cattle gadding in the heat** | herds stray unwatched; trampling; fences | a condition row: on a hot, still summer day (the climate's temperature and wind, D4-109) a herd on open pasture without water or a wood in its parcel or next door strays with a raised chance through its fence into a neighbour's crop (`herds.py`, 37.4's file) | on such days unwatched herds stray more; a herd by water or shade does not |

## 6. Touches in 37.4's files

- `things.py`: a kind of thing `set` (§4), noticed by the existing rule.
- `herds.py`: the gadding condition raises the straying chance (§5).
Both are small and keep the files' rules; they need agreement on the board.

## 7. Tests (the gate)

- Unit: displacement (a turned group raids the unwatched next target the same night; a `displace: false` group rests); the lapse
  probe (the first open building is raided; the remembered one is tried first); the flock row (habituation over nights; landing
  where it fed); set works (a set snare catches with no one present, holds the catch, can be robbed by another person who finds it,
  ends after its life; eel traps fish the night they are set); doors by gap (fox, stoat, rats against wattle, stone, damaged); stores
  by property; each K1 item's test above.
- Guard: no kind name in rule code (all in data rows); every new sign follows the senses guide (a change, grounded, worth acting on).
- Regression: the wild_year probes on fixed seeds: total wild losses per household-season within about a third of before except where
  this brief means them to move (boar down to its target; pigeon losses now answerable); all tests pass.
- Society-level (dry, scripted): two neighbouring fields, one watched and one not: the unwatched loses more than if neither were
  watched; a hamlet with one lax house loses more hens in its other houses than a hamlet with none.
- **Gate to brief 3:** the above, a short dry-run report to Zach, and, if he allows one, a small live run (17 agents, 8 days, about
  $10) on a generated village with a wood, read against the pack off.

## Why

- Zach (9 Nov): general methods used in a specific way, not one action per animal; nothing social forced (a rota or a by-law is the
  agents' to make; the engine only makes the neighbour's loss real); everything built from how the engine already works.
- 02zr §1.2 and M3 (displacement is the cheapest route to a shared problem); 02zs §5 (stores and barriers at scale); 02zw §1 (C5, C6,
  C7: the raid loop, refill, fences and stores exist; the set trap and size-read gaps are the small additions).

## Alternatives considered

- **A new animal interface with alarm, follow, probe and cache** (02zr §3.2): not needed for these; the raid loop expresses
  displacement and probing as rules over target rows.
- **Standing works as a general system with capacity and depreciation** (02zu B.4): fences, stores and wear exist; only the set trap
  is new.
- **Shared perception through a reverse noticing rule** (02zr M1): deferred; it needs a wind direction and refines what exists.

## Open questions (for Zach)

1. Displacement on the same night (as here, the default under D2-207) or the next night?
2. ~~The cat~~ decided: D2-206 (by itself, or found and brought).
3. May 37.2 raise the two touches in 37.4's files (§6) on the board?

## History

- 9 Nov 2026: written by 37.2 from 02zv's stages 2 and 3 and pack K1, built from how the engine already works (02zw), at Zach's request
  for briefs beyond stage 1.

## Sources

docs/review/37_growth/02zw_wild_engine_comparison.md, 02zv_wild_consolidation.md (C5 to C7, K1), 02zr_wild_behaviour_critique.md §1.2,
§4.1, §4.5, §4.8, §4.12, M3, §6 nos. 1, 9, 14, 15, 22, 39; branch `ecology`: `engine/wild.py`, `engine/data.py`, `wild/kinds.py`,
`wild/ecology.py`, `engine/things.py`, `engine/herds.py`; D2-21, D2-123, D2-198, D2-199, D2-203, D4-23, D4-70, D4-109, D4-114.
- 9 Nov 2026: Zach decided D2-206, D2-207 (bodies scavenged: yes; the cat by itself or found; one small live run after brief 2's gate) and asked for the briefs to be built; open points take the briefs' defaults.
